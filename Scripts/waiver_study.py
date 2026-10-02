#!/usr/bin/env python3
r"""
waiver_study.py -- doc 111.  The provenance for directive 4.19 and 4.17b.

Answers two questions that had only ever been answered league-wide:
  1. How often does a waiver add that MATT makes turn into a startable player?
  2. How many weeks a season is a drafted starting QB / a drafted RB1-2 actually missing?

WHY THIS EXISTS AS A FILE: doc 12's hit rates are quoted all over this project and its bar is
unrecoverable from its text (its QB 0.62 cannot come from the replacement ppg it prints).  So the
bar is DECLARED here, at the top, and both sides of every comparison are measured under it.
Change BAR and every number moves together -- which is the point.

INPUTS   Source\waiver_report_2022..2025.csv, Source\draft_history_2021_2025.csv,
         ..\03_data\manager_identity_map.csv,
         nflverse weekly stats (downloaded to .\nfl\ on first run; needs internet ONCE)
OUTPUT   .\waiver_study.csv  plus a printed summary
RUN      py waiver_study.py
"""
import os, re, sys, urllib.request
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.normpath(os.path.join(HERE, '..', 'Source'))
IDMAP= os.path.normpath(os.path.join(HERE, '..', '03_data', 'manager_identity_map.csv'))
NFL  = os.path.join(HERE, 'nfl')
YEARS= (2022, 2023, 2024, 2025)
MATT = 'MATT (JUG)'

# THE BAR.  From the add week through week 14 (the fantasy regular season), points per PLAYED
# week must reach the position's replacement rate.  These are doc 12's own VBD levels.
BAR = {'QB': 20.09, 'RB': 9.92, 'WR': 9.62, 'TE': 8.25}

# league scoring, directive section 2
def _n(d, c): return pd.to_numeric(d[c], errors='coerce').fillna(0) if c in d.columns else 0.0
def score(d):
    return (0.04*_n(d,'passing_yards') + 6*_n(d,'passing_tds') - 2*_n(d,'passing_interceptions')
          + 0.1*_n(d,'rushing_yards')  + 6*_n(d,'rushing_tds')
          + 0.1*_n(d,'receiving_yards')+ 6*_n(d,'receiving_tds') + 0.5*_n(d,'receptions')
          - 2*(_n(d,'rushing_fumbles_lost')+_n(d,'receiving_fumbles_lost')+_n(d,'sack_fumbles_lost'))
          + 2*(_n(d,'passing_2pt_conversions')+_n(d,'rushing_2pt_conversions')+_n(d,'receiving_2pt_conversions'))
          + 6*_n(d,'special_teams_tds'))

def key(s):
    s = re.sub(r'\b(jr|sr|ii|iii|iv|v)\b', '', str(s).lower())
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z ]', '', s)).strip()

def weekly():
    os.makedirs(NFL, exist_ok=True)
    out = []
    for y in YEARS:
        f = os.path.join(NFL, f'w{y}.csv')
        if not os.path.exists(f):
            url = ('https://github.com/nflverse/nflverse-data/releases/download/'
                   f'stats_player/stats_player_week_{y}.csv')
            print(f'  downloading {y} ...'); urllib.request.urlretrieve(url, f)
        d = pd.read_csv(f, low_memory=False)
        d = d[d.season_type == 'REG']
        out.append(pd.DataFrame({'season': y, 'week': d.week.astype(int),
                                 'pos': d.position, 'k': d.player_display_name.map(key),
                                 'pts': score(d)}))
    W = pd.concat(out, ignore_index=True)
    return W[W.pos.isin(BAR)]

