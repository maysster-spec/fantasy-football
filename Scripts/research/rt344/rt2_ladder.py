#!/usr/bin/env python3
"""RED TEAM ITEM 2 -- the drop-cost ladder: which counterfactual, and are K and D/ST priced?

The page's ladder (sheet_engine.py, 'WHAT EVERY MAN YOU OWN COSTS TO DROP'):
    net      = season(roster) - season(roster - man + BEST FREE BODY AT HIS POSITION)
    absence  = rate[pos] * (non-bye weeks) * max(0, man.wk - streamer[pos])     (real_price)
    printed  = net + absence
TESTABLE FORM: for the drops the page prints at 0.0, the same swap priced in one currency (the man
removed, a streamer body always in the pool, byes only) differs by more than 0.5. And: K and D/ST
either print a number (then the code comment 'NOT priced' is false) or print 'not priced'.
Four counterfactuals per man, byes only, deterministic:
  A  nobody takes the seat                      (drop_costs(), doc 240)
  B  the best free body at his position takes it (the page's ladder, doc 327 s3 'page')
  C  a streamer body at his position takes it    (the one-currency object, no absences)
  D  as B, but the best free body has ALREADY been added to the roster (the pool is depleted by the
     add that motivated the drop) -- the next-best free body takes the seat
"""
import csv, json, os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))   # every path resolves against this file (0.4)
SCRIPTS = os.environ.get('RT_SCRIPTS', os.path.normpath(os.path.join(HERE, '..', '..')))
SRC = os.environ.get('RT_SRC', os.path.normpath(os.path.join(SCRIPTS, '..', 'Source')))
OUT = os.environ.get('RT_OUT', HERE)
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, SCRIPTS)
import sheet_engine as se                                    # noqa: E402

c = json.load(open(os.path.join(SRC, 'sheet_constants.json'), encoding='utf-8'))
RATE = {k: float(v) for k, v in c['absence']['rate'].items()}
STRM = {k: float(v) for k, v in c['absence']['streamer'].items()}
rate, why = se.rates(SRC)
mine = {}
for r in csv.DictReader(open(os.path.join(SRC, 'MY_ROSTER.csv'), newline='', encoding='utf-8-sig')):
    mine[str(r['espn_id']).strip()] = r['player']
roster = [dict(rate[p]) for p in mine if p in rate]
owned = set(mine)
for r in csv.DictReader(open(os.path.join(SRC, 'LEAGUE_ROSTERS.csv'), newline='', encoding='utf-8-sig')):
    owned.add(str(r['espn_id']).strip())
free = [dict(v) for pid, v in rate.items() if pid not in owned]
bestfree = {}
for f in free:
    if f['pos'] not in bestfree or f['wk'] > bestfree[f['pos']]['wk']:
        bestfree[f['pos']] = f
second = {}
for f in free:
    if f['pos'] in bestfree and f is not bestfree[f['pos']] and f['name'] != bestfree[f['pos']]['name']:
        if f['pos'] not in second or f['wk'] > second[f['pos']]['wk']:
            second[f['pos']] = f
print('best free body by position:', {p: f"{v['name']} {v['wk']:.1f}" for p, v in bestfree.items()})
print('second free body:', {p: f"{v['name']} {v['wk']:.1f}" for p, v in second.items()})

base = se.season(roster)
strm_body = lambda pos: {'name': f'STREAMER {pos}', 'pos': pos, 'tm': '', 'bye': 0, 'wk': STRM[pos]}
rows = []
for pl in roster:
    rest = [x for x in roster if x is not pl]
    pos = pl['pos']
    A = base - se.season(rest)
    rep = bestfree.get(pos)
    B = None if rep is None else base - se.season(rest + [rep])
    Cc = None if pos not in STRM else base - se.season(rest + [strm_body(pos)])
    rep2 = second.get(pos)
    # D: the best free body is already on the roster (added), so the drop leaves the second-best to fill
    D = None
    if rep is not None:
        base_d = se.season(roster + [rep])
        D = base_d - se.season(rest + [rep] + ([rep2] if rep2 else []))
    wks = len([w for w in se.WEEKS if pl['bye'] != w])
    absence = (RATE[pos] * wks * max(0.0, pl['wk'] - STRM[pos])) if pos in RATE and pos in STRM else 0.0
    rows.append(dict(name=pl['name'], pos=pos, wk=round(pl['wk'], 2), bye=pl['bye'],
                     A_nobody=round(A, 1), B_page_net=None if B is None else round(B, 1),
                     absence_term=round(absence, 1),
                     B_page_printed=None if B is None else round(B + absence, 1),
                     C_streamer=None if Cc is None else round(Cc, 1),
                     C_plus_absence=None if Cc is None else round(Cc + absence, 1),
                     D_after_add=None if D is None else round(D, 1),
                     replaced_by=None if rep is None else f"{rep['name']} {rep['wk']:.1f}",
                     then_by=None if rep2 is None else f"{rep2['name']} {rep2['wk']:.1f}"))
rows.sort(key=lambda r: (r['B_page_printed'] is None, r['B_page_printed'] or 0))
with open(os.path.join(OUT, 'RT2_ladder_four_ways.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print(f"\n{'man':<22}{'pos':<5}{'wk':>6}{'A nobody':>9}{'B net':>7}{'abs':>6}{'B page':>8}{'C strm':>8}{'C+abs':>7}{'D after add':>12}  replaced by / then")
for r in rows:
    f = lambda v: '   n/p' if v is None else f'{v:6.1f}'
    print(f"{r['name']:<22}{r['pos']:<5}{r['wk']:>6.1f}{f(r['A_nobody']):>9}{f(r['B_page_net']):>7}{r['absence_term']:>6.1f}"
          f"{f(r['B_page_printed']):>8}{f(r['C_streamer']):>8}{f(r['C_plus_absence']):>7}{f(r['D_after_add']):>12}  {r['replaced_by']} / {r['then_by']}")

# ---- the double count, on the page's own top swap at each position --------------------------
print('\nTHE DOUBLE COUNT: the page shows an add row (price against the bar) and a drop row (netted '
      'against the best free body). Adding that same best free body and dropping the man:')
bar = se.bar_grid(roster)
for pos, rep in bestfree.items():
    cheap = [r for r in rows if r['pos'] == pos and r['B_page_printed'] is not None]
    if not cheap:
        continue
    victim = min(cheap, key=lambda r: r['B_page_printed'])
    vpl = next(p for p in roster if p['name'] == victim['name'])
    add_row = se.price(rep, bar)[1]
    true_swap = se.season([x for x in roster if x is not vpl] + [rep]) - base
    print(f"  {pos:5s} add {rep['name']} (page add value {add_row:5.1f}) and drop {victim['name']} "
          f"(page drop cost {victim['B_page_printed']:5.1f}): reader nets {add_row - victim['B_page_printed']:+5.1f}; "
          f"the actual swap is {true_swap:+5.1f}")
json.dump(dict(rows=rows, bestfree={p: v['name'] for p, v in bestfree.items()}), open(os.path.join(OUT, 'RT2_summary.json'), 'w'), indent=1)
