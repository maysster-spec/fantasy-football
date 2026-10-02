"""routes_vs_snaps.py -- does ROUTE PARTICIPATION add anything to SNAP SHARE at predicting a claimable
receiver's next four weeks? (doc 437 section 6 item 5: routes run is the one published waiver signal with no free
LIVE source; test on history before anyone pays for it.)

TESTABLE FORM, stated before the run (0.5(a2)):
  POPULATION  WR and TE player-weeks, REG 2023-2025, weeks 2-16, NOT startable in week w on 4.13b's bar
              (season-to-date half-PPR average through w below WR 9.62 / TE 8.25), at least one target in w,
              a game row in w-1 (so a two-game mean exists), played in w+1, and a snap-share row and a
              participation row in w.
  PREDICTORS  measured in week w: SNAP = offensive snap share (nflverse snap counts, offense_pct);
              ROUTE = route participation = dropbacks on which he was on the field / team dropbacks
              (nflverse pbp_participation offense_players joined to play-by-play qb_dropback == 1; an
              APPROXIMATION of routes run, because a man on the field for a dropback who stays in to block is
              counted as if he ran a route); ROUTE2 = the two-game mean of ROUTE; TGT = targets in w;
              TPRR = targets per route run = targets / routes (the published metric), and its two-game form.
  OUTCOMES    spike in w+1 (18.0+ half-PPR); startable in w+1 (>= bar); NEXT4 = mean half-PPR over the games he
              plays in w+1..w+4 (2+ games), and startable over those four (NEXT4 >= bar).
  TESTS       (a) Spearman (rank then Pearson) of each predictor with NEXT4; (b) OLS of NEXT4 and of start4 on
              SNAP and ROUTE together (both in percentage points), HC1 robust se, then with targets and TPRR
              added; (c) top-fifth cells: snap top fifth, route top fifth, both, route-only, snap-only, on
              spike / start1 / start4 / next4 with n.
  FALSIFIER   fixed in advance: if the ROUTE coefficient net of SNAP is under +0.05 points of NEXT4 per
              percentage point of participation AND the route-only cell is under +3 points of start4 over the
              snap-only cell, routes add nothing worth buying.
"""
import os, sys, urllib.request
import numpy as np, pandas as pd
import numpy.linalg as la

# Paths resolve against THIS file (0.4). Play-by-play is the b1_dst cache (symlinked here, not re-downloaded);
# weekly stats, snap counts and players.csv are the research cache; the three participation files were fetched
# into this folder once and are re-fetched only if absent.
HERE = os.path.dirname(os.path.abspath(__file__))
# On the drive: Scripts\research\wk1\routes_vs_snaps.py; the research cache is ..\_nflverse_cache and holds the
# play-by-play, weekly stats, snaps and players files (fetched once if absent).
CACHE = os.environ.get('FF_CACHE') or os.path.normpath(os.path.join(HERE, '..', '_nflverse_cache'))
PBP_DIR = CACHE
NFLV = 'https://github.com/nflverse/nflverse-data/releases/download/'
SEASONS = [2023, 2024, 2025]
BAR = {'WR': 9.62, 'TE': 8.25}
SPIKE = 18.0

OUT = open(os.path.join(HERE, 'run_routes_vs_snaps.txt'), 'w', encoding='utf-8')
def say(*a):
    s = ' '.join(str(x) for x in a)
    print(s); OUT.write(s + '\n')

def _fetch(name, url):
    q = os.path.join(HERE, name)
    if os.path.exists(q) and os.path.getsize(q) > 1000:
        return q
    say(f'  fetching {name} from {url}')
    try:
        with urllib.request.urlopen(url, timeout=300) as fh:
            body = fh.read()
    except Exception as ex:
        say(f'  BLOCKED: {url} -> {ex}')
        return None
    if len(body) < 1000:
        say(f'  BLOCKED: {url} returned {len(body)} bytes')
        return None
    with open(q, 'wb') as out:
        out.write(body)
    return q

