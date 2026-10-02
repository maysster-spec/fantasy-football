#!/usr/bin/env python3
r"""b1_absence_bar.py -- catalog B1: every free player priced against an absence-aware bar.

THE CLAIM IN ITS TESTABLE FORM, written before the run (0.5a2):
  On Matt's 15 plus every free QB/RB/WR/TE in the newest WIRE_*.csv, weeks 1-14, with every man's
  weekly availability (the candidate included) drawn at the position absence rates in
  sheet_constants.json and an empty slot filled at the streamer rate, the RANKING of free players
  by what they add to the starting nine differs from the page's byes-only ranking.
FALSIFIER, fixed before the run: if the top five overall and the top man at every position are the
  same under both arms, the correction changes nothing the page acts on and B1 closes as a null.

BASELINE: arm A, byes only, hole charged at zero -- exactly what the shipped page computes with
  price() and bar_grid(). Arm A is ALSO run through this simulator with every rate at zero, and it
  must reproduce price() to the cent, or the harness is not exercising the page's object (0.2).
POPULATION of the rates: doc 297, prior-season top-24 RB / top-24 WR / top-12 QB / top-12 TE,
  read the following season, 2022-2025, n=318 player-seasons. A defence is zero by construction.
  There is no kicker rate in the constants file (deleted, doc 302); no kicker is in the wire file.
PAIRED: one availability draw per simulation, reused for the bare roster, for every candidate, and
  across every arm, so every difference carries only the noise of the thing that changed.

Stdlib only apart from sheet_engine, the production lineup code.
Run:  py b1_absence_bar.py          (about ten minutes at N=3000; B1_N=300 for a smoke test)
"""
import csv, glob, json, os, random, statistics, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.environ.get('B1_SCRIPTS', os.path.normpath(os.path.join(HERE, '..', '..')))
SRC = os.environ.get('B1_SRC', os.path.normpath(os.path.join(SCRIPTS, '..', 'Source')))
sys.path.insert(0, SCRIPTS)
import sheet_engine as se                                    # noqa: E402

N = int(os.environ.get('B1_N', '3000'))
SEED = int(os.environ.get('B1_SEED', '20260916'))
OUT = os.environ.get('B1_OUT', HERE)


def load_constants():
    c = json.load(open(os.path.join(SRC, 'sheet_constants.json'), encoding='utf-8'))
    ab = c['absence']
    rate = {k: float(v) for k, v in ab['rate'].items()}          # QB RB WR TE D/ST ; no K on purpose
    streamer = {k: float(v) for k, v in ab['streamer'].items()}  # QB RB WR TE D/ST ; no K on purpose
    relief = float(c['seat']['relief_ppg'])                      # 12.13, supersedes 11.2 (doc 302)
    return rate, streamer, relief


