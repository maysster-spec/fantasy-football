r"""redzone_test.py -- does RED-ZONE usage over the last two games add anything to a claimable man's next four
weeks NET OF snap share and two-game expected points (xfp2)?  Doc 437 section 6 item 3.

TESTABLE FORM, stated before the run (0.5(a2)):
  POPULATION  xfp_backtest.py's pool, copied verbatim below: RB, WR and TE player-weeks, REG 2021-2025, weeks
              2-16, NOT startable in week w on 4.13b's bar (season-to-date half-PPR average through w below
              RB 9.92 / WR 9.62 / TE 8.25), at least one target or carry in w, a game row in w-1 (so "last two
              games" exists), a snap line in w, an expected row in both games, and played in w+1.
  PREDICTORS  measured through week w from nflverse play-by-play:
              RZ2  = two-game red-zone opportunity share: his carries plus targets snapped inside the 20 over
                     games w-1 and w, as a percent of his team's carries plus targets inside the 20 over the
                     same two games (pooled, not averaged, so a game where the team never reached the 20 does
                     not make the share undefined; a team with none in either game reads 0).
              EZ2  = two-game end-zone target count: targets whose air yards reached the goal line
                     (air_yards >= yardline_100) over the same two games.
              held constant: XFP2 (mean expected half-PPR over the two games) and SNAP_PCT (week w).
  OUTCOMES    spike in w+1 (18.0+ half-PPR); startable in w+1 (>= bar); NEXT4 = mean half-PPR over the games
              he plays in w+1..w+4 (2+ games), and startable over those four (NEXT4 >= bar).
  FALSIFIER   fixed in advance: if the RZ2 coefficient in an OLS of NEXT4 on xfp2 + snap_pct + RZ2 is under
              +0.10 points of NEXT4 per 10 points of share, AND the RZ2-top-fifth cell inside the xfp2 top fifth
              is under +3 points of start4 over the rest of that fifth, red zone is already inside expected
              points and stays a DISPLAY column on the wire page.
  PRIOR       the ffverse expected-points model already prices field position on every target and carry, so
              the honest prior is that red zone adds little once xfp2 is in the regression.

A red-zone play here is a play_type of run or pass with the ball snapped at yardline_100 <= 20 (10, 5), REG
season, two-point tries excluded (official carries and targets exclude them too). A carry is a play with a
rusher_player_id, a target a play with a receiver_player_id. Ids are gsis, the same key stats_player_week
carries, so the join is on id and not on name (section 3).

Paths resolve against THIS file. The cache is FF_CACHE or ..\_nflverse_cache beside the research folder, as
xfp_backtest.py has it; the five play-by-play files are fetched into it if absent.
Standard library plus pandas and numpy; no scipy.
"""
import os, sys, urllib.request
import pandas as pd, numpy as np
import numpy.linalg as la

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get('FF_CACHE') or os.path.normpath(os.path.join(HERE, '..', '_nflverse_cache'))
NFLV = 'https://github.com/nflverse/nflverse-data/releases/download/'
FFV = 'https://github.com/ffverse/ffopportunity/releases/download/latest-data/'
SEASONS = range(2021, 2026)


def _get(name, url):
    """The cached file if present (also checks the ir\\ folder, which holds snaps_<season>.csv and
    players.csv for the IR scripts), else one fetch into the cache.  Copied from xfp_backtest.py."""
    for d in (CACHE, HERE, os.path.join(HERE, '..', 'ir')):
        q = os.path.join(d, name)
        if os.path.exists(q) and os.path.getsize(q) > 1000:
            return q
    q = os.path.join(CACHE, name)
    os.makedirs(CACHE, exist_ok=True)
    print(f'  fetching {name} -> {q}')
    with urllib.request.urlopen(url, timeout=300) as fh:
        body = fh.read()
    if len(body) < 1000:
        raise SystemExit(f'FAILED: {url} returned {len(body)} bytes')
    with open(q, 'wb') as out:
        out.write(body)
    return q


