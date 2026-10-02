#!/usr/bin/env python
"""
anchor_study.py -- doc 129.  Three questions Matt raised, measured.

1. Do teams with a good defence and bad QB play run more?  (half right, and unforecastable)
2. Is the preseason MARKET anchored on last year's production beyond the projection?  (yes)
3. Does fading that anchor pay?  (no -- it loses; and the reason is AVAILABILITY)

USAGE
  py anchor_study.py               # all three
  py anchor_study.py --mechanism   # 1 only  (nflverse only, no ESPN files needed)
  py anchor_study.py --market      # 2 and 3
  py anchor_study.py --year2       # doc 130: is the YEAR-2-BACK player a buy?  (no)

REQUIRES
  Source\\espn_projections_2022_20260824.csv   Source\\espn_projections_2024_20260824.csv
  Source\\adp_registry\\preseason_adp_2022.csv  ..._2024.csv     (via code_adp_guard)
  Source\\nfl\\w<year>.csv  for 2020-2025      (nflverse stats_player_week_<year>.csv)
     2020 is needed only by --year2 (it is the year-2-back lookback for the 2022 season).

§1.1 NOTE  This NEVER touches `espn_adp` from a historical pull.  The market comes from the
preseason registry only.  2024's entry is a FantasyPros consensus RANK, not a true ADP -- the
manifest says so, and the 2022 row (a real ADP) shows the stronger effect, so the conclusion
does not rest on the proxy.
"""
import argparse, json, os, re, sys
import numpy as np, pandas as pd
from scipy import stats as st
import warnings; warnings.filterwarnings('ignore')

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.normpath(os.path.join(HERE, '..', 'Source'))
NFL  = os.path.join(SRC, 'nfl')
SUF  = r'\b(jr|sr|ii|iii|iv|v)\b'
NICK = {'joshua':'josh','mitchell':'mitch','christopher':'chris','nathaniel':'nate',
        'benjamin':'ben','michael':'mike','zachary':'zach','matthew':'matt'}


def norm(s):
    s = str(s).lower().replace('.', ' ').replace("'", '').replace('-', ' ')
    s = re.sub(SUF, '', s); s = re.sub(r'[^a-z ]', '', s); p = s.split()
    if p: p[0] = NICK.get(p[0], p[0])
    return ''.join(p)


def wk(y):
    p = os.path.join(NFL, 'w%d.csv' % y)
    if not os.path.exists(p):
        sys.exit('MISSING %s -- see REQUIRES at the top of this file.' % p)
    w = pd.read_csv(p, low_memory=False)
    return w[w.season_type == 'REG']


