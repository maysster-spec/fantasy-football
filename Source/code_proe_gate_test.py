"""GATE TEST — Pass Rate Over Expected (PROE), proposed by Gemini Pro.

Design corrections applied vs the proposal as written:
  1. CLUSTERED INFERENCE. PROE is constant within a team, so ~210 players carry only ~32
     independent values. An unclustered bootstrap would treat them as 210 and produce a
     CI far too narrow. Every bootstrap here resamples TEAMS, not players.
  2. FORWARD-LOOKING ASSIGNMENT. The predictor for a player's year t+1 output is the
     year-t PROE of the team he plays for in t+1 -- which is what a drafter can know
     before the season. Not the PROE of the team he played for in year t.
  3. CHANGED-SITUATION SUBSAMPLE. Gemini's own rationale is that PROE matters when a
     player's environment changes; prior-year PPG already embeds team pass volume for
     everyone who stayed. That subsample is tested separately, and via an interaction.

PROE: nflfastR play-by-play, mean pass_oe over plays with win probability in [0.2, 0.8]
(situation-neutral). 160 team-seasons 2021-2025, median 710 qualifying plays each.
"""
import pandas as pd, numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression

PFF2NFL = {'ARZ': 'ARI', 'BLT': 'BAL', 'CLV': 'CLE', 'HST': 'HOU', 'LA': 'LA'}
proe = pd.read_csv('proe_team_season.csv')

def load(y):
    d = pd.read_csv(f'{y}_YPRR.csv')
    d = d[d.position.isin(['WR', 'TE', 'HB', 'RB', 'FB'])].copy()
    d['pos'] = d.position.replace({'HB': 'RB', 'FB': 'RB'})
    d['g'] = d.player_game_count.clip(lower=1)
    d['ppg'] = (0.5 * d.receptions + 0.1 * d.yards + 6 * d.touchdowns) / d.g
    d['tpg'] = d.targets / d.g
    d['tm'] = d.team_name.replace(PFF2NFL)
    d['yr'] = y
    return d[['player_id', 'player', 'pos', 'tm', 'routes', 'ppg', 'tpg', 'yr']]

D = {y: load(y) for y in (2023, 2024, 2025)}
P = {y: proe[proe.season == y].set_index('posteam').proe for y in (2023, 2024, 2025)}

def pair(y0, y1, minr=100):
    a = D[y0][D[y0].routes >= minr]
    b = D[y1][D[y1].routes >= minr]
    m = a.merge(b, on='player_id', suffixes=('_0', '_1'))
    m['proe_next_team'] = m.tm_1.map(P[y0])          # correction 2
    m['proe_own_team'] = m.tm_0.map(P[y0])
    m['moved'] = (m.tm_0 != m.tm_1).astype(int)
    return m.dropna(subset=['proe_next_team', 'ppg_1', 'ppg_0', 'tpg_0'])

tr, te = pair(2023, 2024), pair(2024, 2025)
print(f"train {len(tr)} players / {tr.tm_1.nunique()} teams   "
      f"test {len(te)} players / {te.tm_1.nunique()} teams   "
      f"changed team: train {tr.moved.sum()}, test {te.moved.sum()}")

print("\n" + "=" * 74)
print("GATE 1 — STICKINESS")
print("=" * 74)
piv = proe.pivot(index='posteam', columns='season', values='proe')
allp = []
for a, b in [(2021, 2022), (2022, 2023), (2023, 2024), (2024, 2025)]:
    g = piv[[a, b]].dropna(); r = stats.pearsonr(g[a], g[b])
    print(f"  {a}->{b}: r={r[0]:+.3f}  p={r[1]:.1e}  n={len(g)}")
    allp += list(zip(g[a], g[b]))
x, y = zip(*allp); r = stats.pearsonr(x, y)
print(f"  POOLED : r={r[0]:+.3f}  p={r[1]:.1e}  n={len(allp)}      "
      f"[Gemini predicted 0.60]")
print(f"  VERDICT: {'PASS' if r[0] > 0.3 else 'FAIL'} — sticky, but below the predicted 0.60"
      " and decaying year over year.")

def fit(cols, label, train, test, verbose=True):
    def X(d):
        z = d[cols].copy()
        z['is_WR'] = (d.pos_0 == 'WR').astype(int)
        z['is_TE'] = (d.pos_0 == 'TE').astype(int)
        return z
    Xtr, Xte = X(train), X(test)
    ok_tr, ok_te = Xtr.notna().all(axis=1), Xte.notna().all(axis=1)
    M = LinearRegression().fit(Xtr[ok_tr], train.ppg_1[ok_tr])
    pred = M.predict(Xte[ok_te]); yte = train.ppg_1[ok_tr].mean()
    res = ((test.ppg_1[ok_te] - pred) ** 2).sum()
    tot = ((test.ppg_1[ok_te] - yte) ** 2).sum()
    r2 = 1 - res / tot
    if verbose:
        print(f"  {label:52s} OOS R2 = {r2:.4f}  (n={ok_te.sum()})")
    return r2, test.ppg_1[ok_te].values, pred, test.tm_1[ok_te].values

