#!/usr/bin/env python3
"""build_pedigree.py -- writes Source\\pedigree_2026.csv, the draft-capital column 4.28 asked for
and the 4.30 receiver screen, so wire.py can rank on POTENTIAL and not only on today's value.

Matt, 2026-09-09: "We are not just looking at current market value, but POTENTIAL value as well."
The two measured screens this file carries, and nothing else:
  1. NFL FIRST-ROUND ROOKIE RECEIVER (4.28, n=364). 9 of 15 out-targeted the incumbent in year one
     against 7.4% for everyone else, and 6 of those 9 were startable. It is a ROUND-1 event: NFL
     rounds 2-3 measured 3.3%.
  2. THE THREE-SIGNAL SCREEN (4.30, n=152). Young non-startable receivers who clear NFL rounds 1-3
     AND yards per target over 7.13 AND targets per game over 3.20 became startable 39.4% of the
     time, against 0-7% for those clearing two or fewer.
Neither is a forecast for one player (4.13d: nothing in this project computes a ceiling).

Stdlib only (SECTION 0.4). Paths resolve against this file, never the shell's cwd.
Inputs : Scripts\\live_draft\\board_v8_fixed.csv (the spine -- espn_id, player, pos)
         Source\\games_2025.csv                  (games played, joined on espn_id)
         Source\\nfl_draft_picks.csv             (nflverse draft_picks)
         Source\\rec_2025.csv                    (2025 receiving, built from nflverse play-by-play)
Output : Source\\pedigree_2026.csv
"""
import csv, os, re, sys, unicodedata, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
SRC  = os.path.join(ROOT, 'Source')
BOARD = os.path.join(ROOT, 'Scripts', 'live_draft', 'board_v8_fixed.csv')
OUT   = os.path.join(SRC, 'pedigree_2026.csv')
SEASON, WR_REPLACEMENT = 2026, 9.62          # WR replacement per game, DERIVED: the board's WR30 season total / 17 (not measured)


def nk(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode()
    s = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", s.lower())
    return re.sub(r"[^a-z]", "", s)


def read(path):
    if not os.path.exists(path):
        sys.exit(f"  MISSING INPUT: {path}\n  pedigree_2026.csv was NOT written.")
    with open(path, newline='', encoding='utf-8-sig') as fh:
        return list(csv.DictReader(fh))


def main():
    board = read(BOARD)
    picks = [r for r in read(os.path.join(SRC, 'nfl_draft_picks.csv'))
             if r['season'] and int(r['season']) >= SEASON - 5
             and r['position'] in ('WR', 'RB', 'TE', 'QB')]
    rec = {r['gsis_id']: r for r in read(os.path.join(SRC, 'rec_2025.csv'))}
    g25 = {str(r['espn_id']).strip(): int(r['g25'])
           for r in read(os.path.join(SRC, 'games_2025.csv')) if int(r['g25']) > 0}

    by_name = collections.defaultdict(list)
    for p in picks:
        by_name[(nk(p['pfr_player_name']), p['position'])].append(p)
    ambiguous = {k: len(v) for k, v in by_name.items() if len(v) > 1}

    out, matched = [], 0
    for b in board:
        key = (nk(b['player']), b['pos'])
        if key in ambiguous:                       # SECTION 3: never default an ambiguous join
            continue
        hit = by_name.get(key)
        if not hit:
            continue
        p = hit[0]
        matched += 1
        yr = SEASON - int(p['season']) + 1
        s = rec.get(p['gsis_id'])
        g = g25.get(str(b['espn_id']).strip())
        tgt = float(s['tgt']) if s else 0.0
        ypt = (float(s['yds']) / tgt) if (s and tgt) else ''
        tpg = (tgt / g) if (s and g) else ''
        ppg = (((0.1 * float(s['yds'])) + (0.5 * float(s['rec'])) + (6 * float(s['td']))) / g) \
            if (s and g) else ''
        sig = ''
        screen = ''
        if b['pos'] == 'WR':
            if yr == 1 and int(p['round']) == 1:
                screen = 'first-round rookie'
            elif yr <= 3 and ypt != '' and tpg != '' and ppg != '' and ppg < WR_REPLACEMENT:
                sig = sum([int(p['round']) <= 3, ypt > 7.13, tpg > 3.20])
                if sig == 3:
                    screen = 'pedigree screen 3 of 3'
        out.append(dict(espn_id=str(b['espn_id']).strip(), player=b['player'], pos=b['pos'],
                        nfl_season=p['season'], nfl_round=p['round'], nfl_pick=p['pick'],
                        nfl_year=yr, g25=(g or ''), tgt25=int(tgt),
                        ypt25=(round(ypt, 2) if ypt != '' else ''),
                        tpg25=(round(tpg, 2) if tpg != '' else ''),
                        ppg25=(round(ppg, 2) if ppg != '' else ''),
                        signals=sig, screen=screen))

    if matched < 150:
        sys.exit(f"  ONLY {matched} board rows matched a draft pick -- that is a broken join, not a\n"
                 f"  thin draft class. pedigree_2026.csv was NOT written.")
    with open(OUT, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    rook = sum(1 for r in out if r['screen'] == 'first-round rookie')
    thr = sum(1 for r in out if r['screen'] == 'pedigree screen 3 of 3')
    print(f"  wrote {OUT}")
    print(f"  {matched} of {len(board)} board rows carry an NFL draft round "
          f"({len(ambiguous)} names skipped as ambiguous)")
    print(f"  first-round rookie receivers: {rook}   |   receivers clearing 3 of 3: {thr}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
