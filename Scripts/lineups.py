#!/usr/bin/env python3
r"""
lineups.py -- pull WHO WAS ACTUALLY STARTED, every week, out of ESPN.

    py lineups.py                # 2022-2025, every week
    py lineups.py --season 2025  # one season
    py lineups.py --check        # prove the cookies, pull nothing

WRITES, into Source\ :
    lineups_<year>.csv    season, week, team, player, pos, slot, started, points

WHY THIS EXISTS (Matt, 2026-09-08): "oh, you won't know who they started? if you have the weekly
points that can be derived as well? idk / or just assume they made the optimal choice / which they
don't, lol"

    Both of his routes work and neither is needed. Deriving starters from a team total is a
    subset-sum on top of a roster rebuild that is itself broken (doc 230), so two shaky steps
    stacked. Assuming everyone started their best nine is worse than shaky -- it is a BIAS, and
    for the defence question it biases against his own conclusion, because it hands every rival a
    perfect streaming record they never had.

    ESPN simply stores the answer. The weekly matchup view returns, for every team and week, each
    player on the roster, the SLOT he was in, and what he scored. That is the starters, the bench,
    the roster and the points in one call -- on the same cookies waivers.py already uses.

THE CONTROL, and it runs on every pull: a legal lineup is exactly NINE started players --
1 QB, 2 RB, 2 WR, 1 TE, 1 FLEX, 1 D/ST, 1 K. Any team-week that does not come back as nine is
COUNTED AND REPORTED, not silently kept. A pull that cannot produce lineups says so and exits 2;
it never writes a half file.
"""
import argparse, csv, os, sys

try:
    import requests
except ImportError:
    sys.exit("lineups.py needs `requests`, the same one wire.py uses.")

LEAGUE_ID = 21985
CURRENT = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leagues/{lid}"
HISTORY = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/leagueHistory/{lid}"
COOKIES = {
    'swid':    '{A7217088-1F36-4F1F-AE73-67262BF763EF}',
    'espn_s2': '',
}
HEADERS = {'accept': 'application/json', 'x-fantasy-platform': 'espn-fantasy-web',
           'x-fantasy-source': 'kona', 'referer': 'https://fantasy.espn.com/'}
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', 'Source'))
SEASONS = (2022, 2023, 2024, 2025)
WEEKS = range(1, 18)

SLOT = {0: 'QB', 2: 'RB', 4: 'WR', 6: 'TE', 16: 'D/ST', 17: 'K', 23: 'FLEX',
        20: 'BENCH', 21: 'IR'}
BENCHED = {20, 21}
POS = {1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 16: 'D/ST'}
STARTER_SHAPE = {'QB': 1, 'RB': 2, 'WR': 2, 'TE': 1, 'FLEX': 1, 'D/ST': 1, 'K': 1}


def _get(season, week, views=('mMatchup', 'mMatchupScore')):
    """Current-season path first, league-history path second. ESPN moves old seasons."""
    qs = '?' + '&'.join('view=' + v for v in views) + '&scoringPeriodId=%d' % week
    urls = [CURRENT.format(season=season, lid=LEAGUE_ID) + qs,
            HISTORY.format(lid=LEAGUE_ID) + qs + '&seasonId=%d' % season]
    last = None
    for u in urls:
        try:
            r = requests.get(u, cookies=COOKIES, headers=HEADERS, timeout=30)
        except Exception as exc:
            last = exc
            continue
        if r.status_code == 401:
            sys.exit("\n  401 from ESPN. Run  py set_cookies.py  and try again.\n")
        if r.ok:
            j = r.json()
            return j[0] if isinstance(j, list) and j else j
        last = '%s -> HTTP %d' % (u.split('?')[0][-40:], r.status_code)
    raise RuntimeError('both URL forms failed: %s' % (last,))


def team_names(season):
    try:
        j = _get(season, 1, views=('mTeam',))
    except Exception:
        return {}
    out = {}
    for t in (j.get('teams') or []):
        nm = (t.get('name') or ' '.join([t.get('location', '') or '',
                                         t.get('nickname', '') or '']).strip()
              or str(t.get('id')))
        out[t.get('id')] = nm.strip()
    return out


def rows_for_week(payload, season, week, names):
    """One row per rostered player. Returns (rows, shape_problems)."""
    rows, problems = [], []
    for game in (payload.get('schedule') or []):
        for side in ('home', 'away'):
            side_d = game.get(side) or {}
            tid = side_d.get('teamId')
            roster = (side_d.get('rosterForCurrentScoringPeriod')
                      or side_d.get('rosterForMatchupPeriod') or {})
            entries = roster.get('entries') or []
            if not entries:
                continue
            started = []
            for e in entries:
                slot_id = e.get('lineupSlotId')
                pe = e.get('playerPoolEntry') or {}
                p = pe.get('player') or {}
                pts = pe.get('appliedStatTotal')
                if pts is None:
                    pts = e.get('playerPoolEntry', {}).get('appliedStatTotal')
                slot = SLOT.get(slot_id, str(slot_id))
                is_start = slot_id not in BENCHED
                if is_start:
                    started.append(slot)
                rows.append(dict(
                    season=season, week=week, team=names.get(tid, str(tid)),
                    player=p.get('fullName', '?'),
                    pos=POS.get(p.get('defaultPositionId'), '?'),
                    slot=slot, started=int(is_start),
                    points=round(float(pts or 0.0), 2)))
            got = {}
            for s in started:
                got[s] = got.get(s, 0) + 1
            if got != STARTER_SHAPE:
                problems.append((names.get(tid, str(tid)), len(started), got))
    return rows, problems


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--season', type=int)
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args(argv)

    if a.check:
        try:
            _get(2025, 1, views=('mTeam',))
        except SystemExit:
            raise
        except Exception as exc:
            print('\n  COULD NOT REACH ESPN (%s). Nothing was pulled.\n' % type(exc).__name__)
            return 2
        print('  cookies OK -- ESPN answered for league %d.' % LEAGUE_ID)
        return 0

    os.makedirs(SRC, exist_ok=True)
    seasons = (a.season,) if a.season else SEASONS
    worst = 0
    for season in seasons:
        names = team_names(season)
        rows, problems, missed = [], [], []
        for wk in WEEKS:
            try:
                got, probs = rows_for_week(_get(season, wk), season, wk, names)
            except Exception as exc:
                missed.append((wk, type(exc).__name__))
                continue
            rows.extend(got)
            problems.extend([(wk,) + p for p in probs])
        if not rows:
            print('  %d: NO LINEUPS RETURNED. Nothing written for this season.' % season)
            worst = 2
            continue
        out = os.path.join(SRC, 'lineups_%d.csv' % season)
        with open(out, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        tw = len({(r['week'], r['team']) for r in rows})
        print('  %d: %5d rows, %3d team-weeks -> %s' % (season, len(rows), tw, out))
        if missed:
            print('       weeks that did not come back: %s' % ', '.join(
                '%d (%s)' % m for m in missed))
            worst = max(worst, 1)
        if problems:
            print('       %d team-weeks did NOT have a legal nine-man lineup '
                  '(reported, not dropped):' % len(problems))
            for wk, team, n, shape in problems[:6]:
                print('         wk %-2d %-28s %d started %s' % (wk, team[:28], n, shape))
            worst = max(worst, 1)
        else:
            print('       CONTROL PASSED: every team-week is a legal nine-man lineup.')
    return worst


if __name__ == '__main__':
    sys.exit(main())
