"""
ir_return_rate.py  --  how long does a parked IR seat hold?

PRE-REGISTERED FORM (directive 0.5a2), written before the run:

  POPULATION  offensive skill players (QB/RB/WR/TE) carrying report_status == 'Out'
              on the final official NFL injury report of regular-season week w,
              seasons 2021-2025, whose team also plays a regular-season game in
              week w+1 (bye weeks excluded and counted separately).

  OUTCOME 1   his report_status in week w+1: Out / Doubtful / Questionable / none.
  OUTCOME 2   did he take at least one offensive snap in week w+1.

  DIRECTION   this is a BASE RATE, not a hypothesis test.  Nothing is being
              confirmed or killed.  The number prices one thing: how often the
              seat a 'Out' player is parked in has to be given back after a
              single week.  A high return rate makes the parked seat a one-week
              loan; a low one makes it a month.

  FALSIFIER   n/a.  If the rate cannot be computed on n >= 300 the answer is
              'blocked', not a number.

  JOIN        gsis_id -> pfr_id through nflverse players.csv, then pfr_player_id
              in snap_counts.  No name join (directive 3, identity rule).

  KNOWN GAP   a player placed on NFL injured reserve leaves the 53 and stops
              appearing on the weekly report entirely.  He shows here as
              'no designation, no snaps', which is NOT the same as cleared.
              The run separates the two by looking 4 weeks forward.
"""
import glob, os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
# doc 144: resolve against the script's own location, never the shell's. Same convention as
# wk1/wopr_spike.py -- look in the shared nflverse cache first, then beside this file.
CACHE = os.environ.get('FF_CACHE') or os.path.normpath(os.path.join(HERE, '..', '_nflverse_cache'))


def _find(name):
    for d in (CACHE, HERE):
        q = os.path.join(d, name)
        if os.path.exists(q):
            return q
    raise SystemExit(
        f"missing {name}. Put the nflverse files in {CACHE} (or beside this script):\n"
        "  injuries/injuries_<season>.csv -> inj_<season>.csv\n"
        "  snap_counts_<season>.csv, players.csv")

SEASONS = (2021, 2022, 2023, 2024, 2025)
SKILL = ('QB', 'RB', 'WR', 'TE', 'FB')

inj = pd.concat([pd.read_csv(_find(f'inj_{s}.csv'), low_memory=False)
                 for s in SEASONS], ignore_index=True)
_pre = set(inj['season'].unique())
inj = inj[inj['game_type'] == 'REG'].copy()
_post = set(inj['season'].unique())
assert _pre == _post, f"REG filter dropped whole seasons {sorted(_pre-_post)} -- schema drift, see 2021-2024 vs 2025 headers"
print('seasons surviving the REG filter:', sorted(_post))
inj['report_status'] = inj['report_status'].fillna('NONE')

snaps = pd.concat([pd.read_csv(_find(f'snaps_{s}.csv'), low_memory=False)
                   for s in SEASONS], ignore_index=True)
snaps = snaps[snaps['game_type'] == 'REG'].copy()

players = pd.read_csv(_find('players.csv'), low_memory=False)
g2p = players.dropna(subset=['gsis_id', 'pfr_id']).set_index('gsis_id')['pfr_id'].to_dict()

# who played, by (season, week, pfr_id)
played = set()
for r in snaps[snaps['offense_snaps'] > 0][['season', 'week', 'pfr_player_id']].itertuples(index=False):
    played.add((r.season, r.week, r.pfr_player_id))

# which teams played which week (bye detection)
team_week = set((r.season, r.week, r.team) for r in snaps[['season', 'week', 'team']].itertuples(index=False))

# every status row, keyed
status = {}
for r in inj[['season', 'week', 'gsis_id', 'report_status']].itertuples(index=False):
    status[(r.season, r.week, r.gsis_id)] = r.report_status

sk = inj[inj['position'].isin(SKILL)].copy()
out_rows = sk[sk['report_status'] == 'Out']