print("\n" + "=" * 74)
print("GATE 2 — OUT-OF-SAMPLE GAIN, bootstrap CLUSTERED BY TEAM")
print("=" * 74)
r2b, yb, pb, tmb = fit(['ppg_0'], 'baseline: prior-year PPG + position', tr, te)
r2p, yp, pp, tmp = fit(['ppg_0', 'proe_next_team'], '+ PROE (next-season team, prior-year value)', tr, te)
print(f"\n  delta OOS R2 = {r2p - r2b:+.5f}     [Gemini predicted +0.012]")

rng = np.random.default_rng(11)
teams = np.unique(tmb); idx_by_team = {t: np.where(tmb == t)[0] for t in teams}
boot = []
for _ in range(4000):
    pick = rng.choice(teams, len(teams), replace=True)
    ix = np.concatenate([idx_by_team[t] for t in pick])
    tot = ((yb[ix] - yb.mean()) ** 2).sum()
    boot.append((((yb[ix] - pb[ix]) ** 2).sum() - ((yp[ix] - pp[ix]) ** 2).sum()) / tot)
lo, hi = np.percentile(boot, [2.5, 97.5])
print(f"  team-clustered 95% CI on the delta: [{lo:+.5f}, {hi:+.5f}]")
print(f"  VERDICT: {'PASS' if lo > 0 else 'FAIL — interval contains zero'}")
u_lo, u_hi = np.percentile(
    [(((yb[i] - pb[i]) ** 2).sum() - ((yp[i] - pp[i]) ** 2).sum())
     / ((yb[i] - yb.mean()) ** 2).sum()
     for i in (rng.integers(0, len(yb), len(yb)) for _ in range(2000))], [2.5, 97.5])
print(f"  (unclustered CI would have been [{u_lo:+.5f}, {u_hi:+.5f}] — "
      f"{'narrower, i.e. the correction mattered' if (hi-lo) > (u_hi-u_lo) else 'similar'})")

print("\n" + "=" * 74)
print("GATE 3 — SURVIVES VOLUME CONTROL")
print("=" * 74)
r2v, yv, pv, tmv = fit(['ppg_0', 'tpg_0'], 'prior PPG + targets/game', tr, te)
r2vp, yvp, pvp, _ = fit(['ppg_0', 'tpg_0', 'proe_next_team'], 'prior PPG + targets/game + PROE', tr, te)
print(f"\n  delta after volume control = {r2vp - r2v:+.5f}")
s = te.dropna(subset=['ppg_1', 'ppg_0', 'tpg_0', 'proe_next_team'])
base = LinearRegression().fit(s[['ppg_0', 'tpg_0']], s.ppg_1)
ry = s.ppg_1 - base.predict(s[['ppg_0', 'tpg_0']])
rx = s.proe_next_team - LinearRegression().fit(
    s[['ppg_0', 'tpg_0']], s.proe_next_team).predict(s[['ppg_0', 'tpg_0']])
pc = stats.pearsonr(rx, ry)
print(f"  partial r(PROE, next-year PPG | prior PPG, targets/g) = {pc[0]:+.3f}  p={pc[1]:.3g}")
print(f"  corr(PROE, targets/game) = {stats.pearsonr(s.proe_next_team, s.tpg_0)[0]:+.3f}"
      f"     [Gemini predicted 0.18]")
print(f"  raw corr(PROE_t, PPG_t+1) = {stats.pearsonr(s.proe_next_team, s.ppg_1)[0]:+.3f}")

print("\n" + "=" * 74)
print("THE CHANGED-SITUATION TEST — Gemini's actual argument, operationalised")
print("=" * 74)
for lab, sub_tr, sub_te in [('stayed put', tr[tr.moved == 0], te[te.moved == 0]),
                            ('changed team', tr[tr.moved == 1], te[te.moved == 1])]:
    if len(sub_te) < 15: 
        print(f"  {lab}: n={len(sub_te)} too small"); continue
    a, *_ = fit(['ppg_0'], f'{lab}: baseline', sub_tr, sub_te, verbose=False)
    b, *_ = fit(['ppg_0', 'proe_next_team'], f'{lab}: + PROE', sub_tr, sub_te, verbose=False)
    print(f"  {lab:14s} n_test={len(sub_te):3d}  baseline {a:.4f} -> +PROE {b:.4f}"
          f"   delta {b-a:+.4f}")
