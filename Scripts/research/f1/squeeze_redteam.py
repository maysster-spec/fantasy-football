#!/usr/bin/env python3
r"""squeeze_redteam.py -- the red team of doc 299's arrival squeeze.

Drop beside squeeze.py in Scripts\research\f1\. Reads stats_player_week_<season>.csv
from its own folder (override with WK1_DATA). Stdlib only. Python 3.12 safe.

DOC 299 AS PUBLISHED: team-seasons with a 60+ target incumbent still on the team.
TREATMENT = a 60+ target receiver from ANOTHER team is now here. OUTCOME = each
man's share of his team's receiver targets, per game played, this season minus last.
ROOM BELOW = 3rd and 4th by LAST season's targets.

WHAT THIS ADDS

  1  THE PLACEBO. Run the identical test on the 2nd receiver, where doc 299's
     claim predicts nothing in particular. If the 2nd man is hit as hard as the
     3rd and 4th, "the room below" is not the thing being measured.
  2  A SECOND NULL. Doc 299 permutes the arrival label within TEAM. Permute it
     within SEASON instead and see whether the p-value depends on the choice.
  3  THE DENOMINATOR. A share is a share of 100%. Adding a target-earner drops
     every incumbent share arithmetically, whether or not anybody is squeezed.
     Recompute every share over the HOLDOVER POOL only -- the men on the team in
     both seasons, arrival excluded from numerator and denominator, the same men
     on both sides of the difference. If the 3rd and 4th still lose ground
     relative to their own teammates, the squeeze is real. If it vanishes,
     doc 299 measured dilution.

Run:  py squeeze_redteam.py
      py squeeze_redteam.py --years 2021 2022 2023 2024 2025
"""
import collections, csv, os, random, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get('WK1_DATA', HERE)
MING = 4
INCUMBENT_TARGETS = 60


def find_seasons():
    out = []
    for fn in os.listdir(DATA):
        if fn.startswith('stats_player_week_') and fn.endswith('.csv'):
            try:
                out.append(int(fn[18:22]))
            except ValueError:
                pass
    return sorted(out)


