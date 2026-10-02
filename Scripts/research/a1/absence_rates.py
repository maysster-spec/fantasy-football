#!/usr/bin/env python3
r"""absence_rates.py -- A1 step 1: how often does a STARTER-QUALITY player miss a week?

POPULATION, and it is chosen to avoid selecting on the season being measured: for season t, the
players who finished top-24 at RB, top-24 at WR, top-12 at QB and top-12 at TE in season t-1 by
half-PPR points over that season's weeks 1-14. Their availability is then read in season t. Nothing
about season t enters the population.

BASELINE / DENOMINATOR: his team's weeks 1-14 that were actually played, so the team's BYE is
removed. The sheet already models byes; this measures the OTHER kind of absence.
OUTCOME: the share of those weeks with no line in the weekly file, which is "he did not play".

Source: nflverse stats_player_week_<season>.csv, 2021-2025, regular season only.
Stdlib only.
"""
import collections, csv, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get('A1_DATA', HERE)
SEASONS = [2021, 2022, 2023, 2024, 2025]
WEEKS = range(1, 15)
TOPN = {'RB': 24, 'WR': 24, 'QB': 12, 'TE': 12, 'K': 12}


def half_ppr(r):
    g = lambda k: float(r.get(k) or 0)
    return (0.04 * g('passing_yards') + 6 * g('passing_tds') - 2 * g('passing_interceptions')
            + 0.1 * g('rushing_yards') + 6 * g('rushing_tds')
            + 0.1 * g('receiving_yards') + 6 * g('receiving_tds') + 0.5 * g('receptions'))


def load(season):
    p = os.path.join(DATA, f'stats_player_week_{season}.csv')
    rows = []
    with open(p, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            if (r.get('season_type') or 'REG') != 'REG':
                continue
            try:
                w = int(r['week'])
            except (TypeError, ValueError):
                continue
            if w not in WEEKS:
                continue
            rows.append(r)
    return rows


def main():
    per_season = {s: load(s) for s in SEASONS}
    # team -> weeks actually played (the complement inside 1-14 is the bye)
    team_weeks = {s: collections.defaultdict(set) for s in SEASONS}
    played = {s: collections.defaultdict(set) for s in SEASONS}     # player -> weeks with a line
    pos = {s: {} for s in SEASONS}
    team_of = {s: {} for s in SEASONS}
    pts = {s: collections.Counter() for s in SEASONS}
    name = {}
    for s in SEASONS:
        for r in per_season[s]:
            pid, w = r['player_id'], int(r['week'])
            team_weeks[s][r['team']].add(w)
            played[s][pid].add(w)
            pos[s][pid] = r.get('position') or ''
            team_of[s][pid] = r['team']
            pts[s][pid] += half_ppr(r)
            name[pid] = r.get('player_display_name') or r.get('player_name') or pid

    out = collections.defaultdict(list)
    rows_used = 0
    for i in range(1, len(SEASONS)):
        prev, cur = SEASONS[i - 1], SEASONS[i]
        by_pos = collections.defaultdict(list)
        for pid, p in pos[prev].items():
            if p in TOPN:
                by_pos[p].append((pts[prev][pid], pid))
        for p, lst in by_pos.items():
            lst.sort(reverse=True)
            for _, pid in lst[:TOPN[p]]:
                if pid not in team_of[cur]:
                    # not in the league at all the next season: a different event (cut, retired,
                    # not signed). Excluded and COUNTED, because excluding it silently would be
                    # the survivorship trap this project keeps meeting.
                    out['_gone_' + p].append((cur, name.get(pid, pid)))
                    continue
                tm = team_of[cur][pid]
                elig = team_weeks[cur][tm] & set(WEEKS)
                if not elig:
                    continue
                miss = len(elig - played[cur][pid])
                out[p].append((miss, len(elig), cur, name.get(pid, pid)))
                rows_used += 1

    print(f'A1 step 1 -- weekly absence among prior-season starters, weeks 1-14')
    print(f'seasons measured: {SEASONS[1]}-{SEASONS[-1]} ({len(SEASONS)-1} transitions), '
          f'{rows_used} player-seasons\n')
    print(f"{'pos':<5}{'n':>5}{'miss/season':>13}{'weekly absence':>16}{'played all':>12}"
          f"{'3+ missed':>11}   gone from the league")
    summary = {}
    for p in ('QB', 'RB', 'WR', 'TE', 'K'):
        rec = out.get(p, [])
        if not rec:
            continue
        tot_miss = sum(m for m, e, _, _ in rec)
        tot_elig = sum(e for m, e, _, _ in rec)
        rate = tot_miss / tot_elig
        allin = sum(1 for m, e, _, _ in rec if m == 0) / len(rec)
        three = sum(1 for m, e, _, _ in rec if m >= 3) / len(rec)
        gone = len(out.get('_gone_' + p, []))
        summary[p] = rate
        print(f'{p:<5}{len(rec):>5}{tot_miss/len(rec):>13.2f}{rate:>15.1%}{allin:>12.0%}'
              f'{three:>11.0%}   {gone}')
    print('\nPER-SEASON, to show it is not one year:')
    for p in ('QB', 'RB', 'WR', 'TE'):
        by_year = collections.defaultdict(lambda: [0, 0])
        for m, e, cur, _ in out.get(p, []):
            by_year[cur][0] += m
            by_year[cur][1] += e
        print(' ', p, ' '.join(f'{y}:{a/b:.0%}' for y, (a, b) in sorted(by_year.items())))
    print('\nCHECK AGAINST doc 111 [INHERITED]: a drafted starting QB missing 2.98 weeks a season, '
          f'measured here at {sum(m for m,_,_,_ in out["QB"])/len(out["QB"]):.2f}.')
    import json
    json.dump({p: round(v, 4) for p, v in summary.items()},
              open(os.path.join(HERE, 'absence_rates.json'), 'w'), indent=1)
    print('\nwrote absence_rates.json')


if __name__ == '__main__':
    main()
