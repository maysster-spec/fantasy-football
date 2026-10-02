#!/usr/bin/env python3
r"""
make_gridboard.py -- the draft board as a 12-wide SNAKE GRID, the way
fantasyfootballcalculator.com/adp draws it, but built from OUR numbers.

    py make_gridboard.py            build Source\ADP_GRID.html and .pdf
    py make_gridboard.py --no-pdf   page only

WHY IT IS NOT JUST THE WEBSITE (doc 169). The site is a generic 12-team half-PPR board. This
league is not generic in two ways that move every cell:

  1. TWELVE KEEPERS ARE ALREADY GONE.  s2.1(c): the pool is depleted from pick 1, not round 15.
     `board_v8_fixed.csv` already has them removed, so dealing the survivors into slots 1..144
     in ADP order IS the keeper-adjusted board. On the website Rashee Rice, Chris Olave,
     Javonte Williams, Zay Flowers, Tetairoa McMillan, Cam Skattebo, Colston Loveland, Drake
     Maye, Travis Etienne Jr., Rhamondre Stevenson, Stefon Diggs and George Pickens all still
     occupy cells they cannot occupy here -- so every player behind them is one to twelve picks
     too deep. That is the whole point of this page.
  2. NEWS REMOVALS APPLY.  Josh Jacobs is zeroed by `news_overrides.csv` and therefore is not on
     this grid at all, at any pick.

WHAT MAKES IT SMARTER THAN A PRICE LIST (doc 170). Raw ADP put Josh Allen in Matt's pick-17
cell, which s4.2 already measured at a ~3% chance of being true. Two MEASURED league behaviours
are applied to the ordering, and nothing else is invented:

  * s5 / s4.12 -- SNYDER TAKES ALLEN AT HIS TURN. 4-for-4 whenever available (2.21, 2.23, 2.21,
    then 1.01 overall in 2025); the 2024 miss was a two-pick snipe. Fitted q ~ 0.90. He picks 9
    and 16, so Allen is drawn at 9, not 17.
  * s4.12 -- TE EFFECTIVE ADP IS +15 PICKS in this league (fitted). Corroborated independently by
    s4.7: one TE before round 3 in 43 team-seasons, ZERO inside the first 17 picks in 2024 or
    2025, median first TE round 7. National ADP prices tight ends for a league that is not this
    one. Every TE therefore slides 15 picks later than his price.

WHAT IS DELIBERATELY *NOT* USED, and this one matters. It is tempting to colour a cell by how far
our board rank sits from the market's pick -- "we like him more than they do". **That signal is
RETIRED (s4.13) and was then re-measured at rho = -0.173, n=409, pointing the WRONG WAY (s4.22b):
the players who looked like the biggest bargains did slightly worse.** The VALUE LADDER greys its
own BOARD badge out for exactly this reason. So no cell on this page is coloured by board-vs-ADP,
and if a future session is tempted, that is the finding to read first.

AND WHAT IT DELIBERATELY WILL NOT DRAW.  s4.14: only 144 rows of this board carry a genuine ESPN
draft position; the other 336 sit inside a two-pick-wide "undrafted" sentinel around pick 170
where ESPN supplies no ordering at all. 144 is exactly 12 rounds. So this page stops at round 12
rather than printing three rounds of invented order. Matt's remaining picks are 152 (D/ST) and
161 (K), which s4.8 says have no realisable draft value anyway.

Standard library + pandas only. Paths resolve against this file (s0.4 v6.8). The PDF is made by
importing `to_pdf.render` rather than shelling out again -- one renderer, one zoom, one place
where the wkhtmltopdf-is-missing fallback lives.
"""
import argparse, datetime as dt, html, os, re, sys
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, 'live_draft')
SRC = os.path.normpath(os.path.join(HERE, '..', 'Source'))
BOARD = os.path.join(KIT, 'board_v8_fixed.csv')
STAMP = os.path.join(KIT, 'adp_vintage.txt')
OUT_HTML = os.path.join(SRC, 'ADP_GRID.html')
OUT_PDF = os.path.join(SRC, 'ADP_GRID.pdf')

TEAMS = 12
MY_SLOT = 8
SPLIT = 8                  # s4.13: risk from round 9, never before -- the natural seam
SENTINEL = 168          # s4.14: at or beyond this, ESPN's ADP is a placeholder, not a price
MY_PICKS = {8, 17, 32, 41, 56, 65, 80, 89, 104, 113, 128, 137}
REPL = {'QB': 341.603, 'RB': 168.589, 'WR': 163.540, 'TE': 140.295}   # s4.1
LADDER = os.path.join(HERE, 'values.csv')
CTX = os.path.join(KIT, 'player_context.csv')
NEWS = os.path.join(HERE, 'news_overrides.csv')
OVR = os.path.join(SRC, 'override_card.csv')

