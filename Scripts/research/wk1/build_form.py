#!/usr/bin/env python3
r"""build_form.py -- Source\form_2026.csv: the IN-SEASON workload the weekly page cannot see.

WHY THIS EXISTS (doc 308). Every input to WEEK_SHEET's recommendation is fixed before week 1 --
board_v8_fixed.csv, player_context.csv, pedigree_2026.csv (whose columns are all 2025),
inherit_2026.csv, and the 2025 team files. Week 1 has been played and no runtime path reads a
snap of it. 4.31 measures week 2 as the best claim week of the season BECAUSE it bets on a snap
count rather than a depth chart, so the blindness lands on the one week it costs most.

WHAT IT WRITES, one row per player per completed week plus a cumulative row (week 0):
  snap_pct, targets, carries, tgt_share, car_share, touches, half_ppr  -- under 2's scoring.
  air_yards, adot, ay_share, wopr  -- doc 435 / finding 4.35: the feed has carried
  receiving_air_yards all along and nothing read it. adot = air yards per target; ay_share =
  his share of his team's receiving air yards; wopr = 1.5 x target share + 0.7 x air-yards
  share (as fractions), the instrument 4.35 measured. Blank adot when he has no target.
  xfp, xtd, fp_oe  -- doc 437: EXPECTED fantasy points under OUR scoring, from ffverse's
  ffopportunity model (nflverse play-by-play, xgboost on 2006-2020; every target and carry
  priced by field position, down, distance and air yards). Their file scores full PPR and
  4-point passing TDs, so xfp = their total_fantasy_points_exp - 0.5 x receptions_exp
  + 2 x pass_touchdown_exp. fp_oe = half_ppr - xfp (points over expected: positive is luck
  or talent, negative is a man whose role paid less than it should). Blank, never zero, on
  a week the model has not processed (it lags nflverse by a night on Monday games), and
  blank at QB, where half_ppr carries no passing points (doc 375) so the difference would lie.
  act2 / xfp2  -- on the cumulative row only: his actual and his EXPECTED half-PPR averaged
  over his LAST TWO completed games (doc 438). Measured 2021-2025 on 9,999 claimable
  RB/WR/TE weeks: the two-game expected predicts the next four weeks better than the
  two-game actual at every position (rho .50 against .42), and a man at 8+ actual on
  under 5 expected is WORSE than the pool (startable next four 12% against 17%).
  in_progress  -- 1 on a week still being played, 0 on a finished one. The page reads the
  last game with in_progress == 0; without this column it would have to infer it from row
  counts, and a wrong guess silently prices a man on half a game.
Key: normalised name + position + team (3's rule where no shared id exists). The page must
ASSERT on the join and never default a miss to '?' (doc 251).

Portable per 0.4: stdlib only, paths off __file__, no shelling out, no invalid escapes.
"""
import collections, csv, os, re, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
IN_PROGRESS = set()
SRC = os.environ.get('FF_SOURCE') or os.path.abspath(os.path.join(HERE, '..', '..', '..', 'Source'))
BASE = 'https://github.com/nflverse/nflverse-data/releases/download'
FEEDS = {'stats_player_week_2026.csv': f'{BASE}/stats_player/stats_player_week_2026.csv',
         'snap_counts_2026.csv':       f'{BASE}/snap_counts/snap_counts_2026.csv',
         # ffverse, not nflverse-data: the expected-points release (doc 437)
         'ep_weekly_2026.csv': 'https://github.com/ffverse/ffopportunity/releases/download/latest-data/ep_weekly_2026.csv'}
# ONE SPELLING OR NO JOIN (section 3). The project's own map lives in sheet_engine.py and it
# runs the OTHER WAY from nflverse: LA -> LAR and WAS -> WSH, where nflverse writes LA and WAS.
# Emitting nflverse's spelling would have silently dropped the Rams and Washington from every
# join the page makes. Import the real map; the literal below is only a standalone fallback and
# is asserted against the import when both are present.
_FALLBACK = {'ARZ': 'ARI', 'BLT': 'BAL', 'CLV': 'CLE', 'HST': 'HOU', 'LA': 'LAR', 'WAS': 'WSH',
             'JAC': 'JAX', 'GNB': 'GB', 'KAN': 'KC', 'NWE': 'NE', 'NOR': 'NO', 'SFO': 'SF',
             'TAM': 'TB', 'LVR': 'LV', 'SD': 'LAC', 'OAK': 'LV', 'STL': 'LAR'}
