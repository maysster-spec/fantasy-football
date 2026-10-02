"""Doc 267's pairs.py question, asked of QUARTERBACKS in the playoff weeks.
CLAIM (Matt's, stated before the run): hold two QBs so that in weeks 15-17 you always have a good
matchup, the way two defences marry two schedules.
TESTABLE FORM: over weeks 15-17, does starting whichever of {QB1, a streamable QB2} faces the softer
defence beat simply always starting QB1?
EX ANTE: opponent generosity is computed from weeks 1-14 ONLY, so the rule uses nothing from the
weeks it is scored on. Tiers likewise fixed on weeks 1-14.
Population: nflverse REG 2021-2025, QB starts, scored under this league's rules.
"""
import pandas as pd, numpy as np, itertools

def score(d):
    g = lambda c: pd.to_numeric(d.get(c, 0), errors='coerce').fillna(0)
    return (g('passing_yards')*0.04 + g('passing_tds')*6 - g('passing_interceptions')*2
            + g('rushing_yards')*0.1 + g('rushing_tds')*6
            - (g('sack_fumbles_lost')+g('rushing_fumbles_lost')+g('receiving_fumbles_lost'))*2
            + (g('passing_2pt_conversions')+g('rushing_2pt_conversions')+g('receiving_2pt_conversions'))*2)

rows=[]
for yr in range(2021, 2026):
    d = pd.read_csv(f'/mnt/user-data/uploads/2026/Scripts/research/_nflverse_cache/stats_player_week_{yr}.csv',
                    low_memory=False)
    d = d[(d['position']=='QB') & (d['season_type']=='REG') & (d['week'].between(1,17))].copy()
    d['pts']=score(d); d['season']=yr
    rows.append(d[['season','week','player_display_name','team','opponent_team','pts']])
q = pd.concat(rows, ignore_index=True)
q = q.sort_values('pts',ascending=False).groupby(['season','week','team'],as_index=False).first()

A_always, B_matchup, n_pairs, swaps, swap_gain = [], [], 0, 0, []
for yr, s in q.groupby('season'):
    reg, po = s[s['week']<=14], s[s['week'].between(15,17)]
    tot = reg.groupby('player_display_name').agg(g=('pts','size'), ppg=('pts','mean'))
    tot = tot[tot['g']>=8].sort_values('ppg',ascending=False)
    elite = list(tot.index[:6]); stream = list(tot.index[12:24])
    gen = reg.groupby('opponent_team')['pts'].mean()          # weeks 1-14 only
    gen = gen - gen.mean()
    po = po[po['opponent_team'].isin(gen.index)].copy()
    po['gen'] = po['opponent_team'].map(gen)
    idx = {(r.player_display_name, r.week): r for r in po.itertuples()}
    wks = sorted(po['week'].unique())
    for e, t in itertools.product(elite, stream):
        a, b, sw, sg = [], [], 0, []
        for w in wks:
            re_, rt = idx.get((e,w)), idx.get((t,w))
            if re_ is None: continue                 # QB1 did not start: a different question
            a.append(re_.pts)
            if rt is not None and rt.gen > re_.gen:
                b.append(rt.pts); sw += 1; sg.append(rt.pts - re_.pts)
            else:
                b.append(re_.pts)
        if len(a) < 3: continue
        n_pairs += 1; swaps += sw; swap_gain += sg
        A_always.append(np.mean(a)); B_matchup.append(np.mean(b))

A, B = np.array(A_always), np.array(B_matchup)
d = B - A
se = d.std(ddof=1)/np.sqrt(len(d))
print(f'elite-QB1 x streamable-QB2 pairs, weeks 15-17, 2021-2025: n={n_pairs}')
print(f'  A  always start QB1            : {A.mean():.2f} a week')
print(f'  B  start the softer matchup    : {B.mean():.2f} a week')
print(f'  B minus A                      : {d.mean():+.2f}  se {se:.2f}  t {d.mean()/se:+.2f}')
print(f'  the rule benched QB1 in {swaps} of {int(sum(len(x) for x in [A])*0)+swaps+0} swap chances'
      f'  ({swaps/ (len(A)*3):.0%} of pair-weeks)')
sg = np.array(swap_gain)
if len(sg):
    print(f'  when it DID bench QB1: {sg.mean():+.2f} a week, se {sg.std(ddof=1)/np.sqrt(len(sg)):.2f},'
          f' won {100*(sg>0).mean():.0f}% of the time, n={len(sg)}')
