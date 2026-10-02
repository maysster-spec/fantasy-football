#!/usr/bin/env python3
"""Same-team WR1/WR2 weekly points vs a cross-team control (half-PPR, REG weeks 1-14, 2021-2025).

Run: python3 wr_pair.py   (cache dir from env FF_CACHE; pandas and numpy only)

Control design:
  (a)/(b) per season-week, the WR2s of the qualifying same-team pairs are randomly re-dealt among
  the WR1s of OTHER teams (uniform random derangement). Every control draw therefore has exactly the
  same WR1 values and the same WR2 values as the same-team sample; only who is paired with whom changes.
  Median per-pair r: each WR1 is given a random WR2 from another team in the same season (fixed
  partner all season), correlated over the weeks both played (needs >= MIN_JOINT joint weeks).
Intervals: bootstrap over pairs (resampling season-team pairs) of the same-team statistic, with the
control held at its mean over draws. The draw-to-draw sd of the control is printed as well.
"""
import os
import numpy as np
import pandas as pd

CACHE = os.environ.get("FF_CACHE", os.path.join(os.path.dirname(os.path.abspath(__file__)), '_nflverse_cache'))
SEASONS = range(2021, 2026)
WEEKS = 14
MIN_GAMES = 8        # each receiver must have a row in at least this many of weeks 1-14
MIN_JOINT = 6        # joint weeks needed for a per-pair correlation
THRESH = 30.0        # pair sum at or above this counts as an upside week
MIN_PPG = 10.0       # starter-quality filter for (c)
N_DRAWS = 2000
N_BOOT = 1000
SEED = 20260930

COLS = ["season", "season_type", "week", "player_id", "player_display_name", "position", "team",
        "targets", "receptions", "receiving_yards", "receiving_tds", "rushing_yards", "rushing_tds",
        "rushing_fumbles_lost", "receiving_fumbles_lost", "sack_fumbles_lost"]


def load():
    frames = []
    for s in SEASONS:
        d = pd.read_csv(os.path.join(CACHE, "stats_player_week_%d.csv" % s), usecols=COLS)
        frames.append(d)
    d = pd.concat(frames, ignore_index=True)
    d = d[(d.season_type == "REG") & d.week.between(1, WEEKS) & (d.position == "WR")].copy()
    num = [c for c in COLS if c not in ("season_type", "player_id", "player_display_name", "position", "team")]
    d[num] = d[num].fillna(0)
    d["pts"] = (0.1 * (d.rushing_yards + d.receiving_yards)
                + 6.0 * (d.rushing_tds + d.receiving_tds)
                + 0.5 * d.receptions
                - 2.0 * (d.rushing_fumbles_lost + d.receiving_fumbles_lost + d.sack_fumbles_lost))
    return d


def build_pairs(d):
    """One row per (season, team): top two WRs by total targets in weeks 1-14 (a player-team stint)."""
    st = (d.groupby(["season", "team", "player_id"])
            .agg(targets=("targets", "sum"), games=("week", "count"), ppg=("pts", "mean"))
            .reset_index())
    st = st.sort_values(["season", "team", "targets", "player_id"], ascending=[True, True, False, True])
    st["rk"] = st.groupby(["season", "team"]).cumcount()
    top = st[st.rk < 2]
    w1 = top[top.rk == 0].set_index(["season", "team"])
    w2 = top[top.rk == 1].set_index(["season", "team"])
    pr = w1.join(w2, lsuffix="1", rsuffix="2", how="inner").reset_index()
    n_all = len(pr)
    pr = pr[(pr.games1 >= MIN_GAMES) & (pr.games2 >= MIN_GAMES)].reset_index(drop=True)
    pr["pair"] = np.arange(len(pr))
    return pr, n_all


def matrices(d, pr):
    """P x WEEKS matrices of weekly points for WR1 and WR2 of each pair (NaN = no row that week)."""
    wk = d.set_index(["season", "team", "player_id", "week"])["pts"]
    P = len(pr)
    X = np.full((P, WEEKS), np.nan)
    Y = np.full((P, WEEKS), np.nan)
    for i, r in enumerate(pr.itertuples(index=False)):
        for w in range(1, WEEKS + 1):
            a = wk.get((r.season, r.team, r.player_id1, w))
            b = wk.get((r.season, r.team, r.player_id2, w))
            if a is not None:
                X[i, w - 1] = a
            if b is not None:
                Y[i, w - 1] = b
    return X, Y