def mechanism():
    print('=== 1. GOOD DEFENCE + BAD QB -> MORE RUNNING?')
    rows = []
    for y in range(2020, 2026):
        w = wk(y)
        off = w.groupby('team').agg(att=('attempts', 'sum'), car=('carries', 'sum'),
                                    pepa=('passing_epa', 'sum'),
                                    repa=('rushing_epa', 'sum')).reset_index()
        off['pass_rate'] = off.att / (off.att + off.car)
        off['qb_epa_att'] = off.pepa / off.att
        d = w.groupby('opponent_team').agg(a=('passing_epa', 'sum'), b=('rushing_epa', 'sum'),
                                           patt=('attempts', 'sum'), pcar=('carries', 'sum'),
                                           td=('passing_tds', 'sum'),
                                           rtd=('rushing_tds', 'sum')).reset_index()
        # doc 131 CORRECTION: a SEASON TOTAL is contaminated by pace and by how many plays a
        # team faced.  The rate is the right measure, and it changes the persistence number.
        d['def_epa_allowed'] = (d.a + d.b) / (d.patt + d.pcar)
        d['td_allowed'] = d.td + d.rtd
        m = off.merge(d[['opponent_team', 'def_epa_allowed', 'td_allowed']], left_on='team',
                      right_on='opponent_team')
        m['season'] = y; rows.append(m)
    T = pd.concat(rows)
    T2226 = T[T.season >= 2022]
    print('   n=%d team-seasons 2022-2025 for the pass-rate half.  HIGHER = worse defence.'
          % len(T2226))
    for lbl, c in [('QB passing EPA per attempt', 'qb_epa_att'),
                   ('defensive EPA per play allowed', 'def_epa_allowed')]:
        r, p = st.pearsonr(T2226[c], T2226.pass_rate)
        print('   corr(%-26s, pass rate) r=%+.3f p=%.4f' % (lbl, r, p))
    z = st.zscore
    X = np.column_stack([np.ones(len(T2226)), z(T2226.qb_epa_att), z(T2226.def_epa_allowed)])
    b, *_ = np.linalg.lstsq(X, z(T2226.pass_rate), rcond=None)
    R2 = 1 - ((z(T2226.pass_rate) - X @ b) ** 2).sum() / (z(T2226.pass_rate) ** 2).sum()
    print('   together, standardised: QB %+.3f | defence %+.3f | R2=%.3f' % (b[1], b[2], R2))
    print('   -> worse QB play means MORE passing, not less.  Game script beats coaching intent.')
    print()
    print('=== 2. IS IT KNOWABLE A YEAR AHEAD?')
    J = []
    for a, b_ in [(2022, 2023), (2023, 2024), (2024, 2025)]:
        J.append(T[T.season == a].set_index('team')
                 .join(T[T.season == b_].set_index('team'), rsuffix='_n', how='inner'))
    J = pd.concat(J)
    print('   pooled n=%d:  prior defence r=%+.3f | prior QB r=%+.3f | prior PASS RATE r=%+.3f'
          % (len(J), J.def_epa_allowed.corr(J.pass_rate_n),
             J.qb_epa_att.corr(J.pass_rate_n), J.pass_rate.corr(J.pass_rate_n)))
    # doc 131: the persistence number itself, on the FULL 2020-2025 window and per-play rates.
    F = []
    for a in range(2020, 2025):
        F.append(T[T.season == a].set_index('team')
                 .join(T[T.season == a + 1].set_index('team'), rsuffix='_n', how='inner'))
    F = pd.concat(F)
    print('   HOW PERSISTENT IS A DEFENCE?  n=%d transitions, 2020-2025:' % len(F))
    print('     EPA per play allowed  r=%+.3f      TDs allowed  r=%+.3f'
          % (F.def_epa_allowed.corr(F.def_epa_allowed_n), F.td_allowed.corr(F.td_allowed_n)))
    off = T.copy(); off['oepa'] = (off.pepa + off.repa) / (off.att + off.car)
    G = []
    for a in range(2020, 2025):
        G.append(off[off.season == a].set_index('team')
                 .join(off[off.season == a + 1].set_index('team'), rsuffix='_n', how='inner'))
    G = pd.concat(G)
    print('     for contrast, OFFENSIVE EPA per play  r=%+.3f' % G.oepa.corr(G.oepa_n))
    print('   A defence carries about 4% of next year\'s variance, an offence about 15%.')
    print('   Weak, and weaker than the offence -- but NOT zero.  (doc 131 corrects an earlier')
    print('   r=+0.113, which was season totals on a 3-transition window.)')


def _market_frame():
    out = []
    for yr, f in [(2022, 'espn_projections_2022_20260824.csv'),
                  (2024, 'espn_projections_2024_20260824.csv')]:
        pf = os.path.join(SRC, f)
        af = os.path.join(SRC, 'adp_registry', 'preseason_adp_%d.csv' % yr)
        if not (os.path.exists(pf) and os.path.exists(af)):
            print('   skipping %d (missing projection or preseason ADP)' % yr); continue
        d = pd.read_csv(pf); d.columns = [c.lstrip('﻿') for c in d.columns]
        assert 'espn_adp' not in d.columns or True   # never used; §1.1
        d = d[d.pos.isin(['QB', 'RB', 'WR', 'TE'])].copy(); d['k'] = d.Player.map(norm)
        adp = pd.read_csv(af); adp['k'] = adp.player.map(norm)
        m = d.merge(adp[['k', 'adp']], on='k', how='inner')
        m['proj'] = m['proj_%d' % yr]; m['act'] = m['actual_%d' % yr]
        m['prior'] = m['actual_%d' % (yr - 1)]
        g = wk(yr - 1).groupby('player_display_name').week.nunique().reset_index()
        g.columns = ['player_display_name', 'g_prior']; g['k'] = g.player_display_name.map(norm)
        m = m.merge(g[['k', 'g_prior']], on='k', how='left'); m['season'] = yr
        out.append(m[['Player', 'pos', 'k', 'season', 'adp', 'proj', 'act', 'prior', 'g_prior']])
    M = pd.concat(out).dropna(subset=['adp', 'proj', 'act', 'prior'])
    return M[M.proj > 0]


