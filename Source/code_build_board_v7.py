#!/usr/bin/env python3
"""
code_build_board_v7.py — draft board for slot 8, 2026. Supersedes v6.

WHAT CHANGED FROM v6 (all four are defect fixes, not preference):
 1. K/D-ST no longer carry a cross-position VBD (code_kdst_guard). On the v6 board Broncos D/ST
    ranked 41st overall, ahead of Drake Maye (43) and Tetairoa McMillan (45), and the kicker
    Brandon Aubrey ranked 51st. Cause: replacement = "Nth best of pool", but D/ST12 is the 12th
    of only 32 candidates (top third) while RB30 is the 30th of 116 (bottom quartile).
 2. All 12 predicted keepers are removed from the pool BEFORE pick 1, per 2.1(c)/(d) -- the
    round-15 accounting is bookkeeping and has nothing to do with when players leave the board.
 3. injury_status is surfaced on the board. Audit 19 flagged 32 players inside ADP 170 who
    appeared on NO shipped artifact. Surfaced, never scored -- an August flag has untested
    predictive value (see doc 42 on why no position-level injury haircut is applied).
 4. ADP refreshed to the 2026-08-23 pull (projections identical to 08-20; ADP moved 1.05 picks
    on average inside ADP 70).

Does NOT touch the live draft board or the draft grid -- those are pending redesign.
"""
import sys, pandas as pd, numpy as np
sys.path.insert(0, '/tmp/build')
from code_kdst_guard import apply_kdst_guard, skill_only, assert_kdst_pool_intact, STREAMED

SRC = '/mnt/user-data/uploads/2026/Source/'
OUT = '/tmp/build/'
MY_PICKS = [8, 17, 32, 41, 56, 65, 80, 89, 104, 113, 128, 137, 152, 161]
KEEPER_BYE = 14      # George Pickens, settled

u = pd.read_csv(SRC + 'code_universe_v5.csv'); u.columns = [c.replace('﻿','') for c in u.columns]
e = pd.read_csv(SRC + 'espn_projections_2026_20260823.csv'); e.columns = [c.replace('﻿','') for c in e.columns]
kp = pd.read_csv(SRC + 'predicted_keepers_v5.csv')

assert_kdst_pool_intact(u)                       # C3/D3 guard: 32 defenses, no constant fills

# --- refresh ADP from the newer pull, on espn_id (never on name -- C1) -------------------
n0 = len(u)
u = u.merge(e[['espn_id','espn_adp','injuryStatus']], on='espn_id', how='left')
assert len(u) == n0, 'ADP refresh changed row count'
u['adp_pick'] = u['espn_adp'].fillna(u['adp_pick'])
u['injury_status'] = u['injuryStatus'].fillna(u.get('injury_status'))

# --- guard K/DST, then deplete keepers BEFORE pick 1 -------------------------------------
u = apply_kdst_guard(u)
# C1: names are not identifiers. This exact pair ("Travis Etienne" vs "Travis Etienne Jr.")
# is the worked example in ERROR_PATTERNS C1 and it recurred here -- Etienne is Snyder's keeper
# and was showing as available at picks 32 and 41. Alias table + a hard assert, not a warning.
from keeper_alias import KEEPER_ALIAS   # J5 (doc 58): generated from the spine
kp['Player'] = kp['Player'].replace(KEEPER_ALIAS)
keeper_ids = set(kp['Player'])
u['is_keeper'] = u['player'].isin(keeper_ids)
print(f"keepers matched on the spine: {u.is_keeper.sum()} of {len(kp)}")
missing = keeper_ids - set(u.loc[u.is_keeper, 'player'])
assert not missing, (f"UNMATCHED KEEPERS {sorted(missing)} -- these players would stay in the "
                    f"draft pool and be recommended to you. Fix KEEPER_ALIAS. (ERROR_PATTERNS C1)")

pool = u[~u.is_keeper].copy()

# effective pick: 12 keepers are off the board, so everyone behind them slides earlier
# B2 (doc 58): keeper ADPs MUST come from the same pull as the pool. predicted_keepers_v5.csv
# carries its own older column; using it put gone_ahead wrong on 22 rows (Stevenson 98.6 vs 86.1).
_kfresh = kp['Player'].map(e.set_index('Player')['espn_adp'])
assert _kfresh.notna().all(), f"keeper ADP unresolved for {kp.loc[_kfresh.isna(),'Player'].tolist()}"
kadp = sorted(_kfresh)
pool['gone_ahead'] = pool['adp_pick'].map(lambda a: sum(1 for x in kadp if x < a) if pd.notna(a) else 0)
pool['eff_pick'] = pool['adp_pick'] - pool['gone_ahead']

# --- board -------------------------------------------------------------------------------
# B6 (doc 58): 6 exact VBD tie groups, 37 rows. pandas' default quicksort is unstable, so a
# spine rebuild can permute them. mergesort + an explicit secondary key makes ordering total.
board = pool[pool['vbd'].notna()].sort_values(['vbd','adp_pick','player'],
                                              ascending=[False,True,True], kind='mergesort').reset_index(drop=True)
board['rank'] = board.index + 1
board['bye_clash_pickens'] = np.where(board['bye'] == KEEPER_BYE, 'YES', '')
board['flag'] = board['injury_status'].where(
    board['injury_status'].isin(['QUESTIONABLE','OUT','DOUBTFUL','INJURY_RESERVE']), '')