class Sample:
    """Pair-weeks (both receivers have a row) for a set of pairs, sorted by season-week group."""

    def __init__(self, pr, X, Y, sel):
        self.pr = pr[sel].reset_index(drop=True)
        self.X, self.Y = X[sel], Y[sel]
        P = len(self.pr)
        m = ~np.isnan(self.X) & ~np.isnan(self.Y)
        pi, wi = np.nonzero(m)
        seas = self.pr.season.values[pi]
        grp = seas * 100 + (wi + 1)
        # drop season-weeks with fewer than 2 qualifying pairs (a cross-team match is impossible)
        u, cnt = np.unique(grp, return_counts=True)
        keep = np.isin(grp, u[cnt >= 2])
        self.n_dropped_groups = int((cnt < 2).sum())
        self.X, self.Y = self.X.copy(), self.Y.copy()
        self.X[pi[~keep], wi[~keep]] = np.nan
        self.Y[pi[~keep], wi[~keep]] = np.nan
        pi, wi, grp = pi[keep], wi[keep], grp[keep]
        o = np.lexsort((pi, grp))
        self.pi, self.wi, self.grp = pi[o], wi[o], grp[o]
        self.x = self.X[self.pi, self.wi]
        self.y = self.Y[self.pi, self.wi]
        # within-pair (pair means over joint weeks removed)
        cnt_p = np.bincount(self.pi, minlength=P)
        mx = np.bincount(self.pi, self.x, minlength=P) / np.maximum(cnt_p, 1)
        my = np.bincount(self.pi, self.y, minlength=P) / np.maximum(cnt_p, 1)
        self.xd = self.x - mx[self.pi]
        self.yd = self.y - my[self.pi]
        bounds = np.flatnonzero(np.diff(self.grp)) + 1
        starts = np.r_[0, bounds]
        ends = np.r_[bounds, len(self.grp)]
        self.groups = list(zip(starts, ends))
        self.n = len(self.x)
        self.P = P
        self.used_pairs = len(np.unique(self.pi))

    def stats(self, x, y, xd, yd):
        s = x + y
        return dict(r=np.corrcoef(x, y)[0, 1], rw=np.corrcoef(xd, yd)[0, 1],
                    share=float(np.mean(s >= THRESH)), sd=float(np.std(s, ddof=1)))

    def same(self):
        return self.stats(self.x, self.y, self.xd, self.yd)

    def control_draw(self, rng):
        perm = np.empty(self.n, dtype=int)
        for s, e in self.groups:
            m = e - s
            base = np.arange(s, e)
            while True:
                p = rng.permutation(m)
                if not np.any(p == np.arange(m)):
                    break
            perm[s:e] = base[p]
        return self.stats(self.x, self.y[perm], self.xd, self.yd[perm])


def masked_corr(X, Y, min_n):
    m = ~np.isnan(X) & ~np.isnan(Y)
    n = m.sum(1)
    nn = np.maximum(n, 1)
    mx = np.where(m, X, 0).sum(1) / nn
    my = np.where(m, Y, 0).sum(1) / nn
    dx = np.where(m, X - mx[:, None], 0)
    dy = np.where(m, Y - my[:, None], 0)
    cov = (dx * dy).sum(1)
    vx = (dx ** 2).sum(1)
    vy = (dy ** 2).sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        r = cov / np.sqrt(vx * vy)
    r[(n < min_n) | (vx == 0) | (vy == 0)] = np.nan
    return r


def pair_median_control(sm, rng):
    """Median per-pair r with each WR1 matched to a fixed WR2 from another team in the same season."""
    seas = sm.pr.season.values
    perm = np.arange(sm.P)
    for s in np.unique(seas):
        idx = np.flatnonzero(seas == s)
        if len(idx) < 2:
            continue
        while True:
            p = rng.permutation(len(idx))
            if not np.any(p == np.arange(len(idx))):
                break
        perm[idx] = idx[p]
    r = masked_corr(sm.X, sm.Y[perm], MIN_JOINT)
    return float(np.nanmedian(r)), int(np.sum(~np.isnan(r)))


