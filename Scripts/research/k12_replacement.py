"""k12_replacement.py -- the kicker replacement level, measured the way D/ST12 was (doc 265).

WHY. The week sheet's drop table could not price a kicker. Section 4.8 and 4.9 keep K off the wire,
so there was no free row to price against, and the row printed `not priced` -- which Matt read, correctly,
as "this man is free to drop":

    "Who am i replacing my kicker with? ... If i drop my kicker i'm not going to gain 1.8 points, lol."

Doc 420 replaced the blank with an honest sentence and left the number NOT ESTABLISHED, on the grounds
that inventing one is worse than admitting the gap (0.2). This measures it instead.

THE POPULATION, stated here and not inherited (0.6):
    nflverse weekly, seasons 2021-2025, season_type REG, position K
    weeks 1 to 14 only -- this league's regular season ends at 14 (section 2)
    a kicker counts as rosterable with 8 or more games in that window, which is 29 to 31 men a year
    scored under THIS LEAGUE'S rules, from 2026_League_Settings.txt via section 2:
        PAT made        +1
        FG 0-39         +3
        FG 40-49        +4
        FG 50+          +5
        FG missed       -1
    (a missed PAT is NOT penalised in these settings; only a missed field goal is)

REPLACEMENT is K12's season average, ranked by season TOTAL, exactly as doc 265 ranked D/ST12.

    py k12_replacement.py

Standard library only (doc 144); paths resolve against this file, never the shell.
"""
import collections
import csv
import os
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, '_nflverse_cache')
SEASONS = (2021, 2022, 2023, 2024, 2025)
LAST_WEEK = 14
MIN_GAMES = 8


def _f(v):
    try:
        return float(v or 0)
    except (TypeError, ValueError):
        return 0.0


def week_points(r):
    """This league's kicker scoring, applied to one nflverse week."""
    return (_f(r['pat_made']) * 1.0
            + (_f(r['fg_made_0_19']) + _f(r['fg_made_20_29']) + _f(r['fg_made_30_39'])) * 3.0
            + _f(r['fg_made_40_49']) * 4.0
            + (_f(r['fg_made_50_59']) + _f(r['fg_made_60_'])) * 5.0
            - _f(r['fg_missed']) * 1.0)


def season_table(yr):
    tot, games = collections.defaultdict(float), collections.Counter()
    path = os.path.join(CACHE, f'stats_player_week_{yr}.csv')
    if not os.path.exists(path):
        raise SystemExit(f'missing {path} -- build the nflverse cache first')
    with open(path, newline='', encoding='utf-8', errors='replace') as fh:
        for r in csv.DictReader(fh):
            if r.get('season_type') != 'REG' or r.get('position') != 'K':
                continue
            try:
                wk = int(r.get('week') or 0)
            except ValueError:
                continue
            if not 1 <= wk <= LAST_WEEK:
                continue
            n = r['player_display_name']
            tot[n] += week_points(r)
            games[n] += 1
    per = {n: (tot[n] / games[n], games[n]) for n in tot if games[n] >= MIN_GAMES}
    return sorted(per.items(), key=lambda kv: -kv[1][0] * kv[1][1])   # by season TOTAL


def main():
    print(f'  kicker replacement, this league\'s scoring, weeks 1-{LAST_WEEK}, '
          f'{MIN_GAMES}+ games:')
    k12s = []
    for yr in SEASONS:
        rank = season_table(yr)
        if len(rank) <= 11:
            print(f'  {yr}: only {len(rank)} rosterable kickers, skipped')
            continue
        k1, k12 = rank[0], rank[11]
        k12s.append(k12[1][0])
        print(f'  {yr}: {len(rank):>2} kickers | K1 {k1[1][0]:5.2f}/wk ({k1[0]}) '
              f'| K12 {k12[1][0]:5.2f}/wk ({k12[0]})')
    if not k12s:
        return 2
    print()
    print(f'  K12 by season: {[round(x, 2) for x in k12s]}')
    print(f'  REPLACEMENT = {st.mean(k12s):.2f} a week, sd {st.pstdev(k12s):.2f}, '
          f'n={len(k12s)} seasons')
    print(f'  (doc 265 measured D/ST12 the same way at 5.99 a week on a file short 142 team-weeks; doc 441 re-measured it at 5.51 on all 2,718)')
    print()
    print(f'  WHAT IT IS FOR: a kicker\'s drop cost is his rate minus this, because the slot is')
    print(f'  mandatory and what replaces him is another kicker. It is NOT a weekly number -- a')
    print(f'  kicker\'s week is his matchup and his leg, and this says nothing about either.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
