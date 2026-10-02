#!/usr/bin/env python3
r"""
make_board.py -- ONE draft board. Everything about a player on his own row.

    py make_board.py            builds Source\DRAFT_BOARD.pdf (+ .html)
    py make_board.py --n 200    more rows

Doc 116. Matt: "these all carry player based information. Is there a way to condense into one
draft board listing without losing valuable information?"

WHAT IT REPLACES. Five paper artifacts each held one slice of one player:
    FALLBACK_BOARD    the ranking, and nothing about why
    LATE_RB_SHEET     the backfield picture, RBs only, picks 104-137 only
    AUDITION_WINDOW   the keeper-audition view, picks 56-89 only
    ANALYST_CALLS     who is high on whom, 78 players only
    INJURY_CONTEXT    the grades, as a spreadsheet nothing else could read
Flipping between them at 60 seconds a pick is the failure mode. This is one list, in VBD order
(the order you actually decide in), with everything that was in those five folded into the row.

SORTED BY VBD, NOT BY ADP, ON PURPOSE. On the clock the question is "who is the best player left
that fits my caps", which is a VBD question. `goes at` is a column so you can still see who will
keep. The pick strip at the top carries the ADP view that AUDITION_WINDOW used to carry.

Reads:  live_draft\board_v8_fixed.csv · live_draft\player_context.csv · depth_map.csv ·
        analyst_takes.csv (optional) · analyst_calls_joined.csv (optional) · news_overrides.csv
Writes: ..\Source\DRAFT_BOARD.pdf and .html.  Needs wkhtmltopdf; without it the .html still lands.
"""
import argparse, datetime as dt, html, os, re, shutil, subprocess, sys
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
KIT  = os.path.join(HERE, 'live_draft')
SRC  = os.path.normpath(os.path.join(HERE, '..', 'Source'))
SHOW_MINE = False
KEY_ROW = ('<tr class="key"><td colspan="11">'
    '<span class="b bA">AVOID</span> hurt or unavailable &nbsp;'
    '<span class="b bD">DISC&nbsp;14</span> injury flag &mdash; the number is games the sweep still '
    'expects him to play &nbsp;'
    '<span class="b bN">note</span> flagged, but 17 games expected &mdash; not a discount &nbsp;'
    '<span class="b bY">BUY</span> both analyst panels ahead of ADP &nbsp;'
    '<span class="b bO">OPEN</span> unsettled backfield &mdash; a job to be won &nbsp;'
    '<span class="b bS">DART</span> direct backup, pick 104+ &nbsp;'
    # doc 191: the composite. Three signals -- top-quartile 2025 target share, 13+ games,
    # NFL rounds 1-3.  Measured +12.2 pts of beat-vs-price per signal (p=0.0008, n=252 RB-seasons,
    # player-clustered).  Ladder: 0 of 3 = -24.4  |  1 = -19.3  |  2 = -0.4  |  3 of 3 = +7.8.
    # Only the ENDS are drawn: 2 of 3 measures ~0 and a badge there would be noise.
    '<span class="b bR3">3/3</span> RB: all three composite signals &mdash; measured +8 vs price &nbsp;'
    '<span class="b bR1">1/3</span> RB: one or none &mdash; measured &minus;20 &nbsp;'
    '<span class="b bG">11g</span><span class="b bG2">8g</span><span class="b bG3">4g</span> '
    '2025 games played &mdash; darker is worse; missing time repeats'
    '&nbsp;&nbsp;&#124;&nbsp;&nbsp; '
    '<b>row shading</b> &mdash; <span class="sw sa">pink = AVOID</span> '
    '<span class="sw sd">gold = a real DISC</span> white = neither &nbsp;'
    '<b>coloured line under a row</b> = last player in that position&rsquo;s tier '
    '(<span class="lg RB">RB</span> <span class="lg WR">WR</span> '
    '<span class="lg TE">TE</span> <span class="lg QB">QB</span>); '
    'the grey <b>TIER n</b> divider is the overall tier'
    '&nbsp;&nbsp;&#124;&nbsp;&nbsp; where the commentary sits: '
    '<span class="lp L2">BULL</span> <span class="lp L1">bull</span> '
    '<span class="lp L0">split</span> <span class="lp Lm1">bear</span> '
    '<span class="lp Lm2">BEAR</span> &nbsp; blank = nobody has said anything</td></tr>')
