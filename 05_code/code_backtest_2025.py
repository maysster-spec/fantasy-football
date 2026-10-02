#!/usr/bin/env python3
"""
code_backtest_2025.py — the 2025 holdout backtest.
HANDOFF_v2 section 6 calls this "the strongest available self-red-team and it has never
been done." It scores the whole pipeline instead of its parts.

DESIGN
  Matt drafted slot 11 in 2025. Selections: 11 14 35 38 59 62 83 86 107 110 131 134 155 158.
  Keeper Jayden Daniels at 179 is held constant for every policy.
  At each of his picks the AVAILABLE POOL is every player taken at a later pick in the real
  2025 draft. That is ground-truth availability, not modelled availability -- it removes the
  survival model from the test entirely so the test measures the VALUE rule alone.
  Preseason information only: ESPN's proj_2025. Outcome: actual_2025.

POLICIES
  ACTUAL   what Matt took
  BAV      best available by 2025 VBD, no constraints
  NEED     best available by 2025 VBD subject to filling 1QB 2RB 2WR 1TE 1FLEX 1DST 1K
  ORACLE   best available by ACTUAL 2025 points (hindsight ceiling, not a policy)

SCORING  season-total starting lineup: best 1QB 2RB 2WR 1TE 1FLEX 1DST 1K by actual_2025.
LIMITS   no weekly data, so no bye or injury adjustment and no week-by-week optimum;
         pool restricted to players someone actually drafted.
"""
import pandas as pd, numpy as np

SRC='src/'
d=pd.read_csv(SRC+'draft_history_2021_2025.csv')
e=pd.read_csv(SRC+'espn_projections_2026_20260820.csv'); e.columns=[c.replace('﻿','') for c in e.columns]
d25=d[d['Year']==2025].copy()

ALIAS={'Devonta Smith':'DeVonta Smith','Marvin Harrison':'Marvin Harrison Jr.',
       'Brian Robinson':'Brian Robinson Jr.','Travis Etienne':'Travis Etienne Jr.',
       'Kenneth Walker':'Kenneth Walker III','Michael Pittman':'Michael Pittman Jr.',
       'Marvin Mims':'Marvin Mims Jr.','Jayden Higgins':'Jayden Higgins'}
d25['key']=d25['Player'].replace(ALIAS)

# D/ST naming: draft history "Bills D/ST" matches ESPN exactly
ref=e[['Player','pos','proj_2025','actual_2025']].rename(columns={'Player':'key','pos':'pos_e'})
assert ref['key'].duplicated().sum()==0, "duplicate player names in ESPN pull"
n0=len(d25)
d25=d25.merge(ref,on='key',how='left')
assert len(d25)==n0, "merge changed row count"
matched=d25['proj_2025'].notna()
print(f"JOIN  {int(matched.sum())} of {n0} 2025 picks carry a 2025 projection")
print("      unmatched:", sorted(d25.loc[~matched,'Player'].unique()))
pos_dis=d25[matched&(d25['Pos'].str.upper()!=d25['pos_e'].str.upper())]
print("      position disagreements:", len(pos_dis), pos_dis['Player'].tolist()[:5])

# 2025 replacement levels from the 2025 preseason projection
ST={'QB':12,'RB':30,'WR':30,'TE':12,'D/ST':12,'K':12}
repl={}
for p,n in ST.items():
    v=e.loc[e['pos']==p,'proj_2025'].dropna().sort_values(ascending=False)
    repl[p]=float(v.iloc[n-1])
print("\n2025 REPLACEMENT (preseason proj):", {k:round(v,1) for k,v in repl.items()})
d25['vbd25']=d25.apply(lambda r: r['proj_2025']-repl.get(r['pos_e'],np.nan)
                       if pd.notna(r['proj_2025']) else np.nan, axis=1)

MATT='Matt Mays'
my=d25[(d25['Manager']==MATT)&(~d25['Keeper'])].sort_values('Pick')
MY_PICKS=my['Pick'].tolist()
KEEPER=d25[(d25['Manager']==MATT)&(d25['Keeper'])].iloc[0]
print(f"\nslot 11, {len(MY_PICKS)} selections: {MY_PICKS}")
print(f"keeper held constant: {KEEPER['Player']} ({KEEPER['pos_e']}) actual {KEEPER['actual_2025']:.1f}")

