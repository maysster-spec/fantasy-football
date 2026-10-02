"""make_online.py -- turn WEEK_SHEET.html into the copy that gets published to the web.

[doc 430] WHY THIS EXISTS. The published page sat six days stale while every local page was current,
because publishing was a HAND edit somebody did once in a chat and nobody could repeat. ff.bat
cannot publish: it writes files to this PC, and nothing on this PC can push to claude.ai. So the
split is fixed and this script owns the half that can be automated -- producing a publish-ready
file every time the sheet is built, so the only manual step left is the upload itself.

Run by ff.bat. Writes Source\\ONLINE_WEEK_SHEET.html. No network, no ESPN.

THE TRANSFORM, and each line of it is a thing the web copy must do differently:
  1. the page bar lists the ONLINE pages, because MY_TODO.html and the rest are on this PC only
  2. a stamp says when the pull ran and that the page does not refresh itself
  3. local-only links become plain text, so nothing on the web points at a file:// path
  4. the outer document is stripped and the title is pinned, because the artifact platform wraps
     the page in its own skeleton and the artifact's NAME must not change every build

WHAT IT DOES NOT BUILD, AND SAYS SO EVERY RUN. ONLINE_POCKET_SHEET.html is a hand-built snapshot
of the week sheet that only a Claude session edits; no script produces it, so this one cannot
rebuild it and does not pretend to. The decision (claude_todo, 29 Sept) is to accept the snapshot
practice: the page carries a dated note at the top of its body saying it is a snapshot and that the
week sheet is the live page, check_pages.py warns when that date is more than 7 days old, and this
script prints the date and the age each run rather than skipping the file in silence.
"""
import os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'Source')

ONLINE = [
    ('',                                                   'week sheet'),
    ('https://claude.ai/artifact/1iFS2iFyDACxRknmbJiFNT',  'pocket sheet'),
    ('https://claude.ai/artifact/BwUBENtMAZzTdjfgq7kqCJ',  'the takes'),
    ('https://claude.ai/artifact/NpLWo1xBiWRG4bztW7L5xw',  'roster clock'),
]
ART_TITLE = 'Where the Season Breaks'   # the artifact's name. Stable across every republish.

LOCAL_ONLY = {'MY_TODO.html': 'to-do list', 'THE_WEEKLY_WIRE.html': 'the wire',
              'LINEUP_CHECK.html': 'lineup check', '../COMMANDS.html': 'commands'}

BAR_CSS = ('<style>span.todolink.off{display:inline-block;margin:0 14px 0 0;font-family:var(--disp);'
           'text-transform:uppercase;letter-spacing:.07em;font-size:11.5px;color:var(--muted);'
           'border-bottom:none;padding-bottom:1px}</style>')


def online_bar():
    out = ['<p class="jump pagebar"><span class="pbl">online</span>']
    for href, label in ONLINE:
        if not href:
            out.append(f'<span class="todolink here">{label}</span>')
        else:
            out.append(f'<a class="todolink" href="{href}">{label}</a>')
    out.append('</p>')
    return ''.join(out)


def stamp(built):
    return ('<p class="stamp-online" style="margin:12px 0 0;font-family:var(--mono);font-size:11.5px;'
            'color:var(--muted);background:var(--sunk);border-left:3px solid var(--hole);'
            f'padding:8px 11px">PUBLISHED COPY. Built from the pull that ran <b>{built}</b>. '
            'It does not update itself and it is only as fresh as the last time somebody '
            'republished it. The to-do page, the wire and the lineup check live on your PC and '
            'are not on the web: a browser will not follow a link from here to a file on your '
            'drive, so open them from <b>G:\\My Drive\\_Fantasy\\2026\\Source\\</b>, '
            'where the week sheet links back to every page on both sides.</p>')


