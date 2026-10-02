#!/usr/bin/env python3
r"""wk1_redteam.py -- the red team of doc 300's week-1 share table.

Drop this beside week1_share.py in Scripts\research\wk1\ and run it the same way.
It reads stats_player_week_<season>.csv from its OWN folder (override with WK1_DATA).
Stdlib only. Python 3.12 safe.

WHAT IT ADDS TO week1_share.py, in the order the red team asked for them:

  A  the original table, reproduced
  B  the cut point is not cherry-picked: every split from 15% to 45%, plus a
     cut-free Spearman so the bands do not have to be trusted at all
  C  the confound doc 300 does not exclude: the lead back getting hurt later.
     Table re-run on team-seasons where the lead back played EVERY week 2-14,
     and separately scoring RB2 only in the weeks the lead back played
  D  the population question: is "the second back by week-1 work" the same as
     "the handcuff you could have claimed"? Split on whether RB2 was already a
     startable fantasy back the PRIOR season
  E  the labelling question: in how many rows was the man called "the lead
     back" not the team's weeks 2-14 usage leader

Run:  py wk1_redteam.py            (all seasons found)
      py wk1_redteam.py --years 2021 2022 2023 2024 2025
"""
import collections, csv, math, os, random, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get('WK1_DATA', HERE)
RB_REPL = 9.92  # [INHERITED: 4.1's RB30 season total / 17]
BANDS = [(0, .20, 'under 20%'), (.20, .30, '20 to 30%'),
         (.30, .40, '30 to 40%'), (.40, 1.01, '40% or more')]


def half_ppr(r):
    g = lambda k: float(r.get(k) or 0)
    return (0.1 * g('rushing_yards') + 6 * g('rushing_tds')
            + 0.1 * g('receiving_yards') + 6 * g('receiving_tds')
            + 0.5 * g('receptions')
            - 2 * (g('rushing_fumbles_lost') + g('receiving_fumbles_lost')))


def find_seasons():
    out = []
    for fn in os.listdir(DATA):
        if fn.startswith('stats_player_week_') and fn.endswith('.csv'):
            try:
                out.append(int(fn[18:22]))
            except ValueError:
                pass
    return sorted(out)


