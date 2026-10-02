#!/usr/bin/env python3
r"""a1_injury_sim.py -- catalog A1: what the drop costs look like when the page can see an absence.

THE CLAIM IN ITS TESTABLE FORM, written before the run (0.5a2):
  On Matt's 15, weeks 1-14, with each man's weekly availability drawn from the measured
  position absence rates in absence_rates.json instead of byes alone, the CHEAPEST-DROP ORDER
  changes: Hockenson stops pricing at 0.0, because he enters the lineup in the weeks LaPorta is
  out, and the ordering of the cheap bodies is not the bye-only ordering.

BASELINE: the same fourteen weeks, same projections, same best-legal-nine function, byes only.
That is exactly what the shipped page computes, so the two numbers are comparable by construction.
POPULATION of the rates: prior-season top-24 RB / top-24 WR / top-12 QB / top-12 TE, measured the
following season, 2022-2025, 318 player-seasons (absence_rates.py).
PAIRED: one availability draw per simulation, reused for the full roster and for every candidate
drop, so the difference carries no extra noise.

Stdlib only, apart from sheet_engine, which is the production lineup code (0.2: the object
production builds, not an equivalent one).
"""
import csv, json, os, random, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.environ.get('A1_SCRIPTS', HERE)
SRC = os.environ.get('A1_SRC', HERE)
sys.path.insert(0, SCRIPTS)
import sheet_engine as se                                    # noqa: E402

N = int(os.environ.get('A1_N', '4000'))
SEED = int(os.environ.get('A1_SEED', '20260912'))
# D/ST is a TEAM: it plays every week but its bye, so its absence rate is zero by construction.
DST = 0.0


