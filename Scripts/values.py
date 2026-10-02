import pandas as pd, numpy as np, re, warnings; warnings.filterwarnings('ignore')
from scipy.stats import norm as N
m=pd.read_csv('rankers.csv')
ctx=pd.read_csv('/home/claude/out/player_context.csv')
m=m.merge(ctx[['ESPN_ID','job_ceil','why','who','quote','lean']],left_on='espn_id',right_on='ESPN_ID',how='left',suffixes=('','_c'))
g25=pd.read_csv('/home/claude/env/ship/games_2025.csv')[['espn_id','g25']]
m=m.merge(g25,on='espn_id',how='left')
PICKS=[8,17,32,41,56,65,80,89,104,113,128,137]
EFF  =[8,17,35,51,66,75,91,100,115,124,140,149]
def sd(a): return 0.111*a+5.40
def surv(eff,pick):                      # P(still there at this pick) -- dispersion only, §4.15 optimistic
    return float(1-N.cdf(pick,loc=eff,scale=sd(eff)))
m=m[(m.proj_leaguepts>0)&(m.pos.isin(['QB','RB','WR','TE']))&(m.adp_pick<168)].copy()
m['both']=m[['Boone','Harmon']].mean(axis=1)
m['gap']=m.adp_pick-m.both
# where does he FIRST become a realistic take, and where is he likely gone
# take_at = the LATEST of his picks where the player is still a coin flip or better to be there.
# Taking him earlier than that is a reach; later is a miss.  §4.15: dispersion alone runs
# OPTIMISTIC, so every one of these is a ceiling -- he will often be gone a pick sooner.
def take_at(eff):
    out=None
    for p,e in zip(PICKS,EFF):
        if surv(eff,e)>=0.50: out=p
    return out
def p_at(eff,p):
    e=dict(zip(PICKS,EFF))[p]; return surv(eff,e)
m['take_at']=m.eff_pick.map(take_at)
m['p_there']=[p_at(e,t) if pd.notna(t) else np.nan for e,t in zip(m.eff_pick,m.take_at)]
# injury-created path: a same-team, same-position player carries an OUT/PUP/exempt/season flag
BLOCK=r'(?i)(EXEMPT|PUP|OUT_WEEKS|torn|Achilles|season-ending|placed on)'
hurt=m[m.why_c.astype(str).str.contains(BLOCK,na=False)][['team_c','pos','player']]
hmap={}
for _,r in hurt.iterrows(): hmap.setdefault((r.team_c,r.pos),[]).append(r.player)
def opened(r):
    o=[x for x in hmap.get((r.team_c,r.pos),[]) if x!=r.player]
    return '; '.join(o)
m['opened_by']=m.apply(opened,axis=1)
# the evidence count -- NOT a model.  each flag is one independent source saying the same thing.
def ev(r):
    e=[]
    if r.board_rank < r.adp_pick-12: e.append('BOARD')            # our VBD is well ahead of his price
    if r.gap>=25: e.append('ANALYSTS')                            # Boone+Harmon mean, >75th pct of band
    if r.buy==1: e.append('BUY')
    if str(r.job) in ('UNSETTLED','contested') and pd.notna(r.job_ceil) and r.job_ceil>=150: e.append('JOB')
    if r.opened_by: e.append('INJURY-OPENED')
    return e
m['ev']=m.apply(ev,axis=1); m['nev']=m.ev.map(len)
def caution(r):
    c=[]
    if str(r.grade)=='AVOID': c.append('AVOID')
    elif str(r.grade)=='DISCOUNT': c.append('DISC')
    if pd.notna(r.g25) and 0<r.g25<=12: c.append('%dg'%r.g25)
    if str(r.lean).startswith('lean bear') or str(r.lean).startswith('strongly bear'): c.append('bear')
    return ' '.join(c)
m['caution']=m.apply(caution,axis=1)
out=m[(m.nev>=2)&m.take_at.notna()].copy()
out=out.sort_values(['take_at','nev','gap'],ascending=[True,False,False])
print('=== VALUE LIST — players with 2+ independent reasons, gated to picks you can reach')
print('    %d players across %d of your picks\n'%(len(out),out.take_at.nunique()))
for p in PICKS:
    g=out[out.take_at==p]
    if not len(g): continue
    print('--- PICK %d ---'%p)
    for _,r in g.head(7).iterrows():
        print('  %-23s %-3s adp%3.0f brd#%3.0f  p=%.2f  %-30s %s'%(
            r.player,r.pos,r.adp_pick,r.board_rank,r.p_there,
            '+'.join(r.ev),('[%s]'%r.caution) if r.caution else ''))
    print()
out.to_csv('values.csv',index=False)