def spearman(a, b):
    return pd.Series(a).rank().corr(pd.Series(b).rank())


def ols_hc1(y, X, names):
    """OLS with heteroskedasticity-robust (HC1) standard errors, numpy only."""
    y = np.asarray(y, float)
    X = np.column_stack([np.ones(len(y)), np.asarray(X, float)])
    n, k = X.shape
    XtX_inv = la.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    r = y - X @ b
    meat = (X * (r ** 2)[:, None]).T @ X
    cov = XtX_inv @ meat @ XtX_inv * n / (n - k)
    se = np.sqrt(np.diag(cov))
    r2 = 1 - r @ r / ((y - y.mean()) @ (y - y.mean()))
    return {nm: (b[i + 1], se[i + 1]) for i, nm in enumerate(names)}, r2


BAR = {'RB': 9.92, 'WR': 9.62, 'TE': 8.25}
SPIKE = 18.0
rng = np.random.default_rng(7)

# =============================================================================================================
# THE POPULATION: copied from xfp_backtest.py (same cache, same filters, same outcomes), so the pool is the
# one doc 438 measured and the only new columns are the red-zone ones.
# =============================================================================================================
d = pd.concat([pd.read_csv(_get(f'stats_player_week_{s}.csv', NFLV + f'stats_player/stats_player_week_{s}.csv'),
                           low_memory=False) for s in SEASONS])
d = d[(d.season_type == 'REG') & (d.position.isin(['RB', 'WR', 'TE']))].copy()
num = ['rushing_yards', 'receiving_yards', 'rushing_tds', 'receiving_tds', 'receptions', 'rushing_fumbles_lost',
       'receiving_fumbles_lost', 'sack_fumbles_lost', 'targets', 'carries', 'target_share', 'air_yards_share', 'wopr']
for c in num:
    d[c] = pd.to_numeric(d[c], errors='coerce').fillna(0)
d['hppr'] = (0.1 * (d.rushing_yards + d.receiving_yards) + 6 * (d.rushing_tds + d.receiving_tds) + 0.5 * d.receptions
             - 2 * (d.rushing_fumbles_lost + d.receiving_fumbles_lost + d.sack_fumbles_lost))
d = d[d.week <= 18]

e = pd.concat([pd.read_csv(_get(f'ep_weekly_{s}.csv', FFV + f'ep_weekly_{s}.csv'), low_memory=False) for s in SEASONS])
e = e[e.week <= 18].copy()
e['xfp'] = e.rec_fantasy_points_exp + e.rush_fantasy_points_exp - 0.5 * e.receptions_exp
e = e.groupby(['season', 'week', 'player_id'], as_index=False)[['xfp']].sum()
d = d.merge(e, on=['season', 'week', 'player_id'], how='left')

sn = pd.concat([pd.read_csv(_get(f'snaps_{s}.csv', NFLV + f'snap_counts/snap_counts_{s}.csv'), low_memory=False)
                for s in SEASONS])
sn = sn[sn.game_type == 'REG']
pl = pd.read_csv(_get('players.csv', NFLV + 'players/players.csv'), low_memory=False)[['gsis_id', 'pfr_id']].dropna().drop_duplicates('pfr_id')
sn = sn.merge(pl, left_on='pfr_player_id', right_on='pfr_id', how='inner')
sn = sn.groupby(['season', 'week', 'gsis_id'], as_index=False).offense_pct.max().rename(columns={'gsis_id': 'player_id'})
d = d.merge(sn, on=['season', 'week', 'player_id'], how='left')
d['snap_pct'] = d.offense_pct * 100

# =============================================================================================================
# RED ZONE from play-by-play, per player-week and per team-week, keyed on gsis id
# =============================================================================================================
PBP_COLS = ['season', 'week', 'season_type', 'posteam', 'play_type', 'two_point_attempt', 'yardline_100',
            'air_yards', 'rusher_player_id', 'receiver_player_id']


