#!/usr/bin/env python3
r"""
build_weekly.py -- one weekly table for doc 293's low-pedigree study, 2014-2025, RB/WR/TE.

Base: nflverse snap counts (every player who took an offensive snap, keyed on PFR id). Attached: weekly player
stats (gsis id) for points, touches, yards and EPA; PFR weekly advanced stats (2018+) for yards after contact and
broken tackles; weekly rosters for gsis<->pfr, age, experience and status; draft picks for the tier.
JOIN, stated because it decides who is in the population: snap PFR id -> gsis through the weekly roster or the
draft file; where that fails, a normalised name + team + season + position match to the stats rows (research
only, counted). A row still unjoined keeps its snaps with zero points and is COUNTED BY TIER, because an
unjoined undrafted player is exactly the bias this study cannot afford.
Writes r1/weekly.pkl. Prints the join report.
"""
import re
import os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))   # outputs and common.py live beside this file
import pandas as pd

YEARS = list(range(2014, 2026))
POS = ('RB', 'WR', 'TE')
SUFFIX = {'jr', 'sr', 'ii', 'iii', 'iv', 'v'}

def norm(s):
    s = re.sub(r"[.']", '', str(s or '').lower()).replace('-', ' ')
    return ' '.join(t for t in s.split() if t not in SUFFIX)

snaps = pd.concat([pd.read_csv(f'snap_counts_{y}.csv', low_memory=False) for y in YEARS], ignore_index=True)
snaps = snaps[(snaps.game_type == 'REG') & snaps.position.isin(POS)].copy()
snaps = snaps.groupby(['season', 'week', 'team', 'pfr_player_id', 'player', 'position'], as_index=False).agg(
    offense_snaps=('offense_snaps', 'sum'), offense_pct=('offense_pct', 'max'), st_pct=('st_pct', 'max'))

frames = []
for y in YEARS:
    if y == 2025:
        d = pd.read_csv('stats_player_week_2025.csv', low_memory=False)
        d = d.rename(columns={'player_name': 'player_short'})
    else:
        d = pd.read_csv(f'player_stats_{y}.csv', low_memory=False).rename(columns={'recent_team': 'team'})
    d['season'] = y
    frames.append(d)
keep = ['player_id', 'player_display_name', 'position', 'team', 'season', 'week', 'season_type', 'carries', 'rushing_yards',
        'rushing_tds', 'rushing_epa', 'receptions', 'targets', 'receiving_yards', 'receiving_tds', 'receiving_epa',
        'receiving_yards_after_catch', 'fantasy_points']
st = pd.concat([f[[c for c in keep if c in f.columns]] for f in frames], ignore_index=True)
st = st[st.season_type == 'REG'].copy()
st['half'] = st.fantasy_points.fillna(0) + 0.5 * st.receptions.fillna(0)

ros = pd.concat([pd.read_csv(f'roster_weekly_{y}.csv', low_memory=False,
                             usecols=lambda c: c in ('season', 'week', 'team', 'gsis_id', 'pfr_id', 'birth_date', 'years_exp',
                                                     'status', 'draft_number', 'entry_year', 'rookie_year', 'full_name'))
                 for y in YEARS], ignore_index=True)
dp = pd.read_csv('draft_picks_all.csv', low_memory=False)
pfr2g = pd.concat([ros[['pfr_id', 'gsis_id']].dropna().rename(columns={'pfr_id': 'pfr'}),
                   dp[['pfr_player_id', 'gsis_id']].dropna().rename(columns={'pfr_player_id': 'pfr'})]).drop_duplicates('pfr')
snaps = snaps.merge(pfr2g, left_on='pfr_player_id', right_on='pfr', how='left').drop(columns=['pfr'])
path = np.where(snaps.gsis_id.notna(), 'id', '')

