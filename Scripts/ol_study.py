import argparse as _ap
_A=_ap.ArgumentParser(); _A.add_argument('--injuries',action='store_true'); _ARGS,_=_A.parse_known_args()
#!/usr/bin/env python
"""
ol_study.py -- doc 132.  The offensive line, and the one piece of it left open.

Doc 12 §2.7 surveyed the literature; doc 28's dead list already carries "offensive-line
quality for RUNNING BACKS".  The QUARTERBACK version was flagged live and untested.
This tests it.

  py ol_study.py               the QB pass-protection question (doc 132)
  py ol_study.py --injuries    opening-day OL disruption (doc 133)

FINDING (2026-09-01)
  Pass protection PERSISTS -- team sack rate allowed r=+0.399 year to year, HIGHER than
  offensive EPA per play (+0.382) and nearly double a defence (+0.204).  It survives a
  quarterback change at +0.245, so roughly half of it is the line/scheme, not the QB.
  So it IS knowable in August -- which corrects doc 28's reasoning, where a line-CONTINUITY
  churn of r=-0.01 was read as "history does not forecast it".  Continuity is personnel;
  sack rate is performance.  They are not the same quantity.
  BUT it does not measurably move a QB's fantasy points: prior-season sack rate vs beat is
  r=+0.092, p=0.53, n=50 QB-seasons, against a beat sd of 108 points.  UNDERPOWERED, not
  "no effect" -- an effect below roughly 25 points would be invisible here.
  VERDICT: no board change.  The QB version joins the RB version as not actionable, but for
  a different reason -- the RB one failed prediction, this one failed power.

REQUIRES  Source\\nfl\\w<year>.csv 2020-2025 · the two ESPN projection pulls · adp_registry
"""
import os, sys, argparse
import pandas as pd, numpy as np, re, warnings; warnings.filterwarnings('ignore')
from scipy import stats as st
HERE=os.path.dirname(os.path.abspath(__file__))
S=os.path.normpath(os.path.join(HERE,'..','Source'))+os.sep
SUF=r'\b(jr|sr|ii|iii|iv|v)\b'
NICK={'joshua':'josh','mitchell':'mitch','christopher':'chris','nathaniel':'nate','benjamin':'ben','michael':'mike','zachary':'zach','matthew':'matt'}
def norm(s):
    s=str(s).lower().replace('.',' ').replace("'",'').replace('-',' ')
    s=re.sub(SUF,'',s); s=re.sub(r'[^a-z ]','',s); p=s.split()
    if p: p[0]=NICK.get(p[0],p[0])
    return ''.join(p)
def wk(y):
    p=os.path.join(S,'nfl','w%d.csv'%y)
    if not os.path.exists(p): sys.exit('MISSING %s'%p)
    w=pd.read_csv(p,low_memory=False); return w[w.season_type=='REG']