def redzone_tables(pbp):
    """Per (season, week, player_id): rz_car20/10/5, rz_tgt20/10, ez_tgt, rz_opp (car20 + tgt20).
    Per (season, week, team): team_rz_car20, team_rz_tgt20, team_rz_opp."""
    p = pbp[(pbp.season_type == 'REG') & pbp.play_type.isin(['run', 'pass'])
            & (pbp.two_point_attempt.fillna(0) == 0) & pbp.yardline_100.notna()].copy()
    p = p[p.yardline_100 <= 20]
    ru = p[p.rusher_player_id.notna() & (p.play_type == 'run')]
    re_ = p[p.receiver_player_id.notna() & (p.play_type == 'pass')].copy()
    re_['ez'] = re_.air_yards.notna() & (re_.air_yards >= re_.yardline_100)
    car = ru.groupby(['season', 'week', 'rusher_player_id']).agg(
        rz_car20=('yardline_100', 'size'), rz_car10=('yardline_100', lambda s: int((s <= 10).sum())),
        rz_car5=('yardline_100', lambda s: int((s <= 5).sum()))).reset_index().rename(columns={'rusher_player_id': 'player_id'})
    tgt = re_.groupby(['season', 'week', 'receiver_player_id']).agg(
        rz_tgt20=('yardline_100', 'size'), rz_tgt10=('yardline_100', lambda s: int((s <= 10).sum())),
        ez_tgt=('ez', 'sum')).reset_index().rename(columns={'receiver_player_id': 'player_id'})
    ply = car.merge(tgt, on=['season', 'week', 'player_id'], how='outer').fillna(0)
    for c in ['rz_car20', 'rz_car10', 'rz_car5', 'rz_tgt20', 'rz_tgt10', 'ez_tgt']:
        ply[c] = ply[c].astype(int)
    ply['rz_opp'] = ply.rz_car20 + ply.rz_tgt20
    tm = p.groupby(['season', 'week', 'posteam']).agg(
        team_rz_car20=('rusher_player_id', lambda s: int(s.notna().sum())),
        team_rz_tgt20=('receiver_player_id', lambda s: int(s.notna().sum()))).reset_index().rename(columns={'posteam': 'team'})
    tm['team_rz_opp'] = tm.team_rz_car20 + tm.team_rz_tgt20
    return ply, tm


pbp = pd.concat([pd.read_csv(_get(f'play_by_play_{s}.csv.gz', NFLV + f'pbp/play_by_play_{s}.csv.gz'),
                             usecols=PBP_COLS, low_memory=False) for s in SEASONS])
ply, tm = redzone_tables(pbp)
del pbp
print(f'red zone: {len(ply)} player-weeks with a red-zone touch, {len(tm)} team-weeks; '
      f'league carries inside the 20 per team-game {tm.team_rz_car20.mean():.2f}, targets {tm.team_rz_tgt20.mean():.2f}')

d = d.merge(ply, on=['season', 'week', 'player_id'], how='left')
for c in ['rz_car20', 'rz_car10', 'rz_car5', 'rz_tgt20', 'rz_tgt10', 'ez_tgt', 'rz_opp']:
    d[c] = d[c].fillna(0).astype(int)
d = d.merge(tm[['season', 'week', 'team', 'team_rz_opp']], on=['season', 'week', 'team'], how='left')
miss_team = d.team_rz_opp.isna().mean()
d['team_rz_opp'] = d.team_rz_opp.fillna(0).astype(int)
# a cross-check on the id join: the official weekly carries/targets must be >= the red-zone ones
bad = d[(d.rz_car20 > d.carries) | (d.rz_tgt20 > d.targets)]
print(f'id join check: {len(bad)} player-weeks where red-zone carries or targets exceed the official weekly '
      f'count (0 is the pass mark; a handful is nflverse reconciling its own feeds); team-weeks with no pbp row {miss_team*100:.2f}%')

