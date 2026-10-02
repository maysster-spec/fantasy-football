"""What is one breakout actually worth, in title odds?"""
import sys, numpy as np, pandas as pd
sys.path.insert(0,'/tmp/eng'); sys.path.insert(0,'/tmp/var')
import league
from league import draft, standings, POOL, band_of, PAYOUT, N_TEAMS, KEEP, NW, NEED, REPL_PG
from engine import Sim, load, GP_PROJ
from rules import RULES, PC
league.OPP_WINDOW=22
b,_=load()

def realise_track(sim, rosters, rng):
    pts=np.zeros((N_TEAMS,NW)); booms=0; busts=0; best=0.0
    for slot in range(1,N_TEAMS+1):
        idx=rosters[slot]
        pc=[PC[sim.pos[i]] for i in idx]; pg0=[sim.proj[i]/GP_PROJ for i in idx]
        by=[sim.bye[i] for i in idx]; adp=[sim.adp_opp[i] for i in idx]
        k=KEEP[KEEP.slot==slot]
        if len(k):
            r=k.iloc[0]; pc.append(PC[r.pos]); pg0.append(r.proj/GP_PROJ); by.append(float(r.bye)); adp.append(30.0)
        n=len(pc); pc=np.array(pc); pg0=np.array(pg0); by=np.array(by)
        form=np.empty(n); gpv=np.empty(n)
        for j,a in enumerate(adp):
            f,g=POOL[band_of(a)]; t=rng.integers(0,len(f)); form[j]=f[t]; gpv[j]=g[t]
        if slot==8:
            booms=int(((form>1.35)&(gpv>=12)).sum()); busts=int((form<0.70).sum())
            best=float((pg0*form*np.minimum(gpv,14)).max())
        pg=pg0*form
        live=np.zeros((n,NW),bool)
        for j in range(n):
            wk=rng.permutation(17)[:int(round(gpv[j]))]
            live[j]=np.isin(np.arange(1,NW+1),wk+1); live[j]&=(np.arange(1,NW+1)!=by[j])
        for w in range(NW):
            lv=live[:,w]; used=~lv; s=0.0; order=np.argsort(-pg)
            for p in range(4):
                kk=NEED[p]; c=0
                for i in order:
                    if c==kk: break
                    if lv[i] and not used[i] and pc[i]==p: s+=pg[i]; used[i]=True; c+=1
                s+=REPL_PG[p]*(kk-c)
            got=False
            for i in order:
                if lv[i] and not used[i] and pc[i] in (1,2,3): s+=pg[i]; got=True; break
            if not got: s+=max(REPL_PG[1],REPL_PG[2],REPL_PG[3])
            pts[slot-1,w]=s
    return pts,booms,busts,best

rows=[]
for d in range(60):
    r0=np.random.default_rng(5000+d); s0=Sim(b,198.68,r0); pref=s0.draw_pref()
    rng=np.random.default_rng(51_000+d); sim=Sim(b,198.68,rng)
    ros=draft(sim,RULES['R6 rollout'],pref,rng,r0.random()<0.85)
    for s in range(30):
        orng=np.random.default_rng(60_000+d*97+s)
        p,bm,bs,best=realise_track(sim,ros,orng)
        tot,rh,_=standings(p,np.random.default_rng(65_000+d*97+s))
        rows.append(dict(booms=bm,busts=bs,pts=tot[7],rank=int(rh[7]),
                         win=int(rh[7]==1),top6=int(rh[7]<=6),pay=PAYOUT.get(int(rh[7]),0)))
D=pd.DataFrame(rows); D.to_csv('/tmp/var/boom_value.csv',index=False)
print(f"n={len(D)} simulated seasons\n")
print("YOUR TITLE ODDS BY HOW MANY OF YOUR PLAYERS BREAK OUT (form > 1.35, played 12+ games)")
t=D.groupby('booms').agg(seasons=('win','size'),P_1st=('win','mean'),P_top6=('top6','mean'),
                         mean_pts=('pts','mean'),E_pay=('pay','mean')).round(3)
print(t[t.seasons>=25].to_string())
print("\nAND BY BUSTS (form < 0.70)")
t2=D.groupby('busts').agg(seasons=('win','size'),P_1st=('win','mean'),mean_pts=('pts','mean')).round(3)
print(t2[t2.seasons>=25].to_string())
import numpy as np
c=np.corrcoef(D.booms,D.pts)[0,1]; c2=np.corrcoef(D.busts,D.pts)[0,1]
print(f"\ncorr(booms, points) = {c:+.3f}   corr(busts, points) = {c2:+.3f}")
print(f"distribution of booms per season: {D.booms.value_counts().sort_index().to_dict()}")
