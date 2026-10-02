import pandas as pd, numpy as np, re, warnings; warnings.filterwarnings('ignore')
from scipy import stats as st
SUF=r'\b(jr|sr|ii|iii|iv|v)\b'
NICK={'joshua':'josh','mitchell':'mitch','christopher':'chris','nathaniel':'nate','benjamin':'ben','michael':'mike','zachary':'zach','matthew':'matt'}
def norm(s):
    s=str(s).lower().replace('.',' ').replace("'",'').replace('-',' ')
    s=re.sub(SUF,'',s); s=re.sub(r'[^a-z ]','',s); p=s.split()
    if p: p[0]=NICK.get(p[0],p[0])
    return ''.join(p)
def pts(y):
    w=pd.read_csv(f'/home/claude/nfl/w{y}.csv',low_memory=False)
    w=w[(w.season_type=='REG')&(w.week<=14)]
    g=w.groupby(['player_display_name','position']).agg(
        py=('passing_yards','sum'),ptd=('passing_tds','sum'),pint=('passing_interceptions','sum'),
        ry=('rushing_yards','sum'),rtd=('rushing_tds','sum'),
        rec=('receptions','sum'),recy=('receiving_yards','sum'),rectd=('receiving_tds','sum'),
        f1=('sack_fumbles_lost','sum'),f2=('rushing_fumbles_lost','sum'),f3=('receiving_fumbles_lost','sum'),
        t1=('passing_2pt_conversions','sum'),t2=('rushing_2pt_conversions','sum'),t3=('receiving_2pt_conversions','sum')
    ).reset_index()
    g['pf']=(0.04*g.py+6*g.ptd-2*g.pint+0.1*g.ry+6*g.rtd+0.5*g.rec+0.1*g.recy+6*g.rectd
             -2*(g.f1+g.f2+g.f3)+2*(g.t1+g.t2+g.t3))
    g['k']=g.player_display_name.map(norm); g['Year']=y
    return g[['k','position','pf','Year']]
P=pd.concat([pts(y) for y in range(2021,2026)])
d=pd.read_csv('draft_hist.csv')
d=d[d.adp.notna()&d.Pos.isin(['QB','RB','WR','TE'])]
m=d.merge(P,on=['k','Year'],how='left')
m=m[m.pf.notna()].copy()
# positional finish rank vs ADP-implied positional rank, within each season's drafted pool
m['fin_rank']=m.groupby(['Year','Pos']).pf.rank(ascending=False)
m['adp_rank']=m.groupby(['Year','Pos']).adp.rank()
m['beat']=m.adp_rank-m.fin_rank        # + = finished BETTER than his price implied
print('=== DOES A DRAFT-DAY REACH PAY?  league-wide, 2021-2025, weeks 1-14, §2 scoring')
print('   n=%d picks with both a preseason ADP and a measurable season'%len(m))
r,p=st.pearsonr(m.reach,m.beat)
print('   corr(reach, positional-finish beat) = %+.3f  p=%.4f'%(r,p))
sl,ic,rr,pp,se=st.linregress(m.reach,m.beat)
print('   slope %+.3f positional slots gained per pick of reach  CI[%+.3f, %+.3f]'%(sl,sl-1.96*se,sl+1.96*se))
print()
print('=== AND FOR YOU SPECIFICALLY')
mm=m[m.Manager.astype(str).str.contains('Matt Mays',na=False)]
oth=m[~m.Manager.astype(str).str.contains('Matt Mays',na=False)]
r2,p2=st.pearsonr(mm.reach,mm.beat)
print('   Matt Mays n=%d   corr(reach, beat) = %+.3f  p=%.3f'%(len(mm),r2,p2))
print('   his reaches (>15 picks early) n=%d  mean beat %+.1f positional slots'%((mm.reach>15).sum(),mm[mm.reach>15].beat.mean()))
print('   his falls  (>15 picks late)  n=%d  mean beat %+.1f'%((mm.reach<-15).sum(),mm[mm.reach<-15].beat.mean()))
print('   everyone else, reaches >15:  n=%d  mean beat %+.1f'%((oth.reach>15).sum(),oth[oth.reach>15].beat.mean()))
print()
print('=== HOW EVERY MANAGER DID ON REACHES (n>=8 reaches only)')
for mgr,g in m.groupby('Manager'):
    rr_=g[g.reach>15]
    if len(rr_)<8: continue
    print('   %-26s reaches n=%2d  mean beat %+6.1f  |  all picks corr %+.3f (n=%d)'%(
        mgr[:26],len(rr_),rr_.beat.mean(),g.reach.corr(g.beat),len(g)))
m.to_csv('reach_test.csv',index=False)
