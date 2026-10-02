#!/usr/bin/env python3
r"""
flips.py -- doc 293, batch R1 part 2 (B): nobody is hurt. A backup is in the rotation. Who takes the role, and do
performance signals read more clearly for late picks? (The Hubbard 2023 shape: Sanders at 3.1 yards a carry, Hubbard
better on fewer carries, snaps creeping 34% -> 54% before the week-6 cameo.)

POPULATION: RB/WR/TE player-seasons 2015-2025, not established last season. The FIRST week s (weeks 4-14) where his
snap share over his last two games sat in the rotation band (RB 20-49%, TE 25-59%, WR 30-64%) while he was not the
position leader by snaps (WR: not top three), and every leader played the game before s. One row per player-season.
OUTCOME: four straight games at or above the bar starting within his team's next four games. CLEAN FLIP: rows where a
leader missed a game in that window are dropped (that is an absence, part A), and the count dropped is printed.
SIGNALS (before s): snap share, last two games and season; the trend (last two minus earlier); EPA and yards per play
over this season and last (15 plays minimum); the leader's EPA per play this season (a failing incumbent); the gap;
points per snap this season; years in the league; special-teams share. Each on a within-position scale.
TESTS: median split inside each position, within low and high pedigree; pooled logistic with signal x low.
"""
import sys
import os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))   # outputs and common.py live beside this file
import pandas as pd
from scipy.stats import fisher_exact
sys.path.insert(0, HERE)
from common import BAR, LINE, load, established, window_starts, logistic

BAND = {'RB': (0.20, 0.50), 'TE': (0.25, 0.60), 'WR': (0.30, 0.65)}
w = load()
est = established(w)
ws = window_starts(w)
team_weeks = w.groupby(['season', 'team']).week.apply(lambda s: sorted(set(s))).to_dict()
played = set(zip(w.season, w.week, w.team, w.key))
room = {k: g for k, g in w.groupby(['season', 'team', 'position'])}

def eff(rows):
    n = rows.plays.sum()
    return (rows.epa.sum() / n, rows.yds.sum() / n) if n >= 15 else (np.nan, np.nan)

rows, dropped = [], 0
for (key, season), g in w[w.season >= 2015].sort_values('week').groupby(['key', 'season']):
    if (key, season) in est:
        continue
    g = g.reset_index(drop=True)
    for i in range(2, len(g)):
        s = int(g.week[i])
        if not (4 <= s <= 14):
            continue
        pos, team = g.position[i], g.team[i]
        last2 = g.iloc[i - 2:i]
        if (last2.team != team).any():
            continue
        lo, hi = BAND[pos]
        sh2 = last2.offense_pct.mean()
        if not (lo <= sh2 < hi):
            continue
        prior = room[(season, team, pos)]
        prior = prior[prior.week < s]
        snapsum = prior.groupby('key').offense_snaps.sum().sort_values(ascending=False)
        top = 1 if pos in ('RB', 'TE') else 3
        leaders = [k for k in snapsum.index if k != key][:top]
        if key in snapsum.index and int((snapsum > snapsum[key]).sum()) < top:
            continue                                            # he is already the leader / top three
        weeks = team_weeks[(season, team)]
        prev = [x for x in weeks if x < s][-1]
        if any((season, prev, team, k) not in played for k in leaders):
            continue                                            # a leader was out: that is part A
        nxt = [x for x in weeks if x >= s][:4]
        absence = any((season, x, team, k) not in played for x in nxt for k in leaders)
        dropped += int(absence)
        # TOOK THE ROLE (second outcome, added for the Hubbard 2023 shape): in at least two of the next four team games
        # in which every leader played, his snap share beat the lowest leader's share.
        shares = w[(w.season == season) & (w.team == team) & (w.position == pos) & w.week.isin(nxt)]
        took_games = 0
        for x in nxt:
            if all((season, x, team, k) in played for k in leaders):
                sx = shares[shares.week == x].set_index('key').offense_pct
                if sx.get(key, 0) > min(sx.get(k, 0) for k in leaders):
                    took_games += 1
        me = g.iloc[:i]
        lastyr = w[(w.key == key) & (w.season == season - 1)]
        e_me, y_me = eff(pd.concat([me, lastyr]))
        e_ld, _ = eff(prior[prior.key == leaders[0]]) if leaders else (np.nan, np.nan)
        early = me.iloc[:-2]
        starts, _ = ws.get((key, season), (set(), []))
        rows.append(dict(season=season, week=s, team=team, pos=pos, key=key, player=g.player[i], tier=g.tier[i], low=bool(g.low[i]),
                         years_exp=g.years_exp[i], share_last2=sh2, share_pre=me.offense_pct.mean(),
                         trend=sh2 - early.offense_pct.mean() if len(early) else np.nan, epa=e_me, ypp=y_me, epa_lead=e_ld,
                         gap=e_me - e_ld if pd.notna(e_me) and pd.notna(e_ld) else np.nan,
                         pps=me.half.sum() / max(me.offense_snaps.sum(), 1), st_share=me.st_pct.mean(),
                         hit=any(x in starts for x in nxt), absence=absence, took=took_games >= 2))
        break

