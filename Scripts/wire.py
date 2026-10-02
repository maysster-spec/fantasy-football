#!/usr/bin/env python3
r"""
wire.py -- WHO IS ACTUALLY AVAILABLE, PRICED ON OUR OWN BOARD.

    py wire.py                 # the weekly claim sheet, on screen
    py wire.py --html          # ALSO write the sheet Windows Task Scheduler leaves for you
    py wire.py --all           # every free agent we can price, not just the top of each position
    py wire.py --check         # just prove the cookies still work, pull nothing

WHY THIS EXISTS
    ESPN orders the free-agent list by PERCENT OWNED, which is the market's opinion, not ours.
    This pulls the real pool and re-sorts it on the board's own value, then hangs the job flag,
    the job's worth, the back signals and the news grade off each row.

WHY IT IS NOT waivers.py
    `waivers.py` already exists and pulls HISTORICAL transactions into waiver_report_<year>.csv.
    Different job, different output.  One name, one job.

WHAT IT WRITES
    Source\WIRE_<date>.csv        -- every priceable free agent, ranked
    Source\FREE_UNRANKED_<date>.csv -- every free skill player the board never rated (doc 292)
    Source\THE_WEEKLY_WIRE.html   -- the sheet you read (with --html)
    and prints the short claim sheet to the console.

RUN BY THE SCHEDULER, NOT BY YOU
    `weekly.bat` runs this every Tuesday morning. If it cannot do its job the PAGE says so in
    red -- it never leaves yesterday's sheet sitting there looking current.

IF IT 401s: your cookies expired.  Run `py set_cookies.py` and try again.
"""
import argparse, collections, csv, datetime as dt, json, os, sys

try:
    import requests
except ImportError:
    sys.exit("wire.py needs `requests`.  It is already used by live_draft.py, so if this fires "
             "you are running a different Python than the one the draft kit uses.")

LEAGUE_ID  = 21985
SEASON     = 2026
MY_TEAM_ID = 9                     # JUG
READS = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leagues/{lid}"
COOKIES = {
    'swid':    '{A7217088-1F36-4F1F-AE73-67262BF763EF}',
    'espn_s2': '',
}
HEADERS = {'accept': 'application/json', 'x-fantasy-platform': 'espn-fantasy-web',
           'x-fantasy-source': 'kona', 'referer': 'https://fantasy.espn.com/'}

HERE = os.path.dirname(os.path.abspath(__file__))
LIVE = os.path.join(HERE, 'live_draft')
SRC  = os.path.normpath(os.path.join(HERE, '..', 'Source'))
BOARD   = os.path.join(LIVE, 'board_v8_fixed.csv')
CONTEXT = os.path.join(LIVE, 'player_context.csv')
# SECTION 4.28 / 4.30 -- the draft-capital column and the receiver screen. Matt, 2026-09-09:
# "we are not just looking at current market value, but POTENTIAL value as well."
# Built by Scripts\research\build_pedigree.py.
PEDIGREE = os.path.join(SRC, 'pedigree_2026.csv')
# SECTION 4.31 / doc 308 -- the IN-SEASON workload. Every other input on this page is frozen
# before week 1, so the three names in the sheet's Priority pickups could not change from one
# week to the next. 4.31 measures a week-2 claim at 34.6% against week 1's 9.4% precisely
# BECAUSE a week-2 claim bets on a snap count, and the page had no snap count.
# Built by Scripts\research\wk1\build_form.py.
FORM = os.path.join(SRC, 'form_2026.csv')

POS = {1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 16: 'D/ST'}
SHOW_PER_POS = 8

# ONE TEAM-CODE MAP FOR BOTH PAGES, and it lives in sheet_engine.py (doc 291). This file used to
# carry its own copy and check it on ONE path -- the receiver-shape table -- while the schedule,
# last season's team scoring, the positions-allowed table and ESPN's pro-team ids each spelled
# Washington and the Rams their own way. Every loader below now resolves its codes through
# team_key() and reports any it cannot resolve, on the page, instead of silently losing the team.
try:
    from sheet_engine import (ESPN_TEAMS, TEAM_ALIAS, team_key, norm_name,
                              unknown_teams, code_stamp, page_bar, PAGEBAR_CSS,
                              GONE_FOR_WEEKS as _GONE_FOR_WEEKS)     # doc 443: one predicate
except ImportError as _exc:
    sys.exit("wire.py needs sheet_engine.py beside it -- the team-code map lives there "
             "(%s). Run  py check_kit.py  to see which file is missing." % _exc)
# doc 380: the read-time stamp and the on-open age line. Guarded separately so a sheet_engine.py
# that predates them costs the wire its stamp, never the page.
try:
    from sheet_engine import build_meta as _build_meta, age_line as _age_line
except ImportError:
    _build_meta = _age_line = None
LOAD_PROBLEMS = []          # every join that could not resolve, printed in red at the top of the page


def _check_codes(label, codes):
    bad = unknown_teams(codes)
    if bad:
        LOAD_PROBLEMS.append(f'{label} carries team codes that match no team: {", ".join(bad)}')
    return not bad


def write_standings(teams, out_path, my_team_id, asof=None):
    """[30 Sept, doc 456] Source\\standings_2026.csv off the mTeam read the wire already makes: one row a
    team with record, points for and against, playoff seed, ESPN's projected finish and the
    transaction counts. Matt, 30 Sept: "By my estimation my team hasn't been putting up enough points
    to be competitive season long." No file held his record or his points, so the estimate could not
    be checked; the week sheet reads this file and says where he stands. Every field is .get() with a
    blank when ESPN omits it, never a zero (section 3). Returns the rows written."""
    rows = []
    for t in (teams or []):
        rec = ((t.get('record') or {}).get('overall') or {})
        tc = t.get('transactionCounter') or {}
        nm = (t.get('abbrev') or t.get('name')
              or ' '.join(x for x in (t.get('location'), t.get('nickname')) if x) or '?')
        rows.append({'asof': asof or dt.date.today().isoformat(), 'team_id': t.get('id'),
                     'abbrev': str(nm).strip(), 'mine': 'yes' if t.get('id') == my_team_id else '',
                     'wins': rec.get('wins', ''), 'losses': rec.get('losses', ''), 'ties': rec.get('ties', ''),
                     'points_for': rec.get('pointsFor', ''), 'points_against': rec.get('pointsAgainst', ''),
                     'playoff_seed': t.get('playoffSeed', ''), 'projected_rank': t.get('currentProjectedRank', ''),
                     'waiver_rank': t.get('waiverRank', ''), 'acquisitions': tc.get('acquisitions', ''),
                     'drops': tc.get('drops', ''), 'trades': tc.get('trades', '')})
    rows.sort(key=lambda r: (float(r['playoff_seed']) if r['playoff_seed'] != '' else 99))
    with open(out_path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else
                           ['asof', 'team_id', 'abbrev', 'mine', 'wins', 'losses', 'ties', 'points_for',
                            'points_against', 'playoff_seed', 'projected_rank', 'waiver_rank',
                            'acquisitions', 'drops', 'trades'])
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return rows


