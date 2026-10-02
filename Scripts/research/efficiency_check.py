#!/usr/bin/env python3
r"""
efficiency_check.py -- Matt's performance metrics, in the two forms that decide whether they can carry
the in-season signal he means (doc 292, catalog B11). nflverse pfr_advstats weekly 2022-2025 and
player_stats weekly; NGS separation where it exists.

(1) DO THEY REPEAT AT A BACKUP'S VOLUME? Within each season, split a player's games into odd and even
weeks and correlate the metric between the halves, by volume per half. A number that does not repeat
cannot predict anything. Benchmarks: carries per game (RB) and targets per game (WR/TE), volume stats.
   RB:    yards after contact per carry; broken tackles per touch (rush + receiving).
   WR/TE: yards after catch per reception; broken tackles per reception; yards per target.
(2) DO THEY ADD TO WHAT THE USAGE ALREADY SAYS? Population: lane_precision.py's first snap-line week per
non-established player-season, weeks 3-13. Efficiency to date = season to date through the flag week
(volume floors: RB 15 carries, WR/TE 5 receptions). Outcome: next four games at the bar. Split at the
position's median efficiency among flagged players; within 'scored the bar that week' and 'did not'.
Direction, Matt's: above-median efficiency converts more. Prints tables; writes nothing.
RUN: python efficiency_check.py [--years 2019,...,2025]   (default 2022-2025)
INPUTS (nflverse releases, in the folder you run it from): advstats_week_rush_<year>.csv, advstats_week_rec_<year>.csv,
player_stats_<year>.csv, stats_player_week_2025.csv, roster_weekly_<year>.csv, snap_counts_<year>.csv,
draft_picks_all.csv.
RESULT on 11 Sept (doc 292), 2019-2025. Split-half r at backup volume: RB yards after contact a carry +0.55,
broken tackles a touch +0.21 (carries a game +0.65); WR YAC a catch +0.32, broken tackles +0.15, yards a target
+0.14 (targets a game +0.59); TE +0.18, +0.21, +0.13 (+0.60). Added to usage at the first snap-line week: 16
splits, 10 lean his way, two in both periods (receiver broken tackles with the bar, pooled p=0.020; tight-end yards a
target with the bar, p=0.025), none under 0.05/16. UNDERPOWERED.
"""
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, fisher_exact

import sys
YEARS = tuple(int(y) for y in (sys.argv[sys.argv.index('--years') + 1].split(',') if '--years' in sys.argv else '2022,2023,2024,2025'.split(',')))
PRIOR = tuple(sorted(set(YEARS) | {min(YEARS) - 1}))
BAR = {'RB': 9.92, 'WR': 9.62, 'TE': 8.25}
LINE = {'RB': 0.50, 'WR': 0.65, 'TE': 0.60}

ru = pd.concat([pd.read_csv(f'advstats_week_rush_{y}.csv') for y in YEARS])
rc = pd.concat([pd.read_csv(f'advstats_week_rec_{y}.csv') for y in YEARS])
ru, rc = ru[ru.game_type == 'REG'], rc[rc.game_type == 'REG']
ros = pd.concat([pd.read_csv(f'roster_weekly_{y}.csv', low_memory=False,
                             usecols=['season', 'gsis_id', 'pfr_id', 'position', 'draft_number'])
                 for y in YEARS]).dropna(subset=['gsis_id', 'pfr_id']).drop_duplicates(['season', 'pfr_id'])
frames = [pd.read_csv('stats_player_week_2025.csv', low_memory=False) if y == 2025 else
          pd.read_csv(f'player_stats_{y}.csv', low_memory=False).rename(columns={'recent_team': 'team'}) for y in PRIOR]
keep = ['player_id', 'position', 'season', 'week', 'season_type', 'fantasy_points', 'receptions', 'carries',
        'targets', 'receiving_yards', 'receiving_yards_after_catch']
ws = pd.concat([f[[c for c in keep if c in f.columns]] for f in frames], ignore_index=True)
ws = ws[(ws.season_type == 'REG') & ws.position.isin(BAR)].copy()
ws['half'] = ws.fantasy_points.fillna(0) + 0.5 * ws.receptions.fillna(0)

# one weekly frame keyed on gsis id
ru = ru.merge(ros[['season', 'pfr_id', 'gsis_id']], left_on=['season', 'pfr_player_id'], right_on=['season', 'pfr_id'])
rc = rc.merge(ros[['season', 'pfr_id', 'gsis_id']], left_on=['season', 'pfr_player_id'], right_on=['season', 'pfr_id'])
wk = ws.rename(columns={'player_id': 'gsis_id'}).merge(
    ru[['gsis_id', 'season', 'week', 'rushing_yards_after_contact', 'rushing_broken_tackles']],
    on=['gsis_id', 'season', 'week'], how='left').merge(
    rc[['gsis_id', 'season', 'week', 'receiving_broken_tackles']], on=['gsis_id', 'season', 'week'], how='left')
for c in ('carries', 'receptions', 'targets', 'receiving_yards', 'receiving_yards_after_catch',
          'rushing_yards_after_contact', 'rushing_broken_tackles', 'receiving_broken_tackles'):
    wk[c] = wk[c].fillna(0)
wk['btk'] = wk.rushing_broken_tackles + wk.receiving_broken_tackles
wk['touch'] = wk.carries + wk.receptions

