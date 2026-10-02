#!/usr/bin/env python3
r"""
lane_precision.py -- the cost side of a pedigree-blind usage lane (doc 292). NFL-wide, 2022-2025,
weeks 3-13: every player-week of a NOT-established RB/WR/TE (same filter as emergence_by_tier.py) who is
not already scoring at the bar over his season so far, flagged by (a) snap share at the starter line
that week (RB 50%, WR 65%, TE 60%), (b) scoring the bar that week, (c) both. OUTCOME: his NEXT four
games played average at or above replacement (at least two games). Reports names flagged per week and
the hit rate, by draft tier. One row per player-week, so a player repeats; the clustered count (distinct
player-seasons ever flagged) is printed beside it.
RUN: python lane_precision.py [--years 2019,...,2025]   (default 2022-2025). Tier joins on the PFR id.
INPUTS (nflverse releases, in the folder you run it from): player_stats_<year>.csv, stats_player_week_2025.csv,
roster_weekly_<year>.csv, snap_counts_<year>.csv, draft_picks_all.csv.
RESULT on 11 Sept (doc 292), 2019-2025, weeks 3-13: first flags, snap line AND the bar 26.0% (623), snap line only
16.0% (898), the bar only 13.6% (543); neither 3.8% of all player-weeks. First snap-line week: already 35%+ of snaps,
undrafted 17.8% (107) vs drafted 22.2% (623), p=0.37; a spike from under 35%, undrafted 5.5% (91) vs drafted 14.8%
(203), p=0.031. The spike on 2022-2025 alone (1 of 46, p=0.013) did not replicate on 2019-2021 (4 of 45, p=0.59).
"""
import sys
import numpy as np
import pandas as pd
EV = tuple(int(y) for y in (sys.argv[sys.argv.index('--years') + 1].split(',') if '--years' in sys.argv else '2022,2023,2024,2025'.split(',')))
PRIOR = tuple(sorted(set(EV) | {min(EV) - 1}))

BAR = {'RB': 9.92, 'WR': 9.62, 'TE': 8.25}
LINE = {'RB': 0.50, 'WR': 0.65, 'TE': 0.60}
frames = []
for y in PRIOR:
    if y == 2025:
        frames.append(pd.read_csv('stats_player_week_2025.csv', low_memory=False))
    else:
        frames.append(pd.read_csv(f'player_stats_{y}.csv', low_memory=False).rename(columns={'recent_team': 'team'}))
keep = ['player_id', 'position', 'team', 'season', 'week', 'season_type', 'fantasy_points', 'receptions']
ws = pd.concat([f[[c for c in keep if c in f.columns]] for f in frames], ignore_index=True)
ws = ws[(ws.season_type == 'REG') & ws.position.isin(BAR)].copy()
ws['half'] = ws.fantasy_points.fillna(0) + 0.5 * ws.receptions.fillna(0)
season = ws.groupby(['player_id', 'season']).agg(g=('week', 'count'), ppg=('half', 'mean'),
                                                   pos=('position', 'last')).reset_index()
season['established'] = (season.g >= 6) & (season.ppg >= season.pos.map(BAR))
est = set(zip(season.player_id[season.established], season.season[season.established] + 1))

ros = pd.concat([pd.read_csv(f'roster_weekly_{y}.csv', low_memory=False,
                             usecols=['season', 'gsis_id', 'pfr_id', 'draft_number', 'position'])
                 for y in EV], ignore_index=True).dropna(subset=['gsis_id'])
ros1 = ros.drop_duplicates(['season', 'gsis_id'])
dp = pd.read_csv('draft_picks_all.csv', low_memory=False)[['gsis_id', 'round']].dropna().drop_duplicates('gsis_id')
snaps = pd.concat([pd.read_csv(f'snap_counts_{y}.csv', low_memory=False) for y in EV])
snaps = snaps[(snaps.game_type == 'REG') & snaps.position.isin(BAR)]
snaps = snaps.merge(ros1[['season', 'gsis_id', 'pfr_id']].dropna(), left_on=['season', 'pfr_player_id'],
                    right_on=['season', 'pfr_id'])
