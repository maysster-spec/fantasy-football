#!/usr/bin/env python3
"""
code_backtest_redteam_v2.py — adversarial re-test of doc 40. Writes claude/41.

WHAT THIS CHANGES vs code_backtest_multiyear.py (doc 40) and code_backtest_redteam.py (doc 21):
  Both prior scripts let the greedy policy take K and D/ST whenever their VBD topped the board.
  Measured: median overall pick used on K/D-ST was 75, with 36 of 48 inside pick 108. Directive
  4.7 says the league's median first D/ST is round 12 and 95.8% of team-seasons take their first
  K at round 11+; 4.8 says that draft value is not realizable at all because everyone streams.
  So the prior policy was a strawman. V1 below adds ONE constraint -- no K/D-ST before KDST_DEADLINE
  -- and changes nothing else. Effect: +105.6 pts per manager-season, 20 of 24 improved.

  It also adds 2025 so all three seasons run on identical code (doc 40 compared its own numbers
  against doc 21's separately-computed 2025 figure). 2025 V0 reproduces doc 21's 9-of-12 exactly.

2023 IS EXCLUDED AND THAT IS FINAL. Confirmed twice against raw payloads: ESPN serves no 2023
preseason projections. Of 178 players drafted in 2023, 18 carry a usable proj_2023.

Usage: python code_backtest_redteam_v2.py --src <dir>
"""
import argparse
import pandas as pd, numpy as np

ALIAS = {'Devonta Smith':'DeVonta Smith','Marvin Harrison':'Marvin Harrison Jr.',
         'Brian Robinson':'Brian Robinson Jr.','Travis Etienne':'Travis Etienne Jr.',
         'Kenneth Walker':'Kenneth Walker III','Michael Pittman':'Michael Pittman Jr.',
         'Marvin Mims':'Marvin Mims Jr.','DJ Moore':'D.J. Moore','Gabe Davis':'Gabriel Davis',
         'Chig Okonkwo':'Chigoziem Okonkwo','Cam Akers':'Cameron Akers'}
MIN = {'QB':1,'RB':2,'WR':2,'TE':1,'D/ST':1,'K':1}
CAP = {'QB':2,'TE':2,'D/ST':1,'K':1,'RB':6,'WR':6}
ST  = {'QB':12,'RB':30,'WR':30,'TE':12,'D/ST':12,'K':12}
KDST_DEADLINE = 121   # round 11, per directive 4.7. Sensitivity swept in doc 41 RT-2.
FILES = {2022:('espn_projections_2022_20260824.csv','proj_2022','actual_2022'),
         2024:('espn_projections_2024_20260824.csv','proj_2024','actual_2024'),
         2025:('espn_projections_2026_20260820.csv','proj_2025','actual_2025')}


def lineup_pts(rows):
    r = pd.DataFrame(rows).dropna(subset=['actual'])
    if not len(r):
        return 0.0
    tot, used = 0.0, set()
    for p, n in [('QB',1),('RB',2),('WR',2),('TE',1),('D/ST',1),('K',1)]:
        g = r[(r['pos']==p) & (~r.index.isin(used))].nlargest(n,'actual')
        tot += g['actual'].sum(); used |= set(g.index)
    tot += r[(r['pos'].isin(['RB','WR','TE'])) & (~r.index.isin(used))].nlargest(1,'actual')['actual'].sum()
    return tot


