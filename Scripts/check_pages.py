"""check_pages.py -- fail the build when a generated page ships a template instead of a value.

WHY THIS EXISTS. On 18 September eleven CSS rules on the commands page were found to have shipped
as literal ``{{ }}`` and to have NEVER applied, on any build, since the page was written. Matt found
them by looking at the page, which is the only reason they were found at all. Nothing in the tree
refuses to build a page carrying an unsubstituted template, a dead local link or a cell that says
None. Doc 369, doc 353, doc 372.

WHAT IT CHECKS, five things, each one an instance of a defect this project actually shipped:

    C1  ``{{`` inside a <style> block.      Doc 369. Two opening braces are never valid CSS; they
                                            are a .format() escape on a string nobody formatted.
    C2  an unsubstituted ``{token}`` or     The general case of C1: a placeholder that reached the
        ``%s`` in visible text or in an     reader. Checked outside <style> and <script>, where a
        attribute value.                    brace means CSS and a percent means a width.
    C3  a local href pointing at a file     Doc 353: the commands link went to a stub. Doc 372: two
        that is not on disk.                pages had no way back. Resolved against the PAGE's own
                                            directory, which is how a browser resolves it.
    C4  a table cell whose whole content    The pandas defect: a missing value rendered rather than
        is None, nan, NaN or NULL.          caught. Doc 375's Pickens row was its cousin.
    C5  a page built from an ESPN pull      Doc 380: the Saturday claim settled at 03:11 and every
        that does not carry the read time   page still described Friday's roster, with nothing on
        in machine-readable form            it saying when ESPN had last been read. The three
        (data-built="<epoch ms>").          pull-built pages now carry it; this refuses one that
                                            lost it.
    C6  THE CALL's first row on the week    The take contract (directive 0.1(h)) and doc 433: the
        sheet does not PRINT, beside the    page must DISPLAY the inputs the screen did not measure,
        man taken, (a) a vintage word,      not filter on them. A take with no vintage is a guess
        (b) the man ahead when he is a      wearing a number; a back with no man ahead is a seat
        running back, (c) one display-only  nobody checked; a take that prints none of what the
        input the project holds for him     project holds for the man cannot be fact-checked from
        (last two games, air yards, the     the page. Display, not filter: the rule never changes
        depth-chart slot) or "not held".    who is taken, only what is printed beside him.
                                            A WARNING, NOT A FAILURE, UNTIL 2026-10-06: measured
                                            on the 29 Sept page the first row fails (a) and (c),
                                            and the builder is being changed to print them. The
                                            rule is not weakened to pass today's page.
    C7  the pocket sheet's snapshot note    ONLINE_POCKET_SHEET.html is a hand-built snapshot of
        is missing or its date is more      the week sheet that only a Claude session edits, and
        than 7 days old.                    make_online.py cannot build what no script builds. The
                                            page says so in a dated line; a stale date is a
                                            warning, because the page still carries a true date.

WHAT IT DELIBERATELY DOES NOT CHECK, and this is the finding that shaped it:

    Doc 374's catalog proposed linting for ``{{``, ``}}`` and ``{token}`` anywhere in a built page.
    MEASURED ON THE SHIPPED TREE, 19 SEPT, THAT RULE PRODUCES TWENTY-ONE FALSE POSITIVES AND ZERO
    TRUE ONES. Every ``}}`` on every page is a nested CSS close (``@media{.x{...}}``), which is
    correct CSS, and the single ``{{`` is MY_TODO.html's prose describing the doc 369 bug. A guard
    that cries wolf twenty-one times on its first run is worse than no guard, because the reader
    learns to skip it. So ``}}`` is not checked at all and ``{{`` is checked only where it cannot
    be legitimate.

    py check_pages.py              check the shipped pages, exit 1 if anything is wrong
    py check_pages.py --selftest   run the negative controls and exit

THE NEGATIVE CONTROLS RUN FIRST (0.2: a guard that has never been shown to fire is not a guard).
--selftest reproduces each of the four defects and asserts the guard FIRES, then reproduces the
four legitimate shapes that look like them and asserts it stays QUIET.
"""
import datetime as dt
import html as _html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
SRC = os.path.join(ROOT, 'Source')

