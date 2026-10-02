#!/usr/bin/env python3
"""Does the size of the absent starter's job predict the relief back's half-PPR points a game?

Runs with `python3 job_slope.py`. Cache dir from env FF_CACHE (default below). pandas + numpy only.
Writes job_slope_results.md and job_slope_absences.csv next to this script.
"""
import os
import numpy as np
import pandas as pd

CACHE = os.environ.get(
    "FF_CACHE", os.path.join(os.path.dirname(os.path.abspath(__file__)), '_nflverse_cache'))
HERE = os.path.dirname(os.path.abspath(__file__))
SEASONS = range(2021, 2026)
SEED = 20260930
B = 5000
FLAT = 12.1


def load():
    cols = ["season", "season_type", "week", "player_id", "player_display_name",
            "position", "team", "carries", "rushing_yards", "rushing_tds",
            "targets", "receptions", "receiving_yards", "receiving_tds",
            "rushing_fumbles_lost", "receiving_fumbles_lost", "sack_fumbles_lost"]
    frames = []
    for y in SEASONS:
        d = pd.read_csv(os.path.join(CACHE, f"stats_player_week_{y}.csv"), usecols=cols)
        frames.append(d[(d.season_type == "REG") & (d.week.between(1, 14))])
    d = pd.concat(frames, ignore_index=True)
    num = [c for c in cols if c not in ("season_type", "player_id", "player_display_name", "position", "team", "season", "week")]
    d[num] = d[num].fillna(0)
    d["pts"] = (0.1 * (d.rushing_yards + d.receiving_yards)
                + 6 * (d.rushing_tds + d.receiving_tds) + 0.5 * d.receptions
                - 2 * (d.rushing_fumbles_lost + d.receiving_fumbles_lost + d.sack_fumbles_lost))
    d["opp"] = d.carries + d.targets
    return d


def build(d, drop_departures=True, per="played", starter_mode="total"):
    """One row per absence. per='played' divides Y by relief games with opps>0; 'team' by absence length."""
    rows = []
    n_departed = 0
    for (season, team), tm in d.groupby(["season", "team"]):
        weeks = sorted(tm.week.unique())  # team games, bye skipped automatically
        rb = tm[tm.position == "RB"]
        if rb.empty:
            continue
        if starter_mode == "total":
            starter = rb.groupby("player_id").opp.sum().idxmax()
        else:  # "rate": most opportunities per game played, among RBs with 4+ games played
            act = rb[rb.opp > 0].groupby("player_id").opp.agg(["mean", "size"])
            act = act[act["size"] >= 4]
            if act.empty:
                continue
            starter = act["mean"].idxmax()
        srows = rb[rb.player_id == starter].set_index("week")
        active_all = srows[srows.opp > 0]
        if len(active_all) == 0 or active_all.opp.mean() < 10:
            continue
        opp_by_week = {w: (srows.opp.get(w, 0)) for w in weeks}
        # maximal runs of consecutive team games with zero opportunities
        i = 0
        while i < len(weeks):
            if opp_by_week[weeks[i]] == 0:
                j = i
                while j + 1 < len(weeks) and opp_by_week[weeks[j + 1]] == 0:
                    j += 1
                run = weeks[i:j + 1]
                i = j + 1
                if len(run) < 2:
                    continue
                before = [w for w in weeks if w < run[0] and opp_by_week[w] > 0]
                if len(before) < 2:
                    continue
                # starter on another team during the run = left the team, not an absence
                other = d[(d.season == season) & (d.player_id == starter) & (d.team != team)
                          & (d.week.isin(run)) & (d.opp > 0)]
                if len(other) and drop_departures:
                    n_departed += 1
                    continue
                pre = srows.loc[before]
                X = pre.pts.mean()
                during = rb[(rb.week.isin(run)) & (rb.player_id != starter)]
                if during.empty:
                    continue
                g = during.groupby("player_id").agg(opp=("opp", "sum"), pts=("pts", "sum"),
                                                    gp=("opp", lambda s: int((s > 0).sum())))
                relief = g.opp.idxmax()
                gp = int(g.loc[relief, "gp"])
                if gp == 0:
                    continue
                denom = gp if per == "played" else len(run)
                Y = g.loc[relief, "pts"] / denom
                # relief back's own games before the absence this season (any team), with opportunities
                rp = d[(d.season == season) & (d.player_id == relief) & (d.week < run[0]) & (d.opp > 0)]
                Z = rp.pts.mean() if len(rp) else np.nan
                name = d.loc[d.player_id == starter, "player_display_name"].iloc[0]
                rname = d.loc[d.player_id == relief, "player_display_name"].iloc[0]
                rows.append(dict(season=season, team=team, starter=name, relief=rname,
                                 start_week=run[0], length=len(run), relief_games=gp, pre_games=len(before),
                                 X=X, starter_opp_pg=pre.opp.mean(), Y=Y, Z=Z, Z_games=len(rp)))
            else:
                i += 1
    return pd.DataFrame(rows), n_departed


