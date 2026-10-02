#!/usr/bin/env python3
r"""j1_one_currency.py -- JOB 1: every lane of the priority list in one currency, net of its drop.

THE CLAIM IN ITS TESTABLE FORM (REDTEAM_TASKING_PROMPT.md section B, fixed before the run):
  on the live wire, re-pricing all three lanes of the priority list in one currency changes the
  TOP FIVE of the list.
FALSIFIER: if the top five, and the top man in each of the three lanes, are the same under both
  arms, the lane mixing costs nothing the page acts on and JOB 1 closes as a null.

THE PAGE'S CURRENCY (arm P), reproduced here from sheet_engine's own functions so the control is
the live list and not a description of it:
  fill  = price(): sum over weeks of max(0, his rate - the bar), byes only, an empty slot at ZERO
  bet   = odds x bet(): the mean per-week gain at the hit rate, times the weeks a hit lasts
  seat  = p_opens x the mean per-week gain at the relief rate, times the weeks a seat stays open
  and nothing is charged for the drop; the drop is a separate line.

ONE CURRENCY (arm U): the change in weeks-1-to-14 starting-nine points from making the SWAP
  (add him, drop one of your own), with
  - every man's weekly availability drawn at the constants' absence rates (the candidate too),
  - a waiver body at the streamer rate in the lineup pool every week at every position that has
    one, so no slot is ever empty and nobody below the streamer ever starts,
  - a bet scored at the hit rate for the measured number of weeks a hit lasts, with the odds,
    and at his own projection otherwise; a seat scored the same way at the relief rate,
  - ONE draw reused across every cell (every candidate, every drop, every lane), so every
    difference is paired.
  Each row's number is the best swap available for him: the max over the fifteen drops.
  U_gross, the same arithmetic with no drop charged, is kept beside it.

POPULATION (0.6): every free player ESPN prices, from the newest projection pull minus the twelve
rosters in LEAGUE_ROSTERS.csv (the page's own free pool); the wire file supplies the screens, the
workload signals, the touches and the status for the men it carries. Rates [INHERITED] from
sheet_constants.json: absence (doc 297, n=318), streamer (doc 92 / doc 12), hit size (doc 276),
seat (doc 302). Matt's DO NOT rulings and the page's multi-week-injury demotion apply to every arm.

Stdlib + numpy + sheet_engine.  Run:  py j1_one_currency.py   (J1_N=200 for a smoke test)
"""
import csv, glob, json, os, random, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.environ.get('J1_SCRIPTS', os.path.normpath(os.path.join(HERE, '..', '..')))
SRC = os.environ.get('J1_SRC', os.path.normpath(os.path.join(SCRIPTS, '..', 'Source')))
OUT = os.environ.get('J1_OUT', HERE)
N = int(os.environ.get('J1_N', '1500'))
SEED = int(os.environ.get('J1_SEED', '20260916'))
WEEK = int(os.environ.get('J1_WEEK', '2'))
sys.path.insert(0, SCRIPTS)
import sheet_engine as se                                    # noqa: E402

FILL_LANE, BET_LANE, SEAT_LANE = 'fill', 'bet', 'seat'
MULTIWEEK = frozenset({'INJURY_RESERVE', 'SUSPENSION', 'PUP', 'NOT_ACTIVE'})


