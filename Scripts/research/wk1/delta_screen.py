"""delta_screen.py -- three measurements on the claimable pool (copied from xfp_backtest.py's population build,
doc 438; the base script's own tests are in run_xfp_backtest.txt and are not repeated here).

  TEST 1  the air-yards threshold (WOPR, air-yards share) as a FOURTH signal on the wire's three-signal
          workload screen, on doc 389's WR/TE population.
  TEST 2  the DELTA in expected points (xfp_w minus xfp_{w-1}) over and above the two-game level, on the
          xfp_backtest population (RB/WR/TE).
  TEST 3  Matt's claim: a week-over-week RISE in both snap share and targets as a signal for a role that could
          expand, net of the level of either, same population.

Each test prints its testable form (population, predictor, outcome, direction, falsifier) BEFORE its numbers
(0.5(a2)). Standard library plus pandas and numpy only; Spearman is rank-then-Pearson; no scipy.
"""
import os, sys, urllib.request
import pandas as pd, numpy as np
import numpy.linalg as la

HERE = os.path.dirname(os.path.abspath(__file__))
# The nflverse cache this run reads: Scripts\research\_nflverse_cache, the one build_form.py keeps, so the
# population is the one doc 438 built. Missing files are fetched once (see _get below, as in xfp_backtest.py).
CACHE = os.environ.get('FF_CACHE') or os.path.normpath(os.path.join(HERE, '..', '_nflverse_cache'))
NFLV = 'https://github.com/nflverse/nflverse-data/releases/download/'
FFV = 'https://github.com/ffverse/ffopportunity/releases/download/latest-data/'

def _get(name, url):
    """The cached file if present, else one fetch into the cache (the fetch says so)."""
    for d in (CACHE, HERE):
        q = os.path.join(d, name)
        if os.path.exists(q) and os.path.getsize(q) > 1000:
            return q
    q = os.path.join(CACHE, name)
    os.makedirs(CACHE, exist_ok=True)
    print(f'  fetching {name} -> {q}')
    with urllib.request.urlopen(url, timeout=180) as fh:
        body = fh.read()
    if len(body) < 1000:
        raise SystemExit(f'FAILED: {url} returned {len(body)} bytes')
    with open(q, 'wb') as out:
        out.write(body)
    return q

def spearman(a, b):
    return pd.Series(a).rank().corr(pd.Series(b).rank())

BAR = {'RB': 9.92, 'WR': 9.62, 'TE': 8.25}
SPIKE = 18.0
rng = np.random.default_rng(7)
print(f'cache: {CACHE}')

# ---- actuals, this league's half-PPR, from the nflverse weekly file (verbatim from xfp_backtest.py) ---------
d = pd.concat([pd.read_csv(_get(f'stats_player_week_{s}.csv', NFLV + f'stats_player/stats_player_week_{s}.csv'),
                           low_memory=False) for s in range(2021, 2026)])
d = d[(d.season_type == 'REG') & (d.position.isin(['RB', 'WR', 'TE']))].copy()
num = ['rushing_yards', 'receiving_yards', 'rushing_tds', 'receiving_tds', 'receptions', 'rushing_fumbles_lost',
       'receiving_fumbles_lost', 'sack_fumbles_lost', 'targets', 'carries', 'target_share', 'air_yards_share', 'wopr']
for c in num:
    d[c] = pd.to_numeric(d[c], errors='coerce').fillna(0)
d['hppr'] = (0.1 * (d.rushing_yards + d.receiving_yards) + 6 * (d.rushing_tds + d.receiving_tds) + 0.5 * d.receptions
             - 2 * (d.rushing_fumbles_lost + d.receiving_fumbles_lost + d.sack_fumbles_lost))
d = d[d.week <= 18]

# ---- expected, ffverse ep_weekly, converted to half-PPR ------------------------------------------------------
e = pd.concat([pd.read_csv(_get(f'ep_weekly_{s}.csv', FFV + f'ep_weekly_{s}.csv'), low_memory=False) for s in range(2021, 2026)])
e = e[e.week <= 18].copy()
e['xfp'] = e.rec_fantasy_points_exp + e.rush_fantasy_points_exp - 0.5 * e.receptions_exp
e['afp_ff'] = e.rec_fantasy_points + e.rush_fantasy_points - 0.5 * e.receptions
e = e.groupby(['season', 'week', 'player_id'], as_index=False)[['xfp', 'afp_ff']].sum()
d = d.merge(e, on=['season', 'week', 'player_id'], how='left')
j = d[(d.targets + d.carries) > 0]
print(f'join: {j.xfp.notna().mean()*100:.1f}% of {len(j)} touch-weeks carry an expected row; '
      f'actual vs ffverse actual corr {j[["hppr","afp_ff"]].corr().iloc[0,1]:.4f} (fumbles differ)')

