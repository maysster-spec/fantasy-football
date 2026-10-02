r"""mkoverride.py -- the instrument doc 62 Option A always needed and never had.

doc 62 CONFIRMED that `board_v8_fixed.csv` HAS NO BUILDER: no script produces it, and
`code_build_board_v7.py` is hardcoded to the Aug-23 pull and writes a differently-named file
that was trashed as a trap.  So when `sept5_check.py` returns REBUILD, there is nothing to run.
doc 62 s5 Option A is the standing answer -- "draft off the verified board, handle the news
manually as overrides at the pick" -- but nobody ever built the thing you hold while doing that.

This is it.  It compares the SHIPPED board against the NEWEST pull and prints, for every player
whose projection has moved enough to matter, what the board says versus what ESPN now says.

BASELINE, stated on the card: VBD against s4.1's replacement levels, recomputed from the new
projection with the board's own arithmetic, so old and new ranks are on one scale.
POPULATION: every board row.  It reports the ones that move.
"""
import os, sys, datetime as dt, html, shutil, subprocess
import pandas as pd, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
KIT  = os.path.join(HERE, 'live_draft')
SRC  = os.path.normpath(os.path.join(HERE, '..', 'Source'))
REPL = {'QB': 341.603, 'RB': 168.589, 'WR': 163.540, 'TE': 140.295}   # s4.1
MOVE = 15.0          # points of projection change worth a card line
DEEP = 175           # ignore churn beyond any pick Matt owns

def newest_pull():
    import glob
    c = sorted(glob.glob(os.path.join(SRC, 'espn_projections_2026_*.csv')))
    if not c: sys.exit(f'  no 2026 pull in {SRC}')
    return c[-1]

def main():
    pull = sys.argv[1] if len(sys.argv) > 1 else newest_pull()
    b = pd.read_csv(os.path.join(KIT, 'board_v8_fixed.csv'))
    p = pd.read_csv(pull); p.columns = [c.replace('﻿', '') for c in p.columns]
    col = [c for c in p.columns if c.startswith('proj_2026')]
    if not col: sys.exit(f'  {os.path.basename(pull)} has no proj_2026 column')
    p = p[['espn_id', col[0]]].rename(columns={col[0]: 'new_proj'})
    n = len(b); m = b.merge(p, on='espn_id', how='left')
    assert len(m) == n, 'pull merge inflated the board -- duplicate espn_id in the pull'

    # recompute VBD and rank on the NEW projection, with the board's own arithmetic
    m['new_proj'] = pd.to_numeric(m.new_proj, errors='coerce')
    have = m.new_proj.notna()
    m['new_vbd'] = m.new_proj - m.pos.map(REPL)
    m['new_rank'] = m.new_vbd.rank(ascending=False, method='first')
    m['delta'] = (m.new_proj - m.proj_leaguepts).round(1)

    # s4.22 / doc 101: a player the NEWS says is out must never be "restored" by a pull.
    news = os.path.join(HERE, 'news_overrides.csv')
    held = {}
    if os.path.exists(news):
        nw = pd.read_csv(news)
        held = dict(zip(nw.espn_id, nw.note.fillna(nw.action)))

    live = m[have & ((m['rank'] <= DEEP) | (m.new_rank <= DEEP)) & (m.delta.abs() >= MOVE)]
    live = live.reindex(live.delta.abs().sort_values(ascending=False).index)
    print(f'  board  : {os.path.basename(os.path.join(KIT,"board_v8_fixed.csv"))}  ({n} rows)')
    print(f'  pull   : {os.path.basename(pull)}')
    print(f'  movers : {len(live)} inside pick {DEEP} moved >= {MOVE:.0f} projected points')
    print(f'  {len(m[~have])} board rows are not in this pull (they keep the board number)\n')
    rows = []
    for _, r in live.iterrows():
        note = held.get(r.espn_id, '')
        rows.append(dict(player=r.player, pos=r.pos, team=r.team_c, adp=r.adp_pick,
                         old_rank=int(r['rank']), new_rank=int(r.new_rank),
                         old_proj=r.proj_leaguepts, new_proj=r.new_proj, delta=r.delta,
                         hold=bool(note), note=note))
        flag = '  <-- NEWS OVERRIDE HOLDS, IGNORE THE PULL' if note else ''
        print(f'    {r.player:<24}{r.pos:<4}{r.team_c:<4} adp{r.adp_pick:6.1f}   '
              f'rank {int(r["rank"]):>3} -> {int(r.new_rank):>3}   '
              f'proj {r.proj_leaguepts:6.1f} -> {r.new_proj:6.1f} ({r.delta:+6.1f}){flag}')
    pd.DataFrame(rows).to_csv(os.path.join(SRC, 'override_card.csv'), index=False)
    render(rows, pull)

