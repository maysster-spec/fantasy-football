"""job_opens.py -- does the backfield open, and does a big week-1 share tell you? (doc 343)

Run it:   py research\wk1\job_opens.py            the whole thing, about 30 seconds
          py research\wk1\job_opens.py --share    only the 2026 column for inherit_2026.csv

WHAT IT ANSWERS, and the testable form was written before any of it ran (directive 0.5(a2)):
  POPULATION  every NFL team-season 2022-2025 whose week-1 RB usage leader and second back both
              played in week 1 with combined RB work (carries + targets) of 10 or more; n=126.
  PREDICTOR   the second back's share of his team's week-1 RB carries plus targets, the leader IN
              the denominator. This is doc 300's measure. It is NOT doc 292's T5, which excludes
              the leader and runs on snaps and is roughly double on a clean two-man room -- the
              two must never be swapped.
  OUTCOME 1   the week-1 leader misses a game in weeks 2-14, byes excluded.  <- what shipped
  OUTCOME 2   the second back is startable over weeks 2-14 (9.92 half-PPR a game, doc 12's RB
              replacement, which is 4.1 / 17 and is DERIVED not measured -- 4.13b).
  OUTCOME 3   how many of weeks 2-14 he spends as the room's usage leader.   <- did NOT ship
  DIRECTION   if a seat is worth more than the sheet says, outcome 3 in the top band must be
              materially above the sheet's 3.02 weeks.

AND OUTCOME 3 FAILED ITS OWN TEST, WHICH IS WHY IT IS HERE AND NOT ON THE SHEET. The raw
gradient is 1.24 / 1.91 / 4.20 / 6.00 weeks. Counted only from the FIRST ABSENCE onward -- the
only weeks that are an inheritance rather than a man who was already half the backfield -- it is
2.05 / 3.21 / 3.12 / 4.71, p=0.081; and after dropping the men who already led the room before any
absence, +0.75 at p=0.286. UNDERPOWERED, NOT DISPROVED. Do not quote 6.00 weeks.

INPUTS: research\_nflverse_cache\stats_player_week_2022..2025.csv and, for --share,
research\wk1\stats_player_week_2026.csv. Standard library plus pandas and numpy only (0.4).
"""
import glob
import os
import re
import sys
import unicodedata

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.normpath(os.path.join(HERE, '..', '_nflverse_cache'))
SRC = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'Source'))
BAR = 9.92
WEEKS = range(2, 15)
rng = np.random.default_rng(20260917)


