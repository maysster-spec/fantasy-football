"""What target share does a man ACTUALLY hold while producing at the hit rate?
[doc 432] The bet lane prices every candidate at one archetype hit rate. Nothing in it asks whether
his own offence throws enough for that to be reachable. Matt found it twice in one evening: Cade
Otton, whose ceiling is capped by having no end-zone role, and Malik Washington, whose 26% share is
26% of the 28th-ranked passing game.

TESTABLE FORM, stated before the run: among WR/TE six-week windows where the man averaged the hit
rate or better under this league's scoring, what share of his team's targets did he hold? The top of
that distribution is the most anyone has sustained, and it is the only honest ceiling for a REQUIRED
share. POPULATION: nflverse REG 2021-2025, WR and TE, windows fully inside one season.
"""
import pandas as pd, numpy as np
HIT = 12.71
rows = []
for yr in range(2021, 2026):
    d = pd.read_csv(f'/mnt/user-data/uploads/2026/Scripts/research/_nflverse_cache/stats_player_week_{yr}.csv',
                    low_memory=False)
    d = d[(d['season_type'] == 'REG') & (d['week'].between(1, 17))].copy()
    g = lambda c: pd.to_numeric(d.get(c, 0), errors='coerce').fillna(0)
    d['pts'] = (g('receptions')*0.5 + g('receiving_yards')*0.1 + g('receiving_tds')*6
                + g('rushing_yards')*0.1 + g('rushing_tds')*6
                - (g('receiving_fumbles_lost') + g('rushing_fumbles_lost'))*2)
    d['tgt'] = g('targets')
    tm = d.groupby(['week', 'team'])['tgt'].sum().rename('team_tgt')
    d = d.join(tm, on=['week', 'team'])
    d = d[d['position'].isin(['WR', 'TE'])]
    d['season'] = yr
    rows.append(d[['season', 'week', 'player_display_name', 'position', 'team', 'pts', 'tgt', 'team_tgt']])
a = pd.concat(rows, ignore_index=True)

hits = []
for (yr, p, pos), s in a.groupby(['season', 'player_display_name', 'position']):
    s = s.sort_values('week')
    if len(s) < 6:
        continue
    v, t, tt = s['pts'].values, s['tgt'].values, s['team_tgt'].values
    for i in range(len(s) - 5):
        w = v[i:i+6]
        if w.mean() >= HIT:
            share = t[i:i+6].sum() / tt[i:i+6].sum() if tt[i:i+6].sum() else 0
            hits.append({'pos': pos, 'ppg': w.mean(), 'share': share,
                         'tgt_pg': t[i:i+6].mean(), 'team_pg': tt[i:i+6].mean()})
h = pd.DataFrame(hits)
print(f'six-week windows at {HIT}+ a game, 2021-2025 WR/TE: n={len(h)}')
for pos in ('WR', 'TE'):
    s = h[h['pos'] == pos]
    if not len(s):
        continue
    print(f'\n{pos}  (n={len(s)} windows)')
    print(f'   target share held while producing: median {s["share"].median()*100:.1f}%  '
          f'p90 {s["share"].quantile(.90)*100:.1f}%  p99 {s["share"].quantile(.99)*100:.1f}%  '
          f'max {s["share"].max()*100:.1f}%')
    print(f'   targets a game:                    median {s["tgt_pg"].median():.1f}  '
          f'p90 {s["tgt_pg"].quantile(.90):.1f}  max {s["tgt_pg"].max():.1f}')
    print(f'   his team threw:                    median {s["team_pg"].median():.1f} a game')
print('\nTHE CEILING TO USE AS THE GATE (p99 share, the most anyone has sustained):')
for pos in ('WR', 'TE'):
    s = h[h['pos'] == pos]
    if len(s):
        print(f'   {pos}: {s["share"].quantile(.99)*100:.1f}%   max ever {s["share"].max()*100:.1f}%')
