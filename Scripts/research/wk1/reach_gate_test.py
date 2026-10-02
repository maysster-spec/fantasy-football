#!/usr/bin/env python3
"""reach_gate_test.py -- does the bet lane's reach gate (doc 432) call the men who went on to HIT
"out of reach"? (Matt, 30 Sept: "I still don't understand why we have him as low given upside.")

THE CLAIM IN TESTABLE FORM: on the week-3 population of doc 453 (young receivers, NFL years 1 to 3,
not startable before, read on weeks 1 to 3; outcome startable 9.62+ over weeks 4 to 14 on 4+ games),
apply the page's gate exactly as sheet_engine.reach_check does: need = his targets a game x (12.71 /
his points a game), share = need / his team's targets a game (WR+TE+RB), out of reach when share >
0.378. If the gate marks a large share of the men who HIT as out of reach, the gate's assumption
(his points per target stays where it is) is wrong for this population.
"""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rookie_screen as R

HP, CEIL = 12.71, 0.378

def main():
    d = R.load()
    W = 3
    a = R.table(d, W)
    # team targets a game over weeks 1..W, every WR/TE/RB on the team (the engine's target_load)
    full = pd.concat([pd.read_csv(R._get(f'stats_player_week_{s}.csv', R.NFLV + f'stats_player/stats_player_week_{s}.csv'),
                                  low_memory=False) for s in range(2021, 2026)])
    full = full[(full.season_type == 'REG') & (full.week <= W) & (full.position.isin(['WR', 'TE', 'RB']))]
    full['targets'] = pd.to_numeric(full['targets'], errors='coerce').fillna(0)
    tt = full.groupby(['season', 'team']).agg(tg=('targets', 'sum'), g=('week', 'nunique')).reset_index()
    tt['team_pg'] = tt.tg / tt.g
    # the man's team in weeks 1..W (most common)
    pre = d[d.week <= W]
    tm = pre.groupby(['player_id', 'season'])['team'].agg(lambda s: s.mode().iloc[0]).reset_index()
    a = a.merge(tm, on=['player_id', 'season'], how='left').merge(tt[['season', 'team', 'team_pg']], on=['season', 'team'], how='left')
    a['need'] = a.tpg * (HP / a.ppg_pre.replace(0, np.nan))
    a['share'] = a.need / a.team_pg
    a['gated'] = (a.share > CEIL) | a.share.isna() & (a.ppg_pre <= 0)
    # points per target before and after, for the hits
    post = d[d.week > W].groupby(['player_id', 'season']).agg(tgt_post=('targets', 'sum'), pts_post2=('hppr', 'sum')).reset_index()
    a = a.merge(post, on=['player_id', 'season'], how='left')
    a['ppt_pre'] = a.pts / a.tgt.replace(0, np.nan)
    a['ppt_post'] = a.pts_post2 / a.tgt_post.replace(0, np.nan)
    def cell(mask, label):
        n = int(mask.sum()); k = int(a.loc[mask, 'startable_post'].sum())
        print(f'    {label:<64} {k:>3} of {n:<4} {100*k/n if n else float("nan"):5.1f}%')
    print(f'population: n={len(a)}, hits {int(a.startable_post.sum())}; gate: need = tpg x {HP}/ppg, share = need/team targets a game, out of reach above {CEIL:.1%}')
    print('  the gate on the whole population:')
    cell(a.gated, 'OUT OF REACH by the gate')
    cell(~a.gated, 'in reach')
    print('  the gate on the three-of-three men (the screen):')
    s3 = a.sig == 3
    cell(s3 & a.gated, '3 of 3, OUT OF REACH')
    cell(s3 & ~a.gated, '3 of 3, in reach')
    ub = s3 & (a.ppg_pre < R.BAR)
    print('  three of three AND under the bar (the wire, doc 453 cell):')
    cell(ub & a.gated, '3 of 3, under the bar, OUT OF REACH')
    cell(ub & ~a.gated, '3 of 3, under the bar, in reach')
    hits = a[a.startable_post == 1]
    print(f'  of the {len(hits)} hits in the population, the gate would have called {int(hits.gated.sum())} out of reach')
    h3 = a[(a.startable_post == 1) & s3]
    print(f'  of the {len(h3)} three-of-three hits, {int(h3.gated.sum())} out of reach; their shares at week 3: '
          + ', '.join(f'{x:.0%}' for x in sorted(h3.share.dropna(), reverse=True)))
    print('  points per target, weeks 1-3 -> weeks 4-14, median:')
    for lab, m in [('hits', a.startable_post == 1), ('misses', a.startable_post == 0), ('3 of 3 hits', (a.startable_post == 1) & s3), ('3 of 3 misses', (a.startable_post == 0) & s3)]:
        x = a[m]
        print(f'    {lab:<16} {x.ppt_pre.median():.2f} -> {x.ppt_post.median():.2f}   (n={len(x)}); share of men whose rate ROSE: {(x.ppt_post > x.ppt_pre).mean():.0%}')
    # Bell's shape: 3 of 3, under the bar, share > ceil at week 3
    names = d[['player_id', 'player_display_name']].drop_duplicates('player_id')
    hh = h3.merge(names, on='player_id')
    print('  three-of-three hits and the share the gate would have demanded of each at week 3:')
    for r in hh.sort_values('share', ascending=False).itertuples():
        print(f'    {r.player_display_name:<22} {int(r.season)}  ppg 1-3 {r.ppg_pre:4.1f}  tpg {r.tpg:3.1f}  team {r.team_pg:4.1f}/g  needs {r.share:.0%} {"OUT" if r.gated else ""}  -> {r.ppg_post:.1f} a game after')
    return 0

if __name__ == '__main__':
    sys.exit(main())
