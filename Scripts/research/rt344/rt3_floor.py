#!/usr/bin/env python3
"""RED TEAM ITEM 3 -- is the printed second figure a FLOOR?

The page prints, for a bye-week fill: alt = tot - len(empty) * min(his rate, streamer), where tot is
price() (byes only, empty slot at zero) and empty is the weeks he fills a slot nobody else can.
Doc 321 calls alt a FLOOR on the simulated figure (doc 319 arm C: absences drawn for everybody, the
candidate too, an empty slot filled at the streamer rate).

TESTABLE FORM: for at least one free player on the current wire, alt exceeds arm C by more than two
paired standard errors. One such row and the word "floor" is wrong.
Two mechanisms can do it, and both are measured separately below:
  (1) the candidate's OWN absence: arm C removes him in ~14-17% of his weeks, alt never does;
  (2) a week whose bar is below the streamer rate: alt credits him against the bar, a streamer-in-pool
      currency credits him only against the streamer. (Arm C does not have a streamer in the pool,
      so (2) is measured against the one-currency arm U from doc 327, also run here.)
Stdlib + the production sheet_engine. Paired: one availability draw reused for every candidate and arm.
"""
import csv, glob, json, os, random, statistics, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))   # every path resolves against this file (0.4)
SCRIPTS = os.environ.get('RT_SCRIPTS', os.path.normpath(os.path.join(HERE, '..', '..')))
SRC = os.environ.get('RT_SRC', os.path.normpath(os.path.join(SCRIPTS, '..', 'Source')))
OUT = os.environ.get('RT_OUT', HERE)
N = int(os.environ.get('RT_N', '1500'))
SEED = int(os.environ.get('RT_SEED', '20260917'))
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, SCRIPTS)
import sheet_engine as se                                    # noqa: E402

c = json.load(open(os.path.join(SRC, 'sheet_constants.json'), encoding='utf-8'))
RATE = {k: float(v) for k, v in c['absence']['rate'].items()}
STRM = {k: float(v) for k, v in c['absence']['streamer'].items()}
rate, why = se.rates(SRC)
print('rates:', why)

mine = {}
with open(os.path.join(SRC, 'MY_ROSTER.csv'), newline='', encoding='utf-8-sig') as fh:
    for r in csv.DictReader(fh):
        mine[str(r['espn_id']).strip()] = r['player']
roster = [dict(rate[p]) for p in mine if p in rate]
print(f'roster priced: {len(roster)} of {len(mine)}:',
      ', '.join(f"{p['name']} {p['pos']} {p['wk']:.1f} bye {p['bye']}" for p in roster))

# THE PAGE'S FREE POOL IS ESPN'S AVAILABLE LIST, NOT THE WIRE FILE: wire.py builds freerows from
# every priced man in `avail`, which carries D/ST and K. Without the ESPN session the nearest object
# is every priced man on nobody's roster (doc 327 did the same): rates() minus LEAGUE_ROSTERS.csv.
wire = os.path.join(SRC, 'LEAGUE_ROSTERS.csv')
owned = set()
with open(wire, newline='', encoding='utf-8-sig') as fh:
    for r in csv.DictReader(fh):
        owned.add(str(r['espn_id']).strip())
owned |= set(mine)
cands = [dict(v) for pid, v in rate.items() if pid not in owned and v['pos'] in STRM]
print(f'free pool = rates() minus LEAGUE_ROSTERS.csv: {len(cands)} men at a position with a streamer rate; '
      f'by position {dict(__import__("collections").Counter(c["pos"] for c in cands))}')

# ---- the page's two figures -------------------------------------------------------------------
bar = se.bar_grid(roster)
page = {}
for cd in cands:
    wkp, tot = se.price(cd, bar)
    ws = [w for w in se.WEEKS if (wkp[w] or 0) > 0.049]
    empty = [w for w in ws if bar[cd['pos']][w] == 0]
    alt = round(tot - len(empty) * min(cd['wk'], STRM[cd['pos']]), 2)
    page[cd['espn_id']] = dict(tot=tot, alt=alt, empty=empty, ws=ws)

print('\nweeks where 0 < bar < streamer (mechanism 2 can bite):')
for pos in se.POS:
    if pos in STRM:
        low = [w for w in se.WEEKS if 0 < bar[pos][w] < STRM[pos]]
        print(f'  {pos:5s} streamer {STRM[pos]:5.2f}  bars:', ' '.join(f'{bar[pos][w]:.1f}' for w in se.WEEKS),
              ('  <-- weeks ' + str(low)) if low else '')