def spearman(a, b):
    return pd.Series(np.asarray(a, float)).rank().corr(pd.Series(np.asarray(b, float)).rank())

def ols_hc1(y, X, names):
    """OLS with HC1 (heteroskedasticity-robust) standard errors. Returns list of (name, b, se)."""
    y = np.asarray(y, float); X = np.column_stack([np.ones(len(y))] + [np.asarray(x, float) for x in X])
    n, k = X.shape
    XtX_inv = la.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    e = y - X @ b
    meat = (X * (e ** 2)[:, None]).T @ X
    cov = XtX_inv @ meat @ XtX_inv * n / (n - k)
    se = np.sqrt(np.diag(cov))
    return [(nm, b[i], se[i]) for i, nm in enumerate(['const'] + names)]

say(__doc__.strip())
say('')

# ---- 1. participation: routes (dropbacks on the field) per player-week, team dropbacks per team-week -----------
say('==== PARTICIPATION COVERAGE ====')
routes_rows, team_db_rows, coverage = [], [], []
for s in SEASONS:
    url = NFLV + f'pbp_participation/pbp_participation_{s}.csv'
    pf = _fetch(f'pbp_participation_{s}.csv', url)
    if pf is None:
        say(f'  {s}: BLOCKED (tried {url}); season skipped')
        continue
    part = pd.read_csv(pf, usecols=['nflverse_game_id', 'play_id', 'possession_team', 'offense_players'],
                       low_memory=False)
    part['week'] = part.nflverse_game_id.str.split('_').str[1].astype(int)
    pbp_path = os.path.join(PBP_DIR, f'play_by_play_{s}.csv.gz')
    if not os.path.exists(pbp_path):
        pbp_path = os.path.join(HERE, f'play_by_play_{s}.csv.gz')
    pbp = pd.read_csv(pbp_path, usecols=['game_id', 'play_id', 'week', 'season_type', 'posteam', 'qb_dropback',
                                          'pass_attempt', 'qb_spike', 'qb_kneel'], low_memory=False)
    reg = pbp[pbp.season_type == 'REG']
    db = reg[(reg.qb_dropback == 1) & (reg.qb_spike != 1) & (reg.qb_kneel != 1)]
    passes = reg[reg.pass_attempt == 1]
    pj = part.drop(columns=['week'])
    m = db.merge(pj, left_on=['game_id', 'play_id'], right_on=['nflverse_game_id', 'play_id'], how='left')
    mp = passes.merge(pj, left_on=['game_id', 'play_id'], right_on=['nflverse_game_id', 'play_id'], how='left')
    has = m.offense_players.notna() & (m.offense_players.astype(str).str.len() > 5)
    hasp = mp.offense_players.notna() & (mp.offense_players.astype(str).str.len() > 5)
    wk = sorted(part[part.week <= 18].week.unique())
    coverage.append(dict(season=s, plays=len(part), games=part.nflverse_game_id.nunique(),
                         weeks=f'{min(wk)}-{max(wk)}' + (' plus playoffs' if part.week.max() > 18 else ''),
                         reg_dropbacks=len(db), db_with_list=has.mean(), pass_with_list=hasp.mean(),
                         team_match=(m.posteam == m.possession_team).mean()))
    say(f'  {s}: {len(part)} plays, {part.nflverse_game_id.nunique()} games, weeks {min(wk)}-{max(wk)}'
        f'{" plus playoffs" if part.week.max() > 18 else ""}; REG dropbacks {len(db)}, '
        f'{has.mean()*100:.1f}% carry an offense_players list; pass attempts {len(passes)}, '
        f'{hasp.mean()*100:.1f}% carry one; posteam == possession_team on {(m.posteam == m.possession_team).mean()*100:.1f}%')
    m = m[has].copy()
    m['season'] = s
    tdb = m.groupby(['season', 'week', 'posteam'], as_index=False).size().rename(columns={'size': 'team_db'})
    team_db_rows.append(tdb)
    ex = m[['season', 'week', 'posteam', 'offense_players']].copy()
    ex['offense_players'] = ex.offense_players.str.split(';')
    ex = ex.explode('offense_players').rename(columns={'offense_players': 'player_id'})
    ex = ex[ex.player_id.astype(str).str.startswith('00-')]
    r = ex.groupby(['season', 'week', 'player_id', 'posteam'], as_index=False).size().rename(columns={'size': 'routes'})
    # a man traded mid-week is at most on one team per game week; keep the team he had the most dropbacks with
    r = r.sort_values('routes', ascending=False).drop_duplicates(['season', 'week', 'player_id'])
    routes_rows.append(r)
    del part, pbp, m, ex
