#!/usr/bin/env python3
r"""
verify_prerank.py -- read back what ESPN ACTUALLY STORED and compare it, row by row,
against ESPN_prerank_with_ids.csv.

    py verify_prerank.py            # full 1:1 check
    py verify_prerank.py --top 250  # also report anything odd inside the first N

WHY (doc 90): until now the only confirmation that the prerank reached ESPN correctly was
Matt looking at the web page. That is a spot check -- and it is how the Broncos D/ST at
position 74 was found, by eye, a week before the draft. Eyes do not scan 544 rows.
This does. It reads only; it never writes.
"""
import argparse, os, sys
import pandas as pd, requests

CSV     = r"G:\My Drive\_Fantasy\2026\Scripts\live_draft\ESPN_prerank_with_ids.csv"
LEAGUE, TEAM, SEASON = 21985, 9, 2026
COOKIES = {
    'swid':    '{A7217088-1F36-4F1F-AE73-67262BF763EF}',
    'espn_s2': '',
}
HEADERS = {'accept':'application/json','x-fantasy-platform':'espn-fantasy-web',
           'x-fantasy-source':'kona','referer':'https://fantasy.espn.com/'}
BASE = (f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{SEASON}"
        f"/segments/0/leagues/{LEAGUE}")

def find_draft_list(obj, depth=0):
    if depth > 6: return None, None
    if isinstance(obj, dict):
        ds = obj.get("draftStrategy")
        if isinstance(ds, dict) and isinstance(ds.get("draftList"), list):
            return ds["draftList"], "draftStrategy.draftList"
        for k, v in obj.items():
            got, path = find_draft_list(v, depth+1)
            if got is not None: return got, f"{k}.{path}"
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:40]):
            got, path = find_draft_list(v, depth+1)
            if got is not None: return got, f"[{i}].{path}"
    return None, None

def fetch_stored():
    for url, label in [(f"{BASE}/teams/{TEAM}?view=mDraftDetail", "teams/ID mDraftDetail"),
                       (f"{BASE}/teams/{TEAM}?view=mTeam",        "teams/ID mTeam"),
                       (f"{BASE}?view=mDraftDetail",              "league mDraftDetail"),
                       (f"{BASE}?view=mTeam",                     "league mTeam")]:
        try:
            d = requests.get(url, cookies=COOKIES, headers=HEADERS, timeout=20).json()
        except Exception as e:
            print(f"  {label}: request failed - {e}"); continue
        if isinstance(d, list): d = d[0] if d else {}
        got, path = find_draft_list(d)
        if got: return [x if isinstance(x, int) else x.get('playerId') for x in got], f"{label} -> {path}"
    return None, None

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--top', type=int, default=250)
    a = ap.parse_args(argv)

    if not os.path.exists(CSV): sys.exit(f"not found: {CSV}")
    want = pd.read_csv(CSV).sort_values('prerank').reset_index(drop=True)
    name = dict(zip(want.ESPN_ID.astype(int), want.player))
    posn = dict(zip(want.ESPN_ID.astype(int), want.pos))
    wid  = [int(x) for x in want.ESPN_ID]

    print(f"local file : {CSV}  ({len(wid)} rows)")
    got, where = fetch_stored()
    if got is None:
        print("\n  COULD NOT READ a stored prerank from any view.")
        print("  Either nothing has been injected, or the cookies are stale.")
        print("  Try:  py set_cookies.py --check")
        return 2
    got = [int(x) for x in got if x is not None]
    print(f"ESPN stored: {len(got)} rows   [{where}]\n")

    ok = True
    if len(got) != len(wid):
        ok = False
        print(f"  !! COUNT MISMATCH: ESPN has {len(got)}, the file has {len(wid)} "
              f"({len(wid)-len(got):+d})")
        if len(wid)-len(got) == 32:
            print("     32 short = the negative D/ST ids were rejected. That is the known risk.")
    missing = [i for i in wid if i not in set(got)]
    extra   = [i for i in got if i not in set(wid)]
    if missing:
        ok = False
        print(f"  !! {len(missing)} player(s) in the file are NOT stored at ESPN:")
        for i in missing[:12]:
            print(f"       {name.get(i,'?')} ({posn.get(i,'?')})  id {i}")
        if len(missing) > 12: print(f"       ... and {len(missing)-12} more")
    if extra:
        ok = False
        print(f"  !! {len(extra)} id(s) stored at ESPN are not in the file: {extra[:12]}")

    n = min(len(got), len(wid))
    diffs = [(k, wid[k], got[k]) for k in range(n) if wid[k] != got[k]]
    if diffs:
        ok = False
        print(f"\n  !! ORDER DIFFERS at {len(diffs)} of the first {n} positions. First 10:")
        for k, w, g in diffs[:10]:
            print(f"       #{k+1:<4} file: {name.get(w,'?'):24s} | ESPN: {name.get(g, f'id {g}')}")
    else:
        print(f"  ORDER MATCHES exactly for all {n} positions.")

    bad = [(k+1, name.get(got[k], f'id {got[k]}'), posn.get(got[k], '?'))
           for k in range(min(a.top, len(got))) if posn.get(got[k]) in ('K', 'D/ST')]
    print(f"\n  K / D-ST inside ESPN's top {a.top}: {len(bad)}")
    for rank, nm, ps in bad:
        ok = False
        print(f"     !! #{rank} {nm} ({ps})  <- autodraft would take this if your clock expired")
    if not bad:
        print("     none - if your clock expires, autodraft takes a skill player.")

    print("\n" + ("  PASS: ESPN holds exactly what the file says." if ok
                  else "  FAIL: see above. Re-run py espn_draft_injector_Gemini.py, then this again."))
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
