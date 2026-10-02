"""snaps_2026.py -- the SNAP COUNT and the TEAM PLAY COUNT, which no file here has ever held.

[doc 434] Matt, 27 Sept, one question: "do we have number of snaps?" No. `form_2026.csv` and the
wire carry `snap_pct` and nothing else, and a percentage is a SHARE with the denominator thrown
away. That is the same defect the reach gate fixed for targets (doc 432), one layer down and still
live: the screen ranks men on share of plays while the pies differ by 35%, from Houston's 79.5 a
game to Tennessee's 51.5.

WHAT IT CHANGES, measured on the men on the board at the time:
    Cade Otton        93% of snaps, 57.0 a game, Tampa runs 61.0
    Xavier Worthy     82% of snaps, 61.0 a game, Kansas City runs 74.5
  Otton LOOKS like the bigger workload and Worthy plays four more snaps a game.
    Malik Washington  85% of snaps, 49.0 a game, Miami runs 57.5
  Twelve fewer snaps a game than Worthy while reading eleven points higher.

SOURCE: nflverse-data, the snap_counts release, which is a DIFFERENT file from the player stats we
already cache. Columns: offense_snaps (the count) and offense_pct. Team plays are derived as the
most snaps any one man took for that team in that game, which is a lineman and is the play count.

Standard library only (0.4: it runs on Matt's machine). Needs the internet, like build_form.py.
Writes Source\\snaps_2026.csv. Run it after build_form.py.
"""
import csv, io, collections, os, sys, urllib.request

URL = ('https://github.com/nflverse/nflverse-data/releases/download/'
       'snap_counts/snap_counts_{season}.csv')
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'Source')
POS = ('WR', 'TE', 'RB', 'QB')


def _f(x):
    try:
        return float(x or 0)
    except (TypeError, ValueError):
        return 0.0


def fetch(season=2026):
    req = urllib.request.Request(URL.format(season=season),
                                 headers={'User-Agent': 'Mozilla/5.0'})
    raw = urllib.request.urlopen(req, timeout=60).read()
    rows = [r for r in csv.DictReader(io.StringIO(raw.decode('utf-8', 'replace')))
            if r.get('game_type') == 'REG']
    if not rows:
        raise SystemExit('FAILED: the snap_counts release returned no regular-season rows. '
                         'That is not an empty week, it is a broken read.')
    return rows


def build(rows):
    # team offensive plays in a game = the most snaps any ONE player took for that team.
    plays = collections.defaultdict(float)
    for r in rows:
        k = (r['week'], r['team'])
        plays[k] = max(plays[k], _f(r['offense_snaps']))
    out = []
    for r in rows:
        if r.get('position') not in POS:
            continue
        tp = plays[(r['week'], r['team'])]
        sn = _f(r['offense_snaps'])
        out.append({'week': r['week'], 'player': r['player'], 'pos': r['position'],
                    'team': r['team'], 'snaps': f'{sn:.0f}', 'team_plays': f'{tp:.0f}',
                    'snap_pct': f'{(sn / tp * 100) if tp else 0:.1f}'})
    return out, plays


def main():
    season = int(sys.argv[1]) if len(sys.argv) > 1 else 2026
    rows = fetch(season)
    out, plays = build(rows)
    # THE GUARD: a team that ran no plays is a broken read, not a bye. Fail rather than write it.
    zero = [k for k, v in plays.items() if v <= 0]
    if zero:
        raise SystemExit(f'FAILED: {len(zero)} team-weeks show zero offensive plays: {zero[:5]}')
    if not out:
        raise SystemExit('FAILED: no skill-position rows survived the filter.')
    dst = os.path.join(SRC, f'snaps_{season}.csv')
    with open(dst, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=['week', 'player', 'pos', 'team',
                                           'snaps', 'team_plays', 'snap_pct'])
        w.writeheader()
        w.writerows(out)
    wks = sorted({r['week'] for r in out}, key=int)
    tp = collections.defaultdict(list)
    for (wk, t), v in plays.items():
        tp[t].append(v)
    avg = sorted(((t, sum(v) / len(v)) for t, v in tp.items()), key=lambda x: -x[1])
    print(f'  written: {dst}  ({len(out)} rows, weeks {wks[0]} to {wks[-1]})')
    print(f'  team plays a game: {avg[0][0]} {avg[0][1]:.1f} highest, '
          f'{avg[-1][0]} {avg[-1][1]:.1f} lowest. That spread is the point of this file.')


if __name__ == '__main__':
    main()
