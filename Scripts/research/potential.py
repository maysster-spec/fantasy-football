#!/usr/bin/env python3
"""Matt, 2026-09-10: "did you factor in potential value to your waiver/roster recommendations?"
No -- doc 268 priced every add on this year's projection only, which is why every skill claim came
out at +0.00. This puts potential in the SAME CURRENCY as the hole fills.

TESTABLE FORM, stated before running (0.5a2): the value of a potential claim is
E[ points he adds to the nine Matt actually starts ], taken over the MEASURED distribution of what
players clearing that screen went on to score -- not over the hit RATE, and not against replacement,
but against MATT'S OWN LINEUP BAR, which is much higher than replacement.

POPULATION for the screen (4.30): WR seasons 2021-2024, NFL years 1-3, under 9.62 half-PPR ppg,
4+ games, who played 4+ games again the next season. OUTCOME: next season's half-PPR per game.
POPULATION for the rookie screen (4.28): every WR taken in NFL round 1, 2021-2025, 4+ games as a
rookie. OUTCOME: his own rookie half-PPR per game.
Receiving only -- a WR's rushing and return work is not counted, so both are slight under-reads.
"""
import csv, re, unicodedata, collections, statistics as st
import pandas as pd, numpy as np

REG = 'REG'
def half_ppr(y, r, t): return 0.1*y + 0.5*r + 6*t

# --- draft rows: gsis <-> pfr, round, season -------------------------------------------------
dp = pd.read_csv('draft_picks.csv', low_memory=False)
dp = dp[(dp.position == 'WR') & dp.gsis_id.notna()]
dp = dp.rename(columns={'round': 'rnd'})
draft = {r.gsis_id: (int(r.season), int(r.rnd), r.pfr_player_id, r.pfr_player_name)
         for r in dp.itertuples()}

# --- receiving by player-season from play-by-play ---------------------------------------------
rec = {}
for yr in range(2021, 2026):
    d = pd.read_csv(f'play_by_play_{yr}.csv.gz', compression='gzip', low_memory=False,
                    usecols=['receiver_player_id','complete_pass','pass_attempt','yards_gained',
                             'pass_touchdown','play_type','season_type','two_point_attempt'])
    d = d[(d.season_type == REG) & (d.play_type == 'pass') & d.receiver_player_id.notna()
          & (d.two_point_attempt != 1)]
    d['ry'] = d.yards_gained.where(d.complete_pass == 1, 0)
    g = d.groupby('receiver_player_id').agg(tgt=('pass_attempt','sum'), rc=('complete_pass','sum'),
                                            yds=('ry','sum'), td=('pass_touchdown','sum'))
    for pid, row in g.iterrows():
        rec[(pid, yr)] = (float(row.tgt), float(row.rc), float(row.yds), float(row.td))

# --- games played from snap counts (offence snaps > 0), joined on pfr id -----------------------
games = collections.defaultdict(int)
for yr in range(2021, 2026):
    s = pd.read_csv(f'snaps_{yr}.csv', low_memory=False,
                    usecols=['season','game_type','pfr_player_id','offense_snaps','position'])
    s = s[(s.game_type == 'REG') & (s.offense_snaps > 0)]
    for pid, n in s.groupby('pfr_player_id').size().items():
        games[(pid, yr)] = int(n)

def line(gsis, yr):
    if gsis not in draft or (gsis, yr) not in rec: return None
    dseason, rnd, pfr, nm = draft[gsis]
    g = games.get((pfr, yr), 0)
    if g < 4: return None
    tgt, rc, yds, td = rec[(gsis, yr)]
    if tgt < 1: return None
    return dict(name=nm, yr_in_league=yr-dseason+1, rnd=rnd, g=g, tgt=tgt,
                ypt=yds/tgt, tpg=tgt/g, ppg=half_ppr(yds, rc, td)/g)

WR_REPL = 9.62
# ---- 4.30's three-of-three cell, and what those players scored the NEXT year -----------------
cell, base = [], []
for gsis in draft:
    for yr in range(2021, 2025):
        a, b = line(gsis, yr), line(gsis, yr+1)
        if not a or not b: continue
        if not (1 <= a['yr_in_league'] <= 3) or a['ppg'] >= WR_REPL: continue
        sig = sum([a['rnd'] <= 3, a['ypt'] > 7.13, a['tpg'] > 3.20])
        (cell if sig == 3 else base).append(b['ppg'])
print(f"  4.30 population rebuilt: 3-of-3 n={len(cell)}, under-3 n={len(base)}")
print(f"    3-of-3 next-year half-PPR per game: mean {st.mean(cell):.2f}, median {st.median(cell):.2f}, "
      f"max {max(cell):.2f}   startable rate {sum(x>=WR_REPL for x in cell)/len(cell):.1%}")
print(f"    under-3                            mean {st.mean(base):.2f}, "
      f"startable rate {sum(x>=WR_REPL for x in base)/len(base):.1%}")
print(f"    3-of-3 deciles: {[round(np.percentile(cell,p),1) for p in (10,25,50,75,90,100)]}")

# ---- 4.28's first-round rookies, year one ----------------------------------------------------
rook = []
for gsis, (dseason, rnd, pfr, nm) in draft.items():
    if rnd != 1 or not (2021 <= dseason <= 2025): continue
    a = line(gsis, dseason)
    if a: rook.append((a['ppg'], nm, dseason))
rook.sort(reverse=True)
vals = [v for v, _, _ in rook]
print(f"\n  4.28 first-round rookie receivers 2021-2025, n={len(vals)} with 4+ games")
print(f"    rookie half-PPR per game: mean {st.mean(vals):.2f}, median {st.median(vals):.2f}, "
      f"startable rate {sum(v>=WR_REPL for v in vals)/len(vals):.1%}")
print(f"    deciles: {[round(np.percentile(vals,p),1) for p in (10,25,50,75,90,100)]}")
print("    top six: " + ", ".join(f"{n} {v:.1f}" for v, n, _ in rook[:6]))
np.save('dist_3of3.npy', np.array(cell)); np.save('dist_rook1.npy', np.array(vals))
