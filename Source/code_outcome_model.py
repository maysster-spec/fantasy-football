import pandas as pd, numpy as np, json, re
def norm(s):
    s=str(s).lower(); s=re.sub(r"[^a-z ]","",s)
    s=re.sub(r"\b(jr|sr|ii|iii|iv|v)\b","",s); return re.sub(r"\s+"," ",s).strip()
def gp(x):
    try:
        d=json.loads(x); return float(d.get("210")) if "210" in d else np.nan
    except Exception: return np.nan

SRC={2021:('/tmp/audit_src/espn_projections_2022_20260824.csv','proj_2021','actual_2021',None,None),
     2022:('/tmp/audit_src/espn_projections_2022_20260824.csv','proj_2022','actual_2022','raw_stats','raw_actual_stats'),
     2024:('/tmp/audit_src/espn_projections_2024_20260824.csv','proj_2024','actual_2024','raw_stats','raw_actual_stats'),
     2025:('/tmp/audit_src/espn_projections_2026_20260820.csv','proj_2025','actual_2025',None,None)}
rows=[]
for yr,(f,pc,ac,rp,ra) in SRC.items():
    d=pd.read_csv(f); d.columns=[c.lstrip('﻿') for c in d.columns]
    keep=['Player','pos',pc,ac]+[c for c in (rp,ra) if c]
    d=d[keep].rename(columns={pc:'proj',ac:'actual',rp:'rp',ra:'ra'})
    d=d[d.pos.isin(['QB','RB','WR','TE'])].dropna(subset=['proj','actual'])
    d=d[d.proj>20]
    d['gp_a']=d.ra.map(gp) if 'ra' in d else np.nan
    d['k']=d.Player.map(norm)
    a=pd.read_csv(f'/tmp/n412/adp/preseason_adp_{yr}.csv')[['k','adp']]
    m=d.merge(a,on='k',how='inner'); m['year']=yr
    rows.append(m[['Player','k','pos','proj','actual','gp_a','adp','year']])
D=pd.concat(rows,ignore_index=True); D=D[D.adp<=180].copy()
have=D.gp_a.notna()
print(f"n={len(D)}  with games-played: {have.sum()} ({sorted(D.loc[have,'year'].unique())})")
print("gp_a distribution:", D.loc[have,'gp_a'].describe()[['mean','std','min','25%','50%','max']].round(2).to_dict())

# decompose on the seasons where GP is present
E=D[have].copy()
E['gp_a']=E.gp_a.clip(0,17)
E['ppg_a']=E.actual/E.gp_a.replace(0,np.nan)
E['ppg_p']=E.proj/15.32                       # doc 42: ESPN's implied games
E['form']=(E.ppg_a/E.ppg_p).clip(0,3.0)       # per-game form, injury removed
E=E.dropna(subset=['form'])
E['band']=pd.cut(E.adp,[0,24,48,84,120,180],labels=['1-24','25-48','49-84','85-120','121-180'])
def desc(g):
    return pd.Series(dict(n=len(g), form_mean=g.form.mean(), form_sd=g.form.std(),
        form_p10=g.form.quantile(.1), form_p90=g.form.quantile(.9),
        gp_mean=g.gp_a.mean(), gp_sd=g.gp_a.std(), gp_p10=g.gp_a.quantile(.1)))
print("\n=== PER-GAME FORM (injury stripped out) and GAMES PLAYED, by ADP band ===")
print(E.groupby('band',observed=True).apply(desc,include_groups=False).round(2).to_string())
print("\n=== by position ===")
print(E.groupby('pos').apply(desc,include_groups=False).round(2).to_string())
print("\ncorr(form, games played):", round(E[['form','gp_a']].corr().iloc[0,1],3))
E.to_csv('/tmp/var/decomposed.csv',index=False)
print("\nboom (form>1.35):", round((E.form>1.35).mean(),3), " bust (form<0.70):", round((E.form<0.70).mean(),3))