# s4.12, both FITTED, both applied to the ordering. Nothing else moves a player.
# doc 175. ALL FOUR POSITIONS MEASURED, IN THE KEEPER-ADJUSTED COORDINATE, AND THE EARLIER
# NUMBERS SHRANK BY ~3x. The old +15 / -15 were taken against RAW national ADP; this league
# removes 12 keepers before pick 1, which compresses the whole board ~10-12 picks, so a raw
# comparison charges each position for a shift the ENTIRE board shares. Re-run properly:
#
#   speed = actual slot - effective ADP        (negative = comes off the board FASTER)
#   5 seasons, n=680 true selections, s1.1 preseason registry, keepers removed from the market
#
#   eff ADP     RB              WR              TE              QB
#   1-24        -0.1  t -0.16   +3.5  t +4.55   +4.3  t +4.43   -9.3  t -3.40
#   25-60       -2.2  t -1.25   +6.6  t +5.00   +3.2  t +1.26   -3.1  t -1.04
#   61-120      +1.8  t +0.81   +5.8  t +3.53   -4.3  t -1.28   +1.4  t +0.37
#
# WR IS THE FINDING: significant in all three bands, same sign, n = 53/80/103. Receivers last
# 3-7 picks LONGER here than the market says. RB IS A NULL in every band -- the "RB-heavy league"
# is real as an EXPERIENCE and its mechanism is receivers falling, not backs flying.
# TE at the top reproduces year by year (first TE off the board: +5.0 +5.0 +1.8 +9.0 +6.0), which
# is why n=6 is trusted there. QB top-24 is n=6 and UNDERPOWERED; kept because it agrees with s5's
# independent timing table (four managers take their first QB in rounds 2.5-3.2).
#
# The 121+ band is NOT used: the draft is 168 long, so a player priced near it can only ever go
# earlier. That is censoring, not tendency.
WR_SHIFT = 5.0             # eff ADP <= WR_DEEP. Bands give +3.5/+6.6/+5.8; none differ, so one number
TE_SHIFT = 5.0             # eff ADP <= PREMIUM
QB_SHIFT = -4.0            # eff ADP <= PREMIUM
RB_SHIFT = 0.0             # measured, and it is a NULL in every usable band. Stated, not omitted.
PREMIUM = 60               # TE and QB were measured at the top; do not extrapolate past it
WR_DEEP = 120              # WR holds to 120, which is where the censoring starts
SNYDER_PICK = 9            # s5: Snyder's first turn; he takes Allen at q ~ 0.90 when available
SNYDER_TARGET = 'Josh Allen'

# s7, measured in DOLLARS over 100 board states, N=2000 paired drafts. The only names the
# project actually ranks at pick 32 -- policy spread across all five is $2.7.
TIE32 = {'Brock Bowers', 'Trey McBride', 'Kyren Williams', 'Quinshon Judkins',
         'Lamar Jackson', 'Breece Hall'}
# s7, CI-clear BEHIND those five at 32 even where the board shows them within a point.
BEHIND32 = {'Joe Burrow': 24, 'Matthew Stafford': 23, 'Jayden Daniels': 21, 'Emeka Egbuka': 20,
            "D'Andre Swift": 20, 'Jalen Hurts': 20, 'Tyler Warren': 15, 'Davante Adams': 14,
            'DeVonta Smith': 10}