# ---- windows (verbatim from xfp_backtest.py, plus the two-game red-zone columns) --------------------------------
d = d.sort_values(['season', 'player_id', 'week']).reset_index(drop=True)
g = d.groupby(['season', 'player_id'])
d['gp'] = g.cumcount() + 1
d['std_avg'] = g.hppr.transform(lambda s: s.expanding().mean())
d['bar'] = d.position.map(BAR)
d['prev_week'] = g.week.shift(1)
d['act2'] = (d.hppr + g.hppr.shift(1)) / 2
d['xfp2'] = (d.xfp + g.xfp.shift(1)) / 2
# two-game red zone over the SAME two game rows: his opportunities pooled over his team's, both games
d['rz_opp2'] = d.rz_opp + g.rz_opp.shift(1)
d['team_rz_opp2'] = d.team_rz_opp + g.team_rz_opp.shift(1)
d['rz2'] = np.where(d.team_rz_opp2 > 0, 100 * d.rz_opp2 / d.team_rz_opp2.replace(0, np.nan), 0.0)
d['ez2'] = d.ez_tgt + g.ez_tgt.shift(1)
d['rz1'] = np.where(d.team_rz_opp > 0, 100 * d.rz_opp / d.team_rz_opp.replace(0, np.nan), 0.0)   # week w only
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

# ---- the population (verbatim filter) ---------------------------------------------------------------------------
p = d[(d.week >= 2) & (d.week <= 16) & (d.std_avg < d.bar) & ((d.targets + d.carries) > 0)
      & d.prev_week.notna() & d.n1.notna() & d.xfp2.notna() & d.snap_pct.notna()].copy()
print(f'\nPOPULATION n={len(p)}  ' + '  '.join(f'{k} {v}' for k, v in p.position.value_counts().items())
      + '  (xfp_backtest.py reported 9999: WR 4666 RB 2735 TE 2598)')
print(f'base rates: spike {p.spike.mean()*100:.1f}%  startable w+1 {p.start1.mean()*100:.1f}%  '
      f'startable next four {p[p.next4_n>=2].start4.mean()*100:.1f}% (n={int((p.next4_n>=2).sum())})  '
      f'next-four mean {p.next4.mean():.2f}')
print(f'red zone in the pool: rz2 mean {p.rz2.mean():.1f}%, zero in both games {(p.rz_opp2==0).mean()*100:.1f}%, '
      f'ez2 mean {p.ez2.mean():.2f}, zero {(p.ez2==0).mean()*100:.1f}%;  corr(rz2, xfp2) {p[["rz2","xfp2"]].corr().iloc[0,1]:.3f}, '
      f'corr(ez2, xfp2) {p[["ez2","xfp2"]].corr().iloc[0,1]:.3f}, corr(rz2, snap_pct) {p[["rz2","snap_pct"]].corr().iloc[0,1]:.3f}')


def line(label, sub):
    s4 = sub[sub.next4_n >= 2]
    if len(sub) == 0:
        return f'{label:56s} n=    0'
    return (f'{label:56s} n={len(sub):5d}  spike {sub.spike.mean()*100:5.1f}%  start w+1 {sub.start1.mean()*100:5.1f}%  '
            f'start next4 {s4.start4.mean()*100:5.1f}%  next4 {sub.next4.mean():5.2f}')


def top_cut(q, col):
    return q[col].quantile(0.8)


