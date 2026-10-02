#!/usr/bin/env python3
"""Matt, 2026-09-10: "other teams have bye weeks too and we need to factor in scarcity and how many
weeks/days ahead are optimal to fill that position without negatively impacting the rest of the
roster."

TWO TESTABLE FORMS, both stated before running (0.5a2):
  T1 DEMAND. POPULATION: every EXECUTED add in this league 2022-2025 that maps to a position,
     weeks 2-14. PREDICTOR: how many of the twelve managers have their DRAFTED STARTER at that
     position on bye that week. OUTCOME: adds at that position that week. DIRECTION: more managers
     short a body -> more adds at that position.
  T2 LEAD TIME. POPULATION: every (manager, season, position) whose drafted starter had a bye,
     for the positions with one starter -- QB, TE, K, D/ST. OUTCOME: the week of that manager's
     nearest add at the position, minus the bye week. DIRECTION: if the field fills IN the bye week,
     buying one week early wins the body outright.
"""
import csv, re, collections, statistics as st, unicodedata, math
import pandas as pd

SEASONS=[2022,2023,2024,2025]
SRC='/mnt/user-data/uploads/2026/Source/'

# ---- byes, from the real schedule ------------------------------------------------------------
g=pd.read_csv('/home/claude/dst/games.csv',low_memory=False)
g=g[(g.game_type=='REG')]
bye={}                                   # (season, team) -> week
playing=collections.defaultdict(set)
for r in g.itertuples():
    playing[(r.season,r.week)].add(r.home_team); playing[(r.season,r.week)].add(r.away_team)
for season in SEASONS+[2026]:
    wks=sorted(w for (s,w) in playing if s==season)
    teams=set().union(*[playing[(season,w)] for w in wks])
    for t in teams:
        off=[w for w in wks if t not in playing[(season,w)]]
        if len(off)==1: bye[(season,t)]=off[0]
byeload={}                               # (season, week) -> NFL teams off
for season in SEASONS+[2026]:
    c=collections.Counter(w for (s,t),w in bye.items() if s==season)
    byeload[season]={w:c.get(w,0) for w in range(1,19)}

# ---- id -> position, union of every projection pull we have ----------------------------------
pos={}
for f in ('espn_projections_2022_20260824.csv','espn_projections_2023_20260824.csv',
          'espn_projections_2024_20260824.csv','espn_projections_2026_20260907_1258.csv'):
    for r in csv.DictReader(open(SRC+f,encoding='utf-8-sig')):
        pid=str(r.get('espn_id','')).strip()
        if pid and r.get('pos'): pos.setdefault(pid, r['pos'])
def ppos(pid):
    pid=str(pid)
    if pid.startswith('-'): return 'D/ST'
    return pos.get(pid)

# ---- executed adds and drops, by position and week --------------------------------------------
ADD=re.compile(r'ADD Player ID (-?\d+)'); DROP=re.compile(r'DROP Player ID (-?\d+)')
adds=collections.Counter(); unmapped=0; total=0
addrows=[]                                # (season, week, team, position)
for season in SEASONS:
    for r in csv.DictReader(open(SRC+f'waiver_report_{season}.csv',encoding='utf-8-sig')):
        if r['Status']!='EXECUTED': continue
        w=int(r['Week'])
        for pid in ADD.findall(r['Transaction'] or ''):
            total+=1; p=ppos(pid)
            if p is None: unmapped+=1; continue
            adds[(season,w,p)]+=1; addrows.append((season,w,r['Team'],p))
print(f"  executed adds mapped to a position: {total-unmapped} of {total} "
      f"({unmapped} unmapped, {unmapped/total:.1%})")

# ---- who is short a body: drafted starters on bye ---------------------------------------------
TEAMFIX={'Jax':'JAX','Was':'WAS','Lar':'LA','Lac':'LAC','Kan':'KC','Kc':'KC','Sfo':'SF','Sf':'SF',
 'Tam':'TB','Tb':'TB','Gnb':'GB','Gb':'GB','Nor':'NO','No':'NO','Nwe':'NE','Ne':'NE','Sea':'SEA',
 'Ari':'ARI','Atl':'ATL','Bal':'BAL','Buf':'BUF','Car':'CAR','Chi':'CHI','Cin':'CIN','Cle':'CLE',
 'Dal':'DAL','Den':'DEN','Det':'DET','Hou':'HOU','Ind':'IND','Lv':'LV','Lvr':'LV','Mia':'MIA',
 'Min':'MIN','Nyg':'NYG','Nyj':'NYJ','Phi':'PHI','Pit':'PIT','Ten':'TEN','Was':'WAS','Wsh':'WAS'}
dh=list(csv.DictReader(open(SRC+'draft_history_2021_2025.csv',encoding='utf-8-sig')))
starters=collections.defaultdict(dict)    # (season, manager) -> pos -> team  (best pick at that pos)
for r in dh:
    y=int(r['Year'])
    if y not in SEASONS: continue
    p=r['Pos']; tm=TEAMFIX.get((r['NFL'] or '').strip().title(), (r['NFL'] or '').strip().upper())
    key=(y,r['Team'])
    if p not in starters[key]:            # rows are in pick order, so the first is the earliest
        starters[key][p]=tm
short=collections.Counter()               # (season, week, pos) -> managers whose starter is off
for (y,team),d in starters.items():
    for p,tm in d.items():
        w=bye.get((y,tm))
        if w: short[(y,w,p)]+=1
