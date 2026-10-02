#!/usr/bin/env python3
r"""wk1_redteam2.py -- third reader on doc 300, answering doc 302.

Runs beside wk1_redteam.py in the same folder and reads the same
stats_player_week_<season>.csv files (override with WK1_DATA).
Stdlib only. Python 3.11 and 3.12 safe. Writes nothing.

WHAT IT ADDS TO wk1_redteam.py:

  F  THE CUT NEITHER DOC RAN: claimable AND the labels held, at once.
     Doc 302's E1 kills the startable half; its own D1 strengthens it.
     They are not the same objection and only the intersection separates them.
  G  THE TIE-BREAK, SIZED. Doc 302 counts nine rows "at 45% or above" as
     exposed to the player-id tie-break. The sort is on (work, player_id), so
     the id decides only on an EXACT tie. Count the exact ties and re-run the
     whole table with the tie broken the other way.
  H  OUTCOME KEYED ON (team, player_id), so a traded second back does not
     carry his new team's points into the outcome.

  Every variant builder is proved against wk1_redteam.build() on the default
  settings BEFORE its result is read (directive 5.5: build the real object).
"""
import collections, os, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wk1_redteam as W


def build2(seasons, tie='id', team_key=False):
    """wk1_redteam.build() with two switches.

    tie='id'   -- the shipped behaviour: sort on (work, player_id) descending
    tie='rev'  -- break an EXACT tie the other way
    team_key   -- score the second back on (team, player_id), not player_id
    """
    recs = []
    for s in seasons:
        wk1 = collections.defaultdict(list)
        rest = collections.defaultdict(lambda: [0.0, 0])
        prior = collections.defaultdict(lambda: [0.0, 0])
        work214 = collections.defaultdict(lambda: collections.defaultdict(float))
        team_weeks = collections.defaultdict(set)
        pl_weeks = collections.defaultdict(set)
        name = {}
        for r in W.load(s):
            team_weeks[r['team']].add(r['_w'])
            if r.get('position') != 'RB':
                continue
            pid = r['player_id']
            key = (r['team'], pid) if team_key else pid
            name[pid] = r.get('player_display_name') or pid
            pl_weeks[pid].add(r['_w'])
            if r['_w'] == 1:
                wk1[r['team']].append(
                    (float(r.get('carries') or 0) + float(r.get('targets') or 0), pid))
            elif 2 <= r['_w'] <= 14:
                rest[key][0] += W.half_ppr(r)
                rest[key][1] += 1
                work214[r['team']][pid] += (float(r.get('carries') or 0)
                                            + float(r.get('targets') or 0))
        try:
            for r in W.load(s - 1):
                if r.get('position') == 'RB' and 1 <= r['_w'] <= 14:
                    prior[r['player_id']][0] += W.half_ppr(r)
                    prior[r['player_id']][1] += 1
        except FileNotFoundError:
            prior = None

        for tm, lst in wk1.items():
            lst.sort(reverse=True)
            if len(lst) < 2:
                continue
            tot = sum(u for u, _ in lst)
            if tot < 10:
                continue
            (u1, p1), (u2, p2) = lst[0], lst[1]
            exact_tie = (u1 == u2)
            if exact_tie and tie == 'rev':
                (u1, p1), (u2, p2) = (u2, p2), (u1, p1)
            k2 = (tm, p2) if team_key else p2
            if u1 <= 0 or u2 <= 0 or rest[k2][1] < 4:
                continue
            played = {w for w in team_weeks[tm] if 2 <= w <= 14}
            w2 = work214[tm]
            leader214 = max(w2, key=w2.get) if w2 else None
            pr = prior[p2] if prior is not None else None
            recs.append(dict(
                season=s, tm=tm, rb1=name[p1], rb2=name[p2],
                share=u2 / tot, ppg=rest[k2][0] / rest[k2][1],
                hit=1 if rest[k2][0] / rest[k2][1] >= W.RB_REPL else 0,
                lead_missed=len(played - pl_weeks[p1]),
                lead_kept_lead=(leader214 == p1),
                prior_ppg=(pr[0] / pr[1] if pr and pr[1] >= 4 else None),
                exact_tie=exact_tie))
    return recs


