#!/usr/bin/env python3
"""What is actually in Matt's favour, computed rather than argued.

TESTABLE FORM, stated before running (0.5a2): a roster move is worth what it ADDS TO THE NINE HE
ACTUALLY STARTS across weeks 1-14, and nothing else. POPULATION: his 15 plus the free pool as of
the Sept 8 snapshot. BASELINE: his current roster's best legal nine every week. A bye is a ZERO in
a required slot, not a missing row. Weekly rate = season projection / 14 (doc 259's convention).
Roster is FULL at 15, so every add is priced NET of its drop.
"""
import csv, json, re, unicodedata, itertools, collections

REPL = {'RB':168.589, 'WR':163.540, 'QB':341.603, 'TE':140.295}   # 4.1
BOARD='/mnt/user-data/uploads/2026/Scripts/live_draft/board_v8_fixed.csv'
PROJ ='/mnt/user-data/uploads/2026/Source/espn_projections_2026_20260907_1258.csv'
BYES ='/mnt/user-data/uploads/2026/Source/byes_2026.csv'

def nk(s):
    s=unicodedata.normalize('NFKD',s or '').encode('ascii','ignore').decode()
    s=re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?","",s.lower())
    return re.sub(r"[^a-z]","",s)

bye={r['team']:int(r['bye']) for r in csv.DictReader(open(BYES,encoding='utf-8-sig'))}
prows=list(csv.DictReader(open(PROJ,encoding='utf-8-sig')))
PK=[k for k in prows[0] if k.lower().strip()=='player'][0]
proj={(nk(r[PK]), r['pos']): (float(r['proj_2026'] or 0), r['team']) for r in prows}

MINE=[('Puka Nacua','WR',1),('Ashton Jeanty','RB',2),('Quinshon Judkins','RB',3),
      ('Davante Adams','WR',4),('Jalen Hurts','QB',5),('Sam LaPorta','TE',6),
      ('Rico Dowdle','RB',7),('J.K. Dobbins','RB',8),('Tyjae Spears','RB',9),
      ('Xavier Worthy','WR',10),('Mike Washington Jr.','RB',11),('Tyler Shough','QB',12),
      ('Browns D/ST','D/ST',13),('Eddy Pineiro','K',14),('George Pickens','WR',15)]

def mk(name,pos):
    p,t = proj.get((nk(name),pos), (0.0,''))
    return dict(name=name,pos=pos,tm=t,bye=bye.get(t,0),wk=p/14.0)

roster=[dict(mk(n,p), rd=r) for n,p,r in MINE]
for r in roster: assert r['wk']>0 and r['bye'], r

SLOTS=[('QB',{'QB'}),('RB',{'RB'}),('RB',{'RB'}),('WR',{'WR'}),('WR',{'WR'}),
       ('TE',{'TE'}),('FLEX',{'RB','WR','TE'}),('D/ST',{'D/ST'}),('K',{'K'})]

def week_points(players, w, detail=False):
    """Greedy-by-scarcity is wrong; do it exactly. Only 9 slots and <=15 bodies, so fill the
    single-position slots best-first and then FLEX from what is left -- that IS optimal here
    because FLEX is a superset of RB/WR/TE and every other slot is a singleton position."""
    avail=collections.defaultdict(list)
    for p in players:
        if p['bye']!=w: avail[p['pos']].append(p['wk'])
    for k in avail: avail[k].sort(reverse=True)
    used=collections.Counter(); total=0.0; holes=[]
    for label,ok in SLOTS:
        if label=='FLEX': continue
        pool=avail.get(label,[])
        i=used[label]
        if i < len(pool): total+=pool[i]; used[label]+=1
        else: holes.append(label)
    best=0.0
    for pos in ('RB','WR','TE'):
        pool=avail.get(pos,[]); i=used[pos]
        if i < len(pool): best=max(best, pool[i])
    if best>0: total+=best
    else: holes.append('FLEX')
    return (total, holes) if detail else total