KEY_EVERY = 30
FIRST_UNITS, PAGE_UNITS = 36, 50  # RENDERED rows, not players: note rows and tier
                                  # dividers each cost one.  Page 1 carries the ladder.

PICKS = [8, 17, 32, 41, 56, 65, 80, 89, 104, 113, 128, 137, 152, 161]
EFF   = [8, 17, 35, 51, 66, 75, 91, 100, 115, 124, 140, 149, 164, 173]

CSS = """
@page{margin:8mm 7mm}
body{font:11.6px/1.30 "Segoe UI",Arial,sans-serif;color:#111;margin:0}
h1{font-size:18px;margin:0 0 3px;letter-spacing:.2px}
.sub{font-size:10.4px;color:#555;margin:0 0 6px}
.strip{background:#eef1f5;border:1px solid #ccd2da;padding:5px 7px;margin:0 0 7px;font-size:10.4px}
.strip b{color:#000}
.strip span{display:inline-block;margin-right:9px;white-space:nowrap}
.warn{background:#fdeceb;border-left:4px solid #c0392b;padding:5px 8px;margin:0 0 7px;font-size:10.6px}
table{border-collapse:collapse;width:100%}
th{background:#e9edf2;border-bottom:1.5px solid #97a0ac;text-align:left;padding:3px 4px;font-size:10px;
   text-transform:uppercase;letter-spacing:.4px}
td{padding:4px 5px;vertical-align:top;border-bottom:1px solid #eef0f3}
tr.a td{background:#fdeceb}
tr.d td{background:#fdf6e8}
tr.m td{box-shadow:inset 3px 0 0 #b8860b}
tr.note td{border-bottom:1px solid #e4e8ec;padding-top:0;padding-bottom:6px}
.pb{page-break-after:always}
.why{font-size:9.6px;color:#555;line-height:1.28}
.why b{color:#111}
.q{color:#15628f;font-style:italic}
.n{text-align:right;color:#333;width:30px}
.rk{text-align:right;color:#8b93a0;width:26px}
.pl{font-weight:600;white-space:nowrap}
.pos{font-weight:700;width:20px}
.QB{color:#6b3fa0}.RB{color:#12734f}.WR{color:#15628f}.TE{color:#9a6212}
.tm{color:#555;width:26px;font-size:10.4px}
.mk{white-space:nowrap;font-size:9px;font-weight:700;letter-spacing:.3px}
.b{display:inline-block;padding:0 3px;border-radius:2px;margin-right:2px;color:#fff}
.bA{background:#c0392b}.bD{background:#c98a17}.bM{background:#b8860b}.bY{background:#12734f}
.bO{background:#15628f}.bS{background:#6b7280}.bR3{background:#0f5d3f}.bR1{background:#8c6d3f}.bG{background:#f0ece0;color:#6b6250;border-color:#d8d0b8}.bG2{background:#e0d3a8;color:#4a4130;border-color:#c2b184}.bG3{background:#c9a86a;color:#3a3018;border-color:#a98a4c}.bN{background:#9aa3af}
.lean{font-size:9.2px;white-space:nowrap;font-weight:700;letter-spacing:.2px}
.lean span{display:inline-block;padding:1px 5px;border-radius:8px;border:1px solid}
.L2{background:#0f7a4d;border-color:#0b5c3a;color:#fff}
.L1{background:#dff2e7;border-color:#7cc39d;color:#0b5c3a}
.L0{background:#f0f2f5;border-color:#c3c9d2;color:#4a5260}
.Lm1{background:#fbe4e2;border-color:#e0a49d;color:#8f2c21}
.Lm2{background:#b8362a;border-color:#8f2c21;color:#fff}
thead{display:table-header-group}
.sw{padding:0 4px;border:1px solid #d8dce3;border-radius:2px}
.sa{background:#fdeceb}.sd{background:#fdf6e8}
.lg{font-weight:700;border-bottom:2px solid;padding-bottom:1px;margin:0 1px}
.lg.RB{color:#12734f;border-color:#12734f}.lg.WR{color:#15628f;border-color:#15628f}
.lg.TE{color:#9a6212;border-color:#9a6212}.lg.QB{color:#6b3fa0;border-color:#6b3fa0}
tr.key td{background:#fafbfc;border-bottom:1px solid #dfe3e8;padding:3px 4px;font-size:8.8px;color:#444}
.lp{display:inline-block;padding:0 5px;border-radius:8px;border:1px solid;font-weight:700;font-size:8.4px}
/* doc 128 */
td.bx{width:11px;padding-left:2px}
td.bx i{display:inline-block;width:7px;height:7px;border:1px solid #b6bcc6;border-radius:1px}
/* doc 134: the positional tier end is a rule UNDER THE WHOLE ROW in the position's colour.
   It used to be a border on the tier cell alone, which collided with the text beside it. */
/* doc 158.  This class used to be `te`, and EVERY tier line on the page came out the same
   gold -- Matt: "I couldn't easily figure out the rhyme or reason."  There was none to find.
   These pages carry no <!doctype>, so the browser renders them in QUIRKS MODE, where CSS class
   selectors match CASE-INSENSITIVELY.  `te` therefore also matched the POSITION class `TE`, so
   `tr.te.TE` -- last of the four and thus the winner -- painted the tight-end colour under
   running backs and receivers alike.  Measured off the rendered pixels: every rule was
   rgb(154,98,18) = #9a6212 = the TE colour.  Renamed to `tend`, which cannot collide.
   Renaming beats adding a doctype three days out: a doctype would also flip the box model and
   the page breaks on a document that is about to be printed and used. */
tr.tend td{border-bottom-width:1.5px;border-bottom-style:solid}
tr.tend.RB td{border-bottom-color:#12734f}
tr.tend.WR td{border-bottom-color:#15628f}
tr.tend.TE td{border-bottom-color:#9a6212}
tr.tend.QB td{border-bottom-color:#6b3fa0}
/* doc 134: the OVERALL tier break is its own labelled row, with air on both sides. */
tr.tb td{border:0;padding:9px 0 8px;font-size:9.2px;font-weight:700;letter-spacing:1.4px;
         color:#5b6470;text-align:center;white-space:nowrap}
tr.tb i{display:inline-block;height:0;border-top:1px solid #aab1bb;width:34%;
        vertical-align:middle;margin:0 9px}

td.ti{font-size:9px;font-weight:700;color:#5b6470}
.tier{font-size:9px;font-weight:700;letter-spacing:.2px;width:26px;text-align:center}
/* the ADP band lives on the ROW, as a left edge -- never as a divider across a VBD sort */
tr.b1 td:first-child{box-shadow:inset 3px 0 0 #14532d}
tr.b2 td:first-child{box-shadow:inset 3px 0 0 #2f7a4c}
tr.b3 td:first-child{box-shadow:inset 3px 0 0 #7cc39d}
tr.b4 td:first-child{box-shadow:inset 3px 0 0 #cfe3d6}
tr.b5 td:first-child{box-shadow:inset 3px 0 0 #eef1f4}
table.ladder{width:100%;border-collapse:collapse;margin:0 0 8px}
table.ladder td{vertical-align:top;width:25%;padding:0 6px 0 0;border:0}
table.ladder h4{margin:0 0 3px;font-size:11px;letter-spacing:.6px;text-transform:uppercase}
.tg{font-size:9.4px;line-height:1.35;margin-bottom:1px}
.tg b{display:inline-block;min-width:30px}
.tg span{color:#555}
.tl{font-size:9.2px;line-height:1.3;margin-bottom:2px;padding-left:2px}
.tn{display:inline-block;min-width:26px;font-weight:700}
.tv{display:inline-block;min-width:44px;color:#666}
.tw{color:#333}
.foot{padding-top:6px;font-size:9px;color:#777;text-align:center}
"""

