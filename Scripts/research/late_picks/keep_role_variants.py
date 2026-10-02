#!/usr/bin/env python3
r"""
keep_role_variants.py -- doc 294 section 1: which reading of doc 244 reproduces its numbers (2021-2025, RB and WR/TE).
Doc 244 never committed its script. This tries the choices its text leaves open: PLAYED by snaps or by touches; the
return game inside the after window or not; weeks 1-17 or 1-18; receivers pooled or by position; and, in the second
block, the replacement as the designated number two by weeks 1-4 usage rather than the man who got the work.
Its target line prints first. keep_role.py --maxwk 14 then pins the week-14 window from doc 244's named rows.
RESULT (11 Sept 2026): with the man who got the work, none of 32 variants reproduces (non-producers +4.1 to +7.8,
differences +6.4 to +12.9, p 0.10 to 0.37); with the designated backup all 16 do (non-producers -5.0 to -7.2,
differences +16.5 to +22.4, p 0.001 to 0.013).
"""
import itertools
import numpy as np, pandas as pd
from common import load, BAR
rng = np.random.default_rng(1)

def perm_p(a, b, n=4000):
    a, b = np.asarray(a, float), np.asarray(b, float)
    obs = a.mean() - b.mean(); pool = np.concatenate([a, b]); c = 0
    for _ in range(n):
        rng.shuffle(pool)
        c += abs(pool[:len(a)].mean() - pool[len(a):].mean()) >= abs(obs) - 1e-12
    return (c + 1) / (n + 1)

W = load()
W = W[(W.season >= 2021) & (W.season <= 2025)].copy()
W['use'] = np.where(W.position == 'RB', W.carries + W.targets, W.targets)

def build(presence='snaps', after_incl=True, before='all', maxwk=18, pooled=False):
    w = W[W.week <= maxwk].copy()
    w['grp'] = np.where(w.position == 'RB', 'RB', 'WR/TE' if pooled else w.position)
    on = w[w.offense_snaps > 0] if presence == 'snaps' else w[w.use > 0]
    games = w.groupby(['season', 'team']).week.apply(lambda s: sorted(set(s))).to_dict()
    out = []
    for (season, team, grp), g in on.groupby(['season', 'team', 'grp']):
        wk = games[(season, team)]
        eu = g[g.week <= 4].groupby('key').use.sum()
        if eu.empty or eu.max() <= 0: continue
        lead = eu.idxmax(); lw = set(g.loc[g.key == lead, 'week'])
        later = [x for x in wk if x >= 5]
        st = next((i for i, x in enumerate(later) if x not in lw), None)
        if st is None: continue
        j = st
        while j < len(later) and later[j] not in lw: j += 1
        if j >= len(later): continue
        missed, ret = later[st:j], later[j]
        bw = [x for x in wk if x < missed[0]] if before == 'all' else [x for x in wk if x <= 4]
        aw = ([x for x in wk if x >= ret] if after_incl else [x for x in wk if x > ret])[:4]
        ab = g[g.week.isin(missed) & (g.key != lead)]
        if ab.empty: continue
        au = ab.groupby('key').use.sum()
        if au.max() <= 0: continue
        rep = au.idxmax(); r = g[g.key == rep]
        guard = (int((r.week <= 4).sum()) >= 2) and (float(r.loc[r.week <= 4, 'use'].sum()) < 0.6 * float(eu.max()))
        tb = float(g.loc[g.week.isin(bw), 'use'].sum()); ta = float(g.loc[g.week.isin(aw), 'use'].sum())
        if tb <= 0 or ta <= 0 or len(aw) < 1: continue
        rel = r.loc[r.week.isin(missed)]
        out.append(dict(grp='RB' if grp == 'RB' else 'WR/TE', guard=guard,
                        change=float(r.loc[r.week.isin(aw), 'use'].sum()) / ta - float(r.loc[r.week.isin(bw), 'use'].sum()) / tb,
                        relief=float(rel.half.mean()) if len(rel) else np.nan, low=bool(r.low.iloc[0])))
    return pd.DataFrame(out)

