#!/usr/bin/env python3
r"""
injury_overlap.py -- can a coach's reaction be told apart from an injury? (doc 291, catalog G2)

Matt, 11 Sept: "did I hear you can't distinguish injury from drops? if so research historical
injury info." It can be told apart, and this measures how much of the question it touches.

POPULATION: RB/WR/TE regular-season player-games 2021-2025 with 5+ carries plus targets.
EVENT: a lost fumble (rushing or receiving). OUTCOME, at his team's NEXT game: on the injury
report at all / listed Out or Doubtful / roster status not ACT / no offensive snaps.

INPUTS (nflverse releases, downloaded beside this file; nothing else is read):
  player_stats_2021..2024.csv and stats_player_week_2025.csv   (weekly player stats)
  injuries_2021..2025.csv      (weekly injury reports: report_status)
  roster_weekly_2021..2025.csv (weekly roster status, gsis_id -> pfr_id)
  snap_counts_2021..2025.csv   (offensive snaps, keyed on pfr_player_id)
Result on 11 Sept: after a lost fumble 11.2% were on the next injury report (8.5% without one),
4.9% Out or Doubtful (2.6%), 6.7% not active (5.6%), 7.8% played no snaps (6.7%); n=448 vs 10,488.
So G2 drops any event whose next game carries an injury designation or an inactive status, and the
snap and route change is measured on the rest.
"""
import pandas as pd, numpy as np
Y=[2021,2022,2023,2024,2025]
ps=[]
for y in [2021,2022,2023,2024]:
    d=pd.read_csv(f'player_stats_{y}.csv',low_memory=False)
    d=d.rename(columns={'recent_team':'team'})
    ps.append(d[['player_id','player_display_name','position','team','season','week','season_type','carries','targets','rushing_fumbles_lost','receiving_fumbles_lost']])
d=pd.read_csv('stats_player_week_2025.csv',low_memory=False)
namecol='player_display_name' if 'player_display_name' in d.columns else 'player_name'
d=d.rename(columns={namecol:'player_display_name'})
ps.append(d[['player_id','player_display_name','position','team','season','week','season_type','carries','targets','rushing_fumbles_lost','receiving_fumbles_lost']])
ps=pd.concat(ps,ignore_index=True)
ps=ps[(ps.season_type=='REG')&(ps.position.isin(['RB','WR','TE']))].copy()
for c in ['carries','targets','rushing_fumbles_lost','receiving_fumbles_lost']: ps[c]=ps[c].fillna(0)
ps['fl']=ps.rushing_fumbles_lost+ps.receiving_fumbles_lost
ps['use']=ps.carries+ps.targets
inj=pd.concat([pd.read_csv(f'injuries_{y}.csv',low_memory=False) for y in Y],ignore_index=True)
inj=inj[inj.game_type=='REG'][['season','week','gsis_id','report_status']].drop_duplicates(['season','week','gsis_id'])
ros=pd.concat([pd.read_csv(f'roster_weekly_{y}.csv',low_memory=False,usecols=['season','week','game_type','gsis_id','status','pfr_id']) for y in Y],ignore_index=True)
ros=ros[ros.game_type=='REG'].drop_duplicates(['season','week','gsis_id'])
snap=pd.concat([pd.read_csv(f'snap_counts_{y}.csv',low_memory=False) for y in Y],ignore_index=True)
snap=snap[snap.game_type=='REG']
teamweeks=snap[['season','team','week']].drop_duplicates()
# normalise team codes between stats and snap counts
st=set(ps.team.unique()); sn=set(teamweeks.team.unique())
print('stat-only codes',sorted(st-sn),'snap-only codes',sorted(sn-st))
alias={}
for a,b in [('LA','LAR'),('LAR','LA'),('WAS','WSH'),('WSH','WAS'),('JAX','JAC'),('JAC','JAX'),('LV','OAK')]:
    if a in st-sn and b in sn: alias[a]=b
ps['team_s']=ps.team.replace(alias)
tw=teamweeks.sort_values(['season','team','week'])
tw['next_week']=tw.groupby(['season','team']).week.shift(-1)
ps=ps.merge(tw.rename(columns={'team':'team_s'}),on=['season','team_s','week'],how='left')
print('rows',len(ps),'without a team-week match',ps.next_week.isna().sum(),'(last game of season or unmatched)')
ps=ps[ps.next_week.notna()].copy(); ps['next_week']=ps.next_week.astype(int)
ps=ps.merge(inj.rename(columns={'week':'next_week','gsis_id':'player_id','report_status':'next_report'}),on=['season','next_week','player_id'],how='left')
ps=ps.merge(ros.rename(columns={'week':'next_week','gsis_id':'player_id','status':'next_roster'})[['season','next_week','player_id','next_roster','pfr_id']],on=['season','next_week','player_id'],how='left')
idmap=ros[['gsis_id','pfr_id']].dropna().drop_duplicates('gsis_id')
sn2=snap[['season','week','pfr_player_id','offense_snaps']].rename(columns={'week':'next_week','pfr_player_id':'pfr_id2','offense_snaps':'next_snaps'})
ps=ps.merge(idmap.rename(columns={'gsis_id':'player_id','pfr_id':'pfr_id2'}),on='player_id',how='left')
print('id join rate gsis->pfr',round(ps.pfr_id2.notna().mean(),4))
ps=ps.merge(sn2,on=['season','next_week','pfr_id2'],how='left')
ps['listed']=ps.next_report.notna()
ps['out_doubt']=ps.next_report.isin(['Out','Doubtful'])
ps['not_active']=ps.next_roster.notna()&(ps.next_roster!='ACT')
ps['no_snaps']=ps.next_snaps.isna()|(ps.next_snaps==0)
base=ps[ps.use>=5]
ev=base[base.fl>=1]; ctl=base[base.fl==0]
def row(df):
    return len(df), df.listed.mean(), df.out_doubt.mean(), df.not_active.mean(), df.no_snaps.mean()
print('\nPOPULATION: RB/WR/TE regular-season player-games 2021-2025 with 5+ carries plus targets; outcome at the team NEXT game')
print(f"{'group':24s} {'n':>6s} {'on report':>9s} {'out/doubt':>9s} {'not active':>10s} {'no snaps':>9s}")
for name,df in [('lost a fumble',ev),('no lost fumble',ctl)]:
    n,a,b,c,e=row(df); print(f"{name:24s} {n:6d} {a:9.1%} {b:9.1%} {c:10.1%} {e:9.1%}")
for pos in ['RB','WR','TE']:
    for name,df in [('lost a fumble',ev),('no lost fumble',ctl)]:
        n,a,b,c,e=row(df[df.position==pos]); print(f"{pos+' '+name:24s} {n:6d} {a:9.1%} {b:9.1%} {c:10.1%} {e:9.1%}")
print('\nreport_status values:',inj.report_status.value_counts(dropna=False).head(8).to_dict())
print('roster status values:',ros.status.value_counts().head(8).to_dict())
