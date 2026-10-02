#!/usr/bin/env python3
"""Potential, priced in the same currency as the hole fills. Roster is Matt's CURRENT 14 --
Spears is gone (WIRE_20260910.csv shows him back in the free pool, ESPN shows him WA until Friday).
For each candidate we take the MEASURED distribution of what players clearing his screen went on to
score, drop a synthetic receiver on that rate into the roster, and recompute the best legal nine
for all fourteen weeks. E[gain] is the average over the whole distribution -- the misses included."""
import numpy as np
exec(open('moves.py').read().split('# ---- every (add, drop) pair')[0]
     .replace("('Tyjae Spears','RB',9),", ""))          # he is dropped

print(f"\n  CURRENT roster {len(roster)} players. Baseline weeks 1-14: {base:.1f}")
print("  the bar a new receiver has to clear, week by week (the lineup slot he would take):")
bar={}
for w in range(1,15):
    lo, hi = 0.0, 40.0
    for _ in range(40):                                  # bisect the rate that first adds a point
        mid=(lo+hi)/2
        cand=dict(name='X',pos='WR',tm='',bye=0,wk=mid)
        if week_points(roster+[cand],w) > week_points(roster,w)+0.001: hi=mid
        else: lo=mid
    bar[w]=hi
print("   " + "  ".join(f"w{w}:{bar[w]:.1f}" for w in range(1,15)))

DIST={'3 of 3 screen (4.30)': np.load('/home/claude/dst/dist_3of3.npy'),
      'first-round rookie (4.28)': np.load('/home/claude/dst/dist_rook1.npy')}
CAND=[('Ricky Pearsall','SF',8,'3 of 3 screen (4.30)'),
      ('Pat Bryant','DEN',10,'3 of 3 screen (4.30)'),
      ('Jalen McMillan','TB',10,'3 of 3 screen (4.30)'),
      ('Omar Cooper Jr.','NYJ',13,'first-round rookie (4.28)')]
print(f"\n  {'candidate':<20}{'bye':>4}{'screen':<28}{'E[gain]':>9}{'P(adds anything)':>18}{'p90 gain':>10}")
for nm,tm,by,screen in CAND:
    d=DIST[screen]; gains=[]
    for x in d:
        cand=dict(name=nm,pos='WR',tm=tm,bye=by,wk=float(x))
        gains.append(season(roster+[cand])-base)
    g=np.array(gains)
    print(f"  {nm:<20}{by:>4}{screen:<28}{g.mean():>+9.2f}{(g>0.5).mean():>17.0%}{np.percentile(g,90):>+10.1f}")

# and the same question for the three hole-fills, so they sit on one scale
print("\n  against the three hole fills, unchanged and certain:")
for nm,pos,tm,by,wk,lab in (('Brenton Strange','TE','JAX',7,8.07,'week 6 tight end'),
                            ('Chris Boswell','K','PIT',9,10.20,'week 8 kicker')):
    cand=dict(name=nm,pos=pos,tm=tm,bye=by,wk=wk)
    print(f"  {nm:<20}{by:>4}{lab:<28}{season(roster+[cand])-base:>+9.2f}{'certain':>17}")

# ---- the sensitivity that matters: his bar is 14.2 only while his receivers are healthy -------
print("\n  IF ONE OF HIS RECEIVERS MISSES TIME, the bar collapses and potential is worth more.")
print(f"  {'scenario':<34}{'bar':>6}{'Pearsall':>10}{'Cooper Jr.':>12}")
for lab, out in (('everyone healthy (the model above)', None),
                 ('Davante Adams out all season', 'Davante Adams'),
                 ('George Pickens out all season', 'George Pickens'),
                 ('Puka Nacua out all season', 'Puka Nacua')):
    r2=[p for p in roster if p['name']!=out] if out else roster
    b2=season(r2)
    lo,hi=0.0,40.0
    for _ in range(40):
        mid=(lo+hi)/2
        if week_points(r2+[dict(name='X',pos='WR',tm='',bye=0,wk=mid)],1) > week_points(r2,1)+0.001: hi=mid
        else: lo=mid
    res=[]
    for nm,by,key in (('Ricky Pearsall',8,'3 of 3 screen (4.30)'),('Omar Cooper Jr.',13,'first-round rookie (4.28)')):
        d=DIST[key]
        res.append(np.mean([season(r2+[dict(name=nm,pos='WR',tm='',bye=by,wk=float(x))])-b2 for x in d]))
    print(f"  {lab:<34}{hi:>6.1f}{res[0]:>+10.2f}{res[1]:>+12.2f}")
