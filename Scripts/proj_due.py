#!/usr/bin/env python3
r"""proj_due.py -- is ESPN's projection pull due, what did the last one change, and tidy the old ones (docs 451, 454)

    py proj_due.py              exit 0 when the newest Source\espn_projections_2026_*.csv is more than
                                MAX_DAYS old or there is none; exit 1 when it is fresh. Prints which.
    py proj_due.py --report     the newest two pulls compared: how many season projections moved, and the
                                largest moves. Run after a pull; over a season this is ESPN's cadence, measured.
    py proj_due.py --prune      MOVE every pull older than the newest KEEP into _archive\projections\ (the CSV
                                and its raw JSON). Never deletes. Prints each move.
    py proj_due.py --selftest   the gate (fresh, stale, empty), the prune (five pulls, two move) and the report.

WHY THIS EXISTS. ff.bat pulled the projection on the TUE task only (doc 439: a pull is about 5.6 MB, the
raw JSON most of it, and ESPN was assumed to re-project once a week). On 29 Sept the 06:00 Tuesday task
ran the batch file as it stood the night before, which had no projection step, so the sheet went into
the claim week on a pull from Thursday 24 Sept, made before week 3 was played. Doc 454: the once-a-week
assumption was never measured and the cost of a pull is a few seconds and 5.6 MB, so the gate is now
HALF A DAY (one pull a day at most, on whichever run comes first), --report shows what each pull moved,
and --prune keeps Source\ to the newest KEEP pulls by moving the rest to the archive.
Standard library only; the path is resolved against this file, never the shell.
"""
import glob
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'Source')
PATTERN = 'espn_projections_2026_*.csv'
MAX_DAYS = 0.5          # doc 454: at most one pull a day, on whichever run comes first
KEEP = 3                # pulls kept in Source\; older ones move to _archive\projections\
ARCH = os.path.join(os.path.dirname(HERE), '_archive', 'projections')
RAW = 'espn_raw_2026_*.json'
PRUNE_FROM = '20260910'  # only in-season pulls are pruned: the draft-era pulls (20 Aug to 7 Sept) are read by name
                         # by depth_map.py (live_draft\adp_vintage.txt) and stay where they are


def due(src=SRC, now=None):
    """(is_due, reason). Age is the file's modification time, which is when the pull landed."""
    now = time.time() if now is None else now
    files = sorted(glob.glob(os.path.join(src, PATTERN)))
    if not files:
        return True, 'no %s in %s: the pull is due' % (PATTERN, src)
    newest = max(files, key=os.path.getmtime)
    age = (now - os.path.getmtime(newest)) / 86400.0
    if age > MAX_DAYS:
        return True, '%s is %.1f days old (limit %.1f): the pull is due' % (os.path.basename(newest), age, MAX_DAYS)
    return False, '%s is %.1f days old (limit %.1f): fresh, not pulled' % (os.path.basename(newest), age, MAX_DAYS)


def _stamp(name):
    """The pull time in the file name, 'YYYYMMDD_HHMM', or '' (the sort key: the name, not the mtime,
    because a copy or a sync can touch mtime and the name is what the pull wrote)."""
    import re
    m = re.search(r'_(\d{8}_\d{4})\.(?:csv|json)$', name)
    return m.group(1) if m else ''


def prune(src=SRC, arch=ARCH, keep=KEEP):
    """[(from, to)] moved. The newest `keep` CSV pulls stay, with their raw JSON; everything older
    of either kind moves. A file that already exists in the archive is not overwritten: it is skipped
    and named."""
    import shutil
    csvs = sorted((f for f in glob.glob(os.path.join(src, PATTERN)) if _stamp(f) >= PRUNE_FROM), key=_stamp)
    stay = {_stamp(f) for f in csvs[-keep:]} if keep > 0 else set()
    moved, skipped = [], []
    for f in sorted(glob.glob(os.path.join(src, PATTERN)) + glob.glob(os.path.join(src, RAW))):
        st = _stamp(f)
        if not st or st in stay or st < PRUNE_FROM:
            continue
        os.makedirs(arch, exist_ok=True)
        to = os.path.join(arch, os.path.basename(f))
        if os.path.exists(to):
            skipped.append(f)
            continue
        shutil.move(f, to)
        moved.append((f, to))
    return moved, skipped


