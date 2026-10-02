#!/usr/bin/env python3
r"""
build_inherit.py -- the seat, not the man.

Writes Source\inherit_2026.csv: for every NFL backfield, who holds the job, whether that job is
at risk, who is listed directly behind him, and whether you can still go and get him.

AND WHY IT NO LONGER GATES ON THE STARTER'S INJURY HISTORY (doc 276).  Doc 275 shipped a
fragility gate -- "the man ahead missed a game last season" -- and did not test it at the object it
uses.  Tested since, on 115 lead-back seasons 2022-2025 with the same player on file the year
before: a back who missed a game last season misses a week-1-to-14 game this season 45.9% of the
time, against 46.3% for one who played every game.  A difference of -0.4 points, p=0.60, and the
dose bands are non-monotone.  The gate carried nothing.
What the same number DOES say is the reason this list matters: 46% of lead backfields open up at
some point in weeks 1-14, every year, at every team.  The risk is near-universal, so it cannot rank
teams -- and every backfield with a claimable direct backup belongs on the list, sorted by the job.
A LIVE injury tag is a different object and is kept as its own column: it is this week's
information, not last season's, and nothing here has tested it.

WHY IT SORTS BY THE JOB AND NOT BY THE BACKUP (doc 275).  Directive 4.27's second gate -- the
backup's best consecutive two-week half-PPR stretch -- was measured FORWARD for the first time
here, on 62 real absences from 2022-2025 where a starter missed a week and the direct backup had
a line.  Nothing about the backup predicted what he then scored in relief:

    his best two weeks the season before   rho +0.006   p 0.97   n 39
    his own weeks 1-4 rate this season     rho +0.094   p 0.46   n 62
    his share of the backfield, weeks 1-4  rho +0.184   p 0.15   n 62
    what the starter he backs up scores    rho -0.056   p 0.66   n 62

So the two-week number stays as a FLOOR LABEL -- it separates a man who has played NFL football
from one who has not -- and never as a ranking.  What is forecastable in advance is whose job is
about to be empty and what that job pays, which is directive 4.20 arriving from a third side:
buy the job, never the name.

INPUTS, all under Source\ :
    depth_daily.csv                        [doc 441] TODAY'S order: ESPN's own depth chart via
                                           nflverse, rebuilt every run by research\wk1\
                                           build_depth_daily.py, one row per team x position x
                                           depth with espn_id and gsis_id on every man. When it
                                           exists it is the authority on WHO is the direct backup
                                           and the join to the pull is on espn_id, never a name.
                                           THE CAVEAT THE BUILDER MEASURED: ESPN lists the man
                                           PLAYING this week, not the job holder -- an injured
                                           starter is demoted (Achane RB3 at MIA, Jacobs RB4 at
                                           GB), so holds_the_job on a team like that is the
                                           stand-in and job_pays is HIS projection. The output
                                           carries chart_as_of so a reader can see which chart
                                           built it.
    2026_NFL_Depth_Charts_All_Teams.csv    the 8 August scrape, read ONLY when depth_daily.csv is
                                           absent, and the run says so. Joined by name, as before.
                                           ESPN's projection order disagrees with it on about a
                                           fifth of teams, and depth_map.csv built off the
                                           keeper-removed board cannot see four starters at all,
                                           so neither of those is used for the ordering.
    espn_projections_2026_*.csv (newest)   what the job pays, and the live injury tag.
    form_2025.csv                          games played and best two-week rate, 2025.
    WIRE_*.csv (newest)                    who is still free.  Optional: without it every row is
                                           reported with an unknown ownership rather than dropped.
    inherit_2026.csv (the previous one)    wk1_share / wk1_work / wk1_band are week-1 facts about
                                           the backup that no script in the tree writes any more;
                                           they are carried forward by next_man_id and left blank
                                           for a man who was not the next man last time (the sheet
                                           then prices him at the flat rate and says so).

Standard library only.  Every path resolves against this file, never the shell's directory.
"""
import csv, os, re, sys, glob, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
SRC  = os.path.join(ROOT, 'Source')
FLOOR = 11.2                      # doc 244's median relief rate.  A LABEL, not a ranking key.
ALIAS = {'ARZ': 'ARI', 'WAS': 'WSH'}          # depth-chart code -> ESPN pull code
TAGS  = [re.compile(p) for p in (r'^\d{2}/\d+$', r'^[A-Za-z]{1,2}/[A-Za-z]{2,4}$',
                                 r'^[A-Za-z]{2,3}\d{2}$', r'^U$', r'^IR$', r'^PS\d*$')]


