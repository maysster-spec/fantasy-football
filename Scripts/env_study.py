#!/usr/bin/env python
"""
env_study.py -- "opportunity environment" measurement.  Doc 128.

Answers: how much of a player's target change is his TEAM throwing more,
versus HIM taking a bigger slice?  And is a team-level environment signal
worth putting on the board?

Answer (measured 2026-09-01): team volume is 7.5% of the variance for WR/TE,
5.7% for RB.  Perfect foresight of it is worth about +2 points a season.
Do not build the flag.  See 128_opportunity_environment.md.

USAGE
  py env_study.py                 # rerun every measurement in doc 128
  py env_study.py --vacated       # just the 2026 vacated-target table
  py env_study.py --team-volume   # just ESPN's 2026 repricing vs 2025 actual

REQUIRES
  Source\espn_projections_2022_20260824.csv
  Source\espn_projections_2024_20260824.csv
  Source\espn_projections_2026_*.csv          (newest is used)
  nflverse weekly player stats 2022-2025 as  Source\nfl\w<year>.csv
     -> https://github.com/nflverse/nflverse-data/releases/tag/player_stats
        file: stats_player_week_<year>.csv   (rename to w<year>.csv)

NOTE  espn_projections_2023 is NOT usable here: only 5 of 103 QB rows carry a
      non-zero projected pass attempt.  It is skipped deliberately, not missed.
"""
import argparse, glob, json, os, re, sys, warnings
import numpy as np, pandas as pd
from scipy import stats as st
warnings.filterwarnings('ignore')

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(os.path.dirname(HERE), 'Source')
NFL  = os.path.join(SRC, 'nfl')
TMAP = {'WSH': 'WAS', 'LAR': 'LA'}
SUF  = r'\b(jr|sr|ii|iii|iv|v)\b'
NICK = {'joshua':'josh','mitchell':'mitch','christopher':'chris','nathaniel':'nate',
        'benjamin':'ben','michael':'mike','zachary':'zach','matthew':'matt'}
# ESPN stat ids, verified against nflverse (r=1.000, MAD=0.0, n=292 receivers, 2024)
ATT, TGT, REC = '0', '58', '53'   # doc 131: receptions is 53 in PROJECTIONS, 41+53 in ACTUALS


def norm(s):
    """§3 identity rule: no bare name joins.  Suffix + nickname normalised key."""
    s = str(s).lower().replace('.', ' ').replace("'", '').replace('-', ' ')
    s = re.sub(SUF, '', s)
    s = re.sub(r'[^a-z ]', '', s)
    p = s.split()
    if p:
        p[0] = NICK.get(p[0], p[0])
    return ''.join(p)


def stat(v, k):
    try:
        return float(json.loads(v).get(k, 0) or 0)
    except Exception:
        return 0.0


def espn(path):
    d = pd.read_csv(path)
    d.columns = [c.lstrip('﻿') for c in d.columns]
    d['tm'] = d.team.astype(str).map(lambda t: TMAP.get(t, t))
    d['key'] = d.Player.map(norm)
    return d


def week(year):
    p = os.path.join(NFL, 'w%d.csv' % year)
    if not os.path.exists(p):
        sys.exit('MISSING %s -- see the REQUIRES block at the top of this file.' % p)
    w = pd.read_csv(p, low_memory=False)
    return w[w.season_type == 'REG']


def newest_2026():
    g = sorted(glob.glob(os.path.join(SRC, 'espn_projections_2026_*.csv')))
    if not g:
        sys.exit('no espn_projections_2026_*.csv in %s' % SRC)
    return g[-1]