def esc(t): return html.escape(str(t), quote=True)

def load():
    b = pd.read_csv(os.path.join(KIT, 'board_v8_fixed.csv'))
    def opt(p, **kw):
        return pd.read_csv(p, **kw) if os.path.exists(p) else pd.DataFrame()
    c = opt(os.path.join(KIT, 'player_context.csv'))
    d = opt(os.path.join(HERE, 'depth_map.csv'))
    t = opt(os.path.join(HERE, 'analyst_takes.csv'))
    j = opt(os.path.join(HERE, 'analyst_calls_joined.csv'))
    # doc 129: 2025 games played.  Static -- 2025 is over -- so it is a committed file, not a
    # script.  -1 means no 2025 regular-season snap at all (rookie, or a full miss).
    gp = opt(os.path.join(SRC, 'games_2025.csv'))
    m = b.copy()
    if len(c):
        keep = [x for x in ['ESPN_ID','grade','why','dart','buy','calls_up','calls_down','who',
                            'mine','mine_note','job','job_ceil'] if x in c.columns]
        m = m.merge(c[keep], left_on='espn_id', right_on='ESPN_ID', how='left')
    if len(d) and 'ahead' in d.columns:
        m = m.merge(d[['espn_id','ahead','depth']], on='espn_id', how='left')
    if len(t):
        m = m.merge(t[['player','lean','quote','source','concrete']], on='player', how='left')
    if len(j) and 'quote' in j.columns:
        m = m.merge(j[['player','quote']].rename(columns={'quote':'pod_quote'}), on='player', how='left')
    if len(gp) and 'g25' in gp.columns:
        m = m.merge(gp[['espn_id','g25']], on='espn_id', how='left')
    return m.fillna('')


