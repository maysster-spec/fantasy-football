#!/usr/bin/env python3
r"""
open_threads.py -- BUILD THE LIST OF WHAT WE DROPPED, FROM THE DOCS THEMSELVES.

    py open_threads.py              look; print the list and write OPEN_THREADS.md
    py open_threads.py --quiet      write the file, print only the counts
    py open_threads.py --selftest   prove the scanner fires (SECTION 0.2)

WRITES:  Source\OPEN_THREADS.md

WHY THIS EXISTS
    SECTION 0.5(e) says: "At the end of any session that produced more than one doc, list the
    open threads BY NAME in the final reply." It has been obeyed -- into a chat window that
    scrolls away. Matt, 2026-09-09: "I keep missing stuff I need to do."

    A reply is not a tracker. And a HAND-MAINTAINED list is not one either: SECTION 9 already
    records that every prose file map in this project went stale within hours and that the
    checker is the map. So this does not ask anyone to maintain a list. It READS THE DOCS,
    which are written under SECTION 0.5(a4) and already carry the markers:

        NOT YET RUN . BLOCKED . [OPEN] . STILL UNTESTED . UNRESOLVED . post-draft . queued

    Closing a thread: put a distinctive substring of it on its own line in
    Source\threads_closed.txt. Matched threads move to a CLOSED section -- they are NOT
    deleted, so a wrongly-closed one is still visible and can be un-closed.
"""
import argparse, os, re, sys, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
# Scripts\research\ -> 2026\Source\ ; also works if dropped in Scripts\ or Source\
def _find_source(start):
    d = start
    for _ in range(4):
        cand = os.path.join(d, 'Source')
        if os.path.isdir(cand):
            return cand
        if os.path.basename(d).lower() == 'source':
            return d
        d = os.path.dirname(d)
    return None

# TIER 1 -- the SECTION 0.5(a4) contract. These three are what I owe him for every
# mechanism, so a doc that declares one is declaring a real thread.
HARD = [
    ('NOT YET RUN', re.compile(r'NOT\s+YET\s+RUN', re.I)),
    ('BLOCKED',     re.compile(r'\bBLOCKED\b', re.I)),
    ('OPEN',        re.compile(r'\[\s*OPEN\s*\]', re.I)),
]
# TIER 2 -- softer language that USUALLY means deferred but often just describes one.
SOFT = [
    ('UNTESTED',   re.compile(r'STILL\s+UNTESTED|\bUNTESTED\b', re.I)),
    ('UNRESOLVED', re.compile(r'\bUNRESOLVED\b', re.I)),
    ('POST-DRAFT', re.compile(r'\bpost-?draft\b', re.I)),
    ('QUEUED',     re.compile(r'\bqueued\b', re.I)),
]

# THE FALSE-POSITIVE FILTER, AND IT IS THE WHOLE DIFFERENCE BETWEEN A TRACKER AND NOISE.
# Doc 263 alone produced NINE rows on a plain keyword scan -- six of them prose ABOUT being
# blocked ("Both are wrong. Neither was blocked."), which is not a thread. A list that is
# 60% noise trains you to skim it, which is the doc-97 failure check_kit already records.
# This project's docs declare a real thread in EMPHATIC position: bolded, bracketed, in a
# heading, or opening a bullet. Prose mentions are none of those.
EMPHATIC = re.compile(
    r'\*\*[^*]*(?:NOT\s+YET\s+RUN|BLOCKED|\[\s*OPEN\s*\])[^*]*\*\*'   # **BLOCKED, INPUTS NAMED:**
    r'|\[\s*OPEN\s*\]'                                                  # [OPEN]
    r'|^#{1,6}\s.*(?:NOT\s+YET\s+RUN|BLOCKED|OPEN)'                      # ## 6. OPEN, NAMED
    r'|^\s*[-*]\s+\*\*[^*]{0,40}(?:NOT\s+YET\s+RUN|BLOCKED)'            # - **BLOCKED** ...
    , re.I | re.M)

# WHOSE JOB IS IT. Matt, 2026-09-09, on the first version of this file: "that was a long
# file you provided. I'm not clear what i do tho." He is right and the defect is SECTION 0.4's:
# "Before any reply, re-read your do-this list and delete every item that is yours." A tracker
# that mixes the two hands him an inventory and calls it a to-do list.
#
# SECTION 0.4 fixes exactly four kinds of thing to Matt. Everything else is mine.
MATTS = re.compile(
    r'\bpy\s+\w+\.py'            # a command he runs
    r'|\.bat\b'
    r'|\bESPN\b.*\b(session|cookie|login|write|inject|prerank|lock)\b'
    r'|\bhis (machine|session|console|drive)\b'
    r'|\bonly Matt can\b'
    r'|\bbehind a login\b'
    , re.I)

DOCNUM = re.compile(r'^(\d+)_')
STRIP  = re.compile(r'[*_`~>#]+')

def clean(s, n=210):
    s = STRIP.sub('', s).strip()
    s = re.sub(r'\s+', ' ', s)
    return s if len(s) <= n else s[:n - 1] + '…'