def main():
    W = weekly()
    grp = {k: v for k, v in W.groupby(['season', 'k'])}

    ident = pd.read_csv(IDMAP)
    t2m = {str(r[c]).strip(): r['manager'] for _, r in ident.iterrows()
           for c in ('team_2022','team_2023','team_2024','team_2025')
           if isinstance(r[c], str) and r[c].strip()}

    rows = []
    for y in YEARS:
        d = pd.read_csv(os.path.join(SRC, f'waiver_report_{y}.csv'))
        d = d[d.Status.astype(str).str.upper() == 'EXECUTED']
        for _, r in d.iterrows():
            m = re.match(r'\s*ADD\s+(.+?)(?:\s*\|\s*DROP\b.*)?$', str(r.Transaction))
            if m: rows.append(dict(season=y, week=int(r.Week), team=str(r.Team).strip(),
                                   player=m.group(1).strip(), k=key(m.group(1))))
    A = pd.DataFrame(rows); A['manager'] = A.team.map(t2m)
    print(f'executed ADD rows: {len(A)}   unmapped teams: {A.manager.isna().sum()}')

    pos = W.groupby(['season','k']).pos.agg(lambda s: s.mode().iat[0]).reset_index()
    A = A.merge(pos, on=['season','k'], how='left')
    A = A[A.pos.notna()]                       # K and D/ST have no rows in the stat file
    print(f'resolved to a skill player: {len(A)}')

    rec = []
    for _, r in A.iterrows():
        g = grp.get((r.season, r.k))
        if g is None: continue
        rest = g[(g.week >= r.week) & (g.week <= 14)]
        rec.append(dict(**r.to_dict(), n_wk=len(rest),
                        ppg=rest.pts.mean() if len(rest) else np.nan,
                        best=rest.pts.max() if len(rest) else np.nan))
    R = pd.DataFrame(rec); R = R[R.n_wk > 0].copy()
    R['hit'] = R.ppg >= R.pos.map(BAR)
    R.to_csv(os.path.join(HERE, 'waiver_study.csv'), index=False)

    print('\nHIT RATE  (rest-of-season ppg from the add week thru wk14 >= replacement ppg)')
    print(f'{"pos":<4}{"league n":>9}{"league":>9}{"Matt n":>8}{"Matt":>8}')
    for p in ('QB','RB','WR','TE'):
        a = R[R.pos == p]; m = a[a.manager == MATT]
        print(f'{p:<4}{len(a):>9}{a.hit.mean():>9.3f}{len(m):>8}{m.hit.mean():>8.3f}')

    rb = R[R.pos == 'RB']; mine = rb[rb.manager == MATT]; oth = rb[rb.manager != MATT]
    print(f'\nRB  Matt {mine.hit.mean():.3f} (n={len(mine)})  vs others {oth.hit.mean():.3f} (n={len(oth)})')
    try:
        from scipy.stats import fisher_exact, mannwhitneyu
        tab = [[int(mine.hit.sum()), int((~mine.hit).sum())],
               [int(oth.hit.sum()),  int((~oth.hit).sum())]]
        print(f'    Fisher p={fisher_exact(tab)[1]:.3f}   ppg MWU p={mannwhitneyu(mine.ppg, oth.ppg).pvalue:.3f}')
    except ImportError:
        print('    (scipy not installed -- p-values skipped)')

    # is he earlier than the field on players more than one manager wanted?
    c = R.join(R.groupby(['season','k']).agg(teams=('manager','nunique'),
                                             medwk=('week','median'),
                                             firstwk=('week','min')), on=['season','k'])
    c = c[c.teams >= 2]
    for label, d in (('all pos', c), ('RB only', c[c.pos == 'RB'])):
        m = d[d.manager == MATT]; o = d[d.manager != MATT]
        print(f'{label:<8} Matt {(m.week-m.medwk).mean():+.2f} wk vs field median, first '
              f'{100*(m.week==m.firstwk).mean():.0f}%   |   others {(o.week-o.medwk).mean():+.2f} wk, '
              f'first {100*(o.week==o.firstwk).mean():.0f}%')

    # how many weeks a season is the slot actually empty?
    dh = pd.read_csv(os.path.join(SRC, 'draft_history_2021_2025.csv'))
    dh = dh[dh.Year.between(2022, 2025)].copy(); dh['k'] = dh.Player.map(key)
    played = {kk: set(g[g.week <= 14].week.astype(int)) for kk, g in W.groupby(['season','k'])}
    print('\nMISSING-STARTER WEEKS PER SEASON (weeks 1-14, from the draft board)')
    for p, topn, lab in (('QB',1,'drafted starting QB'), ('RB',2,'top-2 drafted RBs'),
                         ('RB',3,'top-3 drafted RBs')):
        v = []
        for (yr, mgr), g in dh[dh.Pos == p].groupby(['Year','Manager']):
            g = g.sort_values(['Rd','Pick']).head(topn)
            if len(g) < topn: continue
            v.append(sum(topn - sum(1 for _, r in g.iterrows()
                                    if wk in played.get((r.Year, r.k), set()))
                         for wk in range(1, 15)))
        v = np.array(v)
        print(f'  {lab:<22} n={len(v):3d}  mean {v.mean():.2f}  median {np.median(v):.0f}  p75 {np.percentile(v,75):.0f}')

if __name__ == '__main__':
    main()
