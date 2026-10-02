#!/usr/bin/env python3
r"""
set_cookies.py -- refresh the ESPN cookies in EVERY script that carries them, in one go.

    py set_cookies.py                 # prompts for the two values
    py set_cookies.py --check         # just test the cookies already in the files
    py set_cookies.py --swid "{...}" --s2 "AEA..."      # non-interactive

WHY THIS EXISTS (doc 86): the guide said "refresh cookies in both scripts". There are FOUR
files, and Espn_pull_projections.py was carrying a DIFFERENT espn_s2 from the other three.
Hand-editing four files at 7:02 PM on draft night, from a card that says "both", is how you
end up with two working scripts and two broken ones and no idea which.

IT TESTS BEFORE IT WRITES. Bad cookies written into four files is worse than one 401.

WHERE TO GET THE VALUES (Chrome, signed in to fantasy.espn.com):
    F12 -> Application -> Storage -> Cookies -> https://fantasy.espn.com
    SWID     : copy the whole value INCLUDING the curly braces
    espn_s2  : copy the whole value, it is long and ends in %3D%3D
    Copy them verbatim. Do not decode, unescape, or "clean up" anything.
"""
import argparse, datetime as dt, os, re, shutil, sys, urllib.parse

HERE  = os.path.dirname(os.path.abspath(__file__))
ARCH  = os.path.normpath(os.path.join(HERE, '..', '_archive'))
FILES = [
    os.path.join(HERE, 'Espn_pull_projections.py'),
    os.path.join(HERE, 'espn_draft_injector_Gemini.py'),
    os.path.join(HERE, 'fetch_keepers.py'),
    os.path.join(HERE, 'live_draft', 'live_draft.py'),
    os.path.join(HERE, 'wire.py'),
    os.path.join(HERE, 'lineup.py'),
    os.path.join(HERE, 'waivers.py'),          # added 2026-09-08 with wire.py itself -- a fifth
                                            # file carrying cookies is the doc-86 defect unless
                                            # it is on this list from the day it ships.
    os.path.join(HERE, 'lineups.py'),          # added 2026-09-08 the same day it shipped, same reason.
]
LEAGUE, SEASON = 21985, 2026
TEST_URL = (f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{SEASON}"
            f"/segments/0/leagues/{LEAGUE}?view=mTeam")
HEADERS = {'accept': 'application/json', 'x-fantasy-platform': 'espn-fantasy-web',
           'x-fantasy-source': 'kona', 'referer': 'https://fantasy.espn.com/'}

RX_S2   = re.compile(r"('espn_s2'\s*:\s*)'[^']*'")
RX_SWID = re.compile(r"('swid'\s*:\s*)'[^']*'", re.I)

def read_current(path):
    t = open(path, encoding='utf-8').read()
    s2 = re.search(r"'espn_s2'\s*:\s*'([^']*)'", t)
    sw = re.search(r"'swid'\s*:\s*'([^']*)'", t, re.I)
    return (sw.group(1) if sw else None), (s2.group(1) if s2 else None)

def try_auth(swid, s2):
    """Return (ok, detail). Tries the value as given, then percent-encoded."""
    try:
        import requests
    except ImportError:
        return None, "requests not installed - cannot test"
    for label, v in (("as given", s2), ("percent-encoded", urllib.parse.quote(s2, safe='%'))):
        if label == "percent-encoded" and v == s2:
            continue
        try:
            r = requests.get(TEST_URL, cookies={'swid': swid, 'espn_s2': v},
                             headers=HEADERS, timeout=15)
        except Exception as e:
            return False, f"request failed: {e}"
        if r.status_code == 200:
            try:
                n = len((r.json() or {}).get('teams') or [])
            except Exception:
                n = '?'
            return True, f"HTTP 200, {n} teams visible ({label})"
        if r.status_code in (401, 403) and label == "as given":
            continue
        return False, f"HTTP {r.status_code} ({label})"
    return False, "HTTP 401/403 both as given and percent-encoded - the cookies are stale"

def normalise_swid(s):
    s = s.strip().strip('"').strip("'")
    if not s.startswith('{'): s = '{' + s
    if not s.endswith('}'):   s = s + '}'
    return s

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--swid'); ap.add_argument('--s2')
    ap.add_argument('--check', action='store_true', help='test what is already in the files')
    a = ap.parse_args(argv)

    missing = [f for f in FILES if not os.path.exists(f)]
    if missing:
        print("  !! not found (paths are absolute - is this the canonical Scripts folder?):")
        for f in missing: print("    ", f)
        return 1

    print("Files that carry ESPN cookies:")
    seen = {}
    for f in FILES:
        sw, s2 = read_current(f)
        tag = (s2 or '')[:14]
        seen.setdefault(tag, []).append(os.path.basename(f))
        print(f"   {os.path.basename(f):32s} espn_s2 starts {tag}...  swid {(sw or '')[:10]}...")
    if len(seen) > 1:
        print(f"   !! {len(seen)} DIFFERENT espn_s2 values across these files:")
        for k, v in seen.items(): print(f"      {k}... -> {', '.join(v)}")
        print("      After this run they will all match.")
    print()

    if a.check:
        sw, s2 = read_current(FILES[-1])
        ok, detail = try_auth(sw, s2)
        print(f"  live_draft.py cookies: {'OK' if ok else 'FAIL'} - {detail}")
        return 0 if ok else 1

    swid = a.swid or input("SWID    (with the braces): ")
    s2   = a.s2   or input("espn_s2 (long, ends %3D%3D): ")
    swid = normalise_swid(swid); s2 = s2.strip().strip('"').strip("'")
    if not re.fullmatch(r'\{[0-9A-Fa-f-]{30,40}\}', swid):
        print(f"  REFUSING: SWID does not look like {{8-4-4-4-12}}: {swid}"); return 1
    if len(s2) < 100:
        print(f"  REFUSING: espn_s2 is only {len(s2)} chars. It should be 300+."); return 1

    print("\nTesting against ESPN before touching any file...")
    ok, detail = try_auth(swid, s2)
    if ok is None:
        print(f"  cannot test ({detail}). Writing anyway - verify by running the tool.")
    elif not ok:
        print(f"  REFUSING TO WRITE: {detail}")
        print("  Nothing was changed. Re-copy both values from Chrome and try again.")
        return 1
    else:
        print(f"  OK - {detail}")
        if urllib.parse.quote(s2, safe='%') != s2 and 'percent-encoded' in detail:
            s2 = urllib.parse.quote(s2, safe='%')
            print("  (your value needed percent-encoding; the encoded form is what will be written)")

    os.makedirs(ARCH, exist_ok=True)
    stamp = f"{dt.datetime.now():%Y%m%d_%H%M}"
    print()
    for f in FILES:
        shutil.copy2(f, os.path.join(ARCH, f"{os.path.basename(f)}.cookies_{stamp}.bak"))
        t = open(f, encoding='utf-8').read()
        t2, n1 = RX_S2.subn(lambda m: m.group(1) + "'" + s2 + "'", t)
        t2, n2 = RX_SWID.subn(lambda m: m.group(1) + "'" + swid + "'", t2)
        open(f, 'w', encoding='utf-8', newline='').write(t2)
        print(f"   updated {os.path.basename(f):32s} ({n1} espn_s2, {n2} swid)")
    print(f"\n  Backups of the previous versions are in {ARCH}")
    print("  check_kit.py will now report these files STALE -- that is EXPECTED after a cookie")
    print("  refresh. Re-pin the manifest when things are calm, not at 7:02 PM.")
    print("  NEXT: re-run whatever threw the 401.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