if not routes_rows:
    say('BLOCKED: no participation file for any season; nothing to test.'); OUT.close(); sys.exit(1)
routes = pd.concat(routes_rows).merge(pd.concat(team_db_rows), on=['season', 'week', 'posteam'], how='left')
routes['route_part'] = routes.routes / routes.team_db * 100
have = sorted(int(x) for x in routes.season.unique())
say(f'  seasons in the test: {have}; file dates (GitHub Last-Modified): 2023 and 2024 4 Sep 2025, 2025 10 Feb 2026')
say(f'  team dropbacks per team-game: mean {routes.drop_duplicates(["season","week","posteam"]).team_db.mean():.1f}')

# ---- 2. actuals, this league's half-PPR, from the nflverse weekly file -------------------------------------------
d = pd.concat([pd.read_csv(os.path.join(CACHE, f'stats_player_week_{s}.csv'), low_memory=False) for s in have])
d = d[(d.season_type == 'REG') & (d.position.isin(['WR', 'TE']))].copy()
num = ['rushing_yards', 'receiving_yards', 'rushing_tds', 'receiving_tds', 'receptions', 'rushing_fumbles_lost',
       'receiving_fumbles_lost', 'sack_fumbles_lost', 'targets', 'carries', 'target_share', 'air_yards_share', 'wopr']
for c in num:
    d[c] = pd.to_numeric(d[c], errors='coerce').fillna(0)
d['hppr'] = (0.1 * (d.rushing_yards + d.receiving_yards) + 6 * (d.rushing_tds + d.receiving_tds) + 0.5 * d.receptions
             - 2 * (d.rushing_fumbles_lost + d.receiving_fumbles_lost + d.sack_fumbles_lost))
d = d[d.week <= 18]

# ---- 3. snap share, keyed on gsis via players.csv ----------------------------------------------------------------
sn = pd.concat([pd.read_csv(os.path.join(CACHE, f'snaps_{s}.csv'), low_memory=False) for s in have])
sn = sn[sn.game_type == 'REG']
pl = pd.read_csv(os.path.join(CACHE, 'players.csv'), low_memory=False)[['gsis_id', 'pfr_id']].dropna().drop_duplicates('pfr_id')
sn = sn.merge(pl, left_on='pfr_player_id', right_on='pfr_id', how='inner')
sn = sn.groupby(['season', 'week', 'gsis_id'], as_index=False).offense_pct.max().rename(columns={'gsis_id': 'player_id'})
d = d.merge(sn, on=['season', 'week', 'player_id'], how='left')
d['snap_pct'] = d.offense_pct * 100

# ---- 4. routes onto the weekly rows ---------------------------------------------------------------------------------
d = d.merge(routes[['season', 'week', 'player_id', 'routes', 'team_db', 'route_part']], on=['season', 'week', 'player_id'], how='left')
tw = d[d.targets > 0]
say(f'\njoin: {tw.route_part.notna().mean()*100:.1f}% of {len(tw)} WR/TE target-weeks carry a participation row, '
    f'{tw.snap_pct.notna().mean()*100:.1f}% a snap-share row')
# routes are counted from being on the field, so targets > routes should be impossible; count violations
bad = tw[tw.targets > tw.routes]
say(f'targets > routes on {len(bad)} of {tw.routes.notna().sum()} joined target-weeks (a participation gap, dropped from TPRR)')
d.loc[d.targets > d.routes, ['routes', 'route_part']] = np.nan
d['tprr'] = np.where(d.routes > 0, d.targets / d.routes * 100, np.nan)

