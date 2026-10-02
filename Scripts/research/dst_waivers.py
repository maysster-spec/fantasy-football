#!/usr/bin/env python3
"""THE D/ST WAIVER HIT RATE BY WEEK -- the 20.2% of the wire SECTION 4.31 excluded."""
import csv, re, collections, statistics as st, itertools, random

SRC='/mnt/user-data/uploads/2026/Source/'
# THE MAP, FROM HIS OWN PULL -- not typed from memory (SECTION 3).
espn={}
for r in csv.DictReader(open(SRC+'espn_projections_2026_20260907_1258.csv',encoding='utf-8-sig')):
    i=str(r.get('espn_id','')).strip()
    if i.startswith('-') and i[1:].isdigit():
        espn[int(i)]=r['team'].strip()
print(f"D/ST id map: {len(espn)} teams from the 2026 pull")

# ESPN abbreviations vs nflverse. ASSERT the join; never default it (doc 251).
ALIAS={'WSH':'WAS','LAR':'LA','OAK':'LV','SD':'LAC','STL':'LA','JAC':'JAX'}
def nfl(t): return ALIAS.get(t,t)

wk=collections.defaultdict(dict)      # (season,team) -> week -> pts
for r in csv.DictReader(open('dst_weekly_2021_2025.csv',encoding='utf-8')):
    wk[(int(r['season']),r['team'])][int(r['week'])]=float(r['dst_pts'])

REP=5.99            # measured: mean of D/ST12's season average, 2021-2025
ADD=re.compile(r'ADD\s+Player ID\s+(-?\d+)')

rows=[]; unmatched=collections.Counter()
for season in (2022,2023,2024,2025):
    for t in csv.DictReader(open(SRC+f'waiver_report_{season}.csv',encoding='utf-8')):
        if t['Status']!='EXECUTED': continue
        w=int(t['Week'])
        if not 1<=w<=14: continue
        for m in ADD.findall(t['Transaction'] or ''):
            pid=int(m)
            if pid>=0: continue                      # skill positions -- SECTION 4.31's population
            team=espn.get(pid)
            if team is None:
                unmatched[pid]+=1; continue
            key=(season, nfl(team))
            if key not in wk:
                unmatched[('nojoin',key)]+=1; continue
            g=wk[key]
            rest=[g[x] for x in range(w,15) if x in g]
            nxt =[g[x] for x in range(w,min(w+4,15)) if x in g]
            if not rest: continue
            rows.append({'season':season,'week':w,'team':nfl(team),
                         'A': st.mean(rest)>=REP, 'B': st.mean(nxt)>=REP if nxt else None,
                         'a_ppg': st.mean(rest)})
assert not unmatched, f"UNJOINED D/ST adds -- fix before reading any number: {dict(unmatched)}"
print(f"every D/ST add joined. n = {len(rows)}\n")

def band(lo,hi): return [r for r in rows if lo<=r['week']<=hi]
def rate(rs,k): 
    v=[r[k] for r in rs if r[k] is not None]
    return (100*sum(v)/len(v), len(v)) if v else (float('nan'),0)

print("  add week      n      A: rest of season    B: next four weeks")
for lab,lo,hi in [('1',1,1),('2',2,2),('3',3,3),('4',4,4),('5-8',5,8),('9-14',9,14)]:
    rs=band(lo,hi); a,_=rate(rs,'A'); b,nb=rate(rs,'B')
    print(f"  {lab:<10}{len(rs):>5}      {a:>6.1f}%              {b:>6.1f}%")
allA,_=rate(rows,'A'); allB,_=rate(rows,'B')
print(f"  {'ALL':<10}{len(rows):>5}      {allA:>6.1f}%              {allB:>6.1f}%")

# rho(week, hit) and the early-vs-late split -- the exact objects SECTION 4.31 reported
def rho(xs,ys):
    n=len(xs)
    rx={v:i+1 for i,v in enumerate(sorted(set(xs)))}
    def rank(vals):
        s=sorted(range(len(vals)), key=lambda i: vals[i]); out=[0]*len(vals); i=0
        while i<len(s):
            j=i
            while j+1<len(s) and vals[s[j+1]]==vals[s[i]]: j+=1
            r=(i+j)/2+1
            for k in range(i,j+1): out[s[k]]=r
            i=j+1
        return out
    a,b=rank(xs),rank(ys)
    ma,mb=st.mean(a),st.mean(b)
    num=sum((x-ma)*(y-mb) for x,y in zip(a,b))
    den=(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))**.5
    return num/den if den else 0.0
def perm(xs,ys,n=20000):
    obs=rho(xs,ys); ys=list(ys); c=0
    rnd=random.Random(7)
    for _ in range(n):
        rnd.shuffle(ys)
        if abs(rho(xs,ys))>=abs(obs)-1e-12: c+=1
    return obs,(c+1)/(n+1)

for k in ('A','B'):
    rs=[r for r in rows if r[k] is not None]
    o,p=perm([r['week'] for r in rs],[1 if r[k] else 0 for r in rs])
    print(f"\n  rho(week, hit) on {k}: {o:+.3f}   permutation p = {p:.3f}   (n={len(rs)})")

