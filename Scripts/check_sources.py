"""check_sources.py -- test what we BELIEVE about outside data against the data itself.

WHY THIS EXISTS. Matt, 24 Sept: *"how are we still at the stage of 'pulling the wrong numbers'.
that's what the red team process is meant to solve for"*. He is right, and the honest answer is
that the red team could not have caught any of that day's errors. Steps 1 to 5 of 0.5(c) are
internal-consistency checks: they compare a file against another file. Every error that day passed
that bar perfectly, because every file agreed. What none of them tested was whether a FIELD FROM
AN OUTSIDE SYSTEM means what this project assumes it means.

  * `proj_2026` was read as a FULL-SEASON total for three weeks. It is REST-OF-SEASON. Every file
    believed the same wrong thing, consistently, so nothing disagreed (doc 419).
  * `MY_ROSTER.csv` said Tre Tucker was owned while `WIRE_*.csv` said he was free. Two files DID
    disagree and nothing compared them, so the page printed "replaced by Tre Tucker" (doc 420).
  * this league's feed had only ever written ACTIVE and QUESTIONABLE into `STATUS_LOG.csv`, so the
    string ESPN sends for Out was a guess until the free-agent pool was read (doc 417).

Each check below states a BELIEF in one sentence and then tries to break it. A belief that cannot
be tested with the files on hand says so and is skipped, rather than passing quietly (0.2: cannot
check is not the same as passed).

    py check_sources.py              check everything, exit 1 on a broken belief
    py check_sources.py --selftest   run the negative controls and exit

THE CONTROLS RUN FIRST and each reproduces the real defect it exists for. Standard library only,
so it runs anywhere (doc 144), and every path resolves against this file rather than the shell.
"""
import csv
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', 'Source'))

# Every injury string this project has ever seen from ESPN, across the roster read and the pool.
# A new one is not an error by itself -- it is a thing nobody has checked, which is what this
# guard exists to surface before it silently changes a decision (the IR slot takes only two of
# these, so an unrecognised string is treated as ineligible and a park is refused).
KNOWN_STATUS = {'ACTIVE', 'QUESTIONABLE', 'DOUBTFUL', 'OUT', 'INJURY_RESERVE',
                'INJURED_RESERVE', 'IR', 'SUSPENSION', 'DAY_TO_DAY', 'PROBABLE', 'NORMAL'}

PULL_RX = re.compile(r'espn_projections_2026_(\d{8})_(\d{4})\.csv$')


def _f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def rows(path):
    if not os.path.exists(path):
        return None
    with open(path, newline='', encoding='utf-8-sig', errors='replace') as fh:
        return list(csv.DictReader(fh))


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    return None if not n else (xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2.0)


# --------------------------------------------------------------------- the beliefs --
def belief_projection_is_rest_of_season(src):
    """BELIEF: `proj_2026` is what ESPN expects FROM HERE, so it shrinks as the season runs and
    (projection + points already banked) stays about constant between two pulls.

    This is the one that was wrong for three weeks and cost about 11% on every rate on the page.
    Needs two pulls; with one it reports SKIPPED rather than passing."""
    pulls = sorted(glob.glob(os.path.join(src, 'espn_projections_2026_*.csv')))
    if len(pulls) < 2:
        return ('SKIP', 'only %d projection pull on the drive; this needs two' % len(pulls))
    old, new = rows(pulls[-2]), rows(pulls[-1])
    if not old or not new:
        return ('SKIP', 'a projection pull would not read')
    o = {(r.get('Player') or '').strip(): r for r in old}
    # THE INVARIANT, and it is exact rather than a band: if the projection is what is LEFT, then
    # between two pulls it must fall by however many points the man banked in between.
    #     (old projection - new projection) == (new actual - old actual)
    # A FULL-season total stays FLAT while the actual grows, so the two sides diverge immediately.
    # That is the doc 419 defect, and this is the sentence that would have caught it in week 2.
    gaps, total = [], 0
    for r in new:
        nm = (r.get('Player') or '').strip()
        if nm not in o or (r.get('pos') or '').upper() not in ('RB', 'WR', 'TE'):
            continue
        pn, po = _f(r.get('proj_2026')), _f(o[nm].get('proj_2026'))
        an, ao = _f(r.get('actual_2026')) or 0.0, _f(o[nm].get('actual_2026')) or 0.0
        if pn is None or po is None or po < 40:
            continue
        banked = an - ao
        if banked < 1.0:                      # he did not play; the projection has nothing to shed
            continue
        total += 1
        gaps.append((po - pn) - banked)
    if total < 30:
        return ('SKIP', 'only %d players banked points between the two pulls' % total)
    med = median(gaps)
    scale = median([abs(g) for g in gaps]) or 1.0
    if med is None or abs(med) > 12.0:
        return ('FAIL', 'the projection fell by %.1f points MORE than each man actually banked '
                        '(median, n=%d). A rest-of-season total sheds exactly what was scored; a '
                        'FULL-season total sheds nothing. sheet_engine.proj_games() is dividing by '
                        'the wrong number' % (med, total))
    return ('OK', 'holds on %d players: the projection sheds what they bank, median gap %.1f '
                  '(typical move %.1f)' % (total, med, scale))


