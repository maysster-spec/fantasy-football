"""lookahead_box.py -- the five-week look-ahead, on the week sheet.

WHY THIS EXISTS. wire.py's look_ahead() has ranked the next five weeks since the schedule was first
fetched: who on the roster is off, and the softest free quarterback and defense for each week. It
printed only to the wire page and the console, and the week sheet, the page Matt reads, never
carried it (claude_todo, 29 Sept). This module renders the same computation as one compact box for
WEEK_SHEET.html. It adds no ranking of its own: the schedule, last season's averages, the pregame
lines and the ranking rule are wire.py's, imported, so there is one look-ahead and not two.

Standard library only. box() never raises: it returns the box's HTML, or '' after printing one
console line, so a failure here can never take the week sheet down.

Inputs are what sheet_engine.render() already holds: the week, the roster rows and the free rows
(each a dict with name, pos, tm, wk, bye and status). The free quarterbacks are the twelve highest
rated, the same cut wire.py makes so the list is not third-stringers with a soft draw; a man ruled
out for weeks is left out of both pools and the box says how many.
"""
import html
import sys

E = lambda s: html.escape(str(s))

GONE = ('OUT', 'INJURY_RESERVE', 'SUSPENSION', 'PUP', 'NOT_ACTIVE')
TOP_QB = 12

CSS = ('<style>.ahead{margin:14px 0 6px}.ahead h4{margin:0 0 4px}'
       '.ahead table{border-collapse:collapse;width:100%;font-size:13.5px}'
       '.ahead th,.ahead td{text-align:left;vertical-align:top;padding:5px 8px;'
       'border-bottom:1px solid var(--rule,#ddd)}'
       '.ahead th{font-size:11px;text-transform:uppercase;letter-spacing:.06em}'
       '.ahead .m{font-size:12px;opacity:.75}.ahead .n{font-variant-numeric:tabular-nums}</style>')


def _wire():
    """wire.py's loaders and look_ahead(), without loading wire.py twice.

    When wire.py is the running script it is `__main__`, not `wire`, so a plain import would parse
    its 150 KB a second time and give the loaders a second LOAD_PROBLEMS list nobody prints. wire.py
    makes no ESPN call at import (every read sits inside a function), so importing it from another
    script is safe; the one thing it does at import is exit when `requests` is absent, and box()
    catches that exit.
    """
    m = sys.modules.get('__main__')
    if m is not None and all(hasattr(m, k) for k in
                             ('look_ahead', 'load_sched', 'load_team25', 'load_lines', 'LOAD_PROBLEMS')):
        return m
    import wire
    return wire


def compute(week, roster, freerows):
    """(weeks, notes, skipped). weeks is wire.look_ahead()'s list; notes are the loader problems that
    belong to this box (they are taken back off wire's own list so the wire page does not print them
    twice); skipped is how many free QB/D/ST were left out for being ruled out."""
    w = _wire()
    n0 = len(w.LOAD_PROBLEMS)
    sched, t25, lines = w.load_sched(), w.load_team25(), w.load_lines()
    notes = list(w.LOAD_PROBLEMS[n0:])
    del w.LOAD_PROBLEMS[n0:]

    def gone(r):
        return (r.get('status') or 'ACTIVE').upper() in GONE

    qbs = [r for r in (freerows or []) if r.get('pos') == 'QB' and r.get('tm')]
    dsts = [r for r in (freerows or []) if r.get('pos') == 'D/ST' and r.get('tm')]
    skipped = sum(1 for r in qbs + dsts if gone(r))
    qbs = sorted((r for r in qbs if not gone(r)), key=lambda r: -float(r.get('wk') or 0))[:TOP_QB]
    dsts = [r for r in dsts if not gone(r)]
    free_qb = [{'player': r['name'], 'team': r['tm']} for r in qbs]
    free_dst = [{'player': r['name'], 'team': r['tm']} for r in dsts]
    my_byes = {}
    for p in (roster or []):
        try:
            b = int(float(p.get('bye') or 0))
        except (TypeError, ValueError):
            continue
        if b:
            my_byes.setdefault(b, []).append(p.get('name', '?'))
    weeks = w.look_ahead(int(week), sched, t25, free_qb, free_dst, my_byes, lines=lines) or []
    return weeks, notes, skipped


def _cell(picks, detail, axis, kind):
    """One cell: the best man with his number and the axis it was read on, then the next two."""
    if not picks:
        return '<span class="m">nobody free with a game</span>'
    v, name, tm, opp = picks[0]
    d = detail.get(tm, {})
    vs = ('at ' if d.get('side') == 'away' else 'v ') + opp
    if axis == 'line':
        num = (f'own total <b class="n">{v:.1f}</b> on the line' if kind == 'qb'
               else f'opponent total <b class="n">{v:.1f}</b> on the line')
    else:
        num = (f'opponent allows <b class="n">{v:.1f}</b> a game, last season' if kind == 'qb'
               else f'opponent scores <b class="n">{v:.1f}</b> a game, last season')
    rest = ', '.join(f'{E(p[1])} {p[0]:.1f}' for p in picks[1:3])
    return (f'<b>{E(name)}</b> <span class="m">{E(tm)} {E(vs)}</span><br>{num}'
            + (f'<br><span class="m">then {rest}</span>' if rest else ''))


def render_box(weeks, notes=(), skipped=0):
    if not weeks:
        why = '; '.join(notes) if notes else 'no schedule on file for the weeks ahead'
        return (CSS + '<div class="ahead"><h4>The five weeks ahead</h4>'
                f'<p class="m">Not built: {E(why)}.</p></div>')
    rows = []
    for wk in weeks:
        off = ', '.join(E(n) for n in wk.get('off') or []) or '<span class="m">nobody</span>'
        detail = wk.get('detail') or {}
        rows.append(f'<tr><th scope="row">week {int(wk["week"])}</th><td>{off}</td>'
                    f'<td>{_cell(wk.get("qb") or [], detail, wk.get("axis"), "qb")}</td>'
                    f'<td>{_cell(wk.get("dst") or [], detail, wk.get("axis"), "dst")}</td></tr>')
    foot = []
    if any(w.get('axis') != 'line' for w in weeks):
        foot.append('A week with no posted line yet is ranked on the averages from last season and says so.')
    if skipped:
        foot.append(f'{skipped} free man ruled out for weeks {"is" if skipped == 1 else "are"} left out.')
    foot.extend(notes)
    return (CSS + '<div class="ahead"><h4>The five weeks ahead: who is off, and the best free '
            'quarterback and defense</h4>'
            '<p class="m">Claim the bye cover the week before it bites. A quarterback wants his own '
            'team\'s total high; a defense wants the opponent\'s total low. Every number here is the '
            'pregame line where every game that week has one.</p>'
            '<table><thead><tr><th>week</th><th>your men off</th><th>best free QB</th>'
            '<th>best free D/ST</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table>'
            + (f'<p class="m">{" ".join(E(f) for f in foot)}</p>' if foot else '')
            + '</div>')


def box(week, roster, freerows):
    """The box, or '' after one console line. Never raises."""
    try:
        if not week:
            return ''
        weeks, notes, skipped = compute(week, roster, freerows)
        return render_box(weeks, notes, skipped)
    except (Exception, SystemExit) as exc:
        print(f'  weeks-ahead box NOT built -- {type(exc).__name__}: {exc}')
        return ''
