#!/usr/bin/env python3
r"""
keep_role.py -- doc 294, catalog E6 batch R2c: when the man ahead comes back, does a late pick KEEP the job?

EVENT (doc 244's definition, rebuilt here because doc 244's script was never committed): a team-season where the
player with the most weeks-1-4 usage at a position (RB: carries + targets; WR and TE: targets) later missed one or
more of his team's games from week 5 on AND CAME BACK for the same team. If he never came back the job was vacated,
which is a different event. One event per team-season per position: the first absence.
PLAYED means one or more offensive snaps (nflverse snap counts), not a stat line. WEEKS: every regular-season week by
default, because keeping an NFL job does not stop at our week 14. Doc 244 used weeks 1-14 (its named after-return shares
for Dillon, White, Singletary and Charbonnet match only with the window capped there); --maxwk 14 is that control.
REPLACEMENT, two definitions, both printed, because they answer different questions:
  backup  = the number two by weeks-1-4 usage, the designated backup, whether or not he got the work (the STASH
            question). This is doc 244's definition: its numbers reproduce with it (control below) and do not
            reproduce with the other one.
  work    = the player at that position with the most usage in the missed games (the CLAIM question: the man
            who actually filled in).
GUARD (doc 244): the replacement was on the field in 2+ of weeks 1-4 and his weeks-1-4 usage was under 60% of the
lead man's (stars returning from an early absence otherwise score as takeovers).
BEFORE: his share of the position's team usage in the team's games before the absence.
AFTER: his share in the first four team games from the lead man's return, return game included (1+ required).
RELIEF: his half-PPR points a game in the missed games he played (0 if he played none of them, backup
definition only). PRODUCED: relief >= 11.2 (doc 244's median,
fixed in advance rather than re-fitted on these rows; the median split is printed as a check).
TOOK: he out-used the returning lead man in 2+ of the after games the lead man played.
STARTABLE AFTER: his half-PPR a game in the after games he played >= the position bar (RB 9.92, WR 9.62, TE 8.25).
TIER: NFL draft round from the weekly table (late = round 4+ or undrafted), for the replacement and the lead man.
Writes keep_role_<definition>_<years>.pkl beside this file. --years a-b (default 2015-2025).

RESULT (11 Sept 2026, run_keep_role_20260911.txt, doc 294):
  CONTROL. Doc 244 reproduces only with the designated backup. 2021-2025, weeks 1-14: produced +13.6 pp against
  did not -6.7, p=0.004 (doc 244: +12.4 against -4.1, p=0.006); with the man who got the work, weeks 1-18: +8.5,
  p=0.276. Six seasons doc 244 never saw, 2015-2020: +14.0, p=0.001 (designated backup), +17.1, p<0.001 (work).
  R2c. Backs who produced, 2015-2025: late picks kept +12.1 pp against early picks' +11.6 (work, n=39/11, p=0.94)
  and +9.8 against +11.7 (designated backup, n=24/12, p=0.76); no gap under about 18-19 pp is visible. Inside
  our season (return by week 14) -3.5 (work) and -8.5 (backup), intervals spanning zero: UNRESOLVED.
  Startable in the four games after: 8 of 39 late against 5 of 11 early (all weeks, p=0.13); 5 of 29 against
  4 of 7 when the return came by week 14 (p=0.050).
"""
import argparse
import os
import numpy as np
import pandas as pd
from common import load, HERE, BAR

PRODUCED = 11.2
rng = np.random.default_rng(294)

def boot_ci(x, n=4000):
    x = np.asarray(x, float)
    if len(x) < 3:
        return (np.nan, np.nan)
    m = rng.choice(x, size=(n, len(x)), replace=True).mean(1)
    return tuple(np.percentile(m, [2.5, 97.5]))

def perm_p(a, b, n=10000):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 2 or len(b) < 2:
        return np.nan
    obs = a.mean() - b.mean()
    pool = np.concatenate([a, b])
    cnt = 0
    for _ in range(n):
        rng.shuffle(pool)
        if abs(pool[:len(a)].mean() - pool[len(a):].mean()) >= abs(obs) - 1e-12:
            cnt += 1
    return (cnt + 1) / (n + 1)