# THE SIZES BELOW ARE PRE-MULTIPLIED BY 1/0.78, AND THAT CANCELS A KNOWN CONSTANT (doc 169).
# `to_pdf.render` injects `html{zoom:0.78}` on the Chrome path because every OTHER page here was
# laid out against wkhtmltopdf's 1024px assumption and has to shrink to reproduce its page count.
# This page was laid out natively, in landscape, and needs no such correction -- so it scales up
# by the reciprocal and the two cancel. Rendered without compensating it prints at 78% and wastes
# the bottom quarter of the sheet. Do NOT "tidy" these numbers back to round values.
CSS = r"""@page{size:letter landscape;margin:6mm 5mm}
body{font:12.8px/1.25 "Segoe UI",Arial,sans-serif;color:#111;margin:0}
h1{font-size:19.2px;margin:0 0 3px}
.sub{font-size:11.5px;color:#555;margin:0 0 6px}
.sub b{color:#222}
table{border-collapse:separate;border-spacing:0;width:100%;table-layout:fixed}
th,td{border:1px solid #c8cfd8;padding:0;vertical-align:top;
      print-color-adjust:exact;-webkit-print-color-adjust:exact}
th.sl{background:#33415c;color:#fff;font-size:12.2px;font-weight:700;padding:4px 0;text-align:center}
th.sl.me{background:#c0392b}
th.rd{background:#eef1f5;color:#33415c;font-size:12.2px;font-weight:700;width:26px;text-align:center}
/* two sheets, two cell sizes. Round 9 is where the ordering stops deciding (s4.13), so the
   late cells get roughly double the height and spend it on the job flag and the analyst read. */
.s1{page-break-after:always}
.s1 td{height:76px}
.s2 td{height:136px}
.ex{margin-top:3px;font-size:9.6px;line-height:1.3;color:#3c4450;border-top:1px solid rgba(0,0,0,.12);
    padding-top:3px}
.ex b.ju{color:#12734f}.ex b.jc{color:#7d4f0d}.ex b.tg{color:#33415c;letter-spacing:.3px}
.c{padding:2px 3px 2px 6px;height:100%;box-sizing:border-box;position:relative}
/* LOCKED to two lines. Without this a long surname wraps, that one cell grows, and the
   twelfth round lands on a second sheet -- which is exactly what will happen when the
   7:00 PM keeper swap changes who is on the board. Height must not depend on names. */
.nm{font-size:10.8px;font-weight:600;line-height:1.06;letter-spacing:-.15px;
    height:2.12em;overflow:hidden}
/* nowrap on purpose: a wrapped meta line makes ONE cell taller and pushes the whole
   twelfth round onto a second sheet. The adjustment tag is written last, so if a very
   long team+bye ever clips, it clips the least important item. */
.mt{font-size:9.2px;margin-top:2px;opacity:.9;font-variant-numeric:tabular-nums;white-space:nowrap;overflow:hidden}
/* ONE flex line: value, then any chips, then the price. They used to float with clear:right,
   which stacked each chip on its own row and cost a line of height per marked cell. */
.r1{display:flex;align-items:baseline;gap:3px;overflow:hidden;white-space:nowrap}
.chs{flex:1 1 auto;min-width:0;overflow:hidden;text-align:left}
.pk{flex:0 0 auto;font-size:9.1px;color:#8a94a3;font-weight:600;font-variant-numeric:tabular-nums}
.pk.mine{color:#c0392b;font-weight:800;font-size:11px}
/* VOR -- the board's own value number, top-left, opposite the price. Below replacement it goes
   GREY on purpose: s0.3, "rank comparisons among below-replacement players are noise", and half
   of these 144 cells are below it. The eye should skip them, not weigh them. */
.vo{flex:0 0 auto;font-size:10.4px;font-weight:800;font-variant-numeric:tabular-nums;letter-spacing:-.2px}
.vo.neg{color:#98a0aa;font-weight:600}
.QB .vo{color:#55317f}.RB .vo{color:#0f5c3f}.WR .vo{color:#0f4e73}.TE .vo{color:#7d4f0d}
.QB .vo.neg,.RB .vo.neg,.WR .vo.neg,.TE .vo.neg{color:#98a0aa}
.QB{background:#e7dcf3}.QB .mt{color:#55317f}
.RB{background:#d6efe2}.RB .mt{color:#0f5c3f}
.WR{background:#d8e8f6}.WR .mt{color:#0f4e73}
.TE{background:#f8e7cb}.TE .mt{color:#7d4f0d}
/* YOUR COLUMN IS ONE CONTINUOUS STRIP, not twelve boxes. Left and right edges on every cell,
   a cap top and bottom, and NO red rule between rounds -- doc 170, Matt asked for the border
   without the horizontal lines and he is right, the rungs read as a table inside a table. */
td.me{border-left:3px solid #c0392b;border-right:3px solid #c0392b}
td.metop{border-top:3px solid #c0392b}
td.mebot{border-bottom:3px solid #c0392b}
/* value and caution marks live INSIDE the cell so they never collide with that strip */
td.hot .c{box-shadow:inset 5px 0 0 #12734f}
.ch{display:inline-block;font-size:8.2px;font-weight:800;letter-spacing:.2px;color:#fff;
    padding:0 3px;border-radius:2px;margin-right:2px;vertical-align:1px}
.ch.av{background:#c0392b}.ch.di{background:#d68910}.ch.by{background:#12734f}
/* doc 206 (Matt): this session's two MEASURED signals belong on the grid too, not only on
   the board and the tier sheet. Composite green matches the board's bR3; the snap warning is
   the board's rz amber. */
.ch.c3{background:#0f5d3f}.ch.c1{background:#8c6d3f}.ch.sn{background:#8c4a3f}
/* doc 206 (Matt): 'contrast and compare both ways without as much mental math.' One number,
   one meaning, on BOTH grids: the room's slot MINUS our slot. + = the room takes him later
   than we rank him, so value falls to you. - = he goes before we would take him. Drawn only
   at 10 slots or more, so the page stays quiet and only real divergence is marked. */
.gp{font-weight:800;font-size:9px;margin-left:3px}.gp.up{color:#12734f}.gp.dn{color:#c0392b}
/* the analysts' written case, where one exists. Opinion, not measurement -- the key says so. */
.cs{font-size:9px;letter-spacing:-1px}
.cs.cb{color:#12734f}.cs.cr{color:#c0392b}.cs.csp{color:#7a828c}.cs.co{color:#9aa3ad}
.st{color:#b8860b;font-size:12px}
.bh{color:#7a828c;font-weight:700}
.aj{color:#7a828c;font-style:italic;font-weight:700;margin-left:2px}
.fx{color:#0b6ea9;font-weight:800;font-size:9.5px;margin-left:1px}
.hurt{color:#c0392b;font-weight:700}
.key{margin-top:5px;font-size:9.6px;color:#444;line-height:1.32}
.key b{color:#111}
.sw{display:inline-block;width:13px;height:13px;border:1px solid #8a94a3;vertical-align:-2px;
    margin-right:3px;print-color-adjust:exact;-webkit-print-color-adjust:exact}
.bar{display:inline-block;width:6px;height:13px;background:#12734f;vertical-align:-2px;margin-right:3px}
"""


def vintage():
    try:
        return open(STAMP, encoding='utf-8').read().strip()
    except Exception:
        return 'unknown (adp_vintage.txt unreadable)'