# doc 128. TIERS. Matt asked for horizontal breaks -- "middle round players", "late round".
#
# A full-width divider on a VBD-SORTED list would be a lie: the list is not in draft order, so
# "the middle rounds" is not a contiguous block of it. Row 60 can be an ADP-25 player who slid.
#
# What he actually wants is "where does the value step down", and on a VBD sort that IS honest --
# but only WITHIN a position. A drop in RB value is not a drop in WR value, so the break belongs
# on the row, in the position's own colour, not across the page.
#
# Threshold: the (n-1)th largest gap inside the reachable part of each position, so each position
# gets a readable number of tiers instead of whatever an absolute cut-off happens to produce.
# The output is the directive made visible: QB1 is Allen ALONE and QB2 holds five men (4.14's
# 47-point cliff then an 11.8-point plateau); TE1 is Bowers and McBride, TE2 is Warren alone,
# TE3 is eight players (4.3).
TIER_TARGET = {'RB': 10, 'WR': 10, 'TE': 7, 'QB': 7}
TIER_DEPTH  = {'RB': 60, 'WR': 60, 'TE': 30, 'QB': 24}
BAND = [(0, 24, 'b1'), (24, 48, 'b2'), (48, 84, 'b3'), (84, 120, 'b4'), (120, 999, 'b5')]


def add_tiers(m):
    import numpy as np
    m['tier'] = 0
    for pos, ntier in TIER_TARGET.items():
        sub = m[(m.pos == pos) & (m.proj_leaguepts > 0)].sort_values('vbd', ascending=False)
        if len(sub) < 3: continue
        head = sub.head(TIER_DEPTH[pos])
        gaps = -np.diff(head.vbd.values)
        thr = np.sort(gaps)[-(ntier - 1)] if len(gaps) >= ntier else 0.0
        cur, out = 1, []
        allg = -np.diff(sub.vbd.values)
        for x in allg:
            out.append(cur)
            if x >= thr: cur += 1
        out.append(cur)
        m.loc[sub.index, 'tier'] = out
    # the LAST row of each positional tier gets the rule under it
    m['tier_end'] = False
    for (pos, t), sub in m[m.tier > 0].groupby(['pos', 'tier']):
        last = sub.sort_values('vbd', ascending=False).index[-1]
        m.loc[last, 'tier_end'] = True
    return m


def band_of(eff):
    try: e = float(eff)
    except (TypeError, ValueError): return ''
    for lo, hi, cls in BAND:
        if lo <= e < hi: return cls
    return ''


def tier_ladder(m):
    """Page 1. What the five sheets were really for: how deep is each position before it steps
    down. Read a column top to bottom and you can see whether waiting costs you anything."""
    cells = []
    for pos in ('RB', 'WR', 'TE', 'QB'):
        rows = []
        sub = m[(m.pos == pos) & (m.tier > 0)]
        for t in sorted(sub.tier.unique())[:6]:
            g = sub[sub.tier == t].sort_values('vbd', ascending=False)
            if g.empty: continue
            who = ', '.join(g.player.head(7))
            if len(g) > 7: who += f' +{len(g)-7}'
            rows.append(f'<div class="tl"><span class="tn {pos}">{pos}{t}</span>'
                        f'<span class="tv">{g.vbd.iloc[0]:.0f}&ndash;{g.vbd.iloc[-1]:.0f}</span>'
                        f'<span class="tw">{esc(who)}</span></div>')
        cells.append(f'<td><h4 class="{pos}">{pos}</h4>{"".join(rows)}</td>')
    return ('<table class="ladder"><tr>' + ''.join(cells) + '</tr></table>')



