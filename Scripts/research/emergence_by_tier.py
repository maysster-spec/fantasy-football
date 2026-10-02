#!/usr/bin/env python3
r"""
emergence_by_tier.py -- how often does a player nobody started become startable mid-season, by
NFL draft tier, undrafted included (doc 292; Matt, 11 Sept: "even undrafted free agent pick ups
nfl teams get can begin to earn enough targets to be fantasy relevant... no sense in ruling it out").

POPULATION: RB/WR/TE regular-season player-seasons 2022-2025 who were NOT an established starter
(last season under the position's rate per game with 6+ games, or no NFL line last season) and who
averaged under that rate in weeks 1-4 or did not play them. Rates are the project's derived
replacement per game: RB 9.92, WR 9.62, TE 8.25 (board WR30 etc. / 17; catalog B1 re-tests them).
OUTCOME: four straight games played in weeks 5-17 averaging at or above the rate (half-PPR).
TIER: NFL round from nflverse draft_picks (gsis_id); undrafted when the weekly roster carries no
draft number. Inputs: nflverse player_stats 2021-2024, stats_player_week_2025, roster_weekly
2021-2025, draft_picks. Prints counts and rates; writes nothing.
RUN: python emergence_by_tier.py [--years 2019,2020,2021,2022,2023,2024,2025]   (default 2022-2025)
INPUTS (nflverse releases, in the folder you run it from; nothing else is read): player_stats_<year>.csv for the
seasons before 2025, stats_player_week_2025.csv, roster_weekly_<year>.csv, draft_picks_all.csv.
RESULT on 11 Sept (doc 292): 2019-2025, 2,504 player-seasons, 355 risers. Round 1 44/155 = 28.4% (12.4% of risers),
rounds 2-3 122/536 = 22.8% (34.4%), rounds 4-7 129/939 = 13.7% (36.3%), undrafted 60/873 = 6.9% (16.9%). A rounds
1-3 gate discards 53%. 2022-2025 alone: 27.7 / 21.6 / 12.6 / 5.7%, undrafted 26 of 194 risers.
"""
import sys
import pandas as pd
EV = tuple(int(y) for y in (sys.argv[sys.argv.index('--years') + 1].split(',') if '--years' in sys.argv else '2022,2023,2024,2025'.split(',')))
PRIOR = tuple(sorted(set(EV) | {min(EV) - 1}))

BAR = {'RB': 9.92, 'WR': 9.62, 'TE': 8.25}
frames = []
for y in PRIOR:
    if y == 2025:
        frames.append(pd.read_csv('stats_player_week_2025.csv', low_memory=False))
    else:
        frames.append(pd.read_csv(f'player_stats_{y}.csv', low_memory=False).rename(columns={'recent_team': 'team'}))
keep = ['player_id', 'player_display_name', 'position', 'team', 'season', 'week', 'season_type',
        'fantasy_points', 'receptions']
ws = pd.concat([f[[c for c in keep if c in f.columns]] for f in frames], ignore_index=True)
ws = ws[(ws.season_type == 'REG') & ws.position.isin(BAR)].copy()
ws['half'] = ws.fantasy_points.fillna(0) + 0.5 * ws.receptions.fillna(0)
ws['bar'] = ws.position.map(BAR)

# last season's rate, for the "not an established starter" filter
season = ws.groupby(['player_id', 'season']).agg(g=('week', 'count'), ppg=('half', 'mean'),
                                                   pos=('position', 'last')).reset_index()
season['bar'] = season.pos.map(BAR)
season['established'] = (season.g >= 6) & (season.ppg >= season.bar)
prior = season[['player_id', 'season', 'established']].copy()
prior['season'] = prior.season + 1
prior = prior.rename(columns={'established': 'est_last'})

# draft tier
dp = pd.read_csv('draft_picks_all.csv', low_memory=False)[['gsis_id', 'round']].dropna().drop_duplicates('gsis_id')
ros = pd.concat([pd.read_csv(f'roster_weekly_{y}.csv', low_memory=False,
                             usecols=['season', 'gsis_id', 'draft_number', 'years_exp'])
                 for y in EV], ignore_index=True)
ros = ros.dropna(subset=['gsis_id']).drop_duplicates(['season', 'gsis_id'])

rows = []
print('EVENT SEASONS', EV)
for (pid, yr), g in ws[ws.season >= min(EV)].groupby(['player_id', 'season']):
    g = g.sort_values('week')
    pos, bar = g.position.iloc[-1], g.bar.iloc[-1]
    early = g[g.week <= 4]
    late = g[(g.week >= 5) & (g.week <= 17)]
    if late.empty:
        continue
    early_ok = early.empty or early.half.mean() < bar
    roll = late.half.rolling(4).mean()
    emerged = bool((roll >= bar).any())
    first = int(late.week.iloc[int((roll >= bar).values.argmax())]) if emerged else None
    rows.append(dict(player_id=pid, season=yr, pos=pos, name=g.player_display_name.iloc[-1],
                     early_below=early_ok, emerged=emerged, first_week=first))
pop = pd.DataFrame(rows).merge(prior, on=['player_id', 'season'], how='left')
pop['est_last'] = pop.est_last.fillna(False).astype(bool)
pop = pop[pop.early_below & ~pop.est_last].copy()
pop = pop.merge(dp, left_on='player_id', right_on='gsis_id', how='left').drop(columns=['gsis_id'])
pop = pop.merge(ros.rename(columns={'gsis_id': 'player_id'}), on=['season', 'player_id'], how='left')

def tier(r):
    if pd.notna(r['round']):
        k = int(r['round'])
        return '1' if k == 1 else ('2-3' if k <= 3 else '4-7')
    if pd.isna(r['draft_number']) and pd.notna(r['years_exp']):
        return 'undrafted'
    return 'unknown'
pop['tier'] = pop.apply(tier, axis=1)
pop['young'] = pop.years_exp.fillna(9) <= 2

print('POPULATION rows', len(pop), '| emerged', int(pop.emerged.sum()),
      '| tier unknown', int((pop.tier == 'unknown').sum()))
order = ['1', '2-3', '4-7', 'undrafted', 'unknown']
t = pop.groupby('tier').agg(n=('emerged', 'size'), hits=('emerged', 'sum')).reindex(order).fillna(0)
t['rate'] = (t.hits / t.n).round(3)
t['share_of_hits'] = (t.hits / t.hits.sum()).round(3)
print(t.to_string())
print('\nby position')
print(pop.groupby(['pos', 'tier']).agg(n=('emerged', 'size'), hits=('emerged', 'sum')).unstack('tier').fillna(0).astype(int).to_string())
print('\nyoung (years_exp <= 2) only')
tt = pop[pop.young].groupby('tier').agg(n=('emerged', 'size'), hits=('emerged', 'sum')).reindex(order).fillna(0)
tt['rate'] = (tt.hits / tt.n).round(3); tt['share_of_hits'] = (tt.hits / tt.hits.sum()).round(3)
print(tt.to_string())
u = pop[(pop.tier == 'undrafted') & pop.emerged].sort_values(['season', 'first_week'])
print('\nundrafted emergences:', len(u))
print(u[['season', 'pos', 'name', 'first_week', 'years_exp']].to_string(index=False))