def load_roster(rate):
    mine = {}
    with open(os.path.join(SRC, 'MY_ROSTER.csv'), newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            mine[str(r['espn_id']).strip()] = r['player']
    roster = [dict(rate[p]) for p in mine if p in rate]
    assert len(roster) == len(mine), f'{len(mine) - len(roster)} of his men carry no projection'
    return roster


def load_wire(rate):
    hits = sorted(glob.glob(os.path.join(SRC, 'WIRE_*.csv')))
    assert hits, 'no WIRE_*.csv in Source'
    path = hits[-1]
    priced, unpriced = [], []
    with open(path, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            pid = str(r['espn_id']).strip()
            if pid in rate:
                c = dict(rate[pid])
                c['status'] = (r.get('status') or '').strip()
                c['owned_pct'] = r.get('owned_pct', '')
                c['screen'] = (r.get('screen') or '').strip()
                priced.append(c)
            else:
                unpriced.append((r['player'], r['pos'], r['team'], (r.get('status') or '').strip()))
    return os.path.basename(path), priced, unpriced


def page_prices(roster, cands):
    """What the shipped page prints: price() against bar_grid(), byes only."""
    bar = se.bar_grid(roster)
    return {c['espn_id']: se.price(c, bar)[1] for c in cands}


def simulate(roster, cands, rates, streamer, n, seed, fill, relief=None, cuff=None, probe=True):
    """Paired draw. Returns per-candidate per-draw season gains, per-draw bare totals and the mean
    absence-aware bar per (pos, week).

    fill    : charge an empty slot at the streamer rate instead of zero
    relief  : if set, the handcuff scores max(own, relief) in the weeks the man ahead is out
    cuff    : (backup name, man-ahead name)
    """
    rng = random.Random(seed)
    W = se.WEEKS
    nr, nc = len(roster), len(cands)
    r_rate = [rates.get(p['pos'], 0.0) for p in roster]
    c_rate = [rates.get(p['pos'], 0.0) for p in cands]
    bi = ai = None
    if cuff:
        names = {p['name']: i for i, p in enumerate(roster)}
        bi, ai = names.get(cuff[0]), names.get(cuff[1])
    gains = [[0.0] * n for _ in range(nc)]
    bare = [0.0] * n
    barsum = {pos: {w: 0.0 for w in W} for pos in se.POS}
    probes = {pos: {'name': 'PROBE', 'pos': pos, 'tm': '', 'bye': 0, 'wk': 45.0} for pos in se.POS}
    for d in range(n):
        av = [[rng.random() >= r_rate[i] for _ in W] for i in range(nr)]
        cav = [[rng.random() >= c_rate[j] for _ in W] for j in range(nc)]
        for wi, w in enumerate(W):
            here = []
            for i, p in enumerate(roster):
                if not av[i][wi]:
                    continue
                if relief is not None and i == bi and (not av[ai][wi] or roster[ai]['bye'] == w):
                    p = dict(p, wk=max(p['wk'], relief))
                here.append(p)
            base, empty = se.week_points(here, w)
            if fill:
                base += sum(streamer.get(lab, 0.0) for lab in empty)
            bare[d] += base
            for j, c in enumerate(cands):
                if c['bye'] == w or not cav[j][wi]:
                    continue
                t, e2 = se.week_points(here + [c], w)
                if fill:
                    t += sum(streamer.get(lab, 0.0) for lab in e2)
                g = t - base
                if g > 0:
                    gains[j][d] += g
            if probe:
                for pos in se.POS:
                    t, e2 = se.week_points(here + [probes[pos]], w)
                    if fill:
                        t += sum(streamer.get(lab, 0.0) for lab in e2)
                    barsum[pos][w] += 45.0 - (t - base)
    bar = {pos: {w: round(barsum[pos][w] / n, 2) for w in W} for pos in se.POS}
    return gains, bare, bar


def mean_se(v):
    m = statistics.mean(v)
    s = statistics.stdev(v) / (len(v) ** 0.5) if len(v) > 1 else 0.0
    return m, s


def rank(vals):
    """1 = highest. Ties broken by name so the ordering is reproducible."""
    order = sorted(vals, key=lambda k: (-vals[k][0], vals[k][1]))
    return {k: i + 1 for i, k in enumerate(order)}


def main():
    t0 = time.time()
    rate, why = se.rates(SRC)
    assert not why, why
    rates_abs, streamer, relief = load_constants()
    roster = load_roster(rate)
    wirefile, cands, unpriced = load_wire(rate)
    print(f'B1 -- every free player against an absence-aware bar    N={N} seed={SEED}')
    print(f'  roster {len(roster)} men, {wirefile}: {len(cands)} priced, {len(unpriced)} unpriced')
    print('  absence rates:', ' '.join(f'{k} {v:.1%}' for k, v in sorted(rates_abs.items())))
    print('  streamer     :', ' '.join(f'{k} {v}' for k, v in sorted(streamer.items())))
    print(f'  handcuff relief {relief} (Mike Washington Jr. behind Ashton Jeanty)')

    page = page_prices(roster, cands)
    zero = {k: 0.0 for k in rates_abs}
    hard = {k: min(0.95, v * (2.98 / 1.79)) for k, v in rates_abs.items()}   # doc 111's level
    cuff = ('Mike Washington Jr.', 'Ashton Jeanty')
    arms = [
        ('A', 'byes only, hole at zero (the page)', zero, False, None),
        ('B', 'measured absences, hole at zero', rates_abs, False, None),
        ('C', 'measured absences, hole streamed', rates_abs, True, None),
        ('D', 'C plus handcuff relief 12.13', rates_abs, True, relief),
        ('E', 'doc 111 rates, hole streamed', hard, True, None),
    ]
    res = {}
    for tag, label, r, fl, rel in arms:
        t1 = time.time()
        gains, bare, bar = simulate(roster, cands, r, streamer, N, SEED, fl, rel, cuff)
        res[tag] = (label, gains, bare, bar)
        print(f'  arm {tag} done in {time.time() - t1:.0f}s: bare roster {statistics.mean(bare):.1f}')

    # CONTROL: arm A must reproduce price() to the cent for every candidate.
    worst = 0.0
    for j, c in enumerate(cands):
        worst = max(worst, abs(statistics.mean(res['A'][1][j]) - page[c['espn_id']]))
    print(f'  CONTROL arm A vs page price(): largest gap {worst:.4f}  '
          f'{"PASS" if worst < 0.05 else "FAIL -- harness is not the page"}')
    assert worst < 0.05

    # the table
    rows = []
    for j, c in enumerate(cands):
        row = {'espn_id': c['espn_id'], 'player': c['name'], 'pos': c['pos'], 'team': c['tm'],
               'bye': c['bye'], 'status': c['status'], 'proj_per_game': round(c['wk'], 2),
               'page_price': round(page[c['espn_id']], 2)}
        for tag in 'ABCDE':
            m, s = mean_se(res[tag][1][j])
            row[f'price_{tag}'] = round(m, 2)
            row[f'se_{tag}'] = round(s, 3)
        # paired difference C - A, its own SE (the draw is shared)
        dif = [x - y for x, y in zip(res['C'][1][j], res['A'][1][j])]
        m, s = mean_se(dif)
        row['C_minus_A'] = round(m, 2)
        row['se_C_minus_A'] = round(s, 3)
        rows.append(row)
    for tag in 'ABCDE':
        rk = rank({r['espn_id']: (r[f'price_{tag}'], r['player']) for r in rows})
        for r in rows:
            r[f'rank_{tag}'] = rk[r['espn_id']]
        for pos in ('QB', 'RB', 'WR', 'TE'):
            sub = {r['espn_id']: (r[f'price_{tag}'], r['player']) for r in rows if r['pos'] == pos}
            rk = rank(sub)
            for r in rows:
                if r['pos'] == pos:
                    r[f'posrank_{tag}'] = rk[r['espn_id']]
    for r in rows:
        r['rank_move_A_to_C'] = r['rank_A'] - r['rank_C']          # positive = climbs
        r['posrank_move_A_to_C'] = r['posrank_A'] - r['posrank_C']
    rows.sort(key=lambda r: r['rank_C'])

    cols = ['rank_C', 'rank_A', 'rank_move_A_to_C', 'player', 'pos', 'team', 'bye', 'status',
            'proj_per_game', 'page_price', 'price_A', 'price_B', 'price_C', 'price_D', 'price_E',
            'C_minus_A', 'se_C_minus_A', 'se_C', 'posrank_A', 'posrank_C', 'posrank_move_A_to_C',
            'rank_B', 'rank_D', 'rank_E', 'espn_id']
    out_csv = os.path.join(OUT, 'B1_free_pool_prices.csv')
    with open(out_csv, 'w', newline='', encoding='utf-8') as fh:
        wr = csv.DictWriter(fh, fieldnames=cols, extrasaction='ignore')
        wr.writeheader()
        wr.writerows(rows)
    with open(os.path.join(OUT, 'B1_unpriced.csv'), 'w', newline='', encoding='utf-8') as fh:
        wr = csv.writer(fh)
        wr.writerow(['player', 'pos', 'team', 'status', 'why'])
        for nm, pos, tm, st in unpriced:
            wr.writerow([nm, pos, tm, st, 'no ESPN projection in the newest pull; not priced by the page either'])

    # the bar grid, page vs expected under C
    bar_page = se.bar_grid(roster)
    with open(os.path.join(OUT, 'B1_bar_grid.csv'), 'w', newline='', encoding='utf-8') as fh:
        wr = csv.writer(fh)
        wr.writerow(['pos', 'arm'] + [f'wk{w}' for w in se.WEEKS])
        for pos in se.POS:
            wr.writerow([pos, 'page (byes only)'] + [bar_page[pos][w] for w in se.WEEKS])
            for tag in 'BCDE':
                wr.writerow([pos, f'mean bar, arm {tag}'] + [res[tag][3][pos][w] for w in se.WEEKS])

    # THE FALSIFIER
    topA = [r['player'] for r in sorted(rows, key=lambda r: r['rank_A'])[:5]]
    topC = [r['player'] for r in rows[:5]]
    firstA = {pos: next(r['player'] for r in sorted(rows, key=lambda r: r['rank_A']) if r['pos'] == pos)
              for pos in ('QB', 'RB', 'WR', 'TE')}
    firstC = {pos: next(r['player'] for r in rows if r['pos'] == pos) for pos in ('QB', 'RB', 'WR', 'TE')}
    print('\nTOP FIVE OVERALL')
    print('  page (A):', ' | '.join(topA))
    print('  corrected (C):', ' | '.join(topC))
    print('TOP MAN BY POSITION')
    for pos in ('QB', 'RB', 'WR', 'TE'):
        print(f'  {pos}: page {firstA[pos]:<24} corrected {firstC[pos]}')
    null = (topA == topC) and (firstA == firstC)
    print(f'\nFALSIFIER: top five and top man per position identical under A and C -> {null}')
    print('  VERDICT:', 'NULL -- the correction changes nothing the page acts on' if null
          else 'the correction changes what the page would recommend')

    # EVERY ROW WHOSE ORDER CHANGES. The page ties most of the pool at zero, and a tie is not an
    # order, so "order changes" means a STRICT INVERSION: some other row the page put strictly
    # above him is now strictly below him, or the reverse. Counted pairwise; a row is listed once,
    # with the number of men it swapped places with and the one it swapped furthest with.
    pa = {r['espn_id']: r['price_A'] for r in rows}
    pc = {r['espn_id']: r['price_C'] for r in rows}
    nm = {r['espn_id']: r['player'] for r in rows}
    swaps = {k: [] for k in pa}
    keys = list(pa)
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            a, b = keys[i], keys[j]
            da, dc = pa[a] - pa[b], pc[a] - pc[b]
            if (da > 0 and dc < 0) or (da < 0 and dc > 0):
                swaps[a].append(b)
                swaps[b].append(a)
    for r in rows:
        s = swaps[r['espn_id']]
        r['n_inversions'] = len(s)
        r['left_zero'] = int(r['price_A'] == 0 and r['price_C'] > 0)
    moved = [r for r in rows if r['n_inversions'] > 0]
    left_zero = [r for r in rows if r['left_zero']]
    cols = cols + ['n_inversions', 'left_zero']
    with open(os.path.join(OUT, 'B1_order_changes.csv'), 'w', newline='', encoding='utf-8') as fh:
        wr = csv.DictWriter(fh, fieldnames=cols, extrasaction='ignore')
        wr.writeheader()
        wr.writerows(moved)
    with open(os.path.join(OUT, 'B1_free_pool_prices.csv'), 'w', newline='', encoding='utf-8') as fh:
        wr = csv.DictWriter(fh, fieldnames=cols, extrasaction='ignore')
        wr.writeheader()
        wr.writerows(rows)
    print(f'\nROWS IN A STRICT INVERSION (page order vs corrected order): {len(moved)} of {len(rows)}; '
          f'rows the page priced at zero that are now above zero: {len(left_zero)} of {len(rows)}')
    print(f"  {'player':<26}{'pos':<4}{'page':>7}{'corr':>7}{'diff':>7}{'+/-':>6}  overall  by position  swaps")
    for r in sorted(moved, key=lambda r: -r['n_inversions'])[:40]:
        print(f"  {r['player']:<26}{r['pos']:<4}{r['price_A']:>7.2f}{r['price_C']:>7.2f}"
              f"{r['C_minus_A']:>7.2f}{r['se_C_minus_A']:>6.2f}  {r['rank_A']:>3}->{r['rank_C']:<3}"
              f"  {r['posrank_A']:>3}->{r['posrank_C']:<3}  {r['n_inversions']}")
    print('\nTOP TWENTY UNDER THE CORRECTION (C), with the page price and every arm')
    print(f"  {'player':<26}{'pos':<4}{'a game':>7}{'page':>7}{'B':>7}{'C':>7}{'D':>7}{'E':>7}")
    for r in rows[:20]:
        print(f"  {r['player']:<26}{r['pos']:<4}{r['proj_per_game']:>7.2f}{r['price_A']:>7.2f}"
              f"{r['price_B']:>7.2f}{r['price_C']:>7.2f}{r['price_D']:>7.2f}{r['price_E']:>7.2f}")
    print('\nTOP TEN ON THE PAGE (A), and where each went')
    for r in sorted(rows, key=lambda r: r['rank_A'])[:10]:
        print(f"  {r['player']:<26}{r['pos']:<4}{r['price_A']:>7.2f} -> {r['price_C']:>6.2f}   "
              f"rank {r['rank_A']:>3} -> {r['rank_C']:<3}")
    print(f"  {'player':<26}{'pos':<4}{'page':>7}{'corr':>7}{'diff':>7}{'+/-':>6}  overall  by position")
    for r in moved[:40]:
        print(f"  {r['player']:<26}{r['pos']:<4}{r['price_A']:>7.2f}{r['price_C']:>7.2f}"
              f"{r['C_minus_A']:>7.2f}{r['se_C_minus_A']:>6.2f}  {r['rank_A']:>3}->{r['rank_C']:<3}"
              f"  {r['posrank_A']:>3}->{r['posrank_C']:<3}")
    pos_summary = {}
    for pos in ('QB', 'RB', 'WR', 'TE'):
        sub = [r for r in rows if r['pos'] == pos]
        pos_summary[pos] = {'n': len(sub),
                            'mean_page': round(statistics.mean(r['price_A'] for r in sub), 2),
                            'mean_C': round(statistics.mean(r['price_C'] for r in sub), 2),
                            'zero_on_page': sum(1 for r in sub if r['price_A'] == 0),
                            'zero_under_C': sum(1 for r in sub if r['price_C'] == 0)}
    print('\nBY POSITION (mean price, rows priced at zero)')
    for pos, s in pos_summary.items():
        print(f"  {pos}: n={s['n']:<4} page {s['mean_page']:>6.2f} -> C {s['mean_C']:>6.2f}   "
              f"zero rows {s['zero_on_page']} -> {s['zero_under_C']}")
    json.dump({'N': N, 'seed': SEED, 'wire': wirefile, 'n_priced': len(cands), 'n_unpriced': len(unpriced),
               'top5_A': topA, 'top5_C': topC, 'first_A': firstA, 'first_C': firstC, 'null': null,
               'n_moved': len(moved), 'by_position': pos_summary,
               'bare_roster': {t: round(statistics.mean(res[t][2]), 1) for t in 'ABCDE'},
               'arms': {t: res[t][0] for t in 'ABCDE'}},
              open(os.path.join(OUT, 'B1_summary.json'), 'w'), indent=1)
    print(f'\nwrote B1_free_pool_prices.csv, B1_order_changes.csv, B1_unpriced.csv, B1_bar_grid.csv, '
          f'B1_summary.json in {time.time() - t0:.0f}s')


if __name__ == '__main__':
    main()
