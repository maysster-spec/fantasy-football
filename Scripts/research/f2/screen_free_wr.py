#!/usr/bin/env python3
r"""screen_free_wr.py -- catalog F2: run 4.30's three-signal screen on EVERY free receiver.

WHY: `build_pedigree.py` screens only receivers who are ON the draft board, so a free receiver the
board never rated has never been screened at all. Doc 248 scored Jayden Higgins above all three
cutoffs and he is not in `pedigree_2026.csv`, because he is not on the board.

POPULATION -- restate it every time (0.6): receivers who are FREE in Matt's league right now (the
newest WIRE_<date>.csv plus FREE_UNRANKED_<date>.csv, so on-board and off-board alike), who were
drafted into the NFL in 2024 or 2025 (years 2 and 3 in 2026; a 2026 rookie has no 2025 line and is
4.28's separate first-round screen, not this one), who played 4+ games in 2025, and who averaged
under 9.62 half-PPR points a game in 2025.
THE THREE SIGNALS (4.30, n=152): NFL draft rounds 1-3 - yards per target above 7.13 - targets a
game above 3.20. Base rate 11.4%; 3 of 3 became startable the next season 39.4% of the time.
BASELINE: 4.30's own cutoffs, unchanged. This is a SCREEN, never a per-player forecast (4.13d).

AND IT FIXES TWO THINGS THE BOARD VERSION GOT WRONG, both named in the catalog: the 9.62 bar is
compared against FULL half-PPR scoring here (the board version used receiving points only, so a
receiver with carries was scored low and wrongly qualified), and the 4-game minimum is applied.

Joins: ESPN has no nflverse id, so the key is normalised name + position, and the join rate is
ASSERTED and the misses are printed (3). Stdlib only.
"""
import collections, csv, glob, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get('F2_SRC', HERE)
DATA = os.environ.get('F2_DATA', HERE)
YPT, TPG, BAR, MING = 7.13, 3.20, 9.62, 4
DRAFTED = (2024, 2025)


