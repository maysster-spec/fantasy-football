#!/usr/bin/env python3
r"""
cookie_jar.py -- ONE command to fix expired ESPN cookies.

    py cookie_jar.py            # try automatic, fall back to guided paste
    py cookie_jar.py --check    # just test what the scripts currently hold
    py cookie_jar.py --manual   # skip the automatic attempt

WHAT IT DOES, in order, so you never have to remember the steps:
  1. Tests the cookies already in your scripts. If they work it stops -- nothing to fix.
  2. Tries to read SWID and espn_s2 straight out of Chrome. If that works you are done;
     no F12, no filter box, no copy-paste.
  3. If Chrome cannot be read, it OPENS the right page for you and walks you through the
     two copies, one at a time, waiting after each.
  4. Whatever the source, it TESTS the values against your league BEFORE writing anything,
     then updates all four scripts and backs up the originals to 2026\_archive\.

doc 91: this replaces a five-step manual procedure. Every step of that procedure was a place
to get it wrong at 7:02 PM, which is exactly when it would be needed.
"""
import argparse, os, subprocess, sys, time, webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
COOKIE_URL = "https://fantasy.espn.com"

def _sc():
    import set_cookies
    return set_cookies

def from_chrome():
    """Read the two cookies out of the local Chrome profile. Returns (swid, s2) or None."""
    try:
        import browser_cookie3
    except ImportError:
        print("  browser_cookie3 is not installed -- that is the library that can read Chrome.")
        ans = input("  Install it now? (about 5 seconds) [Y]/n: ").strip().lower()
        if ans in ('n', 'no'):
            return None
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "browser_cookie3", "--quiet"],
                           check=True, timeout=180)
            import browser_cookie3            # noqa: F811
        except Exception as e:
            print(f"  install failed ({e}). Falling back to the guided paste.")
            return None
    try:
        jar = browser_cookie3.chrome(domain_name='espn.com')
    except Exception as e:
        print(f"  could not read Chrome ({e}).")
        print("  Common cause: Chrome is running and holding the cookie file open. "
              "Close Chrome fully and re-run, or continue with the guided paste.")
        return None
    got = {c.name: c.value for c in jar if c.name in ('SWID', 'swid', 'espn_s2')}
    swid = got.get('SWID') or got.get('swid')
    s2 = got.get('espn_s2')
    if not swid or not s2:
        print(f"  Chrome had {sorted(got)} but not both. Are you signed in to ESPN in Chrome?")
        return None
    print(f"  read from Chrome: SWID {swid[:12]}...  espn_s2 {s2[:14]}... ({len(s2)} chars)")
    return swid, s2

def guided():
    """Open the page and walk him through the two copies, one at a time."""
    print("\n  GUIDED MODE -- two copies, one at a time. Nothing to remember.\n")
    print(f"  Opening {COOKIE_URL} ...")
    try: webbrowser.open(COOKIE_URL)
    except Exception: print(f"  (could not open a browser -- go to {COOKIE_URL} yourself)")
    time.sleep(1)
    print("""
  In that Chrome window:
     1. Sign in if it asks.
     2. Press F12.
     3. Click the  Application  tab along the top of the panel.
        (not there? click the  >>  chevron to find it)
     4. Left sidebar:  Storage -> Cookies -> https://fantasy.espn.com
     5. A table appears. Above it is a box marked  Filter.
""")
    input("  Press Enter when you can see that Filter box... ")
    print("""
     6. Type   espn_s2   into the Filter box. One row is left.
     7. DOUBLE-CLICK its Value cell, then Ctrl+A, then Ctrl+C.
        It is long and ends in %3D%3D.
""")
    s2 = input("  Paste espn_s2 here (right-click pastes in PowerShell): ").strip()
    print("""
     8. Clear the Filter box and type   SWID   instead.
     9. DOUBLE-CLICK its Value cell, Ctrl+A, Ctrl+C.
        It looks like {A7217088-1F36-...} -- KEEP THE CURLY BRACES.
""")
    swid = input("  Paste SWID here: ").strip()
    return swid, s2

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--check',  action='store_true', help='only test what is already there')
    ap.add_argument('--manual', action='store_true', help='skip the automatic Chrome read')
    a = ap.parse_args(argv)
    SC = _sc()

    print("=" * 66)
    print("  COOKIE JAR -- one command, four scripts")
    print("=" * 66)
    print("\n  Step 1 of 3: testing the cookies already in your scripts...")
    swid_now, s2_now = SC.read_current(SC.FILES[-1])
    ok, detail = SC.try_auth(swid_now, s2_now)
    if ok:
        print(f"  ALREADY FINE - {detail}")
        print("  Nothing to do. Stop here.")
        return 0
    if ok is None:
        print(f"  cannot test ({detail}) -- carrying on anyway.")
    else:
        print(f"  EXPIRED - {detail}")
    if a.check:
        print("\n  --check only. Nothing was changed. Re-run without --check to fix them.")
        return 1

    print("\n  Step 2 of 3: getting fresh values...")
    pair = None if a.manual else from_chrome()
    if pair is None:
        pair = guided()
    swid, s2 = pair

    print("\n  Step 3 of 3: testing and writing...")
    rc = SC.main(['--swid', swid, '--s2', s2])
    if rc == 0:
        print("\n  DONE. Re-run whatever threw the 401.")
        print("  check_kit.py will report those four files STALE -- that is expected.")
    return rc

if __name__ == '__main__':
    sys.exit(main())