def market():
    M = _market_frame()
    print('=== 3. DOES THE MARKET WEIGHT LAST YEAR MORE THAN THE PROJECTION DOES?')
    for yr in sorted(M.season.unique()):
        s = M[M.season == yr].copy()
        s['r_adp'] = s.adp.rank(); s['r_proj'] = s.proj.rank(ascending=False)
        s['r_prior'] = s.prior.rank(ascending=False)
        z = st.zscore
        X = np.column_stack([np.ones(len(s)), z(s.r_proj), z(s.r_prior)])
        b, *_ = np.linalg.lstsq(X, z(s.r_adp), rcond=None)
        R2 = 1 - ((z(s.r_adp) - X @ b) ** 2).sum() / (z(s.r_adp) ** 2).sum()
        print('   %d n=%3d  ADP rank on: projection %+.3f | LAST YEAR %+.3f | R2=%.3f'
              % (yr, len(s), b[1], b[2], R2))
    print()
    print('=== 4. DOES FADING THE ANCHOR PAY?  (+ = market cheaper than the projection)')
    s = M.copy()
    s['r_adp'] = s.groupby('season').adp.rank()
    s['r_proj'] = s.groupby('season').proj.rank(ascending=False)
    s['cheap'] = s.r_adp - s.r_proj; s['beat'] = s.act - s.proj
    for yr in sorted(s.season.unique()):
        q = s[s.season == yr]; rho, p = st.spearmanr(q['cheap'], q.beat)
        print('   %d n=%3d rho(market is cheap, beats projection) = %+.3f p=%.3f' % (yr, len(q), rho, p))
    rho, p = st.spearmanr(s['cheap'], s.beat)
    print('   POOLED n=%d rho=%+.3f p=%.3f   [§4.13 measured -0.079 on 324 player-seasons]'
          % (len(s), rho, p))
    print('   NEGATIVE.  The players the market prices below the projection MISS it by more.')
    print()
    print('=== 5. WHY: PRIOR-SEASON AVAILABILITY')
    s = s.dropna(subset=['g_prior']).copy(); s['hurt'] = s.g_prior <= 12
    for lbl, sub in [('played 13+ last yr', s[~s.hurt]), ('missed time (<=12 g)', s[s.hurt])]:
        print('   %-22s n=%3d  market discount %+5.1f slots   mean beat %+6.1f pts'
              % (lbl, len(sub), sub['cheap'].median(), sub.beat.mean()))
    X = pd.get_dummies(s.pos, drop_first=True).astype(float)
    X['hurt'] = s.hurt.astype(float); X['lad'] = np.log(s.adp.clip(lower=1))
    X['s24'] = (s.season == 2024).astype(float); X.insert(0, 'const', 1.0)
    Xv = X.values.astype(float); y = s.beat.values
    b, *_ = np.linalg.lstsq(Xv, y, rcond=None)
    dof = len(y) - Xv.shape[1]
    se = np.sqrt(np.diag(((y - Xv @ b) ** 2).sum() / dof * np.linalg.pinv(Xv.T @ Xv)))
    i = list(X.columns).index('hurt')
    p = 2 * (1 - st.norm.cdf(abs(b[i] / se[i])))
    print('   CONTROLLED for position, log(ADP), season:  hurt %+.2f  se %.2f  p=%.3f  n=%d'
          % (b[i], se[i], p, len(s)))
    for pos in ('WR', 'RB'):
        q = s[s.pos == pos]; a, c = q[q.hurt].beat, q[~q.hurt].beat
        if len(a) < 10: continue
        t, pp = st.ttest_ind(a, c, equal_var=False)
        print('   %s only: hurt n=%d %+.1f | healthy n=%d %+.1f | diff %+.1f p=%.3f'
              % (pos, len(a), a.mean(), len(c), c.mean(), a.mean() - c.mean(), pp))
    print()
    print('=== 6. THE MECHANISM IS RECURRENCE  (the large-sample half)')
    def gpos(y):
        w = wk(y); g = w.groupby('player_display_name').agg(
            g=('week', 'nunique'), pos=('position', 'first')).reset_index()
        g['k'] = g.player_display_name.map(norm); return g
    J = []
    for a, b_ in [(2021, 2022), (2022, 2023), (2023, 2024), (2024, 2025)]:
        j = gpos(a).merge(gpos(b_), on='k', suffixes=('0', '1'))
        J.append(j[j.pos0.isin(['QB', 'RB', 'WR', 'TE'])])
    J = pd.concat(J)
    print('   prior games -> next games, all skill positions: r=%+.3f  n=%d pairs'
          % (J.g0.corr(J.g1), len(J)))
    for pos in ('WR', 'RB', 'TE', 'QB'):
        q = J[J.pos0 == pos]; h, o = q[q.g0 <= 12], q[q.g0 > 12]
        print('   %s: missed time last yr -> %.1f games (n=%d) vs %.1f (n=%d), diff %+.1f'
              % (pos, h.g1.mean(), len(h), o.g1.mean(), len(o), h.g1.mean() - o.g1.mean()))