def nk(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode()
    s = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", s.lower())
    return re.sub(r"[^a-z]", "", s)


def read(p):
    if not os.path.exists(p):
        sys.exit(f'  MISSING INPUT: {p}')
    with open(p, newline='', encoding='utf-8-sig') as fh:
        return list(csv.DictReader(fh))


def newest(pattern):
    hits = sorted(glob.glob(os.path.join(SRC, pattern)))
    if not hits:
        sys.exit(f'  MISSING INPUT: {pattern}')
    return hits[-1]


def half_ppr(r):
    g = lambda k: float(r.get(k) or 0)
    return (0.04 * g('passing_yards') + 6 * g('passing_tds') - 2 * g('passing_interceptions')
            + 0.1 * g('rushing_yards') + 6 * g('rushing_tds')
            + 0.1 * g('receiving_yards') + 6 * g('receiving_tds') + 0.5 * g('receptions'))


def main():
    wire_f, free_f = newest('WIRE_*.csv'), newest('FREE_UNRANKED_*.csv')
    pool = []
    for r in read(wire_f):
        if (r.get('pos') or '').upper() == 'WR':
            pool.append((r['espn_id'], r['player'], r.get('team', ''), float(r.get('owned_pct') or 0), 'on the board'))
    for r in read(free_f):
        if (r.get('pos') or '').upper() == 'WR':
            pool.append((r['espn_id'], r['player'], r.get('team', ''), float(r.get('owned_pct') or 0), 'NOT on the board'))
    print(f'free receivers in the pool: {len(pool)}   '
          f'({sum(1 for p in pool if p[4] == "on the board")} on the board, '
          f'{sum(1 for p in pool if p[4] != "on the board")} off it)')
    print(f'  {os.path.basename(wire_f)} + {os.path.basename(free_f)}\n')

    picks = collections.defaultdict(list)
    for r in read(os.path.join(SRC, 'nfl_draft_picks.csv')):
        if r['season'] and r['position'] == 'WR':
            picks[nk(r['pfr_player_name'])].append(r)
    # 2025 weekly lines, full scoring
    wk = collections.defaultdict(list)
    name_by_gsis, name_key = {}, collections.defaultdict(list)
    with open(os.path.join(DATA, 'stats_player_week_2025.csv'), newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            if (r.get('season_type') or 'REG') != 'REG' or (r.get('position') or '') != 'WR':
                continue
            pid = r['player_id']
            wk[pid].append(r)
            nm = r.get('player_display_name') or r.get('player_name') or pid
            name_by_gsis[pid] = nm
            if pid not in name_key[nk(nm)]:
                name_key[nk(nm)].append(pid)

    rows, miss_draft, miss_stats = [], [], []
    for pid, name, tm, own, where in pool:
        k = nk(name)
        dr = picks.get(k)
        if not dr:
            miss_draft.append(name)
            continue
        if len(dr) > 1:                       # never guess between two men with one name (3)
            miss_draft.append(name + ' (ambiguous draft row)')
            continue
        d = dr[0]
        season, rnd = int(d['season']), int(d['round'])
        if season not in DRAFTED:
            continue
        gs = name_key.get(k)
        if not gs:
            miss_stats.append(f'{name} (drafted {season} r{rnd})')
            continue
        if len(gs) > 1:
            miss_stats.append(name + ' (two nflverse ids)')
            continue
        lines = wk[gs[0]]
        games = len(lines)
        if games < MING:
            continue
        pts = sum(half_ppr(r) for r in lines) / games
        if pts >= BAR:
            continue
        tgt = sum(float(r.get('targets') or 0) for r in lines)
        yds = sum(float(r.get('receiving_yards') or 0) for r in lines)
        ypt = (yds / tgt) if tgt else 0.0
        tpg = tgt / games
        sig = [rnd <= 3, ypt > YPT, tpg > TPG]
        rows.append(dict(name=name, tm=tm, own=own, where=where, season=season, rnd=rnd,
                         pick=int(d['pick']), g=games, ppg=pts, ypt=ypt, tpg=tpg, n=sum(sig),
                         sig=sig))

    rows.sort(key=lambda r: (-r['n'], -r['ypt']))
    print(f"{'receiver':<22}{'tm':<4}{'own%':>6}{'drafted':>9}{'g':>4}{'ppg':>7}"
          f"{'y/tgt':>7}{'tgt/g':>7}{'signals':>9}   where")
    for r in rows:
        marks = ''.join('X' if b else '.' for b in r['sig'])
        print(f"{r['name']:<22}{r['tm']:<4}{r['own']:>6.1f}{str(r['season'])+' r'+str(r['rnd']):>9}"
              f"{r['g']:>4}{r['ppg']:>7.2f}{r['ypt']:>7.2f}{r['tpg']:>7.2f}"
              f"{str(r['n'])+'/3 '+marks:>9}   {r['where']}")
    three = [r for r in rows if r['n'] == 3]
    print(f"\n  {len(rows)} free receivers are in 4.30's population; {len(three)} clear 3 of 3.")
    for r in three:
        print(f"    {r['name']} ({r['tm']}, {r['own']:.1f}% rostered, {r['where']})")
    print(f"\n  JOIN: no NFL draft row for {len(miss_draft)} of {len(pool)} "
          f"({len(miss_draft)/len(pool):.0%}) -- undrafted men and spelling, both expected here.")
    print('   ', ', '.join(sorted(miss_draft)[:12]), '...' if len(miss_draft) > 12 else '')
    print(f"  no 2025 nflverse line for {len(miss_stats)} drafted men (no NFL snaps in 2025):")
    print('   ', ', '.join(sorted(miss_stats)[:12]), '...' if len(miss_stats) > 12 else '')


if __name__ == '__main__':
    main()
