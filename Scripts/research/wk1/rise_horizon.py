"""rise_horizon.py -- finding 4.38 on a longer horizon (claude_todo: "THE RISE ON A LONGER HORIZON (4.38 scope).
Same script, outcome = startable over the next eight weeks and over the rest of the season; Matt's 'role could
expand' may live there.")

Population, predictors and the falsifier are delta_screen.py TEST 3's (doc 440), verbatim; only the OUTCOME changes:
  start4   startable over the next four weeks (mean of the next four game rows at or above the position bar, 2+ rows)
  start8   the same over the next eight weeks (4+ rows)
  startROS the same over every remaining week of the season (4+ rows)
  peak8    the best four-game stretch inside the next eight weeks clears the bar (role EXPANDS at some point)
Standard library plus pandas and numpy only. Spearman is rank-then-Pearson; no scipy.
"""
import os, sys, urllib.request
import pandas as pd, numpy as np
import numpy.linalg as la

HERE = os.path.dirname(os.path.abspath(__file__))
# The nflverse cache this run reads. Fixed to the work5 cache so the population is the one doc 438 built.
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


# ---- horizons ------------------------------------------------------------------------------------------------
for k in range(5, 18):
    d[f'n{k}'] = future(k)
N8 = [f'n{k}' for k in range(1, 9)]
NR = [f'n{k}' for k in range(1, 18)]
d['next8_n'] = d[N8].notna().sum(axis=1)
d['next8'] = d[N8].mean(axis=1)
d['ros_n'] = d[NR].notna().sum(axis=1)
d['ros'] = d[NR].mean(axis=1)
d['start8'] = d.next8 >= d.bar
d['startROS'] = d.ros >= d.bar
# the best four-game stretch inside the next eight (consecutive game rows, not calendar weeks)
arr = d[N8].values
best = np.full(len(d), np.nan)
for i in range(len(d)):
    row = arr[i][~np.isnan(arr[i])]
    if len(row) >= 4:
        best[i] = max(row[j:j+4].mean() for j in range(len(row) - 3))
d['peak8'] = best >= d.bar
d['peak8_ok'] = ~np.isnan(best)

p = d[(d.week >= 2) & (d.week <= 16) & (d.std_avg < d.bar) & ((d.targets + d.carries) > 0)
      & d.prev_week.notna() & d.n1.notna() & d.xfp2.notna() & d.snap_pct.notna()].copy()
t3 = p[p.snap_prev.notna()].copy()
t3['d_snap'] = t3.snap_pct - t3.snap_prev
t3['d_tgt'] = t3.targets - t3.tgt_prev
t3['both_rose'] = (t3.d_snap > 0) & (t3.d_tgt > 0)
t3['strict'] = (t3.d_snap >= 10) & (t3.d_tgt >= 3)
print(f'\nTEST 3 POPULATION n={len(t3)}  ' + '  '.join(f'{k} {v}' for k, v in t3.position.value_counts().items()))

print('\nTESTABLE FORM: the doc 440 TEST 3 population and predictors (both_rose = snap share AND targets rose from the '
      'previous game, entered beside the LEVELS snap_pct and targets); OUTCOMES = start4 (2+ rows), start8 (4+ rows), '
      'startROS (4+ rows), peak8 (best four-game stretch inside the next eight clears the bar); DIRECTION = a rise adds '
      'over the levels on the longer horizons where it did not on four weeks; FALSIFIER = the both_rose coefficient net '
      'of levels is under +3.0 points on every horizon, in which case the rise is not a role-expansion signal either.')

def ols(y, X, names):
    X1 = np.column_stack([np.ones(len(y)), X]); y = np.asarray(y, float)
    b, *_ = la.lstsq(X1, y, rcond=None)
    r = y - X1 @ b
    XtXi = la.inv(X1.T @ X1)
    V = XtXi @ (X1.T * (r ** 2)) @ X1 @ XtXi * len(y) / (len(y) - X1.shape[1])
    se = np.sqrt(np.diag(V))
    return {n: (b[i + 1], se[i + 1]) for i, n in enumerate(names)}

