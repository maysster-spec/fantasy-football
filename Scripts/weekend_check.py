#!/usr/bin/env python3
r"""
weekend_check.py -- every pre-draft test that can be run without touching ESPN's WRITE
side, in one command, with one verdict at the end.

    py weekend_check.py            # everything except the injector (which writes)
    py weekend_check.py --inject   # also re-inject the prerank and verify it

doc 94: this replaces five separate commands from COMMANDS.html. Running them one at a
time meant five chances to skip one, and five outputs to interpret. This runs them in
dependency order, stops nothing on a failure, and prints a single PASS/FAIL table.
"""
import argparse, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PY   = sys.executable

STEPS = [
    ('board numbers',    ['board_audit.py'],                'the VBD, ranks and engine rules are RIGHT'),
    ('file tree',        ['check_kit.py'],                  'every file is the one it should be'),
    ('ESPN cookies',     ['cookie_jar.py', '--check'],      'will they survive to Sept 7'),
    ('prerank at ESPN',  ['verify_prerank.py'],             'ESPN holds what the file says, row by row'),
    ('keeper read',      ['fetch_keepers.py', '--dry'],     'how many of the 12 have chosen'),
]
INJECT = ('prerank inject', ['espn_draft_injector_Gemini.py'], 'push the list to ESPN')

def run(label, argv, why, log):
    print('\n' + '=' * 72)
    print(f"  {label.upper()}  --  {why}")
    print('=' * 72)
    t = time.time()
    try:
        r = subprocess.run([PY, os.path.join(HERE, argv[0])] + argv[1:],
                           cwd=HERE, timeout=600)
        rc = r.returncode
    except subprocess.TimeoutExpired:
        print("  !! timed out after 10 minutes"); rc = 99
    except Exception as e:
        print(f"  !! could not run: {e}"); rc = 98
    log.append((label, rc, time.time() - t))
    return rc

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--inject', action='store_true',
                    help='also re-inject the prerank (this WRITES to ESPN) and re-verify')
    a = ap.parse_args()

    print("=" * 72)
    print("  WEEKEND CHECK -- everything testable, one command")
    print("  Nothing here writes to ESPN unless you passed --inject.")
    print("=" * 72)

    log = []
    steps = list(STEPS)
    if a.inject:
        steps.insert(2, INJECT)          # inject, THEN verify
    cookies_bad = False
    for label, argv, why in steps:
        # doc 94: NOT gated -- every step still runs, because seeing the whole picture in one
        # pass is the point. But an expired cookie makes the two ESPN steps below fail for the
        # SAME single reason, and four red lines look like four problems. Say so once, here.
        if cookies_bad and label in ('prerank at ESPN', 'keeper read', 'prerank inject'):
            print('\n' + '=' * 72)
            print(f"  {label.upper()}  --  SKIPPED")
            print('=' * 72)
            print("  The cookies failed above. This step talks to ESPN, so it would fail for")
            print("  that one reason and tell you nothing new. Fix the cookies, re-run this.")
            log.append((label, 97, 0.0))
            continue
        rc = run(label, argv, why, log)
        if label == 'ESPN cookies' and rc != 0:
            cookies_bad = True
            print("\n  ^^ COOKIES ARE THE PROBLEM. Everything below needs them, so the rest of")
            print("     this run is skipped. One fix, not four:  py cookie_jar.py")

    print("\n" + "=" * 72)
    print("  SUMMARY")
    print("=" * 72)
    # rc semantics differ per script, so translate rather than assume 0 == good
    def verdict(label, rc):
        if rc == 97:                            return 'skipped - fix the cookies first', False
        if rc in (98, 99):                      return 'COULD NOT RUN', False
        if label == 'board numbers':            return ('ALL CHECKS PASS' if rc == 0 else 'FAIL - DO NOT DRAFT ON IT'), rc == 0
        if label == 'file tree':                return ('PASS' if rc == 0 else 'FAIL'), rc == 0
        if label == 'ESPN cookies':             return ('OK' if rc == 0 else 'EXPIRED - run py cookie_jar.py'), rc == 0
        if label == 'prerank at ESPN':          return ('MATCHES' if rc == 0 else 'DIFFERS - see above'), rc == 0
        if label == 'keeper read':              return ('12 SELECTED' if rc == 0 else 'not all 12 yet - expected before Sept 7'), True
        if label == 'prerank inject':           return ('sent' if rc == 0 else 'see output above'), rc == 0
        return str(rc), rc == 0

    allgood = True
    for label, rc, secs in log:
        v, ok = verdict(label, rc)
        allgood = allgood and ok
        print(f"   {label:18s} {v:42s} {secs:5.1f}s")

    print()
    if allgood:
        print("  ALL CLEAR. Nothing left to do until Sept 5.")
    else:
        print("  Something above needs attention. Each line says what to run.")
        print("  If 'prerank at ESPN' differs:  py weekend_check.py --inject")
    return 0 if allgood else 1

if __name__ == '__main__':
    sys.exit(main())