cols = ['rank','player','pos','team_c','bye','proj_leaguepts','vbd','adp_pick','eff_pick',
        'flag','bye_clash_pickens']
board[cols].to_csv(OUT + 'board_v7_2026.csv', index=False)

# V6b (doc 57): D/ST and K must be ordered as SEPARATE blocks, D/ST first.
# Sorting them together on raw points puts all 26 kickers ahead of the best defense, and
# ESPN's autodraft walks this list in order -- so a timeout at pick 152 takes a kicker.
_kd  = pool[pool['pos'].isin(STREAMED)]
kdst = pd.concat([_kd[_kd['pos']=='D/ST'].sort_values('proj_leaguepts', ascending=False),
                  _kd[_kd['pos']=='K'   ].sort_values('proj_leaguepts', ascending=False)],
                 ignore_index=True)
kdst[['player','pos','team_c','bye','proj_leaguepts','adp_pick','injury_status']].to_csv(
    OUT + 'board_v7_kdst_separate.csv', index=False)

print(f"\nboard: {len(board)} ranked skill players | K/DST held separately: {len(kdst)}")
print(f"injury flags surfaced inside the top 150: {(board.head(150).flag != '').sum()}")
print(f"week-14 bye clashes with Pickens inside the top 100: {(board.head(100).bye_clash_pickens=='YES').sum()}")

print("\n=== WHO IS ACTUALLY THERE AT EACH OF YOUR PICKS (eff_pick, keeper-depleted) ===")
for pk in MY_PICKS[:8]:
    live = board[(board.eff_pick >= pk - 4) & (board.eff_pick <= pk + 6)].head(4)
    names = ' | '.join(f"{r.player} ({r.pos}{' ⚑' if r.flag else ''}{' bye14' if r.bye_clash_pickens=='YES' else ''})"
                       for r in live.itertuples())
    print(f"  pick {pk:>3}: {names}")

print("\n=== TOP 12 BY VBD, KEEPER-DEPLETED ===")
print(board.head(12)[['rank','player','pos','bye','vbd','adp_pick','eff_pick','flag']].to_string(index=False))


# ============================================================================
# ESPN PRERANK INJECTION FILE — REQUIRED OUTPUT, DO NOT REMOVE
# ============================================================================
# Matt injects the pre-draft ranking straight into ESPN's draft room via
# `espn_draft_injector_Gemini.py` (OneDrive\Fantasy\Scripts). That script does:
#     df = pd.read_csv("ESPN_prerank_with_ids.csv")
#     if "ESPN_ID" not in df.columns: sys.exit(...)
#     ids = df["ESPN_ID"].dropna().astype(int).tolist()
# and it HARD-EXITS on: a missing `ESPN_ID` column, or any duplicate ESPN_ID.
# It silently drops blank IDs with only a warning.
#
# CONTRACT — every board build must emit ESPN_prerank_with_ids.csv with:
#   * a column named EXACTLY `ESPN_ID` (case-sensitive), integer, no nulls, no dupes
#   * rows in FINAL DRAFT PREFERENCE ORDER, top to bottom (row order IS the ranking)
#   * K and D/ST placed LAST — that is how the 4.7/4.8 block move gets applied
#   * predicted keepers EXCLUDED (they are not in the draft pool)
# Extra columns are ignored by the injector, so player/pos/bye/flag are kept for
# eyeballing before the push.
#
# This was missed once (2026-08-25) and cost Matt a round trip. Never ship a board
# without also shipping this file.
# ============================================================================
import sys as _sys
_sys.path.insert(0, '/tmp/build')

# board and kdst both descend from the spine, so espn_id is already on them.
# Do NOT re-merge it -- that produces espn_id_x/espn_id_y and breaks the export.
assert 'espn_id' in board.columns and 'espn_id' in kdst.columns, 'espn_id lost upstream'
_inj = pd.concat([board.assign(_tier=0), kdst.assign(_tier=1)], ignore_index=True)

_missing = _inj[_inj.espn_id.isna()]
assert len(_missing) == 0, (
    f"{len(_missing)} players have no ESPN_ID and would be silently dropped by the "
    f"injector: {list(_missing.player)[:10]}")

_inj = _inj[_inj.espn_id.notna()].copy()
_inj['ESPN_ID'] = _inj.espn_id.astype('int64')
assert _inj.ESPN_ID.is_unique, "duplicate ESPN_IDs — the injector hard-exits on this"

_inj.insert(0, 'prerank', range(1, len(_inj) + 1))
_cols = ['prerank', 'ESPN_ID', 'player', 'pos', 'team_c', 'bye', 'vbd', 'adp_pick', 'flag']
_cols = [c for c in _cols if c in _inj.columns]
_inj[_cols].to_csv(OUT + 'ESPN_prerank_with_ids.csv', index=False)
print(f"\nESPN_prerank_with_ids.csv — {len(_inj)} players, "
      f"K/DST start at {int(_inj[_inj.pos.isin(['K','D/ST'])].prerank.min())}, "
      f"IDs unique={_inj.ESPN_ID.is_unique}, nulls={int(_inj.ESPN_ID.isna().sum())}")
