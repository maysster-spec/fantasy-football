#!/usr/bin/env python3
r"""rb_composite.py -- does the count-composite method that worked at receiver (4.30) work at RB?

Direct analogy to doc 248. Same shape, same outcome definition, same permutation test.
Stdlib only. Reads stats_player_week_<yr>.csv and draft_picks.csv from its own folder.
"""
import csv, collections, os, random, statistics, sys
HERE = os.path.dirname(os.path.abspath(__file__))
RB_REPL = 9.92   # [INHERITED: 4.1's RB30 season total / 17, derived not measured -- 4.13b]

def hp(r):
    g = lambda k: float(r.get(k) or 0)
    return (0.1*g('rushing_yards') + 6*g('rushing_tds') + 0.1*g('receiving_yards')
            + 6*g('receiving_tds') + 0.5*g('receptions')
            - 2*(g('rushing_fumbles_lost') + g('receiving_fumbles_lost')))

def load(y):
    p = os.path.join(HERE, f'stats_player_week_{y}.csv')
    with open(p, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            if (r.get('season_type') or 'REG') == 'REG':
                try: r['_w'] = int(r['week'])
                except (TypeError, ValueError): continue
                yield r

# draft round by gsis_id
rnd, first_seen = {}, {}
for r in csv.DictReader(open(os.path.join(HERE, 'draft_picks.csv'), encoding='utf-8-sig')):
    if r['gsis_id']:
        try: rnd[r['gsis_id']] = int(r['round'])
        except (TypeError, ValueError): pass

SEASONS = [2020, 2021, 2022, 2023, 2024, 2025]
agg = collections.defaultdict(lambda: collections.defaultdict(
    lambda: {'pts':0.0,'g':0,'car':0.0,'tgt':0.0,'ryd':0.0,'reyd':0.0,'rec':0.0,'name':''}))
for y in SEASONS:
    for r in load(y):
        if r.get('position') != 'RB' or not (1 <= r['_w'] <= 14): continue
        a = agg[y][r['player_id']]
        a['pts'] += hp(r); a['g'] += 1
        a['car'] += float(r.get('carries') or 0); a['tgt'] += float(r.get('targets') or 0)
        a['ryd'] += float(r.get('rushing_yards') or 0); a['reyd'] += float(r.get('receiving_yards') or 0)
        a['rec'] += float(r.get('receptions') or 0)
        a['name'] = r.get('player_display_name') or r['player_id']
        first_seen.setdefault(r['player_id'], y)
        first_seen[r['player_id']] = min(first_seen[r['player_id']], y)

rows = []
for y in (2021, 2022, 2023, 2024):
    for pid, a in agg[y].items():
        nxt = agg.get(y+1, {}).get(pid)
        if a['g'] < 4 or not nxt or nxt['g'] < 4: continue
        ppg = a['pts'] / a['g']
        if ppg >= RB_REPL: continue                     # NOT startable, same as 4.30
        exp = y - first_seen[pid] + 1
        if exp > 3: continue                            # years 1-3
        touch = a['car'] + a['rec']
        if touch < 1: continue
        rows.append(dict(season=y, pid=pid, name=a['name'],
                         rd=rnd.get(pid, 99),
                         ypt=(a['ryd'] + a['reyd']) / touch,
                         tpg=touch / a['g'],
                         hit=1 if nxt['pts']/nxt['g'] >= RB_REPL else 0))

print(f'POPULATION: RB seasons 2021-2024, NFL years 1-3, NOT startable (under {RB_REPL} half-PPR ppg,')
print(f'  weeks 1-14), 4+ games, who played 4+ games again the next season.  n = {len(rows)}')
base = sum(r['hit'] for r in rows)/len(rows)
print(f'OUTCOME: startable the following season.  BASE RATE {base:.1%}  ({sum(r["hit"] for r in rows)} of {len(rows)})')

MED_Y = statistics.median(r['ypt'] for r in rows)
MED_T = statistics.median(r['tpg'] for r in rows)
print(f'\nTHRESHOLDS taken as the population MEDIAN so the cut is not chosen: '
      f'yards per touch {MED_Y:.2f}, touches per game {MED_T:.2f}')

def perm(a, b, reps=6000, seed=20260913):
    """one-sided permutation on the difference in hit rate"""
    if not a or not b: return None, None
    d = sum(a)/len(a) - sum(b)/len(b)
    pool = a + b; n, k = len(pool), len(a)
    rng = random.Random(seed); c = 0; idx = list(range(n))
    for _ in range(reps):
        rng.shuffle(idx)
        if sum(pool[i] for i in idx[:k])/k - sum(pool[i] for i in idx[k:])/(n-k) >= d: c += 1
    return d, c/reps

def score(r, my, mt):
    return (1 if r['rd'] <= 3 else 0) + (1 if r['ypt'] > my else 0) + (1 if r['tpg'] > mt else 0)

print('\nTHE COMPOSITE, count of three')
print(f"  {'signals':<10}{'n':>5}{'startable next season':>24}")
cells = collections.defaultdict(list)
for r in rows: cells[score(r, MED_Y, MED_T)].append(r['hit'])
for k in (0,1,2,3):
    v = cells[k]
    print(f'  {k} of 3    {len(v):>5}{(sum(v)/len(v) if v else 0):>23.1%}')
hi = cells[3]; lo = cells[0]+cells[1]+cells[2]
d, p = perm(hi, lo)
print(f'\n  3 of 3 (n={len(hi)}) minus under 3 (n={len(lo)}): {d:+.1%}, permutation p = {p:.4f}')

print('\nEACH SIGNAL ALONE (same population, same test)')
for lab, f in (('NFL rounds 1-3', lambda r: r['rd'] <= 3),
               ('NFL round 1 only', lambda r: r['rd'] == 1),
               (f'yards/touch > {MED_Y:.2f}', lambda r: r['ypt'] > MED_Y),
               (f'touches/game > {MED_T:.2f}', lambda r: r['tpg'] > MED_T)):
    a = [r['hit'] for r in rows if f(r)]; b = [r['hit'] for r in rows if not f(r)]
    d2, p2 = perm(a, b)
    print(f'  {lab:<22}n={len(a):>4} vs {len(b):<4} {d2:+.1%}  p={p2:.4f}')

print('\nIS THE THRESHOLD CHOSEN? every percentile cut, both continuous signals moved together')
import math
vals_y = sorted(r['ypt'] for r in rows); vals_t = sorted(r['tpg'] for r in rows)
q = lambda v, f: v[max(0, min(len(v)-1, int(f*len(v))))]
for f in (0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65):
    my, mt = q(vals_y, f), q(vals_t, f)
    c = collections.defaultdict(list)
    for r in rows: c[score(r, my, mt)].append(r['hit'])
    h = c[3]; l = c[0]+c[1]+c[2]
    d3, p3 = perm(h, l)
    print(f'  cut at p{f*100:.0f}  3of3 n={len(h):>3} rate {(sum(h)/len(h) if h else 0):>5.1%}   '
          f'diff {d3:+.1%}  p={p3:.4f}')

print('\nTHE 3-of-3 CELL, named (median cut)')
for r in sorted([x for x in rows if score(x, MED_Y, MED_T) == 3], key=lambda x: -x['hit']):
    print(f"   {r['season']} {r['name']:<24}rd {r['rd'] if r['rd']<99 else 'UDFA':<5}"
          f"ypt {r['ypt']:.2f}  tpg {r['tpg']:.1f}  -> {'STARTABLE' if r['hit'] else 'no'}")