def load_roster():
    rate, why = se.rates(SRC)
    assert not why, why
    mine = {}
    with open(os.path.join(SRC, 'MY_ROSTER.csv'), newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            mine[str(r['espn_id']).strip()] = r['player']
    roster = [dict(rate[p]) for p in mine if p in rate]
    assert len(roster) == len(mine), f'{len(mine) - len(roster)} of his men carry no projection'
    return roster


# WHAT AN EMPTY SLOT IS ACTUALLY WORTH. Dropping a man does not leave a hole all season: Matt
# streams. Charging the full hole overstates every drop cost, and it overstates a BACKUP most of
# all, because a backup exists precisely for the weeks the slot would otherwise be empty.
# Measured waiver returns, per played week, declared [INHERITED]: QB 16.65 (doc 92, re-derived from
# the raw files), TE 5.53, WR 6.54, RB 5.43 (doc 12). D/ST and K are streamed by 11-12 of 12 teams
# every season (4.8), so their replacement is the position's own startable rate.
WAIVER = {'QB': 16.65, 'RB': 5.43, 'WR': 6.54, 'TE': 5.53, 'FLEX': 6.54, 'D/ST': 5.99, 'K': 7.5}


# AND A HANDCUFF DOES NOT SCORE HIS OWN PROJECTION IN THE WEEKS HE PLAYS. 6's rule, in Matt's
# words through doc 240: "a bench running back earns his spot by the job he would inherit, never by
# his own projection." Mike Washington Jr. is depth 2 behind Ashton Jeanty; that job pays 248 for
# the season (depth_map job_ceil), which is 14.6 a game, and doc 244's median relief rate across 40
# measured events is 11.2. His own projection is 3.68. All three are run, because the answer for
# him is a bracket and not a point.
HANDCUFF = {'Mike Washington Jr.': 'Ashton Jeanty'}


def run(roster, rates, n=N, seed=SEED, fill=False, relief=None):
    """Returns (mean season total, {name: mean drop cost}) under drawn availability."""
    rng = random.Random(seed)
    names = [p['name'] for p in roster]
    idx = {p['name']: i for i, p in enumerate(roster)}
    cuffs = [(idx[b], idx[a]) for b, a in HANDCUFF.items() if b in idx and a in idx]
    base, cost = [], {nm: [] for nm in names}
    for _ in range(n):
        # one draw, reused everywhere: availability[i][w]
        av = [[rng.random() >= rates.get(p['pos'], 0.0) for w in se.WEEKS] for p in roster]
        def total(skip=None):
            t = 0.0
            for wi, w in enumerate(se.WEEKS):
                here = []
                for i, p in enumerate(roster):
                    if i == skip or not av[i][wi]:
                        continue
                    if relief:
                        for bi, ai in cuffs:
                            # the man ahead is out this week (or was dropped): the backup inherits
                            if i == bi and (ai == skip or not av[ai][wi]
                                            or roster[ai]['bye'] == w):
                                p = dict(p, wk=max(p['wk'], relief))
                    here.append(p)
                pts, empty = se.week_points(here, w)
                t += pts
                if fill:
                    t += sum(WAIVER.get(lab, 0.0) for lab in empty)
            return t
        full = total()
        base.append(full)
        for i, nm in enumerate(names):
            cost[nm].append(full - total(skip=i))
    return statistics.mean(base), {nm: statistics.mean(v) for nm, v in cost.items()}, \
        {nm: statistics.stdev(v) / (len(v) ** 0.5) for nm, v in cost.items()}


def main():
    roster = load_roster()
    measured = json.load(open(os.path.join(HERE, 'absence_rates.json')))
    zero = {p: 0.0 for p in measured}
    meas = dict(measured); meas['D/ST'] = DST
    # doc 111 measured a drafted starting QB missing 2.98 weeks of 14 in THIS league, against the
    # 1.79 measured here on prior-season top-12 finishers. His population is the harsher one and is
    # the right sensitivity: scale every rate by the same factor.
    hard = {p: min(0.95, v * (2.98 / 1.79)) for p, v in meas.items()}

    print('A1 -- the drop cost when the page can see an absence\n')
    print('rates used (share of non-bye weeks missed):')
    print('  measured :', ' '.join(f'{k} {v:.1%}' for k, v in sorted(meas.items())))
    print("  doc 111  :", ' '.join(f'{k} {v:.1%}' for k, v in sorted(hard.items())))
    rows = {}
    # THE 2x2, because two things change at once and they must be separated: does the model see
    # INJURIES, and does a hole get STREAMED? The page today is the top-left cell.
    for tag, r, fl in (('byes only, hole unfilled (the page today)', zero, False),
                       ('byes only, hole streamed', zero, True),
                       ('measured, hole unfilled', meas, False),
                       ('measured, hole streamed', meas, True),
                       ('doc 111 scaled, hole streamed', hard, True)):
        b, c, se_ = run(roster, r, fill=fl)
        rows[tag] = (b, c, se_)
        print(f'\n{tag}: season total {b:.1f}')
        order = sorted(c.items(), key=lambda kv: kv[1])
        for nm, v in order[:8]:
            print(f'   {nm:<24}{v:>7.2f}  +/- {se_[nm]:.2f}')
    print('\nWHAT MOVED, cheapest eight, byes-only order on the left:')
    _, c0, _ = rows['byes only, hole unfilled (the page today)']
    _, c1, s1 = rows['measured, hole streamed']
    o0 = [nm for nm, _ in sorted(c0.items(), key=lambda kv: kv[1])]
    o1 = [nm for nm, _ in sorted(c1.items(), key=lambda kv: kv[1])]
    print(f"   {'byes only':<26}{'measured, streamed':<26}")
    for i in range(8):
        print(f'   {i+1:>2}. {o0[i]:<22}{i+1:>2}. {o1[i]:<22}'
              f'{c0[o0[i]]:>7.2f} -> {c1[o1[i]]:>7.2f}')
    print('\nTHE HANDCUFF, PRICED THREE WAYS (measured rates, hole streamed).')
    print('  what Washington scores in the weeks Jeanty is out ->  his drop cost')
    for lab, rel in (('his own projection, 3.68 (what the page assumes)', None),
                     ("doc 244's median relief rate, 11.2", 11.2),
                     ("the job itself, 248/17 = 14.6", 248 / 17.0)):
        _, cc, ss = run(roster, meas, fill=True, relief=rel)
        print(f"   {lab:<46}{cc['Mike Washington Jr.']:>7.2f}  +/- {ss['Mike Washington Jr.']:.2f}")
    print(f"\n  cheapest man, byes only : {o0[0]} ({c0[o0[0]]:.2f})")
    print(f"  cheapest man, measured  : {o1[0]} ({c1[o1[0]]:.2f} +/- {s1[o1[0]]:.2f})")
    print(f"  ORDER OF THE CHEAPEST FOUR CHANGES: {o0[:4] != o1[:4]}")
    json.dump({'byes_only': c0, 'measured_unfilled': rows['measured, hole unfilled'][1],
               'measured_streamed': c1, 'doc111_streamed': rows['doc 111 scaled, hole streamed'][1]},
              open(os.path.join(HERE, 'a1_drop_costs.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
