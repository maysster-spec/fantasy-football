r"""wopr_spike.py -- doc 389. CAN LAST WEEK'S OPPORTUNITY SHARE CALL NEXT WEEK'S SPIKE?

TESTABLE FORM, written before the run (0.5a2):
  POPULATION  player-weeks 2021 to 2025, regular season, WR and TE, who were NOT startable in week w
              (half-PPR under this league's bar: WR 9.62, TE 8.25 per game, 4.13b) and who played in w+1.
              That is the pool a claim comes from: a man you could have had.
  PREDICTOR   week w opportunity, four of them: targets, target_share, air_yards_share, and WOPR
              (nflverse's 1.5*target_share + 0.7*air_yards_share).
  OUTCOME     a SPIKE in w+1: half-PPR >= 18.0 on this league's scoring (Tre Tucker's week 2 was 20.4).
              Secondary: startable in w+1 (>= the same bar).
  DIRECTION   Matt's, 22 Sept: "I wish there was a way we could have predicted the break out for him."
              The claim is that opportunity share in the week before separates the spikes from the rest,
              and separates them BETTER than raw targets, which is what our page screens on today.
  FALSIFIER   top quintile spike rate no better than the base rate, or no better than the targets-only
              top quintile -> the share adds nothing and the page's screen is already as good as it gets.
Standard library plus pandas and numpy. Paths against this file.
"""
import os, sys
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
# ...\Scripts\research\wk1 -> ...\Scripts\research\_nflverse_cache, and the 2026 file sits here in wk1
CACHE = os.environ.get('FF_CACHE') or os.path.normpath(os.path.join(HERE, '..', '_nflverse_cache'))
LIVE = HERE
BAR = {'WR': 9.62, 'TE': 8.25}
SPIKE = 18.0

def score(df):
    g = lambda c: pd.to_numeric(df.get(c, 0), errors='coerce').fillna(0.0)
    return (0.1 * g('rushing_yards') + 6 * g('rushing_tds')
            + 0.5 * g('receptions') + 0.1 * g('receiving_yards') + 6 * g('receiving_tds')
            - 2 * (g('rushing_fumbles_lost') + g('receiving_fumbles_lost'))
            + 2 * (g('rushing_2pt_conversions') + g('receiving_2pt_conversions'))
            + 6 * g('special_teams_tds'))

def load(season):
    p = os.path.join(CACHE, f'stats_player_week_{season}.csv')
    w = pd.read_csv(p, low_memory=False)
    w = w[(w.season_type == 'REG') & (w.position.isin(('WR', 'TE')))].copy()
    w['pts'] = score(w)
    w['week'] = w.week.astype(int)
    for c in ('targets', 'target_share', 'air_yards_share', 'wopr', 'receiving_air_yards'):
        w[c] = pd.to_numeric(w.get(c), errors='coerce')
    w['season'] = season
    return w[['season', 'week', 'player_id', 'player_display_name', 'position', 'team', 'pts',
              'targets', 'target_share', 'air_yards_share', 'wopr', 'receiving_air_yards']]

def build(seasons):
    w = pd.concat([load(s) for s in seasons], ignore_index=True)
    nxt = w[['season', 'week', 'player_id', 'pts', 'position']].copy()
    nxt['week'] = nxt.week - 1
    nxt = nxt.rename(columns={'pts': 'pts_next'})[['season', 'week', 'player_id', 'pts_next']]
    d = w.merge(nxt, on=['season', 'week', 'player_id'], how='inner')
    d['bar'] = d.position.map(BAR)
    d = d[(d.pts < d.bar) & d.targets.notna() & (d.targets >= 1)].copy()   # the claimable pool
    d['spike_next'] = (d.pts_next >= SPIKE).astype(int)
    d['startable_next'] = (d.pts_next >= d.bar).astype(int)
    return d

def bands(d, col, n=5):
    q = pd.qcut(d[col].rank(method='first'), n, labels=False)
    out = []
    for b in range(n):
        m = q == b
        out.append((b + 1, int(m.sum()), float(d[col][m].min()), float(d[col][m].max()),
                    float(d.spike_next[m].mean()), float(d.startable_next[m].mean()),
                    float(d.pts_next[m].mean())))
    return pd.DataFrame(out, columns=['band', 'n', 'lo', 'hi', 'spike_rate', 'startable_rate', 'pts_next'])

