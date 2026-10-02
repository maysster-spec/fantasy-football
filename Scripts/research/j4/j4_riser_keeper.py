#!/usr/bin/env python3
r"""
j4_riser_keeper.py -- JOB 4 from Source\REDTEAM_TASKING_PROMPT.md: THE RISER AS A KEEPER. Doc 382.

Matt, 16 Sept: "the model steered me to players who don't have that upside potential as keeper
candidates because they are not risers. That value was never measured."

TESTABLE FORM (the job's, verbatim in substance, written before the run):
  POPULATION  player-seasons in year N at QB RB WR TE, carrying a section 1.1 preseason ADP of 50 or
              later in year N (the keeper-eligible band) AND priced again in year N+1. N = 2022, 2023,
              2024, and 2021 with --with-2021 (doc 385: the 2021 weekly file is fetched into the cache).
  PREDICTOR   the riser: his share of team opportunity in weeks 10 to 14 of year N MINUS the same share
              in weeks 1 to 5. Opportunity = carries+targets at RB, targets at WR and TE, attempts at
              QB. Share = his opportunities / his team's opportunities of that kind over the team's
              games in the window (a missed game is a zero share for that game).
              Variant 2: share over year N (weeks 1 to 17) minus share over year N-1.
  CONTROL     log(preseason ADP in year N), mandatory, plus position.
  OUTCOMES    (i) year N+1 VBD14 on section 4.18b's baseline: weeks 1 to 14 league-scored points
              minus the SAME season's RB30 / WR30 / QB12 / TE12 weeks-1-to-14 total.
              (ii) startable at all in N+1, section 4.13b's absolute bar: weeks 1 to 14 ppg over games
              played (4+ games) at or above QB 20.09 / RB 9.92 / WR 9.62 / TE 8.25.
  MATT PREDICTS at equal price the riser beats the flat or declining man on both.
  FALSIFIER   trajectory adds nothing net of price with a CI excluding a 10-point VBD14 gap -> strike
              "ascending" from section 6. Trajectory carries 10+ net of price -> section 4.26(a) is the
              wrong instruction. CI spans both -> say what n would resolve it.
  SECOND ARM  youth (three seasons or fewer of NFL experience in year N) x trajectory; report which
              of substitution or amplification the number showed (section 0.5a3).

SCORING (section 2): pass 0.04/yd, 6 per pass TD, -2 INT, rush/rec 0.1/yd, 6 per TD, 0.5 per
reception, -2 per fumble lost, 2 per two-point conversion, 6 per return TD.

IDENTITY: the ADP registry carries names only (no id, no position), so the join to nflverse is by a
normalised name (lower-case, punctuation and Jr/Sr/II/III/IV stripped). A name that resolves to two
nflverse players at QB/RB/WR/TE in that season is DROPPED and counted, never guessed (section 3).

Standard library + pandas + numpy only. Paths resolve against this file. Writes J4_*.csv/json beside it.
"""
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))            # ...\2026
CACHE = os.path.join(ROOT, 'Scripts', 'research', '_nflverse_cache')
REG = os.path.join(ROOT, 'Source', 'adp_registry')
DRAFT = os.path.join(ROOT, 'Source', 'draft_history_2021_2025.csv')
for p in (CACHE, REG):
    if not os.path.isdir(p):
        sys.exit(f'missing input folder: {p}')

POS = ('QB', 'RB', 'WR', 'TE')
BAR = {'QB': 20.09, 'RB': 9.92, 'WR': 9.62, 'TE': 8.25}          # section 4.13b absolute bar, ppg
REPL_RANK = {'QB': 12, 'RB': 30, 'WR': 30, 'TE': 12}              # section 4.18b baseline
SEASONS_N = (2022, 2023, 2024)
ADP_MIN = 50.0
# Sensitivity switches (section 0.6: the population is the first thing that is wrong):
#   --no-price-next        drop the "priced again in N+1" condition (keep anyone with 4+ games in N+1)
#   --missing-window-zero  a man with no game in a window gets share 0 there instead of being dropped
#   --exclude-2024         drop N=2024, whose registry is a consensus RANK proxy, not an ADP
#   --with-2021            add N=2021 (doc 385): needs stats_player_week_2021.csv in the cache, from
#                          github.com/nflverse/nflverse-data/releases/download/stats_player/, and the
#                          2021 registry on the half-PPR page; refuses if either is missing
ARGS = set(sys.argv[1:])
if '--exclude-2024' in ARGS:
    SEASONS_N = (2022, 2023)