print(f"  manager-seasons with a drafted roster read: {len(starters)}")

print("\n" + "="*76)
print("  T1  DOES DEMAND AT A POSITION SPIKE IN THE WEEKS ITS BYES CLUSTER?")
print("="*76)
print(f"  {'pos':<6}{'weeks':>7}{'r':>8}{'p':>9}   adds when 0-1 managers short | 2 | 3+")
def pear(xs,ys):
    n=len(xs); mx,my=st.mean(xs),st.mean(ys)
    sx=math.sqrt(sum((x-mx)**2 for x in xs)); sy=math.sqrt(sum((y-my)**2 for y in ys))
    if sx==0 or sy==0: return 0.0,1.0
    r=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/(sx*sy)
    t=r*math.sqrt((n-2)/max(1e-9,1-r*r))
    return r, 2*(1-0.5*(1+math.erf(abs(t)/math.sqrt(2))))
for p in ('QB','RB','WR','TE','D/ST','K'):
    xs,ys=[],[]; band=collections.defaultdict(list)
    for season in SEASONS:
        for w in range(2,15):
            s=short[(season,w,p)]; a=adds[(season,w,p)]
            xs.append(s); ys.append(a)
            band['0-1' if s<=1 else ('2' if s==2 else '3+')].append(a)
    r,pv=pear(xs,ys)
    m=lambda k: (st.mean(band[k]) if band[k] else float('nan'))
    print(f"  {p:<6}{len(xs):>7}{r:>+8.3f}{pv:>9.4f}   {m('0-1'):.2f}  |  {m('2'):.2f}  |  {m('3+'):.2f}"
          f"   (n {len(band['0-1'])}/{len(band['2'])}/{len(band['3+'])})")

print("\n" + "="*76)
print("  T2  WHEN DOES THE FIELD ACTUALLY FILL A BYE-WEEK HOLE?")
print("="*76)
# only positions where one body is the whole depth chart
addsby=collections.defaultdict(list)      # (season, team, pos) -> [weeks]
for season,w,team,p in addrows: addsby[(season,team,p)].append(w)
counts=collections.defaultdict(collections.Counter)
for r in dh:
    y=int(r['Year'])
    if y in SEASONS: counts[(y,r['Team'])][r['Pos']]+=1
lead=collections.defaultdict(list); nofill=collections.Counter(); cases=collections.Counter()
for (y,team),d in starters.items():
    for p in ('QB','TE','K','D/ST'):
        if p not in d: continue
        if counts[(y,team)][p] > 1: continue          # he drafted a backup, no hole
        w=bye.get((y,d[p]))
        if not w or not (2 <= w <= 14): continue
        cases[p]+=1
        got=[a for a in addsby[(y,team,p)] if w-4 <= a <= w]
        if got: lead[p].append(w - max(got))
        else:   nofill[p]+=1
print(f"  {'pos':<6}{'cases':>7}{'filled':>8}{'median lead':>13}   in the bye week | 1 wk early | 2+ early")
for p in ('QB','TE','K','D/ST'):
    L=lead[p]; n=cases[p]
    if not L: print(f"  {p:<6}{n:>7}{0:>8}"); continue
    c=collections.Counter(L)
    print(f"  {p:<6}{n:>7}{len(L):>8}{st.median(L):>13.0f}   "
          f"{c[0]:>13} | {c[1]:>10} | {sum(v for k,v in c.items() if k>=2):>9}"
          f"   (never filled {nofill[p]})")

print("\n" + "="*76)
print("  2026 -- HOW MANY OF THE OTHER ELEVEN LOSE A STARTER IN THE WEEKS YOU HAVE HOLES")
print("="*76)
import json
d26=json.load(open('/home/claude/drafted.json'))
NFL2ABBR={'ARI':'ARI','ATL':'ATL','BAL':'BAL','BUF':'BUF','CAR':'CAR','CHI':'CHI','CIN':'CIN',
 'CLE':'CLE','DAL':'DAL','DEN':'DEN','DET':'DET','GB':'GB','HOU':'HOU','IND':'IND','JAX':'JAX',
 'KC':'KC','LAC':'LAC','LAR':'LA','LV':'LV','MIA':'MIA','MIN':'MIN','NE':'NE','NO':'NO','NYG':'NYG',
 'NYJ':'NYJ','PHI':'PHI','PIT':'PIT','SEA':'SEA','SF':'SF','TB':'TB','TEN':'TEN','WAS':'WAS','WSH':'WAS'}
r26=collections.defaultdict(lambda: collections.defaultdict(list))
for rd,name,p,tm,team in d26:
    r26[team][p].append(NFL2ABBR.get(tm,tm))
print(f"  {'week':>5}{'NFL teams off':>15}   managers short a starter at ...")
for w in range(2,15):
    line=[]
    for p in ('QB','TE','K','D/ST','RB','WR'):
        n=0
        for team,d in r26.items():
            tms=d.get(p,[])
            if not tms: continue
            need = 1 if p in ('QB','TE','K','D/ST') else 2
            off=sum(1 for t in tms if bye.get((2026,t))==w)
            if len(tms)-off < need: n+=1
        if n: line.append(f"{p} {n}")
    mark='   <<< YOU' if w in (6,8,11) else ''
    print(f"  {w:>5}{byeload[2026].get(w,0):>15}   {', '.join(line) or '-'}{mark}")
