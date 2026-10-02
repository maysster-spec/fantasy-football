#!/usr/bin/env python3
r"""
emergence_lead.py -- for every mid-season emergence in emergence_by_tier.py, what could be seen in the
two games BEFORE the four-game stretch began? (doc 292). Which lane would have named him in time:
a snap lane (share at the starter line in one of those games), a production lane (scored the bar in
one of them), or neither. By draft tier. Same population and outcome as emergence_by_tier.py; the
window START is the first of the four games (that script prints the window's LAST week).
RUN: python emergence_lead.py   (2022-2025)
INPUTS (nflverse releases, in the folder you run it from): player_stats_2021..2024.csv, stats_player_week_2025.csv,
roster_weekly_2022..2025.csv, snap_counts_2022..2025.csv, draft_picks_all.csv.
RESULT on 11 Sept (doc 292): 194 risers. In the two games before the stretch: snap line only 38.1%, both 16.0%,
the bar only 7.7%, neither 36.1%, no game 2.1%. Snap line seen first: round 1 22 of 26, undrafted 11 of 26.
"""
import numpy as np
import pandas as pd

BAR = {'RB': 9.92, 'WR': 9.62, 'TE': 8.25}
LINE = {'RB': 0.50, 'WR': 0.65, 'TE': 0.60}
frames = []
for y in (2021, 2022, 2023, 2024):
    frames.append(pd.read_csv(f'player_stats_{y}.csv', low_memory=False).rename(columns={'recent_team': 'team'}))
frames.append(pd.read_csv('stats_player_week_2025.csv', low_memory=False))
keep = ['player_id', 'player_display_name', 'position', 'team', 'season', 'week', 'season_type',
        'fantasy_points', 'receptions', 'carries', 'targets']
ws = pd.concat([f[[c for c in keep if c in f.columns]] for f in frames], ignore_index=True)
ws = ws[(ws.season_type == 'REG') & ws.position.isin(BAR)].copy()
ws['half'] = ws.fantasy_points.fillna(0) + 0.5 * ws.receptions.fillna(0)
ws['opp'] = ws.carries.fillna(0) + ws.targets.fillna(0)
ws['bar'] = ws.position.map(BAR)

season = ws.groupby(['player_id', 'season']).agg(g=('week', 'count'), ppg=('half', 'mean'),
                                                   pos=('position', 'last')).reset_index()
season['established'] = (season.g >= 6) & (season.ppg >= season.pos.map(BAR))
est = set(zip(season.player_id[season.established], season.season[season.established] + 1))

ros = pd.concat([pd.read_csv(f'roster_weekly_{y}.csv', low_memory=False,
                             usecols=['season', 'gsis_id', 'pfr_id', 'draft_number', 'years_exp'])
                 for y in (2022, 2023, 2024, 2025)], ignore_index=True)
ros = ros.dropna(subset=['gsis_id']).drop_duplicates(['season', 'gsis_id'])
dp = pd.read_csv('draft_picks_all.csv', low_memory=False)[['gsis_id', 'round']].dropna().drop_duplicates('gsis_id')
snaps = pd.concat([pd.read_csv(f'snap_counts_{y}.csv', low_memory=False) for y in (2022, 2023, 2024, 2025)])
snaps = snaps[snaps.game_type == 'REG'].merge(ros[['season', 'gsis_id', 'pfr_id']].dropna(),
                                               left_on=['season', 'pfr_player_id'], right_on=['season', 'pfr_id'])
share = snaps.set_index(['gsis_id', 'season', 'week']).offense_pct.groupby(level=[0, 1, 2]).max()

rows = []
for (pid, yr), g in ws[ws.season >= 2022].groupby(['player_id', 'season']):
    if (pid, yr) in est:
        continue
    g = g.sort_values('week')
    pos, bar = g.position.iloc[-1], g.bar.iloc[-1]
    early, late = g[g.week <= 4], g[(g.week >= 5) & (g.week <= 17)]
    if late.empty or (not early.empty and early.half.mean() >= bar):
        continue
    roll = late.half.rolling(4).mean()
    if not (roll >= bar).any():
        continue
    end_i = int((roll >= bar).values.argmax())
    start_week = int(late.week.iloc[end_i - 3])
    before = g[g.week < start_week].tail(2)
    sh = [share.get((pid, yr, w), np.nan) for w in before.week]
    snap_seen = any((s >= LINE[pos]) for s in sh if not np.isnan(s))
    prod_seen = bool((before.half >= bar).any())
    rows.append(dict(player_id=pid, season=yr, pos=pos, name=g.player_display_name.iloc[-1],
                     start_week=start_week, n_before=len(before),
                     share_before=np.nanmean(sh) if sh and not all(np.isnan(sh)) else np.nan,
                     opp_before=before.opp.mean() if len(before) else np.nan,
                     snap_seen=snap_seen, prod_seen=prod_seen))
em = pd.DataFrame(rows).merge(dp, left_on='player_id', right_on='gsis_id', how='left')
em = em.merge(ros.rename(columns={'gsis_id': 'player_id'})[['season', 'player_id', 'draft_number', 'years_exp']],
              on=['season', 'player_id'], how='left')
em['tier'] = np.where(em['round'].notna(), np.where(em['round'] == 1, '1', np.where(em['round'] <= 3, '2-3', '4-7')),
                      np.where(em.draft_number.isna(), 'undrafted', '4-7'))
em['lane'] = np.select([em.snap_seen & em.prod_seen, em.snap_seen, em.prod_seen],
                       ['both', 'snaps only', 'points only'], 'neither')
em.loc[em.n_before == 0, 'lane'] = 'no game before'
print('EMERGENCES', len(em))
order = ['1', '2-3', '4-7', 'undrafted']
t = pd.crosstab(em.tier, em.lane).reindex(order)
t['n'] = t.sum(axis=1)
print(t.to_string())
print('\nshare of emergences visible in the two games before, by lane')
print((em.lane.value_counts(normalize=True).round(3)).to_string())
print('\nmedian snap share and opportunities (carries+targets) per game in the two games before, by tier')
print(em.groupby('tier').agg(share=('share_before', 'median'), opp=('opp_before', 'median')).reindex(order).round(2).to_string())
u = em[em.tier == 'undrafted'].sort_values(['season', 'start_week'])
print('\nundrafted:')
print(u[['season', 'pos', 'name', 'start_week', 'years_exp', 'share_before', 'opp_before', 'lane']].round(2).to_string(index=False))