try:
    sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..')))
    from sheet_engine import TEAM_ALIAS as TF          # the canonical map
    TEAM_MAP_SOURCE = 'sheet_engine.TEAM_ALIAS'
except Exception:
    TF = _FALLBACK
    TEAM_MAP_SOURCE = 'the local fallback (sheet_engine.py not importable)'


def norm(n):
    n = (n or '').lower()
    n = re.sub(r"[.'`’]", '', n)
    n = re.sub(r'\b(jr|sr|ii|iii|iv|v)\b', '', n)
    return re.sub(r'[^a-z]', '', n)


def tk(t):
    t = (t or '').upper().strip()
    return TF.get(t, t)


def half_ppr(r):
    g = lambda k: float(r.get(k) or 0)
    return (0.1 * g('rushing_yards') + 6 * g('rushing_tds') + 0.1 * g('receiving_yards')
            + 6 * g('receiving_tds') + 0.5 * g('receptions')
            - 2 * (g('rushing_fumbles_lost') + g('receiving_fumbles_lost')))


def fetch(name, url, cache):
    """ALWAYS re-fetch. An in-season feed grows every week, and the first version of this
    function returned any cached file over 1 KB -- so Matt's 15 Sept run silently reused a
    13 Sept partial download sitting in this folder and built the whole file from TWENTY of
    the thirty-two teams. Green Bay, Denver and Miami were simply absent, which is three of
    the six names the screen was meant to surface. 0.2: the run printed a row count and
    exited 0, and the count looked fine. A cache is only allowed to serve a fetch that
    FAILED, and then it must say so out loud."""
    p = os.path.join(cache, name)
    try:
        with urllib.request.urlopen(url, timeout=120) as fh:
            body = fh.read()
        if len(body) < 1000:
            raise ValueError(f'the feed returned {len(body)} bytes')
        with open(p, 'wb') as out:
            out.write(body)
        return p
    except Exception as exc:
        if os.path.exists(p) and os.path.getsize(p) > 1000:
            import datetime
            when = datetime.datetime.fromtimestamp(os.path.getmtime(p))
            print(f'  WARNING: could not fetch {name} ({exc}).\n'
                  f'  FALLING BACK to the copy already here, dated {when:%d %b %H:%M}.\n'
                  f'  If that is older than the last game it is STALE and this run is wrong.')
            return p
        sys.exit(f'FAILED to fetch {name}: {exc}\n'
                 f'  put the file in {cache} by hand and re-run.')