def run_year(src, d, year, kdst_deadline):
    f, pcol, acol = FILES[year]
    e = pd.read_csv(src + f); e.columns = [c.replace('﻿','') for c in e.columns]
    dy = d[d['Year']==year].copy(); dy['key'] = dy['Player'].replace(ALIAS)
    ref = e[['Player','pos',pcol,acol]].rename(columns={'Player':'key','pos':'pos_e'})
    ref = ref.drop_duplicates(subset='key', keep='first')
    n0 = len(dy); dy = dy.merge(ref, on='key', how='left')
    assert len(dy)==n0, f'{year}: merge changed row count'
    repl = {p: float(e.loc[e['pos']==p, pcol].dropna().sort_values(ascending=False).iloc[n-1])
            for p, n in ST.items()}
    dy['vbd'] = dy[pcol] - dy['pos_e'].map(repl)
    pool = dy[dy[pcol].notna()].copy()

    out = []
    for mgr, g in dy.groupby('Manager'):
        keep = g[g['Keeper']]; sel = g[~g['Keeper']].sort_values('Pick')
        counts = {p:0 for p in MIN}; roster = []
        real = [dict(Player=r['Player'], pos=r['pos_e'], actual=r[acol]) for _, r in g.iterrows()]
        if len(keep):
            kp = keep.iloc[0]
            counts[kp['pos_e']] = counts.get(kp['pos_e'],0)+1
            roster.append(dict(Player=kp['Player'], pos=kp['pos_e'], actual=kp[acol]))
        taken = {r['Player'] for r in roster}
        picks = sel['Pick'].tolist()
        for i, pk in enumerate(picks):
            rem = len(picks) - i
            av = pool[(pool['Pick']>=pk) & (~pool['Player'].isin(taken)) & pool['vbd'].notna()]
            unmet = [p for p,m in MIN.items() if counts.get(p,0) < m]
            need = sum(max(0, MIN[p]-counts.get(p,0)) for p in MIN)
            if need >= rem and unmet:
                av = av[av['pos_e'].isin(unmet)]
            else:
                av = av[av['pos_e'].map(lambda p: counts.get(p,0) < CAP.get(p,6))]
                if kdst_deadline and pk < kdst_deadline:
                    av = av[~av['pos_e'].isin(['K','D/ST'])]
            if not len(av):
                continue
            c = av.nlargest(1,'vbd').iloc[0]
            roster.append(dict(Player=c['Player'], pos=c['pos_e'], actual=c[acol]))
            taken.add(c['Player']); counts[c['pos_e']] = counts.get(c['pos_e'],0)+1
        out.append(dict(year=year, manager=mgr, actual=lineup_pts(real), rule=lineup_pts(roster)))
    o = pd.DataFrame(out); o['delta'] = o['rule'] - o['actual']
    return o


def main(src, out):
    d = pd.read_csv(src + 'draft_history_2021_2025.csv')
    frames = {}
    print(f"{'year':>6} {'V0 beats':>9} {'V0 mean':>9} {'V1 beats':>9} {'V1 mean':>9}")
    for yr in (2022, 2024, 2025):
        v0 = run_year(src, d, yr, None)
        v1 = run_year(src, d, yr, KDST_DEADLINE)
        frames[yr] = (v0, v1)
        print(f"{yr:>6} {int((v0.delta>0).sum()):>6}/12 {v0.delta.mean():>+9.1f} "
              f"{int((v1.delta>0).sum()):>6}/12 {v1.delta.mean():>+9.1f}")
    a0 = pd.concat([frames[y][0] for y in frames]); a1 = pd.concat([frames[y][1] for y in frames])
    print(f"\npooled n={len(a1)}")
    print(f"  V0 beats {int((a0.delta>0).sum())}/{len(a0)} | mean {a0.delta.mean():+.1f}")
    print(f"  V1 beats {int((a1.delta>0).sum())}/{len(a1)} | mean {a1.delta.mean():+.1f}")
    b = [np.random.default_rng(s).choice(a1.delta.values, len(a1), replace=True).mean() for s in range(4000)]
    lo, hi = np.percentile(b, [2.5, 97.5])
    print(f"  V1 bootstrap 95% CI [{lo:+.1f}, {hi:+.1f}] -> {'EXCLUDES' if lo>0 or hi<0 else 'INCLUDES'} zero")
    print("\nbetween-year means (the variance doc 21 did not measure):")
    for yr in (2022, 2024, 2025):
        v1 = frames[yr][1]
        print(f"  {yr}: league {v1.actual.mean():7.1f} | rule {v1.rule.mean():7.1f}")
    a1.to_csv(out + 'backtest_redteam_v2_all_managers.csv', index=False)
    print(f"\nwrote {out}backtest_redteam_v2_all_managers.csv")


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--src', default='src/'); ap.add_argument('--out', default='out/')
    a = ap.parse_args(); main(a.src, a.out)
