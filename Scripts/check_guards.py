"""check_guards.py -- break the engine on purpose and see which guards stay silent.

WHY THIS EXISTS. Matt, 24 Sept: *"the guard has to be designed correctly because those have been
faulty too, lol"* and *"The check doesn't seem to cover all critical components else this wouldn't
have been missed for so long."* Both are right, and neither is answerable by writing more guards.

Every guard here already ships with a negative control: it is shown firing on the ONE defect it was
written for (0.2). What no control can tell you is the opposite question -- **which real defects
would slip past ALL of them.** That is the blind spot, and a blind spot is invisible by definition
until something is deliberately broken.

THE OUTSIDE PRACTICE THIS COPIES is mutation testing. Trail of Bits, 18 Sept 2025, *Use mutation
testing to find the bugs your tests don't catch*: coverage measures whether code was EXECUTED, not
whether it was checked for correctness, so the real measure is "systematically introducing bugs and
checking if your tests catch them". Their cost advice is taken too: mutations are grouped by
priority rather than generated exhaustively, because an exhaustive sweep of a 200 KB engine would
never be run twice.

WHAT IT DOES. Each MUTATION below re-introduces a defect this project actually shipped. For each
one it patches a copy of the engine, rebuilds the page, runs every guard, and records whether
ANYTHING failed.

    CAUGHT   -- some guard fired. That defect cannot come back silently.
    SURVIVED -- the page rebuilt clean with a known defect in it. A NAMED BLIND SPOT.

A survivor is not a bug in this file. It is a guard that needs writing, and the point of the run is
to produce that list rather than to pass.

    py check_guards.py            run every mutation
    py check_guards.py --fast     the highest-priority group only
    py check_guards.py --selftest prove the harness can tell CAUGHT from SURVIVED

EXIT CODES. 0 every mutation caught · 1 at least one survivor · 2 the clean engine will not build
a page · 3 a guard named in GUARDS is not on disk (the run still reports the guards that are).

A GUARD THAT IS NOT ON DISK IS REPORTED BY NAME AND FAILS THE RUN (doc 435). The first version of
this file skipped an absent guard with a bare `continue`, so a copy of Scripts\\ without
check_plain.py ran every mutation, printed CAUGHT and SURVIVED for each, and said nothing about the
instrument it had not used. That is an exit code standing in for a result (0.2): coverage measured
without one of the guards is not the coverage the output claims. Now the missing names print
before the first mutation, every line below them is labelled as measured without them, and the
exit code is 3 whatever the mutations show. --selftest proves it on a copy with one guard removed.

Standard library only (doc 144); nothing is written outside a temporary directory, and the real
`Scripts\\` tree is never modified. (That backslash was an invalid escape in a non-raw docstring until
29 Sept: silent on 3.11, a SyntaxWarning on every run under Matt's 3.12, 0.4.)
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', 'Source'))

# Each mutation is (name, priority, doc, find, replace, what it breaks in one line).
# `find` must match EXACTLY ONCE in sheet_engine.py or the mutation reports NOT APPLICABLE rather
# than passing quietly -- an engine that has moved on is a reason to re-aim, not to report success.
MUTATIONS = [
    ('divisor back to 17', 1, 419,
     '    _left = proj_games(week)',
     '    _left = PROJ_GAMES',
     'prices a rest-of-season projection over a full season; every rate goes ~11% low'),

    ('weekly positions priced on a season rate', 1, 424,
     '    return pos not in WEEKLY_VALUE',
     '    return True',
     'lets a defense or kicker be added and dropped on a season number'),

    ('losing moves recommended', 1, 424,
     '            if _net <= 0.05:\n                _skipped += 1\n                continue',
     '            if False:\n                _skipped += 1\n                continue',
     'prints a move under WHAT TO DO whose net is negative'),

    ('blend switched off', 1, 417,
     '            if _meas and week:',
     '            if False:',
     'reverts every pts/wk to a preseason projection with no label change'),

    ('drop may empty a starting slot', 2, 420,
     '                if not _may_drop(_pp.get(\'pos\')):\n                    continue',
     '                if False:\n                    continue',
     'offers both defenses, or the only kicker, leaving a lineup slot unfilled'),

    # [doc 462] RE-AIMED: the rule now refuses a same-position drop only when that man starts (his cost
    # on the bye grid is above zero). The mutation lets a STARTER at the add's position be the drop.
    ('add paired with a drop at its own position', 2, 417,
     "                if _pp.get('pos') == _m.get('pos') and (_grid.get(id(_pp), 1.0) or 0.0) > 0.05:",
     "                if False:",
     'prices a straight swap as if it were an add'),

    ('a man replaces himself', 2, 420,
     '        if (norm_name(_fr.get(\'name\')), _fp) in _own:\n            continue',
     '        if False:\n            continue',
     'uses a rostered man as the free replacement for another rostered man'),

    ('negative drop cost inflates the net', 3, 416,
     '            _net = _m[\'worth\'] - max(0.0, _cost)',
     '            _net = _m[\'worth\'] - _cost',
     'counts one upgrade twice off a single roster spot'),

    # [doc 436] A MAN IN THE IR SLOT HOLDS NONE OF THE FIFTEEN, SO DROPPING HIM FREES NO SEAT.
    # On 28 Sept THE CALL paired "take Kalif Raymond" with "drop Jonah Coleman, 0.0" while Coleman
    # sat in slot 21; the claim runs as sixteen of fifteen and fails on the roster limit. The fix
    # was one predicate, `_is_parked`, on the ladder and on the cheapest-thing table. These two
    # take it off again, one site each, and check_page_logic.py is the guard that sees it: it reads
    # slot_id out of MY_ROSTER.csv itself and never asks the engine who is parked.
    ('a parked man offered as the drop in THE CALL', 1, 436,
     "              if c is not None and norm_name(pl.get('name')) not in dn and not _is_parked(pl)]",
     "              if c is not None and norm_name(pl.get('name')) not in dn]",
     'pairs an add with a drop who is in the injured-reserve slot, so the claim fails on the limit'),

    ('a parked man is the cheapest thing you own', 1, 436,
     '    costs = [x for x in adj if not _is_parked(x[1])][:4]',
     '    costs = adj[:4]',
     'names a man in the injured-reserve slot as the cheapest drop, in the table and the cost line'),
]

# [doc 436] check_page_logic.py is the layer doc 425 said was missing: the page against the league's
# rules, reading the roster file itself, so an engine that forgets a rule cannot make the guard
# forget with it. Doc 425 named the file; the parked-man rule is the first thing in it.
GUARDS = ['check_vintage.py', 'check_sources.py', 'check_plain.py', 'check_page_logic.py']


def missing_guards(folder):
    """The guards named in GUARDS that are not on disk in `folder`, by name, in GUARDS order."""
    return [g for g in GUARDS if not os.path.exists(os.path.join(folder, g))]


def build_and_check(scripts, source, log, guards=None):
    """Rebuild the page from `scripts`, then run every guard in `guards` (GUARDS when None).
    Returns the set of guards that exited non-zero, or {'the build itself'}."""
    render = os.path.join(scripts, '_render.py')
    with open(render, 'w', encoding='utf-8') as fh:
        fh.write(
            "import csv, glob, os, sys\n"
            "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n"
            "import sheet_engine as SE\n"
            "SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Source')\n"
            "SE.set_horizon(3)\n"
            "rate, why = SE.rates(SRC, 3)\n"
            "assert not why, why\n"
            "mine, status = {}, {}\n"
            "for r in csv.DictReader(open(os.path.join(SRC,'MY_ROSTER.csv'), newline='', encoding='utf-8-sig')):\n"
            "    mine[str(r['espn_id'])] = r['player']; status[str(r['espn_id'])] = r['status']\n"
            "roster = [dict(rate[p], status=status[p]) for p in mine if p in rate]\n"
            "free = []\n"
            "wf = sorted(glob.glob(os.path.join(SRC, 'WIRE_*.csv')))[-1]\n"
            "for r in csv.DictReader(open(wf, newline='', encoding='utf-8-sig')):\n"
            "    pid = str(r['espn_id'])\n"
            "    if pid not in rate: continue\n"
            "    f = dict(rate[pid]); f['owned'] = SE._f(r['owned_pct']); f['screen'] = r.get('screen') or ''\n"
            "    for k in ('form_sig','snap_pct','w1_targets','tgt_share','touches'): f[k] = r.get(k) or ''\n"
            "    f['status'] = r.get('status') or 'ACTIVE'\n"
            "    free.append(f)\n"
            # [1 Oct, doc 467] the wire files carry no kicker or defense; the live run's avail does. Every priced
            # kicker and defense on no league roster is free here too, so the weekly-position mutation has the
            # object it changes (0.2) and check_page_logic's P8 can measure it. The hand-made "Jets D/ST" row at
            # 6.2 that used to stand in for them is gone: it collided with the real Jets D/ST and P9 read it as a
            # divisor error.
            "_owned = {str(r['espn_id']) for r in csv.DictReader(open(os.path.join(SRC,'LEAGUE_ROSTERS.csv'), newline='', encoding='utf-8-sig'))}\n"
            "for pid, v in rate.items():\n"
            "    if v.get('pos') in ('K','D/ST') and pid not in _owned:\n"
            "        free.append(dict(v, owned=None, screen='', status='ACTIVE'))\n"
            "const, cnote = SE.load_constants(SRC)\n"
            # doc 451: the open jobs the live wire page marks, so the sheet this harness renders carries
            # what the live one carries and check_page_logic's P3 measures the mutation, not the harness.
            "import re, html as _h\n"
            "oj = []\n"
            "wp = os.path.join(SRC, 'THE_WEEKLY_WIRE.html')\n"
            "if os.path.exists(wp):\n"
            "    for row in re.findall(r'<tr\\b[^>]*>(?:(?!</tr>).)*?the job is open(?:(?!</tr>).)*?</tr>', open(wp, encoding='utf-8', errors='replace').read(), re.S | re.I):\n"
            "        c = [' '.join(_h.unescape(re.sub(r'<[^>]+>', ' ', x)).split()) for x in re.findall(r'<t[hd]\\b[^>]*>(.*?)</t[hd]>', row, re.S | re.I)]\n"
            "        if len(c) >= 4:\n"
            "            oj.append(dict(player=c[0], tm=c[1], hurt=c[2].replace(' (yours)', ''), status=c[3].split(' \\u00b7 ')[0], ceil=0.0, mine='(yours)' in c[2]))\n"
            # [30 Sept] the crowd list, so P4 (every most-added man answered) measures the mutation and not the harness\n
            "crowd = []\n"
            "for wf2 in [wf] + sorted(glob.glob(os.path.join(SRC, 'FREE_UNRANKED_*.csv')))[-1:]:\n"
            "    for r in csv.DictReader(open(wf2, newline='', encoding='utf-8-sig')):\n"
            "        crowd.append(dict(name=r['player'], pos=r['pos'], tm=r['team'], owned=r.get('owned_pct'), own_chg=r.get('own_chg'), espn_id=r['espn_id']))\n"
            "SE.write(os.path.join(SRC,'WEEK_SHEET.html'), roster, free, const, note=cnote,\n"
            "         unpriced=[], seats_used=len(mine), week=3, team_name='JUG', open_jobs=oj, crowd=crowd)\n")
    r = subprocess.run([sys.executable, render], cwd=scripts,
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        log.append('  the page would not build: ' + (r.stderr.strip().splitlines() or ['?'])[-1][:120])
        return {'the build itself'}
    # THE RESULT IS A SET, AND IT IS COMPARED AGAINST A BASELINE (doc 425). The first run of this
    # harness refused to start because check_sources.py was ALREADY failing on a live defect (a man
    # owned and free at once). Refusing was correct -- a guard that is already red cannot prove
    # anything about a mutation -- but it also made the harness unusable exactly when the project
    # has an open problem, which is most of the time. So: record which guards are red BEFORE any
    # mutation, and count a mutation as caught only when it turns a guard red that was GREEN.
    failed = set()
    for g in (GUARDS if guards is None else guards):
        if not os.path.exists(os.path.join(scripts, g)):
            # [doc 435] NEVER A BARE `continue` HERE. main() and selftest() report the absent
            # guards by name before the first build and pass only the present ones in, so reaching
            # this line means a guard vanished mid-run, which is not a thing to be quiet about.
            raise RuntimeError('guard named in GUARDS is not on disk: %s' % g)
        gr = subprocess.run([sys.executable, g], cwd=scripts,
                            capture_output=True, text=True, timeout=300)
        if gr.returncode != 0:
            failed.add(g)
    return failed


def report_missing(missing):
    """Print the absent guards by name. Called before anything is measured, so the reader knows
    what every CAUGHT and SURVIVED below was measured without."""
    if not missing:
        return
    print('  %d GUARD(S) NAMED IN GUARDS %s NOT ON DISK IN %s:'
          % (len(missing), 'IS' if len(missing) == 1 else 'ARE', HERE))
    for g in missing:
        print('    - %s' % g)
    print('  Everything below is measured WITHOUT %s, and this run exits 3 whatever it finds.'
          % ('it' if len(missing) == 1 else 'them'))
    print('  A guard that is not there catches nothing; a run that skipped it would be reporting')
    print('  coverage it never measured (doc 435). Put the file back, then run this again.')
    print()


def prepare(tmp, fixture=False):
    """A working copy of Scripts\\ and Source\\ that the mutations can be applied to. With `fixture`,
    the files in Source\\fixture\\ are laid over the copy (doc 466, catalog A5): a frozen roster on
    which the parked-man and own-position mutations change the page, so they read caught or
    survived rather than NO EFFECT. The live tree is never touched either way."""
    s, d = os.path.join(tmp, 'Scripts'), os.path.join(tmp, 'Source')
    os.makedirs(s); os.makedirs(d)
    for f in os.listdir(HERE):
        if f.endswith('.py'):
            shutil.copy2(os.path.join(HERE, f), s)
    for f in os.listdir(SRC):
        # doc 451: the wire page is an INPUT now (check_page_logic P3 reads the open jobs it marks)
        if f.endswith(('.csv', '.json', '.txt')) or f == 'THE_WEEKLY_WIRE.html':
            shutil.copy2(os.path.join(SRC, f), d)
    if fixture:
        fx = os.path.join(SRC, 'fixture')
        if not os.path.isdir(fx):
            raise SystemExit('--fixture asked for and Source\\fixture\\ is not there (doc 466)')
        for f in os.listdir(fx):
            if f.endswith('.csv'):
                shutil.copy2(os.path.join(fx, f), d)
        print('  FIXTURE: Source\\fixture\\ laid over the working copy (' + ', '.join(sorted(f for f in os.listdir(fx) if f.endswith('.csv'))) + ')')
    return s, d


def main(argv):
    fast = '--fast' in argv
    fixture = '--fixture' in argv
    todo = [m for m in MUTATIONS if m[1] == 1] if fast else MUTATIONS
    # [doc 435] THE ABSENT GUARDS ARE NAMED FIRST, against the real tree, before anything is copied
    # or built. The run goes on with the guards that are present, so the coverage of those is still
    # measured, and the exit code is 3 regardless of what the mutations show.
    missing = missing_guards(HERE)
    report_missing(missing)
    present = [g for g in GUARDS if g not in missing]
    rc = _run_mutations(todo, present, fixture)
    return 3 if missing else rc


def _run_mutations(todo, guards, fixture=False):
    tmp = tempfile.mkdtemp(prefix='guards_')
    try:
        scripts, source = prepare(tmp, fixture)
        clean = os.path.join(scripts, 'sheet_engine.py')
        original = open(clean, encoding='utf-8').read()

        log = []
        base = build_and_check(scripts, source, log, guards)
        if 'the build itself' in base:
            print('  THE UNMUTATED ENGINE WILL NOT BUILD A PAGE.')
            print('  Fix that first; nothing below would mean anything (0.2).')
            for line in log:
                print(line)
            return 2
        # [30 Sept] THE PAGE THE CLEAN ENGINE BUILT, so a mutation that changes nothing on today's
        # inputs is reported as NO EFFECT and not as a blind spot. The two parked-man mutations
        # (doc 436) read SURVIVED on 30 Sept because the parked man's cost is filtered upstream of
        # the mutated line on that roster: the page came out byte-identical, no guard could see a
        # defect that was not on the page, and "no guard covers it" was the wrong sentence. A
        # NO EFFECT row is a mutation to re-aim, or a fixture to build (the harness runs on the
        # live roster, so what it proves changes with the roster).
        page = os.path.join(source, 'WEEK_SHEET.html')
        # two clean builds differ only in the build stamp and the footer's own bytes/hash/time line,
        # and [1 Oct, doc 461] in the <title> and masthead time when the two builds straddle a minute:
        # the two parked-man mutations read SURVIVED on 1 Oct 07:48/07:49 on a page that differed by
        # that minute alone. The stamp text is stripped wherever the page prints it.
        _stamp = re.compile(rb'data-built="\d+"|Built by sheet_engine\.py [^<]*'
                            rb'|<title>Week Sheet [^<]*</title>|built [A-Z][a-z]+day \d+ [A-Z][a-z]+ \d\d:\d\d[^<]*'
                            rb'|just now|\d+ (?:minutes|hours|days) old')      # the inputs box's file ages
        def _page_bytes():
            return _stamp.sub(b'', open(page, 'rb').read()) if os.path.exists(page) else b''
        base_page = _page_bytes()
        if base:
            print('  NOTE: %s already failing before any mutation, on a real defect. A mutation'
                  % ', '.join(sorted(base)))
            print('  counts as caught only if it turns a DIFFERENT guard red.')
            print()

        print('  %d mutation(s), each one a defect this project actually shipped, against %s:'
              % (len(todo), ', '.join(guards) or 'NO GUARDS AT ALL'))
        survivors, no_effect = [], []
        for name, prio, doc, find, repl, breaks in todo:
            if original.count(find) != 1:
                print('  %-9s %-44s the engine has moved on; re-aim this one' % ('RE-AIM', name))
                survivors.append((name, doc, breaks, 'could not be applied'))
                continue
            open(clean, 'w', encoding='utf-8').write(original.replace(find, repl))
            log = []
            now_failing = build_and_check(scripts, source, log, guards)
            open(clean, 'w', encoding='utf-8').write(original)
            caught = ', '.join(sorted(now_failing - base)) or None
            mut_page = _page_bytes()
            if caught:
                print('  %-9s %-44s %s' % ('caught', name, caught))
            elif base_page and mut_page == base_page:
                print('  %-9s %-44s the page is byte-identical: nothing to catch on today\'s inputs'
                      % ('NO EFFECT', name))
                no_effect.append((name, doc, breaks))
            else:
                print('  %-9s %-44s NOTHING FIRED' % ('SURVIVED', name))
                survivors.append((name, doc, breaks, 'no guard covers it'))

        print()
        if no_effect:
            print('  %d mutation(s) had NO EFFECT on today\'s inputs (the page did not change), so they'
                  % len(no_effect))
            print('  prove nothing either way today. Re-aim them, or give the harness a fixed roster:')
            for name, doc, breaks in no_effect:
                print('   - %s (doc %s)' % (name, doc))
            print()
        if not survivors:
            print('  Every mutation that changed the page was caught. No blind spot among the defects we know about.')
            return 0
        print('  %d BLIND SPOT(S). Each is a guard that needs writing, not a bug in this file:'
              % len(survivors))
        for name, doc, breaks, why in survivors:
            print('   - %s (doc %s): %s' % (name, doc, breaks))
            print('     %s' % why)
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def selftest():
    """The harness must be able to tell CAUGHT from SURVIVED, or its output means nothing."""
    tmp = tempfile.mkdtemp(prefix='guards_self_')
    try:
        # [doc 435] CONTROL 0: AN ABSENT GUARD MUST BE NAMED, NOT SKIPPED. First the real tree,
        # which must report none: otherwise the controls below run without an instrument and
        # cannot prove what they claim, and that is reported as the real tree's gap, not as a
        # control failing. Then a copy of the tree with one guard deleted, which must report
        # exactly that name.
        missing = missing_guards(HERE)
        if missing:
            print('  control 0, the real tree: %s NOT ON DISK. The controls below need every'
                  % ', '.join(missing))
            print('  guard present to mean anything, so this selftest stops here and exits 3.')
            return 3
        print('  control 0, the real tree: every guard in GUARDS is on disk. OK')
        scripts, source = prepare(tmp)
        victim = GUARDS[0]
        os.remove(os.path.join(scripts, victim))
        got = missing_guards(scripts)
        assert got == [victim], ('the missing-guard check did not name the removed guard', got)
        print('  control 0, %s removed from a copy of Scripts: reported by name. OK' % victim)
        shutil.rmtree(tmp, ignore_errors=True)
        tmp = tempfile.mkdtemp(prefix='guards_self_')

        scripts, source = prepare(tmp)
        log = []
        base = build_and_check(scripts, source, log)
        assert 'the build itself' not in base, ('the clean engine must build', log)
        print('  control 1, the clean engine builds a page. Guards already red: %s'
              % (', '.join(sorted(base)) or 'none'))

        # THE CONTROL MUTATION IS ONE THAT MUST BE DETECTABLE, and it is deliberately NOT one of
        # the real ones. The first draft used doc 419's divisor and the harness reported it
        # SURVIVED -- which turned out to be true and important (check_vintage recomputes from the
        # same engine, so a divisor error changes the page and the check together and they agree).
        # A control has to prove the harness can SEE, so it uses a defect no guard could miss:
        # doc-voice on the page, which check_plain.py exists to refuse.
        clean = os.path.join(scripts, 'sheet_engine.py')
        original = open(clean, encoding='utf-8').read()
        find = "<h4>the injured-reserve seat</h4>"
        assert original.count(find) == 1, original.count(find)
        open(clean, 'w', encoding='utf-8').write(
            original.replace(find, "<h4>the injured-reserve seat (&sect;4.36, n=1,431)</h4>"))
        now_failing = build_and_check(scripts, source, [])
        open(clean, 'w', encoding='utf-8').write(original)
        new_red = now_failing - base
        assert new_red, 'the harness failed to notice a KNOWN defect -- its output is worthless'
        print('  control 2, doc-voice written onto the page: %s went red. OK'
              % ', '.join(sorted(new_red)))
        print('  all three controls pass: an absent guard is named, and CAUGHT and SURVIVED are '
              'distinguishable.')
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    raise SystemExit(selftest() if '--selftest' in sys.argv else main(sys.argv[1:]))