# ---- snap share, keyed on gsis via players.csv ---------------------------------------------------------------
sn = pd.concat([pd.read_csv(_get(f'snaps_{s}.csv', NFLV + f'snap_counts/snap_counts_{s}.csv'), low_memory=False)
                for s in range(2021, 2026)])
sn = sn[sn.game_type == 'REG']
pl = pd.read_csv(_get('players.csv', NFLV + 'players/players.csv'), low_memory=False)[['gsis_id', 'pfr_id']].dropna().drop_duplicates('pfr_id')
sn = sn.merge(pl, left_on='pfr_player_id', right_on='pfr_id', how='inner')
sn = sn.groupby(['season', 'week', 'gsis_id'], as_index=False).offense_pct.max().rename(columns={'gsis_id': 'player_id'})
d = d.merge(sn, on=['season', 'week', 'player_id'], how='left')
d['snap_pct'] = d.offense_pct * 100

# ---- windows -------------------------------------------------------------------------------------------------
d = d.sort_values(['season', 'player_id', 'week']).reset_index(drop=True)
g = d.groupby(['season', 'player_id'])
d['gp'] = g.cumcount() + 1
d['std_avg'] = g.hppr.transform(lambda s: s.expanding().mean())
d['bar'] = d.position.map(BAR)
d['prev_week'] = g.week.shift(1)
d['act2'] = (d.hppr + g.hppr.shift(1)) / 2
d['xfp2'] = (d.xfp + g.xfp.shift(1)) / 2
d['xfp_prev'] = g.xfp.shift(1)
# the previous GAME ROW's snap share and targets (the same "last game" xfp2 uses; a bye or a missed week
# makes it more than one calendar week back, and the share of calendar-adjacent rows is reported below)
d['snap_prev'] = g.snap_pct.shift(1)
d['tgt_prev'] = g.targets.shift(1)
d['std_prev'] = g.std_avg.shift(1)   # the season-to-date average BEFORE week w (doc 389's bar, see TEST 1)
key = d.set_index(['season', 'player_id', 'week']).hppr
def future(k, col=None):
    idx = pd.MultiIndex.from_arrays([d.season, d.player_id, d.week + k])
    return (key if col is None else d.set_index(['season', 'player_id', 'week'])[col]).reindex(idx).values
for k in range(1, 5):
    d[f'n{k}'] = future(k)
d['tgt_n1'] = future(1, 'targets')
d['next4_n'] = d[['n1', 'n2', 'n3', 'n4']].notna().sum(axis=1)
d['next4'] = d[['n1', 'n2', 'n3', 'n4']].mean(axis=1)
d['spike'] = d.n1 >= SPIKE
d['start1'] = d.n1 >= d.bar
d['start4'] = d.next4 >= d.bar

# ---- the three-signal count in week w (wire.py FORM_SIGS: targets 8+, snaps 80%+, target share 20%+) ------------
d['s_tgt'] = d.targets >= 8
d['s_snap'] = d.snap_pct >= 80
d['s_share'] = d.target_share * 100 >= 20
d['sig3'] = d[['s_tgt', 's_snap', 's_share']].sum(axis=1)

# ---- the xfp_backtest population (doc 438) ------------------------------------------------------------------
p = d[(d.week >= 2) & (d.week <= 16) & (d.std_avg < d.bar) & ((d.targets + d.carries) > 0)
      & d.prev_week.notna() & d.n1.notna() & d.xfp2.notna() & d.snap_pct.notna()].copy()
print(f'\nXFP_BACKTEST POPULATION n={len(p)}  ' + '  '.join(f'{k} {v}' for k, v in p.position.value_counts().items()))
print(f'base rates: spike {p.spike.mean()*100:.1f}%  startable w+1 {p.start1.mean()*100:.1f}%  '
      f'startable next four {p[p.next4_n>=2].start4.mean()*100:.1f}% (n={int((p.next4_n>=2).sum())})  '
      f'next-four mean {p.next4.mean():.2f}')
adj = (p.prev_week == p.week - 1).mean()
print(f'previous game row is the calendar week before (w-1 exactly): {adj*100:.1f}% of the pool; the rest have a bye '
      f'or a missed week between the two games')

