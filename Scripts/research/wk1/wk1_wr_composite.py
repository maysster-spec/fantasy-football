r"""The week-1 pass-catcher composite: do the three workload signals COMPOUND (4.30's shape) or
substitute (doc 191's)? Matt's standing frame, 0.5(a3): measure the cell, do not assume a direction.

THE CLAIM IN ITS TESTABLE FORM, written before the run (0.5a2): among wire-eligible pass-catchers,
the COUNT of three week-1 workload signals -- 8 or more targets, 80% or more of his team's offensive
snaps, 20% or more of his team's targets -- predicts reaching replacement over weeks 2-14 better
than any one of them alone.
POPULATION: as wr_week1_share.py -- every WR/TE 2021-2025 who played week 1 with 1+ target, was
BELOW his position's replacement rate the prior season or has no prior season, played 4+ of weeks
2-14, and has a week-1 snap line. BASELINE: the population's own 18% startable rate.
OUTCOME: half-PPR ppg weeks 2-14 reaching WR 9.62 / TE 8.25 (derived, 9.4).
"""
import collections, csv, os, re, random, statistics
SEASONS=[2021,2022,2023,2024,2025]; SCORE=[2022,2023,2024,2025]; REPL={'WR':9.62,'TE':8.25}
def hp(r):
    g=lambda k: float(r.get(k) or 0)
    return (0.1*g('rushing_yards')+6*g('rushing_tds')+0.1*g('receiving_yards')
            +6*g('receiving_tds')+0.5*g('receptions')
            -2*(g('rushing_fumbles_lost')+g('receiving_fumbles_lost')))
def norm(n):
    n=(n or '').lower(); n=re.sub(r"[.'`’]",'',n)
    n=re.sub(r'\b(jr|sr|ii|iii|iv|v)\b','',n); return re.sub(r'[^a-z]','',n)
def load(s):
    out=[]
    for r in csv.DictReader(open(f'stats_player_week_{s}.csv',newline='',encoding='utf-8-sig')):
        if (r.get('season_type') or 'REG')!='REG' or (r.get('position') or '') not in ('WR','TE'): continue
        try: r['_w']=int(r['week'])
        except: continue
        out.append(r)
    return out
prior={}
for s in SEASONS:
    agg=collections.defaultdict(list)
    for r in load(s):
        if r['_w']<=14: agg[r['player_id']].append(hp(r))
    for p,v in agg.items(): prior[(s,p)]=sum(v)/len(v)
snap={}
for s in SEASONS:
    for r in csv.DictReader(open(f'snap_counts_{s}.csv',newline='',encoding='utf-8-sig')):
        if r.get('week')!='1': continue
        try: p=float(r['offense_pct'] or 0)
        except: continue
        snap[(s,norm(r['player']),r['team'])]=p*100 if p<=1 else p
TF={'LAR':'LA','JAC':'JAX','WSH':'WAS','ARZ':'ARI','LVR':'LV','SFO':'SF','GNB':'GB','KAN':'KC','NWE':'NE','NOR':'NO','TAM':'TB'}
rows=[]
for s in SCORE:
    rs=load(s); wk1=[r for r in rs if r['_w']==1]
    tt=collections.Counter()
    for r in wk1: tt[r['team']]+=float(r.get('targets') or 0)
    rest=collections.defaultdict(list)
    for r in rs:
        if 2<=r['_w']<=14: rest[r['player_id']].append(hp(r))
    for r in wk1:
        tg=float(r.get('targets') or 0)
        if tg<1 or not tt[r['team']]: continue
        pos=r['position']; p=prior.get((s-1,r['player_id']))
        if p is not None and p>=REPL[pos]: continue
        g=rest.get(r['player_id'],[])
        if len(g)<4: continue
        nm=norm(r['player_display_name']); tm=TF.get(r['team'],r['team'])
        sp=snap.get((s,nm,r['team']))
        if sp is None: sp=snap.get((s,nm,tm))
        if sp is None: continue                     # assert on the join, never default it (doc 251)
        sig=(1 if tg>=8 else 0)+(1 if sp>=80 else 0)+(1 if tg/tt[r['team']]>=0.20 else 0)
        rows.append({'season':s,'name':r['player_display_name'],'pos':pos,'sig':sig,
                     'ppg':sum(g)/len(g),'hit':1 if sum(g)/len(g)>=REPL[pos] else 0})
print(__doc__.split('\n')[0]); print(f'\npopulation: {len(rows)} player-seasons, 2022-2025 -- 2021 is EXCLUDED because\nno 2020 prior season is on file, so every 2021 man passed the not-startable filter and\nthe top cell filled with Kupp, Jefferson, Hill and Diggs (4.23 selection trap).')
print(f'base rate: {100*statistics.mean(r["hit"] for r in rows):.1f}% startable\n')
print(f'{"signals of three":22s} {"n":>4s} {"ppg":>6s} {"reached replacement":>20s}')
for k in (0,1,2,3):
    c=[r for r in rows if r['sig']==k]
    if not c: continue
    print(f'{k:>16d} of 3 {len(c):4d} {statistics.mean(r["ppg"] for r in c):6.2f} '
          f'{100*statistics.mean(r["hit"] for r in c):19.0f}%')
hi=[r for r in rows if r['sig']==3]; lo=[r for r in rows if r['sig']<3]
d=statistics.mean(r['hit'] for r in hi)-statistics.mean(r['hit'] for r in lo)
random.seed(7); vals=[r['hit'] for r in rows]; n=len(hi); c=0
for _ in range(6000):
    random.shuffle(vals)
    if statistics.mean(vals[:n])-statistics.mean(vals[n:])>=d: c+=1
print(f'\n  3 of 3 (n={len(hi)}) minus under 3 (n={len(lo)}): {100*d:+.1f} points, '
      f'permutation p={(c+1)/6001:.4f}')
print('\n  every 3-of-3:')
for r in sorted(rows,key=lambda r:-r['ppg']):
    if r['sig']==3:
        print(f'    {r["season"]} {r["name"][:24]:25s} {r["pos"]} {r["ppg"]:5.1f} ppg'
              f'{"   STARTABLE" if r["hit"] else ""}')
