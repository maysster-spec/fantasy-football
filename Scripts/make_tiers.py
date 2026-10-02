"""
make_tiers.py -- doc 192.  THE TIER SHEET.

Matt, 2026-09-06: "a new draft grid that shows our rankings like we have them on the board...
turning the draft board into a grid may help more with the tiering making sense because ADP
won't be in order of the tiering."

He is right and this is the missing artifact.  We ship two things today and neither answers the
question he is actually asking at the table:

  DRAFT_BOARD.pdf  is our ranking, but as a 180-row LIST over seven pages.  The tier lines are
                   there  and you cannot see across them -- RB tier 3 and WR tier 3 are
                   forty rows apart.
  ADP_GRID.pdf     is a 12-wide snake in PICK order.  A positional tier is scattered across it by
                   construction, because the market does not sort by our value.

The question under a 60-second clock is "how many are LEFT in this tier, and do any survive to my
next turn."  Neither artifact answers it in one look.  This one is built for exactly that:
one column per position, one row per tier, and every player carries the pick he is expected to
go at, so the count that matters is a glance instead of a search.

TIERS ARE NOT RE-DERIVED HERE.  `add_tiers` is imported from make_board.py -- one derivation,
two consumers, the same rule doc 146 used for `to_pdf.render`.  A second copy of that gap logic
would be the two-names-for-one-job defect (SS0.2).

Reads : Scripts\\live_draft\\board_v8_fixed.csv, player_context.csv, Scripts\\depth_map.csv
Writes: Source\\TIER_SHEET.html and .pdf
Run   : py make_tiers.py
"""
import os
import re
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))          # SS0.4: never the shell's cwd
KIT = os.path.join(HERE, 'live_draft')
SRC = os.path.normpath(os.path.join(HERE, '..', 'Source'))
OUT_HTML = os.path.join(SRC, 'TIER_SHEET.html')
OUT_PDF = os.path.join(SRC, 'TIER_SHEET.pdf')

MATT_PICKS = [8, 17, 32, 41, 56, 65, 80, 89, 104, 113, 128, 137, 152, 161]
POS = ['RB', 'WR', 'TE', 'QB']
PCOL = {'RB': '#d6efe2', 'WR': '#dbe7f6', 'TE': '#f6e6d6', 'QB': '#eee0f2'}

CSS = """
<style>
*{box-sizing:border-box}
body{font:11.5px/1.35 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;margin:14px;color:#1a1a1a}
h1{font-size:16px;margin:0 0 2px}
.sub{font-size:10px;color:#555;margin:0 0 8px}
table{border-collapse:collapse;width:100%;table-layout:fixed}
th{font-size:11px;text-align:left;padding:3px 5px;border-bottom:2px solid #333}
th.RB{background:#d6efe2}th.WR{background:#dbe7f6}th.TE{background:#f6e6d6}th.QB{background:#eee0f2}
td{vertical-align:top;padding:4px 6px;border-bottom:1px solid #d8d8d8;width:25%}
.tn{font-size:9px;font-weight:700;color:#666;letter-spacing:.3px}
.p{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.nm{font-weight:600}
.v{color:#0f5d3f;font-weight:700}.v.neg{color:#a33}
.at{color:#555}
.gone{color:#999}
.mine{background:#fff6c9}
.b{display:inline-block;padding:0 3px;border-radius:2px;color:#fff;font-size:9px;margin-left:2px}
.bA{background:#c0392b}.bD{background:#c98a17}.bY{background:#12734f}
.bO{background:#15628f}.bR3{background:#0f5d3f}.bR1{background:#8c6d3f}
.sp{font-size:9px;font-weight:700;color:#7a7a7a;letter-spacing:.3px;border-top:1px dotted #bbb;margin:3px 0 1px;padding-top:2px}
.by{color:#777;font-size:9.5px}\n.rz{color:#555;font-size:9px;font-weight:600}\n.rz1{color:#8a2b1f;background:#f7e3df;padding:0 2px;border-radius:2px}
.key{font-size:9.5px;color:#444;margin-top:8px;line-height:1.5}
.key b{color:#111}
@media print{body{margin:8px}}
</style>
"""


def _i(v):
    try:
        return int(float(v or 0))
    except (TypeError, ValueError):
        return 0


def badges(r):
    """The same marks the board draws, trimmed to the four that change a tier decision."""
    out = []
    g = str(r.get('grade', '')).upper()
    exg = re.search(r'exp (\d+) gm', str(r.get('why', '')))
    exg = int(exg.group(1)) if exg else None
    if g == 'AVOID':
        out.append(('bA', 'AVOID'))
    elif g == 'DISCOUNT' and not (exg is not None and exg >= 17):
        out.append(('bD', 'DISC'))
    if _i(r.get('buy')):
        out.append(('bY', 'BUY'))
    if str(r.get('job', '')) == 'UNSETTLED' and r.get('pos') == 'RB':
        out.append(('bO', 'OPEN'))
    sig = re.search(r'RB SIGNALS: (\d)/3', str(r.get('why', '')))
    if sig:
        s = int(sig.group(1))
        if s == 3:
            out.append(('bR3', '3/3'))
        elif s <= 1:
            out.append(('bR1', '%d/3' % s))
    return ''.join('<span class="b %s">%s</span>' % (c, t) for c, t in out[:3])