pfr_of = snaps.drop_duplicates(['gsis_id']).set_index('gsis_id').pfr_player_id   # for the tier join below
snaps = snaps.groupby(['gsis_id', 'season', 'week']).agg(share=('offense_pct', 'max'), pos=('position', 'last')).reset_index()
pts = ws.groupby(['player_id', 'season', 'week']).half.sum()

snaps = snaps[snaps.season >= min(EV)]
print('EVENT SEASONS', EV)
snaps['half'] = [pts.get((a, b, c), 0.0) for a, b, c in zip(snaps.gsis_id, snaps.season, snaps.week)]
snaps = snaps.sort_values(['gsis_id', 'season', 'week'])
out = []
for (gid, yr), g in snaps.groupby(['gsis_id', 'season']):
    if (gid, yr) in est:
        continue
    pos = g.pos.iloc[-1]; bar, line = BAR[pos], LINE[pos]
    wk, sh, hp = g.week.values, g.share.values, g.half.values
    for i in range(len(g)):
        if not (3 <= wk[i] <= 13):
            continue
        sofar = hp[:i + 1].mean()
        if i >= 1 and hp[:i].mean() >= bar:      # already a startable scorer this season: not a find
            continue
        nxt = hp[i + 1:i + 5]
        if len(nxt) < 2:
            continue
        out.append(dict(gsis_id=gid, season=yr, week=int(wk[i]), pos=pos, snap=sh[i] >= line,
                        scored=hp[i] >= bar, hit=nxt.mean() >= bar))
# TIER, joined on the PFR id that the snap rows carry (draft_picks has it for ~100% of picks since 2010).
# The first version joined on gsis id and fell back to a blank roster draft number, which is thin in
# 2019-2021 rosters and can call a drafted player undrafted. The old label is kept for the diagnostic.
dpp = pd.read_csv('draft_picks_all.csv', low_memory=False)[['pfr_player_id', 'round']].dropna().drop_duplicates('pfr_player_id')
pw = pd.DataFrame(out)
pw['pfr'] = pw.gsis_id.map(pfr_of)
pw = pw.merge(dpp.rename(columns={'pfr_player_id': 'pfr'}), on='pfr', how='left')
pw = pw.merge(ros1[['season', 'gsis_id', 'draft_number']], on=['season', 'gsis_id'], how='left')
old_tier = np.where(pw.draft_number.isna(), 'undrafted', 'drafted')
pw['tier'] = np.where(pw['round'].notna(), np.where(pw['round'] == 1, '1', np.where(pw['round'] <= 3, '2-3', '4-7')), 'undrafted')
print('tier join: no PFR draft row (undrafted)', int((pw.tier == 'undrafted').sum()), 'player-weeks;',
      'of those the roster shows a draft number for', int(((pw.tier == 'undrafted') & (old_tier == 'drafted')).sum()))
weeks = pw.groupby(['season', 'week']).ngroups
order = ['1', '2-3', '4-7', 'undrafted']
print(f'player-weeks {len(pw)} across {weeks} season-weeks; base hit rate {pw.hit.mean():.3f}')
for lab, m in (('snap line, no points', pw.snap & ~pw.scored), ('points, under the snap line', ~pw.snap & pw.scored),
               ('snap line AND points', pw.snap & pw.scored), ('neither', ~pw.snap & ~pw.scored)):
    d = pw[m]
    t = d.groupby('tier').hit.agg(['size', 'mean']).reindex(order)
    per_week = len(d) / weeks
    print(f'\n{lab}: {len(d)} player-weeks = {per_week:.1f} names a week NFL-wide; hit {d.hit.mean():.3f}; '
          f'distinct player-seasons {d.groupby(["gsis_id", "season"]).ngroups}')
    print('   ' + ' | '.join(f'{k}: n={int(r["size"]) if pd.notna(r["size"]) else 0} hit={r["mean"]:.3f}'
                             for k, r in t.iterrows() if pd.notna(r['size'])))

