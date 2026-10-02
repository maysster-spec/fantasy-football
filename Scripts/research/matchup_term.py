#!/usr/bin/env python3
"""matchup_term.py -- does the opponent's points allowed to the position predict a receiver's or tight end's
next week, net of his own rate? (claude_todo, doc 456 section 4: "the one thing the crowd prices and the
page does not"; doc 468.)

THE CLAIM IN TESTABLE FORM. Population: receivers and tight ends with three or more games played so far in
the season, nflverse regular season 2021 to 2025, weeks 5 to 17, so the defense has at least four weeks of
record. Own rate: the man's half-PPR points per game through the previous week. Matchup: half-PPR points the
coming opponent has allowed per game to that position through the previous week, centred on the league
average that week (so a defense is "soft" relative to the field, not in raw points). Outcome: the man's
half-PPR points in the coming week. Direction: a softer defense means more points, net of the own rate.
DECISION FORM (0.5(a7)): between two men of equal own rate, how many points a week does taking the one
with the softer matchup gain, top quartile of defenses against bottom quartile? The bar is a point a week,
the size byes are worth (4.11). Falsifier: under a point.

    py research\\matchup_term.py              stdlib + pandas/numpy; FF_CACHE names the nflverse cache
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get('FF_CACHE') or os.path.join(HERE, '_nflverse_cache')
SEASONS = (2021, 2022, 2023, 2024, 2025)
POS = ('WR', 'TE', 'RB')          # RB printed beside the two the item asked about, as a comparison
MIN_GAMES = 3
MIN_DEF_WEEKS = 4


def load():
    out = []
    for s in SEASONS:
        p = os.path.join(CACHE, f'stats_player_week_{s}.csv')
        if not os.path.exists(p):
            print(f'  !! missing {p}')
            continue
        d = pd.read_csv(p, low_memory=False,
                        usecols=['player_id', 'player_display_name', 'position', 'season', 'week',
                                 'season_type', 'team', 'opponent_team', 'fantasy_points',
                                 'fantasy_points_ppr', 'targets'])
        d = d[(d.season_type == 'REG') & d.position.isin(POS)]
        d['half'] = (d.fantasy_points.fillna(0) + d.fantasy_points_ppr.fillna(0)) / 2.0
        out.append(d)
    return pd.concat(out, ignore_index=True)


def build(d):
    """One row per player-week with: own rate to date, the opponent's allowed-per-game to the position to
    date (centred on that week's league mean), and the outcome."""
    rows = []
    for (season, pos), g in d.groupby(['season', 'position']):
        # defense allowed per game to this position, by week, cumulative through the previous week
        allowed = g.groupby(['opponent_team', 'week']).half.sum().reset_index()
        allowed = allowed.rename(columns={'opponent_team': 'defense'})
        weeks = sorted(g.week.unique())
        # the man's own cumulative rate
        pw = g.groupby(['player_id', 'week']).agg(half=('half', 'sum'), name=('player_display_name', 'first'),
                                                   team=('team', 'first'), opp=('opponent_team', 'first')).reset_index()
        pw = pw.sort_values(['player_id', 'week'])
        pw['games_before'] = pw.groupby('player_id').cumcount()
        pw['pts_before'] = pw.groupby('player_id').half.cumsum() - pw.half
        pw['own_rate'] = pw.pts_before / pw.games_before.replace(0, np.nan)
        for w in weeks:
            if w < MIN_DEF_WEEKS + 1:
                continue
            prior = allowed[allowed.week < w]
            dw = prior.groupby('defense').agg(allowed=('half', 'sum'), n=('week', 'nunique'))
            dw = dw[dw.n >= MIN_DEF_WEEKS]
            if dw.empty:
                continue
            dw['apg'] = dw.allowed / dw.n
            mean = dw.apg.mean()
            dw['soft'] = dw.apg - mean
            cur = pw[(pw.week == w) & (pw.games_before >= MIN_GAMES)].copy()
            cur = cur.join(dw[['soft', 'apg']], on='opp', how='inner')
            cur['season'] = season
            cur['pos'] = pos
            rows.append(cur[['season', 'pos', 'week', 'player_id', 'name', 'team', 'opp', 'own_rate', 'soft', 'apg', 'half']])
    return pd.concat(rows, ignore_index=True)


def lines():
    """Own implied team total from nflverse games.csv (doc 441's convention): total/2 + own spread/2.
    Returns {(season, week, team): (own_total, opp_total)} or {} when the file is not beside this script."""
    p = os.path.join(HERE, 'games.csv')
    if not os.path.exists(p):
        return {}
    g = pd.read_csv(p, low_memory=False)
    g = g[(g.game_type == 'REG') & g.season.isin(SEASONS)].dropna(subset=['spread_line', 'total_line'])
    out = {}
    for r in g.itertuples():
        home = r.total_line / 2 + r.spread_line / 2
        away = r.total_line / 2 - r.spread_line / 2
        out[(r.season, r.week, r.home_team)] = (home, away)
        out[(r.season, r.week, r.away_team)] = (away, home)
    return out


def ols(y, X):
    X = np.column_stack([np.ones(len(X))] + [X[:, i] for i in range(X.shape[1])])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    n, k = X.shape
    s2 = (resid @ resid) / (n - k)
    cov = s2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    return beta, se


def main():
    d = load()
    t = build(d)
    L = lines()
    if L:
        t['own_total'] = [L.get((a, b, c), (np.nan, np.nan))[0] for a, b, c in zip(t.season, t.week, t.team)]
        t = t.dropna(subset=['own_total'])
        print(f'line control on: own implied team total joined for {len(t):,} player-weeks (games.csv beside this script)')
    print(f'population: {len(t):,} player-weeks, {", ".join(str(s) for s in SEASONS)}, weeks {t.week.min()} to {t.week.max()}, '
          f'{MIN_GAMES}+ games played, defense with {MIN_DEF_WEEKS}+ weeks of record')
    print()
    print(f'{"pos":<4}{"seasons":<9}{"n":>8}  {"rho(own,next)":>14}  {"rho(soft,next)":>15}  {"rho(soft,resid)":>16}  '
          f'{"b_soft/pt":>10}  {"se":>6}  {"top-bottom quartile gain":>24}')
    for pos in POS:
        for label, sub in [('all', t[t.pos == pos])] + [(str(s), t[(t.pos == pos) & (t.season == s)]) for s in SEASONS]:
            if len(sub) < 200:
                continue
            y = sub.half.values
            cols = [sub.own_rate.values, sub.soft.values] + ([sub.own_total.values] if 'own_total' in sub else [])
            X = np.column_stack(cols)
            beta, se = ols(y, X)
            resid = y - (beta[0] + beta[1] * sub.own_rate.values + (beta[3] * sub.own_total.values if len(beta) > 3 else 0))
            r_own = np.corrcoef(sub.own_rate, y)[0, 1]
            r_soft = np.corrcoef(sub.soft, y)[0, 1]
            r_res = np.corrcoef(sub.soft, resid)[0, 1]
            q1, q3 = sub.soft.quantile(0.25), sub.soft.quantile(0.75)
            # the decision: equal own rate, softest quarter against hardest quarter
            top = sub[sub.soft >= q3]; bot = sub[sub.soft <= q1]
            gain = (top.half.mean() - beta[1] * top.own_rate.mean()) - (bot.half.mean() - beta[1] * bot.own_rate.mean())
            extra = f'  b_line {beta[3]:+.3f} se {se[3]:.3f}' if len(beta) > 3 else ''
            print(f'{pos:<4}{label:<9}{len(sub):>8,}  {r_own:>14.3f}  {r_soft:>15.3f}  {r_res:>16.3f}  '
                  f'{beta[2]:>10.3f}  {se[2]:>6.3f}  {gain:>+24.2f}{extra}')
    print()
    print('read: b_soft/pt is the coefficient on the defense term (points the man gains per point the defense allows above')
    print('the league average to his position, net of his own rate); the last column is the decision, in points a week.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
