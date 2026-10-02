"""make_commands.py -- rebuild COMMANDS.html from the files themselves.

MATT, 2026-09-18: "i wanted this updated ... if there are commands that live better in a bat file
for simplicity do that."

WHY THIS EXISTS AT ALL. COMMANDS.html was hand-written on 6 September, for the draft, and nothing
rebuilt it, nothing pinned it and nothing checked it. Eleven days later it still described draft
night. SECTION 9 of the directive already records the rule it broke: every prose map in this
project went stale within hours, so the map has to be GENERATED. This is make_howto.py's pattern
(it regenerates HOW_TO_READ_IT from live_draft.COLGLOSS) applied to the command page.

ONE SOURCE, TWO RENDERINGS. The command list lives in sheet_engine.TODO_CMDS -- the same list the
to-do page prints. This page renders that list and adds two things it can only get by reading the
tree: what each .bat file ACTUALLY runs, line by line, and when Task Scheduler fires it. Neither
is typed out here, so neither can drift.

THE GUARD (0.5(c)5, the missing-row check). Every script named on the page is checked against the
folder before the page is written. A page that names a script which is not there is the same
defect as a printed board missing the row it was built for, so this REFUSES to write and says
which names failed.

    py make_commands.py            rebuild it
    py make_commands.py --check    say what it would do, write nothing

Standard library only. Paths resolve against this file, never the shell's cwd.
"""
import datetime as dt
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
SRC = os.path.join(ROOT, 'Source')
PAGE = os.path.join(ROOT, 'COMMANDS.html')
sys.path.insert(0, HERE)
import sheet_engine                                                        # noqa: E402

E = html.escape
TEAM = 'The Poetry of Junkyard Juggers'

# The batch files worth putting on a page, in the order a season uses them. A .bat NOT listed here
# is either a stub or draft-night only; the page says so rather than pretending it does not exist.
BATS = ['ff.bat', 'draft_night.bat', 'sept5_after.bat', 'refresh_pull.bat', 'setup_tasks.bat']


def bat_steps(name):
    """What a batch file REALLY runs: every `py X.py ...` line, in order, deduped consecutively.

    Read out of the file, never typed here. A step this cannot find is a step the page does not
    claim.
    """
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        return None
    txt = open(p, encoding='utf-8', errors='replace').read()
    out = []
    for ln in txt.splitlines():
        s = ln.strip()
        low = s.lower()
        if low.startswith('rem') or s.startswith('::'):
            continue
        # AN ECHO IS NOT A STEP. The first version of this read ff.bat's own reminder line --
        # `echo ... ^(rebuild weekly: py research\\wk1\\build_form.py^)` -- and printed it as
        # something ff.bat RUNS. ff.bat deliberately does not run it, and its comment block says
        # why. A page that claims a batch file runs a step it refuses to run is worse than no page.
        if low.startswith('echo') or 'echo ' in low[:low.find('py ') if 'py ' in low else 0]:
            continue
        m = re.search(r'\bpy\s+([A-Za-z0-9_\\/.-]+\.py)([^>|&]*)', s)
        if m:
            step = ('py ' + m.group(1) + ' ' + m.group(2).strip()).strip()
            if not out or out[-1] != step:
                out.append(step)
    return out


def bat_purpose(name):
    """The one-line purpose, taken from the batch file's own second REM line."""
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        return ''
    for ln in open(p, encoding='utf-8', errors='replace'):
        s = ln.strip()
        if s.lower().startswith('rem') and '--' in s:
            body = s.split('--', 1)[1].strip()
            if len(body) > 8:
                return body.rstrip('.')
    return ''


def schedule():
    """The live schedule, parsed out of setup_tasks.bat's own schtasks lines."""
    p = os.path.join(HERE, 'setup_tasks.bat')
    if not os.path.exists(p):
        return []
    rows = []
    for ln in open(p, encoding='utf-8', errors='replace'):
        if 'schtasks /create' not in ln:
            continue
        tn = re.search(r'/tn\s+"([^"]+)"', ln)
        # /tr carries ESCAPED quotes (`/tr "cmd /c \\"%S%ff.bat\\" TUE"`), so anchoring on the
        # closing quote finds `cmd /c \\` and no batch file. Take the .bat name from the rest of
        # the line instead; there is exactly one.
        tr = re.search(r'/tr\s+(.*)$', ln)
        d = re.search(r'/d\s+(\w+)', ln)
        st = re.search(r'/st\s+([\d:]+)', ln)
        if tn:
            runs = ''
            if tr:
                b = re.search(r'([A-Za-z0-9_]+\.bat)', tr.group(1))
                runs = b.group(1) if b else ''
            rows.append((tn.group(1), (d.group(1) if d else ''),
                         (st.group(1) if st else ''), runs))
    return rows