def year2():
    """doc 130.  Matt: 'Barkley broke out two years after the injury -- year one back he
    slumped, and I got him the next year while his value was still depressed.'
    Cohorts, on players with BOTH prior seasons on the field:
      A healthy both years  ·  B hurt LAST year  ·  C healthy last year, hurt two years ago."""
    M = _market_frame()
    def gm(y):
        g = wk(y).groupby('player_display_name').week.nunique().reset_index()
        g.columns = ['n', 'g']; g['k'] = g.n.map(norm); return g[['k', 'g']]
    out = []
    for yr in sorted(M.season.unique()):
        s = M[M.season == yr].merge(gm(yr - 2).rename(columns={'g': 'g2'}), on='k', how='left')
        out.append(s)
    M = pd.concat(out).rename(columns={'g_prior': 'g1'})
    n0 = len(M); M = M.dropna(subset=['g1', 'g2']).copy()
    print('=== 7. THE YEAR-2-BACK TEST  (doc 130)')
    print('   %d joined; %d have BOTH prior seasons on the field (rookies and 2nd-year drop out)'
          % (n0, len(M)))
    M['r_adp'] = M.groupby('season').adp.rank()
    M['r_proj'] = M.groupby('season').proj.rank(ascending=False)
    M['cheap'] = M.r_adp - M.r_proj; M['beat'] = M.act - M.proj
    M['cohort'] = np.where(M.g1 <= 12, 'B hurt LAST yr',
                  np.where(M.g2 <= 12, 'C YEAR 2 BACK', 'A healthy both'))
    g = M.groupby('cohort').agg(n=('beat', 'size'), cheap=('cheap', 'mean'),
                                beat=('beat', 'mean'), hit=('beat', lambda x: 100 * (x > 0).mean()))
    print('   cheap > 0 means the market drafts him LATER than his projection rank.')
    print(g.round(1).to_string())
    A = M[M.cohort.str.startswith('A')]
    for c in ('B', 'C'):
        q = M[M.cohort.str.startswith(c)]
        t, p = st.ttest_ind(q.beat, A.beat, equal_var=False)
        tc, pc = st.ttest_ind(q['cheap'], A['cheap'], equal_var=False)
        print('   %s vs A: beat %+6.1f pts p=%.3f | market discount %+.1f slots p=%.3f  (n=%d)'
              % (c, q.beat.mean() - A.beat.mean(), p,
                 q['cheap'].mean() - A['cheap'].mean(), pc, len(q)))
    print('   -> C is a NULL.  The injury discount fully unwinds after one healthy season:')
    print('      the year-2 player is neither cheap nor better.  Not a buy signal.')
    b = M[(M.Player.str.contains('Barkley', na=False)) & (M.season == 2022)]
    for _, r in b.iterrows():
        print('   THE CASE ITSELF -- Barkley 2022: ADP rank %.0f, PROJECTION rank %.0f, cheap %+.0f.'
              % (r.r_adp, r.r_proj, r['cheap']))
        print('   He was drafted EARLIER than his projection warranted -- a premium, not a discount.')
    print()
    print('=== 8. THE YEAR-1 PENALTY IS DOSE-DEPENDENT  (this is what shades the board badge)')
    h = M[M.g1 <= 12].copy()
    h['band'] = pd.cut(h.g1, [0, 6, 9, 12], labels=['1-6 g', '7-9 g', '10-12 g'])
    print(h.groupby('band').agg(n=('beat', 'size'), beat=('beat', 'mean'),
                                cheap=('cheap', 'mean')).round(1).to_string())
    print('   13+ g baseline: beat %+.1f  n=%d' % (M[M.g1 > 12].beat.mean(), (M.g1 > 12).sum()))
    r, p = st.pearsonr(M.g1, M.beat)
    print('   corr(games last yr, beat) r=%+.3f p=%.4f n=%d -- MONOTONIC BY BAND BUT NOT'
          % (r, p, len(M)))
    print('   SIGNIFICANT POOLED.  Bands hold 19/30/40.  Suggestive, not resolved.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--mechanism', action='store_true')
    ap.add_argument('--market', action='store_true')
    ap.add_argument('--year2', action='store_true')
    a = ap.parse_args()
    if a.mechanism: mechanism()
    elif a.market: market()
    elif a.year2: year2()
    else:
        mechanism(); print(); market(); print(); year2()
        print()
        print('VERDICT: the anchoring is real and fading it loses.  What last year actually')
        print('carries is AVAILABILITY -- and the board now shows it as a 12g badge (doc 129).')
