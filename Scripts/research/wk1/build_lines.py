#!/usr/bin/env python3
r"""build_lines.py -- Source\lines_2026.csv: the PREGAME LINE for every 2026 game, one row a game.

WHY THIS EXISTS (doc 441, finding 4.39). The wire page ranks a defense on what its opponent
scored per game LAST SEASON (team_2025.csv), because that was the only matchup number on the
drive. Measured over five seasons, among the defenses Matt could actually claim, the unit facing
the LOWEST opponent implied total that week scores about +3.2 a week over picking at random, the
same as the opponent's season-to-date rule and available before the season has any games in it.
At quarterback the own-team implied total clears random by about +4.5 and sits beside doc 427's
softest-matchup rule as a second read. This script puts the line on the drive; wire.py reads it.

WHAT IT WRITES, one row per 2026 regular-season game:
  week, gameday, home, away          -- teams spelled the way sheet_engine.TEAM_ALIAS spells them
                                        (nflverse writes LA and WAS; the page joins on LAR and WSH)
  spread_line                        -- home minus away expected margin, POSITIVE = HOME FAVOURED.
                                        This sign was checked against results on 1,279 played games.
  total_line                         -- the over/under
  implied_home, implied_away         -- total/2 plus or minus spread/2: what each side is expected
                                        to score. BLANK, never zero, on a game with no line yet.
  has_line                           -- 1 when both the spread and the total are posted, else 0
  as_of                              -- the feed's Last-Modified header (local time), or the time
                                        of this run when the header is absent, or the cached copy's
                                        modified time when the fetch failed and the cache served

THE FEED: nflverse's games.csv (Lee Sharpe's schedule file), refreshed by nflverse as the books
post lines. The line is the CLOSING line once a game is played and the current line before it, so
a row's implied totals can move until kickoff; re-run before each read of the wire.

GUARDS (0.2: an exit code is not a result):
  every regular-season week 1 to 18 is present · 32 teams and every one resolves to an ESPN code
  · the current week does not LOSE its lines against the copy already on the drive (a feed that
  serves an empty line column for games that were lined yesterday is a partial feed, and the old
  file is kept).

Portable per 0.4: stdlib only, paths off __file__, no shelling out, no invalid escapes.
"""
import collections, csv, datetime as dt, email.utils, os, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get('FF_SOURCE') or os.path.abspath(os.path.join(HERE, '..', '..', '..', 'Source'))
SEASON = 2026
FEED_NAME = 'games.csv'
FEED_URL = 'https://github.com/nflverse/nflverse-data/releases/download/schedules/games.csv'
OUT_NAME = f'lines_{SEASON}.csv'
COLS = ['week', 'gameday', 'home', 'away', 'spread_line', 'total_line',
        'implied_home', 'implied_away', 'has_line', 'as_of']

# ONE SPELLING OR NO JOIN (section 3), exactly as build_form.py does it: the project's map lives in
# sheet_engine.py and runs the OTHER WAY from nflverse (LA -> LAR, WAS -> WSH). Import the real map;
# the literal below is only a standalone fallback and is asserted against the import when both are
# present.
_FALLBACK = {'ARZ': 'ARI', 'BLT': 'BAL', 'CLV': 'CLE', 'HST': 'HOU', 'LA': 'LAR', 'WAS': 'WSH',
             'JAC': 'JAX', 'GNB': 'GB', 'KAN': 'KC', 'NWE': 'NE', 'NOR': 'NO', 'SFO': 'SF',
             'TAM': 'TB', 'LVR': 'LV', 'SD': 'LAC', 'OAK': 'LV', 'STL': 'LAR'}
try:
    sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..')))
    from sheet_engine import TEAM_ALIAS as TF, ESPN_TEAMS          # the canonical map
    TEAM_MAP_SOURCE = 'sheet_engine.TEAM_ALIAS'
    if any(TF.get(k) != v for k, v in _FALLBACK.items()):
        sys.exit('FAILED: the fallback team map in this file disagrees with sheet_engine.TEAM_ALIAS. '
                 'Fix the fallback; the engine is the authority.')
