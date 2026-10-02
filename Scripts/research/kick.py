#!/usr/bin/env python3
"""Matt, 2026-09-10: "i sometimes remember to look for a kicker who is performing well on waivers
and pick him up if the value seems worth it. And then keep that kicker."

TESTABLE FORM, stated before running (0.5a2). This is a DIFFERENT object from doc 213, which asked
whether a team's kicking tendency carries from one SEASON to the next (it barely does, r=+0.200).
His claim is about WITHIN one season: does what a kicker has done through week W predict what he
does after week W, and is the edge durable enough to keep him.
  T1 PERSISTENCE. POPULATION: team-kicker seasons 2021-2025, weeks 1-14, scored under this league's
     own kicker rules. PREDICTOR: points per game through week W. OUTCOME: points per game from
     W+1 to 14. DIRECTION: hot early -> higher later.
  T2 THE SWAP. At week W, the best-scoring kicker NOT drafted in this league that year, against the
     median DRAFTED kicker. OUTCOME: rest-of-season points per game. This is the move he described.
  T3 DURABILITY. Same swap, split into the next four weeks and everything after, because "keep that
     kicker" is a claim about weeks 9-14 and not about the week you claim him.
"""
import csv, collections, statistics as st, math, random
rows=[r for r in csv.DictReader(open('/home/claude/k_weekly_2021_2025.csv',encoding='utf-8-sig'))]
K=collections.defaultdict(dict)                      # (season, team) -> week -> pts
for r in rows:
    w=int(r['week'])
    if 1<=w<=14: K[(int(r['season']),r['team'])][w]=float(r['kick'])
TEAMFIX={'Jax':'JAX','Was':'WAS','Wsh':'WAS','Lar':'LA','Lac':'LAC','Kan':'KC','Kc':'KC','Sfo':'SF',
 'Sf':'SF','Tam':'TB','Tb':'TB','Gnb':'GB','Gb':'GB','Nor':'NO','No':'NO','Nwe':'NE','Ne':'NE',
 'Lv':'LV','Lvr':'LV','Oak':'LV'}
drafted=collections.defaultdict(set)                 # season -> {team}
for r in csv.DictReader(open('/mnt/user-data/uploads/2026/Source/draft_history_2021_2025.csv',encoding='utf-8-sig')):
    if r['Pos']=='K':
        t=(r['NFL'] or '').strip()
        drafted[int(r['Year'])].add(TEAMFIX.get(t.title(), t.upper()))
def pear(xs,ys):
    n=len(xs); mx,my=st.mean(xs),st.mean(ys)
    sx=math.sqrt(sum((x-mx)**2 for x in xs)); sy=math.sqrt(sum((y-my)**2 for y in ys))
    if sx==0 or sy==0: return 0.0,1.0,n
    r=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/(sx*sy)
    t=r*math.sqrt((n-2)/max(1e-9,1-r*r))
    return r, 2*(1-0.5*(1+math.erf(abs(t)/math.sqrt(2)))), n
def ppg(key, a, b):
    v=[K[key][w] for w in range(a,b+1) if w in K[key]]
    return (st.mean(v), len(v)) if len(v)>=2 else (None,0)

allw=[v for d in K.values() for v in d.values()]
print(f"  a kicker week in this league: mean {st.mean(allw):.2f}, sd {st.pstdev(allw):.2f}, n={len(allw)}")
print("\n"+"="*74); print("  T1  DOES THE FIRST PART OF A SEASON PREDICT THE REST?"); print("="*74)
print(f"  {'through wk':>11}{'n':>6}{'r':>9}{'p':>9}   hot half ppg after | cold half ppg after")
for Wc in (4,6,8,10):
    xs,ys,pairs=[],[],[]
    for key in K:
        a,na=ppg(key,1,Wc); b,nb=ppg(key,Wc+1,14)
        if a is None or b is None or na<Wc-1 or nb<2: continue
        xs.append(a); ys.append(b); pairs.append((a,b))
    r,p,n=pear(xs,ys)
    pairs.sort(); half=len(pairs)//2
    hot=st.mean([b for a,b in pairs[half:]]); cold=st.mean([b for a,b in pairs[:half]])
    print(f"  {Wc:>11}{n:>6}{r:>+9.3f}{p:>9.4f}   {hot:>18.2f} | {cold:>19.2f}   (gap {hot-cold:+.2f})")