def sig(recs):
    return sorted((r['season'], r['tm'], r['rb2'], round(r['share'], 6),
                   round(r['ppg'], 6), r['hit']) for r in recs)


def main(argv):
    seasons = W.find_seasons()
    if '--years' in argv:
        seasons = [int(x) for x in argv[argv.index('--years') + 1:] if x.isdigit()]
    seasons = [s for s in seasons if s >= 2021]
    print(f'seasons used: {seasons}')

    base = W.build(seasons)
    mine = build2(seasons)
    same = sig(base) == sig(mine)
    print(f'CONTROL: build2() default reproduces wk1_redteam.build() exactly: '
          f'{"YES" if same else "NO"}  ({len(base)} vs {len(mine)} rows)')
    if not same:
        print('  refusing to read the variants against a builder that does not reproduce')
        return 1

    claim = [r for r in mine if r['prior_ppg'] is None or r['prior_ppg'] < W.RB_REPL]
    kept = [r for r in mine if r['lead_kept_lead']]
    both = [r for r in claim if r['lead_kept_lead']]

    print('\nF. THE CUT NEITHER DOC RAN')
    W.table(mine, 'F0. everything (doc 300 as published)')
    W.line(mine, .35)
    W.table(claim, 'F1. claimable only (doc 302 D1) -- preseason-knowable filter')
    W.line(claim, .35)
    W.table(kept, 'F2. labels held only (doc 302 E1) -- conditions on a weeks 2-14 outcome')
    W.line(kept, .35)
    W.table(both, 'F3. CLAIMABLE **AND** LABELS HELD -- the intersection')
    W.line(both, .35)
    print(f'\n   of the {len(mine)} rows: {len(claim)} claimable, {len(kept)} labels held, '
          f'{len(both)} both.')
    lost = [r for r in claim if not r['lead_kept_lead'] and r['share'] >= .35]
    print(f'   claimable rows at 35%+ that E1 deletes: {len(lost)}, '
          f'of which startable {sum(r["hit"] for r in lost)}')
    print('   ' + '; '.join(f'{r["season"]} {r["tm"]} {r["rb2"]} {r["share"]:.0%} '
                            f'{r["ppg"]:.1f}ppg' for r in sorted(lost, key=lambda x: -x['share'])))

    print('\nG. THE TIE-BREAK, SIZED')
    ties = [r for r in mine if r['exact_tie']]
    print(f'   rows decided by the player-id string (EXACT week-1 tie): {len(ties)} of {len(mine)}')
    for r in ties:
        print(f'     {r["season"]} {r["tm"]:<4}{r["rb2"]:<22} vs {r["rb1"]:<22}'
              f'{r["ppg"]:>6.1f} ppg  {"STARTABLE" if r["hit"] else ""}')
    rev = build2(seasons, tie='rev')
    W.table(rev, 'G1. THE WHOLE TABLE WITH EXACT TIES BROKEN THE OTHER WAY')
    W.line(rev, .35)

    print('\nH. OUTCOME KEYED ON (team, player_id), so a traded RB2 does not carry new-team points')
    tk = build2(seasons, team_key=True)
    moved = [(a, b) for a, b in zip(sig(mine), sig(tk)) if a != b] if len(tk) == len(mine) else None
    print(f'   rows: {len(tk)} against {len(mine)}; '
          f'rows whose outcome changed: {"n/a (row count differs)" if moved is None else len(moved)}')
    W.table(tk, 'H1. TEAM-KEYED OUTCOME')
    W.line(tk, .35)
    tkc = [r for r in tk if r['prior_ppg'] is None or r['prior_ppg'] < W.RB_REPL]
    W.table(tkc, 'H2. TEAM-KEYED **AND** CLAIMABLE -- the strictest honest decision population')
    W.line(tkc, .35)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