def main():
    cache = os.environ.get('FF_CACHE', HERE)
    stats_p = fetch('stats_player_week_2026.csv', FEEDS['stats_player_week_2026.csv'], cache)
    snaps_p = fetch('snap_counts_2026.csv', FEEDS['snap_counts_2026.csv'], cache)
    ep_p = fetch('ep_weekly_2026.csv', FEEDS['ep_weekly_2026.csv'], cache)

    stats = [r for r in csv.DictReader(open(stats_p, newline='', encoding='utf-8-sig'))
             if (r.get('season_type') or 'REG') == 'REG']
    if not stats:
        sys.exit('FAILED: the weekly feed holds no regular-season rows.')
    weeks = sorted({int(r['week']) for r in stats})
    # [doc 439] A COMPLETED WEEK HAS 32 CLUBS LESS THE ONES ON BYE. The first version said 32
    # flat, which holds for weeks 1 to 4 only: week 5 has two clubs on bye, so it would have been
    # held out as "in progress" for a week and then, the moment week 6 arrived, killed every run
    # for the rest of the season as a "partial feed". byes_2026.csv is the same file the sheet uses.
    need = _clubs_expected()
    # A COMPLETED WEEK HAS ALL ITS CLUBS. Anything less means a partial feed, which is exactly
    # what the cache bug above produced, and it is invisible in a row count.
    by_week = collections.Counter()
    for r in stats:
        by_week[int(r['week'])] += 0
    clubs = collections.defaultdict(set)
    for r in stats:
        clubs[int(r['week'])].add(tk(r['team']))
    short = {w: sorted(c) for w, c in clubs.items() if len(c) < need(w)}
    if short and max(clubs, key=lambda w: len(clubs[w])) is not None:
        newest = max(clubs)
        for w in sorted(short):
            miss = need(w) - len(clubs[w])
            if w == newest:
                print(f'  week {w} has {len(clubs[w])} of {need(w)} clubs -- '
                      f'treating it as STILL IN PROGRESS and keeping it out of the '
                      f'cumulative row.')
            else:
                sys.exit(f'FAILED: week {w} is behind the newest week ({newest}) and still '
                         f'has only {len(clubs[w])} of {need(w)} clubs ({miss} missing). That is a '
                         f'partial feed, not a partial week. Delete '
                         f'{os.path.join(cache, "stats_player_week_2026.csv")} and re-run.')
        IN_PROGRESS.add(newest)

    snap = {}
    for r in csv.DictReader(open(snaps_p, newline='', encoding='utf-8-sig')):
        try:
            p, w = float(r['offense_pct'] or 0), int(r['week'])
        except (ValueError, TypeError):
            continue
        snap[(w, norm(r['player']), tk(r['team']))] = round(p * 100 if p <= 1 else p, 1)

    # doc 437: expected points, keyed like the snap line. A miss stays blank (the model has
    # not processed that game yet); it is never written as zero.
    ep = {}
    for r in csv.DictReader(open(ep_p, newline='', encoding='utf-8-sig')):
        try:
            w = int(r['week'])
            xfp = (float(r['total_fantasy_points_exp'] or 0) - 0.5 * float(r['receptions_exp'] or 0)
                   + 2.0 * float(r['pass_touchdown_exp'] or 0))
            xtd = (float(r['rec_touchdown_exp'] or 0) + float(r['rush_touchdown_exp'] or 0)
                   + float(r['pass_touchdown_exp'] or 0))
        except (ValueError, TypeError, KeyError):
            continue
        ep[(w, norm(r['full_name']), r.get('position') or '', tk(r['posteam']))] = (round(xfp, 2), round(xtd, 2))

    tt = collections.Counter()
    tc = collections.Counter()
    ta = collections.Counter()          # team receiving air yards, the ay_share denominator
    for r in stats:
        k = (int(r['week']), tk(r['team']))
        tt[k] += float(r.get('targets') or 0)
        tc[k] += float(r.get('carries') or 0)
        ta[k] += float(r.get('receiving_air_yards') or 0)

    agg = collections.defaultdict(lambda: collections.defaultdict(float))
    games = {}                                   # doc 438: (name, pos, team) -> [(week, actual, expected)]
    rows, missing_snap = [], 0
    for r in stats:
        w, tm = int(r['week']), tk(r['team'])
        nm, pos = norm(r['player_display_name']), r.get('position') or ''
        tg, ca = float(r.get('targets') or 0), float(r.get('carries') or 0)
        ay = float(r.get('receiving_air_yards') or 0)
        sp = snap.get((w, nm, tm))
        xp = ep.get((w, nm, pos, tm))
        if sp is None and pos in ('RB', 'WR', 'TE'):
            missing_snap += 1
        row = {'week': w, 'name_key': nm, 'player': r['player_display_name'], 'pos': pos,
               'team': tm, 'snap_pct': '' if sp is None else sp,
               'targets': int(tg), 'carries': int(ca),
               'tgt_share': round(100 * tg / tt[(w, tm)], 1) if tt[(w, tm)] else 0.0,
               'car_share': round(100 * ca / tc[(w, tm)], 1) if tc[(w, tm)] else 0.0,
               'touches': int(tg + ca), 'half_ppr': round(half_ppr(r), 2),
               'air_yards': int(ay),
               'adot': round(ay / tg, 1) if tg else '',
               'ay_share': round(100 * ay / ta[(w, tm)], 1) if ta[(w, tm)] else 0.0,
               'wopr': round(1.5 * (tg / tt[(w, tm)] if tt[(w, tm)] else 0)
                             + 0.7 * (ay / ta[(w, tm)] if ta[(w, tm)] else 0), 3),
               'xfp': xp[0] if xp else '', 'xtd': xp[1] if xp else '',
               # fp_oe is blank at QB: half_ppr does not score passing (doc 375), so the
               # actual it would subtract from is rushing only and the difference would lie
               'fp_oe': round(round(half_ppr(r), 2) - xp[0], 2) if (xp and pos != 'QB') else '', 'xfp_g': '',
               'act2': '', 'xfp2': '',
               # doc 453: receiving yards and receptions, so the in-season young-receiver screen
               # (yards per target, targets a game) can be read off this file; games for the rate
               'rec_yds': int(float(r.get('receiving_yards') or 0)), 'rec': int(float(r.get('receptions') or 0)),
               'games': 1,
               # doc 314 needs the LAST COMPLETED game, not the season to date, and a
               # reader cannot tell a half-played week from a finished one by row count
               # alone. So the file SAYS which it is rather than making the page guess.
               'in_progress': 1 if w in IN_PROGRESS else 0}
        rows.append(row)
        if w in IN_PROGRESS:
            continue                       # a half-played week must not move a season rate
        a = agg[(nm, pos, tm)]
        a['games'] += 1
        for f in ('targets', 'carries', 'touches', 'half_ppr', 'rec_yds', 'rec'):
            a[f] += row[f]
        if sp is not None:
            a['snap_sum'] += sp
            a['snap_n'] += 1
        a['tgt_sum'] += tg
        a['team_tgt'] += tt[(w, tm)]
        a['car_sum'] += ca
        a['team_car'] += tc[(w, tm)]
        a['ay_sum'] += ay
        a['team_ay'] += ta[(w, tm)]
        if xp:
            a['xfp'] += xp[0]
            a['xtd'] += xp[1]
            a['xfp_g'] += 1
            a['fp_oe'] += row['half_ppr'] - xp[0]
        # doc 438: the last two completed games, actual beside expected, kept as (week, actual,
        # expected) so the cumulative row can average the two newest rather than the two first
        games.setdefault((nm, pos, tm), []).append((w, row['half_ppr'], xp[0] if xp else None))

    for (nm, pos, tm), a in agg.items():
        # doc 438: mean actual and mean expected over the two NEWEST completed games (one game if
        # he has only one). Expected is blank, never zero, when either game lacks a model row.
        g2 = sorted(games.get((nm, pos, tm), []))[-2:]
        last2 = (round(sum(g[1] for g in g2) / len(g2), 2) if g2 else '',
                 round(sum(g[2] for g in g2) / len(g2), 2) if (g2 and all(g[2] is not None for g in g2)) else '')
        rows.append({'week': 0, 'name_key': nm, 'pos': pos, 'team': tm,
                     'player': next(r['player'] for r in rows
                                    if r['name_key'] == nm and r['team'] == tm),
                     'snap_pct': round(a['snap_sum'] / a['snap_n'], 1) if a['snap_n'] else '',
                     'targets': int(a['targets']), 'carries': int(a['carries']),
                     'tgt_share': round(100 * a['tgt_sum'] / a['team_tgt'], 1) if a['team_tgt'] else 0.0,
                     'car_share': round(100 * a['car_sum'] / a['team_car'], 1) if a['team_car'] else 0.0,
                     'touches': int(a['touches']), 'half_ppr': round(a['half_ppr'], 2),
                     'air_yards': int(a['ay_sum']),
                     'adot': round(a['ay_sum'] / a['tgt_sum'], 1) if a['tgt_sum'] else '',
                     'ay_share': round(100 * a['ay_sum'] / a['team_ay'], 1) if a['team_ay'] else 0.0,
                     'wopr': round(1.5 * (a['tgt_sum'] / a['team_tgt'] if a['team_tgt'] else 0)
                                   + 0.7 * (a['ay_sum'] / a['team_ay'] if a['team_ay'] else 0), 3),
                     # the cumulative expected points cover only the weeks the model has
                     # processed (xfp_g of games), so fp_oe compares like with like
                     'xfp': round(a['xfp'], 2) if a['xfp_g'] else '',
                     'xtd': round(a['xtd'], 2) if a['xfp_g'] else '',
                     'fp_oe': round(a['fp_oe'], 2) if (a['xfp_g'] and pos != 'QB') else '',
                     'xfp_g': int(a['xfp_g']),
                     'act2': last2[0], 'xfp2': last2[1],
                     'rec_yds': int(a['rec_yds']), 'rec': int(a['rec']), 'games': int(a['games']),
                     'in_progress': 0})       # the cumulative row excludes them by construction

    # AND THE ARTIFACT MUST BE USABLE, not merely written (0.2: verify the thing, not the
    # exit code). The page joins on the week-0 cumulative row; if every completed week was
    # excluded as in-progress that row is empty and the file is worthless.
    if not agg:
        sys.exit('FAILED: no COMPLETED week in the feed, so the cumulative row would be '
                 'empty and the page would join against nothing. If a week is genuinely '
                 'still being played, wait for it; otherwise the feed is partial.')

    cols = ['week', 'name_key', 'player', 'pos', 'team', 'snap_pct', 'targets', 'carries',
            'tgt_share', 'car_share', 'touches', 'half_ppr', 'air_yards', 'adot', 'ay_share',
            'wopr', 'xfp', 'xtd', 'fp_oe', 'xfp_g', 'act2', 'xfp2', 'in_progress', 'rec_yds', 'rec', 'games']
    out = os.path.join(SRC, 'form_2026.csv')
    # [doc 439] WRITTEN TO A TEMP FILE AND SWAPPED IN ONLY AFTER EVERY CHECK PASSES, so a run that
    # fails, on a schedule or by hand, leaves last week's file exactly as it was. Doc 353 named
    # this as the one thing keeping this script out of ff.bat.
    tmp = out + '.tmp'
    with open(tmp, 'w', newline='', encoding='utf-8') as fh:
        w_ = csv.DictWriter(fh, fieldnames=cols, lineterminator='\n')
        w_.writeheader()
        w_.writerows(sorted(rows, key=lambda r: (r['week'], -r['touches'])))
    print(f'form_2026.csv  weeks {weeks}  {len(rows)} rows '
          f'({len(agg)} players, week 0 is the cumulative row)')
    for w in sorted(clubs):
        print(f'    week {w}: {len(clubs[w])} of {need(w)} clubs, '
              f'{sum(1 for r in rows if r["week"] == w)} player rows'
              + ('   [IN PROGRESS, excluded from week 0]' if w in IN_PROGRESS else ''))
    print(f'  skill-position rows with no snap line: {missing_snap}')
    print(f'  team codes via {TEAM_MAP_SOURCE}')
    if missing_snap > 0.25 * len(stats):
        os.remove(tmp)
        sys.exit('FAILED: more than a quarter of skill rows have no snap line -- '
                 'the snap join is broken, not the data. form_2026.csv was left as it was.')
    swap_in(tmp, out)
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


def _clubs_expected():
    """Clubs that should appear in a finished week: 32 less the byes in Source\\byes_2026.csv.
    With no bye file every week expects 32, the old rule, and the run says so."""
    byes = collections.Counter()
    p = os.path.join(SRC, 'byes_2026.csv')
    if os.path.exists(p):
        for r in csv.DictReader(open(p, newline='', encoding='utf-8-sig')):
            try:
                byes[int(float(r.get('bye') or 0))] += 1
            except ValueError:
                pass
    else:
        print(f'  WARNING: no {p}, so every week expects 32 clubs and a bye week will read as '
              f'partial.')
    return lambda w: 32 - byes.get(int(w), 0)


if __name__ == '__main__':
    main()
