#!/usr/bin/env python3
r"""
make_howto.py -- HOW_TO_READ_IT, generated FROM the live board, never typed alongside it.

    py make_howto.py            writes Source\HOW_TO_READ_IT.html (+ .pdf if a renderer exists)

WHY THIS EXISTS.  There were three paper explanations of the live board -- HOW_TO_READ_IT.pdf,
DRAFT_DAY_GUIDE.pdf and DRAFT_CARD.pdf -- and all three were hand-written beside the code.  Docs
79 and 82 record what that costs: the guide and the card both described the board's columns
WRONG for days after the UI rewrite, because nothing tied them to the thing they described.
The column text below is not retyped.  It is `live_draft.COLGLOSS`, imported.  If the board's
legend changes, this page changes with it, and it cannot say something the board does not.

THE BADGES cannot be imported -- they are literal strings inside `badges()` -- so they are listed
here AND CHECKED: every label in the table must appear in live_draft.py's source, and the script
REFUSES to write if one does not.  A guard that has never fired is not a guard (SS0.2), so it is
run against the real file every time.
"""
import os, re, sys, html, datetime as dt, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.normpath(os.path.join(HERE, '..', 'Source'))
KIT  = os.path.join(HERE, 'live_draft')
sys.path.insert(0, KIT)
import live_draft as LD

SOURCE = open(os.path.join(KIT, 'live_draft.py'), encoding='utf-8').read()

# ---------------------------------------------------------------------------------------
# THE COLOURS ARE READ OUT OF THE BOARD, NOT RETYPED.  Matt: "add color matching to the
# columns and definitions where it makes sense."  The only honest way to print a key for a
# coloured mark is to print the mark, so every swatch below is rendered with the SAME
# background, border and text colour live_draft.py gives it -- parsed from its stylesheet at
# generation time and resolved through its :root variables.  Change the board's palette and
# this page follows; retyping a hex here is how a key starts lying (docs 157, 158).
# The board is dark and this page is white, so each chip sits on the board's own panel colour
# rather than being tinted onto paper -- what you see here is what is on the screen.
# ---------------------------------------------------------------------------------------
CSS_SRC = re.search(r'CSS\s*=\s*"""(.*?)"""', SOURCE, re.S).group(1)
VARS = dict(re.findall(r'--([\w-]+)\s*:\s*([^;}]+)', re.search(r':root\{([^}]*)\}', CSS_SRC).group(1)))

def _v(x):
    """resolve var(--name) against the board's own :root block."""
    return re.sub(r'var\(--([\w-]+)\)', lambda m: VARS.get(m.group(1), '#000').strip(), x).strip()

def rule(sel):
    """Every declaration the board applies to this selector, merged in source order the way a
    browser would.  ONE match is not enough: the eleven badge classes share a font block --
    `.ctxA,.ctxD,...,.ctxM{font:...}` -- and a first-match lookup finds THAT for `.ctxM` and
    never reaches its own `.ctxM{background:#6b4a08;...}` further down.  MINE came out as a
    plain grey chip and nothing said so.  Caught by checking the rendered page for each
    expected hex, not by reading the output."""
    out = {}
    for m in re.finditer(r'([^{}\n]*?)\{([^}]*)\}', CSS_SRC):
        sels = [x.strip() for x in m.group(1).split(',')]
        if sel not in sels: continue
        for d in m.group(2).split(';'):
            if ':' in d:
                k, v = d.split(':', 1); out[k.strip()] = _v(v)
    return out

PANEL = _v(VARS.get('pnl', '#171a21'))

def chip(sel, text, extra=''):
    """one mark, rendered the way the board renders it."""
    d = rule(sel)
    bg  = d.get('background', PANEL)
    fg  = d.get('color', _v(VARS.get('tx', '#e8eaee')))
    bd  = d.get('border', '1px solid transparent')
    return (f'<span style="display:inline-block;background:{bg};color:{fg};border:{bd};'
            f'border-radius:3px;padding:2px 5px;font:700 9.5px/1.35 system-ui;{extra}">'
            f'{text}</span>')

def onpanel(inner, pad='3px 6px'):
    return (f'<span style="display:inline-block;background:{PANEL};border-radius:4px;'
            f'padding:{pad};white-space:nowrap">{inner}</span>')