# ---- helpers -------------------------------------------------------------------------------------------------
def se_diff(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    return np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))

def line(label, sub, w=52):
    s4 = sub[sub.next4_n >= 2]
    if len(sub) == 0:
        return f'{label:{w}s} n=    0  (empty)'
    return (f'{label:{w}s} n={len(sub):5d}  spike {sub.spike.mean()*100:5.1f}%  start w+1 {sub.start1.mean()*100:5.1f}%  '
            f'start next4 {s4.start4.mean()*100:5.1f}% (n={len(s4):5d})  next4 {sub.next4.mean():5.2f}')

def ols(y, X, names, robust=True):
    """OLS with an intercept; HC1 (heteroskedasticity-robust) standard errors, which matter for the 0/1 outcomes."""
    y = np.asarray(y, float); X = np.column_stack([np.ones(len(y)), np.asarray(X, float)])
    b, *_ = la.lstsq(X, y, rcond=None)
    r = y - X @ b; n, k = X.shape
    XtX_inv = la.inv(X.T @ X)
    if robust:
        meat = (X * (r ** 2)[:, None]).T @ X
        cov = XtX_inv @ meat @ XtX_inv * n / (n - k)
    else:
        cov = XtX_inv * (r @ r) / (n - k)
    s = np.sqrt(np.diag(cov))
    return {nm: (b[i + 1], s[i + 1]) for i, nm in enumerate(names)}, b[0], n

def fmt_ols(res, scale=1.0, unit=''):
    d_, b0, n = res
    return '  '.join(f'{k} {v[0]*scale:+.3f} (se {v[1]*scale:.3f})' for k, v in d_.items()) + f'   [n={n}{unit}]'

def perm_p(flag, y, reps=2000):
    """Two-sided permutation p for mean(y | flag) minus mean(y | not flag), shuffling the flag."""
    flag = np.asarray(flag, bool).copy(); y = np.asarray(y, float)
    obs = y[flag].mean() - y[~flag].mean()
    out = np.empty(reps)
    for i in range(reps):
        rng.shuffle(flag); out[i] = y[flag].mean() - y[~flag].mean()
    return obs, float(np.mean(np.abs(out) >= abs(obs)))

# =============================================================================================================
# TEST 1: the air-yards threshold as a fourth signal, on doc 389's WR/TE population
# =============================================================================================================
print('\n' + '=' * 110)
print('TEST 1: WOPR / air-yards share (top fifth) as a FOURTH signal on the 2-of-3 workload screen')
print('=' * 110)
print('TESTABLE FORM: population = WR and TE player-weeks, REG 2021-2025, weeks 1-17, not startable on the '
      'season-to-date bar (WR 9.62 / TE 8.25), 1+ target in w, played in w+1 (doc 389); predictor = the wire\'s '
      'three-signal count in w (targets 8+, snaps 80%+, target share 20%+), operative bar 2 of 3, plus a fourth flag '
      '"wopr >= its top-fifth cut" (then air_yards_share >= its cut); outcome = spike in w+1 (18+ half-PPR), also '
      'startable w+1, startable next four, next4 mean; direction = the fourth flag lifts the spike rate inside the 2+ '
      'bar; FALSIFIER = a lift under +2.0 points of spike rate keeps it display only.')
print('POPULATION NOTE: doc 389\'s script (wopr_spike.py) is not on hand. Of seven definitions tried, the one that '
      'reproduces its base 4.3% / WOPR top fifth 10.1% / targets 9.6% / air-yards 9.2% and its n within 70 rows is: '
      'season-to-date average through w-1 below the bar (a week-1 row counts as not startable), 1+ target in w, '
      '1+ target in w+1. The base script\'s own definition (average through w, a game row in w+1) gives n=9,053, '
      'base 3.6%, WOPR top fifth 8.1%, and is run as a sensitivity at the end of this test.')

