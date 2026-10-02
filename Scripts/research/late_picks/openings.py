#!/usr/bin/env python3
r"""
openings.py -- doc 293, batch R1 part 2 (A): the man ahead is gone for a game. Who rises, and does pedigree change
which signals matter?

POPULATION: every team-season 2015-2025 where the position's snap leader to date (RB, TE: the leader; WR: any of
the top three) misses a regular-season game in weeks 3-15 while his team plays; the FIRST such game for each
candidate-season. CANDIDATE: the next man by snaps before that game (RB and TE: number two; WR: number four),
not established last season. OUTCOME: four straight games at or above the bar starting that game or the next.
SIGNALS, all knowable before the game: snap share before and in the last two games; the backup's share of the
non-leader snaps (RB and TE, the clear path); his EPA per play and yards per play over this season and last
(carries for backs, targets for receivers and tight ends; 15 plays minimum or missing); the leader's EPA per play
this season; the gap between them; a relief game already on his record (at the snap line AND the bar, this season or
last); special-teams share; years in the league. PEDIGREE: rounds 1-3 (high) against rounds 4-7 and undrafted (low).
TESTS: within each group, rate above against below the pooled median; logistic within each group; and the
interaction (signal x low pedigree) on the pooled rows: Matt's claim is that the signals read more clearly once
pedigree is out of the way.
"""
import sys
import os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))   # outputs and common.py live beside this file
import pandas as pd
from scipy.stats import fisher_exact
sys.path.insert(0, HERE)
from common import BAR, LINE, load, established, window_starts, logistic

w = load()
est = established(w)
ws = window_starts(w)
team_weeks = w.groupby(['season', 'team']).week.apply(lambda s: sorted(set(s))).to_dict()
by_tw = {k: g for k, g in w.groupby(['season', 'team', 'position'])}
played = set(zip(w.season, w.week, w.team, w.key))

def eff(rows):
    n = rows.plays.sum()
    if n < 15:
        return np.nan, np.nan, n
    return rows.epa.sum() / n, rows.yds.sum() / n, n

events, seen = [], set()
for (season, team, pos), g in by_tw.items():
    if season < 2015:
        continue
    weeks = team_weeks[(season, team)]
    for s in weeks:
        if not (3 <= s <= 15):
            continue
        prior = g[g.week < s]
        if prior.week.nunique() < 2:
            continue
        snapsum = prior.groupby('key').offense_snaps.sum().sort_values(ascending=False)
        top = 1 if pos in ('RB', 'TE') else 3
        leaders = list(snapsum.index[:top])
        absent = [k for k in leaders if (season, s, team, k) not in played
                  and prior[prior.key == k].week.nunique() >= 2]
        if not absent:
            continue
        # first game of the absence only
        prevs = [x for x in weeks if x < s]
        if prevs and all((season, prevs[-1], team, k) not in played for k in absent):
            continue
        rest = snapsum.drop(leaders, errors='ignore')
        if rest.empty:
            continue
        cand = rest.index[0]
        if (cand, season) in est or (cand, season) in seen:
            continue
        seen.add((cand, season))
        me = prior[prior.key == cand].sort_values('week')
        last = w[(w.key == cand) & (w.season == season - 1)]
        lead = prior[prior.key == absent[0]]
        e_me, y_me, n_me = eff(pd.concat([me, last]))
        e_ld, y_ld, n_ld = eff(lead)
        relief = bool(((pd.concat([me, last]).offense_pct >= LINE[pos]) & (pd.concat([me, last]).half >= BAR[pos])).any())
        conc = snapsum.get(cand, 0) / rest.sum() if pos in ('RB', 'TE') else np.nan
        nxt = [x for x in weeks if x >= s][:2]
        starts, pweeks = ws.get((cand, season), (set(), []))
        hit = any(x in starts for x in nxt)
        info = me.iloc[-1] if len(me) else None
        events.append(dict(season=season, team=team, pos=pos, week=s, key=cand, player=info.player if info is not None else '',
                           tier=info.tier if info is not None else 'undrafted', low=bool(info.low) if info is not None else True,
                           years_exp=info.years_exp if info is not None else np.nan,
                           share_pre=me.offense_pct.mean(), share_last2=me.offense_pct.tail(2).mean(),
                           st_share=me.st_pct.mean(), conc=conc, epa=e_me, ypp=y_me, plays=n_me,
                           epa_lead=e_ld, gap=(e_me - e_ld) if pd.notna(e_me) and pd.notna(e_ld) else np.nan,
                           relief=relief, hit=hit))

