import pandas as pd, numpy as np, html, re, datetime as dt, subprocess, shutil, os, warnings
warnings.filterwarnings('ignore')
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.normpath(os.path.join(HERE,'..','Source'))
# doc 144: bare filenames again -- values.csv sits beside this script and the sheet belongs in
# Source\ with the other artifacts, not in whatever folder the shell happened to be in.
HTML=os.path.join(SRC,'VALUE_LADDER.html'); PDF=os.path.join(SRC,'VALUE_LADDER.pdf')
v=pd.read_csv(os.path.join(HERE,'values.csv'))
PICKS=[17,32,41,56,65,80,89,104,113,128,137]
EVW={'BOARD':'greyed on purpose &mdash; our projection likes him more than the market does, '
  'which is the signal this project RETIRED. See the note below',
 'ANALYSTS':"Boone and Harmon's RANKINGS both 25+ slots ahead of ADP",
 'BUY':'the analyst COMMENTARY sweep called him up &mdash; a different source from '
  'ANALYSTS, not the same thing said twice',
 'JOB':'unsettled or contested job worth having',
 'INJURY-OPENED':'a teammate at his position is OUT / PUP / exempt'}
CSS="""@page{margin:9mm 8mm}
body{font:11.5px/1.32 "Segoe UI",Arial,sans-serif;color:#111;margin:0}
h1{font-size:17px;margin:0 0 2px}.sub{font-size:10.2px;color:#555;margin:0 0 8px}
.warn{background:#fdeceb;border-left:4px solid #c0392b;padding:6px 9px;margin:0 0 9px;font-size:10.4px}
.key{background:#eef1f5;border:1px solid #ccd2da;padding:6px 8px;margin:0 0 10px;font-size:10px}
h2{font-size:12.5px;margin:13px 0 4px;padding:4px 7px;background:#e9edf2;border-left:4px solid #33415c;
 letter-spacing:.4px}
table{border-collapse:collapse;width:100%}
/* doc 143, item 1.  Each PICK section is its own <table>, and with no declared widths every
   table auto-sizes its columns to ITS OWN content -- so the same column can land in a
   different place on Pick 17 than on Pick 32.  A clean render happened to line up, which is
   luck, not a guarantee: it depends on the longest name in each block and on which
   wkhtmltopdf build is doing the layout.  Declaring percentages removes the whole class of
   problem.  MEASURED: percentages alone did NOT fix it -- the header still landed at seven
   different offsets across the eleven tables, because `white-space:nowrap` on the player cell
   forces that column wider than its declared share and pushes everything right.  So: fixed
   layout, which makes the declared widths authoritative, AND let the player name wrap. */
table.vl th:nth-child(1),table.vl td:nth-child(1){width:15%}
table.vl th:nth-child(2),table.vl td:nth-child(2){width:3%}
table.vl th:nth-child(3),table.vl td:nth-child(3){width:3.5%}
table.vl th:nth-child(4),table.vl td:nth-child(4){width:4%}
table.vl th:nth-child(5),table.vl td:nth-child(5){width:4%}
table.vl th:nth-child(6),table.vl td:nth-child(6){width:4%}
table.vl th:nth-child(7),table.vl td:nth-child(7){width:7.5%}
table.vl th:nth-child(8),table.vl td:nth-child(8){width:5%}
table.vl th:nth-child(9),table.vl td:nth-child(9){width:19%}
table.vl th:nth-child(10),table.vl td:nth-child(10){width:9%}
table.vl th:nth-child(11),table.vl td:nth-child(11){width:26%}
table.vl{table-layout:fixed}
table.vl td{overflow-wrap:anywhere}
td{padding:4px 5px;vertical-align:top;border-bottom:1px solid #eef0f3;font-size:11px}
th{padding:1px 5px;text-align:left;font-size:8.2px;font-weight:700;letter-spacing:.5px;
 text-transform:uppercase;color:#8b93a0;border-bottom:1px solid #ccd2da}
th.r{text-align:right}
.pl{font-weight:600}.n{text-align:right;color:#444;width:30px}
.tm{font-size:9.4px;color:#667;font-family:Consolas,monospace;width:26px}
.v{text-align:right;font-weight:700;color:#1d2733}
.ag{text-align:center;font:700 12px/1 Consolas,monospace;color:#33415c}
.QB{color:#6b3fa0}.RB{color:#12734f}.WR{color:#15628f}.TE{color:#9a6212}
.pos{font-weight:700;width:20px}
.e{font-size:8.6px;font-weight:700;letter-spacing:.3px;line-height:1.5}
.e span{display:inline-block;padding:0 4px;border-radius:2px;margin:0 2px 2px 0;color:#fff}
.EB{background:#eef1f5;color:#6b7480 !important;border:1px solid #ccd2da}.EA{background:#15628f}.EY{background:#12734f}.EJ{background:#9a6212}.EI{background:#c0392b}
.c{font-size:8.8px;color:#8a4b12;font-weight:700}
.why{font-size:9.4px;color:#555}
tr.nw td{font-size:9px;color:#8a4b12;padding:0 4px 4px 0;border-top:none;line-height:1.35}
tr.nw td:first-child:before{content:"NEWS";font-weight:700;letter-spacing:.4px;color:#c0392b}
.pb{page-break-after:always}
/* doc 169: the page-break ESTIMATE was wrong from page 1 and stayed wrong.
   `used` counted only table rows, never the h1 + sub + warn + key header block that
   eats most of page 1 -- so the forced break after PICK 65 fired with HALF of page 2
   still empty. Nothing guesses now: each PICK block simply refuses to be split, and
   the renderer paginates. There is no number left to go stale. */
.blk{break-inside:avoid;page-break-inside:avoid}
.foot{font-size:9px;color:#777;text-align:center;padding-top:8px}"""
CLS={'BOARD':'EB','ANALYSTS':'EA','BUY':'EY','JOB':'EJ','INJURY-OPENED':'EI'}
def esc(x): return html.escape(str(x))
def fmt_caution(c):
 """doc 141: `10g` next to an orange DISC reads like a nutrition label. Matt said so, and
 he is right -- the eye takes it as a quantity of something bad rather than as the number
 of games he PLAYED. Spell it. And the legend used to say 'darker is worse', which is true
 of the DRAFT_BOARD's shaded badge and false here: this sheet renders every caution in one
 colour, so it was describing a different artifact."""
 if not isinstance(c,str) or not c.strip(): return ''
 return re.sub(r'\b(\d+)g\b', r'played \1', c)