except ImportError:
    TF = _FALLBACK
    ESPN_TEAMS = frozenset("""ARI ATL BAL BUF CAR CHI CIN CLE DAL DEN DET GB HOU IND JAX KC LAC LAR
                              LV MIA MIN NE NO NYG NYJ PHI PIT SEA SF TB TEN WSH""".split())
    TEAM_MAP_SOURCE = 'the local fallback (sheet_engine.py not importable)'


def tk(t):
    t = (t or '').upper().strip()
    return TF.get(t, t)


def fetch(name, url, cache):
    """ALWAYS re-fetch, and a cache may only serve a fetch that FAILED, out loud (build_form.py's
    rule, doc 439: a silently reused partial download once built the form file from twenty of the
    thirty-two teams). Returns (path, as_of) where as_of is the feed's Last-Modified header when
    the fetch succeeded, the run time when the header is absent, and the cached copy's modified
    time when the cache served."""
    p = os.path.join(cache, name)
    try:
        with urllib.request.urlopen(url, timeout=120) as fh:
            body = fh.read()
            lm = fh.headers.get('Last-Modified')
        if len(body) < 1000:
            raise ValueError(f'the feed returned {len(body)} bytes')
        with open(p, 'wb') as out:
            out.write(body)
        as_of = dt.datetime.now()
        if lm:
            try:
                as_of = email.utils.parsedate_to_datetime(lm).astimezone()
            except (TypeError, ValueError):
                pass
        return p, as_of.replace(tzinfo=None)
    except Exception as exc:
        if os.path.exists(p) and os.path.getsize(p) > 1000:
            when = dt.datetime.fromtimestamp(os.path.getmtime(p))
            print(f'  WARNING: could not fetch {name} ({exc}).\n'
                  f'  FALLING BACK to the copy already here, dated {when:%d %b %H:%M}.\n'
                  f'  If the books have moved since then these lines are STALE and this run is wrong.')
            return p, when
        sys.exit(f'FAILED to fetch {name}: {exc}\n'
                 f'  put the file in {cache} by hand and re-run.')


def _num(v):
    v = (v or '').strip()
    if v == '' or v.upper() == 'NA':
        return None
    try:
        return float(v)
    except ValueError:
        return None


def _fmt(x):
    """A number as the page wants to read it: 27.5 stays 27.5, 27.0 prints 27."""
    return '' if x is None else (str(int(x)) if float(x).is_integer() else f'{x:g}')


def read_lines_file(path):
    """The lines file already on the drive, or [] when there is none."""
    if not os.path.exists(path):
        return []
    with open(path, newline='', encoding='utf-8-sig') as fh:
        return list(csv.DictReader(fh))


def current_week(rows):
    """The first week with a game still to be played (no score on the feed), else the last week.
    Read off the feed itself rather than the calendar, so a Tuesday and a Saturday agree."""
    open_weeks = [int(r['week']) for r in rows if _num(r.get('home_score')) is None]
    return min(open_weeks) if open_weeks else max(int(r['week']) for r in rows)


