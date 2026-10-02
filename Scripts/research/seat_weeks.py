#!/usr/bin/env python3
"""seat_weeks.py -- what each seat on his roster has returned this season: seat-weeks held against startable weeks
delivered, for the men he drafted and the men he added (doc 463 section 3, item 5; doc 465).

Matt, 1 Oct: "I did end up dropping him ... I don't feel great about it." The question a swap should be judged on is
what the SEAT produced, not the names. This rebuilds his roster week by week from the executed moves in
waiver_report_2026.csv (walking back from MY_ROSTER.csv), scores every man-week off form_2026.csv, and counts the
weeks each man was held against the weeks he scored at or above the position's startable bar (RB 9.92, WR 9.62,
TE 8.25 half-PPR a game, 4.1's season totals over 17). Backs, receivers and tight ends only: the form file scores
rushing and receiving, so quarterbacks, kickers and defenses are left out. A man-week counts whether or not he was in the lineup (lineups are not on file).
Week N's moves apply to week N's games (ESPN's Week column is the scoring period the move lands in).

    py research\\seat_weeks.py            prints the table; stdlib + pandas; paths resolve against this file
"""
import csv
import os
import re
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get('FF_SRC') or os.path.normpath(os.path.join(HERE, '..', '..', 'Source'))
TEAM = os.environ.get('FF_TEAM_NAME', 'The Poetry of Junkyard Juggers')
BAR = {'RB': 9.92, 'WR': 9.62, 'TE': 8.25}      # no QB: the form file scores rushing and receiving only (doc 375)
_SUFFIX = {'jr', 'sr', 'ii', 'iii', 'iv', 'v'}


def norm(s):
    s = str(s or '').lower().replace('.', '').replace("'", '').replace('-', ' ')
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    return ' '.join(t for t in s.split() if t not in _SUFFIX)


def names_by_id():
    out = {}
    for f in ('LEAGUE_ROSTERS.csv', 'MY_ROSTER.csv') + tuple(sorted(x for x in os.listdir(SRC) if x.startswith(('WIRE_', 'FREE_UNRANKED_')))):
        p = os.path.join(SRC, f)
        if not os.path.exists(p):
            continue
        with open(p, newline='', encoding='utf-8-sig') as fh:
            for r in csv.DictReader(fh):
                if r.get('espn_id') and r.get('player'):
                    out.setdefault(str(r['espn_id']).strip(), (r['player'].strip(), (r.get('pos') or '').strip().upper()))
    return out


def main():
    names = names_by_id()
    cur = {}
    with open(os.path.join(SRC, 'MY_ROSTER.csv'), newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            pid = str(r['espn_id']).strip()
            pos = (r.get('pos') or '').strip().upper() or (names.get(pid) or ('', ''))[1]   # Pickens carries no pos on the file
            cur[pid] = (r['player'].strip(), pos)
    w = pd.read_csv(os.path.join(SRC, 'waiver_report_2026.csv'))
    me = w[(w.Team == TEAM) & (w.Status == 'EXECUTED')].copy()
    me['add'] = me.Transaction.str.extract(r'ADD Player ID (-?\d+)')[0]
    me['drop'] = me.Transaction.str.extract(r'DROP Player ID (-?\d+)')[0]
    me = me.sort_values('Date')
    last_week = int(me.Week.max()) if len(me) else 1
    # walk back from the current roster to the roster at the start of each week
    roster_at = {}                                 # week -> set of ids on the roster for that week's games
    r = set(cur)
    for wk in range(last_week, 0, -1):
        roster_at[wk] = set(r)
        for _, m in me[me.Week == wk].sort_values('Date', ascending=False).iterrows():
            if pd.notna(m['add']):
                r.discard(str(m['add']))
            if pd.notna(m['drop']):
                r.add(str(m['drop']))
    drafted = set(r)                               # the roster before any move: the draft and the keeper
    acquired = set(me['add'].dropna().astype(str))
    # points by week off the form file, name + pos
    fm = pd.read_csv(os.path.join(SRC, 'form_2026.csv'), low_memory=False)
    fm = fm[fm.week > 0]
    pts = {}
    for _, x in fm.iterrows():
        pts[(norm(x.player), str(x.pos).upper(), int(x.week))] = float(x.half_ppr or 0)
    played = sorted(int(wk) for wk in fm.week.unique())
    rows = []
    for pid in drafted | acquired:
        nm, pos = cur.get(pid) or names.get(pid) or (f'id {pid}', '')
        if pos not in BAR:
            continue
        held = [wk for wk in played if pid in roster_at.get(wk, set())]
        start = [wk for wk in held if pts.get((norm(nm), pos, wk), 0.0) >= BAR[pos]]
        scored = [round(pts.get((norm(nm), pos, wk), 0.0), 1) for wk in held]
        rows.append(dict(man=nm, pos=pos, how='drafted' if pid in drafted else 'added', seat_weeks=len(held),
                         startable=len(start), points=scored))
    d = pd.DataFrame(rows).sort_values(['how', 'seat_weeks', 'startable'], ascending=[True, False, False])
    print(f'his roster rebuilt from {len(me)} executed moves; weeks scored: {played}; skill positions only')
    print(d.to_string(index=False))
    for how, g in d.groupby('how'):
        print(f'  {how:<8} seat-weeks {int(g.seat_weeks.sum()):>3}  startable weeks {int(g.startable.sum()):>3}  '
              f'seat-weeks per startable week {g.seat_weeks.sum() / max(g.startable.sum(), 1):.1f}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
