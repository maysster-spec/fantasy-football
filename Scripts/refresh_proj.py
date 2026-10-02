#!/usr/bin/env python3
r"""
refresh_proj.py -- re-freeze the PROJECTIONS, the sibling refresh_adp.py never had.

    py refresh_proj.py            show what would change   (default, writes nothing)
    py refresh_proj.py --write    apply it

WHY THIS EXISTS (doc 144, correcting doc 143). When sept5_check.py returns REBUILD there was
nothing to run, and doc 62 -- "the shipped board has no builder" -- was read as meaning the board
could not be updated at all. That is true of the SPINE (raw ESPN JSON -> league scoring -> the
480-row universe, with s2's scoring map and s3's stat-id traps). It is NOT true of the board.
MEASURED on the shipped board, 480 rows:

    vbd  = proj_leaguepts - s4.1 replacement    max error 0.000426   (i.e. exactly)
    rank = vbd rank descending                  480 of 480 rows
    the pull's proj_2026 is the SAME league-scored quantity as proj_leaguepts:
        45.2% of matched rows identical to 0.1 pts, 83.8% within 5, r = 0.9925

So the board is a pure function of (projection, position) with the replacement levels held fixed.
The expensive, trap-laden part is already done by Espn_pull_projections.py. This script does the
cheap part refresh_adp.py already does for the market -- swap the column in, recompute what
derives from it, archive, re-pin -- and NOTHING else.

WHAT IT TOUCHES: proj_leaguepts, vbd, rank, flag. Nothing else. adp_pick / gone_ahead / eff_pick
belong to refresh_adp.py and are asserted unchanged.

REPLACEMENT LEVELS ARE HELD FIXED, on purpose -- s4.1b: "Do NOT make this self-refitting; the same
method on 2024's projections gives RB25/WR35, a ten-rank swing off one season's noise."

THE NEWS OVERRIDE IS RE-APPLIED HERE, NOT BOLTED ON AFTER. doc 101's runbook says to run
apply_news.py after a rebuild; a rebuild that forgets it restores a player the league knows is
out. Josh Jacobs is the live case: the board holds him at 0.0 and the 09-03 pull wants to put him
at rank 93. This script re-zeroes every row in news_overrides.csv and REFUSES to write if any of
them survives with a projection.
"""
import argparse, datetime as dt, glob, hashlib, os, re, shutil, sys
import pandas as pd

HERE  = os.path.dirname(os.path.abspath(__file__))
KIT   = os.path.join(HERE, 'live_draft')
BOARD = os.path.join(KIT, 'board_v8_fixed.csv')
SRC   = os.path.normpath(os.path.join(HERE, '..', 'Source'))
ARCH  = os.path.normpath(os.path.join(HERE, '..', '_archive'))
NEWS  = os.path.join(HERE, 'news_overrides.csv')
STAMP = os.path.join(KIT, 'proj_vintage.txt')
CHECK = os.path.join(HERE, 'check_kit.py')
REPL  = {'QB': 341.603, 'RB': 168.589, 'WR': 163.540, 'TE': 140.295}   # s4.1, HELD FIXED

