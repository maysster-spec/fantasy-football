#!/usr/bin/env python3
r"""j3_breadth.py -- JOB 3 TASK A: does role BREADTH predict how much of the vacated job the backup takes?

THE CLAIM IN ITS TESTABLE FORM, pre-registered in FABLE_JOB3_seat_lane.md (18 Sept) and restated here
before the run:
  Among direct backups who inherited an absence, the COMPOSITION of his pre-absence work predicts the
  share of the starter's vacated work he captures, OVER AND ABOVE his total pre-absence work share.
  Direction: a lopsided back (nearly all carries, or nearly all targets) captures LESS than a mixed
  back, because a specialist's role does not expand when the man ahead is gone.
KILL CONDITIONS, fixed before any number existed: breadth adds under 3 percentage points of captured
  share per 1.0 of breadth, or p above 0.10 -> DEAD. 3 to 8 points -> suggestive, a tiebreak only.
  Over 8 points with p under 0.05 -> a column.

POPULATION (0.6, restated): doc 320's 114 absence events, 2021-2025, weeks 2-14 -- the team-week in
  which the running back who led his team in carries plus targets to date played the previous week
  and has no line this week while his team plays; one event per absence, its first week. Rebuilt here
  by the same function (b2_depth_order.build_events()) on the same files as JOB 2 (doc 348), so the
  rows are the same rows. The BACKUP is the usage order's man (the man the page names, doc 320); the
  actual first-week inheritor is run as a sensitivity. The SPELL is the run of team-played weeks from
  the event week in which the leader has no line, capped at week 14 (the sheet's horizon), as in JOB 2.
  Every filter below prints how many of the 114 survive it and why.
PREDICTOR: breadth = 1 - |targets / (carries + targets) - 0.5| * 2 on the backup's weeks BEFORE the
  absence only (1.0 = an even split, 0.0 = pure specialist at either end); target_ratio reported raw
  because the fold hides which end he sits on.
OUTCOME: the backup's carries plus targets in the spell weeks, divided by the starter's per-game
  carries plus targets over his pre-absence weeks times the number of spell weeks; capped at 1.0, and
  the rows that hit the cap are counted.
BASELINE, the whole test: OLS of the outcome on the backup's TOTAL pre-absence work share alone (M1),
  then with breadth added (M2). Breadth earns its place only by the increment. Both coefficients,
  both standard errors, n and R-squared for each model; standard errors both player-level (classical)
  and clustered on the NFL team (a backfield's composition is close to a team constant).
INPUTS: nflverse stats_player_week_2021..2025.csv, depth_charts_2021..2025.csv, games.csv (fetched
  into the cache beside research\ if absent). pandas + numpy only (0.4).
Run:  py research\j3\j3_breadth.py        (J3_NFLVERSE and J3_OUT override the paths)
"""
import importlib.util
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
NFL = os.environ.get('J3_NFLVERSE', os.path.normpath(os.path.join(HERE, '..', '_nflverse_cache')))
OUT = os.environ.get('J3_OUT', HERE)
os.environ['B2_NFLVERSE'] = NFL
SEASONS = [2021, 2022, 2023, 2024, 2025]
HORIZON = 14
SEED = 20260918

_spec = importlib.util.spec_from_file_location('b2', os.path.join(HERE, '..', 'b2', 'b2_depth_order.py'))
b2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(b2)


def spell_weeks(t, teams_playing, lead_wks, w):
    out = []
    for x in range(w, HORIZON + 1):
        if x not in teams_playing or t not in teams_playing[x]:
            continue
        if x in lead_wks:
            break
        out.append(x)
    return out


# ---- OLS with classical and team-clustered standard errors, standard library + numpy only ----------
def t_sf(t, df):
    """Two-sided p from a Student t: 2 * P(T > |t|), by numerical integration of the density."""
    t = abs(float(t))
    if df <= 0:
        return float('nan')
    from math import lgamma, log, pi, exp
    c = exp(lgamma((df + 1) / 2) - lgamma(df / 2)) / (df * pi) ** 0.5
    x = np.linspace(t, t + 60, 200001)
    dens = c * (1 + x * x / df) ** (-(df + 1) / 2)
    area = float(((dens[1:] + dens[:-1]) * np.diff(x) / 2).sum())     # trapezoid, numpy 1.x and 2.x alike
    return float(min(1.0, 2 * area))