def season(players):
    return sum(week_points(players,w) for w in range(1,15))

base=season(roster)
print(f"  BASELINE  weeks 1-14 starting-lineup points: {base:.1f}\n")
print("  where the holes are:")
for w in range(1,15):
    t,h=week_points(roster,w,detail=True)
    off=[p['name'] for p in roster if p['bye']==w]
    if h: print(f"    week {w:>2}  {t:6.1f}   EMPTY: {', '.join(h):<12} off: {', '.join(off)}")
print()

# ---- drop cost: what the roster loses if he is not there at all ---------------------------
print("  cost of dropping each man (points off the season's starting nine), plus what a 2027")
print("  keeper slot on him is worth by 4.18b:")
drops=[]
for p in roster:
    cost = base - season([q for q in roster if q is not p])
    drops.append((cost,p))
for cost,p in sorted(drops, key=lambda x: x[0]):
    if p['rd']<5:  keep='ineligible (round 1-4)'
    elif p['pos'] in ('K','D/ST'): keep='keeper-ineligible position'
    elif p['rd']>=9: keep='round 9+: 4.18b measures the option at or below zero'
    else: keep=f"round {p['rd']}: inside the 5-8 audition band"
    print(f"    {p['name']:<22}{p['pos']:<5}rd{p['rd']:>3}  drop costs {cost:6.2f}   {keep}")

# ---- the free pool -------------------------------------------------------------------------
free=[]
for p in json.load(open('/home/claude/wire_now.json')):
    pos=p['pos']
    if pos not in REPL: continue
    pr,tm = proj.get((nk(p['player']),pos), (None,None))
    if pr is None: pr = p['v'] + REPL[pos]; tm = p['team']
    b = bye.get(tm or p['team'], 0)
    if not b: continue
    free.append(dict(name=p['player'],pos=pos,tm=tm or p['team'],bye=b,wk=pr/14.0,
                     news=(p.get('news') or '')[:60]))
# free defences: every D/ST not taken in the draft
taken={r[1] for r in json.load(open('/home/claude/drafted.json')) if r[2]=='D/ST'}
for r in prows:
    if r['pos']=='D/ST' and r[PK] not in taken:
        free.append(dict(name=r[PK],pos='D/ST',tm=r['team'],bye=bye.get(r['team'],0),
                         wk=float(r['proj_2026'] or 0)/14.0,news=''))
for r in prows:
    if r['pos']=='K' and r[PK] not in {x[1] for x in json.load(open('/home/claude/drafted.json')) if x[2]=='K'}:
        free.append(dict(name=r[PK],pos='K',tm=r['team'],bye=bye.get(r['team'],0),
                         wk=float(r['proj_2026'] or 0)/14.0,news=''))
print(f"\n  free pool priced: {collections.Counter(f['pos'] for f in free)}")

# ---- every (add, drop) pair, netted --------------------------------------------------------
cand_drop=[p for p in roster if p['rd']>=7]          # nobody in rounds 1-6 is a live drop
best=[]
for a in free:
    for d in cand_drop:
        if a['name']==d['name']: continue
        new=[q for q in roster if q is not d]+[a]
        best.append((season(new)-base, a, d))
best.sort(key=lambda x:-x[0])
seen=set(); out=[]
for gain,a,d in best:
    if a['name'] in seen: continue
    seen.add(a['name']); out.append((gain,a,d))
    if len(out)>=15: break
print("\n  THE MOVES, ranked by what they add to the starting nine over weeks 1-14")
print(f"  {'add':<24}{'pos':<5}{'tm':<5}{'bye':>4}{'/wk':>7}   drop{'':<18}{'net':>7}")
for gain,a,d in out:
    print(f"    {a['name']:<22}{a['pos']:<5}{a['tm']:<5}{a['bye']:>4}{a['wk']:>7.2f}   {d['name']:<22}{gain:>+7.2f}")