def ols(X, y):
    """X has intercept column. Returns beta, se (classical), r2."""
    n, k = X.shape
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    s2 = res @ res / (n - k)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    r2 = 1 - (res @ res) / ((y - y.mean()) @ (y - y.mean()))
    return beta, se, r2


def boot(X, y, idx_coef, rng):
    n = len(y)
    out = np.empty(B)
    for b in range(B):
        ii = rng.integers(0, n, n)
        try:
            out[b] = np.linalg.lstsq(X[ii], y[ii], rcond=None)[0][idx_coef]
        except np.linalg.LinAlgError:
            out[b] = np.nan
    return np.nanpercentile(out, [2.5, 97.5])


def analyse(a):
    rng = np.random.default_rng(SEED)
    r = {}
    y = a.Y.values
    x = a.X.values
    A = np.column_stack([np.ones(len(a)), x])
    beta, se, r2 = ols(A, y)
    r.update(n=len(a), meanY=y.mean(), medY=np.median(y), sdY=y.std(ddof=1),
             slope=beta[1], icpt=beta[0], se=se[1], r2=r2,
             ci=boot(A, y, 1, rng), corr=np.corrcoef(x, y)[0, 1],
             meanX=x.mean(), pred15=beta[0] + beta[1] * 15, pred9=beta[0] + beta[1] * 9)
    # Spearman via ranks
    rk = lambda v: pd.Series(v).rank().values
    r["spearman"] = np.corrcoef(rk(x), rk(y))[0, 1]
    q = a.X.quantile([1 / 3, 2 / 3]).values
    a = a.assign(tercile=np.where(a.X <= q[0], "bottom", np.where(a.X <= q[1], "middle", "top")))
    r["terc"] = [(t, int((a.tercile == t).sum()), a[a.tercile == t].X.mean(),
                  a[a.tercile == t].Y.mean(), a[a.tercile == t].Y.median()) for t in ("bottom", "middle", "top")]
    r["cuts"] = q
    # control for relief back's own prior ppg
    s = a.dropna(subset=["Z"])
    ys, xs, zs = s.Y.values, s.X.values, s.Z.values
    A1 = np.column_stack([np.ones(len(s)), xs])
    A2 = np.column_stack([np.ones(len(s)), xs, zs])
    b1, se1, _ = ols(A1, ys)
    b2, se2, r22 = ols(A2, ys)
    r.update(nz=len(s), slope_sub=b1[1], se_sub=se1[1], ci_sub=boot(A1, ys, 1, rng),
             slope_ctl=b2[1], se_ctl=se2[1], ci_ctl=boot(A2, ys, 1, rng),
             zcoef=b2[2], zse=se2[2], ci_z=boot(A2, ys, 2, rng), r2_ctl=r22,
             corr_xz=np.corrcoef(xs, zs)[0, 1], corr_zy=np.corrcoef(zs, ys)[0, 1])
    return r, a


def fmt_ci(ci):
    return f"[{ci[0]:+.3f}, {ci[1]:+.3f}]"


