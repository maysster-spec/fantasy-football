"""xfp_backtest.py -- does EXPECTED fantasy points (ffverse ep_weekly) over the last two games predict a
claimable man's next four weeks better than his ACTUAL points, and does it lift the wire's three-signal
workload screen (targets 8+, snaps 80%+, target share 20%+) as a fourth signal?

TESTABLE FORM, stated before the run (0.5(a2)):
  POPULATION  RB, WR and TE player-weeks, REG 2021-2025, weeks 2-16, NOT startable in week w on 4.13b's bar
              (season-to-date half-PPR average through w below RB 9.92 / WR 9.62 / TE 8.25), at least one
              target or carry in w, a game row in w-1 (so "last two games" exists), and played in w+1.
  PREDICTORS  measured through week w: ACT2 = mean actual half-PPR over games w-1 and w;
              XFP2 = mean expected half-PPR (ffverse, full-PPR minus 0.5 per expected reception) over the same
              two games; the three-signal count in week w.
  OUTCOMES    spike in w+1 (18.0+ half-PPR); startable in w+1 (>= bar); NEXT4 = mean half-PPR over the games he
              plays in w+1..w+4 (2+ games), and startable over those four (NEXT4 >= bar).
  FALSIFIER   fixed in advance (doc 437): if the top fifth by XFP2 is under +2 points of spike rate over the top
              fifth by ACT2, and adding XFP2 as a fourth signal is under +2 points over the three-signal count
              alone, xfp stays a DISPLAY column and does not enter the screen.
"""
import os, sys, urllib.request
import pandas as pd, numpy as np

# Paths resolve against THIS file (0.4): Scripts\research\wk1\xfp_backtest.py. The nflverse weekly
# files are the research cache build_form.py already keeps; snap counts, players.csv and the five
# ffverse files are fetched once into the same cache if absent, and the fetch says so.
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get('FF_CACHE') or os.path.normpath(os.path.join(HERE, '..', '_nflverse_cache'))
NFLV = 'https://github.com/nflverse/nflverse-data/releases/download/'
FFV = 'https://github.com/ffverse/ffopportunity/releases/download/latest-data/'

def _get(name, url):
    """The cached file if present (also checks the ir\ folder, which holds snaps_<season>.csv and
    players.csv for the IR scripts), else one fetch into the cache."""
    for d in (CACHE, HERE, os.path.join(HERE, '..', 'ir')):
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

# ---- actuals, this league's half-PPR, from the nflverse weekly file ----------------------------------------
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
e['afp_ff'] = e.rec_fantasy_points + e.rush_fantasy_points - 0.5 * e.receptions   # ffverse's own actual, for the join check
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
# next-week and next-four by CALENDAR week (a missed week is a missed week; byes are excluded because the
# team has no game row, so a bye inside w+1..w+4 simply shortens the window)
key = d.set_index(['season', 'player_id', 'week']).hppr
def future(k):
    idx = pd.MultiIndex.from_arrays([d.season, d.player_id, d.week + k])
    return key.reindex(idx).values
for k in range(1, 5):
    d[f'n{k}'] = future(k)
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

# ---- the population --------------------------------------------------------------------------------------------
p = d[(d.week >= 2) & (d.week <= 16) & (d.std_avg < d.bar) & ((d.targets + d.carries) > 0)
      & d.prev_week.notna() & d.n1.notna() & d.xfp2.notna() & d.snap_pct.notna()].copy()
print(f'\nPOPULATION n={len(p)}  ' + '  '.join(f'{k} {v}' for k, v in p.position.value_counts().items()))
print(f'base rates: spike {p.spike.mean()*100:.1f}%  startable w+1 {p.start1.mean()*100:.1f}%  '
      f'startable next four {p[p.next4_n>=2].start4.mean()*100:.1f}% (n={int((p.next4_n>=2).sum())})  '
      f'next-four mean {p.next4.mean():.2f}')
print(f'xfp2 vs act2: mean {p.xfp2.mean():.2f} vs {p.act2.mean():.2f}, corr {p[["xfp2","act2"]].corr().iloc[0,1]:.3f}')

def se(x):
    x = np.asarray(x, float); return x.std(ddof=1) / np.sqrt(len(x))

def top(pop, col, q=0.8):
    return pop[pop[col] >= pop[col].quantile(q)]

def line(label, sub):
    s4 = sub[sub.next4_n >= 2]
    return (f'{label:52s} n={len(sub):5d}  spike {sub.spike.mean()*100:5.1f}%  start w+1 {sub.start1.mean()*100:5.1f}%  '
            f'start next4 {s4.start4.mean()*100:5.1f}%  next4 {sub.next4.mean():5.2f}')

