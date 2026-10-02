#!/usr/bin/env python3
r"""
usage_jump_by_tier.py -- after a player's snap share jumps, how often does it turn into a startable
stretch, and does the rate still depend on NFL draft tier? (doc 292; Matt, 11 Sept: "even undrafted
free agent pick ups nfl teams get can begin to earn enough targets to be fantasy relevant... We don't
want rules that create blind spots".)

TESTABLE FORM, stated before running: among RB/WR/TE player-seasons 2022-2025 who were not
established starters last season, take the FIRST game in weeks 2-14 where his offensive snap share
reaches the starter line (RB 50%, WR 65%, TE 60%) after he averaged under 35% in the games he played
before it that season (or played none). OUTCOME A: his next four games played average at or above
replacement per game, half-PPR (RB 9.92, WR 9.62, TE 8.25); at least two games needed, and the rows
with fewer are counted, not silently dropped. OUTCOME B: the same bar on points over his team's next
four games, a missed game counting zero (what a claim actually delivers). SPLITS: NFL draft tier
(undrafted = no draft number on the weekly roster); a same-team same-position teammate who led the
position's snaps in the prior games sat out the jump game (a shock) or not; production in the jump
game itself at or above the bar.
Inputs: nflverse snap_counts 2022-2025, roster_weekly 2021-2025 (pfr_id -> gsis_id), player_stats
2021-2024 plus stats_player_week_2025, draft_picks. Prints tables; writes nothing.
RUN: python usage_jump_by_tier.py --strict [--years 2019,...,2025]   (--strict is the definition doc 292 quotes:
at least one earlier game this season, and not a snap starter last season; the stated form counted Allen Lazard's
2022 return from injury as a jump). Tier joins on the PFR id the snap row carries.
INPUTS (nflverse releases, in the folder you run it from): player_stats_<year>.csv, stats_player_week_2025.csv,
roster_weekly_<year>.csv, snap_counts_<year>.csv, draft_picks_all.csv.
RESULT on 11 Sept (doc 292), strict, 2019-2025, n=349: 15.2% converted. Undrafted 6.2% (97) vs drafted 18.7% (252),
p=0.0027. Shock (the position's snap leader sat out) 17.6% vs 13.8%, p=0.35. Jump game at the bar 24.0% vs 10.3%,
p=0.001, z 0.96 with position and tier in. Drafted RBs 31-39%; receivers 5-13%; tight ends under 8%.
"""
import numpy as np
import pandas as pd
from scipy.stats import fisher_exact

BAR = {'RB': 9.92, 'WR': 9.62, 'TE': 8.25}
LINE = {'RB': 0.50, 'WR': 0.65, 'TE': 0.60}
BEFORE = 0.35
import sys
YEARS = tuple(int(y) for y in (sys.argv[sys.argv.index('--years') + 1].split(',') if '--years' in sys.argv else '2022,2023,2024,2025'.split(',')))
PRIOR = tuple(sorted(set(YEARS) | {min(YEARS) - 1}))
STRICT = '--strict' in sys.argv   # corrected form: >=1 prior game this season AND not a snap starter last season

# ---- weekly points, half-PPR ----------------------------------------------------------------
frames = []
for y in PRIOR:
    frames.append(pd.read_csv('stats_player_week_2025.csv', low_memory=False) if y == 2025 else
                  pd.read_csv(f'player_stats_{y}.csv', low_memory=False).rename(columns={'recent_team': 'team'}))
keep = ['player_id', 'position', 'team', 'season', 'week', 'season_type', 'fantasy_points', 'receptions']
ws = pd.concat([f[[c for c in keep if c in f.columns]] for f in frames], ignore_index=True)
ws = ws[ws.season_type == 'REG'].copy()
ws['half'] = ws.fantasy_points.fillna(0) + 0.5 * ws.receptions.fillna(0)
pts = ws.set_index(['player_id', 'season', 'week']).half.groupby(level=[0, 1, 2]).sum()

# established last season (same definition as emergence_by_tier.py)
sk = ws[ws.position.isin(BAR)]
season = sk.groupby(['player_id', 'season']).agg(g=('week', 'count'), ppg=('half', 'mean'),
                                                  pos=('position', 'last')).reset_index()
season['established'] = (season.g >= 6) & (season.ppg >= season.pos.map(BAR))
est = set(zip(season.player_id[season.established], season.season[season.established] + 1))

