#!/usr/bin/env python3
r"""build_depth_daily.py -- Source\depth_daily.csv and Source\practice_2026.csv, from nflverse.

WHY THIS EXISTS (doc 437 section 6 item 4). The seat lane, which backup inherits a job when the
man ahead is out, is built on Scripts\depth_map.csv, a depth chart captured 8 August 2026, and on
Source\inherit_2026.csv, which build_inherit.py reads off the same August scrape
(Source\2026_NFL_Depth_Charts_All_Teams.csv). Nothing in the runtime path reads a chart younger
than the preseason. nflverse publishes ESPN's depth chart twice a day and the NFL's injury report
nightly, both free, both keyed on gsis_id. This script turns them into two small files the page
can join on.

WHAT THE FEEDS CARRY (read from the live headers on 29 Sept 2026, not from memory):
  depth_charts_2026.csv  dt, team, player_name, espn_id, gsis_id, pos_grp_id, pos_grp, pos_id,
                         pos_name, pos_abb, pos_slot, pos_rank
      One row per man per formation slot per snapshot; `dt` is the snapshot timestamp and every
      snapshot covers all 32 clubs. The offence is one formation, "3WR 1TE". `pos_rank` is his
      depth WITHIN his position across all of that position's slots: QB, RB and TE have one slot
      each and rank 1..n straight down; WR has three slots (X, Z, slot), so ranks 1 to 3 are the
      three starters, 4 to 6 the second string, and so on. That is depth_map.csv's depth 1 /
      depth 2 for WR, flattened. Fullbacks are their own pos_abb (FB) and are LEFT OUT: a fullback
      is not the man who inherits a running back's job (doc 275). Measured on 29 Sept: ranks are
      contiguous 1..n on every team x position, and no man appears twice within one team x position.
  injuries_2026.csv      season, season_type, game_type, team, week, gsis_id, position, full_name,
                         first_name, last_name, report_primary_injury, report_secondary_injury,
                         report_status, practice_primary_injury, practice_secondary_injury,
                         practice_status
      One row per man per week, the week's LATEST report. practice_primary_injury is filled on
      every row; report_primary_injury only when he carries a game designation (Out, Doubtful,
      Questionable), and the two never disagree when both are present. There is NO per-row
      timestamp, so the age of the report is the feed's own HTTP Last-Modified header when the
      file was downloaded this run, else the newest depth-chart `dt` (a --probe run, or a fetch
      that fell back to a cached copy); the run prints WHICH. A week-N report first appears on the
      Wednesday of week N; until then the newest week in the file is LAST week's final
      designation and the run says so.

WHAT IT WRITES, both through a temp file and swapped in only after every check passes:
  Source\depth_daily.csv   one row per team x position (QB, RB, WR, TE) x depth, from the NEWEST
                           snapshot per team:
        team, pos, depth, player, name_key, gsis_id, espn_id, as_of
  Source\practice_2026.csv one row per man on the newest week's injury report, every position:
        team, pos, player, name_key, gsis_id, week, report_status, practice_status,
        practice_injury, days_old
  `name_key` IS build_form.py's norm(): the function is imported from the build_form.py in this
  folder and used directly; the verbatim copy below exists only for a run where that import fails,
  and when both are present the two are compared on EVERY real name in both feeds before anything
  is written. Team codes go through sheet_engine.TEAM_ALIAS the way build_form.py does (nflverse
  writes LA and WAS; the sheet writes LAR and WSH).

FETCH CONVENTION: build_form.py's. ALWAYS re-fetch; a cached copy is served only when the fetch
FAILS, and then with a dated WARNING, because a silently reused stale file is the defect this
script exists to remove. `--probe DIR` reads both feeds from DIR and downloads nothing (a test run).

Portable per 0.4: standard library plus pandas, paths off __file__, no shelling out, no invalid
escapes. Python 3.12 clean.

USAGE  py build_depth_daily.py [--probe DIR]
       Run from Scripts\research\wk1\ beside build_form.py. Source is ..\..\..\Source against this
       file, or the FF_SOURCE environment variable. Downloads land in FF_CACHE, else this folder.
"""
import argparse, csv, datetime, email.utils, os, re, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get('FF_SOURCE') or os.path.abspath(os.path.join(HERE, '..', '..', '..', 'Source'))
BASE = 'https://github.com/nflverse/nflverse-data/releases/download'
FEEDS = {'depth_charts_2026.csv': f'{BASE}/depth_charts/depth_charts_2026.csv',
         'injuries_2026.csv':     f'{BASE}/injuries/injuries_2026.csv'}
POS = ('QB', 'RB', 'WR', 'TE')             # FB is excluded on purpose (doc 275)
POS_ORDER = {p: i for i, p in enumerate(POS)}
STALE_DAYS = 3                             # the chart feed rebuilds twice a day; older than this is wrong