# fallback: normalised name + team + season + position against the stats rows of that week
st['nk'] = st.player_display_name.map(norm)
key_st = st.drop_duplicates(['season', 'team', 'position', 'nk'])[['season', 'team', 'position', 'nk', 'player_id']]
dup = st.groupby(['season', 'team', 'position', 'nk']).player_id.nunique()
ambiguous = set(dup[dup > 1].index)
snaps['nk'] = snaps.player.map(norm)
fb = snaps[snaps.gsis_id.isna()].merge(key_st, on=['season', 'team', 'position', 'nk'], how='left')
fb = fb[fb.player_id.notna() & ~fb.set_index(['season', 'team', 'position', 'nk']).index.isin(ambiguous)]
fbmap = fb.drop_duplicates('pfr_player_id').set_index('pfr_player_id').player_id
m = snaps.gsis_id.isna() & snaps.pfr_player_id.isin(fbmap.index)
snaps.loc[m, 'gsis_id'] = snaps.loc[m, 'pfr_player_id'].map(fbmap)
path = np.where(path == 'id', 'id', np.where(snaps.gsis_id.notna(), 'name', 'none'))
snaps['jpath'] = path

w = snaps.merge(st.drop(columns=['position', 'team', 'season_type', 'nk']).rename(columns={'player_id': 'gsis_id'}),
                on=['gsis_id', 'season', 'week'], how='left')
for c in ('carries', 'rushing_yards', 'rushing_tds', 'rushing_epa', 'receptions', 'targets', 'receiving_yards',
          'receiving_tds', 'receiving_epa', 'receiving_yards_after_catch', 'half'):
    w[c] = w[c].fillna(0.0)

adv_r = pd.concat([pd.read_csv(f'advstats_week_rush_{y}.csv') for y in range(2018, 2026)])
adv_c = pd.concat([pd.read_csv(f'advstats_week_rec_{y}.csv') for y in range(2018, 2026)])
adv_r = adv_r[adv_r.game_type == 'REG'].groupby(['season', 'week', 'pfr_player_id'], as_index=False).agg(
    yaco=('rushing_yards_after_contact', 'sum'), btk_r=('rushing_broken_tackles', 'sum'))
adv_c = adv_c[adv_c.game_type == 'REG'].groupby(['season', 'week', 'pfr_player_id'], as_index=False).agg(
    btk_c=('receiving_broken_tackles', 'sum'), drops=('receiving_drop', 'sum'))
w = w.merge(adv_r, on=['season', 'week', 'pfr_player_id'], how='left').merge(adv_c, on=['season', 'week', 'pfr_player_id'], how='left')
w['adv'] = w.season >= 2018
for c in ('yaco', 'btk_r', 'btk_c', 'drops'):
    w[c] = np.where(w.adv, w[c].fillna(0.0), np.nan)

# tier: draft file by gsis, else by pfr; undrafted when neither matches
tg = dp[['gsis_id', 'round']].dropna().drop_duplicates('gsis_id').set_index('gsis_id')['round']
tp = dp[['pfr_player_id', 'round']].dropna().drop_duplicates('pfr_player_id').set_index('pfr_player_id')['round']
rnd = w.gsis_id.map(tg)
rnd = rnd.fillna(w.pfr_player_id.map(tp))
w['round'] = rnd
w['tier'] = np.where(rnd.isna(), 'undrafted', np.where(rnd == 1, '1', np.where(rnd <= 3, '2-3', '4-7')))
w['low'] = w.tier.isin(['4-7', 'undrafted'])

# age and experience from the roster (season level)
rs = ros.dropna(subset=['gsis_id']).sort_values('week').drop_duplicates(['season', 'gsis_id'])[['season', 'gsis_id', 'birth_date', 'years_exp']]
w = w.merge(rs, on=['season', 'gsis_id'], how='left')
w['age'] = (pd.to_datetime(w.season.astype(str) + '-09-01') - pd.to_datetime(w.birth_date, errors='coerce')).dt.days / 365.25

w.to_pickle(os.path.join(HERE, 'weekly.pkl'))
print('rows', len(w), '| join: id', int((w.jpath == 'id').sum()), 'name', int((w.jpath == 'name').sum()), 'none', int((w.jpath == 'none').sum()))
print('unjoined share by season:', w.groupby('season').jpath.apply(lambda s: round((s == 'none').mean(), 3)).to_dict())
print('snap-weighted unjoined by tier (tier from PFR where no gsis):')
t = w.groupby('tier').apply(lambda d: round(d.offense_snaps[d.jpath == 'none'].sum() / d.offense_snaps.sum(), 3))
print(t.to_dict())