def scan_text(text, label, sort_key):
    """lines that DECLARE a thread -- not every line that mentions one"""
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if len(line.strip()) < 12:
            continue
        hard = [n for n, rx in HARD if rx.search(line)]
        soft = [n for n, rx in SOFT if rx.search(line)]
        if hard and EMPHATIC.search(line):
            tier = 1
        elif hard or soft:
            tier = 2
        else:
            continue
        out.append({'doc': label, 'sort': sort_key, 'line': i, 'tier': tier,
                    'who': 'MATT' if MATTS.search(line) else 'ME',
                    'markers': (hard + soft) or ['?'], 'text': clean(line)})
    return out


def collect(src):
    rows = []
    for fn in sorted(os.listdir(src)):
        if not fn.lower().endswith('.md'):
            continue
        if fn.upper().startswith('OPEN_THREADS'):
            # [doc 435] never scan our own output: each run re-ingested the previous
            # OPEN_THREADS.md as a doc, nesting 42 garbage rows and growing the file by a
            # quarter per run (368 KB on 20 Sept, 460 KB after one more run).
            continue
        path = os.path.join(src, fn)
        try:
            text = open(path, encoding='utf-8', errors='replace').read()
        except OSError as exc:
            print(f"  could not read {fn}: {exc}")
            continue
        m = DOCNUM.match(fn)
        key = int(m.group(1)) if m else -1
        rows.extend(scan_text(text, fn[:-3], key))
    return rows

def load_todo(src, name='matt_todo.txt'):
    """Items born in a REPLY, which the doc scan can never see.
    Matt, 2026-09-09: "If you are waiting on me to run something then put it on my to-do list."

    [doc 430] AND THE SAME HOLE EXISTED ON MY SIDE, one level further in. 0.5(e) gave Matt's
    reply-items a home and left MINE with none: a thing I said in a reply that I would do myself
    went into no doc, so the scan above could not see it and no list held it. That is exactly the
    defect 0.5(e) was written to fix, reappearing in the mirror. Measured cost: I told Matt the
    online sheet would refresh every run, did not wire it, and it sat six days until he found it.
    Matt, 25 Sept: "if you do need to wait for me then shouldn't that go on my todo list so
    neither of us drop it?" Both sides now have a file and both render at the top.
    """
    p = os.path.join(src, name)
    if not os.path.exists(p):
        return [], []
    todo, done = [], []
    for ln in open(p, encoding='utf-8', errors='replace'):
        ln = ln.strip()
        if ln.startswith('[ ]'):
            todo.append(ln[3:].split('#')[0].strip())
        elif ln.lower().startswith('[x]'):
            done.append(ln[3:].split('#')[0].strip())
    return todo, done


def load_closed(src):
    p = os.path.join(src, 'threads_closed.txt')
    if not os.path.exists(p):
        return []
    pats = []
    for ln in open(p, encoding='utf-8', errors='replace'):
        ln = ln.strip()
        if ln and not ln.startswith('#'):
            pats.append(ln.lower())
    return pats

