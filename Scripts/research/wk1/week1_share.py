#!/usr/bin/env python3
r"""week1_share.py -- "we would have caught this earlier": is a backup's WEEK 1 share of a healthy
starter's backfield a signal, or is it noise?

MATT, 2026-09-12: "Other analysts call for Kaelon Black to be a bench stash, but we never heeded
those signals and we need to learn from that." Black took 16 snaps to Christian McCaffrey's 15 in
the first half of week 1 and led the team in carries, with McCaffrey healthy. The seat model on our
page prices a backfield seat at what it pays WHEN THE JOB OPENS, so a back who is already being
paid while the starter plays is invisible to it. This asks whether that is worth seeing.

THE CLAIM IN ITS TESTABLE FORM, written before the run (0.5a2):
  Among teams whose week-1 lead back PLAYED, the second back's share of the team's week-1 backfield
  work predicts his weeks 2-14 scoring, and a high week-1 share marks a back who becomes startable
  more often than the ordinary handcuff does.

POPULATION -- restate it every time (0.6): every team-season 2021-2025. Week 1 only for the
predictor. The team's leading week-1 back must have PLAYED in week 1 (if he did not, the job was
already open and that is a different event, doc 294's). The second back must have played too.
PREDICTOR: RB2's share of his team's week-1 running-back carries plus targets.
OUTCOME: his half-PPR points a game over weeks 2-14, and whether he averaged the RB replacement
rate of 9.92 [INHERITED: 4.1's RB30 season total / 17].
BASELINE: the same population, split by that share. Permutation on the difference, 4,000 draws.
Source: nflverse stats_player_week_<season>.csv, regular season. Stdlib only.
"""
import collections, csv, os, random, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get('WK1_DATA', HERE)
SEASONS = [2021, 2022, 2023, 2024, 2025]
RB_REPL = 9.92


def half_ppr(r):
    g = lambda k: float(r.get(k) or 0)
    return (0.1 * g('rushing_yards') + 6 * g('rushing_tds')
            + 0.1 * g('receiving_yards') + 6 * g('receiving_tds') + 0.5 * g('receptions')
            - 2 * (g('rushing_fumbles_lost') + g('receiving_fumbles_lost')))


def load(season):
    rows = []
    with open(os.path.join(DATA, f'stats_player_week_{season}.csv'), newline='',
              encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            if (r.get('season_type') or 'REG') != 'REG' or (r.get('position') or '') != 'RB':
                continue
            try:
                r['_w'] = int(r['week'])
            except (TypeError, ValueError):
                continue
            rows.append(r)
    return rows


def main():
    recs = []
    for s in SEASONS:
        rows = load(s)
        wk1 = collections.defaultdict(list)
        rest = collections.defaultdict(lambda: [0.0, 0])
        name = {}
        for r in rows:
            pid = r['player_id']
            name[pid] = r.get('player_display_name') or pid
            if r['_w'] == 1:
                wk1[r['team']].append((float(r.get('carries') or 0) + float(r.get('targets') or 0),
                                       pid))
            elif 2 <= r['_w'] <= 14:
                rest[pid][0] += half_ppr(r)
                rest[pid][1] += 1
        for tm, lst in wk1.items():
            lst.sort(reverse=True)
            if len(lst) < 2:
                continue
            tot = sum(u for u, _ in lst)
            if tot < 10:                       # a backfield with no work in week 1 says nothing
                continue
            (u1, p1), (u2, p2) = lst[0], lst[1]
            if u1 <= 0 or u2 <= 0:
                continue
            g = rest[p2][1]
            if g < 4:                          # he has to be around to be measured
                continue
            recs.append(dict(season=s, tm=tm, rb1=name[p1], rb2=name[p2],
                             share=u2 / tot, ratio=u2 / u1, u1=u1, u2=u2,
                             ppg=rest[p2][0] / g, g=g,
                             hit=1 if rest[p2][0] / g >= RB_REPL else 0))
    n = len(recs)
    print("week-1 share of a HEALTHY starter's backfield, and what the backup did afterwards")
    print(f'population: {n} team-seasons, 2021-2025, lead back played in week 1\n')
    print(f"{'RB2 share of week-1 RB work':<30}{'n':>4}{'wks 2-14 ppg':>14}{'reached 9.92':>14}")
    bands = [(0, .20, 'under 20%'), (.20, .30, '20 to 30%'), (.30, .40, '30 to 40%'),
             (.40, 1.01, '40% or more')]
    for lo, hi, lab in bands:
        b = [r for r in recs if lo <= r['share'] < hi]
        if b:
            print(f'{lab:<30}{len(b):>4}{statistics.mean(r["ppg"] for r in b):>14.2f}'
                  f'{sum(r["hit"] for r in b) / len(b):>13.0%}')
    hi_ = [r for r in recs if r['share'] >= .35]
    lo_ = [r for r in recs if r['share'] < .35]
    d_ppg = statistics.mean(r['ppg'] for r in hi_) - statistics.mean(r['ppg'] for r in lo_)
    d_hit = sum(r['hit'] for r in hi_) / len(hi_) - sum(r['hit'] for r in lo_) / len(lo_)
    print(f'\n  35% or more (n={len(hi_)}) minus under 35% (n={len(lo_)}): '
          f'ppg {d_ppg:+.2f}, startable rate {d_hit:+.1%}')
    rng = random.Random(20260912)
    vals_p = [r['ppg'] for r in recs]
    vals_h = [r['hit'] for r in recs]
    k = len(hi_)
    hp = hh = 0
    REPS = 4000
    for _ in range(REPS):
        idx = list(range(n))
        rng.shuffle(idx)
        a, b = idx[:k], idx[k:]
        if statistics.mean(vals_p[i] for i in a) - statistics.mean(vals_p[i] for i in b) >= d_ppg:
            hp += 1
        if (sum(vals_h[i] for i in a) / k - sum(vals_h[i] for i in b) / (n - k)) >= d_hit:
            hh += 1
    print(f'  permutation, {REPS} draws, one-sided: ppg p={hp/REPS:.4f}   startable p={hh/REPS:.4f}')
    print('\n  the ten biggest week-1 shares, and what happened next:')
    for r in sorted(recs, key=lambda r: -r['share'])[:10]:
        print(f"    {r['season']} {r['tm']:<4} {r['rb2']:<22} {r['share']:.0%} of the work behind "
              f"{r['rb1']:<20} -> {r['ppg']:>5.1f} ppg over {r['g']:>2} games"
              f"{'   STARTABLE' if r['hit'] else ''}")
    # the honest counterweight: what does the SAME table look like for the generic handcuff?
    base_hit = sum(r['hit'] for r in recs) / n
    print(f'\n  base rate across the whole population: {base_hit:.0%} startable, '
          f'{statistics.mean(r["ppg"] for r in recs):.2f} ppg')


if __name__ == '__main__':
    main()