def load(season):
    path = os.path.join(DATA, f'stats_player_week_{season}.csv')
    with open(path, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            if (r.get('season_type') or 'REG') != 'REG':
                continue
            try:
                r['_w'] = int(r['week'])
            except (TypeError, ValueError):
                continue
            yield r


def build(seasons):
    recs = []
    for s in seasons:
        wk1 = collections.defaultdict(list)
        rest = collections.defaultdict(lambda: [0.0, 0])
        prior = collections.defaultdict(lambda: [0.0, 0])
        work214 = collections.defaultdict(lambda: collections.defaultdict(float))
        team_weeks = collections.defaultdict(set)
        pl_weeks = collections.defaultdict(set)
        name = {}
        for r in load(s):
            team_weeks[r['team']].add(r['_w'])
            if r.get('position') != 'RB':
                continue
            pid = r['player_id']
            name[pid] = r.get('player_display_name') or pid
            pl_weeks[pid].add(r['_w'])
            if r['_w'] == 1:
                wk1[r['team']].append(
                    (float(r.get('carries') or 0) + float(r.get('targets') or 0), pid))
            elif 2 <= r['_w'] <= 14:
                rest[pid][0] += half_ppr(r)
                rest[pid][1] += 1
                work214[r['team']][pid] += (float(r.get('carries') or 0)
                                            + float(r.get('targets') or 0))
        try:
            for r in load(s - 1):
                if r.get('position') == 'RB' and 1 <= r['_w'] <= 14:
                    prior[r['player_id']][0] += half_ppr(r)
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
            if u1 <= 0 or u2 <= 0 or rest[p2][1] < 4:
                continue
            played = {w for w in team_weeks[tm] if 2 <= w <= 14}
            missed = sorted(played - pl_weeks[p1])
            w2 = work214[tm]
            leader214 = max(w2, key=w2.get) if w2 else None
            pr = prior[p2] if prior is not None else None
            recs.append(dict(
                season=s, tm=tm, rb1=name[p1], rb2=name[p2], p1=p1, p2=p2,
                share=u2 / tot, ppg=rest[p2][0] / rest[p2][1], g=rest[p2][1],
                hit=1 if rest[p2][0] / rest[p2][1] >= RB_REPL else 0,
                lead_missed=len(missed),
                lead_kept_lead=(leader214 == p1),
                lead_share214=(w2.get(p1, 0) / sum(w2.values()) if sum(w2.values()) else 0),
                prior_ppg=(pr[0] / pr[1] if pr and pr[1] >= 4 else None),
                lead_weeks=pl_weeks[p1], team_weeks=played, second=p2))
    return recs


def rb2_ppg_when_lead_played(recs, seasons):
    """RB2's ppg counted only in weeks the lead back also had a line."""
    want = collections.defaultdict(dict)
    for r in recs:
        want[r['season']][(r['tm'], r['second'])] = r
    for s in seasons:
        pts = collections.defaultdict(list)
        for r in load(s):
            if r.get('position') == 'RB' and 2 <= r['_w'] <= 14:
                pts[(r['team'], r['player_id'])].append((r['_w'], half_ppr(r)))
        for key, rec in want[s].items():
            keep = [p for w, p in pts.get(key, []) if w in rec['lead_weeks']]
            rec['ppg_lp'] = (sum(keep) / len(keep)) if keep else None
            rec['hit_lp'] = (1 if keep and sum(keep) / len(keep) >= RB_REPL else 0) if keep else None


def table(recs, label, key='ppg', flag='hit'):
    v = [r for r in recs if r.get(key) is not None]
    print(f'\n{label}   n={len(v)}')
    print(f"  {'RB2 share of week-1 RB work':<30}{'n':>4}{'wks 2-14 ppg':>14}{'reached 9.92':>14}")
    for lo, hi, lab in BANDS:
        b = [r for r in v if lo <= r['share'] < hi]
        if not b:
            print(f'  {lab:<30}{0:>4}')
            continue
        print(f'  {lab:<30}{len(b):>4}{statistics.mean(r[key] for r in b):>14.2f}'
              f'{sum(r[flag] for r in b) / len(b):>13.0%}')
    if v:
        print(f"  {'ALL':<30}{len(v):>4}{statistics.mean(r[key] for r in v):>14.2f}"
              f"{sum(r[flag] for r in v) / len(v):>13.0%}")


def perm(recs, cut, key='ppg', flag='hit', reps=4000, seed=20260913):
    v = [r for r in recs if r.get(key) is not None]
    hi = [r for r in v if r['share'] >= cut]
    lo = [r for r in v if r['share'] < cut]
    if not hi or not lo:
        return None
    dp = statistics.mean(r[key] for r in hi) - statistics.mean(r[key] for r in lo)
    dh = sum(r[flag] for r in hi) / len(hi) - sum(r[flag] for r in lo) / len(lo)
    vp = [r[key] for r in v]
    vh = [r[flag] for r in v]
    n, k = len(v), len(hi)
    rng = random.Random(seed)
    cp = ch = 0
    idx = list(range(n))
    for _ in range(reps):
        rng.shuffle(idx)
        a, b = idx[:k], idx[k:]
        if statistics.mean(vp[i] for i in a) - statistics.mean(vp[i] for i in b) >= dp:
            cp += 1
        if sum(vh[i] for i in a) / k - sum(vh[i] for i in b) / (n - k) >= dh:
            ch += 1
    return dp, cp / reps, dh, ch / reps, k, n - k


def spearman(xs, ys):
    def rank(v):
        s = sorted(range(len(v)), key=lambda i: v[i])
        out = [0.0] * len(v)
        i = 0
        while i < len(s):
            j = i
            while j + 1 < len(s) and v[s[j + 1]] == v[s[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                out[s[k]] = avg
            i = j + 1
        return out
    rx, ry = rank(xs), rank(ys)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else 0.0


def line(recs, cut, key='ppg', flag='hit', pre='  '):
    r = perm(recs, cut, key=key, flag=flag)
    if not r:
        print(f'{pre}{100*cut:.0f}%+ : not enough rows')
        return
    print(f'{pre}{100*cut:.0f}% or more (n={r[4]}) minus under {100*cut:.0f}% (n={r[5]}): '
          f'ppg {r[0]:+.2f} p={r[1]:.4f} | startable {r[2]:+.0%} p={r[3]:.4f}')


def main(argv):
    seasons = find_seasons()
    if '--years' in argv:
        seasons = [int(x) for x in argv[argv.index('--years') + 1:] if x.isdigit()]
    seasons = [s for s in seasons if s >= 2021]
    print(f'seasons used: {seasons}')
    recs = build(seasons)
    rb2_ppg_when_lead_played(recs, seasons)
    print(f'population: {len(recs)} team-seasons')

    table(recs, 'A. DOC 300 AS PUBLISHED')
    line(recs, .35)

    print('\nB. IS 35% A CHOSEN CUT? every split, and a cut-free rank correlation')
    for c in (.15, .20, .25, .30, .35, .40, .45):
        line(recs, c, pre='   ')
    print(f"   cut-free Spearman(share, ppg) = "
          f"{spearman([r['share'] for r in recs], [r['ppg'] for r in recs]):+.3f}")

    clean = [r for r in recs if r['lead_missed'] == 0]
    table(clean, 'C1. LEAD BACK PLAYED EVERY WEEK 2-14 (the confound removed)')
    line(clean, .35)
    table([r for r in recs if r['lead_missed'] > 0],
          'C2. LEAD BACK MISSED AT LEAST ONE WEEK 2-14')
    table(recs, 'C3. ALL TEAMS, RB2 SCORED ONLY IN WEEKS THE LEAD BACK PLAYED',
          key='ppg_lp', flag='hit_lp')
    print('\n   is the predictor correlated with the confound?')
    for lo, hi, lab in BANDS:
        b = [r for r in recs if lo <= r['share'] < hi]
        if b:
            print(f'   {lab:<14} n={len(b):>3}  lead missed a game '
                  f'{sum(1 for r in b if r["lead_missed"]):>3}/{len(b):<3} '
                  f'({sum(1 for r in b if r["lead_missed"])/len(b):.0%})  '
                  f'mean weeks missed {statistics.mean(r["lead_missed"] for r in b):.2f}')

    claim = [r for r in recs if r['prior_ppg'] is None or r['prior_ppg'] < RB_REPL]
    rost = [r for r in recs if r not in claim]
    print(f'\nD. CLAIMABLE? RB2 startable the PRIOR season = already rostered everywhere.')
    print(f'   {len(rost)} of {len(recs)} team-seasons were not claims at all.')
    for lo, hi, lab in BANDS:
        b = [r for r in recs if lo <= r['share'] < hi]
        g = [r for r in rost if lo <= r['share'] < hi]
        if b:
            print(f'   {lab:<14} {len(g):>3} of {len(b):<3} ({len(g)/len(b):.0%}) '
                  + ', '.join(sorted(x['rb2'] for x in g)[:5]))
    table(claim, 'D1. CLAIMABLE ONLY')
    line(claim, .35)
    table([r for r in claim if r['lead_missed'] == 0],
          'D2. CLAIMABLE AND THE LEAD BACK NEVER MISSED A WEEK')
    line([r for r in claim if r['lead_missed'] == 0], .35)
    table([r for r in claim if r['lead_missed'] > 0],
          'D3. CLAIMABLE AND THE LEAD BACK MISSED TIME  <-- the cell Kaelon Black is in')
    line([r for r in claim if r['lead_missed'] > 0], .35)

    print('\nE. WAS THE MAN CALLED "THE LEAD BACK" ACTUALLY THE LEAD BACK?')
    print('   (did he lead his own team in weeks 2-14 carries plus targets)')
    for lo, hi, lab in BANDS:
        b = [r for r in recs if lo <= r['share'] < hi]
        if b:
            no = [r for r in b if not r['lead_kept_lead']]
            print(f'   {lab:<14} n={len(b):>3}  labelled RB1 did NOT keep the lead: '
                  f'{len(no):>3} ({len(no)/len(b):.0%})')
    bad = [r for r in recs if not r['lead_kept_lead']]
    print(f'   overall {len(bad)} of {len(recs)} ({len(bad)/len(recs):.0%})')
    print('\n   the 40%+ rows where the labels were the wrong way round:')
    for r in sorted([x for x in recs if x['share'] >= .40 and not x['lead_kept_lead']],
                    key=lambda x: -x['share']):
        print(f'    {r["season"]} {r["tm"]:<4}{r["rb2"]:<23}{r["share"]:.0%} behind '
              f'{r["rb1"]:<21} -> {r["ppg"]:>5.1f} ppg'
              f'{" STARTABLE" if r["hit"] else "         "}  '
              f'(that "lead back" kept {r["lead_share214"]:.0%} of the work)')
    table([r for r in recs if r['lead_kept_lead']],
          'E1. ONLY ROWS WHERE THE LABELLED LEAD BACK KEPT THE JOB')
    line([r for r in recs if r['lead_kept_lead']], .35)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