def named_scripts(cmds):
    """Every script this page is about to name, so the guard can check it exists."""
    names = set()
    for cmd, _t, _w, _p in cmds:
        m = re.search(r'\b([A-Za-z0-9_\\/.-]+\.(?:py|bat))\b', cmd)
        if m:
            names.add(m.group(1).replace('\\', os.sep))
    return sorted(names)


def build(stamp):
    cmds = list(sheet_engine.TODO_CMDS)
    links = list(sheet_engine.TODO_LINKS)

    # ---- THE GUARD, BEFORE ANY HTML IS BUILT -------------------------------------------------
    missing = [n for n in named_scripts(cmds) if not os.path.exists(os.path.join(HERE, n))]
    bats_missing = [b for b in BATS if not os.path.exists(os.path.join(HERE, b))]
    if missing or bats_missing:
        raise SystemExit('REFUSING TO WRITE: the page would name scripts that are not in %s --\n'
                         '  %s\nFix the list or the tree; do not ship a map to a missing file.'
                         % (HERE, ', '.join(missing + bats_missing)))

    rows = []
    for cmd, title, why, primary in cmds:
        cls = ' class="lead"' if primary else ''
        rows.append('<tr%s><td class="cmd"><code>%s</code>'
                    '<button class="cp" type="button" data-cmd="%s">copy</button></td>'
                    '<td class="what"><b>%s</b><br><span class="why">%s</span></td></tr>'
                    % (cls, E(cmd), E(cmd), E(title), E(why)))

    bat_html = []
    for b in BATS:
        steps = bat_steps(b)
        purpose = bat_purpose(b)
        if steps is None:
            continue
        body = ('<ol class="steps">' + ''.join('<li><code>%s</code></li>' % E(s) for s in steps)
                + '</ol>') if steps else '<p class="why">No python steps; it registers or gates.</p>'
        bat_html.append('<div class="batbox"><h4>%s</h4><p class="why">%s</p>%s</div>'
                        % (E(b), E(purpose), body))

    sched = schedule()
    sched_html = ''
    if sched:
        sched_html = ('<table class="g"><thead><tr><th>task</th><th>day</th><th>time</th>'
                      '<th>runs</th></tr></thead><tbody>'
                      + ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td><code>%s</code></td></tr>'
                                % (E(a), E(d), E(s), E(r)) for a, d, s, r in sched)
                      + '</tbody></table>')

    # [doc 435] An absolute URL (the roster clock, an https:// artifact) is used as is; only a page
    # in Source\ is reached from ROOT by the Source/ prefix. Prefixing the URL made a dead link
    # that check_pages.py flagged on every run from 25 Sept (C3: Source/https://claude.ai/...).
    link_html = ''.join('<li><a href="%s">%s</a> <span class="why">%s</span></li>'
                        % (E(f if '://' in f else 'Source/' + f), E(t), E(w)) for f, t, w in links)

    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Commands</title><style>{css}{tcss}
table.g{border-collapse:collapse;width:100%;margin:0 0 10px}
table.g th,table.g td{border:1px solid var(--rule);padding:6px 9px;text-align:left;
font-size:13.5px;vertical-align:top}
table.g thead th{background:var(--sunk);font-family:var(--disp);text-transform:uppercase;
letter-spacing:.06em;font-size:11.5px;color:var(--ink2)}
tr.lead td{background:var(--sunk)}
td.cmd{white-space:nowrap;width:1%}
code{font-family:var(--mono);font-size:13px}
.why{color:var(--muted);font-size:13px}
.batbox{border:1px solid var(--rule);border-left:4px solid var(--struct);background:var(--sunk);
padding:10px 14px;margin:0 0 10px}
.batbox h4{margin:0 0 3px;font-family:var(--disp);text-transform:uppercase;letter-spacing:.06em;
font-size:12.5px;color:var(--struct)}
ol.steps{margin:7px 0 0 18px;padding:0}
ol.steps li{margin:2px 0;font-size:13px}
/* THE COPY BUTTON, BACK. Matt, 2026-09-19: "once i finally find the commands page, the copy
   button was removed". It copies with execCommand as well as the clipboard API, because this
   page is opened over file:// where the modern call is refused without warning. */