def run(name, pr, X, Y, sel, rng):
    sm = Sample(pr, X, Y, sel)
    same = sm.same()
    draws = [sm.control_draw(rng) for _ in range(N_DRAWS)]
    ctrl = {k: float(np.mean([dd[k] for dd in draws])) for k in same}
    ctrl_sd = {k: float(np.std([dd[k] for dd in draws], ddof=1)) for k in same}
    # median per-pair r
    r_same = masked_corr(sm.X, sm.Y, MIN_JOINT)
    med_same = float(np.nanmedian(r_same))
    n_med = int(np.sum(~np.isnan(r_same)))
    med_ctrl_draws = [pair_median_control(sm, rng)[0] for _ in range(N_DRAWS)]
    med_ctrl = float(np.mean(med_ctrl_draws))
    med_ctrl_sd = float(np.std(med_ctrl_draws, ddof=1))
    # bootstrap over pairs of the same-team statistic, control held at its mean
    pair_slices = {}
    for p in range(sm.P):
        pair_slices[p] = np.flatnonzero(sm.pi == p)
    boots = {k: [] for k in same}
    boots["med"] = []
    live = [p for p in range(sm.P) if len(pair_slices[p]) > 0]
    for _ in range(N_BOOT):
        pick = rng.choice(live, size=len(live), replace=True)
        ix = np.concatenate([pair_slices[p] for p in pick])
        st = sm.stats(sm.x[ix], sm.y[ix], sm.xd[ix], sm.yd[ix])
        for k in same:
            boots[k].append(st[k])
        boots["med"].append(float(np.nanmedian(r_same[pick])))
    ci = {k: np.percentile(np.array(v) - (med_ctrl if k == "med" else ctrl[k]), [2.5, 97.5]) for k, v in boots.items()}
    cnt_p = np.bincount(sm.pi, minlength=sm.P)
    lvl = np.corrcoef(np.bincount(sm.pi, sm.x, minlength=sm.P)[cnt_p > 0] / cnt_p[cnt_p > 0],
                      np.bincount(sm.pi, sm.y, minlength=sm.P)[cnt_p > 0] / cnt_p[cnt_p > 0])[0, 1]
    res = dict(lvl=lvl, name=name, pairs=sm.used_pairs, weeks=sm.n, dropped=sm.n_dropped_groups,
               same=same, ctrl=ctrl, ctrl_sd=ctrl_sd, ci=ci,
               med_same=med_same, med_ctrl=med_ctrl, med_ctrl_sd=med_ctrl_sd, n_med=n_med)
    return res


def show(res):
    s, c, sd, ci = res["same"], res["ctrl"], res["ctrl_sd"], res["ci"]
    print("== %s: %d pairs, %d pair-weeks (season-weeks with <2 pairs dropped: %d)" %
          (res["name"], res["pairs"], res["weeks"], res["dropped"]))
    def line(label, a, b, sdv, k, fmt="%.3f"):
        lo, hi = ci[k]
        print(("  %-34s same " + fmt + "  control " + fmt + " (draw sd " + fmt + ")  diff %+.3f  95%% CI [%+.3f, %+.3f]")
              % (label, a, b, sdv, a - b, lo, hi))
    print("  correlation across pairs of the two receivers' average points (level, not weekly): %+.3f" % res["lvl"])
    line("pooled r", s["r"], c["r"], sd["r"], "r")
    line("within-pair pooled r", s["rw"], c["rw"], sd["rw"], "rw")
    line("median per-pair r (n=%d pairs)" % res["n_med"], res["med_same"], res["med_ctrl"], res["med_ctrl_sd"], "med")
    line("share of weeks sum >= %d" % THRESH, s["share"], c["share"], sd["share"], "share")
    line("sd of pair sum (pts)", s["sd"], c["sd"], sd["sd"], "sd", fmt="%.2f")


def main():
    rng = np.random.default_rng(SEED)
    d = load()
    pr, n_all = build_pairs(d)
    print("cache:", CACHE)
    print("team-seasons with two WRs: %d; qualifying (both >= %d games in wk 1-%d): %d" %
          (n_all, MIN_GAMES, WEEKS, len(pr)))
    X, Y = matrices(d, pr)
    allsel = np.ones(len(pr), dtype=bool)
    starters = ((pr.ppg1 >= MIN_PPG) & (pr.ppg2 >= MIN_PPG)).values
    show(run("(a,b) all qualifying pairs", pr, X, Y, allsel, rng))
    show(run("(c) both >= %d pts/game" % MIN_PPG, pr, X, Y, starters, rng))
    print("per-season qualifying pairs:", pr.groupby("season").size().to_dict(),
          "| starter-level:", pr[starters].groupby("season").size().to_dict())


if __name__ == "__main__":
    main()
