"""practice_out.py -- what the injury report's designation and practice status are worth as a "not playing this
week" signal, 2021 to 2025 (claude_todo: "should the practice report's Out be next_man_up()'s step-past trigger
beside ESPN's injuryStatus?").

TESTABLE FORM (stated before the numbers): population = RB/WR/TE player-weeks 2021-2025 REG with a row on that
week's injury report (nflverse injuries_YYYY.csv, one row per man per week, the week's latest report), joined to
snap counts on gsis_id; predictor = report_status (Out / Doubtful / Questionable / none) crossed with
practice_status (DNP / Limited / Full) as the final report carried them; outcome = played an offensive snap that
week (snap counts; a man with no snap row and no stat line did not play); direction = Out and DNP-without-
designation predict not playing, Questionable does not; DECISION it feeds: whether next_man_up() should step past
a Doubtful man (it steps past Out, IR, suspended and not-active today and keeps Questionable and Doubtful on
purpose), and whether DNP-with-no-designation earns a flag. WHAT IT CANNOT TEST: the practice report against
ESPN's live injuryStatus, because no history of ESPN's status exists here; see the BLOCKED line at the end.
Standard library plus pandas and numpy only.
"""
import os, sys, urllib.request
import pandas as pd, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get('FF_CACHE') or os.path.normpath(os.path.join(HERE, '..', '_nflverse_cache'))
NFLV = 'https://github.com/nflverse/nflverse-data/releases/download/'

def _get(name, url):
    q = os.path.join(CACHE, name)
    if os.path.exists(q) and os.path.getsize(q) > 1000:
        return q
    os.makedirs(CACHE, exist_ok=True)
    print(f'  fetching {name}')
    with urllib.request.urlopen(url, timeout=180) as fh:
        body = fh.read()
    if len(body) < 1000:
        raise SystemExit(f'FAILED: {url} returned {len(body)} bytes')
    open(q, 'wb').write(body)
    return q

inj = pd.concat([pd.read_csv(_get(f'injuries_{s}.csv', NFLV + f'injuries/injuries_{s}.csv'), low_memory=False)
                 for s in range(2021, 2026)])
inj = inj[(inj.game_type == 'REG') & (inj.position.isin(['RB', 'WR', 'TE']))].copy()   # game_type is on every year; season_type only on 2025
inj = inj.drop_duplicates(['season', 'week', 'gsis_id'])
print(f'injury-report rows, RB/WR/TE, REG 2021-2025: {len(inj)}  (one per man per week; the week\'s latest report)')

sn = pd.concat([pd.read_csv(_get(f'snaps_{s}.csv', NFLV + f'snap_counts/snap_counts_{s}.csv'), low_memory=False)
                for s in range(2021, 2026)])
sn = sn[sn.game_type == 'REG']
pl = pd.read_csv(_get('players.csv', NFLV + 'players/players.csv'), low_memory=False)[['gsis_id', 'pfr_id']].dropna().drop_duplicates('pfr_id')
sn = sn.merge(pl, left_on='pfr_player_id', right_on='pfr_id', how='inner')
sn = sn.groupby(['season', 'week', 'gsis_id'], as_index=False).offense_snaps.max()
st = pd.concat([pd.read_csv(_get(f'stats_player_week_{s}.csv', NFLV + f'stats_player/stats_player_week_{s}.csv'),
                            low_memory=False)[['season', 'week', 'player_id', 'targets', 'carries']] for s in range(2021, 2026)])
st = st.rename(columns={'player_id': 'gsis_id'})
d = inj.merge(sn, on=['season', 'week', 'gsis_id'], how='left').merge(st, on=['season', 'week', 'gsis_id'], how='left')
d['played'] = (d.offense_snaps.fillna(0) > 0) | ((d.targets.fillna(0) + d.carries.fillna(0)) > 0)
# a bye week for the team: the report row exists but there is no game; drop weeks where the team had no snap rows at all
teamweeks = pd.concat([pd.read_csv(_get(f'snaps_{s}.csv', NFLV + f'snap_counts/snap_counts_{s}.csv'), low_memory=False)
                       for s in range(2021, 2026)])
