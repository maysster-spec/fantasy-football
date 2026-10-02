"""width_study.py -- does a team's PERSONNEL SHAPE change what moving up the receiver order is
worth?   Matt, 2026-09-10, and the claim is quoted rather than paraphrased (SECTION 0.5a2):

   "Teams who favor 3 WR sets have more target distribution and perhaps even more so if they have
    a productive pass catching RB and TE (Bowers). However, there are also teams that run heavy
    personnel with two TE sets ... less target distribution due to fewer WRs on the field ...
    a team with more common 2 WR sets may favor a WR3 who moves up to WR2."

THE FOUR TESTABLE FORMS, run in this order because the premise has to survive before the claim is
worth a test:
  1  Is personnel shape a TEAM TRAIT that persists year to year?  (SECTION 4.24a: persistence
     before payoff.  A trait that does not persist cannot be planned around in August.)
  2  THE PREMISE -- on a heavier team, is the WR2 slot a bigger share of the targets?
  3  THE CLAIM -- among receivers who actually MOVED UP the order, is the gain bigger there?
  4  HIS OTHER MECHANISM -- do a pass-catching tight end and back eat the WR2's share?

POPULATION: every team-season 2022-2025 in Source\\pff_receiving_<year>.csv, regular season, 32
teams a year = 128 team-seasons.

MEASUREMENT NOTE, AND IT KILLED THE FIRST VERSION OF THIS STUDY (SECTION 0.2).  The obvious
"receivers on the field per pass play" is routes divided by team pass plays -- and THIS FILE HAS NO
TEAM PASS-PLAY COLUMN.  `pass_plays` is per player: the team's pass plays while HE was on the
field.  Using the team's maximum as the denominator gave Buffalo 4.13 receivers per pass play in
2025, which is impossible, because their most-used receiver was on for only 453 snaps.  The error is
worst on exactly the teams that rotate or lose receivers -- the thing being measured -- so it is a
confound and not just noise.  Every measure below is therefore a RATIO OF TWO ROUTE COUNTS or a
share of TARGETS, both of which cancel the missing denominator:
    heavy      = TE routes / WR routes        (higher = more tight end relative to receiver)
    rb_ratio   = RB routes / WR routes
    te_share   = TE targets / all team targets
    fed        = how many receivers draw 8% or more of the team's targets

CLUSTERING: personnel shape is a TEAM CONSTANT, so the unit is the TEAM-SEASON, never the player
(ERROR_PATTERNS A5; this trap has already cost three results in this project -- SECTION 4.21,
4.23a, 4.24c).  Player-level numbers are printed only next to their clustered version.

Standard library only; paths resolve against this file, not the shell (SECTION 0.4).
"""
import csv
import os
import random
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', 'Source'))
YEARS = (2022, 2023, 2024, 2025)
MIN_ROUTES = 50      # under 50 routes is a camp body, not a slot in the order
MIN_BOTH = 100       # a promotion needs a real role in both seasons, not a cameo
FED_BAR = 0.08       # "the team feeds him" -- 8% of team targets
RB = ('HB', 'FB')


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


_CACHE = {}


def load(y):
    if y in _CACHE:
        return _CACHE[y]
    p = os.path.join(SRC, f'pff_receiving_{y}.csv')
    if not os.path.exists(p):
        raise SystemExit(f'missing {p} -- this study cannot run')
    with open(p, newline='', encoding='utf-8-sig') as fh:
        _CACHE[y] = list(csv.DictReader(fh))
    return _CACHE[y]


