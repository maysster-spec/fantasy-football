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

--- PATCHED 2026-08-28, doc 61 (D1/D2/D3/D5) + doc 62 + doc 63. Four changes, all marked [P]. ---
"""
import pandas as pd, numpy as np, datetime as dt, sys, glob, os

SRC='src/'; OUT='out/'
CENSOR=169.40   # ESPN undrafted sentinel: 492 of 700 rows inside [169.40, 170.97]

# [P-D5] The input was a bare hardcoded filename. The patched pull script now writes
# espn_projections_2026_<YYYYMMDD>_<HHMM>.csv, so a Sep-5 re-pull would leave this
# reading the Aug-20 file and silently rebuild the spine on stale projections,
# stamped with today's date. Doc 62 then showed the downstream board has NO builder,
# so a fresh spine cannot reach board_v8_fixed.csv anyway.
# Therefore this does NOT auto-glob to the newest file: that would silently desync the
# spine from a frozen board, and code_integrity.py does not compare their projections.
# It stays pinned, and REFUSES TO RUN if a newer pull exists. Loud, not silent.
PINNED = 'espn_projections_2026_20260820.csv'
_newer = sorted(os.path.basename(p) for p in glob.glob(SRC + 'espn_projections_2026_*.csv')
                if os.path.basename(p) > PINNED)
if _newer:
    sys.exit(
        f"PULL/SPINE MISMATCH — refusing to build.\n"
        f"  pinned : {PINNED}\n"
        f"  newer  : {', '.join(_newer)}\n"
        f"  Doc 63 measured ZERO change in proj_2026 between the 08-20 and 08-23 pulls\n"
        f"  (0 of 700 rows). If the newest pull also shows zero projection change, the\n"
        f"  spine does not need rebuilding at all. If it DOES show change, doc 62's\n"
        f"  freeze-vs-reconstruct decision must be made first — board_v8_fixed.csv has\n"
        f"  no builder, so a fresh spine cannot reach the board.\n"
        f"  Update PINNED here deliberately once that decision is made.")

u=pd.read_csv(SRC+'code_universe.csv')
e=pd.read_csv(SRC+PINNED); e.columns=[c.replace('﻿','') for c in e.columns]
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
# [P-D1] The assert above CANNOT fire on a broken join: a left merge always preserves
# left length. Measured (doc 61): a key with trailing whitespace matched 0 of 3 rows and
# the assert passed. Report the match RATE, which is the thing that actually degrades.
# Non-fatal on purpose -- the true expected rate has never been measured on real inputs.
_rate = s['gsis_id'].notna().mean()
print(f"[join] crosswalk match rate {_rate:.1%} ({int(s['gsis_id'].notna().sum())}/{len(s)})")
if _rate < 0.80:
    print(f"[join] *** WARNING: match rate {_rate:.1%} is low -- suspect an espn_id dtype or "
          f"whitespace defect (ERROR_PATTERNS C1), not a real data gap.", file=sys.stderr)

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
s['proj_src']=PINNED.replace('espn_projections_','espn_').replace('.csv','')
s['proj_missing']=s['proj_leaguepts'].isna()

# ---- replacement levels + VBD, recomputed on the rebuilt pool ----
STARTERS={'QB':12,'RB':30,'WR':30,'TE':12,'D/ST':12,'K':12}
repl={}
for pos,n in STARTERS.items():
    v=s.loc[s['pos']==pos,'proj_leaguepts'].dropna().sort_values(ascending=False)
    repl[pos]=float(v.iloc[n-1]) if len(v)>=n else np.nan
s['vbd']=s.apply(lambda r: r['proj_leaguepts']-repl.get(r['pos'],np.nan)
                 if pd.notna(r['proj_leaguepts']) else np.nan, axis=1)
# [P-D2] Directive 4.8: D/ST and K draft value is not realizable, and their vbd is on a
# scale that is NOT comparable to skill vbd. Measured (doc 61): on a naive cross-position
# sort the best D/ST lands at rank 34 and the best K at 39 -- inside the pick-41 window.
# The shipped board is safe only because K/D-ST were separated into a different file.
# Null it AT SOURCE so no future consumer of the spine can inherit the poison.
s.loc[s['pos'].isin(['K','D/ST']),'vbd']=np.nan

# ---- synthetic flag carried forward from the old universe (never rank on a flagged row) ----
# [P-D3] Was `s['espn_id'].isin(set(syn))` with syn cast to int. Measured (doc 61): if
# espn_id ever reads as object/str this silently matches 0 rows and the flag is all-False
# with no error. Coerce both sides.
syn=set(pd.to_numeric(u.loc[u['synthetic']==True,'espn_id'],errors='coerce').dropna().astype(int))
s['synthetic']=pd.to_numeric(s['espn_id'],errors='coerce').isin(syn)

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
    print(f"  {p:5s}{STARTERS[p]:>3}  {repl[p]:7.1f}"
          + ("   [vbd nulled at source -- 4.8]" if p in ('K','D/ST') else ""))
print("\nsanity — did adding rows move skill replacement? old universe:")
for pos,n in [('RB',30),('WR',30),('QB',12),('TE',12)]:
    v=u[u['pos']==pos]['TOT'].dropna().sort_values(ascending=False)
    print(f"  {pos}{n}: old {v.iloc[n-1]:.1f} -> new {repl[pos]:.1f}")
print("\nD/ST now differentiated:")
print(s[s['pos']=='D/ST'].nlargest(6,'proj_leaguepts')[['player','team_c','proj_leaguepts','vbd','adp_pick','bye']].to_string(index=False))
print("\ninjury flags now on the spine:",s['injury_status'].value_counts(dropna=False).to_dict())
print("censored ADP rows:",int(s['adp_censored'].sum()),"of",len(s))
print(f"\nwrote {OUT}code_universe_v5.csv")
