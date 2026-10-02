"""WHAT DESERVES THE INK? Measured, not designed.
At each of Matt's picks, across many rooms, compare the two quantities the board could
emphasise: how far apart the candidates are on the engine's own score (`cost vs #1`), and
how far apart they are on survival (`p(next)`). Also: how often the top two are a TIE the
engine cannot separate while their survival differs a lot -- the case where p(next) is the
only real information on the row and currently carries no visual weight at all.
"""
import sys, os, collections, time
import numpy as np, pandas as pd
KIT='/home/claude/work/kit'; sys.path.insert(0,KIT); os.chdir(KIT)
import live_draft as LD
eng=LD.Engine(os.path.join(KIT,'board_v8_fixed.csv'),os.path.join(KIT,'ESPN_prerank_with_ids.csv'))
LD.load_context()
b=eng.b.reset_index(drop=True); EID=b.espn_id.values
PICKS=list(LD.CLE.MY_PICKS)
sd=0.111*b.adp_pick.values+5.40
ROOMS=int(sys.argv[1]) if len(sys.argv)>1 else 12
INNER=int(sys.argv[2]) if len(sys.argv)>2 else 24
acc=collections.defaultdict(lambda: collections.defaultdict(list))
forced=collections.Counter(); t0=time.time()
for s in range(ROOMS):
    rng=np.random.default_rng(9000+31*s)
    order=[int(i) for i in np.argsort(b.eff_pick.values+rng.normal(0,sd))]
    mine=[]; taken=set()
    for pk in PICKS:
        need=(pk-1)-len(taken)
        if need>0: taken.update([i for i in order if i not in taken][:need])
        eng.set_taken([int(EID[i]) for i in taken],[int(EID[i]) for i in mine])
        pl=sum(1 for p in PICKS if p>=pk)
        allowed=eng.legal(pl)
        r=eng.recommend(pk, rollout_inner=INNER, top=8)
        if not r: break
        shown=r[:12]
        cost=[x['cost'] for x in shown]; pn=[x['p_next'] for x in shown]
        acc[pk]['marg'].append(-shown[1]['cost'] if len(shown)>1 else 0.0)
        acc[pk]['cspread'].append(max(cost)-min(cost))
        acc[pk]['pspread'].append((max(pn)-min(pn))*100)
        # rows the engine cannot separate from #1
        ties=[x for x in shown[1:] if abs(x['cost'])<=1.5]
        acc[pk]['nties'].append(len(ties))
        if ties:
            acc[pk]['tie_psplit'].append(max(abs(x['p_next']-shown[0]['p_next']) for x in ties)*100)
        if len(allowed)<4: forced[pk]+=1
        mine.append(int(shown[0]['i'])); taken.add(int(shown[0]['i']))
def m(pk,k): v=acc[pk][k]; return float(np.mean(v)) if v else float('nan')
print(f"\n{ROOMS} rooms, rollout_inner={INNER}, CURRENT board (09-03 ADP)\n")
print(f"  {'pick':>5}{'margin #1v#2':>14}{'cost spread':>13}{'p(next) spread':>16}"
      f"{'rows tied to #1':>17}{'their p(next) gap':>19}")
for pk in PICKS:
    print(f"  {pk:>5}{m(pk,'marg'):>14.2f}{m(pk,'cspread'):>13.2f}{m(pk,'pspread'):>15.0f}pp"
          f"{m(pk,'nties'):>17.1f}{m(pk,'tie_psplit'):>17.0f}pp")
print(f"\n  picks where the engine was position-CONSTRAINED (fewer than 4 positions legal):")
print('   ', dict(forced) or 'none')
print(f"[{time.time()-t0:.0f}s]")