# doc 128b. Matt: "the tier break i had in mind was like the one we had on the board -- the one
# between Jahmyr Gibbs and Bijan." That break is real and it is NOT positional: it is a step down
# in OVERALL value, which on a VBD-sorted list is exactly what a full-width rule can honestly say.
# So there are two kinds of break on this page and they mean different things:
#   a full-width dashed rule  = the whole board steps down here
#   a coloured underline      = THAT POSITION steps down after this row
OVERALL_TIERS = 8       # full-width rules across the whole list
MIN_TIER = 4            # ...and never two of them within this many rows


def add_overall_tiers(m, n):
    """The gaps at the very top of a VBD list are all large, so a bare threshold puts a rule
    under every one of the first fifteen players and the page turns into a ladder. Take the
    largest gaps in order and refuse any that lands too close to one already taken."""
    import numpy as np
    top = m.sort_values('vbd', ascending=False).head(n)
    gaps = -np.diff(top.vbd.values)
    m['ovr_end'] = False
    idx = list(top.index)
    chosen = []
    for i in np.argsort(gaps)[::-1]:
        if len(chosen) >= OVERALL_TIERS - 1: break
        if all(abs(int(i) - c) >= MIN_TIER for c in chosen):
            chosen.append(int(i))
    for i in chosen: m.loc[idx[i], 'ovr_end'] = True
    return m


def targets(m, picks):
    """Two names to aim at per pick. NOT a recommendation -- the live board does that with a
    rollout. This is the static version: walk the picks in order and take the best VBD still
    plausibly on the board, so there is a plan on paper when the screen is gone."""
    pool = m[(m.pos.isin(['QB', 'RB', 'WR', 'TE'])) & (m.proj_leaguepts > 0)] \
             .sort_values('vbd', ascending=False)
    # Without caps this walks straight into the flat-VBD trap that produced the prerank defect:
    # once the RBs and WRs are spoken for, TEs carry the highest remaining VBD and the last three
    # turns come back as four tight ends. CAPS are the directive's own target roster (section 6:
    # never a second QB or TE unless a drought has actually happened).
    CAPS = {'QB': 1, 'RB': 6, 'WR': 6, 'TE': 1}
    REACH = 15          # and never name a man 15+ picks before the market takes him
    have = {k: 0 for k in CAPS}
    used, out = set(), []
    for p in picks:
        cand = pool[(~pool.player.isin(used)) &
                    (pool.eff_pick >= p - 3) & (pool.eff_pick <= p + REACH) &
                    (pool.pos.map(lambda q: have[q] < CAPS[q])) &
                    (pool.get('grade', '').astype(str) != 'AVOID')]   # Tank Dell is on IR
        # 4.13: from round 9 break near-ties toward the wider bet. Before round 9, never.
        if p >= 104 and 'job' in cand.columns:
            cand = cand.assign(_open=(cand.job.astype(str) == 'UNSETTLED').astype(int)) \
                       .sort_values(['_open', 'vbd'], ascending=[False, False])
        rows = cand.head(2)
        # two OPTIONS per turn, of which he takes one -- so only the first consumes a roster slot.
        # Counting both filled the caps at twice the real rate and the last five turns came back
        # empty, which is how this was caught.
        for k, (_, r) in enumerate(rows.iterrows()):
            used.add(r.player)
            if k == 0: have[r.pos] += 1
        out.append((p, [(r.player, r.pos, r.vbd, r.eff_pick) for _, r in rows.iterrows()]))
    return out