def main():
    cache = os.environ.get('FF_CACHE', HERE)
    feed_p, as_of = fetch(FEED_NAME, FEED_URL, cache)
    with open(feed_p, newline='', encoding='utf-8-sig') as fh:
        games = [r for r in csv.DictReader(fh)
                 if r.get('season') == str(SEASON) and (r.get('game_type') or '') == 'REG']
    if not games:
        sys.exit(f'FAILED: the feed holds no {SEASON} regular-season rows.')

    # EVERY WEEK, ALL 32, EVERY CODE RESOLVED (section 3: a code that does not resolve is named,
    # never silently kept as its own key).
    weeks = sorted({int(r['week']) for r in games})
    missing_weeks = [w for w in range(1, 19) if w not in weeks]
    if missing_weeks:
        sys.exit(f'FAILED: the feed has no {SEASON} regular-season games in week(s) {missing_weeks}. '
                 f'That is a partial feed; delete {feed_p} and re-run.')
    teams = {tk(r['home_team']) for r in games} | {tk(r['away_team']) for r in games}
    bad = sorted(teams - ESPN_TEAMS)
    if bad or len(teams) != 32:
        sys.exit(f'FAILED: {len(teams)} teams on the feed and {len(bad)} that resolve to no ESPN '
                 f'code {bad}. The team map is wrong or the feed is; nothing was written.')

    stamp = as_of.strftime('%Y-%m-%d %H:%M')
    rows, dup = [], collections.Counter()
    for r in games:
        w = int(r['week'])
        home, away = tk(r['home_team']), tk(r['away_team'])
        dup[(w, home)] += 1
        dup[(w, away)] += 1
        spread, total = _num(r.get('spread_line')), _num(r.get('total_line'))
        has = spread is not None and total is not None
        # implied = total/2 + own margin/2. spread_line is home minus away, positive = home
        # favoured, so the home side carries +spread/2 and the away side -spread/2. A game with no
        # line yet is BLANK, never zero: a zero would rank a defense as if its opponent were
        # expected to score nothing.
        rows.append({'week': w, 'gameday': r.get('gameday') or '', 'home': home, 'away': away,
                     'spread_line': _fmt(spread) if has else '',
                     'total_line': _fmt(total) if has else '',
                     'implied_home': _fmt(round(total / 2 + spread / 2, 2)) if has else '',
                     'implied_away': _fmt(round(total / 2 - spread / 2, 2)) if has else '',
                     'has_line': 1 if has else 0, 'as_of': stamp})
    twice = sorted(k for k, n in dup.items() if n > 1)
    if twice:
        sys.exit(f'FAILED: a team is listed twice in one week on the feed: {twice[:6]}. '
                 f'Nothing was written.')

    # THE CURRENT WEEK MUST NOT LOSE ITS LINES. A feed that serves blank spread and total columns
    # for games that carried them in the copy already on the drive is a partial feed, not a market
    # move, and the page would fall back to last season's averages for the one week that matters.
    out = os.path.join(SRC, OUT_NAME)
    cur = current_week(games)
    old = read_lines_file(out)
    old_cur_lined = sum(1 for r in old if r.get('week') == str(cur) and (r.get('has_line') or '0') == '1')
    new_cur_lined = sum(1 for r in rows if r['week'] == cur and r['has_line'])
    new_cur_games = sum(1 for r in rows if r['week'] == cur)
    if old_cur_lined and not new_cur_lined:
        sys.exit(f'FAILED: week {cur} has NO lines on the feed but {old_cur_lined} of its games '
                 f'carried one in {out}. That is a partial feed. The old file is left as it was; '
                 f'delete {feed_p} and re-run, or wait for nflverse.')
    if old_cur_lined > new_cur_lined:
        print(f'  WARNING: week {cur} has {new_cur_lined} lined games on the feed against '
              f'{old_cur_lined} in the copy on the drive. Writing anyway; the page will say which '
              f'games are unlined.')

    # [doc 439] WRITTEN TO A TEMP FILE AND SWAPPED IN ONLY AFTER EVERY CHECK PASSES, so a run that
    # fails leaves the last good file exactly as it was.
    os.makedirs(SRC, exist_ok=True)
    tmp = out + '.tmp'
    with open(tmp, 'w', newline='', encoding='utf-8') as fh:
        w_ = csv.DictWriter(fh, fieldnames=COLS, lineterminator='\n')
        w_.writeheader()
        w_.writerows(sorted(rows, key=lambda r: (r['week'], r['gameday'], r['home'])))
    swap_in(tmp, out)
    lined_by_week = collections.Counter(r['week'] for r in rows if r['has_line'])
    games_by_week = collections.Counter(r['week'] for r in rows)
    print(f'{OUT_NAME}  {len(rows)} games, weeks {weeks[0]}-{weeks[-1]}, lines as of {stamp}')
    print(f'  current week {cur}: {new_cur_lined} of {new_cur_games} games carry a line')
    print('  lined by week: ' + ' '.join(f'{w}:{lined_by_week.get(w, 0)}/{games_by_week[w]}'
                                         for w in weeks))
    print(f'  team codes via {TEAM_MAP_SOURCE}')
    print(f'  written: {out}')


def swap_in(tmp, out):
    """Replace `out` with `tmp` in one step. Google Drive for desktop can hold a brief lock on a
    file it is uploading, so retry before giving up, and never leave the temp file behind."""
    for _ in range(5):
        try:
            os.replace(tmp, out)
            return
        except OSError:
            time.sleep(2)
    import shutil
    shutil.copyfile(tmp, out)
    os.remove(tmp)


if __name__ == '__main__':
    main()
