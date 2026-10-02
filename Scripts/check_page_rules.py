#!/usr/bin/env python3
r"""check_page_rules.py -- the standing rules a page states, read against the directive's (doc 450).

    py check_page_rules.py              the built pages in ..\Source
    py check_page_rules.py --selftest   the wire page as it stood on 29 Sept (Tuesday night) must fire; the fixed one must not

WHY THIS EXISTS. The wire page said "Tuesday night: put in claims" and "the league settings file gives a two-day
waiver period and names no day" for a week after v9.26 measured the run (Thursday 03:00 to 06:00, every season)
and set the rule to Wednesday night. check_page_logic.py reads the week sheet against the roster; check_plain.py
reads the register; nothing read a page's standing-rule SENTENCES against SECTION 2. A static string in a page
builder does not know when a rule changes, so a guard has to.

TWO KINDS OF LINE, both read on the visible text of every page listed:
  DEAD    a phrase or a number the directive has retracted (its DO-NOT-QUOTE table, and the rules v9.26 and v9.32
          replaced). Any one on a page fails.
  LIVE    a rule sentence the page is expected to carry, on the page that carries the routine. Missing fails.
Standard library only. Exit 1 on a hit, 2 on a page that is missing when it should exist.
"""
import html, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'Source')
PAGES = ['THE_WEEKLY_WIRE.html', 'WEEK_SHEET.html', 'LINEUP_CHECK.html', 'MY_TODO.html']

# DEAD: (what it is, regex on visible text). Each is a retraction the directive carries, in the page's register.
DEAD = [
    ('the Tuesday-night claim rule (v9.26: place claims Wednesday night)',
     r'Tuesday night:?\s*put (?:in|the) claims|put (?:in|the) claims (?:on )?Tuesday night'),
    ('the Sunday-night claim rule (retracted, doc 405)',
     r'place claims Sunday night|Sunday night:?\s*put (?:in|the) claims|claims? (?:in )?on Sunday night'),
    ('a Tuesday waiver run (there is none; claims execute Thursday morning)',
     r'run(?:s)? Tuesday morning|Tuesday(?:\'s| morning) run|the Tuesday run'),
    ('an unsourced processing day (doc 405 is the source)',
     r'names no day|never had a source for one'),
    ('the two-run week (there is no two-run week)',
     r'one of two runs'),
    ('a retracted D/ST bar (5.99 or 5.46; the bar is 5.51, a week 4.99)',
     r'\b5\.99\b|\b5\.46\b'),
    ('the retracted no-drop failure rate (6.1%; it is 16.2% on waiver claims)',
     r'\b6\.1%'),
    ('the retracted QB2 capture (96%; it is 66%)',
     r'\b96%\s*of (?:a|the) season'),
    ('the retracted seat curve (73.8 / 53.8 / 40.8 / 31.2 / 23.8)',
     r'\b73\.8%|\b23\.8%'),
    ('the retracted claim-order ladder (61.1 / 29.1 / 11.2)',
     r'\b61\.1%|\b29\.1%|\b11\.2%'),
    ('the retracted Out-designation timing (91.9% / 92% filed Thursday or later)',
     r'\b9[12](?:\.9)?%\s*of Out'),
    ('PUP/NFI/suspension stashes cost nothing (SSPD is never IR-eligible)',
     r'stash(?:es)? cost nothing'),
    ('the v9.38 lane trigger by points rank (v9.39: the simulated top-six odds under 30% decide, doc 469)',
     r'in points for, so (?:this lane leads|the seat list leads)'),
    ('the tight-end matchup at zero (doc 468: a tiebreak within a point at RB and TE; zero at WR only)',
     r'Receivers and tight ends: matchup is worth zero'),
]
# LIVE: (what it is, page, regex on visible text). Only the routine page is held to these.
LIVE = [
    ('the claim day is Wednesday night', 'THE_WEEKLY_WIRE.html', r'Wednesday night'),
    ('claims execute Thursday morning', 'THE_WEEKLY_WIRE.html', r'Thursday morning|Thursday, 03:00|3am Thursday'),
    ('a drop on every claim', 'THE_WEEKLY_WIRE.html', r'drop on every claim'),
    ('add before claim', 'THE_WEEKLY_WIRE.html', r'says Add'),
    ('the simulated top-six odds on the standings line (doc 469)', 'WEEK_SHEET.html', r'to make the top six'),
    ('the matchup tiebreak at RB and TE (doc 468)', 'THE_WEEKLY_WIRE.html', r'Backs and tight ends: .{0,80}tiebreak within a point'),
]