ev = pd.DataFrame(events)
ev.to_pickle(os.path.join(HERE, 'openings.pkl'))
print(f'OPENINGS {len(ev)} (first game of an absence, one per candidate-season) | risers {int(ev.hit.sum())} '
      f'({ev.hit.mean():.1%}) | low pedigree {int(ev.low.sum())} ({ev[ev.low].hit.mean():.1%}) | high {int((~ev.low).sum())} ({ev[~ev.low].hit.mean():.1%})')
print(ev.groupby(['pos', 'low']).hit.agg(['size', 'mean']).round(3).to_string())

signals = [('share_pre', 'snap share before'), ('share_last2', 'snap share, last two games'), ('conc', 'share of the backup snaps (RB/TE)'),
           ('epa', 'EPA per play, this season + last'), ('ypp', 'yards per play'), ('gap', 'EPA gap over the leader'),
           ('epa_lead', "the leader's EPA per play"), ('st_share', 'special-teams share'), ('years_exp', 'years in the league')]
# Every signal is put on ONE scale inside its position before any split or model: a back's EPA per carry and a
# receiver's EPA per target live on different scales, and a pooled median sorts positions, not players (the first
# run of this script did exactly that and reported efficiency backwards).
for col, _ in [('share_pre', ''), ('share_last2', ''), ('conc', ''), ('epa', ''), ('ypp', ''), ('gap', ''), ('epa_lead', ''),
               ('st_share', ''), ('years_exp', '')]:
    ev[col + '_z'] = ev.groupby('pos')[col].transform(lambda v: (v - v.mean()) / (v.std() if v.std() else 1))
print('\nABOVE vs AT-OR-BELOW the median INSIDE EACH POSITION, within each group (rate above / rate below, n, Fisher p)')
for col, lab in signals:
    d = ev.dropna(subset=[col]).copy()
    d['above'] = d[col] > d.groupby('pos')[col].transform('median')
    med = d[col].median()
    parts = []
    for grp, name in ((d[d.low], 'low'), (d[~d.low], 'high')):
        a, b = grp[grp.above].hit, grp[~grp.above].hit
        if len(a) >= 5 and len(b) >= 5:
            p = fisher_exact([[a.sum(), len(a) - a.sum()], [b.sum(), len(b) - b.sum()]])[1]
            parts.append(f'{name}: {a.mean():.3f} / {b.mean():.3f} (n {len(a)}/{len(b)}, p={p:.3f})')
    print(f'  {lab:<34} | ' + ' | '.join(parts))
for grp, name in ((ev[ev.low], 'low'), (ev[~ev.low], 'high')):
    a, b = grp[grp.relief].hit, grp[~grp.relief].hit
    p = fisher_exact([[a.sum(), len(a) - a.sum()], [b.sum(), len(b) - b.sum()]])[1] if len(a) and len(b) else np.nan
    print(f'  relief game already on record, {name}: {a.mean():.3f} (n {len(a)}) vs {b.mean():.3f} (n {len(b)}), p={p:.3f}')

print('\nINTERACTION (pooled logistic: signal z-scored, low, signal x low, position dummies)')
for col, lab in signals + [('relief', 'relief game on record')]:
    d = ev.dropna(subset=[col]).copy()
    x = d[col].astype(float) if col == 'relief' else d[col + '_z'].astype(float)
    X = pd.DataFrame({'const': 1.0, 'x': x, 'low': d.low.astype(float), 'x_low': x * d.low.astype(float),
                      'RB': (d.pos == 'RB').astype(float), 'TE': (d.pos == 'TE').astype(float)})
    if d.pos.nunique() == 1:
        X = X.drop(columns=['RB', 'TE'])
    b, se = logistic(X.values, d.hit.values)
    names = list(X.columns)
    ix, il = names.index('x'), names.index('x_low')
    print(f'  {lab:<34} n={len(d):<4} signal in high {b[ix]:+.2f} (z {b[ix]/se[ix]:+.2f}) | extra in low {b[il]:+.2f} (z {b[il]/se[il]:+.2f}) '
          f'| signal in low {b[ix]+b[il]:+.2f}')