rows=[]
for i,p in enumerate(PICKS):
 CAP = 9
 # doc 145.  Order: the one FACT first, then how many independent things point here, then how
 # big the prize is if it lands, then the analyst gap. NOT by VBD or board rank -- ranking by
 # value is the draft board's job, and a second copy of it would be strictly worse.
 _all = v[v.take_at==p].sort_values(['fact','nev','jobw','gap'],ascending=False)
 g = _all.head(CAP)
 if len(_all) > CAP:
  print(f' !! pick {p}: {len(_all)} qualifiers, showing {CAP} -- '
   f'dropped {", ".join(_all.player[CAP:])}')
 if not len(g): continue
 rows.append('<div class="blk">')
 rows.append(f'<h2>PICK {p} &nbsp;&middot;&nbsp; effective ADP available here '
  f'~{int(g.eff_pick.median())}</h2><table class="vl">'
  '<tr><th>player</th><th>tm</th><th>pos</th><th class="r">vbd</th>'
  '<th class="r">brd&nbsp;#</th><th class="r">adp</th>'
  # doc 146: the &nbsp; here forced STILL THERE onto one line, which overflowed a 7.5%
  # column and ran into AGREE -- on the printout the two headers read as one word,
  # STILL THEREAGREE. Letting it wrap to two lines is the whole fix.
  '<th class="r">still there</th><th style="text-align:center">agree</th>'
  '<th>why he is on this sheet</th>'
  '<th>caution</th><th>detail</th></tr>')
 for _,r in g.iterrows():
  ev=''.join(f'<span class="{CLS[e]}">{e}</span>' for e in eval(r.ev) if e in CLS)
  why=[]
  if r.opened_by and str(r.opened_by)!='nan': why.append('path opened by <b>%s</b>'%esc(r.opened_by))
  if str(r.job) in ('UNSETTLED','contested') and pd.notna(r.job_ceil):
   why.append('%s job, worth %d pts to whoever wins it'%(r.job,r.job_ceil))
  if r.gap>=25: why.append('Boone %d / Harmon %d vs ADP %d'%(r.Boone,r.Harmon,r.adp_pick))
  rows.append('<tr><td class="pl">%s</td><td class="tm">%s</td>'
   '<td class="pos %s">%s</td><td class="v">%.0f</td><td class="n">%d</td>'
   '<td class="n">%d</td>'
   '<td class="n">%d%%</td><td class="ag">%d</td>'
   '<td class="e">%s</td><td class="c">%s</td>'
   '<td class="why">%s</td></tr>'%(
   esc(r.player),esc(r.team_c),r.pos,r.pos,r.vbd,r.board_rank,r.adp_pick,
   round(r.p_there*100),len([e for e in eval(r.ev) if e in CLS]),ev,
   esc(fmt_caution(r.caution)),
   ' &middot; '.join(why)))
  # doc 155.  The ladder had NO channel for a dated fact.  `values.py` reads player_context's
  # `why` only to regex out an injury BLOCK for `opened_by`; the rendered "why he is on this
  # sheet" column is built from opened_by + the job label + the analyst gap and nothing else.
  # So the Gemini sweep -- 15 of these 49 players carry a dated line, and three of them
  # CONTRADICT the reason the player is on the sheet (Dowdle demoted to backup, Dobbins
  # possibly to IR, Monangai week-to-week) -- was invisible here.  One extra row, under the
  # player, spanning the table: it cannot squeeze a column, and a player with no news costs
  # nothing because the row is not emitted at all.
  nw = str(r.get('news','') or '')
  if nw and nw != 'nan':
   rows.append('<tr class="nw"><td></td><td colspan="10">%s</td></tr>' % esc(nw))
 rows.append('</table></div>')
