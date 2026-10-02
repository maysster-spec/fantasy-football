"""Does the DEFENSE or KICKER pool thin out as the season goes on?
[doc 431] Doc 252 built this curve for RB/WR/TE/QB and EXCLUDED defenses and kickers in its own
words, because it needed weekly D/ST scoring under our rules and section 2 did not carry it.
Section 2 has carried it since v9.3 and D/ST12 was measured at 5.99 (doc 265), corrected to 5.51 at doc 441
(the file it was measured on was missing 142 event-less team-weeks); K12 at 8.26 (doc 423).
The blocker named when it was skipped is gone, so this is that table.

METHOD, and it differs from doc 252 on purpose. Doc 252 rebuilt who was ROSTERED week by week from
the draft plus every executed add and drop. There are only 32 defenses and about 32 kickers, and a
12-team league rosters 12 of each, so the count that clears the bar is nearly the whole story and a
roster reconstruction is not needed to bound it. A player is USABLE in week W if he averages his
position's replacement rate over weeks W to W+3 (doc 252's own definition).
  usable          = how many clear the bar in that window
  free and usable = usable minus 12, the WORST CASE, assuming every rostered one is a good one.
Baselines: D/ST 5.51 a week (doc 441), K 8.26 a week, both under this league's scoring. 2021-2025 REG.
"""
import os
import pandas as pd, numpy as np

# paths resolve against this file (0.4): Scripts\research\dst_k_supply.py
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', '..', 'Source'))
CACHE = os.path.join(HERE, '_nflverse_cache')

DST_BAR, K_BAR, ROSTERED = 5.51, 8.26, 12    # D/ST12 re-measured on the full file, doc 441

def curve(df, bar, label):
    out = []
    for w in range(1, 15):
        counts = []
        for yr, s in df.groupby('season'):
            win = s[s['week'].between(w, w + 3)]
            if win.empty:
                continue
            m = win.groupby('unit')['pts'].mean()
            counts.append(int((m >= bar).sum()))
        if counts:
            out.append((w, np.mean(counts)))
    print(f'\n{label}  (bar {bar} a week, window W to W+3, 2021-2025)')
    print(f"  {'week':<6}{'usable':>8}{'free and usable':>18}")
    for w, c in out:
        print(f'  {w:<6}{c:>8.1f}{max(0.0, c-ROSTERED):>18.1f}')
    early = np.mean([c for w, c in out if w <= 5])
    late = np.mean([c for w, c in out if w >= 10])
    print(f'  weeks 1-5 average {early:.1f} usable, {max(0,early-ROSTERED):.1f} free.  '
          f'weeks 10-14 average {late:.1f} usable, {max(0,late-ROSTERED):.1f} free.')
    return early, late

d = pd.read_csv(os.path.join(SRC, 'dst_weekly_2021_2025.csv'))
d = d.rename(columns={'team': 'unit', 'dst_pts': 'pts'})
d = d[d['week'].between(1, 17)]
print(f'D/ST rows: {len(d)}, {d["unit"].nunique()} units')
de, dl = curve(d, DST_BAR, 'DEFENSES')

rows = []
for yr in range(2021, 2026):
    k = pd.read_csv(os.path.join(CACHE, f'stats_player_week_{yr}.csv'), low_memory=False)
    k = k[(k['position'] == 'K') & (k['season_type'] == 'REG') & (k['week'].between(1, 17))].copy()
    g = lambda c: pd.to_numeric(k.get(c, 0), errors='coerce').fillna(0)
    fg = {'fg_made_0_19': 3, 'fg_made_20_29': 3, 'fg_made_30_39': 3,
          'fg_made_40_49': 4, 'fg_made_50_59': 5, 'fg_made_60_': 5}
    # doc 440: a MISSED PAT is not scored in this league (section 2: PAT 1, FG missed -1 and
    # nothing else), so it is not deducted. The old term cost 0.086 a week on average and moved
    # the usable count by 0.4; the shape of the curve did not change.
    pts = g('pat_made') * 1 - g('fg_missed') * 1
    for c, v in fg.items():
        pts = pts + g(c) * v
    k['pts'] = pts
    k['season'] = yr
    k = k.rename(columns={'player_display_name': 'unit'})
    rows.append(k[['season', 'week', 'unit', 'pts']])
kk = pd.concat(rows, ignore_index=True)
kk = kk.sort_values('pts', ascending=False).groupby(['season', 'week', 'unit'], as_index=False).first()
print(f'\nK rows: {len(kk)}, {kk["unit"].nunique()} kickers')
ke, kl = curve(kk, K_BAR, 'KICKERS')
