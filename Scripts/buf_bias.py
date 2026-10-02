import pandas as pd, numpy as np, re, warnings; warnings.filterwarnings('ignore')
from scipy import stats as st
S='/mnt/user-data/uploads/2026/Source/'
SUF=r'\b(jr|sr|ii|iii|iv|v)\b'
NICK={'joshua':'josh','mitchell':'mitch','christopher':'chris','nathaniel':'nate','benjamin':'ben','michael':'mike','zachary':'zach','matthew':'matt'}
def norm(s):
    s=str(s).lower().replace('.',' ').replace("'",'').replace('-',' ')
    s=re.sub(SUF,'',s); s=re.sub(r'[^a-z ]','',s); p=s.split()
    if p: p[0]=NICK.get(p[0],p[0])
    return ''.join(p)
d=pd.read_csv(S+'draft_history_2021_2025.csv')
d=d[d.Keeper!=True]                      # true selections only, §4.7
d['k']=d.Player.map(norm)
d['buf']=d.NFL.astype(str).str.upper().isin(['BUF'])
adp={}
for y in range(2021,2026):
    a=pd.read_csv(S+f'adp_registry/preseason_adp_{y}.csv'); a['k']=a.player.map(norm)
    adp[y]=dict(zip(a.k,a.adp))
d['adp']=[adp.get(y,{}).get(k,np.nan) for y,k in zip(d.Year,d.k)]
d['reach']=d.adp-d.Pick          # + = drafted EARLIER than ADP (a reach)
print('=== BILLS BIAS BY MANAGER — true selections only, 2021-2025')
print('   reach = preseason ADP minus actual pick.  POSITIVE = took him earlier than the market.')
print('   n(BUF) counts Bills players a manager drafted.\n')
print('%-26s %5s %6s   %8s %8s  %8s'%('manager','picks','n(BUF)','BUF reach','other','difference'))
rows=[]
for mgr,g in d.groupby('Manager'):
    b=g[g.buf & g.adp.notna()]; o=g[~g.buf & g.adp.notna()]
    if len(o)<10: continue
    diff=b.reach.mean()-o.reach.mean() if len(b) else np.nan
    rows.append((mgr,len(g),len(b),b.reach.mean() if len(b) else np.nan,o.reach.mean(),diff))
for r in sorted(rows,key=lambda x:-(x[5] if x[5]==x[5] else -99)):
    print('%-26s %5d %6d   %8s %8.1f  %8s'%(r[0],r[1],r[2],
        ('%.1f'%r[3]) if r[3]==r[3] else '--',r[4],('%+.1f'%r[5]) if r[5]==r[5] else '--'))
print()
b=d[d.buf&d.adp.notna()]; o=d[~d.buf&d.adp.notna()]
t,p=st.ttest_ind(b.reach,o.reach,equal_var=False)
print('   LEAGUE-WIDE: Bills players taken %.1f picks early vs %.1f for everyone else'%(b.reach.mean(),o.reach.mean()))
print('   difference %+.1f picks, Welch p=%.3f  (n=%d BUF picks vs %d)'%(b.reach.mean()-o.reach.mean(),p,len(b),len(o)))
print()
print('=== WHICH BILLS WENT, AND TO WHOM (biggest reaches)')
for _,r in b.nlargest(12,'reach').iterrows():
    print('   %d  %-22s %-26s pick %3d  adp %5.1f  reach %+5.1f'%(r.Year,r.Player,r.Manager[:26],r.Pick,r.adp,r.reach))
d.to_csv('draft_hist.csv',index=False)