def agg(season):
    """(team, pid) -> [targets, games] for WRs, regular season."""
    out = collections.defaultdict(lambda: [0.0, 0])
    path = os.path.join(DATA, f'stats_player_week_{season}.csv')
    with open(path, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            if (r.get('season_type') or 'REG') != 'REG' or r.get('position') != 'WR':
                continue
            k = (r['team'], r['player_id'])
            out[k][0] += float(r.get('targets') or 0)
            out[k][1] += 1
    return out


def shares(pool, keys):
    rates = {p: pool[p][0] / pool[p][1] for p in keys if pool[p][1] > 0}
    tot = sum(rates.values())
    return {p: (v / tot if tot else 0.0) for p, v in rates.items()}


def build(seasons, holdover_only):
    A = {s: agg(s) for s in seasons + [min(seasons) - 1]}
    recs = []
    for s in seasons:
        prev, cur = A[s - 1], A[s]
        cur_t, prev_t = collections.defaultdict(dict), collections.defaultdict(dict)
        for (tm, pid), v in cur.items():
            cur_t[tm][pid] = v
        for (tm, pid), v in prev.items():
            prev_t[tm][pid] = v
        best = {}
        for (tm, pid), (t, g) in prev.items():
            if pid not in best or t > best[pid][1]:
                best[pid] = (tm, t, g)
        for tm, roster in cur_t.items():
            pt = prev_t.get(tm, {})
            if not [p for p in roster if pt.get(p, (0, 0))[0] >= INCUMBENT_TARGETS]:
                continue
            arr = [p for p in roster
                   if p not in pt and best.get(p, ('', 0, 0))[1] >= INCUMBENT_TARGETS]
            if holdover_only:
                # SAME men in the denominator on both sides, or the difference is
                # just the denominator changing size.
                keys_cur = [p for p in roster if p in pt]
                keys_prev = keys_cur
                if len(keys_cur) < 3:
                    continue
            else:
                keys_cur = list(roster)
                keys_prev = list(pt)
            sp, sc = shares(pt, keys_prev), shares(roster, keys_cur)
            order = [p for p, _ in sorted(pt.items(), key=lambda kv: -kv[1][0])
                     if p in sc]

            def d(i):
                if i > len(order):
                    return None
                p = order[i - 1]
                if pt[p][1] < MING or roster[p][1] < MING:
                    return None
                return sc[p] - sp[p]

            recs.append(dict(season=s, team=tm, arrival=1 if arr else 0,
                             s1=d(1), s2=d(2), s3=d(3), s4=d(4)))
    return recs


def vals(recs, which, arr):
    out = []
    for r in recs:
        if r['arrival'] != arr:
            continue
        for k in (('s3', 's4') if which == '34' else (which,)):
            if r[k] is not None:
                out.append(r[k])
    return out


def diff(recs, which):
    a, b = vals(recs, which, 1), vals(recs, which, 0)
    if not a or not b:
        return None
    return statistics.mean(a) - statistics.mean(b), statistics.mean(a), \
        statistics.mean(b), len(a), len(b)


def permute(recs, which, by, reps=4000, seed=20260913):
    rng = random.Random(seed)
    o = diff(recs, which)
    if not o:
        return None
    groups = collections.defaultdict(list)
    for r in recs:
        groups[r[by]].append(r)
    hits = 0
    for _ in range(reps):
        shuf = []
        for _k, rs in groups.items():
            labs = [r['arrival'] for r in rs]
            rng.shuffle(labs)
            for r, l in zip(rs, labs):
                d2 = dict(r)
                d2['arrival'] = l
                shuf.append(d2)
        e = diff(shuf, which)
        if e and e[0] <= o[0]:
            hits += 1
    return o, hits / reps


SLOTS = [('s1', '1st, the incumbent'), ('s2', '2nd  <-- PLACEBO'),
         ('s3', '3rd alone'), ('s4', '4th alone'), ('34', '3rd + 4th (doc 299)')]


def report(recs, title):
    nt = sum(r['arrival'] for r in recs)
    print(f'\n{title}')
    print(f'  {len(recs)} team-seasons, treatment {nt}, control {len(recs)-nt}')
    print(f"  {'slot':22}{'arrival':>10}{'none':>10}{'diff':>10}"
          f"{'p by team':>12}{'p by season':>13}   n")
    for which, lab in SLOTS:
        wt = permute(recs, which, 'team')
        ws = permute(recs, which, 'season')
        if not wt:
            print(f'  {lab:22}  no data')
            continue
        (d, a, b, na, nb), p1 = wt
        _, p2 = ws
        print(f'  {lab:22}{a:>+10.4f}{b:>+10.4f}{d:>+10.4f}'
              f'{p1:>12.4f}{p2:>13.4f}   {na}/{nb}')


def main(argv):
    seasons = [s for s in find_seasons() if s >= 2021]
    if '--years' in argv:
        seasons = [int(x) for x in argv[argv.index('--years') + 1:] if x.isdigit()]
    print(f'seasons used: {seasons}   (p-values one-sided, in his direction)')
    report(build(seasons, False),
           'DESIGN 1 -- DOC 299 AS PUBLISHED: share of ALL team WR targets')
    report(build(seasons, True),
           'DESIGN 2 -- HOLDOVER POOL: the arrival is out of the denominator, so\n'
           '            only a real reallocation between the men already here can show')
    print('\nREAD IT LIKE THIS. Design 1 answers "did his slice of the pie shrink",\n'
          'and adding a man who eats guarantees that for everyone. Design 2 answers\n'
          '"did the arrival take more from the bottom than from the top", which is\n'
          'the claim. Where the two disagree, design 2 is the one about the mechanism.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
