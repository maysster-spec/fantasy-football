#!/usr/bin/env python3
"""claim_rank.py -- how often a WAIVER claim lands by the claimant's waiver rank that week (doc 463).
THE CLAIM IN TESTABLE FORM: in this league, the share of claims on a CONTESTED man that land falls with the
claimant's waiver rank (inverse standings after the previous week: worst record first, then fewer points), and
the share on an UNCONTESTED man does not. Population: every WAIVER-type claim that reached a decision in
waiver_report_2022..2025 (EXECUTED or FAILED_*; CANCELED and PENDING excluded), weeks 2 to 14, matched to the
standings rebuilt from historical_scoreboard_2022_2025.csv. Week 1 excluded (no standings). stdlib + pandas.
"""
import os, re, sys, glob
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get('FF_SRC') or os.path.normpath(os.path.join(HERE, '..', '..', 'Source'))   # Scripts\research\ -> Source\

def standings_before(sb, season, week):
    g = sb[(sb.Season == season) & (sb.Week < week) & (sb['Bracket Type'] == 'NONE')]
    rec = {}
    for _, r in g.iterrows():
        for side, other in (('Home', 'Away'), ('Away', 'Home')):
            t = r[f'{side} Team']; s = r[f'{side} Score']; o = r[f'{other} Score']
            w, l, pf = rec.get(t, (0, 0, 0.0))
            rec[t] = (w + (1 if s > o else 0), l + (1 if s < o else 0), pf + s)
    # waiver order: inverse standings -> worst first (fewest wins, then fewest points)
    order = sorted(rec, key=lambda t: (rec[t][0], rec[t][2]))
    return {t: i + 1 for i, t in enumerate(order)}

def main():
    sb = pd.read_csv(os.path.join(SRC, 'historical_scoreboard_2022_2025.csv'))
    rows = []
    for f in sorted(glob.glob(os.path.join(SRC, 'waiver_report_20*.csv'))):
        season = int(re.search(r'(\d{4})', os.path.basename(f)).group(1))
        if season not in set(sb.Season): continue
        w = pd.read_csv(f)
        w = w[(w.Type == 'WAIVER') & (w.Status.str.startswith(('EXECUTED', 'FAILED'))) & (w.Week >= 2) & (w.Week <= 14)].copy()
        w['pid'] = w.Transaction.str.extract(r'ADD Player ID (-?\d+)')[0]
        w = w[w.pid.notna()]
        for wk, g in w.groupby('Week'):
            ranks = standings_before(sb, season, wk)
            n = len(ranks)
            for _, r in g.iterrows():
                rk = ranks.get(r.Team)
                if rk is None: continue
                rows.append(dict(season=season, week=wk, team=r.Team, pid=r.pid, rank=rk, n=n,
                                 won=r.Status == 'EXECUTED', status=r.Status))
    d = pd.DataFrame(rows)
    d['claimants'] = d.groupby(['season', 'week', 'pid']).team.transform('nunique')
    d['contested'] = d.claimants >= 2
    d['band'] = pd.cut(d['rank'], [0, 4, 8, 12], labels=['ranks 1-4', 'ranks 5-8', 'ranks 9-12'])
    print(f'claims matched to a rank: {len(d)} of which contested {d.contested.sum()} ({d.contested.mean():.1%}); unmatched team names: see below')
    print('\nshare of claims that LANDED, by the claimant\'s waiver rank that week:')
    print(f'  {"":<12}{"contested n":>12}{"landed":>8}{"uncontested n":>15}{"landed":>8}')
    for b, c in d.groupby('band', observed=True):
        ct, un = c[c.contested], c[~c.contested]
        print(f'  {b:<12}{len(ct):>12}{ct.won.mean():>8.1%}{len(un):>15}{un.won.mean():>8.1%}')
    print('\n  by exact rank, contested only:')
    for rk, c in d[d.contested].groupby('rank'):
        print(f'   rank {rk:>2}: n={len(c):>3} landed {c.won.mean():.0%}')
    # the one-line rule: a contested claim at rank r lands when nobody above you files; measured directly
    print('\n  the uncontested-claim failure reasons (these are the no-drop and limit failures, not priority):')
    print(d[~d.contested & ~d.won].status.value_counts().head(5).to_string())
    # names that never matched the scoreboard
    allw = pd.concat([pd.read_csv(f) for f in glob.glob(os.path.join(SRC, 'waiver_report_20*.csv'))])
    miss = sorted(set(allw.Team) - set(sb['Home Team']) - set(sb['Away Team']))
    print('\n  team names in the waiver reports with no scoreboard row (their claims are left out):', miss)
    if '--check' in sys.argv:
        # [doc 463] the bands in sheet_constants.json claims.by_rank_band must equal this run
        import json
        held = ((json.load(open(os.path.join(SRC, 'sheet_constants.json'), encoding='utf-8')).get('claims') or {})
                .get('by_rank_band') or {}).get('bands') or []
        drift = []
        for b in held:
            c = d[d.contested & (d['rank'] >= b['lo']) & (d['rank'] <= b['hi'])]
            if len(c) != b['n'] or abs(c.won.mean() - b['land']) > 0.0051:
                drift.append(f"ranks {b['lo']}-{b['hi']}: file n={b['n']} land={b['land']} computed n={len(c)} land={c.won.mean():.3f}")
        if not held:
            drift.append('no by_rank_band block in sheet_constants.json')
        if drift:
            print('\nCHECK FAILED: claims.by_rank_band drifts from this run:\n  ' + '\n  '.join(drift))
            return 1
        print(f'\ncheck: every by_rank_band cell in sheet_constants.json matches this run ({len(held)} bands)')
    return 0

if __name__ == '__main__':
    sys.exit(main())