# ---- snaps, joined to gsis ids ------------------------------------------------------------------
ros = pd.concat([pd.read_csv(f'roster_weekly_{y}.csv', low_memory=False,
                             usecols=['season', 'gsis_id', 'pfr_id', 'draft_number', 'years_exp', 'position'])
                 for y in PRIOR], ignore_index=True)
ros = ros.dropna(subset=['pfr_id', 'gsis_id']).drop_duplicates(['season', 'pfr_id'])
dp = pd.read_csv('draft_picks_all.csv', low_memory=False)[['gsis_id', 'round']].dropna().drop_duplicates('gsis_id')

snaps = pd.concat([pd.read_csv(f'snap_counts_{y}.csv', low_memory=False) for y in PRIOR], ignore_index=True)
snaps = snaps[(snaps.game_type == 'REG') & snaps.position.isin(BAR)].copy()
n0 = len(snaps)
snaps = snaps.merge(ros[['season', 'pfr_id', 'gsis_id', 'draft_number', 'years_exp']],
                    left_on=['season', 'pfr_player_id'], right_on=['season', 'pfr_id'], how='left')
unmatched = snaps.gsis_id.isna()
print(f'snap rows RB/WR/TE {n0}; joined to a gsis id {int((~unmatched).sum())} '
      f'({(~unmatched).mean():.1%}); unmatched by position:',
      snaps[unmatched].position.value_counts().to_dict())
snaps = snaps[~unmatched].copy()
dpp = pd.read_csv('draft_picks_all.csv', low_memory=False)[['pfr_player_id', 'round']].dropna().drop_duplicates('pfr_player_id')
snaps = snaps.merge(dpp, on='pfr_player_id', how='left')      # tier on the PFR id the snap row carries
team_games = snaps.groupby(['season', 'team']).week.apply(lambda s: sorted(set(s))).to_dict()
last_share = snaps.groupby(['gsis_id', 'season']).offense_pct.mean()
snaps = snaps[snaps.season >= min(YEARS)].copy()
print('EVENT SEASONS', YEARS)

def tier(r):
    if pd.notna(r['round']):
        k = int(r['round'])
        return '1' if k == 1 else ('2-3' if k <= 3 else '4-7')
    return 'undrafted'    # no PFR draft row (draft_picks carries a PFR id for ~100% of picks since 2010)

events, short = [], 0
for (gid, yr), g in snaps.groupby(['gsis_id', 'season']):
    g = g.sort_values('week')
    pos = g.position.iloc[-1]
    if (gid, yr) in est:
        continue
    prior_shares = []
    for i, row in enumerate(g.itertuples()):
        if row.week > 14:
            break
        line = LINE[pos]
        prior_mean = np.mean(prior_shares) if prior_shares else 0.0
        starter_last = last_share.get((gid, yr - 1), 0.0) >= line
        ok_strict = (len(prior_shares) >= 1 and not starter_last) if STRICT else True
        if row.week >= 2 and row.offense_pct >= line and prior_mean < BEFORE and ok_strict:
            # the four games after the jump game
            later = g[g.week > row.week]
            nxt = later.week.tolist()[:4]
            ptsA = [pts.get((gid, yr, w), 0.0) for w in nxt]
            tg = [w for w in team_games.get((yr, row.team), []) if w > row.week][:4]
            ptsB = sum(pts.get((gid, yr, w), 0.0) for w in tg) / 4.0 if len(tg) == 4 else np.nan
            # shock: the teammate who led this position's snaps before this week sat out this game
            mates = snaps[(snaps.season == yr) & (snaps.team == row.team) & (snaps.position == pos)
                          & (snaps.week < row.week) & (snaps.gsis_id != gid)]
            shock = False
            if not mates.empty:
                lead = mates.groupby('gsis_id').offense_snaps.sum().idxmax()
                shock = not ((snaps.season == yr) & (snaps.team == row.team) & (snaps.week == row.week)
                             & (snaps.gsis_id == lead)).any()
            jump_pts = pts.get((gid, yr, row.week), 0.0)
            events.append(dict(gsis_id=gid, season=yr, pos=pos, team=row.team, week=row.week,
                               share=row.offense_pct, prior=prior_mean, tier=tier(row._asdict()),
                               years_exp=row.years_exp, n_after=len(nxt),
                               A=float(np.mean(ptsA) >= BAR[pos]) if len(nxt) >= 2 else np.nan,
                               ppgA=np.mean(ptsA) if len(nxt) >= 2 else np.nan,
                               B=float(ptsB >= BAR[pos]) if not np.isnan(ptsB) else np.nan,
                               shock=shock, jump_hit=jump_pts >= BAR[pos], player=row.player))
            break
        prior_shares.append(row.offense_pct)

