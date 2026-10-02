"""Does matchup move a STREAMABLE quarterback more than an ELITE one?
Population: QB player-weeks, nflverse REG, weeks 1-14, 2021-2025, scored under THIS league's rules
(0.04/pass yd, 6-pt pass TD, -2 INT, 0.1/rush yd, 6 rush TD, -2 fumble lost, 2-pt = 2).
Matchup: the opponent's QB points allowed per game that season, LEAVE-ONE-OUT (the focal QB's own
games against that opponent are removed), centred within season so 0 = an average defence.
Tier: within each season, QBs with 8+ games ranked by points per game. elite 1-6, streamable 13-24.
"""
import pandas as pd, numpy as np

def score(d):
    g = lambda c: pd.to_numeric(d.get(c, 0), errors='coerce').fillna(0)
    return (g('passing_yards')*0.04 + g('passing_tds')*6 - g('passing_interceptions')*2
            + g('rushing_yards')*0.1 + g('rushing_tds')*6
            - (g('sack_fumbles_lost') + g('rushing_fumbles_lost') + g('receiving_fumbles_lost'))*2
            + (g('passing_2pt_conversions') + g('rushing_2pt_conversions')
               + g('receiving_2pt_conversions'))*2)

rows = []
for yr in range(2021, 2026):
    d = pd.read_csv(f'/mnt/user-data/uploads/2026/Scripts/research/_nflverse_cache/stats_player_week_{yr}.csv',
                    low_memory=False)
    d = d[(d['position'] == 'QB') & (d['season_type'] == 'REG') & (d['week'].between(1, 14))].copy()
    d['pts'] = score(d); d['season'] = yr
    rows.append(d[['season','week','player_display_name','team','opponent_team','pts']])
q = pd.concat(rows, ignore_index=True)
# a QB-week only counts as a start: 10+ points of volume OR he is his team's top scorer that week
q = q.sort_values('pts', ascending=False).groupby(['season','week','team'], as_index=False).first()
print(f'QB starts, 2021-2025 REG wk1-14: n={len(q)}')

out = []
for yr, s in q.groupby('season'):
    tot = s.groupby('player_display_name').agg(g=('pts','size'), ppg=('pts','mean'))
    tot = tot[tot['g'] >= 8].sort_values('ppg', ascending=False)
    tier = {}
    for i, nm in enumerate(tot.index, 1):
        tier[nm] = 'elite' if i <= 6 else ('streamable' if 13 <= i <= 24 else None)
    s = s.copy(); s['tier'] = s['player_display_name'].map(tier)
    # leave-one-out opponent generosity
    opp_sum = s.groupby('opponent_team')['pts'].transform('sum')
    opp_n   = s.groupby('opponent_team')['pts'].transform('size')
    pair_sum = s.groupby(['opponent_team','player_display_name'])['pts'].transform('sum')
    pair_n   = s.groupby(['opponent_team','player_display_name'])['pts'].transform('size')
    s['gen'] = (opp_sum - pair_sum) / (opp_n - pair_n)
    s['gen'] = s['gen'] - s['gen'].mean()
    out.append(s)
a = pd.concat(out, ignore_index=True).dropna(subset=['tier','gen'])

print(f"\n{'tier':<12}{'n':>6}{'ppg':>8}{'sd':>7}{'slope':>9}{'se':>7}{'t':>7}{'r2':>7}")
res={}
for t in ('elite','streamable'):
    s = a[a['tier'] == t]
    x, y = s['gen'].values, s['pts'].values
    b, b0 = np.polyfit(x, y, 1)
    yh = b*x + b0; resid = y - yh
    se = np.sqrt((resid**2).sum()/(len(x)-2) / ((x-x.mean())**2).sum())
    r2 = 1 - (resid**2).sum()/((y-y.mean())**2).sum()
    res[t]=(b,se)
    print(f'{t:<12}{len(s):>6}{y.mean():>8.2f}{y.std():>7.2f}{b:>9.3f}{se:>7.3f}{b/se:>7.2f}{r2:>7.3f}')
d_b = res['streamable'][0]-res['elite'][0]
d_se = np.hypot(res['streamable'][1], res['elite'][1])
print(f"\ndifference in slope (streamable minus elite): {d_b:+.3f}  se {d_se:.3f}  t {d_b/d_se:+.2f}")
print("his direction is a POSITIVE difference: matchup moves the streamer more.")

# decision version: within a week, how much is picking the best-matchup streamer worth?
print('\nDECISION VERSION -- among streamable QBs in a given season-week:')
g = a[a['tier']=='streamable'].groupby(['season','week'])
best, avg, n = [], [], 0
for _, s in g:
    if len(s) < 3: continue
    n += 1
    best.append(s.loc[s['gen'].idxmax(), 'pts']); avg.append(s['pts'].mean())
best, avg = np.array(best), np.array(avg)
dif = best-avg
print(f'  season-weeks with 3+ streamable starters: {n}')
print(f'  take the softest matchup: {best.mean():.2f}/wk   take one at random: {avg.mean():.2f}/wk')
print(f'  gain {dif.mean():+.2f} a week, se {dif.std(ddof=1)/np.sqrt(len(dif)):.2f}, t {dif.mean()/(dif.std(ddof=1)/np.sqrt(len(dif))):+.2f}')