def render(rows, closed_pats, src, window=25):
    live, closed = [], []
    for r in rows:
        (closed if any(p in r['text'].lower() for p in closed_pats) else live).append(r)
    newest = max([r['sort'] for r in live], default=0)
    cutoff = newest - window

    directive = [r for r in live if r['doc'].startswith('00_PROJECT_DIRECTIVE')
                 and not r['doc'].endswith('_v4')]
    rest      = [r for r in live if r not in directive]
    hard_now  = [r for r in rest if r['tier'] == 1 and r['sort'] >= cutoff]
    hard_old  = [r for r in rest if r['tier'] == 1 and r['sort'] <  cutoff]
    soft_now  = [r for r in rest if r['tier'] == 2 and r['sort'] >= cutoff]
    for g in (directive, hard_now, hard_old, soft_now):
        g.sort(key=lambda r: (-r['sort'], r['line']))

    matt = [r for r in hard_now if r['who'] == 'MATT']
    mine = [r for r in hard_now if r['who'] == 'ME']

    todo, todo_done = load_todo(src)
    ctodo, ctodo_done = load_todo(src, 'claude_todo.txt')

    L = ['# OPEN THREADS', '']
    L.append('## WHAT MATT DOES')
    L.append('')
    if todo:
        L.append('**From the conversation** - these need his machine, his ESPN session or his '
                 'approval. Nothing else in this file is his.')
        L.append('')
        for t in todo:
            L.append(f"- [ ] {t}")
        L.append('')
    if todo_done:
        L.append('<sub>done: ' + ' · '.join(todo_done) + '</sub>')
        L.append('')
    if matt:
        L.append('These are the only ones that need his machine, his ESPN session, or his money '
                 '(SECTION 0.4). Everything below this block is mine to run and he does not have '
                 'to track it.')
        L.append('')
        for r in matt:
            L.append(f"- [ ] **{r['doc']}** - {r['text']}")
    elif not todo:
        L.append('**Nothing.** Every open thread below needs no command from him - they are all '
                 'mine to run (SECTION 0.4). He can read the rest or ignore it.')
    L.append('')
    if ctodo or ctodo_done:
        L.append('## WHAT I SAID I WOULD DO')
        L.append('')
        L.append('**From the conversation** - things I promised in a reply. The doc scan cannot '
                 'see a reply, so without this block they are held by nothing.')
        L.append('')
        for t in ctodo:
            L.append(f"- [ ] {t}")
        L.append('')
        if ctodo_done:
            L.append('<sub>done: ' + ' \u00b7 '.join(ctodo_done) + '</sub>')
            L.append('')
    L.append('---')
    L.append('')
    L.append(f"Generated {dt.datetime.now().strftime('%Y-%m-%d %H:%M')} by `open_threads.py` "
             "from the docs in `Source\\`. **Do not edit this file** -- every run overwrites it.")
    L.append('')
    L.append(f"Generated from {len({r['doc'] for r in rows})} docs. **{len(todo) + len(matt)} need Matt; "
             f"{len(mine) + len(ctodo)} are mine.** (Last {window} docs, {max(cutoff,0)}-{newest}. "
             f"{len(directive)} more in the directive, {len(hard_old)} older, {len(soft_now)} soft, "
             f"{len(closed)} closed - all reference, none of it his.)")
    L.append('')

    def block(title, note, items):
        if not items:
            return
        L.append('## ' + title)
        L.append('')
        if note:
            L.append(note)
            L.append('')
        cur = None
        for r in items:
            if r['doc'] != cur:
                cur = r['doc']
                L.append(f"### {cur}")
            L.append(f"- **{'/'.join(r['markers'])}** (line {r['line']}) - {r['text']}")
        L.append('')

    block('MINE TO RUN', 'Declared under SECTION 0.5(a4) - NOT YET RUN, BLOCKED with the '
                          'input named, or [OPEN]. Matt does not action these; they are the queue '
                          'for the next session. Newest doc first.',
          mine)
    block('THE DIRECTIVE\'S OWN LIST', 'The curated version. If one of these disagrees with a '
                                       'doc above, the doc is newer.', directive)
    block(f'OLDER THAN DOC {max(cutoff,0)}', 'Probably superseded - check before spending a '
                                             'session on one.', hard_old)
    block('SOFT - deferred language, not a formal declaration',
          'post-draft / queued / untested / unresolved, and some of these are just prose. '
          'Skim, do not work from.', soft_now)

    if closed:
        L.append('---')
        L.append('')
        L.append('## CLOSED')
        L.append('')
        L.append('Kept visible on purpose: a wrongly-closed thread is worse than an open one.')
        L.append('')
        for r in sorted(closed, key=lambda r: -r['sort']):
            L.append(f"- ~~{r['doc']} - {r['text']}~~")
        L.append('')
    return '\n'.join(L), len(hard_now), len(closed)


SELFTEST = """
# fake doc
This line is ordinary prose and must not be picked up at all.
**NOT YET RUN, with the inputs named:** the D/ST version of the hit rate.
Short.
The tight end draw is `[OPEN]` and must be settled before any tool is built.
Nothing here.
**BLOCKED, INPUTS NAMED:** Breakout Age needs a college receiving table.
"""

def selftest():
    rows = scan_text(SELFTEST, 'selftest', 999)
    got = {tuple(r['markers']) for r in rows}
    print(f"  selftest: {len(rows)} lines flagged out of {len(SELFTEST.splitlines())}")
    for r in rows:
        print(f"    {'/'.join(r['markers']):<14} {r['text'][:70]}")
    ok = len(rows) == 3 and ('NOT YET RUN',) in got and ('OPEN',) in got and ('BLOCKED',) in got
    # the negative control matters as much as the positive one
    neg = [r for r in rows if 'ordinary prose' in r['text'] or r['text'] == 'Short.']
    print(f"  negative control (plain prose NOT flagged): {'PASS' if not neg else 'FAIL'}")
    print(f"  positive control (all three markers found): {'PASS' if ok else 'FAIL'}")
    return 0 if (ok and not neg) else 1

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--quiet', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--source', help='override the Source folder')
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()

    src = a.source or _find_source(HERE)
    if not src or not os.path.isdir(src):
        sys.exit("  could not find the Source folder from %s -- pass --source" % HERE)

    rows = collect(src)
    if not rows:
        sys.exit("  scanned %s and found NO markers. That is not a clean bill of health, it is a\n"
                 "  broken scan -- this project's docs always carry some. Check the folder." % src)

    body, nlive, nclosed = render(rows, load_closed(src), src)
    out = os.path.join(src, 'OPEN_THREADS.md')
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write(body)

    # SECTION 0.2: verify the artifact, not the exit code.
    if not os.path.exists(out) or os.path.getsize(out) < 200:
        sys.exit("  *** OPEN_THREADS.md was not written, or is too small to be real.")

    if not a.quiet:
        print(body)
    print()
    print(f"  {nlive} open threads, {nclosed} closed -> {out} ({os.path.getsize(out):,} bytes)")
    return 0

if __name__ == '__main__':
    sys.exit(main())