# The pages ff.bat builds, plus the two static signposts a reader can land on.
PAGES = [
    os.path.join(SRC, 'WEEK_SHEET.html'),
    os.path.join(SRC, 'MY_TODO.html'),
    os.path.join(SRC, 'LINEUP_CHECK.html'),
    os.path.join(SRC, 'THE_WEEKLY_WIRE.html'),
    os.path.join(SRC, 'COMMANDS.html'),
    os.path.join(ROOT, 'COMMANDS.html'),
]
# The hand-built snapshot (C7). Held to its dated note only: it is not built by any script, so C1
# to C5 have no builder to fix and would only teach the reader to skip the report.
POCKET = os.path.join(SRC, 'ONLINE_POCKET_SHEET.html')

# C6: a warning, not a failure, until this date. The 29 Sept page fails (a) and (c) and the
# builder is being changed to print them; the guard ships now so the fix is measured, not asserted.
C6_WARN_UNTIL = dt.date(2026, 10, 6)
C6_WHY = ('the builder does not print these beside the take yet; the roster-table and bet-lane '
          'columns that carry them are being added. A warning until %s, a failure after.'
          % C6_WARN_UNTIL.isoformat())
# (a) a vintage word: a projection, or this season's games.
VINTAGE = re.compile(r'\bproj\b|\bprojection\b|\bprojected\b|this season|\b\d+ games?\b|of \d+ game', re.I)
# (b) the man ahead, for a running back: named, or "not checked".
MAN_AHEAD = re.compile(r'\bbehind\b|man ahead|ahead of him|not checked', re.I)
# (c) one display-only input the project holds for him, or the words "not held".
HELD_INPUT = re.compile(r'last two|expected\b|air.yards|air yards|depth.chart|chart slot|'
                        r'\b(?:RB|WR|TE|QB)[1-4]\b|on the line|implied total|not held', re.I)
# "on the line" and "implied total": the pregame line is the held input for a defense or a
# quarterback (finding 4.39, doc 443), and the builder prints it beside the take.
CALL_HEAD = re.compile(r'The call\s*</h3>', re.I)
POS_META = re.compile(r'<span class="meta">\s*([A-Z/]{1,4})\b')
# C7: the pocket sheet's note, machine-readable first, the prose date second.
POCKET_NOTE = re.compile(r'class="snapshot"[^>]*data-snapshot="(\d{4}-\d{2}-\d{2})"')
POCKET_PROSE = re.compile(r'snapshot from the week sheet of\s+(?:\w+\s+)?(\d{1,2} \w+ \d{4})', re.I)
POCKET_MAX_DAYS = 7


def _text(fragment):
    return _html.unescape(re.sub(r'<[^>]+>', ' ', fragment))


def first_take(text):
    """(row_html, name, pos) for THE CALL's first row on the week sheet, or None when the page
    has no such table. A table with a heading and no rows returns ('', '', '')."""
    m = CALL_HEAD.search(text)
    if not m:
        return None
    body = re.search(r'<tbody>(.*?)</tbody>', text[m.end():], re.S)
    if not body:
        return ('', '', '')
    row = re.search(r'<tr>(.*?)</tr>', body.group(1), re.S)
    if not row or '<th scope="row">' not in row.group(1):
        return ('', '', '')
    r = row.group(1)
    head = re.search(r'<th scope="row">(.*?)</th>', r, re.S)
    name = _text(re.sub(r'<span class="meta">.*?</span>', '', head.group(1), flags=re.S)).strip() if head else ''
    pm = POS_META.search(r)
    return (r, name, pm.group(1) if pm else '')


def scan_take(text, today=None):
    """C6. The findings, with no grace applied; scan() decides whether they warn or fail."""
    found = first_take(text)
    if found is None:
        return [('C6 no "The call" table, so the take rule could not be checked', 0, 'WEEK_SHEET.html')]
    row, name, pos = found
    if not row:
        return []
    plain = _text(row)
    bad = []
    if not VINTAGE.search(plain):
        bad.append(('C6(a) the top take prints no vintage word', _lineno(text, text.find(row)),
                    '%s: nothing says proj, this season or N games' % name))
    if pos == 'RB' and not MAN_AHEAD.search(plain):
        bad.append(('C6(b) a running back taken with no man ahead printed', _lineno(text, text.find(row)),
                    '%s: name the incumbent or print "not checked"' % name))
    if not HELD_INPUT.search(plain):
        bad.append(('C6(c) the top take prints none of the inputs the project holds for him',
                    _lineno(text, text.find(row)),
                    '%s: last two games actual/expected, air-yards share or the depth-chart slot, or "not held"' % name))
    return bad