def test1(t1, label, brief=False):
    print(f'\n--- {label}: n={len(t1)}  ' + '  '.join(f'{k} {v}' for k, v in t1.position.value_counts().items()))
    print(f'base rates: spike {t1.spike.mean()*100:.1f}%  start w+1 {t1.start1.mean()*100:.1f}%  '
          f'start next4 {t1[t1.next4_n>=2].start4.mean()*100:.1f}% (n={int((t1.next4_n>=2).sum())})  next4 {t1.next4.mean():.2f}')
    miss = int(t1.snap_pct.isna().sum())
    print(f'rows with no snap line (the snap signal cannot be scored for them): {miss} of {len(t1)}; the screen tables '
          f'run on the {len(t1)-miss} with a snap line; the cuts are taken on the full population')
    print('\n(a) top-fifth cut values on the full population:')
    cuts = {}
    for col in (['wopr', 'air_yards_share'] if brief else ['wopr', 'air_yards_share', 'targets', 'target_share']):
        c = t1[col].quantile(0.8); cuts[col] = c
        print(f'    {col:16s} cut {c:.4f}   n at or above {int((t1[col] >= c).sum())} of {len(t1)}  '
              f'(strict above {int((t1[col] > c).sum())})')
        print('      ' + line(f'top fifth by {col}', t1[t1[col] >= c], w=40))
    t1s = t1[t1.snap_pct.notna()].copy()
    print(f'\n(b) the screen on the {len(t1s)} with a snap line (WR {int((t1s.position=="WR").sum())}, TE {int((t1s.position=="TE").sum())}):')
    for k in range(4):
        print('  ' + line(f'{k} of 3 signals', t1s[t1s.sig3 == k]))
    print('  ' + line('2+ of 3 (the operative bar)', t1s[t1s.sig3 >= 2]))
    for col in ['wopr', 'air_yards_share']:
        cut = cuts[col]
        t1s['s4'] = t1s[col] >= cut
        a = t1s[t1s.sig3 >= 2]; b_ = a[a.s4]; c_ = a[~a.s4]
        print(f'\n  fourth signal = {col} >= {cut:.4f} (top fifth of the population)')
        print('   ' + line('2+ of 3', a))
        print('   ' + line('2+ of 3 AND fourth', b_))
        print('   ' + line('2+ of 3 and NOT fourth', c_))
        print('   ' + line('fourth alone, fewer than 2 of 3', t1s[(t1s.sig3 < 2) & t1s.s4]))
        gain = (b_.spike.mean() - a.spike.mean()) * 100
        gain_vs_not = (b_.spike.mean() - c_.spike.mean()) * 100
        a4 = a[a.next4_n >= 2]; b4 = b_[b_.next4_n >= 2]
        print(f'   GAIN in spike rate, (2+ AND fourth) minus (2+ bar): {gain:+.1f} points; '
              f'(2+ AND fourth) minus (2+ NOT fourth): {gain_vs_not:+.1f} points (se {se_diff(b_.spike, c_.spike)*100:.1f}); '
              f'start w+1 {(b_.start1.mean()-a.start1.mean())*100:+.1f}; start next4 {(b4.start4.mean()-a4.start4.mean())*100:+.1f}; '
              f'next4 {b_.next4.mean()-a.next4.mean():+.2f}')
        obs, pp = perm_p(a.s4.values, a.spike.values.astype(float), 2000)
        print(f'   permutation p (2000 shuffles of the fourth flag inside the 2+ bar, spike, with minus without): '
              f'{obs*100:+.1f} points, p={pp:.3f}')
        verdict = 'PASSES the +2 bar' if gain >= 2.0 else 'FAILS the +2 bar: stays display only'
        print(f'   VERDICT ({col}): {verdict}')
        if brief:
            continue
        t1s['sig4'] = t1s.sig3 + t1s.s4
        for k in range(5):
            print('     ' + line(f'{k} of 4', t1s[t1s.sig4 == k]))
        for pos in ['WR', 'TE']:
            q = t1s[t1s.position == pos]; qa = q[q.sig3 >= 2]
            print(f'     {pos}: ' + line('2+ of 3', qa, w=22))
            print(f'     {pos}: ' + line('2+ of 3 AND fourth', qa[qa.s4], w=22))
            print(f'     {pos}: ' + line('2+ of 3 NOT fourth', qa[~qa.s4], w=22))

wrte = (d.week >= 1) & (d.week <= 17) & d.position.isin(['WR', 'TE']) & (d.targets >= 1)
t1 = d[wrte & ~(d.std_prev >= d.bar) & (d.tgt_n1 >= 1)].copy()
test1(t1, 'doc 389 population, matched (average through w-1, 1+ target in w and in w+1); doc 389 printed 8,651, cold audit 8,671')
t1b = d[wrte & (d.std_avg < d.bar) & d.n1.notna()].copy()
test1(t1b, 'SENSITIVITY, the base script\'s definition (average through w, a game row in w+1)', brief=True)