def marks(r):
    out = []
    g = str(r.get('grade','')).upper()
    # doc 135 (Matt): "DISC on Christian McCaffrey can't be right -- there is no taking him later."
    # He was right.  11 of 32 DISCOUNT rows carry `exp 17 gm` from the sweep itself, i.e. the tag
    # was firing on load-management notes.  The expected-games number is what makes it readable,
    # so it goes ON the badge, and a 17 demotes it to a plain note.
    exg = re.search(r'exp (\d+) gm', str(r.get('why','')))
    exg = int(exg.group(1)) if exg else None
    if g == 'AVOID':
        out.append(('bA','AVOID %d'%exg if exg is not None else 'AVOID'))
    elif g == 'DISCOUNT':
        if exg is not None and exg >= 17: out.append(('bN','note'))
        else: out.append(('bD','DISC %d'%exg if exg is not None else 'DISC'))
    if SHOW_MINE and _i(r.get('mine')) > 0:  out.append(('bM','MINE'))
    if SHOW_MINE and _i(r.get('mine')) < 0:  out.append(('bA','FADE'))
    if _i(r.get('buy')):       out.append(('bY','BUY'))
    if str(r.get('job','')) == 'UNSETTLED' and r.get('pos') == 'RB': out.append(('bO','OPEN'))
    if _i(r.get('dart')) and float(r.get('eff_pick') or 0) >= 90:    out.append(('bS','DART'))
    # doc 129.  Prior-year availability is the one injury signal this project could TEST, and it
    # came back positive: a WR who missed time last season loses ~3.7 more games the next one
    # (r=+0.50, n=710 pairs) and came in 25 points under his projection (n=45, p=0.003).  RB null.
    # Shown as a fact for every position; the measured penalty is WR-only.  Surfaced, NOT scored.
    # doc 130: the penalty is DOSE-DEPENDENT, so the badge is shaded, not binary.
    # measured mean beat vs projection, by games played the prior season:
    #   1-6 g  -40.8  |  7-9 g  -27.1  |  10-12 g  -16.9  |  13+ g  -12.6 (baseline)
    sig = re.search(r'RB SIGNALS: (\d)/3', str(r.get('why','')))
    if sig:
        s = int(sig.group(1))
        if s == 3:   out.append(('bR3','3/3'))
        elif s <= 1: out.append(('bR1','%d/3' % s))
    g25 = _i(r.get('g25', 0))
    if 0 < g25 <= 12:
        out.append(('bG3' if g25 <= 6 else 'bG2' if g25 <= 9 else 'bG', '%dg' % g25))
    return ''.join(f'<span class="b {c}">{t}</span>' for c, t in out[:4])

def _i(v):
    try: return int(float(v or 0))
    except (TypeError, ValueError): return 0

NOISE = re.compile(r'\s*\|\s*(exp \d+ gm|\[(low|medium|high) confidence\])', re.I)