ev = pd.DataFrame(events)
print('DEFINITION:', 'STRICT (>=1 prior game, not a snap starter last season)' if STRICT else 'AS STATED')
print(f'\nJUMP EVENTS {len(ev)} | fewer than two games after (outcome A missing): '
      f'{int(ev.A.isna().sum())}, by tier {ev[ev.A.isna()].tier.value_counts().to_dict()}')
order = ['1', '2-3', '4-7', 'undrafted']

def table(df, col, label):
    d = df.dropna(subset=[col])
    t = d.groupby('tier')[col].agg(['size', 'sum']).reindex(order).fillna(0)
    t.columns = ['n', 'hits']
    t['rate'] = (t.hits / t.n).round(3)
    print(f'\n{label}  (base {d[col].mean():.3f}, n={len(d)})')
    print(t.to_string())
    return d

dA = table(ev, 'A', 'OUTCOME A: next four games played at or above replacement, by draft tier')
dB = table(ev, 'B', 'OUTCOME B: points over the next four team games / 4, missed games zero')

def fisher(d, col, mask, lab):
    a = d[mask][col].astype(bool); b = d[~mask][col].astype(bool)
    tab = [[a.sum(), (~a).sum()], [b.sum(), (~b).sum()]]
    orr, p = fisher_exact(tab)
    print(f'  {lab}: {a.mean():.3f} (n={len(a)}) vs {b.mean():.3f} (n={len(b)}), Fisher p={p:.4f}')

print('\nCONTRASTS on outcome A')
fisher(dA, 'A', dA.tier == 'undrafted', 'undrafted vs drafted')
fisher(dA, 'A', dA.tier.isin(['1', '2-3']), 'rounds 1-3 vs everyone else')
fisher(dA, 'A', dA.shock, 'jump came with the position leader sitting out vs not')
fisher(dA, 'A', dA.jump_hit, 'scored the bar in the jump game vs not')

print('\nBY POSITION, outcome A')
print(dA.groupby(['pos', 'tier']).A.agg(['size', 'mean']).round(3).unstack('tier').to_string())

print('\nWITHIN THE JUMP-GAME SPLIT, by tier (does pedigree still sort once production is seen?)')
for jh in (True, False):
    s = dA[dA.jump_hit == jh]
    t = s.groupby('tier').A.agg(['size', 'mean']).reindex(order).round(3)
    print(f'  jump game at the bar = {jh}:', {k: (int(v['size']) if pd.notna(v['size']) else 0,
                                               v['mean']) for k, v in t.iterrows()})

# logistic, by hand (no statsmodels here): A ~ tier dummies + jump_hit + shock + pos dummies
T = dA[['tier', 'pos']].copy(); T['tier'] = T.tier.replace({'1': '1-3', '2-3': '1-3'})
X = pd.get_dummies(T, drop_first=False).astype(float)
X = X.drop(columns=['tier_4-7', 'pos_WR'])          # reference: a round 4-7 WR
X['jump_hit'] = dA.jump_hit.astype(float); X['shock'] = dA.shock.astype(float)
X.insert(0, 'const', 1.0)
y = dA.A.astype(float).values
Xm = X.values; beta = np.zeros(Xm.shape[1])
for _ in range(50):
    pr = 1 / (1 + np.exp(-Xm @ beta)); W = pr * (1 - pr)
    H = Xm.T @ (Xm * W[:, None]); g_ = Xm.T @ (y - pr)
    step = np.linalg.solve(H, g_); beta += step
    if np.abs(step).max() < 1e-8:
        break
se = np.sqrt(np.diag(np.linalg.inv(H)))
print('\nLOGISTIC on outcome A (reference: a round 4-7 WR, no shock, jump game under the bar)')
for name, b, s in zip(X.columns, beta, se):
    print(f'  {name:<16} {b:+.3f}  se {s:.3f}  z {b/s:+.2f}')

u = dA[(dA.tier == 'undrafted') & (dA.A == True)].sort_values(['season', 'week'])
print(f'\nundrafted conversions after a jump: {len(u)}')
print(u[['season', 'week', 'pos', 'team', 'player', 'share', 'ppgA', 'shock', 'jump_hit']].to_string(index=False))
