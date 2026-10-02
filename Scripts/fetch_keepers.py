"""
fetch_keepers.py -- read the 12 ACTUAL keepers off ESPN after the 7:00 PM lock
and write actual_keepers.csv for keeper_swap.py.

    py fetch_keepers.py --dry     # show what ESPN reports, write nothing
    py fetch_keepers.py --write   # archive the old file, write the new one

WHY THIS EXISTS: typing 12 names under time pressure at 7:00 PM is the single
most error-prone step left on draft night. keeper_swap.py only needs a 'Player'
column, so this script's whole job is to produce those 12 names correctly.

IT REFUSES TO WRITE unless it finds exactly 12. A partial file is worse than no
file -- keeper_swap would silently rebuild the board against the wrong set.
"""
import argparse, datetime as dt, json, os, shutil, sys
import requests, pandas as pd

LEAGUE_ID = 21985
SEASON    = 2026
HERE      = os.path.dirname(os.path.abspath(__file__))
KFILE     = os.path.join(HERE, 'actual_keepers.csv')
# doc 80: was Scripts\_archive\ -- a second archive folder nobody else writes to.
# keeper_swap.py archives to 2026\_archive\; one archive, per the naming rule.
ARCHIVE   = os.path.normpath(os.path.join(HERE, '..', '_archive'))
SPINE     = os.path.normpath(os.path.join(HERE, '..', 'Source', 'code_universe_v5.csv'))

COOKIES = {
    'swid':    '{A7217088-1F36-4F1F-AE73-67262BF763EF}',
    'espn_s2': '',
}
HEADERS = {'accept':'application/json','x-fantasy-platform':'espn-fantasy-web',
           'x-fantasy-source':'kona','referer':'https://fantasy.espn.com/'}
BASE = (f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{SEASON}"
        f"/segments/0/leagues/{LEAGUE_ID}")