def note(r):
    bits = []
    why = str(r.get('why','')).split('||')[0].strip()
    if str(r.get('grade','')).upper() not in ('AVOID','DISCOUNT'):
        why = NOISE.sub('', why).strip(' |')
    else:
        why = re.sub(r'\s*\|\s*\[(low|medium|high) confidence\]', '', why, flags=re.I).strip(' |')
    # "no injury news found" on 107 of 143 rows is not information, it is the absence of it.
    # Keep it ONLY where a grade makes it meaningful; otherwise the page is 60% boilerplate.
    if why.lower().startswith('no injury news found') and \
       str(r.get('grade','')).upper() not in ('AVOID', 'DISCOUNT'):
        why = ''
    if why and why.lower() != 'nan': bits.append(esc(why[:190]))
    # doc 199.  `why` is a MULTI-SEGMENT field and the line above prints segment 0 only, so the
    # measured signals -- which are appended as later segments -- were on the tier sheet and the
    # badge but NOT on the card, while doc 199 claimed they were.  Found by Matt asking which
    # sheets he can print.  Surfaced COMPACTLY: the badge already says what it means, the card
    # carries the NUMBER.  The red-zone segment is deliberately NOT printed -- it tested null
    # (doc 193) and null signals do not get board ink.
    raw = str(r.get('why', ''))
    m = re.search(r'RB TGT SHARE 2025: ([\d.]+% \w+)', raw)
    if m: bits.append('tgt ' + esc(m.group(1)))
    # 5 of 61 stamps carry no (+N vs 2024) delta -- a rookie has no 2024 baseline -- and requiring
    # it dropped exactly those, Burden's 40% BOTTOM among them.  The delta is optional.
    m = re.search(r'SNAP SHARE 2025: (\d+% \w+)(?: \(([+-]\d+) vs 2024\))?', raw)
    if m:
        seg = 'snaps %s%s' % (m.group(1), ' (%s)' % m.group(2) if m.group(2) else '')
        a = re.search(r'air-yard share ([\d.]+%)', raw)
        if a: seg += ' &middot; air ' + a.group(1)
        bits.append(esc(seg).replace('&amp;middot;', '&middot;'))
    # the backfield label describes a JOB, so it belongs on the man who might take it -- printing
    # "LEAD BACK, job worth 331" beside Jahmyr Gibbs tells you nothing you did not know.
    show_job = (r.get('pos') == 'RB' and
                (_i(r.get('depth')) >= 2 or str(r.get('job','')) == 'UNSETTLED'))
    if show_job and str(r.get('job','')):
        jb = f"{r['job']}"
        if str(r.get('ahead','')): jb += f", behind {esc(r['ahead'])}"
        if str(r.get('job_ceil','')): jb += f", job worth {str(r['job_ceil']).split('.')[0]}"
        bits.append(f'<b>{jb}</b>')
    if SHOW_MINE and str(r.get('mine_note','')).strip():
        bits.append(f'<b>YOUR TAKE:</b> {esc(str(r["mine_note"])[:130])}')
    q = str(r.get('quote','')).strip() or str(r.get('pod_quote','')).strip()
    if q and q.lower() != 'nan':
        who = str(r.get('who','')) or str(r.get('source',''))[:44]
        bits.append(f'<span class="q">&ldquo;{esc(q[:170])}&rdquo;</span>'
                    + (f' &mdash; {esc(who)}' if who and who.lower() != 'nan' else ''))
    if str(r.get('concrete','')).strip():
        bits.append(esc(str(r['concrete'])[:150]))
    return ' &middot; '.join(bits)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=180)
    # This board carries EVIDENCE. Matt's own takes are a decision aid at the moment of picking,
    # which is the live board's job -- printing them here reads his opinion back to him as if it
    # were a source, and it produced a row marked BUY and FADE at the same time.
    ap.add_argument('--mine', action='store_true', help="also print your own takes (off by default)")
    a = ap.parse_args()
    global SHOW_MINE
    SHOW_MINE = a.mine
    m = load()
    m = add_tiers(m)
    m = add_overall_tiers(m, a.n)
    ladder = tier_ladder(m)
    tg = targets(m, PICKS[:12])
    plan = '<div class="strip"><b>A PLAN FOR THE PAPER</b> &mdash; the best two still plausibly on '\
           'the board at each turn, walked in order. The live board decides with a rollout; this is '\
           'what to aim at when the screen is gone.<br>' + ' &nbsp;'.join(
        f'<span class="tg"><b>{p}</b> <span>' +
        ', '.join(f'{nm} ({ps})' for nm, ps, v, e in lst) + '</span></span>'
        for p, lst in tg) + '</div>'
    m = m[m.pos.isin(['QB','RB','WR','TE'])].sort_values('vbd', ascending=False).head(a.n)
    strip = ' '.join(f'<span><b>{p}</b> &rarr; ~{e}</span>' for p, e in zip(PICKS, EFF))
    HEAD = ('<table><thead>' + KEY_ROW +
            '<tr><th></th><th>#</th><th>player</th><th>pos</th><th>tier</th><th>tm</th><th>bye</th>'
            '<th>vbd</th><th>goes&nbsp;at</th><th>marks</th><th>lean</th></tr></thead><tbody>')
    rows = []
    units, budget = 0, FIRST_UNITS          # doc 134: count RENDERED rows, not players
    ovr_n = 1
    for i, (_, r) in enumerate(m.iterrows(), 1):
        nt = note(r)
        # doc 134: a note WRAPS.  Costing it a flat 1 unit is what overflowed pages 2 and 6 --
        # a 300-character note is three printed lines, not one.  ~135 chars fit on a line at
        # 9.6px across the note's colspan; charge accordingly so a wordy news cycle cannot
        # silently push a page over again.
        import re as _re
        ntxt = _re.sub(r'<[^>]+>', '', nt) if nt else ''
        cost = 1 + (max(1, -(-len(ntxt) // 135)) if nt else 0)
        if units and units + cost > budget:
            rows.append('</tbody></table><div class="pb"></div>' + HEAD)
            units, budget = 0, PAGE_UNITS
        units += cost
        cls = []
        # doc 157.  Matt, on seeing McCaffrey, Jeanty and Breece Hall all shaded: "remind why are
        # some rows shaded gold?"  They are DISCOUNT rows -- but doc 135 already established that
        # 11 of the 32 DISCOUNT grades fire on load-management notes, not on risk, and demoted
        # THEIR BADGE to a plain grey `note` when the sweep expects a full 17 games.  The ROW
        # SHADING was never demoted with it, so a third of the gold rows were warning about
        # players the badge system had already stood down -- McCaffrey, Jeanty, Hall, Nabers,
        # Judkins, Mahomes and five more.  Half a fix is how a page ends up contradicting itself.
        # The shading now follows the badge exactly: gold only when the badge really says DISC.
        _g = str(r.get('grade','')).upper()
        _x = re.search(r'exp (\d+) gm', str(r.get('why','')))
        _x = int(_x.group(1)) if _x else None
        if _g == 'AVOID': cls.append('a')
        elif _g == 'DISCOUNT' and not (_x is not None and _x >= 17): cls.append('d')
        if SHOW_MINE and _i(r.get('mine')) != 0: cls.append('m')
        cls.append(band_of(r.eff_pick))
        if r.get('tier_end') and not nt: cls += ['tend', str(r.pos)]
        cls = [c for c in cls if c]
        cl = (' class="%s"' % ' '.join(cls)) if cls else ''
        lean = str(r.get('lean','')).strip()
        LCL = {'strongly bull':'L2','lean bull':'L1','genuinely split':'L0',
               'lean bear':'Lm1','strongly bear':'Lm2'}
        LTX = {'strongly bull':'BULL','lean bull':'bull','genuinely split':'split',
               'lean bear':'bear','strongly bear':'BEAR'}
        leanhtml = (f'<span class="{LCL[lean]}">{LTX[lean]}</span>' if lean in LCL else '')
        rows.append(
            f'<tr{cl}><td class="bx"><i></i></td><td class="rk">{i}</td>'
            f'<td class="pl">{esc(r.player)}</td>'
            f'<td class="pos {r.pos}">{r.pos}</td>'
            f'<td class="tier {r.pos}">{(str(r.pos)+str(int(r.tier))) if r.tier else ""}</td>'
            f'<td class="tm">{esc(r.team_c)}</td>'
            f'<td class="n">{int(r.bye) if str(r.bye) not in ("","nan") else ""}</td>'
            f'<td class="n">{r.vbd:.0f}</td><td class="n">{r.eff_pick:.0f}</td>'
            f'<td class="mk">{marks(r)}</td><td class="lean">{leanhtml}</td></tr>')
        if nt:
            ncls = cls + (['tend', str(r.pos)] if r.get('tier_end') else [])
            rows.append(f'<tr class="note{" "+" ".join(ncls) if ncls else ""}">'
                        f'<td></td><td></td><td colspan="9" class="why">{nt}</td></tr>')
        # doc 134: the overall tier break is a labelled divider row of its own, placed AFTER the
        # last player of the tier and its note -- never a border painted over the row above.
        if r.get('ovr_end'):
            ovr_n += 1
            rows.append('<tr class="tb"><td colspan="11"><i></i>'
                        f'TIER {ovr_n}<i></i></td></tr>')
            units += 1
    doc = f"""<meta charset="utf-8"><style>{CSS}</style>
<h1>DRAFT BOARD &mdash; JUG, slot 8 &middot; Mon Sept 7, 8:00 PM</h1>
<p class="sub">One list, {len(m)} players, sorted by VOR &mdash; the order you decide in.
Replaces the fallback board, the late-RB sheet, the audition window, the analyst calls sheet and
the injury spreadsheet. Cross off names as they go; take the highest row that fits your caps
(QB2 / RB6 / WR6 / TE2). Generated {dt.datetime.now():%b %d %Y, %H:%M}.</p>
<div class="strip"><b>YOUR PICKS &rarr; the effective ADP available there:</b><br>{strip}</div>
{ladder}{plan}
<div class="warn"><b>Read the row, not just the rank.</b> The full key is repeated at the foot of
every page. <b>lean</b> is where the weight of 2026 preseason commentary sits &mdash; blank means
nobody has said anything, which is not the same as agreement. Byes cost at most 1.2 points, so they
break a tie and never make a pick. Everything on a row is EVIDENCE; your own calls live on the live
board, not here.</div>
{HEAD}{''.join(rows)}</tbody></table>
<p class="foot">make_board.py &middot; board_v8_fixed.csv + player_context.csv + depth_map.csv + analyst_takes.csv</p>"""
    hp = os.path.join(SRC, 'DRAFT_BOARD.html')
    open(hp, 'w', encoding='utf-8').write(doc)
    exe = shutil.which('wkhtmltopdf')
    if not exe:
        print(f"  wkhtmltopdf not on PATH -- wrote {hp}; print it to PDF by hand."); return
    pdf = os.path.join(SRC, 'DRAFT_BOARD.pdf')
    r = subprocess.run([exe, '--enable-local-file-access', '--quiet', '-s', 'Letter',
                        '-B', '8mm', '-T', '8mm', hp, pdf])
    if r.returncode or not os.path.exists(pdf) or os.path.getsize(pdf) < 2048:
        sys.exit(f"  PDF BUILD FAILED (rc={r.returncode}) -- the old {os.path.basename(pdf)} is STALE.")
    print(f"  wrote {pdf}  ({os.path.getsize(pdf):,} bytes, {len(m)} players)")
    print("  Now  py sync_desk_copies.py")

if __name__ == '__main__':
    main()
