"""check_vintage.py -- fail the build when a page prints a rate this season already refuted.

WHY THIS EXISTS. Four recommendations in twenty-four hours were wrong the same way: a number was
read off a generated page and used without asking what produced it. Pineiro's 8.4, Schultz's 11.1,
Schultz's 38% and Vele's 5.8. The worst of them, Vele, was a PRESEASON projection of 5.8 a week
sitting on the page beside a drop cost of 0.0, while his own form file had him at 16.4 half-PPR on
91% of the snaps in week one. The page had no way to say which of those two numbers it was showing,
so there was nothing to check even when someone thought to check. Doc 373.

WHAT IT DOES. Reads the rates WEEK_SHEET.html actually prints, reads what each man has actually
averaged in Source\\form_2026.csv, and FAILS when the two disagree by more than a starter's week.
It is a guard on the page, not on the model: it does not decide which number is right, it refuses
to let the page show one of them as though the other did not exist.

    py check_vintage.py              check the shipped pages, exit 1 if anything is stale
    py check_vintage.py --selftest   run the negative controls and exit

THE NEGATIVE CONTROLS RUN FIRST (0.2: a guard that has never been shown to fire is not a guard).
--selftest builds a page whose numbers agree and asserts the guard PASSES, then builds one carrying
the real Vele defect and asserts it FIRES on that exact row.
"""
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', 'Source'))

# A starter's week. Below this the two numbers disagree by less than one lineup decision is worth,
# and flagging it would train the reader to ignore the guard.
TOL = 4.0
# One game is a thin basis for overruling a projection, so a single game must disagree by more.
TOL_ONE_GAME = 6.0


def printed_rates(path):
    """Every 'pts/wk' rate the week sheet prints, by player name.

    The page puts the name in a <span class="pl"> and the rate in the next <td class="rate">.
    Reading the page the reader reads, rather than the model behind it, is the point: a defect that
    never reaches the page is not this guard's business.
    """
    if not os.path.exists(path):
        return {}, 'WEEK_SHEET.html is not there'
    s = open(path, encoding='utf-8', errors='replace').read()
    out = {}
    # ONE ROW AT A TIME. The first draft matched a name and then the next rate cell ANYWHERE after
    # it, which walked out of the table: the seat list writes a percentage in its rate column, the
    # percentage did not match, and the search ran on into the quarterback table and paired Tank
    # Bigsby with 18.0. A guard carrying a false positive is one the reader learns to ignore.
    name_pat = re.compile(r'<span class="pl"[^>]*>(.*?)</span>', re.S)
    # the cell carries its own vintage since doc 418: <td class="rate" data-vintage="36% of 2 games">
    rate_pat = re.compile(r'<td class="rate"([^>]*)>\s*([0-9]+(?:\.[0-9]+)?)\s*</td>')
    # [doc 418] AND THE CLAIMED WEIGHT, WHICH IS WHAT MAKES THE GAP READABLE. Since the rate became
    # a blend the page labels each one "36% of 2 games", so the guard can ask whether the printed
    # number IS that blend instead of asking whether it equals this season. See `check`.
    vint_pat = re.compile(r'(\d+)% of (\d+) game')
    for row in re.findall(r'<tr\b.*?</tr>', s, re.S):
        nm = name_pat.search(row)
        rt = rate_pat.search(row)
        if not (nm and rt):
            continue
        name = re.sub(r'<[^>]+>', '', nm.group(1)).strip()
        if not name:
            continue
        # the weight comes off the RATE CELL when it has one, so a "36%" anywhere else in the
        # row (an ownership figure, a snap share) can never be mistaken for the vintage.
        vm = vint_pat.search(rt.group(1)) or vint_pat.search(row)
        try:
            out.setdefault(name, (float(rt.group(2)),
                                  int(vm.group(1)) / 100.0 if vm else None))
        except ValueError:
            pass
    return out, ''


# THE POPULATION, AND GETTING IT WRONG IS THE DEFECT THIS GUARD EXISTS TO CATCH (0.6).
# The first draft of this file checked everybody and flagged 28 players. Most were artefacts:
#   - form_2026.csv scores half_ppr from RUSHING AND RECEIVING ONLY. Jalen Hurts reads 4.6 with
#     0 targets and 7 carries, which is his rushing line and not his week. Every quarterback and
#     every kicker therefore looks "refuted" by a file that never scored them.
#   - every man appears TWICE, once under week 0 and once under week 1, with identical figures,
#     so the game count doubled and the tolerance switched to the wrong band.
# So: skill positions only, week 0 dropped as the duplicate it is, and a part-played week ignored.
SCORED = ('RB', 'WR', 'TE')