if '--with-2021' in ARGS:
    SEASONS_N = (2021,) + tuple(SEASONS_N)
    if not os.path.exists(os.path.join(CACHE, 'stats_player_week_2021.csv')):
        sys.exit('--with-2021: missing ' + os.path.join(CACHE, 'stats_player_week_2021.csv'))
TAG = '_'.join(a.strip('-').replace('-', '') for a in sorted(ARGS)) or 'main'
SEED = 20260921
rng = np.random.default_rng(SEED)


def norm_name(s):
    s = str(s).lower().replace('.', '').replace("'", '').replace('-', ' ')
    s = re.sub(r'[^a-z0-9 ]', '', s)
    toks = [t for t in s.split() if t not in ('jr', 'sr', 'ii', 'iii', 'iv', 'v')]
    return ' '.join(toks)


def score(df):
    """League-scored fantasy points per row (section 2)."""
    g = lambda c: pd.to_numeric(df.get(c, 0), errors='coerce').fillna(0.0)
    return (0.04 * g('passing_yards') + 6 * g('passing_tds') - 2 * g('passing_interceptions')
            + 0.1 * g('rushing_yards') + 6 * g('rushing_tds')
            + 0.5 * g('receptions') + 0.1 * g('receiving_yards') + 6 * g('receiving_tds')
            - 2 * (g('rushing_fumbles_lost') + g('receiving_fumbles_lost') + g('sack_fumbles_lost'))
            + 2 * (g('passing_2pt_conversions') + g('rushing_2pt_conversions') + g('receiving_2pt_conversions'))
            + 6 * g('special_teams_tds'))


def load_week(season):
    p = os.path.join(CACHE, f'stats_player_week_{season}.csv')
    w = pd.read_csv(p, low_memory=False)
    w = w[(w.season_type == 'REG') & (w.position.isin(POS))].copy()
    w['pts'] = score(w)
    w['week'] = w.week.astype(int)
    for c in ('carries', 'targets', 'attempts'):
        w[c] = pd.to_numeric(w[c], errors='coerce').fillna(0.0)
    w['opp_rb'] = w.carries + w.targets                       # RB opportunity
    w['opp_tgt'] = w.targets                                  # WR / TE opportunity
    w['opp_att'] = w.attempts                                 # QB opportunity
    w['k'] = w.player_display_name.map(norm_name)
    return w


def team_totals(w):
    """Team opportunity per team-week, each kind, summed over every player on the team."""
    return w.groupby(['team', 'week']).agg(t_rb=('opp_rb', 'sum'), t_tgt=('opp_tgt', 'sum'),
                                          t_att=('opp_att', 'sum')).reset_index()


def share_in_window(w, tt, lo, hi, played_only=False):
    """Per player: share of team opportunity over the team's games in weeks lo..hi.
    Numerator: his opportunities in games he played. Denominator: the team's opportunities in every
    game the team played in the window (so a missed game is a zero for him). Team = the team he
    played the most games for in the window (a mid-window trade splits the denominator; rare).
    played_only=True: the denominator is only the games HE played, so the share is his role when on
    the field and an absence does not move it (the availability confound, section 4.22)."""
    ww = w[(w.week >= lo) & (w.week <= hi)]
    if ww.empty:
        return pd.DataFrame(columns=['player_id', 'share'])
    kind = {'RB': 'opp_rb', 'WR': 'opp_tgt', 'TE': 'opp_tgt', 'QB': 'opp_att'}
    tkind = {'RB': 't_rb', 'WR': 't_tgt', 'TE': 't_tgt', 'QB': 't_att'}
    rows = []
    ttw = tt[(tt.week >= lo) & (tt.week <= hi)]
    tsum = ttw.groupby('team')[['t_rb', 't_tgt', 't_att']].sum()
    tidx = ttw.set_index(['team', 'week'])
    for pid, g in ww.groupby('player_id'):
        pos = g.position.iloc[-1]
        team = g.team.mode().iloc[0]
        if team not in tsum.index:
            continue
        if played_only:
            wks = [(team, wk) for wk in g[g.team == team].week.unique() if (team, wk) in tidx.index]
            den = tidx.loc[wks, tkind[pos]].sum() if wks else 0.0
        else:
            den = tsum.loc[team, tkind[pos]]
        num = g[g.team == team][kind[pos]].sum()
        rows.append((pid, num / den if den > 0 else np.nan))
    return pd.DataFrame(rows, columns=['player_id', 'share'])