# SECOND TEST (doc 389 section 3). THE NEWS SIGNAL WE CAN ACTUALLY HOLD ON A TUESDAY: was the week's
# usage bought by somebody's ABSENCE?
#   POPULATION  as above, inside the top fifth of week-w WOPR (the men a screen would surface).
#   PREDICTOR   the team's ALPHA (highest target share over the three weeks before w, at least 20%)
#               did not play in week w.
#   OUTCOME     spike in w+1, same bar. DIRECTION: usage bought by an absence should hold LESS often.
def alpha_absence(d_all, d_pool):
    rows = []
    for (s_, t), g in d_all.groupby(['season', 'team']):
        by_week = {w: set(x.player_id) for w, x in g.groupby('week')}
        for w in sorted(by_week):
            prior = g[(g.week >= w - 3) & (g.week < w)]
            if prior.empty:
                continue
            sh = prior.groupby('player_id').target_share.mean().sort_values(ascending=False)
            if sh.empty or not (sh.iloc[0] >= 0.20):
                continue
            rows.append((s_, t, w, sh.index[0], int(sh.index[0] not in by_week.get(w, set()))))
    a = pd.DataFrame(rows, columns=['season', 'team', 'week', 'alpha_id', 'alpha_out'])
    m = d_pool.merge(a, on=['season', 'team', 'week'], how='inner')
    return m[m.player_id != m.alpha_id]


if __name__ == '__main__':
    d = build(range(2021, 2026))
    print(f'POPULATION {len(d)} player-weeks, {d.season.nunique()} seasons, WR {int((d.position=="WR").sum())} '
          f'TE {int((d.position=="TE").sum())}')
    print(f'BASE RATES: spike next week {d.spike_next.mean():.3f}   startable next week {d.startable_next.mean():.3f}   '
          f'mean points next week {d.pts_next.mean():.2f}')
    for col in ('targets', 'target_share', 'air_yards_share', 'wopr'):
        print(f'\n--- {col} ---')
        print(bands(d.dropna(subset=[col]), col).round(3).to_string(index=False))
    dd = d.dropna(subset=['wopr', 'targets'])
    for col in ('wopr', 'targets', 'air_yards_share'):
        cut = dd[col].rank(method='first', pct=True) >= 0.8
        print(f'\nTOP FIFTH by {col}: n={int(cut.sum())} spike {dd.spike_next[cut].mean():.3f} '
              f'startable {dd.startable_next[cut].mean():.3f} pts {dd.pts_next[cut].mean():.2f}')
    hi_w = dd.wopr.rank(method='first', pct=True) >= 0.8
    hi_t = dd.targets.rank(method='first', pct=True) >= 0.8
    print('THE CROSS:')
    for lab, m_ in (('air yards only', hi_w & ~hi_t), ('targets only', hi_t & ~hi_w), ('both', hi_w & hi_t), ('neither', ~hi_w & ~hi_t)):
        print(f'  {lab:15s} n={int(m_.sum()):5d} spike {dd.spike_next[m_].mean():.3f} startable {dd.startable_next[m_].mean():.3f}')

    print('\n=== SECOND TEST: was the usage bought by an absence? ===')
    allrows = pd.concat([load(s_) for s_ in range(2021, 2026)], ignore_index=True)
    m = alpha_absence(allrows, d)
    top = m[m.wopr.rank(method='first', pct=True) >= 0.8]
    print(f'pool with a defined alpha: {len(m)}; top fifth of WOPR inside it: {len(top)}')
    for lab, sub in (('alpha PLAYED in week w', top[top.alpha_out == 0]),
                     ('alpha was OUT in week w', top[top.alpha_out == 1]),
                     ('whole pool, alpha played', m[m.alpha_out == 0]),
                     ('whole pool, alpha out', m[m.alpha_out == 1])):
        if len(sub):
            print(f'  {lab:26s} n={len(sub):5d}  spike next {sub.spike_next.mean():.3f}  '
                  f'startable next {sub.startable_next.mean():.3f}')

    # LIVE CHECK: 2026 week 1 into week 2, from the 2026 file build_form.py keeps in wk1
    p26 = os.path.join(LIVE, 'stats_player_week_2026.csv')
    if os.path.exists(p26):
        global CACHE_2026
        w = pd.read_csv(p26, low_memory=False)
        w = w[(w.season_type == 'REG') & (w.position.isin(('WR', 'TE')))].copy()
        w['pts'] = score(w); w['week'] = w.week.astype(int)
        for c in ('targets', 'target_share', 'air_yards_share', 'wopr'):
            w[c] = pd.to_numeric(w.get(c), errors='coerce')
        w1 = w[w.week == 1]; w2 = w[w.week == 2][['player_id', 'pts']].rename(columns={'pts': 'pts_w2'})
        pool = w1.merge(w2, on='player_id', how='inner')
        pool = pool[(pool.pts < pool.position.map(BAR)) & (pool.targets >= 1)].copy()
        pool['spike'] = (pool.pts_w2 >= SPIKE).astype(int)
        pool['wopr_pct'] = pool.wopr.rank(pct=True)
        top26 = pool[pool.wopr_pct >= 0.8]
        print(f'\n=== LIVE 2026, week 1 into week 2 === pool {len(pool)}, spikes {int(pool.spike.sum())} '
              f'({pool.spike.mean():.1%}); top fifth by WOPR caught {int(top26.spike.sum())} of {int(pool.spike.sum())}')
        print(pool[pool.spike == 1].sort_values('wopr_pct', ascending=False)
              [['player_display_name', 'position', 'team', 'targets', 'wopr', 'wopr_pct', 'pts', 'pts_w2']]
              .round(3).to_string(index=False))