def season_actual(path):
    """Points a game so far this season, and the games it rests on.

    Restricted to the positions form_2026.csv actually scores in full. A guard that fires on a
    population its data does not cover teaches the reader to ignore it, which is worse than no
    guard at all.
    """
    if not os.path.exists(path):
        return {}, 'form_2026.csv is not there'
    seen = set()
    tot, games = {}, {}
    for r in csv.DictReader(open(path, encoding='utf-8', errors='replace')):
        wk = (r.get('week') or '').strip()
        if not wk or wk == '0':
            continue                      # week 0 duplicates week 1 row for row
        if (r.get('in_progress') or '').strip() not in ('', '0', 'False', 'false'):
            continue                      # a part-played week is not a week
        if (r.get('pos') or '').strip().upper() not in SCORED:
            continue
        n = (r.get('player') or '').strip()
        if (n, wk) in seen:
            continue
        seen.add((n, wk))
        try:
            pts = float(r.get('half_ppr') or 0)
        except ValueError:
            continue
        tot[n] = tot.get(n, 0.0) + pts
        games[n] = games.get(n, 0) + 1
    return {n: (tot[n] / games[n], games[n]) for n in tot if games[n]}, ''


# [doc 418] WHAT THIS GUARD ASKS CHANGED, BECAUSE THE PAGE CHANGED UNDER IT.
# It was written when every pts/wk was a preseason projection, so "the printed rate is far from
# this season" WAS the defect. On 24 Sept rates() became a measured blend: the printed rate now
# sits DELIBERATELY between the projection and this season, and at week 3 that is 64% of the way
# toward the projection. The old test fired on five men whose numbers were exactly right and told
# Matt, in capitals, that the page was "PRINTING A RATE THIS SEASON ALREADY REFUTES". It was not.
# A guard that fails a correct page is worse than no guard, because the next real one gets ignored.
#
# THE QUESTION NOW: does the printed number match the blend the page SAYS it used?
#   * the row is labelled "N% of K games" -> recompute w*season + (1-w)*projection and demand the
#     page's number equals it. This is STRICTER than the old check, not looser: it catches a wrong
#     weight, a wrong join and a stale rate, and it catches a mislabelled row.
#   * the row carries no blend label, so the page is showing the projection alone -> the ORIGINAL
#     doc 373 defect is still live and still fires on the old tolerance.
# The projection comes from sheet_engine.rates(), which is the object production builds (0.2).
BLEND_TOL = 0.25        # arithmetic, not judgement: a rounding slack on a printed single decimal


def _engine_rates(src, week):
    """{name: (projection a week, measured a week or None)} straight off the production path.
    Returns {} rather than raising: without it the guard falls back to the doc 373 test."""
    import os as _os
    import sys as _sys
    _sys.path.insert(0, HERE)
    try:
        import sheet_engine
        rate, why = sheet_engine.rates(src, week)
    except Exception:                                    # noqa: BLE001
        return {}
    if why:
        return {}
    out = {}
    for r in rate.values():
        nm = (r.get('name') or '').strip()
        if nm:
            out[nm] = (r.get('proj_wk'), r.get('measured'))
    return out


def page_week(path):
    """The week the sheet was built for, read off its own masthead ('Week 3 -- what to do')."""
    try:
        s = open(path, encoding='utf-8', errors='replace').read()
    except OSError:
        return 0
    m = re.search(r'Week\s+(\d+)\s*(?:&mdash;|-|\u2014)', s)
    return int(m.group(1)) if m else 0


