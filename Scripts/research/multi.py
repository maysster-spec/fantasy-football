"""reprice.py across many rooms: how often does each lever change the pick?"""
import os, sys, shutil, collections, time
import numpy as np, pandas as pd
BB='/home/claude/work/bb'; KIT='/home/claude/work/lb/new'
sys.path.insert(0,KIT); os.chdir(KIT)
import live_draft as LD
PICKS=list(LD.CLE.MY_PICKS)
ROOMS=int(sys.argv[1]) if len(sys.argv)>1 else 6
INNER=int(sys.argv[2]) if len(sys.argv)>2 else 20
SEEDS=[1000+7*i for i in range(ROOMS)]
res=collections.defaultdict(dict)
t0=time.time()
for t in ('A','P','D','PD'):
    dst=os.path.join(KIT,f'_tmp_{t}.csv'); shutil.copy(os.path.join(BB,f'board_{t}.csv'),dst)
    eng=LD.Engine(dst, os.path.join(KIT,'ESPN_prerank_with_ids.csv'))
    b=eng.b.reset_index(drop=True); sd=0.111*b.adp_pick.values+5.40
    for s in SEEDS:
        rng=np.random.default_rng(s)
        order=[int(i) for i in np.argsort(b.eff_pick.values+rng.normal(0,sd))]
        mine=[]; taken=set(); out=[]
        for pk in PICKS:
            need=(pk-1)-len(taken)
            if need>0: taken.update([i for i in order if i not in taken][:need])
            eng.set_taken([int(b.espn_id.iloc[i]) for i in taken],[int(b.espn_id.iloc[i]) for i in mine])
            r=eng.recommend(pk, rollout_inner=INNER, top=8)
            if not r: break
            out.append((r[0]['player'],r[0]['pos'],round(r[0]['roll']-r[1]['roll'],2)))
            mine.append(int(r[0]['i'])); taken.add(int(r[0]['i']))
        res[t][s]=out
    os.remove(dst)
print(f"  {ROOMS} rooms, rollout_inner={INNER}, identical opponent draws across all four boards\n")
print(f"  {'pick':>5} {'A: margin #1v#2':>16} {'P changes':>11} {'D changes':>11} {'PD changes':>11}")
for j,pk in enumerate(PICKS):
    mA=np.mean([res['A'][s][j][2] for s in SEEDS if j<len(res['A'][s])])
    row=f"  {pk:>5} {mA:>16.2f}"
    for t in ('P','D','PD'):
        n=sum(1 for s in SEEDS if j<len(res[t][s]) and j<len(res['A'][s])
              and res[t][s][j][0]!=res['A'][s][j][0])
        row+=f" {n:>6}/{ROOMS:<4}"
    print(row)
for t in ('P','D','PD'):
    tot=sum(1 for s in SEEDS for j in range(min(len(res[t][s]),len(res['A'][s])))
            if res[t][s][j][0]!=res['A'][s][j][0])
    e=sum(1 for s in SEEDS for j in range(4)
          if res[t][s][j][0]!=res['A'][s][j][0])
    print(f"\n  {t:<3} {tot} of {12*ROOMS} pick-decisions changed; {e} of {4*ROOMS} at picks 8/17/32/41")
print(f"[{time.time()-t0:.0f}s]")
