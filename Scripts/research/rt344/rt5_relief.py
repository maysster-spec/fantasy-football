#!/usr/bin/env python3
"""RED TEAM ITEM 5 -- reproduce seat.relief_ppg (12.13, n=51) and seat.weeks_played (3.02).

The constants say: NFL team-seasons 2022-2025 where the weeks-1-4 RB usage leader missed a week
between 5 and 14 and the direct backup had a line; his half-PPR per game in those weeks. Doc 276 adds:
the starter is out 3.3 weeks and the backup plays 3.0 of them. No script in the tree computes either
number, so this is a re-derivation from the stated population, with every choice the sentence leaves
open listed and tried:
  (a) per-event mean of the backup's ppg vs pooled games
  (b) 'missed a week' = no stat line in a week the team played (bye excluded), first absence only vs every absent week
  (c) usage leader by carries+targets over weeks 1-4; backup = second by the same measure
  (d) weeks 5-14 window for the absence
"""
import collections, csv, os, statistics
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))   # every path resolves against this file (0.4)
NFL = os.environ.get('RT_NFL', os.path.normpath(os.path.join(HERE, '..', '_nflverse_cache')))
if not os.path.exists(os.path.join(NFL, 'games.csv')):      # the cache holds players + stats only
    import urllib.request
    os.makedirs(NFL, exist_ok=True)
    with urllib.request.urlopen('https://github.com/nflverse/nflverse-data/releases/download/schedules/games.csv', timeout=300) as fh:
        body = fh.read()
    assert len(body) > 100000, 'games.csv download too small'
    open(os.path.join(NFL, 'games.csv'), 'wb').write(body)
SEASONS = (2022, 2023, 2024, 2025)

games = collections.defaultdict(set)     # (season, week) -> teams playing
for r in csv.DictReader(open(os.path.join(NFL, 'games.csv'), newline='', encoding='utf-8')):
    if r['game_type'] != 'REG':
        continue
    s, w = int(r['season']), int(r['week'])
    games[(s, w)].add(r['home_team']); games[(s, w)].add(r['away_team'])

def half(r):
    g = lambda k: float(r.get(k) or 0)
    return g('fantasy_points') + 0.5 * g('receptions')

lines = collections.defaultdict(dict)     # (season, team, gsis) -> week -> (touch, half, name)
for yr in SEASONS:
    for r in csv.DictReader(open(os.path.join(NFL, f'stats_player_week_{yr}.csv'), newline='', encoding='utf-8')):
        if r.get('season_type') != 'REG' or (r.get('position') or '') != 'RB':
            continue
        g = lambda k: float(r.get(k) or 0)
        lines[(yr, r['team'] if 'team' in r else r['recent_team'], r['player_id'])][int(r['week'])] = (
            g('carries') + g('targets'), half(r), r.get('player_display_name') or r.get('player_name'))

teams = collections.defaultdict(list)
for (yr, tm, g), wk in lines.items():
    teams[(yr, tm)].append((g, wk))

events = []
for (yr, tm), plist in teams.items():
    usage = sorted(((sum(wk[w][0] for w in wk if w <= 4), g, wk) for g, wk in plist), key=lambda x: -x[0])
    if len(usage) < 2 or usage[0][0] <= 0:
        continue
    lead_u, lead, lwk = usage[0]
    back_u, back, bwk = usage[1]
    played = [w for w in range(5, 15) if tm in games[(yr, w)]]
    absent = [w for w in played if w not in lwk]
    if not absent:
        continue
    # the backup's line in the weeks the leader was out
    bl = [(w, bwk[w][1]) for w in absent if w in bwk]
    events.append(dict(season=yr, team=tm, lead=lwk[max(lwk)][2] if lwk else lead, back=(bwk[max(bwk)][2] if bwk else back),
                       n_absent=len(absent), n_back_played=len(bl),
                       ppg=(statistics.mean(v for _, v in bl) if bl else None),
                       first_absent=min(absent), games=[v for _, v in bl]))

def report(sel, label):
    ev = [e for e in sel if e['ppg'] is not None]
    pooled = [v for e in ev for v in e['games']]
    print(f'  {label}: n_events={len(ev)}  per-event mean ppg={statistics.mean(e["ppg"] for e in ev):.2f}  '
          f'median={statistics.median(e["ppg"] for e in ev):.2f}  pooled per-game mean={statistics.mean(pooled):.2f} '
          f'(games {len(pooled)})  starter out {statistics.mean(e["n_absent"] for e in ev):.2f} wks, backup played '
          f'{statistics.mean(e["n_back_played"] for e in ev):.2f}')

print(f'team-seasons with a usage leader who missed a week 5-14: {len(events)}')
report(events, 'all events, every absent week')
report([e for e in events if e['n_absent'] >= 1 and e['season'] >= 2022], '2022-2025')
# stricter: backup must have a line in EVERY absent week?
strict = [dict(e, ppg=e['ppg']) for e in events if e['n_back_played'] == e['n_absent']]
report(strict, 'backup had a line in every absent week')
# the first spell only
def spells(e):
    return e
# variants on the leader definition: weeks 1-4 carries only
print('\nsensitivity, weeks 5-14 window, leader by weeks 1-4 carries+targets, backup second by the same:')
for lo_games in (1, 2, 3):
    report([e for e in events if e['n_back_played'] >= lo_games], f'backup played >= {lo_games} of the absent weeks')