td.cmd{position:relative}
button.cp{font-family:var(--disp);text-transform:uppercase;letter-spacing:.07em;font-size:10.5px;
color:var(--struct);background:var(--structbg);border:1px solid var(--struct);border-radius:3px;
padding:3px 8px;margin-left:10px;cursor:pointer;vertical-align:middle}
button.cp:hover{background:var(--struct);color:var(--surface)}
button.cp.done{background:var(--okbg);color:var(--ok);border-color:var(--ok)}
</style></head><body id="top"><div class="wrap">
<header><p class="kick">{team} &middot; built {stamp}</p>
<h1>Commands</h1>
<p class="dek">Everything you can run, and what each one does. This page is <b>generated</b> from
the command list the to-do page uses and from the batch files themselves, so it cannot drift from
what is actually on disk. Open a shell in <code>Scripts</code> and type the line, or press
<b>copy</b> and paste it.</p>
{pagebar}</header>
<nav class="secnav" aria-label="sections of this page">
<a href="#run">run these</a><a href="#bats">what each batch file runs</a>
<a href="#sched">when it fires</a><a href="#pages">the pages</a>
<a class="top" href="#top">top &uarr;</a></nav>

<h3 class="sub0" id="run">Run these</h3>
<p class="why">The first row does everything, in order. The rest are what it runs, for when you
only want one of them.</p>
<table class="g"><tbody>{rows}</tbody></table>

<h3 class="sub0" id="bats">What each batch file actually runs</h3>
<p class="why">Read out of the files, not typed here.</p>
{bats}

<h3 class="sub0" id="sched">When it fires on its own</h3>
<p class="why">Four separately-named tasks so Task Scheduler reports a result for each occasion.
Re-register with <code>setup_tasks.bat</code> from an administrator prompt.</p>
{sched}

<h3 class="sub0" id="pages">The pages</h3>
<div class="hub"><ul>{links}</ul></div>

<footer>Generated by <code>make_commands.py</code>. The command list is
<code>sheet_engine.TODO_CMDS</code>, shared with the to-do page; the steps and the schedule are
parsed from the batch files. If a script named here is missing from the folder, this page refuses
to build rather than pointing you at nothing.</footer>
<script>
document.addEventListener('click', function (ev) {
  var b = ev.target.closest ? ev.target.closest('button.cp') : null;
  if (!b) return;
  var txt = b.getAttribute('data-cmd') || '';
  function flag() { b.textContent = 'copied'; b.classList.add('done');
    setTimeout(function () { b.textContent = 'copy'; b.classList.remove('done'); }, 1400); }
  // execCommand first: over file:// the async clipboard API is refused silently in some builds,
  // and a button that reports success without copying is the exit-code defect in a browser.
  try {
    var ta = document.createElement('textarea');
    ta.value = txt; ta.setAttribute('readonly', '');
    ta.style.position = 'fixed'; ta.style.top = '-1000px';
    document.body.appendChild(ta); ta.select();
    var ok = document.execCommand('copy');
    document.body.removeChild(ta);
    if (ok) { flag(); return; }
  } catch (e) { /* fall through */ }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(txt).then(flag, function () { b.textContent = 'copy failed'; });
  } else { b.textContent = 'copy failed'; }
});
</script>
</div></body></html>""".replace('{css}', sheet_engine.CSS).replace('{tcss}', sheet_engine.TODO_CSS) \
        .replace('{team}', E(TEAM)).replace('{stamp}', E(stamp)) \
        .replace('{rows}', ''.join(rows)).replace('{bats}', ''.join(bat_html)) \
        .replace('{sched}', sched_html).replace('{links}', link_html) \
        .replace('{pagebar}', sheet_engine.page_bar(current='../COMMANDS.html', at_root=True))


def main(argv):
    stamp = dt.date.today().strftime('%d %B %Y')
    page = build(stamp)
    if '--check' in argv:
        print('  --check: would write %s, %d bytes. Nothing written.' % (PAGE, len(page)))
        return 0
    open(PAGE, 'w', encoding='utf-8').write(page)
    # VERIFY THE ARTIFACT, NOT THE EXIT CODE (0.2).
    if not os.path.exists(PAGE):
        print('  *** NOTHING ON DISK AT %s' % PAGE)
        return 1
    n = os.path.getsize(PAGE)
    print('  written: %s  (%d bytes, %d commands, %d batch files, %d scheduled tasks)'
          % (PAGE, n, len(sheet_engine.TODO_CMDS), len(BATS), len(schedule())))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