def visible(page):
    page = re.sub(r'(?is)<style.*?</style>|<script.*?</script>|<!--.*?-->', ' ', page)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?s)<[^>]+>', ' ', page)))


def scan(name, page):
    """(dead hits, live misses) for one page's HTML."""
    text = visible(page)
    dead = [(what, m.group(0)) for what, rx in DEAD for m in [re.search(rx, text, re.I)] if m]
    live = [what for what, pg, rx in LIVE if pg == name and not re.search(rx, text, re.I)]
    return dead, live


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if '--selftest' in argv:
        return selftest()
    bad = 0
    print('check_page_rules: the standing rules a page states, against the directive\'s')
    for name in PAGES:
        p = os.path.join(SRC, name)
        if not os.path.exists(p):
            print('  missing   %s' % name)
            bad = max(bad, 2 if name == 'THE_WEEKLY_WIRE.html' else bad)
            continue
        dead, live = scan(name, open(p, encoding='utf-8', errors='replace').read())
        for what, got in dead:
            print('  DEAD      %s carries %s: %r' % (name, what, got))
        for what in live:
            print('  MISSING   %s does not state %s' % (name, what))
        if dead or live:
            bad = max(bad, 1)
        else:
            print('  ok        %s' % name)
    print('\n' + ('every page states the live rule and none carries a dead one' if not bad
                  else 'A PAGE STATES A RULE THE DIRECTIVE HAS RETRACTED, OR OMITS ONE IT CARRIES. Fix the builder.'))
    return bad


OLD_WIRE = ('<h2>The routine, three things, once a week</h2><ol><li><b>Tuesday night: put in claims.</b> Priority resets '
            'every week</li><li>Check the processing day on ESPN rather than trusting a day printed here: the league '
            'settings file gives a two-day waiver period and names no day, so this page has never had a source for one.'
            '</li></ol>')
NEW_WIRE = ('<h2>The routine</h2><ol><li><b>Wednesday night: put the claims in, before 3am Thursday.</b> Claims execute '
            'Thursday morning.</li><li><b>A drop on every claim.</b></li><li><b>If the button says Add, add now.</b></li></ol>'
            '<p>Backs and tight ends: the opponent\'s points allowed to the position this season is a tiebreak within a point, never more.</p>')


def selftest():
    fails = 0
    dead, live = scan('THE_WEEKLY_WIRE.html', OLD_WIRE)
    ok = len(dead) >= 2 and len(live) >= 1
    print('  %-4s the 29 Sept wire page (Tuesday night, no sourced day) fires: %d dead, %d missing' % ('ok' if ok else 'BAD', len(dead), len(live)))
    fails += 0 if ok else 1
    dead, live = scan('THE_WEEKLY_WIRE.html', NEW_WIRE)
    ok = not dead and not live
    print('  %-4s the fixed routine stays quiet: %d dead, %d missing' % ('ok' if ok else 'BAD', len(dead), len(live)))
    fails += 0 if ok else 1
    dead, live = scan('WEEK_SHEET.html', '<p>The empty D/ST slot is charged 5.99 a week.</p>')
    ok = len(dead) == 1 and live == ['the simulated top-six odds on the standings line (doc 469)']
    print('  %-4s a retracted number on the week sheet fires, and the missing odds line is named: %s' % ('ok' if ok else 'BAD', dead))
    fails += 0 if ok else 1
    dead, live = scan('WEEK_SHEET.html', '<p>You are 9 of 12 in points for, so this lane leads the seat list.</p><p><b>39%</b> to make the top six</p>')
    ok = len(dead) == 1 and not live
    print('  %-4s the v9.38 points-rank trigger on the sheet fires (doc 469): %s' % ('ok' if ok else 'BAD', dead))
    fails += 0 if ok else 1
    dead, live = scan('THE_WEEKLY_WIRE.html', NEW_WIRE[:NEW_WIRE.index('<p>Backs')] + '<p>Receivers and tight ends: matchup is worth zero week to week.</p>')
    ok = len(dead) == 1 and 'the matchup tiebreak at RB and TE (doc 468)' in live
    print('  %-4s the old tight-end matchup sentence on the wire fires and the new one is named missing: %s' % ('ok' if ok else 'BAD', dead))
    fails += 0 if ok else 1
    dead, live = scan('WEEK_SHEET.html', '<p>The empty D/ST slot is charged 5.51 a week; a claim placed Wednesday night runs Thursday. <b>39%</b> to make the top six.</p>')
    ok = not dead and not live
    print('  %-4s the live number and the live day stay quiet' % ('ok' if ok else 'BAD'))
    fails += 0 if ok else 1
    print('selftest: %s' % ('all six controls behaved' if not fails else '%d control(s) failed' % fails))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