print("\n"+"="*74); print("  T2  THE SWAP HE DESCRIBES, AGAINST HOLDING WHAT YOU DRAFTED"); print("="*74)
print(f"  {'at week':>8}{'n seasons':>11}{'best free so far':>18}{'median drafted':>16}{'gap':>8}")
for Wc in (4,6,8,10):
    gaps=[]; bestafter=[]; medafter=[]
    for season in sorted(drafted):
        if season not in {s for s,_ in K}: continue
        own=drafted[season]
        freek=[(ppg((season,t),1,Wc)[0], t) for t in {tm for s,tm in K if s==season} if t not in own]
        freek=[(a,t) for a,t in freek if a is not None]
        heldk=[(ppg((season,t),1,Wc)[0], t) for t in own if (season,t) in K]
        heldk=[(a,t) for a,t in heldk if a is not None]
        if len(freek)<5 or len(heldk)<5: continue
        best=max(freek)[1]
        ba=ppg((season,best),Wc+1,14)[0]
        ha=[ppg((season,t),Wc+1,14)[0] for _,t in heldk]
        ha=[x for x in ha if x is not None]
        if ba is None or not ha: continue
        bestafter.append(ba); medafter.append(st.median(ha)); gaps.append(ba-st.median(ha))
    if gaps:
        print(f"  {Wc:>8}{len(gaps):>11}{st.mean(bestafter):>18.2f}{st.mean(medafter):>16.2f}"
              f"{st.mean(gaps):>+8.2f}   per-season gaps {[round(g,1) for g in gaps]}")

print("\n"+"="*74); print("  T3  AND DOES IT LAST -- 'AND THEN KEEP THAT KICKER'"); print("="*74)
print(f"  {'at week':>8}{'next 4 weeks':>15}{'everything after':>19}")
for Wc in (4,6):
    n4,nr=[],[]
    for season in sorted(drafted):
        own=drafted[season]
        freek=[(ppg((season,t),1,Wc)[0], t) for t in {tm for s,tm in K if s==season} if t not in own]
        freek=[(a,t) for a,t in freek if a is not None]
        heldk=[t for t in own if (season,t) in K]
        if len(freek)<5 or len(heldk)<5: continue
        best=max(freek)[1]
        for lab,rng,acc in (('n4',(Wc+1,Wc+4),n4), ('nr',(Wc+5,14),nr)):
            b=ppg((season,best),*rng)[0]
            h=[ppg((season,t),*rng)[0] for t in heldk]; h=[x for x in h if x is not None]
            if b is not None and h: acc.append(b-st.median(h))
    f=lambda v: f"{st.mean(v):+.2f} (n={len(v)})" if v else "-"
    print(f"  {Wc:>8}{f(n4):>15}{f(nr):>19}")

print("\n"+"="*74)
print("  T2b  MORE POWER: the top THREE free kickers, not just the best, and a bootstrap")
print("="*74)
random.seed(7)
for Wc in (6,8):
    gaps=[]
    for season in sorted(drafted):
        own=drafted[season]
        freek=[(ppg((season,t),1,Wc)[0], t) for t in {tm for s,tm in K if s==season} if t not in own]
        freek=sorted([(a,t) for a,t in freek if a is not None], reverse=True)
        heldk=[t for t in own if (season,t) in K]
        ha=[ppg((season,t),Wc+1,14)[0] for t in heldk]; ha=[x for x in ha if x is not None]
        if len(freek)<5 or len(ha)<5: continue
        med=st.median(ha)
        for _,t in freek[:3]:
            a=ppg((season,t),Wc+1,14)[0]
            if a is not None: gaps.append(a-med)
    bs=[st.mean([random.choice(gaps) for _ in gaps]) for _ in range(4000)]
    bs.sort()
    win=sum(1 for g in gaps if g>0)/len(gaps)
    print(f"  through week {Wc}: n={len(gaps)} swaps   mean {st.mean(gaps):+.2f}/wk   "
          f"median {st.median(gaps):+.2f}   95% CI [{bs[100]:+.2f}, {bs[3900]:+.2f}]   "
          f"beat the median holder {win:.0%} of the time")

print("\n"+"="*74)
print("  T2c  FALSIFIER: is it the SIGNAL, or just that any free kicker beats a drafted one?")
print("="*74)
for Wc in (6,8):
    top,rand=[],[]
    for season in sorted(drafted):
        own=drafted[season]
        freek=[(ppg((season,t),1,Wc)[0], t) for t in {tm for s,tm in K if s==season} if t not in own]
        freek=sorted([(a,t) for a,t in freek if a is not None], reverse=True)
        heldk=[t for t in own if (season,t) in K]
        ha=[ppg((season,t),Wc+1,14)[0] for t in heldk]; ha=[x for x in ha if x is not None]
        if len(freek)<5 or len(ha)<5: continue
        med=st.median(ha)
        for _,t in freek[:3]:
            a=ppg((season,t),Wc+1,14)[0]
            if a is not None: top.append(a-med)
        for _,t in random.sample(freek, 3):
            a=ppg((season,t),Wc+1,14)[0]
            if a is not None: rand.append(a-med)
    print(f"  through week {Wc}:  TOP-3 by what they have done {st.mean(top):+.2f}/wk   "
          f"|  THREE AT RANDOM off the same free list {st.mean(rand):+.2f}/wk   "
          f"|  the signal is worth {st.mean(top)-st.mean(rand):+.2f}")
