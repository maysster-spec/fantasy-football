#!/usr/bin/env python3
r"""
check_plain.py -- refuse to let the PAPER talk like the DOCS.

WHY THIS EXISTS (doc 208, Matt, 2026-09-06):
    "somehow that refinement gets left out in the word construction phase... seems overly technical
     and causes more confusion than clarification when the goal is the opposite. not sure if that
     can be addressed going forward since a repeated issue by my humble measure"

He is right that it repeats, and the cause is not style. It is that two rules in the directive
collide and only one of them has teeth:

  * s0.2 and s3 REQUIRE provenance -- baseline, population, sample size, a doc number, a tag.
    Specific, mandatory, and checked by `audit_directive.py`.
  * s0.1 asks for plain English with no jargon. General, aspirational, and checked by nobody.

When both apply to one sentence the specific mandatory rule wins, every time, and a key line comes
out reading "the only names s7 ranks at pick 32, in dollars over 100 board states (N=2,000)".
That is correct for a DOC and wrong for a SHEET he reads at 60 seconds a pick.

THE SCOPE RULE THIS ENFORCES:
    Provenance belongs in `Source\*.md`. A PRINTED page carries the instruction and the plain
    number, and nothing else. Same fact, two registers, chosen by who is reading.

Stdlib only (s0.4): no pandas, no network, no shelling out. Exits 1 if any printed page carries
doc-voice, so it can gate a build; run with --warn to report without failing.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'Source')

# Every page Matt actually reads. DRAFT_CARD and DRAFT_DAY_GUIDE are excluded for the same reason
# to_pdf excludes them -- they are not rebuilt, so flagging them would cry wolf every run.
PAGES = ['ADP_GRID.html', 'BOARD_GRID.html', 'TIER_SHEET.html',
         'DRAFT_BOARD.html', 'VALUE_LADDER.html', 'HOW_TO_READ_IT.html',
         'FALLBACK_BOARD.html', 'OVERRIDE_CARD.html',
         # the in-season pages the scheduler builds. They were missing: the draft is over and
         # these are now the only pages Matt reads, so the guard was watching an empty room.
         'THE_WEEKLY_WIRE.html', 'LINEUP_CHECK.html',
         # and the week sheet, rebuilt by wire.py since 10 Sept and never on this list (doc 291, D7).
         'WEEK_SHEET.html']

# What doc-voice looks like. Each is a thing that belongs in a doc and never on paper.
BANNED = [
    (r'&sect;\s*\d|§\s*\d',              'a directive section number'),
    (r'\bdoc\s+\d+',                     'a doc number'),
    (r'\bp\s*=\s*0?\.\d|p&lt;|p\s*<\s*0?\.\d', 'a p-value'),
    (r'\bn\s*=\s*\d|\bN\s*=\s*[\d,]+',   'a sample size'),
    (r'\brho\b(?![a-z])|\br\s*=\s*[+-]?0?\.\d', 'a correlation coefficient'),
    (r'\bCI\b|confidence interval',      'a confidence interval'),
    (r'\bVBD\b',                         'VBD (the paper says VOR)'),
    (r'\bbootstrap\b|\bquartile\b|\bregress',   'statistics vocabulary'),
    (r'\beff_pick\b|\badp_pick\b|\bproj_leaguepts\b|\broll\b(?![a-z])', 'an internal column name'),
]

def visible(html):
    """Text a reader can actually see: drop <style>, <script> and every tag."""
    html = re.sub(r'(?is)<style.*?</style>', ' ', html)
    html = re.sub(r'(?is)<script.*?</script>', ' ', html)
    html = re.sub(r'(?s)<!--.*?-->', ' ', html)
    html = re.sub(r'(?s)<[^>]+>', ' ', html)
    return re.sub(r'\s+', ' ', html)

def scan(text):
    out = []
    for pat, why in BANNED:
        for m in re.finditer(pat, text):
            a = max(0, m.start() - 55)
            out.append((why, m.group(0).strip(), text[a:m.start() + 60].strip()))
    return out

def main():
    warn = '--warn' in sys.argv
    if '--selftest' in sys.argv:
        # s0.2: a guard that has never been executed is not a guard. Run it against the exact
        # sentence Matt quoted back, which is the defect that motivated the file.
        bad = ('the only names &sect;7 ranks at pick 32, in dollars over 100 board states '
               '(N=2,000): spread across all five is $2.7')
        hits = scan(bad)
        print('SELFTEST on the line Matt quoted:')
        for why, tok, ctx in hits:
            print('   caught %-28s %r' % (why, tok))
        good = 'One of the five worth taking at pick 32. Take whichever shows first.'
        print('SELFTEST on its replacement: %d hits' % len(scan(good)))
        ok = len(hits) >= 2 and len(scan(good)) == 0
        print('SELFTEST %s' % ('PASS' if ok else 'FAIL'))
        return 0 if ok else 1

    total, seen = 0, 0
    for name in PAGES:
        path = os.path.join(SRC, name)
        if not os.path.exists(path):
            continue
        seen += 1
        with open(path, encoding='utf-8', errors='replace') as f:
            hits = scan(visible(f.read()))
        if hits:
            total += len(hits)
            print('  %-22s %d' % (name, len(hits)))
            for why, tok, ctx in hits[:6]:
                print('       %-28s ...%s...' % (why, ctx[-72:]))
            if len(hits) > 6:
                print('       ... and %d more' % (len(hits) - 6))
        else:
            print('  %-22s clean' % name)
    if not seen:
        print('  !! no pages found in %s -- nothing was checked' % SRC)
        return 1
    if total:
        print('\n  %d line(s) of doc-voice on paper. Provenance goes in Source\\*.md;' % total)
        print('  the printed page carries the instruction and the plain number.')
        return 0 if warn else 1
    print('\n  %d pages, no doc-voice on any of them.' % seen)
    return 0

if __name__ == '__main__':
    sys.exit(main())
