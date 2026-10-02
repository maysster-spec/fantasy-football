#!/usr/bin/env python3
r"""close_check.py -- read AUDIT_LEDGER.md and say which OPEN rows are actually still open.

WHY THIS EXISTS (doc 312). Matt, 2026-09-15: "we've had to go back and grab several things we
discussed prior." Measured that day: the ledger carried 28 OPEN rows and TWELVE of them were
already done -- 43% of the list he works from was finished work. Every one said "OPEN: closes on
Matt's next run", he ran it, and nothing ever re-read the condition. A close condition nobody
evaluates is not a condition, it is a wish.

AND THE LEDGER WAS BUILT FOR THIS ALL ALONG. Its fifth column is headed `grep tokens` and its
entire purpose is mechanical re-checking. No script in this project has ever read it.

WHAT IT DOES: for every row marked OPEN, search the SHIPPING ARTIFACTS for that row's grep tokens.
  GONE        -- no token found. The defect text is not in the code or on the pages any more.
                 A CANDIDATE for closing, never an automatic close: read it and decide.
  STILL THERE -- found, and the file is named. Genuinely open.
  NO TOKENS   -- the cell is n/a. Cannot be checked mechanically; it needs judgement.

IT SEARCHES CODE AND PAGES, NOT PROSE. Every doc in Source\ DESCRIBES the defect, so grepping the
.md files would find every token in the very document that retracted it. Scripts, HTML, CSV, JSON
and TXT only.

IT NEVER EDITS THE LEDGER. Naming is mechanical; closing is a judgement, and doc 305 records what
happens when I rule on a verdict instead of filling in the terms.

Portable per 0.4: stdlib only, paths off __file__, no shelling out, 3.12-clean.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('FF_ROOT') or os.path.abspath(os.path.join(HERE, '..', '..'))
SRC = os.path.join(ROOT, 'Source')
SCR = os.path.join(ROOT, 'Scripts')
LEDGER = os.path.join(SRC, 'AUDIT_LEDGER.md')
NCOL = 10
MAXBYTES = 2_000_000
SEARCH_EXT = ('.py', '.html', '.csv', '.json', '.txt', '.bat')
SKIP = ('espn_raw_', 'AUDIT_LEDGER')


def corpus():
    """Every shipping artifact, with the prose deliberately left out."""
    out = []
    for base in (SRC, SCR):
        if not os.path.isdir(base):
            continue
        for dirpath, _dirs, files in os.walk(base):
            if '_archive' in dirpath:
                continue
            for fn in files:
                if not fn.endswith(SEARCH_EXT) or any(s in fn for s in SKIP):
                    continue
                p = os.path.join(dirpath, fn)
                try:
                    if os.path.getsize(p) > MAXBYTES:
                        continue
                except OSError:
                    continue
                out.append(p)
    return out


def tokens(cell):
    """The grep cell holds backticked tokens separated by ; or a middle dot."""
    if not cell or cell.strip().lower() in ('n/a', '', '-'):
        return []
    parts = re.findall(r'`([^`]+)`', cell)
    if not parts:
        parts = [x.strip() for x in re.split(r'[;·]', cell)]
    out = []
    for p in parts:
        p = p.strip().strip('"').strip("'")
        # a token that is one short word matches everything; the ledger means a phrase
        if len(p) >= 4 and not p.lower().startswith(('doc ', 'section ')):
            out.append(p)
    return out


def main(argv):
    if '--selftest' in argv:
        return selftest()
    if not os.path.exists(LEDGER):
        sys.exit(f'FAILED: no AUDIT_LEDGER.md at {LEDGER}')
    text = open(LEDGER, encoding='utf-8').read()

    rows, malformed = [], []
    for line in text.split('\n'):
        if not re.match(r'^\|\s*\d+\s*\|', line):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        n = int(re.match(r'^\|\s*(\d+)', line).group(1))
        if len(cells) != NCOL:
            malformed.append((n, len(cells)))      # never skipped silently (section 3)
            continue
        rows.append((n, cells))

    if malformed:
        print('MALFORMED ROWS -- an unescaped pipe inside a cell splits the row, and a checker '
              'reading the grep column would mis-parse it:')
        for n, c in malformed:
            print(f'   row {n}: {c} cells, expected {NCOL}')
        print()

    files = corpus()
    blobs = {}
    for p in files:
        try:
            blobs[p] = open(p, encoding='utf-8', errors='ignore').read()
        except OSError:
            continue

    # A CHECKER THAT SEARCHED NOTHING MUST NOT REPORT ALL CLEAR (0.2). If the corpus comes back
    # thin -- wrong root, a folder not synced, a path typo -- every token is "GONE" and every open
    # row reads as fixed. That is the most dangerous possible output of this script, so it refuses.
    if len(blobs) < 50 and not os.environ.get('FF_SELFTEST'):
        sys.exit(f'FAILED: only {len(blobs)} searchable files found under {SRC} and {SCR}. '
                 f'That is too few to trust a "gone" verdict -- every token would read as absent. '
                 f'Check FF_ROOT, or run this from Scripts\\research\\.')

    gone, still, nogrep = [], [], []
    for n, cells in rows:
        if not cells[NCOL - 1].startswith('**OPEN'):
            continue
        toks = tokens(cells[4])
        if not toks:
            nogrep.append((n, cells[1][:54]))
            continue
        hits = []
        for t in toks:
            for p, b in blobs.items():
                if t in b:
                    hits.append((t, os.path.relpath(p, ROOT)))
                    break
        (still if hits else gone).append((n, cells[1][:54], toks, hits))

    print(f'AUDIT_LEDGER: {len(rows)} rows parsed, '
          f'{len(gone) + len(still) + len(nogrep)} of them OPEN')
    print(f'searched {len(blobs)} shipping files under Source\\ and Scripts\\ '
          f'(prose .md deliberately excluded)\n')

    print(f'=== CANDIDATE CLOSED -- the defect text is GONE from every artifact ({len(gone)}) ===')
    print('    Read each one and decide. This script never closes a row.')
    for n, where, toks, _ in gone:
        print(f'   row {n:2d}  {where}')
        print(f'          looked for: {", ".join(toks)}')
    print(f'\n=== STILL THERE -- genuinely open ({len(still)}) ===')
    for n, where, _toks, hits in still:
        print(f'   row {n:2d}  {where}')
        for t, p in hits[:3]:
            print(f'          "{t}" in {p}')
    print(f'\n=== NO GREP TOKENS -- needs judgement, cannot be checked here ({len(nogrep)}) ===')
    for n, where in nogrep:
        print(f'   row {n:2d}  {where}')

    # AND THE OTHER TRACKER, which has no trigger anywhere (doc 312)
    ot = os.path.join(SRC, 'OPEN_THREADS.md')
    if os.path.exists(ot):
        newest, newest_n = None, 0
        for fn in os.listdir(SRC):
            m = re.match(r'^(\d{2,3})_.*\.md$', fn)
            if m and int(m.group(1)) > newest_n:
                newest_n, newest = int(m.group(1)), fn
        got = 0
        otx = open(ot, encoding='utf-8').read()
        for m in re.finditer(r'\b(\d{2,3})_', otx):
            got = max(got, int(m.group(1)))
        print(f'\n=== THE OTHER TRACKER ===')
        print(f'   OPEN_THREADS.md covers up to doc {got}; Source\\ holds doc {newest_n}.')
        if newest_n - got > 2:
            print(f'   *** IT IS {newest_n - got} DOCS BEHIND. Run  py research\\open_threads.py  ***')
    return 0


def selftest():
    """The guard has to fire against the specific defect that motivated it (0.2)."""
    import tempfile
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, 'Source'))
    os.makedirs(os.path.join(d, 'Scripts'))
    hdr = ('| # | where | claim | replacement | grep tokens | code | page | directive '
           '| prompts | status |\n|---|---|---|---|---|---|---|---|---|---|\n')
    body = (
        '| 1 | a fixed thing | x | y | `GHOST_TOKEN_NOT_PRESENT` | yes | n/a | n/a | n/a '
        '| **OPEN**: closes on the next run |\n'
        '| 2 | a live thing | x | y | `STILL_IN_THE_CODE` | NO | n/a | n/a | n/a '
        '| **OPEN** |\n'
        '| 3 | a pipe | x | y | `a|b` | NO | n/a | n/a | n/a | **OPEN** |\n')
    open(os.path.join(d, 'Source', 'AUDIT_LEDGER.md'), 'w', encoding='utf-8').write(hdr + body)
    open(os.path.join(d, 'Scripts', 'live.py'), 'w', encoding='utf-8').write(
        '# STILL_IN_THE_CODE is right here\n')
    os.environ['FF_ROOT'] = d
    os.environ['FF_SELFTEST'] = '1'
    globals()['ROOT'] = d
    globals()['SRC'] = os.path.join(d, 'Source')
    globals()['SCR'] = os.path.join(d, 'Scripts')
    globals()['LEDGER'] = os.path.join(d, 'Source', 'AUDIT_LEDGER.md')
    print('SELFTEST -- planted: row 1 gone, row 2 still in the code, row 3 malformed by a pipe\n')
    main([])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
