r"""Is a receiver's WEEK-1 share of his team's targets a signal, the way the week-1 backfield
share is at running back (week1_share.py, +29.1pp startable, p=0.0003)?

THE CLAIM IN ITS TESTABLE FORM, written before the run (0.5a2):
  Among pass-catchers who were NOT startable the previous season -- i.e. men you could have had off
  a waiver wire -- the share of his team's WEEK 1 targets predicts his weeks 2-14 half-PPR scoring,
  and a high week-1 share marks a receiver who reaches replacement more often than the rest do.

POPULATION -- restate it every time (0.6): every WR and TE, seasons 2021-2025, who (a) played in
week 1 and saw at least one target, (b) averaged BELOW his position's replacement rate over the
prior season or has no prior season on file, and (c) played 4+ games in weeks 2-14. The prior-season
filter is what makes this a WAIVER population rather than a draft-pick population; without it the
top share band is just the league's WR1s and the test measures nothing (4.23's selection trap).
PREDICTOR: his share of his team's week-1 targets, that team's week-1 targets being the denominator.
OUTCOME: half-PPR ppg over weeks 2-14, and whether it reaches WR 9.62 / TE 8.25 (doc 12; derived
from 4.1 / 17, and flagged as derived per 9.4).
BASELINE: the same population split by share. Permutation on the difference, 4,000 draws.
Stdlib only.
"""
import collections, csv, os, random, statistics

SEASONS = [2021, 2022, 2023, 2024, 2025]
REPL = {'WR': 9.62, 'TE': 8.25}
HERE = os.path.dirname(os.path.abspath(__file__))

def half_ppr(r):
    g = lambda k: float(r.get(k) or 0)
    return (0.1 * g('rushing_yards') + 6 * g('rushing_tds') + 0.1 * g('receiving_yards')
            + 6 * g('receiving_tds') + 0.5 * g('receptions')
            - 2 * (g('rushing_fumbles_lost') + g('receiving_fumbles_lost')))

def load(season):
    out = []
    with open(os.path.join(HERE, f'stats_player_week_{season}.csv'), newline='',
              encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            if (r.get('season_type') or 'REG') != 'REG':
                continue
            if (r.get('position') or '') not in ('WR', 'TE'):
                continue
            try:
                r['_w'] = int(r['week'])
            except Exception:
                continue
            out.append(r)
    return out

# prior-season ppg, so we can keep only men who were NOT startable last year
prior = {}
for s in SEASONS + [2020]:
    try:
        rows = load(s)
    except FileNotFoundError:
        continue
    agg = collections.defaultdict(list)
    for r in rows:
        if r['_w'] <= 14:
            agg[r['player_id']].append(half_ppr(r))
    for pid, v in agg.items():
        prior[(s, pid)] = sum(v) / len(v)

rows_out = []
for s in SEASONS:
    rows = load(s)
    wk1 = [r for r in rows if r['_w'] == 1]
    team_tgt = collections.Counter()
    for r in wk1:
        team_tgt[r['team']] += float(r.get('targets') or 0)
    rest = collections.defaultdict(list)
    for r in rows:
        if 2 <= r['_w'] <= 14:
            rest[r['player_id']].append(half_ppr(r))
    for r in wk1:
        tg = float(r.get('targets') or 0)
        if tg < 1 or not team_tgt[r['team']]:
            continue
        pid, pos = r['player_id'], r['position']
        p = prior.get((s - 1, pid))
        if p is not None and p >= REPL[pos]:
            continue                      # he was already startable: not a wire man
        g = rest.get(pid, [])
        if len(g) < 4:
            continue
        rows_out.append({'season': s, 'name': r['player_display_name'], 'pos': pos,
                         'team': r['team'], 'share': tg / team_tgt[r['team']],
                         'ppg': sum(g) / len(g), 'games': len(g),
                         'hit': 1 if (sum(g) / len(g)) >= REPL[pos] else 0,
                         'rookie': p is None})

print(__doc__.split('\n')[0])
print(f'population: {len(rows_out)} player-seasons, {SEASONS[0]}-{SEASONS[-1]}, '
      f'wire-eligible pass-catchers who played week 1\n')
BANDS = [(0, .10), (.10, .15), (.15, .20), (.20, 1.01)]
LBL = ['under 10%', '10 to 15%', '15 to 20%', '20% or more']
print(f'{"week-1 target share":24s} {"n":>4s} {"wks 2-14 ppg":>13s} {"reached replacement":>20s}')
for (lo, hi), lab in zip(BANDS, LBL):
    c = [r for r in rows_out if lo <= r['share'] < hi]
    if not c:
        continue
    print(f'{lab:24s} {len(c):4d} {statistics.mean(r["ppg"] for r in c):13.2f} '
          f'{100*statistics.mean(r["hit"] for r in c):19.0f}%')

CUT = .15
hi = [r for r in rows_out if r['share'] >= CUT]
lo = [r for r in rows_out if r['share'] < CUT]
dp = statistics.mean(r['ppg'] for r in hi) - statistics.mean(r['ppg'] for r in lo)
dh = statistics.mean(r['hit'] for r in hi) - statistics.mean(r['hit'] for r in lo)
print(f'\n  {CUT:.0%} or more (n={len(hi)}) minus under (n={len(lo)}): '
      f'ppg {dp:+.2f}, startable rate {100*dh:+.1f}%')

random.seed(11)
def perm(key, obs):
    vals = [r[key] for r in rows_out]
    n = len(hi); c = 0
    for _ in range(4000):
        random.shuffle(vals)
        d = statistics.mean(vals[:n]) - statistics.mean(vals[n:])
        if d >= obs:
            c += 1
    return (c + 1) / 4001
print(f'  permutation, 4000 draws, one-sided: ppg p={perm("ppg", dp):.4f}   '
      f'startable p={perm("hit", dh):.4f}')

print('\n  the ten biggest week-1 shares, and what happened next:')
for r in sorted(rows_out, key=lambda r: -r['share'])[:10]:
    print(f'    {r["season"]} {r["team"]:4s} {r["name"][:22]:23s} {r["pos"]} '
          f'{r["share"]:4.0%} of week-1 targets -> {r["ppg"]:5.1f} ppg over {r["games"]:2d} games'
          f'{"   STARTABLE" if r["hit"] else ""}')
print(f'\n  base rate across the whole population: '
      f'{100*statistics.mean(r["hit"] for r in rows_out):.0f}% startable, '
      f'{statistics.mean(r["ppg"] for r in rows_out):.2f} ppg')