def wr_mark(r):
    """WR/TE only. Games played last season -- the ONE receiver signal that measures.

    doc 193.  I shipped a red-zone mark here an hour before this, labelled "a raw fact, not a
    tested signal", because SS4.5 says inside-10 targets persist at r=+0.59.  Then I built the
    red-zone panel from five seasons of play-by-play (2,032 player-seasons, new to the project)
    and TESTED it: in-10 targets -0.3 (p=0.64), in-10 TDs -1.1 (p=0.39), and targets-net-of-TDs
    -- the "he is owed touchdowns" idea the green highlight encoded -- +0.4 (p=0.59).  All null.
    The role persists AND the market already pays for it.

    What does measure, on the same 390 receiver-seasons: prior games played, +1.7 per game
    (p=0.043).  So that is what prints.  Matt: "don't add noise that can't be measured."
    """
    out = ''
    try:
        g = int(float(r.get('g25', 0) or 0))
    except (TypeError, ValueError):
        g = 0
    if 0 < g <= 12:
        out += ' <span class="rz%s">%dg</span>' % (' rz1' if g <= 9 else '', g)
    # doc 197: 2025 snap share. +0.79 points of beat per point of share (p<0.0001), and the ONLY
    # receiver signal that survives the prior-games control -- prior games drops to p=0.73 with it
    # in. Drawn only at the bottom of the board, where it is a warning: a receiver at 70% or less
    # of his team's snaps was not on the field, whatever his rate stats say.
    m = re.search(r'SNAP SHARE 2025: (\d+)% (TOP|BOTTOM|mid)', str(r.get('why', '')))
    if m and m.group(2) == 'BOTTOM':
        out += ' <span class="rz rz1">%s%% snaps</span>' % m.group(1)
    elif m and m.group(2) == 'TOP':
        out += ' <span class="rz">%s%% snaps</span>' % m.group(1)
    return out


