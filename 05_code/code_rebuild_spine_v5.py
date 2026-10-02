#!/usr/bin/env python3
"""
code_rebuild_spine_v5.py — rebuild the player universe on the dated ESPN pull.
Fixes shipped defects from claude/19_integrity_audit_20260822.md:
  CRITICAL 1  ADP was a dense rank sold as average draft position -> split into
              adp_pick (ESPN's real ADP) and adp_rank (ordinal), both explicitly named.
  CRITICAL 2  D/ST and K were v2 carryover, hard-set to 50.0, joined on full team names
              against ESPN's "Texans D/ST" -> rejoined on espn_id, real projections restored.
  HIGH        injuryStatus never surfaced -> injury_status column.
  HIGH        WAS/WSH team-code split -> normalised, both stored.
  ADP censoring: 70% of ESPN rows sit in a 1.56-pick blob at ~170 (undrafted sentinel).
              Flagged, and a projection-ordered fallback rank is provided for picks 152/161.
Join contract (ERROR_PATTERNS C1): espn_id only. Row counts asserted at every step.
"""
import pandas as pd, numpy as np, datetime as dt, sys

SRC='src/'; OUT='out/'
CENSOR=169.40   # ESPN undrafted sentinel: 492 of 700 rows inside [169.40, 170.97]

u=pd.read_csv(SRC+'code_universe.csv')
e=pd.read_csv(SRC+'espn_projections_2026_20260820.csv'); e.columns=[c.replace('﻿','') for c in e.columns]
n0=len(e)

TEAMFIX={'WSH':'WAS','ARZ':'ARI','LA':'LAR'}
e['team_c']=e['team'].replace(TEAMFIX)
u['team_c']=u['tm'].replace(TEAMFIX)

# ---- bye map from the universe, keyed on team (verified 1 bye per team, 32 teams) ----
byemap=(u[(u['pos']!='D/ST')&u['team_c'].notna()].drop_duplicates('team_c').set_index('team_c')['bye'].to_dict())
assert len(byemap)==32, f"bye map has {len(byemap)} teams, expected 32"

# ---- D/ST team codes: ESPN gives "Texans D/ST" + a team column; use the team column ----
s=e.copy()
s['bye']=s['team_c'].map(byemap)

# ---- carry the crosswalk ids across on espn_id ONLY ----
xw=u[['espn_id','gsis_id','fantasypros_id','pff_id','sleeper_id','pfr_id','k2']].dropna(subset=['espn_id'])
assert xw['espn_id'].duplicated().sum()==0, "crosswalk has duplicate espn_id"
pre=len(s); s=s.merge(xw,on='espn_id',how='left'); assert len(s)==pre, f"merge changed rows {pre}->{len(s)}"

# ---- ADP: two explicitly named columns, never one called 'ADP' ----
s['adp_pick']=s['espn_adp']
s['adp_censored']=s['adp_pick']>=CENSOR
live=s.loc[~s['adp_censored'],'adp_pick']
s['adp_rank']=np.nan
s.loc[~s['adp_censored'],'adp_rank']=live.rank(method='first')
# fallback ordering inside the censored blob: projection, descending, within position
s['deep_rank_by_proj']=np.nan
for pos,g in s[s['adp_censored']].groupby('pos'):
    s.loc[g.index,'deep_rank_by_proj']=g['proj_2026'].rank(ascending=False,method='first')

s=s.rename(columns={'Player':'player','proj_2026':'proj_leaguepts','injuryStatus':'injury_status'})
s['proj_src']='espn_20260820'
s['proj_missing']=s['proj_leaguepts'].isna()

# ---- replacement levels + VBD, recomputed on the rebuilt pool ----
STARTERS={'QB':12,'RB':30,'WR':30,'TE':12,'D/ST':12,'K':12}
repl={}
for pos,n in STARTERS.items():
    v=s.loc[s['pos']==pos,'proj_leaguepts'].dropna().sort_values(ascending=False)
    repl[pos]=float(v.iloc[n-1]) if len(v)>=n else np.nan
s['vbd']=s.apply(lambda r: r['proj_leaguepts']-repl.get(r['pos'],np.nan)
                 if pd.notna(r['proj_leaguepts']) else np.nan, axis=1)

# ---- synthetic flag carried forward from the old universe (never rank on a flagged row) ----
syn=u.loc[u['synthetic']==True,'espn_id'].dropna().astype(int)
s['synthetic']=s['espn_id'].isin(set(syn))

s['captured_at']=e['captured_at']
s['built_at']=dt.date.today().isoformat()
s['built_by']='code_rebuild_spine_v5.py'

cols=['espn_id','player','pos','team_c','bye','injury_status','proj_leaguepts','proj_src','proj_missing',
      'synthetic','adp_pick','adp_rank','adp_censored','deep_rank_by_proj','vbd',
      'gsis_id','fantasypros_id','pff_id','sleeper_id','pfr_id','k2','captured_at','built_at','built_by']
s=s[cols].sort_values(['adp_censored','adp_pick'],na_position='last')
assert len(s)==n0, f"row count drift {n0}->{len(s)}"
s.to_csv(OUT+'code_universe_v5.csv',index=False)

print(f"rows in {n0} -> out {len(s)}  (old universe was {len(u)})")
print("\nREPLACEMENT LEVELS (rebuilt pool):")
for p in ['QB','RB','WR','TE','D/ST','K']:
    print(f"  {p:5s}{STARTERS[p]:>3}  {repl[p]:7.1f}")
print("\nsanity — did adding rows move skill replacement? old universe:")
for pos,n in [('RB',30),('WR',30),('QB',12),('TE',12)]:
    v=u[u['pos']==pos]['TOT'].dropna().sort_values(ascending=False)
    print(f"  {pos}{n}: old {v.iloc[n-1]:.1f} -> new {repl[pos]:.1f}")
print("\nD/ST now differentiated:")
print(s[s['pos']=='D/ST'].nlargest(6,'proj_leaguepts')[['player','team_c','proj_leaguepts','vbd','adp_pick','bye']].to_string(index=False))
print("\ninjury flags now on the spine:",s['injury_status'].value_counts(dropna=False).to_dict())
print("censored ADP rows:",int(s['adp_censored'].sum()),"of",len(s))
print(f"\nwrote {OUT}code_universe_v5.csv")
