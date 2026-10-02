#!/usr/bin/env python3
"""RED TEAM ITEM 1 -- doc 314's contest bands, re-run with the men nobody filed on.

TESTABLE FORM (stated before the run): among every FREE RB/WR/TE with a prior regular-season game,
in the free pool rebuilt week by week from the draft plus every executed add and drop 2022-2025,
the mean number of teams filing a WAIVER claim on him that week (ZERO for the men nobody filed on)
and the share drawing two or more claims still rise with targets+carries in his last completed game.
FALSIFIER: the 15+ band is not above the under-5 band once the zero-filer men are in.

CONTROL: the claimed-only rows from this join must reproduce doc 314's table (1.17 / 1.49 / 1.83 /
2.27 filers; 14 / 29 / 40 / 56 % contested; n 88 / 180 / 94 / 41) to within rounding, or the join is
wrong and nothing below counts.

Stdlib + numpy. Inputs: Source\\waiver_report_2022..2025.csv, Source\\draft_history_2021_2025.csv,
nflverse players.csv and stats_player_week_2022..2025.csv.
"""
import collections, csv, os, re, sys, unicodedata, random, json
from datetime import datetime
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))   # every path resolves against this file (0.4)
SRC = os.environ.get('RT_SRC', os.path.normpath(os.path.join(HERE, '..', '..', '..', 'Source')))
NFL = os.environ.get('RT_NFL', os.path.normpath(os.path.join(HERE, '..', '_nflverse_cache')))
OUT = os.environ.get('RT_OUT', HERE)
os.makedirs(OUT, exist_ok=True)
SEASONS = (2022, 2023, 2024, 2025)
WMAX = int(os.environ.get('RT_WMAX', '18'))
BANDS = [(0, 5, 'under 5'), (5, 10, '5 to 9'), (10, 15, '10 to 14'), (15, 1e9, '15 or more')]


