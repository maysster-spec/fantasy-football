"""STEP 4b — WEAKNESS #1. Does the week 1-14 objective pick the same strategy as
championship equity?

Changes vs league.py:
  * random weekly re-pairing  ->  fixed schedule matching the real league's observed
    structure (single round robin over 11 weeks + 3 repeat weeks; verified in 4a:
    every team plays exactly 11 distinct opponents in 14 games, all four seasons).
  * bracket built explicitly, with a 3rd-place game, so places 1-6 all pay.
  * CALIBRATION GATE: before any strategy claim, the sim's weekly score distribution
    is compared to the 412 real games. If the sim's between-team spread is wrong, every
    'how much does drafting matter' number is wrong too.
"""
import numpy as np, pandas as pd, sys, time, os
import sim

PAYOUT = {1: 525, 2: 225, 3: 150, 4: 85, 5: 25, 6: 25}
SLOT = 8


def round_robin(n=12):
    """Circle method -> 11 rounds of 6 pairings covering every pair exactly once."""
    ids = list(range(n))
    rounds = []
    fixed, rot = ids[0], ids[1:]
    for _ in range(n - 1):
        arr = [fixed] + rot
        rounds.append([(arr[i], arr[n - 1 - i]) for i in range(n // 2)])
        rot = rot[1:] + rot[:1]
    return rounds


SCHED = round_robin(12)
SCHED = SCHED + SCHED[:3]           # 14 weeks: 11 distinct + 3 repeats (matches reality)
assert len(SCHED) == 14


def load_universe(u_df):
    res_z = pd.read_csv('resid_z.csv'); av = pd.read_csv('avail_pool.csv')
    u = u_df.copy()
    missing = [k for k in sim.KEEPERS if k not in set(u['full'])]
    assert not missing, f"keeper missing: {missing}"
    mine = u[u['full'] == sim.MY_KEEPER].copy()
    u = u[~u['full'].isin(sim.KEEPERS)].copy().sort_values('ADP').reset_index(drop=True)
    u['avail_rank'] = np.nan
    sk = ~u['pos'].isin(['K', 'D/ST'])
    u.loc[sk, 'avail_rank'] = np.arange(1, sk.sum() + 1); u.loc[~sk, 'avail_rank'] = 140.0
    u['avail_rank'] = u['avail_rank'].astype(float)
    u['tier_rank'] = u.groupby('pos')['TOT'].rank(ascending=False)
    u['band'] = pd.cut(u['tier_rank'], [0, 12, 24, 48, 10_000],
                       labels=['1-12', '13-24', '25-48', '49+']).astype(str)
    mine['avail_rank'] = 0; mine['tier_rank'] = 1; mine['band'] = '13-24'
    pools = {(p, b): g['frac'].values for (p, b), g in av.groupby(['position', 'band'])}
    res_pool = {'z': res_z['z'].values, 'slope': sim.NZ_SLOPE, 'icept': sim.NZ_ICEPT}
    return u.reset_index(drop=True), mine, pools, res_pool


def snake_owner(pick, teams=12):
    rd, idx = divmod(pick - 1, teams)
    return idx if rd % 2 == 0 else teams - 1 - idx


def draft_league(u, res_pool, rng, opening, pi, base, caps, st, names, snyder_q=0.85):
    """12 rosters. Mine at index SLOT-1 uses the same policy sim.run_draft uses."""
    order = sim.draw_order(u, res_pool, rng, snyder_q)
    n = len(u); taken = np.zeros(n, bool); ptr = 0
    rosters = [[] for _ in range(12)]
    counts = np.zeros(len(sim.POSL), int); counts[sim.POSL.index('WR')] += 1
    mypick = {p: i for i, p in enumerate(sim.MY_PICKS)}
    for pick in range(1, sim.N_PICKS + 1):
        who = snake_owner(pick)
        if pick in mypick:
            rd = mypick[pick] + 1
            val = base.copy(); val[taken] = -1e9
            val[counts[pi] >= caps[pi]] = -1e9
            if rd < 14: val[pi == sim.POSL.index('K')] = -1e9
            if rd < 13: val[pi == sim.POSL.index('D/ST')] = -1e9
            need = st[pi] - counts[pi]
            val = val + np.where(need > 0, 18.0, 0.0) - np.where(counts[pi] >= st[pi] + 2, 12.0, 0.0)
            if opening and rd <= len(opening) and opening[rd - 1]:
                w = sim.POSL.index(opening[rd - 1])
                m = (pi == w) & ~taken & (counts[pi] < caps[pi])
                if m.any(): val = np.where(m, val, -1e9)
            j = int(np.argmax(val))
            if val[j] <= -1e8: j = int(np.argmax(np.where(taken, -1e9, base)))
            taken[j] = True; counts[pi[j]] += 1; rosters[who].append(j)
        else:
            while ptr < n and taken[order[ptr]]: ptr += 1
            if ptr < n:
                taken[order[ptr]] = True; rosters[who].append(order[ptr]); ptr += 1
    return rosters


def weekly(roster_idx, u, extra, pools, rng, W=17):
    if extra is not None:
        pos = np.append(extra['pos'].values, u['pos'].values[roster_idx])
        tot = np.append(extra['TOT'].values, u['TOT'].values[roster_idx])
        bye = np.append(extra['bye'].values, u['bye'].values[roster_idx]).astype(int)
        band = np.append(extra['band'].values, u['band'].values[roster_idx])
    else:
        pos = u['pos'].values[roster_idx]; tot = u['TOT'].values[roster_idx]
        bye = u['bye'].values[roster_idx].astype(int); band = u['band'].values[roster_idx]
    n = len(pos); pergame = tot / 17.0
    frac = np.array([rng.choice(pools.get((p, b), pools.get((p, '49+'), np.array([0.8]))))
                     for p, b in zip(pos, band)])
    if sim.USE_BREAKOUT:
        for i in range(n):
            bo = sim.BREAKOUT.get(band[i])
            if bo and pos[i] in ('RB', 'WR', 'TE'):
                ph, mh, mm = bo
                pergame[i] *= (mh if rng.random() < ph else mm)
    avail = np.ones((n, W), bool); wk = np.arange(1, W + 1)
    for i in range(n):
        avail[i, wk == bye[i]] = False
        miss = int(round((1 - frac[i]) * 17))
        if miss > 0: avail[i, rng.choice(W, min(miss, W), replace=False)] = False
    if sim.CVMAP is None: sim.load_cv()
    cvv = np.clip(np.array([sim.CVMAP.get((p, b), sim.CVMAP.get((p, '49+'), 0.8))
                            for p, b in zip(pos, band)]), 0.25, 1.4)
    pts = pergame[:, None] * rng.gamma((1 / cvv ** 2)[:, None], (cvv ** 2)[:, None], size=(n, W)) * avail
    out = np.zeros(W)
    for w in range(W):
        p_w = pts[:, w].copy(); used = np.zeros(n, bool); t = 0.0
        for p, cnt in sim.STARTERS.items():
            e = np.where((pos == p) & ~used & avail[:, w])[0]
            top = e[np.argsort(-p_w[e])][:cnt] if len(e) else np.array([], int)
            t += p_w[top].sum() if len(top) else 0.0
            used[top] = True
        e = np.where(np.isin(pos, sim.FLEX) & ~used & avail[:, w])[0]
        if len(e): t += p_w[e].max()
        out[w] = t
    return out


def season(P, rng):
    """P: 12 x 17 weekly points. Returns (my pf14, my place, my $, champ_idx)."""
    wins = np.zeros(12); pf = P[:, :14].sum(axis=1)
    for w in range(14):
        for a, b in SCHED[w]:
            if P[a, w] > P[b, w]: wins[a] += 1
            else: wins[b] += 1
    seed = np.lexsort((-pf, -wins))
    po = seed[:6]
    a = po[2] if P[po[2], 14] > P[po[5], 14] else po[5]
    b = po[3] if P[po[3], 14] > P[po[4], 14] else po[4]
    la = po[5] if a == po[2] else po[2]
    lb = po[4] if b == po[3] else po[3]
    s1, s2 = po[0], po[1]
    f1 = s1 if P[s1, 15] > P[b, 15] else b
    f2 = s2 if P[s2, 15] > P[a, 15] else a
    l1 = b if f1 == s1 else s1
    l2 = a if f2 == s2 else s2
    champ = f1 if P[f1, 16] > P[f2, 16] else f2
    runner = f2 if champ == f1 else f1
    third = l1 if P[l1, 16] > P[l2, 16] else l2
    fourth = l2 if third == l1 else l1
    fifth, sixth = (la, lb) if pf[la] >= pf[lb] else (lb, la)
    place = {champ: 1, runner: 2, third: 3, fourth: 4, fifth: 5, sixth: 6}
    rest = [t for t in range(12) if t not in place]
    for i, t in enumerate(sorted(rest, key=lambda t: -pf[t])): place[t] = 7 + i
    me = SLOT - 1
    return pf[me], place[me], PAYOUT.get(place[me], 0), champ


OPENINGS = [('RB', 'RB', 'RB'), ('RB', 'RB', 'WR'), ('WR', 'RB', 'WR'), ('WR', 'RB', 'RB'),
            ('WR', 'RB', 'TE'), ('RB', 'WR', 'RB'), ('QB', 'RB', 'RB'), ('RB', 'QB', 'RB'),
            ('WR', 'WR', 'RB'), ('WR', 'QB', 'RB'), ('TE', 'RB', 'RB'), ('WR', 'TE', 'RB'),
            ('WR', 'WR', 'WR')]


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    u_df = pd.read_csv('universe_v3.csv')
    u, mine, pools, res_pool = load_universe(u_df)
    pi, base, caps, st = sim.prep(u); names = u['full'].values
    SEED = 20260907

    # ---------------- CALIBRATION GATE ----------------
    print("=" * 74); print("CALIBRATION GATE — sim weekly scores vs 412 real games"); print("=" * 74)
    real = pd.read_csv('historical_scoreboard_2022_2025.csv')
    rl = pd.concat([real[['Season', 'Week', 'Home Team', 'Home Score']].rename(
                        columns={'Home Team': 't', 'Home Score': 'p'}),
                    real[['Season', 'Week', 'Away Team', 'Away Score']].rename(
                        columns={'Away Team': 't', 'Away Score': 'p'})])
    rl = rl[rl['Week'] <= 14]
    r_mean = rl['p'].mean(); r_within = rl.groupby(['Season', 't'])['p'].std().median()
    r_between = rl.groupby(['Season', 't'])['p'].mean().groupby(level=0).std().mean()
    allw = []
    for it in range(60):
        rng = np.random.default_rng(SEED + it * 7919)
        rost = draft_league(u, res_pool, rng, None, pi, base, caps, st, names)
        P = np.array([weekly(r, u, mine if i == SLOT - 1 else None, pools,
                             np.random.default_rng(SEED + it * 31 + i)) for i, r in enumerate(rost)])
        allw.append(P[:, :14])
    A = np.array(allw)                                   # 60 x 12 x 14
    s_mean = A.mean()
    s_within = np.median(A.std(axis=2))
    s_between = A.mean(axis=2).std(axis=1).mean()
    print(f"{'':22s} {'REAL':>9s} {'SIM':>9s} {'ratio':>7s}")
    print(f"{'weekly mean':22s} {r_mean:9.1f} {s_mean:9.1f} {s_mean/r_mean:7.2f}")
    print(f"{'within-team weekly sd':22s} {r_within:9.1f} {s_within:9.1f} {s_within/r_within:7.2f}")
    print(f"{'between-team sd':22s} {r_between:9.1f} {s_between:9.1f} {s_between/r_between:7.2f}")
    print(f"{'single-week S/N':22s} {r_between/r_within:9.2f} {s_between/s_within:9.2f} "
          f"{(s_between/s_within)/(r_between/r_within):7.2f}")

    # ---------------- TWO OBJECTIVES ----------------
    print("\n" + "=" * 74)
    print(f"STRATEGY UNDER BOTH OBJECTIVES   N={N} paired seasons")
    print("=" * 74)
    res = {o: {'pf': [], 'usd': [], 'title': [], 'po': []} for o in OPENINGS}
    t0 = time.time()
    for it in range(N):
        s = SEED + it * 104729
        for o in OPENINGS:
            rng = np.random.default_rng(s)
            rost = draft_league(u, res_pool, rng, list(o), pi, base, caps, st, names)
            P = np.array([weekly(r, u, mine if i == SLOT - 1 else None, pools,
                                 np.random.default_rng(s + 977 * (i + 1))) for i, r in enumerate(rost)])
            pf, place, usd, champ = season(P, np.random.default_rng(s + 5))
            res[o]['pf'].append(pf); res[o]['usd'].append(usd)
            res[o]['title'].append(int(place == 1)); res[o]['po'].append(int(place <= 6))
        if it and it % 50 == 0:
            print(f"  ... {it}/{N}  ({time.time()-t0:.0f}s)", flush=True)

    rows = []
    for o in OPENINGS:
        d = res[o]
        rows.append(('-'.join(o), np.mean(d['pf']), np.mean(d['usd']),
                     np.std(d['usd'], ddof=1) / np.sqrt(N),
                     np.mean(d['title']), np.mean(d['po'])))
    R = pd.DataFrame(rows, columns=['opening', 'pf14', 'E_dollars', 'se_$', 'P_title', 'P_playoff'])
    R['rank_pf'] = R['pf14'].rank(ascending=False).astype(int)
    R['rank_$'] = R['E_dollars'].rank(ascending=False).astype(int)
    R = R.sort_values('pf14', ascending=False)
    print(R.to_string(index=False, float_format=lambda x: f"{x:9.3f}"))
    from scipy import stats as st2
    print(f"\nSpearman(rank by wk1-14 points, rank by expected dollars) = "
          f"{st2.spearmanr(R['pf14'], R['E_dollars'])[0]:+.3f}")
    print(f"Spearman(rank by wk1-14 points, P(title))                 = "
          f"{st2.spearmanr(R['pf14'], R['P_title'])[0]:+.3f}")
    print(f"top-by-points  : {R.iloc[0]['opening']}")
    print(f"top-by-dollars : {R.sort_values('E_dollars', ascending=False).iloc[0]['opening']}")
    R.to_csv('out_objective_test.csv', index=False)


if __name__ == '__main__' and os.environ.get('RUN4B'):
    main()
