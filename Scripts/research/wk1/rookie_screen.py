#!/usr/bin/env python3
"""rookie_screen.py -- does the 4.30 receiver screen work IN SEASON, on a young receiver's first few
weeks, and does a rookie's first big game say anything on its own? (doc 453)

THE CLAIM IN TESTABLE FORM (Matt, 29 Sept, on Chris Bell: "young and talented and broke out his first
game at the NFL level with a suspect QB speaks volumes. This is what I've been calling upside"):
  among receivers in NFL years 1 to 3 (drafted 2021 or later) who were not startable the season
  before (under 9.62 half-PPR a game, this league's WR replacement) or had no season before,
  read at the end of week W on weeks 1 to W alone:
    S1  NFL draft round 1 to 3
    S2  yards per target over 7.13 (on 5 or more targets)
    S3  targets per game over 3.20
    B   the last game was a breakout: 60 or more receiving yards, or 7 or more targets
  OUTCOME: startable over the rest of the regular season (weeks W+1 to 14): 9.62 or more a game
  over 4 or more games played.
4.30 (doc 248) measured S1 to S3 on a FULL prior season predicting the NEXT season (39.4% at 3 of 3,
n=33). Nothing had measured them on three weeks predicting the next eleven, which is the object the
week sheet would be applying them to for a rookie. This is that measurement.

Reads the nflverse weekly file (the same cache doc 438 built) and Source\\nfl_draft_picks.csv.
pandas + numpy only. Paths resolve against this file.
"""
import os, sys, urllib.request
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get('FF_CACHE') or os.path.normpath(os.path.join(HERE, '..', '_nflverse_cache'))
SRC = os.environ.get('FF_SRC') or os.path.normpath(os.path.join(HERE, '..', '..', '..', 'Source'))
NFLV = 'https://github.com/nflverse/nflverse-data/releases/download/'
BAR = 9.62          # WR replacement per game, doc 12 / 4.30's population line
YPT_BAR, TPG_BAR, RND_BAR = 7.13, 3.20, 3
MIN_TGT_FOR_YPT = 5


def _get(name, url):
    for d in (CACHE, HERE):
        q = os.path.join(d, name)
        if os.path.exists(q) and os.path.getsize(q) > 1000:
            return q
    q = os.path.join(CACHE, name)
    os.makedirs(CACHE, exist_ok=True)
    print(f'  fetching {name} -> {q}')
    with urllib.request.urlopen(url, timeout=180) as fh:
        body = fh.read()
    with open(q, 'wb') as out:
        out.write(body)
    return q


def load():
    d = pd.concat([pd.read_csv(_get(f'stats_player_week_{s}.csv', NFLV + f'stats_player/stats_player_week_{s}.csv'),
                               low_memory=False) for s in range(2021, 2026)])
    d = d[(d.season_type == 'REG') & (d.position == 'WR') & (d.week <= 14)].copy()
    for c in ['receiving_yards', 'receiving_tds', 'receptions', 'targets', 'rushing_yards', 'rushing_tds',
              'rushing_fumbles_lost', 'receiving_fumbles_lost', 'sack_fumbles_lost']:
        d[c] = pd.to_numeric(d[c], errors='coerce').fillna(0)
    d['hppr'] = (0.1 * (d.rushing_yards + d.receiving_yards) + 6 * (d.rushing_tds + d.receiving_tds)
                 + 0.5 * d.receptions - 2 * (d.rushing_fumbles_lost + d.receiving_fumbles_lost + d.sack_fumbles_lost))
    picks = pd.read_csv(os.path.join(SRC, 'nfl_draft_picks.csv'))
    picks = picks[picks.position == 'WR'][['gsis_id', 'season', 'round']].rename(
        columns={'season': 'draft_season', 'round': 'nfl_round'})
    d = d.merge(picks, left_on='player_id', right_on='gsis_id', how='inner')   # drafted 2021 or later only
    d['nfl_year'] = d.season - d.draft_season + 1
    d = d[(d.nfl_year >= 1) & (d.nfl_year <= 3)]
    # prior season ppg, for the not-startable-before condition
    prior = (d.groupby(['player_id', 'season']).agg(g=('week', 'nunique'), pts=('hppr', 'sum')).reset_index())
    prior['ppg_prior'] = prior.pts / prior.g
    prior['season'] = prior.season + 1
    d = d.merge(prior[['player_id', 'season', 'ppg_prior', 'g']].rename(columns={'g': 'g_prior'}),
                on=['player_id', 'season'], how='left')
    return d