# ---------------------------------------------------------------- section 1
def decompose():
    print('=== 1. WHERE A TARGET CHANGE COMES FROM  (nflverse only, no ESPN proxy)')
    for pos, minv, label in [(['WR', 'TE'], 50, 'WR/TE, >=50 targets'),
                             (['RB'],     100, 'RB, >=100 touches')]:
        rows = []
        for y in (2023, 2024, 2025):
            a, b = week(y - 1), week(y)
            ta, tb = a.groupby('team').attempts.sum(), b.groupby('team').attempts.sum()

            def agg(df):
                return (df[df.position.isin(pos)]
                        .groupby(['player_display_name', 'team'])
                        .agg(t=('targets', 'sum'), c=('carries', 'sum'), g=('week', 'nunique'))
                        .reset_index())
            m = agg(a).merge(agg(b), on='player_display_name', suffixes=('0', '1'))
            base = (m.t0 + m.c0) if pos == ['RB'] else m.t0
            m = m[(base >= minv) & (m.g0 >= 12) & (m.g1 >= 12) & (m.t1 > 0)]
            m['va'] = m.team0.map(ta); m['vb'] = m.team1.map(tb)
            m = m.dropna(subset=['va', 'vb'])
            m['d_tgt'] = np.log(m.t1.clip(lower=1) / m.t0.clip(lower=1))
            m['d_vol'] = np.log(m.vb / m.va)
            m['d_shr'] = m.d_tgt - m.d_vol
            rows.append(m)
        D = pd.concat(rows)
        vt, vv, vs = D.d_tgt.var(), D.d_vol.var(), D.d_shr.var()
        cov = D[['d_vol', 'd_shr']].cov().iloc[0, 1]
        print('   %s, >=12 games both years.  n=%d pairs, 3 transitions' % (label, len(D)))
        print('     Var(log target change) %.4f  [sd %.1f%%]' % (vt, 100 * np.sqrt(vt)))
        print('       team pass VOLUME     %.4f  = %4.1f%%  [sd %.1f%%]'
              % (vv, 100 * vv / vt, 100 * np.sqrt(vv)))
        print('       his own SHARE        %.4f  = %4.1f%%  [sd %.1f%%]'
              % (vs, 100 * vs / vt, 100 * np.sqrt(vs)))
        print('       2*cov               %+.4f  = %+4.1f%%' % (2 * cov, 100 * 2 * cov / vt))
        print('     corr(volume, target change) %+.3f   corr(share, target change) %+.3f'
              % (D.d_vol.corr(D.d_tgt), D.d_shr.corr(D.d_tgt)))
        if pos == ['RB']:
            r = D[(D.t0 >= 20)]
            print('     stickiness yr->yr: targets/g r=%+.3f  carries/g r=%+.3f'
                  % ((r.t0 / r.g0).corr(r.t1 / r.g1), (r.c0 / r.g0).corr(r.c1 / r.g1)))


# ---------------------------------------------------------------- section 2
def oracle():
    print()
    print('=== 2. ORACLE UPPER BOUND -- perfect foresight of the team volume change')
    T, P = [], []
    for yr, f in [(2022, 'espn_projections_2022_20260824.csv'),
                  (2024, 'espn_projections_2024_20260824.csv')]:
        p = os.path.join(SRC, f)
        if not os.path.exists(p):
            print('   skipping %d, missing %s' % (yr, f)); continue
        d = espn(p); w = week(yr)
        d['p_att'] = d.raw_stats.map(lambda v: stat(v, ATT))
        tp = d[(d.pos == 'QB') & (d.p_att > 0)].groupby('tm').p_att.max().rename('p_att')
        ta = w.groupby('team').attempts.sum().rename('a_att')
        t = pd.concat([tp, ta], axis=1).dropna(); t = t[t.p_att > 50]
        t['season'] = yr; t = t.reset_index().rename(columns={'index': 'tm'}); T.append(t)
        pl = d[d.pos.isin(['WR', 'TE', 'RB'])].copy()
        pl['p_tgt'] = pl.raw_stats.map(lambda v: stat(v, TGT))
        ap = (w.groupby('player_display_name')
                .agg(a_tgt=('targets', 'sum'), g=('week', 'nunique')).reset_index())
        ap['key'] = ap.player_display_name.map(norm)
        pl = pl.merge(ap, on='key', how='left')
        pl['proj'] = pl['proj_%d' % yr]; pl['act'] = pl['actual_%d' % yr]; pl['season'] = yr
        P.append(pl[['Player', 'pos', 'tm', 'season', 'p_tgt', 'a_tgt', 'g', 'proj', 'act']])
    if not T:
        return
    T = pd.concat(T); P = pd.concat(P); T['surp'] = T.a_att - T.p_att
    print('   ESPN team pass-volume forecast: r=%+.3f  MAE=%.0f att  n=%d team-seasons'
          % (T.p_att.corr(T.a_att), T.surp.abs().mean(), len(T)))
    for y in sorted(T.season.unique()):
        s = T[T.season == y]
        print('     %d n=%d r=%+.3f' % (y, len(s), s.p_att.corr(s.a_att)))
    M = P.merge(T[['tm', 'season', 'surp']], on=['tm', 'season'], how='inner')
    M['beat'] = M.act - M.proj
    for lbl, sub in [('WR/TE', M[M.pos.isin(['WR', 'TE']) & (M.p_tgt >= 40)]),
                     ('WR',    M[(M.pos == 'WR') & (M.p_tgt >= 40)]),
                     ('TE',    M[(M.pos == 'TE') & (M.p_tgt >= 40)]),
                     ('RB',    M[(M.pos == 'RB') & (M.p_tgt >= 25)])]:
        sub = sub[(sub.a_tgt > 0) & (sub.g >= 8)]
        if len(sub) < 25:
            continue
        sl, ic, r, p_, se = st.linregress(sub.surp, sub.beat)
        print('   %-5s n=%3d r=%+.3f p=%.3f | %+.1f pts per +50 team attempts '
              'CI[%+.1f,%+.1f] | sd(beat)=%.0f'
              % (lbl, len(sub), r, p_, sl * 50, (sl - 1.96 * se) * 50,
                 (sl + 1.96 * se) * 50, sub.beat.std()))
    print('   +50 attempts is a ~9% environment change -- a real coordinator/QB swap.')