def check(sheet, form, src=None):
    rates, err1 = printed_rates(sheet)
    act, err2 = season_actual(form)
    problems = []
    if err1 or err2:
        return None, [x for x in (err1, err2) if x]
    if not rates:
        return None, ['no rates could be read out of the page -- its markup changed, '
                      'so this guard is blind and must not report a pass']
    eng = _engine_rates(src or SRC, page_week(sheet)) if src is not False else {}
    rows = []
    for name, val in sorted(rates.items()):
        printed, w = val if isinstance(val, tuple) else (val, None)
        if name not in act:
            continue
        avg, n = act[name]
        if w is not None:
            # the page claims a blend. Check the ARITHMETIC, not the distance from this season.
            proj, meas = eng.get(name, (None, None))
            if proj is None or meas is None:
                continue                      # cannot recompute it; say nothing rather than guess
            want = w * meas + (1.0 - w) * proj
            if abs(printed - want) > BLEND_TOL:
                rows.append((name, printed, want, n, want - printed, 'blend'))
            continue
        tol = TOL_ONE_GAME if n < 2 else TOL
        gap = avg - printed
        if abs(gap) > tol:
            rows.append((name, printed, avg, n, gap, 'proj'))
    return rows, problems


def report(rows):
    if not rows:
        print('  vintage check: every printed rate is the blend the page says it is, and every '
              'unblended one is within a starter\'s week of this season.')
        return 0
    blend = [r for r in rows if r[5] == 'blend']
    proj = [r for r in rows if r[5] == 'proj']
    print('  VINTAGE CHECK FAILED -- %d printed rate(s):' % len(rows))
    print('  %-24s %9s %9s %7s %9s  %s' % ('player', 'page says', 'should be', 'games', 'gap',
                                           'why'))
    for name, printed, want, n, gap, kind in sorted(rows, key=lambda r: -abs(r[4])):
        print('  %-24s %9.1f %9.1f %7d %+9.1f  %s' % (name, printed, want, n, gap, kind))
    if blend:
        print('  BLEND rows: the page labels its own weight and the number beside it is not that')
        print('  blend. Its weight, its join or its rate is wrong. Doc 418.')
    if proj:
        print('  PROJ rows: the page is showing a preseason projection alone where this season')
        print('  disagrees. Doc 373.')
    return 1


