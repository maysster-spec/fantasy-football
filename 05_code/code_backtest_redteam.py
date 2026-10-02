#!/usr/bin/env python3
"""Adversarial checks on the 2025 holdout result before anyone acts on it."""
import pandas as pd, numpy as np
SRC='src/'
e=pd.read_csv(SRC+'espn_projections_2026_20260820.csv'); e.columns=[c.replace('﻿','') for c in e.columns]
d=pd.read_csv(SRC+'draft_history_2021_2025.csv'); d25=d[d['Year']==2025].copy()
ALIAS={'Devonta Smith':'DeVonta Smith','Marvin Harrison':'Marvin Harrison Jr.',
       'Brian Robinson':'Brian Robinson Jr.','Travis Etienne':'Travis Etienne Jr.',
       'Kenneth Walker':'Kenneth Walker III','Michael Pittman':'Michael Pittman Jr.',
       'Marvin Mims':'Marvin Mims Jr.'}
d25['key']=d25['Player'].replace(ALIAS)
ref=e[['Player','pos','proj_2025','actual_2025']].rename(columns={'Player':'key','pos':'pos_e'})
d25=d25.merge(ref,on='key',how='left')

print("="*74); print("RT1 — is proj_2025 really PRESEASON, or is it hindsight-contaminated?"); print("="*74)
sk=e[(~e['pos'].isin(['K','D/ST']))&e['proj_2025'].notna()&e['actual_2025'].notna()]
for lab,g in [('all skill',sk),('proj_2025>=100',sk[sk['proj_2025']>=100])]:
    r=g['proj_2025'].corr(g['actual_2025']); rs=g['proj_2025'].corr(g['actual_2025'],method='spearman')
    print(f"  {lab:18s} n={len(g):4d}  pearson {r:.3f}  spearman {rs:.3f}")
print("  benchmark: a genuine preseason projection lands ~0.55-0.75; >0.90 means in-season data leaked.")
big=sk[(sk['proj_2025']>=150)&(sk['actual_2025']<=40)]
print(f"  players projected >=150 who finished <=40 (season-enders the projection did NOT see): {len(big)}")
print("   ",", ".join(big.nlargest(8,'proj_2025')['Player']))

print("\n"+"="*74); print("RT2 — A10: is the win concentrated in a handful of picks?"); print("="*74)
t=pd.read_csv('out/backtest_2025_pickbypick.csv')
t=t.sort_values('delta',ascending=False)
print(t[['Pick','matt','a_m','rule','a_r','delta']].to_string(index=False,float_format=lambda x:f"{x:7.1f}"))
tot=t['delta'].sum(); top3=t.nlargest(3,'delta')['delta'].sum()
print(f"\n  total {tot:+.1f} | top 3 picks {top3:+.1f} ({100*top3/tot:.0f}% of it) | other 11 picks {tot-top3:+.1f}")
print(f"  median pick-level delta {t['delta'].median():+.1f}  mean {t['delta'].mean():+.1f}  sd {t['delta'].std():.1f}")
b=[np.random.default_rng(s).choice(t['delta'].values,len(t),replace=True).mean() for s in range(4000)]
lo,hi=np.percentile(b,[2.5,97.5])
print(f"  bootstrap 95% CI on mean pick delta: [{lo:+.1f}, {hi:+.1f}]  -> {'EXCLUDES' if lo>0 or hi<0 else 'INCLUDES'} zero")

print("\n"+"="*74); print("RT3 — does the rule beat EVERY manager, or only Matt?"); print("="*74)
pool=d25[d25['proj_2025'].notna()].copy()
ST={'QB':12,'RB':30,'WR':30,'TE':12,'D/ST':12,'K':12}
repl={p:float(e.loc[e['pos']==p,'proj_2025'].dropna().sort_values(ascending=False).iloc[n-1]) for p,n in ST.items()}
pool['vbd25']=pool['proj_2025']-pool['pos_e'].map(repl)
MIN={'QB':1,'RB':2,'WR':2,'TE':1,'D/ST':1,'K':1}; CAP={'QB':2,'TE':2,'D/ST':1,'K':1,'RB':6,'WR':6}
def lineup(rows):
    r=pd.DataFrame(rows).dropna(subset=['actual']); tot=0; used=set()
    for p,n in [('QB',1),('RB',2),('WR',2),('TE',1),('D/ST',1),('K',1)]:
        g=r[(r['pos']==p)&(~r.index.isin(used))].nlargest(n,'actual'); tot+=g['actual'].sum(); used|=set(g.index)
    tot+=r[(r['pos'].isin(['RB','WR','TE']))&(~r.index.isin(used))].nlargest(1,'actual')['actual'].sum()
    return tot
out=[]
for mgr,g in d25.groupby('Manager'):
    keep=g[g['Keeper']]; sel=g[~g['Keeper']].sort_values('Pick')
    if not len(keep): continue
    kp=keep.iloc[0]
    picks=sel['Pick'].tolist()
    counts={p:0 for p in MIN}; counts[kp['pos_e']]=counts.get(kp['pos_e'],0)+1
    roster=[dict(Player=kp['Player'],pos=kp['pos_e'],actual=kp['actual_2025'])]
    taken=set()
    for i,pk in enumerate(picks):
        rem=len(picks)-i
        av=pool[(pool['Pick']>=pk)&(~pool['Player'].isin(taken))&pool['vbd25'].notna()]
        unmet=[p for p,m in MIN.items() if counts.get(p,0)<m]
        need=sum(max(0,MIN[p]-counts.get(p,0)) for p in MIN)
        av=av[av['pos_e'].isin(unmet)] if (need>=rem and unmet) else av[av['pos_e'].map(lambda p: counts.get(p,0)<CAP.get(p,6))]
        if not len(av): continue
        pk2=av.nlargest(1,'vbd25').iloc[0]
        roster.append(dict(Player=pk2['Player'],pos=pk2['pos_e'],actual=pk2['actual_2025']))
        taken.add(pk2['Player']); counts[pk2['pos_e']]=counts.get(pk2['pos_e'],0)+1
    real=[dict(Player=r['Player'],pos=r['pos_e'],actual=r['actual_2025']) for _,r in g.iterrows()]
    out.append(dict(manager=mgr,slot=int(sel['Pick'].min()),actual=lineup(real),rule=lineup(roster)))
o=pd.DataFrame(out); o['delta']=o['rule']-o['actual']
print(o.sort_values('delta',ascending=False).to_string(index=False,float_format=lambda x:f"{x:8.1f}"))
print(f"\n  rule beat {int((o['delta']>0).sum())} of {len(o)} managers | mean {o['delta'].mean():+.1f} "
      f"| median {o['delta'].median():+.1f} | sd {o['delta'].std():.1f}")
print(f"  Matt's rank on actual points: {int((o['actual']>o.loc[o['manager'].str.contains('Matt'),'actual'].iloc[0]).sum())+1} of {len(o)}")
o.to_csv('out/backtest_2025_all_managers.csv',index=False)

print("\n"+"="*74); print("RT4 — how much of the edge is injury luck the rule could not have known?"); print("="*74)
inj=t[(t['a_m']<60)|(t['a_r']<60)]
print(f"  picks where one side finished under 60 points (a season-ending event): {len(inj)}")
print(inj[['Pick','matt','a_m','rule','a_r','delta']].to_string(index=False,float_format=lambda x:f"{x:7.1f}"))
print(f"  delta from those picks alone: {inj['delta'].sum():+.1f} of {tot:+.1f}")