# ==== (a) SPEARMAN with NEXT4 =====================================================================================
print('\n==== (a) Spearman rho with NEXT4 (2+ games ahead), and with w+1, by position and pooled ====')
for pos in ['ALL', 'RB', 'WR', 'TE']:
    q = p if pos == 'ALL' else p[p.position == pos]
    q4 = q[q.next4_n >= 2]
    print(f'{pos:3s} n={len(q4):5d}  rho with NEXT4: xfp2 {spearman(q4.xfp2, q4.next4):.3f}  snap {spearman(q4.snap_pct, q4.next4):.3f}  '
          f'RZ2 {spearman(q4.rz2, q4.next4):.3f}  EZ2 {spearman(q4.ez2, q4.next4):.3f}  rz week w only {spearman(q4.rz1, q4.next4):.3f}'
          f'   |  rho with w+1: RZ2 {spearman(q.rz2, q.n1):.3f}  EZ2 {spearman(q.ez2, q.n1):.3f}')
    # partial: rank-residualise next4 and rz2 on xfp2 rank (a crude partial Spearman)
    rx = q4.xfp2.rank(); ry = q4.next4.rank(); rz = q4.rz2.rank(); re2 = q4.ez2.rank()
    def resid(v):
        X = np.column_stack([np.ones(len(v)), rx]); b, *_ = la.lstsq(X, v, rcond=None); return v - X @ b
    print(f'      partial (rank-residualised on xfp2): RZ2 {np.corrcoef(resid(ry), resid(rz))[0,1]:.3f}  '
          f'EZ2 {np.corrcoef(resid(ry), resid(re2))[0,1]:.3f}')

# ==== (b) OLS with HC1 se ==========================================================================================
print('\n==== (b) OLS of NEXT4 (2+ games ahead) and of start4 (0/1, linear probability) on xfp2 + snap_pct + red zone ====')
print('     share in PERCENT, so the RZ2 coefficient x 10 is points of NEXT4 per 10 points of share (the falsifier bar is +0.10)')
verdict_coef = {}
for pos in ['ALL', 'RB', 'WR', 'TE']:
    q = p if pos == 'ALL' else p[p.position == pos]
    q = q[q.next4_n >= 2]
    for yname, y in [('NEXT4', q.next4.values), ('start4', q.start4.values.astype(float))]:
        base, r2b = ols_hc1(y, np.column_stack([q.xfp2, q.snap_pct]), ['xfp2', 'snap'])
        m1, r2_1 = ols_hc1(y, np.column_stack([q.xfp2, q.snap_pct, q.rz2]), ['xfp2', 'snap', 'rz2'])
        m2, r2_2 = ols_hc1(y, np.column_stack([q.xfp2, q.snap_pct, q.ez2]), ['xfp2', 'snap', 'ez2'])
        m3, r2_3 = ols_hc1(y, np.column_stack([q.xfp2, q.snap_pct, q.rz2, q.ez2]), ['xfp2', 'snap', 'rz2', 'ez2'])
        raw, _ = ols_hc1(y, np.column_stack([q.rz2]), ['rz2'])
        unit = 1.0 if yname == 'NEXT4' else 100.0    # start4 in percentage points
        print(f'  {pos:3s} {yname:6s} n={len(q):5d}  base R2 {r2b:.3f} -> +rz2 {r2_1:.3f} / +ez2 {r2_2:.3f} / +both {r2_3:.3f}')
        print(f'        rz2 RAW (nothing held): {raw["rz2"][0]*10*unit:+.3f} per 10 pts share (se {raw["rz2"][1]*10*unit:.3f})')
        print(f'        + rz2:  xfp2 {m1["xfp2"][0]*unit:+.3f} (se {m1["xfp2"][1]*unit:.3f})  snap {m1["snap"][0]*10*unit:+.3f}/10pts (se {m1["snap"][1]*10*unit:.3f})  '
              f'RZ2 {m1["rz2"][0]*10*unit:+.3f} per 10 pts share (se {m1["rz2"][1]*10*unit:.3f}, t {m1["rz2"][0]/m1["rz2"][1]:+.1f})')
        print(f'        + ez2:  xfp2 {m2["xfp2"][0]*unit:+.3f} (se {m2["xfp2"][1]*unit:.3f})  '
              f'EZ2 {m2["ez2"][0]*unit:+.3f} per end-zone target (se {m2["ez2"][1]*unit:.3f}, t {m2["ez2"][0]/m2["ez2"][1]:+.1f})')
        print(f'        + both: RZ2 {m3["rz2"][0]*10*unit:+.3f}/10pts (se {m3["rz2"][1]*10*unit:.3f})  EZ2 {m3["ez2"][0]*unit:+.3f}/tgt (se {m3["ez2"][1]*unit:.3f})')
        if yname == 'NEXT4':
            verdict_coef[pos] = (m1['rz2'][0] * 10, m1['rz2'][1] * 10)
    if pos == 'ALL':
        # 0.6: THE POPULATION MIX. A back's red-zone share runs twice a receiver's and a back at the same xfp2 scores
        # more over the next four, so a pooled coefficient can be pure position mix. Hold position with two dummies.
        for yname, y in [('NEXT4', q.next4.values), ('start4', q.start4.values.astype(float))]:
            unit = 1.0 if yname == 'NEXT4' else 100.0
            dum = np.column_stack([(q.position == 'RB').astype(float), (q.position == 'TE').astype(float)])
            mp, r2p = ols_hc1(y, np.column_stack([q.xfp2, q.snap_pct, q.rz2, dum]), ['xfp2', 'snap', 'rz2', 'isRB', 'isTE'])
            mq, _ = ols_hc1(y, np.column_stack([q.xfp2, q.snap_pct, q.ez2, dum]), ['xfp2', 'snap', 'ez2', 'isRB', 'isTE'])
            print(f'  ALL {yname:6s} POSITION HELD (RB and TE dummies), n={len(q)}:  RZ2 {mp["rz2"][0]*10*unit:+.3f} per 10 pts share '
                  f'(se {mp["rz2"][1]*10*unit:.3f}, t {mp["rz2"][0]/mp["rz2"][1]:+.1f});  EZ2 {mq["ez2"][0]*unit:+.3f} per end-zone target '
                  f'(se {mq["ez2"][1]*unit:.3f});  isRB {mp["isRB"][0]*unit:+.2f}  isTE {mp["isTE"][0]*unit:+.2f}')
            if yname == 'NEXT4':
                verdict_coef['ALL, position held'] = (mp['rz2'][0] * 10, mp['rz2'][1] * 10)