rec = []
for r in out_rows.itertuples(index=False):
    s, w, gid, team, pos = r.season, r.week, r.gsis_id, r.team, r.position
    pid = g2p.get(gid)
    nxt = w + 1
    if nxt > 18:
        continue
    bye = (s, nxt, team) not in team_week
    st_next = status.get((s, nxt, gid), 'NONE')
    # consecutive weeks already Out coming in
    streak = 0
    k = w
    while status.get((s, k, gid)) == 'Out':
        streak += 1
        k -= 1
    # played next week?
    pl = (s, nxt, pid) in played if pid else None
    # played at all in the next four weeks? (separates NFL-IR from cleared)
    pl4 = any(((s, w + j, pid) in played) for j in (1, 2, 3, 4)) if pid else None
    rec.append(dict(season=s, week=w, gsis_id=gid, pos=pos, team=team,
                    streak=streak, bye=bye, st_next=st_next, played_next=pl, played_4wk=pl4))

d = pd.DataFrame(rec)
print(f"Out rows, skill positions, REG, 2021-2025, with a week w+1 in the regular season: n={len(d)}")
print(f"  unmatched to a pfr_id (dropped from the snap half): {d['played_next'].isna().sum()}")
print(f"  team on bye in w+1: {d['bye'].sum()} ({d['bye'].mean():.1%})")
print()

live = d[~d['bye'] & d['played_next'].notna()].copy()
print(f"=== A. HE PLAYS IN WEEK w+1  (team plays, n={len(live)}) ===")
print(f"  played a snap in w+1:            {live['played_next'].mean():.1%}")
print(f"  still carried 'Out' in w+1:      {(live['st_next']=='Out').mean():.1%}")
print(f"  carried Doubtful in w+1:         {(live['st_next']=='Doubtful').mean():.1%}")
print(f"  carried Questionable in w+1:     {(live['st_next']=='Questionable').mean():.1%}")
print(f"  no designation at all in w+1:    {(live['st_next']=='NONE').mean():.1%}")
print()

print("=== B. BY HOW MANY STRAIGHT WEEKS HE HAS ALREADY BEEN OUT ===")
print(f"{'weeks Out':>10} {'n':>6} {'plays w+1':>10} {'still Out':>10} {'no design.':>11}")
for k in (1, 2, 3, 4):
    sub = live[live['streak'] == k] if k < 4 else live[live['streak'] >= 4]
    lbl = str(k) if k < 4 else '4+'
    if len(sub) == 0:
        continue
    print(f"{lbl:>10} {len(sub):>6} {sub['played_next'].mean():>9.1%} "
          f"{(sub['st_next']=='Out').mean():>9.1%} {(sub['st_next']=='NONE').mean():>10.1%}")
print()

print("=== C. BY POSITION (all streaks) ===")
print(f"{'pos':>5} {'n':>6} {'plays w+1':>10} {'still Out':>10}")
for p in ('QB', 'RB', 'WR', 'TE'):
    sub = live[live['pos'] == p]
    if len(sub) < 20:
        continue
    print(f"{p:>5} {len(sub):>6} {sub['played_next'].mean():>9.1%} {(sub['st_next']=='Out').mean():>9.1%}")
print()

print("=== D. THE 'NO DESIGNATION, NO SNAPS' CELL  (is he on NFL IR, or just cleared and benched?) ===")
ghost = live[(live['st_next'] == 'NONE') & (~live['played_next'])]
print(f"  n={len(ghost)} ({len(ghost)/len(live):.1%} of all Out rows with a live w+1)")
print(f"  of those, played at some point in the NEXT FOUR weeks: {ghost['played_4wk'].mean():.1%}")
print(f"  never played in the next four weeks (reads as NFL IR): {1-ghost['played_4wk'].mean():.1%}")
print()

print("=== E. THE SEAT'S LIFE: given Out in w, how far does the parked seat hold? ===")
print("  share of Out-in-w players who are STILL not playing, k weeks later")
first = d[(d['streak'] == 1) & d['played_next'].notna()].copy()
print(f"  (population: the week he FIRST went Out, n={len(first)})")
for k in range(1, 6):
    col = []
    for r in first.itertuples(index=False):
        pid = g2p.get(r.gsis_id)
        if not pid or r.week + k > 18:
            continue
        col.append(not any(((r.season, r.week + j, pid) in played) for j in range(1, k + 1)))
    if col:
        print(f"    still had not played by w+{k}: {sum(col)/len(col):>6.1%}   (n={len(col)})")
