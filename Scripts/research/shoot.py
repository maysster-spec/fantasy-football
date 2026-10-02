"""Render the CURRENT board at engine-driven states -- Matt's roster is what the tool would build."""
import sys, os, shutil, re
import numpy as np
from collections import Counter
KIT='/home/claude/work/kit'; sys.path.insert(0,KIT); os.chdir(KIT)
import live_draft as LD
eng=LD.Engine('board_v8_fixed.csv','ESPN_prerank_with_ids.csv'); LD.load_context()
b=eng.b.reset_index(drop=True); EID=b.espn_id.values
PICKS=list(LD.CLE.MY_PICKS); sd=0.111*b.adp_pick.values+5.40
OUT='/home/claude/work/shots'; os.makedirs(OUT,exist_ok=True)
rng=np.random.default_rng(4242)
order=[int(i) for i in np.argsort(b.eff_pick.values+rng.normal(0,sd))]
WANT={int(x) for x in sys.argv[1:]} or {8,89,113}
mine=[]; taken=set(); shapes=[]
for pk in PICKS:
    need=(pk-1)-len(taken)
    if need>0: taken.update([i for i in order if i not in taken][:need])
    # taken ALREADY holds Matt's players; adding them again made the feed 10 picks long by
    # round 11 and the strip said "0 skill turns left" at pick 128. Harness bug, not the board's.
    picks=[{'pid':int(EID[i]),'team':(9 if i in set(mine) else 100),'keeper':False} for i in taken]
    LD.step(eng, picks, 9)
    s=open('live_board.html',encoding='utf-8').read()
    trs=re.findall(r'<tr\b[^>]*>', s)
    cls=Counter(re.search(r'class="([^"]*)"',t).group(1) if 'class=' in t else '' for t in trs)
    st=re.search(r'<div class="pos-fill">(.*?)</div>', s, re.S)
    txt=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',st.group(1))).strip() if st else '(MISSING)'
    shapes.append((cls.get('pr',0), cls.get('tier',0)+cls.get('tier gh',0)))
    print('  pick %3d  rows=%d tiers=%d gof=%d strip=%d | %s'
          % (pk, cls.get('pr',0), cls.get('tier',0)+cls.get('tier gh',0),
             s.count('class="gof"'), bool(st), txt[:130]))
    if pk in WANT: shutil.copy('live_board.html', OUT+'/v3_%d.html'%pk)
    r=eng.recommend(pk, rollout_inner=20, top=8)
    if r: mine.append(int(r[0]['i'])); taken.add(int(r[0]['i']))
print('\n  SHAPES seen:', sorted(set(shapes)), '<- doc 139 requires exactly one')
