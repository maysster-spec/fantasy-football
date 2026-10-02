"""THE FACTORIAL: which of the two levers actually moves Matt's picks?
  A   frozen           08-23 points, 08-23 ADP           (the shipped board)
  P   re-priced        09-03 points, 08-23 ADP           4.1 levels HELD (4.1b)
  D   re-timed         08-23 points, 09-03 ADP           refresh_adp.py's lever
  PD  both
Nothing is written to the live board. Each board is run through the REAL Engine at all 12 of
Matt's picks against one fixed opponent room, and the top recommendation compared.
"""
import os, sys, re, shutil
import numpy as np, pandas as pd

BB='/home/claude/work/bb'; KIT='/home/claude/work/lb/new'
SRC='/mnt/user-data/uploads/2026/Source/'
PULL=SRC+'espn_projections_2026_20260903_0902.csv'
REPL={'QB':341.602860180,'RB':168.588855840,'WR':163.539573570,'TE':140.294884170}

def key(n):
    import unicodedata as u
    n=u.normalize('NFKD',str(n)).encode('ascii','ignore').decode()
    n=re.sub(r"[^A-Za-z ]",'',n)
    n=re.sub(r'(?i)\b(jr|sr|ii|iii|iv|v)\b','',n)
    return ' '.join(n.split()).lower()

A=pd.read_csv('/home/claude/work/lb/new/board_v8_fixed.csv')
p=pd.read_csv(PULL); p.columns=[c.replace('﻿','') for c in p.columns]
p=p[['espn_id','proj_2026','espn_adp']].dropna(subset=['espn_id']).drop_duplicates('espn_id')
kp=pd.read_csv(os.path.join(BB,'actual_keepers.csv'))
news=pd.read_csv(os.path.join(BB,'news_overrides.csv'))
nid=set(news[news[[c for c in news.columns if 'action' in c.lower()][0]]
             .astype(str).str.strip().str.lower().isin(('out','remove'))].espn_id)

m=A.merge(p,on='espn_id',how='left')

def make(newproj, newadp):
    o=A.copy()
    if newproj:
        o['proj_leaguepts']=np.where(m.proj_2026.notna(), m.proj_2026, A.proj_leaguepts)
        o.loc[o.espn_id.isin(nid),'proj_leaguepts']=0.0     # step 7, re-applied LAST
        o['vbd']=o.proj_leaguepts-o.pos.map(REPL)
        o['rank']=o.vbd.rank(ascending=False,method='first').astype(int)
    if newadp:
        o['adp_pick']=np.where(m.espn_adp.notna(), m.espn_adp.round(2), A.adp_pick)
        # gone_ahead = keepers whose ADP is ahead of this player, on the SAME pull
        pk=p.merge(kp.assign(k=kp.Player.map(key)),
                   left_on=p.Player.map(key) if 'Player' in p.columns else p.espn_id,
                   right_on='k', how='inner') if 'Player' in p.columns else None
        kadp=[]
        praw=pd.read_csv(PULL); praw['k']=praw.Player.map(key)
        km={r.k:r.espn_adp for _,r in praw.iterrows()}
        for nm in kp.Player:
            v=km.get(key(nm))
            assert v is not None and v==v, f'keeper {nm} has no ADP in the pull'
            kadp.append(float(v))
        kadp=np.array(sorted(kadp))
        o['gone_ahead']=[int((kadp<a).sum()) for a in o.adp_pick]
        o['eff_pick']=(o.adp_pick-o.gone_ahead).round(2)
    return o.sort_values('rank').reset_index(drop=True)

BOARDS={'A':A.copy(),'P':make(True,False),'D':make(False,True),'PD':make(True,True)}
for t,bd in BOARDS.items():
    fn=os.path.join(BB,f'board_{t}.csv'); bd.to_csv(fn,index=False)
print('  boards written:', ', '.join(BOARDS))
kk=pd.read_csv(PULL); kk['k']=kk.Player.map(key)
km={r.k:r.espn_adp for _,r in kk.iterrows()}
print('  keeper ADPs on the 09-03 pull:',
      ', '.join(f'{n.split()[-1]} {km[key(n)]:.1f}' for n in kp.Player))

# ---- run the REAL engine on each board, one fixed room ----
sys.path.insert(0,KIT); os.chdir(KIT)
import live_draft as LD
PICKS=list(LD.CLE.MY_PICKS)
res={}
for t in BOARDS:
    src=os.path.join(BB,f'board_{t}.csv'); dst=os.path.join(KIT,f'_tmp_{t}.csv')
    shutil.copy(src,dst)
    eng=LD.Engine(dst, os.path.join(KIT,'ESPN_prerank_with_ids.csv'))
    b=eng.b.reset_index(drop=True)
    rng=np.random.default_rng(4242)
    sd=0.111*b.adp_pick.values+5.40
    order=[int(i) for i in np.argsort(b.eff_pick.values+rng.normal(0,sd))]
    mine=[]; taken=set(); out=[]
    for pk in PICKS:
        need=(pk-1)-len(taken)
        if need>0: taken.update([i for i in order if i not in taken][:need])
        eng.set_taken([int(b.espn_id.iloc[i]) for i in taken],
                      [int(b.espn_id.iloc[i]) for i in mine])
        r=eng.recommend(pk, rollout_inner=24, top=8)
        if not r: break
        out.append((r[0]['player'], r[0]['pos'], round(r[0]['roll']-r[1]['roll'],2)))
        mine.append(int(r[0]['i'])); taken.add(int(r[0]['i']))
    res[t]=out
    os.remove(dst)

print(f"\n{'pick':>5}  {'A  frozen':<26}{'P  re-priced':<26}{'D  re-timed':<26}{'PD both':<26}")
for j,pk in enumerate(PICKS):
    row=f'{pk:>5}  '
    for t in ('A','P','D','PD'):
        v=res[t][j] if j<len(res[t]) else ('-','','')
        mark='' if t=='A' or (j<len(res[t]) and v[0]==res['A'][j][0]) else ' *'
        row+=f"{v[0][:20]+mark:<26}"
    print(row)
print("\n  * = differs from the frozen board at that pick")
for t in ('P','D','PD'):
    n=sum(1 for j in range(min(len(res[t]),len(res['A']))) if res[t][j][0]!=res['A'][j][0])
    e=sum(1 for j in range(4) if res[t][j][0]!=res['A'][j][0])
    print(f"  {t:<3} changes {n} of 12 picks   ({e} of them at 8/17/32/41)")
