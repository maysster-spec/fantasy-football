"""
ir_seat_validity.py  --  when does the ESPN IR seat actually become invalid?

Doc 399, directive v9.22, batch D1 of doc 397's red-team catalog.

WHY THIS EXISTS.  ir_return_rate.py (doc 391) priced the seat by asking when the
parked man TAKES A SNAP.  That is not the event.  ESPN's own football help, read
as page text at v9.19 (doc 394), says the IR slot is invalidated only when the
player goes "from OUT to no longer having an injury designation"; an update
"from OUT or IR to QUESTIONABLE or DOUBTFUL" leaves the roster "NOT invalid".
So the seat survives a downgrade, and it survives NFL injured reserve, because
ESPN accepts the IR status in that slot.

PRE-REGISTERED FORM (directive 0.5a2), written before the run:

  POPULATION  identical to ir_return_rate.py, and the run REPRODUCES that
              script's headline rates before measuring anything new.  QB/RB/WR/
              TE/FB carrying report_status == 'Out' on the final official report
              of REG week w, seasons 2021-2025, whose team also plays in w+1.

  OUTCOME     the first week k in 1..5 at which the seat is INVALID, defined as:
                designation in {Out, Doubtful, Questionable}  -> seat VALID
                no designation AND he played                  -> seat INVALID
                no designation AND dark for 3 more weeks      -> reads as NFL IR,
                                                                 seat VALID
                no designation, did not play, plays later     -> seat INVALID
              bye weeks are skipped, not counted as either.

  DIRECTION   NOT PREDICTED.  Two mechanisms push opposite ways: a Questionable
              downgrade keeps a seat the old measure killed, and losing the
              designation without playing kills a seat the old measure kept.
              38.2% of Out players already carry no designation in w+1, so the
              net is an open question and the run decides it.

  FALSIFIER   if the two curves agree within a couple of points at every step,
              the published number stands and D1 is closed as a null.

  KNOWN GAP   the NFL-IR arm is a PROXY.  nflverse drops a player off the weekly
              report when he leaves the 53, so 'no designation' conflates
              cleared-and-healthy with on-IR-and-gone.  ESPN's own injuryStatus
              settles it directly and STATUS_LOG.csv (doc 393) begins recording
              it this season.  Until then, treat the SOURCED curve as the better
              of two imperfect measures, not as exact.

RESULT (doc 399): the published curve could not be reproduced under ANY of six
population definitions and is RETRACTED, not patched.  The headline rates
reproduce to the decimal, so the defect is in the curve.  Against the right
event the seat is SAFER in w+1 (75.5% valid vs 70.4% not-playing) and SHORTER
from w+3 (35.2% vs 41.9%).  The median still dies between two and three weeks.
New and actionable: the roster is invalid, and the lineup frozen, the following
Sunday 24.5% of the time.  The position ordering INVERTS.
"""
import os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get('FF_CACHE') or os.path.normpath(os.path.join(HERE, '..', '_nflverse_cache'))
SEASONS = (2021, 2022, 2023, 2024, 2025)
SKILL = ('QB', 'RB', 'WR', 'TE', 'FB')
DESIG = {'OUT', 'DOUBTFUL', 'QUESTIONABLE'}


def _find(name):
    for d in (CACHE, HERE):
        q = os.path.join(d, name)
        if os.path.exists(q):
            return q
    raise SystemExit(f"missing {name}. Put the nflverse files in {CACHE} (or beside this script).")


def load():
    inj = pd.concat([pd.read_csv(_find(f'inj_{s}.csv'), low_memory=False) for s in SEASONS],
                    ignore_index=True)
    pre = set(inj['season'].unique())
    inj = inj[inj['game_type'] == 'REG'].copy()
    # doc 391's own defect: 2021-24 carry game_type, 2025 carries season_type. Assert, never trust.
    assert pre == set(inj['season'].unique()), "REG filter dropped whole seasons -- schema drift"
    inj['report_status'] = inj['report_status'].fillna('NONE')
    inj = inj[inj['position'].isin(SKILL)].copy()

    snaps = pd.concat([pd.read_csv(_find(f'snaps_{s}.csv'), low_memory=False) for s in SEASONS],
                      ignore_index=True)
    snaps = snaps[snaps['game_type'] == 'REG'].copy()

    players = pd.read_csv(_find('players.csv'), low_memory=False)
    g2p = players.dropna(subset=['gsis_id', 'pfr_id']).set_index('gsis_id')['pfr_id'].to_dict()

    played = set((r.season, r.week, r.pfr_player_id)
                 for r in snaps[snaps['offense_snaps'] > 0][['season', 'week', 'pfr_player_id']]
                 .itertuples(index=False))
    team_week = set((r.season, r.week, r.team)
                    for r in snaps[['season', 'week', 'team']].itertuples(index=False))
    status = {(r.season, r.week, r.gsis_id): str(r.report_status).strip().upper()
              for r in inj[['season', 'week', 'gsis_id', 'report_status']].itertuples(index=False)}
    outs = (inj[inj['report_status'].str.strip().str.upper() == 'OUT']
            [['season', 'week', 'gsis_id', 'team', 'position']]
            .drop_duplicates(subset=['season', 'week', 'gsis_id']))
    return status, played, team_week, outs, g2p


