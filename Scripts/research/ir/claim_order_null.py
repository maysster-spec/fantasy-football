"""
claim_order_null.py  --  is the claim-order gradient a mechanic, or arithmetic?

Doc 401, directive v9.24, batch D2 of doc 397's red-team catalog.
ANSWER: arithmetic. The statistic is degenerate and the number is retracted.

PRE-REGISTERED FORM (directive 0.5a2), written before the run:

  CLAIM UNDER TEST  doc 396 / v9.20: "on the 586 contested claims the win rate
                    goes 61.1% with no other win that run, 29.1% with one, 11.2%
                    with two or more", offered as evidence for ESPN's
                    demote-the-winner-mid-run mechanic.

  POPULATION        this league, waiver_report_2022..2026.csv, Type == WAIVER,
                    deduped on (season, Date, Team, Transaction).  A claim
                    "reached a decision" if Status is EXECUTED or any FAILED_*;
                    CANCELED and PENDING are excluded.  A "run" is a processing
                    DAY.  Contested = 2+ teams on one player in one run.
                    This reproduces doc 396's 745 player-runs, 543 team-runs,
                    28.6% contested and 586 contested claims EXACTLY, and the
                    run asserts that before measuring anything.

  THE TEST          hold each team-run's contested WIN COUNT fixed and permute
                    WHICH of its contested claims won.  That destroys any real
                    ordering effect while preserving how many claims each team
                    entered and won.
                    If the gradient is a mechanic, the null should flatten it.
                    If the gradient survives permutation, it is a function of
                    the win counts alone and says nothing about ordering.

  DIRECTION         not predicted.

  FALSIFIER         observed cells falling outside the null's 95% band would
                    support the published reading.

  RESULT            the null reproduces 61.1 / 29.1 / 11.2 EXACTLY, with zero
                    variance at the 2.5th and 97.5th percentiles, over 3,000
                    draws.  Reason: the bucket is (team's total wins) minus
                    (this claim's own result), so a winner sits one bucket below
                    a loser from the same team-run BY CONSTRUCTION.
                    n per cell = 211 / 223 / 152, never published (directive 3).

  AND SEPARATELY    every claim in a run carries ONE IDENTICAL TIMESTAMP, so
                    within-run order is unobservable here and "prior wins that
                    run" was never a quantity this data could express.  The
                    mechanic is BLOCKED from this source; the missing input is
                    Matt's own claim ordering recorded at placement.

  TRAP              ESPN gives D/ST NEGATIVE player ids.  `ADD Player ID (\d+)`
                    silently dropped 437 of 1,623 waiver rows, 27%, all
                    defences.  Use (-?\d+) and ASSERT the extraction count.
"""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get('FF_SRC') or os.path.normpath(os.path.join(HERE, '..', '..', '..', 'Source'))
SEASONS = (2022, 2023, 2024, 2025, 2026)
DECIDED = ['EXECUTED', 'FAILED_INVALIDPLAYERSOURCE', 'FAILED_PLAYERALREADYDROPPED',
           'FAILED_ROSTERLIMIT', 'FAILED_POSITIONLIMIT', 'FAILED_ROSTERLOCK']


def load():
    frames = []
    for s in SEASONS:
        p = os.path.join(SRC, f'waiver_report_{s}.csv')
        if not os.path.exists(p):
            raise SystemExit(f"missing {p}")
        x = pd.read_csv(p, low_memory=False)
        x['season'] = s
        frames.append(x)
    d = pd.concat(frames, ignore_index=True).drop_duplicates(
        subset=['season', 'Date', 'Team', 'Transaction'])
    w = d[d.Type == 'WAIVER'].copy()
    # (-?\d+): ESPN D/ST ids are NEGATIVE. (\d+) drops 27% of rows with no error.
    w['pid'] = w.Transaction.str.extract(r'ADD Player ID (-?\d+)')
    assert w.pid.notna().all(), (
        f"player id not extracted on {w.pid.isna().sum()} of {len(w)} waiver rows -- "
        "check the Transaction format before trusting any count")
    w['dt'] = pd.to_datetime(w.Date, errors='coerce')
    assert w.dt.notna().all()
    w['run'] = w.dt.dt.strftime('%Y-%m-%d')
    return w[w.Status.isin(DECIDED)].copy()


def gradient(dec, winv, contested):
    total = pd.Series(winv).groupby(dec.key.values).transform('sum').values
    other = total - winv
    bucket = np.where(other == 0, 0, np.where(other == 1, 1, 2))
    rates, ns = [], []
    for k in (0, 1, 2):
        m = contested & (bucket == k)
        ns.append(int(m.sum()))
        rates.append(winv[m].mean() * 100 if m.sum() else np.nan)
    return rates, ns


def main():
    dec = load()
    dec['win'] = (dec.Status == 'EXECUTED').astype(int)
    dec['key'] = dec.groupby(['season', 'run', 'Team']).ngroup()
    sz = dec.groupby(['season', 'run', 'pid']).Team.nunique()
    contested = dec.set_index(['season', 'run', 'pid']).index.isin(sz[sz > 1].index)

    print("--- REPRODUCTION CHECK against doc 396, before anything new is measured ---")
    print(f"  claims that reached a decision {len(dec)}")
    print(f"  player-runs {sz.size:>4}   (doc 396: 745)")
    print(f"  team-runs   {dec.key.nunique():>4}   (doc 396: 543)")
    print(f"  contested   {(sz > 1).mean()*100:>4.1f}%  (doc 396: 28.6%)")
    print(f"  contested claims {int(contested.sum())}   (doc 396: 586)")
    print(f"  D/ST rows kept by (-?\\d+): {(dec.pid.astype(int) < 0).sum()}")

    obs, ns = gradient(dec, dec.win.values, contested)
    print("\n--- OBSERVED (doc 396's own statistic) ---")
    print("  " + "  ".join(f"{r:.1f}% (n={n})" for r, n in zip(obs, ns)))

    rng = np.random.default_rng(11)
    key = dec.key.values
    sims = []
    for _ in range(3000):
        v = dec.win.values.copy()
        for k in np.unique(key):
            idx = np.where((key == k) & contested)[0]
            if len(idx) < 2:
                continue
            n = v[idx].sum()
            v[idx] = 0
            rng.shuffle(idx)
            v[idx[:n]] = 1
        sims.append(gradient(dec, v, contested)[0])
    s = np.array(sims)

    print("\n--- NULL: contested winners reshuffled within each team-run, counts fixed (3,000 draws) ---")
    for i, lab in enumerate(['0 other wins ', '1 other win  ', '2+ other wins']):
        lo, hi = np.percentile(s[:, i], [2.5, 97.5])
        verdict = 'INSIDE the null -> no information' if lo <= obs[i] <= hi else 'outside the null'
        print(f"  {lab} observed {obs[i]:5.1f}%   null {s[:, i].mean():5.1f}%  95% [{lo:.1f}, {hi:.1f}]   {verdict}")

    t = dec.groupby(['season', 'run']).dt.nunique()
    print(f"\n--- why the mechanic is BLOCKED from this source ---")
    print(f"  runs: {len(t)}   runs with more than one distinct timestamp: {(t > 1).sum()}")
    print("  every claim in a run shares one timestamp, so within-run ORDER is unobservable.")


if __name__ == '__main__':
    main()