def get(view):
    r = requests.get(BASE, params={'view': view}, cookies=COOKIES, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.json()

def team_label(t):
    n = (t.get('name') or '').strip()
    if not n:
        n = f"{(t.get('location') or '').strip()} {(t.get('nickname') or '').strip()}".strip()
    return n or f"team {t.get('id')}"

def from_keeper_ids():
    """doc 90 -- THE RIGHT DOOR, found by --probe on 2026-08-30.
    ESPN stores each team's saved keeper at teams[].draftStrategy.keeperPlayerIds in the
    mTeam view. It is populated AS SOON AS A MANAGER SELECTS, not at the 7:00 PM lock, so
    this can be watched all week. mRoster (last season's full rosters) and mDraftDetail
    (empty until picks exist) were both the wrong doors."""
    data = get('mTeam')
    if isinstance(data, list): data = data[0] if data else {}
    out, seen_teams = [], 0
    for t in data.get('teams', []):
        seen_teams += 1
        ids = ((t.get('draftStrategy') or {}).get('keeperPlayerIds')) or []
        for pid in ids:
            out.append((team_label(t), '', pid))
    return out, seen_teams

def from_roster():
    """Pre-draft, a keeper league team's roster should hold exactly its kept player."""
    data = get('mRoster')
    out = []
    for t in data.get('teams', []):
        ents = ((t.get('roster') or {}).get('entries')) or []
        for e in ents:
            p = ((e.get('playerPoolEntry') or {}).get('player')) or {}
            nm = p.get('fullName')
            if nm: out.append((team_label(t), nm, p.get('id')))
    return out

def from_draft():
    """Fallback: ESPN carries the 12 keepers inside draftDetail.picks (doc 58)."""
    data = get('mDraftDetail')
    picks = ((data.get('draftDetail') or {}).get('picks')) or []
    names = {}
    try:
        tm = {t['id']: team_label(t) for t in get('mTeam').get('teams', [])}
    except Exception:
        tm = {}
    out = []
    for pk in picks:
        # doc 123: ESPN pre-creates the whole pick grid with EMPTY playerIds, and one of those
        # empty slots can carry keeper=True. `if pk.get('keeper')` alone would return a keeper
        # with no player in it. |pid| > 100 keeps real players and D/ST (-16000 - proTeamId)
        # and cannot keep a 0/-1 sentinel.
        try: pid = int(pk.get('playerId'))
        except (TypeError, ValueError): continue
        if pk.get('keeper') and abs(pid) > 100:
            out.append((tm.get(pk.get('teamId'), f"team {pk.get('teamId')}"),
                        names.get(pid, ''), pid))
    return out

def resolve_names(rows):
    """Fill blank names from an id map when the draft view gave ids only.

    doc 80 -- THE SPINE, NOT THE PRERANK. ESPN_prerank_with_ids.csv is the DRAFTABLE
    list, which by construction excludes the 12 keepers: measured 0 of 12 resolvable.
    That made the whole mDraftDetail fallback dead, and dead in the worst way -- it
    printed 12 rows of '<unknown id N>' and called it success. code_universe_v5.csv is
    the spine keeper_swap.py itself matches against: 12 of 12, both directions.
    """
    blanks = [r for r in rows if not r[1]]
    if not blanks: return rows
    idmap = {}
    for src, idcol, namecol in ((SPINE, 'espn_id', 'player'),
                                (os.path.join(HERE, 'live_draft',
                                              'ESPN_prerank_with_ids.csv'), 'ESPN_ID', 'player')):
        if not os.path.exists(src): continue
        m = pd.read_csv(src)
        for i, n in zip(m[idcol], m[namecol]):
            if pd.notna(i): idmap.setdefault(int(i), n)
    if not idmap:
        print("  !! no id->name source found; names will stay blank")
    return [(t, (n or idmap.get(int(i), f"<unknown id {i}>")), i) for t, n, i in rows]

def probe():
    """doc 90: ESPN's UI already SHOWS the saved keeper selections, so the data exists in the
    API somewhere -- mRoster and mDraftDetail are just the wrong doors. Rather than guess a
    field name, ask several views and report every key that looks like a keeper. One run
    answers it. Reads only; writes nothing."""
    VIEWS = ['mTeam', 'mRoster', 'mDraftDetail', 'mSettings', 'mMatchup', 'kona_player_info']
    hits = []

    def walk(o, path='', depth=0):
        if depth > 7: return
        if isinstance(o, dict):
            for k, v in o.items():
                kl = str(k).lower()
                if 'keeper' in kl:
                    if isinstance(v, (list, tuple)):
                        hits.append((f"{path}.{k}", f"list[{len(v)}]", str(v[:6])))
                    elif isinstance(v, dict):
                        hits.append((f"{path}.{k}", "dict", str(list(v.keys())[:6])))
                    else:
                        hits.append((f"{path}.{k}", type(v).__name__, str(v)[:60]))
                walk(v, f"{path}.{k}", depth + 1)
        elif isinstance(o, list):
            for i, v in enumerate(o[:14]):
                walk(v, f"{path}[{i}]", depth + 1)

    for v in VIEWS:
        hits.clear()
        try:
            data = get(v)
        except Exception as e:
            print(f"  {v:18s} request failed -- {e}"); continue
        if isinstance(data, list): data = data[0] if data else {}
        keys = ",".join(sorted(data.keys())[:10]) if isinstance(data, dict) else type(data).__name__
        walk(data)
        uniq = sorted(set(hits))
        print(f"\n  view={v}   top-level keys: {keys}")
        if not uniq:
            print("     no key containing 'keeper'")
        for path, kind, sample in uniq[:25]:
            print(f"     {path:52s} {kind:10s} {sample}")
        if len(uniq) > 25: print(f"     ... and {len(uniq)-25} more")

    print("\n  WHAT TO LOOK FOR: a list of 12 player ids, or one id per team. If you see it,")
    print("  send this output back and fetch_keepers.py will be pointed straight at it.")
    print("  Nothing was written. This is read-only.")

def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--dry',   action='store_true', help='show what ESPN reports, write nothing')
    g.add_argument('--write', action='store_true', help='archive the old file and write the new one')
    g.add_argument('--probe', action='store_true',
                   help='hunt for the keeper field across several ESPN views; writes nothing')
    a = ap.parse_args()

    if a.probe:
        probe(); return

    rows, how = [], ''
    # doc 90: keeperPlayerIds FIRST. It is the field ESPN actually uses, it is live from the
    # moment a manager selects, and it needs no lock. The other two are fallbacks now.
    try:
        kr, nteams = from_keeper_ids()
        kr = resolve_names(kr)
        print(f"  mTeam/keeperPlayerIds: {len(kr)} keeper(s) selected across {nteams} teams")
        if len(kr) == 12:
            rows, how = kr, 'mTeam/keeperPlayerIds'
        elif kr:
            missing = nteams - len(kr)
            print(f"  -> {len(kr)} of {nteams} teams have chosen. {missing} still to select:")
            for t, n, i in kr:
                print(f"       {t[:34]:36s} {n}")
            print(f"  This is a LIVE view, not a lock artefact -- re-run any time to watch it fill.")
            rows, how = kr, 'mTeam/keeperPlayerIds (INCOMPLETE)'
    except Exception as e:
        print(f"  mTeam/keeperPlayerIds: failed -- {e}")

    for label, fn in (('mRoster', from_roster), ('mDraftDetail', from_draft)):
        if how.startswith('mTeam/keeperPlayerIds') and len(rows) == 12: break
        try:
            got = resolve_names(fn())
        except Exception as e:
            print(f"  {label}: request failed -- {e}")
            continue
        print(f"  {label}: {len(got)} keeper-ish rows")
        if len(got) == 12:
            rows, how = got, label; break
        # doc 164: THIS LINE THREW AWAY THE RIGHT ANSWER. On 2026-09-04 keeperPlayerIds
        # returned 7 real keepers WITH NAMES; mRoster then returned 194 last-season roster
        # rows, `len(got) > len(rows)` was true, and `rows`/`how` were overwritten. The
        # "ONLY n OF 12 TEAMS HAVE SELECTED" message below is gated on `how`, so it could no
        # longer fire, and Matt was told the automatic path might be dead and to type twelve
        # names by hand -- while this script was holding seven of them. At 7:00 PM with
        # eleven of twelve chosen that is the worst advice it could give. A bigger pile of
        # rows is not a better answer: only an EXACT 12 (handled above) may displace the
        # right door.
        if how.startswith('mTeam/keeperPlayerIds'):
            print(f"    (ignoring {label}: keeperPlayerIds already answered with "
                  f"{len(rows)} of 12 -- a roster dump does not improve on that)")
            continue
        if len(got) > len(rows):
            rows, how = got, label + ' (WRONG COUNT)'

    if not rows:
        sys.exit("\nNOTHING RETURNED. Cookies may be expired (check for 401/403 above),\n"
                 "or the keeper lock has not happened yet. Fall back to editing\n"
                 "actual_keepers.csv by hand -- that path still works.")

    if len(rows) <= 20:
        print(f"\n{'team':38s} player")
        print('-'*72)
        for t, n, i in rows:
            print(f"{t[:36]:38s} {n}")
    else:
        # doc 89: 194 names scrolled the actual verdict off the screen at the one moment
        # it needs reading. Summarise instead.
        from collections import Counter as _C
        per = _C(t for t, _, _ in rows)
        print(f"\n  {len(rows)} players across {len(per)} teams -- too many to be keepers.")
        for t, c in list(per.items())[:4]:
            print(f"    {t[:36]:38s} {c} players")
        print(f"    ... and {max(0, len(per)-4)} more teams")

    from collections import Counter
    if len(rows) != 12:
        # doc 89: MEASURED on 2026-08-30, pre-lock -- mRoster returned 194 rows and
        # mDraftDetail returned 0. Doc 80 assumed "pre-draft, a keeper team's roster holds
        # exactly its kept player". FALSE: ESPN still has LAST SEASON's full rosters loaded
        # until the keeper lock. Printing 194 names and a generic refusal made a normal,
        # expected pre-lock state look like a malfunction. Name the shape instead.
        per = Counter(t for t, _, _ in rows)
        avg = (len(rows) / len(per)) if per else 0
        if how.startswith('mTeam/keeperPlayerIds'):
            sys.exit(f"\nONLY {len(rows)} OF 12 TEAMS HAVE SELECTED A KEEPER.\n"
                     f"Nothing is broken -- this is the live count, and it fills in as managers\n"
                     f"choose. Re-run closer to the 7:00 PM lock on Sept 7.\n"
                     f"If it is still short AFTER the lock, the league is waiting on someone:\n"
                     f"pause the draft, let them pick, then re-run this and keeper_swap.py.")
        if len(rows) > 12 and avg >= 5:
            sys.exit(f"\nNOT LOCKED YET -- and that is the expected answer before 7:00 PM.\n"
                     f"ESPN returned {len(rows)} players across {len(per)} teams "
                     f"({avg:.0f} each): those are LAST SEASON'S FULL ROSTERS, not keepers.\n"
                     f"ESPN does not narrow them to the kept player until the keeper lock.\n"
                     f"\nThis is a PASS for a pre-lock dry run. Nothing is broken.\n"
                     f"  - Re-run this at 7:00 PM on Sept 7, after the lock.\n"
                     f"  - If it still shows full rosters THEN, the automatic path is dead:\n"
                     f"    type the 12 names into actual_keepers.csv by hand and carry on.\n"
                     f"    draft_night.bat already opens it in Notepad for exactly this.")
        sys.exit(f"\nREFUSING TO WRITE: found {len(rows)} rows, expected exactly 12.\n"
                 f"Every team keeps exactly one player. A partial file would make\n"
                 f"keeper_swap.py rebuild the board against the wrong set -- silently.\n"
                 f"Edit actual_keepers.csv by hand instead.")

    # doc 80: counting to 12 is NOT the rule. The rule is ONE PER TEAM (directive 2.1a).
    # Twelve rows spread 2/1/1/.../0 also counts to 12 and would have been written.
    from collections import Counter
    per = Counter(t for t, _, _ in rows)
    if len(per) != 12 or max(per.values()) != 1:
        bad = ', '.join(f"{t} x{c}" for t, c in per.items() if c != 1) or 'a team with none'
        sys.exit(f"\nREFUSING TO WRITE: 12 rows, but not one per team -- {bad}.\n"
                 f"{len(per)} distinct teams seen. Eligibility is one keeper per team;\n"
                 f"this shape means the view returned rosters, not keepers.\n"
                 f"Edit actual_keepers.csv by hand instead.")

    unknown = [n for _, n, _ in rows if str(n).startswith('<unknown id')]
    if unknown:
        sys.exit(f"\nREFUSING TO WRITE: {len(unknown)} name(s) could not be resolved: "
                 f"{unknown}.\nkeeper_swap.py would reject these anyway. Look them up on the\n"
                 f"ESPN league page and edit actual_keepers.csv by hand.")

    dupe = [n for n, c in Counter(n for _, n, _ in rows).items() if c > 1]
    if dupe:
        sys.exit(f"\nREFUSING TO WRITE: duplicate player name(s) {dupe}.")

    if a.dry:
        print(f"\n--dry: nothing written. Source view = {how}. Re-run with --write when this looks right.")
        return

    os.makedirs(ARCHIVE, exist_ok=True)
    if os.path.exists(KFILE):
        shutil.copy2(KFILE, os.path.join(
            ARCHIVE, f"actual_keepers_{dt.datetime.now():%Y%m%d_%H%M}.csv"))
    pd.DataFrame([{'Team': t, 'Player': n} for t, n, _ in rows]).to_csv(
        KFILE, index=False, encoding='utf-8')
    print(f"\nWROTE {KFILE}  (source view: {how}; previous version archived)")
    print("NEXT:  py keeper_swap.py --check")

if __name__ == '__main__':
    main()