def count_starters(d):
    """Starter team-seasons under the total-opportunities rule, and how many of them missed any team game."""
    n = miss = 0
    for (season, team), tm in d.groupby(["season", "team"]):
        rb = tm[tm.position == "RB"]
        if rb.empty:
            continue
        st = rb.groupby("player_id").opp.sum().idxmax()
        act = rb[(rb.player_id == st) & (rb.opp > 0)]
        if len(act) and act.opp.mean() >= 10:
            n += 1
            miss += int(len(act) < tm.week.nunique())
    return n, miss


def sig(ci):
    return ci[0] > 0 or ci[1] < 0


def main():
    d = load()
    a, ndep = build(d)
    r, a = analyse(a)
    a.to_csv(os.path.join(HERE, "job_slope_absences.csv"), index=False)
    nst, nmiss = count_starters(d)
    rng = np.random.default_rng(SEED + 1)
    ymean_ci = np.percentile([a.Y.values[rng.integers(0, len(a), len(a))].mean() for _ in range(B)], [2.5, 97.5])
    # sensitivities
    r_lit, _ = analyse(build(d, drop_departures=False)[0])
    r_tm, _ = analyse(build(d, per="team")[0])
    a_rate, _ = build(d, starter_mode="rate")
    r_rate, _ = analyse(a_rate)
    r_L, _ = analyse(a[a.length >= 3])
    r_first, _ = analyse(a.sort_values("start_week").groupby(["season", "team", "starter"]).head(1))
    # X as opportunities a game instead of points a game
    A = np.column_stack([np.ones(len(a)), a.starter_opp_pg.values])
    bo, seo, _ = ols(A, a.Y.values)
    cio = boot(A, a.Y.values, 1, np.random.default_rng(SEED + 2))

    diff = r["pred15"] - r["pred9"]
    hi_gap = r["ci"][1] * 6
    lo_gap = r["ci"][0] * 6
    ctl_sig = sig(r["ci_ctl"])
    lines = []
    L = lines.append
    L("# Job size vs relief scoring, RB absences 2021-2025 (REG weeks 1-14, nflverse, half-PPR)")
    L("")
    L("**Claim, testable form:** across RB absences, the relief back's half-PPR points a game during the absence (Y) rise with the absent starter's points a game before it (X). A flat 12.1 is wrong if that slope is real and large.")
    L("")
    L(f"**Population (n = {r['n']} absences, {a.starter.nunique()} starters):** starter = RB who led his team-season in carries plus targets over weeks 1-14 and averaged 10+ a game when active ({nst} such starter team-seasons, {nmiss} missed at least one team game). "
      f"Absence = maximal run of 2+ consecutive team games (bye skipped) with zero opportunities, after 2+ games played. Relief = team RB with the most opportunities in the run. "
      f"Y = his points per game played in the run. X = starter's points per game played before it (median {a.pre_games.median():.0f} games). "
      f"{ndep} run dropped because the starter was playing for another team (a departure). Mean absence length {a.length.mean():.1f} games. Rows: job_slope_absences.csv.")
    L("")
    L("| measure | value |")
    L("|---|---|")
    L(f"| Y mean (bootstrap 95%) / median / sd | {r['meanY']:.2f} ({ymean_ci[0]:.1f} to {ymean_ci[1]:.1f}) / {r['medY']:.2f} / {r['sdY']:.2f}; flat sheet rate is {FLAT} |")
    L(f"| X mean | {r['meanX']:.2f} points a game |")
    L(f"| Slope of Y on X (OLS) | {r['slope']:+.3f} per point of X, se {r['se']:.3f}, bootstrap 95% {fmt_ci(r['ci'])} ({B} resamples of absences) |")
    L(f"| Correlation of Y with X | Pearson {r['corr']:+.3f}, Spearman {r['spearman']:+.3f}, R2 {r['r2']:.3f} |")
    for t, n, mx, my, md in r["terc"]:
        L(f"| X tercile {t} (mean X {mx:.1f}) | n={n}, mean Y {my:.2f}, median Y {md:.2f} |")
    L(f"| Subset with relief back's prior ppg known | n={r['nz']}, slope on X alone {r['slope_sub']:+.3f} (se {r['se_sub']:.3f}, 95% {fmt_ci(r['ci_sub'])}) |")
    L(f"| Slope on X controlling for relief back's own prior ppg | {r['slope_ctl']:+.3f} (se {r['se_ctl']:.3f}, 95% {fmt_ci(r['ci_ctl'])}); prior-ppg coefficient {r['zcoef']:+.3f} (se {r['zse']:.3f}, 95% {fmt_ci(r['ci_z'])}); corr(X, prior ppg) {r['corr_xz']:+.2f} |")
    L(f"| Check: X as starter's opportunities a game | slope {bo[1]:+.3f} (se {seo[1]:.3f}, 95% {fmt_ci(cio)}) |")
    L(f"| Check: first absence per starter-season only | n={r_first['n']}, slope {r_first['slope']:+.3f} (se {r_first['se']:.3f}, 95% {fmt_ci(r_first['ci'])}) |")
    L(f"| Check: absences of 3+ games | n={r_L['n']}, slope {r_L['slope']:+.3f} (se {r_L['se']:.3f}, 95% {fmt_ci(r_L['ci'])}) |")
    L(f"| Check: departures kept (literal spec) | n={r_lit['n']}, slope {r_lit['slope']:+.3f} (se {r_lit['se']:.3f}, 95% {fmt_ci(r_lit['ci'])}) |")
    L(f"| Check: Y per team game instead of per game played | n={r_tm['n']}, mean Y {r_tm['meanY']:.2f}, slope {r_tm['slope']:+.3f} (se {r_tm['se']:.3f}, 95% {fmt_ci(r_tm['ci'])}) |")
    L(f"| Check: starter = top RB by opportunities per game (4+ games played, 10+) | n={r_rate['n']}, slope {r_rate['slope']:+.3f} (se {r_rate['se']:.3f}, 95% {fmt_ci(r_rate['ci'])}), mean Y {r_rate['meanY']:.2f} |")
    L("")
    L(f"**Face value (fitted line):** a 15-a-game job (260 points a season) gets {r['pred15']:.2f} and a 9-a-game job (150 points) gets {r['pred9']:.2f}, a gap of {diff:+.2f} points a game. The 95% interval on the slope allows a gap from {lo_gap:+.1f} to {hi_gap:+.1f}.")
    L("")
    lean = "toward" if r["slope"] > 0 else "against"
    s1 = (f"It leans {lean} the claim: relief scoring moved {r['slope']:+.2f} a game per point of starter job (95% {r['ci'][0]:+.2f} to {r['ci'][1]:+.2f}), "
          f"{'which excludes zero.' if sig(r['ci']) else 'which cannot be told apart from zero.'}")
    s2 = (f"The job adds {'something' if ctl_sig else 'nothing detectable'} beyond the man: with the relief back's own prior scoring held fixed the job slope is {r['slope_ctl']:+.2f} "
          f"(95% {r['ci_ctl'][0]:+.2f} to {r['ci_ctl'][1]:+.2f}, n={r['nz']}).")
    flat_in = ymean_ci[0] <= FLAT <= ymean_ci[1]
    s3 = (f"At face value the 260-point job gets {r['pred15']:.1f} and the 150-point job {r['pred9']:.1f} ({diff:+.1f} a game, top of the interval {hi_gap:+.1f}), "
          f"and the mean relief rate here is {r['meanY']:.1f} ({ymean_ci[0]:.1f} to {ymean_ci[1]:.1f}), so "
          f"{'nothing here supports replacing the flat ' + str(FLAT) + ' with a job-size rate' if not (sig(r['ci']) and abs(diff) >= 1.0) else 'job size should be priced'}; "
          f"with n={r['n']} this caps the slope near {r['ci'][1]:+.2f} a point rather than proving it is zero.")
    L(s1 + " " + s2 + " " + s3)
    out = "\n".join(lines).replace(chr(0x2014), ",").replace(chr(0x2013), "-")
    assert chr(0x2014) not in out
    with open(os.path.join(HERE, "job_slope_results.md"), "w") as f:
        f.write(out + "\n")
    print(out)
    print("\nlines:", out.count("\n") + 1)


if __name__ == "__main__":
    main()