def ols(y, X, groups):
    """Returns coef, classical se, classical p, cluster se, cluster p, r2, n, G."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    e = y - X @ b
    ss_res = float(e @ e); ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float('nan')
    sigma2 = ss_res / (n - k)
    se = np.sqrt(np.diag(XtX_inv * sigma2))
    p = [t_sf(b[i] / se[i], n - k) for i in range(k)]
    # cluster-robust (Liang-Zeger) with the usual small-sample correction
    groups = np.asarray(groups)
    G = len(set(groups.tolist()))
    meat = np.zeros((k, k))
    for g in set(groups.tolist()):
        m = groups == g
        Xg = X[m]; eg = e[m]
        s = Xg.T @ eg
        meat += np.outer(s, s)
    corr = (G / (G - 1)) * ((n - 1) / (n - k))
    V = corr * XtX_inv @ meat @ XtX_inv
    se_c = np.sqrt(np.diag(V))
    p_c = [t_sf(b[i] / se_c[i], G - 1) for i in range(k)]
    return b, se, p, se_c, p_c, r2, n, G


def main():
    games = pd.read_csv(b2.need('games.csv', 'schedules'), low_memory=False)
    players = pd.read_csv(b2.need('players.csv', 'players'), low_memory=False, usecols=['gsis_id', 'display_name'])
    names = dict(zip(players.gsis_id, players.display_name))
    rows = []
    n_events = 0
    for s in SEASONS:
        stats = b2.load_stats(s)
        chart = b2.load_chart(s, games)
        events = b2.build_events(s, stats, chart)
        n_events += len(events)
        rb = stats[stats.position == 'RB'].copy()
        for c in ('carries', 'targets'):
            rb[c] = pd.to_numeric(rb[c], errors='coerce').fillna(0.0)
        rb['half'] = rb.fantasy_points.fillna(0) + 0.5 * rb.receptions.fillna(0)
        teams_playing = stats.groupby('week').team.apply(set).to_dict()
        for e in events:
            tm, w, lead = e['team'], e['week'], e['lead']
            t = rb[rb.team == tm]
            lead_wks = set(t[t.player_id == lead].week)
            spell = spell_weeks(tm, teams_playing, lead_wks, w)
            pre = t[t.week < w]
            pre_wks = sorted(w_ for w_ in set(pre.week))
            lead_pre = pre[pre.player_id == lead]
            lead_pg = float(lead_pre.touch.sum()) / len(lead_pre) if len(lead_pre) else 0.0
            pre_tot = float(pre.touch.sum())
            r = dict(season=s, team=tm, week=w, lead=lead, lead_name=names.get(lead, lead), spell_weeks=len(spell),
                     lead_pre_games=int(len(lead_pre)), lead_pre_work_pg=round(lead_pg, 2),
                     pre_weeks=len(pre_wks), pre_team_work=pre_tot)
            for tag in ('usage', 'actual'):
                m = e['pred_usage'] if tag == 'usage' else e['actual']
                r[f'{tag}_man'] = m; r[f'{tag}_name'] = names.get(m)
                mp = pre[pre.player_id == m]
                c_, t_ = float(mp.carries.sum()), float(mp.targets.sum())
                work = c_ + t_
                r[f'{tag}_pre_carries'] = c_; r[f'{tag}_pre_targets'] = t_; r[f'{tag}_pre_work'] = work
                r[f'{tag}_pre_games'] = int(len(mp))
                r[f'{tag}_share_pre'] = (work / pre_tot) if pre_tot > 0 else None
                if work > 0:
                    tr = t_ / work
                    r[f'{tag}_target_ratio'] = tr
                    r[f'{tag}_breadth'] = 1 - abs(tr - 0.5) * 2
                else:
                    r[f'{tag}_target_ratio'] = None; r[f'{tag}_breadth'] = None
                ms = t[t.week.isin(spell) & (t.player_id == m)]
                got = float(ms.touch.sum())
                r[f'{tag}_spell_work'] = got
                vac = lead_pg * len(spell)
                r[f'{tag}_captured_raw'] = (got / vac) if vac > 0 else None
                r[f'{tag}_captured'] = (min(1.0, got / vac)) if vac > 0 else None
                r[f'{tag}_capped'] = int(vac > 0 and got / vac > 1.0)
            rows.append(r)
    ev = pd.DataFrame(rows)
    ev.to_csv(os.path.join(OUT, 'J3_breadth_events.csv'), index=False)
    lines = []

    def say(*a):
        s_ = ' '.join(str(x) for x in a); print(s_); lines.append(s_)

    say(f'TASK A -- events rebuilt: {n_events} (JOB 2 had 114); spells capped at week {HORIZON}')
    assert n_events == 114, f'the event count moved: {n_events}'
    summary = {'n_events': n_events, 'arms': {}}
    for tag in ('usage', 'actual'):
        who = "the usage order's man (the page's man)" if tag == 'usage' else 'the ACTUAL first-week inheritor (sensitivity)'
        say(f'\n===== BACKUP = {who} =====')
        z = ev.copy()
        say(f'  start {len(z)}')
        z = z[z[f'{tag}_man'].notna()]; say(f'  has a named man: {len(z)}')
        z = z[z.spell_weeks > 0]; say(f'  spell of at least one week inside the horizon: {len(z)}')
        z = z[z.lead_pre_games > 0]; say(f'  starter has pre-absence games (a per-game rate exists): {len(z)}')
        z = z[z[f'{tag}_pre_work'] > 0]; say(f'  backup touched the ball before the absence (breadth defined): {len(z)}  <- the analysis rows')
        n_cap = int(z[f'{tag}_capped'].sum())
        say(f'  outcome capped at 1.0 on {n_cap} of {len(z)} rows (raw mean {z[f"{tag}_captured_raw"].mean():.3f}, capped mean {z[f"{tag}_captured"].mean():.3f})')
        y = z[f'{tag}_captured'].values
        sh = z[f'{tag}_share_pre'].values
        br = z[f'{tag}_breadth'].values
        tr = z[f'{tag}_target_ratio'].values
        groups = z.team.values
        X1 = np.column_stack([np.ones(len(z)), sh])
        X2 = np.column_stack([np.ones(len(z)), sh, br])
        b1, se1, p1, sc1, pc1, r21, n1, G1 = ols(y, X1, groups)
        b2_, se2, p2, sc2, pc2, r22, n2, G2 = ols(y, X2, groups)
        say(f'\n  M1  captured ~ share_pre                 n={n1}  R2={r21:.3f}  teams={G1}')
        say(f'      share_pre  coef {b1[1]:+.3f}  se {se1[1]:.3f} (p={p1[1]:.4f})   team-clustered se {sc1[1]:.3f} (p={pc1[1]:.4f})')
        say(f'  M2  captured ~ share_pre + breadth       n={n2}  R2={r22:.3f}  increment in R2 {r22 - r21:+.4f}')
        say(f'      share_pre  coef {b2_[1]:+.3f}  se {se2[1]:.3f} (p={p2[1]:.4f})   team-clustered se {sc2[1]:.3f} (p={pc2[1]:.4f})')
        say(f'      breadth    coef {b2_[2]:+.3f}  se {se2[2]:.3f} (p={p2[2]:.4f})   team-clustered se {sc2[2]:.3f} (p={pc2[2]:.4f})')
        pts = b2_[2] * 100
        verdict = ('DEAD' if (pts < 3 or p2[2] > 0.10) else 'SUGGESTIVE, a tiebreak only' if pts <= 8
                   else ('A COLUMN' if p2[2] < 0.05 else 'SUGGESTIVE, a tiebreak only'))
        say(f'  KILL CONDITION: breadth adds {pts:+.1f} points of captured share per 1.0 of breadth, p={p2[2]:.4f} -> {verdict}')
        # which end: the two ends separately, and the raw ratio as a bivariate description (NOT the test)
        X3 = np.column_stack([np.ones(len(z)), sh, tr])
        b3, se3, p3, sc3, pc3, r23, _, _ = ols(y, X3, groups)
        say(f'  M3  captured ~ share_pre + target_ratio  R2={r23:.3f}: target_ratio coef {b3[2]:+.3f} se {se3[2]:.3f} (p={p3[2]:.4f}; clustered p={pc3[2]:.4f})')
        # ends
        lo = z[z[f'{tag}_target_ratio'] < 0.15]; mid = z[(z[f'{tag}_target_ratio'] >= 0.15) & (z[f'{tag}_target_ratio'] <= 0.5)]; hi = z[z[f'{tag}_target_ratio'] > 0.5]
        say(f'  by end: carry-specialist (target ratio < 0.15) n={len(lo)} captured {lo[f"{tag}_captured"].mean() if len(lo) else float("nan"):.3f} share_pre {lo[f"{tag}_share_pre"].mean() if len(lo) else float("nan"):.3f} | '
            f'mixed (0.15-0.50) n={len(mid)} captured {mid[f"{tag}_captured"].mean() if len(mid) else float("nan"):.3f} share_pre {mid[f"{tag}_share_pre"].mean() if len(mid) else float("nan"):.3f} | '
            f'target-specialist (> 0.50) n={len(hi)} captured {hi[f"{tag}_captured"].mean() if len(hi) else float("nan"):.3f} share_pre {hi[f"{tag}_share_pre"].mean() if len(hi) else float("nan"):.3f}')
        # breadth terciles, described, with share_pre beside so the reader sees the confound
        q = z[f'{tag}_breadth'].quantile([1 / 3, 2 / 3]).values
        for lab, sel in (('breadth low', z[f'{tag}_breadth'] < q[0]), ('breadth mid', (z[f'{tag}_breadth'] >= q[0]) & (z[f'{tag}_breadth'] < q[1])), ('breadth high', z[f'{tag}_breadth'] >= q[1])):
            g = z[sel]
            say(f'  {lab:<13} n={len(g):>3}  breadth {g[f"{tag}_breadth"].mean():.2f}  share_pre {g[f"{tag}_share_pre"].mean():.3f}  captured {g[f"{tag}_captured"].mean():.3f}  pre work {g[f"{tag}_pre_work"].mean():.1f}')
        # sensitivity: the uncapped outcome, and a minimum of 10 pre-absence touches
        b4, se4, p4, sc4, pc4, r24, n4, _ = ols(z[f'{tag}_captured_raw'].values, X2, groups)
        say(f'  sensitivity, uncapped outcome: breadth coef {b4[2]:+.3f} se {se4[2]:.3f} (p={p4[2]:.4f})')
        z10 = z[z[f'{tag}_pre_work'] >= 10]
        if len(z10) > 10:
            X5 = np.column_stack([np.ones(len(z10)), z10[f'{tag}_share_pre'].values, z10[f'{tag}_breadth'].values])
            b5, se5, p5, sc5, pc5, r25, n5, _ = ols(z10[f'{tag}_captured'].values, X5, z10.team.values)
            say(f'  sensitivity, 10+ pre-absence touches (n={n5}): breadth coef {b5[2]:+.3f} se {se5[2]:.3f} (p={p5[2]:.4f}; clustered p={pc5[2]:.4f})')
        summary['arms'][tag] = dict(n=int(n2), teams=int(G2), capped=n_cap, r2_m1=round(r21, 4), r2_m2=round(r22, 4),
                                    share_coef_m1=round(float(b1[1]), 4), share_se_m1=round(float(se1[1]), 4),
                                    share_coef_m2=round(float(b2_[1]), 4), share_se_m2=round(float(se2[1]), 4),
                                    breadth_coef=round(float(b2_[2]), 4), breadth_se=round(float(se2[2]), 4), breadth_p=round(float(p2[2]), 4),
                                    breadth_se_cluster=round(float(sc2[2]), 4), breadth_p_cluster=round(float(pc2[2]), 4),
                                    breadth_points_per_unit=round(float(pts), 2), verdict=verdict,
                                    target_ratio_coef=round(float(b3[2]), 4), target_ratio_p=round(float(p3[2]), 4))
    with open(os.path.join(OUT, 'run_j3_breadth.txt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines) + '\n')
    json.dump(summary, open(os.path.join(OUT, 'J3_breadth_summary.json'), 'w'), indent=1)
    say(f'\nwrote J3_breadth_events.csv, J3_breadth_summary.json, run_j3_breadth.txt in {OUT}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