# ==== TEST 1: which two-game number predicts the next four weeks? ==============================================
print('\n==== TEST 1: two-game ACTUAL vs two-game EXPECTED as a predictor, whole pool and by position ====')
for pos in ['ALL', 'RB', 'WR', 'TE']:
    q = p if pos == 'ALL' else p[p.position == pos]
    q4 = q[q.next4_n >= 2]
    ra = spearman(q4.act2, q4.next4); rx = spearman(q4.xfp2, q4.next4)
    r1a = spearman(q.act2, q.n1); r1x = spearman(q.xfp2, q.n1)
    print(f'{pos:3s} n={len(q):5d}  rho with NEXT4: act2 {ra:.3f}  xfp2 {rx:.3f}   |  rho with w+1: act2 {r1a:.3f}  xfp2 {r1x:.3f}')
    print('   ' + line('top fifth by ACT2', top(q, 'act2')))
    print('   ' + line('top fifth by XFP2', top(q, 'xfp2')))
    print('   ' + line('top fifth by BOTH', q[(q.act2 >= q.act2.quantile(.8)) & (q.xfp2 >= q.xfp2.quantile(.8))]))
    print('   ' + line('top fifth XFP2, NOT top fifth ACT2', q[(q.act2 < q.act2.quantile(.8)) & (q.xfp2 >= q.xfp2.quantile(.8))]))
    print('   ' + line('top fifth ACT2, NOT top fifth XFP2', q[(q.act2 >= q.act2.quantile(.8)) & (q.xfp2 < q.xfp2.quantile(.8))]))

# regression: next4 on act2 and xfp2 jointly (does xfp carry information given actual?)
import numpy.linalg as la
def ols(y, X):
    X = np.column_stack([np.ones(len(y)), X]); b, *_ = la.lstsq(X, y, rcond=None)
    r = y - X @ b; s2 = r @ r / (len(y) - X.shape[1]); cov = s2 * la.inv(X.T @ X)
    return b, np.sqrt(np.diag(cov))
print('\nOLS of NEXT4 on both (pool, 2+ games ahead):')
for pos in ['ALL', 'RB', 'WR', 'TE']:
    q = p if pos == 'ALL' else p[p.position == pos]; q = q[q.next4_n >= 2]
    b, s = ols(q.next4.values, np.column_stack([q.act2.values, q.xfp2.values]))
    print(f'  {pos:3s} n={len(q):5d}  act2 {b[1]:+.3f} (se {s[1]:.3f})   xfp2 {b[2]:+.3f} (se {s[2]:.3f})')
    b, s = ols(q.next4.values, np.column_stack([q.xfp2.values, (q.act2 - q.xfp2).values]))
    print(f'       as xfp2 + (act2 - xfp2): xfp2 {b[1]:+.3f} (se {s[1]:.3f})   over-expected {b[2]:+.3f} (se {s[2]:.3f})')

# ==== TEST 2: the screen, and xfp as a fourth signal ===========================================================
print('\n==== TEST 2: the three-signal screen, WR/TE (its gate), then xfp as a fourth signal ====')
w = p[p.position.isin(['WR', 'TE'])].copy()
print(f'WR/TE pool n={len(w)}  base spike {w.spike.mean()*100:.1f}%  start w+1 {w.start1.mean()*100:.1f}%')
for k in range(4):
    print('  ' + line(f'{k} of 3 signals', w[w.sig3 == k]))
print('  ' + line('2+ of 3 (the operative bar)', w[w.sig3 >= 2]))
# xfp fourth signal: a bar at the WR/TE pool's top fifth on the single-week xfp and on xfp2
for col, nm in [('xfp', 'week-w xfp'), ('xfp2', 'two-game xfp2')]:
    cut = w[col].quantile(0.8)
    w['s_x'] = w[col] >= cut
    print(f'\n  fourth signal = {nm} >= {cut:.2f} (top fifth of the pool)')
    a = w[w.sig3 >= 2]; b_ = w[(w.sig3 >= 2) & w.s_x]; c_ = w[(w.sig3 >= 2) & ~w.s_x]
    print('   ' + line('2+ of 3', a))
    print('   ' + line('2+ of 3 AND xfp signal', b_))
    print('   ' + line('2+ of 3 and NOT xfp signal', c_))
    print('   ' + line('xfp signal alone, fewer than 2 of 3', w[(w.sig3 < 2) & w.s_x]))
    gain = (b_.spike.mean() - a.spike.mean()) * 100
    print(f'   GAIN in spike rate from the fourth signal, on the 2+ bar: {gain:+.1f} points '
          f'(se about {np.sqrt(b_.spike.var()/len(b_) + a.spike.var()/len(a))*100:.1f});  '
          f'startable next four: {(b_[b_.next4_n>=2].start4.mean()-a[a.next4_n>=2].start4.mean())*100:+.1f} points')
    w['sig4'] = w.sig3 + w.s_x
    for k in range(5):
        print('     ' + line(f'{k} of 4', w[w.sig4 == k]))