def overall(rnd, slot):
    """Snake. Odd rounds run 1->12, even rounds run 12->1."""
    return (rnd - 1) * TEAMS + (slot if rnd % 2 else TEAMS + 1 - slot)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-pdf', action='store_true')
    # doc 203 (Matt): the SAME snake grid, filled in OUR order instead of the room's. One
    # script, two outputs -- a second FILE for one job is the defect s0.2 names, and the only
    # thing that differs is the sort key and the words at the top.
    ap.add_argument('--board', action='store_true',
                    help='fill the grid by OUR VOR rank, not by where the room takes them')
    a = ap.parse_args()
    if not os.path.exists(BOARD):
        sys.exit(f'  missing {BOARD}')
    full = pd.read_csv(BOARD)
    b = full[full.adp_pick < SENTINEL].copy()

    # ---- the two MEASURED adjustments (s4.12). Base is eff_pick, the keeper-depleted
    # coordinate (s2.1e), because that is the space the noise and the opponent model were
    # fitted in. Do not "correct" it back to raw ADP.
    b['sim'] = b.eff_pick.astype(float)
    b['adj'] = ''
    # doc 175. Each position moves by its OWN measured speed, inside the band it was measured
    # in. RB's measured speed is ~0, so RB moves by nothing -- that is its measurement, not an
    # omission. The board-wide component (-1.9 picks) is deliberately NOT applied: a constant
    # added to every row reorders nothing on a grid.
    for pos, shift, deep in (('WR', WR_SHIFT, WR_DEEP), ('TE', TE_SHIFT, PREMIUM),
                             ('QB', QB_SHIFT, PREMIUM), ('RB', RB_SHIFT, PREMIUM)):
        if not shift:
            continue
        sel = (b.pos == pos) & (b.eff_pick <= deep)
        b.loc[sel, 'sim'] += shift
        b.loc[sel, 'adj'] = '%+d' % shift
    hit = b.player == SNYDER_TARGET
    if hit.any():
        b.loc[hit, 'sim'] = SNYDER_PICK - 0.5
        b.loc[hit, 'adj'] = 'SNY'
    # VOR rank WITHIN position, on the drawn population -- free, and it turns a bare
    # number into a tier at a glance ('RB7' reads faster than '+71').
    b['prank'] = b.groupby('pos').vbd.rank(ascending=False, method='min').astype(int)
    # doc 206: the two orderings, side by side, so either grid can print the gap between them.
    b['mkt_slot'] = b['sim'].rank(method='min').astype(int)
    b['brd_slot'] = b.vbd.rank(ascending=False, method='min').astype(int)
    b['gap'] = b.mkt_slot - b.brd_slot
    BOARD_ORDER = bool(getattr(a, 'board', False))
    if BOARD_ORDER:
        # slot N holds OUR Nth-ranked player. Ties broken by the room, so the page is
        # deterministic and two runs of the same board draw the same grid.
        real = b.sort_values(['vbd', 'sim'], ascending=[False, True]).reset_index(drop=True)
    else:
        real = b.sort_values('sim').reset_index(drop=True)
    globals()['OUT_HTML'] = os.path.join(SRC, 'BOARD_GRID.html' if BOARD_ORDER else 'ADP_GRID.html')
    globals()['OUT_PDF'] = os.path.join(SRC, 'BOARD_GRID.pdf' if BOARD_ORDER else 'ADP_GRID.pdf')

    # ---- what we already know about these players. Both files are optional; the page
    # degrades to plain placement and says so rather than dying at T-2.
    hot, grade, buy, lean, bull = {}, {}, set(), {}, set()
    job, dart, rook = {}, set(), set()
    try:
        lad = pd.read_csv(LADDER)
        hot = {str(r.player): int(r.take_at) for _, r in lad.iterrows()}
    except Exception as e:
        print(f'  !! values.csv unreadable ({e}) -- no value marks on this page')
    try:
        cx = pd.read_csv(CTX)
        k = 'ESPN_ID' if 'ESPN_ID' in cx.columns else 'espn_id'
        grade = {int(i): str(g) for i, g in zip(cx[k], cx.grade.fillna(''))
                 if str(g) in ('AVOID', 'DISCOUNT')}
        # doc 170 addendum. `buy` is a 0/1 flag from the analyst sweep. The bull/bear PROSE
        # cannot fit a 100px cell and should not try -- but `lean` already condenses it to a
        # verdict in <=15 chars, and it is populated on exactly the 34 players who have BOTH a
        # bull and a bear case written. `bear` never appears without `bull` (34 / 0), so a
        # bull-with-no-lean is "somebody wrote the upside and nobody wrote the other side".
        buy = {int(i) for i, v in zip(cx[k], cx.get('buy', 0)) if str(v) == '1'}
        # doc 206: the RB composite (doc 191, +12.2/signal p=0.0008) and the WR/TE snap share
        # (doc 197, +0.79 per point p<0.0001) live in `why` as later segments. Only the two
        # DECISION-RELEVANT halves are drawn: 3-of-3 and 0-or-1 at RB, and the BOTTOM-quartile
        # snap warning at WR/TE. Top-quartile snaps are confirmatory and would cost a chip slot.
        _why = {int(i): str(v) for i, v in zip(cx[k], cx.get('why', '').fillna(''))}
        sig3, sig1, snaplo = set(), set(), {}
        for _i, _v in _why.items():
            _m = re.search(r'RB SIGNALS: (\d)/3', _v)
            if _m:
                (sig3 if _m.group(1) == '3' else sig1 if _m.group(1) in '01' else set()).add(_i)
            _m = re.search(r'SNAP SHARE 2025: (\d+)% BOTTOM', _v)
            if _m:
                snaplo[_i] = _m.group(1)
        lean = {int(i): str(v) for i, v in zip(cx[k], cx.get('lean', '').fillna(''))
                if str(v) and str(v) != 'nan'}
        bull = {int(i) for i, v in zip(cx[k], cx.get('bull', '').fillna(''))
                if str(v) and str(v) != 'nan'}
        # s4.20: "BUY THE JOB, NEVER THE NAME." The flag says the job is unresolved and what it
        # is worth; it has no opinion on who wins it, and neither does the test behind it.
        job = {int(i): (str(j), float(w) if w == w else 0.0)
               for i, j, w in zip(cx[k], cx.get('job', '').fillna(''), cx.get('job_ceil', 0))
               if str(j) and str(j) != 'nan'}
        dart = {int(i) for i, v in zip(cx[k], cx.get('dart', 0)) if str(v) in ('1', '1.0')}
        rook = {int(i) for i, v in zip(cx[k], cx.get('rook', 0)) if str(v) in ('1', '1.0')}
    except Exception as e:
        print(f'  !! player_context.csv unreadable ({e}) -- no caution marks on this page')
    # doc 170: a news-zeroed player is still on this grid, because the grid draws where the
    # ROOM will spend picks and somebody will spend one on him. His VOR gives him away
    # instantly (Jacobs is -168.6 against a round-5 median of +4.7) but the number alone does
    # not say WHY, so the override's own reason is stamped on the cell.
    out = set()
    try:
        out = set(int(x) for x in pd.read_csv(NEWS).espn_id)
    except Exception as e:
        print(f'  !! news_overrides.csv unreadable ({e}) -- no removal marks on this page')
    # doc 171. The board's projections are the Aug-23 SPINE and cannot be rebuilt before the
    # draft (docs 62/143/144), so a few cells carry a VOR ESPN has since moved a long way.
    # MarShawn Lloyd reads -90 here and -44 on the current pull -- at Matt's pick 89.
    # `mkoverride.py` already computes exactly this, so read ITS output rather than recompute:
    # the page and the printed override card then cannot disagree.
    fixed = {}
    try:
        ov = pd.read_csv(OVR)
        fixed = {str(r.player): float(r.new_proj) for _, r in ov.iterrows() if not r.hold}
    except Exception as e:
        print(f'  !! override_card.csv unreadable ({e}) -- stale projections NOT flagged')

    rounds = len(real) // TEAMS
    if rounds < 1:
        sys.exit('  fewer than one full round of real ADP -- nothing to draw')
    used = rounds * TEAMS
    print(f'  board  : {os.path.basename(BOARD)}  ({len(full)} rows, 12 keepers already removed)')
    print(f'  market : {vintage()}')
    print(f'  real ADP rows: {len(real)}  ->  {rounds} full rounds ({used} cells); '
          f'{len(real) - used} real-ADP players spill past round {rounds} and are not drawn')
    _adj = real.head(used)
    print(f'  adjusted by a measured behaviour: {int((_adj.adj != "").sum())} cells '
          f'({int((_adj.adj != "" ).sum()) - int((_adj.adj == "SNY").sum())} positional, '
          f'{int((_adj.adj == "SNY").sum())} Snyder)')
    print(f'  opinion marks: {sum(1 for i in _adj.espn_id if int(i) in buy)} BUY, '
          f'{sum(1 for i in _adj.espn_id if int(i) in bull)} with a written case '
          f'({sum(1 for i in _adj.espn_id if int(i) in lean)} of them with a lean)')
    print(f'  marks: {sum(1 for p in _adj.player if p in hot)} on the value ladder, '
          f'{sum(1 for i in _adj.espn_id if grade.get(int(i)) == "AVOID")} AVOID, '
          f'{sum(1 for i in _adj.espn_id if grade.get(int(i)) == "DISCOUNT")} DISCOUNT')
    print(f'  {len(full) - len(b)} rows sit inside ESPN\'s undrafted sentinel and are never drawn (s4.14)')

    by_pick = {i + 1: real.iloc[i] for i in range(used)}
    mine = sorted(p for p in MY_PICKS if p <= used)
    # s0.2: a guard that has never been executed is not a guard. The snake formula is the one
    # piece of arithmetic on this page that can be silently wrong -- an off-by-one in the even
    # rounds would draw a correct-looking board with the outline on the wrong twelve cells.
    # So assert the property, not the code: every pick of Matt's must land in Matt's column.
    # The name box is locked to two lines, so a name too long for its line would CLIP rather
    # than wrap -- silent, and exactly the failure mode this project keeps finding. Measured fit
    # at 10.8px in a ~97px cell is about 17 characters; the widest on the whole 480-row board is
    # "Westbrook-Ikhine" at 16. So this should never fire -- and if it ever does, it says so.
    NAME_FIT = 17
    for _p in real.head(used).player.astype(str):
        head, _, tail = _p.partition(' ')
        for _line in (head, tail):
            if len(_line) > NAME_FIT:
                print(f'  !! NAME MAY CLIP: "{_line}" ({len(_line)} chars > {NAME_FIT}) in "{_p}"')
    for pk in mine:
        rnd = (pk - 1) // TEAMS + 1
        got = [s for s in range(1, TEAMS + 1) if overall(rnd, s) == pk]
        assert got == [MY_SLOT], f'snake is wrong: pick {pk} lands in column {got}, not {MY_SLOT}'
    assert sorted(overall(r, s) for r in range(1, rounds + 1)
                  for s in range(1, TEAMS + 1)) == list(range(1, used + 1)), \
        'snake does not cover every pick exactly once'
    print(f'  your picks on this grid: {", ".join(map(str, mine))}')

    head = ''.join('<th class="sl%s">%d</th>' % (' me' if s == MY_SLOT else '', s)
                   for s in range(1, TEAMS + 1))
    def build(lo, hi, detail):
      body = []
      for rnd in range(lo, hi + 1):
        cells = []
        for slot in range(1, TEAMS + 1):
            ov = overall(rnd, slot)
            r = by_pick[ov]
            nm = str(r.player)
            first, _, last = nm.partition(' ')
            me = ov in MY_PICKS
            g = grade.get(int(r.espn_id), '')
            cls = [r.pos]
            if me:
                cls.append('me')
                if rnd == lo:
                    cls.append('metop')
                if rnd == hi:
                    cls.append('mebot')
            if nm in hot:
                cls.append('hot')            # left bar: our sources point here
            # s7 is the strongest thing on this page, so it gets the loudest mark -- but only
            # in the rounds where the pick-32 decision actually lives. Everywhere else it would
            # be a star with no question attached to it.
            star = ' <span class="st">&#9733;</span>' if (nm in TIE32 and 13 <= ov <= 48) else ''
            ring = ''
            if nm in BEHIND32 and 13 <= ov <= 48:
                ring = ' <span class="bh">&minus;$%d</span>' % BEHIND32[nm]
            chip = ''
            if g == 'AVOID':
                chip = '<span class="ch av">AVOID</span>'
            elif g == 'DISCOUNT':
                chip = '<span class="ch di">DISC</span>'
            adj = ('<span class="aj">%s</span>' % r.adj) if r.adj else ''
            # doc 206: the room's slot minus ours. Drawn at 10+ only.
            _g = int(r.gap)
            gapchip = ('<span class="gp %s">%+d</span>' % ('up' if _g > 0 else 'dn', _g)) if abs(_g) >= 10 else ''
            hurt = str(r.get('flag') or '')
            hurt = '' if hurt in ('nan', '') else ' <span class="hurt">%s</span>' % (
                {'QUESTIONABLE': 'Q', 'DOUBTFUL': 'D', 'OUT': 'OUT',
                 'INJURY_RESERVE': 'IR'}.get(hurt, hurt[:3]))
            eid = int(r.espn_id)
            if eid in out:
                chip = '<span class="ch av">NEWS OUT</span>'
            if eid in buy:
                chip = '<span class="ch by">BUY</span>' + chip
            # doc 206: measured signals, after BUY so a BUY still reads first.
            if eid in sig3:
                chip += '<span class="ch c3">3/3</span>'
            elif eid in sig1:
                chip += '<span class="ch c1">1/3</span>'
            if eid in snaplo:
                chip += '<span class="ch sn">%s%% snaps</span>' % snaplo[eid]
            # the analysts' own verdict, where they wrote one. NOT a measurement -- see the key.
            case = {'strongly bull': ('cb', '&#9650;&#9650;'), 'lean bull': ('cb', '&#9650;'),
                    'genuinely split': ('csp', '&#9670;'), 'lean bear': ('cr', '&#9660;')
                    }.get(lean.get(eid, ''))
            if case:
                case = ' <span class="cs %s">%s</span>' % (case[0], case[1])
            elif eid in bull:
                case = ' <span class="cs co">&#9651;</span>'
            else:
                case = ''
            v = float(r.vbd)
            vor = '<span class="vo%s">%+d</span>' % ('' if v >= 0 else ' neg', round(v))
            if nm in fixed:
                vor += '<span class="fx">&rarr;%+d</span>' % round(fixed[nm] - REPL.get(r.pos, 0.0))
            # SHEET 2 ONLY. From round 9 the board stops deciding and Matt does (s4.13:
            # "risk from round 9, never before"), so the late cells are twice the height and
            # spend it on what that decision actually turns on -- s4.20's job flag and what
            # the job is worth, the analysts' verdict spelled out, and the dart/rookie tags.
            extra = ''
            if detail:
                bits = []
                if eid in job:
                    lab, worth = job[eid]
                    bits.append('<b class="%s">%s</b> job worth %d' % (
                        'ju' if lab == 'UNSETTLED' else 'jc', lab, worth))
                lv = lean.get(eid, '')
                if lv:
                    bits.append('analysts <b>%s</b>' % html.escape(lv))
                elif eid in bull:
                    bits.append('bull case only')
                tag = []
                if eid in dart:
                    tag.append('DART')
                if eid in rook:
                    tag.append('ROOKIE')
                if tag:
                    bits.append('<b class="tg">%s</b>' % ' &middot; '.join(tag))
                if bits:
                    extra = '<div class="ex">%s</div>' % '<br>'.join(bits)
            cells.append(
                '<td class="%s"><div class="c"><div class="r1">%s<span class="chs">%s</span>'
                '<span class="pk%s">%d</span></div>'
                '<div class="nm">%s%s%s<br>%s</div>'
                '<div class="mt">%s%d &middot; %s &middot; bye %s%s%s</div>%s</div></td>' % (
                    ' '.join(cls), vor, chip, ' mine' if me else '', ov,
                    html.escape(first), star, case, html.escape(last or '&nbsp;'),
                    r.pos, int(r.prank), html.escape(str(r.team_c)), int(r.bye), hurt,
                    ring + adj + gapchip, extra))
        body.append('<tr><th class="rd">%d</th>%s</tr>' % (rnd, ''.join(cells)))
      return ''.join(body)

    n_av = sum(1 for i in _adj.espn_id if grade.get(int(i)) == 'AVOID')
    n_di = sum(1 for i in _adj.espn_id if grade.get(int(i)) == 'DISCOUNT')
    n_real, n_board = len(real), len(full)
    n_neg = int((_adj.vbd < 0).sum())
    n_buy = sum(1 for i in _adj.espn_id if int(i) in buy)
    n_case = sum(1 for i in _adj.espn_id if int(i) in bull)
    n_adj = int((_adj.adj != '').sum())
    stamp = f'JUG, slot <b>{MY_SLOT}</b> &middot; market <b>{vintage()}</b> &middot; built ' \
           f'{dt.datetime.now():%b %d %Y, %H:%M}'
    KEY = f"""<div class="key">
<span class="sw" style="background:#d6efe2"></span><b>RB</b>
<span class="sw" style="background:#d8e8f6"></span><b>WR</b>
<span class="sw" style="background:#e7dcf3"></span><b>QB</b>
<span class="sw" style="background:#f8e7cb"></span><b>TE</b>
&nbsp;&middot;&nbsp; <b>Value on the left, price on the right.</b> Top-left is <b>VOR</b> &mdash;
points above a replacement starter at his position. His rank inside that position sits under the
name; the overall pick is top-right. <b style="color:#98a0aa">Grey VOR means below replacement</b>
({n_neg} of {used} cells): ranking those against each other is noise.
&nbsp;&middot;&nbsp; <b style="color:#c0392b">Q / D / OUT / IR</b> = ESPN injury status.
&nbsp;&middot;&nbsp; Odd rounds run left&rarr;right and even rounds right&rarr;left, so your cells
stay in column {MY_SLOT}.

<br><br><b>MARKS THAT COME FROM A MEASUREMENT</b><br>
<b style="color:#b8860b">&#9733;</b> <b>One of the five worth taking at pick 32.</b> Take whichever
shows first &mdash; across a hundred simulated drafts all five came out within three dollars of each
other. Do not agonise. <b>This is the hardest number on the page.</b> &nbsp;&middot;&nbsp;
<b style="color:#7a828c">&minus;$n</b> <b>NOT one of the five, and clearly behind</b> by that much.
The board may show him within a point of them; he is not close. Both marks are drawn only in rounds
2&ndash;4, where that decision lives.<br>
<span class="ch c3">3/3</span> <b>A back carrying all three signals that measure</b> &mdash; a real
share of his team's targets, 13+ games last year, and drafted in the NFL's first three rounds. Each
signal is worth roughly twelve points. &nbsp;&middot;&nbsp;
<span class="ch c1">1/3</span> one of the three, or none. &nbsp;&middot;&nbsp;
<span class="ch sn">N% snaps</span> <b>A receiver who was off the field a lot last year</b> &mdash;
bottom quarter of the league. The strongest receiver warning on this page.<br>
<b style="color:#7a828c;font-style:italic">+5 / &minus;4 / SNY</b> <b>This cell was moved by
something your league actually does</b>, measured across five of its drafts &mdash; not an opinion
({n_adj} of {used} cells). <b style="color:#12734f">WR +5: receivers last three to seven picks
longer here than the national market says.</b> That is the real tendency in your league and it is
the one that helps you. <b>TE +5</b> on the first tight end off the board. <b>QB &minus;4</b> early.
<b>RB moves by nothing &mdash; that is its measurement, not an omission.</b> The "RB-heavy league"
is real as an experience; the mechanism is receivers falling, not backs flying.
<b>SNY:</b> Josh Allen is drawn at <b>9, not 17</b> &mdash; Snyder picks 9 and 16 and has taken him
every time he was there. He reaches your 17 about three times in a hundred.

<br><br><b>MARKS THAT ARE SOMEBODY'S OPINION</b> &mdash; useful for what to read, never a reason to
draft.<br>
<span class="ch by">BUY</span> the analyst sweep called him a buy ({n_buy} cells). &nbsp;&middot;&nbsp;
<span class="ch av">AVOID</span> don't draft at this price &middot;
<span class="ch di">DISC</span> worth taking later than this cell &mdash; {n_av} and {n_di} of them
here, drawn where they are likely to be offered. &nbsp;&middot;&nbsp;
<span class="bar"></span><b>on the VALUE LADDER</b> &mdash; board, analysts and depth chart all point
at one name. A shortlist to read, not a ranking to obey.<br>
<b class="cs cb">&#9650;&#9650;</b> strongly bull &middot; <b class="cs cb">&#9650;</b> lean bull
&middot; <b class="cs csp">&#9670;</b> split &middot; <b class="cs cr">&#9660;</b> lean bear
&middot; <b class="cs co">&#9651;</b> a bull case with nobody arguing the other side &mdash; on the
{n_case} players anyone bothered to write about.
<b>Do not read &#9670; as "interesting."</b> The six rankers mostly agree with each other, and the
players they argue about have finished <b>worse</b>, not better.

<br><br><b>TWO NUMBERS THAT OVERRIDE WHAT IS BESIDE THEM</b><br>
<b>The number at the end of the grey line</b> is the room's slot minus ours, drawn at 10 or more.
<span class="gp up">+33</span> <b>the room takes him thirty-three picks later than we rank him</b>
&mdash; you can wait, he is the cheap one. <span class="gp dn">&minus;13</span> <b>he goes thirteen
picks earlier than we would take him</b> &mdash; reach or lose him. Same number on both grids.<br>
<b style="color:#0b6ea9">&rarr;&plusmn;n</b> <b>This player's VOR is out of date and the blue number
is the right one.</b> The projections are frozen and cannot be rebuilt before the draft, so a few
cells are badly stale &mdash; <b>MarShawn Lloyd reads &minus;90 and is really &minus;44</b>, at your
pick 89. Read the blue, not the black. Same source as the printed OVERRIDE CARD.
&nbsp;&middot;&nbsp; <b style="color:#c0392b">NEWS OUT</b> = the news overrides removed him; drawn
only because somebody in the room will still spend the pick.

<br><br><b>AND ONE THING NOT TO DO WITH THIS PAGE.</b> Value and price sit side by side, and the gap
between them is <b>not</b> a signal. "Big value, late pick, therefore bargain" has been tested twice
and came back <b>backwards both times</b>. Read VOR down a round to see where the value falls off;
do not hunt gaps with it. Nothing here is coloured by that gap, on purpose.
<b>A cell is a neighbourhood</b> (give or take twelve picks), a column is nothing &mdash; only column
{MY_SLOT} is yours. It stops at round {rounds} because only {n_real} of {n_board} players carry a
real draft position, and your 152 and 161 are the defense and the kicker.
<b>The live board is what you draft from.</b></div>"""
    sheet1 = build(1, SPLIT, False)
    sheet2 = build(SPLIT + 1, rounds, True)
    if BOARD_ORDER:
        H1A = (f'OUR BOARD AS A GRID &nbsp;1 of 2 &mdash; ROUNDS 1&ndash;{SPLIT}, '
               'IN OUR ORDER OF VALUE')
        H1B = (f'OUR BOARD AS A GRID &nbsp;2 of 2 &mdash; ROUNDS {SPLIT + 1}&ndash;{rounds}, '
               'IN OUR ORDER OF VALUE')
        LEDE = ('<b>EACH CELL IS THE PLAYER OUR BOARD RANKS AT THAT PICK &mdash; not where the room '
                'will take him. Slot 8 down the page is what your fourteen turns are WORTH if the '
                'board is right. Hold it beside the DRAFT BOARD GRID: where a name sits earlier '
                'here than there, the room is giving him away.</b>')
    else:
        H1A = (f'DRAFT BOARD GRID &nbsp;1 of 2 &mdash; ROUNDS 1&ndash;{SPLIT}, '
               'IN THE ORDER THE ROOM TAKES THEM')
        H1B = (f'DRAFT BOARD GRID &nbsp;2 of 2 &mdash; ROUNDS {SPLIT + 1}&ndash;{rounds}, '
               "THE ROOM'S ORDER &mdash; WHERE YOU DECIDE")
        LEDE = ('<b>EACH CELL IS WHERE THE OTHER ELEVEN MANAGERS ARE EXPECTED TO TAKE THAT PLAYER '
                '&mdash; not where our board ranks him. Different on purpose: this page answers WHEN '
                'you have to act, the board answers WHO is worth most. Our own ranking, by tier, is '
                'the TIER SHEET.</b>')
    doc = f"""<!doctype html><meta charset="utf-8"><title>ADP grid</title><style>{CSS}</style>
<div class="s1">
<h1>{H1A}</h1>
<p class="sub">{stamp} &middot; <b>the 12 keepers are already out of this pool</b>, so these cells
are {TEAMS} deep of real picks &mdash; a public ADP board is not. Column headings are draft slots;
only slot {MY_SLOT} is yours. {LEDE} <b>Through round {SPLIT} the engine's ordering is
the answer</b> &mdash;
at pick 8 take the highest VOR on the board, and at pick 32 take the engine's #1 rather than
override it. No margin is quoted for pick 8 because the size of that edge was retracted; WHO to
take is settled, HOW MUCH better he is, is not. Use this sheet to see the shape of a round and spot a run, not to pick.</p>
<table><tr><th class="rd">Rd</th>{head}</tr>{sheet1}</table>
{KEY}
</div>
<div class="s2">
<h1>{H1B}</h1>
<p class="sub">{stamp} &middot; <b>take risk from round 9, never before.</b> Swinging for upside all draft long costs you $22 to $41;
swinging from round 9 on is free. So these cells
are twice the height and spend it on what the decision turns on. <b>Everything here is below
replacement</b> &mdash; that is not a reason to skip it, it is why the ordering stops helping and
the job flag starts. <b>Buy the job, never the name.</b> The flag says a job is
unresolved and what it is worth. Across nineteen unsettled backfields it has <i>no</i> opinion on
who wins it, and neither should you.</p>
<table><tr><th class="rd">Rd</th>{head}</tr>{sheet2}</table>
{KEY}
</div>"""
    with open(OUT_HTML, 'w', encoding='utf-8') as f:
        f.write(doc)
    print(f'  wrote {OUT_HTML} ({os.path.getsize(OUT_HTML)} bytes)')

    if a.no_pdf:
        return 0
    # doc 146: one renderer for the whole project. Importing it means this page inherits the
    # Chrome fallback and the measured zoom instead of growing a second copy of both.
    sys.path.insert(0, HERE)
    try:
        import to_pdf
    except Exception as e:
        print(f'  !! could not import to_pdf.py ({e}) -- page written, PDF NOT made')
        return 1
    kind, exe = to_pdf.find_renderer()
    if not exe:
        print('  !! no PDF renderer found -- page written, PDF NOT made')
        return 1
    why = to_pdf.render(kind, exe, OUT_HTML, OUT_PDF)
    if why:
        print(f'  !! {kind} failed: {why} -- page written, PDF NOT made')
        return 1
    print(f'  wrote {OUT_PDF} ({os.path.getsize(OUT_PDF)} bytes) via {kind}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