def season_totals(w, lo=1, hi=14):
    ww = w[(w.week >= lo) & (w.week <= hi)]
    return ww.groupby('player_id').agg(pts=('pts', 'sum'), games=('week', 'nunique'),
                                       pos=('position', 'last'), name=('player_display_name', 'last'),
                                       k=('k', 'last')).reset_index()


def replacement(tot):
    """The 30th RB's (12th QB's ...) weeks-1-to-14 total in that season."""
    out = {}
    for p in POS:
        s = tot[tot.pos == p].pts.sort_values(ascending=False).values
        r = REPL_RANK[p]
        out[p] = float(s[r - 1]) if len(s) >= r else float('nan')
    return out


def load_adp(season):
    df = pd.read_csv(os.path.join(REG, f'preseason_adp_{season}.csv'))
    df['k'] = df.player.map(norm_name)
    return df[['k', 'adp']].drop_duplicates('k', keep='first')


def ols(X, y):
    X = np.asarray(X, float); y = np.asarray(y, float)
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b
    n, p = X.shape
    s2 = (r @ r) / max(n - p, 1)
    cov = s2 * np.linalg.pinv(X.T @ X)
    return b, np.sqrt(np.diag(cov)), r


def logistic(X, y):
    X = np.asarray(X, float); y = np.asarray(y, float)
    b = np.zeros(X.shape[1])
    for _ in range(200):
        p = 1 / (1 + np.exp(-np.clip(X @ b, -30, 30)))
        W = p * (1 - p) + 1e-9
        H = X.T @ (X * W[:, None]) + 1e-6 * np.eye(X.shape[1])
        step = np.linalg.solve(H, X.T @ (y - p))
        b += step
        if np.abs(step).max() < 1e-9:
            break
    se = np.sqrt(np.diag(np.linalg.inv(H)))
    return b, se