# permutation check on the fourth-signal gain, spike outcome, xfp2
cut = w.xfp2.quantile(0.8); w['s_x'] = w.xfp2 >= cut
a = w[w.sig3 >= 2].copy(); obs = a[a.s_x].spike.mean() - a[~a.s_x].spike.mean()
perm = []
sx = a.s_x.values.copy(); sp = a.spike.values
for _ in range(2000):
    rng.shuffle(sx); perm.append(sp[sx].mean() - sp[~sx].mean())
perm = np.array(perm)
print(f'\n  inside the 2+ bar, xfp2 top fifth vs rest, spike: {obs*100:+.1f} points, permutation p={np.mean(np.abs(perm)>=abs(obs)):.3f}')

# ==== TEST 3: RB, the screen does not apply; xfp2 vs act2 only, and a backfield-share comparison ====================
print('\n==== TEST 3: RB claimable pool, xfp2 vs act2 vs week-w touches ====')
r = p[p.position == 'RB'].copy(); r['touch'] = r.targets + r.carries
for col in ['act2', 'xfp2', 'touch', 'snap_pct']:
    print('  ' + line(f'top fifth by {col}', top(r, col)))
print('  ' + line('top fifth xfp2 AND top fifth touch', r[(r.xfp2 >= r.xfp2.quantile(.8)) & (r.touch >= r.touch.quantile(.8))]))

# ==== 2026 sanity: what the current form file says on the same definitions ===========================

# ==== ROBUSTNESS: by season, against WOPR, the two fixed-bar flags, and mean reversion ===================
print('\n==== by season, rho with NEXT4 (2+ games), whole pool ====')
for s_, q in p[p.next4_n >= 2].groupby('season'):
    print(f'  {s_}: act2 {spearman(q.act2, q.next4):.3f}  xfp2 {spearman(q.xfp2, q.next4):.3f}  n={len(q)}')
print('\n==== WR/TE: the existing best single signal (WOPR, doc 389) against xfp2, same pool ====')
for col in ['wopr', 'targets', 'xfp', 'xfp2', 'act2']:
    print('  ' + line(f'top fifth by {col}', w[w[col] >= w[col].quantile(.8)]))
print('  ' + line('top fifth WOPR AND top fifth xfp2', w[(w.wopr >= w.wopr.quantile(.8)) & (w.xfp2 >= w.xfp2.quantile(.8))]))
print('  ' + line('top fifth WOPR, NOT top fifth xfp2', w[(w.wopr >= w.wopr.quantile(.8)) & (w.xfp2 < w.xfp2.quantile(.8))]))
print('  ' + line('top fifth xfp2, NOT top fifth WOPR', w[(w.wopr < w.wopr.quantile(.8)) & (w.xfp2 >= w.xfp2.quantile(.8))]))
print('\n==== the two flags on FIXED bars, whole pool (the bars wire.py prints) ====')
print('  ' + line('box-score mirage: act2 >= 8 and xfp2 < 5', p[(p.act2 >= 8) & (p.xfp2 < 5)]))
print('  ' + line('quiet volume: xfp2 >= 8 and act2 < 5', p[(p.xfp2 >= 8) & (p.act2 < 5)]))
print('  ' + line('the pool', p))
p['oe2'] = p.act2 - p.xfp2
p['oe_bin'] = pd.qcut(p.oe2, 5, labels=['most under', 'under', 'mid', 'over', 'most over'])
print('\n==== two-game points over expected, fifths: next-four points minus xfp2 (2+ games ahead) ====')
q = p[p.next4_n >= 2]
print(q.groupby('oe_bin', observed=True).apply(lambda g: pd.Series({
    'n': len(g), 'oe2': g.oe2.mean(), 'xfp2': g.xfp2.mean(), 'act2': g.act2.mean(), 'next4': g.next4.mean(),
    'next4_minus_xfp2': (g.next4 - g.xfp2).mean(), 'start4%': g.start4.mean() * 100})).round(2).to_string())

p.to_pickle(os.path.join(HERE, 'xfp_pool.pkl'))
print('\npool pickled beside the script as xfp_pool.pkl')