def die(msg):
    print('  STOP: ' + msg)
    sys.exit(2)


def rd(path):
    with open(path, newline='', encoding='utf-8-sig') as fh:
        return list(csv.DictReader(fh))


def newest(pattern):
    hits = sorted(glob.glob(os.path.join(SRC, pattern)))
    return hits[-1] if hits else None


def num(x, default=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode()
    s = s.lower().replace('.', '').replace("'", '').replace('-', ' ')
    s = re.sub(r'\b(jr|sr|ii|iii|iv|v)\b', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def clean(v):
    """'Mason, Jordan T/SF' -> 'jordan mason'.  The tag can land in the middle after the split."""
    if ',' in v:
        last, first = v.split(',', 1)
        v = first.strip() + ' ' + last.strip()
    return norm(' '.join(t for t in v.split() if not any(p.match(t) for p in TAGS)))


def depth_chart():
    """The running-back order, team by team, as (chart, as_of, source).  chart[team] is the chain
    in depth order, each man a dict(id=espn_id or '', name=normalised name).  FB rows are NOT part
    of it: a fullback is not the man who inherits a running back's job, and folding them in is what
    put a fullback at depth 1 on twelve teams in depth_map.csv (doc 275).

    [doc 441] TODAY'S CHART FIRST.  Source\\depth_daily.csv (build_depth_daily.py, nflverse's copy
    of ESPN's chart, no fullbacks in it by construction) carries an espn_id on every man, so the
    chain joins to the pull on the id and the name is kept only for the report.  The August scrape
    is read only when the daily file is absent, by name as before, and the run prints which."""
    daily = os.path.join(SRC, 'depth_daily.csv')
    if os.path.exists(daily):
        out, stamps = {}, set()
        for r in rd(daily):
            if (r.get('pos') or '').strip().upper() != 'RB':
                continue
            pid = (r.get('espn_id') or '').strip()
            if not pid:
                continue                        # a slot with no man in it is not a man (doc 414)
            team = (r.get('team') or '').strip().upper()
            out.setdefault(team, []).append((int(float(r.get('depth') or 99)),
                                             dict(id=pid, name=norm(r.get('player') or ''))))
            stamps.add((r.get('as_of') or '').strip())
        out = {t: [m for _, m in sorted(chain, key=lambda x: x[0])] for t, chain in out.items()
               if len(chain) >= 2}
        if len(out) < 30:
            die('depth_daily.csv holds only %d backfields with two men -- expected 32; delete it '
                'to fall back to the August chart, or rebuild it.' % len(out))
        return out, (max(stamps) if stamps else 'unknown'), 'depth_daily.csv'

    path = os.path.join(SRC, '2026_NFL_Depth_Charts_All_Teams.csv')
    if not os.path.exists(path):
        die('Source\\depth_daily.csv AND Source\\2026_NFL_Depth_Charts_All_Teams.csv are both '
            'missing, not empty.  Run  py research\\wk1\\build_depth_daily.py')
    out = {}
    for r in rd(path):
        if (r.get('Pos') or '').strip().upper() != 'RB':
            continue
        team = (r.get('Team') or '').strip().upper()
        chain = [dict(id='', name=clean(v))
                 for k in ('Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5')
                 for v in [(r.get(k) or '').strip()] if v]
        if team and len(chain) >= 2:
            out.setdefault(team, chain)
    if len(out) < 30:
        die('parsed only %d backfields out of the depth chart -- expected 32.' % len(out))
    return out, '2026-08-08 (the August scrape)', '2026_NFL_Depth_Charts_All_Teams.csv'


def main():
    chart, chart_as_of, chart_src = depth_chart()

    ppath = newest('espn_projections_2026_*.csv')
    if not ppath:
        die('no espn_projections_2026_*.csv in Source.')
    pull, pull_by_id = {}, {}
    for r in rd(ppath):
        if r.get('pos') == 'RB':
            pull[(norm(r['Player']), (r.get('team') or '').strip().upper())] = r
            pull_by_id[(r.get('espn_id') or '').strip()] = r
    if len(pull) < 100:
        die('only %d running backs in %s -- that is not a full pull.' % (len(pull), os.path.basename(ppath)))

    def in_pull(man, team):
        """The pull row for a chain man: by espn_id when the chart carries one (section 3), by
        name + team only for the August scrape, which has no ids."""
        if man['id']:
            return pull_by_id.get(man['id'])
        return pull.get((man['name'], team))

    # The week-1 columns of the PREVIOUS file, carried forward by next_man_id (see the header).
    prev_path = os.path.join(SRC, 'inherit_2026.csv')
    prev_wk1 = {}
    if os.path.exists(prev_path):
        for r in rd(prev_path):
            prev_wk1[(r.get('next_man_id') or '').strip()] = {k: (r.get(k) or '') for k in
                                                              ('wk1_share', 'wk1_work', 'wk1_band')}

    fpath = os.path.join(SRC, 'form_2025.csv')
    if not os.path.exists(fpath):
        die('Source\\form_2025.csv is missing, not empty.')
    form = {r['espn_id']: r for r in rd(fpath)}

    wpath = newest('WIRE_*.csv')
    wire_by_id, wire_by_name = {}, {}
    for r in (rd(wpath) if wpath else []):
        wire_by_id[r['espn_id']] = r
        if r.get('pos') == 'RB':
            wire_by_name[(norm(r['player']), (r.get('team') or '').upper())] = r
    # [doc 441] THE WIRE IS THE PRICED POOL, NOT THE FREE POOL. WIRE_*.csv holds only the free men
    # the board rated; the free men it never rated are in FREE_UNRANKED_*.csv (doc 292), and
    # `free` below was reading absence from the first file as "rostered". Measured on the 29 Sept
    # chart: four of the ten next men the daily chart changed (Vaki, Goodson, Dillon, Sanders) are
    # free and unranked, and every one printed rostered, which sheet_engine's load_seats() then
    # drops from the page. The unranked file carries owned_pct and no bye.
    upath = newest('FREE_UNRANKED_*.csv')
    for r in (rd(upath) if upath else []):
        if r.get('pos') == 'RB' and r['espn_id'] not in wire_by_id:
            wire_by_id[r['espn_id']] = {'espn_id': r['espn_id'], 'player': r['player'], 'pos': 'RB',
                                        'team': r.get('team', ''), 'owned_pct': r.get('owned_pct', ''),
                                        'bye': ''}

    npath = os.path.join(ROOT, 'Scripts', 'news_overrides.csv')
    news = {r['espn_id']: r for r in rd(npath)} if os.path.exists(npath) else {}
    # [doc 453] THE HOLDER'S TAG COMES FROM THE LIVE READS, NOT THE WEEKLY PULL. `injuryStatus` in the
    # projection pull is as old as the pull (six days on 29 Sept, with Achane still ACTIVE in it);
    # LEAGUE_ROSTERS.csv (every owned man, ESPN's own status, the last wire run) and news_2026.csv
    # (ESPN's injuries feed) are hours old at worst. The pull's field is the last resort.
    live_status = {}
    lpath = os.path.join(SRC, 'LEAGUE_ROSTERS.csv')
    for r in (rd(lpath) if os.path.exists(lpath) else []):
        if r.get('espn_id') and (r.get('status') or '').strip():
            live_status[str(r['espn_id']).strip()] = r['status'].strip().upper()
    for r in (rd(wpath) if wpath else []):
        if r.get('espn_id') and (r.get('status') or '').strip():
            live_status.setdefault(str(r['espn_id']).strip(), r['status'].strip().upper())
    _NEWS_TAG = {'INJURED RESERVE': 'INJURY_RESERVE', 'OUT': 'OUT', 'DOUBTFUL': 'DOUBTFUL',
                 'QUESTIONABLE': 'QUESTIONABLE', 'SUSPENDED': 'SUSPENSION', 'SUSPENSION': 'SUSPENSION',
                 'PHYSICALLY UNABLE TO PERFORM': 'PUP', 'PUP': 'PUP'}
    n2path = os.path.join(SRC, 'news_2026.csv')
    for r in (rd(n2path) if os.path.exists(n2path) else []):
        t_ = _NEWS_TAG.get((r.get('status') or '').strip().upper())
        if r.get('espn_id') and t_:
            live_status.setdefault(str(r['espn_id']).strip(), t_)

    rows, broken, stand_ins = [], [], []
    for code, chain in sorted(chart.items()):
        team = ALIAS.get(code, code)
        held = in_pull(chain[0], team)
        if held is None:
            broken.append((code, 1, chain[0]['name']))
            continue
        nxt, src = in_pull(chain[1], team), 'pull'
        if nxt is None:                       # fall back to the live wire -- NEVER to the third man
            w = (wire_by_id.get(chain[1]['id']) if chain[1]['id']
                 else wire_by_name.get((chain[1]['name'], team)))
            if w and w.get('pos') == 'RB':
                nxt = {'Player': w['player'], 'espn_id': w['espn_id'], 'proj_2026': ''}
                src = 'wire'
        if nxt is None:
            broken.append((code, 2, chain[1]['name']))
            continue

        # [doc 453] THE STAND-IN CASE, RESOLVED: the job belongs to the absent starter, not to the man
        # the chart lists this week. Doc 441 flagged it and left the number as the stand-in's, calling
        # the pricing a rule decision; doc 451 made it: a job whose holder is out for weeks is OPEN and
        # THE CALL prices it from the wire's lane, and the seat list cuts it by name (doc 411). So the
        # row names the absent starter as the holder, with his projection and his tag, and the seat
        # list does the right thing with it. Left as the stand-in's, the row sat under the cap unnamed
        # (Wright at 24 for Achane's 260 on 29 Sept) and, had the stand-in gone down, would have priced
        # a 260 job at 24. Same threshold as before (a chain-mate projected 40+ above the chart RB1).
        stand_in_note = ''
        best = max(((num(in_pull(m, team) and in_pull(m, team).get('proj_2026')), m['name'], k)
                    for k, m in enumerate(chain, 1) if in_pull(m, team)), default=(0.0, '', 0))
        if best[2] > 1 and best[0] - num(held['proj_2026']) > 40:
            deeper_row = in_pull(chain[best[2] - 1], team)
            stand_in_note = ('; the chart lists %s RB1 this week (%.1f) with %s demoted to RB%d; the job is his '
                             'and the row prices it' % (held['Player'], num(held['proj_2026']), deeper_row['Player'], best[2]))
            stand_ins.append((code, held['Player'], deeper_row['Player'], best[2]))
            held = deeper_row
        fh = form.get(held['espn_id'], {})
        g25 = fh.get('g25', '')
        tag = news.get(held['espn_id'], {}).get('action', '')
        if not tag:
            live = live_status.get(str(held['espn_id']).strip()) or (held.get('injuryStatus') or '').strip().upper()
            tag = live if live not in ('ACTIVE', '') else ''
        # A FACT, NOT A GATE (doc 276). Last season's games missed does not predict this season's,
        # so it is printed and never filtered on. The live tag is separate and current.
        # THE FINDING THIS APPLIES: finding 4.25b, doc 203 and doc 204. Age acts through availability,
        # and the availability read (games last season, starter_g25 below, with `why` spelling it out)
        # is a warning on a young or unestablished starter and close to noise on a ten-year veteran;
        # the seat lane prints it as the man ahead's record and never sorts or filters on it. `at_risk`
        # is the LIVE tag, a separate and current channel. check_inputs.py lists a finding no script
        # cites; this is the citation, and the lines below are the implementation.
        if g25 == '':
            why = 'no 2025 NFL record'
        elif int(g25) < 17:
            miss = 17 - int(g25)
            why = 'missed %d game%s in 2025' % (miss, '' if miss == 1 else 's')
        else:
            why = 'played all 17 in 2025'
        # [doc 441] THE STAND-IN CASE, FLAGGED AND NOT REPRICED. ESPN's chart lists the man playing
        # this week, so on a team whose starter is demoted (Achane RB3 at MIA, Jacobs RB4 at GB)
        # holds_the_job is the stand-in and job_pays is HIS projection (24.0 at MIA against
        # Achane's 260.3). Measured on the 29 Sept chart against the 24 Sept pull: the chart RB1's
        # projection differs from the best projection in his chain on exactly those two teams and
        # on no other, and the chain's best equals the team's best in the pull on all 32. The
        # threshold is depth_map.py's own (doc 307: a fall over 40 fired on one team and could not
        # reach the noise). The number is left as the holder's on purpose -- whether a seat behind
        # a stand-in is priced at the stand-in's job or the absent starter's is a rule decision
        # (sheet_engine's doc 411 cuts a seat whose starter is already out) -- and the row says so
        # where a reader will see it.
        why += stand_in_note
        risk = 'live tag' if tag else 'baseline'

        fb = form.get(nxt['espn_id'], {})
        b2 = fb.get('best_2wk', '')
        floor = ('no NFL weeks' if b2 in ('', None)
                 else ('clears' if num(b2) >= FLOOR else 'thin'))
        free = nxt['espn_id'] in wire_by_id
        wk1 = prev_wk1.get(nxt['espn_id'], {})
        rows.append(dict(
            team=code, holds_the_job=held['Player'], starter_g25=g25, job_pays=round(num(held['proj_2026']), 1),
            at_risk=risk, live_tag=(tag.lower() if tag else ''), why=why,
            next_man=nxt['Player'], next_man_id=nxt['espn_id'], source=src,
            best_2wk_2025=b2, floor=floor, free=('yes' if free else 'rostered'),
            owned_pct=wire_by_id.get(nxt['espn_id'], {}).get('owned_pct', ''),
            bye=wire_by_id.get(nxt['espn_id'], {}).get('bye', ''),
            wk1_share=wk1.get('wk1_share', ''), wk1_work=wk1.get('wk1_work', ''),
            wk1_band=wk1.get('wk1_band', ''), chart_as_of=chart_as_of))

    if not rows:
        die('no backfields survived -- refusing to write an empty list.')
    rows.sort(key=lambda r: -r['job_pays'])

    out = os.path.join(SRC, 'inherit_2026.csv')
    with open(out, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print('  depth chart      : %d backfields from %s, as of %s' % (len(chart), chart_src, chart_as_of))
    if chart_src != 'depth_daily.csv':
        print('  WARNING          : depth_daily.csv is absent, so this is the 8 August order -- run '
              'py research\\wk1\\build_depth_daily.py')
    carried = sum(1 for r in rows if r['wk1_band'])
    print('  week-1 columns   : carried forward for %d of %d next men from the previous file'
          % (carried, len(rows)))
    if stand_ins:
        print('  STAND-IN RB1     : ' + '; '.join('%s: the chart has %s RB1, %s (RB%d on the chart) holds the job in the row' % s_ for s_ in stand_ins)
              + ' -- the absent starter is the holder (doc 453)')
    print('  projections      : %s' % os.path.basename(ppath))
    print('  free pool        : %s + %s' % (os.path.basename(wpath) if wpath else 'NONE -- ownership unknown',
                                          os.path.basename(upath) if upath else 'no FREE_UNRANKED file'))
    print('  wrote            : Source\\inherit_2026.csv  (%d rows)' % len(rows))
    if broken:
        print('  JOIN BROKEN on %d name%s -- those teams are NOT in the list, and the third man was'
              ' not promoted in their place:' % (len(broken), '' if len(broken) == 1 else 's'))
        for code, slot, name in broken:
            print('     %-4s RB%d  "%s" is in neither the pull nor the wire' % (code, slot, name))

    live = [r for r in rows if r['free'] == 'yes']
    print('\n  EVERY CLAIMABLE SEAT (%d) -- ordered by what the job pays.  About 46%% of lead'
          '\n  backfields open up in weeks 1-14 and that rate does not vary by history, so the'
          '\n  ordering is the job and nothing else:' % len(live))
    for i, r in enumerate(live, 1):
        print('   %-3d%-4s%-26s%-7s%-24s%-22s%-7s%-9s%s' % (
            i, r['team'], r['holds_the_job'][:24], r['job_pays'], r['why'][:22],
            r['next_man'][:20], r['owned_pct'], r['floor'], r['live_tag']))
    print('\n  The floor column is a label, not a ranking -- nothing about the backup predicted'
          '\n  his relief scoring on 62 measured absences.  Take the seat, not the form.')


if __name__ == '__main__':
    main()
