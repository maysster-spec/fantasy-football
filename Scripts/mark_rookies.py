#!/usr/bin/env python3
r"""
mark_rookies.py -- put ROOKIE status where the board can see it.  Doc 156.

    py mark_rookies.py            show what would change (default, writes nothing)
    py mark_rookies.py --write    apply it

WHY.  Matt: "I do want exciting rookies promoted."  The pipeline already KNOWS -- `games_2025.csv`
carries `g25 = -1` for a player with no 2025 regular-season snap -- and nothing anywhere displays
it.  `make_board.py`'s availability badge correctly EXCLUDES it (`if 0 < g25 <= 12`), because a
rookie is not an injury warning; so the one unambiguous fact about these players falls through
every crack in the project.

WHAT A ROOKIE IS, HERE.  `g25 == -1` alone is NOT rookie status: it also catches a veteran who
missed the whole season.  In the drafted range that conflation is 3 of 12 -- Jonathon Brooks (ACL),
MarShawn Lloyd, Tank Dell -- and calling Tank Dell a rookie on draft night would be worse than
saying nothing.  The test used here is
    no 2025 snaps  AND  absent from BOTH the 2023 and 2024 ESPN player pulls.
Two independent seasons, both already on disk, so it needs no new source and can be re-derived.
64 on the board, 9 inside the drafted range.

WHAT THIS IS NOT.  It is a FACT, not a ceiling.  SS4.13d is explicit that nothing in this project
computes a per-player ceiling and that the analyst panel cannot stand in for one; SS4.13b measured
that 4 of 5 players in the late ADP band never become startable at all.  This badge does not move
VBD, does not move rank, and does not enter any score -- exactly the standing of the `12g` badge
(SS4.22) and the backfield label (SS4.20).  It tells you WHO is a rookie.  It does not tell you
that being one is good.
"""
import argparse, datetime as dt, hashlib, os, re, shutil, sys
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.normpath(os.path.join(HERE, '..', 'Source'))
KIT  = os.path.join(HERE, 'live_draft')
CTX  = os.path.join(KIT, 'player_context.csv')
CHK  = os.path.join(HERE, 'check_kit.py')
ARCH = os.path.normpath(os.path.join(HERE, '..', '_archive'))


def rookie_ids(src=SRC, kit=KIT):
    b = pd.read_csv(os.path.join(kit, 'board_v8_fixed.csv'))
    g = pd.read_csv(os.path.join(src, 'games_2025.csv'))[['espn_id', 'g25']]
    seen = set()
    for f in ('espn_projections_2023_20260824.csv', 'espn_projections_2024_20260824.csv'):
        p = os.path.join(src, f)
        assert os.path.exists(p), f'need {f} to tell a rookie from a full-season miss -- refusing'
        seen |= set(pd.read_csv(p).espn_id.dropna().astype(int))
    m = b.merge(g, on='espn_id', how='left')
    assert m.g25.notna().all(), 'games_2025.csv does not cover the whole board -- refusing'
    r = m[(m.g25 == -1) & (~m.espn_id.astype(int).isin(seen))]
    return set(r.espn_id.astype(int)), m


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args(argv)

    ids, m = rookie_ids()
    pc = pd.read_csv(CTX); before = pc.copy()
    if 'rook' not in pc.columns: pc['rook'] = 0
    pc['rook'] = pc.ESPN_ID.astype(int).isin(ids).astype(int)

    live = m[(m.g25 == -1) & (m.adp_pick < 168)]
    print('=' * 78)
    print('  ROOKIE STATUS -> player_context.csv' + ('' if a.write else '   (dry run)'))
    print('=' * 78)
    print(f'  {len(ids)} rookies on the board; {int(pc.rook.sum())} of them carry a context row.\n')
    print(f"  {'player':<22}{'pos':<5}{'tm':<5}{'adp':>7}  verdict")
    for _, r in live.sort_values('adp_pick').iterrows():
        tag = 'ROOKIE' if int(r.espn_id) in ids else 'not a rookie - missed all of 2025'
        print(f"  {r.player:<22}{r.pos:<5}{r.team_c:<5}{r.adp_pick:>7.1f}  {tag}")

    for c in before.columns:
        if c == 'rook': continue
        if not before[c].fillna('').astype(str).equals(pc[c].fillna('').astype(str)):
            sys.exit(f"  REFUSING TO WRITE: column '{c}' changed")
    if len(before) != len(pc): sys.exit('  REFUSING TO WRITE: row count changed')
    if not a.write:
        print('\n  nothing written. re-run with --write to apply.'); return 0
    os.makedirs(ARCH, exist_ok=True)
    shutil.copy(CTX, os.path.join(ARCH, f'player_context_rook_{dt.date.today():%Y%m%d}.csv'))
    pc.to_csv(CTX, index=False)
    print('\n  written. old copy archived to _archive\\')
    try:
        d = open(CTX, 'rb').read().replace(b'\r\n', b'\n')
        s = open(CHK, encoding='utf-8').read()
        new = f"({len(d)}, '{hashlib.sha256(d).hexdigest()[:16]}'),"
        s2 = re.sub(r"(    'player_context\.csv':\s+)\(\d+, '[0-9a-f]{16}'\),",
                    lambda mm: mm.group(1) + new, s, count=1)
        if s2 != s:
            open(CHK, 'w', encoding='utf-8', newline='').write(s2)
            print(f"  re-pinned player_context.csv -> {new.strip('(),')}")
        else:
            print('  !! pin line not found in check_kit.py -- run it and repin by hand')
    except Exception as e:
        print(f'  (could not re-pin: {e})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
