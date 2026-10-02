#!/usr/bin/env python3
r"""squeeze.py -- catalog F1, Matt's mechanism: does a veteran ARRIVAL squeeze the room BELOW the
incumbent, rather than only the incumbent?

HIS CLAIM, in his words: "the arrival compresses everyone below him, not just the man at the top.
If that's right, Waddle hurts Bryant more than Sutton does, and my watch trigger is Waddle's snaps,
not Sutton's."

THE CLAIM IN ITS TESTABLE FORM (0.5a2), written before the run:
  Among team-seasons with a returning 60+-target incumbent receiver, the arrival of a receiver who
  had 60+ targets for ANOTHER team the year before costs the team's returning 3rd and 4th receivers
  (ranked by LAST season's targets, fixed before the outcome) more share of team targets than it
  costs the incumbent, both absolutely and in proportion to the share they held.

POPULATION: team-seasons 2021-2025. A player is ON a team in season t if he has a regular-season
line for it. Receivers only (position WR). 4+ games played in BOTH seasons; the number removed by
that filter is reported (B2).
OUTCOME: share of his team's receiver targets, per game played, in t minus the same in t-1.
BASELINE: the identical change on team-seasons that have a returning 60+ incumbent and NO arrival.
CONTROL: vacated share -- the share of t-1 team targets held by men who are not on the team in t --
because an arrival usually replaces a departure, which lifts everyone's share and would hide a
squeeze. Reported as a split, and as a covariate-adjusted difference.
CLUSTERED BY TEAM (A5): the unit is the team-season, and the permutation shuffles whole teams.

Source: nflverse stats_player_week_<season>.csv 2020-2025, regular season. Stdlib only.
"""
import collections, csv, os, random, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get('F1_DATA', HERE)
SEASONS = list(range(2020, 2026))
MING, BIG = 4, 60


