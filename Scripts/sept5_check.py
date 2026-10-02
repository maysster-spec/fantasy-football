"""
sept5_check.py -- the whole Sept 5 (T-48h) analysis in one command.

    py sept5_check.py                    # uses the newest espn_projections_2026_*.csv it finds
    py sept5_check.py --pull <file.csv>  # or name one explicitly

WHAT IT DOES, and why this is not a judgment call any more:
The board's `proj_leaguepts` IS the pull's `proj_2026` (verified exact, 480/480 rows).
So the board-order test does not need a spine rebuild -- swap the projections in, recompute
VBD against the same replacement levels, re-rank, and compare. That is doc 64's test, run
in about a second instead of by hand.

VERDICT: FREEZE if >=150 of the top 161 stay within 2 slots. Otherwise REBUILD and doc 62 §5
becomes live.
"""
import argparse, glob, os, sys
import pandas as pd

HERE  = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.join(HERE, 'live_draft', 'board_v8_fixed.csv')
REPL  = {'QB': 341.603, 'RB': 168.589, 'WR': 163.540, 'TE': 140.295}
MYPICKS = [8, 17, 32, 41, 56, 65, 80, 89]

def _pulls():
    pats = [os.path.join(HERE, 'espn_projections_2026_*.csv'),
            os.path.join(HERE, '..', 'Source', 'espn_projections_2026_*.csv')]
    files = [f for p in pats for f in glob.glob(p)]
    return sorted(set(files), key=os.path.getmtime, reverse=True)

def newest_pull():
    files = _pulls()
    if not files:
        sys.exit("No espn_projections_2026_*.csv found. Run the pull first, or pass --pull.")
    return files[0]