allrows = pd.DataFrame(rows)
allrows.to_pickle(os.path.join(HERE, 'flips_all.pkl'))
print(f'ALL ROTATION BACKUPS {len(allrows)}: took the role {allrows.took.mean():.1%} (low {allrows[allrows.low].took.mean():.1%}, '
      f'high {allrows[~allrows.low].took.mean():.1%}); rose {allrows.hit.mean():.1%} (low {allrows[allrows.low].hit.mean():.1%}, high {allrows[~allrows.low].hit.mean():.1%})')
ev = allrows[~allrows.absence].reset_index(drop=True)
ev.to_pickle(os.path.join(HERE, 'flips.pkl'))
print(f'ROTATION BACKUPS {len(ev)} (clean: no leader absence in the next four games; {dropped} dropped for one) | rose {int(ev.hit.sum())} '
      f'({ev.hit.mean():.1%}) | low {int(ev.low.sum())} ({ev[ev.low].hit.mean():.1%}) | high {int((~ev.low).sum())} ({ev[~ev.low].hit.mean():.1%})')
print(ev.groupby(['pos', 'low']).hit.agg(['size', 'mean']).round(3).to_string())
signals = [('share_last2', 'snap share, last two games'), ('share_pre', 'snap share, season'), ('trend', 'snap trend (last two - earlier)'),
           ('epa', 'EPA per play, this season + last'), ('ypp', 'yards per play'), ('epa_lead', "the leader's EPA per play"),
           ('gap', 'EPA gap over the leader'), ('pps', 'points per snap'), ('years_exp', 'years in the league'), ('st_share', 'special-teams share')]
for col, _ in signals:
    ev[col + '_z'] = ev.groupby('pos')[col].transform(lambda v: (v - v.mean()) / (v.std() if v.std() else 1))
for OUT in ('hit', 'took'):
  ev['y'] = ev[OUT]
  print(f'\n===== OUTCOME: {"rose (four games at the bar)" if OUT == "hit" else "took the role (out-snapped the leader in 2 of the next 4)"} | '
        f'low {ev[ev.low].y.mean():.1%} (n {int(ev.low.sum())}), high {ev[~ev.low].y.mean():.1%} (n {int((~ev.low).sum())})')
  print('ABOVE vs AT-OR-BELOW the median inside each position (rate above / below, n, Fisher p)')
  for col, lab in signals:
      d = ev.dropna(subset=[col]).copy()
      d['above'] = d[col] > d.groupby('pos')[col].transform('median')
      parts = []
      for grp, name in ((d[d.low], 'low'), (d[~d.low], 'high')):
          a, b = grp[grp.above].y, grp[~grp.above].y
          if len(a) >= 5 and len(b) >= 5:
              p = fisher_exact([[a.sum(), len(a) - a.sum()], [b.sum(), len(b) - b.sum()]])[1]
              parts.append(f'{name}: {a.mean():.3f} / {b.mean():.3f} (n {len(a)}/{len(b)}, p={p:.3f})')
      print(f'  {lab:<32} | ' + ' | '.join(parts))
  print('\nINTERACTION (pooled logistic: within-position z signal, low, signal x low, position dummies)')
  for col, lab in signals:
      d = ev.dropna(subset=[col]).copy()
      x = d[col + '_z'].astype(float)
      X = pd.DataFrame({'const': 1.0, 'x': x, 'low': d.low.astype(float), 'x_low': x * d.low.astype(float),
                        'RB': (d.pos == 'RB').astype(float), 'TE': (d.pos == 'TE').astype(float)})
      b, se = logistic(X.values, d.y.values)
      print(f'  {lab:<32} n={len(d):<5} signal in high {b[1]:+.2f} (z {b[1]/se[1]:+.2f}) | extra in low {b[3]:+.2f} (z {b[3]/se[3]:+.2f}) | signal in low {b[1]+b[3]:+.2f}')