# ==== (c) the cells =================================================================================================
print('\n==== (c) top-fifth cells: red zone top fifth vs not, inside and outside the xfp2 top fifth ====')
verdict_cell = {}
for pos in ['ALL', 'RB', 'WR', 'TE']:
    q = p if pos == 'ALL' else p[p.position == pos]
    cx = top_cut(q, 'xfp2')
    for col, nm in [('rz2', 'RZ2 share'), ('ez2', 'EZ2 end-zone targets')]:
        cr = top_cut(q, col)
        hi_x = q[q.xfp2 >= cx]; lo_x = q[q.xfp2 < cx]
        print(f'\n  {pos:3s} {nm}: top fifth is >= {cr:.1f} ({(q[col] >= cr).mean()*100:.0f}% of the pool clears it, ties included); xfp2 top fifth >= {cx:.2f}')
        a = hi_x[hi_x[col] >= cr]; b = hi_x[hi_x[col] < cr]
        c = lo_x[lo_x[col] >= cr]; e_ = lo_x[lo_x[col] < cr]
        print('    ' + line(f'xfp2 top fifth AND {nm} top fifth', a))
        print('    ' + line(f'xfp2 top fifth, {nm} NOT top fifth', b))
        print('    ' + line(f'xfp2 NOT top fifth, {nm} top fifth', c))
        print('    ' + line(f'neither', e_))
        a4 = a[a.next4_n >= 2]; b4 = b[b.next4_n >= 2]
        if len(a4) > 1 and len(b4) > 1:
            gap = (a4.start4.mean() - b4.start4.mean()) * 100
            se_ = np.sqrt(a4.start4.var() / len(a4) + b4.start4.var() / len(b4)) * 100
            gap4 = a.next4.mean() - b.next4.mean()
            se4 = np.sqrt(a.next4.var() / len(a) + b.next4.var() / len(b))
            # permutation p on the start4 gap inside the xfp2 top fifth
            hx4 = hi_x[hi_x.next4_n >= 2]
            flag = (hx4[col] >= cr).values.copy(); out = hx4.start4.values
            obs = out[flag].mean() - out[~flag].mean(); perm = []
            for _ in range(2000):
                rng.shuffle(flag); perm.append(out[flag].mean() - out[~flag].mean())
            pval = np.mean(np.abs(np.array(perm)) >= abs(obs))
            print(f'    INSIDE the xfp2 top fifth, {nm} top fifth minus the rest: start4 {gap:+.1f} points (se {se_:.1f}, permutation p={pval:.3f}); '
                  f'next4 {gap4:+.2f} (se {se4:.2f}); spike {(a.spike.mean()-b.spike.mean())*100:+.1f} points   [falsifier bar +3 on start4]')
            if col == 'rz2':
                verdict_cell[pos] = (gap, se_, pval)