print('target (doc 244): RB 40, WR/TE 48, RB avg +4.2, WR/TE -0.9, median 11.2, above +12.4, below -4.1, diff +16.6 p=0.006')
for presence, after_incl, before, maxwk, pooled in itertools.product(['snaps', 'use'], [True, False], ['all', 'early'], [18, 17], [False, True]):
    ev = build(presence, after_incl, before, maxwk, pooled)
    g = ev[ev.guard]; rb = g[g.grp == 'RB']; wr = g[g.grp == 'WR/TE']
    med = rb.relief.median(); a, b = rb[rb.relief > med], rb[rb.relief <= med]
    print(f'{presence:5} after_incl={after_incl!s:5} before={before:5} maxwk={maxwk} pooled={pooled!s:5} | RB {len(rb):>2} WR/TE {len(wr):>3} | '
          f'RB avg {rb.change.mean()*100:+5.1f} WR/TE {wr.change.mean()*100:+5.1f} | med {med:4.1f} above {a.change.mean()*100:+5.1f} below {b.change.mean()*100:+5.1f} '
          f'diff {(a.change.mean()-b.change.mean())*100:+5.1f} p={perm_p(a.change, b.change):.3f}')

print()
print('variant G: the replacement is the number two by weeks 1-4 usage (the designated backup), not the man who got the absence snaps')
def build_g(presence='snaps', after_incl=True, maxwk=18, need_relief=True):
    w = W[W.week <= maxwk].copy()
    w['grp'] = np.where(w.position == 'RB', 'RB', w.position)
    on = w[w.offense_snaps > 0] if presence == 'snaps' else w[w.use > 0]
    games = w.groupby(['season', 'team']).week.apply(lambda s: sorted(set(s))).to_dict()
    out = []
    for (season, team, grp), g in on.groupby(['season', 'team', 'grp']):
        wk = games[(season, team)]
        eu = g[g.week <= 4].groupby('key').use.sum().sort_values(ascending=False)
        if len(eu) < 2 or eu.iloc[0] <= 0: continue
        lead, rep = eu.index[0], eu.index[1]
        lw = set(g.loc[g.key == lead, 'week'])
        later = [x for x in wk if x >= 5]
        st = next((i for i, x in enumerate(later) if x not in lw), None)
        if st is None: continue
        j = st
        while j < len(later) and later[j] not in lw: j += 1
        if j >= len(later): continue
        missed, ret = later[st:j], later[j]
        bw = [x for x in wk if x < missed[0]]
        aw = ([x for x in wk if x >= ret] if after_incl else [x for x in wk if x > ret])[:4]
        r = g[g.key == rep]
        rel = r.loc[r.week.isin(missed)]
        if need_relief and len(rel) == 0: continue
        guard = (int((r.week <= 4).sum()) >= 2) and (float(eu.iloc[1]) < 0.6 * float(eu.iloc[0]))
        tb = float(g.loc[g.week.isin(bw), 'use'].sum()); ta = float(g.loc[g.week.isin(aw), 'use'].sum())
        if tb <= 0 or ta <= 0: continue
        out.append(dict(grp='RB' if grp == 'RB' else 'WR/TE', guard=guard,
                        change=float(r.loc[r.week.isin(aw), 'use'].sum()) / ta - float(r.loc[r.week.isin(bw), 'use'].sum()) / tb,
                        relief=float(rel.half.mean()) if len(rel) else 0.0))
    return pd.DataFrame(out)
for presence, after_incl, maxwk, need in itertools.product(['snaps', 'use'], [True, False], [18, 17], [True, False]):
    ev = build_g(presence, after_incl, maxwk, need)
    g = ev[ev.guard]; rb = g[g.grp == 'RB']; wr = g[g.grp == 'WR/TE']
    med = rb.relief.median(); a, b = rb[rb.relief > med], rb[rb.relief <= med]
    print(f'{presence:5} after_incl={after_incl!s:5} maxwk={maxwk} need_relief={need!s:5} | RB {len(rb):>2} WR/TE {len(wr):>3} | '
          f'RB avg {rb.change.mean()*100:+5.1f} WR/TE {wr.change.mean()*100:+5.1f} | med {med:4.1f} above {a.change.mean()*100:+5.1f} below {b.change.mean()*100:+5.1f} '
          f'diff {(a.change.mean()-b.change.mean())*100:+5.1f} p={perm_p(a.change, b.change):.3f}')
