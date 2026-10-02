#!/usr/bin/env python3
"""build_dst.py: every regular-season team-week of D/ST points under THIS LEAGUE'S rules, 2021-2025.

Writes Source/dst_weekly_2021_2025.csv (resolved against this file: Scripts/research/../../Source),
one row per defence per game week, columns
    season, week, team, opp, allowed, sack, int, fr, saf, dtd, blk, fuml, dst_pts

    py build_dst.py                 writes Source/dst_weekly_2021_2025.csv
    py build_dst.py --out x.csv     writes somewhere else (a dry run)

WHAT CHANGED AND WHY (doc 440, 29 Sept 2026). Two defects in the builder that produced the shipped
file (this file's 2025-only ancestor, doc 264, looped over five seasons as dst_all.py, doc 265):

1. IT DROPPED EVERY TEAM-WEEK WITH NO DEFENSIVE EVENT. The old builder accumulated events in a dict
   keyed by (week, defence) and then wrote one row per dict KEY. A defence that recorded no sack,
   interception, recovery, safety or touchdown that week never got a key, so a week scored by the
   points-allowed band alone never got a row. 142 of 2,718 team-weeks were missing (the shipped file
   has 2,576), every one of them a bad week (mean base points -3.88), so the published week mean and
   D/ST12 were both too high. This version iterates the GAMES: both teams of every regular-season
   game in play-by-play get a row, and the events are looked up, zero when there are none.
   A full regular season is 544 team-weeks (32 teams x 17 games); 2022 has 542 because BUF at CIN in
   week 17 was cancelled and is absent from play-by-play. The script prints the count per season and
   stops if a game has no final score rather than silently dropping it.

2. IT CARRIED NO BLOCKED-KICK TERM AND NO FUMBLE-LOST TERM, both of which the league scores under the
   D/ST header (2026_League_Settings.txt lines 74-95: blocked punt/PAT/FG +2, fumble lost -2).
   Definitions, as stated in price_dst_k_terms.py BEFORE anything was counted (that script reproduced
   all 2,576 shipped dst_pts with zero mismatches before adding either term):
     blk  (+2 each) a blocked field goal, PAT or punt, credited to the defending unit, nflverse
          defteam (on a punt defteam is the receiving team, which is the team that blocks it):
              field_goal_result == 'blocked'  or  extra_point_result == 'blocked'  or  punt_blocked == 1
     fuml (-2 each) a fumble lost by the RETURN or DEFENSIVE unit: fumble_lost == 1 and the fumbling
          team (fumbled_1_team) is the unit's side, which is
              posteam on a kickoff   (nflverse marks the RECEIVING team as posteam on kickoffs)
              defteam on a punt      (the receiving team)
              defteam on any other play (a defender fumbling back an interception or fumble return)
          A fumble the offence loses on a scrimmage play is the player's, not the unit's, and is not
          charged; a kicking team fumbling its own kick (a bad snap) is not charged either.

   dst_pts = sack*1 + int*2 + fr*2 + saf*4 + dtd*6 + band(allowed) + 2*blk - 2*fuml

The old columns (season, week, team, opp, allowed, sack, int, fr, saf, dtd) are computed exactly as
before and are unchanged on every row the old file had, and on those rows
old dst_pts == new dst_pts - 2*blk + 2*fuml. Proved row for row in run_build_dst_check.txt (doc 440).

STILL NOT COUNTED, on purpose, so the old columns stay identical (price_dst_k_terms.py priced both as
asides): a kickoff-return touchdown by the receiving team (td_team == posteam on a kickoff, which the
dtd test excludes; about +0.07 a week) and the punting team recovering a muffed punt (fr requires the
recovering team to be defteam; about +0.08 a week). Adding either changes dtd or fr on existing rows.

Points-allowed bands are SECTION 2 / 2026_League_Settings.txt lines 74-95, read not assumed. The file
lists EIGHT bands; 18-21 is absent and is taken as 0. Flagged, not measured.

Play-by-play comes from nflverse and is cached in _nflverse_cache beside this file (the folder
k12_replacement.py already uses); a copy beside the script itself is also accepted. Standard library
plus pandas; paths resolve against this file, never the shell (doc 144).
"""
import argparse
import csv
import gzip
import os
import statistics as st
import sys
import urllib.request

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, '_nflverse_cache')
DEFAULT_OUT = os.path.normpath(os.path.join(HERE, '..', '..', 'Source', 'dst_weekly_2021_2025.csv'))
SEASONS = (2021, 2022, 2023, 2024, 2025)
PBP_URL = 'https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_{}.csv.gz'
PBP_COLS = ['season', 'week', 'season_type', 'game_id', 'play_type', 'posteam', 'defteam',
            'home_team', 'away_team', 'total_home_score', 'total_away_score',
            'sack', 'interception', 'safety', 'fumble_lost', 'fumbled_1_team',
            'fumble_recovery_1_team', 'touchdown', 'td_team',
            'field_goal_result', 'extra_point_result', 'punt_blocked']