def table(d, W):
    """One row per player-season read at the end of week W."""
    pre = d[d.week <= W]
    post = d[d.week > W]
    a = pre.groupby(['player_id', 'season']).agg(
        games=('week', 'nunique'), tgt=('targets', 'sum'), yds=('receiving_yards', 'sum'),
        pts=('hppr', 'sum'), nfl_year=('nfl_year', 'first'), rnd=('nfl_round', 'first'),
        ppg_prior=('ppg_prior', 'first'), g_prior=('g_prior', 'first')).reset_index()
    last = pre[pre.week == W][['player_id', 'season', 'receiving_yards', 'targets']].rename(
        columns={'receiving_yards': 'last_yds', 'targets': 'last_tgt'})
    a = a.merge(last, on=['player_id', 'season'], how='left')
    b = post.groupby(['player_id', 'season']).agg(g_post=('week', 'nunique'), pts_post=('hppr', 'sum')).reset_index()
    a = a.merge(b, on=['player_id', 'season'], how='left')
    a['g_post'] = a.g_post.fillna(0)
    a['ppg_post'] = a.pts_post / a.g_post.replace(0, np.nan)
    # population: played W weeks' worth (at least 2 games by week 3), not startable before (or no before), and 4+ games after
    a = a[(a.games >= max(2, W - 1)) & (a.g_post >= 4)]
    a = a[a.ppg_prior.isna() | (a.ppg_prior < BAR) | (a.g_prior < 4)]
    a['startable_post'] = (a.ppg_post >= BAR).astype(int)
    a['s1'] = (a.rnd <= RND_BAR).astype(int)
    a['ypt'] = a.yds / a.tgt.replace(0, np.nan)
    a['s2'] = ((a.tgt >= MIN_TGT_FOR_YPT) & (a.ypt > YPT_BAR)).astype(int)
    a['tpg'] = a.tgt / a.games
    a['s3'] = (a.tpg > TPG_BAR).astype(int)
    a['sig'] = a.s1 + a.s2 + a.s3
    a['breakout'] = ((a.last_yds >= 60) | (a.last_tgt >= 7)).astype(int)
    a['ppg_pre'] = a.pts / a.games
    a['W'] = W
    return a


def cell(df, mask, label):
    n = int(mask.sum())
    k = int(df.loc[mask, 'startable_post'].sum())
    print(f'    {label:<58} {k:>3} of {n:<4} {100*k/n if n else float("nan"):5.1f}%')
    return n, k


def perm_p(df, mask, draws=4000, seed=7):
    """Permutation p for the rate inside `mask` against the rest, outcome labels shuffled."""
    rng = np.random.default_rng(seed)
    y = df.startable_post.values
    m = mask.values
    obs = y[m].mean() - y[~m].mean()
    cnt = 0
    for _ in range(draws):
        yy = rng.permutation(y)
        if yy[m].mean() - yy[~m].mean() >= obs:
            cnt += 1
    return obs, cnt / draws


def main():
    d = load()
    print(f'population: WR seasons 2021-2025, drafted 2021 or later, NFL years 1 to 3, not startable the season before '
          f'(under {BAR} a game) or no season before; outcome startable (>= {BAR}) over weeks W+1 to 14 on 4+ games')
    for W in (3, 4, 5, 6):
        a = table(d, W)
        print(f'\n== read at the end of week {W}: n={len(a)}, base rate {100*a.startable_post.mean():.1f}% '
              f'({int(a.startable_post.sum())} of {len(a)}); rookies {int((a.nfl_year==1).sum())}')
        for s in (0, 1, 2, 3):
            cell(a, a.sig == s, f'{s} of 3 signals (rounds 1-3, ypt>{YPT_BAR} on {MIN_TGT_FOR_YPT}+ tgt, tpg>{TPG_BAR})')
        obs, p = perm_p(a, a.sig == 3)
        print(f'    3 of 3 against fewer: {100*obs:+.1f} points, permutation p={p:.4f}')
        cell(a, (a.sig == 3) & (a.nfl_year == 1), 'ROOKIES, 3 of 3')
        cell(a, (a.sig < 3) & (a.nfl_year == 1), 'ROOKIES, fewer than 3')
        cell(a, (a.sig == 3) & (a.nfl_year >= 2), 'years 2 to 3, 3 of 3')
        cell(a, a.breakout == 1, 'the last game was a breakout (60+ yds or 7+ targets)')
        cell(a, a.breakout == 0, 'the last game was not')
        cell(a, (a.breakout == 1) & (a.nfl_year == 1) & (a.s1 == 1), 'ROOKIE, rounds 1-3, breakout last game')
        cell(a, (a.breakout == 1) & (a.nfl_year == 1) & (a.s1 == 1) & (a.ppg_pre < BAR),
             '  ... and still under the bar through week W (Bell\'s shape)')
        cell(a, (a.breakout == 0) & (a.nfl_year == 1) & (a.s1 == 1), 'ROOKIE, rounds 1-3, no breakout last game')
        obs, p = perm_p(a[(a.nfl_year == 1) & (a.s1 == 1)], a[(a.nfl_year == 1) & (a.s1 == 1)].breakout == 1)
        print(f'    breakout against not, among rounds 1-3 rookies: {100*obs:+.1f} points, permutation p={p:.4f}')
        cell(a, (a.sig == 3) & (a.breakout == 1), '3 of 3 AND a breakout last game')
        cell(a, (a.sig == 3) & (a.breakout == 0), '3 of 3, no breakout last game')
        if W == 3:
            hit = a[(a.sig == 3) & (a.nfl_year == 1)].merge(
                d[['player_id', 'player_display_name']].drop_duplicates('player_id'), on='player_id')
            hit = hit.sort_values('startable_post', ascending=False)
            print('    rookies 3 of 3 at week 3: ' + '; '.join(
                f"{r.player_display_name} {int(r.season)} ({'hit' if r.startable_post else 'miss'}, {r.ppg_post:.1f})"
                for r in hit.itertuples()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