OUT = [('start4', 'next4_n', 2), ('start8', 'next8_n', 4), ('startROS', 'ros_n', 4), ('peak8', 'next8_n', 4)]
print('\n(a) the both_rose coefficient net of the levels (spec A, HC1 se; the pooled row carries WR and TE dummies as doc 440 did), percentage points, by horizon:')
print(f'  {"":6s}' + ''.join(f'{o:>22s}' for o, _, _ in OUT))
for pos in ['ALL', 'RB', 'WR', 'TE']:
    q = t3 if pos == 'ALL' else t3[t3.position == pos]
    cells = []
    for o, nc, m in OUT:
        qq = q[q[nc] >= m]
        if o == 'peak8':
            qq = qq[qq.peak8_ok]
        X = [qq.snap_pct, qq.targets, qq.both_rose.astype(float)]
        names = ['snap_pct', 'targets', 'both_rose']
        if pos == 'ALL':                       # position dummies on the pooled row, as doc 440's spec A had
            X += [(qq.position == 'WR').astype(float), (qq.position == 'TE').astype(float)]
            names += ['WR', 'TE']
        r = ols(qq[o].astype(float), np.column_stack(X), names)['both_rose']
        cells.append(f'{r[0]*100:+6.1f} (se {r[1]*100:4.1f}) n={len(qq):5d}')
    print(f'  {pos:6s}' + ''.join(f'{c:>22s}' for c in cells))

print('\n(b) raw cells, pooled: both rose vs neither rose, each horizon (rate in %, n)')
for o, nc, m in OUT:
    qq = t3[t3[nc] >= m]
    if o == 'peak8':
        qq = qq[qq.peak8_ok]
    b = qq[qq.both_rose][o]; n_ = qq[~qq.both_rose][o]; pool = qq[o]
    print(f'  {o:9s} pool {pool.mean()*100:5.1f}% (n={len(pool)})   both rose {b.mean()*100:5.1f}% (n={len(b)})   '
          f'neither/one {n_.mean()*100:5.1f}% (n={len(n_)})   raw gap {(b.mean()-n_.mean())*100:+.1f}')

print('\n(c) the strict rise (snaps +10 points, targets +3), pooled, net of levels:')
for o, nc, m in OUT:
    qq = t3[t3[nc] >= m]
    if o == 'peak8':
        qq = qq[qq.peak8_ok]
    r = ols(qq[o].astype(float), np.column_stack([qq.snap_pct, qq.targets, qq.strict.astype(float),
                                                 (qq.position == 'WR').astype(float), (qq.position == 'TE').astype(float)]),
            ['snap_pct', 'targets', 'strict', 'WR', 'TE'])['strict']
    print(f'  {o:9s} strict {r[0]*100:+6.1f} (se {r[1]*100:4.1f})  n={len(qq)}  strict cell rate '
          f'{qq[qq.strict][o].mean()*100:5.1f}% (n={int(qq.strict.sum())}) vs pool {qq[o].mean()*100:5.1f}%')

print('\n(d) by season, pooled, both_rose net of levels on start8 and peak8:')
for s in range(2021, 2026):
    q = t3[t3.season == s]
    out = []
    for o, nc, m in (('start8', 'next8_n', 4), ('peak8', 'next8_n', 4)):
        qq = q[q[nc] >= m]
        if o == 'peak8':
            qq = qq[qq.peak8_ok]
        r = ols(qq[o].astype(float), np.column_stack([qq.snap_pct, qq.targets, qq.both_rose.astype(float),
                                                     (qq.position == 'WR').astype(float), (qq.position == 'TE').astype(float)]),
                ['snap_pct', 'targets', 'both_rose', 'WR', 'TE'])['both_rose']
        out.append(f'{o} {r[0]*100:+5.1f} (se {r[1]*100:3.1f}) n={len(qq)}')
    print(f'  {s}: ' + '   '.join(out))

print('\n(e) the level, for scale: startable-next-eight by targets-in-week-w band, pooled (the signal 4.38 says to use)')
qq = t3[t3.next8_n >= 4]
for lo, hi in ((0, 2), (3, 4), (5, 7), (8, 99)):
    c = qq[(qq.targets >= lo) & (qq.targets <= hi)]
    print(f'  targets {lo}-{hi if hi < 99 else "+"}: start8 {c.start8.mean()*100:5.1f}%  peak8 {c.peak8.mean()*100:5.1f}%  n={len(c)}')
print('\ndone')