def build(status, played, team_week, g2p, origins, require_next=True, horizon=9):
    rows = []
    for r in origins.itertuples(index=False):
        s, w, gid, tm, pos = r.season, r.week, r.gsis_id, r.team, r.position
        if require_next and (s, w + 1, tm) not in team_week:
            continue
        pid = g2p.get(gid)
        seq = []
        for k in range(1, horizon + 1):
            bye = (s, w + k, tm) not in team_week
            seq.append(('BYE' if bye else status.get((s, w + k, gid), 'NONE'),
                        (not bye) and pid is not None and ((s, w + k, pid) in played)))
        rows.append((pos, seq))
    return rows


def invalid_week(seq):
    """first k in 1..5 at which the IR seat is invalid, or None."""
    for k, (d, p) in enumerate(seq[:5], 1):
        if d == 'BYE' or d in DESIG:
            continue
        if p:
            return k, 'played'
        future = [x for x in seq[k:k + 3] if x[0] != 'BYE']
        if future and not any(pp for _, pp in future):
            continue                      # reads as NFL IR; ESPN accepts the IR status
        return k, 'cleared, did not play'
    return None, None


def main():
    status, played, team_week, outs, g2p = load()
    rows = build(status, played, team_week, g2p, outs)
    n = len(rows)

    print(f"population n = {n}   (doc 391 published 1,431)")
    p1 = [sq[0] for _, sq in rows]
    from collections import Counter
    c = Counter(d for d, _ in p1)
    print("\n--- REPRODUCTION CHECK against doc 391, before anything new is measured ---")
    print(f"  plays a snap w+1   {sum(1 for _, p in p1 if p)/n*100:5.1f}%   (published 29.6)")
    for k, pub in (('OUT', 38.9), ('QUESTIONABLE', 19.5), ('DOUBTFUL', 3.4), ('NONE', 38.2)):
        print(f"  {k:14}     {c[k]/n*100:5.1f}%   (published {pub})")

    res = [(pos,) + invalid_week(sq) for pos, sq in rows]
    valid = [sum(1 for r in res if r[1] is None or r[1] > k) / n * 100 for k in range(1, 6)]
    notplay = [sum(1 for _, sq in rows if not any(p for _, p in sq[:k])) / n * 100 for k in range(1, 6)]
    print("\n--- THE TWO CURVES ---")
    print("  seat still VALID (sourced event) : " + "  ".join(f"{x:5.1f}" for x in valid))
    print("  still not playing (old measure)  : " + "  ".join(f"{x:5.1f}" for x in notplay))
    print("  doc 391's published curve        :   73.8   53.8   40.8   31.2   23.8  <- reproduces under none")

    w1 = [r for r in res if r[1] == 1]
    print(f"\n  SEAT INVALID AT w+1: {len(w1)/n*100:.1f}%  ({len(w1)} of {n})  -> lineup frozen the next Sunday")
    print("    by how:", dict(Counter(r[2] for r in w1)))
    print("\n  by position, seat invalid at w+1 (old measure: plays w+1):")
    for p in ('RB', 'QB', 'TE', 'WR'):
        sub = [r for r in res if r[0] == p]
        old = sum(1 for pos, sq in rows if pos == p and sq[0][1])
        print(f"    {p}  n={len(sub):4}   {sum(1 for r in sub if r[1]==1)/len(sub)*100:5.1f}%"
              f"   (old {old/len(sub)*100:5.1f}%)")

    # the six variants that failed to reproduce the published curve; kept so the retraction is checkable
    print("\n--- WHY THE PUBLISHED CURVE IS RETRACTED: every variant tried, none matches ---")
    o = outs.sort_values(['season', 'gsis_id', 'week'])
    variants = {'all Out-weeks': o, 'first Out per player-season':
                o.drop_duplicates(subset=['season', 'gsis_id'], keep='first')}
    eps, prev = [], None
    for r in o.itertuples(index=False):
        key = (r.season, r.gsis_id)
        if prev is None or prev[0] != key or r.week - prev[1] > 2:
            eps.append(r)
        prev = (key, r.week)
    variants['episodes, gap > 2'] = pd.DataFrame(eps)
    for lab, df in variants.items():
        for req in (True, False):
            rr = build(status, played, team_week, g2p, df, require_next=req)
            m = len(rr)
            a = [sum(1 for _, q in rr if not any(p for _, p in q[:k])) / m * 100 for k in range(1, 6)]
            tag = 'team plays w+1' if req else 'byes kept    '
            print(f"  {lab:28} {tag}  n={m:5}  " + " ".join(f"{x:5.1f}" for x in a))
    print("  published                                          n= 1035   73.8  53.8  40.8  31.2  23.8")


if __name__ == '__main__':
    main()