def main():
    sys.path.insert(0, HERE)
    try:
        from make_board import add_tiers                    # one derivation, two consumers
    except Exception as e:
        print('  !! could not import add_tiers from make_board.py (%s) -- nothing written' % e)
        return 1

    b = pd.read_csv(os.path.join(KIT, 'board_v8_fixed.csv'))
    for col in ('pos', 'vbd', 'proj_leaguepts', 'eff_pick', 'adp_pick', 'player', 'espn_id'):
        assert col in b.columns, 'board_v8_fixed.csv is missing %r' % col

    ctx_p = os.path.join(KIT, 'player_context.csv')
    if os.path.exists(ctx_p):
        c = pd.read_csv(ctx_p).rename(columns={'ESPN_ID': 'espn_id'})
        keep = [k for k in ('espn_id', 'grade', 'buy', 'why') if k in c.columns]
        b = b.merge(c[keep], on='espn_id', how='left')
    # doc 129's committed static file -- the same source make_board.py reads for its 12g badge.
    g_p = os.path.join(SRC, 'games_2025.csv')
    if os.path.exists(g_p):
        g = pd.read_csv(g_p)[['espn_id', 'g25']].drop_duplicates('espn_id')
        b = b.merge(g, on='espn_id', how='left')
    else:
        print('  !! games_2025.csv not found -- the WR games mark will not print')

    dm_p = os.path.join(HERE, 'depth_map.csv')
    if os.path.exists(dm_p):
        d = pd.read_csv(dm_p)
        if 'job' in d.columns:
            b = b.merge(d[['espn_id', 'job']], on='espn_id', how='left')

    b = add_tiers(b)
    live = b[(b.tier > 0) & (b.adp_pick < 168)].copy()

    cells = {}
    ntier = 0
    for p in POS:
        sub = live[live.pos == p].sort_values('vbd', ascending=False)
        for t, grp in sub.groupby('tier'):
            cells[(p, int(t))] = grp
            ntier = max(ntier, int(t))

    rows = []
    for t in range(1, ntier + 1):
        tds = []
        for p in POS:
            grp = cells.get((p, t))
            if grp is None or not len(grp):
                tds.append('<td></td>')
                continue
            lines = []
            big = len(grp) > 8          # only the flat tail needs breaking up
            # Inside a tier every name is close in value by construction, so VALUE order carries
            # almost nothing once the tier is long -- and it makes the turn blocks non-contiguous.
            # Long tiers therefore sort by the pick, which is the order the question is asked in.
            if big:
                grp = grp.sort_values('eff_pick')
            last_turn = None
            for _, r in grp.iterrows():
                eff = float(r.eff_pick)
                # the number that decides it: the pick he is expected to go at
                nxt = next((q for q in MATT_PICKS if q >= eff), None)
                if big and nxt != last_turn:
                    lines.append('<div class="sp">%s</div>' % (
                        ('BY YOUR PICK %d' % nxt) if nxt else 'AFTER YOUR LAST PICK'))
                    last_turn = nxt
                cls = ' gone' if eff < MATT_PICKS[0] else ''
                v = float(r.vbd)
                lines.append(
                    '<div class="p%s"><span class="nm">%s</span> '
                    '<span class="v%s">%+d</span> '
                    '<span class="at">~%d</span> <span class="by">b%s</span>%s</div>' % (
                        cls, str(r.player)[:22], '' if v >= 0 else ' neg', round(v),
                        round(eff), r.get('bye', '?'),
                        badges(r) + (wr_mark(r) if r.pos in ('WR', 'TE') else '')))
            tds.append('<td class="%s">%s</td>' % (p, ''.join(lines)))
        rows.append('<tr><td colspan="4" class="tn">TIER %d</td></tr><tr>%s</tr>'
                    % (t, ''.join(tds)))

    html = (
        '<!doctype html><html><head><meta charset="utf-8"><title>Tier Sheet</title>' + CSS +
        '</head><body><h1>TIER SHEET &mdash; our ranking, arranged by tier</h1>'
        '<p class="sub">One column per position, one row per tier, best first inside each cell. '
        'The green number is VOR (points above a replacement starter). '
        'The grey <b>~n</b> is the pick he is expected to go at and <b>b</b> is his bye. '
        'Any tier with more than eight names is broken into <b>BY YOUR PICK n</b> blocks &mdash; '
        'everyone in a block is expected to be gone by that turn of yours. '
        'Your picks: ' + ' &middot; '.join(str(x) for x in MATT_PICKS) + '. '
        'Tiers are the board&rsquo;s own, imported &mdash; not recomputed here.</p>'
        '<table><tr>' + ''.join('<th class="%s">%s</th>' % (p, p) for p in POS) + '</tr>' +
        ''.join(rows) + '</table>'
        '<p class="key"><b>How to use it:</b> find the tier you are picking in, count how many '
        'names in it have a <b>~n</b> below your next pick. If none do, the tier breaks before you '
        'come back and the choice is now. If several do, you can take the other position.<br>'
        '<b>Tiers are the board&rsquo;s own, imported &mdash; not recomputed here.</b> &nbsp;'
        '<span class="b bA">AVOID</span> hurt or unavailable &nbsp;'
        '<span class="b bD">DISC</span> injury flag &nbsp;'
        '<span class="b bY">BUY</span> both analyst panels ahead of ADP &nbsp;'
        '<span class="b bO">OPEN</span> unsettled backfield &nbsp;'
        '<span class="b bR3">3/3</span> / <span class="b bR1">1/3</span> a back carrying all three '
        'signals that measure &mdash; a real share of his team&rsquo;s targets, 13+ games last year, '
        'drafted in the NFL&rsquo;s first three rounds. Each one is worth about twelve points. &nbsp;'
        '<span class="rz rz1">9g</span> games he played in 2025, darker under ten &mdash; every game '
        'he missed is worth about two points off this year. &nbsp;'
        '<span class="rz">88% snaps</span> / <span class="rz rz1">40% snaps</span> how much of his '
        'team&rsquo;s season he was actually on the field for, drawn only at the top and bottom of the '
        'league. <b>Red means he was not out there</b>, and it is the strongest receiver warning we have.'
        '</p></body></html>')

    with open(OUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    print('  wrote %s (%d bytes, %d players in %d tiers)'
          % (OUT_HTML, os.path.getsize(OUT_HTML), len(live), ntier))

    # doc 146: one renderer for the whole project, imported rather than shelled out to.
    try:
        import to_pdf
    except Exception as e:
        print('  !! could not import to_pdf.py (%s) -- page written, PDF NOT made' % e)
        return 1
    kind, exe = to_pdf.find_renderer()
    if not kind:
        print('  !! no PDF renderer found -- page written, PDF NOT made')
        return 1
    why = to_pdf.render(kind, exe, OUT_HTML, OUT_PDF)
    if why or not os.path.exists(OUT_PDF):
        print('  !! PDF NOT made (%s)' % (why or 'no output'))
        return 1
    print('  wrote %s (%d bytes) via %s' % (OUT_PDF, os.path.getsize(OUT_PDF), kind))
    return 0


if __name__ == '__main__':
    sys.exit(main())