def pos_chips():
    return ' '.join(chip('.' + p, p, 'width:26px;text-align:center;padding:2px 0')
                    for p in ('QB', 'RB', 'WR', 'TE'))


def token(cls, text):
    """a `cost vs #1` value, in the colour the board gives it."""
    col = _v(rule('.' + cls).get('color', '#fff'))
    return f'<span style="color:{col};font:700 11px/1 monospace">{text}</span>'

# label -> (where it sits, what it means).  Checked against the source below.
BADGES = [
 ('AVOID',  'ctxA', 'left of the name',  'The injury sheet grades him AVOID. Do not draft him at this price.'),
 ('OUT', 'ctxA',    'left of the name',  'ESPN has him OUT.'),
 ('IR', 'ctxA',     'left of the name',  'ESPN has him on injured reserve.'),
 ('DISC', 'ctxD',   'left of the name',  'DISCOUNT &mdash; worth taking later than this rank, not here.'),
 ('BYE', 'ctxB',    'left of the name',  'His bye week collides with someone already on your roster. '
                                 '<b>Worth at most 1.2 points, ever</b> (&sect;4.11) &mdash; never move a pick with real margin behind it.'),
 ('FADE', 'ctxF',   'left of the name',  'Analysts called him DOWN and nobody called him up.'),
 ('MINE', 'ctxM',   'either side',       'Your own take. It outranks every list on the page &mdash; red if you faded him, amber if you like him.'),
 ('BUY', 'ctxY2',    'right of the name', 'Both analyst panels are ahead of his ADP. Brighter = more independent kinds of evidence agreeing (max 2 kinds: ANALYSTS and ROLE).'),
 ('CALLS', 'ctxY1',  'right of the name', 'No panel signal, but named analysts targeted him on a podcast.'),
 ('OPEN', 'ctxS',   'right of the name', 'He is the direct backup into an UNSETTLED backfield. Only from pick 104.'),
 ('DART', 'ctxS',   'right of the name', 'Direct backup, but the job in front of him is settled &mdash; only pays on an injury. Only from pick 104.'),
 ('ok', 'ctxN',     'right of the name', 'The injury sheet actively cleared him. Stop flinching.'),
 ('R', 'i.rk', 'after the name',    'Rookie &mdash; no 2025 NFL snaps and not in the 2023 or 2024 player pool. '
                                 'Grey and plain on purpose: a <b>fact, not a rating</b>. Nothing here computes a ceiling.'),
 ('goes first', 'i.gof', 'in still there?','This row is a TIE with the recommendation AND at least 20 points less likely to survive. '
                                 'It is the one you can <b>only</b> get on this turn.'),
]

STRIP = [
 ('__STRIP__',
  'Your NINE starting slots, not your roster size. Green = filled, amber = one short, red = empty.'),
 ('+n', 'Bench depth at that position, beyond the slots that start. The left-hand number never '
        'goes above the right-hand one, because the right-hand one is <b>how many of that position '
        'start</b> &mdash; "3 of 2" would mean nothing.'),
 ('full', 'You are at this roster’s cap for that position; the board will stop offering it.'),
 ('N skill turns left', 'How many of your twelve skill picks remain, this one included.'),
 ('&hellip; next turn the board can only offer QB and TE',
  'A warning, one turn early. The engine force-drafts your missing starters when turns run out.'),
 ('FORCED &mdash; only QB and TE from here',
  'It is happening now. Every row on the board is one of those positions until the slot is filled.'),
]

CSS = """body{font:13px/1.5 -apple-system,Segoe UI,system-ui,sans-serif;color:#1b1f26;margin:0;padding:22px 26px;max-width:1050px}
h1{font-size:20px;margin:0 0 2px}h2{font-size:13px;letter-spacing:.09em;text-transform:uppercase;color:#5a6270;
   margin:20px 0 7px;border-bottom:1px solid #d8dce3;padding-bottom:4px}
.sub{color:#6b7480;font-size:11.5px;margin:0 0 6px}
table{border-collapse:collapse;width:100%;margin-bottom:4px}
td,th{border-bottom:1px solid #e6e9ee;padding:5px 8px 5px 0;vertical-align:top;text-align:left;font-size:12px}
th{font:700 10px/1 sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#8a929d;padding-bottom:6px}
td.k{font-weight:700;white-space:nowrap;width:150px}td.w{color:#6b7480;white-space:nowrap;width:130px;font-size:11px}
.rule{background:#fff8e6;border:1px solid #e8d9a8;border-radius:6px;padding:10px 13px;margin:14px 0;font-size:12.5px}
.rule b{color:#8a5a00}
.foot{color:#8a929d;font-size:10.5px;text-align:center;margin-top:18px}
@page{size:Letter portrait;margin:12mm}"""