OUT_COLS = ['season', 'week', 'team', 'opp', 'allowed', 'sack', 'int', 'fr', 'saf', 'dtd',
            'blk', 'fuml', 'dst_pts']

# SECTION 2 / 2026_League_Settings.txt lines 74-95, READ not assumed.
# NOTE: the file lists EIGHT bands; 18-21 is absent and is taken as 0. Flagged, not measured.
BANDS = [(0, 0, 10), (1, 6, 7), (7, 13, 4), (14, 17, 1), (18, 21, 0),
         (22, 27, -1), (28, 34, -4), (35, 45, -7), (46, 999, -10)]


def pa_points(pts):
    for lo, hi, v in BANDS:
        if lo <= pts <= hi:
            return v
    return -10


def pbp_path(yr):
    """The cached play-by-play file for one season, downloaded if it is nowhere beside this script."""
    for folder in (CACHE, HERE):
        path = os.path.join(folder, 'play_by_play_{}.csv.gz'.format(yr))
        if os.path.exists(path) and os.path.getsize(path) > 1_000_000:
            return path
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, 'play_by_play_{}.csv.gz'.format(yr))
    print('downloading {} -> {}'.format(PBP_URL.format(yr), path))
    urllib.request.urlretrieve(PBP_URL.format(yr), path)
    if not os.path.exists(path) or os.path.getsize(path) < 1_000_000:
        raise SystemExit('{}: download failed or is too small'.format(path))
    return path


def load_pbp(yr):
    with gzip.open(pbp_path(yr), 'rt', encoding='utf-8', errors='replace') as fh:
        p = pd.read_csv(fh, usecols=PBP_COLS, low_memory=False)
    p = p[p['season_type'] == 'REG'].copy()
    if p.empty:
        raise SystemExit('play_by_play_{}: no REG rows, the download is bad'.format(yr))
    p['week'] = pd.to_numeric(p['week'], errors='coerce')
    p = p[p['week'].notna()].copy()
    p['week'] = p['week'].astype(int)
    return p


def count_events(p):
    """One Counter-like table per event, keyed by (week, team). Same tests as the old builder for
    sack, int, fr, saf and dtd; blk and fuml as defined in the docstring."""
    num = lambda c: pd.to_numeric(p[c], errors='coerce').fillna(0)
    has_def = p['defteam'].notna()
    has_off = p['posteam'].notna()
    sack, itc, saf = num('sack') != 0, num('interception') != 0, num('safety') != 0
    fl, td, pb = num('fumble_lost') != 0, num('touchdown') != 0, num('punt_blocked') != 0

    def tally(mask, team_col, weight=None):
        sub = p.loc[mask, ['week', team_col]]
        if weight is not None:
            sub = sub.assign(n=weight[mask].values)
        else:
            sub = sub.assign(n=1)
        return sub.groupby(['week', team_col])['n'].sum().to_dict()

    ev = {}
    ev['sack'] = tally(has_def & sack, 'defteam')
    ev['int'] = tally(has_def & itc, 'defteam')
    ev['saf'] = tally(has_def & saf, 'defteam')
    # a fumble the offence lost and the defence recovered
    ev['fr'] = tally(has_def & fl & (p['fumble_recovery_1_team'] == p['defteam']), 'defteam')
    # any TD scored by the team NOT on offence: pick-6, fumble-6, punt return (a kickoff return by the
    # receiving team is posteam's and is excluded, as before)
    ev['dtd'] = tally(has_def & has_off & td & p['td_team'].notna() & (p['td_team'] != p['posteam']), 'td_team')
    # NEW: blocked FG / PAT / punt, credited to defteam
    blk_n = ((p['field_goal_result'] == 'blocked').astype(int)
             + (p['extra_point_result'] == 'blocked').astype(int)
             + pb.astype(int))
    ev['blk'] = tally(has_def & (blk_n > 0), 'defteam', weight=blk_n)
    # NEW: a fumble lost by the return / defensive unit
    unit = p['defteam'].where(p['play_type'] != 'kickoff', p['posteam'])
    ev['fuml'] = tally(fl & p['fumbled_1_team'].notna() & (p['fumbled_1_team'] == unit), 'fumbled_1_team')
    return ev