def newest_pull():
    c = sorted(glob.glob(os.path.join(SRC, 'espn_projections_2026_*.csv')))
    if not c: sys.exit(f"  no 2026 pull found in {SRC}")
    return c[-1]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--pull', help='use this pull instead of the newest')
    a = ap.parse_args()
    pull = a.pull or newest_pull()

    b = pd.read_csv(BOARD)
    p = pd.read_csv(pull); p.columns = [c.replace('﻿', '') for c in p.columns]
    for need in ('espn_id', 'proj_2026'):
        if need not in p.columns: sys.exit(f"  {os.path.basename(pull)} has no {need} column")
    assert p.espn_id.is_unique, "the pull has duplicate espn_id -- the merge would inflate the board"

    print("=" * 74)
    print(f"  RE-FREEZE THE PROJECTIONS from {os.path.basename(pull)}"
          + ("" if a.write else "   (dry run)"))
    print("=" * 74)

    n0 = len(b)
    m = b.merge(p[['espn_id', 'proj_2026', 'injuryStatus']], on='espn_id', how='left')
    assert len(m) == n0, f"merge inflated the board {n0} -> {len(m)}"
    miss = m.proj_2026.isna()
    if miss.any():
        print(f"  !! {int(miss.sum())} board players are not in this pull; they keep their old "
              f"projection.")
        for _, r in m[miss & (m['rank'] <= 161)].iterrows():
            print(f"     rank {int(r['rank']):3d}  {r.player}")

    new_proj = pd.to_numeric(m.proj_2026, errors='coerce').fillna(b.proj_leaguepts).round(2)

    # ---- the news override, re-applied BEFORE anything derives from the projection ----
    held = {}
    if os.path.exists(NEWS):
        nw = pd.read_csv(NEWS)
        for _, r in nw.iterrows():
            if str(r.get('action', '')).strip().lower() == 'out':
                held[int(r.espn_id)] = r.get('player', '')
    if held:
        hit = m.espn_id.isin(held)
        for _, r in m[hit].iterrows():
            was = float(new_proj[r.name])
            print(f"  NEWS OVERRIDE: {r.player:<22} pull says {was:7.1f} -> forced to 0.0 "
                  f"(news_overrides.csv)")
        new_proj = new_proj.where(~hit, 0.0)

    new_vbd  = (new_proj - b.pos.map(REPL)).round(6)
    new_rank = new_vbd.rank(ascending=False, method='first').astype(int)

    d = pd.DataFrame(dict(player=b.player, pos=b.pos, old_rank=b['rank'], new_rank=new_rank,
                          old_proj=b.proj_leaguepts, new_proj=new_proj, adp=b.adp_pick))
    d['dproj'] = (d.new_proj - d.old_proj).round(1)
    d['drank'] = d.new_rank - d.old_rank
    top = d[(d.old_rank <= 175) | (d.new_rank <= 175)]
    moved = top[top.dproj.abs() >= 1.0]
    print(f"\n  players compared              {len(d)}")
    print(f"  inside pick 175, moved >=1pt  {len(moved)} of {len(top)}")
    if len(moved):
        print(f"  median |move| {moved.dproj.abs().median():.2f}   max {moved.dproj.abs().max():.1f}")
    big = moved.reindex(moved.dproj.abs().sort_values(ascending=False).index).head(14)
    print("\n  biggest projection movers inside your picks:")
    for _, r in big.iterrows():
        print(f"    {r.player:<24}{r.pos:<4} adp{r.adp:6.1f}   proj {r.old_proj:6.1f} ->"
              f" {r.new_proj:6.1f} ({r.dproj:+6.1f})   rank {int(r.old_rank):>3} ->"
              f" {int(r.new_rank):>3} ({r.drank:+4d})")

    if not a.write:
        print("\n  DRY RUN -- nothing written. Re-run with --write.")
        return

    out = b.copy()
    out['proj_leaguepts'] = new_proj
    out['vbd'] = new_vbd
    out['rank'] = new_rank
    if 'injuryStatus' in m.columns:
        out['flag'] = m.injuryStatus.where(m.injuryStatus.notna(), b.flag)

    # ---- gates. Refuse rather than ship a board that failed one. ----
    assert len(out) == n0, "row count changed"
    assert set(out.espn_id) == set(b.espn_id), "the player set changed"
    for c in ('adp_pick', 'gone_ahead', 'eff_pick', 'bye', 'team_c', 'pos', 'player'):
        assert out[c].equals(b[c]), f"{c} changed -- this script must not touch it"
    if held:
        bad = out[out.espn_id.isin(held) & (out.proj_leaguepts != 0.0)]
        assert bad.empty, f"NEWS OVERRIDE LOST for {list(bad.player)} -- refusing to write"
    assert out['rank'].is_unique and out['rank'].min() == 1 and out['rank'].max() == n0, \
        "rank is not a clean 1..N permutation"

    os.makedirs(ARCH, exist_ok=True)
    st = f"{dt.datetime.now():%Y%m%d_%H%M}"
    shutil.copy2(BOARD, os.path.join(ARCH, f"board_v8_fixed_preProj_{st}.csv"))
    out.to_csv(BOARD, index=False)
    open(STAMP, 'w', encoding='utf-8').write(os.path.basename(pull) + "\n")
    print(f"\n  archived the old board to {ARCH}")
    print(f"  wrote {BOARD}")
    print(f"  stamped {os.path.basename(STAMP)}")
    repin(BOARD)
    print("\n  NOW, IN THIS ORDER:")
    print("    py board_audit.py            (must still pass 39/39)")
    print("    py depth_map.py              (job labels read the board)")
    print("    py make_fallback.py          (the paper board's ranks just moved)")
    print("    py make_board.py             (DRAFT_BOARD.pdf)")
    print("    py mkoverride.py             (should now report ZERO movers)")
    print("  The ESPN prerank IS ordered by VBD rank, and rank just changed --")
    print("  re-run  py make_prerank.py  and re-inject if you want ESPN's own board to match.")

def repin(pth):
    if not os.path.exists(CHECK): return
    d = open(pth, 'rb').read().replace(b'\r\n', b'\n')
    name = os.path.basename(pth)
    s = open(CHECK, encoding='utf-8').read()
    new = f"({len(d)}, '{hashlib.sha256(d).hexdigest()[:16]}'),"
    s2 = re.sub(r"(    '" + re.escape(name) + r"':\s+)\(\d+, '[0-9a-f]{16}'\),",
                lambda m: m.group(1) + new, s, count=1)
    if s2 != s:
        open(CHECK, 'w', encoding='utf-8', newline='').write(s2)
        print(f"  re-pinned {name}: {new.strip('(),')}")

if __name__ == '__main__':
    main()