# ---------------------------------------------------------------- section 3
def vacated(write=True):
    print()
    print('=== 3. VACATED TARGET SHARE 2026  (targeting list -- FAILS as a predictor, see 4)')
    d = espn(newest_2026())
    roster = dict(zip(d.key, d.tm))
    w = week(2025); w = w[w.position.isin(['WR', 'TE', 'RB', 'FB'])]
    p = (w.groupby(['player_display_name', 'team']).targets.sum().reset_index()
           .sort_values('targets', ascending=False).drop_duplicates('player_display_name'))
    p['key'] = p.player_display_name.map(norm)
    p['tm26'] = p.key.map(roster)
    p['vac'] = p.tm26.isna() | (p.tm26 != p.team)
    unmatched = p[p.tm26.isna() & (p.targets >= 30)]
    moved = p[p.tm26.notna() & p.vac & (p.targets >= 30)]
    print('   JOIN AUDIT (§3 identity rule -- the first build of this table reported 8 FALSE')
    print('   departures out of 15 from suffix mismatches: Pitts Sr., Pittman Jr., Etienne Jr.,')
    print('   Jones Sr., Sills V, Tre\' Harris, Gadsden, Joshua Palmer.)')
    print('   %d moved to a named 2026 team -- safe.  %d are NOT on the 2026 board at all;'
          % (len(moved), len(unmatched)))
    print('   those are the join-failure risk and must be eyeballed:')
    print('     ' + '; '.join('%s %s %d' % (r.player_display_name, r.team, r.targets)
                              for _, r in unmatched.nlargest(12, 'targets').iterrows()))
    tt = p.groupby('team').targets.sum().rename('tgt25')
    v = p[p.vac].groupby('team').targets.sum().rename('vacated')
    out = pd.concat([tt, v], axis=1).fillna(0)
    out['pct'] = 100 * out.vacated / out.tgt25
    out = out.sort_values('pct', ascending=False)
    print('   median %.1f%%  sd %.1f' % (out.pct.median(), out.pct.std()))
    print('   most vacated: ' + '  '.join('%s %.0f%%' % (t, r.pct)
                                          for t, r in out.head(8).iterrows()))
    print('   least:        ' + '  '.join('%s %.0f%%' % (t, r.pct)
                                          for t, r in out.tail(5).iterrows()))
    if write:
        o = os.path.join(SRC, 'vacated_targets_2026.csv')
        out.to_csv(o); print('   wrote %s' % o)
    return out


