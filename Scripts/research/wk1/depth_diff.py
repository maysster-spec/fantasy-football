#!/usr/bin/env python3
r"""depth_diff.py -- how stale is the 8 August chart? READ-ONLY.

For every team, the seat lane's chart (Scripts\depth_map.csv, captured 8 August 2026 off the
keeper-removed board) is set beside today's (Source\depth_daily.csv, written by
build_depth_daily.py from the nflverse feed) at RB1, RB2, WR1, WR2, WR3 and TE1, and every
disagreement is printed with a count per slot. Nothing is written except run_depth_diff.txt
beside this script, which is the same text that goes to the screen.

WHAT COUNTS AS A CHANGE, and what does not:
  RB1, RB2, TE1   the man at that depth on 8 August is not the man there today (joined on
                  espn_id, which both files carry; name_key only where an id is blank).
  WR1, WR2, WR3   the 8 August file has no order among a team's three starting receivers (the
                  scrape gave one row per slot, X, Z and slot, each at depth 1, and depth_map.py
                  flattened them), so today's rank-N receiver is "changed" when he was NOT AMONG
                  the 8 August starters at all. A reshuffle inside the same three is not a change.
  no row          depth_map.csv was built off the board with the twelve keepers removed and off
                  only the men the board carried, so a slot it has nobody at (NE, NO and NYG RB1;
                  CHI TE1; six teams with two named starting receivers) is UNKNOWN on 8 August,
                  listed under its own heading, and never counted as a change.

USAGE  py depth_diff.py [--map FILE] [--daily FILE]
       Defaults: ..\..\depth_map.csv against this file (Scripts\depth_map.csv when this sits in
       Scripts\research\wk1\), and depth_daily.csv in Source (..\..\..\Source, or FF_SOURCE).
Standard library only; paths off __file__; Python 3.12 clean.
"""
import argparse, csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get('FF_SOURCE') or os.path.abspath(os.path.join(HERE, '..', '..', '..', 'Source'))
ALIAS = {'ARZ': 'ARI', 'BLT': 'BAL', 'CLV': 'CLE', 'HST': 'HOU', 'LA': 'LAR', 'WAS': 'WSH',
         'JAC': 'JAX', 'GNB': 'GB', 'KAN': 'KC', 'NWE': 'NE', 'NOR': 'NO', 'SFO': 'SF',
         'TAM': 'TB', 'LVR': 'LV', 'SD': 'LAC', 'OAK': 'LV', 'STL': 'LAR'}   # sheet_engine.TEAM_ALIAS
SLOTS = (('RB', 1), ('RB', 2), ('WR', 1), ('WR', 2), ('WR', 3), ('TE', 1))


def tk(t):
    t = (t or '').strip().upper()
    return ALIAS.get(t, t)


def norm(n):                      # build_form.py's norm(), verbatim, the fallback key only
    n = (n or '').lower()
    n = re.sub(r"[.'`’]", '', n)
    n = re.sub(r'\b(jr|sr|ii|iii|iv|v)\b', '', n)
    return re.sub(r'[^a-z]', '', n)


def rd(path):
    with open(path, newline='', encoding='utf-8-sig') as fh:
        return list(csv.DictReader(fh))