# ONE SPELLING OR NO JOIN (section 3). The canonical map is sheet_engine.TEAM_ALIAS, imported the
# way build_form.py imports it (Scripts\ is two folders up). The literal is a standalone fallback
# and is asserted against the import when both are present.
_FALLBACK = {'ARZ': 'ARI', 'BLT': 'BAL', 'CLV': 'CLE', 'HST': 'HOU', 'LA': 'LAR', 'WAS': 'WSH',
             'JAC': 'JAX', 'GNB': 'GB', 'KAN': 'KC', 'NWE': 'NE', 'NOR': 'NO', 'SFO': 'SF',
             'TAM': 'TB', 'LVR': 'LV', 'SD': 'LAC', 'OAK': 'LV', 'STL': 'LAR'}
try:
    sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..')))
    from sheet_engine import TEAM_ALIAS as TF          # the canonical map
    TEAM_MAP_SOURCE = 'sheet_engine.TEAM_ALIAS'
    if TF != _FALLBACK:
        sys.exit('FAILED: sheet_engine.TEAM_ALIAS differs from the fallback literal in this file. '
                 'Fix the literal so a run without the import spells teams the same way.')
except SystemExit:
    raise
except Exception:
    TF = _FALLBACK
    TEAM_MAP_SOURCE = 'the local fallback (sheet_engine.py not importable)'


def _norm_copy(n):
    """build_form.py's norm(), VERBATIM, for a run where build_form.py cannot be imported. When it
    can, the imported function is what writes name_key and this copy is only checked against it."""
    n = (n or '').lower()
    n = re.sub(r"[.'`’]", '', n)
    n = re.sub(r'\b(jr|sr|ii|iii|iv|v)\b', '', n)
    return re.sub(r'[^a-z]', '', n)


try:
    sys.path.insert(0, HERE)
    from build_form import norm                          # the same folder, the same function
    NORM_SOURCE = os.path.join(HERE, 'build_form.py')
except Exception as _exc:
    norm = _norm_copy
    NORM_SOURCE = f'the verbatim copy in this file, UNCHECKED (build_form.py not importable: {_exc})'


def assert_norm_matches(names):
    """When build_form.py was imported, prove the copy above equals it on every real name this
    run will write. A silent divergence is a join that drops men with no error (section 3)."""
    if norm is _norm_copy:
        print(f'  WARNING: name_key from {NORM_SOURCE}')
        return
    bad = [n for n in names if norm(n) != _norm_copy(n)]
    if bad:
        sys.exit(f'FAILED: the norm() copy in this file differs from build_form.norm() on '
                 f'{len(bad)} real name(s), e.g. {bad[:3]}. Copy it again.')


def tk(t):
    t = (t or '').upper().strip()
    return TF.get(t, t)


def fetch(name, url, cache):
    """ALWAYS re-fetch (build_form.py's rule). An in-season feed grows every day, and a cache that
    serves any file over 1 KB is what built form_2026.csv from twenty teams on 15 Sept. A cached
    copy is served ONLY when the fetch FAILS, and then it says so with the date. Returns
    (path, last_modified) where last_modified is the server's header as a UTC datetime, or None
    on a fallback."""
    p = os.path.join(cache, name)
    try:
        with urllib.request.urlopen(url, timeout=180) as fh:
            body = fh.read()
            lm = fh.headers.get('Last-Modified')
        if len(body) < 1000:
            raise ValueError(f'the feed returned {len(body)} bytes')
        with open(p, 'wb') as out:
            out.write(body)
        when = None
        if lm:
            try:
                when = email.utils.parsedate_to_datetime(lm)
                if when.tzinfo is None:
                    when = when.replace(tzinfo=datetime.timezone.utc)
            except (TypeError, ValueError):
                when = None
        print(f'  {name}: downloaded {len(body):,} bytes'
              + (f', Last-Modified {when:%d %b %H:%M} UTC' if when else ', no Last-Modified header'))
        return p, when
    except Exception as exc:
        if os.path.exists(p) and os.path.getsize(p) > 1000:
            when = datetime.datetime.fromtimestamp(os.path.getmtime(p))
            print(f'  WARNING: could not fetch {name} ({exc}).\n'
                  f'  FALLING BACK to the copy already here, dated {when:%d %b %H:%M}.\n'
                  f'  If that is older than the last game it is STALE and this run is wrong.')
            return p, None
        sys.exit(f'FAILED to fetch {name}: {exc}\n'
                 f'  put the file in {cache} by hand and re-run.')


def swap_in(tmp, out):
    """Replace `out` with `tmp` in one step (build_form.py). Google Drive for desktop can hold a
    brief lock on a file it is uploading, so retry before giving up, and never leave the temp
    file behind."""
    for _ in range(5):
        try:
            os.replace(tmp, out)
            return
        except OSError:
            time.sleep(2)
    import shutil
    shutil.copyfile(tmp, out)
    os.remove(tmp)


