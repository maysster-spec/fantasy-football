#!/usr/bin/env python3
"""dst_weekly_2021_2025.csv -- the file doc 212's reproduce line named and never shipped."""
import gzip, csv, collections, statistics as st

BANDS=[(0,0,10),(1,6,7),(7,13,4),(14,17,1),(18,21,0),(22,27,-1),(28,34,-4),(35,45,-7),(46,999,-10)]
def pa(p):
    for lo,hi,v in BANDS:
        if lo<=p<=hi: return v
    return -10
def f(x):
    try: return float(x)
    except (TypeError,ValueError): return 0.0

rows=[]
for season in (2021,2022,2023,2024,2025):
    acc=collections.defaultdict(collections.Counter); finals={}; opp={}
    with gzip.open(f'play_by_play_{season}.csv.gz','rt',encoding='utf-8',errors='replace') as fh:
        for p in csv.DictReader(fh):
            if p.get('season_type')!='REG': continue
            wk=p.get('week'); pos=p.get('posteam'); d=p.get('defteam')
            if not wk: continue
            wk=int(wk)
            h,a=p.get('home_team'),p.get('away_team')
            if h and a:
                opp[(wk,h)]=a; opp[(wk,a)]=h
                hs,as_=p.get('total_home_score'),p.get('total_away_score')
                if hs not in (None,'') and as_ not in (None,''):
                    finals[(wk,h)]=max(finals.get((wk,h),0),int(float(hs)))
                    finals[(wk,a)]=max(finals.get((wk,a),0),int(float(as_)))
            if not d: continue
            k=(wk,d)
            if f(p.get('sack')): acc[k]['sack']+=1
            if f(p.get('interception')): acc[k]['int']+=1
            if f(p.get('safety')): acc[k]['saf']+=1
            if f(p.get('fumble_lost')) and p.get('fumble_recovery_1_team')==d: acc[k]['fr']+=1
            if f(p.get('touchdown')):
                t=p.get('td_team')
                if t and pos and t!=pos: acc[(wk,t)]['dtd']+=1
    n=0
    for (wk,team),c in acc.items():
        o=opp.get((wk,team)); al=finals.get((wk,o)) if o else None
        if al is None: continue
        pts=c['sack']+2*c['int']+2*c['fr']+4*c['saf']+6*c['dtd']+pa(al)
        rows.append({'season':season,'week':wk,'team':team,'opp':o,'allowed':al,
                     'sack':c['sack'],'int':c['int'],'fr':c['fr'],'saf':c['saf'],'dtd':c['dtd'],
                     'dst_pts':round(pts,2)})
        n+=1
    print(f"  {season}: {n} team-weeks")

with open('dst_weekly_2021_2025.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

print(f"\ntotal {len(rows)} team-weeks, {len({r['season'] for r in rows})} seasons")
v=[r['dst_pts'] for r in rows]
print(f"mean {st.mean(v):.2f}  sd {st.pstdev(v):.2f}   (doc 212: 5.10 / 6.56)")

# REPLACEMENT: D/ST12 by season average -- 12 starters in a 12-team league. Measured, not assumed.
print("\nD/ST12 season average, per season:")
reps={}
for s in sorted({r['season'] for r in rows}):
    per=collections.defaultdict(list)
    for r in rows:
        if r['season']==s and r['week']<=14: per[r['team']].append(r['dst_pts'])
    avg=sorted((st.mean(v) for v in per.values()), reverse=True)
    reps[s]=avg[11]
    print(f"  {s}: {avg[11]:.2f}   (best {avg[0]:.2f}, worst {avg[-1]:.2f})")
print(f"\npooled D/ST replacement = {st.mean(reps.values()):.2f} points a week")