doc=f"""<meta charset="utf-8"><style>{CSS}</style>
<h1>VALUE LADDER &mdash; where the board, the analysts and the depth chart agree</h1>
<p class="sub">JUG, slot 8 &middot; built {dt.datetime.now():%b %d %Y, %H:%M} &middot; research sheet, NOT a draft-night artifact &mdash;
the board is still the one list you draft from.</p>
<div class="warn"><b>Read this as an agreement count, not a model.</b> Every signal here except
<b>BOARD</b> is unpriced and unmeasured in this project. Three separate tests looked for a link between
&quot;the analysts like him more than the market does&quot; and &quot;he actually beat his
projection.&quot; <b>A perfect link scores 1.0 and no link scores 0. All three came back between
&minus;0.08 and &minus;0.24</b> &mdash; no link at all, and the sign is <i>backwards</i>: the players
who looked like the biggest bargains did slightly <b>worse</b>. For scale, the signals this project
does trust score <b>+0.40 to +0.59</b>. What these rows give you is <b>where several independent
sources happen to point the same way</b> &mdash; a shortlist to research, not a ranking to obey.
<b>still there</b> is the chance he lasts to that pick, from ADP dispersion alone
(&sect;4.12's noise, no opponent model). &sect;4.15 measured that this family of number runs
<b>optimistic</b> &mdash; on Josh Allen it read 74% where the calibrated answer was 3%, because it
cannot know that Snyder takes Allen at his turn. <b>Treat every one of these as a ceiling.</b>
The live board's <b>still there?</b> column is the same idea computed a different way (a 400-run
simulation on the players actually left) and carries the same optimism &mdash; do not read one as a
check on the other.</div>
<div class="key"><b>BOARD</b> {EVW['BOARD']} &nbsp;&middot;&nbsp; <b>ANALYSTS</b> {EVW['ANALYSTS']}
&nbsp;&middot;&nbsp; <b>BUY</b> {EVW['BUY']} &nbsp;&middot;&nbsp; <b>JOB</b> {EVW['JOB']}
&nbsp;&middot;&nbsp; <b>INJURY-OPENED</b> {EVW['INJURY-OPENED']}<br>
Cautions in orange, all from the injury sweep: <b>AVOID</b> = do not draft him at this price ·
<b>DISC</b> = discount &mdash; he is worth taking later than this rank, not here ·
<b>played N</b> = he played N games in 2025, and <b>the number is the warning, not the badge</b>
(&sect;4.22e: an 11-game season cost &minus;17 points against his projection, a 4-game season
&minus;41) · <b>bear</b> = the analyst commentary leans against him.<br>
<b>THE BADGES ARE NOT EQUAL, SO READ THEM IN THIS ORDER.</b>
<b>INJURY-OPENED is the only FACT</b> &mdash; a teammate at his position is actually out, so the path
already changed. <b>JOB is a SIZE</b> &mdash; the job is open and worth this many points to whoever
wins it; measured on 19 unsettled backfields it does <i>not</i> tell you who wins.
<b>ANALYSTS and BUY are OPINION</b>, from two different sources. <b>BOARD is greyed out and is NOT
counted in AGREE:</b> it fires when our projection likes him more than the market does &mdash; the
&quot;market is sleeping on him&quot; idea this project <b>retired</b>, then measured again at
<b>&minus;0.17</b> (n=409) pointing the <i>wrong</i> way. It also fires on <b>40 of these 49 rows</b>,
so it separates almost nothing. It is shown because the disagreement is worth seeing, <b>not</b>
because it is a reason to draft him.<br>
<b>So: rows are ordered by the FACT first, then AGREE</b> (the four non-BOARD badges), then by how
big the open job is, then by the analyst gap. Everything inside one PICK block is reachable at the
same pick, so this is a <b>reading order, not a ranking</b> &mdash; and deliberately not by VBD or
board rank, because that is the draft board's job and a second copy of it would be worse. Ranking by value is
the draft board's job; this sheet answers a different question, which is where several independent
things happen to point at the same name.<br>
<b>vbd</b> is points above a replacement starter &mdash; the same number the draft board sorts
on, so a row here lines up against that page. <b>brd #</b> is his rank on it, and the
<b>BOARD</b> badge is exactly &quot;brd # is 12+ better than adp&quot;, so you can check it in place.<br>
<b>UNSETTLED / contested tells you the job is open, NOT who wins it.</b> Measured on 19 such
backfields (2022 + 2024): the incumbent and the challenger beat their price by the same amount
on average, and individual pairs swing &plusmn;110 points either way &mdash; Brooks lost his job to
Dowdle, and Pollard kept his over Spears, by the same margin. <b>Buy the job, never the name.</b><br>
<b>still there</b> is a ceiling, never a check on the live board's column of the same name &mdash;
they answer different questions (here: is he there when you ARRIVE; there: is he there at your NEXT
turn if you pass).</div>
{''.join(rows)}
<p class="foot">values.py &rarr; values.csv &rarr; mkvalue.py &middot; board_v8_fixed +
player_context + Boone/Harmon 09-01 + games_2025 &middot; team joined on the board spine</p>"""
open(HTML,'w',encoding='utf-8').write(doc)
exe=shutil.which('wkhtmltopdf')
if exe is None:
 print(f'  wkhtmltopdf not on PATH. Wrote {HTML} -- open it and print to PDF.')
else:
 subprocess.run([exe,'--enable-local-file-access','--quiet','-s','Letter',HTML,PDF],check=True)
 _shown = sum(min(len(v[v.take_at==p]), 9) for p in PICKS)
 print('wrote VALUE_LADDER.pdf (%d bytes), %d of %d qualifiers shown'
  % (os.path.getsize(PDF), _shown, int(v.take_at.isin(PICKS).sum())))