# =============================================================================================================
# TEST 2: the delta in expected points
# =============================================================================================================
print('\n' + '=' * 110)
print('TEST 2: dxfp = xfp in week w minus xfp in the previous game, over and above the two-game level xfp2')
print('=' * 110)
print('TESTABLE FORM: population = the xfp_backtest pool (RB/WR/TE, REG 2021-2025, weeks 2-16, not startable in w, '
      '1+ touch, a previous game row, snap line, played in w+1; doc 438); predictors = xfp2 (mean expected half-PPR '
      'over the last two games) and dxfp (xfp_w minus xfp of the previous game); outcomes = next4 mean (2+ games), '
      'spike w+1, startable w+1, startable next four; direction = a rise adds over the level; FALSIFIER = the dxfp '
      'coefficient in OLS of next4 on xfp2 and dxfp is under +0.10 a point, or the delta-only top-fifth cell is under '
      '+2 points of startable-next-four over the pool.')
p['dxfp'] = p.xfp - p.xfp_prev
print(f'\nn={len(p)}  dxfp mean {p.dxfp.mean():+.2f}, sd {p.dxfp.std():.2f}; xfp2 mean {p.xfp2.mean():.2f}, sd {p.xfp2.std():.2f}; '
      f'corr(xfp2, dxfp) {p[["xfp2","dxfp"]].corr().iloc[0,1]:+.3f}')
print('\n(a) OLS of next4 on xfp2 and dxfp (2+ games ahead), HC1 se:')
for pos in ['ALL', 'RB', 'WR', 'TE']:
    q = p if pos == 'ALL' else p[p.position == pos]; q = q[q.next4_n >= 2]
    res = ols(q.next4, np.column_stack([q.xfp2, q.dxfp]), ['xfp2', 'dxfp'])
    print(f'  {pos:3s} ' + fmt_ols(res))
    # the same thing as this game and last game separately (the algebra of xfp2 + dxfp), for the reader
    res2 = ols(q.next4, np.column_stack([q.xfp, q.xfp_prev]), ['xfp_w', 'xfp_prev'])
    print(f'      as the two games separately: ' + fmt_ols(res2))
print('  (dxfp coefficient under +0.10 = falsified on the regression half)')
print('\n(a2) the same with start4 as 0/1 (linear probability, coefficients in percentage points per point of xfp):')
for pos in ['ALL', 'RB', 'WR', 'TE']:
    q = p if pos == 'ALL' else p[p.position == pos]; q = q[q.next4_n >= 2]
    res = ols(q.start4.astype(float), np.column_stack([q.xfp2, q.dxfp]), ['xfp2', 'dxfp'])
    print(f'  {pos:3s} ' + fmt_ols(res, 100, ' pts'))

print('\n(b) top fifth by dxfp against top fifth by xfp2, and (c) the cross, by position and pooled:')
for pos in ['ALL', 'RB', 'WR', 'TE']:
    q = p if pos == 'ALL' else p[p.position == pos]
    cl = q.xfp2.quantile(0.8); cd = q.dxfp.quantile(0.8)
    L = q.xfp2 >= cl; D = q.dxfp >= cd
    print(f'  {pos:3s} n={len(q):5d}  cuts: xfp2 {cl:.2f}  dxfp {cd:+.2f}')
    print('    ' + line('the pool', q, w=44))
    print('    ' + line('top fifth by xfp2 (level)', q[L], w=44))
    print('    ' + line('top fifth by dxfp (delta)', q[D], w=44))
    print('    ' + line('both top fifths', q[L & D], w=44))
    print('    ' + line('level only', q[L & ~D], w=44))
    print('    ' + line('delta only', q[~L & D], w=44))
    print('    ' + line('neither', q[~L & ~D], w=44))
    pool4 = q[q.next4_n >= 2].start4.mean(); do4 = q[~L & D & (q.next4_n >= 2)].start4.mean()
    lo4 = q[L & ~D & (q.next4_n >= 2)].start4.mean(); bo4 = q[L & D & (q.next4_n >= 2)].start4.mean()
    ne4 = q[~L & ~D & (q.next4_n >= 2)].start4.mean()
    print(f'    delta-only minus pool, start next4: {(do4-pool4)*100:+.1f} points; level-only minus pool {(lo4-pool4)*100:+.1f}; '
          f'both minus pool {(bo4-pool4)*100:+.1f}; interaction (both - level - delta + neither) '
          f'{(bo4-lo4-do4+ne4)*100:+.1f} points')
    # also: within the top fifth by level, does the delta split it?
    ql = q[L & (q.next4_n >= 2)]
    print(f'    inside the level top fifth: rising (dxfp > 0) start next4 {ql[ql.dxfp>0].start4.mean()*100:.1f}% (n={int((ql.dxfp>0).sum())}) '
          f'vs falling {ql[ql.dxfp<=0].start4.mean()*100:.1f}% (n={int((ql.dxfp<=0).sum())})')