def fisher_p(k1, n1, k2, n2):
    """two-sided Fisher exact via the hypergeometric, pure python"""
    from math import comb
    K, N = k1 + k2, n1 + n2
    def pr(k):
        return comb(n1, k) * comb(n2, K - k) / comb(N, K)
    lo, hi = max(0, K - n2), min(n1, K)
    p0 = pr(k1)
    return min(1.0, sum(pr(k) for k in range(lo, hi + 1) if pr(k) <= p0 * (1 + 1e-9)))

def build(w, replacement='work', maxwk=18):
    w = w[w.week <= maxwk].copy()
    w['use'] = np.where(w.position == 'RB', w.carries + w.targets, w.targets)
    on = w[w.offense_snaps > 0]
    games = w.groupby(['season', 'team']).week.apply(lambda s: sorted(set(s))).to_dict()
    out = []
    for (season, team, pos), g in on.groupby(['season', 'team', 'position']):
        wk = games[(season, team)]
        eu = g[g.week <= 4].groupby('key').use.sum()
        if eu.empty or eu.max() <= 0:
            continue
        lead = eu.idxmax()
        lead_weeks = set(g.loc[g.key == lead, 'week'])
        later = [x for x in wk if x >= 5]
        start = next((i for i, x in enumerate(later) if x not in lead_weeks), None)
        if start is None:
            continue
        j = start
        while j < len(later) and later[j] not in lead_weeks:
            j += 1
        if j >= len(later):
            continue                                   # never came back: vacated
        missed, ret = later[start:j], later[j]
        before_wk = [x for x in wk if x < missed[0]]
        after_wk = [x for x in wk if x >= ret][:4]
        ab = g[g.week.isin(missed) & (g.key != lead)]
        au = ab.groupby('key').use.sum()
        worker = au.idxmax() if (len(au) and au.max() > 0) else None
        if replacement == 'backup':
            order = eu.sort_values(ascending=False)
            if len(order) < 2:
                continue
            rep = order.index[1]
        else:
            if worker is None:
                continue
            rep = worker
        r = g[g.key == rep]
        l = g[g.key == lead]
        rep_early_games = int((r.week <= 4).sum())
        rep_early_use = float(r.loc[r.week <= 4, 'use'].sum())
        guard = (rep_early_games >= 2) and (rep_early_use < 0.6 * float(eu.max()))
        team_before = float(g.loc[g.week.isin(before_wk), 'use'].sum())
        team_after = float(g.loc[g.week.isin(after_wk), 'use'].sum())
        if team_before <= 0 or team_after <= 0 or len(after_wk) < 1:
            continue
        before = float(r.loc[r.week.isin(before_wk), 'use'].sum()) / team_before
        after = float(r.loc[r.week.isin(after_wk), 'use'].sum()) / team_after
        relief = r.loc[r.week.isin(missed)]
        aft = r.loc[r.week.isin(after_wk)]
        took_n = 0
        for x in after_wk:
            if x in lead_weeks:
                ru = float(r.loc[r.week == x, 'use'].sum())
                lu = float(l.loc[l.week == x, 'use'].sum())
                took_n += int(ru > lu)
        out.append(dict(
            season=season, team=team, pos=pos, grp='RB' if pos == 'RB' else 'WR/TE',
            lead=l.player.iloc[0], rep=r.player.iloc[0], rep_key=rep,
            rep_tier=r.tier.iloc[0], rep_low=bool(r.low.iloc[0]), lead_tier=l.tier.iloc[0], lead_low=bool(l.low.iloc[0]),
            rep_round=r['round'].iloc[0], rep_age=float(r.age.iloc[0]) if pd.notna(r.age.iloc[0]) else np.nan,
            rep_exp=float(r.years_exp.iloc[0]) if pd.notna(r.years_exp.iloc[0]) else np.nan,
            lead_age=float(l.age.iloc[0]) if pd.notna(l.age.iloc[0]) else np.nan,
            guard=guard, missed=len(missed), first_missed=missed[0], ret=ret, n_after=len(after_wk),
            before=before, after=after, change=after - before,
            relief_g=len(relief), relief_ppg=float(relief.half.mean()) if len(relief) else 0.0,
            after_g=len(aft), after_ppg=float(aft.half.mean()) if len(aft) else np.nan,
            took=took_n >= 2, bar=BAR[pos], got_the_work=(rep == worker)))
    ev = pd.DataFrame(out)
    ev['produced'] = ev.relief_ppg >= PRODUCED
    ev['startable_after'] = (ev.after_g >= 2) & (ev.after_ppg >= ev.bar)
    return ev