def write_tmp(path, rows, cols):
    tmp = path + '.tmp'
    with open(tmp, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    return tmp


def build_depth(depth_p):
    """One row per team x position x depth from the newest snapshot per team."""
    import pandas as pd
    need = ['dt', 'team', 'player_name', 'espn_id', 'gsis_id', 'pos_abb', 'pos_slot', 'pos_rank']
    d = pd.read_csv(depth_p, usecols=lambda c: c in need, low_memory=False)
    missing = [c for c in need if c not in d.columns]
    if missing:
        sys.exit(f'FAILED: depth_charts_2026.csv is missing {missing}; its header is {list(d.columns)}. '
                 f'The schema moved; fix build_depth() before trusting anything it writes.')
    d = d[d.pos_abb.isin(POS)].copy()
    if d.empty:
        sys.exit('FAILED: no QB/RB/WR/TE rows in the depth feed.')
    newest = d.groupby('team').dt.transform('max')
    d = d[d.dt == newest].copy()
    d['team'] = d.team.map(tk)
    stamps = sorted(d.dt.unique())
    rows, ghosts = [], []
    for (tm, pos), g in d.groupby(['team', 'pos_abb']):
        g = g.sort_values(['pos_rank', 'pos_slot'])
        ranks = g.pos_rank.tolist()
        if ranks != list(range(1, len(ranks) + 1)):
            sys.exit(f'FAILED: {tm} {pos} pos_rank is not 1..n on the newest chart: {ranks}. '
                     f'The rank column no longer means what this script assumes.')
        # A ROW WITH NO NAME IS NOT A MAN (doc 414). The feed carries the odd ghost slot, an espn_id
        # with no player_name and no gsis_id (NYG TE rank 3 on 29 Sept, espn_id 2531358). It cannot
        # be keyed, so it is dropped, SAID, and the men below it move up one: depth is his order
        # among the real men, which is what "who is next" means.
        depth = 0
        for r in g.itertuples(index=False):
            if not isinstance(r.player_name, str) or not r.player_name.strip():
                ghosts.append(f'{tm} {pos} rank {int(r.pos_rank)} espn_id {"" if pd.isna(r.espn_id) else int(r.espn_id)}')
                continue
            depth += 1
            rows.append({'team': tm, 'pos': pos, 'depth': depth, 'player': r.player_name,
                         'name_key': norm(r.player_name),
                         'gsis_id': '' if pd.isna(r.gsis_id) else r.gsis_id,
                         'espn_id': '' if pd.isna(r.espn_id) else int(r.espn_id), 'as_of': r.dt})
    if ghosts:
        print(f'  {len(ghosts)} nameless chart row(s) dropped, the men below each moved up one: '
              + '; '.join(ghosts))
    rows.sort(key=lambda r: (r['team'], POS_ORDER[r['pos']], r['depth']))
    teams = sorted({r['team'] for r in rows})
    if len(teams) != 32:
        sys.exit(f'FAILED: {len(teams)} teams on the newest chart, not 32: {teams}')
    have = {(r['team'], r['pos']) for r in rows if r['depth'] == 1}
    short = [f'{tm} {pos}' for tm in teams for pos in POS if (tm, pos) not in have]
    if short:
        sys.exit(f'FAILED: no depth-1 man at {short} on the newest chart.')
    return rows, stamps


def build_practice(inj_p, aged_from):
    """One row per man on the newest week's injury report. `aged_from` is the UTC datetime the
    report is aged against (Last-Modified, or the newest chart dt)."""
    import pandas as pd
    i = pd.read_csv(inj_p, low_memory=False)
    need = ['season_type', 'team', 'week', 'gsis_id', 'position', 'full_name', 'report_status',
            'practice_status', 'practice_primary_injury']
    missing = [c for c in need if c not in i.columns]
    if missing:
        sys.exit(f'FAILED: injuries_2026.csv is missing {missing}; its header is {list(i.columns)}.')
    i = i[i.season_type == 'REG']
    if i.empty:
        sys.exit('FAILED: the injuries feed holds no regular-season rows.')
    wk = int(i.week.max())
    i = i[i.week == wk].copy()
    now = datetime.datetime.now(datetime.timezone.utc)
    days_old = round((now - aged_from).total_seconds() / 86400, 1)
    s = lambda v: v if isinstance(v, str) else ''       # NaN to blank, never the string 'nan'
    rows = []
    for r in i.itertuples(index=False):
        rows.append({'team': tk(r.team), 'pos': s(r.position), 'player': s(r.full_name),
                     'name_key': norm(s(r.full_name)), 'gsis_id': s(r.gsis_id), 'week': wk,
                     'report_status': s(r.report_status), 'practice_status': s(r.practice_status),
                     'practice_injury': s(r.practice_primary_injury), 'days_old': days_old})
    rows.sort(key=lambda r: (r['team'], POS_ORDER.get(r['pos'], 9), r['player']))
    return rows, wk


def completed_weeks(src):
    """The newest completed week in form_2026.csv, to say whether the injury report is this
    week's or last week's. None when the file is absent."""
    p = os.path.join(src, 'form_2026.csv')
    if not os.path.exists(p):
        return None
    best = 0
    with open(p, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            try:
                if int(r.get('in_progress') or 0) == 0:
                    best = max(best, int(r['week']))
            except (TypeError, ValueError):
                pass
    return best or None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--probe', metavar='DIR', help='read both feeds from DIR; download nothing')
    a = ap.parse_args()
    cache = os.environ.get('FF_CACHE', HERE)
    os.makedirs(SRC, exist_ok=True)

    if a.probe:
        depth_p = os.path.join(a.probe, 'depth_charts_2026.csv')
        inj_p = os.path.join(a.probe, 'injuries_2026.csv')
        for p in (depth_p, inj_p):
            if not os.path.exists(p):
                sys.exit(f'FAILED: --probe given but {p} is not there.')
        inj_lm = None
        print(f'  PROBE run: feeds read from {a.probe}, nothing downloaded')
    else:
        os.makedirs(cache, exist_ok=True)
        depth_p, _ = fetch('depth_charts_2026.csv', FEEDS['depth_charts_2026.csv'], cache)
        inj_p, inj_lm = fetch('injuries_2026.csv', FEEDS['injuries_2026.csv'], cache)

    drows, stamps = build_depth(depth_p)
    newest_dt = datetime.datetime.strptime(stamps[-1], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
    if inj_lm is not None:
        aged_from, aged_how = inj_lm, 'the injuries feed HTTP Last-Modified header'
    else:
        aged_from, aged_how = newest_dt, 'the newest depth-chart dt (no Last-Modified this run)'
    prows, wk = build_practice(inj_p, aged_from)

    # THE KEY IS CHECKED ON THE NAMES IT WILL WRITE, not on a hand-picked probe list.
    assert_norm_matches([r['player'] for r in drows] + [r['player'] for r in prows])

    now = datetime.datetime.now(datetime.timezone.utc)
    chart_age = (now - newest_dt).total_seconds() / 86400
    if chart_age > STALE_DAYS:
        print(f'  WARNING: the newest chart snapshot is {stamps[-1]}, {chart_age:.1f} days old. The feed '
              f'rebuilds twice a day, so this is a stale feed, not a quiet week. Check the download.')

    dcols = ['team', 'pos', 'depth', 'player', 'name_key', 'gsis_id', 'espn_id', 'as_of']
    pcols = ['team', 'pos', 'player', 'name_key', 'gsis_id', 'week', 'report_status',
             'practice_status', 'practice_injury', 'days_old']
    dout = os.path.join(SRC, 'depth_daily.csv')
    pout = os.path.join(SRC, 'practice_2026.csv')
    # written to temp files and swapped in only once both are built, so a failed run leaves the
    # last good pair exactly as it was (build_form.py, doc 439)
    dtmp = write_tmp(dout, drows, dcols)
    ptmp = write_tmp(pout, prows, pcols)
    swap_in(dtmp, dout)
    swap_in(ptmp, pout)

    by_pos = {p: sum(1 for r in drows if r['pos'] == p) for p in POS}
    print(f'depth_daily.csv    {len(drows)} rows, 32 teams, {by_pos}')
    print(f'  chart as_of      : {stamps[-1]}' + ('' if len(stamps) == 1 else
          f'  (WARNING: {len(stamps)} different snapshots across teams, oldest {stamps[0]})'))
    print(f'  written          : {dout}')
    st = {}
    for r in prows:
        k = r['report_status'] or '(practice only)'
        st[k] = st.get(k, 0) + 1
    print(f'practice_2026.csv  {len(prows)} rows, week {wk} report, designations {st}')
    print(f'  days_old         : {prows[0]["days_old"] if prows else "?"}, measured from {aged_how} '
          f'({aged_from:%Y-%m-%d %H:%M} UTC). The feed carries NO per-row timestamp.')
    done = completed_weeks(SRC)
    if done is not None and wk <= done:
        print(f'  NOTE: form_2026.csv says week {done} is complete, so this week-{wk} report is LAST '
              f"week's final designation. The week-{done + 1} report starts on Wednesday; re-run then.")
    print(f'  written          : {pout}')
    print(f'  team codes via {TEAM_MAP_SOURCE}')
    print(f'  name_key via {NORM_SOURCE}' + ('' if norm is _norm_copy else
          f' (imported; the in-file copy agrees on all {len(drows) + len(prows)} names written)'))


if __name__ == '__main__':
    main()