def convert(html):
    notes = []
    m = re.search(r'<p class="jump pagebar".*?</p>', html, re.S)
    if not m:
        raise SystemExit('FAILED: no page bar in the sheet, so the online bar has nothing to replace.')
    k = re.search(r'<p class="kick">[^<]*?built ([^<(]+)', html)
    if not k:
        # [doc 435] a page with no build time is not publishable: the published copy's whole
        # point is that it says WHEN it was built. Before this, the guard below only tested a
        # string this script inserts itself, so it could never fail on input (measured: the
        # kick line stripped, exit 0, stamp "an unknown time").
        raise SystemExit('FAILED: no build time in the kick line, so the online stamp would lie.')
    built = k.group(1).strip()
    html = html.replace(m.group(0), online_bar() + stamp(built), 1)
    notes.append(f'page bar replaced; build stamp read as "{built}"')

    # every remaining link to a local page becomes plain text
    n = 0
    for href, label in LOCAL_ONLY.items():
        pat = re.compile(r'<a class="todolink" href="' + re.escape(href) + r'"[^>]*>(.*?)</a>', re.S)
        html, c = pat.subn(
            lambda mm: f'<span class="todolink off" title="on your PC only">{mm.group(1)}'
                       ' (on your PC)</span>', html)
        n += c
    notes.append(f'{n} local-only links turned to plain text')

    # the platform supplies its own doctype/head/body, so ship the CONTENT only, and pin the name
    html = re.sub(r'^\s*<!doctype[^>]*>\s*<html[^>]*>\s*<head>', '', html, count=1, flags=re.I)
    html = re.sub(r'<meta[^>]*>', '', html, count=2)
    html = re.sub(r'<title>.*?</title>', f'<title>{ART_TITLE}</title>', html, count=1, flags=re.S)
    html = re.sub(r'</head>\s*<body[^>]*>', '<div id="top"></div>', html, count=1, flags=re.I)
    html = re.sub(r'</body>\s*</html>\s*$', '', html, count=1, flags=re.I)
    html = BAR_CSS + html
    notes.append(f'outer document stripped, title pinned to "{ART_TITLE}"')
    return html, notes


def main():
    src = os.path.join(SRC, 'WEEK_SHEET.html')
    if not os.path.exists(src):
        raise SystemExit('FAILED: no WEEK_SHEET.html. Run the wire first.')
    html = open(src, encoding='utf-8').read()
    out, notes = convert(html)
    # THE GUARD: the thing this script is named after must actually be true of the output.
    # An exit code is not a result (0.2).
    bad = [h for h in LOCAL_ONLY if f'href="{h}"' in out]
    if bad:
        raise SystemExit('FAILED: local links survived the transform: ' + ', '.join(bad))
    if 'stamp-online' not in out:
        raise SystemExit('FAILED: the published-copy stamp is not in the output.')
    if 'NpLWo1xBiWRG4bztW7L5xw' not in out:
        raise SystemExit('FAILED: the roster clock is not linked in the output.')
    if re.search(r'<!doctype|</body>|</html>', out, re.I):
        raise SystemExit('FAILED: the outer document survived; the platform adds its own.')
    if f'<title>{ART_TITLE}</title>' not in out:
        raise SystemExit('FAILED: the artifact title is not pinned.')
    dst = os.path.join(SRC, 'ONLINE_WEEK_SHEET.html')
    open(dst, 'w', encoding='utf-8').write(out)
    print(f'  written: {dst}  ({len(out):,} bytes)')
    for n in notes:
        print('    ' + n)
    print('    NOT PUBLISHED. Ask Claude to publish this file; nothing on this PC can upload it.')
    print('  ' + pocket_status())


POCKET = 'ONLINE_POCKET_SHEET.html'
POCKET_NOTE = re.compile(r'class="snapshot"[^>]*data-snapshot="(\d{4}-\d{2}-\d{2})"')
POCKET_MAX_DAYS = 7


def pocket_status(today=None):
    """One printed line about the pocket sheet, which this script does not build. Never raises."""
    today = today or datetime.date.today()
    p = os.path.join(SRC, POCKET)
    if not os.path.exists(p):
        return f'{POCKET} NOT rebuilt: not on the drive. It is a hand-built snapshot; ask Claude for one.'
    try:
        m = POCKET_NOTE.search(open(p, encoding='utf-8', errors='replace').read())
        when = datetime.date.fromisoformat(m.group(1)) if m else None
    except (OSError, ValueError):
        when = None
    if when is None:
        return (f'{POCKET} NOT rebuilt: it is a hand-built snapshot no script produces, and it carries '
                f'no dated snapshot note. Ask Claude to add the note (check_pages.py warns on it).')
    age = (today - when).days
    stale = ' STALE, past %d days: ask Claude to rebuild it from the week sheet.' % POCKET_MAX_DAYS \
        if age > POCKET_MAX_DAYS else ''
    return (f'{POCKET} NOT rebuilt: hand-built snapshot dated {when.isoformat()}, {age} day'
            f'{"" if age == 1 else "s"} old; no script produces it and this one does not pretend to.{stale}')


if __name__ == '__main__':
    main()
