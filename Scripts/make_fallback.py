#!/usr/bin/env python3
r"""
make_fallback.py -- rebuild FALLBACK_BOARD.pdf from the CURRENT board.

    py make_fallback.py

WHY (doc 97): the paper board was made by hand in a chat and had no builder, so when Josh Jacobs
went on the exempt list on Aug 30 the board could be corrected in seconds and the PAPER could not.
A paper board that disagrees with the live board is worse than no paper board -- it is only ever
read at the moment the live one has failed and cannot be checked. Directive §8 already says a
REBUILD invalidates three files; this makes the second of them a command instead of a memory.

Reads:  Scripts\live_draft\board_v8_fixed.csv  and  Scripts\news_overrides.csv
Writes: Source\FALLBACK_BOARD.pdf  (sync_desk_copies.py puts the dated copy at the root)
Needs:  wkhtmltopdf on PATH. If it is missing this writes the .html beside the PDF and says so.
"""
import datetime as dt, html, os, shutil, subprocess, sys
import pandas as pd

HERE  = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.join(HERE, 'live_draft', 'board_v8_fixed.csv')
OVR   = os.path.join(HERE, 'news_overrides.csv')
CTX   = os.path.join(HERE, 'live_draft', 'player_context.csv')
SRC   = os.path.normpath(os.path.join(HERE, '..', 'Source'))
OUT   = os.path.join(SRC, 'FALLBACK_BOARD.pdf')
N, PER_COL, COLS = 180, 30, 3   # 3 columns x 30 = 90 a page, 2 landscape pages

CSS = """
@page{size:Letter landscape;margin:9mm 8mm}
body{font:12.4px/1.32 "Segoe UI",Arial,sans-serif;color:#111;margin:0}
h1{font-size:19px;margin:0 0 4px;text-align:center;letter-spacing:.3px}
.note{font-size:10.6px;color:#333;margin:0 0 7px;text-align:justify}
.note b{color:#000}
.warn{background:#fde8e6;border-left:4px solid #c0392b;padding:6px 9px;margin:0 0 8px;font-size:11.4px}
.pg{page-break-after:always}
.pg:last-child{page-break-after:auto}
table{border-collapse:collapse;width:32%;float:left;font-size:12.4px}
table+table{margin-left:2%}
th{background:#eceff3;border-bottom:1px solid #99a;text-align:left;padding:3px 4px;font-size:11px}
td{padding:2.4px 4px;border-bottom:1px solid #e6e8ec}
tr:nth-child(even) td{background:#f7f8fa}
.r{text-align:right}.r{text-align:right}.c{text-align:center}
.g{width:16px;text-align:center;font-weight:700;font-size:10px}
.ga{color:#b3261e}.gd{color:#9a6212}.gn{color:#12734f}
.n{color:#666;width:24px;text-align:right}
.pos{font-weight:700;width:22px}
.QB{color:#6b3fa0}.RB{color:#12734f}.WR{color:#15628f}.TE{color:#9a6212}
.tier td{border-top:2px solid #c0392b}
.foot{clear:both;padding-top:6px;font-size:9.5px;color:#666;text-align:center}
"""

GRADE = {}
def load_ctx():
    if not os.path.exists(CTX): return
    try:
        c = pd.read_csv(CTX)
        for _, r in c.iterrows():
            g = str(r.get('grade','')).strip().upper()
            if g in ('AVOID','DISCOUNT','NEUTRAL'):
                GRADE[int(r['ESPN_ID'])] = g[0] if g!='NEUTRAL' else 'ok'
    except Exception as e:
        print(f"  (player_context.csv unreadable: {e} -- printing without grades)")

def rows_html(df):
    out=[]
    for _, r in df.iterrows():
        cls = r.pos if r.pos in ('QB','RB','WR','TE') else ''
        g = GRADE.get(int(r.espn_id), '') if 'espn_id' in df.columns else ''
        gcell = (f'<td class="g {"ga" if g=="A" else "gd" if g=="D" else "gn"}">{g}</td>'
                 if g else '<td class="g"></td>')
        out.append(
            f'<tr><td class="n">{int(r["rank"])}</td>'
            f'<td>{html.escape(str(r.player))}</td>'
            f'<td class="pos {cls}">{r.pos}</td>'
            f'<td class="c">{html.escape(str(r.team_c))}</td>'
            f'<td class="c">{int(r.bye)}</td>'
            f'<td class="r">{r.vbd:.1f}</td>'
            f'<td class="r">{r.eff_pick:.1f}</td>' + gcell + '</tr>')
    return ''.join(out)

