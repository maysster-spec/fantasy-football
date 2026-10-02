#!/usr/bin/env python3
r"""
hubbard.py -- doc 293's worked example: Chuba Hubbard (NFL round 4, pick 126, 2021, Carolina) from the data.
Prints Carolina's weekly RB snap shares 2021-2025 and the efficiency of the backs around each change of job.
INPUTS (nflverse releases, in the folder you run it from): snap_counts_2021..2025.csv, player_stats_2021..2024.csv,
stats_player_week_2025.csv, advstats_week_rush_2021..2025.csv, draft_picks_all.csv.
"""
import pandas as pd

Y = [2021, 2022, 2023, 2024, 2025]
dp = pd.read_csv('draft_picks_all.csv', low_memory=False)
print(dp[dp.pfr_player_name == 'Chuba Hubbard'][['season', 'round', 'pick', 'team', 'college']].to_string(index=False))
sn = pd.concat([pd.read_csv(f'snap_counts_{y}.csv', low_memory=False) for y in Y])
sn = sn[(sn.game_type == 'REG') & (sn.position == 'RB') & (sn.team == 'CAR')]
frames = [pd.read_csv(f'player_stats_{y}.csv', low_memory=False).rename(columns={'recent_team': 'team'}) for y in Y[:-1]]
frames.append(pd.read_csv('stats_player_week_2025.csv', low_memory=False))
cols = ['player_display_name', 'season', 'week', 'season_type', 'carries', 'rushing_yards', 'rushing_epa', 'receptions', 'fantasy_points']
ws = pd.concat([f[[c for c in cols if c in f.columns]] for f in frames])
ws = ws[ws.season_type == 'REG']
adv = pd.concat([pd.read_csv(f'advstats_week_rush_{y}.csv') for y in Y])
adv = adv[adv.game_type == 'REG']
for y in Y:
    piv = sn[sn.season == y].pivot_table(index='week', columns='player', values='offense_pct', aggfunc='max').fillna(0)
    piv = (piv[[c for c in piv.columns if piv[c].max() >= 0.25]] * 100).round(0).astype(int)
    print(f'\n{y} Carolina RB snap % by week'); print(piv.T.to_string())

def line(name, yr, w0, w1):
    d = ws[(ws.player_display_name == name) & (ws.season == yr) & ws.week.between(w0, w1)]
    a = adv[(adv.pfr_player_name == name) & (adv.season == yr) & adv.week.between(w0, w1)]
    c = d.carries.sum()
    half = d.fantasy_points.fillna(0) + 0.5 * d.receptions.fillna(0)
    return (f'{name:<19} {yr} wks {w0}-{w1}: games {len(d)}, carries {int(c)}, ypc {d.rushing_yards.sum() / max(c, 1):.2f}, '
            f'EPA/carry {d.rushing_epa.sum() / max(c, 1):+.3f}, YACo/att {a.rushing_yards_after_contact.sum() / max(a.carries.sum(), 1):.2f}, '
            f'half-PPR/g {half.mean():.1f}')
print()
for args in (('Chuba Hubbard', 2021, 3, 8), ("D'Onta Foreman", 2022, 7, 18), ('Chuba Hubbard', 2022, 7, 18),
             ('Miles Sanders', 2023, 1, 5), ('Chuba Hubbard', 2023, 1, 5), ('Miles Sanders', 2023, 7, 18), ('Chuba Hubbard', 2023, 7, 18),
             ('Chuba Hubbard', 2025, 1, 4), ('Rico Dowdle', 2025, 1, 4), ('Rico Dowdle', 2025, 5, 6), ('Chuba Hubbard', 2025, 7, 18),
             ('Rico Dowdle', 2025, 7, 18)):
    print(line(*args))