def nk(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode()
    s = re.sub(r'\b(jr|sr|ii|iii|iv|v)\b', '', s.lower())
    return re.sub(r'[^a-z]', '', s)


def corr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.std() == 0 or b.std() == 0:
        return float('nan')
    return float(((a - a.mean()) * (b - b.mean())).mean() / (a.std() * b.std()))


# ---- players: espn id -> gsis, name -> gsis ---------------------------------------------------
emap, byname, gpos = {}, collections.defaultdict(list), {}
for r in csv.DictReader(open(os.path.join(NFL, 'players.csv'), newline='', encoding='utf-8')):
    g = r['gsis_id']
    if not g:
        continue
    gpos[g] = r.get('position') or ''
    e = (r.get('espn_id') or '').strip()
    if e:
        emap[e[:-2] if e.endswith('.0') else e] = g
    byname[(nk(r['display_name']), r.get('position') or '')].append(g)
    byname[(nk(r['display_name']), '')].append(g)

# ---- transactions ----------------------------------------------------------------------------
ADD = re.compile(r'ADD Player ID (-?\d+)')
DROP = re.compile(r'DROP Player ID (-?\d+)')
tx = []            # every row, parsed
for yr in SEASONS:
    f = os.path.join(SRC, f'waiver_report_{yr}.csv')
    assert re.search(r'(\d{4})', os.path.basename(f)).group(1) == str(yr)
    for row in csv.DictReader(open(f, newline='', encoding='utf-8-sig')):
        t = row['Transaction'] or ''
        tx.append(dict(season=yr, week=int(row['Week']), team=row['Team'], kind=row['Type'],
                       status=row['Status'], date=datetime.strptime(row['Date'], '%Y-%m-%d %H:%M'),
                       adds=ADD.findall(t), drops=DROP.findall(t)))
print(f'transaction rows: {len(tx)}')
print('  by (Type, Status):', dict(collections.Counter((r['kind'], r['status']) for r in tx)))

# ---- doc 314's object: waiver filings grouped by (season, week, pid), any status -------------
who = collections.defaultdict(set)          # (season, week, pid) -> teams that filed (any status)
who_x = collections.defaultdict(set)        # same, but CANCELED and PENDING excluded
for r in tx:
    if r['kind'] != 'WAIVER':
        continue
    for pid in r['adds']:
        who[(r['season'], r['week'], pid)].add(r['team'])
        if r['status'] not in ('CANCELED', 'PENDING'):
            who_x[(r['season'], r['week'], pid)].add(r['team'])
print(f'waiver player-weeks filed on: {len(who)}; contested: '
      f'{sum(1 for v in who.values() if len(v) > 1)}')

# ---- weekly lines -----------------------------------------------------------------------------
form = {}                                   # (season, gsis) -> {week: (touch, half)}
played_any = collections.defaultdict(set)   # season -> gsis with any REG line
for yr in SEASONS:
    for r in csv.DictReader(open(os.path.join(NFL, f'stats_player_week_{yr}.csv'), newline='',
                                 encoding='utf-8')):
        if r.get('season_type') != 'REG':
            continue
        g = lambda k: float(r.get(k) or 0)
        form.setdefault((yr, r['player_id']), {})[int(r['week'])] = (
            g('targets') + g('carries'), g('fantasy_points') + 0.5 * g('receptions'))
        played_any[yr].add(r['player_id'])

# ---- the draft, by name -----------------------------------------------------------------------
drafted = collections.defaultdict(set)      # season -> gsis
unmatched = collections.Counter()
for r in csv.DictReader(open(os.path.join(SRC, 'draft_history_2021_2025.csv'), newline='',
                             encoding='utf-8-sig')):
    yr = int(r['Year'])
    if yr not in SEASONS:
        continue
    pos = (r['Pos'] or '').strip()
    if pos in ('D/ST', 'DST', 'K'):
        continue
    cands = byname.get((nk(r['Player']), pos)) or byname.get((nk(r['Player']), ''))
    if not cands:
        unmatched[yr] += 1
        continue
    # prefer the one who played that season
    pick = [c for c in cands if c in played_any[yr]] or cands
    drafted[yr].add(pick[0])
print('drafted skill players matched to a gsis id per season:',
      {yr: len(drafted[yr]) for yr in SEASONS}, ' unmatched:', dict(unmatched))

# ---- roster reconstruction: executed adds and drops in date order ----------------------------
def roster_at(season, when):
    ros = set(drafted[season])
    for r in sorted((r for r in tx if r['season'] == season and r['status'] == 'EXECUTED'),
                    key=lambda r: r['date']):
        if r['date'] >= when:
            break
        for pid in r['drops']:
            ros.discard(emap.get(pid, 'x'))
        for pid in r['adds']:
            if pid in emap:
                ros.add(emap[pid])
    return ros

run_time = {}
for yr in SEASONS:
    for w in range(2, WMAX + 1):
        ws = [r['date'] for r in tx if r['season'] == yr and r['week'] == w
              and r['kind'] == 'WAIVER' and r['status'] == 'EXECUTED']
        if not ws:
            ws = [r['date'] for r in tx if r['season'] == yr and r['week'] == w]
        run_time[(yr, w)] = max(ws) if ws else None   # the LAST run of the week: a man dropped
        # after Wednesday and claimed Saturday is free by then; claimed men count as free anyway

# ---- the population: every free RB/WR/TE with a prior game, weeks 2-14 ----------------------
rows = []
claimed_seen, claimed_missing = 0, []
for yr in SEASONS:
    for w in range(2, WMAX + 1):
        T = run_time[(yr, w)]
        if T is None:
            continue
        ros = roster_at(yr, T)
        filed_here = {emap.get(pid): teams for (s, wk, pid), teams in who.items()
                      if s == yr and wk == w and not pid.startswith('-') and pid in emap}
        filed_x = {emap.get(pid): teams for (s, wk, pid), teams in who_x.items()
                   if s == yr and wk == w and not pid.startswith('-') and pid in emap}
        for (s, g), weeks in form.items():
            if s != yr:
                continue
            prior = {k: v for k, v in weeks.items() if k < w}
            if not prior:
                continue
            free = g not in ros
            filers = len(filed_here.get(g, ()))
            if filers and gpos.get(g) in ('RB', 'WR', 'TE'):
                claimed_seen += 1
                if not free:
                    claimed_missing.append((yr, w, g))
            if not free and not filers:
                continue
            last = prior[max(prior)]
            rows.append(dict(season=yr, week=w, gsis=g, pos=gpos.get(g, ''), free=free,
                             filers=filers, filers_x=len(filed_x.get(g, ())),
                             touch=last[0], pts=last[1]))
print(f'\nclaimed RB/WR/TE player-weeks (weeks 2-14, with a prior line): {claimed_seen}; '
      f'of them my rebuilt pool says ROSTERED: {len(claimed_missing)} '
      f'({len(claimed_missing) / max(1, claimed_seen):.1%})')

pop = [r for r in rows if r['pos'] in ('RB', 'WR', 'TE')]
claimed = [r for r in pop if r['filers'] > 0]
freepool = [r for r in pop if r['free'] or r['filers'] > 0]   # a claimed man counts as free


def band_table(sel, label):
    print(f'\n  {label}: n={len(sel)}')
    print(f'  {"touches last game":18s} {"n":>5} {"filers":>7} {"P(>=1)":>7} {"P(>=2)":>7} {"P(>=2|>=1)":>11}')
    out = []
    for lo, hi, lab in BANDS:
        ch = [r for r in sel if lo <= r['touch'] < hi]
        if not ch:
            continue
        f = np.array([r['filers'] for r in ch], float)
        p1 = (f >= 1).mean()
        p2 = (f >= 2).mean()
        c = (f[f >= 1] >= 2).mean() if (f >= 1).any() else float('nan')
        print(f'  {lab:18s} {len(ch):5d} {f.mean():7.2f} {p1:7.1%} {p2:7.1%} {c:11.0%}')
        out.append(dict(band=lab, n=len(ch), filers=round(float(f.mean()), 3), p_ge1=round(float(p1), 3),
                        p_ge2=round(float(p2), 3), contested_given_filed=round(float(c), 3)))
    return out


print('\n=== CONTROL: doc 314 reproduced on claimed-only rows from THIS join ===')
r_c = corr([r['touch'] for r in claimed], [r['filers'] for r in claimed])
print(f'  r(touches, filers) = {r_c:+.3f}   (doc 314: +0.296, n=403)')
ctrl = band_table(claimed, 'claimed only (doc 314 population)')

print('\n=== THE TEST: the whole free pool, zero filers included ===')
tt = [r['touch'] for r in freepool]
ff = [r['filers'] for r in freepool]
r_all = corr(tt, ff)
print(f'  r(touches, filers) = {r_all:+.3f}   n={len(freepool)}')
random.seed(7)
z, hits, N = list(ff), 0, 5000
for _ in range(N):
    random.shuffle(z)
    if abs(corr(tt, z)) >= abs(r_all):
        hits += 1
print(f'  permutation p = {(hits + 1) / (N + 1):.5f} (N={N})')
full = band_table(freepool, 'free pool, zero filers included')

print('\n  by position (free pool):')
for pos in ('RB', 'WR', 'TE'):
    sel = [r for r in freepool if r['pos'] == pos]
    print(f'   {pos}: r={corr([r["touch"] for r in sel], [r["filers"] for r in sel]):+.3f} n={len(sel)}')
    band_table(sel, pos)

print('\n=== SELECTION CHECKS not named in doc 314 ===')
st = collections.Counter(r['status'] for r in tx if r['kind'] == 'WAIVER')
print('  waiver-claim rows by status:', dict(st))
print(f'  player-weeks where CANCELED/PENDING rows change the filer count: '
      f'{sum(1 for k in who if len(who[k]) != len(who_x.get(k, ())))} of {len(who)}')
band_table([r for r in claimed if r['filers_x'] > 0] and
           [dict(r, filers=r['filers_x']) for r in claimed if r['filers_x'] > 0],
           'claimed only, CANCELED and PENDING claims not counted')
# the claimant's view: given that ONE team (say Matt) files, how often does anyone else?
view = []
for r in claimed:
    for _ in range(r['filers']):
        view.append(dict(r, others=r['filers'] - 1))
print(f'\n  from the claimant\'s seat (one row per CLAIM, n={len(view)}): P(at least one other team also filed)')
for lo, hi, lab in BANDS:
    ch = [v for v in view if lo <= v['touch'] < hi]
    if ch:
        print(f'   {lab:18s} n={len(ch):4d}  {np.mean([v["others"] >= 1 for v in ch]):.0%}')

# how big is the zero-filer population per band, and what is P(any claim) for a 15+ touch free man
print('\n  size of the free pool per week (RB/WR/TE with a prior game):',
      round(len(freepool) / (len(SEASONS) * 13), 1), 'men a week')
json.dump(dict(control=ctrl, full=full, r_claimed=round(r_c, 3), r_full=round(r_all, 3),
               n_claimed=len(claimed), n_full=len(freepool),
               claimed_missing_from_pool=len(claimed_missing), claimed_seen=claimed_seen),
          open(os.path.join(OUT, 'RT1_summary.json'), 'w'), indent=1)
with open(os.path.join(OUT, 'RT1_free_pool_rows.csv'), 'w', newline='') as fh:
    wtr = csv.DictWriter(fh, fieldnames=list(freepool[0].keys()))
    wtr.writeheader()
    wtr.writerows(freepool)
print(f'\nwrote {OUT}/RT1_summary.json and RT1_free_pool_rows.csv')