def line(label, d):
    if len(d) == 0:
        return f'  {label:<44} n=0'
    lo, hi = boot_ci(d.change * 100)
    return (f'  {label:<44} n={len(d):>3}  change {d.change.mean()*100:+6.1f} pp [{lo:+.1f}, {hi:+.1f}]'
            f'  took {d.took.mean()*100:5.1f}%  startable after {d.startable_after.mean()*100:5.1f}%')

def report(ev, label):
    g = ev[ev.guard]
    print(f'==== replacement = {label} ====')
    print(f'events before the guard: {len(ev)} (RB {int((ev.grp=="RB").sum())}, WR/TE {int((ev.grp=="WR/TE").sum())});'
          f' after: {len(g)} (RB {int((g.grp=="RB").sum())}, WR/TE {int((g.grp=="WR/TE").sum())})')
    for grp in ('RB', 'WR/TE'):
        d = g[g.grp == grp]
        lo, hi = boot_ci(d.change * 100)
        print(f'{grp}: average share change {d.change.mean()*100:+.1f} pp [{lo:+.1f}, {hi:+.1f}], n={len(d)}')
    rb = g[g.grp == 'RB']
    med = rb.relief_ppg.median()
    above, below = rb[rb.relief_ppg > med], rb[rb.relief_ppg <= med]
    print(f'RB median relief ppg {med:.1f}; above median {above.change.mean()*100:+.1f} pp (n={len(above)}),'
          f' at or below {below.change.mean()*100:+.1f} pp (n={len(below)}),'
          f' difference {(above.change.mean()-below.change.mean())*100:+.1f}, p={perm_p(above.change, below.change):.3f}')
    nw = rb[~rb.produced]
    print(f'RB replacements who did not produce: {int((~nw.got_the_work).sum())} of {len(nw)} were not the man who got the most work'
          f' in the missed games ({int((nw.relief_g == 0).sum())} played none of them)')
    p, n_ = rb[rb.produced], rb[~rb.produced]
    print(f'RB at the fixed {PRODUCED}: produced {p.change.mean()*100:+.1f} pp (n={len(p)}), did not {n_.change.mean()*100:+.1f} pp'
          f' (n={len(n_)}), difference {(p.change.mean()-n_.change.mean())*100:+.1f}, p={perm_p(p.change, n_.change):.3f}')
    print()
    for grp in ('RB', 'WR/TE'):
        d = g[g.grp == grp]
        print(f'--- {grp}: replacement pedigree x relief production (produced = {PRODUCED} half-PPR a game or more) ---')
        for prod in (True, False):
            for low in (False, True):
                s = d[(d.produced == prod) & (d.rep_low == low)]
                print(line(f'{"produced" if prod else "did not"} / {"late pick" if low else "rounds 1-3"}', s))
        for prod in (True, False):
            s = d[d.produced == prod]
            e, l = s[~s.rep_low], s[s.rep_low]
            if len(e) >= 2 and len(l) >= 2:
                diff = (l.change.mean() - e.change.mean()) * 100
                sd = np.sqrt(e.change.var(ddof=1) / len(e) + l.change.var(ddof=1) / len(l)) * 100
                lo, hi = diff_ci(l.change * 100, e.change * 100)
                print(f'  {"produced" if prod else "did not"}: late minus early {diff:+.1f} pp [{lo:+.1f}, {hi:+.1f}],'
                      f' p={perm_p(l.change, e.change):.3f}, smallest gap this could see at 80% power about {2.8*sd:.0f} pp;'
                      f' took {int(l.took.sum())}/{len(l)} vs {int(e.took.sum())}/{len(e)} p={fisher_p(int(l.took.sum()), len(l), int(e.took.sum()), len(e)):.3f};'
                      f' startable after {int(l.startable_after.sum())}/{len(l)} vs {int(e.startable_after.sum())}/{len(e)}'
                      f' p={fisher_p(int(l.startable_after.sum()), len(l), int(e.startable_after.sum()), len(e)):.3f}')
        if len(d) > 20:
            def did(x):
                m = x.groupby(['produced', 'rep_low']).change.mean()
                try:
                    return ((m[(True, True)] - m[(False, True)]) - (m[(True, False)] - m[(False, False)])) * 100
                except KeyError:
                    return np.nan
            obs = did(d)
            idx = np.arange(len(d))
            bs = np.array([did(d.iloc[rng.choice(idx, len(idx), replace=True)]) for _ in range(2000)])
            bs = bs[np.isfinite(bs)]
            print(f'  production effect, late picks minus rounds 1-3 (difference in differences): {obs:+.1f} pp'
                  f' [{np.percentile(bs, 2.5):+.1f}, {np.percentile(bs, 97.5):+.1f}]')
        print()
    s = rb[rb.produced]
    print('--- RB, replacement produced: the returning lead man\'s pedigree (the sunk-cost cut) ---')
    for low in (False, True):
        print(line(f'lead man {"late pick" if low else "rounds 1-3"}', s[s.lead_low == low]))
    e, l = s[~s.lead_low], s[s.lead_low]
    if len(e) >= 2 and len(l) >= 2:
        lo, hi = diff_ci(l.change * 100, e.change * 100)
        print(f'  lead late minus lead early {(l.change.mean()-e.change.mean())*100:+.1f} pp [{lo:+.1f}, {hi:+.1f}], p={perm_p(l.change, e.change):.3f}')
    print('--- RB, replacement produced: absence length ---')
    for short in (True, False):
        q = s[(s.missed <= 2) == short]
        for low in (False, True):
            print(line(f'{"1-2 games" if short else "3+ games"} / {"late pick" if low else "rounds 1-3"}', q[q.rep_low == low]))
    print()
    return g