def scan_pocket(text, today=None):
    """C7. The snapshot note and its date."""
    today = today or dt.date.today()
    m = POCKET_NOTE.search(text)
    if m:
        try:
            when = dt.date.fromisoformat(m.group(1))
        except ValueError:
            return [('W7 the pocket sheet note carries a date that does not parse', 0, m.group(1))]
    else:
        p = POCKET_PROSE.search(text)
        if not p:
            return [('W7 the pocket sheet has no dated snapshot note', 0,
                     'expected: Hand-built snapshot from the week sheet of <date>')]
        try:
            when = dt.datetime.strptime(p.group(1), '%d %B %Y').date()
        except ValueError:
            return [('W7 the pocket sheet note carries a date that does not parse', 0, p.group(1))]
    age = (today - when).days
    if age > POCKET_MAX_DAYS:
        return [('W7 the pocket sheet snapshot is %d days old, past %d' % (age, POCKET_MAX_DAYS), 0,
                 'rebuild it from the week sheet, or accept that it is stale and say so on the page')]
    return []

# The pages built from a live ESPN read (doc 380). MY_TODO and the two COMMANDS pages are built
# from files on the drive, not from a pull, and are not held to C5.
PULL_BUILT = ('WEEK_SHEET.html', 'LINEUP_CHECK.html', 'THE_WEEKLY_WIRE.html')
BUILT_AT = re.compile(r'data-built="(\d{12,14})"')

STYLE = re.compile(r'<style\b[^>]*>(.*?)</style>', re.S | re.I)
SCRIPT = re.compile(r'<script\b[^>]*>(.*?)</script>', re.S | re.I)
BRACED = re.compile(r'\{[A-Za-z_][A-Za-z0-9_]*\}')
PCTFMT = re.compile(r'%\([A-Za-z_]\w*\)s|(?<![0-9])%[sdifr](?![A-Za-z0-9])')
HREF = re.compile(r'href\s*=\s*"([^"]*)"', re.I)
NULLCELL = re.compile(r'<t[dh]\b[^>]*>\s*(None|nan|NaN|NULL)\s*</t[dh]>', re.I)
SKIP_SCHEME = ('http://', 'https://', 'mailto:', 'javascript:', 'data:', 'tel:')


def _lineno(s, idx):
    return s.count('\n', 0, idx) + 1


def scan(name, text, base):
    """Return a list of (check, line, detail). base is the directory the page sits in."""
    bad = []

    # C1 -- two opening braces inside CSS. Never legitimate; always a .format() escape that
    # never met a .format(). The offset arithmetic keeps the reported line number honest.
    for m in STYLE.finditer(text):
        css, off = m.group(1), m.start(1)
        for b in re.finditer(r'\{\{', css):
            bad.append(('C1 literal {{ in <style>', _lineno(text, off + b.start()),
                        css[max(0, b.start() - 60):b.start() + 40].strip().replace('\n', ' ')))

    # C2 -- a placeholder that survived into something the reader sees. Style and script are
    # blanked first, preserving length so line numbers still point at the real line.
    body = SCRIPT.sub(lambda m: ' ' * len(m.group(0)), STYLE.sub(lambda m: ' ' * len(m.group(0)), text))
    for rx, label in ((BRACED, 'C2 unsubstituted {token}'), (PCTFMT, 'C2 unsubstituted %-format')):
        for m in rx.finditer(body):
            bad.append((label, _lineno(text, m.start()),
                        text[max(0, m.start() - 50):m.start() + 50].strip().replace('\n', ' ')))

    # C3 -- a local link with nothing behind it. A browser resolves a relative href against the
    # page's own directory, so that is what this resolves against; resolving against the shell's
    # working directory is how this check would silently pass on Matt's machine and fail here.
    for m in HREF.finditer(text):
        h = m.group(1).strip()
        if not h or h.startswith('#') or h.lower().startswith(SKIP_SCHEME):
            continue
        target = h.split('#')[0].split('?')[0].replace('/', os.sep)
        if not target:
            continue
        full = os.path.normpath(os.path.join(base, target))
        if not os.path.exists(full):
            bad.append(('C3 dead local link', _lineno(text, m.start()), h))

    # C4 -- a missing value rendered as a word.
    for m in NULLCELL.finditer(text):
        bad.append(('C4 null in a cell', _lineno(text, m.start()), m.group(0)))

    # C5 -- a pull-built page with no machine-readable read time (doc 380). The visible stamp is
    # for Matt; this attribute is what the on-open script reads, and a page without it can never
    # say how old it is.
    if name in PULL_BUILT and not BUILT_AT.search(text):
        bad.append(('C5 no data-built read time on a pull-built page', 0, name))

    # C6 -- the top take prints its inputs (display, not filter). A warning, with its reason,
    # until C6_WARN_UNTIL; a failure after. The rule itself is the same on both sides of the date.
    if name == 'WEEK_SHEET.html':
        grace = dt.date.today() < C6_WARN_UNTIL
        for check, line, detail in scan_take(text):
            if grace:
                bad.append(('W' + check[1:], line, detail + ' -- ' + C6_WHY))
            else:
                bad.append((check, line, detail))

    return bad


