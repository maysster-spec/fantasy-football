#!/usr/bin/env python3
"""RED TEAM OF MY OWN T1/T2 (0.2): the obvious confound is OPPONENT QUALITY. Inside one
team-season, the games where my offence looks good are the games against weak opponents -- and a
weak opponent is also why my defence scored. So every number is re-run with the opponent-season
swept out as well (two-way within transformation, team-season AND opponent-season), which is the
only way the surviving variation is 'this same defence, against this same opponent, on a busier
than usual day'."""
# INPUTS: play_by_play_{2021..2025}.csv.gz from
#   https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_<year>.csv.gz
#   plus Source\\dst_weekly_2021_2025.csv. ~95 MB of play-by-play, so this is a research
#   script for the record and not part of any weekly run.
import math, numpy as np, pandas as pd
tg = pd.read_csv('tired_games.csv')
tg['ts'] = tg.team+'_'+tg.season.astype(str)
tg['os'] = tg.opp +'_'+tg.season.astype(str)
tg['abs_margin']=tg.margin_q4.abs()

VARS=['q4_allowed','faced13','faced_all','own_epa13','own_plays13','three_and_outs13',
      'dst_pts','margin_q4','abs_margin','allowed']
def twoway(cols, iters=40):
    d=tg[cols+['ts','os']].dropna().copy()
    for c in cols:
        for _ in range(iters):
            d[c]-=d.groupby('ts')[c].transform('mean')
            d[c]-=d.groupby('os')[c].transform('mean')
    return d
W = twoway(VARS)
print(f"  two-way demeaned rows: {len(W):,}   (team-season and opponent-season both swept out)")

def ols(d, y, X, label, dfloss=0):
    dd=d[[y]+X].dropna(); Xm=np.column_stack([np.ones(len(dd))]+[dd[c].values for c in X]); yv=dd[y].values
    b,*_=np.linalg.lstsq(Xm,yv,rcond=None); r=yv-Xm@b; n,k=Xm.shape
    s2=r@r/(n-k-dfloss); se=np.sqrt(np.diag(s2*np.linalg.inv(Xm.T@Xm)))
    print(f"\n  {label}   n={n:,}")
    for nm,bi,si in zip(X,b[1:],se[1:]):
        t=bi/si; p=2*(1-0.5*(1+math.erf(abs(t)/math.sqrt(2))))
        lo,hi=bi-1.96*si, bi+1.96*si
        print(f"      {nm:<22} {bi:+9.4f}  CI [{lo:+7.4f},{hi:+7.4f}]  t {t:+6.2f}  p {p:.4f}"
              f"{'  <<<' if p<0.05 else ''}")
    return b,se

DF = 2*160          # ~160 team-seasons on each side
print("\n"+"="*78); print("  T1 TIRED -- Q4 points allowed vs plays faced Q1-3"); print("="*78)
ols(W,'q4_allowed',['faced13'],'no score control', DF)
ols(W,'q4_allowed',['faced13','margin_q4','abs_margin'],'with the score-state controls', DF)
sd13=W.faced13.std(); print(f"      [sd of the surviving plays-faced variation = {sd13:.2f} plays]")

print("\n"+"="*78); print("  T2 CRATER -- D/ST fantasy points vs his own offence"); print("="*78)
b,_=ols(W,'dst_pts',['own_epa13'],'own offence EPA/play, Q1-3', DF)
sde=W.own_epa13.std(); print(f"      [sd {sde:.3f} EPA/play -> {b[1]*sde:+.2f} D/ST points per sd]")
b,_=ols(W,'dst_pts',['three_and_outs13'],'own three-and-outs, Q1-3', DF)
print(f"      [sd {W.three_and_outs13.std():.2f} -> {b[1]*W.three_and_outs13.std():+.2f} per sd]")
b,_=ols(W,'dst_pts',['faced_all'],'plays faced, whole game', DF)
print(f"      [sd {W.faced_all.std():.2f} plays -> {b[1]*W.faced_all.std():+.2f} D/ST points per sd]")
b,_=ols(W,'allowed',['faced_all'],'points allowed, whole game', DF)
print(f"      [-> {b[1]*W.faced_all.std():+.2f} points allowed per sd of plays faced]")
b,_=ols(W,'dst_pts',['own_epa13','faced_all'],'both together (do they overlap?)', DF)

# decile spread: the honest 'how big is it' answer
raw=tg.dropna(subset=['dst_pts','own_epa13']).copy()
raw['q']=pd.qcut(W.own_epa13.reindex(raw.index), 5, labels=False)
print("\n  D/ST points by quintile of (two-way demeaned) own-offence EPA:")
for q,g in raw.groupby('q'):
    print(f"      Q{int(q)+1}  n={len(g):4d}   D/ST {g.dst_pts.mean():5.2f}   allowed {g.allowed.mean():5.2f}")