pool_all=d25[d25['proj_2025'].notna()].copy()

def run(score_col, need_constrained):
    roster=[]; counts={'QB':0,'RB':0,'WR':0,'TE':0,'D/ST':0,'K':0}
    counts[KEEPER['pos_e']]+=1
    MIN={'QB':1,'RB':2,'WR':2,'TE':1,'D/ST':1,'K':1}
    for i,pk in enumerate(MY_PICKS):
        remaining=len(MY_PICKS)-i
        avail=pool_all[(pool_all['Pick']>=pk)&(~pool_all['Player'].isin([r['Player'] for r in roster]))]
        avail=avail[avail[score_col].notna()]
        if need_constrained:
            unmet=[p for p,m in MIN.items() if counts[p]<m]
            slots_needed=sum(max(0,MIN[p]-counts[p]) for p in MIN)
            if slots_needed>=remaining and unmet:
                avail=avail[avail['pos_e'].isin(unmet)]
            else:  # cap hoarding: no 3rd QB/TE/DST/K
                cap={'QB':2,'TE':2,'D/ST':1,'K':1,'RB':6,'WR':6}
                avail=avail[avail['pos_e'].map(lambda p: counts[p]<cap.get(p,6))]
        if not len(avail): continue
        pick=avail.sort_values(score_col,ascending=False).iloc[0]
        roster.append(dict(Pick=pk,Player=pick['Player'],pos=pick['pos_e'],
                           proj=pick['proj_2025'],actual=pick['actual_2025'],vbd=pick['vbd25']))
        counts[pick['pos_e']]+=1
    return pd.DataFrame(roster)

def lineup_pts(df):
    r=pd.concat([df,pd.DataFrame([dict(Player=KEEPER['Player'],pos=KEEPER['pos_e'],
                 actual=KEEPER['actual_2025'])])],ignore_index=True)
    r=r.dropna(subset=['actual']); tot=0; used=set()
    for p,n in [('QB',1),('RB',2),('WR',2),('TE',1),('D/ST',1),('K',1)]:
        g=r[(r['pos']==p)&(~r.index.isin(used))].nlargest(n,'actual')
        tot+=g['actual'].sum(); used|=set(g.index)
    fx=r[(r['pos'].isin(['RB','WR','TE']))&(~r.index.isin(used))].nlargest(1,'actual')
    tot+=fx['actual'].sum()
    return tot

actual=my.rename(columns={'pos_e':'pos','proj_2025':'proj','actual_2025':'actual','vbd25':'vbd'})[
        ['Pick','Player','pos','proj','actual','vbd']]
res={'ACTUAL (Matt)':actual,'BAV (max VBD)':run('vbd25',False),
     'NEED (VBD + roster need)':run('vbd25',True),'ORACLE (hindsight)':run('actual_2025',True)}

print("\n"+"="*74)
print("RESULT — season-total starting-lineup points, 2025, keeper held constant")
print("="*74)
for k,v in res.items():
    print(f"  {k:28s} {lineup_pts(v):8.1f}   (14 picks, sum actual {v['actual'].sum():.0f})")

print("\nPICK BY PICK — Matt vs the value rule")
cmp=actual[['Pick','Player','pos','actual']].rename(columns={'Player':'matt','pos':'p_m','actual':'a_m'})
nd=res['NEED (VBD + roster need)'][['Pick','Player','pos','actual']].rename(
    columns={'Player':'rule','pos':'p_r','actual':'a_r'})
t=cmp.merge(nd,on='Pick',how='left'); t['delta']=t['a_r']-t['a_m']
print(t.to_string(index=False,float_format=lambda x:f"{x:7.1f}"))
print(f"\n  rule beat Matt on {int((t['delta']>0).sum())} of {len(t)} picks; "
      f"total raw-point delta {t['delta'].sum():+.1f}")
t.to_csv('out/backtest_2025_pickbypick.csv',index=False)
for k,v in res.items(): v.assign(policy=k).to_csv(f"out/backtest_2025_{k.split()[0].lower()}.csv",index=False)
print("\nwrote out/backtest_2025_pickbypick.csv and one file per policy")