def belief_owned_and_free_are_disjoint(src):
    """BELIEF: a man cannot be on Matt's roster AND in the free-agent pool.

    Both files are written by the same run of wire.py, so they should never disagree. When they
    did, the page offered "Tre Tucker, replaced by Tre Tucker"."""
    mine = rows(os.path.join(src, 'MY_ROSTER.csv'))
    wires = sorted(glob.glob(os.path.join(src, 'WIRE_*.csv')))
    if mine is None or not wires:
        return ('SKIP', 'MY_ROSTER.csv or WIRE_*.csv is not on the drive')
    free = rows(wires[-1]) or []
    owned = {(r.get('player') or '').strip() for r in mine if (r.get('player') or '').strip()}
    both = sorted(owned & {(r.get('player') or '').strip() for r in free})
    if both:
        return ('FAIL', '%d man/men are owned AND free at once: %s. %s is older than the roster '
                        'read, so any "replaced by" it feeds is suspect'
                        % (len(both), ', '.join(both), os.path.basename(wires[-1])))
    return ('OK', 'no overlap between %d owned and %d free' % (len(owned), len(free)))


def belief_status_strings_are_known(src):
    """BELIEF: every injury string ESPN sends is one this project has already reasoned about.

    The IR slot accepts exactly two of them. An unrecognised string is treated as ineligible, so a
    new spelling silently refuses a legal park rather than erroring."""
    seen, where = {}, {}
    for path in ([os.path.join(src, 'MY_ROSTER.csv')]
                 + sorted(glob.glob(os.path.join(src, 'WIRE_*.csv')))[-1:]
                 + [os.path.join(src, 'STATUS_LOG.csv')]):
        for r in (rows(path) or []):
            st = (r.get('status') or '').strip().upper().replace(' ', '_')
            if st:
                seen[st] = seen.get(st, 0) + 1
                where.setdefault(st, os.path.basename(path))
    if not seen:
        return ('SKIP', 'no file carrying a status column')
    new = {k: v for k, v in seen.items() if k not in KNOWN_STATUS}
    if new:
        return ('FAIL', 'ESPN sent %d status string(s) nobody here has reasoned about: %s. Check '
                        'whether the IR slot accepts any of them before the next claim'
                        % (len(new), ', '.join(f'{k} ({v} rows, {where[k]})' for k, v in new.items())))
    return ('OK', '%d distinct strings, all known: %s' % (len(seen), ', '.join(sorted(seen))))


def belief_roster_joins_the_pull(src):
    """BELIEF: every man on the roster can be found in the projection pull by espn_id.

    A miss is not fatal -- rates() drops men ESPN prices at zero -- but it is the thing doc 281
    caught the hard way, where an unpriced man vanished from the page AND took his roster seat
    with him."""
    mine = rows(os.path.join(src, 'MY_ROSTER.csv'))
    pulls = sorted(glob.glob(os.path.join(src, 'espn_projections_2026_*.csv')))
    if mine is None or not pulls:
        return ('SKIP', 'MY_ROSTER.csv or a projection pull is missing')
    ids = {(r.get('espn_id') or '').strip() for r in (rows(pulls[-1]) or [])}
    missing = [(r.get('player') or '?') for r in mine
               if (r.get('espn_id') or '').strip() and (r.get('espn_id') or '').strip() not in ids]
    if missing:
        return ('WARN', '%d of your men are not in the pull by id: %s. They are priced at nothing '
                        'and still hold a seat' % (len(missing), ', '.join(missing)))
    return ('OK', 'all %d of your men join the pull by id' % len(mine))


CHECKS = [
    ('the projection is rest-of-season', belief_projection_is_rest_of_season),
    ('owned and free are disjoint', belief_owned_and_free_are_disjoint),
    ('every status string is known', belief_status_strings_are_known),
    ('the roster joins the pull by id', belief_roster_joins_the_pull),
]


