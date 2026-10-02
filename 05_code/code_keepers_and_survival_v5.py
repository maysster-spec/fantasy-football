#!/usr/bin/env python3
"""
Predict the 12 keepers on CORRECTED ADP, remove them before pick 1, and simulate
availability at each of Matt's 14 selections.

Fixes carried in from claude/19_integrity_audit_20260822.md:
 - keeper_eligibility_VERIFIED.ESPN_ADP was the rank column, not ADP. Re-keyed to adp_pick.
 - K and D/ST excluded from keeper prediction (directive 4.9).
Population gates (ERROR_PATTERNS A11):
 - the residual noise model sd = 0.1255*rank + 5.31 was fitted on BOARD RANK, so it is
   applied to adp_rank, never to adp_pick.
 - the tight-end draft lag was measured at +14.9 for ADP<=40 (n=8) and -3.7 for ADP 61-120
   (n=24). It is applied ONLY to the top band.
"""
import pandas as pd, numpy as np
rng=np.random.default_rng(20260822)
s=pd.read_csv('out/code_universe_v5.csv')
k=pd.read_csv('src/keeper_eligibility_VERIFIED.csv')

nm=s.set_index('player')
def look(p,col):
    for cand in [p,p+' Jr.',p+' Sr.',p+' II',p+' III',p.replace(' Jr.','')]:
        if cand in nm.index: return nm.loc[cand,col]
    return np.nan
k['adp_pick']=k['Player'].map(lambda p: look(p,'adp_pick'))
k['adp_rank']=k['Player'].map(lambda p: look(p,'adp_rank'))
k['pos_v']  =k['Player'].map(lambda p: look(p,'pos'))
k['proj_v'] =k['Player'].map(lambda p: look(p,'proj_leaguepts'))
k['inj']    =k['Player'].map(lambda p: look(p,'injury_status'))
print("keeper file: %d rows, %d matched to the v5 spine"%(len(k),k['adp_pick'].notna().sum()))
print("unmatched:",k.loc[k['adp_pick'].isna(),'Player'].tolist())

elig=k[~k['pos_v'].isin(['K','D/ST'])&k['adp_pick'].notna()]
pred=elig.loc[elig.groupby('Team')['adp_pick'].idxmin()][
    ['Team','Player','pos_v','adp_pick','proj_v','inj','ESPN_ADP']]
pred=pred.rename(columns={'ESPN_ADP':'old_rank_col'}).sort_values('adp_pick')
print("\nPREDICTED KEEPERS — lowest corrected ADP per team, K and D/ST excluded")
print(pred.to_string(index=False,float_format=lambda x:f"{x:7.1f}"))
pred.to_csv('out/predicted_keepers_v5.csv',index=False)

KEEPERS=set(pred['Player'])
MY_PICKS=[8,17,32,41,56,65,80,89,104,113,128,137,152,161]

# Deep pool: ESPN censors ADP at ~170, so 492 rows share one value and carry no order.
# Give them a synthetic rank continuing past the last real one, ordered by projection.
# Labelled in the output so nobody mistakes it for observed ADP.
s=s.copy()
last=s['adp_rank'].max()
deep=s[s['adp_censored']&s['proj_leaguepts'].notna()&(s['proj_leaguepts']>=35)].copy()
deep=deep.sort_values('proj_leaguepts',ascending=False)
s.loc[deep.index,'adp_rank']=last+np.arange(1,len(deep)+1)
s.loc[deep.index,'rank_src']='projection_order_adp_censored'
s['rank_src']=s['rank_src'].fillna('espn_adp') if 'rank_src' in s else np.where(s['adp_censored'],'projection_order_adp_censored','espn_adp')
board=s[s['adp_rank'].notna()].copy()
board=board[~board['player'].isin(KEEPERS)]
print(f"\nboard pool: {len(board)} players ({int((~board['adp_censored']).sum())} with observed ADP, "
      f"{int(board['adp_censored'].sum())} deep-pool ordered by projection)")
# directive 4.8: D/ST and K draft value is not realizable (11-12 of 12 teams stream every
# season). They keep a vbd for ordering WITHIN position at picks 152 and 161, but they are
# never allowed to compete against skill players on a cross-position ranking.
board['vbd_rank_elig']=np.where(board['pos'].isin(['D/ST','K']),np.nan,board['vbd'])
N=4000
avail=np.zeros((len(board),len(MY_PICKS)))
r=board['adp_rank'].values
sd=0.1255*r+5.31
te_lag=np.where((board['pos'].values=='TE')&(r<=40),15.0,0.0)   # A11: top band only
allen=(board['player'].values=='Josh Allen')
for it in range(N):
    draw=r+te_lag+rng.normal(0,sd)
    draw=np.where(allen & (rng.random()<0.85), 9.0, draw)        # Snyder behavioural rule
    order=np.argsort(draw)
    gone_by=np.empty(len(board)); gone_by[order]=np.arange(1,len(board)+1)
    # available at pick pk if at least pk-1 other players are drafted after him
    for j,pk in enumerate(MY_PICKS):
        avail[:,j]+= (gone_by>=pk).astype(float)
avail/=N
for j,pk in enumerate(MY_PICKS): board[f'p{pk}']=avail[:,j]
board.to_csv('out/board_with_survival_v5.csv',index=False)

print("\nSIMULATED availability (N=4000, keepers removed before pick 1). "
      "Directive 7: simulated numbers have run LOW against every checkable observation — treat as lower bounds.")
for pk in [8,17,32,41,56]:
    top=board[(board[f'p{pk}']>0.05)].nlargest(8,'vbd_rank_elig')[['player','pos','team_c','vbd','adp_pick','bye','injury_status',f'p{pk}']]
    print(f"\n--- pick {pk} ---")
    print(top.to_string(index=False,float_format=lambda x:f"{x:7.2f}"))
