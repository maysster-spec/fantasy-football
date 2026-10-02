#!/usr/bin/env python3
"""own_quality_dst2.py -- the finer point (Matt, 1 Oct): within SOFT matchups, do really bad units still deliver, and
does the unit's quality help as a tie-break when two matchups are close? Same population as own_quality_dst.py.

THE CLAIM IN TESTABLE FORM: among unit-weeks in the softest band of opponent implied total, D/ST points fall with the
unit's own season-to-date rank (bad units waste soft matchups); and a pick rule that takes the better unit when two
matchups are within 1.5 points beats the plain lowest-total rule.
"""
import numpy as np, pandas as pd
import vegas_streams as V
g = V.load_games(); tg = V.team_games(g)
d = pd.read_csv(V.DST_CSV); d = d[d.season.isin(V.SEASONS) & d.week.between(*V.WEEKS)].copy()
d = d.rename(columns={'pts_adj': 'pts'})[['season', 'week', 'team', 'opp', 'pts']]
d = V.prior_mean(d, ['season', 'team'], 'pts')
x = d.merge(tg[['season', 'week', 'team', 'implied_opp', 'spread_team']], on=['season', 'week', 'team'], how='inner')
x = x[x.n_prior >= 2].copy()
x['rank'] = x.groupby(['season', 'week'])['pts_prior'].rank(ascending=False, method='min')
x['tier'] = pd.cut(x['rank'], [0, 8, 16, 24, 33], labels=['top 8', '9 to 16', '17 to 24', '25 to 32'])
x['band'] = pd.cut(x.implied_opp, [0, 17.5, 20, 22.5, 25, 99], labels=['<=17.5', '17.5-20', '20-22.5', '22.5-25', '>25'])
print(f'n={len(x)} unit-weeks; cells: mean D/ST points (share of weeks 10+ / share at or below 0), by own tier (rows) and opponent implied total (columns)')
t = x.groupby(['tier', 'band'], observed=True).agg(m=('pts', 'mean'), n=('pts', 'size'), boom=('pts', lambda s: (s >= 10).mean()), bust=('pts', lambda s: (s <= 0).mean())).reset_index()
cols = ['<=17.5', '17.5-20', '20-22.5', '22.5-25', '>25']
print(f'{"own tier":<10}' + ''.join(f'{c:>22}' for c in cols))
for tier in ['top 8', '9 to 16', '17 to 24', '25 to 32']:
    row = f'{tier:<10}'
    for c in cols:
        r = t[(t.tier == tier) & (t.band == c)]
        row += (f'{r.m.iloc[0]:6.2f} ({r.boom.iloc[0]:.0%}/{r.bust.iloc[0]:.0%}) n={int(r.n.iloc[0]):<3}' if len(r) else ' ' * 22)
    print(row)
# interaction regression
z = lambda s: (s - s.mean()) / s.std()
X = np.column_stack([np.ones(len(x)), z(x.pts_prior), z(x.implied_opp), z(x.pts_prior) * z(x.implied_opp)])
beta, *_ = np.linalg.lstsq(X, x.pts.values, rcond=None)
res = x.pts.values - X @ beta; sig2 = (res ** 2).sum() / (len(x) - 4); se_ = np.sqrt(np.diag(sig2 * np.linalg.inv(X.T @ X)))
print(f'\ninteraction regression: own {beta[1]:+.2f} (se {se_[1]:.2f}), opponent total {beta[2]:+.2f} (se {se_[2]:.2f}), own x total {beta[3]:+.2f} (se {se_[3]:.2f})')
soft = x[x.implied_opp <= 19]
r, n = V.spearman(soft.pts_prior, soft.pts)
print(f'within soft matchups only (opponent total 19 or less, n={n}): Spearman of own average with points {r:+.3f}; by tier: '
      + ', '.join(f'{tier} {soft[soft.tier == tier].pts.mean():.2f} (n={len(soft[soft.tier == tier])})' for tier in ['top 8', '9 to 16', '17 to 24', '25 to 32']))
# pick rules: plain line; line but excluding the worst units; line with a quality tie-break inside 1.5 points
rows = []
for (s, wk), pool in x.groupby(['season', 'week']):
    if len(pool) < 3: continue
    best = pool.implied_opp.min()
    plain = pool.loc[pool.implied_opp == best, 'pts'].mean()
    close = pool[pool.implied_opp <= best + 1.5]
    tb = close.loc[close.pts_prior == close.pts_prior.max(), 'pts'].mean()
    close2 = pool[pool.implied_opp <= best + 3.0]
    tb2 = close2.loc[close2.pts_prior == close2.pts_prior.max(), 'pts'].mean()
    ok = pool[pool['rank'] <= 24]
    excl = ok.loc[ok.implied_opp == ok.implied_opp.min(), 'pts'].mean() if len(ok) else np.nan
    rows.append(dict(season=s, week=wk, random=pool.pts.mean(), plain=plain, tb15=tb, tb30=tb2, excl=excl))
w = pd.DataFrame(rows)
print(f'\npick rules among all 32, {len(w)} season-weeks:')
for k, lab in [('plain', 'lowest opponent total'), ('tb15', 'best unit among totals within 1.5 of the lowest'), ('tb30', 'best unit among totals within 3.0 of the lowest'), ('excl', 'lowest total, but never a unit ranked 25 to 32')]:
    dlt = w[k] - w['random']; vs = w[k] - w['plain']
    print(f'  {lab:<52} {w[k].mean():.2f} a week, {dlt.mean():+.2f} over random; against the plain rule {vs.mean():+.2f} (se {V.se(vs):.2f}), wins {(vs>0).sum()} loses {(vs<0).sum()} ties {(vs==0).sum()}')