teamweeks = teamweeks[teamweeks.game_type == 'REG'][['season', 'week', 'team']].drop_duplicates()
d = d.merge(teamweeks.assign(had_game=1), on=['season', 'week', 'team'], how='left')
nb = int(d.had_game.isna().sum())
d = d[d.had_game == 1]
print(f'dropped {nb} rows whose team had no game that week (a bye); n={len(d)}')

d['rs'] = d.report_status.fillna('none')
d['ps'] = d.practice_status.fillna('none').str.replace('Did Not Participate In Practice', 'DNP') \
           .str.replace('Limited Participation in Practice', 'Limited').str.replace('Full Participation in Practice', 'Full')
print('\n(a) played that week, by the final report\'s game designation (RB/WR/TE):')
for rs in ['Out', 'Doubtful', 'Questionable', 'none']:
    q = d[d.rs == rs]
    print(f'  {rs:13s} played {q.played.mean()*100:5.1f}%  (n={len(q)})')
print('\n(b) the designation crossed with the practice status on that final report, played %:')
tab = d.groupby(['rs', 'ps']).played.agg(['mean', 'size'])
for (rs, ps), r in tab.iterrows():
    if r['size'] >= 30:
        print(f'  {rs:13s} {ps:8s} played {r["mean"]*100:5.1f}%  (n={int(r["size"])})')
print('\n(c) by position, the two cells the decision turns on:')
for pos in ['RB', 'WR', 'TE']:
    q = d[d.position == pos]
    dbt = q[q.rs == 'Doubtful']; dnp = q[(q.rs == 'none') & (q.ps == 'DNP')]; qst = q[q.rs == 'Questionable']
    print(f'  {pos}: Doubtful played {dbt.played.mean()*100:5.1f}% (n={len(dbt)})   DNP, no designation played '
          f'{dnp.played.mean()*100:5.1f}% (n={len(dnp)})   Questionable played {qst.played.mean()*100:5.1f}% (n={len(qst)})')
print('\n(d) by season, Doubtful and DNP-no-designation, played %:')
for s in range(2021, 2026):
    q = d[d.season == s]
    dbt = q[q.rs == 'Doubtful']; dnp = q[(q.rs == 'none') & (q.ps == 'DNP')]
    print(f'  {s}: Doubtful {dbt.played.mean()*100:5.1f}% (n={len(dbt)})   DNP no designation {dnp.played.mean()*100:5.1f}% (n={len(dnp)})')
print('\n(e) how far ahead a designation reaches: of men Out in week w, share not playing in w+1 and w+2 (their team had a game):')
key = d.set_index(['season', 'gsis_id', 'week']).played
allw = pd.concat([pd.read_csv(_get(f'stats_player_week_{s}.csv', NFLV + f'stats_player/stats_player_week_{s}.csv'),
                              low_memory=False)[['season', 'week', 'player_id']] for s in range(2021, 2026)])
played_any = set(zip(allw.season, allw.player_id, allw.week))
snap_any = set(zip(sn[sn.offense_snaps > 0].season, sn[sn.offense_snaps > 0].gsis_id, sn[sn.offense_snaps > 0].week))
tw = set(zip(teamweeks.season, teamweeks.team, teamweeks.week))
for rs in ['Out', 'Doubtful']:
    q = d[d.rs == rs]
    for k in (1, 2):
        had = q[[(s, t, w + k) in tw for s, t, w in zip(q.season, q.team, q.week)]]
        np_ = [not (((s, g, w + k) in played_any) or ((s, g, w + k) in snap_any)) for s, g, w in zip(had.season, had.gsis_id, had.week)]
        print(f'  {rs:9s} w+{k}: still not playing {np.mean(np_)*100:5.1f}% (n={len(had)})')
print('\nBLOCKED, input named: the practice report against ESPN\'s live injuryStatus cannot be compared on history, because '
      'no history of ESPN\'s status exists in any file here. The input that settles it is ESPN\'s injuryStatus for every '
      'free RB/WR/TE recorded at each ff.bat run beside that day\'s report_status and practice_status, going forward; '
      'wire.py reads both every run and can log the pair.')
print('done')