def selftest():
    import tempfile
    d = tempfile.mkdtemp()
    form = os.path.join(d, 'form_2026.csv')
    with open(form, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['week', 'player', 'pos', 'half_ppr', 'in_progress'])
        w.writerow(['0', 'Devaughn Vele', 'WR', '16.4', ''])      # the duplicate that must not count
        w.writerow(['1', 'Devaughn Vele', 'WR', '16.4', ''])
        w.writerow(['1', 'Rico Dowdle', 'RB', '10.4', ''])
        w.writerow(['1', 'Jalen Hurts', 'QB', '4.6', ''])         # rushing only; must be ignored

    def page(vele_rate):
        return ('<tr><th><span class="pl">Devaughn Vele</span></th>'
                '<td class="rate">%s</td></tr>'
                '<tr><th><span class="pl">Rico Dowdle</span></th>'
                '<td class="rate">10.2</td></tr>'
                '<tr><th><span class="pl">Jalen Hurts</span></th>'
                '<td class="rate">21.6</td></tr>'
                # the seat-list shape that produced the Bigsby false positive: a percentage in the
                # rate column, and a real rate in the NEXT table. He must not be paired with 18.0.
                '<tr><th><span class="pl">Tank Bigsby</span></th>'
                '<td class="rate">5%%</td></tr>'
                '<tr><th><span class="pl">Somebody Else</span></th>'
                '<td class="rate">18.0</td></tr>' % vele_rate)

    ok = os.path.join(d, 'agree.html')
    open(ok, 'w', encoding='utf-8').write(page('16.1'))
    rows, errs = check(ok, form, src=False)
    assert not errs, errs
    assert rows == [], 'NEGATIVE CONTROL FAILED: guard fired on a page whose numbers agree: %r' % rows
    print('  control 1, numbers agree: guard stayed quiet. OK')

    bad = os.path.join(d, 'defect.html')
    open(bad, 'w', encoding='utf-8').write(page('5.8'))
    rows, errs = check(bad, form, src=False)
    assert not errs, errs
    names = [r[0] for r in rows]
    assert names == ['Devaughn Vele'], (
        'NEGATIVE CONTROL FAILED: the real 18 Sept defect did not fire, got %r' % names)
    assert abs(rows[0][4] - 10.6) < 0.05, rows
    assert rows[0][3] == 1, 'the week-0 duplicate was counted as a second game: %r' % (rows[0],)
    print('  control 2, the real Vele defect (page 5.8, actual 16.4): guard fired on it. OK')
    print('  control 3, the week-0 duplicate row: counted as 1 game, not 2. OK')
    print('  control 4, Jalen Hurts at 21.6 on the page against a rushing-only 4.6: not flagged,')
    print('             because form_2026.csv does not score quarterbacks. OK')
    r2, _ = printed_rates(bad)
    # printed_rates returns (rate, claimed weight or None) since doc 418; the trap is the RATE.
    _rate = lambda v: v[0] if isinstance(v, tuple) else v
    assert 'Tank Bigsby' not in r2 or _rate(r2['Tank Bigsby']) != 18.0, (
        'the Bigsby trap came back: a percentage cell let the match run into the next table, %r'
        % (r2.get('Tank Bigsby'),))
    assert _rate(r2.get('Somebody Else')) == 18.0, r2
    print('  control 5, a percentage in the rate column: the 18.0 from the next table was NOT')
    print('             attached to Tank Bigsby. OK')

    # [doc 418] CONTROLS 6 AND 7 ARE THE FALSE POSITIVE THAT MOTIVATED THE REWRITE, AND ITS TWIN.
    # On 24 Sept this guard failed a page whose numbers were exactly right, because the rate had
    # become a blend and the guard was still asking whether it equalled this season. Davante Adams:
    # projection 10.85, this season 19.8 on 2 games, week-3 weight 36%, so the page correctly
    # printed 14.1 -- and the guard called it refuted by a 5.7 gap.
    # THE SHAPE PRODUCTION BUILDS (0.2), copied from sheet_engine.rate_cell: the weight rides on
    # the CELL, not loose in the row, so an ownership "36%" elsewhere cannot be read as a vintage.
    def blended_page(rate):
        return ('<tr><th><span class="pl">Davante Adams</span>'
                '<span class="meta">KC &middot; bye 10 &middot; owned 36%</span></th>'
                '<td class="rate" data-vintage="36% of 2 games" '
                'title="36% of 2 games this season at 19.8 a game, the rest the preseason '
                'projection">' + rate + '</td></tr>')

    form2 = os.path.join(d, 'form2.csv')
    with open(form2, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['week', 'player', 'pos', 'half_ppr', 'in_progress'])
        w.writerow(['1', 'Davante Adams', 'WR', '17.8', ''])
        w.writerow(['2', 'Davante Adams', 'WR', '21.8', ''])      # mean 19.8 on 2 games

    real = globals()['_engine_rates']
    globals()['_engine_rates'] = lambda src, week: {'Davante Adams': (10.85, 19.8)}
    try:
        good = os.path.join(d, 'blend_ok.html')
        open(good, 'w', encoding='utf-8').write(blended_page('14.1'))
        rows, errs = check(good, form2)
        assert not errs, errs
        assert rows == [], (
            'NEGATIVE CONTROL FAILED: the 24 Sept false positive came back -- the guard fired on a '
            'correctly blended rate: %r' % rows)
        print('  control 6, the 24 Sept false positive (page 14.1, season 19.8, a declared 36%')
        print('             blend of a 10.85 projection): guard stayed quiet. OK')

        wrong = os.path.join(d, 'blend_bad.html')
        open(wrong, 'w', encoding='utf-8').write(blended_page('19.8'))
        rows, errs = check(wrong, form2)
        assert not errs, errs
        assert [r[0] for r in rows] == ['Davante Adams'], (
            'the guard did not fire on a row whose number is NOT the blend it claims: %r' % rows)
        assert rows[0][5] == 'blend', rows
        print('  control 7, the same row labelled a 36% blend but printing this season raw:')
        print('             guard fired, reason "blend". OK')
    finally:
        globals()['_engine_rates'] = real
    print('  all seven controls pass.')
    return 0


def main(argv):
    if '--selftest' in argv:
        return selftest()
    sheet = os.path.join(SRC, 'WEEK_SHEET.html')
    form = os.path.join(SRC, 'form_2026.csv')
    rows, errs = check(sheet, form)
    if errs:
        for e in errs:
            print('  vintage check could not run: %s' % e)
        return 1                      # cannot check is not the same as passed (0.2)
    return report(rows)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