def boot_gap(df, col, ycol, B=2000):
    """Adjusted gap, top tercile of `col` minus bottom tercile, net of log ADP and position, by
    bootstrap over player-seasons. Returns (point, lo, hi)."""
    def one(d):
        q1, q2 = d[col].quantile([1 / 3, 2 / 3])
        hi = (d[col] >= q2).astype(float); lo = (d[col] <= q1).astype(float)
        X = np.column_stack([np.ones(len(d)), hi, lo, np.log(d.adp), d.pos_RB, d.pos_WR, d.pos_TE])
        b, _, _ = ols(X, d[ycol])
        return b[1] - b[2]
    pt = one(df)
    bs = []
    idx = np.arange(len(df))
    for _ in range(B):
        s = df.iloc[rng.choice(idx, len(idx), replace=True)]
        try:
            bs.append(one(s))
        except Exception:                                       # noqa: BLE001
            continue
    return pt, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def main():
    weeks = {s: load_week(s) for s in range(min(SEASONS_N), 2026)}
    players = pd.read_csv(os.path.join(CACHE, 'players.csv'), low_memory=False,
                          usecols=['gsis_id', 'rookie_season', 'draft_round', 'draft_year'])
    rook = players.dropna(subset=['gsis_id']).drop_duplicates('gsis_id').set_index('gsis_id')

    rows, dropped = [], {'no_nflverse_match': 0, 'ambiguous_name': 0, 'no_window_share': 0,
                         'not_priced_next_year': 0, 'no_next_year_games': 0}
    for N in SEASONS_N:
        w, w1 = weeks[N], weeks[N + 1]
        tt = team_totals(w)
        early = share_in_window(w, tt, 1, 5).set_index('player_id').share
        late = share_in_window(w, tt, 10, 14).set_index('player_id').share
        early_pg = share_in_window(w, tt, 1, 5, played_only=True).set_index('player_id').share
        late_pg = share_in_window(w, tt, 10, 14, played_only=True).set_index('player_id').share
        full_n = share_in_window(w, tt, 1, 17).set_index('player_id').share
        full_prev = (share_in_window(weeks[N - 1], team_totals(weeks[N - 1]), 1, 17)
                     .set_index('player_id').share if (N - 1) in weeks else None)
        tot_n = season_totals(w)
        tot_n1 = season_totals(w1)
        repl = replacement(tot_n1)
        repl_n = replacement(tot_n)
        adp_n, adp_n1 = load_adp(N), load_adp(N + 1)
        # name -> player_id in year N, at the four positions; ambiguous names dropped. A miss on the
        # exact key falls back to LAST NAME + FIRST INITIAL (Gabe/Gabriel Davis, Ken/Kenneth Walker,
        # Chig/Chigoziem Okonkwo), accepted only when that key is unique in nflverse that season;
        # the fallback is generated from the two spines, never typed (section 3).
        ids = w.groupby('k').player_id.nunique()
        first = w.drop_duplicates('k').set_index('k').player_id
        w['k2'] = w.k.map(lambda k: (k.split()[-1] + ' ' + k[0]) if k else '')
        ids2 = w.groupby('k2').player_id.nunique()
        first2 = w.drop_duplicates('k2').set_index('k2').player_id
        for _, a in adp_n.iterrows():
            if a.adp < ADP_MIN:
                continue
            k = a.k
            if k in ids.index:
                if ids[k] > 1:
                    dropped['ambiguous_name'] += 1
                    continue
                pid = first[k]
            else:
                k2 = (k.split()[-1] + ' ' + k[0]) if k else ''
                if k2 in ids2.index and ids2[k2] == 1:
                    pid = first2[k2]
                    dropped['matched_by_fallback'] = dropped.get('matched_by_fallback', 0) + 1
                else:
                    dropped['no_nflverse_match'] += 1
                    continue
            if k not in set(adp_n1.k):
                dropped['not_priced_next_year'] += 1
                if '--no-price-next' not in ARGS:
                    continue
            if pid not in early.index or pid not in late.index:
                dropped['no_window_share'] += 1
                if '--missing-window-zero' not in ARGS:
                    continue
            e_sh = float(early[pid]) if pid in early.index else 0.0
            l_sh = float(late[pid]) if pid in late.index else 0.0
            t1 = tot_n1[tot_n1.player_id == pid]
            if t1.empty or int(t1.games.iloc[0]) < 4:
                dropped['no_next_year_games'] += 1
                continue
            pos = t1.pos.iloc[0]
            g1 = int(t1.games.iloc[0]); p1 = float(t1.pts.iloc[0])
            rk = rook.loc[pid] if pid in rook.index else None
            rs = float(rk.rookie_season) if rk is not None and pd.notna(rk.rookie_season) else np.nan
            rows.append({
                'season_N': N, 'player_id': pid, 'name': t1.name.iloc[0], 'pos': pos,
                'adp_N': float(a.adp),
                'adp_N1': float(adp_n1.set_index('k').adp[k]) if k in set(adp_n1.k) else np.nan,
                'share_early': e_sh, 'share_late': l_sh,
                'riser': l_sh - e_sh,
                'riser_pg': (float(late_pg[pid] - early_pg[pid])
                             if pid in late_pg.index and pid in early_pg.index else np.nan),
                'riser_v2': (float(full_n[pid] - full_prev[pid])
                             if full_prev is not None and pid in full_n.index and pid in full_prev.index
                             else np.nan),
                'games_N': int(tot_n[tot_n.player_id == pid].games.iloc[0]) if (tot_n.player_id == pid).any() else 0,
                'vbd14_N': (float(tot_n[tot_n.player_id == pid].pts.iloc[0]) - repl_n[pos]) if (tot_n.player_id == pid).any() else np.nan,
                'exp_N': (N - rs + 1) if pd.notna(rs) else np.nan,
                'draft_round': float(rk.draft_round) if rk is not None and pd.notna(rk.draft_round) else np.nan,
                'games_N1': g1, 'pts14_N1': p1, 'ppg_N1': p1 / g1,
                'vbd14_N1': p1 - repl[pos],
                'startable_N1': int(p1 / g1 >= BAR[pos]),
            })
    df = pd.DataFrame(rows)
    df['young'] = (df.exp_N <= 3).astype(float)
    for p in ('RB', 'WR', 'TE'):
        df[f'pos_{p}'] = (df.pos == p).astype(float)
    df.to_csv(os.path.join(HERE, f'J4_rows_{TAG}.csv'), index=False)

    out = {'seed': SEED, 'run': TAG, 'population': f'year-N player-seasons {min(SEASONS_N)} to {max(SEASONS_N)}, QB RB WR TE, preseason ADP >= 50 '
                                       'in N (registry), priced again in N+1, 4+ games in N+1 weeks 1 to 14',
           'n_pooled': int(len(df)), 'n_by_pos': df.pos.value_counts().to_dict(),
           'n_by_season': df.season_N.value_counts().sort_index().to_dict(), 'dropped': dropped,
           'replacement_N1': {}, 'base_rates': {}}
    print('POPULATION', out['n_pooled'], out['n_by_pos'], out['n_by_season'])
    print('DROPPED', dropped)
    for N in SEASONS_N:
        out['replacement_N1'][N + 1] = replacement(season_totals(weeks[N + 1]))
    print('REPLACEMENT weeks 1-14 totals by N+1 season', out['replacement_N1'])
    out['base_rates'] = {'startable_N1': float(df.startable_N1.mean()),
                         'vbd14_N1_mean': float(df.vbd14_N1.mean()),
                         'riser_mean': float(df.riser.mean()), 'riser_sd': float(df.riser.std())}
    print('BASE', out['base_rates'])

    # ---- 1. price alone, then price + trajectory (VBD14)
    X0 = np.column_stack([np.ones(len(df)), np.log(df.adp_N), df.pos_RB, df.pos_WR, df.pos_TE])
    b0, se0, r0 = ols(X0, df.vbd14_N1)
    X1 = np.column_stack([X0, df.riser * 10])                 # per 10 points of team share
    b1, se1, r1 = ols(X1, df.vbd14_N1)
    out['vbd_models'] = {
        'price_only': {'log_adp': [float(b0[1]), float(se0[1])],
                       'r2': float(1 - (r0 @ r0) / ((df.vbd14_N1 - df.vbd14_N1.mean()) ** 2).sum())},
        'price_plus_riser': {'log_adp': [float(b1[1]), float(se1[1])],
                             'riser_per_10pts_share': [float(b1[5]), float(se1[5])],
                             'r2': float(1 - (r1 @ r1) / ((df.vbd14_N1 - df.vbd14_N1.mean()) ** 2).sum())}}
    print('VBD14 ~ logADP + pos: logADP %.2f (se %.2f)' % (b0[1], se0[1]))
    print('VBD14 ~ logADP + pos + riser: riser per +10 share pts %.2f (se %.2f), logADP %.2f' % (b1[5], se1[5], b1[1]))

    # ---- 2. the tercile gap, net of price and position, bootstrap
    df['adp_N'] = df.adp_N.astype(float)
    df = df.rename(columns={'adp_N': 'adp'})
    gap = boot_gap(df, 'riser', 'vbd14_N1')
    out['gap_vbd14_top_vs_bottom_tercile_net_of_price'] = {'point': gap[0], 'ci95': [gap[1], gap[2]]}
    print('GAP VBD14, top tercile riser minus bottom, net of price+pos: %.1f [%.1f, %.1f]' % gap)
    q1, q2 = df.riser.quantile([1 / 3, 2 / 3])
    out['tercile_cuts'] = [float(q1), float(q2)]
    for lab, m in (('bottom (fell)', df.riser <= q1), ('middle', (df.riser > q1) & (df.riser < q2)), ('top (rose)', df.riser >= q2)):
        d = df[m]
        out.setdefault('terciles', {})[lab] = {'n': int(len(d)), 'riser_mean': float(d.riser.mean()),
                                               'adp_mean': float(d.adp.mean()), 'vbd14_N1_mean': float(d.vbd14_N1.mean()),
                                               'startable_N1': float(d.startable_N1.mean())}
        print('  %-14s n=%3d riser %+.3f adp %5.1f  VBD14 %+6.1f  startable %.0f%%'
              % (lab, len(d), d.riser.mean(), d.adp.mean(), d.vbd14_N1.mean(), 100 * d.startable_N1.mean()))

    # ---- 3. startable (logistic), price then price + riser
    L0, s0 = logistic(X0, df.startable_N1)
    L1, s1 = logistic(X1, df.startable_N1)
    out['startable_models'] = {'price_only_log_adp': [float(L0[1]), float(s0[1])],
                               'price_plus_riser': {'log_adp': [float(L1[1]), float(s1[1])],
                                                    'riser_per_10pts_share': [float(L1[5]), float(s1[5])]}}
    print('STARTABLE ~ logADP + pos + riser: riser per +10 share pts %.3f (se %.3f)' % (L1[5], s1[5]))
    # adjusted startable rate, top vs bottom tercile, at the mean price
    def adj_rate(d, m):
        Xm = np.column_stack([np.ones(m.sum()), np.log(d.adp[m]), d.pos_RB[m], d.pos_WR[m], d.pos_TE[m], d.riser[m] * 10])
        return float((1 / (1 + np.exp(-(Xm @ L1)))).mean())
    out['startable_adjusted'] = {'top_tercile': adj_rate(df, df.riser >= q2), 'bottom_tercile': adj_rate(df, df.riser <= q1)}
    print('STARTABLE adjusted (model, own prices): top %.1f%%  bottom %.1f%%' % (100 * out['startable_adjusted']['top_tercile'], 100 * out['startable_adjusted']['bottom_tercile']))

    # ---- 4. by position
    out['by_pos'] = {}
    for p in POS:
        d = df[df.pos == p]
        if len(d) < 15:
            out['by_pos'][p] = {'n': int(len(d)), 'note': 'too few'}
            continue
        Xp = np.column_stack([np.ones(len(d)), np.log(d.adp), d.riser * 10])
        bp, sp, _ = ols(Xp, d.vbd14_N1)
        out['by_pos'][p] = {'n': int(len(d)), 'riser_per_10pts_share': [float(bp[2]), float(sp[2])],
                            'log_adp': [float(bp[1]), float(sp[1])], 'startable': float(d.startable_N1.mean())}
        print('  %s n=%3d riser per +10 %.2f (se %.2f)  logADP %.2f' % (p, len(d), bp[2], sp[2], bp[1]))

    # ---- 5. variant 2 (year N vs N-1 share), where both exist
    d2 = df.dropna(subset=['riser_v2'])
    if len(d2) >= 30:
        X2 = np.column_stack([np.ones(len(d2)), np.log(d2.adp), d2.pos_RB, d2.pos_WR, d2.pos_TE, d2.riser_v2 * 10])
        b2, se2, _ = ols(X2, d2.vbd14_N1)
        out['variant2_year_over_year'] = {'n': int(len(d2)), 'riser_v2_per_10pts_share': [float(b2[5]), float(se2[5])]}
        print('VARIANT 2 (N vs N-1 share) n=%d: per +10 %.2f (se %.2f)' % (len(d2), b2[5], se2[5]))

    # ---- 5b. the availability confound: the same regression on the share WHEN HE PLAYED (a missed
    # game does not move it). If this survives, the riser is a role change, not a health record.
    dp = df.dropna(subset=['riser_pg'])
    Xp = np.column_stack([np.ones(len(dp)), np.log(dp.adp), dp.pos_RB, dp.pos_WR, dp.pos_TE, dp.riser_pg * 10])
    bp_, sp_, _ = ols(Xp, dp.vbd14_N1)
    out['riser_when_played'] = {'n': int(len(dp)), 'riser_pg_per_10pts_share': [float(bp_[5]), float(sp_[5])]}
    dpr = dp[dp.pos == 'RB']
    Xr = np.column_stack([np.ones(len(dpr)), np.log(dpr.adp), dpr.riser_pg * 10])
    br_, sr_, _ = ols(Xr, dpr.vbd14_N1)
    out['riser_when_played']['RB'] = {'n': int(len(dpr)), 'per_10': [float(br_[2]), float(sr_[2])]}
    print('WHEN PLAYED (availability held out) n=%d: riser per +10 %.2f (se %.2f); RB n=%d %.2f (se %.2f)'
          % (len(dp), bp_[5], sp_[5], len(dpr), br_[2], sr_[2]))

    # ---- 6. the second arm: youth x trajectory
    dy = df.dropna(subset=['exp_N'])
    Xy = np.column_stack([np.ones(len(dy)), np.log(dy.adp), dy.pos_RB, dy.pos_WR, dy.pos_TE,
                          dy.riser * 10, dy.young, dy.riser * 10 * dy.young])
    by, sy, _ = ols(Xy, dy.vbd14_N1)
    out['youth_arm'] = {'n': int(len(dy)), 'n_young': int(dy.young.sum()),
                        'riser_per_10_old': [float(by[5]), float(sy[5])], 'young_main': [float(by[6]), float(sy[6])],
                        'interaction_per_10': [float(by[7]), float(sy[7])]}
    print('YOUTH ARM n=%d (young %d): riser(old) %.2f (se %.2f)  young %.2f (se %.2f)  riser x young %.2f (se %.2f)'
          % (len(dy), dy.young.sum(), by[5], sy[5], by[6], sy[6], by[7], sy[7]))
    cells = {}
    for yl, ym in (('young', dy.young == 1), ('older', dy.young == 0)):
        for tl, tm in (('rose', dy.riser >= q2), ('fell', dy.riser <= q1)):
            d = dy[ym & tm]
            cells[f'{yl}/{tl}'] = {'n': int(len(d)), 'vbd14': float(d.vbd14_N1.mean()) if len(d) else None,
                                   'startable': float(d.startable_N1.mean()) if len(d) else None,
                                   'adp': float(d.adp.mean()) if len(d) else None}
    out['youth_cells'] = cells
    for k_, v in cells.items():
        print('  %-12s n=%3d VBD14 %s startable %s adp %s' % (k_, v['n'],
              'n/a' if v['vbd14'] is None else '%+.1f' % v['vbd14'],
              'n/a' if v['startable'] is None else '%.0f%%' % (100 * v['startable']),
              'n/a' if v['adp'] is None else '%.0f' % v['adp']))

    # ---- 6b. the section 4.18b object: among year-N HITS (VBD14_N > 0), does the late-season share
    # separate the one-year fluke from the role that carried into N+1? This is the split 4.18b
    # could not make, because its population was defined by price alone.
    hits = df[df.vbd14_N > 0].copy()
    out['hits_arm'] = {'n_hits': int(len(hits))}
    if len(hits) >= 30:
        Xh = np.column_stack([np.ones(len(hits)), np.log(hits.adp), hits.vbd14_N, hits.pos_RB, hits.pos_WR, hits.pos_TE, hits.riser * 10])
        bh, sh, _ = ols(Xh, hits.vbd14_N1)
        out['hits_arm'].update({'riser_per_10_net_of_price_and_size': [float(bh[6]), float(sh[6])],
                                'vbd14_N_coef': [float(bh[2]), float(sh[2])]})
        hq1, hq2 = hits.riser.quantile([1 / 3, 2 / 3])
        for lab, m in (('hit, share fell', hits.riser <= hq1), ('hit, share flat', (hits.riser > hq1) & (hits.riser < hq2)), ('hit, share rose', hits.riser >= hq2)):
            d = hits[m]
            out['hits_arm'][lab] = {'n': int(len(d)), 'vbd14_N': float(d.vbd14_N.mean()), 'vbd14_N1': float(d.vbd14_N1.mean()),
                                    'startable_N1': float(d.startable_N1.mean()), 'kept_value_share': float((d.vbd14_N1 > 0).mean())}
            print('  %-16s n=%3d  VBD14_N %+6.1f -> VBD14_N+1 %+6.1f  startable %.0f%%  still above replacement %.0f%%'
                  % (lab, len(d), d.vbd14_N.mean(), d.vbd14_N1.mean(), 100 * d.startable_N1.mean(), 100 * (d.vbd14_N1 > 0).mean()))
        print('HITS ARM n=%d: riser per +10, net of price and the size of the hit: %.2f (se %.2f); hit size itself %.2f (se %.2f)'
              % (len(hits), bh[6], sh[6], bh[2], sh[2]))

    # ---- 7. what n would resolve a 10-point gap, from the observed residual sd
    sd = float(np.std(r1))
    out['power'] = {'residual_sd': sd,
                    'n_per_arm_for_10pt_gap_80pct_power': int(np.ceil(2 * ((1.96 + 0.84) * sd / 10) ** 2))}
    print('POWER: residual sd %.1f; n per tercile to resolve a 10-point gap at 80%%: %d' % (sd, out['power']['n_per_arm_for_10pt_gap_80pct_power']))

    # ---- 7b. THE BAND SPLIT the directive quotes (section 4.34): ADP 50 to 96 (rounds 5 to 8) against
    # 97 and later. Doc 382 to 384 computed this outside the script; it is inside it since doc 385, and
    # it reproduces doc 384's band row exactly on J4_rows_main_halfppr3.csv (+51.0 [18.5, 73.4], n=100).
    def band(lo, hi_):
        d = df[(df.adp >= lo) & (df.adp < hi_)].reset_index(drop=True)
        Xb = np.column_stack([np.ones(len(d)), np.log(d.adp), d.pos_RB, d.pos_WR, d.pos_TE, d.riser * 10])
        bb, sb, _ = ols(Xb, d.vbd14_N1)
        def one(e):
            c1, c2 = e.riser.quantile([1 / 3, 2 / 3])
            Xg = np.column_stack([np.ones(len(e)), (e.riser >= c2).astype(float), (e.riser <= c1).astype(float),
                                  np.log(e.adp), e.pos_RB, e.pos_WR, e.pos_TE])
            bg, _, _ = ols(Xg, e.vbd14_N1)
            return bg[1] - bg[2]
        rb = np.random.default_rng(SEED)
        bs = []
        for _ in range(2000):
            try:
                bs.append(one(d.iloc[rb.choice(len(d), len(d), replace=True)]))
            except Exception:                                   # noqa: BLE001
                continue
        c1, c2 = d.riser.quantile([1 / 3, 2 / 3])
        dy_ = d.dropna(subset=['exp_N'])
        Xy_ = np.column_stack([np.ones(len(dy_)), np.log(dy_.adp), dy_.pos_RB, dy_.pos_WR, dy_.pos_TE,
                               dy_.riser * 10, dy_.young, dy_.riser * 10 * dy_.young])
        by_, sy_, _ = ols(Xy_, dy_.vbd14_N1)
        return {'n': int(len(d)), 'riser_per_10': [float(bb[5]), float(sb[5])], 'log_adp': [float(bb[1]), float(sb[1])],
                'gap': float(one(d)), 'gap_ci95': [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
                'startable_top': float(d[d.riser >= c2].startable_N1.mean()),
                'startable_bottom': float(d[d.riser <= c1].startable_N1.mean()),
                'youth_x_riser': [float(by_[7]), float(sy_[7])]}
    out['bands'] = {'adp_50_96_rounds_5_to_8': band(50, 97), 'adp_97_plus_round_9_on': band(97, 1e9)}
    for lab, v in out['bands'].items():
        print('BAND %-24s n=%3d gap %+.1f [%.1f, %.1f]  riser per +10 %+.1f (se %.1f)  log ADP %+.1f (se %.0f)  '
              'startable %.0f%% vs %.0f%%  youth x riser %+.1f (se %.1f)'
              % (lab, v['n'], v['gap'], v['gap_ci95'][0], v['gap_ci95'][1], v['riser_per_10'][0], v['riser_per_10'][1],
                 v['log_adp'][0], v['log_adp'][1], 100 * v['startable_top'], 100 * v['startable_bottom'],
                 v['youth_x_riser'][0], v['youth_x_riser'][1]))

    # ---- 8. this league's actual keepers, where they sat on the riser scale (descriptive)
    if os.path.exists(DRAFT):
        try:
            dh = pd.read_csv(DRAFT, low_memory=False)
            kcol = [c for c in dh.columns if 'keep' in c.lower()]
            out['league_keepers_note'] = f'draft_history columns with keep: {kcol}'
        except Exception as exc:                                # noqa: BLE001
            out['league_keepers_note'] = f'could not read draft history: {exc}'

    with open(os.path.join(HERE, f'J4_summary_{TAG}.json'), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1, default=float)
    print(f'written J4_rows_{TAG}.csv, J4_summary_{TAG}.json')


if __name__ == '__main__':
    main()