def metrics(d, pos):
    if pos == 'RB':
        c, t = d.carries.sum(), d.touch.sum()
        return dict(vol=c, yaco=d.rushing_yards_after_contact.sum() / c if c else np.nan,
                    btk=d.btk.sum() / t if t else np.nan, cpg=c / len(d))
    r, tg = d.receptions.sum(), d.targets.sum()
    return dict(vol=r, yac=d.receiving_yards_after_catch.sum() / r if r else np.nan,
                btk=d.receiving_broken_tackles.sum() / r if r else np.nan,
                ypt=d.receiving_yards.sum() / tg if tg else np.nan, tpg=tg / len(d))

print('(1) SPLIT-HALF: odd weeks vs even weeks, same season. r (n player-seasons)')
for pos, names, bands in (('RB', ['yaco', 'btk', 'cpg'], [(10, 30), (30, 60), (60, 999)]),
                          ('WR', ['yac', 'btk', 'ypt', 'tpg'], [(5, 15), (15, 30), (30, 999)]),
                          ('TE', ['yac', 'btk', 'ypt', 'tpg'], [(5, 15), (15, 30), (30, 999)])):
    rows = []
    for (gid, yr), g in wk[wk.position == pos].groupby(['gsis_id', 'season']):
        a, b = metrics(g[g.week % 2 == 1], pos), metrics(g[g.week % 2 == 0], pos)
        rows.append(dict(vol=min(a['vol'], b['vol']), **{f'{k}_a': a[k] for k in names}, **{f'{k}_b': b[k] for k in names}))
    df = pd.DataFrame(rows)
    for lo, hi in bands:
        d = df[(df.vol >= lo) & (df.vol < hi)]
        out = []
        for k in names:
            x = d[[f'{k}_a', f'{k}_b']].dropna()
            out.append(f'{k} {pearsonr(x.iloc[:, 0], x.iloc[:, 1])[0]:+.2f}' if len(x) > 10 else f'{k} n/a')
        unit = 'carries' if pos == 'RB' else 'catches'
        print(f'  {pos} {lo}-{hi if hi < 999 else "+"} {unit} per half (n={len(d)}): ' + ' | '.join(out))

# (2) added value on the first snap-line week
snaps = pd.concat([pd.read_csv(f'snap_counts_{y}.csv', low_memory=False) for y in YEARS])
snaps = snaps[(snaps.game_type == 'REG') & snaps.position.isin(BAR)].merge(
    ros[['season', 'pfr_id', 'gsis_id', 'draft_number']], left_on=['season', 'pfr_player_id'], right_on=['season', 'pfr_id'])
share = snaps.groupby(['gsis_id', 'season', 'week']).offense_pct.max()
season = ws.groupby(['player_id', 'season']).agg(g=('week', 'count'), ppg=('half', 'mean'), pos=('position', 'last')).reset_index()
season['established'] = (season.g >= 6) & (season.ppg >= season.pos.map(BAR))
est = set(zip(season.player_id[season.established], season.season[season.established] + 1))
dp = pd.read_csv('draft_picks_all.csv', low_memory=False)[['gsis_id', 'round']].dropna().drop_duplicates('gsis_id')
ev = []
print('EVENT SEASONS', YEARS)
for (gid, yr), g in wk[wk.season >= min(YEARS)].sort_values('week').groupby(['gsis_id', 'season']):
    if (gid, yr) in est:
        continue
    pos = g.position.iloc[-1]; bar = BAR[pos]
    g = g.reset_index(drop=True)
    for i in range(len(g)):
        w = int(g.week[i])
        if not (3 <= w <= 13):
            continue
        if i >= 1 and g.half[:i].mean() >= bar:
            break
        if share.get((gid, yr, w), 0) < LINE[pos]:
            continue
        nxt = g.half[i + 1:i + 5]
        if len(nxt) < 2:
            break
        m = metrics(g[:i + 1], pos)
        floor = 15 if pos == 'RB' else 5
        ev.append(dict(gsis_id=gid, season=yr, pos=pos, week=w, scored=g.half[i] >= bar, hit=nxt.mean() >= bar,
                       vol=m['vol'], eff1=m['yaco'] if pos == 'RB' else m['yac'], btk=m['btk'],
                       ypt=m.get('ypt', np.nan), enough=m['vol'] >= floor))
        break
ev = pd.DataFrame(ev)
print(f'\n(2) FIRST SNAP-LINE WEEK: {len(ev)} player-seasons; with enough volume to date for an efficiency number: '
      f'{int(ev.enough.sum())} ({ev.enough.mean():.0%}). Base hit rate {ev.hit.mean():.3f}; '
      f'with enough volume {ev[ev.enough].hit.mean():.3f}, without {ev[~ev.enough].hit.mean():.3f}')
d = ev[ev.enough].copy()
for pos in ('RB', 'WR', 'TE'):
    s = d[d.pos == pos]
    for col, lab in (('eff1', 'YAC per carry' if pos == 'RB' else 'YAC per catch'), ('btk', 'broken tackles per touch'),
                     ('ypt', 'yards per target')):
        if s[col].notna().sum() < 20:
            continue
        med = s[col].median()
        for sc in (True, False):
            t = s[s.scored == sc].dropna(subset=[col])
            hi, lo = t[t[col] > med].hit, t[t[col] <= med].hit
            if len(hi) < 5 or len(lo) < 5:
                continue
            p = fisher_exact([[hi.sum(), len(hi) - hi.sum()], [lo.sum(), len(lo) - lo.sum()]])[1]
            print(f'  {pos} {lab:<24} scored that week={str(sc):<5} above median {hi.mean():.3f} (n={len(hi)}) '
                  f'vs at/below {lo.mean():.3f} (n={len(lo)}), p={p:.3f}')
