#!/usr/bin/env python3
r"""te2_split.py -- the week-1 workload screen's hit rate split by whether the man led his own team at his
position in week 1 (doc 457). Mayer cleared the screen as the Raiders' top tight end while Bowers was out and the
page kept pricing him at 38% after Bowers returned with 13 targets to his 3.

THE CLAIM IN TESTABLE FORM: within the screen's own population (doc 308, n=517), the men who cleared 2 or 3 of 3
marks hit less often when a teammate at the same position out-targeted them in week 1.
Run from Scripts\research\_nflverse_cache\ (the weekly files live there); the nflverse snap counts the screen
reads are fetched into that folder if absent. Standard library only. The population builder is the screen's own
(wk1_wr_composite.py), copied so the two cannot drift apart silently.
"""
import os, sys, urllib.request
for _s in (2021, 2022, 2023, 2024, 2025):
    _f = f'snap_counts_{_s}.csv'
    if not os.path.exists(_f):
        print(f'  fetching {_f}')
        urllib.request.urlretrieve(f'https://github.com/nflverse/nflverse-data/releases/download/snap_counts/{_f}', _f)

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

# ---- the split Matt asked for on 1 Oct: was he the top man at his position on his own team in week 1? ----
rank={}
for s in SCORE:
    wk1=[r for r in load(s) if r['_w']==1]
    byteam=collections.defaultdict(list)
    for r in wk1: byteam[(r['team'],r['position'])].append((float(r.get('targets') or 0), r['player_id']))
    for k,v in byteam.items():
        v.sort(reverse=True)
        for i,(tg,pid) in enumerate(v,1): rank[(s,pid)]=i
# rows carry name not id; rebuild with ids
rows2=[]
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
        if sp is None: continue
        sig=(1 if tg>=8 else 0)+(1 if sp>=80 else 0)+(1 if tg/tt[r['team']]>=0.20 else 0)
        rows2.append({'season':s,'name':r['player_display_name'],'pos':pos,'sig':sig,'rank':rank.get((s,r['player_id']),9),
                      'ppg':sum(g)/len(g),'hit':1 if sum(g)/len(g)>=REPL[pos] else 0})
print('population', len(rows2))
def cell(f, label):
    c=[r for r in rows2 if f(r)]; 
    print(f'  {label:<58} {sum(r["hit"] for r in c):>3} of {len(c):<4} {100*sum(r["hit"] for r in c)/len(c) if c else float("nan"):5.1f}%')
cell(lambda r: r['sig']>=2, '2 or 3 of 3, all')
cell(lambda r: r['sig']>=2 and r['rank']==1, '2 or 3 of 3, TOP man at his position on his team (wk 1 targets)')
cell(lambda r: r['sig']>=2 and r['rank']>=2, '2 or 3 of 3, SECOND or lower at his position on his team')
cell(lambda r: r['sig']>=2 and r['pos']=='TE', '2 or 3 of 3, TE, all')
cell(lambda r: r['sig']>=2 and r['pos']=='TE' and r['rank']==1, '2 or 3 of 3, TE, top TE on his team')
cell(lambda r: r['sig']>=2 and r['pos']=='TE' and r['rank']>=2, '2 or 3 of 3, TE, second TE on his team')
cell(lambda r: r['sig']>=2 and r['pos']=='WR' and r['rank']>=2, '2 or 3 of 3, WR, second or lower on his team')
print('  the second-TE men:')
for r in rows2:
    if r['sig']>=2 and r['pos']=='TE' and r['rank']>=2: print('   ', r['season'], r['name'], f"{r['ppg']:.1f}", 'HIT' if r['hit'] else '')