# ------------------------------------------------------------------ inputs, the page's own way
def load_all():
    rate, why = se.rates(SRC)
    assert not why, why
    const, cwhy = se.load_constants(SRC)
    assert not cwhy, cwhy
    mine = {}
    with open(os.path.join(SRC, 'MY_ROSTER.csv'), newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            mine[str(r['espn_id']).strip()] = r['player']
    roster = [dict(rate[p], status='ACTIVE') for p in mine if p in rate]
    assert len(roster) == len(mine), f'{len(mine) - len(roster)} of his men carry no projection'
    owned = set()
    with open(os.path.join(SRC, 'LEAGUE_ROSTERS.csv'), newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            owned.add(str(r['espn_id']).strip())
    assert all(p in owned for p in mine), 'MY_ROSTER is not inside LEAGUE_ROSTERS'
    wires = sorted(glob.glob(os.path.join(SRC, 'WIRE_*.csv')))
    wire = {}
    with open(wires[-1], newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            wire[str(r['espn_id']).strip()] = r
    free = []
    for pid, p in rate.items():
        if pid in owned:
            continue
        r0 = wire.get(pid)
        f = dict(p)
        f['owned'] = se._f(r0['owned_pct']) if r0 else None
        f['screen'] = (r0 or {}).get('screen') or ''
        f['form_sig'] = (r0 or {}).get('form_sig')
        f['touches'] = (r0 or {}).get('touches') or ''
        f['status'] = (r0 or {}).get('status') or 'ACTIVE'
        f['on_wire'] = r0 is not None
        free.append(f)
    seats, snote = se.load_seats(SRC)
    seat_all = se.load_seat_rows(SRC)
    cards = []
    cp = os.path.join(SRC, 'cards_2026.csv')
    if os.path.exists(cp):
        with open(cp, newline='', encoding='utf-8-sig') as fh:
            cards = list(csv.DictReader(fh))
    names = [r['name'] for r in free] + [r['name'] for r in roster] + [c.get('player') for c in cards]
    dn = se.donot_map(se.load_donot(SRC), [n for n in names if n])
    for c in cards:
        if (c.get('verdict') or '').strip().upper().startswith('DO NOT'):
            dn.setdefault(se.norm_name(c.get('player')), (c['verdict'].strip(), 'your player card'))
    return rate, const, roster, free, seats, seat_all, dn, os.path.basename(wires[-1])


# ------------------------------------------------------------------ arm P: the page's own list
def page_rows(roster, free, const, seats, dn):
    """The rows section 0 ranks, with the page's own worth, lane, when, status. Mirrors render()."""
    bar = se.bar_grid(roster)
    rows = []
    # fills: the best price() per position, ruled-out men skipped at selection
    for p in se.POS:
        best = None
        for c in (r for r in free if r.get('pos') == p):
            wkp, tot = se.price(c, bar)
            if tot <= 0.05 or se.norm_name(c['name']) in dn:
                continue
            if best is None or tot > best[1]:
                ws = [w for w in se.WEEKS if (wkp[w] or 0) > 0.049]
                best = (c, tot, ws)
        if best:
            c, tot, ws = best
            rows.append(dict(lane=FILL_LANE, cand=c, worth=tot, when=min(ws) if ws else 0, odds=None))
    # bets: the two screens and the workload lane, one row per man, the page's rates
    pot = const.get('potential', {}).get('in_season', {})
    HP, HW = pot.get('hit_size', {}).get('ppg'), pot.get('hit_size', {}).get('weeks')
    ARCH = {'pedigree screen 3 of 3': pot.get('three_of_three', {}).get('rate'),
            'first-round rookie': pot.get('round1_rookie_inseason', {}).get('rate')}
    wk2, wk3 = pot.get('workload_2of3', {}).get('rate'), pot.get('workload_3of3', {}).get('rate')
    seen = set()
    for c in sorted(free, key=lambda r: -(r.get('wk') or 0)):
        scr = (c.get('screen') or '').strip()
        key = next((k for k in ARCH if k in scr), None)
        if not key or c['name'] in seen:
            continue
        seen.add(c['name'])
        rate = ARCH[key]
        _, fires = se.bet(c, bar, HP, HW)
        if rate:
            rows.append(dict(lane=BET_LANE, cand=c, worth=round(rate * fires, 1), when=0, odds=rate,
                             label=key))
    for c in sorted(free, key=lambda r: -(r.get('wk') or 0)):
        try:
            sig = int(str(c.get('form_sig') or '').strip() or -1)
        except ValueError:
            sig = -1
        if sig < 2 or c['name'] in seen:
            continue
        rate = wk3 if sig >= 3 else wk2
        if not rate:
            continue
        seen.add(c['name'])
        _, fires = se.bet(c, bar, HP, HW)
        rows.append(dict(lane=BET_LANE, cand=c, worth=round(rate * fires, 1), when=0, odds=rate,
                         label='week-1 workload' + (', all three' if sig >= 3 else '')))
    # seats: the page's top ten by job plus own handcuffs; only free ones are moves
    sc = const.get('seat', {})
    s_rate, s_wks, s_p = sc.get('relief_ppg'), sc.get('weeks_played'), sc.get('p_opens')
    show = list(seats[:10]) + [r for r in seats[10:]
                                if se.roster_match(roster, r['holds_the_job'], r['team']) is not None]
    byname = {se.norm_name(r['name']): r for r in free}
    for r in show:
        hp = se.roster_match(roster, r['holds_the_job'], r['team'])
        b = se.bar_grid([p for p in roster if p is not hp]) if hp else bar
        probe = {'name': r['next_man'], 'pos': 'RB', 'tm': r['team'], 'wk': s_rate,
                 'bye': int(float(r['bye'])) if r.get('bye') else 0}
        live = [v for v in se.price(probe, b)[0].values() if v is not None]
        fires = round((sum(live) / len(live) if live else 0.0) * s_wks, 1)
        ev = round(s_p * fires, 1)
        cand = byname.get(se.norm_name(r['next_man']))
        if hp is None and ev > 0.05 and cand is not None:
            rows.append(dict(lane=SEAT_LANE, cand=cand, worth=ev, when=0, odds=s_p,
                             label=f"behind {r['holds_the_job']}", seat=r))
    for r in rows:
        r['ruled'] = se.norm_name(r['cand']['name']) in dn
        r['gone'] = 1 if (r['cand'].get('status') or '').strip().upper() in MULTIWEEK else 0
    return rows, bar, (HP, HW), (s_rate, s_wks, s_p)


def page_order(rows, key, week=WEEK):
    """The page's sort and its this-week / calendar split, on any worth key."""
    live = [r for r in rows if not r['ruled']]
    live.sort(key=lambda r: (r['gone'], -r[key], r['lane'] != FILL_LANE))
    now = [r for r in live if not (r['lane'] == FILL_LANE and r['when'] and week and r['when'] >= week + 2)]
    later = [r for r in live if r not in now]
    return now, later


# ------------------------------------------------------------------ arm U: the paired simulation
def simulate(roster, cands, const, n, seed, hit, seat, absences=True, stream=True, cuffs=(), relief=None):
    """One draw reused everywhere. Returns per-draw season totals:
       base[d], baseY[d][y], own[d][x][y], hitv[d][i][y], seatv[d][j][y]
    where y indexes the roster plus a final 'no drop' column.
    cuffs: [(backup index, holder index)] on the roster; the backup scores max(own, relief) in any
    week the holder is out, on bye, or is the man being dropped -- section 6's rule, doc 297 arm D,
    and what the page's own drop table already does for a handcuff (doc 317)."""
    rng = random.Random(seed)
    W = se.WEEKS
    ab = const['absence']
    rates = {k: float(v) for k, v in ab['rate'].items()} if absences else {}
    streamers = []
    if stream:
        for pos, v in ab['streamer'].items():
            streamers.append({'name': f'streamer {pos}', 'pos': pos, 'tm': '', 'bye': 0, 'wk': float(v)})
    nr, nc, nY = len(roster), len(cands), len(roster) + 1
    r_rate = [rates.get(p['pos'], 0.0) for p in roster]
    c_rate = [rates.get(p['pos'], 0.0) for p in cands]
    hit_ix = [i for i, c in enumerate(cands) if c['espn_id'] in hit]
    seat_ix = [i for i, c in enumerate(cands) if c['espn_id'] in seat]
    base = np.zeros(n); baseY = np.zeros((n, nY))
    own = np.zeros((n, nc, nY), dtype=np.float32)
    hitv = np.zeros((n, len(hit_ix), nY), dtype=np.float32)
    seatv = np.zeros((n, len(seat_ix), nY), dtype=np.float32)
    for d in range(n):
        av = [[rng.random() >= r_rate[i] for _ in W] for i in range(nr)]
        cav = [[rng.random() >= c_rate[j] for _ in W] for j in range(nc)]
        for wi, w in enumerate(W):
            holder_of = {b_: h_ for b_, h_ in cuffs}

            def pool_for(drop):
                out = []
                for i, p in enumerate(roster):
                    if i == drop or not av[i][wi]:
                        continue
                    h = holder_of.get(i)
                    if h is not None and relief and (h == drop or not av[h][wi] or roster[h]['bye'] == w):
                        p = dict(p, wk=max(p['wk'], relief))
                    out.append(p)
                return out + streamers

            pool = pool_for(None)
            b = se.week_points(pool, w)[0]
            base[d] += b
            # the roster with each man removed (index nr = nobody removed)
            for y in range(nY):
                if y < nr and av[y][wi]:
                    poolY = pool_for(y)
                    by = se.week_points(poolY, w)[0]
                else:
                    poolY, by = pool, b          # he was out anyway: dropping him changes nothing
                baseY[d, y] += by
                for j, c in enumerate(cands):
                    if c['bye'] == w or not cav[j][wi]:
                        continue
                    own[d, j, y] += se.week_points(poolY + [c], w)[0] - by
                for k, j in enumerate(hit_ix):
                    c = cands[j]
                    if c['bye'] == w or not cav[j][wi]:
                        continue
                    hitv[d, k, y] += se.week_points(poolY + [dict(c, wk=hit[c['espn_id']])], w)[0] - by
                for k, j in enumerate(seat_ix):
                    c = cands[j]
                    if c['bye'] == w or not cav[j][wi]:
                        continue
                    seatv[d, k, y] += se.week_points(poolY + [dict(c, wk=seat[c['espn_id']])], w)[0] - by
    return dict(base=base, baseY=baseY, own=own, hitv=hitv, seatv=seatv, hit_ix=hit_ix, seat_ix=seat_ix)


def main():
    t0 = time.time()
    rate, const, roster, free, seats, seat_all, dn, wirefile = load_all()
    rows, bar, (HP, HW), (s_rate, s_wks, s_p) = page_rows(roster, free, const, seats, dn)
    nowP, laterP = page_order(rows, 'worth')
    print(f'JOB 1 -- one currency for the priority list   N={N} seed={SEED} week={WEEK}')
    print(f'  roster {len(roster)}, free pool {len(free)} ({sum(1 for f in free if f["on_wire"])} on {wirefile}), '
          f'rows on the page: {len(rows)} ({sum(r["lane"]==FILL_LANE for r in rows)} fills, '
          f'{sum(r["lane"]==BET_LANE for r in rows)} bets, {sum(r["lane"]==SEAT_LANE for r in rows)} seats), '
          f'ruled out {sum(r["ruled"] for r in rows)}')
    print('  THE PAGE, this week:')
    for i, r in enumerate(nowP[:8], 1):
        print(f"   {i}. {r['cand']['name']:<22} {r['lane']:<5} {r['worth']:>6.1f}")
    print('  THE PAGE, calendar:', ' | '.join(f"wk{r['when']} {r['cand']['name']} {r['worth']:.1f}" for r in laterP))

    # the simulation: every free man as a fill; bets and seats as extra rows on the same draw
    cands = free
    # his own handcuffs: a backup he owns behind a job whose holder he also owns (Washington, Jeanty)
    byid = {str(p.get('espn_id', '')): i for i, p in enumerate(roster)}
    cuffs = []
    for r in seat_all:
        bi = byid.get(str(r.get('next_man_id', '')).strip())
        hp = se.roster_match(roster, r.get('holds_the_job'), r.get('team'))
        if bi is not None and hp is not None and roster[bi]['pos'] == 'RB':
            cuffs.append((bi, roster.index(hp)))
    print('  own handcuffs priced at the relief rate when the man ahead is out:',
          ', '.join(f"{roster[b_]['name']} behind {roster[h_]['name']}" for b_, h_ in cuffs) or 'none')
    hit = {r['cand']['espn_id']: HP for r in rows if r['lane'] == BET_LANE}
    seat = {r['cand']['espn_id']: s_rate for r in rows if r['lane'] == SEAT_LANE}
    t1 = time.time()
    A = simulate(roster, cands, const, 1, SEED, hit, seat, absences=False, stream=False)   # no cuffs: the page's own arithmetic
    print(f'  arm A (byes only, no streamer, one draw) {time.time() - t1:.0f}s')
    # CONTROL: arm A must reproduce price() (no drop) and drop_costs() (no add) exactly
    nY = len(roster) + 1
    worst = 0.0
    for j, c in enumerate(cands):
        worst = max(worst, abs(float(A['own'][0, j, nY - 1]) - se.price(c, bar)[1]))
    dc = {p['name']: cst for cst, p in se.drop_costs(roster, used=15)}
    worst_d = max(abs((A['base'][0] - A['baseY'][0, y]) - dc[roster[y]['name']]) for y in range(len(roster)))
    print(f'  CONTROL: arm A vs price() worst gap {worst:.3f}; vs drop_costs() worst gap {worst_d:.3f}  '
          f'{"PASS" if worst < 0.11 and worst_d < 0.06 else "FAIL"}')
    assert worst < 0.11 and worst_d < 0.06

    t1 = time.time()
    U = simulate(roster, cands, const, N, SEED, hit, seat, absences=True, stream=True, cuffs=cuffs, relief=s_rate)
    print(f'  arm U (absences drawn, streamer in the pool) {time.time() - t1:.0f}s; '
          f'bare roster {U["base"].mean():.1f} against {A["base"][0]:.1f} byes-only')

    # drop costs in one currency (mean and paired se), and the matrix
    D = U['base'][:, None] - U['baseY']                     # n x nY, last column zero
    Dm, Dse = D.mean(0), D.std(0, ddof=1) / np.sqrt(N)
    names_y = [p['name'] for p in roster] + ['no drop']
    own = U['own'].astype(np.float64)
    net = own - D[:, None, :]                               # add him, drop y
    netm, netse = net.mean(0), net.std(0, ddof=1) / np.sqrt(N)
    ownm = own.mean(0)
    nh = np.array([len([w for w in se.WEEKS if c['bye'] != w]) for c in cands], dtype=float)

    def lane_value(j, lane, y):
        """One-currency value of candidate j in a lane, given drop y; per draw."""
        g_own = own[:, j, y]
        if lane == FILL_LANE:
            v = g_own
        elif lane == BET_LANE:
            k = U['hit_ix'].index(j); r = odds_of[j]
            v = r * (HW / nh[j]) * U['hitv'][:, k, y].astype(np.float64) + (1 - r) * g_own
        else:
            k = U['seat_ix'].index(j); r = s_p
            v = r * (s_wks / nh[j]) * U['seatv'][:, k, y].astype(np.float64) + (1 - r) * g_own
        return v - D[:, y]

    odds_of = {}
    idx = {c['espn_id']: j for j, c in enumerate(cands)}
    for r in rows:
        if r['lane'] in (BET_LANE, SEAT_LANE):
            odds_of[idx[r['cand']['espn_id']]] = r['odds']

    # one-currency worth for every page row: gross (no drop) and net (best drop)
    # THE DROP A BENCH ADD CAN ACTUALLY SPEND. A kicker or a defence is not a seat a bench body can
    # take: he must start one every week, so 'drop the Browns' is a swap of defences, not a freed
    # seat. The headline net is therefore the best SKILL drop (QB/RB/WR/TE); the best over all
    # fifteen is kept beside it, and every per-drop value is written out.
    skill_y = [y for y, p in enumerate(roster) if p['pos'] in ('QB', 'RB', 'WR', 'TE')]
    for r in rows:
        j = idx[r['cand']['espn_id']]
        vals = np.array([lane_value(j, r['lane'], y).mean() for y in range(nY)])
        ses = np.array([lane_value(j, r['lane'], y).std(ddof=1) / np.sqrt(N) for y in range(nY)])
        r['u_gross'] = float(vals[nY - 1])
        yb = max(skill_y, key=lambda y: vals[y])
        r['u_net'] = float(vals[yb]); r['u_net_se'] = float(ses[yb]); r['u_drop'] = names_y[yb]
        ya = int(np.argmax(vals[:nY - 1]))
        r['u_net_any'] = float(vals[ya]); r['u_drop_any'] = names_y[ya]
        r['u_net_cheapest'] = float(vals[int(np.argmin(Dm[:nY - 1]))])
        r['per_drop'] = {names_y[y]: round(float(vals[y]), 2) for y in range(nY)}
    # the fill lane under one currency must be re-chosen: the best NET fill per position
    ufills = []
    for p in se.POS:
        cj = [j for j, c in enumerate(cands) if c['pos'] == p and se.norm_name(c['name']) not in dn]
        if not cj:
            continue
        best = max(cj, key=lambda j: max(netm[j, y] for y in skill_y))
        yb = max(skill_y, key=lambda y: netm[best, y])
        ya = int(np.argmax(netm[best, :nY - 1]))
        c = cands[best]
        page_when = 0
        wkp, _tot = se.price(c, bar)
        ws = [w for w in se.WEEKS if (wkp[w] or 0) > 0.049]
        page_when = min(ws) if ws else 0
        ufills.append(dict(lane=FILL_LANE, cand=c, worth=_tot, when=page_when, odds=None,
                           ruled=False, gone=1 if (c.get('status') or '').upper() in MULTIWEEK else 0,
                           u_gross=float(ownm[best, nY - 1]), u_net=float(netm[best, yb]),
                           u_net_se=float(netse[best, yb]), u_drop=names_y[yb],
                           u_net_any=float(netm[best, ya]), u_drop_any=names_y[ya],
                           u_net_cheapest=float(netm[best, int(np.argmin(Dm[:nY - 1]))]),
                           per_drop={names_y[y]: round(float(netm[best, y]), 2) for y in range(nY)},
                           refilled=c['espn_id'] != next((r['cand']['espn_id'] for r in rows
                                                          if r['lane'] == FILL_LANE and r['cand']['pos'] == p), None)))
    rowsU = [r for r in rows if r['lane'] != FILL_LANE] + ufills
    nowG, laterG = page_order(rowsU, 'u_gross')
    nowU, laterU = page_order(rowsU, 'u_net')

    # ---- the falsifier
    def top5(now):
        return [r['cand']['name'] for r in now[:5]]
    def first_by_lane(now):
        return {ln: next((r['cand']['name'] for r in now if r['lane'] == ln), None)
                for ln in (FILL_LANE, BET_LANE, SEAT_LANE)}
    same = top5(nowP) == top5(nowU) and first_by_lane(nowP) == first_by_lane(nowU)
    print('\nTOP FIVE THIS WEEK')
    print('  page (P):           ', ' | '.join(top5(nowP)))
    print('  one currency gross: ', ' | '.join(top5(nowG)))
    print('  one currency net (U):', ' | '.join(top5(nowU)))
    print('TOP MAN BY LANE')
    for ln in (FILL_LANE, BET_LANE, SEAT_LANE):
        print(f"  {ln:<5} page {str(first_by_lane(nowP)[ln]):<24} U {first_by_lane(nowU)[ln]}")
    print(f'\nFALSIFIER (top five and top man per lane identical): {same} -> '
          f'{"NULL, the lane mixing costs nothing the page acts on" if same else "the order CHANGES"}')

    # ---- side by side, every row, both orderings
    def rank_of(lst):
        return {r['cand']['espn_id']: i + 1 for i, r in enumerate(lst)}
    rP, rU, rG = rank_of(nowP + laterP), rank_of(nowU + laterU), rank_of(nowG + laterG)
    allrows = {r['cand']['espn_id']: r for r in rows + ufills}
    side = []
    for pid, r in allrows.items():
        side.append(dict(player=r['cand']['name'], pos=r['cand']['pos'], team=r['cand']['tm'],
                         lane=r['lane'], label=r.get('label', ''), status=r['cand'].get('status', ''),
                         ruled_out=int(r['ruled']), calendar_week=r['when'] if r['lane'] == FILL_LANE else '',
                         page_worth=round(r['worth'], 2), page_rank=rP.get(pid, ''),
                         u_gross=round(r['u_gross'], 2), u_gross_rank=rG.get(pid, ''),
                         u_net=round(r['u_net'], 2), u_net_se=round(r['u_net_se'], 3),
                         u_net_rank=rU.get(pid, ''), best_drop=r['u_drop'],
                         u_net_any_drop=round(r['u_net_any'], 2), best_drop_any=r['u_drop_any'],
                         u_net_vs_cheapest_drop=round(r['u_net_cheapest'], 2),
                         change=round(r['u_net'] - r['worth'], 2),
                         **{'drop ' + k: v for k, v in r['per_drop'].items()}))
    side.sort(key=lambda s: (s['u_net_rank'] == '', s['u_net_rank'] if s['u_net_rank'] != '' else 0))
    cols = list(side[0].keys())
    with open(os.path.join(OUT, 'J1_orderings.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(side)
    big = max((s for s in side if not s['ruled_out']), key=lambda s: abs(s['change']))
    print(f"\nLARGEST SINGLE ROW CHANGE: {big['player']} ({big['lane']}) page {big['page_worth']:.1f} -> "
          f"one currency {big['u_net']:.1f} ({big['change']:+.1f}), best drop {big['best_drop']}")
    print(f"  {'player':<22}{'lane':<6}{'page':>7}{'gross':>7}{'net':>7}{'+/-':>6}  best skill drop | any drop")
    for s in side:
        if s['ruled_out']:
            continue
        print(f"  {s['player']:<22}{s['lane']:<6}{s['page_worth']:>7.1f}{s['u_gross']:>7.1f}{s['u_net']:>7.1f}"
              f"{s['u_net_se']:>6.2f}  {s['best_drop']} | {s['u_net_any_drop']:.1f} {s['best_drop_any']}")

    # ---- the matrix: every free man x every drop, the fill lane, net
    with open(os.path.join(OUT, 'J1_add_minus_drop_matrix.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['player', 'pos', 'team', 'bye', 'on_wire', 'status', 'proj_per_game', 'page_price',
                    'add_only_gross'] + [f'drop {nm}' for nm in names_y[:-1]] + ['best_drop', 'best_net',
                    'best_net_se'])
        for j, c in enumerate(cands):
            yb = int(np.argmax(netm[j, :nY - 1]))
            w.writerow([c['name'], c['pos'], c['tm'], c['bye'], int(c['on_wire']), c.get('status', ''),
                        round(c['wk'], 2), round(se.price(c, bar)[1], 2), round(float(ownm[j, nY - 1]), 2)]
                       + [round(float(netm[j, y]), 2) for y in range(nY - 1)]
                       + [names_y[yb], round(float(netm[j, yb]), 2), round(float(netse[j, yb]), 3)])
    with open(os.path.join(OUT, 'J1_drop_costs.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['player', 'pos', 'bye', 'proj_per_game', 'page_drop_cost', 'one_currency_drop_cost', 'se'])
        for y, p in enumerate(roster):
            w.writerow([p['name'], p['pos'], p['bye'], round(p['wk'], 2), round(dc[p['name']], 2),
                        round(float(Dm[y]), 2), round(float(Dse[y]), 3)])
    print('\nDROP COSTS, page (byes only, hole at zero) against one currency (absences, streamed):')
    for y, p in sorted(enumerate(roster), key=lambda t: Dm[t[0]]):
        print(f"  {p['name']:<22}{p['pos']:<5}{dc[p['name']]:>7.2f}{Dm[y]:>8.2f} +/- {Dse[y]:.2f}")
    json.dump({'N': N, 'seed': SEED, 'week': WEEK, 'wire': wirefile, 'n_free': len(cands),
               'top5_page': top5(nowP), 'top5_gross': top5(nowG), 'top5_net': top5(nowU),
               'first_by_lane_page': first_by_lane(nowP), 'first_by_lane_net': first_by_lane(nowU),
               'null': bool(same), 'largest_change': big,
               'bare_roster': {'A': float(A['base'][0]), 'U': float(U['base'].mean())}},
              open(os.path.join(OUT, 'J1_summary.json'), 'w'), indent=1, default=str)
    print(f'\nwrote J1_orderings.csv, J1_add_minus_drop_matrix.csv, J1_drop_costs.csv, J1_summary.json '
          f'in {time.time() - t0:.0f}s')


if __name__ == '__main__':
    main()