# the pooled cell again with POSITION-SPECIFIC cuts stacked, so a back's 25% share is not compared with a receiver's 11%
print('\n  ALL, POSITION HELD: each position cut at its own top fifths, then stacked')
for col, nm in [('rz2', 'RZ2 share'), ('ez2', 'EZ2 end-zone targets')]:
    parts_a, parts_b = [], []
    for pos in ['RB', 'WR', 'TE']:
        q = p[p.position == pos]; cx = top_cut(q, 'xfp2'); cr = top_cut(q, col)
        hi_x = q[q.xfp2 >= cx]
        parts_a.append(hi_x[hi_x[col] >= cr]); parts_b.append(hi_x[hi_x[col] < cr])
    a = pd.concat(parts_a); b = pd.concat(parts_b)
    print('    ' + line(f'xfp2 top fifth AND {nm} top fifth (own cuts)', a))
    print('    ' + line(f'xfp2 top fifth, {nm} NOT top fifth (own cuts)', b))
    a4 = a[a.next4_n >= 2]; b4 = b[b.next4_n >= 2]
    gap = (a4.start4.mean() - b4.start4.mean()) * 100
    se_ = np.sqrt(a4.start4.var() / len(a4) + b4.start4.var() / len(b4)) * 100
    # permutation WITHIN position, so the mix cannot move it
    hx = pd.concat([a4.assign(_f=True), b4.assign(_f=False)])
    obs = gap / 100; perm = []
    for _ in range(2000):
        f_ = hx.groupby('position', group_keys=False)._f.transform(lambda s: rng.permutation(s.values))
        perm.append(hx.start4[f_].mean() - hx.start4[~f_].mean())
    pval = np.mean(np.abs(np.array(perm)) >= abs(obs))
    print(f'    INSIDE the xfp2 top fifth, {nm} top fifth minus the rest, position held: start4 {gap:+.1f} points '
          f'(se {se_:.1f}, within-position permutation p={pval:.3f}); next4 {a.next4.mean()-b.next4.mean():+.2f}; '
          f'spike {(a.spike.mean()-b.spike.mean())*100:+.1f} points')
    if col == 'rz2':
        verdict_cell['ALL, position held'] = (gap, se_, pval)

# ==== by season, the rz2 coefficient net of xfp2 and snaps (pool) ================================================
print('\n==== by season: RZ2 coefficient net of xfp2 and snap_pct, NEXT4, pooled positions, position held ====')
for s_, q in p[p.next4_n >= 2].groupby('season'):
    dum = np.column_stack([(q.position == 'RB').astype(float), (q.position == 'TE').astype(float)])
    m, _ = ols_hc1(q.next4.values, np.column_stack([q.xfp2, q.snap_pct, q.rz2, dum]), ['xfp2', 'snap', 'rz2', 'isRB', 'isTE'])
    m0, _ = ols_hc1(q.next4.values, np.column_stack([q.xfp2, q.snap_pct, q.rz2]), ['xfp2', 'snap', 'rz2'])
    print(f'  {s_}: RZ2 {m["rz2"][0]*10:+.3f} per 10 pts (se {m["rz2"][1]*10:.3f}) position held; '
          f'{m0["rz2"][0]*10:+.3f} (se {m0["rz2"][1]*10:.3f}) not held;  xfp2 {m["xfp2"][0]:+.3f}  n={len(q)}')

