"""When does a starting quarterback's missed time actually fall?
[doc 431] 4.17b prices QB2 at +5 to +11 on a FULL-SEASON hold, driven by a drafted starting QB
missing 2.98 weeks a season. Pro-rating that to "held from week W" is arithmetic nobody measured,
and it is only valid if the misses are spread evenly. This measures the shape.
POPULATION: every team-season 2021-2025. The STARTER is the QB who took the most snaps in weeks
1-3; a week counts as MISSED when he is not his team's top-scoring QB that week.
"""
import pandas as pd, numpy as np
rows=[]
for yr in range(2021,2026):
    d=pd.read_csv(f'/mnt/user-data/uploads/2026/Scripts/research/_nflverse_cache/stats_player_week_{yr}.csv',
                  low_memory=False)
    d=d[(d['position']=='QB')&(d['season_type']=='REG')&(d['week'].between(1,17))].copy()
    g=lambda c: pd.to_numeric(d.get(c,0),errors='coerce').fillna(0)
    d['pts']=(g('passing_yards')*0.04+g('passing_tds')*6-g('passing_interceptions')*2
              +g('rushing_yards')*0.1+g('rushing_tds')*6)
    d['att']=g('attempts') if 'attempts' in d else g('passing_yards')
    top=d.sort_values('pts',ascending=False).groupby(['week','team'],as_index=False).first()
    for tm,s in top.groupby('team'):
        early=s[s['week']<=3]
        if early.empty: continue
        starter=early.groupby('player_display_name')['pts'].sum().idxmax()
        for w in range(1,18):
            r=s[s['week']==w]
            if r.empty: continue
            rows.append({'season':yr,'team':tm,'week':w,
                         'missed':int(r.iloc[0]['player_display_name']!=starter)})
a=pd.DataFrame(rows)
n=a.groupby(['season','team']).ngroups
print(f'team-seasons: {n}')
print(f'missed weeks per team-season, weeks 1-14: {a[a.week<=14].groupby(["season","team"])["missed"].sum().mean():.2f}')
print(f'                        weeks 1-17      : {a.groupby(["season","team"])["missed"].sum().mean():.2f}')
print('\nshare of team-seasons where the week-1 starter is NOT starting, by week:')
by=a.groupby('week')['missed'].mean()
for w in range(1,18):
    bar='#'*int(round(by[w]*100/2))
    print(f'  wk {w:>2}  {by[w]*100:5.1f}%  {bar}')
print('\nEXPECTED MISSED WEEKS INSIDE A WINDOW (what a QB2 held that long can cover):')
for lo in (1,6,8,10,12,15):
    wins=[(lo,14),(lo,17)]
    for a_,b_ in wins:
        if lo>b_: continue
        exp=by[[w for w in range(a_,b_+1)]].sum()
        print(f'  held weeks {a_:>2}-{b_}: {exp:.2f} missed weeks  '
              f'({exp/by[[w for w in range(1,15)]].sum()*100:.0f}% of the full weeks 1-14 exposure)')