# ONE ROW PER PLAYER-SEASON: the first week he shows the flag (the moment a lane would first name him)
print('\nFIRST FLAG ONLY (one row per player-season; the decision moment)')
for lab, m in (('snap line, no points', pw.snap & ~pw.scored), ('snap line AND points', pw.snap & pw.scored),
               ('points, under the snap line', ~pw.snap & pw.scored)):
    d = pw[m].sort_values('week').drop_duplicates(['gsis_id', 'season'])
    t = d.groupby('tier').hit.agg(['size', 'sum', 'mean']).reindex(order)
    print(f'  {lab}: n={len(d)} hit={d.hit.mean():.3f}   ' + ' | '.join(
        f'{k}: {int(r["sum"])}/{int(r["size"])}={r["mean"]:.3f}' for k, r in t.iterrows() if pd.notna(r['size'])))
from scipy.stats import fisher_exact
d = pw[pw.snap & pw.scored].sort_values('week').drop_duplicates(['gsis_id', 'season'])
u, o = d[d.tier == 'undrafted'].hit, d[d.tier.isin(['2-3', '4-7'])].hit
print(f'  first flag, snap line AND points: undrafted {u.mean():.3f} (n={len(u)}) vs rounds 2-7 {o.mean():.3f} (n={len(o)}), '
      f'Fisher p={fisher_exact([[u.sum(), len(u)-u.sum()], [o.sum(), len(o)-o.sum()]])[1]:.3f}')
d = pw[pw.snap & ~pw.scored].sort_values('week').drop_duplicates(['gsis_id', 'season'])
u, o = d[d.tier == 'undrafted'].hit, d[d.tier.isin(['2-3', '4-7'])].hit
print(f'  first flag, snap line only: undrafted {u.mean():.3f} (n={len(u)}) vs rounds 2-7 {o.mean():.3f} (n={len(o)}), '
      f'Fisher p={fisher_exact([[u.sum(), len(u)-u.sum()], [o.sum(), len(o)-o.sum()]])[1]:.3f}')

# SPLIT THE FIRST FLAG BY WHAT CAME BEFORE: a spike from under 35% of snaps, or a player already in the rotation
prior = {}
for (gid, yr), g in snaps.groupby(['gsis_id', 'season']):
    sh = g.share.values; wk = g.week.values
    for i in range(len(g)):
        prior[(gid, yr, int(wk[i]))] = sh[:i].mean() if i else np.nan
pw['prior'] = [prior.get((a, b, c), np.nan) for a, b, c in zip(pw.gsis_id, pw.season, pw.week)]
f = pw[pw.snap].sort_values('week').drop_duplicates(['gsis_id', 'season']).copy()
f['before'] = np.where(f.prior.isna(), 'first game', np.where(f.prior < 0.35, 'spike from under 35%', 'already 35%+'))
print('\nFIRST SNAP-LINE WEEK, by what came before and tier (hits/n)')
t = f.groupby(['before', 'tier']).hit.agg(['sum', 'size'])
for (b, k), r in t.iterrows():
    print(f'  {b:<22} {k:<10} {int(r["sum"])}/{int(r["size"])} = {r["sum"]/r["size"]:.3f}')
for b in ('spike from under 35%', 'already 35%+'):
    s = f[f.before == b]
    u, o = s[s.tier == 'undrafted'].hit, s[s.tier != 'undrafted'].hit
    print(f'  {b}: undrafted {u.mean():.3f} (n={len(u)}) vs drafted {o.mean():.3f} (n={len(o)}), '
          f'Fisher p={fisher_exact([[u.sum(), len(u)-u.sum()], [o.sum(), len(o)-o.sum()]])[1]:.3f}')

# DIAGNOSTIC for older seasons: the tier rests on draft_picks (gsis id) first and a blank draft number second
print('\nTIER SHARE BY SEASON among flagged player-weeks (a jump in "undrafted" would mean a broken join)')
print(pd.crosstab(pw[pw.snap].season, pw[pw.snap].tier, normalize='index').round(3).to_string())