def table(df):
    return ('<table><tr><th class="n">#</th><th>Player</th><th>Pos</th><th>Tm</th>'
            '<th class="c">Bye</th><th class="r">VBD</th><th class="r">Eff</th><th class="g">!</th></tr>'
            + rows_html(df) + '</table>')

def main():
    b = pd.read_csv(BOARD).sort_values('rank').head(N)
    load_ctx()
    banned = []
    if os.path.exists(OVR):
        o = pd.read_csv(OVR)
        banned = [(str(r.player), str(r.get('note',''))[:120]) for _, r in o.iterrows()]

    stamp = f"{dt.datetime.now():%b %d %Y, %H:%M}"
    warn = ''
    if banned:
        items = ''.join(f"<div><b>{html.escape(p)}</b> &mdash; {html.escape(n)}</div>"
                        for p, n in banned)
        warn = ('<div class="warn"><b>DO NOT DRAFT &mdash; removed from this board since the last '
                'printing:</b>' + items + '</div>')

    note = ("<b>Tool dead:</b> cross off names ESPN shows taken, take the highest VBD left that fits "
            "your caps (<b>QB2 / RB6 / WR6 / TE2</b> &mdash; tighter than the league&rsquo;s QB3/TE3, "
            "on purpose), and do not stack a bye. <b>D/ST never before pick 152, K never before 161.</b> "
            "<b>Eff</b> is the keeper-depleted pick a player is expected to go at &mdash; compare it to "
            "your picks 8, 17, 32, 41, 56, 65, 80, 89, 104, 113, 128, 137. "
            "<b>Known stale:</b> Tank Dell shows his pre-drop projection; treat him as a late dart, not "
            "by this rank. Regenerate with <b>py make_fallback.py</b> after any board change.")

    pages, step = [], PER_COL*COLS
    for start in range(0, N, step):
        cols = ''.join(table(b.iloc[start+c*PER_COL : start+(c+1)*PER_COL]) for c in range(COLS))
        head = (f'<h1>FALLBACK BOARD &mdash; top {N} by VBD</h1>'
                f'<div class="note">{note}</div>{warn}') if start == 0 else \
               (f'<h1>Fallback Board &mdash; ranks {start+1}&ndash;{min(start+step, N)}</h1>')
        pages.append(f'<div class="pg">{head}{cols}'
                     f'<div class="foot">generated {stamp} from board_v8_fixed.csv '
                     f'&middot; page {len(pages)+1} of {-(-N//step)}</div></div>')

    doc = (f'<!doctype html><html><head><meta charset="utf-8"><title>Fallback Board</title>'
           f'<style>{CSS}</style></head><body>{"".join(pages)}</body></html>')
    os.makedirs(SRC, exist_ok=True)
    hpath = os.path.join(SRC, 'FALLBACK_BOARD.html')
    open(hpath, 'w', encoding='utf-8').write(doc)

    exe = shutil.which('wkhtmltopdf')
    if not exe:
        print(f"  wkhtmltopdf not on PATH. Wrote {hpath} -- open it and print to PDF.")
        return
    # doc 146: `-O Landscape` is a wkhtmltopdf flag and Chrome ignores it, so the same
    # instruction is ALSO carried in the CSS above as `@page{size:Letter landscape}`.
    # Without that line to_pdf.py's Chrome fallback prints this wide table portrait.
    # wkhtmltopdf honours both, so the belt and the braces do not fight.
    r = subprocess.run([exe, '--enable-local-file-access', '--quiet', '-O', 'Landscape',
                        '-s', 'Letter', hpath, OUT], capture_output=True, text=True)
    if r.returncode or not os.path.exists(OUT) or os.path.getsize(OUT) < 4000:
        sys.exit(f"  PDF build FAILED (rc={r.returncode}). {r.stderr[:300]}\n"
                 f"  The old {os.path.basename(OUT)} has NOT been replaced.")
    # doc 146: this used to delete the .html once the PDF existed. It is now the FRESHNESS
    # REFERENCE -- to_pdf.py and sync_desk_copies.py both compare the PDF's timestamp against
    # it, which is how "the page rebuilt and the PDF did not" gets caught. Deleting it turns
    # that check into a silent skip. Keep it.
    print(f"  wrote {OUT}  ({os.path.getsize(OUT):,} bytes, {len(b)} players"
          + (f", {len(banned)} DO-NOT-DRAFT warning(s)" if banned else "") + ")")
    print("  Now run  py sync_desk_copies.py  to put the dated copy at the root.")

if __name__ == '__main__':
    main()