def ident(r, name_col):
    """espn_id when present, else the normalised name. One key space for both files."""
    e = (r.get('espn_id') or '').strip()
    try:
        return 'e' + str(int(float(e)))
    except ValueError:
        return 'n' + norm(r.get(name_col))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--map', default=os.path.abspath(os.path.join(HERE, '..', '..', 'depth_map.csv')))
    ap.add_argument('--daily', default=os.path.join(SRC, 'depth_daily.csv'))
    a = ap.parse_args()
    for p in (a.map, a.daily):
        if not os.path.exists(p):
            sys.exit(f'STOP: {p} is missing, not empty.')

    # 8 August: {(team, pos): {depth: [(id, name), ...]}}; WR depth 1 holds up to three men
    aug = {}
    for r in rd(a.map):
        pos = (r.get('pos') or '').strip()
        if pos not in ('RB', 'WR', 'TE'):
            continue
        try:
            d = int(float(r.get('depth') or 0))
        except ValueError:
            continue
        aug.setdefault((tk(r.get('tm')), pos), {}).setdefault(d, []).append((ident(r, 'player'), r['player']))
    # today: {(team, pos): {depth: (id, name)}}
    today, as_of = {}, set()
    for r in rd(a.daily):
        pos = (r.get('pos') or '').strip()
        if pos not in ('RB', 'WR', 'TE'):
            continue
        today.setdefault((tk(r.get('team')), pos), {})[int(r['depth'])] = (ident(r, 'player'), r['player'])
        as_of.add(r.get('as_of', ''))
    teams = sorted({t for t, _ in today})
    if len(teams) != 32:
        sys.exit(f'STOP: {len(teams)} teams in {a.daily}, not 32.')

    changed = {s: [] for s in SLOTS}          # slot -> [(team, august man, today's man)]
    unknown = {s: [] for s in SLOTS}          # slot -> [(team, today's man)]
    for tm in teams:
        for pos, d in SLOTS:
            now = today.get((tm, pos), {}).get(d)
            if now is None:
                unknown[(pos, d)].append((tm, '(nobody on today\'s chart)'))
                continue
            was = aug.get((tm, pos), {})
            if pos == 'WR':
                starters = was.get(1, [])
                if len(starters) < 3 and now[0] not in {i for i, _ in starters}:
                    # two named starters on 8 Aug and he is not one of them: cannot tell
                    unknown[(pos, d)].append((tm, now[1] + f' (8 Aug named only {len(starters)} starters)'))
                    continue
                if now[0] not in {i for i, _ in starters}:
                    changed[(pos, d)].append((tm, ' / '.join(n for _, n in starters) or '(nobody)', now[1]))
            else:
                men = was.get(d, [])
                if not men:
                    unknown[(pos, d)].append((tm, now[1]))
                    continue
                if now[0] != men[0][0]:
                    changed[(pos, d)].append((tm, men[0][1], now[1]))

    lines = []
    out = lines.append
    out(f'depth_diff: 8 August chart ({os.path.basename(a.map)}) against today\'s '
        f'({os.path.basename(a.daily)}, as_of {", ".join(sorted(as_of))})')
    out('')
    out('CHANGED (the man at the slot on 8 August is not the man there today; WR: today\'s man was not')
    out('among the 8 August starting three)')
    for pos, d in SLOTS:
        ch = changed[(pos, d)]
        out(f'  {pos}{d}: {len(ch)} of 32 teams')
        for tm, was, now in ch:
            out(f'     {tm:<4} 8 Aug {was:<40} today {now}')
    out('')
    out('UNKNOWN on 8 August (no row in depth_map.csv at that slot: the keeper-removed board, an')
    out('off-board man, or two named starting receivers). Not counted above.')
    for pos, d in SLOTS:
        un = unknown[(pos, d)]
        if un:
            out(f'  {pos}{d}: {len(un)}: ' + '; '.join(f'{tm} today {now}' for tm, now in un))
    out('')
    rb_teams = sorted({tm for s in (('RB', 1), ('RB', 2)) for tm, _, _ in changed[s]})
    wr_teams = sorted({tm for s in (('WR', 1), ('WR', 2), ('WR', 3)) for tm, _, _ in changed[s]})
    te_teams = sorted({tm for tm, _, _ in changed[('TE', 1)]})
    out(f'BACKFIELDS where the 8 August chart is stale at RB1 or RB2: {len(rb_teams)} '
        f'({", ".join(rb_teams)})')
    out(f'RECEIVER ROOMS with a starter today who was not one on 8 August: {len(wr_teams)} '
        f'({", ".join(wr_teams)})')
    out(f'TIGHT END rooms changed at TE1: {len(te_teams)} ({", ".join(te_teams)})')
    text = '\n'.join(lines) + '\n'
    print(text, end='')
    rp = os.path.join(HERE, 'run_depth_diff.txt')
    with open(rp, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)


if __name__ == '__main__':
    main()