def drift_vs_previous(pull, p):
    """doc 85: did ESPN re-forecast AT ALL since the last pull?

    Measured 2026-08-30: two pulls 8 hours apart, **0 of 700 projections changed**. ESPN
    re-forecasts in batches, not continuously -- previously a [HYPOTHESIS] in doc 64, now
    [TESTED]. That matters, because a FREEZE verdict computed on byte-identical projections
    proves the pipeline runs; it does NOT re-validate the board against anything new. Saying
    'FREEZE' without saying 'nothing moved' invites exactly the false confidence this project
    keeps finding."""
    others = [f for f in _pulls() if os.path.abspath(f) != os.path.abspath(pull)]
    if not others:
        print("  drift: no earlier pull on disk to compare against.\n"); return
    prev = others[0]
    try:
        q = pd.read_csv(prev, usecols=['espn_id', 'proj_2026'])
    except Exception as e:
        print(f"  drift: could not read {os.path.basename(prev)} ({e})\n"); return
    j = p[['espn_id', 'proj_2026']].merge(q, on='espn_id', how='inner', suffixes=('', '_prev'))
    d = (j.proj_2026.fillna(-1) - j.proj_2026_prev.fillna(-1)).abs()
    n = int((d > 0.001).sum())
    print(f"  drift vs {os.path.basename(prev)}: "
          f"{n} of {len(j)} projections changed")
    if n == 0:
        print("  !! ESPN HAS NOT RE-FORECAST since that pull. Everything below is arithmetic on")
        print("     IDENTICAL numbers -- a FREEZE here proves the pipeline works, NOT that the")
        print("     board was re-validated against anything new. The real work today is the")
        print("     news sweep, not this verdict.")
    print()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pull', help='projection CSV to test against')
    a = ap.parse_args()
    pull = a.pull or newest_pull()

    if not os.path.exists(BOARD):
        sys.exit(f"board not found: {BOARD}")
    b = pd.read_csv(BOARD)
    p = pd.read_csv(pull, usecols=['espn_id', 'Player', 'proj_2026'])
    print(f"board : {BOARD}  ({len(b)} rows)")
    print(f"pull  : {pull}\n")

    # doc 81: the pull script's PULL REJECTED guard only PRINTS -- it still writes the CSV and
    # still exits 0. So a corrupt pull (the 2023 failure mode, doc 56) becomes the newest file,
    # this script picks it up, and prints an authoritative VERDICT computed on garbage. The
    # VERDICT line is the one thing Matt is told to read. Re-check the invariant here, in the
    # consumer, because this script is also run by hand with --pull.
    live = int(p.proj_2026.notna().sum())
    if live < 400:
        sys.exit(f"  REFUSING TO TEST: this pull carries only {live} live projections "
                 f"(expected >= 400).\n"
                 f"  That is the PULL REJECTED condition -- re-run the pull; ESPN is\n"
                 f"  nondeterministic here. A VERDICT computed on this file means nothing.\n"
                 f"  File: {pull}")
    print(f"  pull integrity: {live} live projections (>= 400 required)  OK\n")
    drift_vs_previous(pull, p)

    m = b.merge(p, on='espn_id', how='left', suffixes=('', '_new'))
    missing = m.proj_2026.isna().sum()
    if missing:
        # doc 81: this used to say "investigate if any sit inside the top 161" -- a job the
        # script can do in one line and was handing back to Matt at 8am on the busiest morning.
        inside = m[m.proj_2026.isna() & (m['rank'] <= 161)]
        print(f"  !! {missing} board players are absent from the new pull -- they keep their old "
              f"projection for this test.")
        if len(inside):
            print(f"     {len(inside)} of them are INSIDE the top 161 and their rank is therefore "
                  f"unretested:")
            for _, r in inside.sort_values('rank').iterrows():
                print(f"       rank {int(r['rank']):3d}  {r.player} ({r.pos})")
        else:
            print(f"     none of them are inside the top 161 -- the tested region is complete.")
    m['new_proj'] = m.proj_2026.fillna(m.proj_leaguepts)
    m['new_vbd']  = m.apply(lambda r: r.new_proj - REPL.get(r.pos, 1e9), axis=1)
    m['new_rank'] = m.new_vbd.rank(ascending=False, method='first').astype(int)

    top = m[m['rank'] <= 161].copy()
    top['move'] = top.new_rank - top['rank']
    same   = int((top.move == 0).sum())
    within = int((top.move.abs() <= 2).sum())
    drop   = int((top.new_rank > 161).sum())

    print("=" * 66)
    print(f"  BOARD-ORDER TEST (doc 64)          top 161 compared")
    print("=" * 66)
    print(f"  identical rank            {same:3d} / 161")
    print(f"  within 2 slots            {within:3d} / 161      <- the threshold is 150")
    print(f"  moved more than 5 slots   {int((top.move.abs() > 5).sum()):3d}")
    print(f"  dropped out of the 161    {drop:3d}")

    # Replacement is the nth-best projection across the FULL pull, by position.
    # Verified: this reproduces the shipped levels exactly on the 08-20 pull.
    print("\n  replacement levels, recomputed on the FULL new pull:")
    pfull = pd.read_csv(pull, usecols=['pos', 'proj_2026'])
    for pos, n in (('RB', 30), ('WR', 30), ('QB', 12), ('TE', 12)):
        col = pfull[(pfull.pos == pos) & pfull.proj_2026.notna()].proj_2026.sort_values(ascending=False)
        got = col.iloc[n - 1] if len(col) >= n else float('nan')
        flag = '' if abs(got - REPL[pos]) < 1.5 else '   <-- MOVED, 4.1b says +/-1.5 VBD matters'
        print(f"    {pos}{n:<3} {got:8.3f}   shipped {REPL[pos]:8.3f}   delta {got - REPL[pos]:+7.3f}{flag}")

    print("\n  your picks, +/-2 window still intact?")
    for pk in MYPICKS:
        old = set(m[(m['rank'] >= pk - 2) & (m['rank'] <= pk + 2)].player)
        new = set(m[(m.new_rank >= pk - 2) & (m.new_rank <= pk + 2)].player)
        print(f"    pick {pk:3d}   {len(old & new)}/5 unchanged")

    big = m[(m.new_proj - m.proj_leaguepts).abs() > 25].copy()
    if len(big):
        big['delta'] = big.new_proj - big.proj_leaguepts
        print(f"\n  projections that moved more than 25 points ({len(big)}):")
        for _, r in big.sort_values('delta').iterrows():
            print(f"    {r.player:24s} {r.pos:3s} {r.proj_leaguepts:7.1f} -> {r.new_proj:7.1f} "
                  f"({r.delta:+6.1f})   board rank {int(r['rank'])} -> {int(r.new_rank)}")
        print("    ^ CHECK THE NEWS ON EACH. A move this size has a reason.")

    print("\n" + "=" * 66)
    if within >= 150:
        print("  VERDICT: FREEZE.  The board stands. No rebuild.")
        print("  Handle any large mover above as a verbal override at the pick.")
    else:
        print("  VERDICT: REBUILD.  Only {}/161 held within 2 slots.".format(within))
        print("  doc 62 section 5 is now live -- read it before doing anything else.")
    print("=" * 66)

if __name__ == '__main__':
    main()
