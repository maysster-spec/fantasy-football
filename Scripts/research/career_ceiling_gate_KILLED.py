"""Would a CAREER-CEILING gate have caught Otton?
The bet prices every candidate at one archetype hit rate (12.71 a game). That number is a claim
about what the man could become. The cheapest falsifier: has he EVER produced at that rate over a
full season? Population: nflverse REG 2021-2025, scored under this league's rules, 8+ games.
"""
import pandas as pd, numpy as np
HIT = 12.71
rows=[]
for yr in range(2021,2026):
    d=pd.read_csv(f'/mnt/user-data/uploads/2026/Scripts/research/_nflverse_cache/stats_player_week_{yr}.csv',
                  low_memory=False)
    d=d[(d['position'].isin(['TE','WR','RB']))&(d['season_type']=='REG')&(d['week'].between(1,17))].copy()
    g=lambda c: pd.to_numeric(d.get(c,0),errors='coerce').fillna(0)
    d['pts']=(g('receptions')*0.5+g('receiving_yards')*0.1+g('receiving_tds')*6
              +g('rushing_yards')*0.1+g('rushing_tds')*6
              -(g('receiving_fumbles_lost')+g('rushing_fumbles_lost'))*2)
    d['season']=yr
    rows.append(d[['season','player_display_name','position','pts']])
a=pd.concat(rows,ignore_index=True)
s=a.groupby(['player_display_name','position','season']).agg(g=('pts','size'),ppg=('pts','mean')).reset_index()
s=s[s['g']>=8]
best=s.groupby(['player_display_name','position'])['ppg'].max()

names=['Cade Otton','Michael Mayer','Malik Washington','Kalif Raymond','Germie Bernard',
       'Xavier Worthy','Luther Burden III','Jalen McMillan','Pat Bryant','Pat Freiermuth',
       'Kyle Pitts','Mike Gesicki','Oronde Gadsden II','Darren Waller','Brenton Strange']
print(f"the bet prices every one of these at {HIT} a game. career best full season, our scoring:\n")
print(f"{'player':<22}{'pos':<5}{'career best/g':>14}{'gate':>10}")
for n in names:
    hit=[(p,v) for (p,pos),v in best.items() if p==n]
    if not hit:
        print(f'{n:<22}{"?":<5}{"no season 8+ games":>14}{"FIRES":>10}'); continue
    p,v=hit[0]
    pos=[pos for (pp,pos) in best.index if pp==n][0]
    print(f'{n:<22}{pos:<5}{v:>14.2f}{("FIRES" if v<HIT else "passes"):>10}')
print()
print('how many of the 137 TEs have EVER had a season at or above 12.71 a game?')
te=best[[i for i in best.index if i[1]=='TE']]
print(f'  {(te>=HIT).sum()} of {len(te)}  ({(te>=HIT).mean()*100:.0f}%)')
wr=best[[i for i in best.index if i[1]=='WR']]
print(f'  WR: {(wr>=HIT).sum()} of {len(wr)}  ({(wr>=HIT).mean()*100:.0f}%)')
