#!/usr/bin/env python3
r"""
risers.py -- doc 293, batch R1 part 1: every mid-season riser 2015-2025 and HOW HIS ROLE OPENED.

POPULATION: RB/WR/TE player-seasons, not established last season (6+ games averaging at or above the bar), from
r1/weekly.pkl (snap-based games). RISER: the first four straight games played that average at or above the bar
(half-PPR a game: RB 9.92, WR 9.62, TE 8.25), starting in week 2 or later, after averaging under the bar in any
earlier games that season.
HOW IT OPENED, at the stretch's first game s, on his team, at his position (RB and TE: the man with the most
snaps before s; WR: the top three by snaps before s):
  already led     he already had the most snaps (WR: already top three); the points caught up to the role
  absent: injury  the man ahead missed game s or the game before it, and was on the injury report (Out or
                  Doubtful) or on reserve (RES, PUP)
  absent: gone    the man ahead was cut, traded or on another roster
  absent: benched the man ahead was on the roster, not injured, and did not play (inactive, practice squad)
  absent: other   missed with no recorded reason
  absent: injured in game   he played game s at under 60% of his usual share and missed the next game
  absent during the stretch the man ahead played game s but missed one of the next three
  overtook        the man ahead played game s and took fewer snaps than the riser did
  grew beside     the man ahead played and still out-snapped him; the riser scored his way to the bar
Prints the mix by pedigree (rounds 1-3 against rounds 4-7 and undrafted) and position. Writes r1/risers.pkl.
"""
import os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))   # outputs and common.py live beside this file
import pandas as pd

BAR = {'RB': 9.92, 'WR': 9.62, 'TE': 8.25}
w = pd.read_pickle(os.path.join(HERE, 'weekly.pkl'))
w['key'] = np.where(w.gsis_id.notna(), w.gsis_id, 'pfr:' + w.pfr_player_id)
w['bar'] = w.position.map(BAR)

ros = pd.concat([pd.read_csv(f'roster_weekly_{y}.csv', low_memory=False, usecols=['season', 'week', 'team', 'gsis_id', 'status'])
                 for y in range(2015, 2026)], ignore_index=True).dropna(subset=['gsis_id'])
ros = ros.drop_duplicates(['season', 'week', 'gsis_id'], keep='last').set_index(['season', 'week', 'gsis_id'])
inj = pd.concat([pd.read_csv(f'injuries_{y}.csv', low_memory=False, usecols=['season', 'week', 'gsis_id', 'report_status', 'game_type'])
                 for y in range(2015, 2026)], ignore_index=True)
inj = inj[inj.game_type == 'REG'].dropna(subset=['gsis_id']).drop_duplicates(['season', 'week', 'gsis_id'], keep='last')
inj = inj.set_index(['season', 'week', 'gsis_id']).report_status

team_weeks = w.groupby(['season', 'team']).week.apply(lambda s: sorted(set(s))).to_dict()
played = set(zip(w.season, w.week, w.team, w.key))

# established last season
ps = w.groupby(['key', 'season']).agg(g=('week', 'nunique'), ppg=('half', 'mean'), bar=('bar', 'last')).reset_index()
est = set(zip(ps.key[(ps.g >= 6) & (ps.ppg >= ps.bar)], ps.season[(ps.g >= 6) & (ps.ppg >= ps.bar)] + 1))

def why_absent(inc_key, season, week, team):
    if str(inc_key).startswith('pfr:'):
        return 'absent: other'
    r = ros.loc[(season, week, inc_key)] if (season, week, inc_key) in ros.index else None
    st = inj.get((season, week, inc_key))
    if r is None or r['team'] != team or r['status'] in ('CUT', 'TRD', 'TRC', 'TRT', 'NWT', 'RET'):
        return 'absent: gone'
    if st in ('Out', 'Doubtful') or r['status'] in ('RES', 'PUP', 'RSN'):
        return 'absent: injury'
    if r['status'] in ('INA', 'DEV'):
        return 'absent: benched'
    if r['status'] == 'SUS':
        return 'absent: other'
    return 'absent: other'

