#!/usr/bin/env python3
"""
code_backtest_multiyear.py — extends code_backtest_redteam.py's RT3 (all-manager
value-rule backtest) to 2022 and 2024, using the newly-fixed actuals pull
(espn_projections_{YEAR}_20260824.csv). This is the falsifier doc 21 named:
"re-run the manager-level backtest on 2022, 2023 and 2024. If the rule beats
Lobsinger and Taylor in two of those three years, this is 2025 noise and I withdraw it."

2023 is EXCLUDED. Its own proj_2023 field is broken in the Aug 24 pull: 575 of 700
rows (82%) are exactly 0.0, including literal top-5-overall picks (Christian McCaffrey
ADP 2.07 -> proj_2023=0.0; Tyreek Hill ADP 2.89 -> proj_2023=0.0). actual_2023 is fine.
2022 and 2024 have normal ~21-22% zero rates (bench/irrelevant players), consistent
with a real preseason projection file. This is a NEW defect, not the one doc 39 already
found (doc 39's issue was 58 MISSING players in the old 2022 pull -- that is fixed in
this new pull, verified: Taylor/Jefferson/Hill/Brown/Kamara/Metcalf/Kittle all present
with plausible values). Quarantine 2023 rather than build on it -- directive Section 0 / B1.
"""
import pandas as pd, numpy as np

SRC = 'src/'
d = pd.read_csv(SRC + 'draft_history_2021_2025.csv')

ALIAS = {'Devonta Smith': 'DeVonta Smith', 'Marvin Harrison': 'Marvin Harrison Jr.',
         'Brian Robinson': 'Brian Robinson Jr.', 'Travis Etienne': 'Travis Etienne Jr.',
         'Kenneth Walker': 'Kenneth Walker III', 'Michael Pittman': 'Michael Pittman Jr.',
         'Marvin Mims': 'Marvin Mims Jr.', 'DJ Moore': 'D.J. Moore', 'DJ Chark': 'D.J. Chark Jr.',
         'Gabe Davis': 'Gabriel Davis', 'Josh Palmer': 'Joshua Palmer',
         'Chig Okonkwo': 'Chigoziem Okonkwo', 'Nathaniel Dell': "Tank Dell",
         'Cam Akers': 'Cameron Akers', 'Ken Walker': 'Kenneth Walker III'}

MIN = {'QB': 1, 'RB': 2, 'WR': 2, 'TE': 1, 'D/ST': 1, 'K': 1}
CAP = {'QB': 2, 'TE': 2, 'D/ST': 1, 'K': 1, 'RB': 6, 'WR': 6}
ST = {'QB': 12, 'RB': 30, 'WR': 30, 'TE': 12, 'D/ST': 12, 'K': 12}


def lineup_pts(rows):
    r = pd.DataFrame(rows).dropna(subset=['actual'])
    if not len(r):
        return 0.0
    tot = 0.0
    used = set()
    for p, n in [('QB', 1), ('RB', 2), ('WR', 2), ('TE', 1), ('D/ST', 1), ('K', 1)]:
        g = r[(r['pos'] == p) & (~r.index.isin(used))].nlargest(n, 'actual')
        tot += g['actual'].sum()
        used |= set(g.index)
    fx = r[(r['pos'].isin(['RB', 'WR', 'TE'])) & (~r.index.isin(used))].nlargest(1, 'actual')
    tot += fx['actual'].sum()
    return tot