# ---- 5. windows ----------------------------------------------------------------------------------------------------
d = d.sort_values(['season', 'player_id', 'week']).reset_index(drop=True)
g = d.groupby(['season', 'player_id'])
d['std_avg'] = g.hppr.transform(lambda s: s.expanding().mean())
d['bar'] = d.position.map(BAR)
d['prev_week'] = g.week.shift(1)
d['route_part2'] = (d.route_part + g.route_part.shift(1)) / 2
d['snap_pct2'] = (d.snap_pct + g.snap_pct.shift(1)) / 2
d['routes2'] = d.routes + g.routes.shift(1)
d['targets2'] = d.targets + g.targets.shift(1)
d['tprr2'] = np.where(d.routes2 > 0, d.targets2 / d.routes2 * 100, np.nan)
d['act2'] = (d.hppr + g.hppr.shift(1)) / 2
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

# ---- 6. the population ------------------------------------------------------------------------------------------------
p = d[(d.week >= 2) & (d.week <= 16) & (d.std_avg < d.bar) & (d.targets >= 1)
      & d.prev_week.notna() & d.n1.notna() & d.snap_pct.notna() & d.route_part.notna() & d.route_part2.notna()].copy()
p4 = p[p.next4_n >= 2]
say(f'\nPOPULATION n={len(p)}  ' + '  '.join(f'{k} {v}' for k, v in p.position.value_counts().items())
    + '  by season ' + '  '.join(f'{k} {v}' for k, v in p.season.value_counts().sort_index().items()))
say(f'base rates: spike {p.spike.mean()*100:.1f}%  startable w+1 {p.start1.mean()*100:.1f}%  '
    f'startable next four {p4.start4.mean()*100:.1f}% (n={len(p4)})  next-four mean {p.next4.mean():.2f}')
say(f'predictors in the pool: snap {p.snap_pct.mean():.1f}% (sd {p.snap_pct.std():.1f}), route part {p.route_part.mean():.1f}% '
    f'(sd {p.route_part.std():.1f}), targets {p.targets.mean():.2f}, TPRR {p.tprr.mean():.1f}%')
for pos in ['WR', 'TE']:
    q = p[p.position == pos]
    say(f'  {pos}: snap {q.snap_pct.mean():.1f}%  route part {q.route_part.mean():.1f}%  corr(snap, route) {q[["snap_pct","route_part"]].corr().iloc[0,1]:.3f}  '
        f'route part minus snap: mean {(q.route_part - q.snap_pct).mean():+.1f}, sd {(q.route_part - q.snap_pct).std():.1f}')
say(f'  ALL: corr(snap, route) {p[["snap_pct","route_part"]].corr().iloc[0,1]:.3f}; corr(route, targets) {p[["route_part","targets"]].corr().iloc[0,1]:.3f}; '
    f'corr(snap, targets) {p[["snap_pct","targets"]].corr().iloc[0,1]:.3f}')

def line(label, sub):
    s4 = sub[sub.next4_n >= 2]
    if len(sub) == 0:
        return f'{label:46s} n=    0'
    return (f'{label:46s} n={len(sub):5d}  spike {sub.spike.mean()*100:5.1f}%  start w+1 {sub.start1.mean()*100:5.1f}%  '
            f'start next4 {s4.start4.mean()*100:5.1f}% (n={len(s4)})  next4 {sub.next4.mean():5.2f}')

# ==== TEST (a): Spearman with NEXT4 ====================================================================================
say('\n==== TEST (a): Spearman rho with NEXT4 (2+ games ahead), whole WR/TE pool and by position ====')
preds = [('snap_pct', 'snap share'), ('snap_pct2', 'snap share, 2-game'), ('route_part', 'route part'),
         ('route_part2', 'route part, 2-game'), ('targets', 'targets'), ('targets2', 'targets, 2-game'),
         ('target_share', 'target share'), ('tprr', 'TPRR'), ('tprr2', 'TPRR, 2-game'), ('wopr', 'WOPR'), ('act2', 'act2')]
