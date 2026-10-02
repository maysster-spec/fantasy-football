"""RIVAL NEED versus THE MAN HIMSELF -- doc 314, and it kills a model before it was built.

Matt, 2026-09-15: "If a player has significant value anyway, very unlikely someone doesn't put in
a claim because everyone tends to have players they would shed for that anyway."

Doc 254 wrote the falsifier down BEFORE any of this ran: a positional-hole flag had to add 0.30
expected filers over a plain "how popular is this man" baseline, or the honest answer was to rank
by value and stop. This script is what tested it.

WHAT IT MEASURES
  POPULATION   every WAIVER-type filing in this league 2022-2025, grouped by (week, player).
               787 player-weeks, 225 of them contested. Excludes D/ST (193) and K (70), which is
               263 of the 787 and the most churned lane in the league (0.6) -- the D/ST version is
               a separate run and is NOT YET RUN. Excludes week-1 filings (19), which have no
               prior game to read.
  OUTCOME      how many of the twelve teams filed on that man in that run.
  PREDICTOR A  what he had DONE: targets + carries, and half-PPR points, in his last game.
  PREDICTOR B  positional need -- how often that rival had filed at that position in the prior
               three weeks. This is REVEALED need, read off the same object as the outcome, so it
               is rigged in B's favour. It still fails.

WHAT IT NEEDS
  Source\\waiver_report_2022..2025.csv   (in the repo)
  Source\\draft_history_2021_2025.csv    (in the repo)
  nflverse stats_player_week_2021..2025.csv and players.csv -- downloaded to a cache beside this
  script, ALWAYS re-fetched, never served stale (the build_form.py lesson, doc 309).

DEPENDENCIES: standard library plus numpy. No scipy, no sklearn, no pandas -- 0.4, because three
scripts have already died on Matt's machine for wanting something my container happened to have.

  py research\\rival_need.py
"""
import collections
import csv
import json
import math
import os
import random
import re
import sys
import unicodedata
import urllib.request

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))          # never the shell's cwd (0.4)
ROOT = os.path.dirname(HERE)
SRC = os.path.join(os.path.dirname(ROOT), 'Source')
CACHE = os.path.join(HERE, '_nflverse_cache')
BASE = 'https://github.com/nflverse/nflverse-data/releases/download'
SEASONS = (2022, 2023, 2024, 2025)
LOOKBACK = 3            # weeks of revealed need
BAR = 0.30              # doc 254's falsifier, fixed before the test


def fetch(name, url):
    """ALWAYS re-fetch. A cached file is a LAST RESORT and says so out loud, because the silent
    reuse of a partial download is what built form_2026.csv from twenty of thirty-two clubs."""
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, name)
    try:
        with urllib.request.urlopen(url, timeout=300) as fh:
            body = fh.read()
        if len(body) < 100000:
            raise ValueError(f'the feed returned only {len(body)} bytes')
        with open(p, 'wb') as out:
            out.write(body)
        return p
    except Exception as exc:
        if os.path.exists(p) and os.path.getsize(p) > 100000:
            print(f'  WARNING: could not fetch {name} ({exc}); using the cached copy, which is '
                  f'from {os.path.getmtime(p)} -- the numbers below may be stale')
            return p
        sys.exit(f'FAILED to fetch {name}: {exc}')


def nk(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode()
    s = re.sub(r'\b(jr|sr|ii|iii|iv|v)\b', '', s.lower())
    return re.sub(r'[^a-z]', '', s)


def corr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.std() == 0 or b.std() == 0:
        return float('nan')
    return float(((a - a.mean()) * (b - b.mean())).mean() / (a.std() * b.std()))


def logit(X, y, iters=400, lr=0.5):
    """Plain gradient-descent logistic. Standardised inside so the step size behaves; coefficients
    are returned on the ORIGINAL scale so they can be read."""
    X = np.asarray(X, float)
    mu, sd = X.mean(0), np.where(X.std(0) == 0, 1.0, X.std(0))
    Z = np.column_stack([np.ones(len(X)), (X - mu) / sd])
    w = np.zeros(Z.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-Z @ w))
        w -= lr * (Z.T @ (p - y)) / len(y)
    beta = w[1:] / sd
    return float(w[0] - (w[1:] * mu / sd).sum()), beta