print('  (delta-only cell under +2 points of start next4 over the pool = falsified on the cell half)')

# =============================================================================================================
# TEST 3: Matt's claim, a rise in both snap share and targets
# =============================================================================================================
print('\n' + '=' * 110)
print('TEST 3: a week-over-week RISE in BOTH snap share and targets, net of the level of either')
print('=' * 110)
print('TESTABLE FORM: population = the same xfp_backtest pool restricted to rows whose previous game carries a snap '
      'line (RB/WR/TE, not startable in w); predictors = d_snap = snap_pct_w minus snap_pct of the previous game, '
      'd_tgt = targets_w minus targets of the previous game, and the indicator both_rose = (d_snap > 0 and d_tgt > 0), '
      'entered alongside the LEVELS snap_pct_w and targets_w; outcome = startable over the next four weeks (0/1, 2+ '
      'games), also spike w+1, startable w+1, next4 mean; direction = both rising adds over the levels; FALSIFIER = '
      'the both_rose coefficient net of levels is under +3.0 points of start4, in which case the level alone is the '
      'signal. Matt\'s words: "counts on the field and targets combined are a signal for a player whose role could '
      'expand... we are picking from the bottom of the bottom."')
t3 = p[p.snap_prev.notna()].copy()
t3['d_snap'] = t3.snap_pct - t3.snap_prev
t3['d_tgt'] = t3.targets - t3.tgt_prev
t3['snap_rose'] = t3.d_snap > 0
t3['tgt_rose'] = t3.d_tgt > 0
t3['both_rose'] = t3.snap_rose & t3.tgt_rose
t3['strict'] = (t3.d_snap >= 10) & (t3.d_tgt >= 3)
print(f'\nn={len(t3)} of {len(p)} (dropped {len(p)-len(t3)} whose previous game has no snap line)  '
      + '  '.join(f'{k} {v}' for k, v in t3.position.value_counts().items()))
print(f'd_snap mean {t3.d_snap.mean():+.1f} sd {t3.d_snap.std():.1f}; d_tgt mean {t3.d_tgt.mean():+.2f} sd {t3.d_tgt.std():.2f}; '
      f'corr(d_snap, d_tgt) {t3[["d_snap","d_tgt"]].corr().iloc[0,1]:+.3f}; corr(snap_pct, d_snap) '
      f'{t3[["snap_pct","d_snap"]].corr().iloc[0,1]:+.3f}; corr(targets, d_tgt) {t3[["targets","d_tgt"]].corr().iloc[0,1]:+.3f}')
print(f'calendar-adjacent (previous game was week w-1 exactly): {(t3.prev_week == t3.week-1).mean()*100:.1f}%')

def cells(q, tag, w=30):
    print('    ' + line('the pool', q, w=w))
    print('    ' + line('both rose', q[q.both_rose], w=w))
    print('    ' + line('only snaps rose', q[q.snap_rose & ~q.tgt_rose], w=w))
    print('    ' + line('only targets rose', q[~q.snap_rose & q.tgt_rose], w=w))
    print('    ' + line('neither rose', q[~q.snap_rose & ~q.tgt_rose], w=w))

print('\n(a) the four cells, pooled and by position:')
for pos in ['ALL', 'RB', 'WR', 'TE']:
    q = t3 if pos == 'ALL' else t3[t3.position == pos]
    print(f'  {pos} n={len(q)}')
    cells(q, pos)