say(f'{"":22s}' + ''.join(f'{pos:>14s}' for pos in ['ALL', 'WR', 'TE']))
for col, nm in preds:
    row = f'{nm:22s}'
    for pos in ['ALL', 'WR', 'TE']:
        q = p4 if pos == 'ALL' else p4[p4.position == pos]
        q = q[q[col].notna()]
        row += f'{spearman(q[col], q.next4):8.3f} n={len(q):4d}'
    say(row)
say('by season, rho with NEXT4:')
for s_, q in p4.groupby('season'):
    say(f'  {s_}: snap {spearman(q.snap_pct, q.next4):.3f}  route {spearman(q.route_part, q.next4):.3f}  '
        f'route2 {spearman(q.route_part2, q.next4):.3f}  targets {spearman(q.targets, q.next4):.3f}  '
        f'tprr {spearman(q[q.tprr.notna()].tprr, q[q.tprr.notna()].next4):.3f}  n={len(q)}')
say('partial: rho of NEXT4 with route part AFTER residualising both on snap share (Spearman of OLS residuals):')
for pos in ['ALL', 'WR', 'TE']:
    q = p4 if pos == 'ALL' else p4[p4.position == pos]
    def resid(y, x):
        X = np.column_stack([np.ones(len(x)), x]); b, *_ = la.lstsq(X, y, rcond=None); return y - X @ b
    ry = resid(q.next4.values, q.snap_pct.values); rr = resid(q.route_part.values, q.snap_pct.values)
    rr2 = resid(q.route_part2.values, q.snap_pct.values)
    say(f'  {pos:3s} n={len(q):5d}  route|snap {spearman(rr, ry):+.3f}   route2|snap {spearman(rr2, ry):+.3f}')

# ==== TEST (b): OLS with HC1 robust se ==================================================================================
say('\n==== TEST (b): OLS of NEXT4 and of start4 on snap share and route participation together (percentage points, HC1 se) ====')
def report(label, y, X, names, q):
    res = ols_hc1(y, X, names)
    say(f'  {label:44s} n={len(q):5d}  ' + '  '.join(f'{nm} {b:+.4f} (se {s:.4f})' for nm, b, s in res[1:]))
for pos in ['ALL', 'WR', 'TE']:
    q = p4 if pos == 'ALL' else p4[p4.position == pos]
    say(f'-- {pos}')
    report('NEXT4 ~ snap', q.next4, [q.snap_pct], ['snap'], q)
    report('NEXT4 ~ route', q.next4, [q.route_part], ['route'], q)
    report('NEXT4 ~ snap + route', q.next4, [q.snap_pct, q.route_part], ['snap', 'route'], q)
    report('NEXT4 ~ snap + route2', q.next4, [q.snap_pct, q.route_part2], ['snap', 'route2'], q)
    report('NEXT4 ~ snap + route + targets', q.next4, [q.snap_pct, q.route_part, q.targets], ['snap', 'route', 'tgt'], q)
    qt = q[q.tprr.notna()]
    report('NEXT4 ~ snap + route + tprr', qt.next4, [qt.snap_pct, qt.route_part, qt.tprr], ['snap', 'route', 'tprr'], qt)
    report('NEXT4 ~ snap + route + targets + tprr', qt.next4, [qt.snap_pct, qt.route_part, qt.targets, qt.tprr], ['snap', 'route', 'tgt', 'tprr'], qt)
    report('start4 (x100) ~ snap + route', q.start4.astype(float) * 100, [q.snap_pct, q.route_part], ['snap', 'route'], q)
    report('start4 (x100) ~ snap + route + targets', q.start4.astype(float) * 100, [q.snap_pct, q.route_part, q.targets], ['snap', 'route', 'tgt'], q)
    if pos == 'ALL':
        te = (q.position == 'TE').astype(float)
        report('NEXT4 ~ snap + route + TE dummy', q.next4, [q.snap_pct, q.route_part, te], ['snap', 'route', 'TE'], q)
        report('NEXT4 ~ snap + route + targets + TE dummy', q.next4, [q.snap_pct, q.route_part, q.targets, te], ['snap', 'route', 'tgt', 'TE'], q)