def check_file(path):
    if not os.path.exists(path):
        return [('C0 page was not built', 0, path)]
    text = open(path, encoding='utf-8', errors='replace').read()
    return scan(os.path.basename(path), text, os.path.dirname(path))


def check_pocket(path):
    """C7 only: the snapshot is hand-built, so a missing page is a warning too, not a failure."""
    if not os.path.exists(path):
        return [('W7 the pocket sheet is not on the drive', 0, path)]
    text = open(path, encoding='utf-8', errors='replace').read()
    return scan_pocket(text)


def report(results):
    """Returns (failures, warnings). A check whose label starts with W is printed and not counted
    as a failure: it is a thing the reader should know, not a thing the page cannot ship with."""
    total = warns = 0
    for path, bad in results:
        rel = os.path.relpath(path, ROOT)
        if not bad:
            print('  ok    %s' % rel)
            continue
        hard = [b for b in bad if not b[0].startswith('W')]
        soft = [b for b in bad if b[0].startswith('W')]
        total += len(hard)
        warns += len(soft)
        print('  %-5s %s -- %d%s' % ('FAIL' if hard else 'warn', rel, len(hard),
                                     (' (+%d warning%s)' % (len(soft), '' if len(soft) == 1 else 's')) if soft else ''))
        for check, line, detail in (hard + soft)[:12]:
            print('          line %-5s %s' % (line, check))
            print('                      %s' % detail[:300])
        if len(bad) > 12:
            print('          ... and %d more' % (len(bad) - 12))
    return total, warns


# ----------------------------------------------------------------------------- negative controls