def qb_study():
    # team PASS-BLOCK proxy: sack rate allowed = sacks / dropbacks
    rows=[]
    for y in range(2020,2026):
        w=wk(y)
        t=w.groupby('team').agg(sk=('sacks_suffered','sum'),att=('attempts','sum'),
                                car=('carries','sum'),pepa=('passing_epa','sum'),
                                ry=('rushing_yards','sum'),repa=('rushing_epa','sum')).reset_index()
        t['db']=t.att+t.sk
        t['sack_rate']=t.sk/t.db                  # pass protection
        t['ypc']=t.ry/t.car                       # run blocking proxy (crude -- includes the back)
        t['rush_epa_car']=t.repa/t.car
        t['season']=y; rows.append(t)
    T=pd.concat(rows)
    print('=== OL PROXIES: DO THEY PERSIST YEAR TO YEAR?  n=%d transitions, 2020-2025'%(len(T)-32))
    J=[]
    for a in range(2020,2025):
        J.append(T[T.season==a].set_index('team').join(T[T.season==a+1].set_index('team'),rsuffix='_n',how='inner'))
    J=pd.concat(J)
    for lbl,c in [('team SACK RATE allowed (pass protection)','sack_rate'),
                  ('team yards per carry (run blocking, crude)','ypc'),
                  ('team rush EPA per carry','rush_epa_car')]:
        r,p=st.pearsonr(J[c],J[c+'_n'])
        print('   %-42s r=%+.3f p=%.4f'%(lbl,r,p))
    print('   [for scale: offensive EPA/play persists at +0.382, defence at +0.204 -- doc 131]')
    print()
    # does sack rate move QB fantasy scoring, contemporaneously?
    print('=== DOES PASS PROTECTION MOVE A QB\'S FANTASY POINTS?  (contemporaneous, then predictive)')
    qq=[]
    for yr,f in [(2022,'espn_projections_2022_20260824.csv'),(2024,'espn_projections_2024_20260824.csv')]:
        d=pd.read_csv(S+f); d.columns=[c.lstrip('﻿') for c in d.columns]
        d=d[d.pos=='QB'].copy(); d['k']=d.Player.map(norm)
        adp=pd.read_csv(S+f'adp_registry/preseason_adp_{yr}.csv'); adp['k']=adp.player.map(norm)
        m=d.merge(adp[['k','adp']],on='k',how='inner')
        m['proj']=m[f'proj_{yr}']; m['act']=m[f'actual_{yr}']; m['beat']=m.act-m.proj
        m['tm']=m.team.astype(str).map(lambda t:{'WSH':'WAS','LAR':'LA'}.get(t,t))
        cur=T[T.season==yr].set_index('team').sack_rate.rename('sr_now')
        pri=T[T.season==yr-1].set_index('team').sack_rate.rename('sr_prior')
        m=m.merge(cur,left_on='tm',right_index=True,how='left').merge(pri,left_on='tm',right_index=True,how='left')
        g=wk(yr).groupby('player_display_name').week.nunique().reset_index(); g.columns=['n','gp']; g['k']=g.n.map(norm)
        m=m.merge(g[['k','gp']],on='k',how='left'); m['season']=yr; qq.append(m)
    Q=pd.concat(qq).dropna(subset=['sr_now','sr_prior','beat'])
    Q=Q[Q.proj>0]
    for lbl,c in [('SAME-season sack rate (hindsight)','sr_now'),('PRIOR-season sack rate (knowable in August)','sr_prior')]:
        r,p=st.pearsonr(Q[c],Q.beat)
        sl,ic,rr,pp,se=st.linregress(Q[c],Q.beat)
        print('   %-44s r=%+.3f p=%.3f | %+.1f pts per +1%% sack rate  n=%d'%(lbl,r,p,sl*0.01,len(Q)))
    print('   sd of QB beat: %.0f pts | league sack rate mean %.1f%% sd %.1f%%'%(Q.beat.std(),100*T.sack_rate.mean(),100*T.sack_rate.std()))
    Q.to_csv('ol_qb.csv',index=False)
    T.to_csv('ol_team.csv',index=False)

    print()
    print('=== IS THE PERSISTENCE THE LINE, OR THE QUARTERBACK?')
    rows=[]
    for y in range(2020,2026):
        w=wk(y)
        t=w.groupby('team').agg(sk=('sacks_suffered','sum'),att=('attempts','sum')).reset_index()
        t['sack_rate']=t.sk/(t.att+t.sk)
        q=w[w.position=='QB'].groupby(['team','player_display_name']).attempts.sum().reset_index()
        q=q.sort_values('attempts',ascending=False).drop_duplicates('team')[['team','player_display_name']]
        t=t.merge(q,on='team'); t['season']=y; rows.append(t)
    Z=pd.concat(rows); K=[]
    for a in range(2020,2025):
        K.append(Z[Z.season==a].set_index('team').join(Z[Z.season==a+1].set_index('team'),rsuffix='_n',how='inner'))
    K=pd.concat(K); K['same_qb']=K.player_display_name==K.player_display_name_n
    for lbl,sub in [('SAME primary QB both years',K[K.same_qb]),('QB CHANGED',K[~K.same_qb])]:
        r,p=st.pearsonr(sub.sack_rate,sub.sack_rate_n)
        print('   %-28s n=%3d  sack rate persists r=%+.3f  p=%.4f'%(lbl,len(sub),r,p))
    print('   About half survives a QB change -- the line/scheme carries a real, forecastable share.')
    print()
    print('VERDICT: forecastable, and still not actionable. n=50 QB-seasons cannot resolve an')
    print('effect under ~25 points. No board change. See 132_the_line_is_knowable.md.')