# ==== TEST (c): top-fifth cells ==========================================================================================
say('\n==== TEST (c): top-fifth cells (fifths cut inside the pool named on the row) ====')
for pos in ['ALL', 'WR', 'TE']:
    q = p if pos == 'ALL' else p[p.position == pos]
    cs, cr = q.snap_pct.quantile(.8), q.route_part.quantile(.8)
    S, R = q.snap_pct >= cs, q.route_part >= cr
    say(f'-- {pos}: snap top fifth = {cs:.1f}%+, route part top fifth = {cr:.1f}%+')
    say('  ' + line('the pool', q))
    say('  ' + line('snap top fifth', q[S]))
    say('  ' + line('route top fifth', q[R]))
    say('  ' + line('both top fifth', q[S & R]))
    say('  ' + line('route-only (route top, snap not)', q[R & ~S]))
    say('  ' + line('snap-only (snap top, route not)', q[S & ~R]))
    say('  ' + line('neither', q[~S & ~R]))
    a, b = q[R & ~S], q[S & ~R]
    a4, b4 = a[a.next4_n >= 2], b[b.next4_n >= 2]
    if len(a4) and len(b4):
        gain = (a4.start4.mean() - b4.start4.mean()) * 100
        se_ = np.sqrt(a4.start4.var() / len(a4) + b4.start4.var() / len(b4)) * 100
        say(f'  route-only minus snap-only, start next4: {gain:+.1f} points (se {se_:.1f}); next4 {a.next4.mean() - b.next4.mean():+.2f}')
    # the two-game version and TPRR the same way
    cr2, ct = q.route_part2.quantile(.8), q[q.tprr.notna()].tprr.quantile(.8)
    R2, T = q.route_part2 >= cr2, q.tprr >= ct
    say(f'  two-game route part top fifth = {cr2:.1f}%+; TPRR top fifth = {ct:.1f}%+')
    say('  ' + line('route2 top fifth', q[R2]))
    say('  ' + line('route2-only (route2 top, snap not)', q[R2 & ~S]))
    say('  ' + line('TPRR top fifth', q[T]))
    say('  ' + line('TPRR top fifth AND route top fifth', q[T & R]))
    say('  ' + line('TPRR top fifth, route NOT top fifth', q[T & ~R]))
    say('  ' + line('targets top fifth', q[q.targets >= q.targets.quantile(.8)]))
    say('  ' + line('targets top fifth AND route top fifth', q[(q.targets >= q.targets.quantile(.8)) & R]))
    say('  ' + line('targets top fifth, route NOT top fifth', q[(q.targets >= q.targets.quantile(.8)) & ~R]))
    say('  ' + line('route top fifth, targets NOT top fifth', q[(q.targets < q.targets.quantile(.8)) & R]))

# ==== inside the snap top fifth, does route participation split anything? =================================================
say('\n==== inside a snap band, route participation fifths (does route split the men snap share already picked?) ====')
for pos in ['WR', 'TE']:
    q = p[p.position == pos].copy()
    q['snap_band'] = pd.cut(q.snap_pct, [0, 40, 60, 80, 101], labels=['<40', '40-60', '60-80', '80+'], right=False)
    for band, qq in q.groupby('snap_band', observed=True):
        if len(qq) < 60:
            continue
        med = qq.route_part.median()
        hi, lo = qq[qq.route_part >= med], qq[qq.route_part < med]
        hi4, lo4 = hi[hi.next4_n >= 2], lo[lo.next4_n >= 2]
        say(f'  {pos} snap {band:5s} n={len(qq):4d}: route above median ({med:.0f}%) start4 {hi4.start4.mean()*100:5.1f}% (n={len(hi4)}) next4 {hi.next4.mean():5.2f}  '
            f'| below: start4 {lo4.start4.mean()*100:5.1f}% (n={len(lo4)}) next4 {lo.next4.mean():5.2f}  | diff start4 {(hi4.start4.mean()-lo4.start4.mean())*100:+.1f}'
            f'  | snap inside the band: above {hi.snap_pct.mean():.1f}% vs below {lo.snap_pct.mean():.1f}%')