def report(src=SRC):
    """Compare the newest two pulls: (n both, n moved, biggest moves) or (0, 0, []) with fewer than two."""
    import csv
    files = sorted((f for f in glob.glob(os.path.join(src, PATTERN)) if _stamp(f)), key=_stamp)
    if len(files) < 2:
        return None
    def load(p):
        out = {}
        with open(p, newline='', encoding='utf-8-sig') as fh:
            for r in csv.DictReader(fh):
                try:
                    out[str(r.get('espn_id')).strip()] = (r.get('Player') or '?', r.get('pos') or '', float(r.get('proj_2026') or 'nan'))
                except ValueError:
                    pass
        return out
    a, b = load(files[-2]), load(files[-1])
    both = [k for k in b if k in a and a[k][2] == a[k][2] and b[k][2] == b[k][2]]
    moves = sorted(((b[k][2] - a[k][2], b[k][0], b[k][1], a[k][2], b[k][2]) for k in both), key=lambda t: -abs(t[0]))
    changed = [m for m in moves if abs(m[0]) > 0.05]
    return os.path.basename(files[-2]), os.path.basename(files[-1]), len(both), len(changed), changed[:5]


def selftest():
    import tempfile
    ok = True
    with tempfile.TemporaryDirectory() as d:
        r0, why0 = due(d)
        print('  %-4s empty folder is due: %s' % ('ok' if r0 else 'BAD', why0))
        ok &= r0
        p = os.path.join(d, 'espn_projections_2026_20260924_0740.csv')
        open(p, 'w').write('x')
        stale = time.time() - 6 * 86400
        os.utime(p, (stale, stale))
        r1, why1 = due(d)
        print('  %-4s a six-day-old pull is due: %s' % ('ok' if r1 else 'BAD', why1))
        ok &= r1
        fresh = time.time() - 0.2 * 86400
        os.utime(p, (fresh, fresh))
        r2, why2 = due(d)
        print('  %-4s a five-hour-old pull is not: %s' % ('ok' if not r2 else 'BAD', why2))
        ok &= not r2
        # the prune: five pulls with raw files, the newest three stay, the two oldest move, a stray file stays
        src, arch = os.path.join(d, 'Source'), os.path.join(d, '_archive', 'projections')
        os.makedirs(src)
        stamps = ['20260924_0740', '20260930_0730', '20261001_0730', '20261002_0730', '20261003_0730']
        for st in stamps:
            open(os.path.join(src, 'espn_projections_2026_%s.csv' % st), 'w').write('Player,espn_id,pos,proj_2026\nA,1,RB,%s\n' % st[6:8])
            open(os.path.join(src, 'espn_raw_2026_%s.json' % st), 'w').write('{}')
        open(os.path.join(src, 'ESPN_projections_in_my_League.csv'), 'w').write('x')
        open(os.path.join(src, 'espn_projections_2026_20260823.csv'), 'w').write('x')   # draft-era, read by name, must stay
        moved, skipped = prune(src, arch, 3)
        left = sorted(os.path.basename(f) for f in glob.glob(os.path.join(src, 'espn_*')))
        r3 = (len(moved) == 4 and not skipped and len(left) == 7 and '20260823' in ''.join(left)
              and all(st in ''.join(left) for st in stamps[2:]) and not any(st in ''.join(left) for st in stamps[:2])
              and os.path.exists(os.path.join(src, 'ESPN_projections_in_my_League.csv')))
        print('  %-4s prune keeps the newest three in-season pulls (six files), moves four, leaves the league file and the draft-era pull: moved %d, left %s'
              % ('ok' if r3 else 'BAD', len(moved), left))
        ok &= r3
        moved2, _ = prune(src, arch, 3)
        r4 = not moved2
        print('  %-4s a second prune moves nothing' % ('ok' if r4 else 'BAD'))
        ok &= r4
        rep = report(src)
        r5 = rep is not None and rep[2] == 1 and rep[3] == 1
        print('  %-4s the report compares the newest two pulls: %s' % ('ok' if r5 else 'BAD', rep))
        ok &= r5
    print('selftest: %s' % ('all six controls behaved' if ok else 'FAILED'))
    return 0 if ok else 1


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if '--selftest' in argv:
        return selftest()
    if '--report' in argv or '--prune' in argv:
        rc = 0
        if '--report' in argv:
            rep = report()
            if rep is None:
                print('proj_due --report: fewer than two pulls in Source, nothing to compare')
            else:
                a, b, n, k, top = rep
                print('proj_due --report: %s -> %s: %d players in both, %d season projections moved' % (a, b, n, k))
                for dlt, nm, pos, x, y in top:
                    print('    %-24s %-4s %7.1f -> %7.1f (%+.1f)' % (nm, pos, x, y, dlt))
        if '--prune' in argv:
            moved, skipped = prune()
            for f, t in moved:
                print('proj_due --prune: moved %s -> %s' % (os.path.basename(f), t))
            for f in skipped:
                print('proj_due --prune: NOT moved, already in the archive: %s' % os.path.basename(f))
            if not moved and not skipped:
                print('proj_due --prune: nothing older than the newest %d pulls' % KEEP)
        return rc
    is_due, why = due()
    print('proj_due: ' + why)
    return 0 if is_due else 1


if __name__ == '__main__':
    sys.exit(main())