def run_year(year):
    e = pd.read_csv(SRC + f'espn_projections_{year}_20260824.csv')
    e.columns = [c.replace('﻿', '') for c in e.columns]
    pcol, acol = f'proj_{year}', f'actual_{year}'

    dy = d[d['Year'] == year].copy()
    dy['key'] = dy['Player'].replace(ALIAS)
    ref = e[['Player', 'pos', pcol, acol]].rename(columns={'Player': 'key', 'pos': 'pos_e'})
    dup = ref['key'].duplicated().sum()
    if dup:
        print(f'  [WARN] {dup} duplicate player names in {year} ESPN pull -- dropping dupes, keeping first')
        ref = ref.drop_duplicates(subset='key', keep='first')

    n0 = len(dy)
    dy = dy.merge(ref, on='key', how='left')
    assert len(dy) == n0, f'{year}: merge changed row count {n0} -> {len(dy)}'
    matched = dy[pcol].notna()
    unmatched = sorted(dy.loc[~matched, 'Player'].unique())
    print(f'{year}: JOIN {int(matched.sum())} of {n0} picks carry a {year} projection '
          f'({len(unmatched)} unmatched){" -- " + ", ".join(unmatched[:12]) if unmatched else ""}'
          f'{" ..." if len(unmatched) > 12 else ""}')

    repl = {}
    for p, n in ST.items():
        v = e.loc[e['pos'] == p, pcol].dropna().sort_values(ascending=False)
        repl[p] = float(v.iloc[n - 1]) if len(v) >= n else float(v.min() if len(v) else 0.0)
    dy['vbd'] = dy.apply(lambda r: r[pcol] - repl.get(r['pos_e'], np.nan) if pd.notna(r[pcol]) else np.nan, axis=1)

    pool = dy[dy[pcol].notna()].copy()

    out = []
    for mgr, g in dy.groupby('Manager'):
        keep = g[g['Keeper']]
        sel = g[~g['Keeper']].sort_values('Pick')
        picks = sel['Pick'].tolist()
        counts = {p: 0 for p in MIN}
        roster = []
        real_rows = [dict(Player=r['Player'], pos=r['pos_e'], actual=r[acol]) for _, r in g.iterrows()]
        if len(keep):
            kp = keep.iloc[0]
            counts[kp['pos_e']] = counts.get(kp['pos_e'], 0) + 1
            roster.append(dict(Player=kp['Player'], pos=kp['pos_e'], actual=kp[acol]))
        taken = set(r['Player'] for r in roster)
        for i, pk in enumerate(picks):
            rem = len(picks) - i
            av = pool[(pool['Pick'] >= pk) & (~pool['Player'].isin(taken)) & pool['vbd'].notna()]
            unmet = [p for p, m in MIN.items() if counts.get(p, 0) < m]
            need = sum(max(0, MIN[p] - counts.get(p, 0)) for p in MIN)
            av = av[av['pos_e'].isin(unmet)] if (need >= rem and unmet) else \
                av[av['pos_e'].map(lambda p: counts.get(p, 0) < CAP.get(p, 6))]
            if not len(av):
                continue
            pk2 = av.nlargest(1, 'vbd').iloc[0]
            roster.append(dict(Player=pk2['Player'], pos=pk2['pos_e'], actual=pk2[acol]))
            taken.add(pk2['Player'])
            counts[pk2['pos_e']] = counts.get(pk2['pos_e'], 0) + 1
        out.append(dict(year=year, manager=mgr, n_picks=len(picks),
                         actual=lineup_pts(real_rows), rule=lineup_pts(roster)))
    o = pd.DataFrame(out)
    o['delta'] = o['rule'] - o['actual']
    return o, dy


all_rows = []
for yr in (2022, 2024):
    o, dy = run_year(yr)
    all_rows.append(o)
    print(o.sort_values('delta', ascending=False).to_string(index=False, float_format=lambda x: f"{x:8.1f}"))
    print(f'  rule beat {int((o.delta>0).sum())} of {len(o)} managers | mean {o.delta.mean():+.1f} '
          f'| median {o.delta.median():+.1f} | sd {o.delta.std():.1f}')
    for target in ('Lobsinger', 'R Taylor', 'Matt Mays'):
        row = o[o.manager == target]
        if len(row):
            print(f'    {target}: actual {row.actual.iloc[0]:.1f} vs rule {row.rule.iloc[0]:.1f} '
                  f'(delta {row.delta.iloc[0]:+.1f}, rule {"BEATS" if row.delta.iloc[0]>0 else "LOSES TO"} them)')
    print()

allo = pd.concat(all_rows, ignore_index=True)
allo.to_csv('out/backtest_2022_2024_all_managers.csv', index=False)
print('wrote out/backtest_2022_2024_all_managers.csv')

print('\n' + '=' * 74)
print('CROSS-YEAR SUMMARY, INCLUDING 2025 (from claude/21) FOR COMPARISON')
print('=' * 74)
prior_2025 = pd.DataFrame([
    dict(year=2025, manager='Lobsinger', delta=-196.3),
    dict(year=2025, manager='R Taylor', delta=-182.0),
    dict(year=2025, manager='Rychlicki', delta=-41.1),
])
print('2025 (doc 21): rule LOST to Lobsinger, R Taylor, Rychlicki -- beat 9 of 12 overall, sd(rule)=76 vs sd(actual)=202')
for yr in (2022, 2024):
    sub = allo[allo.year == yr]
    win_rate = f"{int((sub.delta>0).sum())}/{len(sub)}"
    lob = sub[sub.manager == 'Lobsinger']['delta'].iloc[0] if len(sub[sub.manager == 'Lobsinger']) else None
    tay = sub[sub.manager == 'R Taylor']['delta'].iloc[0] if len(sub[sub.manager == 'R Taylor']) else None
    print(f'{yr}: rule beat {win_rate} managers | vs Lobsinger delta {lob:+.1f} | vs R Taylor delta {tay:+.1f} '
          f'| sd(actual)={sub.actual.std():.1f} sd(rule)={sub.rule.std():.1f}')