# ---- the paired simulation: arms C (doc 319) and U (doc 327) ----------------------------------
def simulate(n, seed):
    rng = random.Random(seed)
    W = se.WEEKS
    nr, nc = len(roster), len(cands)
    r_rate = [RATE.get(p['pos'], 0.0) for p in roster]
    c_rate = [RATE.get(p['pos'], 0.0) for p in cands]
    gC = [[0.0] * n for _ in range(nc)]
    gU = [[0.0] * n for _ in range(nc)]
    gA = [[0.0] * n for _ in range(nc)]            # byes only, hole at zero: must equal price()
    strm_bodies = [{'name': f'STREAMER {p}', 'pos': p, 'tm': '', 'bye': 0, 'wk': STRM[p]} for p in STRM]
    for d in range(n):
        av = [[rng.random() >= r_rate[i] for _ in W] for i in range(nr)]
        cav = [[rng.random() >= c_rate[j] for _ in W] for j in range(nc)]
        for wi, w in enumerate(W):
            here = [p for i, p in enumerate(roster) if av[i][wi]]
            baseC, emptyC = se.week_points(here, w)
            baseC += sum(STRM.get(lab, 0.0) for lab in emptyC)
            baseU, _ = se.week_points(here + strm_bodies, w)
            baseA, _ = se.week_points(roster, w)
            for j, cd in enumerate(cands):
                if cd['bye'] == w:
                    continue
                if d == 0:
                    t, _ = se.week_points(roster + [cd], w)
                    gA[j][0] += max(0.0, t - baseA)
                if not cav[j][wi]:
                    continue
                t, e2 = se.week_points(here + [cd], w)
                t += sum(STRM.get(lab, 0.0) for lab in e2)
                gC[j][d] += max(0.0, t - baseC)
                t, _ = se.week_points(here + strm_bodies + [cd], w)
                gU[j][d] += max(0.0, t - baseU)
    return gA, gC, gU


t0 = time.time()
gA, gC, gU = simulate(N, SEED)
print(f'\nsimulated {N} paired draws for {len(cands)} men in {time.time() - t0:.0f}s')

# CONTROL: arm A (no absences, hole at zero) must reproduce price() -- tolerance is the page's 0.1 rounding
worst = max(abs(gA[j][0] - page[cd['espn_id']]['tot']) for j, cd in enumerate(cands))
print(f'CONTROL arm A vs price(): largest gap {worst:.3f} over {len(cands)} men '
      f'({"PASS" if worst < 0.2 else "FAIL"})')

rows = []
for j, cd in enumerate(cands):
    mC, seC = statistics.mean(gC[j]), (statistics.stdev(gC[j]) / N ** 0.5 if N > 1 else 0)
    mU = statistics.mean(gU[j])
    seU = statistics.stdev(gU[j]) / N ** 0.5 if N > 1 else 0
    pg = page[cd['espn_id']]
    rows.append(dict(name=cd['name'], pos=cd['pos'], wk=round(cd['wk'], 2), bye=cd['bye'],
                     page_tot=pg['tot'], page_alt=pg['alt'], n_empty=len(pg['empty']),
                     armC=round(mC, 3), seC=round(seC, 3), armU=round(mU, 3), seU=round(seU, 3),
                     alt_minus_C=round(pg['alt'] - mC, 3), alt_minus_U=round(pg['alt'] - mU, 3),
                     z_C=round((pg['alt'] - mC) / seC, 2) if seC > 0 else None,
                     z_U=round((pg['alt'] - mU) / seU, 2) if seU > 0 else None))
rows.sort(key=lambda r: -r['alt_minus_C'])
with open(os.path.join(OUT, 'RT3_floor_vs_sim.csv'), 'w', newline='') as fh:
    wtr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    wtr.writeheader()
    wtr.writerows(rows)

over_C = [r for r in rows if r['z_C'] is not None and r['z_C'] > 2 and r['alt_minus_C'] > 0.05]
over_U = [r for r in rows if r['z_U'] is not None and r['z_U'] > 2 and r['alt_minus_U'] > 0.05]
fills = [r for r in rows if r['n_empty'] > 0]
print(f'\nmen whose printed alt EXCEEDS arm C by >2 SE: {len(over_C)} of {len(rows)}; '
      f'among the {len(fills)} bye-week fills (the rows the sentence is printed for): '
      f'{sum(1 for r in fills if r in over_C)}')
print(f'men whose printed alt EXCEEDS the one-currency arm U by >2 SE: {len(over_U)} of {len(rows)}')
print(f"\n{'player':<24}{'pos':<4}{'a gm':>6}{'tot':>7}{'alt':>7}{'emp':>4}{'C':>8}{'seC':>6}{'U':>8}{'alt-C':>8}{'alt-U':>8}")
for r in rows[:25]:
    print(f"{r['name']:<24}{r['pos']:<4}{r['wk']:>6.1f}{r['page_tot']:>7.2f}{r['page_alt']:>7.2f}{r['n_empty']:>4}"
          f"{r['armC']:>8.2f}{r['seC']:>6.2f}{r['armU']:>8.2f}{r['alt_minus_C']:>8.2f}{r['alt_minus_U']:>8.2f}")
print('\n... and the bye-week fills the page prints the sentence for:')
for r in sorted(fills, key=lambda r: -r['page_tot'])[:12]:
    print(f"{r['name']:<24}{r['pos']:<4}{r['wk']:>6.1f}{r['page_tot']:>7.2f}{r['page_alt']:>7.2f}{r['n_empty']:>4}"
          f"{r['armC']:>8.2f}{r['seC']:>6.2f}{r['armU']:>8.2f}{r['alt_minus_C']:>8.2f}{r['alt_minus_U']:>8.2f}")
json.dump(dict(n_draws=N, n_cands=len(rows), control_gap=round(worst, 4), over_C=len(over_C), over_U=len(over_U),
               fills=len(fills), fills_over_C=sum(1 for r in fills if r in over_C),
               worst_over_C=rows[0], roster=[p['name'] for p in roster], wire=os.path.basename(wire)),
          open(os.path.join(OUT, 'RT3_summary.json'), 'w'), indent=1)
print(f'\nwrote {OUT}/RT3_floor_vs_sim.csv and RT3_summary.json')