rows = []
w = w[w.season >= 2015]
for (key, season), g in w.sort_values('week').groupby(['key', 'season']):
    if (key, season) in est:
        continue
    g = g.reset_index(drop=True)
    half = g.half.values
    for i in range(len(g) - 3):
        s = int(g.week[i])
        if s < 2:
            continue
        pos, team = g.position[i], g.team[i]
        bar = BAR[pos]
        if half[i:i + 4].mean() < bar:
            continue
        if i > 0 and half[:i].mean() >= bar:
            break                                   # already scoring at the bar before: not a riser
        prior = w[(w.season == season) & (w.team == team) & (w.position == pos) & (w.week < s)]
        tw = [x for x in team_weeks[(season, team)] if x < s]
        prev = tw[-1] if tw else None
        snapsum = prior.groupby('key').offense_snaps.sum().sort_values(ascending=False)
        mine = snapsum.get(key, 0.0)
        others = snapsum.drop(key, errors='ignore')
        mech = None
        if others.empty or prev is None:
            mech = 'season start'
        else:
            top = 1 if pos in ('RB', 'TE') else 3
            rank = int((snapsum > mine).sum()) + 1 if key in snapsum.index else len(snapsum) + 1
            incs = list(others.index[:top])
            if key in snapsum.index and rank <= top:
                mech = 'already led'
            else:
                for inc in incs:
                    for wk in (s, prev):
                        if (season, wk, team, inc) not in played:
                            mech = why_absent(inc, season, wk, team)
                            break
                    if mech:
                        break
                if mech is None:
                    # IN-GAME INJURY (added after the first run labelled Mike Davis 2020 and Jerome Ford 2023, whose
                    # starters were hurt DURING game s, as 'grew beside' and 'overtook'): the man ahead played game s
                    # at under 60% of his usual share and missed his team's next game.
                    nxt = [x for x in team_weeks[(season, team)] if x > s]
                    sh = w[(w.season == season) & (w.week == s) & (w.team == team)].set_index('key').offense_pct
                    for inc in incs:
                        usual = prior[prior.key == inc].offense_pct.mean()
                        if nxt and sh.get(inc, 0) < 0.6 * usual and (season, nxt[0], team, inc) not in played:
                            mech = 'absent: injured in game'
                            break
                if mech is None:
                    # ...and the man ahead missing a LATER game of the four (the stretch was built while he was out)
                    stretch_weeks = [int(x) for x in g.week[i + 1:i + 4]]
                    if any((season, x, team, inc) not in played for x in stretch_weeks for inc in incs):
                        mech = 'absent during the stretch'
                if mech is None:
                    mech = 'overtook' if sh.get(key, 0) > min(sh.get(x, 0) for x in incs) else 'grew beside'
        pre = g.iloc[:i]
        rows.append(dict(key=key, season=season, week=s, team=team, pos=pos, player=g.player[i], tier=g.tier[i],
                         low=bool(g.low[i]), years_exp=g.years_exp[i], age=g.age[i], mech=mech,
                         pre_games=len(pre), pre_share=pre.offense_pct.mean() if len(pre) else np.nan,
                         pre_ppg=pre.half.mean() if len(pre) else np.nan, stretch_ppg=half[i:i + 4].mean()))
        break

r = pd.DataFrame(rows)
r.to_pickle(os.path.join(HERE, 'risers.pkl'))
print(f'RISERS 2015-2025: {len(r)} | low pedigree (rounds 4-7 + undrafted) {int(r.low.sum())} | high {int((~r.low).sum())}')
order = ['already led', 'absent: injury', 'absent: injured in game', 'absent: gone', 'absent: benched', 'absent: other', 'absent during the stretch', 'overtook', 'grew beside', 'season start']
t = pd.crosstab(r.mech, r.low.map({True: 'low', False: 'high'}), normalize='columns').reindex(order).round(3)
t['n low'] = pd.crosstab(r.mech, r.low).reindex(order)[True]
t['n high'] = pd.crosstab(r.mech, r.low).reindex(order)[False]
print(t.to_string())
for pos in ('RB', 'WR', 'TE'):
    s = r[r.pos == pos]
    tt = pd.crosstab(s.mech, s.low.map({True: 'low', False: 'high'})).reindex(order).fillna(0).astype(int)
    print(f'\n{pos} (n={len(s)})'); print(tt.T.to_string())
from scipy.stats import chi2_contingency
ct = pd.crosstab(r.mech, r.low)
print('\nchi-square, mechanism mix low vs high:', 'p=%.4f' % chi2_contingency(ct)[1])
print('\nmedian years in the league at the stretch: low', r[r.low].years_exp.median(), '| high', r[~r.low].years_exp.median())
print('low-pedigree risers by years of experience:', r[r.low].years_exp.value_counts().sort_index().to_dict())

top = r[r.low].sort_values('stretch_ppg', ascending=False)
print(f'\nLOW-PEDIGREE RISERS, top 30 by the four-game stretch (of {len(top)}):')
print(top.head(30)[['season', 'week', 'team', 'pos', 'player', 'tier', 'years_exp', 'mech', 'pre_share', 'stretch_ppg']].round(2).to_string(index=False))

# RELEVANT FROM WEEK 1: the preseason route this riser table cannot see (stretch starts are week 2 or later)
wk1 = []
for (key, season), g in w.sort_values('week').groupby(['key', 'season']):
    if (key, season) in est or len(g) < 4 or int(g.week.iloc[0]) != 1:
        continue
    if g.half.iloc[:4].mean() >= BAR[g.position.iloc[0]]:
        wk1.append(dict(season=season, player=g.player.iloc[0], team=g.team.iloc[0], pos=g.position.iloc[0], tier=g.tier.iloc[0],
                        low=bool(g.low.iloc[0]), share_w1=g.offense_pct.iloc[0], ppg4=g.half.iloc[:4].mean()))
d1 = pd.DataFrame(wk1)
print(f'\nRELEVANT FROM WEEK 1 (not established last season, first four games from week 1 at the bar): {len(d1)} | low {int(d1.low.sum())} | high {int((~d1.low).sum())}')
print(d1[d1.low].sort_values('ppg4', ascending=False).head(15)[['season', 'team', 'pos', 'player', 'tier', 'share_w1', 'ppg4']].round(2).to_string(index=False))
