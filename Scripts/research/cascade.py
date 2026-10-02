"""WHERE IS THE EDGE, PICK BY PICK?
Two questions, one harness:
  (1) cascade  -- does the position taken at 8 change the SHAPE of the rest of the draft?
  (2) margin   -- at which of the 12 picks does the engine actually decide, and at which
                  is it indifferent (= the picks where Matt's own judgement is the input)?
Rooms are drawn under 4.12's affine noise on eff_pick. Opponents fill every slot up to the
pick; the engine drafts Matt's seat.
"""
import sys, os, collections, time
import numpy as np, pandas as pd
KIT='/home/claude/work/lb/new'; sys.path.insert(0,KIT); os.chdir(KIT)
import live_draft as LD

eng=LD.Engine(os.path.join(KIT,'board_v8_fixed.csv'),os.path.join(KIT,'ESPN_prerank_with_ids.csv'))
LD.load_context()
b=eng.b.reset_index(drop=True)
EID=b.espn_id.values
PICKS=list(LD.CLE.MY_PICKS)
sd=0.111*b.adp_pick.values+5.40
ROOMS=int(sys.argv[1]) if len(sys.argv)>1 else 25
INNER=int(sys.argv[2]) if len(sys.argv)>2 else 12

def run(force_pos_at_8, rng, margins=None):
    noisy=b.eff_pick.values+rng.normal(0,sd)
    order=[int(i) for i in np.argsort(noisy)]
    mine=[]; taken=set(); seq=[]
    for pk in PICKS:
        # top the room up so exactly pk-1 players are off the board before this pick
        need=(pk-1)-len(taken)
        if need>0:
            fresh=[i for i in order if i not in taken][:need]
            taken.update(fresh)
        eng.set_taken([int(EID[i]) for i in taken], [int(EID[i]) for i in mine])
        recs=eng.recommend(pk, rollout_inner=INNER, top=8)
        if not recs: break
        if margins is not None and len(recs)>1:
            margins[pk].append(recs[0]['roll']-recs[1]['roll'])
            margins[('who',pk)].append(recs[0]['player'])
        pick=recs[0]
        if pk==8 and force_pos_at_8:
            alt=[r for r in recs if r['pos']==force_pos_at_8]
            if alt: pick=alt[0]
        row=int(pick['i']); mine.append(row); taken.add(row)
        seq.append((pk,pick['pos'],pick['player']))
    return seq

t0=time.time()
for label,force in (("the engine's own pick 8 (WR)",None),("FORCED RB at pick 8",'RB')):
    rng=np.random.default_rng(717)
    byp=collections.defaultdict(collections.Counter)
    who=collections.defaultdict(collections.Counter)
    marg=collections.defaultdict(list)
    finals=collections.Counter()
    for r in range(ROOMS):
        seq=run(force,rng,marg)
        for pk,pos,pl in seq:
            byp[pk][pos]+=1; who[pk][pl]+=1
        finals[''.join(p[0] for _,p,_ in seq[:6])]+=1
    print(f"\n{'='*74}\n {label} - {ROOMS} rooms, rollout_inner={INNER}\n{'='*74}")
    print(f"  {'pick':>5} {'QB':>6}{'RB':>6}{'WR':>6}{'TE':>6}   {'margin #1v#2':>12}  most-taken player")
    for pk in PICKS:
        c=byp[pk]; tot=sum(c.values()) or 1
        m=marg[pk]; mm=np.mean(m) if m else float('nan')
        top=who[pk].most_common(1)
        tp=f"{top[0][0]} ({100*top[0][1]/tot:.0f}%)" if top else '-'
        print(f"  {pk:>5} "+''.join(f'{100*c[p]/tot:>5.0f}%' for p in ('QB','RB','WR','TE'))
              +f"   {mm:>12.2f}  {tp}")
    print("  opening six:")
    for shape,n in finals.most_common(4):
        print(f"     {shape:<8} {n} of {ROOMS}")
print(f"\n[{time.time()-t0:.0f}s]")