print('\n(b) OLS, levels and deltas, HC1 se. Outcome start4 (0/1, 2+ games ahead) in percentage points; then next4 in points.')
print('    spec A: levels + both_rose (the falsifier\'s object: the indicator net of the LEVELS)')
print('    spec B: levels + d_snap + d_tgt + both_rose (the indicator net of levels AND the single rises)')
for pos in ['ALL', 'RB', 'WR', 'TE']:
    q = t3 if pos == 'ALL' else t3[t3.position == pos]
    q4 = q[q.next4_n >= 2]
    XA = np.column_stack([q4.snap_pct, q4.targets, q4.both_rose.astype(float)])
    XB = np.column_stack([q4.snap_pct, q4.targets, q4.d_snap, q4.d_tgt, q4.both_rose.astype(float)])
    if pos == 'ALL':   # position dummies in the pooled model so RB's bar and rates are not read as a signal
        pw = (q4.position == 'WR').astype(float).values; pt = (q4.position == 'TE').astype(float).values
        XA = np.column_stack([XA, pw, pt]); XB = np.column_stack([XB, pw, pt])
        nA = ['snap_pct', 'targets', 'both_rose', 'WR', 'TE']; nB = ['snap_pct', 'targets', 'd_snap', 'd_tgt', 'both_rose', 'WR', 'TE']
    else:
        nA = ['snap_pct', 'targets', 'both_rose']; nB = ['snap_pct', 'targets', 'd_snap', 'd_tgt', 'both_rose']
    print(f'  {pos} start4, spec A: ' + fmt_ols(ols(q4.start4.astype(float), XA, nA), 100, ' pts'))
    print(f'  {pos} start4, spec B: ' + fmt_ols(ols(q4.start4.astype(float), XB, nB), 100, ' pts'))
    print(f'  {pos} next4,  spec A: ' + fmt_ols(ols(q4.next4, XA, nA)))
    print(f'  {pos} next4,  spec B: ' + fmt_ols(ols(q4.next4, XB, nB)))
    # levels only, for the reader: what the level alone carries
    XL = XA[:, [0, 1] + list(range(3, XA.shape[1]))]; nL = [nA[0], nA[1]] + nA[3:]
    print(f'  {pos} start4, levels only: ' + fmt_ols(ols(q4.start4.astype(float), XL, nL), 100, ' pts'))

print('\n(b2) the other reading of "net of the level": net of the PREVIOUS game\'s levels (snap_prev, tgt_prev), where a rise '
      'carries the current level with it; and net of BOTH games\' levels, where it is the shape of the two-game path only')
for pos in ['ALL', 'RB', 'WR', 'TE']:
    q = t3 if pos == 'ALL' else t3[t3.position == pos]
    q4 = q[q.next4_n >= 2]
    XC = np.column_stack([q4.snap_prev, q4.tgt_prev, q4.both_rose.astype(float)])
    XD = np.column_stack([q4.snap_pct, q4.targets, q4.snap_prev, q4.tgt_prev, q4.both_rose.astype(float)])
    nC = ['snap_prev', 'tgt_prev', 'both_rose']; nD = ['snap_pct', 'targets', 'snap_prev', 'tgt_prev', 'both_rose']
    if pos == 'ALL':
        pw = (q4.position == 'WR').astype(float).values; pt = (q4.position == 'TE').astype(float).values
        XC = np.column_stack([XC, pw, pt]); XD = np.column_stack([XD, pw, pt]); nC = nC + ['WR', 'TE']; nD = nD + ['WR', 'TE']
    print(f'  {pos} start4, spec C (previous game\'s levels): ' + fmt_ols(ols(q4.start4.astype(float), XC, nC), 100, ' pts'))
    print(f'  {pos} start4, spec D (both games\' levels):     ' + fmt_ols(ols(q4.start4.astype(float), XD, nD), 100, ' pts'))

print('\n(c) the interaction on the raw cells (start4, 2+ games): gain of each cell over "neither rose", and both minus the sum')
for pos in ['ALL', 'RB', 'WR', 'TE']:
    q = t3 if pos == 'ALL' else t3[t3.position == pos]
    q = q[q.next4_n >= 2]
    ne = q[~q.snap_rose & ~q.tgt_rose].start4; so = q[q.snap_rose & ~q.tgt_rose].start4
    to = q[~q.snap_rose & q.tgt_rose].start4; bo = q[q.both_rose].start4
    gs = so.mean() - ne.mean(); gt = to.mean() - ne.mean(); gb = bo.mean() - ne.mean()
    inter = gb - gs - gt
    se_i = np.sqrt(sum(x.var(ddof=1) / len(x) for x in (ne, so, to, bo)))
    which = 'AMPLIFICATION (both beats the sum)' if inter > 0 else 'SUBSTITUTION (both is less than the sum)'
    print(f'  {pos:3s} snaps-only {gs*100:+.1f}  targets-only {gt*100:+.1f}  both {gb*100:+.1f}  '
          f'sum of singles {(gs+gt)*100:+.1f}  interaction {inter*100:+.1f} (se {se_i*100:.1f})  -> {which}'
          f'{"" if abs(inter) > 2*se_i else ", inside two se, call it null"}')
    # the same on next4 points
    ne_, so_, to_, bo_ = (q[~q.snap_rose & ~q.tgt_rose].next4, q[q.snap_rose & ~q.tgt_rose].next4,
                          q[~q.snap_rose & q.tgt_rose].next4, q[q.both_rose].next4)
    gs_ = so_.mean() - ne_.mean(); gt_ = to_.mean() - ne_.mean(); gb_ = bo_.mean() - ne_.mean()
    se_j = np.sqrt(sum(x.var(ddof=1) / len(x) for x in (ne_, so_, to_, bo_)))
    print(f'      next4: snaps-only {gs_:+.2f}  targets-only {gt_:+.2f}  both {gb_:+.2f}  sum {gs_+gt_:+.2f}  '
          f'interaction {gb_-gs_-gt_:+.2f} (se {se_j:.2f})')