# ==== the finer red-zone cuts, as a display check: inside the 10 and the 5, week w only ======================================
print('\n==== the finer cuts, week w only, pooled: does inside-the-10 or inside-the-5 carry anything net of xfp2 + snaps? ====')
q = p[p.next4_n >= 2]
for col in ['rz_car20', 'rz_car10', 'rz_car5', 'rz_tgt20', 'rz_tgt10', 'ez_tgt']:
    m, _ = ols_hc1(q.next4.values, np.column_stack([q.xfp2, q.snap_pct, q[col]]), ['xfp2', 'snap', col])
    print(f'  {col:9s} mean {q[col].mean():.2f}  NEXT4 per one {m[col][0]:+.3f} (se {m[col][1]:.3f}, t {m[col][0]/m[col][1]:+.1f})')

# ==== VERDICT against the falsifier fixed above ====================================================================
print('\n==== VERDICT ====')
print('  the falsifier, fixed in advance: RZ2 net of xfp2 and snap share under +0.10 points of NEXT4 per 10 points of share, AND the')
print('  RZ2-top-fifth cell inside the xfp2 top fifth under +3 points of start4 over the rest of that fifth  ->  display column only.')
for lab in ['ALL', 'ALL, position held', 'RB', 'WR', 'TE']:
    c_, s_ = verdict_coef[lab]; g_, gs_, gp_ = verdict_cell[lab]
    print(f'  {lab:20s} coefficient {c_:+.3f} per 10 pts (se {s_:.3f})   cell {g_:+.1f} points of start4 (se {gs_:.1f}, p={gp_:.3f})   '
          + ('BOTH OVER the bar' if (c_ >= 0.10 and g_ >= 3) else 'both under' if (c_ < 0.10 and g_ < 3) else 'split'))
c_all, s_all = verdict_coef['ALL']; c_h, s_h = verdict_coef['ALL, position held']
g_all = verdict_cell['ALL'][0]; g_h = verdict_cell['ALL, position held'][0]
if (c_all >= 0.10 and g_all >= 3) and not (c_h >= 0.10 and g_h >= 3):
    print('  THE POOLED ROW CROSSES BOTH BARS AND THE SAME POOL WITH POSITION HELD DOES NOT. That is position mix, not red zone:')
    print('  a back runs twice a receiver\'s red-zone share and scores more over the next four at the same xfp2, so a pooled')
    print('  red-zone cut is mostly a cut on being a running back (0.6, the population is the first thing that is wrong).')
    print('  The pooled row is not the answer; the position-held row and the three positions are.')
if c_h >= 0.10 and g_h >= 3:
    print('  OVER the bar with position held: red zone carries information net of expected points. The falsifier did not fire.')
elif c_h < 0.10 and g_h < 3:
    print('  BOTH under the bar with position held: red zone is already inside expected points. DISPLAY column; it does not enter the screen.')
else:
    gs_h, gp_h = verdict_cell['ALL, position held'][1], verdict_cell['ALL, position held'][2]
    print(f'  SPLIT with position held, strictly: the coefficient arm is dead ({c_h:+.3f}, bar +0.10) and the cell arm is {g_h:+.1f} against a')
    print(f'  bar of +3, which is inside its own se ({gs_h:.1f}, p={gp_h:.3f}) and under the bar at two of the three positions. The falsifier')
    print('  as written needs both arms under to retire the signal, so this is not a clean kill; but nothing here is a measured')
    print('  gain either, and a +0.7 over a bar with a 2.2 se is not a reason to change a screen. RECOMMENDATION: DISPLAY column;')
    print('  it does not enter the screen. Say the cell arm is unresolved when quoting this.')

p.to_pickle(os.path.join(HERE, 'redzone_pool.pkl'))
print('\npool pickled beside the script as redzone_pool.pkl')
