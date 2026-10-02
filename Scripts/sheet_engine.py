#!/usr/bin/env python3
"""sheet_engine.py -- the weekly sheet's arithmetic and its page, so the whole calculation runs on
Matt's machine instead of in a chat session.

Matt, 2026-09-10: "what to look for each week will change because people will drop players... I'm
not going to be able to do all those calculations week to week."

WHAT IS RECOMPUTED EVERY RUN (because it moves): his roster, the bar grid, the free pool, what each
free player adds. WHAT IS READ FROM Source\\sheet_constants.json (because it is fitted, not weekly):
the two potential distributions, the rival-shortage map, the kicker slope, the defense partners.

The rule the whole page rests on:
    a free player is worth  sum over weeks of max(0, his points a week - the bar)  , skipping his bye
Nothing else. Standard library only. Called by wire.py --html; also runnable on its own for a test.

11 Sept 2026, doc 295 -- THE PAGE NOW LEADS WITH THE MOVE. Matt: "I need the key players, trends
and points of interest right off the bat at the top of the page ... Provide the optimal move, and
the context ... How long to hold the player and the relevant information to help me decide."
Section 0 ranks every candidate the page already prices -- certain fills, screened bets and
backfield seats -- in ONE unit, points above his own bar, and says what it costs, how long to hold
him, when to claim him and what the news is. Nothing in it is typed by hand; it is the sections
below, sorted. Three things came with it: his own open items from matt_todo.txt render on the page
so he is not reading two files; a DO NOT line in that file removes a man from the recommendation
and the block says so and PRICES the rule; and long names clip with the full name on hover, so the
week columns get the width back.
"""
import collections, csv, datetime as dt, hashlib, html, json, os, re, sys

SLOTS = [('QB', 'QB'), ('RB', 'RB'), ('RB', 'RB'), ('WR', 'WR'), ('WR', 'WR'),
         ('TE', 'TE'), ('FLEX', None), ('D/ST', 'D/ST'), ('K', 'K')]
POS = ['QB', 'RB', 'WR', 'TE', 'D/ST', 'K']

# [doc 422] POSITIONS WHOSE VALUE IS THIS WEEK'S MATCHUP, NOT A RATE HELD OVER MANY WEEKS.
# 4.33 measured it at D/ST: take the SCHEDULE, not the player. A kicker is the same shape.
# This page computes season rates. For anyone in this set a season rate is a correct number
# answering a question nobody asked, which is how doc 421 told Matt his Chiefs were droppable in
# the week they projected best in the league. Membership here is what stops that, so a position
# that behaves this way is protected by joining the set rather than by someone remembering 421.
WEEKLY_VALUE = {'D/ST', 'K'}

# [doc 468, finding 4.49] THE MATCHUP TERM, THIS WEEK, RB AND TE ONLY. The opponent's half-PPR
# points allowed per game to the position so far this season, centred on the league average, is
# worth about a point a week between the softest and hardest quarter of defenses at RB (every
# season) and TE (four of five), net of the man's own rate and the pregame line, and nothing at
# WR. The coefficient is points the man gains per point the defense allows above the average to
# his position. It PRINTS beside the rate and never sorts anything: a tiebreak within a point.
# A defense with fewer than four weeks of record prints nothing (the measurement started at
# week 5 for that reason), and so does a man on bye.
MATCHUP_COEF = {'RB': 0.10, 'TE': 0.11}
MATCHUP_MIN_WEEKS = 4


def season_priced(pos):
    """True when a SEASON rate is the right currency for this position.

    [doc 424] ONE PREDICATE, BOTH SIDES. Doc 422 introduced WEEKLY_VALUE and applied it only to the
    replacement lookup, so the drop table was protected and the ADD table was not -- and the page
    offered a defense at a net of MINUS 4.3 that same night. Every consumer of this property calls
    this function, so a position cannot be weekly for one table and seasonal for the other.
    """
    return pos not in WEEKLY_VALUE
FLEXABLE = ('RB', 'WR', 'TE')
WEEKS = list(range(1, 15))
SEASON_WEEKS = list(range(1, 15))     # the fourteen scoring weeks, fixed


def set_horizon(week):
    """Price the weeks that are still AHEAD, never the ones already played (doc 407).

    `WEEKS` was hardcoded to 1..14 and never advanced, so on 23 September the sheet was still
    selling weeks 1, 2 and 3 -- 21% of every total on the page was weeks nobody can buy. wire.py
    has passed the current week into write() since doc 291; nothing ever used it for the horizon.
    Rebinding the module global is deliberate: all thirteen readers of WEEKS take it from here."""
    global WEEKS
    try:
        w0 = int(week or 0)
    except (TypeError, ValueError):
        w0 = 0
    WEEKS = [w for w in SEASON_WEEKS if w >= w0] or list(SEASON_WEEKS)
    return WEEKS
E = lambda s: html.escape(str(s))

# THE 32 TEAM CODES AS ESPN SPELLS THEM, and every other spelling this project has met (doc 291).
# ONE map for both pages: wire.py imports these three names from here. Every join on a team code
# goes through team_key(), and every loader CHECKS that its codes resolve. The first version of
# this check lived only in wire.py's receiver-shape loader, while byes_2026.csv spelled Washington
# WAS and the ESPN pull spelled it WSH -- so rates() silently dropped all 17 Washington players,
# the Commanders defense and kicker Drew Stevens included, from this sheet for four days.
ESPN_TEAMS = frozenset("""ARI ATL BAL BUF CAR CHI CIN CLE DAL DEN DET GB HOU IND JAX KC LAC LAR LV
MIA MIN NE NO NYG NYJ PHI PIT SEA SF TB TEN WSH""".split())
TEAM_ALIAS = {'ARZ': 'ARI', 'BLT': 'BAL', 'CLV': 'CLE', 'HST': 'HOU', 'LA': 'LAR', 'WAS': 'WSH',
              'JAC': 'JAX', 'GNB': 'GB', 'KAN': 'KC', 'NWE': 'NE', 'NOR': 'NO', 'SFO': 'SF',
              'TAM': 'TB', 'LVR': 'LV', 'SD': 'LAC', 'OAK': 'LV', 'STL': 'LAR'}
NO_TEAM = frozenset({'FA', ''})        # a player with no NFL team has no games and no bye


def team_key(t):
    t = str(t or '').strip().upper()
    return TEAM_ALIAS.get(t, t)


_SUFFIX = frozenset({'jr', 'sr', 'ii', 'iii', 'iv', 'v'})


def norm_name(s):
    """One spelling for a name join that has no id (section 3). Case, periods, apostrophes, hyphens
    and generational suffixes are the ways the same man is spelled differently across our files:
    'Christian Mccaffrey', 'Kenneth Walker III', 'J.K. Dobbins'."""
    s = str(s or '').lower().replace('\u2019', "'")
    s = re.sub(r"[.']", '', s).replace('-', ' ')
    return ' '.join(t for t in s.split() if t not in _SUFFIX)


def roster_match(roster, name, team):
    """The roster man with this name on this NFL team, or None. Name AND team, never name alone."""
    key, tm = norm_name(name), team_key(team)
    hits = [pl for pl in roster if norm_name(pl.get('name')) == key and pl.get('tm') == tm]
    return hits[0] if len(hits) == 1 else None


def unknown_teams(codes):
    """The codes that do NOT resolve to one of the 32 after aliasing. Empty means the join is safe."""
    return sorted({team_key(c) for c in codes} - ESPN_TEAMS - NO_TEAM)


# GAMES IN A SEASON PROJECTION (doc 291). ESPN's season projection covers all 17 games, so a
# player's rate per game is his projection divided by 17. The page used 14 -- the number of
# weeks it prices -- which put every player 21% above the per-game rates he is compared with:
# the startable bar, the hit size of a screen, the relief rate of a seat, the defense and kicker
# gaps. Weeks priced stay 14; the rate per week is per game.
PROJ_GAMES = 17.0


# [doc 419] WHAT `Espn_pull_projections.py` ACTUALLY RUNS, read rather than assumed. Matt, 24 Sept:
# "projections were built for pre FF draft. Probably other numbers to check as well. You need to know
# what the job actually runs before you assume you can use it." He was right, and it was not checked.
# The script was last touched 28 August, ten days before the draft. Reading it:
#   * `proj_2026` is ESPN stat row id 102026 -- season split, SOURCE 1, which in season is the REST
#     of the season. That is the mechanism behind the 0.997 reconstruction measured below.
#   * `actual_2026` is id 002026, the season to date, and it is NOT contained in `proj_2026`.
#   * the default sort is `--sort owned`, so the 700 rows are the 700 most-OWNED players, not the
#     top 700 by preseason draft rank. That default is in-season-correct; the `draft` branch is not.
#   * `espn_adp`, `rank_std`, `rank_ppr`, `pct_owned` and `injuryStatus` are ALSO in that file and
#     every one of them is a draft-era or stale field -- `espn_adp` is the contaminated market 1.1
#     forbids, and the two ranks are STANDARD/PPR, neither of them this league's 0.5 PPR. GREPPED:
#     the week sheet reads NONE of them. It takes proj_2026, actual_2026 and raw_actual_stats only,
#     and everything live comes from wire.py. Keep it that way.
def proj_games(week=0):
    """Games left in ESPN's OWN projection, which is what `proj_2026` is a total of.

    [doc 419] MEASURED, AND IT HAD BEEN WRONG SINCE WEEK 1. `proj_2026` is a REST-OF-SEASON total,
    not a full-season one: on the two pulls on the drive (7 Sept and 24 Sept), for the 208 backs and
    receivers projected over 40 preseason, **(24 Sept projection + points already scored) / 7 Sept
    projection has a median of 0.997**. It reconstructs the original almost exactly, which is only
    true if what is left is what is left. 99.1% of those men moved between the two pulls, by a
    median of -6.7 points, and the move does NOT track what they have actually done (r = 0.031 with
    points scored so far) -- ESPN is burning off elapsed games, not re-rating players.

    THE PAGE DIVIDED IT BY 17 EVERY WEEK. With two weeks gone that understates every projected rate
    by about 11%, and it compounds: by week 12 it would be spreading a five-game remainder over
    seventeen. The measured divisor agrees -- the ratio that makes the 24 Sept per-game rate match
    the 7 Sept one is 15.15 games, against 17 - 2 = 15 exactly.

    Games, never weeks: a man plays 17 in an 18-week season. And it is elapsed weeks LEAGUE-WIDE,
    not the man's own games played, because a man who missed week 1 still has the same schedule
    ahead of him as everyone else. With no week given this returns 17, which is right preseason and
    is what every call site did before.

    THIS ALSO MOVES 4.17's CAVEAT THE OTHER WAY, and it is worth saying rather than quietly
    enjoying: BLEND_W was fitted with last season's ppg as the prior, and I recorded its weight on
    this season as an UPPER bound because ESPN's projection is the better prior. Reading that
    projection correctly makes it better still, so the bound is looser, not tighter. The weight is
    NOT shaded to suit: that would be the guess the measurement exists to avoid (0.2).
    """
    done = max(0, int(week or 1) - 1)
    return max(1.0, PROJ_GAMES - done)


def code_stamp(path):
    """Which code built a page: file name, size, modified time and a short hash (doc 291, A6)."""
    try:
        st = os.stat(path)
        with open(path, 'rb') as fh:
            h = hashlib.sha256(fh.read()).hexdigest()[:10]
        when = dt.datetime.fromtimestamp(st.st_mtime).strftime('%d %b %H:%M')
        return f'{os.path.basename(path)} {st.st_size:,} bytes, changed {when}, {h}'
    except OSError:
        return f'{os.path.basename(path)} (unreadable)'


# ----------------------------------------------------------------------- doc 380: what was read, when
# THE SATURDAY CLAIM (doc 374): ESPN settled a waiver at 03:11 ET, every page on the drive still
# described Friday's roster, and nothing looked broken -- the pages were correct about yesterday.
# The published practice, read and dated in doc 380: stamp the READ time of each input rather than
# the build date (Nasdaq data policy v2.6, 2023: the delay message "must prominently appear on all
# displays containing Delayed Data"; the NWS forecast page carries "Last Update" and "Forecast
# Valid" as two separate stamps), and measure staleness at the moment of USE, not of build (IBM,
# May 2026: "the gap between when data was last updated and when it is being used"; RFC 9111's Age).
# So every pull-built page now carries: who read ESPN and when, the vintage and age of every other
# input, and a line the browser writes when the page is OPENED, which turns the block red once a
# settlement window has passed since the build.
#
# 03:30 is where the three settlements this season fell (03:26, 03:26, 03:11 ET, waiver_report_2026.csv,
# 10 to 19 Sept). It is an observed edge, not a rule ESPN publishes; the settings page behind Matt's
# login is the only place the rule lives (ledger row 126).
SETTLE_HHMM = (3, 30)
_PULL_RX = re.compile(r'espn_projections_2026_(\d{8})_(\d{4})\.csv$')


def _when(t):
    """'Saturday 19 September 19:17' -- no leading zero on the day, no year, minutes always.
    (%-d is not portable to Windows, so the day is formatted by hand.)"""
    return f'{t:%A} {t.day} {t:%B} {t:%H:%M}'