def season(y):
    out = {}
    rows = load(y)
    for tm in sorted({r['team_name'] for r in rows}):
        men = [r for r in rows if r['team_name'] == tm]
        tt = sum(num(r['targets']) for r in men)
        wr = [r for r in men if r['position'] == 'WR']
        te = [r for r in men if r['position'] == 'TE']
        rb = [r for r in men if r['position'] in RB]
        wrr = sum(num(r['routes']) for r in wr)
        if tt < 200 or wrr < 500:
            continue
        wrt = sum(num(r['targets']) for r in wr)
        order = sorted([r for r in wr if num(r['routes']) >= MIN_ROUTES],
                       key=lambda r: -num(r['targets']))
        out[tm] = dict(
            tt=tt, wrt=wrt,
            heavy=sum(num(r['routes']) for r in te) / wrr,
            rb_ratio=sum(num(r['routes']) for r in rb) / wrr,
            te_share=sum(num(r['targets']) for r in te) / tt,
            rb_share=sum(num(r['targets']) for r in rb) / tt,
            wr_share=wrt / tt,
            order=order,
            share={r['player']: num(r['targets']) / tt for r in men},
            inwr={r['player']: (num(r['targets']) / wrt if wrt else 0) for r in wr},
            rank={r['player']: i + 1 for i, r in enumerate(order)},
            routes={r['player']: num(r['routes']) for r in men},
            fed=sum(1 for r in wr if tt and num(r['targets']) / tt >= FED_BAR),
        )
    return out


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    sx = sum((x - mx) ** 2 for x in xs) ** .5
    sy = sum((y - my) ** 2 for y in ys) ** .5
    return 0.0 if sx == 0 or sy == 0 else \
        sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy)


def perm_r(xs, ys, n=10000, seed=7):
    """Permutation p on a correlation -- scipy is not on his machine (doc 144)."""
    r0 = pearson(xs, ys)
    rnd = random.Random(seed)
    ys2, hits = list(ys), 0
    for _ in range(n):
        rnd.shuffle(ys2)
        if abs(pearson(xs, ys2)) >= abs(r0):
            hits += 1
    return r0, (hits + 1) / (n + 1)


def boot_diff(a, b, n=10000, seed=11):
    rnd = random.Random(seed)
    d0 = st.mean(a) - st.mean(b)
    ds = []
    for _ in range(n):
        ds.append(st.mean([rnd.choice(a) for _ in a]) - st.mean([rnd.choice(b) for _ in b]))
    ds.sort()
    pool, hits = list(a) + list(b), 0
    for _ in range(n):
        rnd.shuffle(pool)
        if abs(st.mean(pool[:len(a)]) - st.mean(pool[len(a):])) >= abs(d0):
            hits += 1
    return d0, ds[int(.025 * n)], ds[int(.975 * n)], (hits + 1) / (n + 1)


