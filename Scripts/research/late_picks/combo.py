#!/usr/bin/env python3
r"""
combo.py -- doc 293, batch R1 part 3: do the signals that held inside low pedigree in part B stack, and do they hold
on rows they were not chosen on?

CHOSEN ON part B's low-pedigree rows (so part B is in-sample): (1) snap share over the last two games above his
position's median; (2) points per snap this season above his position's median (part B only; part A has no such
column, so part A uses the two signals it carries); (3) special-teams share at or below his position's median.
CHECKED ON: part B split by era (2015-2019 against 2020-2025), and part A (absence openings, a different event)
with the two signals it carries (1 and 3). Count of signals -> rate, within low pedigree, then high for contrast.
"""
import os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))   # outputs and common.py live beside this file
import pandas as pd
from scipy.stats import fisher_exact

def count_table(d, cols, label):
    d = d.copy()
    for c, direction in cols:
        med = d.groupby('pos')[c].transform('median')
        d[c + '_ok'] = (d[c] > med) if direction == 'high' else (d[c] <= med)
    d['n_ok'] = sum(d[c + '_ok'].astype(int) for c, _ in cols)
    print(f'\n{label}')
    for grp, name in ((d[d.low], 'low pedigree'), (d[~d.low], 'high pedigree')):
        t = grp.groupby('n_ok').hit.agg(['size', 'sum', 'mean'])
        cells = ' | '.join(f'{int(k)} signals: {int(r["sum"])}/{int(r["size"])} = {r["mean"]:.3f}' for k, r in t.iterrows())
        top, rest = grp[grp.n_ok == len(cols)].hit, grp[grp.n_ok < len(cols)].hit
        p = fisher_exact([[top.sum(), len(top) - top.sum()], [rest.sum(), len(rest) - rest.sum()]])[1] if len(top) and len(rest) else np.nan
        print(f'  {name:<14} {cells}   (all vs fewer p={p:.4f})')
    return d

B = pd.read_pickle(os.path.join(HERE, 'flips.pkl'))
A = pd.read_pickle(os.path.join(HERE, 'openings.pkl'))
colsB = [('share_last2', 'high'), ('pps', 'high'), ('st_share', 'low')]
count_table(B, colsB, 'PART B, all seasons (in-sample for low pedigree)')
count_table(B[B.season <= 2019], colsB, 'PART B, 2015-2019')
count_table(B[B.season >= 2020], colsB, 'PART B, 2020-2025')
count_table(A, [('share_last2', 'high'), ('st_share', 'low')], 'PART A, absence openings (not chosen on), two signals')
print('\nBY POSITION, part B, low pedigree, all three signals vs fewer:')
Bc = B.copy()
for c, direction in colsB:
    med = Bc.groupby('pos')[c].transform('median')
    Bc[c + '_ok'] = (Bc[c] > med) if direction == 'high' else (Bc[c] <= med)
Bc['n_ok'] = sum(Bc[c + '_ok'].astype(int) for c, _ in colsB)
for pos in ('RB', 'WR', 'TE'):
    g = Bc[(Bc.pos == pos) & Bc.low]
    top, rest = g[g.n_ok == 3].hit, g[g.n_ok < 3].hit
    print(f'  {pos}: all three {int(top.sum())}/{len(top)} = {top.mean():.3f} | fewer {int(rest.sum())}/{len(rest)} = {rest.mean():.3f}')
lowtop = Bc[Bc.low & (Bc.n_ok == 3) & Bc.hit].sort_values(['season', 'week'])
print(f'\nLOW-PEDIGREE ROTATION BACKUPS WITH ALL THREE WHO ROSE ({len(lowtop)}):')
print(lowtop[['season', 'week', 'team', 'pos', 'player', 'tier', 'years_exp', 'share_last2', 'pps', 'st_share']].round(3).to_string(index=False))

# ---- the second outcome: TOOK THE ROLE (out-snapped the leader in 2 of the next 4 games he was active), low against
# ---- high at each signal count, and the era split. The signals were chosen on 'rose', so this is a second outcome.
C = B.copy()
for c, direction in colsB:
    med = C.groupby('pos')[c].transform('median')
    C[c + '_ok'] = (C[c] > med) if direction == 'high' else (C[c] <= med)
C['n_ok'] = sum(C[c + '_ok'].astype(int) for c, _ in colsB)
for out, lab in (('took', 'TOOK THE ROLE'), ('hit', 'ROSE')):
    print(f'\n{lab}: low against high pedigree at each signal count (part B, clean rows)')
    for k, name in ((3, 'all three'), (2, 'two'), (1, 'one'), (0, 'none')):
        lo, hi = C[C.low & (C.n_ok == k)][out], C[~C.low & (C.n_ok == k)][out]
        p = fisher_exact([[lo.sum(), len(lo) - lo.sum()], [hi.sum(), len(hi) - hi.sum()]])[1]
        print(f'  {name:<9} low {int(lo.sum())}/{len(lo)} = {lo.mean():.3f} | high {int(hi.sum())}/{len(hi)} = {hi.mean():.3f} | p={p:.3f}')
    lo, hi = C[C.low & (C.n_ok <= 1)][out], C[~C.low & (C.n_ok <= 1)][out]
    p = fisher_exact([[lo.sum(), len(lo) - lo.sum()], [hi.sum(), len(hi) - hi.sum()]])[1]
    print(f'  0-1       low {int(lo.sum())}/{len(lo)} = {lo.mean():.3f} | high {int(hi.sum())}/{len(hi)} = {hi.mean():.3f} | p={p:.4f}')
for era, g in (('2015-2019', C[C.season <= 2019]), ('2020-2025', C[C.season >= 2020])):
    lo = g[g.low]
    t3, rest = lo[lo.n_ok == 3].took, lo[lo.n_ok < 3].took
    p = fisher_exact([[t3.sum(), len(t3) - t3.sum()], [rest.sum(), len(rest) - rest.sum()]])[1]
    print(f'  took the role, low pedigree, {era}: all three {int(t3.sum())}/{len(t3)} = {t3.mean():.3f} vs fewer {int(rest.sum())}/{len(rest)} = {rest.mean():.3f}, p={p:.4f}')
print('\nposition medians the three signals use (rotation backups):')
print(C.groupby('pos')[['share_last2', 'pps', 'st_share']].median().round(3).to_string())