say('  the same split on the TILT (route part minus snap share, so snap share cannot leak through the split):')
for pos in ['WR', 'TE']:
    q = p[p.position == pos].copy()
    q['tilt'] = q.route_part - q.snap_pct
    q['snap_band'] = pd.cut(q.snap_pct, [0, 40, 60, 80, 101], labels=['<40', '40-60', '60-80', '80+'], right=False)
    for band, qq in q.groupby('snap_band', observed=True):
        if len(qq) < 60:
            continue
        med = qq.tilt.median()
        hi, lo = qq[qq.tilt >= med], qq[qq.tilt < med]
        hi4, lo4 = hi[hi.next4_n >= 2], lo[lo.next4_n >= 2]
        say(f'  {pos} snap {band:5s} n={len(qq):4d}: tilt above median ({med:+.0f}) start4 {hi4.start4.mean()*100:5.1f}% (n={len(hi4)}) next4 {hi.next4.mean():5.2f}  '
            f'| below: start4 {lo4.start4.mean()*100:5.1f}% (n={len(lo4)}) next4 {lo.next4.mean():5.2f}  | diff start4 {(hi4.start4.mean()-lo4.start4.mean())*100:+.1f}'
            f'  | snap: above {hi.snap_pct.mean():.1f}% vs below {lo.snap_pct.mean():.1f}%')
say('  the disagreement cells by season (ALL, fifths cut on the whole pool):')
cs, cr = p.snap_pct.quantile(.8), p.route_part.quantile(.8)
for s_, q in p.groupby('season'):
    S, R = q.snap_pct >= cs, q.route_part >= cr
    a, b = q[R & ~S], q[S & ~R]; a4, b4 = a[a.next4_n >= 2], b[b.next4_n >= 2]
    say(f'  {s_}: route-only start4 {a4.start4.mean()*100:5.1f}% (n={len(a4)}) next4 {a.next4.mean():5.2f}  |  snap-only start4 {b4.start4.mean()*100:5.1f}% (n={len(b4)}) next4 {b.next4.mean():5.2f}')

# ==== the wire's three-signal screen with route participation as a candidate fourth signal ==================================
say('\n==== the three-signal screen (targets 8+, snaps 80%+, target share 20%+) and route part 80%+ as a fourth ====')
p['s_tgt'] = p.targets >= 8; p['s_snap'] = p.snap_pct >= 80; p['s_share'] = p.target_share * 100 >= 20
p['sig3'] = p[['s_tgt', 's_snap', 's_share']].sum(axis=1)
p['s_route'] = p.route_part >= 80
for k in range(4):
    say('  ' + line(f'{k} of 3 signals', p[p.sig3 == k]))
a = p[p.sig3 >= 2]; b_ = p[(p.sig3 >= 2) & p.s_route]; c_ = p[(p.sig3 >= 2) & ~p.s_route]
say('  ' + line('2+ of 3 (the operative bar)', a))
say('  ' + line('2+ of 3 AND route part 80%+', b_))
say('  ' + line('2+ of 3 and route part under 80%', c_))
say('  ' + line('route part 80%+ alone, fewer than 2 of 3', p[(p.sig3 < 2) & p.s_route]))
a4, b4 = a[a.next4_n >= 2], b_[b_.next4_n >= 2]
say(f'  GAIN from the fourth signal on the 2+ bar: spike {(b_.spike.mean()-a.spike.mean())*100:+.1f} points, '
    f'start next4 {(b4.start4.mean()-a4.start4.mean())*100:+.1f} points (n {len(b4)} vs {len(a4)})')
