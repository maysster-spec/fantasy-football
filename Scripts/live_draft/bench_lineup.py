"""doc 139 -- the equivalence and speed check for the pure-Python _lineup rewrite.

s0.2 (v5.5): "A test must exercise the object PRODUCTION builds, not an equivalent one."
So this does not feed _lineup synthetic arrays.  It builds the REAL Engine off the shipped
board, wraps Engine.lv_from so that every single call production makes runs through BOTH
implementations, and asserts they agree EXACTLY -- not to a tolerance, exactly -- then runs
the real recommend() calls the live tool makes at each of Matt's picks.

Run it after touching either _lineup or _lineup_np:   py bench_lineup.py
"""
import os, sys, time
import numpy as np
import code_live_engine as CLE
from code_live_engine import Engine

HERE = os.path.dirname(os.path.abspath(__file__))
BAD = [0]; CALLS = [0]

_orig_lv_from = Engine.lv_from
def _checked(self, cache, extra=None):
    pc, pg, by, m = cache
    if extra is None:
        a = pc[:m], pg[:m], by[:m]
    else:
        pc[m] = CLE.PC[self.pos[extra]]; pg[m] = self.pg[extra]; by[m] = self.bye[extra]
        a = pc[:m+1], pg[:m+1], by[:m+1]
    fast = CLE._lineup(a[0].copy(), a[1].copy(), a[2].copy(), self.repl)
    ref  = CLE._lineup_np(a[0].copy(), a[1].copy(), a[2].copy(), self.repl)
    CALLS[0] += 1
    if fast != ref:
        BAD[0] += 1
        if BAD[0] <= 5:
            print(f"  MISMATCH  fast={fast!r}  ref={ref!r}  diff={fast-ref!r}")
            print(f"    pc={list(a[0])}\n    pg={list(a[1])}\n    bye={list(a[2])}")
    return fast

def build():
    return Engine(os.path.join(HERE, 'board_v8_fixed.csv'),
                  os.path.join(HERE, 'ESPN_prerank_with_ids.csv'))

def main():
    eng = build()
    ids = [int(x) for x in eng.b.ESPN_ID.tolist() if int(x) > 0]
    rng = np.random.default_rng(11)

    print("=" * 72)
    print("  1. EQUIVALENCE -- every lv_from call production makes, both ways, exact match")
    print("=" * 72)
    Engine.lv_from = _checked
    for n_taken, pick in [(7, 8), (16, 17), (31, 32), (55, 56), (88, 89), (127, 128), (150, 137)]:
        order = list(ids); rng.shuffle(order)      # a plausible-ish room, not board order
        taken = order[:n_taken]
        eng.set_taken(taken, taken[:max(1, n_taken // 12)])
        t = time.time()
        recs = eng.recommend(pick, rollout_inner=8, top=12)
        print(f"  pick {pick:>3}  {n_taken:>3} off the board  ->  {len(recs):>2} rows  "
              f"{CALLS[0]:>7} lineup calls  {time.time()-t:5.2f}s (both impls)")
        if BAD[0]:
            print(f"\n  !! {BAD[0]} MISMATCHES. The rewrite is NOT equivalent. Do not ship."); return 1
    print(f"  {CALLS[0]:,} calls, {BAD[0]} mismatches.  EXACT AGREEMENT.\n")

    print("=" * 72)
    print("  2. SPEED -- the on-clock render is the one that has to fit inside 60 seconds")
    print("=" * 72)
    Engine.lv_from = _orig_lv_from
    eng2 = build()
    for label, (top, inner, n_taken, pick) in {
        'pick 8, on the clock ': (12, 24, 7, 8),
        'pick 17, on the clock': (12, 24, 16, 17),
        'waiting (mid draft)  ': (12, 8, 60, 65),
        'waiting (late)       ': (12, 8, 130, 137),
    }.items():
        eng2.set_taken(ids[:n_taken], ids[:max(1, n_taken // 12)])
        t = time.time(); r = eng2.recommend(pick, rollout_inner=inner, top=top)
        fast = time.time() - t
        CLE._lineup, _sv = CLE._lineup_np, CLE._lineup
        eng2.set_taken(ids[:n_taken], ids[:max(1, n_taken // 12)])
        t = time.time(); r2 = eng2.recommend(pick, rollout_inner=inner, top=top)
        slow = time.time() - t
        CLE._lineup = _sv
        same = [x['player'] for x in r] == [x['player'] for x in r2]
        print(f"  {label}  {fast:6.2f}s   was {slow:6.2f}s   {slow/fast:4.1f}x faster   "
              f"same order: {same}")
    print()
    return 0

if __name__ == '__main__':
    sys.exit(main())