# ---------------------------------------------------------------- section 4
def vacated_test():
    print()
    print('=== 4. DOES VACATED SHARE PREDICT?  (2024 is the only testable season)')
    f = os.path.join(SRC, 'espn_projections_2024_20260824.csv')
    if not os.path.exists(f):
        print('   skipped, no 2024 projection file'); return
    d = espn(f); roster = dict(zip(d.key, d.tm))
    w = week(2023); w = w[w.position.isin(['WR', 'TE', 'RB', 'FB'])]
    p = (w.groupby(['player_display_name', 'team']).targets.sum().reset_index()
           .sort_values('targets', ascending=False).drop_duplicates('player_display_name'))
    p['key'] = p.player_display_name.map(norm); p['tm24'] = p.key.map(roster)
    p['vac'] = p.tm24.isna() | (p.tm24 != p.team)
    tm = pd.concat([p.groupby('team').targets.sum().rename('tgt'),
                    p[p.vac].groupby('team').targets.sum().rename('vacated')], axis=1).fillna(0)
    tm['pct_vac'] = 100 * tm.vacated / tm.tgt
    d['proj'] = d.proj_2024; d['act'] = d.actual_2024
    m = (p[~p.vac].merge(d[d.pos.isin(['WR', 'TE', 'RB'])][['key', 'pos', 'proj', 'act']],
                         on='key', how='inner'))
    m = m[m.proj >= 40].merge(tm[['pct_vac']], left_on='team', right_index=True)
    m['beat'] = m.act - m.proj
    sl, ic, r, p_, se = st.linregress(m.pct_vac, m.beat)
    print('   player-level  n=%d  r=%+.3f p=%.3f  %+.2f pts per +10%% vacated'
          % (len(m), r, p_, sl * 10))
    g = m.groupby('team').agg(beat=('beat', 'mean'), pct=('pct_vac', 'first'), n=('beat', 'size'))
    g = g[g.n >= 2]
    sl, ic, r, p_, se = st.linregress(g.pct, g.beat)
    print('   TEAM-CLUSTERED n=%d teams  r=%+.3f p=%.3f  %+.2f pts per +10%% vacated '
          'CI[%+.2f,%+.2f]' % (len(g), r, p_, sl * 10, (sl - 1.96 * se) * 10,
                               (sl + 1.96 * se) * 10))
    print('   Vacated share is a TEAM CONSTANT.  The honest n is the team count, not the')
    print('   player count -- the ERROR_PATTERNS A5 correction that killed PROE.  NOT SHIPPABLE.')


# ---------------------------------------------------------------- section 5
def team_volume_2026():
    print()
    print('=== 5. WHAT ESPN HAS ALREADY REPRICED FOR 2026  (descriptive -- no edge in it)')
    d = espn(newest_2026())
    d['p_att'] = d.raw_stats.map(lambda v: stat(v, ATT))
    p26 = d[(d.pos == 'QB') & (d.p_att > 0)].groupby('tm').p_att.sum().rename('proj_2026')
    a25 = week(2025).groupby('team').attempts.sum().rename('att_2025')
    t = pd.concat([p26, a25], axis=1).dropna()
    t['chg'] = t.proj_2026 - t.att_2025; t['pct'] = 100 * t.chg / t.att_2025
    t = t.sort_values('chg', ascending=False)
    print('   sd of the change: %.0f attempts (%.1f%%)  n=%d teams'
          % (t.chg.std(), t.pct.std(), len(t)))
    print('   more: ' + '  '.join('%s %+.0f' % (i, r.chg) for i, r in t.head(6).iterrows()))
    print('   less: ' + '  '.join('%s %+.0f' % (i, r.chg) for i, r in t.tail(6).iterrows()))
    print('   These are INSIDE the projection and therefore inside VBD.  A team ESPN has')
    print('   already moved carries no edge from that move.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--vacated', action='store_true')
    ap.add_argument('--team-volume', action='store_true')
    a = ap.parse_args()
    if a.vacated:
        vacated()
    elif a.team_volume:
        team_volume_2026()
    else:
        decompose(); oracle(); vacated(); vacated_test(); team_volume_2026()
        print()
        print('VERDICT: team environment is 7.5% of the variance and worth ~+2 pts with')
        print('perfect foresight.  The role/share half is 93% and is already flagged by')
        print('depth_map.py (UNSETTLED / job worth, directive §4.20).  No new flag.')