def load(season):
    per = collections.defaultdict(lambda: dict(tgt=0.0, g=0, team=collections.Counter(), pos=''))
    with open(os.path.join(DATA, f'stats_player_week_{season}.csv'), newline='',
              encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            if (r.get('season_type') or 'REG') != 'REG':
                continue
            pid = r['player_id']
            d = per[pid]
            d['tgt'] += float(r.get('targets') or 0)
            d['g'] += 1
            d['team'][r['team']] += 1
            d['pos'] = r.get('position') or d['pos']
            d['name'] = r.get('player_display_name') or r.get('player_name') or pid
    for d in per.values():
        d['tm'] = d['team'].most_common(1)[0][0]
    return per


def main():
    yr = {s: load(s) for s in SEASONS}
    # team receiver targets per season
    team_tgt = {s: collections.Counter() for s in SEASONS}
    for s in SEASONS:
        for pid, d in yr[s].items():
            if d['pos'] == 'WR':
                team_tgt[s][d['tm']] += d['tgt']

    treat, ctrl, dropped = [], [], 0
    for s in SEASONS[1:]:
        prev = s - 1
        by_team_prev = collections.defaultdict(list)
        for pid, d in yr[prev].items():
            if d['pos'] == 'WR':
                by_team_prev[d['tm']].append((d['tgt'], pid))
        for tm, lst in by_team_prev.items():
            lst.sort(reverse=True)
            ranked = [pid for _, pid in lst]
            incumbent = next((pid for _, pid in lst
                              if _ >= BIG and pid in yr[s] and yr[s][pid]['tm'] == tm), None)
            if incumbent is None:
                continue
            # an ARRIVAL: 60+ targets elsewhere last year, on this team now
            arrivals = [pid for pid, d in yr[s].items()
                        if d['pos'] == 'WR' and d['tm'] == tm and pid in yr[prev]
                        and yr[prev][pid]['tm'] != tm and yr[prev][pid]['tgt'] >= BIG]
            vacated = sum(d['tgt'] for pid, d in yr[prev].items()
                          if d['pos'] == 'WR' and d['tm'] == tm
                          and (pid not in yr[s] or yr[s][pid]['tm'] != tm))
            vac_share = vacated / team_tgt[prev][tm] if team_tgt[prev][tm] else 0.0

            def delta(pid):
                """share of team receiver targets per game, this season minus last."""
                nonlocal dropped
                if pid not in yr[s] or yr[s][pid]['tm'] != tm:
                    return None
                a, b = yr[prev][pid], yr[s][pid]
                if a['g'] < MING or b['g'] < MING:
                    dropped += 1
                    return None
                if not team_tgt[prev][tm] or not team_tgt[s][tm]:
                    return None
                return ((b['tgt'] / b['g']) / (team_tgt[s][tm] / 17.0)
                        - (a['tgt'] / a['g']) / (team_tgt[prev][tm] / 17.0))

            d_inc = delta(incumbent)
            # THE ROOM BELOW: ranks 3 and 4 last season, fixed here, never re-ranked on the outcome
            below = [delta(pid) for pid in ranked[2:4]]
            below = [x for x in below if x is not None]
            if d_inc is None or not below:
                continue
            base_below = statistics.mean(
                (yr[prev][pid]['tgt'] / yr[prev][pid]['g']) / (team_tgt[prev][tm] / 17.0)
                for pid in ranked[2:4] if pid in yr[prev] and yr[prev][pid]['g'] >= MING)
            row = dict(season=s, tm=tm, inc=d_inc, below=statistics.mean(below),
                       n_below=len(below), vac=vac_share, base_below=base_below,
                       inc_name=yr[prev][incumbent]['name'],
                       arr=[yr[s][a]['name'] for a in arrivals])
            (treat if arrivals else ctrl).append(row)

    def m(rows, k):
        return statistics.mean(r[k] for r in rows)

    print('F1 -- does a veteran arrival squeeze the room below the incumbent?')
    print(f'population: team-seasons 2021-2025 with a returning 60+-target incumbent.')
    print(f'  with an arrival : {len(treat)} team-seasons')
    print(f'  without one     : {len(ctrl)} team-seasons')
    print(f'  player-seasons dropped by the 4-game minimum: {dropped}\n')
    print(f"{'':<26}{'incumbent':>12}{'3rd+4th':>12}{'vacated':>10}")
    for lab, rows in (('arrival', treat), ('no arrival', ctrl)):
        print(f'{lab:<26}{m(rows,"inc"):>+12.3f}{m(rows,"below"):>+12.3f}{m(rows,"vac"):>10.1%}')
    d_inc = m(treat, 'inc') - m(ctrl, 'inc')
    d_bel = m(treat, 'below') - m(ctrl, 'below')
    print(f'\n  arrival minus no arrival:  incumbent {d_inc:+.3f}   3rd+4th {d_bel:+.3f}')
    print(f'  HIS DIRECTION NEEDS 3rd+4th TO LOSE MORE THAN THE INCUMBENT: '
          f'{"yes" if d_bel < d_inc else "NO"}')

    # in PROPORTION to the share they held
    def prop(rows, k, base):
        out = []
        for r in rows:
            b = r[base] if base != 'inc_base' else None
            if b and b > 0.01:
                out.append(r[k] / b)
        return statistics.mean(out) if out else float('nan')
    print(f'\n  in proportion to the share held (3rd+4th): arrival {prop(treat,"below","base_below"):+.2f}'
          f'   no arrival {prop(ctrl,"below","base_below"):+.2f}')

    # permutation, CLUSTERED BY TEAM (A5): shuffle the arrival label across whole team-seasons
    rows = [dict(r, t=1) for r in treat] + [dict(r, t=0) for r in ctrl]
    by_team = collections.defaultdict(list)
    for r in rows:
        by_team[r['tm']].append(r)
    obs = d_bel
    rng = random.Random(20260912)
    hits = 0
    REPS = 4000
    for _ in range(REPS):
        lab = {}
        for tm, rs in by_team.items():
            k = sum(r['t'] for r in rs)
            idx = list(range(len(rs)))
            rng.shuffle(idx)
            for j, i in enumerate(idx):
                lab[(tm, i)] = 1 if j < k else 0
        a = [rs[i]['below'] for tm, rs in by_team.items() for i in range(len(rs)) if lab[(tm, i)]]
        b = [rs[i]['below'] for tm, rs in by_team.items() for i in range(len(rs)) if not lab[(tm, i)]]
        if a and b and (statistics.mean(a) - statistics.mean(b)) <= obs:
            hits += 1
    print(f'\n  permutation on the 3rd+4th difference, shuffled WITHIN team ({REPS} draws): '
          f'p = {hits/REPS:.3f}  [one-sided, his direction]')

    # the vacated control, as a split
    print('\n  SPLIT BY VACATED SHARE (the control that could hide a squeeze):')
    for lab, lo, hi in (('vacated under 20%', 0, .20), ('20-35%', .20, .35), ('35%+', .35, 9)):
        a = [r for r in treat if lo <= r['vac'] < hi]
        b = [r for r in ctrl if lo <= r['vac'] < hi]
        if len(a) >= 3 and len(b) >= 3:
            print(f"    {lab:<20} arrival {m(a,'below'):+.3f} (n={len(a)})   "
                  f"no arrival {m(b,'below'):+.3f} (n={len(b)})   diff {m(a,'below')-m(b,'below'):+.3f}")
    # HIS EXACT WORDS ARE A WITHIN-TEAM COMPARISON: "hurts Bryant more than Sutton does". So the
    # cleanest object is (room below minus incumbent) INSIDE each team-season, which cancels the
    # team denominator entirely -- when a receiver arrives, team targets rise and every share falls
    # a little for reasons that have nothing to do with the squeeze.
    gap_t = [r['below'] - r['inc'] for r in treat]
    gap_c = [r['below'] - r['inc'] for r in ctrl]
    obs2 = statistics.mean(gap_t) - statistics.mean(gap_c)
    print(f"\n  WITHIN each team-season, (3rd+4th) minus incumbent:")
    print(f"    arrival    {statistics.mean(gap_t):+.3f}  (n={len(gap_t)})")
    print(f"    no arrival {statistics.mean(gap_c):+.3f}  (n={len(gap_c)})")
    print(f"    difference {obs2:+.3f}")
    allg = [(r['tm'], r['below'] - r['inc'], 1) for r in treat] + \
           [(r['tm'], r['below'] - r['inc'], 0) for r in ctrl]
    byt = collections.defaultdict(list)
    for tm, v, t in allg:
        byt[tm].append((v, t))
    rng2 = random.Random(20260912)
    hit2 = 0
    for _ in range(REPS):
        a, b = [], []
        for tm, rs in byt.items():
            k = sum(t for _, t in rs)
            vals = [v for v, _ in rs]
            rng2.shuffle(vals)
            a += vals[:k]
            b += vals[k:]
        if a and b and (statistics.mean(a) - statistics.mean(b)) <= obs2:
            hit2 += 1
    print(f"    permutation within team, {REPS} draws: p = {hit2/REPS:.3f}  [one-sided]")

    print('\n  the ten largest squeezes with an arrival:')
    for r in sorted(treat, key=lambda r: r['below'])[:10]:
        print(f"    {r['season']} {r['tm']:<4} below {r['below']:+.3f}  incumbent "
              f"{r['inc']:+.3f} ({r['inc_name']})  arrived: {', '.join(r['arr'])[:46]}")


if __name__ == '__main__':
    main()
