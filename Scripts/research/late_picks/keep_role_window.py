#!/usr/bin/env python3
r"""
keep_role_window.py -- doc 294 section 2 and 4: the R2c pedigree gap and the returning starter's pedigree, split by
WHEN the return came (by week 14, our regular season, against week 15 on), for backs who produced (11.2+ in relief).
Reads keep_role_<definition>_2015_2025.pkl (run keep_role.py --years 2015-2025 first) and the _wk14 files
(keep_role.py --years 2015-2025 --maxwk 14).
RESULT (11 Sept 2026, doc 294): the replacement's pedigree gap moves with the window (all weeks +0.6 and -1.9;
return by week 14 -3.5 and -8.5; window capped at 14 -8.7 and -13.1), every interval but one spanning zero.
The returning starter's pedigree, return by week 14: out-used him in 2+ of 4 games 7 of 10 against 4 of 26 (work,
p=0.003) and 5 of 8 against 3 of 19 (backup, p=0.027). Both cuts were chosen after looking.
"""
import os
import numpy as np
import pandas as pd
from common import HERE
from keep_role import perm_p, diff_ci, fisher_p

def gap(d, col):
    e, l = d[~d[col]], d[d[col]]
    if len(e) >= 2 and len(l) >= 2:
        lo, hi = diff_ci(l.change * 100, e.change * 100)
        return (f'late {l.change.mean()*100:+6.1f} (n={len(l):>2})  early {e.change.mean()*100:+6.1f} (n={len(e):>2})'
                f'  late minus early {(l.change.mean()-e.change.mean())*100:+6.1f} [{lo:+.1f}, {hi:+.1f}] p={perm_p(l.change, e.change):.3f}'
                f' | took {int(l.took.sum())}/{len(l)} vs {int(e.took.sum())}/{len(e)} p={fisher_p(int(l.took.sum()), len(l), int(e.took.sum()), len(e)):.3f}'
                f' | startable after {int(l.startable_after.sum())}/{len(l)} vs {int(e.startable_after.sum())}/{len(e)}'
                f' p={fisher_p(int(l.startable_after.sum()), len(l), int(e.startable_after.sum()), len(e)):.3f}'
                f' | median after ppg {l.after_ppg.median():.1f} vs {e.after_ppg.median():.1f}')
    return f'late n={len(l)} early n={len(e)}'

for label in ('work', 'backup'):
    full = pd.read_pickle(os.path.join(HERE, f'keep_role_{label}_2015_2025.pkl'))
    cap = pd.read_pickle(os.path.join(HERE, f'keep_role_{label}_2015_2025_wk14.pkl'))
    pf = full[full.guard & (full.grp == 'RB') & full.produced]
    pc = cap[cap.guard & (cap.grp == 'RB') & cap.produced]
    print(f'==== replacement = {label}: RB backs who produced, 2015-2025 ====')
    for lab, d in (('all weeks', pf), ('return by week 14', pf[pf.ret <= 14]), ('return week 15+', pf[pf.ret >= 15]),
                   ('window capped at week 14', pc)):
        print(f'  the REPLACEMENT\'s pedigree, {lab:<25} {gap(d, "rep_low")}')
    for lab, d in (('all weeks', pf), ('return by week 14', pf[pf.ret <= 14]), ('window capped at week 14', pc)):
        print(f'  the RETURNING STARTER\'s pedigree, {lab:<25} {gap(d, "lead_low")}')
    print()