def write_schedule(payload, out_path, abbrev_by_id, asof=None):
    """[1 Oct, doc 464] Source\\schedule_2026.csv off the mMatchupScore view: one row per matchup for the
    whole regular season, with the scores where the week has been played. Doc 463 named the league's
    remaining schedule as the one input the playoff-odds simulation was blocked on: his probability of
    a top-six finish over the weeks left, with and without a big hit, is the unit a ticket should be
    priced in (0.3). Every field is .get() with a blank when ESPN omits it (section 3). Returns the
    rows written; raises nothing itself, the caller reports."""
    rows = []
    for m in (payload or {}).get('schedule') or []:
        home, away = (m.get('home') or {}), (m.get('away') or {})
        if home.get('teamId') is None and away.get('teamId') is None:
            continue
        rows.append({'asof': asof or dt.date.today().isoformat(), 'week': m.get('matchupPeriodId', ''),
                     'matchup_id': m.get('id', ''), 'playoff': m.get('playoffTierType', ''),
                     'home_id': home.get('teamId', ''), 'home': abbrev_by_id.get(home.get('teamId'), ''),
                     'home_pts': home.get('totalPoints', ''),
                     'away_id': away.get('teamId', ''), 'away': abbrev_by_id.get(away.get('teamId'), ''),
                     'away_pts': away.get('totalPoints', ''), 'winner': m.get('winner', '')})
    rows.sort(key=lambda r: (float(r['week']) if r['week'] != '' else 99, str(r['matchup_id'])))
    fields = ['asof', 'week', 'matchup_id', 'playoff', 'home_id', 'home', 'home_pts', 'away_id', 'away',
              'away_pts', 'winner']
    with open(out_path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return rows


def _get(view, xfilter=None):
    h = dict(HEADERS)
    if xfilter:
        h['x-fantasy-filter'] = json.dumps(xfilter)
    url = READS.format(season=SEASON, lid=LEAGUE_ID) + '?view=' + view
    r = requests.get(url, cookies=COOKIES, headers=h, timeout=30)
    if r.status_code == 401:
        sys.exit("\n  401 from ESPN.  Your cookies have expired.\n"
                 "  Run  py set_cookies.py  and then run this again.\n")
    r.raise_for_status()
    return r.json()


_BYES = None


def load_byes():
    """NFL team -> bye week, from Source\\byes_2026.csv (doc 307).

    Needed because a player's bye on the wire comes from the FROZEN BOARD alongside his team, so
    when doc 307's team fix corrected seven rows they each kept the bye of the team they LEFT.
    All seven were wrong and all seven were exactly the old team's bye: Kaleb Johnson read week 9,
    which is Pittsburgh's, while Green Bay is on 11. That is worse than the job flag it sits next
    to, because section 4.32's first term is what a man adds over the weeks he is NEEDED, and the
    bye is the only fully deterministic part of that.

    Checked, not trusted (doc 291): a code that does not resolve to one of the 32 is NAMED on the
    page rather than silently dropped.
    """
    global _BYES
    if _BYES is not None:
        return _BYES
    _BYES = {}
    p_ = os.path.join(SRC, 'byes_2026.csv')
    if not os.path.exists(p_):
        LOAD_PROBLEMS.append('byes_2026.csv is missing, so a player who changed teams keeps his '
                             'old team bye')
        return _BYES
    try:
        with open(p_, newline='', encoding='utf-8-sig') as fh:
            _BYES = {team_key(r['team']): int(float(r['bye'])) for r in csv.DictReader(fh)}
    except (KeyError, ValueError, OSError) as exc:
        LOAD_PROBLEMS.append(f'byes_2026.csv could not be read ({type(exc).__name__}), so a '
                             f'player who changed teams keeps his old team bye')
        _BYES = {}
        return _BYES
    _check_codes('byes_2026.csv', list(_BYES))
    missing = sorted(ESPN_TEAMS - set(_BYES))
    if missing:
        LOAD_PROBLEMS.append('byes_2026.csv has no bye for ' + ', '.join(missing))
    return _BYES


def load_local():
    """The board's own value, plus everything player_context knows. Keyed on espn_id (SECTION 3)."""
    for p in (BOARD, CONTEXT):
        if not os.path.exists(p):
            sys.exit(f"\n  MISSING: {p}\n  wire.py must live in Scripts\\ beside live_draft\\.\n")
    board = {}
    with open(BOARD, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            try:
                r['_vor'] = float(r['vbd'])
            except (TypeError, ValueError):
                continue
            board[str(r['espn_id']).strip()] = r
    ctx = {}
    with open(CONTEXT, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            ctx[str(r['ESPN_ID']).strip()] = r
    return board, ctx


def flags(c, moved_to=''):
    """Plain-English marks only -- SECTION 0.1's scope rule. No doc numbers, no p-values.

    `moved_to` is the player's CURRENT NFL team when it differs from the board's. It exists
    because job and job_ceil are TEAM constants, not player properties: depth_map stamps one
    number on every man on the roster (doc 224 already asserted this for the stash lane). So a
    player who changed teams after the board froze carries the OTHER team's backfield number, and
    the row reads as authoritative. Kaleb Johnson shipped on WIRE_20260914.csv as
    "PIT, unsettled job, worth 174" after Pittsburgh traded him to Green Bay; 174 is Pittsburgh's.
    The grade and the player-level signals below are his own and survive the move. The job does not.
    """
    if not c:
        return f'moved to {moved_to} since the board' if moved_to else ''
    out = []
    if moved_to:
        out.append(f'moved to {moved_to} since the board')
    why = c.get('why', '') or ''
    g = (c.get('grade') or '').upper()
    if g in ('AVOID', 'DISCOUNT'):
        out.append(g.title())
    job = '' if moved_to else (c.get('job') or '')
    if job:
        # [30 Sept] job_ceil is the AUGUST board's number for the job (player_context.csv, a team
        # constant frozen before the draft), not this season's: on 30 Sept it printed "worth 261"
        # for Miami with Achane on injured reserve and projected at nothing, beside a week sheet
        # that priced the same job at 104. The take contract's first line (0.1h) says every number
        # carries its vintage; this one now does. The week sheet's THE CALL carries the live price.
        worth = c.get('job_ceil') or '?'
        out.append(f"{job.lower()} job, worth {worth} on the August board")
    i = why.find('RB SIGNALS: ')
    if i >= 0:
        n = why[i + 12:i + 15].strip()
        if n and n[0].isdigit():
            out.append(f"back signals {n[0]} of 3")
    i = why.find('TGT SHARE 2025: ')
    if i >= 0:
        seg = why[i + 16:i + 34]
        out.append('targets ' + seg.split('(')[0].strip())
    return ' · '.join(out)


def load_pedigree():
    """espn_id -> the potential screens. Returns ({}, why) when the file is absent, and the caller
    NAMES that rather than printing an empty lane (SECTION 0.2: a step that cannot do its job must
    say so; SECTION 0.5(c)5: a row that should be on the sheet and is not must be named)."""
    if not os.path.exists(PEDIGREE):
        return {}, ("no " + os.path.basename(PEDIGREE) + " -- run  py research\\build_pedigree.py")
    out = {}
    with open(PEDIGREE, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            if r.get('screen'):
                out[str(r['espn_id']).strip()] = r
    if not out:
        return {}, "the pedigree file holds no screened players"
    return out, ''


def load_pedigree_all():
    """espn_id -> the pedigree row for EVERY drafted man on the board, screened or not (doc 453). The
    in-season screen needs the round and the NFL year of a receiver the preseason screen could not
    read, which is every rookie: his yards per target and targets a game did not exist in August."""
    if not os.path.exists(PEDIGREE):
        return {}
    out = {}
    with open(PEDIGREE, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            out[str(r['espn_id']).strip()] = r
    return out





# THE WEEK-1 WORKLOAD SCREEN (doc 308). Three signals, each monotone on its own over 2022-2025:
#   8+ targets (6% at 1-3 -> 49% at 8+) - 80%+ of his team's offensive snaps (3% -> 39%) -
#   20%+ of his team's targets (4% -> 37%).
# Count of three, n=517 wire-eligible pass-catchers, base rate 13.9%:
#     0 of 3   6%      1 of 3  19%      2 of 3  38%      3 of 3  42%     permutation p=0.0002
# THE JUMP IS ONE SIGNAL TO TWO, NOT TWO TO THREE, so the operative bar is TWO. That is the
# OPPOSITE shape to 4.30's receiver composite (5.0 -> 7.1 -> 39.4, where only three counts) and
# 4.30's rule must not be ported across: those three signals are pedigree and career rate, three
# near-independent facts; these three are three views of one week's workload.
# POPULATION, restated because it is inherited (0.6): WR and TE only, 2022-2025, who played
# week 1 with a target, were BELOW replacement the prior season, and played 4+ of weeks 2-14.
# It says nothing about running backs -- the RB version is week1_share.py's backfield share,
# a different predictor on a different outcome -- so this screen is gated to WR and TE.
FORM_SIGS = (('targets', 8.0, 'targets'), ('snap_pct', 80.0, 'snaps'), ('tgt_share', 20.0, 'share'))
FORM_RATE = {2: '38%', 3: '42%'}


def inseason_screen(fr, pa, ypt_bar=7.13, tpg_bar=3.20, round_bar=3, min_games=2, min_tgt=5):
    """(label, flag text) or ('', '') for the 4.30 screen read on THIS season's cumulative form row
    `fr` and the man's pedigree row `pa` (doc 453, finding 4.43). Years 1 to 3 only; needs the games
    and receiving yards columns build_form.py writes since doc 453 (a form file without them returns
    blank, never a wrong screen)."""
    if not pa or not fr:
        return '', ''
    try:
        yr, rnd = int(float(pa.get('nfl_year') or 0)), int(float(pa.get('nfl_round') or 0))
        g, tg, yd = int(float(fr.get('games') or 0)), float(fr.get('targets') or 0), float(fr.get('rec_yds') or 0)
    except (TypeError, ValueError):
        return '', ''
    if not (1 <= yr <= 3) or g < min_games or tg < min_tgt:
        return '', ''
    ypt, tpg = yd / tg, tg / g
    if rnd <= round_bar and ypt > ypt_bar and tpg > tpg_bar:
        return (f'in-season screen 3 of 3 ({g} g)',
                f'in-season screen 3 of 3 (round {rnd} · {ypt:.1f} a target · {tpg:.1f} targets a game · {g} g)')
    return '', ''


def load_form():
    """(name, pos, team) -> (cumulative week-0 row, LAST COMPLETED GAME row). Returns ({}, why)
    when the file is absent, and the caller NAMES that rather than printing a lane that silently
    found nothing (0.2). The key is name + position + team and never less (section 3); build_form.py
    spells its teams through sheet_engine's own TEAM_ALIAS so both sides say LAR and WSH.

    TWO ROWS, NOT ONE, AND THEY ANSWER DIFFERENT QUESTIONS (doc 314). The workload screen wants the
    SEASON so far; the contest estimate wants the man's MOST RECENT GAME. In week 2 those are the
    same row and the difference is invisible, which is exactly how this would have shipped broken
    and stayed broken from week 3 on."""
    # EVERY RETURN IS A THREE-TUPLE. Doc 320 added the week count as a third value and changed
    # only the LAST return; the three below kept returning two, so any of them killed the whole
    # run with `ValueError: not enough values to unpack` instead of printing the reason they were
    # written to print. Found 17 Sept by `redteam_controls.py`, which has been failing its own
    # base control on this since doc 320 -- the harness does not copy form_2026.csv. Second
    # never-executed branch in two days (doc 340 was the first).
    if not os.path.exists(FORM):
        return {}, ("no " + os.path.basename(FORM)
                    + " -- run  py research\\wk1\\build_form.py"), 0
    out, last, weeks, has_flag, note = {}, {}, set(), False, ''
    done = set()                                   # weeks with rows and no game still in progress
    try:
        with open(FORM, newline='', encoding='utf-8-sig') as fh:
            for r in csv.DictReader(fh):
                if 'in_progress' in r:
                    has_flag = True
                w = str(r.get('week', '')).strip()
                weeks.add(w)
                key = (norm_name(r.get('player')), (r.get('pos') or '').strip().upper(),
                       team_key(r.get('team')))
                if w == '0':                       # 0 is the cumulative row; the rest are per week
                    out[key] = r
                    continue
                try:
                    wn = int(w)
                except ValueError:
                    continue
                if str(r.get('in_progress', '0')).strip() == '1':
                    continue                       # half a game must not be read as a game
                done.add(wn)
                prev = last.get(key)
                if prev is None or wn > int(prev['week']):
                    last[key] = r
    except Exception as exc:
        return {}, f'form_2026.csv could not be read ({type(exc).__name__})', 0
    if not out:
        return {}, ('form_2026.csv has no cumulative rows -- every week in it is still in '
                    'progress, so there is nothing to screen on'), 0
    if not has_flag:
        # NEVER GUESS AND NEVER SILENTLY SKIP (0.2). An old file has no in_progress column, so the
        # newest week in it MIGHT be half played. The lane still runs on the newest week; the page
        # is told the column is missing so the number can be discounted rather than trusted.
        note = ('form_2026.csv predates the in_progress column, so "his last game" is the newest '
                'week in the file and may be a week still being played -- re-run '
                'py research\\wk1\\build_form.py to remove the doubt')
    for k, v in out.items():
        v['_last'] = last.get(k)
    # THE THIRD RETURN IS THE COUNT OF COMPLETED WEEKS (doc 320). It is read off the week values
    # this loop already walks, and a week counts only when it produced rows that are NOT still in
    # progress -- a Monday-night game keeps its week open, which is the conservative direction for
    # a switch that re-orders depth charts.
    return out, note, len(done)


def _form_variant(form, player, pos, team):
    """doc 442: ESPN says "Joshua Palmer" and nflverse "Josh Palmer", so the exact name + position +
    team key misses him and every workload column prints blank (spot.py found it; he was the only
    miss on the wire). Same team, same position, same surname, and one of the first names is a
    prefix of the other: that is a variant of one man, not a second man. Exactly one candidate or
    nothing; two candidates is a real ambiguity and stays blank rather than guessing."""
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


def form_signals(fr):
    """How many of the three fire, and the plain-English reason. Never defaults a missing field to
    zero: a blank snap_pct means PFR has not posted him, which is not the same as not playing, so
    that signal simply does not fire and the count says so (doc 251: assert on the join)."""
    n, why, gaps = 0, [], []
    for col, bar, label in FORM_SIGS:
        raw = (fr.get(col) or '').strip()
        if raw == '':
            gaps.append(label)
            continue
        try:
            v = float(raw)
        except ValueError:
            gaps.append(label)
            continue
        if v >= bar:
            n += 1
            why.append(f'{label} {v:.0f}' if col != 'snap_pct' else f'{v:.0f}% of snaps')
    return n, ' · '.join(why), gaps


# --------------------------------------------------------------------------------------------
# THE PAGE.  Static text is the measured scheme (docs 223-225); the two tables are live.
# --------------------------------------------------------------------------------------------
CSS = """
:root{--ink:#1a1a18;--dim:#6b6b66;--ln:#d9d7d2;--bg:#fcfcfb;--go:#0b6b3a;--no:#a33;--pan:#f5f4ef}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 Georgia,'Iowan Old Style',serif;padding:34px 30px 60px}
.wrap{max-width:900px;margin:0 auto}
h1{font:700 27px/1.2 Georgia,serif;margin:0 0 4px}
h2{font:700 12px/1 Georgia,serif;letter-spacing:.13em;text-transform:uppercase;color:var(--dim);
   margin:34px 0 12px;padding-bottom:7px;border-bottom:1px solid var(--ln)}
h3{font:700 11px/1 Georgia,serif;letter-spacing:.11em;text-transform:uppercase;margin:20px 0 6px}
.sub{color:var(--dim);font-size:13px;margin-bottom:6px}
ol{margin:0 0 4px;padding-left:22px} ol li{margin-bottom:9px}
ol li b{font-weight:700}
p{margin:0 0 11px}
.box{background:var(--pan);border:1px solid var(--ln);border-radius:8px;padding:14px 18px;margin:0 0 18px}
table.w{border-collapse:collapse;width:100%;font-size:13.5px;margin-bottom:6px}
table.w th{font:700 10px/1 Georgia,serif;letter-spacing:.1em;text-transform:uppercase;color:var(--dim);
  text-align:left;padding:0 8px 6px 0;border-bottom:1px solid var(--ln)}
table.w td{padding:5px 8px 5px 0;border-bottom:1px solid #efeee9;vertical-align:baseline}
td.p{font-weight:700;white-space:nowrap} td.t{color:var(--dim);font-size:12px;white-space:nowrap}
td.r{text-align:right;white-space:nowrap;width:64px;font-variant-numeric:tabular-nums}
td.n{color:var(--dim);font-size:12.5px} td.n b{color:var(--ink)}
.q{opacity:.6}
tr.dz td.p{color:var(--go)} tr.dr td.p{color:var(--no)} tr.ds td.p{color:var(--dim)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:0 30px}
@media print{body{padding:0;font-size:10.5pt}.wrap{max-width:none}h2{page-break-after:avoid}
  table.w{page-break-inside:avoid}}
@media(max-width:640px){.cols{grid-template-columns:1fr}}
"""
STATIC_TOP = """<h2>The routine</h2>
<div class="box"><ol>
<li><b>Nothing to run.</b> The scheduled tasks rebuild this page; by hand it is <code>.\ff.bat</code>, never <code>py wire.py</code>.</li>
<li><b>Wednesday night: put the claims in, before 3am Thursday.</b> Claims execute Thursday morning; a claim placed Sunday runs in the same batch and gives up four days of news.</li>
<li><b>Order the claims: the man you would most hate to miss goes first.</b> Only your first winning claim comes at your real priority.</li>
<li><b>A drop on every claim.</b> A waiver claim with no drop fails on the roster limit one time in six; the same drop on several claims is a hedge (the first winner takes it); two men you want both need two drops. Never a man in the IR slot.</li>
<li><b>If the button says Add, add now.</b> A free agent costs no priority. If it says Claim, he processes Thursday.</li>
<li><b>Thursday and Sunday: set the lineup.</b> Kicker on matchup; defense held through a soft run (the run is below).</li></ol>
<p style='margin-top:10px'><b>Two lanes, kept apart.</b> <b>The hole:</b> somebody is hurt or on bye and you need a body Sunday (quarterback and tight end are easy, receiver needs discipline, running back is close to hopeless). <b>The gem:</b> a man who cannot start for you today and takes over a real job the week the starter goes down. The gem is claimed before the injury.</p></div>

<h2>The rules that decide a claim</h2>
<div class="cols">
<div>
<p><b>Stream the one-slot positions; build the bench at the many-slot ones.</b> Your added quarterbacks worked about a third of the time, your added receivers about one in eight. A second quarterback or tight end plays on a bye or an injury and nowhere else: claim one for a week you can see, start him, let him go.</p>
<p><b>The wire cannot fix a running-back hole.</b> Four of every five backs you add never give you a startable stretch; the bench is built with backs.</p>
</div>
<div>
<p><b>Buy the job, not the name.</b> The flag says a backfield is unresolved and what the job pays if he wins it; it has no opinion on who wins it.</p>
<p><b>The wire thins but does not dry up.</b> The best free men are about as good in November as in September.</p>
</div>
</div>

"""
STATIC_BOTTOM = """<h2>What the stash lane is worth</h2>
<div class="sub">Your chance that one claim ends with a startable player, four seasons of this league's claims.</div>
<table class="w"><tr><th>position</th><th class="r">chase the popular name</th><th class="r">stash the one nobody wants</th></tr>
<tr><td class="p">Tight end</td><td class="r">4.0%</td><td class="r"><b>19.6%</b></td></tr>
<tr><td class="p">Quarterback</td><td class="r">8.0%</td><td class="r"><b>16.8%</b></td></tr>
<tr><td class="p">Receiver</td><td class="r">5.2%</td><td class="r"><b>11.8%</b></td></tr>
<tr><td class="p">Running back</td><td class="r">4.6%</td><td class="r"><b>5.3%</b></td></tr>
</table>
<div class="sub" style="margin-top:8px"><b>Stash, do not chase, at every position.</b> One bench spot for a backfield stash, not three; the others go to tight end and quarterback.</div>

<h2>Why the gem is claimed early</h2>
<div class="box">
<p><b>You lose five of every six players another team also wants</b> (10 of 63 over two seasons) and land 56% of the ones nobody else claims. Priority resets each week to inverse standings, so the better your team, the later you pick.{WAIVER_LINE}</p>
<p><b>Your long list works:</b> a median of ten claims a week against the league's two, and at least one lands in 97% of the weeks you try. Point it at the man nobody is bidding on yet.</p>
<p><b>Being first wins you the player, not the right one:</b> alone you land 56% against 16% when somebody else bids, but a man the league later came for was startable 22% of the time against 24% for one nobody chased.</p>
</div>

"""


def _esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


# WHAT A DROP COSTS YOU, BUILT FROM THE ROSTER THAT EXISTS (doc 291). This table was typed in on
# draft night and never changed: it still listed Tyjae Spears, who was dropped, and never listed
# T.J. Hockenson, who was added. The draft picks below are fixed facts; who is on the roster is not.
# Keyed on espn_id (SECTION 3). The round bands it prints apply findings 4.18 (rounds 5 to 8 are
# the picks that become keepers) and 4.18b (a round-9+ keep returns about nothing), every week,
# so 4.18's index row saying "draft" only is wrong (doc 440).
DRAFTED_2026 = {'4426515': 8, '4890973': 17, '4685702': 32, '16800': 41, '4040715': 56,
                '4430027': 65, '4038815': 80, '4241985': 89, '4683062': 113, '4686658': 128,
                '4360689': 137, '-16005': 152, '4034949': 161}
KEEPER_2026 = '4426354'              # George Pickens, kept this year, so he cannot be kept in 2027
DROP_NOTE = {'4686658': 'almost none, but he is your only claim on the Las Vegas job'}


def drop_table(roster):
    if not roster:
        return ('<h2>What a drop costs you</h2><div class="bad"><b>The roster read returned nothing, '
                'so the drop table is missing, not empty.</b></div>')
    rows = []
    for pid, nm in roster.items():
        pick = DRAFTED_2026.get(pid)
        if pid == KEEPER_2026:
            cls, pk, txt = 'dz', 'keeper', 'none for 2027: he is this year&rsquo;s keeper and cannot be kept twice in a row'
        elif pick is None:
            cls, pk, txt = 'dz', 'waiver add', 'none: a waiver add can never be a keeper'
        elif pick >= 145:
            cls, pk, txt = 'dz', f'pick {pick}', 'none: a defense or a kicker is never a keeper'
        elif pick >= 97:
            cls, pk, txt = 'dn', f'pick {pick}', 'almost none: a keeper taken in round 9 or later has returned about nothing'
        elif pick >= 49:
            cls, pk, txt = 'dr', f'pick {pick}', 'real: rounds 5 to 8 are the picks that become keepers'
        else:
            cls, pk, txt = 'ds', f'pick {pick}', 'none: the first four rounds can never be kept'
        txt = DROP_NOTE.get(pid, txt)
        order = {'dz': 0, 'dn': 1, 'dr': 2, 'ds': 3}[cls]
        rows.append((order, -(pick or 999), nm, cls, pk, txt))
    rows.sort()
    body = ''.join(f'<tr class="{c}"><td class="p">{_esc(nm)}</td><td class="t">{pk}</td>'
                   f'<td class="n">{txt}</td></tr>' for _, _, nm, c, pk, txt in rows)
    return ('<h2>What a drop costs you</h2>'
            '<div class="sub">A keeper is a man you drafted in round 5 or later and held all year; a wire pickup '
            'never is. The cost of a drop is where he was drafted.</div>'
            '<table class="w"><tr><th>if you drop</th><th>how he got here</th>'
            '<th>what it costs you in 2027</th></tr>' + body + '</table>'
            '<div class="sub" style="margin-top:8px">Green costs nothing. Red is the audition window: do not '
            'drop one of those for a dart.</div>')


def usage_depth(rows, form, completed_weeks, min_weeks=2):
    """Re-rank depth within team by cumulative carries plus targets once the season has enough
    games to trust it. Chart order otherwise.

    DOC 320, MEASURED: the usage order names the man who actually inherits 72.1% of the time
    against the preseason chart's 62.2% (n=111 backfields, McNemar p=0.043), and in a SETTLED
    backfield 85.0% against 68.8% (p=0.001). The week-2 cell is a tie at 62.5% on n=8, which is
    why this does nothing before two completed weeks: the switch pays from week 3 and not before.

    TWO CORRECTIONS TO THE VERSION IN DOC 320 SECTION 4, both of the same shape -- a team with no
    usage signal must come out UNTOUCHED, not blanked:
      * `lead` was taken as '' when no man on the team had a usage row, and then written over
        every row's `ahead`. That silently deletes the man ahead for a whole backfield, and
        "the man ahead" is a printed column on the wire page and the gate on section 4.27's
        inheritance list. A team with nothing measured now returns unchanged.
      * the chart depths were being renumbered before that check, so the same team also lost its
        chart order. Both are now inside the `if not seen: continue`.

    [doc 441] THE CHART THIS RE-RANKS IS TODAY'S NOW, NOT AUGUST'S, and nothing in here changed.
    load_depth() hands this function depth_daily.csv's order when that file exists (the August
    depth_map.csv order otherwise). The relation is: USAGE IS THE EVIDENCE and still wins from the
    third completed week; THE CHART IS THE TIEBREAK inside the usage sort (`was`), THE ORDER for
    every man with no usage line (the +10 below), and THE FRESHNESS SOURCE -- a man ESPN has taken
    off its chart sits below every man on it before this runs, where the August file could not
    see him leave. Off-chart and unmeasured stacks: 50 + August depth + 10.
    """
    if completed_weeks < min_weeks or not form:
        return rows
    by_tm = {}
    for r in rows:
        by_tm.setdefault(r['tm'], []).append(r)
    moved = 0
    for tm, rs in by_tm.items():
        def touches(r):
            f = form.get((norm_name(r['player']), 'RB', team_key(tm)))
            try:
                return float(f['touches']) if f and f.get('touches') not in (None, '') else -1.0
            except (TypeError, ValueError):
                return -1.0
        seen = [r for r in rs if touches(r) >= 0]
        if not seen:                # nothing measured on this team: leave the chart exactly as it is
            continue
        was = {id(r): r['depth'] for r in rs}
        seen.sort(key=lambda r: (-touches(r), was[id(r)]))
        for i, r in enumerate(seen, 1):
            r['depth'] = i
        for r in rs:                # a man with no line sits below every man with one (the FB offset)
            if touches(r) < 0:
                r['depth'] = was[id(r)] + 10
        lead = seen[0]['player']
        for r in rs:
            r['ahead'] = lead if r['depth'] > 1 else ''
            if r['depth'] != was[id(r)]:
                moved += 1
    if moved:
        print(f'  depth re-ranked on usage (doc 320): {moved} rows moved, '
              f'{completed_weeks} completed weeks')
    return rows


# doc 441: today's ESPN depth chart and the newest NFL injury report, both from nflverse, both
# rebuilt every run by Scripts\research\wk1\build_depth_daily.py. Until this the seat lane read
# one chart, captured 8 August, for the whole season.
DEPTH_DAILY = os.path.join(SRC, 'depth_daily.csv')
PRACTICE = os.path.join(SRC, 'practice_2026.csv')
OFF_CHART = 50        # a man in the August map who is NOT on today's chart sorts below every man who is
CHART_STALE_DAYS = 3  # a judgement call, not a measurement: the feed posts twice a day, so three days
                      # old means the builder served its cached copy three runs running


def _name_key(s):
    """build_form.py's norm(): letters only, suffix dropped. practice_2026.csv carries no espn_id,
    so a man with no gsis_id on today's chart is joined on name + position + team (section 3),
    never less. Same result as norm_name() with the spaces and non-letters removed."""
    return ''.join(ch for ch in norm_name(s) if 'a' <= ch <= 'z')


def load_depth_daily():
    """Today's running-back order: espn_id -> dict(depth, player, tm, gsis). Returns ({}, '', why)
    when the file is absent, unreadable or short, and the caller puts `why` on the page (0.2: a
    step that cannot do the thing it is named after says so, it does not fall back in silence)."""
    if not os.path.exists(DEPTH_DAILY):
        return {}, '', ('depth_daily.csv is missing, so the seat lane is on the 8 August chart '
                        '(depth_map.csv) -- run  py research\\wk1\\build_depth_daily.py')
    out, stamps = {}, set()
    try:
        with open(DEPTH_DAILY, newline='', encoding='utf-8-sig') as fh:
            for r in csv.DictReader(fh):
                if (r.get('pos') or '').strip().upper() != 'RB':
                    continue
                pid = str(r.get('espn_id') or '').strip()
                if not pid:
                    continue                     # doc 414: a slot with no man in it is not a man
                out[pid] = dict(depth=int(float(r['depth'])), player=(r.get('player') or '').strip(),
                                tm=team_key(r.get('team')), gsis=(r.get('gsis_id') or '').strip())
                stamps.add((r.get('as_of') or '').strip())
    except (KeyError, ValueError, OSError) as exc:
        return {}, '', (f'depth_daily.csv could not be read ({type(exc).__name__}), so the seat '
                        f'lane is on the 8 August chart (depth_map.csv)')
    teams = {v['tm'] for v in out.values()}
    if len(teams) < 30:
        return {}, '', (f'depth_daily.csv lists running backs for only {len(teams)} teams, so the '
                        f'seat lane is on the 8 August chart (depth_map.csv)')
    _check_codes('depth_daily.csv', sorted(teams))
    as_of = max(stamps) if stamps else ''
    return out, as_of, ''


def load_practice():
    """The newest injury report, Source\\practice_2026.csv. Two maps -- gsis_id -> row and
    (name_key, team) -> row -- plus the report's week, plus why when it is absent."""
    if not os.path.exists(PRACTICE):
        return {}, {}, '', ('practice_2026.csv is missing, so no depth row carries an injury-report '
                            'status -- run  py research\\wk1\\build_depth_daily.py')
    by_gsis, by_key, weeks = {}, {}, set()
    try:
        with open(PRACTICE, newline='', encoding='utf-8-sig') as fh:
            for r in csv.DictReader(fh):
                if (r.get('pos') or '').strip().upper() not in ('RB', 'FB'):
                    continue
                g = (r.get('gsis_id') or '').strip()
                if g:
                    by_gsis[g] = r
                by_key[((r.get('name_key') or '').strip(), team_key(r.get('team')))] = r
                weeks.add((r.get('week') or '').strip())
    except (KeyError, OSError) as exc:
        return {}, {}, '', f'practice_2026.csv could not be read ({type(exc).__name__})'
    return by_gsis, by_key, max(weeks) if weeks else '', ''


def load_depth(form=None, completed_weeks=0):
    """depth_map.csv -- the man behind, and what the job pays if it opens.

    [doc 441] THE ORDER IS TODAY'S, THE JOB IS AUGUST'S. depth_map.csv is a chart captured 8 August
    and it stays the source of job_ceil / job / vbd, which come from projections and which the
    daily chart does not carry. When Source\\depth_daily.csv exists (ESPN's own chart via nflverse,
    rebuilt every run) the depth 1, 2, 3 order comes from it, joined on espn_id (section 3):
      * a man on both keeps his August job fields and takes today's depth;
      * a man on today's chart and NOT in the August map gets a row: job_ceil and job are TEAM
        constants (depth_map.py stamps one number on every man on a roster, and the number is the
        backfield's, not his), so they come from his team's August rows; he has no board value, so
        vor is the -999 sentinel a missing vbd already gets; and his flag says all of that. Three
        of these are lead backs the August map could never see, because the board it was built
        from had the keepers removed (doc 111): Stevenson, Etienne, Skattebo;
      * a man in the August map and NOT on today's chart keeps his row with chart_depth blank, the
        flag "not on today's chart", and a depth of 50 + his August depth so he sorts below every
        man who IS on the chart. NOT a blank depth: next_man_up(), in_doubt() and usage_depth()
        all compare depth as an integer, and a None there takes the whole run down;
      * a man whose team differs between the two (Demercado: KC in August, DAL today) is MOVED.
        His own vor travels with him, the job fields become the new team's, and the old team never
        lists him as an inheritor again (doc 426 is this defect, caught on the page).
    Without the daily file this is the 8 August chart exactly as before, and the page says so.

    HOW THE DAILY CHART AND THE USAGE RE-RANK RELATE. usage_depth() still runs after this and still
    wins: from the third completed week the order within a team is realised carries plus targets
    (doc 320, 72.1% against the chart's 62.2%). The chart is the TIEBREAK inside that sort and the
    ORDER for any man with no usage line (a signing, a rookie, a man back from injury), and it is
    the FRESHNESS source: a man ESPN has taken off its chart, or listed fourth behind a stand-in, is
    seen here the morning it happens. Usage is the evidence; the chart is what you rank on until the
    evidence exists.

    THE CAVEAT THE BUILDER MEASURED: ESPN's chart lists the man PLAYING this week, not the job
    holder. An injured starter is demoted (Achane RB3 at MIA, Jacobs RB4 at GB), so depth 1 on a
    team like that is the stand-in. The August depth is kept on every row as aug_depth, the demoted
    starter is flagged, and the newest injury report (practice_2026.csv, joined on gsis_id through
    the daily chart, else name + team) rides on every row as report_status / practice_status /
    report_week. NOTHING HERE ACTS ON THE REPORT YET. NOT YET RUN: whether the report's Out beats
    ESPN's injuryStatus on the free pool as next_man_up()'s step-past trigger, and whether a
    cumulative-usage leader who is Out should still be depth 1 (he is today, Achane, 3 weeks).
    """
    p = os.path.join(HERE, 'depth_map.csv')
    if not os.path.exists(p):
        return []
    out = []
    with open(p, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            # depth_map is an RB instrument.  Its job columns are computed from the BACKFIELD, so
            # reading job_ceil on a WR row gives you that team's running back (doc 224).  Assert it.
            if r.get('pos') != 'RB':
                continue
            try:
                # NOTE: depth 1 rows are KEPT. in_doubt() needs the starter himself -- filtering
                # them out here is what made the first version of that lane silently return zero
                # rows in every case. next_man_up() does its own depth >= 2 filter instead.
                out.append(dict(espn_id=str(r['espn_id']).strip(), player=r['player'], tm=r['tm'],
                                depth=int(r.get('depth') or 9),
                                vor=float(r.get('vbd') or -999),
                                ahead=r.get('ahead', ''), ceil=float(r.get('job_ceil') or 0),
                                job=r.get('job', '')))
            except ValueError:
                continue
    for r in out:                     # every new key is set on EVERY row, blank, before any join
        r['aug_depth'], r['chart_depth'], r['flag'] = r['depth'], '', ''
        r['report_status'] = r['practice_status'] = r['practice_injury'] = r['report_week'] = ''

    daily, as_of, why = load_depth_daily()
    if why:
        if why not in LOAD_PROBLEMS:          # load_depth() can be called more than once a run
            LOAD_PROBLEMS.append(why)
        daily = {}
    else:
        # THE AGE OF THE CHART IS CHECKED, NOT ASSUMED. build_depth_daily.py serves its cached copy
        # when the fetch fails, with a warning on ITS console that this page never sees.
        try:
            stamp = dt.datetime.strptime(as_of[:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=dt.timezone.utc)
            age = (dt.datetime.now(dt.timezone.utc) - stamp).days
        except ValueError:
            stamp, age = None, None
        if age is not None and age >= CHART_STALE_DAYS:
            LOAD_PROBLEMS.append(f"depth_daily.csv is {age} days old (as of {as_of[:16]}Z), so "
                                 f"'today's chart' below is not today's -- run  py research\\wk1\\"
                                 f"build_depth_daily.py")
        out = _apply_daily(out, daily, as_of)

    _attach_practice(out, daily)
    out = usage_depth(out, form, completed_weeks)
    out.sort(key=lambda x: -x['ceil'])
    return out


def _apply_daily(rows, daily, as_of):
    """Put today's order on the August rows. See load_depth() for the four cases."""
    by_id = {r['espn_id']: r for r in rows}
    spell, const = {}, {}
    for r in rows:
        # depth_map spells Washington WAS and sheet_engine WSH; a new row must group with its
        # team in next_man_up() and in_doubt(), which group on the literal `tm`.
        spell.setdefault(team_key(r['tm']), r['tm'])
        const.setdefault(team_key(r['tm']), (r['ceil'], r['job']))
    lead = {d['tm']: d['player'] for d in daily.values() if d['depth'] == 1}
    n_both = n_off = n_moved = n_new = 0
    demoted, promoted = [], []
    for r in rows:
        d = daily.get(r['espn_id'])
        if d is None:
            n_off += 1
            r['chart_depth'] = ''
            r['depth'] = OFF_CHART + r['aug_depth']
            r['flag'] = "not on today's chart"
            if r['aug_depth'] == 1:
                r['flag'] += ' (August starter)'
                demoted.append((r['tm'], r['player'], 'off the chart'))
            if lead.get(team_key(r['tm'])):
                r['ahead'] = lead[team_key(r['tm'])]
            continue
        n_both += 1
        if d['tm'] != team_key(r['tm']):
            n_moved += 1
            old = r['tm']
            r['tm'] = spell.get(d['tm'], d['tm'])
            r['ceil'], r['job'] = const.get(d['tm'], (0.0, ''))
            r['flag'] = f"moved from {old} since the August chart; job fields are {r['tm']}'s"
        elif r['aug_depth'] == 1 and d['depth'] > 1:
            r['flag'] = (f"August starter, listed RB{d['depth']} today -- the chart lists the man "
                         f"playing this week, not the job holder")
            demoted.append((r['tm'], r['player'], f"RB{d['depth']}"))
        r['chart_depth'] = r['depth'] = d['depth']
        r['ahead'] = lead.get(d['tm'], '') if d['depth'] > 1 else ''
    for pid, d in daily.items():
        if pid in by_id:
            continue
        n_new += 1
        ceil, job = const.get(d['tm'], (0.0, ''))
        rows.append(dict(espn_id=pid, player=d['player'], tm=spell.get(d['tm'], d['tm']),
                         depth=d['depth'], vor=-999.0,
                         ahead=lead.get(d['tm'], '') if d['depth'] > 1 else '',
                         ceil=ceil, job=job, aug_depth='', chart_depth=d['depth'],
                         flag=("on today's chart, not in the August map: job fields are the team's, "
                               "no board value"),
                         report_status='', practice_status='', practice_injury='', report_week=''))
        if d['depth'] == 1:
            promoted.append((spell.get(d['tm'], d['tm']), d['player']))
    print(f"  depth chart: today's order ({as_of[:16]}Z) on {n_both} August men; {n_new} on today's "
          f"chart only, {n_off} August men off it, {n_moved} changed teams")
    if demoted:
        print('  August starters not RB1 today: ' + ', '.join(f'{t} {p} ({how})' for t, p, how in demoted))
    if promoted:
        print('  RB1 today with no August row: ' + ', '.join(f'{t} {p}' for t, p in promoted))
    return rows


def _attach_practice(rows, daily):
    """The newest injury report on every depth row: gsis_id through today's chart first, then
    name + team for a man who is not on it. Blank, never 'ACTIVE', when he has no line: the report
    lists only men with an injury, so an absent row is a fact and not a status."""
    by_gsis, by_key, wk, why = load_practice()
    if why:
        if why not in LOAD_PROBLEMS:
            LOAD_PROBLEMS.append(why)
        return
    hit = 0
    for r in rows:
        d = daily.get(r['espn_id'])
        pr = by_gsis.get(d['gsis']) if d and d.get('gsis') else None
        if pr is None:
            pr = by_key.get((_name_key(r['player']), team_key(r['tm'])))
        if pr is None:
            continue
        hit += 1
        r['report_status'] = (pr.get('report_status') or '').strip()
        r['practice_status'] = (pr.get('practice_status') or '').strip()
        r['practice_injury'] = (pr.get('practice_injury') or '').strip()
        r['report_week'] = (pr.get('week') or '').strip()
        if r['report_status'] and r['flag'].startswith('August starter'):
            r['flag'] += f" ({r['report_status']} on the week {r['report_week']} report)"
    print(f'  injury report: week {wk or "?"}, {hit} of {len(rows)} depth rows carry a line')


def next_man_up(depth_rows, available, status=None, holder_status=None):
    """ONE row per team: the man who would actually inherit, among those you can still get.

    [doc 443] A STASH IS A BET PLACED BEFORE THE INJURY, AND THE MAN AHEAD MUST STILL BE STANDING.
    Doc 411's rule on the week sheet ("a seat is an option on a job that is still held; once the
    starter is already out there is no option left") never reached this lane, so on 29 Sept it
    printed Ollie Gordon II "behind De'Von Achane, job pays 261" with Achane on injured reserve:
    the job was open, Gordon was already in the IN DOUBT lane, and the same man was offered
    twice under two headings. `holder_status` is ESPN's status for EVERY man in the league
    (owned and free); a team whose depth-1 man carries a long absence is set aside and NAMED
    under the table (0.5(c)5), not silently dropped. One predicate, sheet_engine.GONE_FOR_WEEKS,
    on both pages (doc 424). Without `holder_status` the lane behaves exactly as before.

    Filtering on depth >= 2 alone is not 'one injury away' -- it is 'everybody on that team's
    bench', and because every row on a team carries the SAME job value they all sort together at
    the top. The live run on 2026-09-08 put Jacob Saylors (Detroit's FOURTH back) above Brian
    Robinson because Gibbs' job is worth 332. Rank within the team by depth, then by our own
    value, and keep the first man who is still available."""
    by_team, holder = {}, {}
    for r in depth_rows:
        if r['depth'] < 2:                      # the man holding the job is not a stash
            if r['depth'] == 1 and r['tm'] not in holder:
                holder[r['tm']] = r
            continue
        by_team.setdefault(r['tm'], []).append(r)
    status = status or {}
    out, opened = [], []
    for tm, rows in by_team.items():
        h = holder.get(tm)
        hs = ((holder_status or {}).get(h['espn_id'], '') if h else '').upper()
        if h and hs in _GONE_FOR_WEEKS:
            opened.append((tm, h['player'], hs.replace('_', ' ').lower()))
            continue
        rows.sort(key=lambda x: (x['depth'], -x['vor']))
        # Only the men actually next in line. If the true handcuff is on somebody else's
        # roster, that job is not available to you AT ANY PRICE and the team drops off the
        # list -- taking the third-stringer instead is two injuries away, not one.
        # THAT RULE IS UNCHANGED. What is new (doc 296) is the OTHER reason a tier can fail:
        # every free man at that depth is someone ESPN says is not playing. On 11 Sept this list
        # named Jordan James as the man who inherits McCaffrey's 303-point job. James was OUT in
        # ESPN's own pool and did not play in week 1; Kaelon Black, one row deeper, ACTIVE and
        # free, led the team in carries. A man who is OUT is not one injury away, he is two.
        # So: step past a tier only when it is free-but-not-playing, never when it is OWNED, and
        # NAME the man stepped over so the reason is on the page and not in this comment.
        pick, stepped = None, []
        for d in sorted({r['depth'] for r in rows}):
            tier = [r for r in rows if r['depth'] == d]
            free = [r for r in tier if r['espn_id'] in available]
            if not free:
                break                           # owned: the job is not for sale, drop the team
            able = [r for r in free
                    if status.get(r['espn_id'], 'ACTIVE') not in NOT_PLAYING]
            if able:
                pick = dict(max(able, key=lambda x: x['vor']))
                break
            stepped += free                     # free, but not playing: look one deeper
        if pick is None:
            continue
        if stepped:
            pick['over'] = ', '.join(
                f"{r['player']} ({status.get(r['espn_id'], 'ACTIVE').replace('_', ' ').lower()})"
                for r in stepped)
        pick['status'] = status.get(pick['espn_id'], 'ACTIVE')
        out.append(pick)
    out.sort(key=lambda x: -x['ceil'])
    next_man_up.opened = sorted(opened)         # the jobs already open, named on the page
    return out
next_man_up.opened = []


STATUS_PAIRS = os.path.join(SRC, 'status_pairs_2026.csv')


def log_status_pairs(depth_rows, all_status, week):
    """[doc 445] THE INPUT THE PRACTICE-REPORT QUESTION NEEDS, LOGGED EVERY RUN. Whether the injury
    report's Out (or a DNP with no designation) says anything ESPN's live injuryStatus does not cannot
    be measured on history, because no file holds ESPN's status day by day. This writes it: one row per
    depth row per run date, with ESPN's status and the report's status and practice status side by side.
    Appended, never rewritten; a run date already logged is skipped, so a second run in a day adds
    nothing. Read-only for every page; nothing acts on it until it is measured."""
    today = dt.date.today().isoformat()
    try:
        seen = set()
        if os.path.exists(STATUS_PAIRS):
            with open(STATUS_PAIRS, newline='', encoding='utf-8-sig') as fh:
                seen = {r.get('date') for r in csv.DictReader(fh)}
        if today in seen:
            return
        rows = []
        for r in depth_rows:
            es = (all_status.get(r['espn_id']) or 'ACTIVE').upper()
            if es == 'ACTIVE' and not r.get('report_status') and not r.get('practice_status'):
                continue
            rows.append([today, week, r['espn_id'], r['player'], r['pos'] if 'pos' in r else 'RB', r['tm'], es,
                         r.get('report_status', ''), r.get('practice_status', ''), r.get('report_week', '')])
        new = not os.path.exists(STATUS_PAIRS)
        with open(STATUS_PAIRS, 'a', newline='', encoding='utf-8') as fh:
            w = csv.writer(fh)
            if new:
                w.writerow(['date', 'week', 'espn_id', 'player', 'pos', 'tm', 'espn_status', 'report_status',
                            'practice_status', 'report_week'])
            w.writerows(rows)
        print(f'  status pairs: {len(rows)} rows logged for {today} -> {os.path.basename(STATUS_PAIRS)}')
    except Exception as exc:                            # a log must never take the wire down
        print(f'  status pairs NOT logged -- {type(exc).__name__}: {exc}')


def league_status(roster_json):
    """espn_id -> ESPN injury status for every ROSTERED man in the league, off the mTeam read.
    The free pool's statuses come from the player read; this is the other half, and the stash
    lane needs it because the man ahead is, by construction, somebody else's starter."""
    out = {}
    for t in (roster_json or {}).get('teams', []) or []:
        for e in (t.get('roster') or {}).get('entries', []):
            p = e.get('playerPoolEntry', {}).get('player', {}) or {}
            if p.get('id') is not None:
                out[str(p.get('id'))] = (p.get('injuryStatus') or 'ACTIVE').upper()
    return out


SCHED = os.path.join(SRC, 'sched_2026.csv')
TEAM25 = os.path.join(SRC, 'team_2025.csv')
LOOK_WEEKS = 5
PRO = {1:'ATL',2:'BUF',3:'CHI',4:'CIN',5:'CLE',6:'DAL',7:'DEN',8:'DET',9:'GB',10:'TEN',
       11:'IND',12:'KC',13:'LV',14:'LAR',15:'MIA',16:'MIN',17:'NE',18:'NO',19:'NYG',
       20:'NYJ',21:'PHI',22:'ARI',23:'PIT',24:'LAC',25:'SF',26:'SEA',27:'TB',28:'WSH',
       29:'CAR',30:'JAX',33:'BAL',34:'HOU'}


def fetch_schedule():
    """The whole 2026 schedule, from ESPN's own pro-team view. Cached; refreshed weekly.

    Written because Matt asked for weeks-ahead planning: "I likely need to look weeks ahead for
    QB bye week fill in... consider soft schedule when waivers for those an QB are thin."
    You cannot plan a bye-week fill three weeks out without knowing who plays whom.
    """
    fresh = (os.path.exists(SCHED)
             and (dt.datetime.now() - dt.datetime.fromtimestamp(os.path.getmtime(SCHED))).days < 7)
    # doc 381: the file gained a `kick` column (kickoff, epoch ms, ESPN's own `date` field) so the
    # pages can print the next lineup lock. A file written before that column existed is refetched
    # whatever its age; a fresh file that already has it is left alone.
    if fresh:
        try:
            with open(SCHED, newline='', encoding='utf-8-sig') as fh:
                fresh = 'kick' in (next(csv.reader(fh)) or [])
        except (OSError, StopIteration):
            fresh = False
    if fresh:
        return
    try:
        url = ("https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/%d"
               "?view=proTeamSchedules_wl" % SEASON)
        r = requests.get(url, cookies=COOKIES, headers=HEADERS, timeout=30)
        r.raise_for_status()
        teams = ((r.json().get('settings') or {}).get('proTeams')) or []
        out = []
        for t in teams:
            ab = t.get('abbrev') or PRO.get(t.get('id'), '?')
            for wk, games in (t.get('proGamesByScoringPeriod') or {}).items():
                for g in games:
                    h, a = g.get('homeProTeamId'), g.get('awayProTeamId')
                    opp = a if PRO.get(h) == ab or t.get('id') == h else h
                    # doc 381: kickoff as ESPN carries it (epoch ms, UTC) and whether the start
                    # time is still to be announced. Blank when the field is absent, never 0.
                    kick = g.get('date')
                    out.append((int(wk), ab, PRO.get(opp, '?'),
                                'home' if t.get('id') == h else 'away',
                                int(kick) if isinstance(kick, (int, float)) and kick > 0 else '',
                                1 if g.get('startTimeTBD') else 0))
        if not out:
            print("  (ESPN returned no schedule; the look-ahead will say so rather than guess)")
            return
        out.sort()
        with open(SCHED, 'w', newline='', encoding='utf-8') as fh:
            w = csv.writer(fh)
            w.writerow(['week', 'team', 'opp', 'side', 'kick', 'tbd'])
            w.writerows(out)
        print(f"  schedule refreshed: {len(out)} team-weeks -> {SCHED}")
    except Exception as exc:
        print(f"  (could not refresh the schedule: {type(exc).__name__}; using whatever is on file)")


def load_sched():
    if not os.path.exists(SCHED):
        return {}
    out, seen = {}, set()
    with open(SCHED, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            try:
                tm, opp = team_key(r['team']), team_key(r['opp'])
                out.setdefault(int(r['week']), {})[tm] = (opp, r.get('side', ''))
                seen.update((tm, opp))
            except (KeyError, ValueError):
                continue
    _check_codes('sched_2026.csv', seen)
    return out


def load_team25():
    """2025 points scored and allowed per game. The matchup axis, and a rough one --
    a defense carries about 4% of next year's variance and an offence about 15%, so this is
    a tiebreak between streamers, never a reason to start a bad one."""
    out = {}
    if not os.path.exists(TEAM25):
        return out
    with open(TEAM25, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            try:
                out[team_key(r['team'])] = (float(r['pts_allowed_pg']), float(r['pts_scored_pg']))
            except (KeyError, ValueError):
                continue
    _check_codes('team_2025.csv', out)
    return out


LINES = os.path.join(SRC, 'lines_2026.csv')
LINES_ASOF = ''             # when the books' numbers on file were read, for the page; '' when no file


def load_lines():
    """The pregame line, from Source\\lines_2026.csv (built by Scripts\\research\\wk1\\build_lines.py).

    WHY THIS EXISTS (doc 441, finding 4.39). The defense run and the look-ahead were ranked on what
    the opponent scored per game LAST SEASON, because that was the only matchup number on the drive.
    Measured over five seasons among the defenses Matt could actually claim, the unit facing the
    lowest opponent implied total that week scores about +3.2 a week over picking at random, equal to
    the opponent's season-to-date rule and posted before any game is played. At quarterback the
    own-team implied total clears random by about +4.5 and sits beside the softest-matchup rule as
    a second read.

    Returns {(week, team): (opp, own_implied, opp_implied, spread_for_team, total)} for every
    team-game that CARRIES a line. A game with no line yet is simply absent, so a caller that misses
    falls back to last season and says so; it never reads a zero. spread_for_team is this team's
    expected margin, positive when it is favoured. A missing file returns {} and the page says the
    lines are missing (the LOAD_PROBLEMS convention), never that every matchup is average.
    """
    global LINES_ASOF
    out = {}
    if not os.path.exists(LINES):
        LOAD_PROBLEMS.append('lines_2026.csv is missing, so the defense run and the look-ahead are '
                             'ranked on last season\'s averages and not on the pregame line; run '
                             'py research\\wk1\\build_lines.py')
        return out
    seen, asof, nrows = set(), '', 0
    try:
        with open(LINES, newline='', encoding='utf-8-sig') as fh:
            for r in csv.DictReader(fh):
                nrows += 1
                if (r.get('has_line') or '0').strip() != '1':
                    continue
                try:
                    w = int(r['week'])
                    home, away = team_key(r['home']), team_key(r['away'])
                    ih, ia = float(r['implied_home']), float(r['implied_away'])
                    spread, total = float(r['spread_line']), float(r['total_line'])
                except (KeyError, ValueError, TypeError):
                    continue
                seen.update((home, away))
                asof = asof or (r.get('as_of') or '').strip()
                out[(w, home)] = (away, ih, ia, spread, total)
                out[(w, away)] = (home, ia, ih, -spread, total)
    except OSError as exc:
        LOAD_PROBLEMS.append(f'lines_2026.csv could not be read ({type(exc).__name__}), so the '
                             f'defense run and the look-ahead are ranked on last season\'s averages')
        return {}
    if not nrows:
        LOAD_PROBLEMS.append('lines_2026.csv is empty, so the defense run and the look-ahead are '
                             'ranked on last season\'s averages')
        return {}
    if not out:
        LOAD_PROBLEMS.append(f'lines_2026.csv holds {nrows} games and not one carries a line, so the '
                             f'defense run and the look-ahead are ranked on last season\'s averages')
        return {}
    _check_codes('lines_2026.csv', seen)
    LINES_ASOF = asof
    return out


POSALLOW = os.path.join(SRC, 'pos_allowed_2025.csv')
PLAYOFF_WEEKS = (15, 16, 17)


def load_posallow():
    """Last season's points allowed per game, by team and by position.

    Only tight end uses it, and that is deliberate. Measured on five seasons of drafted
    players: an easier week 15-17 slate was worth about +3.4 points at TIGHT END and
    nothing at quarterback, back or receiver -- all three came back flat, and so did the
    same test run across weeks 1 to 14. Tight end is the position where the defenses sit
    furthest apart (last season the softest gave up more than twice the stingiest), and
    three weeks is too short a stretch for that to average itself away.
    """
    out = {}
    if not os.path.exists(POSALLOW):
        return out
    with open(POSALLOW, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            try:
                out[(team_key(r['team']), r['position'])] = float(r['allowed_pg'])
            except (KeyError, ValueError):
                continue
    _check_codes('pos_allowed_2025.csv', {k[0] for k in out})
    return out


def te_playoff_slate(sched, allow, rows, mine_te):
    """Your tight end and the best free ones, ranked by the weeks 15-17 draw.

    THE FINDING THIS APPLIES: finding 4.26(b), doc 229. The tight-end weeks 15 to 17 draw is the one
    schedule effect that measured, so the playoff slate ranks tight ends on it; 4.26(a), the keeper
    rule (take the expensive hit, not the bargain), is a draft-night rule with no in-season term and
    is not applied here or anywhere on a page. check_inputs.py lists a finding no script cites; this
    is the citation, and the code below is the implementation.

    Returns (list, note). The note is filled in whenever the answer cannot be computed --
    a missing schedule must SAY it is missing, not render an empty box.
    """
    if not sched:
        return [], 'no schedule on file, so the playoff slate is missing, not empty'
    if not allow:
        return [], 'pos_allowed_2025.csv is not on the drive, so the playoff slate cannot be built'
    gone = [w for w in PLAYOFF_WEEKS if not sched.get(w)]
    if gone:
        return [], f'the schedule on file has no week {gone} yet, so the playoff slate is not built'
    seen = {m[0] for m in mine_te}
    cand = [(n, team_key(t), m) for n, t, m in mine_te]
    for r in rows:
        if r['pos'] == 'TE' and r['player'] not in seen:
            cand.append((r['player'], team_key(r['team']), False))
            seen.add(r['player'])
        if len(cand) >= 12:
            break
    out = []
    for name, tm, is_mine in cand:
        opps, vals = [], []
        for w in PLAYOFF_WEEKS:
            o = (sched.get(w, {}).get(tm) or ('', ''))[0]
            opps.append(o or '--')
            v = allow.get((o, 'TE'))
            if v is not None:
                vals.append(v)
        if len(vals) < len(PLAYOFF_WEEKS):
            continue
        out.append({'player': name, 'tm': tm, 'mine': is_mine, 'opps': opps,
                    'mean': sum(vals) / len(vals)})
    out.sort(key=lambda d: -d['mean'])
    return out, ''


DST_RUN_WEEKS = 4


def dst_runs(week, sched, t25, free_dst, mine_dst=None, k=DST_RUN_WEEKS, lines=None):
    """The softest RUN ahead for a defense you could hold, not the softest single week.

    Measured on every defense-week of the last four seasons, whether anybody started it or
    not. Against an average defense week of 5.2 points: the easiest fifth of draws returns
    6.5 and the hardest returns 3.5 -- but the important half of that is the BOTTOM. In the
    hardest fifth, more than a quarter of weeks score BELOW ZERO and 37% score under two
    points; in the easiest fifth that is 9% and 17%. The gap is 3.0 points a week and the
    downside half of it is bigger than the upside half.

    So the point is not to chase the best defense each week. It is to never be forced into
    a bad one -- and being forced is exactly what happens when you shop for a defense every
    week and pick late. Four in every ten of your waiver claims went to a defense in each of
    the last two seasons. Every one of those pushes you to the back for the running back you
    cannot replace any other way.

    Hold one defense through a soft run instead. Returns (list, note); a missing schedule or
    a missing team file SAYS so rather than rendering an empty box.

    THE NUMBER A WEEK IS RANKED ON (doc 441, finding 4.39). Where the pregame line is posted, a
    week's "faces" value is the OPPONENT'S IMPLIED TOTAL from `lines` (load_lines()), which is
    what the books expect that offence to score on Sunday; where no line exists yet, which is the
    case for weeks more than one or two out, it stays last season's points scored per game from
    team_2025.csv. Each row carries `lined_weeks` and `games` so the page can print "3 of 4 weeks
    on the line", and `marks`, one per week, with the number and which of the two it is. The sort
    is unchanged: byes first, then faces, softest first.
    """
    if not sched:
        return [], 'no schedule on file, so the defense run is missing, not empty'
    lines = lines or {}
    if not t25 and not lines:
        return [], 'team_2025.csv is not on the drive and no line is on file, so the defense run cannot be built'
    if not week:
        return [], 'the week is unknown, so the defense run was not built'
    weeks = [w for w in range(week, week + k) if sched.get(w)]
    if len(weeks) < 2:
        return [], f'the schedule on file runs out after week {week}, so no run could be built'

    def run_for(tm):
        """One defense's run: the opponents, the number each week is ranked on, and its source."""
        opps, vals, marks, lined = [], [], [], 0
        for w in weeks:
            o, side = (sched.get(w, {}).get(tm) or ('', ''))
            opps.append(o or 'bye')
            if not o:
                marks.append({'opp': 'bye', 'side': '', 'val': None, 'line': False})
                continue
            ln = lines.get((w, tm))
            if ln is not None and ln[0] == o:
                v, on_line = ln[2], True                  # what the books expect that opponent to score
            else:
                # the line's opponent and the schedule's disagree, or there is no line: the line is
                # not used for this week, and a disagreement is named once on the page (section 3)
                if ln is not None and ln[0] != o:
                    _line_mismatch(w, tm, o, ln[0])
                v25 = t25.get(o)
                v, on_line = (v25[1] if v25 is not None else None), False   # what he SCORED per game
            marks.append({'opp': o, 'side': side, 'val': v, 'line': on_line})
            if v is not None:
                vals.append(v)
                lined += 1 if on_line else 0
        return opps, vals, marks, lined

    out = []
    for d in (free_dst or []):
        tm = team_key(d.get('team')) or '?'
        opps, vals, marks, lined = run_for(tm)
        if len(vals) < 2:
            continue
        out.append({'player': d.get('player', '?'), 'team': tm, 'mine': bool(d.get('mine')),
                    'weeks': f'{weeks[0]}-{weeks[-1]}', 'opps': opps,
                    'faces': sum(vals) / len(vals), 'byes': opps.count('bye'),
                    'marks': marks, 'lined_weeks': lined, 'games': len(vals)})
    for d in (mine_dst or []):
        if not any(o['player'] == d['player'] for o in out):
            tm = team_key(d.get('team')) or '?'
            opps, vals, marks, lined = run_for(tm)
            if len(vals) >= 2:
                out.append({'player': d['player'], 'team': tm, 'mine': True,
                            'weeks': f'{weeks[0]}-{weeks[-1]}', 'opps': opps,
                            'faces': sum(vals) / len(vals), 'byes': opps.count('bye'),
                            'marks': marks, 'lined_weeks': lined, 'games': len(vals)})
    # A BYE INSIDE THE RUN IS A CLAIM THAT WEEK ANYWAY (doc 291). The average skips the bye, so a
    # defense with three soft games and a week off used to rank with four soft games -- and the
    # whole point of holding one is not having to claim. A run with no bye comes first.
    out.sort(key=lambda r: (r['byes'], r['faces']))
    return out[:10], ''


_MISMATCH = set()


def _line_mismatch(week, team, sched_opp, line_opp):
    """The schedule and the lines file name different opponents for one team-week. One of the two
    files is stale, and the page says so once rather than silently using either (section 3)."""
    key = (week, team)
    if key in _MISMATCH:
        return
    _MISMATCH.add(key)
    LOAD_PROBLEMS.append(f'week {week}: sched_2026.csv has {team} playing {sched_opp} and '
                         f'lines_2026.csv has {line_opp}, so that week is ranked on last season\'s '
                         f'average until one of the two files is refreshed')


BYE_LEAD_WEEKS = 5          # how far ahead a bye is still tradeable
BYE_WORTH_FIXING = 6.0      # points of lineup hole below which it is not worth a trade
LINEUP_SLOTS = (('QB', 1), ('RB', 2), ('WR', 2), ('TE', 1), ('D/ST', 1), ('K', 1))
FLEX_POS = ('RB', 'WR', 'TE')


def _best_nine(men):
    """Best legal lineup from a list of dicts with pos and ppg. FLEX last, as the rules have it."""
    pool = sorted([m for m in men if m.get('ppg') is not None],
                  key=lambda m: -m['ppg'])
    used, total = set(), 0.0
    for pos, cnt in LINEUP_SLOTS:
        taken = 0
        for i, m in enumerate(pool):
            if taken == cnt:
                break
            if i in used or m['pos'] != pos:
                continue
            used.add(i); total += m['ppg']; taken += 1
    for i, m in enumerate(pool):
        if i not in used and m['pos'] in FLEX_POS:
            total += m['ppg']
            break
    return total


def bye_plan(week, mine, board):
    """What each bye week ACTUALLY costs, and which trade would fix the worst one.
    This is finding 4.11 in season: a bye is priced at its measured lineup loss and constrains
    nothing on its own (doc 440 closed the "uncited" flag on it).

    Written because Matt proposed it -- "trading away a player who has a bye week later in the
    year before your player has a bye week" -- and because the raw points of the men who are off
    is the wrong number. Losing four starters at once is not four times losing one: the lineup
    cannot absorb it, so the hole is what the BEST LEGAL NINE loses, not what the men were worth.

    Returns (rows, headline, note). A missing projection or bye SAYS so; it is never silently
    treated as zero without the count being reported.
    """
    men, blind = [], []
    for pid, nm in mine.items():
        b = board.get(pid) or {}
        pos = str(b.get('pos', '')).upper().replace('DST', 'D/ST')
        try:
            bye = int(float(b.get('bye')))
        except (TypeError, ValueError):
            bye = None
        try:
            ppg = float(b.get('proj_leaguepts')) / 17.0   # per game: a season projection covers 17 (doc 291)
        except (TypeError, ValueError):
            ppg = None
        if ppg is None or bye is None:
            blind.append(nm)
        men.append(dict(name=nm, pos=pos, bye=bye, ppg=ppg))
    if not men:
        return [], None, 'the roster did not load, so the bye plan was not built'
    full = _best_nine(men)
    if full <= 0:
        return [], None, 'no projections on the roster, so the bye plan cannot be built'
    rows = []
    for wk in range(1, 15):
        off = [m for m in men if m['bye'] == wk]
        if not off:
            continue
        cost = full - _best_nine([m for m in men if m['bye'] != wk])
        rows.append({'week': wk, 'off': [m['name'] for m in off], 'cost': cost,
                     'past': week and wk < week})
    rows.sort(key=lambda r: -r['cost'])
    live = [r for r in rows if not r['past'] and r['cost'] >= BYE_WORTH_FIXING]
    headline = None
    if live and week:
        nxt = min(live, key=lambda r: r['week'])
        out = nxt['week'] - week
        if 0 <= out <= BYE_LEAD_WEEKS:
            # who can be sent: a man whose own bye is LATER and whose slot is doubled up
            counts = {}
            for m in men:
                counts[m['pos']] = counts.get(m['pos'], 0) + 1
            send = sorted([m for m in men
                           if m['bye'] and m['bye'] > nxt['week']
                           and counts.get(m['pos'], 0) >= 2 and m['ppg']],
                          key=lambda m: -m['ppg'])
            quiet = sorted(r['week'] for r in rows if r['cost'] < 1.0)
            # ONE HOLE IS NOT A TRADE (doc 291). The trade advice below was written for a week that
            # takes out several starters at once. When every man off is at ONE position that starts
            # one player -- two tight ends, two quarterbacks -- it is a single empty slot, and a
            # one-week pickup fills it. The first build of this section with the week read correctly
            # (offline, on the recorded 10 Sept pool; it had never rendered live because the week was
            # unknown) told him to shop Jalen Hurts and Puka Nacua to cover a tight-end bye.
            offpos = {m['pos'] for m in men if m['bye'] == nxt['week']}
            one_slot = (next(iter(offpos)) if len(offpos) == 1
                        and dict(LINEUP_SLOTS).get(next(iter(offpos))) == 1 else '')
            headline = {'week': nxt['week'], 'out': out, 'cost': nxt['cost'],
                        'off': nxt['off'], 'send': [m['name'] for m in send[:3]],
                        'quiet': quiet, 'one_slot': one_slot}
    note = ''
    if blind:
        note = ('%d of your men are not on our board, so their bye is counted at nothing and the '
                'holes below are UNDERSTATED: %s' % (len(blind), ', '.join(sorted(blind))))
    return rows, headline, note

def look_ahead(week, sched, t25, free_qb, free_dst, my_byes, lines=None):
    """The next few weeks: who is off, and the softest free QB and D/ST for each of them.

    WHICH AXIS (doc 441, finding 4.39). A week where EVERY scheduled game carries a pregame line is
    ranked on the line: a defense by the LOWEST opponent implied total, a quarterback by the HIGHEST
    own-team implied total. A week with no line, or only some of its games lined, is ranked on last
    season's averages as before, so one week is never ranked on two different numbers. Each week
    carries `axis` ('line' or 'last season'), the counts behind it, and `detail` (per team: the
    side, the opponent's implied total and the own total, blank where there is no line) for the
    page to print beside each name. The qb and dst tuples keep their four fields.
    """
    lines = lines or {}
    if not sched or (not t25 and not lines):
        return []
    out = []
    for wk in range(week, week + LOOK_WEEKS):
        wkmap = sched.get(wk)
        if not wkmap:
            continue
        def playing(team):
            return team_key(team) in wkmap

        def opp(team):
            return wkmap[team_key(team)][0]
        games = len(wkmap) // 2 if wkmap else 0
        lined_games = sum(1 for tm in wkmap if (wk, tm) in lines and lines[(wk, tm)][0] == wkmap[tm][0]) // 2
        on_line = bool(games) and lined_games == games
        if on_line:
            # a QB wants a HIGH own-team total; a D/ST wants a LOW opponent total
            qb = [(lines[(wk, team_key(q['team']))][1], q) for q in free_qb
                  if playing(q['team']) and (wk, team_key(q['team'])) in lines]
            ds = [(lines[(wk, team_key(d['team']))][2], d) for d in free_dst
                  if playing(d['team']) and (wk, team_key(d['team'])) in lines]
        else:
            # a QB wants a GENEROUS defense: high points allowed by the opponent
            qb = [(t25[opp(q['team'])][0], q) for q in free_qb
                  if playing(q['team']) and opp(q['team']) in t25]
            # a D/ST wants a WEAK offence: low points scored by the opponent
            ds = [(t25[opp(d['team'])][1], d) for d in free_dst
                  if playing(d['team']) and opp(d['team']) in t25]
        qb.sort(key=lambda x: -x[0])
        ds.sort(key=lambda x: x[0])
        detail = {}
        for _, p in qb[:3] + ds[:3]:
            tm = team_key(p['team'])
            ln = lines.get((wk, tm))
            detail[tm] = dict(side=wkmap[tm][1],
                              opp_total=(ln[2] if ln and ln[0] == wkmap[tm][0] else None),
                              own_total=(ln[1] if ln and ln[0] == wkmap[tm][0] else None))
        out.append(dict(week=wk, off=sorted(my_byes.get(wk, [])),
                        qb=[(v, q['player'], team_key(q['team']), opp(q['team'])) for v, q in qb[:3]],
                        dst=[(v, d['player'], team_key(d['team']), opp(d['team'])) for v, d in ds[:3]],
                        axis='line' if on_line else 'last season',
                        lined_games=lined_games, games=games, detail=detail))
    return out


BAD_STATUS = {'OUT', 'DOUBTFUL', 'QUESTIONABLE', 'INJURY_RESERVE', 'SUSPENSION', 'NOT_ACTIVE'}

# BAD_STATUS is "there is doubt about him", which is the TRIGGER for in_doubt().
# NOT_PLAYING is the narrower set: ESPN says he is not on the field. A man in this set cannot be
# the answer to "who inherits the job", because he is not there to inherit it (doc 296).
# DOUBTFUL and QUESTIONABLE stay OUT of it on purpose: a questionable back still plays most weeks,
# and a stash is a bet on the rest of the season, not on Sunday.
NOT_PLAYING = {'OUT', 'INJURY_RESERVE', 'SUSPENSION', 'NOT_ACTIVE'}


def in_doubt(roster_json, depth_rows, available, my_team_id, free_status=None):
    """SOMEBODY ELSE'S STARTER IS IN DOUBT AND HIS BACKUP IS FREE.

    Matt's lane, in his words: "others might be speculative when there is another manager's
    starter might be in doubt. this one week pickup may not work out but burns me almost
    nothing." The stash list ranks by what a job PAYS. This ranks by whether the job is
    ACTUALLY WOBBLING RIGHT NOW, which is the trigger rather than the prize.

    THE COST CAVEAT THAT BELONGS BESIDE EVERY ROW: as a FREE-AGENT add this is nearly free and
    his claim holds. As a WAIVER CLAIM it is not -- only the first claim that clears each week is
    made at your real priority, so a speculative claim ranked above a real target spends the one
    scarce thing you have.
    """
    owned = {}
    for t in roster_json.get('teams', []) or []:
        for e in (t.get('roster') or {}).get('entries', []):
            p = e.get('playerPoolEntry', {}).get('player', {}) or {}
            owned[str(p.get('id'))] = {'name': p.get('fullName', '?'),
                                       'status': (p.get('injuryStatus') or 'ACTIVE').upper(),
                                       'mine': t.get('id') == my_team_id}

    by_team = {}
    for r in depth_rows:
        by_team.setdefault(r['tm'], []).append(r)

    out = []
    for tm, rows in by_team.items():
        rows.sort(key=lambda x: (x['depth'], -x['vor']))
        hurt = [r for r in rows if r['espn_id'] in owned
                and owned[r['espn_id']]['status'] in BAD_STATUS]
        if not hurt:
            continue
        worst = min(hurt, key=lambda x: x['depth'])
        behind = [r for r in rows if r['depth'] > worst['depth'] and r['espn_id'] in available]
        # A cover who is himself OUT covers nothing (doc 296). Same fix as next_man_up().
        # [doc 445, finding 4.42] AND NEITHER DOES A DOUBTFUL ONE, THIS WEEK: on the final injury report of every
        # week 2021 to 2025, a Doubtful RB/WR/TE played 1 time in 231 (0.4%), an Out man 1 in 1,435.
        # This lane is a claim for THIS week, so Doubtful is Out here. next_man_up() keeps Doubtful on
        # purpose: it is a rest-of-season bet and a Doubtful man is back sooner (54% still out the
        # next week against 68% for Out). One word, two lanes, two horizons.
        behind = [r for r in behind
                  if (free_status or {}).get(r['espn_id'], 'ACTIVE') not in NOT_PLAYING | {'DOUBTFUL'}] or behind
        if not behind:
            continue
        pick = min(behind, key=lambda x: (x['depth'], -x['vor']))
        o = owned[worst['espn_id']]
        out.append(dict(player=pick['player'], tm=tm, ceil=pick['ceil'],
                        hurt=o['name'], status=o['status'].replace('_', ' ').title(),
                        mine=o['mine']))
    out.sort(key=lambda x: -x['ceil'])
    return out


def load_rz():
    """espn_id -> goal-line role last season, from Source\\redzone_te_2025.csv.

    WHY THIS EXISTS (doc 282). The tight-end block was sorted by PROJECTED POINTS, and on
    2026-09-09 that put Brenton Strange at the top -- a man this project had already retracted
    the day before, on its own measurement. Section 4.5 is the only tight-end signal ever found
    sticky here: inside-10 targets year to year r=+0.59, red-zone target volume r=+0.51, and
    red-zone touchdown RATE r=+0.02, noise. A projection is not that signal. So the page now
    carries the signal itself and ranks on it, because a sorted list's top row reads as a
    recommendation whatever the caption says.

    An ABSENT red-zone row is a measured ZERO -- the source lists only players with a red-zone
    target -- and the builder writes those as 0 rather than dropping them. A blank rate means
    fewer than four games, not no looks.
    """
    p = os.path.join(SRC, 'redzone_te_2025.csv')
    if not os.path.exists(p):
        return {}, 'Source\\redzone_te_2025.csv is missing, so the tight ends below are ranked on ' \
                   'projected points -- which is NOT the signal this project trusts at the position.'
    out = {}
    with open(p, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            def f(k):
                v = (r.get(k) or '').strip()
                try:
                    return float(v)
                except ValueError:
                    return None
            out[str(r['espn_id']).strip()] = dict(g=f('g25'), t20=f('in20'), t10=f('in10'),
                                                  td=f('rz_td'), pg20=f('in20_pg'), pg10=f('in10_pg'))
    if len(out) < 50:
        return {}, f'redzone_te_2025.csv holds only {len(out)} rows, which is not the whole position'
    return out, ''


# ESPN_TEAMS, TEAM_ALIAS and team_key() are imported from sheet_engine.py near the top of this file.
# SECTION 3: the map is ASSERTED against the 32, never defaulted -- a silent miss would print
# "no shape" on a real team and read as a fact about the team (doc 284, CTRL C).


def load_shape():
    """team -> how the offence shared the ball last season, from Source\\team_shape_2025.csv.

    WHY (doc 284). Matt, 2026-09-10: "a team with more common 2 WR sets may favor a WR3 who moves
    up to WR2 ... teams who favor 3 WR sets have more target distribution." Measured on 57 real
    promotions across four seasons, it runs the OTHER WAY: moving up the order is worth about twice
    as much on a team that spreads the ball as on a tight-end-heavy one, because on a heavy team
    there is less receiver pie to move into and the top man already holds most of what there is.
    So the shape belongs beside every free receiver, with a caption that says which way it cuts.
    """
    p = os.path.join(SRC, 'team_shape_2025.csv')
    if not os.path.exists(p):
        return {}, 'Source\\team_shape_2025.csv is missing, so no receiver below carries his ' \
                   "team's target distribution."
    out = {}
    with open(p, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            out[team_key(r['team'])] = dict(te=float(r['te_share']), rb=float(r['rb_share']),
                                            wr=float(r['wr_share']), fed=int(float(r['fed'])))
    # THE ASSERTION, and the first version of it did not fire: checking len()==32 passes happily
    # when an alias is wrong, because the unmapped spelling just becomes its own key.
    bad = sorted(set(out) - ESPN_TEAMS)
    if bad or len(out) != 32:
        return {}, ('team_shape_2025.csv resolved %d teams and %d unknown code(s) %s -- the name '
                    'map is wrong, so no receiver carries a shape' % (len(out), len(bad), bad))
    return out, ''


def shapemark(r, shape):
    """Plain English, no section numbers, no p-values (SECTION 0.1's scope rule)."""
    d = shape.get(team_key(r.get('team')))
    if not d:
        return '<span class="q">&mdash;</span>'
    if d['fed'] >= 4 and d['te'] < 0.22:
        tag = '<b>spreads it</b>'
    elif d['fed'] <= 2 and d['te'] >= 0.26:
        tag = 'heavy &mdash; few mouths'
    else:
        tag = 'middling'
    return (f"{tag} &middot; fed {d['fed']} &middot; tight end took "
            f"{100 * d['te']:.0f}%, backs {100 * d['rb']:.0f}%")


def goalline(r, rz):
    """The plain-English mark for one tight end. SECTION 0.1 scope rule: no section numbers."""
    z = rz.get(r['espn_id'])
    if z is None:
        return '<span class="q">no NFL weeks last season</span>'
    if z['pg10'] is None:
        return '<span class="q">under four games last season</span>'
    return (f"<b>{z['pg10']:.2f}</b> inside the ten a game &middot; "
            f"{z['pg20']:.2f} inside the twenty &middot; {int(z['td'] or 0)} red-zone scores")


def _table(rows, cols):
    o = ['<table class="w"><tr>' + ''.join(
        f'<th class="{c[2]}">{c[1]}</th>' for c in cols) + '</tr>']
    for r in rows:
        o.append('<tr>' + ''.join(
            f'<td class="{c[2]}">{c[0](r)}</td>' for c in cols) + '</tr>')
    return '\n'.join(o) + '</table>'


def _plays(opp, side, opp_total):
    """'at KC 27.5' or 'vs KC 27.5': the opponent, the side, and the books' expected score for that
    opponent where a line exists. No number where there is none; never a zero (doc 441)."""
    word = 'at' if side == 'away' else 'vs'
    return f'{word} {_esc(opp)}' + (f' <b>{opp_total:.1f}</b>' if opp_total is not None else '')


def _ranked_on(r):
    """The number a look-ahead row was ranked on, in the register the axis gives it: on the line a
    quarterback carries his own team's total and a defense its opponent's; on last season's
    averages a quarterback carries what the opponent allowed and a defense what it scored."""
    v = r['v']
    if r.get('axis') == 'line':
        return f'own team total <b>{v:.1f}</b>' if r['kind'] == 'QB' else f'opponent total <b>{v:.1f}</b>'
    return f'they allowed {v:.1f}/g' if r['kind'] == 'QB' else f'they scored {v:.1f}/g'


def _opened_note():
    """The teams next_man_up() set aside because the job is already open (doc 443): named under
    the stash table, so a man missing from it is explained and not merely absent."""
    op = getattr(next_man_up, 'opened', None) or []
    if not op:
        return ''
    return ('<div class="sub">Not a stash, the job is already open: '
            + '; '.join(f'{_esc(tm)} ({_esc(who)}, {_esc(st)})' for tm, who, st in op)
            + '. The backup there is a claim for THIS week and sits in the lane above.</div>')


def write_page(rows, stash, note='', missing=None, doubt=None, ahead=None, slate=None, slate_note='',
               runs=None, runs_note='', byerows=None, byehead=None, byenote='', roster=None,
               waiver_rank=None, waiver_n=0, waiver_ahead=None):
    rz, rznote = load_rz()
    shape, shapenote = load_shape()
    pool = ''
    for pos in ('RB', 'TE', 'WR', 'QB'):
        rs = [r for r in rows if r['pos'] == pos]
        cols = [(lambda r: _esc(r['player']), 'player', 'p'),
                (lambda r: _esc(r['team']), 'tm', 't'),
                (lambda r: f"{r['value']:.1f}", 'value', 'r'),
                (lambda r: _esc(str(r['bye']).replace('.0', '')), 'bye', 't'),
                (lambda r: r['flags'] or '<span class="q">nothing flagged</span>',
                 'what the sheet knows', 'n')]
        head = f'<h3>{pos}</h3>'
        if pos == 'WR':
            # A PROMOTION IS WORTH ABOUT TWICE AS MUCH ON A TEAM THAT SPREADS THE BALL (doc 284).
            # Not a sort key -- it is measured at the edge of what 57 promotions can detect, and
            # the receiver's own value still orders the list.
            if shape:
                cols.insert(4, (lambda r: shapemark(r, shape), "his team's target share", 'n'))
                head += ('<div class="sub">Last column: how his offence shared the ball last season. A move '
                         'up the order is worth about twice as much on a team that feeds four receivers as '
                         'on one that feeds two. Not a reason to prefer him today.</div>')
            else:
                head += f'<div class="bad"><b>{_esc(shapenote)}</b></div>'
        if pos == 'TE':
            # RANKED ON GOAL-LINE LOOKS, NOT ON THE PROJECTION (doc 282). The top row of a sorted
            # list reads as a recommendation, so the sort key has to be the signal.
            if rz:
                rs = sorted(rs, key=lambda r: -((rz.get(r['espn_id']) or {}).get('pg10') or -1))
                cols.insert(4, (lambda r: goalline(r, rz), 'goal-line looks last season', 'n'))
                head += ('<div class="sub">Ranked on targets inside the ten last season, per game, the one '
                         'tight-end number that carries year to year. A targeting list, not a projection.</div>')
            else:
                head += f'<div class="bad"><b>{_esc(rznote)}</b></div>'
        rs = rs[:8]
        if not rs:
            continue
        pool += head + _table(rs, cols)
    stab = _table(stash[:12], [
        (lambda r: _esc(r['player']), 'stash', 'p'),
        (lambda r: _esc(r['tm']), 'tm', 't'),
        (lambda r: _esc(r['ahead']), 'the man ahead', 'n'),
        (lambda r: f"<b>{r['ceil']:.0f}</b>", 'his job pays', 'r'),
        (lambda r: _esc(r['job']).lower()
                   + (f" &middot; ahead of him {_esc(r['over'])}, so he is not the one who "
                      f"inherits this week" if r.get('over') else ''), 'flag', 'n')])
    # doc 380: "Built by the scheduler" was printed on every run, including the ones Matt ran by
    # hand, and the bare time said nothing about the 03:11 settlement that had happened since the
    # last one. The stamp is now the READ time plus the run label ff.bat passes in FF_WHO, and the
    # browser writes a line under it when the page is opened (red once a settlement window passed).
    if _build_meta:
        try:
            _meta = _build_meta(src=SRC)          # doc 381: the next kickoff, off sched_2026.csv
        except TypeError:                         # an older sheet_engine without the src argument
            _meta = _build_meta()
        stamp, attrs, agel = _meta['text'], _meta['attrs'], (_age_line() if _age_line else '')
        lock_txt = _meta.get('lock_text') or ''
    else:
        stamp, attrs, agel = dt.datetime.now().strftime('%A %d %B, %H:%M') + ' (run label unknown)', '', ''
        lock_txt = ''
    banner = (f'<div class="bad"><b>{_esc(note)}</b></div>' if note else '')
    built_by = _esc(code_stamp(os.path.abspath(__file__)) + ' and ' +
                    code_stamp(os.path.join(HERE, 'sheet_engine.py')))
    doubt = doubt or []
    ahead = ahead or []
    body = (f'<div class="wrap">{page_bar(current="THE_WEEKLY_WIRE.html")}'
            f'<h1>The weekly wire</h1>'
            f'<div class="sub" id="inputs" {attrs}>Read from ESPN {stamp}. '
            + (f'Next kickoff on file: {lock_txt}; a claimed man locks with his game. ' if lock_txt else '')
            + f'The routine, the stash list and the pool, ranked on our value.</div>'
            f'{agel}'
            f'{banner}{STATIC_TOP}{drop_table(roster)}'
            + (('<h2>Coming up &mdash; plan these now, not in the week</h2>'
                 '<div class="sub">Buy the bye cover two or three weeks ahead, when nobody is bidding. '
                 '<b>Defense: take the schedule</b> (the matchup is worth more than the gap between the units). '
                 '<b>Quarterback: take the better man</b>, matchup only to split two you rate the same (about a point '
                 'a game against a four-point spread). <b>Backs and tight ends: the opponent&rsquo;s points allowed to '
                 'the position this season is a tiebreak within a point, never more.</b> Receivers: matchup is worth '
                 'zero week to week, except the playoff box below.</div>'
                 '<div class="sub"><b>Where the line is posted, the number beside a name is the line.</b> A defense is '
                 'ranked on its opponent&rsquo;s implied total, lowest first; a quarterback on his own team&rsquo;s '
                 'total, highest first, and when it disagrees with the soft-matchup rule take the total. A week with no '
                 'line yet says so and uses last season.</div>'
                 + ''.join(
                     f'<h3>Week {a["week"]}'
                     + (f' &mdash; <span style="color:#a33">off: '
                        f'{", ".join(_esc(x) for x in a["off"])}</span>' if a['off'] else '')
                     + '</h3>'
                     + ('<div class="sub">On the line: every game this week has one.</div>'
                        if a.get('axis') == 'line' else
                        f'<div class="sub">Last season&rsquo;s averages: '
                        + (f'{a.get("lined_games", 0)} of {a.get("games", 0)} games have a line so far, '
                           f'so the line is not used yet.' if a.get('lined_games') else
                           'no game this week has a line yet.') + '</div>')
                     + _table(
                         [dict(kind='QB', name=n, tm=t, opp=o, v=v, axis=a.get('axis'),
                               d=(a.get('detail') or {}).get(t) or {}) for v, n, t, o in a['qb']]
                         + [dict(kind='D/ST', name=n, tm=t, opp=o, v=v, axis=a.get('axis'),
                                 d=(a.get('detail') or {}).get(t) or {}) for v, n, t, o in a['dst']],
                         [(lambda r: _esc(r['kind']), '', 't'),
                          (lambda r: _esc(r['name']), 'free now', 'p'),
                          (lambda r: _esc(r['tm']), 'tm', 't'),
                          (lambda r: _plays(r['opp'], r['d'].get('side'), r['d'].get('opp_total')),
                           'plays', 'n'),
                          (lambda r: _ranked_on(r), 'ranked on', 'n')])
                     for a in ahead)) if ahead else '')

            + ((('<h2>The trade that is sitting there</h2>' if byehead and not byehead.get('one_slot')
                 else '<h2>Your bye weeks</h2>')
                + ((f'<div class="sub"><b>Week {byehead["week"]} is '
                    + ('THIS WEEK' if byehead['out'] == 0
                       else f'{byehead["out"]} week' + ('s' if byehead['out'] != 1 else '') + ' away')
                    + f': {", ".join(_esc(x) for x in byehead["off"])} '
                    + ('is off' if len(byehead['off']) == 1 else 'are off together')
                    + '.</b> That is '
                    f'one empty {_esc(byehead["one_slot"])} slot, and a one-week pickup fills it. '
                    'No trade is needed for a single hole.</div>')
                   if byehead and byehead.get('one_slot') else
                   (f'<div class="bad"><b>Week {byehead["week"]} is '
                   + ('THIS WEEK' if byehead['out'] == 0
                      else f'{byehead["out"]} week' + ('s' if byehead['out'] != 1 else '') + ' away')
                   + f' and it costs you about {byehead["cost"]:.0f} points of lineup &mdash; '
                   + ', '.join(_esc(x) for x in byehead['off'])
                   + ' are all off at once.</b></div>'
                   '<div class="sub">What your best legal nine loses that week; a waiver body will not fix it '
                   'and a trade can. <b>Send</b> a man whose bye falls later at a position you double up: '
                   + (', '.join('<b>' + _esc(x) + '</b>' for x in byehead['send'])
                      if byehead['send'] else 'nobody on your roster fits that shape right now')
                   + '. <b>Ask for</b> a comparable player whose bye lands in '
                   + (', '.join('week ' + str(w) for w in byehead['quiet'])
                      if byehead['quiet'] else 'a week that costs you nothing')
                   + '. Like for like, and never your best man at a position unless what comes back '
                   'starts in the same slot.</div>') if byehead else '')
                + _table(byerows, [
                    (lambda r: ('week ' + str(r['week'])) + (' <span class="q">(gone)</span>'
                                                             if r['past'] else ''), 'when', 't'),
                    (lambda r: ', '.join(_esc(x) for x in r['off']), 'who is off', 'n'),
                    (lambda r: f"{r['cost']:.0f}", 'costs you', 'r')])) if byerows else '')
            + (f'<div class="bad"><b>{_esc(byenote)}.</b></div>' if byenote else '')

            + (('<h2>The defense to HOLD &mdash; not the defense to start this week</h2>'
                '<div class="sub"><b>Take the free defense facing the lowest opponent implied total '
                'this week.</b> Measured over five seasons that is worth about three points a week '
                'over picking at random, and last season&rsquo;s averages are only used where no line '
                'exists yet.'
                + (f' The lines on file were read {_esc(LINES_ASOF)}.' if LINES_ASOF else
                   ' <b>No line is on file, so every number below is last season&rsquo;s average.</b>')
                + '</div>'
                '<div class="sub">Ranked by the whole run ahead, softest first: buy one defense early and keep it. '
                'A bye inside the run ranks below every run without one. A hard draw scores below zero more than a '
                'quarter of the time and an easy one 9%; chasing the best week is worth about a point, avoiding the '
                'worst is worth more. <b>Every defense claim spends the priority the running back needs</b>: four in '
                'ten of your claims the last two seasons were defenses, against three in all for the average manager.</div>'
                + _table(runs, [
                    (lambda r: _esc(r['player']) + (' <b>(yours)</b>' if r['mine'] else ''), 'defense', 'p'),
                    (lambda r: _esc(r['weeks']), 'weeks', 't'),
                    (lambda r: ' &middot; '.join(
                        ('<b>bye</b>' if m['opp'] == 'bye'
                         else _plays(m['opp'], m['side'], m['val'] if m['line'] else None))
                        for m in r['marks']) if r.get('marks') else
                     ' &middot; '.join('<b>bye</b>' if o == 'bye' else 'vs ' + _esc(o)
                                       for o in r['opps']), 'they play', 'n'),
                    (lambda r: (f"{r['lined_weeks']} of {r['games']}" if r.get('games') else '&mdash;'),
                     'weeks on the line', 't'),
                    (lambda r: f"{r['faces']:.1f}", 'opponents expected /g', 'r')])) if runs else '')
            + (f'<div class="bad"><b>The defense run is not on this sheet: '
               f'{_esc(runs_note)}.</b></div>' if runs_note else '')

            + (('<h2>The tight end&rsquo;s December draw</h2>'
                '<div class="sub">Weeks 15 to 17, the playoffs. The draw is worth about <b>+3 points a game at tight '
                'end</b> (about nine across the three weeks, best draw to worst) and nothing at any other position. '
                '<b>Use it only to split two tight ends you rate the same.</b></div>'
                + _table(slate, [
                    (lambda r: _esc(r['player']) + (' <b>(yours)</b>' if r['mine'] else ''), 'tight end', 'p'),
                    (lambda r: _esc(r['tm']), 'tm', 't'),
                    (lambda r: ' &middot; '.join('vs ' + _esc(o) for o in r['opps']), 'wk 15 / 16 / 17', 'n'),
                    (lambda r: f"{r['mean']:.1f}", 'they allowed /g', 'r')])) if slate else '')
            + (f'<div class="bad"><b>The tight end&rsquo;s December draw is not on this sheet: '
               f'{_esc(slate_note)}.</b></div>' if slate_note else '')
            + (('<h2>In doubt this week &mdash; take the shot</h2>'
                '<div class="sub">A rostered starter carries a status and the man behind him is free. <b>Add him '
                'outright if you can; as a claim, rank him below anything you actually want.</b> If nothing happens, '
                'drop him next week. <b>A starter out for weeks is not in doubt, he is gone: that job is open '
                'now, and THE CALL on the week sheet prices it beside everything else.</b></div>'
                + _table(doubt[:10], [
                    (lambda r: _esc(r['player']), 'add him', 'p'),
                    (lambda r: _esc(r['tm']), 'tm', 't'),
                    (lambda r: _esc(r['hurt']) + (' <b>(yours)</b>' if r['mine'] else ''),
                     'because this man is', 'n'),
                    (lambda r: '<b>' + _esc(r['status']) + '</b>'
                     + (' &middot; the job is open, see THE CALL'
                        if (r.get('status') or '').strip().upper().replace(' ', '_') in _GONE_FOR_WEEKS
                        else ''), 'status', 'n'),
                    (lambda r: f"{r['ceil']:.0f}", 'job pays', 'r')])) if doubt else '')
            + '<h2>One injury away &mdash; the stash list</h2>'
            f'<div class="sub">Ranked by what the job pays if it opens, not by what the man is worth today; '
            f'none of them starts for you this week.</div>{stab}{_opened_note()}'
            f'<h2>The pool right now</h2>'
            f'<div class="sub">Everyone not on a roster, ranked on points above a replacement starter; '
            f'negative is normal here, the order and the flags are what matter.</div>{pool}')
    if missing:
        shown = ', '.join(_esc(m) for m in missing[:30])
        more = f' &hellip; and {len(missing) - 30} more' if len(missing) > 30 else ''
        body += (f'<h2>Available, and not on our board at all</h2>'
                 f'<div class="bad"><b>{len(missing)} skill players are on the wire that our '
                 f'ranking has never rated, so they are missing from every table above.</b> '
                 f'Kickers and defenses are skipped on purpose and are not counted here. '
                 f'Check these by eye:<br><br>{shown}{more}</div>')
    # doc 311: the real number, or an honest silence. NEVER the old hard-coded "near the back".
    if waiver_rank and waiver_n:
        _wa = waiver_ahead or []
        if _wa:
            _wl = (f' <b>This week you are {waiver_rank} of {waiver_n}, and the '
                   f'{len(_wa)} team{"s" if len(_wa) != 1 else ""} who pick before you '
                   f'{"are" if len(_wa) != 1 else "is"} {_esc(", ".join(_wa))}.</b>')
        else:
            _wl = f' <b>This week you are first of {waiver_n}. Nobody picks before you.</b>'
    else:
        _wl = (' <b>Your position in the order could not be read from ESPN this run, so this page '
               'is not guessing at it.</b>')
    body += STATIC_BOTTOM.replace('{WAIVER_LINE}', _wl) + f'<div class="sub" style="margin-top:24px">Built by {built_by}.</div></div>'
    out = os.path.join(SRC, 'THE_WEEKLY_WIRE.html')
    tmp = out + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        fh.write("<!doctype html><html><head><meta charset='utf-8'><title>The weekly wire</title>"
                 "<style>" + CSS + "\n.bad{background:#fdeceb;border:1px solid #e0b4b0;color:#8a2a22;"
                 "border-radius:8px;padding:12px 16px;margin:0 0 18px;font-size:14px}"
                 "\n@media print{p.jump.pagebar{display:none}}" + PAGEBAR_CSS + "</style></head>"
                 "<body>" + body + "</body></html>")
    os.replace(tmp, out)                      # never leave a half-written page on the desk
    return out


def fail_page(msg):
    """SECTION 0.2 -- a step that cannot do its job must SAY SO on the artifact, not exit quietly."""
    try:
        write_page([], [], note=msg)
    except Exception:
        pass
    print('\n  ' + msg + '\n')
    return 2


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--all', action='store_true', help='print every priceable free agent')
    ap.add_argument('--html', action='store_true',
                    help='also write THE_WEEKLY_WIRE.html (the week sheet is written anyway)')
    ap.add_argument('--no-sheet', action='store_true', dest='no_sheet',
                    help='skip WEEK_SHEET.html, which is otherwise always rebuilt')
    ap.add_argument('--check', action='store_true', help='test the cookies and stop')
    a = ap.parse_args(argv)

    if a.check:
        _get('mTeam')
        print("  cookies OK -- ESPN answered for league %d, season %d." % (LEAGUE_ID, SEASON))
        return 0

    try:
        board, ctx = load_local()
    except SystemExit as e:
        return fail_page(str(e).strip()) if a.html else 2

    fetch_schedule()

    # --- the pool ESPN says is gettable -----------------------------------------------------
    xf = {"players": {"filterStatus": {"value": ["FREEAGENT", "WAIVERS"]},
                      "limit": 400, "offset": 0,
                      "sortPercOwned": {"sortAsc": False, "sortPriority": 1}}}
    try:
        data = _get('kona_player_info', xf)
    except SystemExit:
        m = ("COOKIES EXPIRED -- ESPN refused this run, so the tables below are NOT current. "
             "Run  py set_cookies.py  then  py wire.py --html .")
        return fail_page(m) if a.html else 2
    except Exception as exc:
        m = f"COULD NOT REACH ESPN ({type(exc).__name__}). The tables below are NOT current."
        return fail_page(m) if a.html else 2

    availability = {}
    pool = data.get('players') or []
    if not pool:
        m = ("ESPN RETURNED AN EMPTY LIST. That is not a result -- do not read anything into it. "
             "Nothing below is current.")
        return fail_page(m) if a.html else 2

    # --- THE WAIVER ORDER, READ FROM ESPN RATHER THAN ASSERTED (doc 311) --------------------
    # The page has been saying "you are near the back of the line" as a HARD-CODED STRING since
    # it was written. Priority resets every week to inverse standings (section 2), so a fixed
    # sentence is wrong most weeks by construction, and it is the one number 4.32 term 4 needs:
    # you cannot count the teams AHEAD of him without knowing where he stands. Doc 254 logged it
    # [OPEN] on 9 Sept and nothing read it.
    # It is FETCHED, never assumed: if ESPN does not serve the field, the page says the order is
    # unknown rather than printing a number or repeating the old sentence (0.2).
    waiver_order, my_waiver_rank, ahead_of_me = [], None, []
    MY_TEAM_NAME_FROM_MTEAM, _abbrev_by_id = [], {}
    try:
        _teams = _get('mTeam')
        for t in (_teams.get('teams') or []):
            wr = t.get('waiverRank')
            if wr is None:
                continue
            nm = (t.get('abbrev') or t.get('name')
                  or ' '.join(x for x in (t.get('location'), t.get('nickname')) if x) or '?')
            waiver_order.append((int(wr), str(nm).strip(), t.get('id')))
            _abbrev_by_id[t.get('id')] = str(nm).strip()
            # THE MASTHEAD NAME LIVES IN THIS VIEW, NOT IN mRoster (doc 316). The code below
            # reads it off mRoster and a comment there claims the page follows his ESPN team
            # name -- it does not, because ESPN serves teams WITHOUT name/location/nickname in
            # the roster view, so the lookup silently returned '' and the header fell back to
            # "Your team" for a week. Same defect shape as 3's silent-skip rule: a missing field
            # that reads as a legitimate blank. FULL name here, not the abbreviation.
            if t.get('id') == MY_TEAM_ID:
                _full = (t.get('name')
                         or ' '.join(x for x in (t.get('location'), t.get('nickname')) if x)
                         or '').strip()
                if _full:
                    MY_TEAM_NAME_FROM_MTEAM.append(_full)
        waiver_order.sort()
        for wr, nm, tid in waiver_order:
            if tid == MY_TEAM_ID:
                my_waiver_rank = wr
            elif my_waiver_rank is None:
                ahead_of_me.append(nm)
        # [30 Sept, doc 456] the standings, off the same read
        try:
            _st = write_standings(_teams.get('teams') or [], os.path.join(SRC, 'standings_2026.csv'), MY_TEAM_ID)
            _me = next((r for r in _st if r['mine']), None)
            if _me:
                print(f"  standings: you are {_me['wins']}-{_me['losses']}"
                      + (f"-{_me['ties']}" if str(_me['ties']) not in ('', '0') else '')
                      + f", seed {_me['playoff_seed']} of {len(_st)}, {_me['points_for']} points for"
                      + f" (standings_2026.csv, {len(_st)} teams)")
            else:
                LOAD_PROBLEMS.append('standings_2026.csv was written but none of its rows is yours')
        except Exception as exc:
            LOAD_PROBLEMS.append(f'standings_2026.csv NOT written ({type(exc).__name__}: {exc})')
        # [1 Oct, doc 464] the league schedule, one more read, for the playoff-odds simulation (doc 463)
        try:
            _sch = write_schedule(_get('mMatchupScore'), os.path.join(SRC, 'schedule_2026.csv'), _abbrev_by_id)
            _played = sum(1 for r in _sch if r['home_pts'] not in ('', 0, 0.0, None) or r['away_pts'] not in ('', 0, 0.0, None))
            print(f"  schedule: {len(_sch)} matchups written to schedule_2026.csv ({_played} with a score)")
            if not _sch:
                LOAD_PROBLEMS.append('schedule_2026.csv was written with no matchups: ESPN served an empty schedule')
        except Exception as exc:
            LOAD_PROBLEMS.append(f'schedule_2026.csv NOT written ({type(exc).__name__}: {exc})')
        if not waiver_order:
            LOAD_PROBLEMS.append('ESPN served no waiverRank on any team, so the waiver order is '
                                 'UNKNOWN this week and the page does not guess at it')
        elif my_waiver_rank is None:
            LOAD_PROBLEMS.append(f'the waiver order came back for {len(waiver_order)} teams but '
                                 f'none of them is team {MY_TEAM_ID}, so your own position is '
                                 f'UNKNOWN')
        else:
            print(f"  waiver order: you are {my_waiver_rank} of {len(waiver_order)}"
                  + (f"; ahead of you: {', '.join(ahead_of_me)}" if ahead_of_me
                     else "; nobody is ahead of you"))
    except Exception as exc:
        LOAD_PROBLEMS.append(f'the waiver order could not be read ({type(exc).__name__}), so this '
                             f'page says nothing about who picks before you')

    # --- my roster, so the sheet can name what a claim would cost ---------------------------
    mine, rosters, mine_meta, my_team_name = {}, {}, {}, ''
    # doc 390: the slot and the status, so a file can answer "who is on IR and how many seats are free".
    # Both were in this payload all along and neither reached the drive; the count in doc 388 was
    # wrong because of it. `lineupSlotId` is ESPN's slot (bench and IR have their own ids, and the
    # first run after this ships is what confirms which id IR is on this league).
    mine_slot = {}
    try:
        rosters = _get('mRoster')
        for t in rosters.get('teams', []):
            if t.get('id') == MY_TEAM_ID:
                # Matt asked whether the sheet's masthead follows his ESPN team name. It does now:
                # ESPN serves it here, so renaming the team renames the page on the next run.
                # mRoster does NOT carry the team name (doc 316) -- this line returned ''
                # every run. mTeam does, and it is read above; this stays only as a fallback.
                my_team_name = (t.get('name') or ' '.join(
                    x for x in (t.get('location'), t.get('nickname')) if x) or '').strip()
                for e in (t.get('roster') or {}).get('entries', []):
                    p = e.get('playerPoolEntry', {}).get('player', {}) or {}
                    mine[str(p.get('id'))] = p.get('fullName', '?')
                    mine_meta[str(p.get('id'))] = (POS.get(p.get('defaultPositionId'), '?'),
                                                   PRO.get(p.get('proTeamId'), '?'))
                    mine_slot[str(p.get('id'))] = (e.get('lineupSlotId'),
                                                   (p.get('injuryStatus') or 'ACTIVE').upper())
    except Exception as exc:
        print(f"  (could not read your roster: {type(exc).__name__}; sheet still built)")

    # ---- FIX 3 (doc 316): the other eleven rosters are FETCHED EVERY RUN AND THROWN AWAY.
    # Matt asked "does anyone else appear to need a TE?" and the only answer available was a
    # bye-week table, because `rosters` above holds all twelve teams and the loop keeps one.
    # 254 called the rival rosters the blocker on a whole lane; they were never blocked, they
    # were discarded. Written out so the question is a lookup from the next run on.
    # NOTE (doc 314) what this does NOT license: positional need does not predict who files on
    # a man. This is for reading the room, not for ordering a claim list.
    try:
        _lr = []
        for t in (rosters.get('teams') or []):
            _tid = t.get('id')
            for e in (t.get('roster') or {}).get('entries', []):
                _p = e.get('playerPoolEntry', {}).get('player', {}) or {}
                _lr.append({'team_id': _tid,
                            'team': _abbrev_by_id.get(_tid, ''),
                            'espn_id': str(_p.get('id')),
                            'player': _p.get('fullName', '?'),
                            'pos': POS.get(_p.get('defaultPositionId'), '?'),
                            'nfl': PRO.get(_p.get('proTeamId'), '?'),
                            'status': (_p.get('injuryStatus') or 'ACTIVE').upper()})
        if len(_lr) < 100:
            LOAD_PROBLEMS.append(f'the league roster dump came back with only {len(_lr)} players '
                                 f'across {len(rosters.get("teams") or [])} teams, which is too '
                                 f'few to be twelve real rosters -- not written')
        else:
            _lrp = os.path.join(SRC, 'LEAGUE_ROSTERS.csv')
            with open(_lrp, 'w', newline='', encoding='utf-8') as fh:
                _w = csv.DictWriter(fh, fieldnames=list(_lr[0].keys()), lineterminator='\n')
                _w.writeheader(); _w.writerows(_lr)
            _byteam = collections.Counter(r['team_id'] for r in _lr)
            _te = collections.Counter(r['team_id'] for r in _lr if r['pos'] == 'TE')
            print(f"  LEAGUE_ROSTERS.csv: {len(_lr)} players across {len(_byteam)} teams "
                  f"({sum(1 for t in _byteam if _te[t] <= 1)} of them carrying one tight end or none)")
    except Exception as exc:
        LOAD_PROBLEMS.append(f'the league rosters could not be written ({type(exc).__name__})')

    if not my_team_name and MY_TEAM_NAME_FROM_MTEAM:
        my_team_name = MY_TEAM_NAME_FROM_MTEAM[0]
    if not my_team_name:
        LOAD_PROBLEMS.append('ESPN served no team name in either view, so the sheet says '
                             '"Your team" rather than guessing one')
    else:
        print(f"  team name: {my_team_name}")

    # doc 395, Matt 23 Sept: "the plus/minus column is what i wanted you to note in terms of
    # likeliness i'll get a waiver pickup", and the reason it matters HERE is the Thursday run:
    # most ESPN leagues clear Tuesday night, so by the time his claims process he is reading the
    # RESULT of everyone else's waiver run rather than a forecast. ESPN has carried this all along
    # in the same `ownership` object we already read for percentOwned, and every run threw it away.
    # Confirmed live on the public endpoint 23 Sept: ownership = {percentOwned, percentChange,
    # percentStarted, date, activityLevel, auctionValue*, averageDraftPosition*}.
    # NEVER DEFAULTED TO ZERO (section 3): a missing field writes blank, because 0.0 and "ESPN did
    # not say" are different answers and owned_pct already learned that the hard way (doc 292).
    def _own(pl, key, nd=1):
        v = (pl.get('ownership') or {}).get(key)
        try:
            return round(float(v), nd)
        except (TypeError, ValueError):
            return ''

    def _own_asof(pl):
        v = (pl.get('ownership') or {}).get('date')
        try:
            return dt.datetime.fromtimestamp(float(v) / 1000.0).strftime('%Y-%m-%d %H:%M')
        except (TypeError, ValueError, OSError, OverflowError):
            return ''

    def _clears(en):
        # ESPN puts the waiver clear time on the POOL ENTRY, not the player. This is the real
        # answer to the D+2 arithmetic in section 2: read it rather than derive it. Blank when
        # ESPN does not serve it (a free agent has nothing to clear).
        v = en.get('waiverProcessDate')
        try:
            return dt.datetime.fromtimestamp(float(v) / 1000.0).strftime('%Y-%m-%d %H:%M')
        except (TypeError, ValueError, OSError, OverflowError):
            return ''

    avail, rows, unpriced, unpriced_kdst, status = set(), [], [], 0, {}
    offboard = []               # the same free skill players as `unpriced`, as rows (doc 292)
    moved_rows = []             # board team != live team: named below, never silent (doc 307)
    for entry in pool:
        p = entry.get('player') or {}
        pid = str(p.get('id'))
        avail.add(pid)
        status[pid] = (p.get('injuryStatus') or 'ACTIVE').upper()
        # ADD OR CLAIM, AND WE HAD IT ALL ALONG (doc 330). The pull above already asks ESPN for
        # BOTH ["FREEAGENT", "WAIVERS"] and ESPN says which each man is, on the pool entry rather
        # than on the player. The wire read injuryStatus off `player` and threw the availability
        # away, so every row said "check the button" when the answer was in the payload.
        # NEVER DEFAULTED (section 3): an unknown stays unknown and the page says so.
        _av = str(entry.get('status') or '').strip().upper()
        if not _av and entry.get('onTeamId') in (0, '0', None):
            _av = ''                          # absent is absent; do not infer FREEAGENT from it
        availability[pid] = _av
        b = board.get(pid)
        if not b:
            # A kicker or a defense missing from the board is expected and uninteresting.
            # A skill player missing from it is a HOLE IN THE SHEET and has to be named.
            if POS.get(p.get('defaultPositionId')) in ('K', 'D/ST'):
                unpriced_kdst += 1
            else:
                unpriced.append(f"{p.get('fullName', pid)} "
                                f"({POS.get(p.get('defaultPositionId'), '?')})")
                offboard.append({'espn_id': pid, 'player': p.get('fullName', ''),
                                 'pos': POS.get(p.get('defaultPositionId'), '?'),
                                 'team': team_key(PRO.get(p.get('proTeamId'))) or 'FA',
                                 'owned_pct': round(float((p.get('ownership') or {}).get('percentOwned') or 0.0), 1),
                                 'own_chg': _own(p, 'percentChange', 2),   # doc 395: a surging man
                                 'own_start': _own(p, 'percentStarted', 1),  # the board never rated
                                 'own_asof': _own_asof(p),
                                 'clears': _clears(entry),
                                 'status': (p.get('injuryStatus') or 'ACTIVE').upper(),
                                 'avail': availability.get(pid, '')})
            continue
        # THE TEAM COMES FROM THE LIVE PULL, NEVER FROM THE FROZEN BOARD (doc 307). The off-board
        # branch eight lines up has always used proTeamId; this branch used the board's team_c,
        # and nothing compared them. Six rows on WIRE_20260914.csv carried a stale team and two of
        # those carried a job number from the wrong backfield. The board is still the fallback,
        # for a player ESPN serves with no pro team (proTeamId 0 is a free agent).
        live_tm = team_key(PRO.get(p.get('proTeamId')) or '')
        board_tm = team_key(b.get('team_c', ''))
        moved_to = live_tm if (live_tm and board_tm and live_tm != board_tm) else ''
        # AND THE BYE MOVES WITH HIM. It came from the board beside the team, so the first version
        # of this fix corrected seven teams and left all seven byes pointing at the old club.
        bye = b.get('bye', '')
        if moved_to:
            nb = load_byes().get(live_tm)
            if nb is None:
                LOAD_PROBLEMS.append(f"{b.get('player') or pid} moved to {live_tm} and "
                                     f"byes_2026.csv has no bye for that team")
            else:
                bye = float(nb)
            moved_rows.append((b.get('player') or p.get('fullName', ''), board_tm, live_tm,
                               b.get('bye', ''), bye))
        rows.append({
            'espn_id': pid,
            'player': b.get('player') or p.get('fullName', ''),
            'pos': b.get('pos') or POS.get(p.get('defaultPositionId'), '?'),
            'team': live_tm or board_tm,
            'bye': bye,
            'value': b['_vor'],
            'owned_pct': round(float((p.get('ownership') or {}).get('percentOwned') or 0.0), 1),   # None crashed the run (doc 292)
            'own_chg': _own(p, 'percentChange', 2),      # doc 395: ESPN's +/- column, the demand signal
            'own_start': _own(p, 'percentStarted', 1),   # rostered is not started
            'own_asof': _own_asof(p),                    # when ESPN last refreshed those two
            'clears': _clears(entry),                    # ESPN's own waiver clear time, not our D+2
            'avail': availability.get(pid, ''),
            'flags': flags(ctx.get(pid), moved_to),
        })
    rows.sort(key=lambda r: -r['value'])

    # --- ADD OR CLAIM, ON THE ROW, IN THE WORDS THE BUTTON USES (doc 330) ----------------------
    # Section 0.1's scope rule: the CSV keeps ESPN's raw token, the PAGE gets the instruction.
    # It goes at the FRONT of the flag string because it is the first thing that decides what he
    # does with the row, and because "costs a claim" changes the ORDER of the list (section 4.32).
    _seen_av = sum(1 for r in rows if r.get('avail'))
    if not _seen_av:
        LOAD_PROBLEMS.append('ESPN served no availability on any player, so no row can say '
                             'whether it is an Add or a Claim. Every row below is one or the '
                             'other and the page does not know which.')
    else:
        _AVWORD = {'FREEAGENT': 'ADD, costs no priority',
                   'WAIVERS':   'CLAIM, costs your priority'}
        for r in rows:
            w = _AVWORD.get(r.get('avail', ''))
            if w:
                r['flags'] = (w + ' · ' + r['flags']) if r['flags'] else w
        _fa = sum(1 for r in rows if r.get('avail') == 'FREEAGENT')
        _wv = sum(1 for r in rows if r.get('avail') == 'WAIVERS')
        _un = len(rows) - _fa - _wv
        print(f"  availability: {_fa} free agents (Add), {_wv} on waivers (Claim), {_un} unknown")

    # SAY IT OUT LOUD. A silent correction is how the stale team survived four wire builds.
    if moved_rows:
        print(f"  team changed since the board, job flag dropped on {len(moved_rows)}:")
        for nm, was, now, oldbye, newbye in sorted(moved_rows, key=lambda x: x[0]):
            ob = str(oldbye).split('.')[0] or '?'
            nb = str(newbye).split('.')[0] or '?'
            bit = f"  bye {ob} -> {nb}" if ob != nb else f"  bye {nb}"
            print(f"    {nm:<24} {was} -> {now}{bit}")

    # --- the POTENTIAL screens, attached to the rows they belong to -----------------------------
    ped, ped_note = load_pedigree()
    ped_all = load_pedigree_all()                 # doc 453: round and year for the unscreened too
    # The pedigree ROW is held in a side map, never on `r` -- the CSV writer below takes
    # fieldnames from rows[0].keys(), so anything hung on a row becomes a column. The first
    # version put the whole dict on r['ped'] and WIRE_20260910.csv shipped a python repr in it.
    pedrow = {}
    for r in rows:
        p2 = ped.get(r['espn_id'])
        r['screen'] = p2['screen'] if p2 else ''
        if p2:
            pedrow[r['espn_id']] = p2
        if r['screen']:
            r['flags'] = (r['flags'] + ' · ' if r['flags'] else '') + r['screen']
    # --- the WEEK-1 WORKLOAD screen (doc 308) ---------------------------------------------------
    # Every key set here becomes a CSV column (rows[0].keys()), so it is set on EVERY row with a
    # default, never only on the ones that matched.
    form, form_note, form_weeks = load_form()
    if form_note:
        LOAD_PROBLEMS.append(form_note)
    formrow, matched, unmatched = {}, 0, []
    for r in rows:
        r['snap_pct'] = r['w1_targets'] = r['tgt_share'] = ''
        r['adot'] = r['ay_share'] = r['wopr'] = ''       # doc 435: air yards, finally read
        r['xfp'] = r['fp_oe'] = r['xfp_g'] = ''          # doc 437: expected points, our scoring
        r['act2'] = r['xfp2'] = ''                       # doc 438: his last two games, actual and expected
        r['touches'] = r['last_game_week'] = ''
        r['form_sig'] = ''
        fr = form.get((norm_name(r.get('player')), (r.get('pos') or '').upper(),
                       team_key(r.get('team'))))
        if fr is None:
            fr = _form_variant(form, r.get('player'), (r.get('pos') or '').upper(),
                               team_key(r.get('team')))
        if fr is None:
            if r.get('pos') in ('WR', 'TE', 'RB'):
                unmatched.append(r.get('player') or r['espn_id'])
            continue
        matched += 1
        formrow[r['espn_id']] = fr
        r['snap_pct'] = fr.get('snap_pct', '')
        r['w1_targets'] = fr.get('targets', '')
        r['tgt_share'] = fr.get('tgt_share', '')
        # doc 435 / 4.35: air yards per target and the team share, from build_form.py's new
        # columns. Blank on a form file built before 29 Sept, never zero.
        r['adot'] = fr.get('adot', '')
        r['ay_share'] = fr.get('ay_share', '')
        r['wopr'] = fr.get('wopr', '')
        # doc 437: expected points under our scoring (ffopportunity), summed over the games
        # the model has processed (xfp_g), and points over expected on the same games.
        r['xfp'] = fr.get('xfp', '')
        r['fp_oe'] = fr.get('fp_oe', '')
        r['xfp_g'] = fr.get('xfp_g', '')
        # doc 438, finding 4.37: the LAST TWO completed games, actual beside expected. Measured 2021-2025 on
        # 9,999 claimable RB/WR/TE weeks: the two-game EXPECTED predicts the next four weeks
        # better than the two-game actual at every position (rho .50 against .42, five seasons
        # of five), and given the expected, points over it carry almost nothing (+0.08 a point).
        # Two fixed cells are flagged, and NEITHER enters the workload count: as a fourth signal
        # xfp moved the screen's spike rate by +0.1 points, so it stays a display column.
        #   box-score mirage  8+ actual on under 5 expected: n=101, startable next four 12%,
        #                     spike 3%, against 17% and 4.3% for the pool. WORSE than the pool.
        #   quiet volume      8+ expected on under 5 actual: n=172, startable next four 28%,
        #                     7.2 a game next four against 5.5. BETTER than the pool on half the points.
        r['act2'] = fr.get('act2', '')
        r['xfp2'] = fr.get('xfp2', '')
        if r.get('pos') in ('RB', 'WR', 'TE'):
            try:
                a2, x2 = float(r['act2']), float(r['xfp2'])
            except (TypeError, ValueError):
                a2 = x2 = None                       # blank stays blank: no model row is not zero
            if a2 is not None:
                tag = ''
                if a2 >= 8 and x2 < 5:
                    tag = f'box-score mirage ({a2:.1f} on {x2:.1f} expected, last two games)'
                elif x2 >= 8 and a2 < 5:
                    tag = f'quiet volume ({a2:.1f} on {x2:.1f} expected, last two games)'
                if tag:
                    r['flags'] = (r['flags'] + ' · ' if r['flags'] else '') + tag
        # doc 314: targets + carries in his LAST COMPLETED GAME is the one number that predicts
        # how many rivals file on him (r=+0.296, p=0.00005, n=403 RB/WR/TE player-weeks 2022-2025).
        # NOT the season total -- fr is the cumulative row and reading touches off it would price a
        # man on six weeks of work when the measured thing is one. It is set for EVERY position,
        # not just the WR/TE composite below, because the decision it serves -- which man goes
        # FIRST on the claim list -- applies to the whole list.
        lg = fr.get('_last')
        r['touches'] = (lg or {}).get('touches', '')
        r['last_game_week'] = (lg or {}).get('week', '')
        if r.get('pos') not in ('WR', 'TE'):       # the measured population, and only it
            continue
        n, why, _gaps = form_signals(fr)
        r['form_sig'] = n
        if n >= 2:
            tag = f'workload {n} of 3'
            r['flags'] = (r['flags'] + ' · ' if r['flags'] else '') + tag + (f' ({why})' if why else '')
        # [doc 453, finding 4.43] THE YOUNG-RECEIVER SCREEN, READ ON THIS SEASON. The preseason screen
        # (4.30) reads LAST season's yards per target and targets a game, which a rookie does not have,
        # so Chris Bell (round 3, 9.2 a target, 3.3 a game through week 3) carried no screen at all and
        # the sheet had no ticket for him. Measured 2021 to 2025 on weeks 1 to 3 predicting weeks 4 to
        # 14 (young receivers, drafted 2021 on, not startable the season before, n=174): 3 of 3 became
        # startable 43.6% against 0 to 20% below; among those still under the bar through week 3, 26.7%
        # (4 of 15) against 5.6%. Same three marks as 4.30, this season's numbers, and the man's
        # own count of games and targets printed beside it because three games is the thinnest input
        # on the page. Only where the preseason screen is blank: one screen per man.
        if r.get('pos') == 'WR' and not r.get('screen'):
            _lab, _why = inseason_screen(fr, ped_all.get(str(r['espn_id'])))
            if _lab:
                r['screen'] = _lab
                r['flags'] = (r['flags'] + ' · ' if r['flags'] else '') + _why
    if form and not matched:
        LOAD_PROBLEMS.append('form_2026.csv loaded but matched NOTHING on the wire -- the name or '
                             'team spelling disagrees, so the workload screen is silently off')
    elif unmatched and form:
        # A man with no week-1 line did not play. That is a FACT about him, not a broken join, so
        # it is reported as a count and only named when it is implausibly large.
        if len(unmatched) > 0.6 * sum(1 for r in rows if r.get('pos') in ('WR', 'TE', 'RB')):
            LOAD_PROBLEMS.append(f'{len(unmatched)} of the free RB/WR/TE rows have no week-1 '
                                 f'workload line, which is too many to be men who did not play')

    for r in rows:
        r['status'] = status.get(r['espn_id'], 'ACTIVE')      # last column: ESPN's own player card
    RANKORDER = {'first-round rookie': 0, 'pedigree screen 3 of 3': 1}
    # doc 453: the in-season screen's label carries the game count, so it ranks by prefix, and its
    # pedigree row is in ped_all (pedrow holds only the preseason-screened men)
    def _rank(r):
        lab = r['screen']
        order = RANKORDER.get(lab, 2 if lab.startswith('in-season screen') else 9)
        pr = pedrow.get(r['espn_id']) or ped_all.get(str(r['espn_id'])) or {}
        try:
            pick = int(float(pr.get('nfl_pick') or 999))
        except (TypeError, ValueError):
            pick = 999
        return (order, pick)
    potential = sorted((r for r in rows if r['screen']), key=_rank)

    # THE WEEK (doc 291). The free-agent view carries no scoringPeriodId, so this read 0 on every
    # run and three sections -- the look-ahead, the defense run and the bye trade -- never built.
    # The roster view carries it; lineup.py has read it from there since week 1.
    # [doc 448] READ HERE, BEFORE LANE 2. It sat below the lane and log_status_pairs() (doc 445) read
    # it first: UnboundLocalError on the 29 Sept 20:06 run, wire 1, no wire page and no week sheet.
    # The unit test called the function directly and never ran main(), which is 0.2's rule broken
    # in the plainest way. `py check_locals.py` (in ff.bat after the kit check) now reads every function's
    # order statically and fires on exactly this shape; it fired on the shipped file and is quiet on this one.
    week = data.get('scoringPeriodId') or (rosters or {}).get('scoringPeriodId') or 0
    # --- lane 2: one injury away, and still unrostered ---------------------------------------
    depth = load_depth(form, form_weeks)
    _all_status = dict(status)
    _all_status.update(league_status(rosters))          # doc 443: the man ahead is owned
    log_status_pairs(depth, _all_status, week)          # doc 445: ESPN's status beside the report's, daily
    stash = next_man_up(depth, avail, status, holder_status=_all_status)
    doubt = in_doubt(rosters, depth, avail, MY_TEAM_ID, status) if rosters else []
    # doc 451: a starter out for weeks is not in doubt, he is gone, and that job is open now. The
    # week sheet prices those rows on THE CALL (sheet_engine, open_jobs); the lane below keeps them
    # too, marked. One predicate, sheet_engine.GONE_FOR_WEEKS, on both pages (doc 424).
    open_jobs = [d for d in doubt
                 if (d.get('status') or '').strip().upper().replace(' ', '_') in _GONE_FOR_WEEKS]

    # --- weeks ahead: the bye fill you have to buy early --------------------------------------
    sched, t25 = load_sched(), load_team25()
    lines = load_lines()                    # doc 441 / 442: the pregame lines, Source\lines_2026.csv
    # Rank by MATCHUP only among quarterbacks who could plausibly start. Without this the
    # list fills with third-stringers whose team happens to draw a soft defense.
    free_qb = [r for r in rows if r['pos'] == 'QB'][:12]
    free_dst = []
    for entry in pool:                       # D/ST are not on the board by design, so read the pool
        p = entry.get('player') or {}
        if POS.get(p.get('defaultPositionId')) == 'D/ST':
            free_dst.append({'player': p.get('fullName', '?'),
                             'team': PRO.get(p.get('proTeamId'), '?')})
    my_byes = {}
    for pid, nm in mine.items():
        b = board.get(pid)
        if not b:
            continue
        try:
            my_byes.setdefault(int(float(b['bye'])), []).append(nm)
        except (KeyError, TypeError, ValueError):
            continue
    ahead = look_ahead(week, sched, t25, free_qb, free_dst, my_byes, lines=lines) if week else []
    # The board has no `team` column -- it is `team_c` -- so every one of his tight ends read '?'
    # and never reached the December draw. And the board carries no defense at all, so his own
    # defense never reached the run. Both now come from the roster read itself (doc 291).
    mine_te = []
    for pid, nm in mine.items():
        b = board.get(pid) or {}
        mpos, mpro = mine_meta.get(pid, ('?', '?'))
        if str(b.get('pos', '')).upper() == 'TE' or mpos == 'TE':
            mine_te.append((nm, team_key(b.get('team_c') or mpro), True))
    slate, slate_note = te_playoff_slate(sched, load_posallow(), rows, mine_te)
    mine_dst = []
    for pid, nm in mine.items():
        mpos, mpro = mine_meta.get(pid, ('?', '?'))
        if mpos == 'D/ST':
            mine_dst.append({'player': nm, 'team': team_key(mpro)})
    runs, runs_note = dst_runs(week, sched, t25, free_dst, mine_dst, lines=lines)
    byerows, byehead, byenote = bye_plan(week, mine, board)

    stamp = dt.date.today().isoformat().replace('-', '')
    os.makedirs(SRC, exist_ok=True)
    out = os.path.join(SRC, f'WIRE_{stamp}.csv')
    if rows:
        with open(out, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    # FREE_UNRANKED_<date>.csv (doc 292). Every free skill player the board has never rated: the page
    # names only the first 30, and a usage jump by a man off the board (an undrafted back, a practice-
    # squad call-up) was otherwise invisible to the weekly read. A header with no rows is a real answer
    # (nobody off the board is free); a failed write says so. The name cannot match a WIRE_*.csv glob,
    # which sheet_engine.py and build_inherit.py use to find the newest wire.
    try:
        out_free = os.path.join(SRC, f'FREE_UNRANKED_{stamp}.csv')
        with open(out_free, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=['asof', 'espn_id', 'player', 'pos', 'team', 'owned_pct',
                                          'own_chg', 'own_start', 'own_asof', 'clears', 'avail',
                                               'status'])
            w.writeheader()
            for r in sorted(offboard, key=lambda r: -r['owned_pct']):
                w.writerow(dict(asof=dt.date.today().isoformat(), **r))
        print(f"  written: {out_free}  ({len(offboard)} free skill players not on our board)")
    except Exception as exc:                  # a failed extra file never takes the wire down
        print(f"  FREE_UNRANKED csv NOT written -- {type(exc).__name__}: {exc}")

    # MY_ROSTER.csv -- written EVERY run, because "what is on his roster right now" was a question
    # no artifact on the drive could answer, and the answer was being asked for in chat instead.
    if mine:
        with open(os.path.join(SRC, 'MY_ROSTER.csv'), 'w', newline='', encoding='utf-8') as fh:
            w = csv.writer(fh)
            w.writerow(['asof', 'espn_id', 'player', 'pos', 'team', 'bye', 'value',
                        'slot_id', 'status'])
            for pid, nm in sorted(mine.items(), key=lambda kv: kv[1]):
                b = board.get(pid) or {}
                _slot, _st = mine_slot.get(pid, ('', ''))
                w.writerow([dt.date.today().isoformat(), pid, nm, b.get('pos', ''),
                            b.get('team_c', ''), str(b.get('bye', '')).replace('.0', ''),
                            (f"{b['_vor']:.1f}" if b.get('_vor') is not None else ''),
                            ('' if _slot is None else _slot), _st])
        print(f"  written: {os.path.join(SRC, 'MY_ROSTER.csv')}  ({len(mine)} players)")
    else:
        # SECTION 0.2 -- a step that cannot do its job says so rather than writing an empty file.
        print("  MY_ROSTER.csv NOT written -- the roster read returned nothing.")

    # STATUS_LOG.csv -- APPEND-ONLY, doc 393. The question that decides whether the IR trick works
    # is not "does ESPN enforce roster limits" (of course it does, Matt: "You think people would use
    # a fantasy football application that had such and obvious loophole?"). It is WHEN ESPN's own
    # injuryStatus flips, because ESPN's support page (11 Aug 2026) says a HEALTHY man in the IR slot
    # blocks every pending claim -- not on headcount, outright. That timing is unobservable in the
    # nflverse feed (one row per player-week, doc 392) but ESPN hands it to us on every pull and
    # every run until now threw it away. Six runs a week x 15 men answers it inside one week.
    # Append every run, all men: no state comparison, so no silent-skip bug (SECTION 3).
    if mine:
        try:
            _log = os.path.join(SRC, 'STATUS_LOG.csv')
            _new = not os.path.exists(_log)
            with open(_log, 'a', newline='', encoding='utf-8') as fh:
                w = csv.writer(fh)
                if _new:
                    w.writerow(['read_at', 'run', 'espn_id', 'player', 'slot_id', 'status'])
                _who = os.environ.get('FF_WHO', 'manual')
                _now = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
                for pid, nm in sorted(mine.items(), key=lambda kv: kv[1]):
                    _slot, _st = mine_slot.get(pid, ('', ''))
                    w.writerow([_now, _who, pid, nm,
                                ('' if _slot is None else _slot), _st])
            print(f"  appended: {_log}  ({len(mine)} rows, run={_who})")
        except Exception as exc:          # a failed extra file never takes the wire down
            print(f"  STATUS_LOG.csv NOT appended -- {type(exc).__name__}: {exc}")
    else:
        print("  STATUS_LOG.csv NOT appended -- the roster read returned nothing.")

    # ---- WEEK_SHEET.html: the arithmetic, rebuilt from THIS pull -------------------------------
    # doc 273. Matt, 2026-09-10: "I'm not going to be able to do all those calculations week to
    # week." The sheet used to be a photograph taken in a chat session; now it is rebuilt every
    # time this runs, which is Tuesday 6am, Thursday 5:30pm and twice on Sunday.
    # THE WEEK SHEET IS NOT BEHIND A FLAG ANY MORE (doc 310). It was gated on `--html`, whose
    # own help text says "also write THE_WEEKLY_WIRE.html" -- one flag, named after one artifact,
    # silently controlling the OTHER page, the one Matt actually reads every week. On 15 Sept he
    # ran `py wire.py` exactly as asked, the wire rewrote, and WEEK_SHEET.html did not move at
    # all: no error, no line, nothing to notice. That is 0.2's exit-code rule at the level of a
    # command-line flag. The sheet now builds by DEFAULT and `--no-sheet` opts out; `--html`
    # keeps THE_WEEKLY_WIRE.html and nothing else.
    if a.no_sheet:
        print("  WEEK_SHEET.html NOT written -- --no-sheet was passed.")
    else:
        try:
            import sheet_engine
            # doc 417: the WEEK is what turns on the measured blend in rates(). It is read at
            # line ~1730 and was never passed, so the blend computed and reached nothing.
            rate, why = sheet_engine.rates(SRC, week)
            const, cnote = sheet_engine.load_constants(SRC)
            nt = getattr(sheet_engine.rates, 'no_team', [])
            if nt:
                print(f"  not priced on the sheet, no NFL team: {len(nt)} ({', '.join(nt[:6])})")
            if why:
                LOAD_PROBLEMS.append('the week sheet was not rebuilt: ' + why)
            if why:
                print(f"  WEEK_SHEET.html NOT written -- {why}.")
            elif not mine:
                print("  WEEK_SHEET.html NOT written -- the roster read returned nothing.")
            else:
                seen = {r['espn_id']: r for r in rows}
                myrows = []
                for pid in mine:
                    if pid in rate:
                        _m = dict(rate[pid])
                        _m['status'] = status.get(pid, 'ACTIVE')
                        myrows.append(_m)
                # A MAN HE OWNS WHO IS NOT IN `rate` WAS SILENTLY GONE FROM THE PAGE (doc 281).
                # rates() drops anybody ESPN prices at zero -- which is what an injury designation
                # looks like -- so his seat disappeared too, and "the open spot, 0.0" appeared on a
                # full roster. Name the man and carry the TRUE seat count.
                unpriced_mine = sorted(mine[pid] for pid in mine if pid not in rate)
                if unpriced_mine:
                    print("  ON YOUR ROSTER, NOT PRICED (no ESPN projection): "
                          + ', '.join(unpriced_mine))
                freerows = []
                for pid in avail:
                    if pid not in rate:
                        continue
                    f = dict(rate[pid])
                    r0 = seen.get(pid)
                    f['owned'] = r0['owned_pct'] if r0 else None
                    f['screen'] = (r0 or {}).get('screen') or ''
                    # doc 308: the week-1 workload, carried through to the sheet's bet lane.
                    # Blank, not zero, when the man has no week-1 line -- he did not play, and
                    # "0 of 3" would read as a measured miss rather than an absence.
                    f['form_sig'] = (r0 or {}).get('form_sig')
                    f['snap_pct'] = (r0 or {}).get('snap_pct') or ''
                    f['w1_targets'] = (r0 or {}).get('w1_targets') or ''
                    f['tgt_share'] = (r0 or {}).get('tgt_share') or ''
                    f['adot'] = (r0 or {}).get('adot') or ''
                    f['ay_share'] = (r0 or {}).get('ay_share') or ''
                    f['wopr'] = (r0 or {}).get('wopr') or ''
                    f['xfp'] = (r0 or {}).get('xfp') or ''
                    f['fp_oe'] = (r0 or {}).get('fp_oe') or ''
                    f['xfp_g'] = (r0 or {}).get('xfp_g') or ''
                    f['act2'] = (r0 or {}).get('act2') or ''      # doc 438
                    f['xfp2'] = (r0 or {}).get('xfp2') or ''
                    # doc 443: the wire's own flag text, so the sheet prints the SAME mirage or
                    # quiet-volume word the wire printed, read off the row rather than re-derived.
                    f['flags'] = (r0 or {}).get('flags') or ''
                    f['clears'] = (r0 or {}).get('clears') or ''   # [doc 469] the card prints the morning a claim processes
                    # doc 443: the pregame line on a defense or a quarterback, so THE CALL can
                    # print the input the pick rests on (finding 4.39). Absent when no line.
                    _ln = lines.get((week, team_key(f.get('tm') or ''))) if (lines and week) else None
                    if _ln and f.get('pos') in ('D/ST', 'QB'):
                        f['opp'] = _ln[0]
                        f['own_total'] = _ln[1]
                        f['opp_total'] = _ln[2]
                    # doc 314: his LAST GAME's touches, which is what the room files on.
                    f['touches'] = (r0 or {}).get('touches') or ''
                    f['status'] = status.get(pid, 'ACTIVE')
                    freerows.append(f)
                missing_pos = {'QB', 'RB', 'WR', 'TE', 'D/ST', 'K'} - {p['pos'] for p in myrows}
                note = (f"Your roster read is missing {', '.join(sorted(missing_pos))} entirely, so "
                        f"the bar for those slots is not real.") if missing_pos else cnote
                # [30 Sept] the crowd's adds: every free man with ESPN's +/- (doc 395), ranked or
                # not, so the sheet can answer the ten most-added by name (sheet_engine.crowd_table).
                crowd = ([dict(name=r['player'], pos=r['pos'], tm=r['team'], owned=r.get('owned_pct'),
                               own_chg=r.get('own_chg'), espn_id=r['espn_id']) for r in rows]
                         + [dict(name=r['player'], pos=r['pos'], tm=r['team'], owned=r.get('owned_pct'),
                                 own_chg=r.get('own_chg'), espn_id=r['espn_id']) for r in offboard])
                out2 = sheet_engine.write(os.path.join(SRC, 'WEEK_SHEET.html'),
                                          myrows, freerows, const, note=note,
                                          unpriced=unpriced_mine, seats_used=len(mine),
                                          week=week, team_name=my_team_name,
                                          open_jobs=open_jobs, crowd=crowd)
                print(f"  written: {out2}  ({len(mine)} on your roster, {len(myrows)} of them "
                      f"priced, {len(freerows)} priced free)")
        except Exception as exc:                       # never let the sheet take the wire down
            print(f"  WEEK_SHEET.html NOT written -- {type(exc).__name__}: {exc}")

    page = write_page(rows, stash, note='; '.join(LOAD_PROBLEMS), missing=unpriced, doubt=doubt,
                      ahead=ahead, slate=slate, slate_note=slate_note,
                      runs=runs, runs_note=runs_note,
                      byerows=byerows, byehead=byehead,
                      byenote=byenote, roster=mine,
                      waiver_rank=my_waiver_rank, waiver_n=len(waiver_order),
                      waiver_ahead=ahead_of_me) if a.html else None
    for prob in LOAD_PROBLEMS:
        print('  LOAD PROBLEM -- ' + prob)

    print(f"\n  {len(pool)} available | {len(rows)} we can price | {len(stash)} one-injury-away backs"
          f" | {len(doubt)} in doubt | roster read: {len(mine)} players")
    print(f"  written: {out}")
    if page:
        print(f"  written: {page}")
    if ahead:
        print("\n  COMING UP -- buy the bye fill early, while nobody else needs it:")
        for a2 in ahead:
            off = ('   OFF: ' + ', '.join(a2['off'])) if a2['off'] else ''
            print(f"    week {a2['week']}{off}")
            on_line = a2.get('axis') == 'line'       # doc 442: the number is a line total, not last season
            for v, n, t, o in a2['qb'][:2]:
                lab = f'own team total {v:.1f}' if on_line else f'they allow {v:.1f}/g'
                print(f"       QB   {n:<22}{t:<5}vs {o:<5}({lab})")
            for v, n, t, o in a2['dst'][:2]:
                lab = f'opponent total {v:.1f}' if on_line else f'they score {v:.1f}/g'
                print(f"       DST  {n:<22}{t:<5}vs {o:<5}({lab})")
    elif not load_sched():
        print("\n  NO SCHEDULE ON FILE -- the weeks-ahead section is missing, not empty.")
    if byehead and byehead.get('one_slot'):
        print(f"\n  WEEK {byehead['week']} BYE -- one empty {byehead['one_slot']} slot "
              f"({', '.join(byehead['off'])}); a one-week pickup fills it, no trade needed.")
    elif byehead:
        print(f"\n  THE TRADE SITTING THERE -- week {byehead['week']} is {byehead['out']} week(s) "
              f"away and costs about {byehead['cost']:.0f} points:")
        print("    off that week: " + ", ".join(byehead['off']))
        print("    send someone whose bye is later and whose slot you double: "
              + (", ".join(byehead['send']) or "nobody fits"))
        print("    ask for a bye in: " + (", ".join('wk %d' % w for w in byehead['quiet']) or "any quiet week"))
    elif byenote:
        print(f"\n  BYE PLAN INCOMPLETE -- {byenote}.")
    if runs:
        print("\n  DEFENCE TO HOLD -- softest RUN ahead, not softest week:")
        for r in runs[:5]:
            tag = '  (YOURS)' if r['mine'] else ''
            print(f"    {r['player']:<22}{r['team']:<5}wks {r['weeks']:<7}"
                  f"{' '.join(r['opps']):<20}who score {r['faces']:.1f}/g{tag}")
    elif runs_note:
        print(f"\n  NO DEFENCE RUN -- {runs_note}.")
    if slate:
        print("\n  TIGHT END, WEEKS 15-17 -- the only place the draw is measured to matter:")
        for d in slate[:6]:
            tag = '  (YOURS)' if d['mine'] else ''
            print(f"    {d['player']:<24}{d['tm']:<5}{' '.join(d['opps']):<18}"
                  f"they allowed {d['mean']:.1f}/g{tag}")
    elif slate_note:
        print(f"\n  NO PLAYOFF SLATE -- {slate_note}.")
    if doubt:
        print("\n  IN DOUBT NOW -- a rostered starter carries a status and his backup is free:")
        for d in doubt[:8]:
            tag = '  (YOURS)' if d['mine'] else ''
            print(f"    {d['player']:<24}{d['tm']:<5}because {d['hurt'][:20]:<22}is {d['status']}{tag}")
    print("\n  LANE 2 -- stash before the injury, ranked by what the job pays:")
    for d in stash[:8]:
        print(f"    {d['player']:<24}{d['tm']:<5}behind {d['ahead'][:22]:<24}job pays {d['ceil']:.0f}")
    for tm, who, st in (getattr(next_man_up, 'opened', None) or []):
        print(f"    (not a stash: {tm} {who} is {st}, the job is already open; see IN DOUBT NOW)")
    print("\n  LANE 3 -- POTENTIAL, not today's value. Young receivers with the pedigree:")
    if ped_note:
        print(f"    NOT BUILT -- {ped_note}. This lane is missing, not empty.")
    elif not potential:
        print("    nobody free clears either screen this week.")
    else:
        for r in potential:
            p2 = pedrow.get(r['espn_id']) or ped_all.get(str(r['espn_id'])) or {}
            if r['screen'] == 'first-round rookie':
                why = f"NFL pick {p2.get('nfl_pick', '?')} this year -- 6 of the last 15 were startable as rookies"
            elif r['screen'].startswith('in-season screen'):
                why = f"year {p2.get('nfl_year', '?')}, NFL pick {p2.get('nfl_pick', '?')}, this season: {r['flags'].split('in-season screen 3 of 3 ')[-1]}"
            else:
                why = (f"year {p2['nfl_year']}, NFL pick {p2['nfl_pick']}, "
                       f"{p2['ypt25']} yards a target on {p2['tpg25']} targets a game")
            st = r.get('status', 'ACTIVE')
            if st != 'ACTIVE':             # the console has no player card beside it (doc 291)
                why += f"  [ESPN: {st.replace('_', ' ').lower()}]"
            print(f"    {r['player']:<24}{r['pos']:<4}{r['team']:<5}owned {r['owned_pct']:>5}%  {why}")

    print("\n  LANE 1 -- best available now, ranked by our value:")
    shown = {}
    for r in rows:
        if not a.all:
            shown[r['pos']] = shown.get(r['pos'], 0) + 1
            if shown[r['pos']] > SHOW_PER_POS:
                continue
        print(f"    {r['player']:<24}{r['pos']:<6}{r['team']:<5}{r['value']:>8.1f}  "
              f"bye {str(r['bye']):<5} owned {r['owned_pct']:>5}%  {r['flags']}")

    # SECTION 0.5(c)5 -- a thing that SHOULD be on the sheet and is not must be named, not silent.
    print(f"\n  {unpriced_kdst} kickers and defenses were skipped -- that is expected.")
    if unpriced:
        print(f"  *** {len(unpriced)} SKILL players are available and NOT on our board, so they are")
        print("  *** missing from the sheet entirely. Check these by hand:")
        for u in unpriced[:30]:
            print("        " + u)
        if len(unpriced) > 30:
            print(f"        ... and {len(unpriced) - 30} more")
    return 0


if __name__ == '__main__':
    sys.exit(main())
