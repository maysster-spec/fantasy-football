import sys, numpy as np, pandas as pd, time, json
sys.path.insert(0,'/tmp/eng'); sys.path.insert(0,'/tmp/var')
import league
from league import draft, realise, standings, POOL, band_of, PAYOUT, N_TEAMS
from engine import Sim, load, MY_SKILL_PICKS
import rules
from rules import RULES, _cand, my_legal, r_rollout

E=pd.read_csv('/tmp/var/decomposed.csv')
BANDS=[0,24,48,84,120,180,10**6]
DISP={}
for b in range(len(BANDS)-1):
    s=E[(E.adp>BANDS[b])&(E.adp<=BANDS[b+1])]
    if len(s)<25: s=E[E.adp>84]
    DISP[b]=float(s.form.quantile(.90)-s.form.mean())     # upside above the mean, in form units

def make_risk_rule(lam, from_pick=1):
    def rule(sim, avail, roster, counts, pk, left, rng):
        i=_cand(sim,avail,counts,left)
        i=i[np.argsort(-sim.vbd[i])][:6]
        if pk<from_pick or lam==0:
            return r_rollout(sim,avail,roster,counts,pk,left,rng)
        from rules import _lv
        # rollout score for the same 6, then add the upside bonus
        base=r_rollout.__wrapped__ if hasattr(r_rollout,'__wrapped__') else None
        future=[p for p in MY_SKILL_PICKS if p>pk]
        gaps=[(k,(p-pk)-(k+1)) for k,p in enumerate(future)]
        sc=np.zeros(len(i)); a=sim.adp_opp
        from rules import _finish
        for _ in range(4):
            pref=np.where(avail, a+rng.normal(0,0.30*np.minimum(a,70.0)), np.inf)
            pr=np.empty(sim.n); pr[np.argsort(pref)]=np.arange(sim.n)
            for j,c in enumerate(i):
                av=avail.copy(); av[c]=False
                cc=dict(counts); cc[sim.pos[c]]=cc.get(sim.pos[c],0)+1
                sc[j]+= _finish(sim,av,list(roster)+[c],cc,gaps,pr) if future else _lv(sim,roster,c)
        sc/=4
        bonus=np.array([sim.proj[c]*DISP[band_of(sim.adp_opp[c])] for c in i])
        return i[int(np.argmax(sc+lam*bonus))]
    return rule

VARIANTS={
 'static VBD + caps'               : RULES['R2 static VBD + caps'],
 'rollout (current engine)'        : RULES['R6 rollout'],
 'rollout + upside tilt L=1.0'     : make_risk_rule(1.0),
 'rollout + LATE tilt L=1.5 (rd9+)': make_risk_rule(1.5, from_pick=104),
}

def main(N, window):
    league.OPP_WINDOW=window
    b,_=load(); out={k:dict(pts=[],r_h2h=[],r_pts=[],pay=[]) for k in VARIANTS}; t0=time.time()
    for s in range(N):
        r0=np.random.default_rng(2000+s); s0=Sim(b,198.68,r0)
        pref=s0.draw_pref(); sny=r0.random()<0.85
        for name,fn in VARIANTS.items():
            rng=np.random.default_rng(70_000+s); sim=Sim(b,198.68,rng)
            ros=draft(sim,fn,pref.copy(),rng,sny)
            orng=np.random.default_rng(90_000+s)          # IDENTICAL season luck across rules
            pts=realise(sim,ros,orng); tot,rh,rp=standings(pts,np.random.default_rng(95_000+s))
            o=out[name]; o['pts'].append(tot[7]); o['r_h2h'].append(int(rh[7])); o['r_pts'].append(int(rp[7]))
            o['pay'].append(PAYOUT.get(int(rh[7]),0))
        if (s+1)%50==0: print(f"  {s+1}/{N} {time.time()-t0:.0f}s",flush=True)
    rows=[]
    for k,o in out.items():
        p=np.array(o['pts']); rh=np.array(o['r_h2h']); rp=np.array(o['r_pts']); pay=np.array(o['pay'])
        rows.append(dict(rule=k, mean_pts=p.mean(), p90_pts=np.percentile(p,90),
                         P_pts_1st=(rp==1).mean(), P_1st=(rh==1).mean(), P_top6=(rh<=6).mean(),
                         E_payout=pay.mean()))
    df=pd.DataFrame(rows)
    print(f"\nN={N} paired sims | opponent window {window} | full 12-team league | EMPIRICAL outcome variance\n")
    print(df.round(3).to_string(index=False))
    json.dump(out,open(f'/tmp/var/risk_out_w{window}.json','w'))
    df.to_csv(f'/tmp/var/risk_summary_w{window}.csv',index=False)
main(int(sys.argv[1]), int(sys.argv[2]))