# What each label must literally look like inside live_draft.py.  A bare `'R' in SOURCE` test
# matches every capital R in the file, and a quoted-literal test misses the two labels that are
# emitted as HTML rather than as Python strings -- which is exactly what the guard caught on its
# first run.  So each label carries the exact substring that proves the board still renders it.
PROBE = {'R': 'class="rk"', 'goes first': '>goes first</i>'}


def check_badges():
    missing = []
    for lbl, _c, _w, _m in BADGES:
        probe = PROBE.get(lbl)
        found = (probe in SOURCE) if probe else (f"'{lbl}'" in SOURCE or f'"{lbl}"' in SOURCE)
        if not found: missing.append(lbl)
    if missing:
        sys.exit('  REFUSING TO WRITE: these labels are in this page but NOT in live_draft.py: '
                 + ', '.join(missing) + '\n  Either the board changed or this table is wrong. Fix, then re-run.')
    print(f'  guard: all {len(BADGES)} badge labels found in live_draft.py')


def main():
    check_badges()
    # COLGLOSS also carries the strip and the rookie mark; both get their own fuller section on
    # this page, so they are dropped HERE rather than printed twice. Everything else is verbatim.
    SKIP = ('the strip under the hero', 'R (beside a name)', 'the marks beside a name')
    cols = ''.join(f'<tr><td class="k">{k}</td><td>{v}</td></tr>'
                   for k, v in LD.COLGLOSS if k not in SKIP)
    assert sum(1 for k, _ in LD.COLGLOSS if k in SKIP) == len(SKIP), \
        'COLGLOSS renamed an entry this page drops by name -- check SKIP'
    bad  = ''.join(f'<tr><td class="k">{onpanel(chip("." + c if not c.startswith("i.") else c, l))}</td>'
                   f'<td class="w">{w}</td><td>{m}</td></tr>' for l, c, w, m in BADGES)
    # the strip, in its own three colours, straight off the board's .ok / .warn / .bad
    live_strip = onpanel(
        token('ok','QB 1/1') + ' &nbsp; ' + token('ok','RB 2/2 +1') + ' &nbsp; '
        + token('warn','WR 1/2') + ' &nbsp; ' + token('bad','TE 0/1') + ' &nbsp; '
        + token('ok','FLEX 1/1'), pad='5px 9px')
    strip= ''.join(f'<tr><td class="k">{live_strip if k == "__STRIP__" else k}</td>'
                   f'<td>{v}</td></tr>' for k, v in STRIP)
    # what `cost vs #1` looks like at each distance, and the two other coloured things on the row
    swatch = ('<table><tr><th>on screen</th><th>what it is</th></tr>'
      f'<tr><td class="k">{onpanel(token("free","free"), pad="5px 9px")}</td>'
      '<td>Row 1 &mdash; the recommendation. It costs nothing because it <i>is</i> the pick.</td></tr>'
      f'<tr><td class="k">{onpanel(token("tie","-0.9") + " " + token("tie","tie"), pad="5px 9px")}</td>'
      '<td>Within 1.5 points. The engine cannot separate this row from row 1 &mdash; take whichever you prefer.</td></tr>'
      f'<tr><td class="k">{onpanel(token("cheap","-4.2"), pad="5px 9px")}</td>'
      '<td>Under 6 points behind. Cheap, if you have a reason.</td></tr>'
      f'<tr><td class="k">{onpanel(token("dear","-13.7"), pad="5px 9px")}</td>'
      '<td>More than 6 behind, and the bar beside it is long. Not cheap.</td></tr>'
      f'<tr><td class="k">{onpanel(chip(".runflag","RUN: 4 RB of the last 6"), pad="5px 9px")}</td>'
      '<td>Four or more of the last six picks went to one position. Three of six is just a draft, so it does not fire.</td></tr>'
      f'<tr><td class="k">{onpanel(pos_chips(), pad="5px 9px")}</td>'
      '<td>The position chip, same four colours everywhere on the page.</td></tr>'
      '</table>')
    doc = f"""<meta charset="utf-8"><style>{CSS}</style>
<h1>How to read the live board</h1>
<p class="sub">JUG, slot 8 &middot; generated {dt.datetime.now():%b %d %Y, %H:%M} from the board's own legend &mdash;
if this disagrees with the screen, the screen is right and this file is stale.</p>

<div class="rule"><b>THE ONE RULE.</b> At picks <b>8, 17, 32, 41 and 56</b> the board beats its own
runner-up by 13.6 / 5.0 / 13.4 / 7.8 / 2.3 points &mdash; <b>take row 1.</b> From pick 65 the margin
falls to 2.5 and then to 0.06: the board cannot separate its top rows, so <b>you</b> decide, on the
badges, the news on the card, and the Value Ladder. <b>Pick 32 is a coin flip even at row 1</b> &mdash;
more computing does not find a winner there, it just becomes consistent about there not being one.</div>

<h2>The strip under the headline</h2><table>{strip}</table>

<h2>The columns that need explaining</h2><table><tr><th>column</th><th>what it is</th></tr>{cols}</table>

<h2>The colours in that column</h2>{swatch}

<h2>The marks beside a name</h2>
<p class="sub">At most <b>two</b> judgement marks per row &mdash; one caution on the left, one edge on the
right. That cap is deliberate. Click any row to open the full card: injury history, the bull and bear
cases, the backfield, and any dated news.</p>
<table><tr><th>mark</th><th>where</th><th>what it means</th></tr>{bad}</table>

<h2>Draft night, in order</h2>
<table>
<tr><td class="k">6:55 PM</td><td><b>draft_night.bat</b> &mdash; verifies the file tree, fetches the actual keepers, rebuilds the board, re-injects the prerank.</td></tr>
<tr><td class="k">7:50 PM</td><td><b>py bridge_server.py</b> FIRST, then open the draft room in Chrome with the espn_bridge extension loaded.</td></tr>
<tr><td class="k">7:55 PM</td><td><b>py live_draft.py --bridge</b> &mdash; check the first poll line reports the keeper-row count.</td></tr>
<tr><td class="k">8:00 PM</td><td>Draft. The board refreshes itself; you never reload it.</td></tr>
<tr><td class="k">if it looks wrong</td><td>The board is <b>always 12 player rows and 3 dashed tier lines</b>. Any other count means something is broken &mdash; say so, do not explain it away.</td></tr>
</table>
<p class="foot">make_howto.py &middot; columns imported from live_draft.COLGLOSS &middot; badge labels verified against live_draft.py</p>"""
    os.makedirs(SRC, exist_ok=True)
    out = os.path.join(SRC, 'HOW_TO_READ_IT.html')
    open(out, 'w', encoding='utf-8').write(doc)
    print(f'  wrote {out}')
    for exe in ('wkhtmltopdf', 'chrome', 'google-chrome', 'chromium', 'msedge'):
        p = shutil.which(exe)
        if not p: continue
        pdf = os.path.join(SRC, 'HOW_TO_READ_IT.pdf')
        cmd = ([p, '--enable-local-file-access', out, pdf] if 'wkhtml' in exe else
               [p, '--headless', '--disable-gpu', '--no-pdf-header-footer',
                f'--print-to-pdf={pdf}', '--virtual-time-budget=3000', 'file://' + out])
        if os.name != 'nt' and 'wkhtml' not in exe: cmd.insert(1, '--no-sandbox')
        subprocess.run(cmd, capture_output=True)
        if os.path.exists(pdf): print(f'  wrote {pdf} ({os.path.getsize(pdf):,} bytes) via {exe}'); return 0
    print('  (no PDF renderer found here -- run py to_pdf.py)')
    return 0

if __name__ == '__main__':
    sys.exit(main())
