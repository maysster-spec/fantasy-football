#!/usr/bin/env python3
r"""
clear_path.py -- Matt's "a clear path to the next man up soaking up enough of that volume" (doc 292,
catalog A9), in testable form:

POPULATION: every NFL team-season 2022-2025 where the RB snap leader to date (2+ games played) misses a
game in weeks 3-15 while his team plays; FIRST game of each absence spell only. The #2 is the back with
the most RB snaps to date behind him. PREDICTOR, knowable before the absence: CONCENTRATION = the #2's
share of all non-leader RB snaps to date (1.0 = he was the only backup who played). OUTCOMES in the
absence game: (a) the #2's share of the team's RB snaps; (b) his half-PPR points at or above the RB bar
9.92; (c) whether the #2 was even the man who got the most RB snaps. Direction, Matt's: a clear path
(high concentration) means he absorbs most of the vacated work and scores; a split backfield does not.
Prints tables; writes nothing.
RUN: python clear_path.py [--years 2019,...,2025]   (default 2022-2025)
INPUTS (nflverse releases, in the folder you run it from): player_stats_<year>.csv, stats_player_week_2025.csv,
roster_weekly_<year>.csv, snap_counts_<year>.csv.
RESULT on 11 Sept (doc 292), 2019-2025, 154 first games of an absence: his share of the backup snaps under 50%
25.0% at the bar (28), 50-70% 31.6% (57), 70-85% 45.7% (35), 85%+ 64.7% (34, median 15.5 points, led the room 88%).
70%+ vs under 55.1% vs 29.4%, p=0.0017. 2019-2021 alone 48.6% vs 28.9%, p=0.10.
"""
import numpy as np
import pandas as pd
from scipy.stats import fisher_exact, spearmanr

import sys
YEARS = tuple(int(y) for y in (sys.argv[sys.argv.index('--years') + 1].split(',') if '--years' in sys.argv else '2022,2023,2024,2025'.split(',')))
frames = []
for y in YEARS:
    frames.append(pd.read_csv('stats_player_week_2025.csv', low_memory=False) if y == 2025 else
                  pd.read_csv(f'player_stats_{y}.csv', low_memory=False).rename(columns={'recent_team': 'team'}))
keep = ['player_id', 'season', 'week', 'season_type', 'fantasy_points', 'receptions', 'carries', 'targets']
ws = pd.concat([f[[c for c in keep if c in f.columns]] for f in frames], ignore_index=True)
ws = ws[ws.season_type == 'REG']
ws['half'] = ws.fantasy_points.fillna(0) + 0.5 * ws.receptions.fillna(0)
pts = ws.groupby(['player_id', 'season', 'week']).half.sum()
opp = ws.assign(o=ws.carries.fillna(0) + ws.targets.fillna(0)).groupby(['player_id', 'season', 'week']).o.sum()

ros = pd.concat([pd.read_csv(f'roster_weekly_{y}.csv', low_memory=False, usecols=['season', 'gsis_id', 'pfr_id'])
                 for y in YEARS]).dropna().drop_duplicates(['season', 'pfr_id'])
sn = pd.concat([pd.read_csv(f'snap_counts_{y}.csv', low_memory=False) for y in YEARS])
sn = sn[(sn.game_type == 'REG') & (sn.position == 'RB')].merge(
    ros, left_on=['season', 'pfr_player_id'], right_on=['season', 'pfr_id'], how='left')
print('SEASONS', YEARS)
print(f'RB snap rows {len(sn)}, joined to gsis {sn.gsis_id.notna().mean():.1%}')
sn['key'] = sn.pfr_player_id                                     # snaps are keyed on pfr, points on gsis
allsn = pd.concat([pd.read_csv(f'snap_counts_{y}.csv', low_memory=False) for y in YEARS])
team_weeks = allsn[allsn.game_type == 'REG'].groupby(['season', 'team']).week.apply(lambda s: sorted(set(s))).to_dict()

rows = []
for (yr, tm), g in sn.groupby(['season', 'team']):
    weeks = team_weeks[(yr, tm)]
    absent_prev = None
    for w in weeks:
        if not (3 <= w <= 15):
            continue
        before = g[g.week < w]
        if before.empty:
            continue
        tot = before.groupby('key').offense_snaps.sum().sort_values(ascending=False)
        games = before.groupby('key').week.nunique()
        lead = tot.index[0]
        if games.get(lead, 0) < 2 or len(tot) < 2:
            continue
        now = g[g.week == w]
        if lead in set(now.key):
            absent_prev = None
            continue
        if absent_prev == lead:                                   # not the first game of the spell
            continue
        absent_prev = lead
        others = tot.drop(lead)
        n2 = others.index[0]
        conc = others.iloc[0] / others.sum()
        share2_before = others.iloc[0] / tot.sum()
        room = now.offense_snaps.sum()
        s2 = now[now.key == n2].offense_snaps.sum()
        top_now = now.groupby('key').offense_snaps.sum().idxmax() if room else None
        gid = now[now.key == n2].gsis_id
        gid = gid.iloc[0] if len(gid) and pd.notna(gid.iloc[0]) else before[before.key == n2].gsis_id.dropna().iloc[0] if before[before.key == n2].gsis_id.notna().any() else None
        p2 = pts.get((gid, yr, w), 0.0) if gid else np.nan
        rows.append(dict(season=yr, team=tm, week=w, n2=before[before.key == n2].player.iloc[0],
                         conc=conc, share2_before=share2_before, n_backs_before=len(others),
                         room_share=(s2 / room) if room else np.nan, played=s2 > 0,
                         was_top=(top_now == n2), pts=p2, opp=opp.get((gid, yr, w), 0.0) if gid else np.nan))
ev = pd.DataFrame(rows).dropna(subset=['pts'])
ev['hit'] = ev.pts >= 9.92
ev['band'] = pd.cut(ev.conc, [0, 0.5, 0.7, 0.85, 1.0001], labels=['under 50%', '50-70%', '70-85%', '85%+'], right=False)
print(f'ABSENCE EVENTS (first game of a spell) {len(ev)}; the #2 played in {ev.played.mean():.1%}')
print(ev.groupby('band', observed=True).agg(n=('hit', 'size'), room_share=('room_share', 'median'),
                                            was_top=('was_top', 'mean'), opp=('opp', 'median'),
                                            pts=('pts', 'median'), hit=('hit', 'mean')).round(3).to_string())
rho, p = spearmanr(ev.conc, ev.room_share, nan_policy='omit')
rho2, p2 = spearmanr(ev.conc, ev.pts)
print(f'\nconcentration vs his share of the room that game: rho {rho:+.3f}, p={p:.4f}')
print(f'concentration vs his points that game:            rho {rho2:+.3f}, p={p2:.4f}')
hi, lo = ev[ev.conc >= 0.7], ev[ev.conc < 0.7]
print(f'clear path (70%+ of the backup snaps) vs not: points at the bar {hi.hit.mean():.3f} (n={len(hi)}) vs '
      f'{lo.hit.mean():.3f} (n={len(lo)}), Fisher p={fisher_exact([[hi.hit.sum(), len(hi)-hi.hit.sum()], [lo.hit.sum(), len(lo)-lo.hit.sum()]])[1]:.4f}')
print(f'  ...and was the man who got the most RB snaps: {hi.was_top.mean():.3f} vs {lo.was_top.mean():.3f}')
rho3, p3 = spearmanr(ev.share2_before, ev.pts)
print(f'alternative predictor, his share of ALL RB snaps before: rho with points {rho3:+.3f}, p={p3:.4f}')