print('\n(d) the stricter version: d_snap >= 10 points AND d_tgt >= 3 targets')
for pos in ['ALL', 'RB', 'WR', 'TE']:
    q = t3 if pos == 'ALL' else t3[t3.position == pos]
    print(f'  {pos} n={len(q)}')
    print('    ' + line('the pool', q, w=44))
    print('    ' + line('strict both (snaps +10, targets +3)', q[q.strict], w=44))
    print('    ' + line('not strict', q[~q.strict], w=44))
    q4 = q[q.next4_n >= 2]
    XA = np.column_stack([q4.snap_pct, q4.targets, q4.strict.astype(float)])
    XB = np.column_stack([q4.snap_pct, q4.targets, q4.d_snap, q4.d_tgt, q4.strict.astype(float)])
    if pos == 'ALL':
        pw = (q4.position == 'WR').astype(float).values; pt = (q4.position == 'TE').astype(float).values
        XA = np.column_stack([XA, pw, pt]); XB = np.column_stack([XB, pw, pt])
        nA = ['snap_pct', 'targets', 'strict', 'WR', 'TE']; nB = ['snap_pct', 'targets', 'd_snap', 'd_tgt', 'strict', 'WR', 'TE']
    else:
        nA = ['snap_pct', 'targets', 'strict']; nB = ['snap_pct', 'targets', 'd_snap', 'd_tgt', 'strict']
    print(f'    start4 spec A: ' + fmt_ols(ols(q4.start4.astype(float), XA, nA), 100, ' pts'))
    print(f'    start4 spec B: ' + fmt_ols(ols(q4.start4.astype(float), XB, nB), 100, ' pts'))
    print(f'    next4  spec A: ' + fmt_ols(ols(q4.next4, XA, nA)))
    s4 = q4[q4.strict].start4.mean(); pool = q4.start4.mean()
    print(f'    strict cell minus pool, start next4: {(s4-pool)*100:+.1f} points (n strict {int(q4.strict.sum())})')

print('\n(e) sensitivity: calendar-adjacent rows only (previous game was week w-1), pooled, start4 spec A and B')
qq = t3[(t3.prev_week == t3.week - 1) & (t3.next4_n >= 2)]
pw = (qq.position == 'WR').astype(float).values; pt = (qq.position == 'TE').astype(float).values
XA = np.column_stack([qq.snap_pct, qq.targets, qq.both_rose.astype(float), pw, pt])
XB = np.column_stack([qq.snap_pct, qq.targets, qq.d_snap, qq.d_tgt, qq.both_rose.astype(float), pw, pt])
print('  spec A: ' + fmt_ols(ols(qq.start4.astype(float), XA, ['snap_pct', 'targets', 'both_rose', 'WR', 'TE']), 100, ' pts'))
print('  spec B: ' + fmt_ols(ols(qq.start4.astype(float), XB, ['snap_pct', 'targets', 'd_snap', 'd_tgt', 'both_rose', 'WR', 'TE']), 100, ' pts'))
XS = np.column_stack([qq.snap_pct, qq.targets, qq.strict.astype(float), pw, pt])
print('  strict, spec A: ' + fmt_ols(ols(qq.start4.astype(float), XS, ['snap_pct', 'targets', 'strict', 'WR', 'TE']), 100, ' pts'))

print('\n(f) by season, pooled: both_rose coefficient on start4 net of levels (spec A), percentage points')
for s_, q in t3[t3.next4_n >= 2].groupby('season'):
    pw = (q.position == 'WR').astype(float).values; pt = (q.position == 'TE').astype(float).values
    XA = np.column_stack([q.snap_pct, q.targets, q.both_rose.astype(float), pw, pt])
    r = ols(q.start4.astype(float), XA, ['snap_pct', 'targets', 'both_rose', 'WR', 'TE'])[0]['both_rose']
    print(f'  {s_}: both_rose {r[0]*100:+.1f} (se {r[1]*100:.1f})  n={len(q)}')

print('\ndone')
