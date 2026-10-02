"""Does the 'goes first' mark ever fire, and is the adp<168 gate killing it?
Engine-driven rooms (Matt takes the engine's own pick), all 12 skill picks."""
import sys, os, collections
import numpy as np
KIT='/home/claude/work/kit'; sys.path.insert(0,KIT); os.chdir(KIT)
import live_draft as LD
eng=LD.Engine(os.path.join(KIT,'board_v8_fixed.csv'),os.path.join(KIT,'ESPN_prerank_with_ids.csv'))
LD.load_context()
b=eng.b.reset_index(drop=True); EID=b.espn_id.values
PICKS=list(LD.CLE.MY_PICKS); sd=0.111*b.adp_pick.values+5.40
ROOMS=int(sys.argv[1]) if len(sys.argv)>1 else 12
cnt=collections.defaultdict(lambda: collections.Counter())
for s in range(ROOMS):
    rng=np.random.default_rng(500+13*s)
    order=[int(i) for i in np.argsort(b.eff_pick.values+rng.normal(0,sd))]
    mine=[]; taken=set()
    for pk in PICKS:
        need=(pk-1)-len(taken)
        if need>0: taken.update([i for i in order if i not in taken][:need])
        eng.set_taken([int(EID[i]) for i in taken],[int(EID[i]) for i in mine])
        r=eng.recommend(pk, rollout_inner=20, top=8)
        if not r: break
        nxt=next((p for p in PICKS if p>pk), None)
        shown=r[:12]; t=shown[0]
        for x in shown[1:]:
            tie = abs(x['cost'])<=1.5
            gap = (t['p_next']-x['p_next'])>=0.20
            real = float(x.get('adp',999))<168
            if tie: cnt[pk]['tie']+=1
            if tie and gap and nxt is not None: cnt[pk]['ungated']+=1
            if tie and gap and real and nxt is not None: cnt[pk]['gated']+=1
        cnt[pk]['states']+=1
        mine.append(int(t['i'])); taken.add(int(t['i']))
print(f"\n{ROOMS} engine-driven rooms\n")
print(f"  {'pick':>5}{'tied rows':>11}{'would fire (no adp gate)':>26}{'fires WITH adp<168 gate':>26}")
for pk in PICKS:
    c=cnt[pk]; st=max(c['states'],1)
    print(f"  {pk:>5}{c['tie']/st:>11.1f}{c['ungated']/st:>26.2f}{c['gated']/st:>26.2f}")
tot=sum(cnt[p]['gated'] for p in PICKS); un=sum(cnt[p]['ungated'] for p in PICKS)
st=sum(cnt[p]['states'] for p in PICKS)
print(f"\n  per board render: {un/st:.2f} marks ungated, {tot/st:.2f} gated  ({st} states)")
