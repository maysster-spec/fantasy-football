#!/usr/bin/env python3
r"""
slate.py -- WHICH DEFENCE TO CLAIM, FOR THE WEEKS AHEAD.

    py slate.py                 the next four weeks
    py slate.py --from 12 --n 4 any window
    py slate.py --playoffs      weeks 15-17

WHY: SECTION 4.33 -- D/ST matchup is 108% of the spread between the units themselves, the only
position where the schedule beats the player. Doc 212 -- the best-to-worst spread is 3.56 points
over ONE week and 11.72 over FOUR, so the horizon roughly triples the signal. Doc 258 -- a forward
claim on a SCHEDULE is not the week-1 depth-chart bet SECTION 4.31 penalises; the schedule has been
fixed since May.

METHOD, and every number in it is measured, not assumed:
  1. 2025 D/ST points per team-week rebuilt from nflverse play-by-play under the league's OWN
     scoring (2026_League_Settings.txt lines 74-95). Reproduces doc 212: mean 5.09 v 5.10.
  2. Each OFFENCE's generosity = mean D/ST points its opponents scored against it. Swing 8.2,
     reproducing doc 212's 8.2 exactly.
  3. SHRUNK toward the league mean by doc 212's measured persistence, r = +0.325. This is the step
     that keeps it a tilt rather than a forecast -- two thirds of 2025 form does not carry.
  4. The 2026 schedule, forward. A bye week contributes the league mean, not zero.

NOT MODELLED, and doc 212 says the same: home field, 2026 roster and coaching turnover, weather,
injuries. The whole model explains about a quarter of a D/ST week. Treat the ordering as worth
roughly 0.8 points a week -- real, small, free.
"""
import argparse, csv, os, sys, collections, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
RHO_OPP = 0.325       # doc 212, an offence's generosity to opposing D/STs, year to year
RHO_DEF = 0.269       # doc 212, a defence's own quality, year to year. BOTH are weak on purpose:
                      # two thirds of 2025 does not carry, and that is why this is a tilt.

def load(p):
    return list(csv.DictReader(open(os.path.join(HERE, p), encoding='utf-8')))

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--from', dest='w0', type=int, default=2)
    ap.add_argument('--n', type=int, default=4)
    ap.add_argument('--playoffs', action='store_true')
    ap.add_argument('--season', type=int, default=2026)
    a = ap.parse_args(argv)
    w0, n = (15, 3) if a.playoffs else (a.w0, a.n)

    gen = {r['offence']: float(r['dst_pts_allowed_per_game']) for r in load('generosity_2025.csv')}
    mean = st.mean(gen.values())
    shrunk = {t: mean + RHO_OPP * (v - mean) for t, v in gen.items()}

    # THE DEFENCE'S OWN 2025 FORM, shrunk on its own measured persistence. SECTION 4.33 says the
    # schedule is the bigger half at this position -- it does not say the unit is nothing, and
    # doc 212's 11.72 carried both. Keeping them in separate columns so the split is legible.
    own = collections.defaultdict(list)
    for r in load('dst_weekly_2025.csv'):
        own[r['team']].append(float(r['dst_pts']))
    ownm = {t: st.mean(v) for t, v in own.items()}
    dmean = st.mean(ownm.values())
    dshr = {t: RHO_DEF * (v - dmean) for t, v in ownm.items()}   # a DELTA off the mean

    sched = collections.defaultdict(dict)          # team -> week -> opponent
    for g in load('sched_2026.csv'):
        if g['season'] != str(a.season) or g['game_type'] != 'REG':
            continue
        wk = int(g['week'])
        sched[g['home_team']][wk] = g['away_team']
        sched[g['away_team']][wk] = g['home_team']

    weeks = list(range(w0, w0 + n))
    out = []
    for team, byweek in sched.items():
        legs, sched_pts, byes, played = [], 0.0, [], 0
        for wk in weeks:
            o = byweek.get(wk)
            if o is None:
                byes.append(wk); sched_pts += mean; legs.append(f"w{wk} BYE")
            else:
                played += 1
                sched_pts += shrunk[o]; legs.append(f"w{wk} {o} {shrunk[o]:.1f}")
        unit = dshr.get(team, 0.0) * len(weeks)
        out.append({'team': team, 'sched': sched_pts, 'unit': unit,
                    'total': sched_pts + unit, 'legs': legs, 'byes': byes})
    out.sort(key=lambda r: -r['total'])

    print()
    print(f"  FORWARD D/ST SLATE  --  weeks {weeks[0]}-{weeks[-1]} of {a.season}")
    print(f"  {'':4}{'D/ST':<6}{'TOTAL':>8}{'sched':>8}{'unit':>7}   the weeks")
    print('  ' + '-' * 84)
    for i, r in enumerate(out, 1):
        mark = '  <<' if i <= 5 else ('  ..' if i > len(out) - 5 else '')
        print(f"  {i:>2}. {r['team']:<6}{r['total']:>8.2f}{r['sched']:>8.2f}{r['unit']:>+7.2f}   "
              + ' | '.join(r['legs']) + mark)
    print('  ' + '-' * 84)
    sp  = out[0]['total'] - out[-1]['total']
    ssp = max(r['sched'] for r in out) - min(r['sched'] for r in out)
    usp = max(r['unit']  for r in out) - min(r['unit']  for r in out)
    print(f"  best-to-worst over {n} weeks: TOTAL {sp:.2f}  ({sp/n:.2f} a week)")
    print(f"     of which SCHEDULE {ssp:.2f} and the UNIT ITSELF {usp:.2f}"
          f"  -- schedule is {100*ssp/(ssp+usp):.0f}% of the movable spread")
    print(f"  TAKE: {' > '.join(r['team'] for r in out[:5])}")
    print(f"  AVOID: {' , '.join(r['team'] for r in out[-5:])}")
    print()
    with open(os.path.join(HERE, f'slate_w{weeks[0]}_{weeks[-1]}.csv'), 'w',
              newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['rank', 'dst', 'total', 'schedule', 'unit'] + [f'wk{x}' for x in weeks])
        for i, r in enumerate(out, 1):
            w.writerow([i, r['team'], round(r['total'], 2), round(r['sched'], 2),
                        round(r['unit'], 2)] + r['legs'])
    return 0

if __name__ == '__main__':
    sys.exit(main())