def run(src):
    bad = 0
    print('  what we believe about ESPN\'s data, tested against the data:')
    for name, fn in CHECKS:
        try:
            state, msg = fn(src)
        except Exception as exc:                                   # noqa: BLE001
            state, msg = 'FAIL', f'the check itself raised {type(exc).__name__}: {exc}'
        print('  %-6s %-34s %s' % (state, name, msg))
        if state == 'FAIL':
            bad += 1
    if bad:
        print('  %d BELIEF(S) BROKEN. A number computed from one of these is suspect until it is '
              'checked by hand.' % bad)
    return 1 if bad else 0


def selftest():
    """Each control reproduces the real defect the check exists for, and must FIRE on it."""
    import tempfile
    d = tempfile.mkdtemp()

    def w(name, header, rws):
        with open(os.path.join(d, name), 'w', encoding='utf-8', newline='') as fh:
            cw = csv.writer(fh)
            cw.writerow(header)
            cw.writerows(rws)

    # --- control 1: the doc 419 defect. A projection that GREW between pulls. ---
    hdr = ['Player', 'espn_id', 'pos', 'status', 'proj_2026', 'actual_2026']
    old = [[f'P{i}', str(i), 'WR', 'ACTIVE', '200', '0'] for i in range(40)]
    w('espn_projections_2026_20260907_1200.csv', hdr, old)
    # a FULL-season total: the projection does not move while 20 points are banked
    flat = [[f'P{i}', str(i), 'WR', 'ACTIVE', '200', '20'] for i in range(40)]
    w('espn_projections_2026_20260924_1200.csv', hdr, flat)
    state, msg = belief_projection_is_rest_of_season(d)
    assert state == 'FAIL' and 'FULL-season' in msg, (state, msg)
    print('  control 1, a full-season projection (doc 419, 11% low for three weeks): FIRED. OK')

    # rest-of-season: it sheds exactly what was banked
    shrank = [[f'P{i}', str(i), 'WR', 'ACTIVE', '180', '20'] for i in range(40)]
    w('espn_projections_2026_20260924_1200.csv', hdr, shrank)
    state, msg = belief_projection_is_rest_of_season(d)
    assert state == 'OK', (state, msg)
    print('  control 2, a correct rest-of-season projection: stayed quiet. OK')

    # --- control 3: the doc 420 defect. Owned and free at once. ---
    w('MY_ROSTER.csv', ['espn_id', 'player', 'pos', 'status'],
      [['1', 'Tre Tucker', 'WR', 'ACTIVE'], ['2', 'Jalen Hurts', 'QB', 'ACTIVE']])
    w('WIRE_20260923.csv', ['espn_id', 'player', 'status'],
      [['1', 'Tre Tucker', 'ACTIVE'], ['9', 'Somebody Free', 'ACTIVE']])
    state, msg = belief_owned_and_free_are_disjoint(d)
    assert state == 'FAIL' and 'Tre Tucker' in msg, (state, msg)
    print('  control 3, owned and free at once (doc 420, "replaced by himself"): FIRED. OK')

    w('WIRE_20260923.csv', ['espn_id', 'player', 'status'], [['9', 'Somebody Free', 'ACTIVE']])
    state, _ = belief_owned_and_free_are_disjoint(d)
    assert state == 'OK', state
    print('  control 4, disjoint lists: stayed quiet. OK')

    # --- control 5: an ESPN status string nobody has reasoned about. ---
    w('WIRE_20260923.csv', ['espn_id', 'player', 'status'], [['9', 'Somebody', 'FOOT_INJURY']])
    state, msg = belief_status_strings_are_known(d)
    assert state == 'FAIL' and 'FOOT_INJURY' in msg, (state, msg)
    print('  control 5, an unknown status string (doc 417, the IR slot silently refuses): FIRED. OK')

    w('WIRE_20260923.csv', ['espn_id', 'player', 'status'], [['9', 'Somebody', 'OUT']])
    state, _ = belief_status_strings_are_known(d)
    assert state == 'OK', state
    print('  control 6, only known strings: stayed quiet. OK')

    # --- control 7: a rostered man missing from the pull (doc 281). ---
    w('MY_ROSTER.csv', ['espn_id', 'player', 'pos', 'status'],
      [['999', 'Ghost Man', 'RB', 'OUT']])
    state, msg = belief_roster_joins_the_pull(d)
    assert state == 'WARN' and 'Ghost Man' in msg, (state, msg)
    print('  control 7, a rostered man absent from the pull (doc 281): FIRED. OK')

    print('  all seven controls pass.')
    return 0


if __name__ == '__main__':
    raise SystemExit(selftest() if '--selftest' in sys.argv else run(SRC))