def diff_ci(a, b, n=4000):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3 or len(b) < 3:
        return (np.nan, np.nan)
    ma = rng.choice(a, size=(n, len(a)), replace=True).mean(1)
    mb = rng.choice(b, size=(n, len(b)), replace=True).mean(1)
    return tuple(np.percentile(ma - mb, [2.5, 97.5]))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--years', default='2015-2025')
    ap.add_argument('--names', action='store_true', help='print the named rows for RB replacements who produced')
    ap.add_argument('--maxwk', type=int, default=18, help='last week in the window (doc 244 used 14)')
    a = ap.parse_args()
    y0, y1 = map(int, a.years.split('-'))
    w = load()
    w = w[(w.season >= y0) & (w.season <= y1)]
    print(f'== keep_role.py, seasons {y0}-{y1}, weeks 1-{a.maxwk} ==')
    for label in ('backup', 'work'):
        ev = build(w, label, a.maxwk)
        ev.to_pickle(os.path.join(HERE, f'keep_role_{label}_{y0}_{y1}' + ('' if a.maxwk == 18 else f'_wk{a.maxwk}') + '.pkl'))
        g = report(ev, label)
        if a.names:
            s = g[(g.grp == 'RB') & g.produced]
            cols = ['season', 'team', 'rep', 'rep_tier', 'lead', 'lead_tier', 'missed', 'relief_ppg', 'before', 'after',
                    'change', 'took', 'after_g', 'after_ppg']
            for low in (True, False):
                print(f'--- RB {"late picks" if low else "rounds 1-3"} who produced ({label}), by share change ---')
                with pd.option_context('display.width', 220, 'display.max_rows', 200):
                    print(s[s.rep_low == low].sort_values('change', ascending=False)[cols].round(3).to_string(index=False))
                print()

if __name__ == '__main__':
    main()
