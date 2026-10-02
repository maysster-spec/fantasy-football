"""How much of a season is decided at the draft, and how much by the season itself?"""
import sys, numpy as np, pandas as pd
sys.path.insert(0,'/tmp/eng'); sys.path.insert(0,'/tmp/var')
import league
from league import draft, realise, standings, PAYOUT
from engine import Sim, load
from rules import RULES
league.OPP_WINDOW=22
b,_=load()
ND, NS = 45, 45                       # draft realisations x season realisations
pts=np.zeros((ND,NS)); rk=np.zeros((ND,NS)); pay=np.zeros((ND,NS))
rosters=[]
for d in range(ND):
    r0=np.random.default_rng(3000+d); s0=Sim(b,198.68,r0); pref=s0.draw_pref()
    rng=np.random.default_rng(31_000+d); sim=Sim(b,198.68,rng)
    ros=draft(sim,RULES['R6 rollout'],pref,rng,r0.random()<0.85)
    rosters.append([sim.name[i] for i in ros[8]])
    for s in range(NS):
        orng=np.random.default_rng(40_000+s)      # SAME season luck across all drafts
        p=realise(sim,ros,orng)
        tot,rh,_=standings(p,np.random.default_rng(45_000+s))
        pts[d,s]=tot[7]; rk[d,s]=rh[7]; pay[d,s]=PAYOUT.get(int(rh[7]),0)
gm=pts.mean()
v_draft = pts.mean(1).var()          # variance of draft-means
v_season= pts.mean(0).var()          # variance of season-means
v_tot   = pts.var()
print(f"Matt's weeks 1-14 points: mean {gm:.0f}, sd {pts.std():.0f}   ({ND} drafts x {NS} seasons)")
print(f"\nVARIANCE DECOMPOSITION of your season point total")
print(f"  set by WHICH PLAYERS you drafted : {v_draft/v_tot:6.1%}   (sd {np.sqrt(v_draft):.0f} pts)")
print(f"  set by HOW THE SEASON GOES       : {v_season/v_tot:6.1%}   (sd {np.sqrt(v_season):.0f} pts)")
print(f"  interaction / residual           : {1-(v_draft+v_season)/v_tot:6.1%}")
print(f"\nBEST vs WORST DRAFT you could realistically end up with (same 45 seasons):")
dm=pts.mean(1); order=np.argsort(dm)
print(f"  worst draft mean {dm[order[0]]:.0f}   best draft mean {dm[order[-1]]:.0f}   spread {dm.max()-dm.min():.0f}")
print(f"BEST vs WORST SEASON LUCK (same 45 drafts):")
sm=pts.mean(0); print(f"  worst season mean {sm.min():.0f}   best season mean {sm.max():.0f}   spread {sm.max()-sm.min():.0f}")
print(f"\nP(1st) overall {np.mean(rk==1):.3f}  E[payout] ${pay.mean():.0f}")
print(f"  P(1st) range across the 45 drafts: {np.mean(rk==1,axis=1).min():.2f} to {np.mean(rk==1,axis=1).max():.2f}")
np.save('/tmp/var/decomp_pts.npy',pts); np.save('/tmp/var/decomp_pay.npy',pay)