CSS = """@page{margin:10mm 9mm}
body{font:11.5px/1.35 "Segoe UI",Arial,sans-serif;color:#111;margin:0}
h1{font-size:17px;margin:0 0 2px}.sub{font-size:10.2px;color:#555;margin:0 0 9px}
.warn{background:#fdeceb;border-left:4px solid #c0392b;padding:7px 10px;margin:0 0 10px;font-size:10.5px}
table{border-collapse:collapse;width:100%}
th{text-align:left;font:700 8.4px/1 Arial;letter-spacing:.5px;text-transform:uppercase;
   color:#8b93a0;border-bottom:1px solid #ccd2da;padding:2px 5px}
th.r{text-align:right}
td{padding:4px 5px;border-bottom:1px solid #eef0f3;font-size:11px;vertical-align:top}
.n{text-align:right;font-variant-numeric:tabular-nums}
.pl{font-weight:600;white-space:nowrap}.tm{font-size:9.4px;color:#667;font-family:Consolas,monospace}
.up{color:#12734f;font-weight:700}.dn{color:#c0392b;font-weight:700}
.hold{background:#fff6e5}
.note{font-size:9px;color:#8a4b12}
.foot{font-size:9px;color:#777;text-align:center;padding-top:10px}"""

def render(rows, pull):
    e = lambda x: html.escape(str(x))
    tr = ''
    for r in rows:
        cls = ' class="hold"' if r['hold'] else ''
        d = r['delta']; dc = 'up' if d > 0 else 'dn'
        note = f'<div class="note">{e(r["note"])[:150]}</div>' if r['hold'] else ''
        tr += (f'<tr{cls}><td class="pl">{e(r["player"])}{note}</td>'
               f'<td class="tm">{e(r["team"])}</td><td>{e(r["pos"])}</td>'
               f'<td class="n">{r["adp"]:.0f}</td>'
               f'<td class="n">{r["old_rank"]}</td><td class="n">{r["new_rank"]}</td>'
               f'<td class="n">{r["old_proj"]:.0f}</td><td class="n">{r["new_proj"]:.0f}</td>'
               f'<td class="n {dc}">{d:+.0f}</td></tr>')
    doc = f"""<meta charset="utf-8"><style>{CSS}</style>
<h1>OVERRIDE CARD &mdash; what the board says vs what ESPN now says</h1>
<p class="sub">JUG, slot 8 &middot; built {dt.datetime.now():%b %d %Y, %H:%M} &middot;
board = the shipped <b>board_v8_fixed.csv</b> &middot; pull = <b>{e(os.path.basename(pull))}</b></p>
<div class="warn"><b>Why this sheet exists.</b> The Sept board-order test returned <b>REBUILD</b>,
and <b>there is nothing to run</b>: doc 62 confirmed the shipped board has <b>no builder</b> &mdash;
no script produces it, and the one called "the board builder" is hardcoded to an August pull and
writes a file that was deleted as a trap. Doc 62's standing answer is <b>Option A: draft off the
verified board and handle the news as overrides at the pick.</b> This is that list.<br>
<b>How to use it:</b> the board is still the one list you draft from. If a name below comes up,
read the NEW rank, not the board's. <b>Amber rows are the exception</b> &mdash; a news override is
already on the board and the pull is trying to undo it. Ignore the pull on those.<br>
<b>VBD baseline:</b> &sect;4.1 replacement (QB 341.6 &middot; RB 168.6 &middot; WR 163.5 &middot;
TE 140.3), recomputed from the new projection so both ranks sit on one scale. The board's own ADP
is already current &mdash; only the projections below are stale.</div>
<table><tr><th>player</th><th>tm</th><th>pos</th><th class="r">adp</th>
<th class="r">board rank</th><th class="r">now</th>
<th class="r">board proj</th><th class="r">now</th><th class="r">move</th></tr>{tr}</table>
<p class="foot">mkoverride.py &middot; doc 62 &sect;5 Option A &middot; board_v8_fixed.csv + the newest pull</p>"""
    open(os.path.join(os.path.normpath(os.path.join(HERE,'..','Source')),'OVERRIDE_CARD.html'),
         'w', encoding='utf-8').write(doc)
    out = os.path.normpath(os.path.join(HERE, '..', 'Source'))
    exe = shutil.which('wkhtmltopdf')
    if not exe:
        print(f'\n  wkhtmltopdf not on PATH. Wrote {out}\\OVERRIDE_CARD.html '
              f'-- open it and print to PDF.')
        return
    subprocess.run([exe,'--enable-local-file-access','--quiet','-s','Letter',
                    os.path.join(out,'OVERRIDE_CARD.html'), os.path.join(out,'OVERRIDE_CARD.pdf')],
                   check=True)
    print(f'\n  wrote {out}\\OVERRIDE_CARD.pdf  ({len(rows)} rows)')

if __name__ == '__main__':
    main()