def main():
    S = {y: season(y) for y in YEARS}
    print('=' * 79)
    print('PERSONNEL SHAPE AND WHAT A PROMOTION IS WORTH   --   PFF receiving, 2022-2025')
    print('  heavy = tight-end routes per receiver route.  Denominator-free, see the header.')
    print('=' * 79)

    # ---- 1. persistence -------------------------------------------------------------------
    print('\n1.  IS PERSONNEL SHAPE A TEAM TRAIT?   unit: consecutive team-season pair')
    for label, key in (('heavy (TE routes / WR routes)', 'heavy'),
                       ('backs routes / WR routes', 'rb_ratio'),
                       ('TE share of targets', 'te_share'),
                       ('RB share of targets', 'rb_share'),
                       ('receivers fed 8%+ of targets', 'fed')):
        xs, ys = [], []
        for y in YEARS[:-1]:
            for tm in S[y]:
                if tm in S[y + 1]:
                    xs.append(S[y][tm][key]); ys.append(S[y + 1][tm][key])
        r, p = perm_r(xs, ys)
        vals = [S[y][tm][key] for y in YEARS for tm in S[y]]
        print('      %-30s r=%+.3f  p=%.4f   n=%d   mean %.3f  sd %.3f  range %.2f-%.2f'
              % (label, r, p, len(xs), st.mean(vals), st.pstdev(vals), min(vals), max(vals)))

    last = S[YEARS[-1]]
    rk = sorted(last, key=lambda t: -last[t]['heavy'])
    print('\n      HEAVIEST 6 in %d:   ' % YEARS[-1]
          + '  '.join('%s %.2f' % (t, last[t]['heavy']) for t in rk[:6]))
    print('      LIGHTEST 6:        '
          + '  '.join('%s %.2f' % (t, last[t]['heavy']) for t in rk[-6:]))

    # ---- 2. the premise -------------------------------------------------------------------
    print('\n2.  THE PREMISE -- on a HEAVIER team, is each receiver slot a bigger share?')
    print('      unit: team-season.  "of WR" = his share of the receivers\' targets only, which')
    print('      removes the arithmetic that shares must add to 100.')
    for slot in (1, 2, 3):
        for tag, field in (('of team', 'share'), ('of WR  ', 'inwr')):
            xs, ys = [], []
            for y in YEARS:
                for tm, d in S[y].items():
                    if len(d['order']) >= slot:
                        xs.append(d['heavy']); ys.append(d[field][d['order'][slot - 1]['player']])
            r, p = perm_r(xs, ys)
            print('      WR%d share %s vs heavy:  r=%+.3f  p=%.4f  n=%d  (mean %.1f%%)'
                  % (slot, tag, r, p, len(xs), 100 * st.mean(ys)))
    xs, ys = [], []
    for y in YEARS:
        for tm, d in S[y].items():
            xs.append(d['heavy']); ys.append(d['fed'])
    r, p = perm_r(xs, ys)
    print('      how many receivers are FED vs heavy:  r=%+.3f  p=%.4f  n=%d  (mean %.2f men)'
          % (r, p, len(xs), st.mean(ys)))

    # ---- 3. the claim ---------------------------------------------------------------------
    print('\n3.  THE CLAIM -- among receivers who MOVED UP, is the gain bigger on heavy teams?')
    print('      Same team both seasons (a man who changed teams is a different question and is')
    print('      excluded).  %d+ routes in both.  Started WR2 or lower.' % MIN_BOTH)
    promo, stay = [], []
    for y in YEARS[:-1]:
        for tm in S[y]:
            if tm not in S[y + 1]:
                continue
            a, b = S[y][tm], S[y + 1][tm]
            for nm, r0 in a['rank'].items():
                if nm not in b['rank'] or a['routes'][nm] < MIN_BOTH or b['routes'][nm] < MIN_BOTH:
                    continue
                rec = dict(player=nm, tm=tm, y=y + 1, r0=r0, r1=b['rank'][nm],
                           d=b['share'][nm] - a['share'][nm],
                           dw=b['inwr'][nm] - a['inwr'][nm], wrpie=b['wr_share'],
                           heavy=b['heavy'], te=b['te_share'], rb=b['rb_share'])
                (promo if (rec['r1'] < r0 and r0 >= 2) else stay).append(rec)
    print('      %d promotions, %d who did not move up' % (len(promo), len(stay)))
    d, lo, hi, p = boot_diff([x['d'] for x in promo], [x['d'] for x in stay])
    print('      BASELINE -- a promotion is worth %+.1f share points against %+.1f for everyone'
          % (100 * st.mean([x['d'] for x in promo]), 100 * st.mean([x['d'] for x in stay])))
    print('      else:  difference %+.1f pp  CI [%+.1f, %+.1f]  p=%.4f   <-- the promotion is real'
          % (100 * d, 100 * lo, 100 * hi, p))
    wid = sorted(promo, key=lambda x: x['heavy'])
    k = len(wid) // 3
    light, heavy = wid[:k], wid[-k:]
    d, lo, hi, p = boot_diff([x['d'] for x in heavy], [x['d'] for x in light])
    print('      HEAVIEST third (%.2f) %+.1f pp   vs   LIGHTEST third (%.2f) %+.1f pp'
          % (st.mean([x['heavy'] for x in heavy]), 100 * st.mean([x['d'] for x in heavy]),
             st.mean([x['heavy'] for x in light]), 100 * st.mean([x['d'] for x in light])))
    print('      DIFFERENCE %+.1f pp  CI [%+.1f, %+.1f]  p=%.4f   (n=%d vs %d)'
          % (100 * d, 100 * lo, 100 * hi, p, len(heavy), len(light)))
    r, p = perm_r([x['heavy'] for x in promo], [x['d'] for x in promo])
    print('      continuous, PLAYER level:        r=%+.3f  p=%.4f  n=%d' % (r, p, len(promo)))
    # THE ROBUSTNESS TEST THAT FOUND THE MECHANISM.  Is the gap the promotion, or is it just that
    # a receiver room on a light team is a bigger slice of the offence to begin with?  Re-run the
    # same comparison on his share of the RECEIVERS' OWN targets, which holds the pie constant.
    d2, lo2, hi2, p2 = boot_diff([x['dw'] for x in heavy], [x['dw'] for x in light])
    print('      SAME TEST, INSIDE THE RECEIVER ROOM: heavy %+.1f  light %+.1f  diff %+.1f'
          '  CI [%+.1f, %+.1f]  p=%.4f'
          % (100 * st.mean([x['dw'] for x in heavy]), 100 * st.mean([x['dw'] for x in light]),
             100 * d2, 100 * lo2, 100 * hi2, p2))
    print('      -> NULL inside the room, so the whole gap is PIE SIZE: the receivers on the light')
    print('         teams held %.1f%% of all targets against %.1f%% on the heavy ones.'
          % (100 * st.mean([x['wrpie'] for x in light]), 100 * st.mean([x['wrpie'] for x in heavy])))
    byteam = {}
    for x in promo:
        byteam.setdefault((x['tm'], x['y']), []).append(x)
    xs = [v[0]['heavy'] for v in byteam.values()]
    ys = [st.mean([q['d'] for q in v]) for v in byteam.values()]
    r, p = perm_r(xs, ys)
    print('      CLUSTERED BY TEAM-SEASON (honest n): r=%+.3f  p=%.4f  n=%d' % (r, p, len(xs)))
    mdd = 2.8 * st.pstdev([x['d'] for x in promo]) / max(len(heavy), 1) ** .5
    print('      MINIMUM DETECTABLE DIFFERENCE at this n: about %.1f share points.' % (100 * mdd))
    print('      the biggest promotions on record, with their team\'s shape:')
    for x in sorted(promo, key=lambda x: -x['d'])[:10]:
        print('        %-24s %-4s %d  WR%d->WR%d  %+5.1f pp   heavy %.2f'
              % (x['player'], x['tm'], x['y'], x['r0'], x['r1'], 100 * x['d'], x['heavy']))

    # ---- 4. his other mechanism -----------------------------------------------------------
    print('\n4.  HIS OTHER MECHANISM -- does a pass-catching TE or back eat the WR2\'s share?')
    print('      unit: team-season.  Read the "of WR" rows: a share of the receivers\' own')
    print('      targets, so a fall there is CONCENTRATION and not just the 100% adding up.')
    for src_lab, src_key in (('TE share of targets', 'te_share'), ('RB share of targets', 'rb_share')):
        for slot in (1, 2, 3):
            for tag, field in (('of team', 'share'), ('of WR  ', 'inwr')):
                xs, ys = [], []
                for y in YEARS:
                    for tm, d in S[y].items():
                        if len(d['order']) >= slot:
                            xs.append(d[src_key]); ys.append(d[field][d['order'][slot - 1]['player']])
                r, p = perm_r(xs, ys)
                print('      %-20s vs WR%d %s:  r=%+.3f  p=%.4f  n=%d'
                      % (src_lab, slot, tag, r, p, len(xs)))
    print('\ndone.')


if __name__ == '__main__':
    main()
