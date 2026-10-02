#!/usr/bin/env python3
r"""
keep_role_checks.py -- doc 294's checks on keep_role.py's events (run keep_role.py --years 2015-2025 first).
(a) the headline cut without replacements who missed every game after the return (his own absence, not the team's call);
(b) directive 4.27's short-absence inversion (1-2 games missed against 3+), on all guarded RB events;
(c) plain levels for RB replacements who produced: share before and after, startable after, by pedigree;
(d) the returning lead man's pedigree against TOOK, the one secondary cut that looked large.
RESULT (11 Sept 2026, doc 294):
  (a) without them the pedigree gap stays inside noise (work -0.9, p=0.90; backup -5.1, p=0.43) and production
      still decides (work +15.1, backup +13.1, both p<=0.001);
  (b) directive 4.27's short-absence inversion does not replicate: 2015-2020 -2.4 (p=0.63); work definition +2.8
      (p=0.60);
  (c) producers go from about 23% to 35% of the backfield's touches; 13 of 50 startable after (work);
  (d) out-used the returning starter in 2+ of 4 games: 7 of 15 when he was a late pick, 6 of 35 when he was a
      round 1-3 pick (p=0.040; chosen after looking); 7 of 10 against 4 of 26 when the return came by week 14.
"""
import os
import numpy as np
import pandas as pd
from common import HERE
from keep_role import perm_p, fisher_p, diff_ci

for label in ('backup', 'work'):
    ev = pd.read_pickle(os.path.join(HERE, f'keep_role_{label}_2015_2025.pkl'))
    rb = ev[ev.guard & (ev.grp == 'RB')]
    print(f'==== replacement = {label}, RB, 2015-2025, n={len(rb)} ====')
    # (a)
    nz = rb[rb.after_g > 0]
    print(f'(a) replacements who missed all the after games: {int((rb.after_g == 0).sum())}; without them n={len(nz)}')
    p = nz[nz.produced]
    e, l = p[~p.rep_low], p[p.rep_low]
    lo, hi = diff_ci(l.change * 100, e.change * 100)
    print(f'    produced: late {l.change.mean()*100:+.1f} (n={len(l)}) early {e.change.mean()*100:+.1f} (n={len(e)}),'
          f' late minus early {(l.change.mean()-e.change.mean())*100:+.1f} [{lo:+.1f}, {hi:+.1f}] p={perm_p(l.change, e.change):.3f}')
    q = nz
    print(f'    production effect: produced {q[q.produced].change.mean()*100:+.1f} (n={int(q.produced.sum())})'
          f' did not {q[~q.produced].change.mean()*100:+.1f} (n={int((~q.produced).sum())})'
          f' p={perm_p(q[q.produced].change, q[~q.produced].change):.3f}')
    # (b)
    s, lg = rb[rb.missed <= 2], rb[rb.missed >= 3]
    lo, hi = diff_ci(lg.change * 100, s.change * 100)
    print(f'(b) all guarded RB events: 3+ games missed {lg.change.mean()*100:+.1f} (n={len(lg)}) against 1-2 {s.change.mean()*100:+.1f}'
          f' (n={len(s)}): {(lg.change.mean()-s.change.mean())*100:+.1f} [{lo:+.1f}, {hi:+.1f}] p={perm_p(lg.change, s.change):.3f}')
    for yrs, d in (('2021-2025', rb[rb.season >= 2021]), ('2015-2020', rb[rb.season <= 2020])):
        s2, l2 = d[d.missed <= 2], d[d.missed >= 3]
        print(f'    {yrs}: 3+ {l2.change.mean()*100:+.1f} (n={len(l2)}) against 1-2 {s2.change.mean()*100:+.1f} (n={len(s2)})'
              f' p={perm_p(l2.change, s2.change):.3f}')
    # (c)
    p = rb[rb.produced]
    for low in (False, True):
        d = p[p.rep_low == low]
        print(f'(c) produced, {"late pick " if low else "rounds 1-3"}: n={len(d)} share before {d.before.mean()*100:.0f}% after'
              f' {d.after.mean()*100:.0f}% | took {int(d.took.sum())}/{len(d)} | startable after {int(d.startable_after.sum())}/{len(d)}'
              f' | after ppg median {d.after_ppg.median():.1f}')
    k1, n1 = int(p[p.rep_low].startable_after.sum()), int(p.rep_low.sum())
    k2, n2 = int(p[~p.rep_low].startable_after.sum()), int((~p.rep_low).sum())
    print(f'    all producers startable after {k1+k2}/{n1+n2} = {(k1+k2)/(n1+n2)*100:.0f}%; late against early Fisher p={fisher_p(k1, n1, k2, n2):.3f}')
    # (d)
    k1, n1 = int(p[p.lead_low].took.sum()), int(p.lead_low.sum())
    k2, n2 = int(p[~p.lead_low].took.sum()), int((~p.lead_low).sum())
    print(f'(d) produced, TOOK by the lead man\'s pedigree: lead late pick {k1}/{n1}, lead rounds 1-3 {k2}/{n2}, Fisher p={fisher_p(k1, n1, k2, n2):.3f}')
    print()
