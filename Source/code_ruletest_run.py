import sys, numpy as np, pandas as pd, time, json
sys.path.insert(0,'/tmp/eng')
from engine import *
from fastscore import score_mc
from rules import RULES, PC

ORDER=[]
for r in range(N_ROUNDS):
    ORDER += list(range(1,N_TEAMS+1) if r%2==0 else range(N_TEAMS,0,-1))

def run_one(sim, rule, pref, rng, snyder_wants):
    avail=np.ones(sim.n,bool); roster=[]; counts={}
    opp={s:{} for s in range(1,N_TEAMS+1)}; allen_gone=False
    for pk in range(1,TOTAL_PICKS+1):
        slot=ORDER[pk-1]
        if slot==MY_SLOT:
            left=sum(1 for p in MY_SKILL_PICKS if p>=pk)
            c=int(rule(sim,avail,roster,counts,pk,left,rng))
            roster.append(c); counts[sim.pos[c]]=counts.get(sim.pos[c],0)+1
        else:
            if slot==9 and snyder_wants and not allen_gone and sim.allen>=0 and avail[sim.allen]:
                c=sim.allen
            else:
                left=sum(1 for q in range(pk,TOTAL_PICKS+1) if ORDER[q-1]==slot)
                m=avail & np.isin(sim.pos,list(Sim.opp_legal(opp[slot],left)))
                if not m.any(): m=avail
                c=int(np.argmin(np.where(m,pref,np.inf)))
            opp[slot][sim.pos[c]]=opp[slot].get(sim.pos[c],0)+1
        if c==sim.allen: allen_gone=True
        avail[c]=False
    pc=[PC[sim.pos[i]] for i in roster]+[PC['WR']]
    pg=[sim.pg[i] for i in roster]+[sim.keeper_pg]
    by=[sim.bye[i] for i in roster]+[14.0]
    return score_mc(pc,pg,by,sim.repl_i,rng,80), [sim.name[i] for i in roster], counts

def main(N=60):
    b,_=load()
    res={k:[] for k in RULES}; ros={k:[] for k in RULES}; cnt={k:[] for k in RULES}; t0=time.time()
    for s in range(N):
        r0=np.random.default_rng(1000+s); s0=Sim(b,198.68,r0)
        pref=s0.draw_pref(); snyder=r0.random()<0.85
        for name,fn in RULES.items():
            rng=np.random.default_rng(50_000+s); sim=Sim(b,198.68,rng)
            sc,ro,ct=run_one(sim,fn,pref.copy(),rng,snyder)
            res[name].append(sc); ros[name].append(ro); cnt[name].append(ct)
        if (s+1)%10==0: print(f"  {s+1}/{N}  {time.time()-t0:.0f}s",flush=True)
    df=pd.DataFrame(res); df.to_csv('/tmp/eng/results.csv',index=False)
    json.dump(ros,open('/tmp/eng/rosters.json','w')); json.dump(cnt,open('/tmp/eng/counts.json','w'))
    base='R2 static VBD + caps'; rng=np.random.default_rng(7); rows=[]
    for k in RULES:
        d=(df[k]-df[base]).values
        bs=[d[rng.integers(0,len(d),len(d))].mean() for _ in range(3000)]
        cc=pd.DataFrame(cnt[k]).fillna(0)
        rows.append(dict(rule=k,mean=df[k].mean(),sd=df[k].std(),p10=np.percentile(df[k],10),
                         p90=np.percentile(df[k],90),vs_R2=d.mean(),
                         lo=np.percentile(bs,2.5),hi=np.percentile(bs,97.5),win=(d>0).mean(),
                         QB=cc.get('QB',0).mean(),RB=cc.get('RB',0).mean(),
                         WR=cc.get('WR',0).mean(),TE=cc.get('TE',0).mean()))
    out=pd.DataFrame(rows).sort_values('mean',ascending=False)
    print(f"\nN={N} PAIRED sims | objective = starting-lineup pts, wks 1-14, injury+bye adjusted\n")
    print(out.round(2).to_string(index=False))
    out.to_csv('/tmp/eng/summary.csv',index=False)
    return out
if __name__=='__main__': main(int(sys.argv[1]) if len(sys.argv)>1 else 60)