say('  swap: route part 80%+ in place of snaps 80%+ inside the three-signal count')
p['sig3r'] = p[['s_tgt', 's_route', 's_share']].sum(axis=1)
for k in range(4):
    say('  ' + line(f'{k} of 3 (route in place of snap)', p[p.sig3r == k]))
say('  ' + line('2+ of 3 (route in place of snap)', p[p.sig3r >= 2]))

# ==== VERDICT against the falsifier ============================================================================================
say('\n==== VERDICT against the falsifier fixed in advance ====')
res = ols_hc1(p4.next4.values, [p4.snap_pct.values, p4.route_part.values], ['snap', 'route'])
b_route, se_route = res[2][1], res[2][2]
q = p; cs, cr = q.snap_pct.quantile(.8), q.route_part.quantile(.8)
S, R = q.snap_pct >= cs, q.route_part >= cr
a, b = q[R & ~S], q[S & ~R]; a4, b4 = a[a.next4_n >= 2], b[b.next4_n >= 2]
cell = (a4.start4.mean() - b4.start4.mean()) * 100
say(f'  route coefficient net of snap share (ALL, NEXT4 per percentage point): {b_route:+.4f} (se {se_route:.4f}); bar +0.05')
say(f'  route-only cell minus snap-only cell, start next4: {cell:+.1f} points (n {len(a4)} vs {len(b4)}); bar +3')
both_fail = (b_route < 0.05) and (cell < 3)
say('  ' + ('FALSIFIED: routes add nothing worth buying net of snap share.' if both_fail else
            'NOT FALSIFIED: route participation carries information net of snap share on both arms.'))
for pos in ['WR', 'TE']:
    q = p4[p4.position == pos]
    r_ = ols_hc1(q.next4.values, [q.snap_pct.values, q.route_part.values], ['snap', 'route'])
    tilt_sd = (q.route_part - q.snap_pct).std()
    say(f'  size in decision units, {pos}: one sd of the tilt (route part minus snap share) is {tilt_sd:.1f} points of '
        f'participation, worth {r_[2][1] * tilt_sd:+.2f} half-PPR a week of NEXT4 net of snap share (pool NEXT4 mean {p[p.position == pos].next4.mean():.2f}, bar {BAR[pos]})')
sc_a = p[p.sig3 >= 2]; sc_b = p[(p.sig3 >= 2) & p.s_route]
sc_a4, sc_b4 = sc_a[sc_a.next4_n >= 2], sc_b[sc_b.next4_n >= 2]
say(f'  as a FOURTH SIGNAL on the wire screen (2+ of 3 bar): spike {(sc_b.spike.mean()-sc_a.spike.mean())*100:+.1f}, start next4 '
    f'{(sc_b4.start4.mean()-sc_a4.start4.mean())*100:+.1f} points (n {len(sc_b4)} vs {len(sc_a4)}), '
    f'the same order doc 437 called display-only for xfp (+2 bar)')
say('  CAVEAT: route participation here is DROPBACK participation (on the field for a dropback), not charted routes; a man who '
    'stays in to block counts as a route. The paid metric strips those out, so this is NOT a measurement of the paid metric. '
    'HYPOTHESIS, not tested here: charted routes add more than this approximation does.')
res_t = ols_hc1(p4[p4.tprr.notna()].next4.values, [p4[p4.tprr.notna()].snap_pct.values, p4[p4.tprr.notna()].route_part.values,
                p4[p4.tprr.notna()].tprr.values], ['snap', 'route', 'tprr'])
say(f'  TPRR net of snap and route (ALL, NEXT4 per percentage point of TPRR): {res_t[3][1]:+.4f} (se {res_t[3][2]:.4f})')

p.to_pickle(os.path.join(HERE, 'routes_pool.pkl'))
say('\npool pickled beside the script as routes_pool.pkl')
OUT.close()