def games_table(p):
    """One row per game: week, home, away, final scores, in play-by-play order."""
    g = (p.groupby('game_id', sort=False)
          .agg(week=('week', 'first'), home=('home_team', 'first'), away=('away_team', 'first'),
               home_pts=('total_home_score', 'max'), away_pts=('total_away_score', 'max'))
          .reset_index())
    bad = g[g['home_pts'].isna() | g['away_pts'].isna() | g['home'].isna() | g['away'].isna()]
    if not bad.empty:
        raise SystemExit('games with no final score, refusing to drop them silently:\n'
                         + bad.to_string())
    return g


def build_season(yr):
    p = load_pbp(yr)
    ev = count_events(p)
    rows = []
    for g in games_table(p).itertuples(index=False):
        wk = int(g.week)
        for team, opp, allowed in ((g.away, g.home, int(g.home_pts)), (g.home, g.away, int(g.away_pts))):
            c = {k: int(ev[k].get((wk, team), 0)) for k in ('sack', 'int', 'fr', 'saf', 'dtd', 'blk', 'fuml')}
            base = (c['sack'] * 1 + c['int'] * 2 + c['fr'] * 2 + c['saf'] * 4
                    + c['dtd'] * 6 + pa_points(allowed))
            rows.append({'season': yr, 'week': wk, 'team': team, 'opp': opp, 'allowed': allowed,
                         **c, 'dst_pts': base + 2 * c['blk'] - 2 * c['fuml']})
    df = pd.DataFrame(rows, columns=OUT_COLS).sort_values(['season', 'week', 'team']).reset_index(drop=True)
    dup = df.duplicated(['season', 'week', 'team']).sum()
    if dup:
        raise SystemExit('{}: {} duplicate team-weeks'.format(yr, dup))
    return df


def dst_rank(df, col, wmax=14, slot=12):
    """Doc 265 / k12_replacement.py: weeks 1-wmax, rank the defences by season TOTAL, report the
    slot-th one's per-game mean, then the mean of that over the seasons."""
    vals = []
    for yr, s in df[df['week'] <= wmax].groupby('season'):
        t = s.groupby('team')[col].agg(['sum', 'mean', 'size']).sort_values('sum', ascending=False)
        vals.append(float(t.iloc[slot - 1]['mean']))
    return st.mean(vals), vals


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--out', default=DEFAULT_OUT, help='where to write (default Source/dst_weekly_2021_2025.csv)')
    a = ap.parse_args(argv)

    df = pd.concat([build_season(yr) for yr in SEASONS], ignore_index=True)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    # the csv module, as the old builder used: CRLF endings on every platform, matching the old file
    with open(a.out, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(OUT_COLS)
        w.writerows(df[OUT_COLS].itertuples(index=False, name=None))

    by = df.groupby('season').size()
    print('wrote {}: {} team-weeks, by season {}'.format(
        a.out, len(df), ', '.join('{} {}'.format(y, n) for y, n in by.items())))
    print('  (a full regular season is 544; 2022 is 542 because BUF at CIN week 17 was cancelled)')
    print('D/ST points a week, all rows: mean {:.2f}  sd {:.2f}  min {}  max {}'.format(
        df['dst_pts'].mean(), df['dst_pts'].std(ddof=0), df['dst_pts'].min(), df['dst_pts'].max()))
    print('blocked kicks {} ({:+.3f} a week), unit fumbles lost {} ({:+.3f} a week)'.format(
        int(df['blk'].sum()), 2 * df['blk'].mean(), int(df['fuml'].sum()), -2 * df['fuml'].mean()))
    d12, by12 = dst_rank(df, 'dst_pts')
    print('D/ST12, weeks 1-14, ranked by season total as k12_replacement.py ranks, mean of {} seasons: '
          '{:.2f} a week, by season {}'.format(len(by12), d12, [round(v, 2) for v in by12]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