early=band(1,4); late=band(9,14)
for k in ('A','B'):
    e,_=rate(early,k); l,_=rate(late,k)
    print(f"  weeks 1-4 vs 9-14 on {k}: {e:.1f}% vs {l:.1f}%")

w1=band(1,1); rest=[r for r in rows if r['week']>1]
for k in ('A','B'):
    a,_=rate(w1,k); b,_=rate(rest,k)
    print(f"  WEEK 1 vs every other week on {k}: {a:.1f}% (n={len(w1)}) vs {b:.1f}%")

# ---------------------------------------------------------------------------
# THE FALSIFIER, AND IT IS THE WHOLE QUESTION (SECTION 0.2).
# 42% looks like skill only if a RANDOMLY CHOSEN defence hits less often. With 32
# defences, 12 rostered and a replacement bar of 5.99 against a league mean of 5.46,
# "reaching replacement" may simply be an easy bar at a shallow position. Same weeks,
# same horizons, same bar -- but the team is drawn at random instead of chosen.
print("\n" + "="*70)
print("  FALSIFIER: the same 208 claims with the DEFENCE CHOSEN AT RANDOM")
print("="*70)
rnd=random.Random(11)
teams_by_season=collections.defaultdict(list)
for (s,t) in wk: teams_by_season[s].append(t)

hitsA=[]; hitsB=[]
for _ in range(400):
    a=b=na=nb=0
    for r in rows:
        t=rnd.choice(teams_by_season[r['season']])
        g=wk[(r['season'],t)]
        rest=[g[x] for x in range(r['week'],15) if x in g]
        nxt =[g[x] for x in range(r['week'],min(r['week']+4,15)) if x in g]
        if rest:
            na+=1; a+= st.mean(rest)>=REP
        if nxt:
            nb+=1; b+= st.mean(nxt)>=REP
    hitsA.append(100*a/na); hitsB.append(100*b/nb)
mA,mB=st.mean(hitsA),st.mean(hitsB)
loA,hiA=sorted(hitsA)[10],sorted(hitsA)[-10]
loB,hiB=sorted(hitsB)[10],sorted(hitsB)[-10]
print(f"  random defence, outcome A: {mA:.1f}%  [{loA:.1f}, {hiA:.1f}]   vs MANAGERS {allA:.1f}%")
print(f"  random defence, outcome B: {mB:.1f}%  [{loB:.1f}, {hiB:.1f}]   vs MANAGERS {allB:.1f}%")
pA=sum(1 for h in hitsA if h>=allA)/len(hitsA)
pB=sum(1 for h in hitsB if h>=allB)/len(hitsB)
print(f"  share of random draws matching or beating the managers: A {pA:.3f}   B {pB:.3f}")
print(f"\n  EDGE OVER RANDOM: A {allA-mA:+.1f} points, B {allB-mB:+.1f} points")

# ---------------------------------------------------------------------------
# AND THE FALSIFIER ABOVE IS TOO KIND TO RANDOM, WHICH CUTS AGAINST MY OWN READING.
# It draws from all 32 defences including the twelve already rostered. A real free pool
# is the LEFTOVERS. Redraw from the bottom 20 by that season's average -- a proxy for
# what is actually claimable -- and the managers' edge should grow if it is real.
print("\n" + "="*70)
print("  THE FAIRER FALSIFIER: random draw from the BOTTOM 20 (a proxy free pool)")
print("="*70)
freepool=collections.defaultdict(list)
for s in sorted({sn for sn,_ in wk}):
    per={t:st.mean([p for w_,p in g.items() if w_<=14]) for (sn,t),g in wk.items() if sn==s}
    freepool[s]=[t for t,_ in sorted(per.items(), key=lambda x:-x[1])[12:]]
print(f"  pool size per season: {[len(freepool[s]) for s in sorted(freepool)]}")

rnd=random.Random(23); hA=[]; hB=[]
for _ in range(400):
    a=b=na=nb=0
    for r in rows:
        t=rnd.choice(freepool[r['season']])
        g=wk[(r['season'],t)]
        rest=[g[x] for x in range(r['week'],15) if x in g]
        nxt =[g[x] for x in range(r['week'],min(r['week']+4,15)) if x in g]
        if rest: na+=1; a+= st.mean(rest)>=REP
        if nxt:  nb+=1; b+= st.mean(nxt)>=REP
    hA.append(100*a/na); hB.append(100*b/nb)
mA2,mB2=st.mean(hA),st.mean(hB)
print(f"  free-pool random, A: {mA2:.1f}%  [{sorted(hA)[10]:.1f}, {sorted(hA)[-10]:.1f}]   vs MANAGERS {allA:.1f}%")
print(f"  free-pool random, B: {mB2:.1f}%  [{sorted(hB)[10]:.1f}, {sorted(hB)[-10]:.1f}]   vs MANAGERS {allB:.1f}%")
pA2=sum(1 for h in hA if h>=allA)/len(hA); pB2=sum(1 for h in hB if h>=allB)/len(hB)
print(f"  share of draws matching/beating the managers: A {pA2:.3f}   B {pB2:.3f}")
print(f"\n  EDGE OVER A CLAIMABLE RANDOM DEFENCE: A {allA-mA2:+.1f}, B {allB-mB2:+.1f}")