def settlements(src):
    """When ESPN actually settled this league's waiver claims: the distinct minutes at which a
    WAIVER-type transaction EXECUTED in waiver_report_2026.csv (py waivers.py --live writes it).
    Read, never typed, so the sentence on the page cannot go stale the way a hand-written one does."""
    p = os.path.join(src, 'waiver_report_2026.csv')
    if not os.path.exists(p):
        return []
    seen = set()
    with open(p, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            if (r.get('Type') or '').strip().upper() == 'WAIVER' and \
               (r.get('Status') or '').strip().upper() == 'EXECUTED':
                seen.add((r.get('Date') or '').strip()[:16])
    out = []
    for d in sorted(seen):
        try:
            out.append(dt.datetime.strptime(d, '%Y-%m-%d %H:%M'))
        except ValueError:
            continue
    return out


def _age(delta):
    s = delta.total_seconds()
    if s < 90:
        return 'just now'
    if s < 5400:
        return f'{s / 60:.0f} minutes old'
    if s < 48 * 3600:
        return f'{s / 3600:.0f} hours old'
    return f'{s / 86400:.0f} days old'


def next_settlement(after):
    """The first SETTLE_HHMM strictly after `after`, in the machine's local time (ET on Matt's)."""
    s = after.replace(hour=SETTLE_HHMM[0], minute=SETTLE_HHMM[1], second=0, microsecond=0)
    if s <= after:
        s += dt.timedelta(days=1)
    return s


def kickoffs(src):
    """Every game on sched_2026.csv that carries a kickoff: (kickoff as local time, week, team, opp,
    side). The `kick` column is ESPN's own `date` field, epoch ms, written by wire.fetch_schedule()
    since doc 381; a file from before that has no column and this returns []."""
    p = os.path.join(src, 'sched_2026.csv')
    out = []
    if not os.path.exists(p):
        return out
    with open(p, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            k = (r.get('kick') or '').strip()
            if not k:
                continue
            try:
                out.append((dt.datetime.fromtimestamp(int(k) / 1000), int(r['week']),
                            team_key(r['team']), team_key(r['opp']), (r.get('side') or '').strip()))
            except (ValueError, KeyError, OSError, OverflowError):
                continue
    return out


def next_lock(src, after, teams=None):
    """The first kickoff strictly after `after`, or with `teams` the first among those teams: the
    moment the next lineup slot locks. None when the file carries no kickoff times."""
    ks = kickoffs(src)
    if teams:
        want = {team_key(t) for t in teams if t}
        ks = [k for k in ks if k[2] in want]
    ks = [k for k in ks if k[0] > after]
    return min(ks, key=lambda k: k[0]) if ks else None


def _game(k):
    """'week 3, KC at MIA' from a kickoffs() row."""
    _, wk, tm, opp, side = k
    return f'week {wk}, {tm} at {opp}' if side == 'away' else f'week {wk}, {opp} at {tm}'


def build_meta(built=None, src=None, teams=None):
    """Who read ESPN and when, for the header of every pull-built page, plus the attributes the
    on-open script reads. FF_WHO is set by ff.bat to the task label (TUE, THU, SUNam, SUNpm, DAILY)
    or BY HAND; a bare `py wire.py` has no label and says so. With `src`, the next lineup lock after
    the build is read off the schedule (doc 381): the first kickoff among `teams` when given, else
    the first kickoff of any game."""
    built = built or dt.datetime.now()
    who = (os.environ.get('FF_WHO') or '').strip() or 'by hand'
    settle = next_settlement(built)
    lock = None
    if src:
        try:
            lock = next_lock(src, built, teams)
        except Exception:                                       # noqa: BLE001
            lock = None
    attrs = (f'data-built="{int(built.timestamp() * 1000)}" '
             f'data-settle="{int(settle.timestamp() * 1000)}"')
    if lock:
        attrs += (f' data-lock="{int(lock[0].timestamp() * 1000)}"'
                  f' data-locktext="{E(_when(lock[0]))}"')
    return {'built': built, 'who': who, 'settle': settle, 'lock': lock,
            'lock_text': (f'{_when(lock[0])} ({_game(lock)})' if lock else ''),
            'text': f'{_when(built)} ({E(who)})', 'attrs': attrs}


# [doc 418] HOW OLD AN INPUT MAY GET BEFORE THE PAGE SAYS SO, in days. Matt, 24 Sept, reading a
# block that stamped every input with its WEEKDAY: "i don't understand the logic of running on Thurs
# when i need the data sooner for waiver decisions." Nothing runs on Thursday. Those were the
# timestamps of the run he had just started, and naming the weekday made a one-off read look like a
# schedule. What he actually needs to know is AGE against the cadence, and the command that resets
# it, so both are on every row now and the weekday is gone.
STALE_DAYS = {'projection': 7.0, 'form': 8.0}


def snaps_newest_week(src):
    """The newest week in Source\\snaps_2026.csv, or 0 when the file is absent or has no week
    column. A freshness fact for the inputs box; nothing prices on it."""
    p = os.path.join(src, 'snaps_2026.csv')
    if not os.path.exists(p):
        return 0
    best = 0
    try:
        with open(p, newline='', encoding='utf-8-sig') as fh:
            for r in csv.DictReader(fh):
                try:
                    best = max(best, int(float(r.get('week') or 0)))
                except ValueError:
                    continue
    except OSError:
        return 0
    return best


def input_rows(src, built, week=0, blended=None):
    """One row per input: what it feeds, how old it is, how to refresh it, and its vintage.

    Every row is read off the file itself (name or modified time), never typed in. Returns
    (feeds, what, vintage, refresh_command, is_stale).

    [doc 418] THE POINTS ROW USED TO SAY "divided by seventeen ... a preseason projection" AND IT
    WAS A CONSTANT STRING. rates() became a measured blend of this season and the projection on
    24 Sept and this sentence did not move, so the page spent a day describing arithmetic it was no
    longer doing, in the one box a reader opens to find out what the numbers are. A provenance box
    that is hand-written is a second source of truth (0.5(c)4): it is now computed from BLEND_W and
    from a count of the rows the page actually printed.
    """
    import glob as _glob
    rows = []
    meta = build_meta(built)
    rows.append(('Roster, free agents and injuries',
                 f'read live from ESPN during this run ({E(meta["who"])})',
                 'this season, live', 'py wire.py, or just .\\ff.bat', False))

    n_meas, n_all = (blended or (0, 0))
    if week and n_meas:
        w = BLEND_W.get(int(week), BLEND_W[max(BLEND_W)])
        last = BLEND_W[max(BLEND_W)]
        rows.append(('Points a week, every pts/wk here',
                     f'a blend of the two rows below: <b>{w*100:.0f}% this season</b> and '
                     f'{100-w*100:.0f}% the projection at week {int(week)}, rising to about '
                     f'{last*100:.0f}% by week 14. {n_meas} of {n_all} men here have a measured '
                     f'rate; the rest show the projection alone',
                     'measured where this season has games, projection where it does not',
                     '', False))
    elif week:
        rows.append(('Points a week, every pts/wk here',
                     'the preseason projection alone, spread over the games still to be played. <b>The measured '
                     'blend is OFF</b> because no man on this page has a rate this season',
                     'a preseason projection', 'py research\\wk1\\build_form.py', True))
    else:
        rows.append(('Points a week, every pts/wk here',
                     'the preseason projection alone, spread over the games still to be played. <b>The measured '
                     'blend is OFF</b> because this build was given no week number',
                     'a preseason projection', '', True))

    fp = os.path.join(src, 'form_2026.csv')
    if os.path.exists(fp):
        mt = dt.datetime.fromtimestamp(os.path.getmtime(fp))
        stale = (built - mt).total_seconds() > STALE_DAYS['form'] * 86400
        # snaps_2026.csv is a FRESHNESS source here and nothing else: its newest week says how far
        # the snap columns reach, beside the form file's age. Read off the file, never typed in.
        _snapwk = snaps_newest_week(src)
        rows.append(('This season\u2019s half of that blend, and the snap and target columns',
                     f'form_2026.csv, {_age(built - mt)}'
                     + (' &mdash; <b>past due</b>' if stale else '')
                     + (f' &middot; snaps through week {_snapwk}' if _snapwk else ''),
                     'this season, measured', 'rebuilt by every ff.bat run',
                     stale))
    else:
        rows.append(('This season\u2019s half of that blend',
                     'form_2026.csv is not on the drive, so <b>the blend is off</b>', 'missing',
                     'py research\\wk1\\build_form.py', True))

    pulls = sorted(_glob.glob(os.path.join(src, 'espn_projections_2026_*.csv')))
    if pulls:
        m = _PULL_RX.search(pulls[-1])
        try:
            pulled = dt.datetime.strptime(m.group(1) + m.group(2), '%Y%m%d%H%M')
            stale = (built - pulled).total_seconds() > STALE_DAYS['projection'] * 86400
            rows.append(('The projection half of that blend',
                         f'ESPN\u2019s own projection, {_age(built - pulled)}'
                         + (' &mdash; <b>past due</b>' if stale else ''),
                         'a preseason projection, updated by ESPN through the season',
                         'pulled by the Tuesday 06:00 run', stale))
        except (AttributeError, ValueError):
            rows.append(('The projection half of that blend',
                         f'{os.path.basename(pulls[-1])}, pull time not in its name',
                         'a preseason projection', 'py Espn_pull_projections.py', True))
    else:
        rows.append(('The projection half of that blend',
                     'no espn_projections_2026_*.csv on the drive', 'missing',
                     'py Espn_pull_projections.py', True))

    fp = os.path.join(src, 'sheet_constants.json')
    if os.path.exists(fp):
        mt = dt.datetime.fromtimestamp(os.path.getmtime(fp))
        rows.append(('The bars, the screen rates and the seat odds',
                     f'sheet_constants.json, {_age(built - mt)}',
                     'fitted on past seasons, not weekly, so age is not staleness', '', False))
    else:
        rows.append(('The bars, the screen rates and the seat odds',
                     'sheet_constants.json is not on the drive', 'missing', '', True))
    return rows


def rate_cell(pl):
    """The pts/wk cell, carrying the vintage of the number inside it (doc 418).

    WHY THE LABEL IS ON THE CELL AND NOT ONLY IN THE BOX AT THE TOP. Two readers need it. Matt,
    24 Sept, on wanting the projection and this season in one place: "I'll also be able to fact
    check your numbers in real time so if I know something is off I know something wasn't updated."
    And `check_vintage.py`, which reads the page the reader reads and, without the label, cannot
    tell a correct blend from the doc 373 defect -- on 24 Sept it called five correct rates refuted
    for exactly that reason. `title` shows it on hover without adding a column; `data-vintage` is
    what the guard parses.
    """
    v = (pl.get('vintage') or 'proj')
    if v == 'proj':
        t = 'ESPN\u2019s projection for the rest of the season, per game'
    else:
        m = pl.get('measured')
        t = (f'{v} this season' + (f' at {m:.1f} a game' if isinstance(m, (int, float)) else '')
             + ', the rest the preseason projection')
    return (f'<td class="rate" data-vintage="{E(v)}" title="{E(t)}">'
            f'{pl.get("wk", 0):.1f}</td>')


def _blend_count(roster, freerows):
    """(men carrying a measured rate, men on the page). Counted off the SAME dicts the page prints,
    so the provenance line cannot claim a blend the table did not apply (doc 418)."""
    allrows = list(roster or []) + list(freerows or [])
    return (sum(1 for r in allrows if (r.get('vintage') or 'proj') != 'proj'), len(allrows))


def inputs_block(src, built=None, teams=None, week=0, blended=None):
    """The box under the masthead. Never raises: a page with a broken inputs box is still a page.
    `teams` are the roster's NFL teams, so the lock line is the reader's own first lock.

    [doc 418] THE PROVENANCE ROWS ARE COLLAPSED AND THE DEADLINES ARE NOT. Matt, 24 Sept: "It's a
    large block of text. Perhaps that section can be collapsed and only expanded when i wish to
    reference." The rows saying where each number came from are reference material, so they fold
    away behind a summary that still carries the one fact worth acting on: whether anything is past
    due. The settlement clock, the kickoff lock and the age line stay OPEN, because those are
    deadlines rather than provenance, and burying a deadline is not tidying.
    """
    built = built or dt.datetime.now()
    meta = build_meta(built, src, teams)
    stale_n = 0
    try:
        rws = input_rows(src, built, week=week, blended=blended)
        stale_n = sum(1 for r in rws if r[4])
        lis = ''
        for feeds, what, vint, refresh, stale in rws:
            cls = ' class="hole"' if stale else ''
            ref = (f' <span class="meta">refresh: <code>{E(refresh)}</code></span>'
                   if refresh else '')
            lis += f'<li{cls}><b>{E(feeds)}:</b> {what}. <em>{E(vint)}.</em>{ref}</li>'
    except Exception as exc:                                    # noqa: BLE001
        lis = f'<li>could not be listed: {E(type(exc).__name__)}: {E(exc)}</li>'
    hh, mm = SETTLE_HHMM
    try:
        runs = settlements(src)
    except Exception:                                           # noqa: BLE001
        runs = []
    if runs:
        clocks = sorted({r.strftime('%H:%M') for r in runs})
        seen = (f'The {len(runs)} settlements this season ran at '
                + (clocks[0] if len(clocks) == 1 else f'{clocks[0]} to {clocks[-1]}')
                + ' ET, the last on ' + _when(runs[-1]) + '.')
    else:
        seen = 'No settlement is on file yet (waiver_report_2026.csv), so the clock below is an assumption.'
    # doc 381: the deadline half of the practice. Lineups lock at kickoff; the next one after the
    # build is read off the schedule, first among the roster's own teams, then the week's first game.
    try:
        any_next = next_lock(src, built)
    except Exception:                                           # noqa: BLE001
        any_next = None
    if meta['lock'] and teams:
        lk = meta['lock']
        lock_line = (f'<li><b>First lineup lock:</b> {_when(lk[0])} '
                     f'({_game(lk)})'
                     + (f'; the week&rsquo;s first game is {_when(any_next[0])} ({_game(any_next)})'
                        if any_next and any_next[0] < lk[0] else '') + '.</li>')
    elif any_next:
        lock_line = (f'<li><b>Lineups lock at kickoff.</b> The next game on file is '
                     f'{_when(any_next[0])} ({_game(any_next)}).</li>')
    else:
        lock_line = ('<li><b>Lineups lock at kickoff.</b> Kickoff times are not on file yet '
                     '(sched_2026.csv has no kick column); the next wire run fetches them.</li>')
    summ = ('every input is current' if not stale_n
            else f'<b>{stale_n} input{"s are" if stale_n != 1 else " is"} past due</b>')
    return (f'<div class="box" id="inputs" {meta["attrs"]}>'
            f'<details><summary>What this page was built from &mdash; {summ}</summary>'
            f'<ul class="inputs">{lis}</ul></details>'
            f'<ul class="inputs">'
            f'{lock_line}'
            f'</ul>{age_line()}</div>')


def age_line():
    """A line the BROWSER writes when the page is opened: how long after the build, and red once a
    settlement window has passed. Static on paper (the text below), live on a screen. Braces are
    doubled nowhere here because this is not an f-string template; check_pages C2 blanks <script>."""
    hh, mm = SETTLE_HHMM
    return ('<p class="sub" id="age"></p>'
            '<script>(function(){var b=document.querySelector("[data-built]"),e=document.getElementById("age");'
            'if(!b||!e)return;var built=Number(b.getAttribute("data-built")),settle=Number(b.getAttribute("data-settle")),'
            'now=Date.now(),h=(now-built)/3600000,age=h<1?Math.round(h*60)+" minutes":h<48?h.toFixed(1)+" hours":Math.round(h/24)+" days";'
            'var msg=h<0?"Your clock says this page was opened before it was built; the build clock and this machine disagree.":"Opened "+age+" after it was built.";'
            'var lock=Number(b.getAttribute("data-lock")||0),lt=b.getAttribute("data-locktext")||"";'
            'if(lock&&now>lock){msg+=" A kickoff ("+lt+") has passed since this page was built, so some of the lineups on it are already locked.";b.classList.add("bad");}'
            'if(now>settle){msg+=" A settlement window (' + f'{hh:02d}:{mm:02d}' + ' ET) has passed since, so the roster and the pool on this page can be yesterday\'s. Run ff.bat before you act on it.";b.classList.add("bad");}'
            'else if(h>24){msg+=" More than a day old: run ff.bat.";b.classList.add("bad");}'
            'e.textContent=msg;})();</script>')


def schedule_sentence(scripts_dir):
    """The footer used to say 'Tuesday 6am, Thursday 5:30pm and twice on Sunday' by hand, and went
    stale the night a fifth run was added (doc 374). Read the times off setup_tasks.bat instead:
    the file that registers them (doc 377: the page reads the batch file, not the scheduler)."""
    fallback = 'Rebuilt by every run of ff.bat; the times are in Scripts\\setup_tasks.bat.'
    days = {'MON': 'Monday', 'TUE': 'Tuesday', 'WED': 'Wednesday', 'THU': 'Thursday',
            'FRI': 'Friday', 'SAT': 'Saturday', 'SUN': 'Sunday'}
    parts = []
    # ONE PARSER FOR ONE FILE: make_commands.schedule() already reads these lines for the
    # commands page. Use it; the regex below is only for a tree where that file is missing.
    try:
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        import make_commands as _mc
        for _tn, day, hhmm, _runs in _mc.schedule():
            if hhmm:
                parts.append(f'{days[day.upper()]} {hhmm}' if day and day.upper() in days
                             else f'every day {hhmm}')
    except Exception:                                           # noqa: BLE001
        parts = []
    if not parts:
        p = os.path.join(scripts_dir, 'setup_tasks.bat')
        try:
            with open(p, encoding='utf-8', errors='replace') as fh:
                lines = [ln for ln in fh if not ln.lstrip().upper().startswith('REM')]
        except OSError:
            return fallback
        rx = re.compile(r'schtasks\s+/create.*?/sc\s+(WEEKLY|DAILY)(?:\s+/d\s+(\w+))?\s+/st\s+(\d\d:\d\d)', re.I)
        for ln in lines:
            m = rx.search(ln)
            if not m:
                continue
            kind, day, hhmm = m.groups()
            parts.append(f'every day {hhmm}' if kind.upper() == 'DAILY'
                         else f'{days.get((day or "").upper(), day)} {hhmm}')
    if not parts:
        return fallback
    return ('Rebuilt by every run of ff.bat, by hand or on the schedule setup_tasks.bat registers: '
            + ', '.join(parts) + '.')


# What ESPN's own player card already shows (doc 291, A15). Matt, 11 Sept: "a 'do not' line only
# earns space on the sheet when the sheet is the only place that information exists. Anything
# ESPN already tells me does not belong there." A status other than ACTIVE is on his player card.
ESPN_SHOWS_STATUS = frozenset({'OUT', 'INJURY_RESERVE', 'SUSPENSION', 'DOUBTFUL', 'QUESTIONABLE',
                               'DAY_TO_DAY', 'PUP', 'NOT_ACTIVE'})
GONE_FOR_WEEKS = frozenset({'OUT', 'INJURY_RESERVE', 'SUSPENSION', 'PUP', 'NOT_ACTIVE'})


# [doc 432] THE REACH GATE. Measured ceilings: the target share a man actually HELD while producing
# at the archetype hit rate, over 854 six-week windows, nflverse REG 2021-2025. p99, which is the most
# anyone has sustained; the max ever is 41.2% (WR) and 33.1% (TE). The median hit sits at 27% / 24.5%
# on an offence throwing about 34 a game. RB was not measured and is not gated.
REACH_CEIL = {'WR': 0.378, 'TE': 0.327}


def target_load(src):
    """[doc 432] {norm_name: his targets a game} and {team: the team's targets a game}, this season.

    THE BET LANE NEVER HAD A DENOMINATOR. It prices every candidate at ONE archetype hit rate and
    never asks whether his own offence throws enough for that to be reachable. Matt found it twice
    in one evening: Cade Otton, capped by having no end-zone role, and Malik Washington, whose 26%
    share is 26% of the 28th-ranked passing game -- he would need 14.4 targets a game out of Miami's
    25. Section 0.5(a6) already said it in his own words, "targets on one offence are zero sum, find
    the resource that constrains him", and the page shipped two takes that ignored it.
    """
    p = os.path.join(src, 'form_2026.csv')
    if not os.path.exists(p):
        return {}, {}
    mine, team, gm = collections.Counter(), collections.Counter(), collections.defaultdict(set)
    with open(p, encoding='utf-8', errors='replace') as fh:
        for r in csv.DictReader(fh):
            w = (r.get('week') or '').strip()
            if not w or w == '0':        # week 0 is the SEASON AGGREGATE. Counting it doubles
                continue                 # every total, which it did on the first cut of this.
            try:
                t = float(r.get('targets') or 0)
            except ValueError:
                continue
            if (r.get('pos') or '') not in ('WR', 'TE', 'RB'):
                continue
            mine[norm_name(r.get('player'))] += t
            team[(r.get('team') or '').strip()] += t
            gm[(r.get('team') or '').strip()].add(w)
    tg = {k: (v / len(gm[k])) for k, v in team.items() if gm.get(k)}
    ng = max((len(v) for v in gm.values()), default=0) or 1
    return {k: v / ng for k, v in mine.items()}, tg


def pos_leaders(src):
    """[1 Oct, doc 457] {(team, pos): (name, targets, week)}: the man with the most targets at each
    position on each team in the NEWEST week on the form file, and {norm_name: his targets that
    week}. Michael Mayer cleared the week-1 workload screen as the top tight end in Las Vegas while
    Brock Bowers was out, Bowers came back in week 3 with 13 targets to Mayer's 3, and the page kept
    pricing Mayer at the screen's 38% and put him in THE CALL. Measured on the screen's own
    population (te2_split.py, n=517): every tight end who cleared two of three marks led his team at
    the position in week 1 (15 of 15); a second receiver cleared it 22 times and hit 5 (22.7%),
    against 25 of 54 (46.3%) for the leaders. The man ahead is the take contract's third line and
    the lane never read it."""
    p = os.path.join(src, 'form_2026.csv')
    if not os.path.exists(p):
        return {}, {}
    rows = []
    with open(p, encoding='utf-8', errors='replace') as fh:
        for r in csv.DictReader(fh):
            try:
                w = int((r.get('week') or '').strip() or 0)
                t = float(r.get('targets') or 0)
            except ValueError:
                continue
            if w <= 0 or (r.get('pos') or '') not in ('WR', 'TE'):
                continue
            rows.append((w, (r.get('team') or '').strip(), r.get('pos'), r.get('player') or '', t))
    if not rows:
        return {}, {}
    newest = max(r[0] for r in rows)
    lead, mine = {}, {}
    for w, tm, pos, nm, t in rows:
        if w != newest:
            continue
        mine[norm_name(nm)] = t
        k = (team_key(tm), pos)
        if k not in lead or t > lead[k][1]:
            lead[k] = (nm, t, w)
    return lead, mine


def rb_usage(src):
    """[1 Oct, doc 459] {norm_name: dict(team, pg, games, last, last_week)} for every running back on the
    form file: carries plus targets a game this season (the week-0 aggregate) and in his last game played.
    Matt, 1 Oct: "Tyler Badie? What is the upside ... a 4th string running back in a RB by committee
    backfield. This must be some kinda error." It was: the wire's doubt lane pairs any ROSTERED back who
    carries a status with the first FREE back on his team, and doc 451's open-job block priced every such
    pair at the lead-back relief rate. Coleman (6.5 touches a game) never held Denver's job; Dobbins (12.3)
    does. Of the five "open jobs" on 30 Sept, one was real (Achane 15.3 a game, Gordon 20 touches in
    relief). The block now asks two questions off this file: did the absent man HOLD the job (the most
    touches a game among his team's backs), and is the free man the one who INHERITS it (the most touches
    in the last game among the backs left)."""
    p = os.path.join(src, 'form_2026.csv')
    if not os.path.exists(p):
        return {}
    out, last = {}, {}
    with open(p, encoding='utf-8', errors='replace') as fh:
        for r in csv.DictReader(fh):
            if (r.get('pos') or '') != 'RB':
                continue
            try:
                w = int((r.get('week') or '').strip() or 0)
                t = float(r.get('carries') or 0) + float(r.get('targets') or 0)
                g = float(r.get('games') or 0)
            except ValueError:
                continue
            k = norm_name(r.get('player'))
            tm = team_key((r.get('team') or '').strip())
            if w == 0:
                try:
                    _pts = float(r.get('half_ppr') or 0)
                except ValueError:
                    _pts = 0.0
                out[k] = {'team': tm, 'pg': (t / g) if g else 0.0, 'games': g, 'last': 0.0, 'last_week': 0,
                          'name': r.get('player') or '', 'ppg': (_pts / g) if g else 0.0}   # doc 460: ppg
            else:
                if w > last.get(k, (0, 0))[0]:
                    last[k] = (w, t)
    for k, (w, t) in last.items():
        if k in out:
            out[k]['last'], out[k]['last_week'] = t, w
    return out


def wr_usage(src):
    """[1 Oct, doc 460] {norm_name: dict(team, tpg, games, ppg, name)} for every receiver on the form
    file, off the week-0 aggregate: targets a game and half-PPR a game this season. The long-shot lane
    reads it to say whether a receiver is under the bar and how much he is thrown to."""
    p = os.path.join(src, 'form_2026.csv')
    if not os.path.exists(p):
        return {}
    out = {}
    with open(p, encoding='utf-8', errors='replace') as fh:
        for r in csv.DictReader(fh):
            if (r.get('pos') or '') != 'WR':
                continue
            try:
                w = int((r.get('week') or '').strip() or 0)
                t = float(r.get('targets') or 0)
                g = float(r.get('games') or 0)
                pts = float(r.get('half_ppr') or 0)
            except ValueError:
                continue
            if w != 0:
                continue
            out[norm_name(r.get('player'))] = {'team': team_key((r.get('team') or '').strip()),
                                              'tpg': (t / g) if g else 0.0, 'games': g,
                                              'ppg': (pts / g) if g else 0.0, 'name': r.get('player') or ''}
    return out


def pf_rank(src):
    """[1 Oct, doc 460] (his rank by points for, teams) off standings_2026.csv, or None. The long-shot
    lane leads the seat list when he is outside the top six by points, and follows it otherwise."""
    p = os.path.join(src, 'standings_2026.csv')
    if not os.path.exists(p):
        return None
    rows = []
    with open(p, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            try:
                rows.append(((r.get('mine') or '').strip() == 'yes', float(r.get('points_for'))))
            except (TypeError, ValueError):
                continue
    me = [v for m, v in rows if m]
    if not me or not rows:
        return None
    return 1 + sum(1 for _, v in rows if v > me[0]), len(rows)


def waiver_rank(src):
    """[1 Oct, doc 462] (his waiver rank, teams) off standings_2026.csv (wire.py writes waiverRank off
    mTeam every run), or None. Never quoted from memory (doc 396)."""
    p = os.path.join(src, 'standings_2026.csv')
    if not os.path.exists(p):
        return None
    rows = []
    with open(p, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            rows.append(r)
    me = next((r for r in rows if (r.get('mine') or '').strip() == 'yes'), None)
    try:
        return (int(float(me.get('waiver_rank'))), len(rows)) if me and me.get('waiver_rank') not in (None, '') else None
    except (TypeError, ValueError):
        return None


def waterfall_html(rows, wr, const, hedge, lane_leads=False):
    """[1 Oct, doc 462] HOW TO PLACE THEM, under THE CALL, folded. Matt, 1 Oct: "the 'you would drop'
    isn't the complete picture. The info i need following is practical movements such as how to place
    my waivers ... chances a player will be there in combination to the value they may add ... I'm
    currently 11 of 12 so that factors in for Friday as well ... my player of lowest value should come
    first for each player i want to pick up since there is always a chance i don't get the 1st or even
    2nd." Every number here is the league's own (doc 396: 71.4% of player-runs uncontested, an
    uncontested claim lands 78%; doc 314: the contested share by last game's usage; doc 224: his own
    contested win rate), read off sheet_constants.json; his rank is read off the standings file.
    [doc 463] The contested term at his rank is measured (claims.by_rank_band), no longer a floor.
    `rows`: dicts with name, pos, tm, claim (bool), drop, worth, net, contested (float or None), when.
    `hedge`: the name of the cheapest man whose cost on the bye grid is zero, or ''."""
    cl = (const or {}).get('claims') or {}
    if not rows or not cl:
        return ''
    unc_land = cl.get('uncontested_land') or 0.0
    r, n = (wr or (None, None))
    # [doc 463] A CONTESTED CLAIM AT HIS RANK IS MEASURED NOW, not a judgement floor: the share of contested
    # claims that landed by the claimant's waiver rank that week, this league 2022 to 2025 (claim_rank.py).
    _bands = ((cl.get('by_rank_band') or {}).get('bands') or [])
    _band = next((b for b in _bands if r and b['lo'] <= r <= b['hi']), None)
    c_land = (_band['land'] if _band else (cl.get('contested_per_claim') or 0.0))
    if r and n:
        where = (f'You are <b>{r} of {n}</b> on waivers this week (the order resets to inverse standings each week). '
                 + (f'From ranks {_band["lo"]} to {_band["hi"]} a contested man has landed <b>{c_land:.0%}</b> of the time in this '
                    f'league; ' if _band else f'a contested claim lands {c_land:.0%} of the time across every rank; ')
                 + f'an uncontested claim lands about {unc_land:.0%} whatever your rank, and a free agent is yours the moment you click.')
    else:
        where = ('Your waiver rank could not be read this run, so the odds below use the league base rates only: '
                 f'an uncontested claim lands about {unc_land:.0%}, a contested one {c_land:.0%} across every rank.')
    # [1 Oct, doc 469] THE CARD, NOT THE PARAGRAPH. Matt, 1 Oct: "please see the difference in the pending
    # move card from ESPN and the one on the week sheet that is a block of text. Which one is easier to
    # follow at a glance ... if i'm going to arrange my waivers, and follow the model suggestion wouldn't
    # i want the two to look visually the similar? ... it only needs what can't be demonstrated with the
    # image." So: one row per move in the shape of ESPN's Pending Moves card (the add, the drop, the
    # morning it processes, the priority to set), free agents first as "now", claims in the order to set
    # them (the contested man first: ESPN moves a winner to the back of the order mid-run, so his priority
    # is highest on the first claim processed, doc 396), and the prose carries only what the card cannot
    # show: the odds, the one-drop-per-claim rule, the hedge.
    def _morning(iso):
        try:
            t = dt.datetime.strptime(str(iso)[:16], '%Y-%m-%d %H:%M')
            return t.strftime('%a %-d %b') if os.name != 'nt' else t.strftime('%a %d %b').replace(' 0', ' ')
        except (TypeError, ValueError):
            return ''
    claims = [x for x in rows if x['claim']]
    frees = [x for x in rows if not x['claim']]
    claims.sort(key=lambda x: -(x.get('contested') or 0))          # the contested man first
    trs = ''
    for x in frees:
        when = f' ({E(x["when"])})' if x.get('when') and x['when'] != 'this week' else ''
        trs += (f'<tr><td class="pri">now</td><td class="l"><b>Add {E(x["name"])} now</b>, {E(x["tm"])} {E(x["pos"])}, '
                f'a free agent{when}<br>drop {E(x["drop"])}'
                + (f', {E(x["drop_tm"])} {E(x["drop_pos"])}' if x.get('drop_pos') else '')
                + '<span class="meta">no claim, no priority spent; yours if you are first to click</span></td>'
                f'<td class="n">click</td><td class="n">{x["net"]:+.1f}</td></tr>')
    for i, x in enumerate(claims, 1):
        c = x.get('contested')
        if c is None:
            lands, exp_txt, note = '?', f'{x["net"]:+.1f}', 'no last game on file, so his contested odds are not read'
        else:
            p_land = (1 - c) * unc_land + c * c_land
            lands, exp_txt = f'{p_land:.0%}', f'{x["net"] * p_land:+.1f}'
            note = (f'contested {c:.0%} of the time by men with his last game (a league base rate); '
                    f'{x["net"]:+.1f} if he lands')
        when = f' ({E(x["when"])})' if x.get('when') and x['when'] != 'this week' else ''
        morning = _morning(x.get('clears'))
        trs += (f'<tr><td class="pri">{i}</td><td class="l"><b>Conditionally add {E(x["name"])}</b>, {E(x["tm"])} {E(x["pos"])} '
                f'from Waivers{when}<br>Conditionally drop {E(x["drop"])}'
                + (f', {E(x["drop_tm"])} {E(x["drop_pos"])}' if x.get('drop_pos') else '')
                + (f'<span class="meta">processes the morning of {E(morning)}; {note}</span>' if morning else f'<span class="meta">{note}</span>')
                + f'</td><td class="n">{lands}</td><td class="n">{exp_txt}</td></tr>')
    card = ('<table class="pend"><thead><tr><th>priority</th><th class="l">move</th><th>lands</th><th>expected</th>'
            '</tr></thead><tbody>' + trs + '</tbody></table>')
    order = ''
    if len(claims) >= 2:
        order = (f' Set the priorities in the order shown: {E(claims[0]["name"])} first because he is the one most '
                 f'likely to be contested, and ESPN moves a winner to the back of the order mid-run, so your priority '
                 f'counts most on the first claim it processes.')
    drops = ('<p class="ctx fine"><b>One drop carries one claim.</b> To land all of them: a different drop on each, as '
             'shown. To land only the first that wins: '
             + (f'the same drop, <b>{E(hedge)}</b>, on every claim' if hedge else 'the same cheapest drop on every claim')
             + '; the first winner takes him and the later claims fail as already dropped. Never name a man in the '
             'injured-reserve slot.' + order + '</p>')
    run = ('<p class="ctx fine">Claims run Thursday 03:00 to 06:00; a man dropped on Wednesday clears Friday about 03:00 '
           'instead, and the card says which. Check the roster the morning a claim processes. Free agents are immediate.'
           + (' The long shots below are claims too, under the same rules, and their drop is the hedge man: a ticket '
              'is never worth a man who starts for you.' if lane_leads else '') + '</p>')
    return ('<details class="leftoff" open><summary>How to place them: your rank, the order, the drops</summary>'
            f'<p class="ctx fine">{where}</p>{card}{drops}{run}</details>')


def tail_shape(c, rb_use, wr_use, tails):
    """[1 Oct, doc 460] Which cell of the measured tail table a FREE man sits in, read off his team's
    own usage this season, and the words that say why. Returns (cell key, shape words, inputs words)
    or (None, why he is not on the lane, ''). Mirrors tail_tickets.py exactly: the same cut points, so
    the page's cell is the measured cell and not a cousin of it."""
    pos = (c.get('pos') or '').strip()
    k = norm_name(c.get('name'))
    bars = (tails.get('bars') or {})
    if pos == 'RB':
        u = (rb_use or {}).get(k)
        if not u or not u.get('games'):
            return None, 'no games on the form file', ''
        if u['ppg'] >= bars.get('RB', 9.92):
            return None, 'already startable, so he is a pickup and priced above', ''
        mates = [v for v in rb_use.values() if v['team'] == u['team'] and v.get('games')]
        mates.sort(key=lambda v: -v['pg'])
        rank = 1 + next((i for i, v in enumerate(mates) if norm_name(v['name']) == k), len(mates))
        lead = mates[0] if mates else u
        leads = sorted((max((v['pg'] for v in rb_use.values() if v['team'] == t and v.get('games')), default=0.0)
                        for t in {v['team'] for v in rb_use.values()}), reverse=True)
        job_rank = 1 + sum(1 for x in leads if x > lead['pg'])
        ahead = '' if rank == 1 else f"behind {lead['name']} ({lead['pg']:.1f} a game, {lead['last']:.0f} last game)"
        inputs = f"{u['pg']:.1f} touches a game, {u['last']:.0f} last game, {u['ppg']:.1f} points a game" + (f'; {ahead}' if ahead else '')
        if rank == 1:
            return (('lead_12', 'lead back under the bar, 12 or more touches a game') if u['pg'] >= 12 else
                    ('lead_u12', 'lead back under the bar, under 12 touches a game')) + (inputs,)
        if rank == 2 and lead['pg'] >= 12 and u['pg'] < 8:
            return ('handcuff_top12' if job_rank <= 12 else 'handcuff_other'), (
                f"handcuff behind the {'top-12' if job_rank <= 12 else 'number ' + str(job_rank)} job"), inputs
        if rank == 2 and 8 <= u['pg'] < 14:
            return 'committee', 'committee partner, the second back with part of the job', inputs
        if rank >= 3 and u['pg'] < 8:
            return 'third', 'third string or lower', inputs
        return None, f"a shape the table did not measure ({u['pg']:.1f} a game, number {rank} on his team)", ''
    if pos == 'WR':
        u = (wr_use or {}).get(k)
        scr = (c.get('screen') or '').strip()
        if u and u.get('games') and u['ppg'] >= bars.get('WR', 9.62):
            return None, 'already startable, so he is a pickup and priced above', ''
        inputs = (f"{u['tpg']:.1f} targets a game, {u['ppg']:.1f} points a game" if u and u.get('games') else 'no games on the form file')
        if 'in-season screen 3 of 3' in scr:
            return 'wr_3of3', 'young receiver with all three marks on this season', inputs
        if u and u.get('games') and u['tpg'] >= 2:
            return 'wr_other', 'receiver without the three marks', inputs
        return None, 'under two targets a game, outside every measured cell', ''
    return None, 'the table covers backs and receivers only', ''


def longshot_lane(freerows, rb_use, wr_use, const, pf, cap=10, odds=None):
    """[1 Oct, doc 460] THE LONG SHOTS, RANKED BY THE ODDS OF A BIG HIT. Matt, 1 Oct: "Just because the
    average of backups doesn't hit or return for extended time doesn't mean it can't happen and strike
    big ... I don't feel we are measuring the right thing the right way." The seat list prices the mean
    (relief points times weeks). This lane prices the tail: for every free man under the bar, the share
    of men in his shape at this point of a season who went on to six or more startable weeks of the
    next ten, or a four-week stretch at 15 a game, measured 2021 to 2025 (tail_tickets.py; the cells
    live in sheet_constants.json under tail_tickets). A shape's rate, never his forecast. Returns
    (html, leads) where leads says whether it goes above the seat list (behind in points) or below."""
    tails = (const or {}).get('tail_tickets') or {}
    cells = tails.get('cells') or {}
    if not cells:
        return ('<div class="box bad"><h4>the long shots are not on this page</h4><p>sheet_constants.json '
                'has no tail_tickets block; run tail_tickets.py and file its cells (doc 460).</p></div>', False)
    rows, left = [], []
    seen = set()
    for c in freerows or []:
        if c.get('pos') not in ('RB', 'WR') or c.get('name') in seen:
            continue
        seen.add(c.get('name'))
        key, shape, inputs = tail_shape(c, rb_use, wr_use, tails)
        if key is None:
            left.append((c.get('name'), shape))
            continue
        cell = cells.get(key) or {}
        if not cell.get('n'):
            left.append((c.get('name'), f'no measured cell for {shape}'))
            continue
        if (cell.get('month') or 0) <= 0 and (cell.get('big') or 0) <= 0:
            left.append((c.get('name'), f"{shape}: 0 of {cell['n']} on both columns"))
            continue
        claim = 'claim' if 'CLAIM' in (c.get('flags') or '') else 'free'
        st = (c.get('status') or 'ACTIVE').replace('_', ' ').lower()
        rows.append({'name': c.get('name'), 'pos': c.get('pos'), 'tm': c.get('tm'), 'shape': shape, 'cell': key,
                     'inputs': inputs, 'big': cell.get('big') or 0.0, 'month': cell.get('month') or 0.0,
                     'four': cell.get('four') or 0.0, 'n': cell['n'], 'claim': claim,
                     'status': '' if st == 'active' else st, 'owned': c.get('owned')})
    # Ranked on the two big-hit columns together, then the four-week one; at most three men of one shape,
    # because five handcuffs behind top-12 jobs carry one identical rate and would fill the lane while a
    # screened receiver with a fatter tail sat under the cut.
    # [1 Oct, doc 470] A CELL UNDER TEN MEN PRINTS NO RATE AND SORTS LAST. Matt, on Lloyd: "Green bay doesn't have
    # a healthy O-line and the run game is not looking good." The lane had him first on a cell of nine men
    # (two of whom gave a 15-point month), printed as "~22%", and I called it the fattest shape on the wire.
    # Two of nine is not a rate; it is an anecdote with a tilde. Under ten the columns say "too few" and the
    # row sorts after every measured shape, so a thin cell can never lead the lane.
    rows.sort(key=lambda r: (r['n'] < 10, -(r['big'] + r['month']), -r['four']))
    shown, more, _per = [], [], {}
    for r in rows:
        if len(shown) < cap and _per.get(r['cell'], 0) < 3:
            shown.append(r)
            _per[r['cell']] = _per.get(r['cell'], 0) + 1
        else:
            more.append(r)
    body = ''
    for r in shown:
        meta = E(r['tm'] or '') + (f" &middot; {r['status']}" if r['status'] else '') + (
            f" &middot; {_f(r['owned']):.0f}% rostered" if _f(r['owned']) is not None else '')
        thin = '~' if r['n'] < 20 else ''      # a shape measured on under twenty men
        if r['n'] < 10:
            _cols = '<td class="meta">too few</td><td class="meta">too few</td><td class="meta">too few</td>'
        else:
            _cols = (f'<td class="tot{" pos" if r["big"] >= 0.05 else ""}">{thin}{r["big"]:.0%}</td>'
                     f'<td class="tot{" pos" if r["month"] >= 0.10 else ""}">{thin}{r["month"]:.0%}</td>'
                     f'<td>{thin}{r["four"]:.0%}</td>')
        body += (f'<tr><th scope="row"><span class="pl">{E(r["name"])}</span><span class="meta">{meta}</span></th>'
                 f'<td><span class="pl">{E(r["shape"])}</span><span class="meta">{E(r["inputs"])}</span></td>'
                 + _cols + f'<td>{E(r["claim"])}</td></tr>')
    # [1 Oct, doc 469, v9.39] THE TRIGGER IS THE SIMULATED ODDS, NOT THE POINTS RANK. Doc 464 measured
    # where a ticket beats the same points spread evenly: under about 30% to make the top six, and not
    # above. The points rank was the stand-in until the schedule file existed (v9.38); it stays as the
    # fallback when the odds cannot be computed.
    if odds:
        behind = odds[0] < 0.30
        where = (f'You are {odds[0]:.0%} to make the top six, so this lane leads the seat list: under 30%, a long shot '
                 f'is worth more than the same points spread evenly.' if behind else
                 f'You are {odds[0]:.0%} to make the top six, so the seat list leads and this follows it: at 30% or '
                 f'better, steady points are worth as much as a long shot or more.')
    else:
        behind = bool(pf and pf[0] > 6)
        where = (f'You are {pf[0]} of {pf[1]} in points for and the playoff odds could not be simulated, so this lane leads the seat list.' if behind else
                 (f'You are {pf[0]} of {pf[1]} in points for and the playoff odds could not be simulated, so the seat list leads and this follows it.' if pf else
                  'No standings line, so the seat list leads.'))
    lede = (f'<h2 id="tickets">The long shots &mdash; ranked by the odds of a BIG hit</h2>'
            f'<p class="lede">{where} Each man under the bar is placed in the shape the usage on his own team puts him in, '
            f'and the columns say how often men of that shape, from this point of a season, went on to six or more '
            f'startable weeks of the next ten, a four-week stretch at 15 a game, and four or more startable weeks. '
            f'Five seasons. The rate is the shape&rsquo;s, never his forecast, and it cannot see who is actually on a 12-team wire.</p>')
    hdr = ('<tr><th class="corner" scope="col">the man</th><th scope="col">his shape, and what he has done</th>'
           '<th class="tot" scope="col">6+ startable weeks</th><th class="tot" scope="col">a 15-point month</th>'
           '<th scope="col">4+ weeks</th><th scope="col">costs</th></tr>')
    note = (f"Not listed: third-string backs (0 of {cells.get('third', {}).get('n', '?')} on both columns in five "
            f"seasons, so the pre-event Wally Pipp is not a bet this lane makes; the wire's relief lane buys him after the "
            f"game that shows it) and receivers without the three marks (under 2% on both). "
            f"A lead back with 12 or more touches a game and the points not yet in is the fattest shape of all "
            f"({(cells.get('lead_12') or {}).get('month', 0):.0%} of them gave a big month), "
            f"and he is almost never free: the one you hold is worth more than anything here.")
    html = lede + (_tbl(hdr, body, 'Best first. The columns are measured on the shape, not on the man; ~ marks a shape measured on under twenty men, and a shape measured on under ten prints no rate at all and sits last.') if body else
                   '<p class="ctx">No free back or receiver sits in a shape with a measured tail this week.</p>') +         f'<p class="ctx fine">{note}</p>'
    if left or more:
        html += ('<details class="leftoff"><summary>Left off: ' + str(len(left) + len(more)) + ' men, and why</summary><p>'
                 + '; '.join([f'<b>{E(nm)}</b> ({E(why)})' for nm, why in left]
                             + [f'<b>{E(r["name"])}</b> ({E(r["shape"])}, {r["big"]:.0%} and {r["month"]:.0%}, below the cut)' for r in more])
                 + '.</p></details>')
    return html, behind


def reach_check(c, HP, mine_pg, team_pg):
    """[doc 432] What the bet is ASKING of him, and whether anyone has ever held that share.

    A CONSTRAINT, NOT A FORECAST. It does not say he will hit. It says he cannot: to reach HP at his
    OWN catch rate and yards per catch, with no touchdown, he needs `need` targets a game, which is
    `share` of everything his team throws. Above the measured ceiling the odds beside his name are
    describing something nobody in five seasons has done.
    Returns (need a game, share of the team, verdict) or (None, None, '') when it cannot be judged.
    """
    ceil = REACH_CEIL.get((c.get('pos') or '').strip())
    now = c.get('measured')
    if not ceil or not HP or not now or now <= 0 or not mine_pg or not team_pg:
        return None, None, ''
    need = mine_pg * (HP / now)
    share = need / team_pg
    return need, share, ('out of reach' if share > ceil else '')


def season_ppg(src):
    """{name: (points a game, games)} this season, IMPORTED from check_vintage so the page and the
    guard can never print two different numbers for one thing (0.5(c)4). RB/WR/TE only: form_2026
    does not score passing or kicking (doc 375)."""
    try:
        import check_vintage
    except Exception:                                    # noqa: BLE001
        return {}
    act, err = check_vintage.season_actual(os.path.join(src, 'form_2026.csv'))
    return {} if err else (act or {})


def season_ppg_keyed(src):
    """season_ppg()'s numbers under section 3's key: {(norm_name, pos, team): (ppg, games, name,
    act2, xfp2)}. Name + position + team, never less.

    The numbers are season_ppg()'s (one claimant, check_vintage.season_actual); only the KEY is
    built here. Position and team are read off form_2026.csv's own rows, the week-0 row when the
    man has one and the newest week row otherwise, so a name that appears under two positions or
    two teams is two keys and can never be joined by name alone. `act2` and `xfp2` are the week-0
    row's last-two-games actual and expected averages (doc 438), carried as strings so a blank
    stays blank, never a zero.
    """
    act = season_ppg(src)
    if not act:
        return {}
    p = os.path.join(src, 'form_2026.csv')
    ident = {}                       # player -> (pos, team, act2, xfp2), the week-0 row winning
    try:
        with open(p, newline='', encoding='utf-8-sig') as fh:
            for r in csv.DictReader(fh):
                n = (r.get('player') or '').strip()
                if not n:
                    continue
                w = (r.get('week') or '').strip()
                pos, tm = (r.get('pos') or '').strip().upper(), team_key(r.get('team'))
                if w == '0' or n not in ident:
                    ident[n] = (pos, tm, (r.get('act2') or '').strip(), (r.get('xfp2') or '').strip())
    except OSError:
        return {}
    out = {}
    for n, (ppg, games) in act.items():
        pos, tm, a2, x2 = ident.get(n, ('', '', '', ''))
        out[(norm_name(n), pos, tm)] = (ppg, games, n, a2, x2)
    return out


def _form_variant(form, player, pos, team):
    """COPIED FROM wire.py's _form_variant (doc 442), not imported: importing wire.py reaches ESPN.
    ESPN says "Joshua Palmer" and nflverse "Josh Palmer", so the exact name + position + team key
    misses him. Same team, same position, same surname, and one of the first names is a prefix of
    the other: that is a variant of one man, not a second man. Exactly one candidate or nothing;
    two candidates is a real ambiguity and stays blank rather than guessing."""
    key = norm_name(player)
    if not key or not form:
        return None
    parts = key.split()
    if len(parts) < 2:
        return None
    first, rest = parts[0], ' '.join(parts[1:])
    hits = []
    for (nm, p, tm), fr in form.items():
        if p != pos or tm != team:
            continue
        q = nm.split()
        if len(q) < 2 or ' '.join(q[1:]) != rest:
            continue
        if q[0].startswith(first) or first.startswith(q[0]):
            hits.append(fr)
    if len(hits) == 1:
        return hits[0]
    return None


def form_lookup(keyed, name, pos, team):
    """The form join, the same two steps wire.py takes (doc 442): exact norm_name + position + team,
    then the one-candidate first-name variant on the same team and position. None when neither
    hits. Every form join in this module goes through here, so the engine and the wire cannot
    join the same man two different ways."""
    if not keyed:
        return None
    pos, tm = (pos or '').strip().upper(), team_key(team)
    hit = keyed.get((norm_name(name), pos, tm))
    if hit is None:
        hit = _form_variant(keyed, name, pos, tm)
    return hit


def this_season_text(pl):
    """'5.7 this season (3 g)' for a row rates() joined to form_2026.csv; '' when it did not.
    Blank, never zero: a man with no form row has no measured rate, not a rate of nothing."""
    m, g = pl.get('measured'), pl.get('measured_g')
    if not isinstance(m, (int, float)) or not g:
        return ''
    return f'{m:.1f} this season ({int(g)} g)'


def last_two_text(pl):
    """'last 2: 10.4 actual / 4.3 expected' plus the wire's flag word when the row carries the
    last-two-games columns (doc 438); '' when either is blank. The flag is read off the wire row's
    own `flags` text when the row has one; a roster row has none, so the same two fixed cells
    wire.py flags (8+ actual on under 5 expected, 8+ expected on under 5 actual) are applied to
    the numbers it carries. Display only."""
    try:
        a2, x2 = float(str(pl.get('act2') or '').strip()), float(str(pl.get('xfp2') or '').strip())
    except (TypeError, ValueError):
        return ''
    txt = f'last 2: {a2:.1f} actual / {x2:.1f} expected'
    flags = str(pl.get('flags') or '')
    word = ''
    if 'box-score mirage' in flags or (not flags and a2 >= 8 and x2 < 5):
        word = 'mirage'
    elif 'quiet volume' in flags or (not flags and x2 >= 8 and a2 < 5):
        word = 'quiet volume'
    return txt + (f' &middot; <b>{word}</b>' if word else '')


def matchup_terms(src, week):
    """The matchup term for the week being priced (doc 468, finding 4.49). Reads form_2026.csv
    (every finished week's player rows, RB and TE) and sched_2026.csv (who played whom, and who
    plays whom in `week`). Returns {'soft': {(defense, pos): centred points allowed per game},
    'opp': {team: opponent in `week`}, 'weeks': {(defense, pos): weeks of record}} or {} when
    either file is missing or no defense has MATCHUP_MIN_WEEKS of record yet. A team absent from
    the week's schedule rows is on bye and has no opponent."""
    fp, sp = os.path.join(src, 'form_2026.csv'), os.path.join(src, 'sched_2026.csv')
    if not (os.path.exists(fp) and os.path.exists(sp)) or not week:
        return {}
    opp_by = {}                                   # (week, team) -> opponent
    with open(sp, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            try:
                opp_by[(int(r['week']), team_key(r['team']))] = team_key(r['opp'])
            except (KeyError, ValueError):
                continue
    allowed = collections.defaultdict(float)      # (defense, pos) -> points
    weeks = collections.defaultdict(set)          # (defense, pos) -> finished weeks faced
    with open(fp, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            try:
                w, pos = int(r['week']), (r.get('pos') or '').strip()
                pts = float(r.get('half_ppr') or 0)
            except (KeyError, ValueError):
                continue
            if w < 1 or w >= int(week) or pos not in MATCHUP_COEF:
                continue
            if str(r.get('in_progress') or '0').strip() == '1':
                continue
            d = opp_by.get((w, team_key(r.get('team'))))
            if not d:
                continue
            allowed[(d, pos)] += pts
            weeks[(d, pos)].add(w)
    soft = {}
    for pos in MATCHUP_COEF:
        apg = {d: allowed[(d, p)] / len(weeks[(d, p)])
               for (d, p) in weeks if p == pos and len(weeks[(d, p)]) >= MATCHUP_MIN_WEEKS}
        if not apg:
            continue
        mean = sum(apg.values()) / len(apg)
        for d, v in apg.items():
            soft[(d, pos)] = v - mean
    if not soft:
        return {}
    return {'soft': soft, 'opp': {t: o for (w, t), o in opp_by.items() if w == int(week)},
            'weeks': {k: len(v) for k, v in weeks.items()}}


def matchup_text(pl, mu):
    """'matchup vs DEN +0.4' for an RB or TE whose opponent this week has four weeks of record;
    '' for every other man, for a bye, and when the term was not built. The number is the
    coefficient times the centred points-allowed term, in points a week. Display only."""
    if not mu:
        return ''
    pos = (pl.get('pos') or '').strip()
    if pos not in MATCHUP_COEF:
        return ''
    opp = mu['opp'].get(team_key(pl.get('tm')))
    if not opp or (opp, pos) not in mu['soft']:
        return ''
    adj = round(MATCHUP_COEF[pos] * mu['soft'][(opp, pos)], 1)
    return f'matchup vs {E(opp)} {"+" if adj >= 0 else "&minus;"}{abs(adj):.1f}'


def take_facts(m, seat_all, week=0):
    """The take contract's three checkable lines, printed beside a name in THE CALL (directive
    0.1(h); check_pages.py C6 reads them). Doc 443. Measured on 174 takes: one missing three or
    more of the five lines was corrected by its own author 44% of the time, two or fewer 21%.
    (a) VINTAGE: 'proj 10.3 a week' when he is on the projection alone, otherwise the measured
        rate with its games and the blend the page priced him on.
    (b) THE MAN AHEAD, for a running back: the job holder on his team from inherit_2026.csv, with
        last season's games and today's tag, or the words 'not checked' when no seat row exists.
    (c) A HELD INPUT: the last two games actual and expected (doc 438) when the form row has
        them; for a defense or a quarterback the pregame line when wire.py passed it; otherwise
        the words 'not held', because a blank reads as nothing to say and this says there was
        nothing to read. Display only: nothing here sorts, filters or prices."""
    row = m.get('row') or {}
    pos = m.get('pos', '')
    bits = []
    vint = str(row.get('vintage') or '')
    meas, g = row.get('measured'), row.get('measured_g')
    if isinstance(meas, (int, float)) and g:
        bits.append(f'{meas:.1f} this season ({int(g)} g), priced at {float(row.get("wk") or 0):.1f} a week')
    elif isinstance(row.get('proj_wk'), (int, float)):
        bits.append(f'proj {row["proj_wk"]:.1f} a week')
    elif vint == 'proj' and isinstance(row.get('wk'), (int, float)):
        bits.append(f'proj {row["wk"]:.1f} a week')
    else:
        bits.append('proj, rate not read')
    if pos == 'RB' and m.get('ahead'):
        bits.append(m['ahead'])              # doc 451: an open job names the man who is out
    elif pos == 'RB':
        seat = next((r for r in (seat_all or []) if (r.get('team') or '') == (m.get('tm') or '')), None)
        if seat and seat.get('holds_the_job'):
            g25 = str(seat.get('starter_g25') or '').strip()
            tag = str(seat.get('live_tag') or '').strip()
            ahead = f'behind {E(seat["holds_the_job"])}'
            if g25:
                ahead += f', played {g25} of 17 last season'
            ahead += f', {tag.lower()} now' if tag and tag.upper() != 'ACTIVE' else ', no injury tag today'
            bits.append(ahead)
        else:
            bits.append('man ahead not checked')
    held = last_two_text(row)
    if not held and pos == 'D/ST' and isinstance(row.get('opp_total'), (int, float)):
        held = f'opponent total {row["opp_total"]:.1f} on the line, {E(row.get("opp") or "")}'.rstrip(', ')
    if not held and pos == 'QB' and isinstance(row.get('own_total'), (int, float)):
        held = f'own total {row["own_total"]:.1f} on the line'
    bits.append(held or 'last two games not held')
    return ' &middot; '.join(bits)


def vintage_block(roster, freerows, src):
    """[doc 409] THE PAGE PRINTS ITS OWN DISAGREEMENT WITH THE SEASON.

    check_vintage.py has computed this every day since doc 373 and written it to ff_log.txt, a
    file nobody opens, about a page that said nothing. Matt, 24 Sept: he wants the projection and
    this season in ONE place, "so that I'm not sourcing it in two places ... I'll also be able to
    fact check your numbers in real time so if I know something is off I know something wasn't
    updated."

    season_actual() is IMPORTED, never reimplemented: two functions claiming one number is the
    defect in 0.5(c)4, and this page would be the second claimant.
    """
    act = season_ppg_keyed(src)       # section 3's key, the same join rates() makes (doc 442)
    if not act:
        return ''
    rows, seen = [], set()
    for p_ in list(roster) + list(freerows):              # roster FIRST: a man he owns is "yours"
        nm = p_.get('name')
        if nm in seen:
            continue                                      # a stale wire can list a man he now owns
        hit = form_lookup(act, nm, p_.get('pos'), p_.get('tm'))
        if not hit or not p_.get('wk'):
            continue
        seen.add(nm)
        ppg, games = hit[0], hit[1]
        gap = ppg - p_['wk']
        if abs(gap) >= 4.0:                               # a starter's week, check_vintage's bar
            rows.append((abs(gap), nm, p_['wk'], ppg, games, gap,
                         'yours' if p_ in roster else 'free'))
    if not rows:
        return ''
    rows.sort(reverse=True)
    body = ''.join(
        f'<tr><td>{E(nm)}</td><td class="meta">{who}</td><td>{shown:.1f}</td>'
        f'<td><b>{ppg:.1f}</b></td><td class="meta">{games}</td>'
        f'<td class="{"up" if gap > 0 else "down"}">{gap:+.1f}</td></tr>'
        for _a, nm, shown, ppg, games, gap, who in rows[:14])
    return (
        '<div class="costbox"><h3>Where this page disagrees with the season</h3>'
        '<p>Page rate against this season&rsquo;s average (skill positions). Believe the '
        'season.</p>'
        '<table><tr><th scope="col">player</th><th scope="col"></th>'
        '<th scope="col">page</th><th scope="col">this season</th>'
        '<th scope="col">games</th><th scope="col">gap</th></tr>'
        f'{body}</table></div>')


def _clip(txt, n=150):
    """First sentence, or n characters, whichever is shorter. The full text rides in the cell's
    title attribute, so nothing is lost and no cell can widen the table past the viewport."""
    t = ' '.join((txt or '').split())
    if len(t) <= n:
        return t
    cut = t[:n]
    dot = cut.rfind('. ')
    return (cut[:dot + 1] if dot > 60 else cut.rstrip() + '\u2026')


def load_news(src):
    """[doc 412] news_2026.csv -> lookups by espn_id AND by (name, pos, team).

    Built by build_news.py off ESPN's public injuries feed. Two keys because that feed carries no
    athlete id field: the id is extracted from the athlete's own links href where one exists, and
    section 3's stated fallback, name + position + team, covers the rest. Never a bare name join.

    Missing file is NOT an error. It means build_news.py has not run, and the page says so where
    the note would have been rather than printing a confident blank (0.2).
    """
    path = os.path.join(src, 'news_2026.csv')
    if not os.path.exists(path):
        return {}, {}, 'news_2026.csv is missing -- run py build_news.py'
    by_id, by_key = {}, {}
    try:
        with open(path, encoding='utf-8-sig', newline='') as fh:
            for r in csv.DictReader(fh):
                if r.get('espn_id'):
                    by_id[str(r['espn_id']).strip()] = r
                by_key[(norm_name(r.get('player')), (r.get('pos') or '').upper(),
                        team_key(r.get('team')))] = r
    except OSError as exc:
        return {}, {}, f'news_2026.csv could not be read: {exc}'
    return by_id, by_key, ''


def news_note(pl, by_id, by_key):
    """One short clause for a player, or ''. Status, what it is, and when he is due back."""
    r = by_id.get(str(pl.get('espn_id') or '')) or by_key.get(
        (norm_name(pl.get('name')), (pl.get('pos') or '').upper(), team_key(pl.get('tm'))))
    if not r:
        return ''
    # [doc 414] Belt and braces with build_news.py's own filter: an Active man with no injury
    # is not news, and the page said "Active" in red beside three healthy men before this existed.
    _st, _inj = (r.get('status') or '').strip(), (r.get('injury') or '').strip()
    if _st.lower() in ('active', '') and not _inj and not r.get('return_date'):
        return ''
    bits = [b for b in (_st, _inj) if b]
    _d = (r.get('detail') or '').strip()
    if _d and _d.lower() not in ('not specified', 'unspecified'):
        bits.append(_d.lower())
    if r.get('return_date'):
        bits.append('back ' + r['return_date'][5:])
    return ', '.join(bits)


def week_points(players, w):
    """Best legal nine for week w. Single-position slots first, then FLEX from what is left --
    optimal here because FLEX is a superset of RB/WR/TE and every other slot is one position."""
    avail = collections.defaultdict(list)
    for p in players:
        if p['bye'] != w and p['wk'] > 0:
            avail[p['pos']].append(p['wk'])
    for k in avail:
        avail[k].sort(reverse=True)
    used, total, empty = collections.Counter(), 0.0, []
    for label, pos in SLOTS:
        if label == 'FLEX':
            continue
        pool = avail.get(pos, [])
        i = used[pos]
        if i < len(pool):
            total += pool[i]
            used[pos] += 1
        else:
            empty.append(label)
    best = 0.0
    for pos in FLEXABLE:
        pool = avail.get(pos, [])
        i = used[pos]
        if i < len(pool):
            best = max(best, pool[i])
    if best > 0:
        total += best
    else:
        empty.append('FLEX')
    return total, empty


def season(players):
    return sum(week_points(players, w)[0] for w in WEEKS)


def bar_grid(roster):
    """The rate a NEW player at each position must beat to change the nine, week by week.
    Bisection against the same lineup function, so the grid cannot drift from the model."""
    out = {}
    for pos in POS:
        out[pos] = {}
        for w in WEEKS:
            lo, hi = 0.0, 45.0
            base = week_points(roster, w)[0]
            for _ in range(45):
                mid = (lo + hi) / 2.0
                cand = {'name': 'X', 'pos': pos, 'tm': '', 'bye': 0, 'wk': mid}
                if week_points(roster + [cand], w)[0] > base + 0.0005:
                    hi = mid
                else:
                    lo = mid
            out[pos][w] = round(hi, 1)
    return out


def _f(v, d=None):
    try:
        return float(v)
    except (TypeError, ValueError):
        return d


def first_material_week(wkp, frac=0.10):
    """The first week this man is actually FOR (doc 407).

    `when` used to be the first week clearing a 0.049 floor, which is epsilon. Harrison Mevis beat
    the kicker Matt owns by 0.3 a week on a preseason projection and by 9.4 in week 8, when that
    kicker is on bye. Thirteen weeks cleared 0.049, so `when` came back 1, the week-8 bye cover
    walked through the week+2 calendar guard at line ~2033, and a hole five weeks out was ranked
    the number one pickup of the week. Matt: "It's telling me to pick up a kicker even though my
    current doesn't have a bye until week 8 ... Completely nuts."

    A week counts only if the gain is a material share of his own best week, which is scale free
    and needs no tuned constant. JUDGEMENT CALL, not a measurement: `frac` is set at a tenth
    because a tenth of a peak week is plainly noise, and nothing here measured it."""
    gains = {w: (wkp.get(w) or 0.0) for w in WEEKS}
    peak = max(gains.values()) if gains else 0.0
    if peak <= 0.049:
        return 0
    floor = max(0.05, frac * peak)
    mat = [w for w in WEEKS if gains[w] >= floor]
    return min(mat) if mat else 0


def price(cand, bar):
    """The calculation, spelled out: per-week gain and the season total."""
    wk, tot = {}, 0.0
    for w in WEEKS:
        if w == cand['bye']:
            wk[w] = None
            continue
        g = max(0.0, cand['wk'] - bar[cand['pos']][w])
        wk[w] = round(g, 1)
        tot += wk[w]
    return wk, round(tot, 2)


def drop_costs(roster, cap=15, used=None):
    """What each rostered body is actually worth to the starting nine, doc 240's method:
    the fourteen-week total with him, minus the same total without him. The cheapest of these
    IS the price of a lottery ticket -- there is nothing else you give up.

    `used` is the TRUE number of roster seats occupied, which is NOT len(roster) whenever ESPN
    publishes no projection for somebody he owns -- an injured man carries proj 0 and rates()
    drops him. Priced off len(roster) this table invented a free seat that does not exist and
    told him a lottery ticket was free when it would cost a drop (doc 281). Pass the count from
    the roster READ, never from the rows that survived pricing."""
    base = season(roster)
    out = []
    for i, p in enumerate(roster):
        out.append((round(base - season(roster[:i] + roster[i + 1:]), 1), p))
    out.sort(key=lambda x: (x[0], x[1].get('wk', 0)))
    if (len(roster) if used is None else used) < cap:   # an open spot costs nothing at all
        out.insert(0, (0.0, {'name': 'the open spot', 'pos': '', 'tm': '', 'bye': 0, 'wk': 0.0}))
    return out


def bet(cand, bar, hit_rate, weeks_of_hit):
    """Price the SIGNAL rather than the man: what he is worth in the weeks he is the player the
    screen says he might be. Same arithmetic as price(), run at the measured hit rate instead of
    his own, then charged for the measured number of weeks a hit actually lasted."""
    probe = dict(cand)
    probe['wk'] = hit_rate
    wk, _ = price(probe, bar)
    live = [v for v in wk.values() if v is not None]
    per = (sum(live) / len(live)) if live else 0.0
    return wk, round(per * weeks_of_hit, 1)


def load_screened(src):
    """Every screened row in the NEWEST wire file, whether or not it survives to the bet table.

    THE DEFECT THIS EXISTS FOR (doc 277): Ricky Pearsall carried BOTH signals -- a first-round pick
    and three of three, the only free player with both -- and never appeared on this page. ESPN gives
    an injured-reserve player a BLANK projection, rates() drops anything at or below zero, and he was
    gone with no error. A row that must be on the page and is not is the one thing no guard here
    covered, so the section now names anybody the pricing dropped instead of quietly shortening.
    """
    import glob as _glob
    hits = sorted(_glob.glob(os.path.join(src, 'WIRE_*.csv')))
    if not hits:
        return [], 'no WIRE_*.csv in Source'
    with open(hits[-1], newline='', encoding='utf-8-sig') as fh:
        rows = [r for r in csv.DictReader(fh) if (r.get('screen') or '').strip()]
    return rows, ''


def load_cards(src):
    """Source\\cards_2026.csv -- dated news and the two cases, written by hand and never computed.
    Returns ([], why) when it is missing; the page says so rather than dropping the section.

    AND EVERY CARD IS CHECKED AGAINST THE NEWEST WIRE (doc 285). The cards are hand-written and the
    pool is not: on 2026-09-10 two of the six -- Jordan James and Brian Robinson Jr. -- were claimed
    by other managers during the day, and nothing on the page would have said so. A card that
    recommends a rostered player is the missing-row check inverted: the row that should NOT be there.
    A card whose man is gone is marked `gone`, never silently dropped, because "he was on here
    yesterday and now he is not" is itself information.
    """
    import glob as _glob
    p = os.path.join(src, 'cards_2026.csv')
    if not os.path.exists(p):
        return [], 'cards_2026.csv is missing, not empty'
    with open(p, newline='', encoding='utf-8-sig') as fh:
        cards = list(csv.DictReader(fh))
    wires = sorted(_glob.glob(os.path.join(src, 'WIRE_*.csv')))
    if not wires:
        for c in cards:
            c['gone'] = ''
        return cards, 'no WIRE file to check the cards against, so none is marked claimed'
    with open(wires[-1], newline='', encoding='utf-8-sig') as fh:
        wrows = list(csv.DictReader(fh))
    by_id = {str(r.get('espn_id', '')).strip(): r for r in wrows}
    # SECTION 3: id first. A card with no id is matched on name + position + team, never less --
    # a blank id used to read as "not on the wire" and marked the man claimed whether he was or not.
    by_npt = {(norm_name(r.get('player')), (r.get('pos') or '').strip().upper(),
               team_key(r.get('team'))): r for r in wrows}
    n, mism = 0, []
    for c in cards:
        cid = str(c.get('espn_id', '')).strip()
        w = by_id.get(cid) if cid else None
        if w is None:
            # AN ID THAT MATCHES NOBODY IS NOT PROOF HE WAS CLAIMED (doc 291, A16). The cards are typed
            # by hand; a wrong digit used to mark a free man gone and, since A15, leave him off the page.
            w = by_npt.get((norm_name(c.get('player')), (c.get('pos') or '').strip().upper(),
                            team_key(c.get('tm'))))
            if w is not None and cid:
                mism.append(f"{c['player']} (card says {cid}, ESPN says {w.get('espn_id')})")
        c['tm'] = team_key(c.get('tm')) or c.get('tm', '')
        c['gone'] = '' if w else 'yes'
        c['espn_status'] = ((w or {}).get('status') or '').strip().upper()
        n += 1 if c['gone'] else 0
    why = '' if not n else (f'{n} of {len(cards)} carded players are no longer free and are left '
                            f'off the page: ' + ', '.join(c['player'] for c in cards if c['gone']))
    if mism:
        why = '; '.join(x for x in (why, 'card ids that match nobody, matched on name, position and '
                                    'team instead -- fix cards_2026.csv: ' + ', '.join(mism)) if x)
    return cards, why


def playoff_odds(src, lift=5.0):
    """[1 Oct, doc 469] His simulated odds of a top-six finish on the weeks left, and the same with
    `lift` points a week added, off research\\playoff_odds.py (doc 464: Brier 0.23 at week 4 against a
    coin flip's 0.25 and the standings' 0.38). Returns (odds, odds_with_lift, lift) or None when the
    schedule file or the simulator is absent. The lane's placement reads this (doc 464's convexity
    test: a ticket beats the same points spread evenly only under about 30%)."""
    try:
        _rd = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research')
        if _rd not in sys.path:
            sys.path.insert(0, _rd)
        import playoff_odds as _po
        r = _po.live_numbers(src, lift)
    except Exception as exc:                       # the page never dies for a missing simulator
        print(f'  playoff odds not computed ({type(exc).__name__}: {exc})')
        return None
    if not r:
        return None
    return (float(r['base'][r['me']]), (float(r['up']) if r['up'] is not None else None), lift)


def load_standings(src, odds=None):
    """[30 Sept, doc 456] Source\\standings_2026.csv (wire.py writes it off mTeam every run): one sentence
    on where he stands, or '' when the file is absent or has no row of his. Numbers are ESPN's own
    (points for is the sum of his weekly scores), so no vintage word is needed."""
    p = os.path.join(src, 'standings_2026.csv')
    if not os.path.exists(p):
        return ''
    rows = []
    with open(p, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            rows.append(r)
    me = next((r for r in rows if (r.get('mine') or '').strip() == 'yes'), None)
    if not me or not rows:
        return ''
    def _f(x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return None
    pf = sorted((v for v in (_f(r.get('points_for')) for r in rows) if v is not None), reverse=True)
    mine_pf = _f(me.get('points_for'))
    seed = me.get('playoff_seed') or '?'
    rec = f"{me.get('wins') or '?'}-{me.get('losses') or '?'}" + (f"-{me['ties']}" if str(me.get('ties') or '0') not in ('', '0') else '')
    out = f"where you stand: <b>{E(rec)}</b>, seed <b>{E(str(seed))}</b> of {len(rows)}"
    if mine_pf is not None and pf:
        med = pf[len(pf) // 2] if len(pf) % 2 else (pf[len(pf) // 2 - 1] + pf[len(pf) // 2]) / 2
        rank_pf = 1 + sum(1 for v in pf if v > mine_pf)
        sixth = pf[5] if len(pf) >= 6 else pf[-1]
        out += (f"; <b>{mine_pf:.0f}</b> points for, {rank_pf}{'st' if rank_pf == 1 else 'nd' if rank_pf == 2 else 'rd' if rank_pf == 3 else 'th'} "
                f"of {len(pf)} (league median {med:.0f}, the sixth-best total {sixth:.0f})")
    if odds:
        # [doc 469] the simulated number replaces "ESPN projects you to finish N", which was a rank with
        # no probability behind it; this is the number the posture rule reads (0.3: dollars come from
        # finishing position, and the top six is the gate).
        out += (f"; <b>{odds[0]:.0%}</b> to make the top six, simulated on the weeks left"
                + (f" (+{odds[2]:.0f} a week would make it {odds[1]:.0%})" if odds[1] is not None else ''))
    else:
        pr = me.get('projected_rank')
        if pr:
            out += f"; ESPN projects you to finish {E(str(pr))}"
    return out + ' (' + E(me.get('asof') or '') + ')'


def load_todo(src, cap=6):
    """Matt\'s own open items, straight off Source\\matt_todo.txt (doc 295).

    His instruction, 2026-09-11: "i don\'t want to be all over the place when the enrichment could be
    done on the main strategy page." The file stays the record; this puts the OPEN lines where the
    decision is.

    2026-09-17: "the to do list is buried for me. Please put a link here." It was: this returned
    SIX of forty-three open items, first line only, into a box at the BOTTOM of section 0 whose
    own CSS clipped every line at the box width. Three separate ways to lose a line. It now
    returns EVERY open item with its indented notes, and the caller decides what to show and
    what to link to. `cap` is kept for the in-page box and is no longer the whole of the list.
    """
    items, _ = load_todo_all(src)
    # RUN-FIRST, not file order. The box holds six of forty-three, so the six it holds should be
    # the ones with a command in them; file order put two commands at 12 and 13 and showed
    # neither. Ties keep the order he wrote them in.
    rank = {'run': 0, 'do': 1, 'later': 2, 'read': 3}
    idx = sorted(range(len(items)), key=lambda i: (rank[items[i]['kind']], i))
    return [items[i]['title'] for i in idx][:cap]


# THE KIND IS READ OFF THE LINE, NOT GUESSED. Three buckets, in the order he would work them:
#   run  -- there is a command in it
#   do   -- a move, a claim, a deadline: something to act on with no command
#   read -- he marked it READ ONLY himself
_TODO_CMD = re.compile(r'(?:^|\s)(py|\.\\)\s*[\w\\./-]*\.?(?:py|bat)\b', re.I)


_TODO_WEEK = re.compile(r'^~?\s*week\s+\d', re.I)


def _todo_kind(title):
    """EVERY RULE HERE IS MECHANICAL, because a judgement call I make on his own list is a
    judgement he cannot audit. Four buckets, read off the words he wrote:
      run   -- the line contains a command
      later -- it is filed under a future week
      read  -- he marked it READ ONLY / NOTHING TO RUN, or it is a standing DO NOT
      do    -- everything else
    The first version had only three and put thirty-two of forty-three items in `do`, which is
    a label that sorts nothing."""
    t = (title or '').strip()
    u = t.upper()
    if _TODO_CMD.search(t):
        return 'run'
    if _TODO_WEEK.match(t):
        return 'later'
    if (re.match(r'^\s*READ[ _-]?ONLY\b', t, re.I) or 'READ ONLY' in u
            or 'NOTHING TO RUN' in u or u.startswith('DO NOT')):
        return 'read'
    return 'do'


def load_todo_all(src):
    """(open items, done items) from matt_todo.txt, each {'title','note','kind'}.

    A `[ ]` or `[x]` line opens an item; every following line that is blank, indented, or a
    comment belongs to it, and the next `[` line ends it. The note is kept verbatim -- it is
    where he put the reason -- and is escaped at render, never here.
    """
    p = os.path.join(src, 'matt_todo.txt')
    if not os.path.exists(p):
        return [], []
    op, dn, cur = [], [], None
    for raw in open(p, encoding='utf-8', errors='replace'):
        ln = raw.rstrip('\n')
        t = ln.strip()
        head = None
        if t.startswith('[ ]'):
            head = ('open', t[3:].strip())
        elif t[:3].lower() == '[x]':
            head = ('done', t[3:].strip())
        if head is not None:
            title = head[1].split('#')[0].strip() or head[1].strip()
            cur = {'title': title, 'note': [], 'kind': _todo_kind(title)}
            (op if head[0] == 'open' else dn).append(cur)
            continue
        if cur is not None:
            # the file's own format: notes are indented and usually start with #
            if not t:
                if cur['note'] and cur['note'][-1] != '':
                    cur['note'].append('')
                continue
            if ln[:1] in (' ', '\t'):
                cur['note'].append(t.lstrip('#').strip())
            else:
                # A LEFT-MARGIN LINE ENDS THE ITEM, `#` OR NOT. The file's section headers are
                # left-margin comments ("# ==== RUN THESE ===="), so treating any `#` line as a
                # note hung the header off whichever item happened to precede it.
                cur = None
    for lst in (op, dn):
        for it in lst:
            while it['note'] and it['note'][-1] == '':
                it['note'].pop()
    return op, dn


TODO_PAGE = 'MY_TODO.html'

CLOCK_URL = 'https://claude.ai/artifact/NpLWo1xBiWRG4bztW7L5xw'
POCKET_URL = 'https://claude.ai/artifact/1iFS2iFyDACxRknmbJiFNT'
TAKES_URL = 'https://claude.ai/artifact/BwUBENtMAZzTdjfgq7kqCJ'

# MATT, 2026-09-17: "link the commands page on the todo list so i don't need a bunch of
# bookmarks?" So the to-do page is the hub: his list, the commands, and every page he opens,
# behind ONE bookmark. Every path below was checked against the folder before it was written
# (0.5(c)4) -- a link to a script that is not there is the same defect as a row that is not on
# the printed page.
TODO_LINKS = [
    ('WEEK_SHEET.html', 'the week sheet', 'the bar, every free body priced, and what to do'),
    ('THE_WEEKLY_WIRE.html', 'the wire', 'who is available, the stash list, the weeks ahead'),
    ('LINEUP_CHECK.html', 'lineup check', 'anyone in your nine who is out, doubtful or on bye'),
    ('../COMMANDS.html', 'the commands page', 'the same list as below, on its own page, with '
                                              'what each batch file actually runs and when it '
                                              'fires'),
    (CLOCK_URL, 'the roster clock', 'what is left on the wire week by week, how the fifteen spots '
                                    'should change, and which positions are worth holding two of'),
]

# ONE COMMAND DOES EVERYTHING, and it already existed: ff.bat. A second batch file for one job is
# doc 146's after_pull.bat defect, so ff.bat was EXTENDED rather than duplicated.
TODO_CMDS = [
    ('ff.bat', 'everything, in order',
     'Double-click it. Every step in order, then the checks; on the Tuesday task, ESPN\u2019s '
     'projections too. It opens the week sheet only if the page changed.', True),
    ('py wire.py --html', 'the wire and the week sheet',
     'What ff.bat runs in the middle. Use it when you only want the two pages.', False),
    ('py lineup.py --html', 'is anyone in my nine not playing',
     'Thursday evening and Sunday late morning, after the inactives.', False),
    ('done "<some words>"', 'tick something off THIS list',
     'Matches the words against the open items (exactly one, or it refuses), ticks it and rebuilds '
     'this page. `done --list` numbers them; `done --undo "..."` puts one back.', True),
    ('py todo_page.py', 'rebuild this page',
     'No network, no ESPN. Reads Source\\matt_todo.txt and rewrites this page and the '
     'sheet\u2019s link.', False),
    ('py check_kit.py', 'are the shipped files the ones I think',
     'Names, byte counts and hashes for the whole tree. Run it after anything of mine lands.',
     False),
    ('py research\\wk1\\build_form.py', 'refresh the week-by-week usage file',
     'ff.bat runs it at the top of every run. By hand only if the log says FORM FILE NOT '
     'REBUILT.', False),
    ('py waivers.py --live', 'pull this season\u2019s transactions',
     'Needs your ESPN cookies. Writes waiver_report_2026.csv.', False),
    ('py research\\redteam\\redteam_controls.py', 'the negative controls',
     'Every guard shown failing on the defect it was built for. Optional, and slow.', False),
    ('py research\\close_check.py', 'what is actually still open',
     'Sorts every OPEN ledger row into candidate-closed / still-there against the shipping '
     'files. It names candidates; it never closes one.', False),
]


# ============================================================================
# ONE NAV, EMITTED IN ONE PLACE, USED BY EVERY PAGE.
#
# Matt, 2026-09-19, after testing the previous batch: "i don't wish to open a new tap to return
# back to the home page, instead the homepage should be launched in place of the commands page.
# The home page should act like a home page", and "i prefer to replace the page instead of
# loading a new page... Otherwise i'll end up with a clutter of pages open in Google Chrome."
#
# So NO target="_blank" anywhere. A middle click or a ctrl-click still opens a new tab, which is
# the browser's job and HIS choice to make per link. Forcing it is also the published guidance
# (WCAG 2.2 success criterion 3.2.5 Change on Request; Nielsen Norman Group on forced new
# windows), so this is not a house style, it is the standard practice and the previous batch
# differed from it by accident. Doc 372.
#
# WHY THIS IS A FUNCTION AND NOT FIVE COPIES: five pages carrying five hand-written bars is a
# second NAME for one JOB, which 0.5(c)4 names as the same defect as two files claiming one
# number. THE_WEEKLY_WIRE.html and LINEUP_CHECK.html had no bar at all, which is how they ended
# up as dead ends Matt had to back out of.
HOME = 'WEEK_SHEET.html'
PAGES = [
    ('WEEK_SHEET.html', 'week sheet'),
    ('MY_TODO.html', 'to-do list'),
    ('THE_WEEKLY_WIRE.html', 'the wire'),
    ('LINEUP_CHECK.html', 'lineup check'),
    ('../COMMANDS.html', 'commands'),
    # [doc 429] The Roster Clock is hosted, not a file on the drive, so it is the one absolute
    # href in this list and `at_root` must not prefix it with Source/.
    (CLOCK_URL, 'roster clock'),
    # [doc 430] AND THE OTHER TWO PUBLISHED PAGES, because this bar is the only hub that can point
    # BOTH ways. A browser refuses a file:// link from an https page, so nothing on the web can
    # link back to this PC. The local bar therefore carries everything; the online bar carries
    # only the online set and names the folder in text.
    (POCKET_URL, 'pocket sheet'),
    (TAKES_URL, 'the takes'),
]


def page_bar(current='', at_root=False, labels=None):
    """The bar every page carries. `current` is the page's own filename, and it renders as
    plain text rather than a link so a page never links to itself.

    at_root=True is for 2026\\COMMANDS.html, which sits one folder ABOVE the others, so every
    href needs the Source/ prefix and its own entry loses the ../ .
    """
    labels = labels or {}
    out = []
    for href, label in PAGES:
        if href.startswith('http'):
            h = href
        elif at_root:
            h = 'COMMANDS.html' if href == '../COMMANDS.html' else 'Source/' + href
        else:
            h = href
        text = labels.get(href, label)
        if href == current:
            out.append('<span class="todolink here">%s</span>' % text)
        elif href == HOME:
            out.append('<a class="todolink home" href="%s">&larr; %s</a>' % (h, text))
        else:
            out.append('<a class="todolink" href="%s">%s</a>' % (h, text))
    return ('<p class="jump pagebar"><span class="pbl">pages</span>' + ''.join(out) + '</p>')


# For the two pages that do not use CSS above: wire.py and lineup.py carry their own stylesheet,
# so they append this rather than inheriting it.
PAGEBAR_CSS = """
p.jump.pagebar{margin:16px 0 18px;display:flex;flex-wrap:wrap;align-items:baseline;gap:0 4px;
font-family:Helvetica Neue,Arial,sans-serif}
p.pagebar .pbl{text-transform:uppercase;letter-spacing:.14em;font-size:11px;color:#6b6b66;
margin-right:8px}
p.pagebar a.todolink,p.pagebar span.todolink{display:inline-block;text-transform:uppercase;
letter-spacing:.07em;font-size:11.5px;margin:0 14px 0 0;text-decoration:none;padding-bottom:1px}
p.pagebar a.todolink{color:#3A63A8;border-bottom:1px solid #3A63A8}
p.pagebar a.todolink.home{font-weight:700}
p.pagebar span.here{color:#6b6b66;border-bottom:none}
@media (prefers-color-scheme:dark){p.pagebar a.todolink{color:#5E94DC;border-bottom-color:#5E94DC}
p.pagebar .pbl,p.pagebar span.here{color:#8E999F}}
"""


def write_todo_page(src, stamp=None, team_name=''):
    """Renders matt_todo.txt as a page beside the week sheet, and returns (path, n_open).

    THE MISSING-ROW CHECK IS INSIDE THE BUILDER (0.5(c)5). It counts the `[ ]` lines in the file
    itself and refuses to write a page carrying a different number, because the failure this
    replaces was a list that silently showed six of forty-three.
    """
    op, dn = load_todo_all(src)
    p = os.path.join(src, 'matt_todo.txt')
    if not os.path.exists(p):
        return '', 0
    raw_open = sum(1 for ln in open(p, encoding='utf-8', errors='replace')
                   if ln.strip().startswith('[ ]'))
    if raw_open != len(op):
        raise ValueError('todo page: parsed %d open items, the file has %d -- refusing to write '
                         'a list that is missing rows' % (len(op), raw_open))
    stamp = stamp or dt.date.today().strftime('%d %B %Y')
    order = {'run': 0, 'do': 1, 'later': 2, 'read': 3}
    label = {'run': 'run this', 'do': 'do this', 'later': 'a later week',
             'read': 'read only'}
    op_sorted = sorted(range(len(op)), key=lambda i: (order[op[i]['kind']], i))

    def block(it, done=False):
        note = ''
        if it['note']:
            para, buf = [], []
            for n in it['note']:
                if n:
                    buf.append(n)
                elif buf:
                    para.append(buf); buf = []
            if buf:
                para.append(buf)
            body = ''.join('<p>' + '<br>'.join(E(x) for x in blk) + '</p>' for blk in para)
            # A LONG REASON IS COLLAPSED, NEVER CUT. The defect being replaced lost text silently;
            # a closed <details> keeps every word and says how much is behind it.
            if len(it['note']) > 12:
                note = (f'<details class="tn"><summary>the reasoning &mdash; '
                        f'{len(it["note"])} lines</summary>{body}</details>')
            else:
                note = f'<div class="tn">{body}</div>'
        return (f'<li class="k-{it["kind"]}{" done" if done else ""}">'
                f'<span class="tag">{label[it["kind"]]}</span>'
                f'<span class="tt">{E(it["title"])}</span>{note}</li>')

    counts = collections.Counter(it['kind'] for it in op)
    short = {'run': 'to run', 'do': 'to do', 'later': 'for a later week', 'read': 'to read'}
    head = ' &middot; '.join(f'{counts[k]} {short[k]}'
                             for k in ('run', 'do', 'later', 'read') if counts[k])
    jump = ''.join(f'<a href="#{k}"><span class="n">{counts[k]}</span>{label[k]}</a>'
                   for k in ('run', 'do', 'later', 'read') if counts[k])
    jump += '<a href="#cmds"><span class="n">%d</span>commands</a>' % len(TODO_CMDS)
    blurb = {'run': 'A command, in a shell in the Scripts folder. Nothing here needs me.',
             'do': 'A move, a claim, a message, a deadline. No command attached.',
             'later': 'Filed under a week that has not arrived. Nothing to do today.',
             'read': 'You marked these read-only, or they are a standing DO NOT.'}
    body = ''
    for k in ('run', 'do', 'later', 'read'):
        rows = [it for it in op if it['kind'] == k]
        if not rows:
            continue
        body += (f'<h2 id="{k}"><span class="n">{counts[k]}</span>{label[k]}</h2>'
                 f'<p class="lede">{blurb[k]}</p>'
                 f'<ol class="todopage">{"".join(block(it) for it in rows)}</ol>')
    donehtml = ''
    if dn:
        donehtml = ('<details class="donewrap"><summary>' + str(len(dn)) +
                    ' already done &mdash; kept so a question about whether something ran has an '
                    'answer</summary><ol class="todopage">'
                    + ''.join(block(it, done=True) for it in dn) + '</ol></details>')
    # Matt, 2026-09-19: "When launched to the to-do list from the week sheet the page is
    # replaced with the to-do list with no link to go back to the week sheet." Both halves of his
    # fix are taken: every cross-page link opens in a new tab, AND the week sheet is named first
    # in a bar at the top of this page so there is always a way back.
    links = ''.join(
        f'<li><a href="{E(href)}">{E(name)}</a><span>{E(why)}</span></li>'
        for href, name, why in TODO_LINKS)
    backbar = page_bar(current=TODO_PAGE)
    cmds = ''.join(
        f'<li class="{"first" if first else ""}"><code>{E(cmd)}</code>'
        f'<span class="tt">{E(what)}</span><div class="tn"><p>{E(why)}</p></div></li>'
        for cmd, what, why, first in TODO_CMDS)
    ncmd = len(TODO_CMDS)
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Your to-do list &mdash; {stamp}</title><style>{CSS}{TODO_CSS}</style></head>
<body id="top"><div class="wrap">
<header><p class="kick">{E(team_name or 'Your team')} &middot; built {stamp}</p>
<h1>Your to-do list</h1>
<p class="dek">Yours: a command to run, a move to make, or something to read. Rewritten whenever an
item is added or closed. <strong>{len(op)} open</strong>{(' &mdash; ' + head) if head else ''}.</p>
{backbar}
</header>
<nav class="secnav" aria-label="sections of this page">{jump}
<a class="top" href="#top">top &uarr;</a></nav>
<div class="hub"><h4>every page, one bookmark</h4><ul>{links}</ul></div>
{body}
<h2 id="cmds"><span class="n">{ncmd}</span>Commands</h2>
<p class="lede"><strong>ff.bat is the only one you need most weeks.</strong> The others run from a
terminal in the Scripts folder.</p>
<ol class="todopage cmds">{cmds}</ol>
{donehtml}
</div></body></html>"""
    out = os.path.join(src, TODO_PAGE)
    tmp = out + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        fh.write(page)
    try:
        os.replace(tmp, out)
    except OSError:
        with open(out, 'w', encoding='utf-8') as fh:
            fh.write(page)
        try:
            os.remove(tmp)
        except OSError:
            pass
    return out, len(op)


# [doc 417] THE IR SLOT, AS A NUMBER ON THE PAGE RATHER THAN A RULE IN A FILE.
# Section 2 carries ESPN's sourced football rule (doc 394, read as page text):
#   * the slot ACCEPTS only a man whose status is Out (O) or Injured/Reserve (IR)
#   * a man ALREADY in the slot who is upgraded to Questionable or Doubtful is explicitly SAFE
#     -- he keeps the seat, claims still process, lineups still move
#   * only losing his designation ENTIRELY invalidates the roster and freezes the lineup
#   * a healthy man sitting in the slot BLOCKS every pending claim
#   * SSPD is never eligible in football
# THOSE ARE TWO DIFFERENT RULES AND CONFLATING THEM COSTS A PLAN. Matt, 24 Sept: "i can wait on
# Rico and put him on IR." Dowdle is QUESTIONABLE, and the rule that lets a man STAY after an
# upgrade is not the rule that lets him ENTER. The park is not available, and nothing on this
# page said so -- it lives in the directive, which is not what he reads on a Wednesday night.
# So the page computes it: who the slot will take TODAY, and what a park would be worth.
IR_SLOT = 21                       # ESPN lineup slot ids: 20 bench, 21 IR (section 2)
IR_TAKES = ('OUT', 'INJURY_RESERVE', 'INJURED_RESERVE', 'IR')
IR_SAFE_ONCE_IN = ('QUESTIONABLE', 'DOUBTFUL')
IR_SLOTS = 3                       # 2026_League_Settings.txt line 29, listed SEPARATELY from the 15


def ir_picture(src):
    """Who is parked, who the slot would take, and who it would refuse. Reads MY_ROSTER.csv.

    Returns {'parked': [(name, status)], 'eligible': [(name, status)],
             'refused': [(name, status)], 'free_slots': int, 'have_file': bool}.

    NOT YET OBSERVED, and named rather than assumed (0.5(a4)): this league's feed has only ever
    written ACTIVE and QUESTIONABLE into STATUS_LOG.csv, so the exact string ESPN sends for Out
    and for IR is unconfirmed here. IR_TAKES carries every spelling the API is documented to use
    and the match is case-folded, so a new spelling shows up as REFUSED rather than as a silent
    eligible -- the safe direction, because a wrong "you can park him" is a frozen lineup.
    """
    out = {'parked': [], 'eligible': [], 'refused': [], 'free_slots': IR_SLOTS, 'have_file': False,
           'parked_ids': set()}
    p = os.path.join(src, 'MY_ROSTER.csv')
    if not os.path.exists(p):
        return out
    out['have_file'] = True
    with open(p, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            name = (r.get('player') or '').strip()
            st = (r.get('status') or '').strip().upper().replace(' ', '_')
            try:
                slot = int(r.get('slot_id') or -1)
            except ValueError:
                slot = -1
            if slot == IR_SLOT:
                out['parked'].append((name, st))
                out['parked_ids'].add(str(r.get('espn_id') or '').strip())
            elif st in IR_TAKES:
                out['eligible'].append((name, st))
            elif st and st != 'ACTIVE':
                out['refused'].append((name, st))
    out['free_slots'] = max(0, IR_SLOTS - len(out['parked']))
    return out


def ir_box(view):
    """The IR seat in plain words. THE SCOPE RULE: what to DO first, then what it is. No rule
    numbers, no sources, no counts of anything -- those live in the docs and he can ask."""
    if not view or not view.get('have_file'):
        return ''
    parked, elig, refused = view['parked'], view['eligible'], view['refused']
    free = view['free_slots']
    if not parked and not elig and not refused:
        return ''

    lead, body, cls = '', [], 'box'

    if elig and free:
        who = ', '.join(E(n) for n, _ in elig)
        lead = f'Move {who} to injured reserve before you claim anyone.'
        body.append('That gives the seat back, so your next pickup does not cost a drop. '
                    'Do it before you enter the claim, not after.')
        cls = 'box good'
    elif elig and not free:
        who = ', '.join(E(n) for n, _ in elig)
        lead = f'{who} could go to injured reserve, but all three slots are full.'
        cls = 'box'
    else:
        lead = 'No one on your roster can be moved to injured reserve right now.'
        body.append('Every pickup costs a drop until that changes.')

    if refused:
        who = ', '.join(f'{E(n)} ({E(st.title().replace("_", " "))})' for n, st in refused)
        body.append(f'<b>{who}</b> cannot go in. The slot only takes a man listed Out or on '
                    f'injured reserve &mdash; questionable is not enough, however long he sits. '
                    f'Waiting for the designation to harden is the only way in.')

    if parked:
        safe, risky = [], []
        for n, st in parked:
            (safe if st in IR_SAFE_ONCE_IN or st in IR_TAKES else risky).append((n, st))
        if safe:
            who = ', '.join(f'{E(n)} ({E(st.title().replace("_", " "))})' for n, st in safe)
            _v = 'are already parked and stay parked' if len(safe) > 1 else 'is already parked and stays parked'
            body.append(f'{who} {_v}.')
        if risky:
            who = ', '.join(E(n) for n, _ in risky)
            _v = ('have no injury designation at all and are sitting' if len(risky) > 1
                  else 'has no injury designation at all and is sitting')
            body.append(f'<b>{who} {_v} in the '
                        f'injured-reserve slot.</b> That makes the roster invalid: your lineup is '
                        f'frozen until you cut someone, and no waiver claim you place will process '
                        f'until you do. Fix it before you enter a claim and before kickoff.')
            cls = 'box bad'

    return (f'<div class="{cls}"><h4>the injured-reserve seat</h4><p><b>{lead}</b> '
            + ' '.join(body) + '</p></div>')


def load_donot(src):
    """Players Matt has RULED OUT, in his own words, so the page cannot recommend one (doc 295).

    Two sources, both already maintained by hand for other reasons:
      * `matt_todo.txt` -- any open `[ ]` line beginning DO NOT, e.g.
        "DO NOT CLAIM BRENTON STRANGE.   # my second bad recommendation on him"
      * `cards_2026.csv` -- a card whose verdict begins DO NOT.
    The NAME is never parsed out of the sentence. The sentence is matched against names the page
    already knows, so a new verb ("do not stash", "do not start") can never silently drop a rule.
    Returns [(line, note)]; `donot_map` does the matching once the names are in hand.
    """
    out = []
    p = os.path.join(src, 'matt_todo.txt')
    if os.path.exists(p):
        for ln in open(p, encoding='utf-8', errors='replace'):
            t = ln.strip()
            if not t.startswith('[ ]'):
                continue
            body = t[3:].strip()
            if not body.upper().startswith('DO NOT'):
                continue
            head, _, note = body.partition('#')
            out.append((head.strip().rstrip('.'), note.strip()))
    # [doc 415] AND THE STANDING RULES BLOCK, WHICH IS NOT A CHECKBOX LIST.
    # This used to read only "[ ] DO NOT ..." lines. On 24 Sept matt_todo.txt was rewritten at
    # Matt's instruction -- 1,504 lines to 43 -- and his never-drop rules moved into a plain
    # "## STANDING RULES -- not tasks, do not tick" block, because a checkbox on a rule he never
    # ticks is exactly the clutter he asked me to remove. THE RULES WERE STILL THERE AND THIS
    # FUNCTION WENT BLIND TO THEM, so the page went straight back to offering Mike Washington Jr.
    # as a drop, which he has ruled out in those words. Tightening a file can break a reader of
    # it: when a format changes, grep every reader (3's merge-collision corollary).
    if os.path.exists(p):
        for ln in open(p, encoding='utf-8', errors='replace'):
            t = ln.strip()
            if t.startswith('[') or t.startswith('#') or not t:
                continue
            u = t.upper()
            if u.startswith('NEVER DROP') or u.startswith('DO NOT DROP') or u.startswith('DO NOT'):
                head, _, note = t.partition('#')
                out.append((head.strip().rstrip('.'), note.strip()))
    return out


def donot_map(rules, names):
    """{norm_name: (line, note)} for every known name that appears in a DO NOT line.

    Whole-token matching on the normalised name, never a substring: 'Dell' must not rule out
    'Dell Jr.' by accident and 'All' must not rule out half the board."""
    out = {}
    for line, note in (rules or []):
        hay = ' ' + norm_name(line) + ' '
        for nm in names:
            k = norm_name(nm)
            if k and f' {k} ' in hay:
                out[k] = (line, note)
    return out


def seat_odds(row, sc):
    """(odds, band, why) for one seat row -- the measured per-band P(the job opens), doc 343.

    THE FLAT 0.46 WAS THE POPULATION AVERAGE AND IT IS WHY THIS TABLE COULD ONLY RANK THE JOB.
    Every seat got the same number, so the only thing that varied between rows was the size of
    the backfield; the page said so in its own words. The share is preseason-knowable from week
    one, and on 126 team-seasons it orders the odds 0.48 / 0.44 / 0.53 / 0.64.

    A MISSING SHARE FALLS BACK TO THE FLAT RATE AND SAYS SO. A man with no week-1 line is no
    information, and guessing his band would be worse than the average it replaces (section 3).
    """
    flat = sc.get('p_opens')
    table = sc.get('p_opens_by_band') or {}
    b = (row.get('wk1_band') or '').strip()
    # A SHARE OF EXACTLY ZERO IS OUTSIDE THE FITTED POPULATION, NOT THE BOTTOM OF IT. Every row
    # the bands were measured on had a second back who actually touched the ball; a man who was
    # dressed and did nothing is a different animal and reading him off the <20 band is an
    # extrapolation. He falls back to the average and the page says so.
    try:
        zero = float(str(row.get('wk1_share') or '').strip() or 'nan') == 0.0
    except ValueError:
        zero = False
    if b and b in table and not zero:
        return float(table[b]), b, ''
    if zero:
        return flat, '', ('he was on the field in week one and touched the ball no times, which '
                          'is outside what this was measured on, so this is the average across '
                          'every backfield rather than his own')
    return flat, '', ('no week-1 backfield line for him, so this is the average across every '
                      'backfield rather than his own')


def load_seat_rows(src):
    """EVERY row of inherit_2026.csv, owned or free (doc 291). A seat behind a job is worth the same
    to whoever holds the man, so a backup Matt already owns is priced by it too -- otherwise his
    handcuff reads 0.0 to drop, because a page that cannot see injuries never starts him."""
    p = os.path.join(src, 'inherit_2026.csv')
    if not os.path.exists(p):
        return []
    with open(p, newline='', encoding='utf-8-sig') as fh:
        return list(csv.DictReader(fh))


def load_pedigree(src):
    """NFL round, pick and year for every player, from Source\\pedigree_2026.csv. Returns [] when
    the file is absent -- the seat table then loses ONE COLUMN and never the section (0.2's
    'a step that cannot do its job must fail' applies to steps, not to optional ornament)."""
    p = os.path.join(src, 'pedigree_2026.csv')
    if not os.path.exists(p):
        return []
    try:
        with open(p, encoding='utf-8-sig') as fh:
            return list(csv.DictReader(fh))
    except OSError:
        return []


def load_seats(src):
    """Source\\inherit_2026.csv (doc 275). Returns ([], why) when it is missing -- the section
    says so rather than rendering an empty table."""
    p = os.path.join(src, 'inherit_2026.csv')
    if not os.path.exists(p):
        return [], 'inherit_2026.csv is missing, not empty -- run py research\\build_inherit.py'
    with open(p, newline='', encoding='utf-8-sig') as fh:
        rows = [r for r in csv.DictReader(fh) if r.get('free') == 'yes']
    rows.sort(key=lambda r: -float(r.get('job_pays') or 0))
    return rows, ('' if rows else 'no backfield has a claimable direct backup this week')


# ---------------------------------------------------------------------------------------------
CSS = """
:root{--ground:#EFF2F1;--surface:#FCFCFB;--sunk:#E4E9E7;--ink:#15181B;--ink2:#39424A;
--muted:#66717A;--rule:#D2D9D7;--hole:#C24E1E;--holebg:#F7E4DA;--ok:#2F8F63;--okbg:#E2F0E9;
--struct:#3A63A8;--structbg:#E3E9F5;
--disp:"Archivo Narrow",Helvetica Neue,Arial,sans-serif;--body:Georgia,"Source Serif 4",serif;
--mono:"IBM Plex Mono",Consolas,ui-monospace,monospace}
@media (prefers-color-scheme:dark){:root{--ground:#0F1213;--surface:#181C1E;--sunk:#22282A;
--ink:#E7EBEC;--ink2:#BFC7CB;--muted:#8E999F;--rule:#2C3336;--hole:#D9773F;--holebg:#3A2318;
--ok:#3AA471;--okbg:#12291F;--struct:#5E94DC;--structbg:#16233A}}
*{box-sizing:border-box}
body{background:var(--ground);color:var(--ink);font-family:var(--body);font-size:16px;
line-height:1.55;margin:0;padding:0 20px 64px}
.wrap{max-width:1180px;margin:0 auto}
header{padding:36px 0 22px;border-bottom:3px solid var(--ink)}
.kick{font-family:var(--disp);text-transform:uppercase;letter-spacing:.14em;font-size:12px;
font-weight:600;color:var(--struct);margin:0 0 8px}
h1{font-family:var(--disp);font-weight:700;font-size:clamp(34px,6vw,58px);line-height:.95;
margin:0;text-transform:uppercase;letter-spacing:-.015em}
.dek{font-size:17px;color:var(--ink2);max-width:64ch;margin:14px 0 0}
h2{font-family:var(--disp);text-transform:uppercase;letter-spacing:.05em;font-size:22px;
font-weight:700;margin:40px 0 6px;padding-top:6px;border-top:1px solid var(--rule)}
h2 .n{color:var(--struct);margin-right:10px}
h3{font-family:var(--disp);font-size:16px;font-weight:600;text-transform:uppercase;
letter-spacing:.05em;margin:26px 0 2px}
p.lede{max-width:66ch;color:var(--ink2);margin:0 0 16px}
p.sub{max-width:70ch;color:var(--muted);font-size:14.5px;margin:0 0 10px}
.scroll{overflow-x:auto;border:1px solid var(--rule);background:var(--surface);margin-bottom:10px}
/* SECTION 0 -- what to do. Matt, 2026-09-11: "I need the hot takes up front." */
.band{border-bottom:3px solid var(--ink);padding-bottom:20px}
.bh{margin-top:26px;border-top:none}
.mv{background:var(--surface);border:1px solid var(--rule);border-left:4px solid var(--struct);
padding:10px 14px;margin:0 0 8px}
.mv.big{border-left:4px solid var(--ok);padding:16px 18px}
.act{margin:0 0 5px;font-family:var(--disp);font-size:19px;line-height:1.25}
.mv.big .act{font-size:clamp(22px,3.2vw,30px)}
.verb{color:var(--muted);text-transform:uppercase;letter-spacing:.09em;font-size:.60em;
margin-right:10px}
.mmeta{font-family:var(--body);font-size:13px;color:var(--muted);margin-left:10px}
.pill{float:right;font-family:var(--mono);font-size:15px;background:var(--structbg);
color:var(--struct);border-radius:3px;padding:4px 10px;white-space:nowrap;line-height:1.05}
.pill.sure{background:var(--okbg);color:var(--ok)}
.mv.big .pill{font-size:26px;padding:6px 13px;font-weight:600}
.ctx{margin:0;font-size:14.5px;color:var(--ink2);max-width:80ch}
.nws{margin:7px 0 0;font-size:13.5px;color:var(--muted);border-left:2px solid var(--rule);
padding-left:10px;max-width:80ch}
.cost{margin:12px 0 2px;font-size:14px;color:var(--ink2)}
.call{font-family:var(--disp);text-transform:uppercase;letter-spacing:.06em;font-size:15px;
margin:2px 0 10px}
.call.yes{color:var(--ok)}
.call.no{color:var(--hole)}
.warn{color:var(--hole)}
/* the cost of a drop, stated before the picks, because it gates all of them */
.costbox{margin:2px 0 16px;border-left:3px solid var(--hole);background:var(--sunk);
padding:10px 14px;font-size:15px;color:var(--ink);max-width:86ch}
h3.sub0{margin:16px 0 8px;font-family:var(--disp);text-transform:uppercase;letter-spacing:.08em;
font-size:12.5px;color:var(--struct);border-bottom:1px solid var(--rule);padding-bottom:5px}
.rank{display:inline-block;min-width:1.25em;margin-right:10px;color:var(--muted);
font-family:var(--disp)}
.pill em{display:block;font-style:normal;font-size:10px;letter-spacing:.06em;text-transform:uppercase;
opacity:.75;margin-top:1px;text-align:right}
table.cal{width:100%;margin-top:4px}
table.cal th[scope="row"]{white-space:nowrap;font-family:var(--disp);text-transform:uppercase;
letter-spacing:.05em;font-size:11.5px;color:var(--struct)}
table.cal td.l,table.cal th.l{text-align:left}
table.cal td:last-child{font-family:var(--mono);width:3.4em}
.fine{margin:0 0 8px;font-size:13px;color:var(--muted);max-width:86ch}
.ruled{margin:12px 0 0;border-left:3px solid var(--hole);background:var(--sunk);
padding:9px 14px}
.ruled h4{margin:0 0 4px;font-family:var(--disp);text-transform:uppercase;letter-spacing:.07em;
font-size:12px;color:var(--hole)}
.ruled ul{margin:0;padding-left:18px;font-size:13.5px;color:var(--ink2)}
.ruled li{margin:3px 0;max-width:86ch;white-space:normal}
.ruled .fine{margin:5px 0 0;font-size:12.5px;color:var(--muted)}
tr.out th,tr.out td{opacity:.45}
tr.out th .pl{text-decoration:line-through}
ul.watch{margin:10px 0 0;padding-left:18px;font-size:14px;color:var(--ink2)}
ul.watch li{margin:3px 0}
.todo{margin-top:14px;background:var(--sunk);border:1px solid var(--rule);padding:10px 14px}
.todo h4{margin:0 0 4px;font-family:var(--disp);text-transform:uppercase;letter-spacing:.07em;
font-size:12px;color:var(--struct)}
.todo ul{margin:0;padding-left:18px;font-size:13.5px}
.todo li{margin:4px 0;max-width:86ch;white-space:normal}
.todo .more{margin:7px 0 0;font-size:12.5px;color:var(--muted)}
a.todolink{display:inline-block;margin-left:10px;font-family:var(--disp);text-transform:uppercase;
letter-spacing:.07em;font-size:11.5px;color:var(--struct);border-bottom:1px solid var(--struct);
text-decoration:none;padding-bottom:1px}
p.jump{margin:6px 0 0}
p.jump a.todolink{margin:0 14px 0 0}
/* THE PAGE BAR AND THE SECTION NAV. Matt, 2026-09-19: "the hyperlinks on the week sheet are too
   high on the page, and jump to links are needed for the endless sections", and "if any sheet
   needs jump to links, it's the damn Week Sheet. It's insufferably long." The page bar now sits
   UNDER the dek instead of above the title, and the section nav sticks to the top of the window
   so it is reachable from anywhere in a 76 KB page. Cross-page links open in a new tab so the
   sheet you came from is never destroyed (his second complaint of the same night). */
p.pagebar{margin:18px 0 0;display:flex;flex-wrap:wrap;align-items:baseline;gap:0 4px}
p.pagebar .pbl{font-family:var(--disp);text-transform:uppercase;letter-spacing:.14em;
font-size:11px;color:var(--muted);margin-right:8px}
p.pagebar a.todolink,p.pagebar span.todolink{margin:0 14px 0 0}
p.pagebar a.todolink.home{font-weight:700}
p.pagebar span.here{color:var(--muted);border-bottom:none;cursor:default}
.secnav{position:sticky;top:0;z-index:50;display:flex;flex-wrap:wrap;align-items:center;
gap:2px;margin:0;padding:7px 0;background:var(--ground);border-bottom:1px solid var(--rule)}
.secnav a{font-family:var(--disp);text-transform:uppercase;letter-spacing:.07em;font-size:11.5px;
color:var(--ink2);text-decoration:none;padding:5px 9px;border-radius:3px;white-space:nowrap;
line-height:1.1}
.secnav a:hover,.secnav a:focus{background:var(--structbg);color:var(--struct);outline:none}
.secnav a .n{color:var(--struct);font-weight:700;margin-right:5px}
.secnav a.top{margin-left:auto;color:var(--muted)}
/* a jumped-to heading must not hide under the sticky bar */
h2,h3,.bh{scroll-margin-top:56px}
@media (max-width:640px){.secnav{padding:5px 0}.secnav a{padding:4px 7px;font-size:11px}}
@media print{.secnav{position:static;border:none}}
/* a long name clips and keeps its full self on hover, so the number columns get the width */
th .pl{display:block;max-width:21ch;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
td.ok,td.zero,td.bye,td.hole,td.rate,td.tot{width:2.9em}
td.why,th.why{max-width:22em;white-space:normal;font-size:11px;color:var(--muted)}
b.hurt{color:var(--bad,#b3261e);font-weight:600}
div.holes{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 14px}
span.hole-chip{border:1px solid var(--hole);background:var(--holebg);color:var(--hole);border-radius:2px;padding:4px 9px;font-size:12.5px;display:inline-flex;gap:7px;align-items:baseline}
span.hole-chip b{font-family:var(--mono);font-size:11px;letter-spacing:.03em}
details.poolblk{margin:10px 0;border-top:1px solid var(--rule);padding-top:6px}
details.poolblk>summary{cursor:pointer;font-family:var(--disp);font-size:15px;letter-spacing:.01em;list-style:revert}
details.poolblk>summary .meta{margin-left:10px;font-size:11.5px;color:var(--muted)}
table{border-collapse:collapse;width:100%;font-family:var(--mono);font-variant-numeric:tabular-nums;
font-size:12.5px}
th,td{border:1px solid var(--rule);padding:5px 6px;text-align:center;white-space:nowrap}
thead th{background:var(--sunk);font-family:var(--disp);font-weight:600;font-size:12px;
letter-spacing:.06em;text-transform:uppercase;color:var(--ink2)}
th[scope=row]{text-align:left;background:var(--sunk);font-family:var(--disp);font-weight:600;
font-size:13px;position:sticky;left:0;z-index:2;min-width:130px}
.corner{text-align:left;z-index:3}
td.hole{background:var(--holebg);color:var(--hole);font-weight:600}
td.ok{background:var(--okbg);color:var(--ok);font-weight:600}
td.zero{color:var(--muted);opacity:.55}
td.bye{background:var(--sunk);color:var(--muted);font-size:11px}
td.rate,th.rate{background:var(--structbg);color:var(--struct);font-weight:600}
td.tot,th.tot{background:var(--sunk);font-weight:700;font-size:13.5px}
td.tot.pos{color:var(--ok)}
.pl{display:block;font-family:var(--disp);font-size:14px;font-weight:700}
.meta{display:block;font-family:var(--mono);font-size:10.5px;color:var(--muted);font-weight:400;
text-transform:none;letter-spacing:0;white-space:normal;max-width:46ch}
p.cap{max-width:70ch;color:var(--muted);font-size:14px;margin:4px 0 8px}
td[colspan]{white-space:normal;text-align:left}
td.meta{display:table-cell;max-width:none}
details.leftoff{margin:4px 0 16px;max-width:86ch;font-size:14px;color:var(--muted)}
table.pend{width:100%;margin:6px 0 4px;border-collapse:collapse;font-size:14px;color:var(--ink)}
table.pend th{font-family:var(--disp);font-size:11px;text-transform:uppercase;letter-spacing:.06em;text-align:center;padding:4px 8px;border-bottom:1px solid var(--rule,#ccc)}
table.pend th.l,table.pend td.l{text-align:left}
table.pend td{padding:8px;border-bottom:1px solid var(--rule,#ddd);vertical-align:top;text-align:center;line-height:1.45}
table.pend td.pri{font-family:var(--mono);font-size:15px;width:4.5em}
table.pend td.n{font-family:var(--mono);width:5em}
table.pend .meta{display:block;font-size:12.5px;color:var(--muted)}
details.leftoff>summary{cursor:pointer}
table.crowd td.n{text-align:left}
table.crowd td.p .fine{font-weight:normal;color:var(--muted)}
.box{background:var(--surface);border:1px solid var(--rule);border-left:4px solid var(--struct);
padding:16px 18px;margin:14px 0 24px;max-width:74ch}
#inputs h4{margin:0 0 6px}#inputs ul.inputs{margin:0 0 8px 18px;padding:0}#inputs li{margin:3px 0;font-size:14.5px}
#inputs.bad{border-left-color:var(--hole)}
.box h4{font-family:var(--disp);text-transform:uppercase;letter-spacing:.08em;font-size:12px;
margin:0 0 8px;color:var(--struct)}
.box p{margin:0 0 8px}
.eq{font-family:var(--mono);font-size:13px;background:var(--sunk);padding:8px 10px;display:block;
overflow-x:auto;white-space:nowrap}
.bad{background:var(--holebg);border-left-color:var(--hole);color:var(--hole)}
footer{border-top:1px solid var(--rule);margin-top:34px;padding-top:14px;color:var(--muted);
font-size:13.5px}

.cards{display:grid;gap:14px;margin:14px 0}
.card{background:var(--surface);border:1px solid var(--rule);border-left:3px solid var(--struct);
padding:14px 16px;border-radius:2px}
.card-bad{border-left-color:var(--hole);background:var(--holebg)}
.card h4{font-family:var(--disp);font-size:15px;margin:0 0 2px;letter-spacing:.01em}
.card .cmeta{font-family:var(--mono);font-size:10px;color:var(--muted);margin-left:10px;
letter-spacing:.04em;text-transform:uppercase}
.card .verdict{font-family:var(--disp);font-size:12px;text-transform:uppercase;letter-spacing:.07em;
color:var(--struct);margin:0 0 8px}
.card-bad .verdict{color:var(--hole)}
.card .sig{font-size:12px;color:var(--ink2);margin:0 0 8px}
.card .sig b{font-family:var(--mono);font-size:9.5px;text-transform:uppercase;letter-spacing:.06em;
color:var(--muted);font-weight:400}
.card ul.news{margin:0 0 10px;padding-left:16px;font-size:12.5px;color:var(--ink2)}
.card ul.news li{margin:0 0 4px}
.card .cases{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:4px}
.card .cases h5{font-family:var(--mono);font-size:9.5px;text-transform:uppercase;letter-spacing:.06em;
margin:0 0 3px;font-weight:400}
.card .bull h5{color:var(--ok)}
.card .bearc h5{color:var(--hole)}
.card .cases p{margin:0;font-size:12.5px;line-height:1.45}
.card .cnote{margin:10px 0 0;padding-top:8px;border-top:1px solid var(--rule);font-size:11.5px;
color:var(--muted);font-style:italic}
@media (max-width:640px){.card .cases{grid-template-columns:1fr}}
"""

TODO_CSS = """
ol.todopage{list-style:none;margin:0;padding:0}
ol.todopage li{border:1px solid var(--rule);border-left:4px solid var(--struct);
background:var(--sunk);padding:10px 14px;margin:0 0 10px}
ol.todopage li.k-read{border-left-color:var(--rule)}
ol.todopage li.k-later{border-left-color:var(--muted)}
.hub{background:var(--sunk);border:1px solid var(--rule);padding:12px 16px;margin:22px 0 4px}
.hub h4{margin:0 0 7px;font-family:var(--disp);text-transform:uppercase;letter-spacing:.07em;
font-size:11.5px;color:var(--struct)}
.hub ul{margin:0;padding:0;list-style:none}
.hub li{margin:5px 0;font-size:13.5px}
.hub li a{font-weight:600;color:var(--ink);border-bottom:1px solid var(--struct);
text-decoration:none;margin-right:10px}
.hub li span{color:var(--muted);font-size:12.5px}
ol.cmds li code{display:block;font-family:var(--mono);font-size:13px;font-weight:600;
margin-bottom:3px}
ol.cmds li.first{border-left-width:6px}
ol.cmds li .tt{font-weight:400;font-size:13px;color:var(--ink2)}
details.tn{margin-top:6px}
details.tn summary{cursor:pointer;font-family:var(--disp);text-transform:uppercase;
letter-spacing:.07em;font-size:11px;color:var(--struct)}
details.donewrap{margin-top:26px}
details.donewrap summary{cursor:pointer;font-family:var(--disp);text-transform:uppercase;
letter-spacing:.07em;font-size:12px;color:var(--muted);margin-bottom:12px}
.todopage .tn p{margin:0 0 7px;font-family:var(--body);font-size:13px;color:var(--ink2);
max-width:92ch}
.todopage .tn p:last-child{margin-bottom:0}
ol.todopage li.k-do{border-left-color:var(--hole)}
ol.todopage li.done{opacity:.5}
ol.todopage li.done .tt{text-decoration:line-through}
.todopage .tag{display:inline-block;font-family:var(--disp);text-transform:uppercase;
letter-spacing:.08em;font-size:10.5px;color:var(--muted);margin-right:9px}
.todopage .tt{font-weight:600;font-size:14.5px}
.todopage .tn{margin-top:6px}
"""



def _tbl(head, body, caption=''):
    # [doc 439] Matt, 29 Sept: the caption was "formatted with a text box ... the end of sentences
    # fall out of sight until i drag my cursor". It sat INSIDE the scrolling table, uppercase at
    # 11px, as wide as the widest row. It is a plain paragraph above the table now.
    cap = f'<p class="cap">{caption}</p>' if caption else ''
    return f'{cap}<div class="scroll"><table><thead>{head}</thead><tbody>{body}</tbody></table></div>'


def lookahead_html(week, roster, freerows):
    """The five weeks ahead, on this page (claude_todo, 29 Sept): who is off, and the best free
    quarterback and defense each week with the number they were ranked on. It computed in wire.py
    from the first week and reached only the wire page and the console. The computation stays
    wire.py's; lookahead_box.py renders it. ONE guarded call: a failure inside the box, including
    a missing lookahead_box.py or wire.py, prints one console line and costs the page nothing."""
    if not week:
        return ''
    try:
        import lookahead_box
        return lookahead_box.box(week, roster, freerows)
    except (Exception, SystemExit) as exc:
        print(f'  weeks-ahead box NOT built -- {type(exc).__name__}: {exc}')
        return ''


CROWD_MIN_CHG = 1.0     # a man is "most-added" when ESPN's +/- since its last reset is at least this
CROWD_ROWS = 10


def crowd_table(crowd, call_rows, picks_shown, oj_under, oj_cut, seat_priced, seat_cut, seat_rows,
                freerows, bar, roster):
    """[30 Sept] THE CROWD'S ADDS, AND THIS PAGE'S ANSWER FOR EACH. ESPN's +/- (percentChange) is the
    column Matt asked for on 23 Sept (doc 395: "the plus/minus column is what i wanted you to note");
    wire.py has read it into every WIRE_<date>.csv since, and no page printed it. On 30 Sept it read
    Ollie Gordon II +48.4, Kalif Raymond +18.1, Jaylen Wright +9.7, and Wright was on no page at all.
    Three misses in three days (Gordon, Bell, Miller) were found by Matt's eye against what the
    analysts were saying; this is that comparison run by the page, every build, against the one
    consensus that costs nothing: what thousands of ESPN managers added since the count last reset.
    A man here with no answer is a defect of the page (0.5(c)5); a man here with an answer is a
    conversation. It reads the page's own lists and prices, so it can never disagree with them."""
    rows = []
    for c in (crowd or []):
        try:
            chg = float(c.get('own_chg'))
        except (TypeError, ValueError):
            continue
        if chg >= CROWD_MIN_CHG:
            rows.append((chg, c))
    rows.sort(key=lambda t: -t[0])
    rows = rows[:CROWD_ROWS]
    if not rows:
        return ('<h3 class="sub0" id="crowd">The crowd&rsquo;s adds</h3><p class="ctx fine">Nobody free has moved a full point '
                'on ESPN&rsquo;s +/- since the count last reset (it read near zero on Monday and Tuesday and 48 '
                'on Wednesday the week of 28 Sept). Read this on Wednesday.</p>')
    call_by = {norm_name(m['name']): (i + 1, m) for i, m in enumerate(call_rows)}
    pick_by = {norm_name(m['name']): (i + 1, m) for i, m in enumerate(picks_shown)}
    under_by = {norm_name(m['name']): m for m in oj_under}
    cut_by = {norm_name(nm): why for nm, why in oj_cut}
    seat_by = {norm_name(r['next_man']): (ev, r) for ev, _f, _o, _b, _w, r, _y in seat_priced}
    seatcut_by = {norm_name(nm): why for nm, why in seat_cut}
    holder_by = {norm_name(r.get('holds_the_job') or ''): r for r in seat_rows}
    free_by = {norm_name(f['name']): f for f in freerows}
    mine_pos = collections.defaultdict(list)
    for p in roster:
        mine_pos[p.get('pos')].append(p)
    out = []
    for chg, c in rows:
        nm, key = c.get('name') or '?', norm_name(c.get('name') or '')
        pos, tm = c.get('pos') or '', c.get('tm') or ''
        if key in call_by:
            i, m = call_by[key]
            ans = f"THE CALL, row {i}: <b>{m['worth']:+.1f}</b>"
        elif key in pick_by:
            i, m = pick_by[key]
            ans = f"pick {i}, <b>{m['worth']:.1f}</b> expected"
        elif key in under_by:
            ans = 'an open job below the cut: ' + under_by[key]['oj_short']
        elif key in cut_by:
            ans = 'an open job, not priced: ' + E(cut_by[key])
        elif key in seat_by:
            ev, r = seat_by[key]
            ans = f"the seat list: behind {E(r.get('holds_the_job') or '?')}, <b>{ev:.1f}</b> expected"
        elif key in seatcut_by:
            ans = 'the seat list left him off: ' + E(seatcut_by[key])
        elif key in holder_by:
            r = holder_by[key]
            f = free_by.get(key)
            ans = (f"he holds the {E(r.get('team') or tm)} job the seat list prices"
                   + (f"; his own rate is <b>{f['wk']:.1f}</b> a week against your bar of "
                      f"{max((bar.get(pos) or {}).values() or [0]):.1f}" if f and pos in bar else '')
                   + (f"; he is {E(str(f.get('status') or '').replace('_', ' ').lower())}"
                      if f and (f.get('status') or 'ACTIVE') != 'ACTIVE' else ''))
        elif key in free_by:
            f = free_by[key]
            if pos in WEEKLY_VALUE:
                ans = 'a weekly position: the wire page prices him by the matchup, not here'
            elif pos in bar:
                b = bar.get(pos) or {}
                live = [b[w] for w in WEEKS if b.get(w) is not None]
                ans = (f"priced at <b>{f['wk']:.1f}</b> a week against your bar of "
                       f"{(max(live) if live else 0):.1f}: " + ('below your nine' if f['wk'] < (max(live) if live else 0)
                                                               else 'clears the bar in some weeks, see the table below'))
                if (f.get('status') or 'ACTIVE') != 'ACTIVE':
                    ans += f"; he is {E(str(f.get('status')).replace('_', ' ').lower())}"
            else:
                ans = f"priced at <b>{f['wk']:.1f}</b> a week; no bar at {E(pos)} on this roster"
        else:
            ans = 'not priced: ESPN projects him at nothing, so no rate exists to price'
        owned = c.get('owned')
        try:
            owned_txt = f"{float(owned):.0f}%"
        except (TypeError, ValueError):
            owned_txt = '?'
        out.append(f'<tr><td class="p"><b>{E(nm)}</b> <span class="fine">{E(pos)} &middot; {E(tm)}</span></td>'
                   f'<td class="r">{chg:+.1f}</td><td class="r">{owned_txt}</td><td class="n">{ans}</td></tr>')
    return ('<h3 class="sub0" id="crowd">The crowd&rsquo;s adds, and this page&rsquo;s answer</h3>'
            '<p class="cap">ESPN&rsquo;s most-added free men since its +/- count last reset (it moves on Wednesday, '
            'after other leagues&rsquo; waivers run). A name here with no answer is a gap in this page; a name '
            'with an answer you disagree with is worth a look.</p>'
            '<table class="crowd"><tr><th>they added</th><th>+/-</th><th>rostered</th><th>this page says</th></tr>'
            + ''.join(out) + '</table>')


def render(roster, freerows, const, stamp=None, note='', seats=None, seatnote='',
           cards=None, screened=None, unpriced=None, seats_used=None, seat_all=None,
           week=0, todo=None, donot=None, team_name='', todo_n=0, pedigree=None,
           inputs='', sched='', vintage_html='', season_rates=None, news_lookup=None,
           ir_view=None, tgt_load=None, open_jobs=None, crowd=None, standing='', leaders=None, rb_use=None,
           wr_use=None, pf=None, wrank=None, playoff=None, matchup=None):
    # doc 380: the stamp is the READ time and who ran it, never the bare date -- two builds on one
    # day were indistinguishable, and "built 19 September" said nothing about a 03:11 settlement.
    stamp = stamp or build_meta()['text']
    sched = sched or schedule_sentence(os.path.dirname(os.path.abspath(__file__)))
    bar = bar_grid(roster)
    base = season(roster)
    # [doc 426, moved by doc 435] THE KEY CONTRACT, ASSERTED ONCE, BEFORE ANY FREE ROW IS READ.
    # The seat guard was shipped reading `team`; free rows spell it `tm` (wire.py builds each one
    # as `dict(rate[pid])`), so every lookup returned None and the filter never fired. It was
    # "verified" against the WIRE CSV, which does spell it `team` -- same logic, different object,
    # doc 80 exactly. Section 3: never gate a mandatory step on a key being present. Assert, and
    # assert FIRST: doc 435 found the original placement unreachable, because the free-pool table
    # read c["pos"], c["wk"], c["bye"], c["name"] and c["tm"] a thousand lines earlier and raised
    # a bare KeyError before this message could print.
    if freerows:
        _need = ('name', 'pos', 'tm', 'wk', 'bye')
        _miss = sorted(set(_need) - set(freerows[0]))
        if _miss:
            raise KeyError('free rows are missing the keys the seat and bet lanes read: '
                           + ', '.join(_miss) + '. Present: ' + ', '.join(sorted(freerows[0])))
    hdr = '<tr><th class="corner" scope="col">position</th>' + \
          ''.join(f'<th scope="col">{w}</th>' for w in WEEKS) + '</tr>'

    holes = []
    for w in WEEKS:
        _, empty = week_points(roster, w)
        for lab in empty:
            holes.append((w, lab))
    hole_txt = ' &middot; '.join(f'week {w} {lab}' for w, lab in holes) or 'none'

    # Matt's own rulings, resolved against the names on this page before anything is ranked.
    # His file is the record and the page must not argue with it by accident (doc 295).
    _dn_names = ([r.get('name') for r in freerows] + [r.get('name') for r in roster]
                 + [c.get('player') for c in (cards or [])])
    dn = donot_map(donot, [n for n in _dn_names if n])
    for c in (cards or []):
        if (c.get('verdict') or '').strip().upper().startswith('DO NOT'):
            dn.setdefault(norm_name(c.get('player')), (c['verdict'].strip(), 'your player card'))

    brows = ''
    for p in POS:
        cells = ''.join(
            (f'<td class="hole">empty</td>' if bar[p][w] == 0 else f'<td>{bar[p][w]:.1f}</td>')
            for w in WEEKS)
        brows += f'<tr><th scope="row">{p}</th>{cells}</tr>'

    # candidates: the best few at each position, priced
    # [doc 413] OPEN THE POSITION THAT IS SHORT, FOLD THE REST. Doc 369 catalogued this and it
    # was never worked: six positions x six men x thirteen week columns is 36 rows of a grid,
    # printed above the bar that explains what its numbers mean, and most weeks he needs ONE
    # position. A position opens when the best free man there actually beats your bar (season
    # total over 0.05) or when you have an empty slot ahead at that position; everything else is
    # one click away, not gone. Matt, 24 Sept: "it's too cluttered for me to figure it out."
    cand_html = ''
    _short = {}
    for p in POS:
        _pool = sorted((r for r in freerows if r['pos'] == p), key=lambda r: -r['wk'])[:6]
        _best = max((price(c, bar)[1] for c in _pool), default=0.0)
        _hole = any(bar[p][w] == 0 for w in WEEKS)
        _short[p] = (_best > 0.05) or _hole
    for p in POS:
        pool = sorted((r for r in freerows if r['pos'] == p), key=lambda r: -r['wk'])[:6]
        if not pool:
            continue
        rows = ''
        for c in pool:
            wk, tot = price(c, bar)
            cells = ''
            for w in WEEKS:
                v = wk[w]
                if v is None:
                    cells += '<td class="bye">bye</td>'
                elif v <= 0.049:
                    cells += '<td class="zero">0</td>'
                else:
                    cells += f'<td class="ok">+{v:.1f}</td>'
            ow = f"{c['owned']:.1f}% rostered" if c.get('owned') is not None else ''
            scr = f" &middot; {E(c['screen'])}" if c.get('screen') else ''
            out_ = dn.get(norm_name(c['name']))
            rule = (' &middot; <b class="warn">ruled out</b>' if out_ else '')
            trc = ' class="out"' if out_ else ''      # 3.11 forbids a backslash inside an f-string
            rows += (f'<tr{trc}>'
                     f'<th scope="row"><span class="pl" title="{E(out_[0] if out_ else c["name"])}">'
                     f'{E(c["name"])}</span>'
                     f'<span class="meta">{E(c["tm"])} &middot; bye {c["bye"]}'
                     f' &middot; {ow}{scr}{rule}</span></th>'
                     + rate_cell(c) + cells +
                     f'<td class="tot{" pos" if tot > 0.05 else ""}">'
                     f'{"+" if tot > 0.05 else ""}{tot:.1f}</td></tr>')
        _tbl_html = _tbl(
            '<tr><th class="corner" scope="col">player</th><th class="rate" scope="col">pts/wk</th>'
            + ''.join(f'<th scope="col">{w}</th>' for w in WEEKS)
            + '<th class="tot" scope="col">season</th></tr>', rows)
        _open = ' open' if _short.get(p) else ''
        _why = ('nothing free here beats what you already have'
                if not _short.get(p) else 'worth a look')
        cand_html += (f'<details class="poolblk"{_open}><summary><b>{p}</b>'
                      f'<span class="meta">{_why}</span></summary>{_tbl_html}</details>')

    # ---- the bet: potential, priced against his own bar, and what the spot costs ------------
    pot = const.get('potential', {}).get('in_season', {})
    t3 = pot.get('three_of_three', {})
    r23 = pot.get('rookie_r2_3', {})
    r1 = pot.get('round1_rookie_inseason', {})
    hs = pot.get('hit_size', {})
    HP, HW = hs.get('ppg'), hs.get('weeks')      # ONE hit size for every row; only the odds differ
    wk2 = pot.get('workload_2of3', {})
    wk3 = pot.get('workload_3of3', {})
    i3 = pot.get('inseason_3of3', {})            # doc 453, finding 4.43
    ARCH = {
        'pedigree screen 3 of 3': ('three signals', t3.get('rate'), t3.get('n')),
        'first-round rookie':     ('first-round rookie', r1.get('rate'), r1.get('n')),
        'in-season screen 3 of 3': ('in-season screen', i3.get('rate'), i3.get('n')),
    }
    # how each screen reads in a sentence, because "he is a three signals" is not English
    # doc 379: the population and horizon behind each screen's rate, printed on the row so the
    # rate cannot be read as the man's own forecast or compared with a rate from another group.
    POP = {'three signals': 'this league added on the same three signals (2022 to 2025) were '
                            'startable from the add week to week 14',
           'first-round rookie': 'in that spot were startable in their rookie season',
           'in-season screen': 'who cleared the same three marks on this season\'s first weeks while still under '
                               'the bar (2021 to 2025) were startable over the rest of the season',
           'week-1 workload': 'who cleared two of the three week-one marks (NFL-wide, 2022 to 2025) '
                              'reached the starting bar over weeks 2 to 14',
           'week-1 workload, all three': 'who cleared all three week-one marks (NFL-wide, 2022 to '
                                         '2025) reached the starting bar over weeks 2 to 14'}
    SHORT = {'three signals': 'Young-receiver screen, all three signals',
             'in-season screen': 'Young-receiver screen on this season, all three signals',
             'first-round rookie': 'First-round rookie receiver',
             'week-1 workload': 'Week-1 workload screen',
             'week-1 workload, all three': 'Week-1 workload screen, all three marks'}
    SAYS = {'three signals': 'He clears all three signals on the young-receiver screen, and',
            'in-season screen': 'He clears all three signals on this season\'s numbers, on a few games, and',
            'first-round rookie': 'He is a first-round rookie receiver, and',
            'week-1 workload': 'He was on the field and being thrown at in week one, and',
            'week-1 workload, all three': 'He cleared every week-one workload mark there is, and'}
    _mine_pg, _team_pg = tgt_load if tgt_load else ({}, {})
    seen_bet, bet_rows = set(), []
    for c in sorted(freerows, key=lambda r: -(r.get('wk') or 0)):
        scr = (c.get('screen') or '').strip()
        key = None
        for k in ARCH:
            if k in scr:
                key = k
                break
        if not key or c['name'] in seen_bet:
            continue
        seen_bet.add(c['name'])
        lab, rate, n = ARCH[key]
        if not HP or not HW:
            continue
        _, today = price(c, bar)
        cells, fires = bet(c, bar, HP, HW)
        ev = round(rate * fires, 1) if rate else None
        odds = f'{rate:.0%}' if rate else 'not measured'
        _nd, _sh, _v = reach_check(c, HP, _mine_pg.get(norm_name(c['name'])),
                                   _team_pg.get(c.get('tm')))
        if _v and lab in ('three signals', 'in-season screen') and rate:
            # [30 Sept, doc 456] ON A SCREENED MAN THE GATE IS A CAUTION, NOT A ZERO. The cell rate
            # (26.7% under the bar, 43.6% overall, doc 453) was measured on a population that
            # INCLUDES the men the gate would exclude, so zeroing him applies the constraint twice.
            # Measured on the same 174 (reach_gate_test.py): the gate separates the broad
            # population (7.6% hit when out of reach, 22.2% in reach) and does not separate the
            # three-of-three men (1 of 3 against 16 of 36; under the bar 1 of 3 against 3 of 12),
            # and the one three-of-three hit it would have excluded was George Pickens, 2024, at
            # 43%. Points per target rose for two thirds of the hits, which is what the gate
            # assumes cannot happen. So: the odds stay the cell's, the expected is priced, and
            # the stretch is printed beside it with the broad-population number.
            odds = (f'{rate:.0%}, a stretch: needs {_sh:.0%} of the passing game; men asked for '
                    f'that much hit 8% against 22% for the rest')
        elif _v:
            # [doc 432] not "not measured" -- MEASURED AS UNREACHABLE. The two must never print
            # the same words (0.5). The odds are true of the archetype and false of this man.
            ev, odds = None, f'out of reach &middot; needs {_sh:.0%} of the passing game'
        bet_rows.append((ev, c, lab, today, fires, odds, n, cells))
    # ---- THE WEEK-1 WORKLOAD LANE (doc 308) -------------------------------------------------
    # Until this existed, every bet on this page came from a PRESEASON fact -- draft round, a
    # career rate, a depth chart -- so the same names printed every week and could not change.
    # 4.31 measures the week-2 claim at 34.6% against week 1's 9.4% precisely BECAUSE it bets on
    # a snap count, and there was no snap count anywhere in this page's inputs.
    # POPULATION, and it is NOT the population of the two screens above (0.6): those rates come
    # from this league's own executed adds, n=108; this one is NFL-wide, WR and TE, 2022-2025,
    # below replacement the prior season, n=517. Two different objects. They are never summed and
    # never compared, and each row prints its own rate.
    for c in sorted(freerows, key=lambda r: -(r.get('wk') or 0)):
        try:
            sig = int(str(c.get('form_sig') or '').strip() or -1)
        except ValueError:
            sig = -1
        if sig < 2 or c['name'] in seen_bet:
            continue
        band = wk3 if sig >= 3 else wk2
        rate, n = band.get('rate'), band.get('n')
        if not HP or not HW or not rate:
            continue
        seen_bet.add(c['name'])
        lab = 'week-1 workload, all three' if sig >= 3 else 'week-1 workload'
        _, today = price(c, bar)
        cells, fires = bet(c, bar, HP, HW)
        _ev, _od = round(rate * fires, 1), f'{rate:.0%}'
        _nd, _sh, _v = reach_check(c, HP, _mine_pg.get(norm_name(c['name'])),
                                   _team_pg.get(c.get('tm')))
        if _v:
            _ev, _od = None, f'out of reach<span class="meta">needs {_sh:.0%} of the passing game</span>'
        # [1 Oct, doc 457] THE MAN AHEAD, read off the newest game: see pos_leaders(). A second
        # tight end has never cleared this screen, so he gets no rate; a second receiver gets the
        # measured second-man cell. Only when the leader is a different man with at least six
        # targets and twice his.
        _lead_by, _last_by = leaders if leaders else ({}, {})
        _ld = _lead_by.get((team_key(c.get('tm') or ''), c.get('pos')))
        _my_last = _last_by.get(norm_name(c['name']))
        _sm = (pot.get('workload_second_man') or {})
        if (_ld and norm_name(_ld[0]) != norm_name(c['name']) and _ld[1] >= 6
                and _ld[1] >= 2 * (_my_last or 0)):
            _who = f"{E(_ld[0])} ({_ld[1]:.0f} targets to {('%.0f' % _my_last) if _my_last is not None else 'none'} last game)"
            if c.get('pos') == 'TE':
                _ev, _od = None, (f'behind {_who}<span class="meta">a second tight end has never cleared '
                                  f'this screen ({_sm.get("te_second_n", 0)} of {_sm.get("te_n", 15)} who cleared led '
                                  f'their team), so no rate</span>')
            elif _sm.get('wr_rate'):
                _ev = round(_sm['wr_rate'] * fires, 1)
                _od = (f"{_sm['wr_rate']:.0%}<span class=\"meta\">second receiver behind {_who}: "
                       f"{_sm.get('wr_hit')} of {_sm.get('wr_n')} such men hit against "
                       f"{_sm.get('top_hit')} of {_sm.get('top_n')} who led their team</span>")
        bet_rows.append((_ev, c, lab, today, fires, _od, n, cells))

    # a row with no measured odds sorts on what it is worth if it fires -- it must never read as a
    # zero, which is the difference between "we measured nothing" and "we measured nothing there"
    bet_rows.sort(key=lambda x: (0 if x[0] is None else 1, -(x[0] if x[0] is not None else x[4])))

    brow_html = ''
    for ev, c, lab, today, fires, odds, n, cells in bet_rows:
        ow = f"{c['owned']:.1f}% rostered" if c.get('owned') is not None else ''
        cel = ''
        for w in WEEKS:
            v = cells[w]
            cel += ('<td class="bye">bye</td>' if v is None else
                    ('<td class="zero">0</td>' if v <= 0.049 else f'<td class="ok">+{v:.1f}</td>'))
        # [doc 438] THE LAST TWO GAMES, ACTUAL BESIDE EXPECTED, AND THE WIRE'S FLAG WORD. The wire
        # carried act2 and xfp2 onto every free row and this lane printed neither. Display only:
        # as a fourth signal expected points moved the screen by nothing, so nothing sorts on it.
        _l2 = last_two_text(c)
        brow_html += (f'<tr><th scope="row"><span class="pl" title="{E(c["name"])}">{E(c["name"])}</span>'
                      f'<span class="meta">{E(c["pos"])} &middot; {E(c["tm"])} &middot; bye {c["bye"]}'
                      f' &middot; {ow}' + (f' &middot; {_l2}' if _l2 else '') + '</span></th>'
                      f'<td>{E(lab)}</td><td class="{"zero" if today <= 0.05 else "ok"}">'
                      f'{today:.1f}</td>{cel}'
                      f'<td class="tot{" pos" if fires > 0.05 else ""}">{fires:.1f}</td>'
                      f'<td>{odds}</td>'
                      + (f'<td class="tot">&mdash;</td>' if ev is None else
                         f'<td class="tot{" pos" if ev > 0.05 else ""}">{ev:.1f}</td>') + '</tr>')
    bet_tbl = _tbl(
        '<tr><th class="corner" scope="col">the player</th><th scope="col">the signal</th>'
        '<th scope="col">this week, as he is</th>'
        + ''.join(f'<th scope="col">{w}</th>' for w in WEEKS)
        + '<th class="tot" scope="col">if it fires</th><th scope="col">odds</th>'
          '<th class="tot" scope="col">expected</th></tr>', brow_html,
        'green cells are the weeks a hit would actually enter your lineup') if brow_html else \
        '<div class="box bad"><h4>nobody on the wire carries a signal this week</h4><p>That is an '\
        'answer, not a gap. Hold the spot &mdash; the screen fires at the same rate in November.</p></div>'

    # ---- THE MISSING-ROW GUARD: name anybody the pricing dropped (doc 277) ------------------
    priced = {b[1]['name'] for b in bet_rows}
    dropped = [r for r in (screened or []) if r['player'] not in priced]
    # Matt's rule (doc 291, A15): a row earns space only when the sheet is the only place that
    # information exists. A screened man ESPN lists as out, doubtful, questionable or on injured
    # reserve is explained by his own player card, so he is not named here. A man with NO status
    # and no price is a hole only this page can show, and he stays.
    dropped = [r for r in dropped if (r.get('status') or '').strip().upper() not in ESPN_SHOWS_STATUS]
    if dropped:
        bits = []
        for r in dropped:
            bits.append(f'<strong>{E(r["player"])}</strong> ({E(r["pos"])} {E(r["team"])}, '
                        f'{E(r["screen"])})')
        miss = ('<div class="box bad"><h4>On the wire with a signal, and NOT priced above</h4><p>'
                + ' &middot; '.join(bits) +
                '. ESPN lists no injury for these men and still publishes no projection, so the '
                'pricing cannot score them, so they are named here rather than silently left '
                'off. <strong>Look them up before doing anything.</strong></p></div>')
    else:
        miss = ''

    # ---- the cards: the news the arithmetic cannot see -------------------------------------
    cards = cards or []
    if cards:
        cbits = ''
        for c in cards:
            # Matt's rule (doc 291, A15). A carded man another team now owns is on ESPN already, and a
            # DO NOT card for a man ESPN lists out or on injured reserve repeats his player card.
            bad = c.get('verdict', '').strip().upper().startswith('DO NOT')
            if c.get('gone') or (bad and c.get('espn_status') in GONE_FOR_WEEKS):
                continue
            lane = 'the screen' if c.get('lane') == 'screen' else 'the seat'
            news = ''.join(f'<li>{n.strip()}</li>' for n in (c.get('news') or '').split('|') if n.strip())
            bad = c.get('verdict', '').strip().upper().startswith('DO NOT')
            cbits += (
                f'<article class="card{" card-bad" if bad else ""}">'
                f'<h4>{E(c["player"])}<span class="cmeta">{E(c["pos"])} &middot; {E(c["tm"])} '
                f'&middot; {lane}</span></h4>'
                f'<p class="verdict">{E(c.get("verdict",""))}</p>'
                f'<p class="sig"><b>the signal</b> {E(c.get("signal",""))} '
                + f'<p>&middot; <b>status</b> {E(c.get("status",""))}</p>'
                f'<ul class="news">{news}</ul>'
                f'<div class="cases"><div class="bull"><h5>the case for</h5><p>{E(c.get("bull",""))}</p></div>'
                f'<div class="bearc"><h5>the case against</h5><p>{E(c.get("bear",""))}</p></div></div>'
                # [doc 439] the note column was commentary on the card, not the card
                + '</article>')
        card_html = (f'<div class="cards">{cbits}</div>' if cbits else
                     '<div class="box"><h4>no live cards this week</h4><p>Every carded man is either '
                     'owned now or listed out by ESPN, and ESPN shows you both.</p></div>')
    else:
        card_html = ('<div class="box bad"><h4>no cards on this page</h4><p>Source\\cards_2026.csv '
                     'was not read, so the news half of this section is missing, not empty.</p></div>')

    # [doc 436] A MAN IN THE INJURED-RESERVE SLOT DOES NOT HOLD ONE OF THE FIFTEEN, SO DROPPING HIM
    # FREES NO ROSTER SEAT. On 28 Sept 22:35 THE CALL paired "take Kalif Raymond" with "drop Jonah
    # Coleman, 0.0" while Coleman sat in slot 21 and fifteen active men filled the roster. That
    # claim runs as sixteen of fifteen and fails on the roster limit, which is the failure this page
    # tells him to prevent everywhere else. ir_box() already knew who was parked; the drop ladder
    # and the seat count never asked it. Now:
    #   - `seats_used` counts the fifteen, not the fifteen plus whoever is parked (the same count
    #     doc 390 got wrong the other way: Nacua parked left fourteen and a free seat), and
    #   - a parked man is never OFFERED as a drop and never sets the floor. He stays in the full
    #     drop table with his cost, marked, because knowing what he costs is not being asked to cut
    #     him (doc 415). Joined on ESPN id, never name (section 3).
    # Dropping a parked man frees a seat only through a SECOND step, an eligible man moving into the
    # slot he left. That is written on his row, never assumed by the ladder.
    _parked = set((ir_view or {}).get('parked_ids') or ())
    _parked.discard('')
    _ir_elig = [n for n, _s in ((ir_view or {}).get('eligible') or [])]
    def _is_parked(pl):
        return str(pl.get('espn_id', '')).strip() in _parked
    if seats_used is not None and _parked:
        seats_used = max(0, seats_used - sum(1 for pl in roster if _is_parked(pl)))
    allcosts = drop_costs(roster, used=seats_used)
    # A BACKUP'S PRICE IS HIS SEAT, NOT HIS STARTS (doc 291). Put the page on per-game rates and the
    # screened tickets rise above zero -- and the cheapest thing he owns became his own handcuff at
    # 0.0, because this page never starts a backup. So a running back he owns who is the direct
    # backup to a job is priced with the same seat arithmetic as the free ones below: against the bar
    # he would have without the starter when the starter is his own man. The larger of the two
    # numbers is the price.
    sc0 = const.get('seat', {})
    r0, w0, p0 = sc0.get('relief_ppg'), sc0.get('weeks_played'), sc0.get('p_opens')
    seat_of = {}
    if r0 and w0 and p0:
        byid = {str(pl.get('espn_id', '')): pl for pl in roster}
        for r in (seat_all or []):
            nid = str(r.get('next_man_id', '')).strip()
            man = byid.get(nid)
            if man is None:
                # THE ID IS CHECKED, AND A MISS IS NOT TRUSTED (doc 291, A16). A wrong id in the seat
                # file priced his own handcuff at 0.0 with no error. Fall back to name and team, say so.
                man = roster_match(roster, r.get('next_man'), r.get('team'))
                if man is not None:
                    print(f"  week sheet: inherit_2026.csv gives {r.get('next_man')} id {nid or '(blank)'}, "
                          f"which matches nobody on the roster; matched on name and team "
                          f"(ESPN id {man.get('espn_id')}). Rebuild the seat file.")
            if not man or man.get('pos') != 'RB':
                continue
            holder = r.get('holds_the_job', '')
            hp = roster_match(roster, holder, r.get('team'))      # name AND team, never name alone
            rest = [pl for pl in roster if pl is not man and pl is not hp]
            b0 = bar_grid(rest)
            probe = {'name': man['name'], 'pos': 'RB', 'tm': man['tm'], 'bye': man['bye'], 'wk': r0}
            live = [v for v in price(probe, b0)[0].values() if v is not None]
            seat_of[man['name']] = (round(p0 * (sum(live) / len(live) if live else 0.0) * w0, 1),
                                    hp['name'] if hp else holder, hp is not None)
    adj = []
    for cost, pl in allcosts:
        st = seat_of.get(pl.get('name'))
        if st and st[0] > cost:
            adj.append((st[0], dict(pl, seat_note=('the handcuff to ' if st[2] else 'the seat behind ')
                                    + st[1])))
        else:
            adj.append((cost, pl))
    adj.sort(key=lambda x: (x[0], x[1].get('wk', 0)))
    costs = [x for x in adj if not _is_parked(x[1])][:4]
    # THE MISSING-ROW GUARD ON HIS OWN ROSTER (doc 281). rates() skips anybody ESPN prices at
    # zero, so an injured man he owns vanished from this page entirely -- and the seat he is
    # sitting in vanished with him. Name him; never let the count speak for itself.
    seatbox = ''
    if unpriced:
        seatbox = ('<div class="box bad"><h4>' + str(len(unpriced)) + ' on your roster '
                   + ('is' if len(unpriced) == 1 else 'are') + ' not priced below</h4><p>'
                   + E(', '.join(unpriced)) + ' &mdash; ESPN publishes no projection for '
                   + ('him' if len(unpriced) == 1 else 'them') + ', which is normally what an '
                   'injury designation looks like. <b>' + ('He' if len(unpriced) == 1 else 'They')
                   + ' still occupy a roster seat.</b> Every number on this page is computed '
                   'without ' + ('him' if len(unpriced) == 1 else 'them') + '.</p></div>')
    elif seats_used is not None and seats_used >= 15:
        seatbox = ('<div class="box"><h4>your roster is full</h4><p>All 15 seats are taken: '
                   'every ticket costs a drop.</p></div>')
    # [doc 417] AND THE IR SEAT IS A NUMBER, NOT A RULE IN A FILE. Two different rules get
    # conflated and it costs a plan: the slot ACCEPTS only Out or IR, while a man ALREADY in it
    # who is upgraded to Questionable keeps his seat. Matt read the second as the first and was
    # planning to park a Questionable back. Say who it would take TODAY, by name.
    seatbox += ir_box(ir_view)
    crow2 = ''
    for cost, pl in costs:
        crow2 += (f'<tr><th scope="row"><span class="pl" title="{E(pl["name"])}">{E(pl["name"])}</span>'
                  f'<span class="meta">{E(pl["pos"])}{" &middot; " + E(pl["tm"]) if pl.get("tm") else ""}'
                  f'{" &middot; priced as " + E(pl["seat_note"]) if pl.get("seat_note") else ""}'
                  f'</span></th><td class="{"zero" if cost <= 0.05 else "hole"}">'
                  f'{cost:.1f}</td></tr>')
    # ---- the seat, priced in the SAME currency as the screen (doc 276) ----------------------
    # A job's season total must never sit next to a gain-above-the-bar; they are different units and
    # putting them in one table invites exactly the comparison the page exists to prevent.
    seat_moves = []
    # DOC 314, AND THE FIRST VERSION OF THIS LANE HAD THE HOLE. The seat rows come from the depth
    # map, which carries no game log, so they shipped with a blank touch count and printed no
    # contest line at all. On 15 Sept that silenced the ONLY man on a 280-row wire in the top
    # contested band -- Kaelon Black, 15 touches, 56% -- while five pass-catchers at 7 to 9 touches
    # each carried their 29%. The lane most likely to be raced was the lane that said nothing.
    # Joined on a NORMALISED NAME against the same priced free pool the rest of the page uses, and
    # left BLANK when the join misses, because a missing game log is no information and a zero
    # would read as "nobody wants him" (4.27's join rule, doc 251).
    _touch_by = {}
    for _fr in freerows:
        _t = str(_fr.get('touches') or '').strip()
        if _t:
            _touch_by[norm_name(_fr.get('name'))] = _t
    # WHO IS ACTUALLY CLAIMABLE, AND IN WHAT SHAPE (doc 349). The seat list said in its own words
    # "these men have never been rostered" while printing Kaelon Black, rostered in this league, and
    # Dylan Sampson, on INJURY RESERVE, at the TOP of the table. Both were Matt's catches, one turn
    # apart. `freerows` IS the free pool, so absence from it is ownership, and it carries ESPN's
    # status, so the multi-week set is already known here. Nothing new is read.
    _free_by = {}
    for _fr in freerows:
        _free_by[norm_name(_fr.get('name'))] = _fr
    # [doc 426] the key contract used to sit here; doc 435 moved it to the top of render(),
    # because five earlier reads (lines around 1809 to 1837) died on a bare KeyError first and
    # the named assertion below could never fire. Same contract, one place, before any read.
    _ped_by = {norm_name(_pr.get('player')): _pr for _pr in (pedigree or [])}
    sc = const.get('seat', {})
    s_rate, s_wks, s_p = sc.get('relief_ppg'), sc.get('weeks_played'), sc.get('p_opens')
    seats = seats or []
    seat_best = 0.0
    priced, _seat_cut = [], []              # read by crowd_table() whether or not the lane prices
    if seats and s_rate and s_wks and s_p:
        # THE HANDCUFF CASE, and pricing it against today's bar is wrong (doc 276). If the man
        # holding the job is on YOUR roster, his going down LOWERS your bar -- that is the whole
        # point of a handcuff -- so the seat behind your own back is priced against the bar you
        # would actually have, with him removed. Everyone else keeps today's bar.
        # A seat behind one of YOUR OWN players is never cut by the row cap -- it is the handcuff,
        # the single biggest number this table can produce, and the first version dropped Judkins'
        # at rank 11 (doc 276).
        show = [r for r in seats[:10]]
        for r in seats[10:]:
            if roster_match(roster, r['holds_the_job'], r['team']) is not None:
                show.append(r)
        show.sort(key=lambda r: -float(r.get('job_pays') or 0))
        alt = {}
        for r in show:
            hp = roster_match(roster, r['holds_the_job'], r['team'])
            if hp is not None and hp['name'] not in alt:
                alt[hp['name']] = bar_grid([p for p in roster if p is not hp])
        srow = ''
        seat_moves_l = []
        # PRICE FIRST, THEN SORT, because the odds are now per man (doc 343) and the old sort key
        # -- what the job pays -- was only defensible while every row shared one probability.
        priced = []
        _seat_cut = []
        # doc 451: a row below the ten-row cap is CUT, and a cut row is named (0.5(c)5). Before this
        # the cap ran silently and only the filters below wrote to the list.
        for r in seats[10:]:
            if r not in show:
                _seat_cut.append((r['next_man'],
                                  f"below the ten-row cap, the job pays {float(r.get('job_pays') or 0):.0f}"))
        for r in show:
            hp = roster_match(roster, r['holds_the_job'], r['team'])
            yours = hp is not None
            # A SEAT YOU CANNOT CLAIM IS NOT A SEAT, AND NEITHER IS A MAN WHO IS NOT PLAYING.
            # Dropped rows are COUNTED and named under the table, never silently removed (0.5 c5).
            #
            # MATT, 18 Sept: "Dylan Sampson is still at the top of the seat list." He was, on IR,
            # for a full day after this filter shipped. THE CHECK WAS INSIDE `if not yours`, so a
            # row whose MAN AHEAD sits on Matt's own roster skipped it entirely -- and Sampson is
            # behind Quinshon Judkins, who is Matt's. Whether the starter is his has nothing to do
            # with whether the BACKUP can be claimed or is playing, and pinning the test to the
            # wrong object is 0.5(a2) inside a filter. `yours` earns the alternative bar below and
            # nothing else.
            _fr = _free_by.get(norm_name(r['next_man']))
            if _fr is None:
                _seat_cut.append((r['next_man'], 'rostered in your league'))
                continue
            _st = (_fr.get('status') or '').strip().upper()
            if _st in GONE_FOR_WEEKS:
                _seat_cut.append((r['next_man'], _st.replace('_', ' ').lower()))
                continue
            # [doc 411] A SEAT IS AN OPTION ON A JOB THAT IS STILL HELD. ONCE THE STARTER IS
            # ALREADY OUT THERE IS NO OPTION LEFT -- THE JOB IS OPEN AND THE ROOM HAS PRICED IT.
            # Matt, 24 Sept: "Chris Brooks is behind MarShawn Lloyd and is NOT behind Josh Jacobs.
            # I've had this discussion before and this bug snuck back in."
            # The row printed "be first to Chris Brooks / if this man goes down: Josh Jacobs".
            # Jacobs has been on the Commissioner's Exempt List since 30 Aug 2026, indefinitely.
            # He is not going to go down; he is down. inherit_2026.csv SAYS SO in its own `why`
            # -- "CAVEAT: this seat is not an option any more, the job is already open" -- and
            # nothing read it. `live_tag` carried the same fact in one word and only ever drew a
            # badge. A caveat in a data file that no code branches on is a comment, not a guard.
            if (r.get('live_tag') or '').strip().upper().replace(' ', '_') in GONE_FOR_WEEKS:
                _seat_cut.append((r['next_man'],
                                  f"{r['holds_the_job']} is already out, so this is not a seat"))
                continue
            # [doc 426] AND THE SAME QUESTION ABOUT THE OTHER MAN: IS THE BACKUP STILL ON THE
            # TEAM? doc 411 checked whether the STARTER had gone and nobody checked whether the
            # SEAT had. Emari Demercado moved to Dallas; inherit_2026.csv still had him behind
            # Kenneth Walker III on Kansas City, so the page printed "Demercado KC bye 5" -- the
            # team and the bye of the man he no longer backs up -- gave him 51% of a 248.9 job he
            # cannot inherit, and promoted the 4.5 that fell out of it to a claim on THE CALL.
            # The live team was in the wire row this loop already holds. A seat is an option on a
            # job; a man on another roster holds no option on it.
            # `freerows` is a COPY OF THE rates() DICT (wire.py: f = dict(rate[pid])), and that
            # dict spells the team `tm`. The first cut of this guard read `team`, got None on
            # every row, and never fired once -- it was verified against the WIRE CSV, which
            # does spell it `team`. Same logic, different object, doc 80, and Matt caught it.
            _seat_tm, _job_tm = team_key(_fr.get('tm') or _fr.get('team')), team_key(r.get('team'))
            if _seat_tm and _job_tm and _seat_tm != _job_tm:
                _seat_cut.append((r['next_man'],
                                  f"he is on {_seat_tm} now, not {_job_tm}, so this is not a seat"))
                continue
            b = alt.get(hp['name'], bar) if hp else bar
            probe = {'name': r['next_man'], 'pos': 'RB', 'tm': r['team'], 'wk': s_rate,
                     'bye': int(float(r['bye'])) if r.get('bye') else 0}
            live = [v for v in price(probe, b)[0].values() if v is not None]
            fires = round((sum(live) / len(live) if live else 0.0) * s_wks, 1)
            odds, oband, owhy = seat_odds(r, sc)
            ev = round(odds * fires, 1)
            seat_best = max(seat_best, ev)
            priced.append((ev, fires, odds, oband, owhy, r, yours))

        # ORDERED BY WHAT IT IS WORTH, WHICH IS NEW (doc 343). While every row carried the same
        # probability the only thing that varied was the size of the job, so "ordered by the job"
        # was the honest caption. It is not any more.
        priced.sort(key=lambda t: (-t[0], -float(t[5].get('job_pays') or 0)))
        for ev, fires, odds, oband, owhy, r, yours in priced:
            if not yours and ev > 0.05:
                oddstxt = (f"about {odds:.0%} of the time" if not owhy
                           else f"about {odds:.0%} of the time (league average)")
                bandtxt = ''
                if oband:
                    bandtxt = (f" He took {E(r.get('wk1_share') and str(round(float(r['wk1_share'])*100)) or '?')}% "
                               f"of that backfield's work in week one, and backs in that range "
                               f"lost the man ahead of them {odds:.0%} of the time.")
                seat_moves_l.append({'sure': False, 'worth': ev, 'name': r['next_man'],
                                     'pos': 'RB', 'tm': r['team'], 'owned': _f(r.get('owned_pct')),
                                     'status': ((_free_by.get(norm_name(r['next_man'])) or {})
                                                .get('status') or ''),
                                     'touches': _touch_by.get(norm_name(r['next_man']), ''),
                                     'line': (f"Backup to {E(r['holds_the_job'])}. The job opens "
                                              f"{oddstxt}; if it does he is worth {fires:.1f} over "
                                              f"about {s_wks:.0f} weeks. Claim before the injury."),
                                     'weeks': [], 'empty': [], 'when': 0,
                                     # doc 443: his own free row, so THE CALL prints his vintage
                                     # and his last two games; the seat row prices the man ahead.
                                     'row': (_free_by.get(norm_name(r['next_man'])) or {})})
            # THE TAG BELONGS TO THE MAN AHEAD, NOT TO THE MAN IN THE FIRST COLUMN (doc 307).
            # live_tag is the STARTER's status and it was printed under the BACKUP's name, so
            # Kaelon Black's row read "15.4% rostered - questionable" when it is McCaffrey who is
            # questionable. Ten of the 32 rows carry a tag. This is doc 301's defect exactly: the
            # row named the wrong man. The tag now renders beside the starter, where it is true.
            holdtag = (f' &middot; <strong>{E(r["live_tag"])} now</strong>'
                       if r.get('live_tag') else '')
            # THE SPEARS RULE, PRINTED: a bench back earns his spot by the job he would inherit
            # and the fragility of the man ahead of him, never by his own projection (section 6).
            # inherit_2026.csv has carried the holder's 2025 games (`starter_g25`), his risk label
            # (`at_risk`: 'live tag' when he carries an injury tag today, 'baseline' when he does
            # not) and the next man's best two-week rate last season (`best_2wk_2025`) since
            # doc 275, and nothing read them. Plain words, blank when blank, display only.
            _g25 = str(r.get('starter_g25') or '').strip()
            _risk = str(r.get('at_risk') or '').strip().lower()
            holdfacts = ''
            if _g25:
                holdfacts += f' &middot; played {E(_g25)} of 17 last season'
            if _risk == 'live tag':
                holdfacts += ' &middot; at risk: carries an injury tag today'
            elif _risk == 'baseline':
                holdfacts += ' &middot; at risk: no injury tag today'
            elif _risk:
                holdfacts += f' &middot; at risk: {E(_risk)}'
            _b2 = str(r.get('best_2wk_2025') or '').strip()
            try:
                best2 = f'best two weeks last season: {float(_b2):.1f} a game'
            except ValueError:
                best2 = ''
            tag = ' &middot; <strong>your own man</strong>' if yours else ''
            ow = f'{r["owned_pct"]}% rostered' if r.get('owned_pct') else ''
            byetxt = f' &middot; bye {int(float(r["bye"]))}' if r.get('bye') else ''
            # HIS SHARE OF THAT BACKFIELD IN WEEK ONE -- the input the ordering was missing, and
            # a dash when there is no line for him, never a zero (section 3, doc 251).
            shr = (f'{round(float(r["wk1_share"]) * 100)}%'
                   if str(r.get('wk1_share') or '').strip() else '&mdash;')
            # WHAT THE SHARE CANNOT SAY, AND MATT NAMED IT (doc 350). "The type of opportunities
            # matter as well... some RBs are pass catching specialists and that role wont change
            # much with depth chart changes. Others are goal line and up the middle short yard
            # specialist... Others like Black can do it all, plus they are trusted with more
            # opportunity in that exact role." One combined number cannot tell those three apart,
            # and a low number on a specialist is not the same warning as a low number on a man
            # nobody trusts. Every field below was already on the drive and simply never joined.
            # PRINTED, NOT SCORED: none of it moves the odds or the sort, because the claim that
            # breadth predicts inheritance is NOT YET RUN (its testable form is in doc 350).
            _fw = _free_by.get(norm_name(r['next_man'])) or {}
            _ped = _ped_by.get(norm_name(r['next_man'])) or {}
            def _n(v):
                try: return float(str(v).strip())
                except (TypeError, ValueError): return None
            _tot, _tg = _n(r.get('wk1_work')), _n(_fw.get('w1_targets'))
            _ca = None if (_tot is None or _tg is None) else max(_tot - _tg, 0)
            if _ca is None or _tg is None:
                mix, role = '&mdash;', ''
            else:
                mix = f'{_ca:.0f} run &middot; {_tg:.0f} caught'
                if _tot and _tot >= 3:
                    _r = _tg / _tot
                    role = ('catches it' if _r >= 0.6 else
                            'runs it' if _r <= 0.2 else 'does both')
                else:
                    role = 'barely used'
            _sn = _n(_fw.get('snap_pct'))
            snaps = f'{_sn:.0f}%' if _sn is not None else '&mdash;'
            _rd, _pk, _yr = _ped.get('nfl_round'), _ped.get('nfl_pick'), _ped.get('nfl_year')
            ped = (f'round {E(_rd)}, pick {E(_pk)}' if _rd and _pk else '')
            if _yr:
                ped = (ped + f' &middot; year {E(_yr)}') if ped else f'year {E(_yr)}'
            buzz = (_fw.get('form_sig') or '').strip() or (_fw.get('screen') or '').strip()
            mixcell = (f'<span class="pl">{mix}</span>'
                       + (f'<span class="meta">{E(role)}'
                          + (f' &middot; {snaps} of snaps' if snaps != '&mdash;' else '')
                          + (f'<br>{ped}' if ped else '')
                          + (f'<br>{best2}' if best2 else '')
                          + (f'<br><b>{E(buzz)}</b>' if buzz else '')
                          + '</span>'))
            srow += (f'<tr><th scope="row"><span class="pl" title="{E(r["next_man"])}">{E(r["next_man"])}</span>'
                     f'<span class="meta">{E(r["team"])}{byetxt}{" &middot; " + ow if ow else ""}{tag}'
                     f'</span></th>'
                     f'<td><span class="pl" title="{E(r["holds_the_job"])}">{E(r["holds_the_job"])}</span>'
                     f'<span class="meta">his job is worth {E(r["job_pays"])} for the season{holdtag}'
                     f'{holdfacts}</span></td>'
                     f'<td class="rate">{shr}</td>'
                     f'<td>{mixcell}</td>'
                     f'<td class="tot{" pos" if fires > 0.05 else ""}">{fires:.1f}</td>'
                     f'<td{" title=" + chr(34) + E(owhy) + chr(34) if owhy else ""}>{odds:.0%}'
                     f'{"*" if owhy else ""}</td>'
                     f'<td class="tot{" pos" if ev > 0.05 else ""}">{ev:.1f}</td>'
                     # [doc 411] THIS CELL IS `why` AND THE HEADER SAID "his 2025".
                     # `best_2wk_2025` exists in inherit_2026.csv and is read by NOTHING, so the
                     # column had no source and printed the note instead. Matt hit the consequence
                     # before the mislabel: one of these notes is 900 characters, which forced a
                     # horizontal scrollbar and pushed the numeric columns off the right of the
                     # page. Header now says what the cell is; the note is clamped and the whole
                     # text stays in the tooltip.
                     f'<td class="why" title="{E(r["why"])}">{E(_clip(r["why"]))}</td></tr>')
        seat_tbl = _tbl('<tr><th class="corner" scope="col">be first to</th>'
                        '<th scope="col">if this man goes down</th>'
                        '<th class="rate" scope="col">his week 1</th>'
                        '<th scope="col">what he actually does</th>'
                        '<th class="tot" scope="col">if it fires</th><th scope="col">odds</th>'
                        '<th class="tot" scope="col">expected</th>'
                        '<th class="why" scope="col">why</th></tr>', srow,
                        'Best first. A star means no week-1 line, so league-average odds.')
        # [doc 439] Matt, 29 Sept, first "I'm not sure why i would need this", then the same
        # morning: "add back the players that have left the board, but make it collapsible. It is
        # valuable after further thought. I was frustrated with how long the page is." It is the
        # missing-row audit (0.5(c)5), so it stays, folded shut, with the full list and no cap.
        if _seat_cut:
            seat_tbl += ('<details class="leftoff"><summary>Left off: ' + str(len(_seat_cut))
                         + (' man' if len(_seat_cut) == 1 else ' men') + ', and why</summary><p>'
                         + '; '.join(f'<b>{E(nm)}</b> ({E(why)})' for nm, why in _seat_cut)
                         + '.</p></details>')
        seat_moves.extend(seat_moves_l)
    else:
        seat_tbl = (f'<div class="box bad"><h4>the seats are not on this page</h4>'
                    f'<p>{E(seatnote or "inherit_2026.csv was not read")}.</p></div>')

    floor = costs[0][0] if costs else 0.0
    # THE INSURANCE CASE (doc 291). A zero-cost body who plays behind a healthier starter at his own
    # position is not free: he is worth what he covers when that starter misses a game, and this page
    # does not price injuries yet. The verdict must say so rather than read the zero as a price.
    fp = costs[0][1] if costs else {}
    # [doc 410] "THE MAN HE COVERS" MEANS THE SAME NFL DEPTH CHART, NOT THE SAME FANTASY SLOT.
    # This selected every rostered player at the same POSITION with a higher rate and took the top
    # one, with NO team check, then the cost line said the cheapest man "covers" him. On 24 Sept
    # that printed: "the cheapest man you own is Jonah Coleman ... it holds only while Ashton Jeanty
    # stays healthy, because that is the man he covers." Coleman is DENVER. Jeanty is LAS VEGAS.
    # He covers nothing of Jeanty's. The man actually ahead of him is J.K. Dobbins, also Denver,
    # who is QUESTIONABLE -- which makes that seat worth MORE, the opposite of what the page said.
    # This is 8.6 in code: a bench back earns his spot by the job he would INHERIT, and you cannot
    # inherit a job on another team.
    ahead_of_fp = sorted((pl for pl in roster if pl is not fp and pl.get('pos') == fp.get('pos')
                          and pl.get('tm') and pl.get('tm') == fp.get('tm')
                          and pl.get('wk', 0) > fp.get('wk', 0)), key=lambda pl: -pl.get('wk', 0))
    insurance = (floor <= 0.05 and fp.get('name') != 'the open spot' and not fp.get('seat_note')
                 and fp.get('pos') in ('QB', 'RB', 'WR', 'TE') and bool(ahead_of_fp))
    scored = [b for b in bet_rows if b[0] is not None]
    best_ev = scored[0][0] if scored else 0.0
    best_nm = scored[0][1]['name'] if scored else ''
    unmeas = [b for b in bet_rows if b[0] is None]
    top = max(best_ev, seat_best)
    if best_ev <= floor + 0.05:
        verdict = (f'<div class="box bad"><h4>The bet does not clear its price</h4>'
                   f'<p>Best ticket <strong>{best_ev:.1f}</strong> against your cheapest drop '
                   f'<strong>{floor:.1f}</strong>. Wait; the screen fires as often later.</p></div>')
    elif top < 1.0:
        verdict = (f'<div class="box"><h4>It clears by almost nothing</h4>'
                   f'<p>Best ticket <strong>{top:.1f}</strong> against your cheapest drop '
                   f'<strong>{floor:.1f}</strong>. <strong>Take it only into a free spot.</strong>'
                   f'</p></div>')
    elif insurance:
        verdict = (f'<div class="box"><h4>It clears on paper</h4>'
                   f'<p>Best ticket <strong>{top:.1f}</strong>; cheapest drop '
                   f'<strong>{E(fp["name"])}</strong> at <strong>{floor:.1f}</strong>, but he backs up '
                   f'<strong>{E(ahead_of_fp[0]["name"])}</strong>. <strong>Swap only if you trust '
                   f'{E(ahead_of_fp[0]["name"])}&rsquo;s health.</strong></p></div>')
    else:
        verdict = (f'<div class="box"><h4>The bet clears its price this week</h4>'
                   f'<p>Best ticket <strong>{top:.1f}</strong> against your cheapest drop '
                   f'<strong>{floor:.1f}</strong>. <strong>Take it.</strong></p></div>')
    if unmeas:
        verdict += ('<div class="box"><h4>And one the arithmetic cannot price</h4><p>'
                    + ' &middot; '.join(f'<strong>{E(b[1]["name"])}</strong> at {b[4]:.1f} if it '
                                        f'fires' for b in unmeas[:3])
                    + '. No measured odds, so no expected value. Worth a free spot, not a drop.'
                      '</p></div>')
    if seat_best > 0.05:
        which = ('bigger' if seat_best > best_ev + 0.05 else
                 ('the same size as' if abs(seat_best - best_ev) <= 0.05 else 'smaller than'))
        _pb = (sc.get('p_opens_by_band') or {})
        _lo, _hi = (min(_pb.values()), max(_pb.values())) if _pb else (s_p, s_p)
        verdict += (f'<div class="box"><h4>The best seat is worth {seat_best:.1f}, {which} the '
                    f'best screen</h4><p>A backup scores <strong>{s_rate:.1f}</strong> a game while '
                    f'the job is open, for about <strong>{s_wks:.0f}</strong> weeks. Backs with 40% '
                    f'or more of their backfield in week 1 lost the man ahead '
                    f'<strong>{_hi:.0%}</strong> of the time, against <strong>{_lo:.0%}</strong> '
                    f'to {_pb.get("<20", _lo):.0%} for the rest.</p></div>')


    # THE SEAT BLOCK RIDES WITH THE PICKUPS, AT THE TOP (doc 349). Matt asked for this three times
    # before it was done, and the reason it kept looking done is that the seats WERE already merged
    # into the same `moves` list -- and then sorted by worth, where a 1-point seat lands below every
    # pickup and the five-row cap cut it. Merged and invisible is not merged. It gets its own
    # labelled block directly under the pickups, AND stays in the merged sort, so a seat that ever
    # outranks a pickup still appears in both places.
    seat_html = (
        '<h2 id="seats">The seat list &mdash; backups to a real job</h2>'
        '<p class="lede">Not men to start. Expected = if it fires &times; odds, comparable with '
        'everything else on this page.</p>'
        + (seat_tbl or ''))
    # [1 Oct, doc 460] THE LONG SHOTS: the same free men priced on the TAIL, which is the unit a team
    # behind in points wants. It leads the seat list when he is outside the top six by points for.
    _ls_html, _ls_leads = longshot_lane(freerows, rb_use, wr_use, const, pf, odds=playoff)
    seat_html = (_ls_html + seat_html) if _ls_leads else (seat_html + _ls_html)

    # ================= SECTION 0: THE MOVE, AND IT LEADS THE PAGE (doc 295) ==================
    # Matt, 2026-09-11: "I need the key players, trends and points of interest right off the bat at
    # the top of the page ... Provide the optimal move, and the context." Everything here is already
    # computed below; nothing is re-derived and nothing is typed by hand. One ranked list in one
    # unit -- points above YOUR bar -- with what it costs, how long to hold him, and the news.
    def _wks(ws):
        ws = sorted(ws)
        if not ws:
            return ''
        if len(ws) == 1:
            return f'week {ws[0]}'
        if len(ws) <= 3:
            return 'weeks ' + ', '.join(str(w) for w in ws[:-1]) + f' and {ws[-1]}'
        return f'{len(ws)} weeks, from week {ws[0]}'

    NOUN = {'K': 'kicker', 'D/ST': 'defense', 'TE': 'tight end', 'QB': 'quarterback',
                  'RB': 'back', 'WR': 'receiver'}

    news_by = {}
    for c in (cards or []):
        if not c.get('gone') and (c.get('news') or '').strip():
            news_by[norm_name(c.get('player'))] = c['news'].strip()

    # WHAT A WAIVER BODY AT THAT POSITION RETURNS PER PLAYED WEEK, hoisted above the moves loop
    # because doc 319 needs it there as well as in real_price() below. Same block, one read.
    _ab = const.get('absence', {}) or {}

    def _priced(c, p):
        """Per-week gain, season total and the weeks it comes from, in the position's own currency.

        [1 Oct, doc 467] A WEEKLY POSITION NEVER ENTERS THE PICKS ON A SEASON RATE. Doc 424 put
        season_priced() on THE CALL and the drop table; the priority list under them was never
        covered, and on 1 Oct it led with "Chiefs D/ST +7.8, outscores your defense in 10 weeks",
        a season number for a position the wire prices by the week's matchup (4.39). A defense or
        kicker enters this list only as a HOLE fill (a week with nobody in the slot), priced on the
        hole weeks alone, and the best man is CHOSEN on the hole weeks too: chosen on the season
        total, the first cut of this fix picked a kicker whose own bye was the hole and the week-8
        calendar row vanished. The matchup lane on the wire prices the rest of the season."""
        wkp, tot = price(c, bar)
        if season_priced(p):
            return wkp, tot
        hole = [w for w in WEEKS if bar[p][w] == 0 and (wkp[w] or 0) > 0.049]
        wkp = {w: (wkp[w] if w in hole else (None if wkp[w] is None else 0.0)) for w in WEEKS}
        return wkp, round(sum(wkp[w] for w in hole), 2)

    moves, ruled = [], []
    for p in POS:
        best, best_out = None, None
        for c in (r for r in freerows if r.get('pos') == p):
            wkp, tot = _priced(c, p)
            if tot <= 0.05:
                continue
            ws_ = [w for w in WEEKS if (wkp[w] or 0) > 0.049]
            if norm_name(c['name']) in dn:       # his ruling applies at SELECTION, not after
                if best_out is None or tot > best_out[1]:
                    best_out = (c, tot, ws_, wkp)
                continue
            if best is None or tot > best[1]:
                best = (c, tot, ws_, wkp)
        if best_out:
            ruled.append({'sure': True, 'worth': best_out[1], 'name': best_out[0]['name'],
                          'pos': p, 'hold': _wks([w for w in best_out[2]])})
        if not best:
            continue
        c, tot, ws, wkp = best          # doc 407: `when` needs the per-week shape, not just the weeks
        empty = [w for w in ws if bar[p][w] == 0]
        # THE WORDS ARE THE PRODUCT HERE. Matt, 2026-09-12: "this wording reads odd to me. That's
        # not how people write ... Make it fun to read and not a chore." The 11 Sept page printed
        # "so anybody who plays is the whole difference" three times in a row.
        noun = NOUN.get(p, p)
        if empty:
            # [doc 319 item 5] BOTH NUMBERS, because the headline one answers a question nobody is
            # asking. `tot` charges the empty slot at ZERO -- it is what he is worth against NOBODY,
            # and that is why four tight ends priced at 6.1 to 6.7 on the 15 Sept page when the
            # choice among them was worth about a point. The decision is against the man you would
            # claim INSTEAD, and doc 12 measured what that man returns per played week: QB 16.65,
            # TE 5.53, WR 6.54, RB 5.43 (the constants' absence block, the same rates real_price()
            # uses below). Netting them turns 6.1 into 0.6 and says the true thing: fill the hole,
            # do not pay to choose who fills it.
            # IT IS A FLOOR AND THE SENTENCE MUST NOT BE READ AS DOC 319's OWN NUMBER. Doc 319's
            # 1.2 for Schultz also credits him for the weeks LaPorta is absent, drawn at the
            # measured rates; this page sees byes only, so it cannot count those weeks. Same
            # direction, smaller. Never quote this figure as the simulator's.
            _strm = (_ab.get('streamer') or {}).get(p)
            _alt = None if _strm is None else round(tot - len(empty) * min(c['wk'], _strm), 1)
            if _alt is None:
                line = (f'No {noun} in {_wks(empty)}; he fills it. Hold him for {_wks(empty)} and '
                        f'let him go.')
            else:
                line = (f'No {noun} in {_wks(empty)}. Against any other free {noun} he is worth '
                        f'<b>{_alt:.1f}</b>, so fill the hole cheaply. Hold him for {_wks(empty)} '
                        f'and let him go.')
        else:
            line = f'Outscores your {noun} in {_wks(ws)}. Hold him for those weeks.'
        moves.append({'sure': True, 'worth': tot, 'name': c['name'], 'pos': p, 'tm': c['tm'],
                      'owned': _f(c.get('owned')), 'status': (c.get('status') or ''),
                      'touches': c.get('touches', ''),          # doc 314: term 4
                      'line': line, 'weeks': ws, 'empty': empty,
                      'when': first_material_week(wkp),
                      'row': c})                                # doc 443: THE CALL prints his inputs
    for _ev, c, lab, _today, fires, odds, _n, _cells in bet_rows:
        if _ev is None:
            continue
        if norm_name(c['name']) in dn:
            ruled.append({'sure': False, 'worth': _ev, 'name': c['name'],
                          'pos': c.get('pos', ''), 'hold': ''})
            continue
        # [1 Oct, doc 457] A BET THAT IS MOSTLY A BYE HOLE IS A CALENDAR CLAIM, NOT A CLAIM NOW.
        # Matt: "why am I being asked to roster TE Michael Mayer who is behind Brock Bowers?" Half
        # of what the row was worth was week 6, LaPorta's bye, where any tight end enters whole;
        # the calendar two inches below said to claim that man in week 5, and THE CALL said this
        # week. Section 6: a second tight end or quarterback is bought for the hole and the week
        # before it, never earlier. So a bet whose hole weeks carry 40% or more of "if it fires"
        # takes the week before its first hole as its claim week; a true ticket (Bell) stays now.
        _hole_w = [w for w in WEEKS if (_cells.get(w) or 0) >= (HP or 0) - 0.05]
        _hole_v = sum(_cells[w] for w in _hole_w)
        _bet_when = 0
        if HP and fires > 0 and _hole_w and _hole_v / fires >= 0.40 and c.get('pos') in ('TE', 'QB'):
            _bet_when = max(week or 0, _hole_w[0] - 1)
        moves.append({'sure': False, 'worth': _ev, 'name': c['name'], 'pos': c.get('pos', ''),
                      'tm': c.get('tm', ''), 'owned': _f(c.get('owned')),
                      'status': (c.get('status') or ''),
                      'touches': c.get('touches', ''),          # doc 314: term 4
                      'row': c,                                 # doc 443: THE CALL prints his inputs
                      # doc 379 (19 Sept): the rate must carry its POPULATION and HORIZON on the row,
                      # because doc 371 read this 38% against 4.30's 7.1% as a five-fold conflict, and
                      # they are two different objects (workload_note in sheet_constants.json says so).
                      # A screen rate printed beside a name without its group reads as his forecast.
                      'line': (f'{SHORT.get(lab, "Screen")}: {odds} of men like him became '
                               f'startable (a group rate, not his forecast). Worth about '
                               f'{fires:.0f} if it hits'
                               + (f', {fires / HW:.1f} a week for {HW:.0f} weeks.' if HW else '.')
                               + (f' <b>Claim him in week {_bet_when}, the week before your hole in '
                                  f'week {_hole_w[0]}, not now:</b> {_hole_v / fires:.0%} of that is the '
                                  f'hole, and the best man then will be named on the calendar.' if _bet_when else '')),
                      'weeks': [], 'empty': _hole_w if _bet_when else [], 'when': _bet_when})
    for _sm in seat_moves:
        (ruled if norm_name(_sm['name']) in dn else moves).append(_sm)
    # [doc 451] THE JOB THAT IS ALREADY OPEN. Doc 411 struck the open job off the seat list (a seat is
    # an option on a job still held) and nothing on this page picked it up: on 29 Sept Ollie Gordon II
    # sat at the top of the wire's IN DOUBT lane with De'Von Achane on injured reserve for the season,
    # and the week sheet did not carry his name. Matt found it. The seat above him on the inherit
    # file named Jaylen Wright (the chart's RB1, a stand-in at 7.45), so the row fell under the cap.
    # A job that is open is priced HERE, on the same unit as every other take: the seat constant's
    # relief rate (a group rate, not his forecast) against the bar, for the weeks the holder is out,
    # read off the news feed's return date where there is one. No odds term: the injury has happened.
    _oj_cut = []                                      # named under the picks, never silently dropped
    for _oj in (open_jobs or []):
        _nm = _oj.get('player') or ''
        _fr = _free_by.get(norm_name(_nm))
        if not (s_rate and s_wks):
            _oj_cut.append((_nm, 'no seat constant on file'))
            continue
        if _fr is None:
            _oj_cut.append((_nm, f"{_oj.get('tm') or '?'}, not priced: ESPN projects him at nothing"))
            continue
        if (_fr.get('status') or '').strip().upper() in GONE_FOR_WEEKS:
            _oj_cut.append((_nm, f"{_oj.get('tm') or '?'}, himself {(_fr.get('status') or '').replace('_', ' ').lower()}"))
            continue                                  # a cover who is himself out covers nothing
        # [1 Oct, doc 459] DID THE ABSENT MAN HOLD THE JOB, AND IS THIS THE MAN WHO INHERITS IT? See
        # rb_usage(). Without these two questions Tyler Badie was priced at the lead-back relief rate
        # behind Jonah Coleman, who never led Denver's backfield, and Kendre Miller behind Travis
        # Etienne, whose job goes to Alvin Kamara, who is rostered.
        _ru = rb_use or {}
        _tmk = team_key(_oj.get('tm') or _fr.get('tm') or '')
        _hk = norm_name(_oj.get('hurt'))
        _mates = {k: v for k, v in _ru.items() if v['team'] == _tmk}
        _hurt_u = _mates.get(_hk)
        if _hurt_u is not None and _mates:
            _others = {k: v for k, v in _mates.items() if k != _hk and v['games'] > 0}
            _lead = max(_others.values(), key=lambda v: v['pg']) if _others else None
            if _lead and _lead['pg'] > _hurt_u['pg']:
                _oj_cut.append((_nm, f"{_oj.get('tm') or '?'}: {E(_oj.get('hurt') or '?')} is out but never held the job; "
                                     f"{E(_lead['name'])} does ({_lead['pg']:.0f} touches a game to {_hurt_u['pg']:.0f}), "
                                     f"so this is a seat behind him at best"))
                continue
            _inh = max(_others.values(), key=lambda v: (v['last_week'], v['last'])) if _others else None
            if _inh and norm_name(_inh['name']) != norm_name(_nm) and _inh['last'] > (_ru.get(norm_name(_nm), {}).get('last') or 0):
                _oj_cut.append((_nm, f"{_oj.get('tm') or '?'}: {E(_oj.get('hurt') or '?')} is out, but {E(_inh['name'])} "
                                     f"inherits it ({_inh['last']:.0f} touches to {(_ru.get(norm_name(_nm), {}).get('last') or 0):.0f} "
                                     f"last game) and he is {'free' if norm_name(_inh['name']) in _free_by else 'rostered'}; "
                                     f"this man is behind him"))
                continue
        _hst = (_oj.get('status') or '').strip().upper().replace(' ', '_')
        _back, _wks_open = '', None
        _nl = news_lookup if isinstance(news_lookup, tuple) else ({}, {}, '')
        _nr = (_nl[1] or {}).get((norm_name(_oj.get('hurt')), 'RB', team_key(_oj.get('tm'))))
        _rd = (_nr or {}).get('return_date') or ''
        try:
            _rdt = dt.date.fromisoformat(_rd[:10]) if _rd else None
        except ValueError:
            _rdt = None
        if _rdt:
            # week w is played on the Sunday of 13 Sept 2026 + 7(w-1); he is back for the first week
            # whose Sunday is on or after his return date
            _out_w = [w for w in WEEKS if dt.date(2026, 9, 13) + dt.timedelta(days=7 * (w - 1)) < _rdt]
            _wks_open = len(_out_w)
            _back = _rdt.strftime('%d %b') if _out_w and _out_w[-1] < WEEKS[-1] else 'not this season'
        if _wks_open is None:
            _wks_open = 4 if _hst in ('INJURY_RESERVE', 'PUP') else int(round(s_wks))
            _back = 'no date on file'
        _wks_open = max(1, min(_wks_open, len(WEEKS)))
        _probe = {'name': _nm, 'pos': 'RB', 'tm': _oj.get('tm') or _fr.get('tm') or '', 'wk': s_rate,
                  'bye': int(float(_fr.get('bye') or 0) or 0)}
        _wkp = price(_probe, bar)[0]
        _open_weeks = [w for w in WEEKS[:_wks_open] if _wkp.get(w) is not None]
        _ev = round(sum(_wkp[w] for w in _open_weeks), 1)
        _hold = _hst.replace('_', ' ').lower()
        _line = (f"The job is open now: {E(_oj.get('hurt') or '?')} is {E(_hold)} (back {E(_back)}). "
                 f"Men in his seat score {s_rate:.1f} a game while a job is open (a group rate, not his "
                 f"forecast); against your bar that is {_ev:.1f} over {len(_open_weeks)} week"
                 f"{'s' if len(_open_weeks) != 1 else ''}"
                 + (f", bye week {_probe['bye']} left out" if _probe['bye'] in WEEKS[:_wks_open] else '')
                 + '.' + (f" In relief last game: {E(str(_touch_by.get(norm_name(_nm), '')))} carries and targets."
                          if _touch_by.get(norm_name(_nm)) else ''))
        _mv_oj = {'sure': False, 'worth': _ev, 'name': _nm, 'pos': 'RB', 'tm': _probe['tm'],
                  'owned': _f(_fr.get('owned')), 'status': (_fr.get('status') or ''),
                  'touches': _touch_by.get(norm_name(_nm), ''), 'line': _line,
                  'weeks': _open_weeks, 'empty': [], 'when': 0, 'row': _fr, 'open_job': True,
                  'oj_short': (f"{E(_probe['tm'])}, {_ev:.1f} over {len(_open_weeks)} week"
                               f"{'s' if len(_open_weeks) != 1 else ''}: {E(_oj.get('hurt') or '?')} "
                               f"{E(_hold)}, back {E(_back)}"),
                  'ahead': (f"behind {E(_oj.get('hurt') or '?')}, {E(_hold)} now, back {E(_back)}")}
        if _ev > 0.05:
            (ruled if norm_name(_nm) in dn else moves).append(_mv_oj)
        else:
            # [30 Sept] worth nothing against the bar is a result, and it is printed, not dropped
            _oj_cut.append((_nm, f"{_probe['tm']}, worth nothing against your bar over "
                                 f"{len(_open_weeks)} week{'s' if len(_open_weeks) != 1 else ''}"))
    # [doc 305] ONLY A MULTI-WEEK DESIGNATION IS DEMOTED. A ONE-WEEK "OUT" IS NOT.
    # Doc 304 demoted everything in GONE_FOR_WEEKS and Matt corrected it the same night: "out one
    # week is one thing and we shouldn't rule the player out of consideration ... most of my pickup
    # options are not going to be play-right-away options anyway ... let's not over correct."
    # He is right, and the two sets are different OBJECTS, not degrees of one thing:
    #   OUT is ESPN's GAME status for ONE game. Jalen McMillan carried it on 13 Sept with a knee,
    #     DOUBTFUL on the league report and LIMITED participation in practice. That is a man
    #     missing a game, not a man missing a month, and a stash is bought for the month.
    #   INJURY_RESERVE / PUP / SUSPENSION / NOT_ACTIVE are ROSTER designations measured in weeks
    #     (IR and PUP carry NFL minimums), so they do change what a claim is worth this period.
    # So the demotion narrows to the multi-week set, and a one-week OUT keeps its rank and its
    # existing warning line. The real reason Black should outrank McMillan is his 45% share, which
    # is AUDIT_LEDGER row 29 and is a missing INPUT, never an ordering patch. Do not fix a missing
    # column by demoting the rows it would have outranked.
    MULTIWEEK = frozenset({'INJURY_RESERVE', 'SUSPENSION', 'PUP', 'NOT_ACTIVE'})
    _gone = lambda m: 1 if (m.get('status') or '').strip().upper() in MULTIWEEK else 0
    moves.sort(key=lambda m: (_gone(m), -m['worth'], not m['sure']))

    # [doc 303] A dead FIRST build of cost_line stood here and was overwritten, unread, by the
    # real one below. It still carried the sentence "this page prices byes and not injuries",
    # which stopped being true when real_price() shipped on 12 Sept. It never reached the page --
    # doc 302 flagged it as POTENTIALLY LIVE and it was not -- but it is two constructions of one
    # string in one function (0.5c4), and the false sentence was one reordering away from print.
    # Deleted rather than corrected: there is only one cost box and it is built below.

    # ---- WHAT A DROP REALLY COSTS, promoted above the picks because it gates every one -------
    # Matt, 2026-09-12: "Anything that has bearing on what decisions I make deserves prominence and
    # should be stated assertively prior to me reviewing the hot takes." This page counts BYES only
    # and charges an empty slot at ZERO, and both are wrong in the same direction for a bench body,
    # who exists for the weeks the man ahead is out. Doc 297 measured it on his own fifteen; this
    # applies the same correction live, so the page stops printing 0.0 for a man worth four.
    # (_ab is read once, above the moves loop.)

    def real_price(pl, shown):
        rate = (_ab.get('rate') or {}).get(pl.get('pos'))
        strm = (_ab.get('streamer') or {}).get(pl.get('pos'))
        if pl is None or rate is None or strm is None:
            return None
        wks = len([w for w in WEEKS if pl.get('bye') != w])
        return shown + rate * wks * max(0.0, (pl.get('wk') or 0) - strm)

    # ---- HOW MANY RIVALS WILL FILE ON HIM -- section 4.32's term 4, doc 314 ------------------
    # Doc 254 logged this as NOT YET RUN and expected it to need a model of the other eleven
    # rosters. It does not. A positional-hole flag adds 0.20 expected filers against a 0.30 bar
    # FIXED BEFORE THE TEST, and held out by season it makes the prediction worse. What does
    # predict is one number: targets plus carries in the man's last completed game.
    _CT = const.get('contest') or {}
    _CT_BANDS = _CT.get('bands') or []

    def contest(m):
        """(short tag, long sentence). Both empty when the man has no last game on file -- a
        missing workload line is NOT a quiet week, it is no information, and a default of zero
        would print 'nobody else wants him' about a man nobody has measured (doc 251)."""
        raw = m.get('touches')
        if raw in (None, '') or not _CT_BANDS:
            return '', ''
        try:
            t = float(raw)
        except (TypeError, ValueError):
            return '', ''
        b = next((b for b in _CT_BANDS if b['lo'] <= t < b['hi']), None)
        if b is None:
            return '', ''
        tag = f'{b["contested"]:.0%} contested'
        many = b['contested'] >= 0.38
        # THE UNIT IS CARRIES PLUS TARGETS, NOT TOUCHES (doc 325). `build_form.py` writes
        # `touches = targets + carries`, which is OPPORTUNITIES: a receiver thrown at nine times
        # and catching seven reads as nine here. Doc 314's bands were FITTED on this same column,
        # so the finding is unaffected -- but the printed sentence said "touched the ball" and that
        # overstated every pass-catcher on the page. 0.1's scope rule: the plain words have to be
        # true. Two outside columns describing the same 49ers backfield are what surfaced it.
        long = (f'{t:.0f} carries and targets last game; men like that are contested '
                f'<b>{b["contested"]:.0%}</b> of the time. '
                + ('<b>Put him first.</b>' if many else 'He can sit below a name you would miss more.'))
        return tag, long

    def _contest_share(m):
        """[doc 462] the contested share for the man's last-game band, or None (no game on file)."""
        raw = m.get('touches')
        if raw in (None, '') or not _CT_BANDS:
            return None
        try:
            t = float(raw)
        except (TypeError, ValueError):
            return None
        b = next((b for b in _CT_BANDS if b['lo'] <= t < b['hi']), None)
        return None if b is None else b['contested']

    def _mv(m, rank):
        """One pickup. The POINTS are the headline, because that is what he reads first."""
        own = (f' &middot; {m["owned"]:.0f}% rostered' if m.get('owned') is not None else '')
        st = ((m.get('status') or '').replace('_', ' ').title())
        st = f' &middot; <b class="warn">{E(st)}</b>' if st and st.upper() != 'ACTIVE' else ''
        news = news_by.get(norm_name(m['name']), '')
        newsh = f'<p class="nws">{E(news)}</p>' if news and rank == 1 else ''
        ctag, clong = contest(m)
        ctagh = f' &middot; <b>{ctag}</b>' if ctag else ''
        # WHO GETS THE SENTENCE, and the first version of this got it backwards. It went to the top
        # two, which tells him to put first the man who is already first. The decision this serves
        # is REORDERING, so the sentence follows the CONTESTED man wherever he sits on the list --
        # rank four is exactly where he is easiest to lose. Ranks one and two keep theirs either
        # way, because "nobody is racing you for him" is what lets a quiet leader be demoted.
        clongh = (f'<p class="ctx fine">{clong}</p>'
                  if clong and (rank <= 2 or 'Put him first' in clong) else '')
        return (f'<div class="mv{" big" if rank == 1 else ""}">'
                f'<p class="act"><span class="rank">{rank}</span>'
                f'<b class="nm" title="{E(m["name"])}">{E(m["name"])}</b>'
                f'<span class="mmeta">{E(m["pos"])} &middot; {E(m["tm"])}{own}{st}{ctagh}</span>'
                f'<span class="pill{" sure" if m["sure"] else ""}">'
                f'{"+" if m["sure"] else ""}{m["worth"]:.1f}'
                f'<em>{"points" if m["sure"] else "points, expected"}</em></span></p>'
                f'<p class="ctx">{m["line"]}</p>{clongh}{newsh}</div>')

    # ---- THIS WEEK versus THE CALENDAR --------------------------------------------------------
    # Matt, 2026-09-12: "Week 1 - the move. This section doesn't make sense. Instead of listing the
    # top takes for that week, it list D/ST and other positions to take in later weeks." He is
    # right, and it was the design, not a slip: the list was sorted on season points, so three bye
    # fills for weeks 6, 8 and 11 outranked anything a man could do in week one. A fill he does not
    # need for a month is a CALENDAR row, keyed to the week he should CLAIM, and the names in it
    # will move, so it says so.
    now = [m for m in moves
           if not (m['sure'] and m['when'] and week and m['when'] >= week + 2)]
    later = sorted((m for m in moves if m not in now), key=lambda m: m['when'])

    # ---- WHAT EVERY MAN YOU OWN COSTS TO DROP (doc 317) ---------------------------------------
    # Matt, 16 Sept: "How do i know drop cost of my players? do i have to pull out a calculator".
    # No, and he should never have had to ask: drop_costs() has computed all fifteen since doc 240
    # and the page printed ONE of them, the cheapest, inside a sentence. The whole ladder is free.
    # Two corrections are folded in so the printed number is the one to act on:
    #   - the SEAT, for a man whose value is the job he would inherit rather than his own starts
    #     (already in `adj` above), and
    #   - the ABSENCE term, real_price(), because the projection prices bye weeks and nothing else,
    #     which is what printed 0.0 beside Hockenson and sent Matt to a calculator (ledger row 25).
    # AND THE COST IS NET OF WHOEVER TAKES THE SEAT. drop_costs() removes a man and puts NOBODY
    # in his place, which is right for the cheapest-ticket question it was built for and wrong as
    # a price: it said dropping the kicker costs 118.7, when the answer is that you add a kicker.
    # 4.16's table is exactly this point -- QB adds hit 62% and RB adds 22%, so the same man is
    # cheap at one position and dear at another. K and D/ST carry no free rows on this wire
    # (4.8/4.9 keep them off it), so they are NOT priced rather than priced wrong.
    # NOTE the variable names. The first draft called the loop variable `_f`, which is the name of
    # a helper defined OUTSIDE this function and used forty lines above -- Python then treated `_f`
    # as local for the whole function and the page died with UnboundLocalError at a line I had not
    # touched. Caught by the control, not by reading.
    # [doc 420] "NOT PRICED" READ AS "FREE", AND THAT IS THE WHOLE COMPLAINT. Matt, 24 Sept:
    # *"The call makes no sense, i should drop both defenses and a kicker if i do that math? What
    # is good about the Jet's d/st? Who am i replacing my kicker with? Those points don't
    # realistically add up... If i drop my kicker i'm not going to gain 1.8 points, lol."*
    # He is reading the table below, which lists EVERY man he owns sorted by cost, and his two
    # defenses and his only kicker sat at the bottom of it with no number at all. A drop table in
    # which three men have no price is a drop table that nominates those three.
    # WHY THEY HAD NO PRICE: 4.8 and 4.9 keep K and D/ST off the wire on purpose, so `_bestfree`
    # has no row at those positions and the replacement-aware cost could not be computed. The
    # previous fix printed "not priced" rather than drop_costs()'s raw 118.7, which was right to
    # reject (the answer to dropping a kicker is that you add a kicker) and wrong to leave blank.
    # ~~WHAT REPLACES THEM IS A STREAMED BODY, AND FOR D/ST THAT IS MEASURED: 5.99 a week, D/ST12's
    # season average (doc 265). His two sit at 5.68 and 6.09, so both are AT replacement.~~
    # [doc 421] RETRACTED THE SAME EVENING, BEFORE IT REACHED HIS DRIVE. Matt sent ESPN's week 3
    # defense projections: **his Chiefs project 7.8, TIED FOR THE BEST DEFENCE IN THE LEAGUE THIS
    # WEEK** (at Miami). This page called them 5.7 and called dropping them an upgrade.
    # THE TWO NUMBERS ARE DIFFERENT OBJECTS. 5.7 is a season-long per-game rate. 7.8 is a WEEK-3
    # MATCHUP. For a skill player those are close enough to argue about; for a defense they are
    # barely related, because 4.33 already measured that at D/ST you take the SCHEDULE and not the
    # player. Comparing a season average against a season-average replacement answers "is this a
    # good defense to roster all year", and the question on the page is "should I drop him now".
    # 0.5(a6) names this exactly: the ceiling, the floor and the present have different answers,
    # and the wrong one is not a partial answer, it is a wasted one.
    # AND THE BAR WAS WRONG TOO, not just the rate. The right bar is not a league-wide season
    # constant; it is THE BEST DEFENCE ACTUALLY FREE THAT WEEK. In his pool that is the Giants at
    # 6.8, with the Saints at 6.4 behind them. Against that bar the Chiefs (7.8) are the best thing
    # available to anybody and the Bengals (5.9) are about a point light -- which is a real,
    # small, ONE-WEEK call and nothing like "both are droppable".
    # WHY THE PAGE COULD NOT SEE ANY OF THIS: 4.8 and 4.9 keep K and D/ST off the wire on purpose,
    # which is right for a draft board and wrong in week 3. The page does not know the Giants and
    # Saints are sitting there free. A constant was reached for because the pool was missing, and
    # it turned a blank into a confident error. **A blank is bad; a confident wrong number is
    # worse, because the blank made him ask and the number would not have.**
    # SO: no synthetic replacement. The row says what is true and points at the one place the
    # answer actually lives. Getting the weekly D/ST pool onto the page is queued (doc 421).
    STREAMED = {}
    # [doc 422] THE GENERAL FORM OF 421, BECAUSE A SPECIAL CASE ONLY PROTECTS THE CASE IT NAMES.
    # Matt: "how are we still at the stage of pulling the wrong numbers. that's what the red team
    # process is meant to solve for." He is right that removing the defense constant fixed one row
    # and nothing else. The real property is that SOME POSITIONS ARE WORTH WHAT THEY DO THIS WEEK
    # and the rest are worth a rate held over many weeks, and this page only computes the second.
    # A defense is its matchup (4.33, measured). A kicker is his matchup and his leg. Printing a
    # season rate against either is a horizon mismatch: a correct number answering a question
    # nobody asked, which is 0.5(a6)'s failure with a number instead of a sentence.
    # Naming it here means the next position that behaves this way gets the protection by joining
    # a set, not by someone remembering doc 421.
    # [doc 420] AND THE REPLACEMENT MUST NOT BE A MAN HE ALREADY OWNS. The page printed
    # "Tre Tucker -- replaced by Tre Tucker at 9.3". He is on the roster AND on the free list:
    # WIRE_20260923.csv carries him while MY_ROSTER.csv has him owned, because the two files are
    # written at different moments and the wire one on disk can be a day old. Dropping a man never
    # makes him available to replace himself, and a roster-mate is not a replacement either --
    # he is already counted in the lineup the cost is measured against, so using him would credit
    # one body twice. Filter by name AND position (3: never less).
    _own = {(norm_name(x.get('name')), x.get('pos')) for x in roster}
    _bestfree = {}
    for _fr in freerows:
        _fp = _fr.get('pos')
        if (norm_name(_fr.get('name')), _fp) in _own:
            continue
        if _fp and (_fp not in _bestfree or (_fr.get('wk') or 0) > (_bestfree[_fp].get('wk') or 0)):
            _bestfree[_fp] = _fr
    for _sp, (_swk, _slabel) in STREAMED.items():
        if _sp not in _bestfree:
            _bestfree[_sp] = {'name': _slabel, 'pos': _sp, 'tm': '', 'bye': 0, 'wk': _swk,
                              'streamed': True}
    _basefull = season(roster)
    _rows_acc = []
    for _c, _pl in adj:
        if _pl.get('name') == 'the open spot':
            continue
        # [doc 422] The property decides, not whether the wire happened to carry a free row. If a
        # free defense ever appears there, a season rate for it is still the wrong number.
        _rep = _bestfree.get(_pl.get('pos')) if season_priced(_pl.get('pos')) else None
        if _rep is None:
            # [doc 420, corrected by doc 421] Kickers and defenses both land here, and for the same
            # reason: neither is on this wire, so the page cannot see who is free. Naming the gap
            # beats both a blank and a made-up number.
            _pp = _pl.get('pos')
            _net = None
            if _pp == 'D/ST':
                _note_rep = ('a defense is worth its MATCHUP, not its season average, and this '
                             'page cannot see which defenses are free this week &mdash; check '
                             'ESPN&rsquo;s weekly D/ST projections before you move one')
            else:
                _note_rep = ('you must put another kicker in this slot the same week, and this '
                             'page does not price kickers')
        else:
            _rest = [x for x in roster if x is not _pl]
            _net = _basefull - season(_rest + [_rep])
            _note_rep = (f'replaced by {E(_rep["name"])}, the average one, at {_rep.get("wk", 0):.1f}'
                         if _rep.get('streamed')
                         else f'replaced by {E(_rep["name"])} at {_rep.get("wk", 0):.1f}')
        _r = real_price(_pl, _c)
        _absence = max(0.0, (_r - _c)) if _r is not None else 0.0
        _shown = None if _net is None else _net + _absence
        _note = _pl.get('seat_note') or ''
        _note = (_note + ' &middot; ' if _note else '') + _note_rep
        if _absence > 0.4:
            _note += f' &middot; {_absence:.1f} of it is the weeks he misses'
        # [doc 420] A NEGATIVE COST IS NOT A BARE MINUS SIGN. It means the replacement is better
        # than the man, which is a real upgrade and the reader should be told in words. 416 already
        # keeps it out of THE CALL's net; this is the other half, on the page he reads.
        if _shown is not None and _shown < -0.05:
            _note += ' &middot; <b>the replacement is better: this is an upgrade, not a cost</b>'
        if _is_parked(_pl):
            _note += (' &middot; <b>he is in the injured-reserve slot, so dropping him frees no roster '
                      'seat and cannot pay for a claim'
                      + (f' unless you then move {E(", ".join(_ir_elig))} into it' if _ir_elig else '')
                      + '</b>')
        _rows_acc.append((_shown, _pl, _note))
    _rows_acc.sort(key=lambda t: (t[0] is None, t[0] if t[0] is not None else 0))
    # NB the kwarg is news_lookup, not news. `news` is rebound TWICE inside render() already
    # (lines ~1580 and ~2190, both to strings), so a `news=` parameter was a string by the time
    # this line ran and unpacked as 'too many values'. Second name collision in this function
    # today, after `season` shadowed season(). Grep before naming a parameter in here.
    _news_id, _news_key, _news_err = (news_lookup or ({}, {}, 'news not loaded'))
    droprows = ''
    for _shown, _pl, _note in _rows_acc:
        _txt = 'not priced' if _shown is None else f'{_shown:.1f}'
        _ts = this_season_text(_pl)               # doc 435: the season beside the blend
        _mu = matchup_text(_pl, matchup)          # doc 468: the matchup beside it, RB and TE
        droprows += (f'<tr><th scope="row"><span class="pl">{E(_pl["name"])}</span>'
                     f'<span class="meta">{E(_pl.get("pos", ""))}'
                     + (f' &middot; bye {_pl["bye"]}' if _pl.get('bye') else '')
                     + (f' &middot; {_ts}' if _ts else '')
                     + (f' &middot; {_mu}' if _mu else '')
                     + (f' &middot; {_note}' if _note else '')
                     + (f' &middot; <b class="hurt">{E(_nn)}</b>'
                        if (_nn := news_note(_pl, _news_id, _news_key)) else '')
                     + (' &middot; <b>you have ruled this one out</b>'
                        if norm_name(_pl.get('name')) in dn else '')
                     + '</span></th>'
                     + rate_cell(_pl) +
                     f'<td class="tot{" pos" if (_shown or 0) > 0.05 else ""}">{_txt}</td></tr>')

    drop_tbl = _tbl('<tr><th class="corner" scope="col">if you drop him</th>'
                    '<th class="rate" scope="col">pts/wk</th>'
                    '<th class="tot" scope="col">it costs</th></tr>', droprows,
                    'Cheapest first: what your starting nine loses over the weeks left once the '
                    'best free man takes the seat.')

    est = real_price(fp, floor) if fp else None
    if (seats_used or 0) >= 15:
        cost_line = (f'<b>Cheapest drop:</b> <b>{E(fp.get("name", "?"))}</b>')
        if est is not None and est > floor + 0.4:
            cost_line += (f', <b>{floor:.1f}</b> (nearer <b>{est:.0f}</b> once injuries ahead of '
                          f'him count)')
        else:
            cost_line += f', <b>{floor:.1f}</b>'
        # [doc 410] ... and if this season says otherwise, SAY SO HERE, not only in the table
        # further down. Matt quoted this exact sentence back: the page called Jonah Coleman 0.0
        # while its own block two screens up had him at 6.7 a game. One page, two numbers, one man.
        # NB the kwarg is season_rates, not season: `season()` is already a function in this
        # module and a `season=` kwarg SHADOWED it, so render() died on base = season(roster).
        # [doc 415] TWO DIFFERENT UNITS AND I PUT THEM IN ONE SENTENCE WITH "BUT". Matt: "huh?"
        # He was right to stop. `floor` is the DROP COST -- what the starting nine loses if this
        # man goes. `_sp[0]` is POINTS A GAME. A man can average 6.7 and still cost 0.0 to drop,
        # because he never enters the nine; those two numbers do not contradict each other and
        # "this season disagrees" said they did. What IS stale is the RATE the drop cost was
        # computed FROM, which is his preseason pts/wk. Compare that with that.
        _sp = (season_rates or {}).get(fp.get('name'))
        _rate = fp.get('wk') or 0.0
        if _sp and abs(_sp[0] - _rate) >= 4.0:
            cost_line += (f'. Priced at {_rate:.1f} a week; he is averaging <b>{_sp[0]:.1f}</b> '
                          f'this season, so treat {floor:.1f} as a floor')
        if insurance:
            cost_line += (f'. It holds only while <b>{E(ahead_of_fp[0]["name"])}</b>, the man '
                          f'he backs up, stays healthy')
        cost_line += '.'
    else:
        cost_line = '<b>You have a free roster spot.</b> The first pickup needs no drop.'

    if now:
        top = now[0]
        ok = top['worth'] > floor + 0.05
        spec = bool((not top['sure']) and week and week <= 1)
        if not ok:
            call = ('<p class="call no">None of it clears what the drop costs. Stand pat this week; '
                    'the page will say so again next run.</p>')
        elif spec:
            # doc 252: a week-one claim hit 9%, a week-two claim 35%, on the same pool.
            call = ('<p class="call no">Every name here is a bet, and a bet made in week one is made '
                    'on a depth chart nobody has tested yet. One week of patience has measured at '
                    'roughly three times the hit rate, and none of these men will be gone.</p>')
        else:
            call = '<p class="call yes">It clears what it costs. Do it.</p>'
        _st = (top.get('status') or '').upper()
        if _st and _st != 'ACTIVE' and ok:
            call += (f'<p class="call no">ESPN has him {E(_st.replace("_", " ").title())}. Let the '
                     f'week start before you spend the drop on him.</p>')
        # WHY FIVE AND NOT THREE. Matt, 2026-09-15: "This file can't be right since it doesn't
        # have but the same 3 players for Priority pickups." He was right, and the cap was the
        # SMALLEST of the three reasons (doc 308): the real one was that no 2026 in-season input
        # reached this page, so the same preseason names printed every week. With the week-1
        # workload lane in, this list has real rows below three for the first time, and the cap
        # now genuinely bites. Five, not ten: the section is read at a glance and a long list is
        # a ranking he has to adjudicate, which is the work he pays this page to do.
        # AND THE CAP MUST NOT EAT THE ROW THE PAGE ITSELF SAYS TO CLAIM FIRST (doc 316,
        # RESTORED 18 Sept -- doc 345). Matt, 16 Sept: "Black is no longer on the priority
        # pickups." He was right and the tag fix of the night before did not reach him: Kaelon
        # Black carried 15 carries and targets, the only 56%-contested row on the wire, and he
        # sat BELOW the cut on worth, so `now[:5]` cut him before his own warning could be read.
        # A cap that hides the row the page is shouting about is 0.5(c)5's missing-row defect
        # with a deliberate-looking cause. So: keep five, then re-admit any row below the cut
        # whose contest band says to claim him first. This changes WHAT IS SHOWN, never the
        # ORDER -- 4.32's terms stay as they are, and docs 255-257 are the record of why I do
        # not get to invent an ordering rule here.
        # THE RE-ADMIT KEYS ON THE SENTENCE, NOT ON THE THRESHOLD, ON PURPOSE. contest() decides
        # at one place whether a man gets "Put him first"; a second copy of 0.38 here could drift
        # away from it silently, and a row re-admitted without the sentence would be the defect
        # inverted. Guarded by C23 in redteam_controls.py, which fails on the pre-restore code.
        _picks_shown = list(now[:5])
        for _m in now[5:]:
            if 'Put him first' in (contest(_m)[1] or ''):
                _picks_shown.append(_m)
        picks = ''.join(_mv(m, i + 1) for i, m in enumerate(_picks_shown))
        # [30 Sept, the first live run of P3] AN OPEN JOB BELOW THE FIVE-ROW CUT IS NAMED, WITH ITS
        # PRICE. The 07:30 run priced Kendre Miller at 2.3 for the one week Etienne is out and DeeJay
        # Dallas at 6.9, both fell under now[:5], and the guard fired on Miller (Dallas happened to be
        # named in the seat lane's left-off line, which is not the decision). Doc 451's rule is that
        # an open job is a claim this week and the sheet names the man; the cap decides what is shown
        # in full, never what is named. Same treatment as the seat lane's left-off line (doc 411).
        _oj_under = [m for m in now if m.get('open_job') and m not in _picks_shown]
        if _oj_under:
            picks += ('<p class="ctx fine">Open jobs below the cut, priced the same way: '
                      + '; '.join(f'<b>{E(m["name"])}</b> ({m["oj_short"]})' for m in _oj_under)
                      + '. Claim one only if a row above does not clear.</p>')
        if _oj_cut:                                   # doc 451: an open job this page could not price
            picks += ('<p class="ctx fine">Open jobs not priced here: '
                      + '; '.join(f'<b>{E(nm)}</b> ({E(why)})' for nm, why in _oj_cut)
                      + '. The wire lists them; each line says why this page does not.</p>')
    else:
        call = ''
        picks = ('<div class="mv big"><p class="act"><span class="rank">&mdash;</span>'
                 '<b class="nm">Nothing this week</b></p><p class="ctx">Not one free player beats '
                 'your own nine in a week you need him. That is the answer, not a gap in the '
                 'sheet.</p></div>')
    # ---- [doc 415] THE CALL: one row per complete decision, and it goes FIRST ---------------
    # Matt, 24 Sept: "consider the inputs i need to make an informed decision for who i should
    # pick up and who i should drop and when ... to me the info seems broken out all over the
    # place ... the most useful information needs to be grouped and at first read."
    # Every number in this table already existed on the page. It was in four places: the pickup
    # worth in Priority pickups, the drop cost in "what each of your own men costs to drop", the
    # week in the calendar, the injury in the drop table. Nobody can hold four tables in their
    # head. THE PAIRING IS THE POINT: the Nth add is charged the Nth CHEAPEST drop, because that
    # is what taking N men actually costs you. Nothing here is a new calculation.
    _dec = ''
    # A man he has ruled out is never offered as the drop (doc 415). He still appears in the
    # full drop table below with his cost, because knowing what he costs is not the same as
    # being asked to cut him.
    _cheap = [(c, pl) for c, pl, _n in _rows_acc
              if c is not None and norm_name(pl.get('name')) not in dn and not _is_parked(pl)]
    if now and _cheap:
        # ONE ROW PER POSITION, AND THE REASON IS ARITHMETIC, NOT TIDINESS. Every `worth` here is
        # priced against the bar AS IT STANDS. The moment you add the best tight end, that bar
        # moves and every other tight end on the list is worth a fraction of what it says. The
        # first build of this table printed FOUR tight ends in five rows, three of them at an
        # identical +13.1, and totalled them to "+54.4" -- a number he cannot have, since the
        # league caps TE at 3 and 6's doctrine caps it at 2. A table that adds up impossible
        # rows is worse than four scattered tables, because it looks decided (0.1(f2)).
        # [doc 424] AND THE SAME PROPERTY MUST GOVERN THE ADD SIDE. Doc 422 put WEEKLY_VALUE on
        # the DROP lookup and stopped there, so the page could still OFFER a defense on a season
        # rate -- and it did, the same night: "take Jets D/ST +1.5, drop Tre Tucker 5.8, net -4.3".
        # Matt: "it still has me picking up Jets D/ST and that doesn't compute." He is right twice
        # over, and his own line about this is the lesson: "the guard has to be designed correctly
        # because those have been faulty too."
        # A HALF-APPLIED PROPERTY IS WORSE THAN NO PROPERTY, because the half that is covered makes
        # the whole thing look handled. One predicate, used by both sides, so they cannot diverge.
        _seen_pos, _picked = set(), []
        for _m in now:
            # [1 Oct, doc 470] A WEEKLY POSITION ENTERS THE CALL ONLY AS A HOLE FILL. Since doc 467 a
            # defense or kicker can only be in `moves` priced on the hole weeks (never on a season rate,
            # which was doc 424's defect), so the week before a bye the kicker or defense that fills it
            # takes a row here and a row on the card with its drop, which is what Matt asked for:
            # "will it also contain Kickers and D/ST when they apply?" Doc 424's rule still holds for
            # every other case: no hole, no row.
            if not season_priced(_m.get('pos')) and not _m.get('empty'):
                continue
            if _m.get('pos') in _seen_pos:
                continue
            _seen_pos.add(_m.get('pos'))
            _picked.append(_m)
            if len(_picked) == 5:
                break
        # [doc 417] AND THE DROP MUST NOT BE AT THE ADD'S OWN POSITION. `worth` is priced against
        # the bar AS IT STANDS, which INCLUDES the man being dropped. Pair "take Schultz (TE)"
        # with "drop LaPorta (TE)" and the +11.1 is measured against a bar that the drop destroys:
        # it is a straight swap wearing an add's price tag. Surfaced the moment the measured blend
        # went live and LaPorta stopped out-scoring the free tight ends. Walk to the next cheapest
        # man at a DIFFERENT position; the same-position swap is a real move but it is a
        # REPLACEMENT decision, not an add, and it is not what this table prices.
        # [doc 420] AND THE ROSTER AFTER THE MOVES MUST STILL FIELD A LEGAL NINE. Matt called this
        # before it was live: *"i should drop both defenses and a kicker if i do that math?"* The
        # moment D/ST got a price (a streamed defense at 6.0), both of his defenses became cheap
        # drops and the ladder took BOTH -- leaving the D/ST slot empty. The second one does not
        # cost 0.8. It costs the whole slot, because there is no third defense behind it.
        # Each drop is priced ONE AT A TIME against the full roster, which is right for any single
        # move and wrong for a set of them, and nothing was checking the set. 0.1(h) rule 4 has
        # required "the fifteen after the move" in every take since doc 378; it was a sentence in
        # a reply and never a line of code. It is a line of code now.
        # FLOORS ARE THE STARTING NINE (2): QB 1, RB 2, WR 2, TE 1, D/ST 1, K 1, plus one FLEX,
        # so RB+WR+TE must keep 6 bodies between them and not merely 5.
        _floor = {'QB': 1, 'RB': 2, 'WR': 2, 'TE': 1, 'D/ST': 1, 'K': 1}
        _left = collections.Counter(x.get('pos') for x in roster if not _is_parked(x))
        _flexpos = ('RB', 'WR', 'TE')
        _flexmin = sum(_floor[q] for q in _flexpos) + 1        # the FLEX body
        def _may_drop(pos):
            if _left.get(pos, 0) - 1 < _floor.get(pos, 0):
                return False
            if pos in _flexpos and sum(_left.get(q, 0) for q in _flexpos) - 1 < _flexmin:
                return False
            return True
        _drows, _run, _used, _skipped, _shown_n, _later_n = '', 0.0, set(), 0, 0, 0
        # [1 Oct, doc 462] A SAME-POSITION DROP IS ALLOWED WHEN THE MAN NEVER STARTS. Doc 417's rule was
        # written for LaPorta: a starter who IS the bar. Vele is not in the bar in any week (0.0 on the
        # bye grid), so dropping him moves no bar and the pairing is exact; refusing him walked the
        # ladder past two free receivers to "drop Sam LaPorta" for a receiver worth +6.3. Matt, 1 Oct:
        # "my player of lowest value ... should come first for each player i want to pick up."
        _grid = {id(_pp): _cc for _cc, _pp in adj}
        _wf_rows = []
        # the hedge man: the cheapest drop who never starts on the bye grid, read before any drop is spent
        _hedge_name = next((_pp.get('name') for _cc, _pp in _cheap
                            if (_grid.get(id(_pp), 1.0) or 0.0) <= 0.05 and _may_drop(_pp.get('pos'))), '')
        # [doc 436] AN OPEN SEAT IS THE CHEAPEST DROP THERE IS, AND THE LADDER NEVER SAW ONE.
        # drop_costs() lists "the open spot" and _rows_acc skips it, so with fourteen of fifteen
        # held this table still charged every add a real man. The first adds take the open seats.
        _open = max(0, 15 - seats_used) if seats_used is not None else 0
        for _m in _picked:
            _c, _pl = None, None
            if _open > 0:
                _open -= 1
                _c, _pl = 0.0, {'name': 'nobody: this fills your open seat', 'pos': '', 'tm': ''}
            for _j, (_cc, _pp) in enumerate(_cheap if _pl is None else ()):
                if _j in _used:
                    continue
                if _pp.get('pos') == _m.get('pos') and (_grid.get(id(_pp), 1.0) or 0.0) > 0.05:
                    continue
                if not _may_drop(_pp.get('pos')):
                    continue
                _c, _pl = _cc, _pp
                _used.add(_j)
                _left[_pp.get('pos')] -= 1
                break
            # A NEGATIVE DROP COST MUST NOT BE ADDED TO THE NET. It is real -- drop_costs() is the
            # season WITH him minus the season WITHOUT him, and it goes below zero when the best
            # free body at his position already outscores him. But `worth` ALREADY assumes the best
            # free body takes the seat, so crediting the negative a second time counts one upgrade
            # twice: the first live render showed "+13.1 minus -1.6 = +14.7" off ONE roster spot.
            # Replacing a man who is below replacement is its own decision and gets its own row.
            _cost = _c if _c is not None else 0.0
            _net = _m['worth'] - max(0.0, _cost)
            _when = ('this week' if not _m.get('when') or (week and _m['when'] <= week)
                     else f"week {_m['when']}")
            _hurt = news_note(_pl, _news_id, _news_key) if _pl else ''
            _dropcell = ('&mdash;' if _pl is None else
                         f'{E(_pl["name"])}<span class="meta">{E(_pl.get("pos", ""))}'
                         + (f' &middot; <b class="hurt">{E(_hurt)}</b>' if _hurt else '')
                         + '</span>')
            # [doc 424] A ROW THAT LOSES POINTS IS NOT A RECOMMENDATION. The Jets row printed
            # "+1.5 worth, 5.8 to drop, net -4.3" under the heading WHAT TO DO. The caption has
            # always said to read down until the net stops being positive, which puts the work on
            # the reader and assumes he is reading a list rather than being told. He was right to
            # call it: "that doesn't compute". The table stops at the last row that GAINS, and
            # says how many were held back rather than silently truncating (0.5(c)5).
            if _net <= 0.05:
                _skipped += 1
                continue
            # [doc 439] The total counts only the rows printed. It used to add every row before
            # the skip, so on 29 Sept it read "Taking all 3 nets +12.1" over two rows worth +12.6.
            if _when == 'this week':                  # doc 457: a calendar row is not in tonight's total
                _run += _net
                _shown_n += 1
            else:
                _later_n += 1
            _own = (f'{_m["owned"]:.0f}% rostered' if _m.get('owned') is not None else '')
            _wf_rows.append({'name': _m['name'], 'pos': _m.get('pos', ''), 'tm': _m.get('tm', ''),
                             'claim': 'CLAIM' in ((_m.get('row') or {}).get('flags') or ''),
                             'drop': (_pl or {}).get('name', ''), 'worth': _m['worth'], 'net': _net,
                             'contested': _contest_share(_m), 'when': _when,
                             'clears': ((_m.get('row') or {}).get('clears') or ''),        # ESPN's own clear time
                             'drop_pos': (_pl or {}).get('pos', ''), 'drop_tm': (_pl or {}).get('tm', '')})
            # [doc 443] THE TAKE CONTRACT, ON THE ROW. 0.1(h)'s vintage, man ahead and held input
            # print under the name; check_pages.py C6 reads them off the first row. The meta span
            # keeps its shape (position first) because that is what C6 parses the position from.
            _facts = take_facts(_m, seat_all, week)
            if not season_priced(_m.get('pos')) and _m.get('empty'):
                _facts = (f'fills the {NOUN.get(_m.get("pos"), _m.get("pos"))} hole in {_wks(_m["empty"])}, priced on '
                          f'{"that week" if len(_m["empty"]) == 1 else "those weeks"} alone')
            _drows += (f'<tr><th scope="row">{E(_m["name"])}'
                       f'<span class="meta">{E(_m.get("pos", ""))} &middot; {E(_m.get("tm", ""))}'
                       f'{" &middot; " + _own if _own else ""}</span>'
                       f'<span class="meta">{_facts}</span></th>'
                       f'<td class="tot pos">+{_m["worth"]:.1f}</td>'
                       f'<td>{_dropcell}</td>'
                       f'<td class="tot">{_cost:.1f}'
                       + ('<span class="meta">below replacement</span>' if _cost < -0.05 else '')
                       + '</td>'
                       f'<td class="tot{" pos" if _net > 0.05 else ""}">{_net:+.1f}</td>'
                       f'<td class="meta">{_when}</td></tr>')
        if _skipped:
            _drows += ('<tr><td colspan="6" class="meta">' + str(_skipped) + ' more '
                       + ('move loses' if _skipped == 1 else 'moves lose')
                       + ' points and ' + ('is' if _skipped == 1 else 'are') + ' left off.</td></tr>')
        _dec = _tbl(
            '<tr><th class="corner" scope="col">take</th>'
            '<th class="tot" scope="col">he is worth</th>'
            '<th scope="col">you would drop</th>'
            '<th class="tot" scope="col">that costs</th>'
            '<th class="tot" scope="col">net</th>'
            '<th scope="col">when</th></tr>', _drows,
            'Points to your starting nine over the weeks left. Each claim takes its own drop.')
        # [doc 416] THE HOLES ARE FOUR DATES AND NOW LOOK LIKE FOUR DATES. Doc 369 catalogued
        # this and it sat: "a calendar of holes buried in a paragraph of prose." It was one
        # run-on line in the standfirst, which is also the wrong PLACE -- a week with no body at
        # a position is a claim deadline, so it belongs beside the decision it drives, not in the
        # opening sentence about method.
        _hole_strip = ''
        if holes:
            _cells = ''.join(
                f'<span class="hole-chip"><b>week {w}</b>{E(lab)}</span>' for w, lab in holes)
            _hole_strip = (f'<p class="sub">Empty slots ahead:</p><div class="holes">{_cells}</div>')
        _dec = (f'<h3 class="sub0">The call</h3>{_dec}'
                + (f'<p class="sub">Taking '
                   + ('it' if _shown_n == 1 else ('both' if _shown_n == 2 else f'all {_shown_n}'))
                   + (' this week' if _later_n else '')
                   + f' nets <b>{_run:+.1f}</b>'
                   + (f'; the row marked for a later week is a calendar claim and is not counted.' if _later_n else '.')
                   + '</p>' if _shown_n else '')
                + waterfall_html(_wf_rows, wrank, const, _hedge_name, lane_leads=_ls_leads)
                + _hole_strip)

    band_moves = (f'{_dec}<div class="costbox">{cost_line}</div>'
                  f'<h3 class="sub0">Priority pickups, in order</h3>{picks}{call}'
                  + crowd_table(crowd, _picked if (now and _cheap) else [], _picks_shown if now else [],
                                _oj_under if now else [], _oj_cut, priced, _seat_cut, seats or [],
                                freerows, bar, roster))

    # ---- the calendar: claim in the week named, and expect the names to change ------------------
    # [doc 439] Matt, 29 Sept: "is this the only place to see my bye weeks? ... promote that
    # section further up so i'm not likely to forget about it." The calendar only listed the weeks
    # a position goes EMPTY; every bye week is printed with it now, and it sits under THE CALL.
    _byew = collections.defaultdict(list)
    for _p in roster:
        if _p.get('bye') and (not week or _p['bye'] >= week):
            _byew[_p['bye']].append(_p['name'])
    _bye_line = ('<p class="byes">' + ' &middot; '.join(
        f'<b>week {w}</b> {E(", ".join(_byew[w]))}' for w in sorted(_byew)) + '</p>'
        if _byew else '')
    cal = ''
    if later:
        crows = ''
        for m in later:
            claim = max(week or 1, m['when'] - 1)
            noun = NOUN.get(m['pos'], m['pos'])
            ow = f' &middot; {m["owned"]:.0f}%' if m.get('owned') is not None else ''
            crows += (f'<tr><th scope="row">week {claim}</th>'
                      f'<td class="l">no {noun} in week {m["when"]}</td>'
                      f'<td class="l"><b>{E(m["name"])}</b><span class="meta">{E(m["tm"])}{ow}'
                      f'</span></td><td>{m["worth"]:.1f}</td></tr>')
        cal = ('<h3 class="sub0" id="byes">Bye weeks &mdash; claim cover the week before</h3>'
               + _bye_line +
               '<p class="fine">Claim in the week on the left, not earlier. Names are today&rsquo;s '
               'best and will change.</p>'
               '<table class="cal"><tr><th scope="col">claim in</th><th scope="col" class="l">what '
               'for</th><th scope="col" class="l">best today</th><th scope="col">pts</th></tr>'
               + crows + '</table>')

    # ---- what he has ruled out, quoted and priced -------------------------------------------
    ruled_html = ''
    if ruled:
        items = ''
        for m in ruled[:3]:
            line, _note = dn[norm_name(m['name'])]
            alt = next((x for x in moves if x['pos'] == m['pos'] and x['sure'] == m['sure']), None)
            cost = ''
            if alt:
                d = m['worth'] - alt['worth']
                cost = (f' {E(alt["name"])} is the next man at {E(m["pos"])} and the gap is '
                        + (f'{d:.1f} points.' if d > 0.05 else 'nothing.'))
            items += (f'<li><b>{E(m["name"])}</b> ({E(m["pos"])}) would price at '
                      f'<b>{m["worth"]:.1f}</b> and is off the list on your instruction.{cost}</li>')
        ruled_html = f'<div class="ruled"><h4>ruled out on your say-so</h4><ul>{items}</ul></div>'

    # ---- what changed, and who to watch: statuses first, then the calendar ------------------
    watch = []
    if standing:
        watch.append(standing)                 # doc 456: the record and the points, first
    # [30 Sept, doc 456] A PARKED MAN DUE BACK NEEDS AN ACTIVE SEAT. Nacua sat in the IR slot as
    # questionable with a return date of Sunday and no page said that starting him costs a drop:
    # the slot keeps him (section 2), but the lineup cannot take him from it without a seat. Matt
    # carried it in his head; the page carries it now, with the man the drop ladder would cut.
    _cheap_now = list(_cheap)[:1]           # the ladder is built above THE CALL, so it exists here
    for pl in roster:
        st = (pl.get('status') or '').upper()
        if _is_parked(pl) and st in ('QUESTIONABLE', 'DOUBTFUL'):
            _nn = news_note(pl, _news_id, _news_key) if isinstance(news_lookup, tuple) else ''
            _cut = (f"the drop ladder's cheapest is <b>{E(_cheap_now[0][1].get('name') or '?')}</b> at {max(0.0, _cheap_now[0][0]):.1f}"
                    if _cheap_now else 'see the drop ladder for the cheapest man')
            watch.append(f'<b>{E(pl["name"])}</b> ({E(pl["pos"])}) is parked and <b class="warn">'
                         f'{E(_nn) if _nn else E(st.title())}</b>. He keeps the seat, but to START '
                         f'him you must move him to an active seat first, which costs a drop that no claim '
                         f'makes for you; {_cut}. Do it before his kickoff.')
    for pl in sorted(roster, key=lambda x: -x.get('wk', 0)):
        st = (pl.get('status') or '').upper()
        if st and st != 'ACTIVE':
            watch.append(f'<b>{E(pl["name"])}</b> ({E(pl["pos"])}) is '
                         f'<b class="warn">{E(st.replace("_", " ").title())}</b> &mdash; your own man')
    for pl in (unpriced or []):
        watch.append(f'<b>{E(pl)}</b> carries no ESPN projection at all, which is what an injury '
                     f'designation looks like, and every number here is computed without him')
    seen_w = set()
    for m in moves[:6]:
        st = (m.get('status') or '').upper()
        if st and st != 'ACTIVE' and m['name'] not in seen_w:
            seen_w.add(m['name'])
            watch.append(f'<b>{E(m["name"])}</b> on the list above is '
                         f'<b class="warn">{E(st.replace("_", " ").title())}</b>')
    if holes and not later:
        watch.append('empty slots ahead: <b>' + hole_txt + '</b>')
    nextbye = sorted({p['bye'] for p in roster if week and p.get('bye') and p['bye'] >= week})
    if nextbye and not later:
        who = ', '.join(E(p['name']) for p in roster if p.get('bye') == nextbye[0])
        watch.append(f'next bye is <b>week {nextbye[0]}</b>: {who}')
    shortnow = const.get('rival_shortages', {}).get(str(week or 1), {})
    shortnow = {k: v for k, v in shortnow.items() if v}
    if shortnow:
        watch.append('rivals short this week: ' + ', '.join(f'{k} {v}' for k, v in shortnow.items())
                     + ' &mdash; a run starts at three')
    watch_html = ('<ul class="watch">' + ''.join(f'<li>{w}</li>' for w in watch[:8]) + '</ul>'
                  if watch else '')

    # MATT, 2026-09-17: "the to do list is buried for me." It was, three ways at once: this box
    # sat at the BOTTOM of section 0, it showed six items, and its own CSS clipped every line at
    # the box width. The list is now a page of its own, linked from the masthead where he drew the
    # arrow; this box keeps the first few and SAYS how many it is not showing, which is the one
    # thing the old one could not do.
    todo_link = ''
    if todo_n:
        # Matt, 18 Sept: the kicker line and the to-do link ran together on one line. The link
        # is its own block directly under the kicker now, which is where he reads for it.
        todo_link = page_bar(
            current='WEEK_SHEET.html',
            labels={TODO_PAGE: f'to-do list &mdash; {int(todo_n)} open'})
    todo_html = ''
    if todo:
        rest = max(0, int(todo_n or 0) - len(todo))
        more = (f'<p class="more">and <strong>{rest}</strong> more &mdash; '
                f'<a class="todolink" href="{TODO_PAGE}">open the full list</a></p>'
                if rest else
                f'<p class="more"><a class="todolink" href="{TODO_PAGE}">'
                f'open the full list</a></p>')
        todo_html = ('<div class="todo"><h4>yours this week'
                     + (f' &mdash; {int(todo_n)} open' if todo_n else '') + '</h4><ul>'
                     + ''.join(f'<li>{E(t)}</li>' for t in todo) + '</ul>' + more + '</div>')

    band = (f'<section class="band"><h2 class="bh" id="s0"><span class="n">0</span>'
            f'{"Week " + str(week) + " &mdash; what to do" if week else "What to do"}</h2>'

            # [doc 411] vintage_html sat FIRST here and Matt moved it: "why is this at the top?"
            # Doc 369 set the objective for this page and it is what to DO, what changed, and
            # what it costs. A table of where the page's own rates are stale is the METHOD, not
            # the answer, and doc 369 says so in those words. It now sits with the workings,
            # below the calendar and the watch list. The live warning still reaches him where
            # it binds: the drop-cost line carries it inline (doc 410).
            f'{band_moves}{cal or _bye_line}{lookahead_html(week, roster, freerows)}'
            f'{watch_html}{ruled_html}{todo_html}</section>')

    # A worked example beats a formula. Matt, 2026-09-12: "I need an example of this formula in use
    # and the heading above those values to actually understand it." Built from a real row on this
    # page so it can never describe an arithmetic the page is not doing.
    worked = ('Every number on this page is the same sum, so here it is on one man.')
    # Prefer a week where the bar is NOT zero, so the subtraction is worth showing, and never use
    # a man he has ruled out as the teaching example.
    _ex = None
    for _want_bar in (True, False):
        for _p in POS:
            for _c in sorted((r for r in freerows if r['pos'] == _p), key=lambda r: -r['wk'])[:4]:
                if norm_name(_c['name']) in dn:
                    continue
                _wk, _tot = price(_c, bar)
                _hit = [w for w in WEEKS
                        if (_wk[w] or 0) > 0.049 and (bar[_c['pos']][w] > 0.05 or not _want_bar)]
                if _hit:
                    _ex = (_c, _wk, _tot, _hit)
                    break
            if _ex:
                break
        if _ex:
            break
    if _ex:
        _c, _wk, _tot, _hit = _ex
        _w = _hit[0]
        _zero = (' &mdash; zero because that slot is empty, which is the whole reason an ordinary '
                 'player prices so high there' if bar[_c['pos']][_w] <= 0.05 else '')
        worked = (f'<b>{E(_c["name"])}</b> scores <b>{_c["wk"]:.1f}</b> a week. In week {_w} your '
                  f'{E(NOUN.get(_c["pos"], _c["pos"]))} bar is <b>{bar[_c["pos"]][_w]:.1f}</b>{_zero}'
                  f', so he '
                  f'adds <b>{_c["wk"]:.1f} &minus; {bar[_c["pos"]][_w]:.1f} = '
                  f'{_wk[_w]:.1f}</b> that week. In a week where the bar is above his rate he adds '
                  f'nothing, and a bye week counts as nothing too. Add up the weeks where the answer '
                  f'is positive and you get <b>{_tot:.1f}</b>, which is the number beside his name '
                  f'in section 2. That is the whole arithmetic, at every position, all the way down '
                  f'the page.')

    # [doc 435] THE MEASURED RATE SITS BESIDE THE BLEND, WITH ITS GAMES. At week 3 the blend is
    # 36% this season and 64% preseason, so it had Pickens 9.4 and Tucker 9.3, 0.1 apart, while
    # the season said 5.7 and 12.0. For a start/sit the blend is the wrong instrument; the blend
    # stays (it is the forecast) and the season is printed next to it. Blank when there is no form
    # row, never zero. Nothing here sorts on it.
    rr = ''
    for pl in sorted(roster, key=lambda x: (POS.index(x['pos']) if x['pos'] in POS else 9, -x['wk'])):
        _ts, _l2 = this_season_text(pl), last_two_text(pl)
        _mu = matchup_text(pl, matchup)           # doc 468: RB and TE, printed, never sorted on
        rr += (f'<tr><th scope="row"><span class="pl" title="{E(pl["name"])}">{E(pl["name"])}</span>'
               f'<span class="meta">{E(pl["pos"])} &middot; {E(pl["tm"])}'
               + (f' &middot; {_l2}' if _l2 else '') + '</span></th>'
               f'<td>{pl["wk"]:.1f}'
               + (f' blend <span class="meta">&middot; {_ts}</span>' if _ts else '')
               + (f' <span class="meta">&middot; {_mu}</span>' if _mu else '')
               + f'</td><td>{pl["bye"]}</td></tr>')

    comp = const.get('rival_shortages', {})
    crows = ''
    for p in ('QB', 'TE', 'K', 'D/ST'):
        cells = ''
        for w in WEEKS:
            n = comp.get(str(w), {}).get(p, 0)
            cells += ('<td class="zero">&mdash;</td>' if not n else
                      f'<td class="{"hole" if n >= 3 else ""}">{n}</td>')
        crows += f'<tr><th scope="row">{p}</th>{cells}</tr>'

    warn = f'<div class="box bad"><h4>read this first</h4><p>{E(note)}</p></div>' if note else ''
    rules = ''.join(f'<div class="box"><h4>{E(r["h"])}</h4><p>{r["p"]}</p></div>'
                    for r in const.get('rules', []))

    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Week Sheet &mdash; {stamp}</title><style>{CSS}</style></head><body id="top">
<div class="wrap">
<header><p class="kick">{E(team_name or 'Your team')} &middot; built {stamp}</p>
<h1>Where the Season Breaks</h1>
<p class="dek">What to claim, what it costs you, and when. Your remaining weeks total
<strong>{base:,.0f}</strong> points as the lineup stands.</p>
{todo_link}</header>
<nav class="secnav" aria-label="sections of this page">
<a href="#s0"><span class="n">0</span>what to do</a>
<a href="#byes">byes</a>
<a href="#s3"><span class="n">1</span>the bet</a>
<a href="#seats">seat list</a>
<a href="#tickets">long shots</a>
<a href="#s1"><span class="n">2</span>free bodies</a>
<a href="#drops">drop costs</a>
<a href="#s2"><span class="n">3</span>the bar</a>
<a href="#cards">the cards</a>
<a href="#s4"><span class="n">4</span>who else is short</a>
<a href="#s5"><span class="n">5</span>your roster</a>
<a href="#s6"><span class="n">6</span>rules</a>
<a class="top" href="#top">top &uarr;</a>
</nav>
{inputs}
{band}
{warn}
<h2 id="s3"><span class="n">1</span>The bet</h2>
<p class="lede">A screened young receiver hits about as often in any week, so the only thing that
moves is what the spot costs.</p>
{bet_tbl}
{miss}
<p class="sub"><em>If it fires</em> = <strong>{HP:.1f}</strong> a game for <strong>{HW:.1f}</strong>
weeks. <em>Expected</em> = that &times; odds. Take a ticket when expected beats your cheapest drop.</p>
{seatbox}
{_tbl('<tr><th class="corner" scope="col">the cheapest thing you own</th><th scope="col">what dropping him costs</th></tr>', crow2)}
{verdict}
{seat_html}
{vintage_html}
<h2 id="s1"><span class="n">2</span>Every free body, priced</h2>
<p class="lede">Green = a week he would start for you.</p>
{cand_html}

<h3 class="sub0" id="drops">And what each of your own men costs to drop</h3>
{drop_tbl}

<h2 id="s2"><span class="n">3</span>The bar</h2>
<p class="lede">What a pickup must beat to start for you that week. <b>empty</b> = nobody there.</p>
{_tbl(hdr, brows)}

<h3 id="cards">The cards &mdash; what the arithmetic cannot see</h3>
{card_html}

<h2 id="s4"><span class="n">4</span>Who else is short, by week</h2>
<p class="sub">From the drafted rosters, so it can overstate. Three or more is a run.</p>
{_tbl(hdr.replace('position', 'rivals short'), crows)}

<h2 id="s5"><span class="n">5</span>Your roster</h2>
{_tbl('<tr><th class="corner" scope="col">player</th><th scope="col">pts/wk</th>'
      '<th scope="col">bye</th></tr>', rr)}

<h2 id="s6"><span class="n">6</span>The standing rules</h2>
{rules}
<footer>{sched}<br>Built by {E(code_stamp(__file__))}.</footer>
</div></body></html>"""


def write(path, roster, freerows, const, note='', unpriced=None, seats_used=None, week=0,
          team_name='', open_jobs=None, crowd=None):
    if not roster:
        raise ValueError('sheet_engine: empty roster -- refusing to write a sheet with no bar')
    set_horizon(week)                    # doc 407: price the weeks still ahead, never the played ones
    src = os.path.dirname(os.path.abspath(path))
    seats, seatnote = load_seats(src)
    cards, _cw = load_cards(src)
    screened, _sw = load_screened(src)
    for _w in (_cw, _sw):                      # the console hears what the page leaves to ESPN
        if _w:
            print('  week sheet: ' + _w)
    # The to-do page is built FIRST, so the link in the masthead can never point at a page that
    # was not written. A failure here is reported and the sheet still writes -- his list is not
    # allowed to take the week sheet down -- but the link is then withheld rather than dangling.
    todo_open = 0
    try:
        _tp, todo_open = write_todo_page(src, team_name=team_name)
        if _tp:
            print(f'  written: {_tp}  ({todo_open} open items)')
    except Exception as exc:
        print(f'  {TODO_PAGE} NOT written -- {type(exc).__name__}: {exc}')
        todo_open = 0
    built = dt.datetime.now()                 # one clock for the stamp and the inputs box
    _odds = playoff_odds(src)                 # doc 469: the standings line and the lane read it
    page = render(roster, freerows, const, note=note, seats=seats, seatnote=seatnote,
                  cards=cards, screened=screened, unpriced=unpriced,
                  seats_used=seats_used, seat_all=load_seat_rows(src), week=week,
                  ir_view=ir_picture(src), open_jobs=open_jobs, crowd=crowd,
                  standing=load_standings(src, _odds), leaders=pos_leaders(src), rb_use=rb_usage(src),
                  wr_use=wr_usage(src), pf=pf_rank(src), wrank=waiver_rank(src), playoff=_odds,
                  matchup=matchup_terms(src, week),
                  vintage_html=vintage_block(roster, freerows, src),
                  season_rates=season_ppg(src), news_lookup=load_news(src),
                  tgt_load=target_load(src),
                  todo=load_todo(src), donot=load_donot(src), team_name=team_name,
                  pedigree=load_pedigree(src),
                  todo_n=todo_open,
                  stamp=build_meta(built)['text'],
                  inputs=inputs_block(src, built, teams=[r.get('tm') for r in roster],
                                      week=week, blended=_blend_count(roster, freerows)))
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        fh.write(page)
    try:
        os.replace(tmp, path)                 # never leave a half-written sheet on the desk
    except OSError:
        # Google Drive for desktop can hold a brief lock on a file it is uploading, and a rename
        # onto a locked file fails on Windows. Write in place rather than lose the rebuild.
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(page)
        try:
            os.remove(tmp)
        except OSError:
            pass
    return path


# [doc 417] MEASURED. Share of the rest-of-season forecast that should come from THIS season's
# games, by the week you are standing in.
#   population  nflverse 2021-2025, season_type REG, RB/WR/TE, half-PPR; every player-season with
#               a prior season and at least one game each side of the week. n = 846 to 1,254.
#   outcome     ppg over weeks W..14 -- this league's regular season ends at 14 (section 2)
#   fit         rest-of-season ppg ~ (ppg so far) + (prior-season ppg), OLS; the weight is the
#               normalised coefficient on `ppg so far`
#   result      the blend beats the better single signal at EVERY week, by 1% to 15% RMSE.
#               Crossover -- the week this season is worth more than the prior -- is week 5.
#   stability   re-fitted under 18 population definitions (min games each side 1/2/3, outcome
#               window ending 14 or 17): every week moves by at most 0.07, and the ordering,
#               the shape and the crossover are identical in all 18.
# REPRODUCE IT: py research\blend_weight.py --check  -- it re-fits from the nflverse cache and
# exits 1 if this table has drifted from the measurement.
#
# THE FIRST VERSION OF THIS TABLE WAS RETRACTED BEFORE IT EVER RENDERED A PAGE. It ran
# {2: 0.36, 3: 0.44, 4: 0.49, 5: 0.53, 6: 0.57, 7: 0.64, 8: 0.67, 9: 0.73, 10: 0.74, 11: 0.79,
# 12: 0.80, 13: 0.79, 14: 0.79} and was fitted inline, from a population that was never written
# down. Nothing on the drive reproduced it: 18 definitions were tried, none returned its numbers
# or even its sample sizes, and its week-2 value sat 0.13 outside the band every one of them
# agreed on. That is doc 399's failure exactly -- a curve with no reproducible population -- and
# it is why `blend_weight.py` exists rather than a comment claiming a number.
#
# CAVEAT, and it bounds the number rather than decorating it: the PRIOR in that fit is last
# season's ppg, not ESPN's in-season projection. ESPN's is the better prior, so the weight here
# is an UPPER bound on how far to trust N games. Not shaded down -- shading it would be the
# guess this measurement exists to avoid (0.2).
BLEND_W = {2: 0.23, 3: 0.36, 4: 0.43, 5: 0.51, 6: 0.54, 7: 0.61,
           8: 0.64, 9: 0.69, 10: 0.72, 11: 0.77, 12: 0.78, 13: 0.77, 14: 0.79}


def rates(src, week=0):
    """espn_id -> {name,pos,tm,bye,wk} for EVERY player in the newest projection pull.

    Deliberately not the board: the board carries no kicker and no defense rows by design, and a bar
    grid missing two of the nine slots would silently price them at zero. The pull's proj_2026 is
    the same league-scored quantity as the board's (verified r=0.9925), so one source serves all
    nine slots. Returns ({}, why) rather than a half-filled dict when an input is missing.
    """
    import csv as _csv
    import glob as _glob
    pulls = sorted(_glob.glob(os.path.join(src, 'espn_projections_2026_*.csv')))
    if not pulls:
        return {}, 'no espn_projections_2026_*.csv in Source'
    byes_p = os.path.join(src, 'byes_2026.csv')
    if not os.path.exists(byes_p):
        return {}, 'no byes_2026.csv in Source'
    with open(byes_p, newline='', encoding='utf-8-sig') as fh:
        byes = {team_key(r['team']): int(r['bye']) for r in _csv.DictReader(fh)}
    # THE JOIN IS CHECKED, NOT TRUSTED (doc 291). Every one of the 32 must have a bye, and every
    # team code in the pull must resolve to one of them. A miss refuses the sheet and names the code.
    if set(byes) != ESPN_TEAMS:
        return {}, ('byes_2026.csv does not resolve to the 32 teams: missing %s, unknown %s'
                    % (sorted(ESPN_TEAMS - set(byes)), sorted(set(byes) - ESPN_TEAMS)))
    # [doc 417] A FEATURE THAT COMPUTES AND REACHES NOTHING IS doc 146's TRAP IN A NEW SHAPE.
    # The blend below is keyed on `week`, and `wire.py` called rates(SRC) with no week for its
    # whole first life, so every function-level test passed and the page kept printing preseason
    # rates. A silently-degraded number is the same class as a step that returns 0 while doing
    # nothing: SAY SO rather than quietly fall back.
    _season = season_ppg(src) if week else {}
    # [doc 426] SECTION 3's IDENTITY RULE, APPLIED TO THE ONE JOIN THAT SKIPPED IT. form_2026
    # spells him 'Kyle Pitts' and the projection pull spells him 'Kyle Pitts Sr.', so the raw
    # dict lookup below missed and he fell back to a PRESEASON projection with no error and a
    # vintage of 'proj' that looked deliberate. Nine men, all suffix or apostrophe: Pitts
    # printed 7.89 against a correct 5.41 and was the page's top cover for the week-6 TE bye.
    # norm_name has existed for exactly this since doc 58 and this call site never used it.
    # [doc 442] AND THE KEY IS NAME + POSITION + TEAM, NEVER LESS (section 3). The name-only
    # lookup this replaced could pair two men who share a spelling, and it could not reach
    # "Joshua Palmer" (ESPN) from "Josh Palmer" (nflverse). form_lookup() takes the two steps
    # wire.py takes: the exact key, then the one-candidate first-name variant on the same team
    # and position. One rule for the engine and the wire.
    _season_k = season_ppg_keyed(src) if _season else {}
    _left = proj_games(week)          # doc 419: proj_2026 is a REST-OF-SEASON total
    if week and _left < PROJ_GAMES:
        print(f'  rates(): week {week} -- ESPN\'s projection is rest-of-season, so it is spread '
              f'over the {_left:.0f} games left, not 17.')
    if not week:
        print('  rates(): no week given -- rates are PRESEASON projections, the measured blend '
              'is OFF. Pass the week from wire.py.')
    elif not _season:
        print(f'  rates(): week {week} but form_2026.csv gave no measured rates -- '
              f'blend OFF, projections only. Run  py research\\wk1\\build_form.py')
    out, no_team, bad = {}, [], collections.Counter()
    with open(pulls[-1], newline='', encoding='utf-8-sig') as fh:
        rdr = _csv.DictReader(fh)
        namecol = [c for c in (rdr.fieldnames or []) if c.lower().strip() == 'player']
        if not namecol:
            return {}, 'the projection pull has no player-name column'
        namecol = namecol[0]
        for r in rdr:
            pid = str(r.get('espn_id', '')).strip()
            try:
                pr = float(r.get('proj_2026') or 0)
            except ValueError:
                pr = 0.0
            tm = team_key(r.get('team'))
            if not pid or pr <= 0:
                continue
            if tm in NO_TEAM:
                no_team.append(r[namecol])          # no NFL team, no games: counted, not priced
                continue
            if tm not in byes:
                bad[tm] += 1
                continue
            # [doc 409] THE RATE IS FORWARD LOOKING WHEN THIS SEASON IS ON FILE.
            # `pr` is ESPN's REST-OF-SEASON forecast (doc 419 -- it was called FULL-SEASON here
            # until 24 Sept and that is the sentence the /17 divisor rested on). `actual_2026` is
            # what the man has already banked, and it is NOT inside `pr`. Weeks remaining is a
            # CALENDAR fact, not a player fact, so no games-played divisor is needed
            # -- which matters, because the only candidate for one (stat id 210 in raw_actual_stats)
            # agreed with independently counted games on just 313 of 375 players, 83.5%, and a
            # divisor wrong by 2x on one player in six is worse than no divisor at all (0.2).
            # With no week this is exactly the old pr / PROJ_GAMES (doc 419: 17 preseason).
            # [doc 417] THE RATE IS A MEASURED BLEND NOW, AND THE WEIGHT IS NOT A GUESS.
            # Every number on THE CALL was computed from a PRESEASON rate: Schultz showed +13.1
            # off 6.06 a week while measuring 12.8. The blend was deferred twice because I would
            # not invent a weight. BLEND_W above carries the weight, the population, the sample
            # sizes and the caveat; research\blend_weight.py --check re-fits it and fails on
            # drift. Do not restate its numbers here -- one copy, and it is the one beside the
            # table (9 rule 7).
            # RB/WR/TE only -- form_2026.csv does not score passing or kicking (doc 375), so QB,
            # K and D/ST stay on the projection and say so in `vintage`.
            # ~~(proj - actual) / weeks remaining~~ TRIED AND KILLED BY ITS OWN TEST, doc 409.
            # It is arithmetically "what ESPN expects from here" and it is ANTI-CORRELATED with the
            # thing this fix exists for. Subtracting banked points from a sticky season total
            # PENALISES the man who has already produced and REWARDS the man who has not:
            #   Schultz  measured 12.8/g -> forward rate FELL 6.38 to 5.53
            #   Tucker   measured 12.1/g -> FELL 6.78 to 6.08
            #   Dobbins  measured  3.6/g -> ROSE 9.37 to 10.14
            #   Dowdle   measured  4.2/g -> ROSE 7.60 to  8.05
            # Every one of the four moved away from the season. DO NOT REBUILD IT -- but the
            # REASON recorded here was wrong, and the wrong reason is what hid doc 419's bug for
            # three weeks. It said "ESPN's proj_2026 barely moves, so the subtraction is just mean
            # reversion wearing a forecast's clothes". It moves for 99.1% of backs and receivers
            # between two pulls seventeen days apart, by a median of -6.7 points, because it is a
            # REST-OF-SEASON total burning off elapsed games (doc 419). So proj - actual was
            # DOUBLE-SUBTRACTING: ESPN had already taken those games out, and taking the man's
            # banked points out again is why it punished whoever had produced. The result stands;
            # the explanation is replaced. A conclusion that is right for the wrong reason leaves
            # the wrong reason in the file, and the next thing built on it inherits the error --
            # here, a divisor of 17 that nobody questioned because the total looked sticky.
            _act = _f(r.get('actual_2026'))
            _proj_wk = pr / _left          # doc 419: games LEFT, not 17. See proj_games().
            _rate, _vintage = _proj_wk, 'proj'
            _meas = (form_lookup(_season_k, r[namecol], r.get('pos'), tm)
                     if _season_k else None)
            if _meas and week:
                _w = BLEND_W.get(int(week), BLEND_W[max(BLEND_W)])
                _rate = _w * _meas[0] + (1.0 - _w) * _proj_wk
                _vintage = f'{_w*100:.0f}% of {_meas[1]} game{"s" if _meas[1] != 1 else ""}'
            out[pid] = {'name': r[namecol], 'pos': (r.get('pos') or '').strip(),
                        'tm': tm, 'bye': byes[tm], 'wk': _rate, 'espn_id': pid,
                        # carried so the PAGE can print both and he can fact-check it live,
                        # which is the whole ask: "if I know something is off I know something
                        # wasn't updated."
                        'proj_wk': _proj_wk, 'actual_2026': _act, 'vintage': _vintage,
                        'measured': (_meas[0] if _meas else None),
                        # doc 435's decision: the measured rate is printed BESIDE the blend, with
                        # the games it rests on. For a start/sit the blend is the wrong instrument.
                        'measured_g': (_meas[1] if _meas else None),
                        # doc 438: the last two games, actual and expected, off the form row, so a
                        # roster row can print them too (wire.py sets them on free rows only).
                        'act2': (_meas[3] if _meas else ''), 'xfp2': (_meas[4] if _meas else '')}
    rates.no_team = no_team
    if bad:
        return {}, ('the projection pull carries team codes that resolve to no team: '
                    + ', '.join(f'{k} ({v} players)' for k, v in sorted(bad.items())))
    if len(out) < 300:
        return {}, f'only {len(out)} priced players read from {os.path.basename(pulls[-1])}'
    return out, ''


def load_constants(src):
    p = os.path.join(src, 'sheet_constants.json')
    if not os.path.exists(p):
        return {}, f'no {os.path.basename(p)} -- sections 3 and 5 are missing, not empty'
    with open(p, encoding='utf-8') as fh:
        return json.load(fh), ''