def predict(a, beta, X):
    return 1 / (1 + np.exp(-(a + np.asarray(X, float) @ beta)))


def main():
    # ---- 1. the filings ----------------------------------------------------------------------
    filings = []
    for yr in SEASONS:
        f = os.path.join(SRC, f'waiver_report_{yr}.csv')
        if not os.path.exists(f):
            sys.exit(f'missing {f}')
        # THE YEAR COMES FROM THE BASENAME. Reading it off the full path matched the "2026" in
        # G:\My Drive\_Fantasy\2026\Source and silently dropped every row (doc 314's own first run).
        assert re.search(r'(\d{4})', os.path.basename(f)).group(1) == str(yr)
        for row in csv.DictReader(open(f, newline='', encoding='utf-8-sig')):
            m = re.search(r'ADD Player ID (-?\d+)', row['Transaction'])
            if not m:
                continue
            # BOTH TYPES ARE READ, AND THEY ARE USED FOR DIFFERENT THINGS. The contest analysis is
            # WAIVER rows only, because a free-agent add is not a claim and nobody competes for it.
            # But section 7's "was he free the whole time" needs EVERY executed add, waiver and free
            # agent alike: reading waivers only made a man added off free agency in week 3 look
            # like he had sat untouched, and it moved that headline from 33% to 46%.
            filings.append(dict(season=yr, week=int(row['Week']), team=row['Team'],
                                pid=m.group(1), status=row['Status'], kind=row['Type']))
    waivers = [f for f in filings if f['kind'] == 'WAIVER']
    print(f'transactions 2022-2025: {len(filings)}, of them WAIVER claims: {len(waivers)}')
    if len(waivers) < 1000:
        sys.exit(f'only {len(waivers)} waiver claims -- that is not this league, stop')

    # ---- 2. espn id -> nflverse ---------------------------------------------------------------
    emap = {}
    for r in csv.DictReader(open(fetch('players.csv', f'{BASE}/players/players.csv'),
                                 newline='', encoding='utf-8')):
        e = (r.get('espn_id') or '').strip()
        if not e:
            continue
        emap[e[:-2] if e.endswith('.0') else e] = (r['gsis_id'], r['display_name'],
                                                   r.get('position') or '')
    ids = {f['pid'] for f in filings if not f['pid'].startswith('-')}
    missed = [i for i in ids if i not in emap]
    print(f'espn ids resolved: {len(ids) - len(missed)} of {len(ids)}'
          + (f'   MISSED {missed}' if missed else ''))
    if len(missed) > 0.05 * len(ids):
        sys.exit('more than 5% of ids did not resolve -- the join is broken, not the data (3)')

    # ---- 3. weekly form -----------------------------------------------------------------------
    want = {emap[i][0] for i in ids if i in emap}
    form = collections.defaultdict(dict)
    for yr in SEASONS:
        f = fetch(f'stats_player_week_{yr}.csv',
                  f'{BASE}/stats_player/stats_player_week_{yr}.csv')
        for r in csv.DictReader(open(f, newline='', encoding='utf-8')):
            if r.get('season_type') != 'REG' or r['player_id'] not in want:
                continue
            g = lambda k: float(r.get(k) or 0)
            form[(yr, r['player_id'])][int(r['week'])] = dict(
                half=g('fantasy_points') + 0.5 * g('receptions'),
                touch=g('targets') + g('carries'))

    # ---- 4. one row per player-week -----------------------------------------------------------
    who = collections.defaultdict(set)
    for f in waivers:
        who[(f['season'], f['week'], f['pid'])].add(f['team'])
    rows, skip = [], collections.Counter()
    for (s, w, pid), teams in who.items():
        if pid.startswith('-'):
            skip['D/ST'] += 1
            continue
        info = emap.get(pid)
        if not info or info[2] not in ('QB', 'RB', 'WR', 'TE'):
            skip['K or unresolved'] += 1
            continue
        if w < 2:
            skip['week 1, no prior game'] += 1
            continue
        prior = {k: v for k, v in form[(s, info[0])].items() if k < w}
        if not prior:
            skip['no prior game played'] += 1
            continue
        last = prior[max(prior)]
        rows.append(dict(season=s, week=w, pid=pid, name=info[1], pos=info[2],
                         filers=len(teams), touch=last['touch'], pts=last['half']))
    print(f'\nplayer-weeks: {len(who)} filed on, {len(rows)} in the population, '
          f'excluded {dict(skip)}')
    core = [r for r in rows if r['pos'] != 'QB']      # a QB's targets+carries is not his workload

    # ---- 5. PREDICTOR A ------------------------------------------------------------------------
    print(f'\n--- A: what he had done. RB/WR/TE, n={len(core)} ---')
    y = [float(r['filers']) for r in core]
    rt, rp = corr([r['touch'] for r in core], y), corr([r['pts'] for r in core], y)
    print(f'  r(last-game touches, filers) = {rt:+.3f}')
    print(f'  r(last-game points,  filers) = {rp:+.3f}')
    random.seed(7)
    z, hits, N = list(y), 0, 20000
    for _ in range(N):
        random.shuffle(z)
        if abs(corr([r['touch'] for r in core], z)) >= abs(rt):
            hits += 1
    print(f'  permutation p on touches = {(hits + 1) / (N + 1):.5f}  (N={N})')
    print('\n  touches last game   n   filers  contested')
    bands = []
    for lo, hi, lab in [(0, 5, 'under 5'), (5, 10, '5 to 9'),
                        (10, 15, '10 to 14'), (15, 1e9, '15 or more')]:
        ch = [r for r in core if lo <= r['touch'] < hi]
        c = sum(1 for r in ch if r['filers'] > 1) / len(ch)
        print(f'  {lab:18s}{len(ch):4d}   {sum(r["filers"] for r in ch) / len(ch):.2f}    {c:.0%}')
        bands.append(dict(lo=lo, hi=(999 if hi > 900 else hi), label=lab, n=len(ch),
                          filers=round(sum(r['filers'] for r in ch) / len(ch), 2),
                          contested=round(c, 2)))
    print('\n  and points add nothing once the workload is known:')
    for lab, sel in [('12+ pts, 10+ touch', lambda r: r['pts'] >= 12 and r['touch'] >= 10),
                     ('12+ pts, <10 touch', lambda r: r['pts'] >= 12 and r['touch'] < 10),
                     ('<12 pts, 10+ touch', lambda r: r['pts'] < 12 and r['touch'] >= 10),
                     ('<12 pts, <10 touch', lambda r: r['pts'] < 12 and r['touch'] < 10)]:
        ch = [r for r in core if sel(r)]
        print(f'  {lab:20s} n={len(ch):4d}  filers {sum(r["filers"] for r in ch) / len(ch):.2f}')

    # ---- 6. PREDICTOR B, and doc 254's falsifier ----------------------------------------------
    season_teams = collections.defaultdict(set)
    by_tp, by_t = collections.defaultdict(list), collections.defaultdict(list)
    for f in waivers:
        season_teams[f['season']].add(f['team'])
        pos = emap.get(f['pid'], (None, None, 'D/ST' if f['pid'].startswith('-') else '?'))[2]
        by_tp[(f['season'], f['team'], pos)].append(f['week'])
        by_t[(f['season'], f['team'])].append(f['week'])
    dec = []
    for r in rows:
        filed = who[(r['season'], r['week'], r['pid'])]
        for t in season_teams[r['season']]:
            dec.append((r['touch'],
                        sum(1 for w in by_t[(r['season'], t)]
                            if r['week'] - LOOKBACK <= w < r['week']),
                        sum(1 for w in by_tp[(r['season'], t, r['pos'])]
                            if r['week'] - LOOKBACK <= w < r['week']),
                        1 if t in filed else 0,
                        (r['season'], r['week'], r['pid']), r['season']))
    X = np.array([[d[0], d[1], d[2]] for d in dec], float)
    yy = np.array([d[3] for d in dec], float)
    a, b = logit(X, yy)
    print(f'\n--- B: does positional need add anything? n={len(dec)} team-decisions ---')
    print(f'  coefficients  touches {b[0]:+.4f}   team activity {b[1]:+.4f}   POSITIONAL NEED {b[2]:+.4f}')
    Xz = X.copy()
    Xz[:, 2] = 0
    d_real, d_zero = collections.Counter(), collections.Counter()
    for d, pr, pz in zip(dec, predict(a, b, X), predict(a, b, Xz)):
        d_real[d[4]] += pr
        d_zero[d[4]] += pz
    delta = np.array([d_real[k] - d_zero[k] for k in d_real])
    print(f'  it moves expected filers per player-week by mean {delta.mean():+.3f} '
          f'(median {np.median(delta):+.3f}, max {delta.max():+.3f})')
    print(f"  doc 254's bar, fixed before the test: {BAR:.2f}  -->  "
          + ('CLEARS' if abs(delta.mean()) >= BAR else 'FAILS, do not build the rival model'))
    print('\n  leave-one-season-out, predicting the filer COUNT (mean absolute error):')
    ss = np.array([d[5] for d in dec])
    for lab, cols in [('workload only', [0]), ('+ team activity', [0, 1]),
                      ('+ POSITIONAL NEED', [0, 1, 2])]:
        errs = []
        for s in SEASONS:
            tr, te = ss != s, ss == s
            aa, bb = logit(X[tr][:, cols], yy[tr])
            got = collections.Counter()
            act = {}
            for d, q in zip([d for d, m in zip(dec, te) if m], predict(aa, bb, X[te][:, cols])):
                got[d[4]] += q
                act[d[4]] = act.get(d[4], 0) + d[3]
            errs += [abs(got[k] - act[k]) for k in got]
        print(f'    {lab:20s} MAE {np.mean(errs):.3f}')

    # ---- 7. does value ever sit? ---------------------------------------------------------------
    drafted = collections.defaultdict(set)
    dh = os.path.join(SRC, 'draft_history_2021_2025.csv')
    for r in csv.DictReader(open(dh, newline='', encoding='utf-8-sig')):
        drafted[int(r['Year'])].add(nk(r['Player']))
    first_add = collections.defaultdict(lambda: 99)
    for f in filings:
        if f['status'] == 'EXECUTED':
            k = (f['season'], f['pid'])
            first_add[k] = min(first_add[k], f['week'])
    sat = []
    for r in core:
        g = form[(r['season'], emap[r['pid']][0])]
        big = [k for k in sorted(g) if k < r['week'] and g[k]['touch'] >= 10]
        if not big:
            continue
        if nk(r['name']) in drafted.get(r['season'], set()):
            continue
        if first_add[(r['season'], r['pid'])] < r['week']:
            continue
        sat.append((r, r['week'] - big[0]))
    late = [x for x in sat if x[1] >= 2]
    print(f'\n--- does a valuable man ever sit? ---')
    print(f'  {len(sat)} men had a 10+ touch game while provably undrafted and never rostered.')
    print(f'  {len(late)} of them ({len(late) / max(1, len(sat)):.0%}) went at least one MORE full '
          f'week before anybody filed.')
    for r, lag in sorted(late, key=lambda x: -x[1])[:8]:
        print(f'    {r["season"]} {r["name"]:22s} {r["pos"]}  first 10+ touch game to claim: '
              f'{lag} weeks, then {r["filers"]} filer(s)')
    print('\n  NOTE the direction of the bias: this joins to the draft list BY NAME (3 forbids it '
          'where an id exists; none does here). A man I fail to match reads as free when he was '
          'rostered, which inflates the count above, not deflates it.')

    out = os.path.join(HERE, 'rival_need_bands.json')
    json.dump(dict(bands=bands, r=round(rt, 3), n=len(core),
                   need_delta=round(float(delta.mean()), 3), bar=BAR), open(out, 'w'), indent=1)
    print(f'\nwrote {out} -- paste the bands into Source\\sheet_constants.json if they move')


if __name__ == '__main__':
    main()
