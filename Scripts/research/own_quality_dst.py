#!/usr/bin/env python3
"""own_quality_dst.py -- does a defence's OWN season-to-date scoring predict its next week, beside the
opponent's implied total? (Matt, 1 Oct: "GB currently ranks at the 30th D/ST ... Chicago is ranked 8th,
no negative weeks ... Are you sure about that?")

THE CLAIM IN TESTABLE FORM: across D/ST team-weeks 2021 to 2025 (REG, weeks 3 to 17, 2+ prior games),
picking the free defence with the HIGHER own season-to-date average beats picking the one facing the
LOWER opponent implied total; and in a regression of this week's D/ST points on both, the own average
carries weight beside the line. Reuses vegas_streams.py's loaders (doc 441) unchanged.
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
print(f'unit-weeks with 2+ prior games and a line: n={len(x)}')
r_own, n = V.spearman(x.pts_prior, x.pts); r_opp, _ = V.spearman(x.implied_opp, x.pts)
print(f'  Spearman with this week\'s D/ST points: own season-to-date average {r_own:+.3f}; opponent implied total {r_opp:+.3f} (n={n})')
# regression, standardised
z = lambda s: (s - s.mean()) / s.std()
X = np.column_stack([np.ones(len(x)), z(x.pts_prior), z(x.implied_opp)])
beta, *_ = np.linalg.lstsq(X, x.pts.values, rcond=None)
res = x.pts.values - X @ beta; sig2 = (res ** 2).sum() / (len(x) - 3)
cov = sig2 * np.linalg.inv(X.T @ X); se_ = np.sqrt(np.diag(cov))
print(f'  regression (points per one sd): own average {beta[1]:+.2f} (se {se_[1]:.2f}), opponent implied total {beta[2]:+.2f} (se {se_[2]:.2f}); sd of own average {x.pts_prior.std():.2f} pts, of implied total {x.implied_opp.std():.2f} pts')
# pick rules among ALL 32 and among the streamable pool
for label, pool in [('all 32 units', x), ('streamable pool, rank 13-32', x[x['rank'] >= 13])]:
    rules = {'line: lowest opp implied total': ('implied_opp', True), 'own: highest season-to-date average': ('pts_prior', False)}
    w = V.run_rules(pool, rules, '  ' + label)
    for k in rules:
        dlt = w[k] - w['random']; print(f'    {k:<40} {w[k].mean():.2f} a week, {dlt.mean():+.2f} over random (se {V.se(dlt):.2f}, t {dlt.mean()/V.se(dlt):.1f})')
    dd = w['line: lowest opp implied total'] - w['own: highest season-to-date average']
    print(f'    line minus own: {dd.mean():+.2f} a week (se {V.se(dd):.2f}); line wins {(dd>0).sum()}, own wins {(dd<0).sum()}, ties {(dd==0).sum()} of {len(dd)} weeks')
# Matt's shape: a top-12 unit with the worse matchup against a bottom-10 unit with the better one, head to head in the same week
rows = []
for (s, wk), p in x.groupby(['season', 'week']):
    good = p[p['rank'] <= 12]; bad = p[p['rank'] >= 23]
    for _, a in good.iterrows():
        for _, b in bad.iterrows():
            if a.implied_opp - b.implied_opp >= 2.0:    # the good unit faces at least 2 more implied points
                rows.append((a.pts, b.pts, a.implied_opp - b.implied_opp))
h = pd.DataFrame(rows, columns=['good_unit', 'bad_unit', 'gap'])
print(f'  head to head, same week: a top-12 unit facing an opponent total at least 2 points HIGHER than a rank-23-or-worse unit\'s: n={len(h)} pairs; the good unit scores {h.good_unit.mean():.2f}, the bad unit with the better matchup {h.bad_unit.mean():.2f}, good unit wins {(h.good_unit>h.bad_unit).mean():.0%} of pairs')
for lo, hi in [(2, 3), (3, 5), (5, 99)]:
    hh = h[(h.gap >= lo) & (h.gap < hi)]
    if len(hh): print(f'    gap {lo} to {hi} points: n={len(hh)}, good unit {hh.good_unit.mean():.2f} vs bad-unit-better-matchup {hh.bad_unit.mean():.2f}, good wins {(hh.good_unit>hh.bad_unit).mean():.0%}')