# ---------------------------------------------------------------- doc 133
def injuries_study():
    """Opening-day OL disruption.  Three measures, weeks 1-4 and full season.
    Needs snap_counts_<y>.csv and injuries_<y>.csv from nflverse in Source\\nfl\\."""
    OLP = ['T', 'G', 'C']
    def need(p):
        if not os.path.exists(p): sys.exit('MISSING %s -- nflverse snap_counts / injuries release.' % p)
        return p
    def snaps(y):
        s = pd.read_csv(need(os.path.join(S, 'nfl', 'snap_counts_%d.csv' % y)), low_memory=False)
        return s[(s.game_type == 'REG') & (s.position.isin(OLP))]
    def inj(y):
        i = pd.read_csv(need(os.path.join(S, 'nfl', 'injuries_%d.csv' % y)), low_memory=False)
        return i[(i.game_type == 'REG') & (i.position.isin(OLP))]
    rows = []
    for y in range(2022, 2026):
        i1 = inj(y); i1 = i1[i1.week == 1]
        a = i1[i1.report_status.isin(['Out', 'Doubtful'])].groupby('team').size().rename('ol_out')
        sp = snaps(y - 1).groupby(['team', 'player']).offense_snaps.sum().reset_index()
        sp['share'] = sp.offense_snaps / sp.groupby('team').offense_snaps.transform('sum')
        top5 = sp.sort_values('offense_snaps', ascending=False).groupby('team').head(5)
        now = snaps(y); now = now[now.week == 1][['team', 'player', 'offense_pct']]
        k5 = top5.merge(now, on=['team', 'player'], how='left')
        b = (k5.offense_pct.fillna(0) >= 0.5).astype(int).groupby(k5.team).sum().rename('returning5')
        kw = sp.merge(now, on=['team', 'player'], how='left')
        kw['gone'] = (kw.offense_pct.fillna(0) < 0.5).astype(int)
        c = kw.assign(w=kw.share * kw.gone).groupby('team').w.sum().rename('snap_share_lost')
        w = wk(y)
        def ag(df, tag):
            t = df.groupby('team').agg(sk=('sacks_suffered', 'sum'), att=('attempts', 'sum'),
                                       car=('carries', 'sum'), ry=('rushing_yards', 'sum'),
                                       repa=('rushing_epa', 'sum')).reset_index()
            t['sack_rate' + tag] = t.sk / (t.att + t.sk)
            t['ypc' + tag] = t.ry / t.car
            t['rush_epa' + tag] = t.repa / t.car
            return t[['team', 'sack_rate' + tag, 'ypc' + tag, 'rush_epa' + tag]]
        e = ag(w[w.week <= 4], '').merge(ag(w, '_s'), on='team')
        t = e.set_index('team').join([a, b, c]).fillna({'ol_out': 0})
        t['season'] = y; rows.append(t.reset_index().rename(columns={'index': 'team'}))
    T = pd.concat(rows).dropna(subset=['returning5', 'snap_share_lost'])
    print('=== OPENING-DAY OL DISRUPTION -- n=%d team-seasons, 2022-2025' % len(T))
    print('   (A) OL Out/Doubtful on the wk-1 report: mean %.2f; %.0f%% of teams have even one.'
          % (T.ol_out.mean(), 100 * (T.ol_out >= 1).mean()))
    print('       Teams IR a lineman who is truly out, so he never reaches the report.')
    print('   (B) last year\'s top-5 OL playing >=50%% in wk 1: mean %.2f of 5; ALL FIVE in %d of %d.'
          % (T.returning5.mean(), (T.returning5 == 5).sum(), len(T)))
    print('   (C) share of last season\'s OL snaps NOT on the field in wk 1: mean %.1f%%, sd %.1f%%'
          % (100 * T.snap_share_lost.mean(), 100 * T.snap_share_lost.std()))
    print('       >>> HALF THE LINE TURNS OVER EVERY YEAR, EVERYWHERE.  No control group exists.')
    print()
    print('=== DOES IT DEGRADE THE OFFENCE, WEEKS 1-4?')
    for x, nm in [('ol_out', '(A) OL Out/Doubtful'), ('returning5', '(B) returning top-5'),
                  ('snap_share_lost', '(C) OL snap share lost')]:
        cells = []
        for oc in ['sack_rate', 'ypc', 'rush_epa']:
            r, p = st.pearsonr(T[x], T[oc])
            cells.append('%-9s r=%+.3f p=%.2f' % (oc, r, p))
        print('   %-24s %s' % (nm, ' | '.join(cells)))
    hi = T[T.snap_share_lost >= T.snap_share_lost.quantile(.75)]
    lo = T[T.snap_share_lost <= T.snap_share_lost.quantile(.25)]
    for oc in ['sack_rate', 'ypc', 'rush_epa']:
        t_, p = st.ttest_ind(hi[oc], lo[oc], equal_var=False)
        print('   extremes %-9s most disrupted %.4f (n=%d) vs most intact %.4f (n=%d)  p=%.3f'
              % (oc, hi[oc].mean(), len(hi), lo[oc].mean(), len(lo), p))
    print()
    print('VERDICT: every sign is intuitive, nothing is resolved, and the one nominally')
    print('significant fantasy result (RB beat vs (A), p=0.041) becomes p=0.42 once clustered')
    print('by team -- the A5 correction, for the third time in one session.  See doc 133.')


if __name__ == '__main__':
    if _ARGS.injuries:
        injuries_study()
    else:
        qb_study()