def selftest():
    """Each defect, reproduced, must fire. Each look-alike, reproduced, must not."""
    import tempfile
    fails = []
    _ran = [0]          # every control counts itself as it prints; a hand sum went stale (doc 443)

    def run(html, note, want, base=None):
        with tempfile.TemporaryDirectory() as d:
            b = base or d
            if base is None:
                # give the clean controls a real file to link at
                open(os.path.join(d, 'there.html'), 'w', encoding='utf-8').write('<p>hi</p>')
            got = scan('control.html', html, b)
            ok = (len(got) > 0) == want
            _ran[0] += 1
            print('  %-4s %-58s fired=%d expected=%s' % ('ok' if ok else 'BAD', note, len(got), want))
            if not ok:
                fails.append((note, got))
            return got

    print('MUST FIRE -- the four defects this project actually shipped')
    # 1. doc 369, verbatim in shape: CSS written for .format() that nobody formatted.
    run('<style>.copy{{background:var(--accent);color:#fff}}</style><p>x</p>',
        'doc 369: eleven CSS rules that shipped as literal braces', True)
    # 2. the general case: a placeholder in text the reader sees.
    run('<style>.a{color:red}</style><p>Take {player} at {pick}.</p>',
        'a {token} that reached the page', True)
    run('<p>bar to start %s points</p>', 'a %-format that reached the page', True)
    # 3. doc 353 / doc 372: a link with nothing behind it.
    run('<p><a href="NOT_THERE.html">commands</a></p>',
        'doc 353: a local link to a file that is not on disk', True)
    # 4. a missing value rendered as a word.
    run('<table><tr><td>Vele</td><td>nan</td></tr></table>', 'a nan cell', True)
    # 5. doc 380: a pull-built page that lost its read time.
    got5 = scan('WEEK_SHEET.html', '<style>.a{color:red}</style><p>built 19 September 2026</p>', '.')
    ok5 = any(b[0].startswith('C5') for b in got5)
    _ran[0] += 1
    print('  %-4s %-58s fired=%d expected=True' % ('ok' if ok5 else 'BAD',
          'doc 380: a pull-built page with no data-built attribute', len(got5)))
    if not ok5:
        fails.append(('C5 silent', got5))
    # 0. the page itself absent.
    missing = check_file(os.path.join(SRC, '__no_such_page__.html'))
    _ran[0] += 1
    print('  %-4s %-58s fired=%d expected=True'
          % ('ok' if missing else 'BAD', 'a page that was never built', len(missing)))
    if not missing:
        fails.append(('missing page', missing))

    print('MUST STAY QUIET -- the four shapes that look like them and are correct')
    # The reason doc 374's catalog rule could not ship: nested CSS closes.
    run('<style>@media (max-width:640px){.secnav a{padding:4px 7px}}\n'
        ':root{--ink:#eee;--ok:#3AA471}}</style><p>x</p>',
        'nested CSS closes, which is what every }} on every page is', False)
    # MY_TODO.html really does contain this sentence.
    run('<style>.a{color:red}</style>'
        '<p>eleven CSS rules that shipped as literal {{ }} and have NEVER applied</p>',
        'prose describing the bug, which MY_TODO.html carries today', False)
    # Percentages and external links.
    run('<p>91% of snaps, 17.3% of the team\'s</p>'
        '<p><a href="https://fantasy.espn.com/x">espn</a> <a href="#s3">jump</a>'
        ' <a href="mailto:a@b.c">mail</a></p>',
        'percentages, an external link, an anchor and a mailto', False)
    # A link that does resolve, and a legitimately empty cell.
    run('<p><a href="there.html">there</a></p><table><tr><td></td><td>none of it</td></tr></table>',
        'a link that resolves and a cell that is empty rather than None', False)
    # doc 380: the read time present on a pull-built page, and absent on a page that is not one.
    got5a = scan('THE_WEEKLY_WIRE.html', '<div class="sub" id="inputs" data-built="1789845420000" '
                 'data-settle="1789875000000">Read from ESPN Saturday 19 September 19:17 (THU).</div>', '.')
    got5b = scan('MY_TODO.html', '<p>built 19 September 2026</p>', '.')
    for got, note in ((got5a, 'a pull-built page carrying data-built'),
                      (got5b, 'the to-do page, which is not pull-built, without it')):
        ok = not got
        _ran[0] += 1
        print('  %-4s %-58s fired=%d expected=False' % ('ok' if ok else 'BAD', note, len(got)))
        if not ok:
            fails.append((note, got))

    # C6 -- the top take prints its inputs. The row below is the 29 Sept shape with the three
    # lines the contract asks for added; each control removes one of them.
    def call(meta, extra):
        return ('<h3 class="sub0">The call</h3><div class="scroll"><table><thead><tr><th>take</th>'
                '</tr></thead><tbody><tr><th scope="row">Michael Mayer<span class="meta">' + meta +
                ' &middot; LV &middot; 16% rostered</span>' + extra + '</th><td class="tot pos">+10.3</td>'
                '<td>Samaje Perine<span class="meta">RB</span></td><td class="tot">0.0</td>'
                '<td class="tot pos">+10.3</td><td class="meta">this week</td></tr></tbody></table></div>')
    full_te = ('<span class="meta">proj 10.3 a week &middot; last two games 8.1 actual on 6.4 expected'
               '</span>')
    full_rb = ('<span class="meta">this season, 3 games &middot; behind Josh Jacobs, missed 0 &middot; '
               'depth chart RB2</span>')
    print('MUST FIRE -- the take contract, one line removed at a time')
    c6 = [
        ('C6(a): the vintage word removed from the top take',
         call('TE', '<span class="meta">last two games 8.1 actual on 6.4 expected</span>'), 'C6(a)'),
        ('C6(b): a running back taken with no man ahead printed',
         call('RB', '<span class="meta">this season, 3 games &middot; depth chart RB2</span>'), 'C6(b)'),
        ('C6(c): a take printing none of the inputs the project holds',
         call('TE', '<span class="meta">proj 10.3 a week</span>'), 'C6(c)'),
        ('C6: the 29 Sept page shape, meta only (fires a and c)', call('TE', ''), 'C6(a)'),
    ]
    for note, page, want_label in c6:
        got = scan_take(page)
        ok = any(b[0].startswith(want_label) for b in got)
        _ran[0] += 1
        print('  %-4s %-58s fired=%d expected=True' % ('ok' if ok else 'BAD', note, len(got)))
        if not ok:
            fails.append((note, got))
    # And the grace period: on the week sheet the finding is a W until the date, a C after.
    got_w = scan('WEEK_SHEET.html', '<p data-built="1790681405625"></p>' + call('TE', ''), '.')
    kinds = {b[0][0] for b in got_w if 'C6' in b[0] or 'W6' in b[0]}
    want = {'W'} if dt.date.today() < C6_WARN_UNTIL else {'C'}
    ok = kinds == want
    _ran[0] += 1
    print('  %-4s %-58s fired=%d expected=True' % ('ok' if ok else 'BAD',
          'C6 on the week sheet is a %s today' % ('warning' if want == {'W'} else 'failure'), len(got_w)))
    if not ok:
        fails.append(('C6 grace', got_w))
    print('MUST STAY QUIET -- the same rows with the three lines present')
    full_dst = ('<span class="meta">proj 6.1 a week &middot; opponent total 20.5 on the line, PIT</span>')
    for note, page in (('a tight end with vintage and a held input', call('TE', full_te)),
                       ('a running back with vintage, the man ahead and the chart slot', call('RB', full_rb)),
                       ('a defense with vintage and the pregame line', call('D/ST', full_dst)),
                       ('a take that says "not held" and "not checked"',
                        call('RB', '<span class="meta">proj 6.1 &middot; not checked &middot; not held</span>')),
                       ('a call table with no rows', '<h3 class="sub0">The call</h3><table><tbody>'
                        '<tr><td colspan="6">nothing clears its price</td></tr></tbody></table>')):
        got = scan_take(page)
        ok = not got
        _ran[0] += 1
        print('  %-4s %-58s fired=%d expected=False' % ('ok' if ok else 'BAD', note, len(got)))
        if not ok:
            fails.append((note, got))

    # C7 -- the pocket sheet's dated note.
    today = dt.date.today()
    note_html = lambda d: ('<p class="snapshot" data-snapshot="%s">Hand-built snapshot from the week sheet '
                           'of %s; the week sheet is the live page.</p>' % (d.isoformat(), d.strftime('%A %d %B %Y')))
    print('MUST FIRE -- the pocket sheet note')
    for note, page in (('C7: a snapshot note dated 10 days ago', note_html(today - dt.timedelta(days=10))),
                       ('C7: no snapshot note at all', '<p class="stamp">Rebuilt from the Sunday pull.</p>'),
                       ('C7: a prose date 30 days old, no attribute',
                        '<p>Hand-built snapshot from the week sheet of %s</p>'
                        % (today - dt.timedelta(days=30)).strftime('%A %d %B %Y'))):
        got = scan_pocket(page)
        _ran[0] += 1
        print('  %-4s %-58s fired=%d expected=True' % ('ok' if got else 'BAD', note, len(got)))
        if not got:
            fails.append((note, got))
    print('MUST STAY QUIET -- the pocket sheet note, fresh')
    for note, page in (('a snapshot note dated today', note_html(today)),
                       ('a snapshot note dated 7 days ago, the edge', note_html(today - dt.timedelta(days=7)))):
        got = scan_pocket(page)
        _ran[0] += 1
        print('  %-4s %-58s fired=%d expected=False' % ('ok' if not got else 'BAD', note, len(got)))
        if got:
            fails.append((note, got))

    n = _ran[0]
    if fails:
        print('\nSELFTEST FAILED: %d control(s) behaved wrongly' % len(fails))
        return 1
    print('\nselftest: %d/%d controls behaved as specified' % (n, n))
    return 0


def main(argv):
    if '--selftest' in argv:
        return selftest()
    print('check_pages: every generated page, for templates that shipped as templates')
    results = [(p, check_file(p)) for p in PAGES] + [(POCKET, check_pocket(POCKET))]
    total, warns = report(results)
    if warns:
        print('\n%d warning(s) above are printed and not counted: read them, they name a page that '
              'is honest about what it lacks.' % warns)
    if total:
        print('\n%d problem(s). A PAGE IS SHOWING A TEMPLATE, A DEAD LINK OR A MISSING VALUE.' % total)
        print('Nothing above is a judgement call: each one is a thing the reader can see and')
        print('cannot act on. Fix the builder, not the page -- the page is rebuilt every run.')
        return 1
    print('\nno problems. Every page substituted what it meant to, and every local link resolves.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