def norm(s):
    s = unicodedata.normalize('NFKD', str(s or '')).encode('ascii', 'ignore').decode()
    s = s.lower().replace('.', '').replace("'", '').replace('-', ' ')
    s = re.sub(r'\b(jr|sr|ii|iii|iv|v)\b', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def rbs(paths):
    out = []
    for p in paths:
        d = pd.read_csv(p, low_memory=False)
        d = d[(d.season_type == 'REG') & (d.position == 'RB')]
        out.append(d[['player_id', 'player_display_name', 'season', 'week', 'team',
                      'carries', 'targets', 'receptions', 'fantasy_points']])
    d = pd.concat(out, ignore_index=True)
    for c in ('carries', 'targets', 'receptions', 'fantasy_points'):
        d[c] = pd.to_numeric(d[c], errors='coerce').fillna(0.0)
    d['work'] = d.carries + d.targets
    d['half'] = d.fantasy_points + 0.5 * d.receptions
    return d


def band(s):
    return '<20' if s < .20 else '20-30' if s < .30 else '30-40' if s < .40 else '40+'


def study():
    paths = sorted(glob.glob(os.path.join(CACHE, 'stats_player_week_*.csv')))
    paths = [p for p in paths if '2026' not in os.path.basename(p)]
    if not paths:
        print('NO INPUT: put stats_player_week_2022..2025.csv in research\\_nflverse_cache')
        return 1
    d = rbs(paths)
    played = set(zip(d.season, d.team, d.week))
    rows = []
    for (season, team), g1 in d[d.week == 1].groupby(['season', 'team']):
        g1 = g1[g1.work > 0].sort_values(['work', 'player_id'], ascending=[False, True])
        if len(g1) < 2:
            continue
        lead, two = g1.iloc[0], g1.iloc[1]
        tot = float(g1.work.sum())
        if tot < 10:
            continue
        later = d[(d.season == season) & (d.team == team) & (d.week.isin(WEEKS))]
        wks = sorted(w for w in WEEKS if (season, team, w) in played)
        if not wks:
            continue
        lead_wk = set(later[later.player_id == lead.player_id].week)
        missed = [w for w in wks if w not in lead_wk]
        first = missed[0] if missed else None
        held_all = held_after = held_before = 0
        for w in wks:
            gw = later[(later.week == w) & (later.work > 0)]
            if not len(gw):
                continue
            top = gw.sort_values(['work', 'player_id'], ascending=[False, True]).iloc[0]
            if top.player_id == two.player_id:
                held_all += 1
                if first is not None and w >= first:
                    held_after += 1
                else:
                    held_before += 1
        tl = later[later.player_id == two.player_id]
        g = len(tl)
        ppg = float(tl.half.sum()) / g if g else 0.0
        rows.append(dict(season=season, team=team, lead=lead.player_display_name,
                         two=two.player_display_name, share=float(two.work) / tot,
                         opens=first is not None, held_all=held_all, held_after=held_after,
                         was_colead=held_before > 0, ppg=ppg,
                         startable=bool(g >= 4 and ppg >= BAR)))
    r = pd.DataFrame(rows)
    r['band'] = r.share.map(band)
    print('POPULATION %d team-seasons, %s' % (len(r), sorted(int(x) for x in r.season.unique())))
    print('P(the job opens), all backfields = %.3f   [the sheet used this flat]' % r.opens.mean())
    print('\n%-8s %4s %8s %10s %10s %11s %8s' % ('band', 'n', 'P(open)', 'startable',
                                                 'held ALL', 'held AFTER', 'co-lead'))
    for b in ('<20', '20-30', '30-40', '40+'):
        x = r[r.band == b]
        o = x[x.opens]
        print('%-8s %4d %8.3f %10.3f %10.2f %11.2f %8.2f'
              % (b, len(x), x.opens.mean(), x.startable.mean(), x.held_all.mean(),
                 o.held_after.mean() if len(o) else 0, x.was_colead.mean()))
    s = r[~r.was_colead]
    print('\nSEATS ONLY -- the men who were NOT already leading the room before any absence')
    for b in ('<20', '20-30', '30-40', '40+'):
        x = s[s.band == b]
        o = x[x.opens]
        if not len(x):
            continue
        print('%-8s %4d %8.3f %10.3f %21.2f'
              % (b, len(x), x.opens.mean(), x.startable.mean(),
                 o.held_after.mean() if len(o) else 0))

    def perm(z, col, split=0.35, n=6000):
        hi = z[z.share >= split][col].astype(float).values
        lo = z[z.share < split][col].astype(float).values
        if len(hi) < 3 or len(lo) < 3:
            return None
        obs = hi.mean() - lo.mean()
        pool = np.concatenate([hi, lo])
        k, c = len(hi), 0
        for _ in range(n):
            rng.shuffle(pool)
            if pool[:k].mean() - pool[k:].mean() >= obs:
                c += 1
        return obs, (c + 1) / (n + 1), len(hi), len(lo)

    print('\nPERMUTATION at a 35%% split, one-sided, 6,000 draws')
    for nm, df in (('all', r), ('seats only', s)):
        for col in ('opens', 'startable', 'held_after'):
            z = df[df.opens] if col == 'held_after' else df
            res = perm(z, col)
            if res:
                print('  %-11s %-11s %+.2f  p=%.4f  (n %d vs %d)' % (nm, col, *res))
    r.to_csv(os.path.join(HERE, 'job_opens_rows.csv'), index=False)
    print('\nrows written to job_opens_rows.csv')
    return 0


def share_2026():
    """Stamp wk1_share and wk1_band onto Source\\inherit_2026.csv, blank on a join miss."""
    import csv
    w = os.path.join(HERE, 'stats_player_week_2026.csv')
    i = os.path.join(SRC, 'inherit_2026.csv')
    for p in (w, i):
        if not os.path.exists(p):
            print('MISSING INPUT: ' + p)
            return 1
    d = rbs([w])
    d = d[d.week == 1]
    tot = d.groupby('team').work.sum()
    got = {}
    for _, x in d.iterrows():
        if tot[x.team] > 0:
            got[norm(x.player_display_name)] = x.work / tot[x.team]
    rows = list(csv.DictReader(open(i, encoding='utf-8-sig')))
    hit = 0
    for r in rows:
        v = got.get(norm(r['next_man']))
        # A MISS IS BLANK, NEVER ZERO. A missing week-1 line is no information; a zero would
        # read as "nobody wants him" and would be priced as the bottom band (section 3, doc 251).
        r['wk1_share'] = '' if v is None else f'{v:.3f}'
        r['wk1_band'] = '' if v is None else band(v)
        hit += v is not None
    cols = list(rows[0].keys())
    with open(i, 'w', newline='', encoding='utf-8') as fh:
        wr = csv.DictWriter(fh, fieldnames=cols)
        wr.writeheader()
        wr.writerows(rows)
    print('inherit_2026.csv: %d of %d rows carry a week-1 share' % (hit, len(rows)))
    return 0


if __name__ == '__main__':
    sys.exit(share_2026() if '--share' in sys.argv[1:] else study())
