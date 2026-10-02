"""build_news.py -- the injury and news feed the week sheet never had. Writes Source\\news_2026.csv.

WHY THIS EXISTS (doc 412). On 24 Sept the sheet recommended dropping Rico Dowdle because his snap
share fell 58% to 26% between weeks 1 and 2, and named Jaylen Warren as the man who took his job.
Matt: *"Dowdle, 26%, yes, he got injured week 2, lol. Somehow you still only see a very narrow
picture of what i see."* He was right. There was no injury feed here at all. What this project
could see about a roster was a preseason projection, two weeks of snap counts, and a one-word ESPN
status string, so a snap share could move for a dozen reasons and nothing could tell them apart.
METHOD_TRAPS.md carries the rule that came out of it; this file is the missing input it names.

WHAT IT WRITES, one row per injured player:
    espn_id, player, pos, team, status, injury, location, detail, return_date, reported, source

THE JOIN IS AN ID, NOT A NAME (section 3). ESPN's injuries feed carries no athlete id field, but
every athlete's `links` href contains one (/nfl/player/_/id/4428718/...), and that id is the SAME
number as the fantasy espn_id -- verified against the 24 Sept pull: Marvin Harrison Jr is 4432708
on both sides. Where no id can be extracted the row still writes, keyed on name + position + team,
which is section 3's stated fallback, and `source` says which key it got.

IT REFUSES RATHER THAN RETURNING A THIN FILE (doc 146: an exit code is not a result). The
league-wide endpoint has been observed returning a single team. If fewer than MIN_TEAMS come back
it falls back to the per-team endpoints and, failing that, exits 2 and writes nothing, because a
news file covering one team would be worse than none: the sheet would print "no news" beside a man
who is actually hurt.

    py build_news.py            write Source\\news_2026.csv
    py build_news.py --dry      print what it would write, touch nothing

Standard library only (doc 144). No cookies: these endpoints are public, so nothing here reads,
prints or needs wire.py's session.
"""
import csv
import json
import os
import re
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))          # doc 144: resolve against the script
SRC = os.path.join(HERE, '..', 'Source')
OUT = os.path.join(SRC, 'news_2026.csv')

BASE = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl'
LEAGUE_INJURIES = BASE + '/injuries'
TEAMS = BASE + '/teams?limit=40'
TEAM_INJURIES = BASE + '/teams/{tid}/injuries'
NEWS = BASE + '/news'

MIN_TEAMS = 20            # below this the league-wide feed is not trusted
TIMEOUT = 20

# [doc 413] THE FIRST LIVE RUN RETURNED 403 ON BOTH ENDPOINTS AND THE HEADERS WERE WHY.
# A custom User-Agent ("fantasy week sheet; personal use") is exactly what ESPN's edge rejects,
# and the container this was written in reaches the same URL fine, so the failure could only
# appear on Matt's machine. `wire.py` has talked to ESPN from that machine for weeks and sends
# NO User-Agent at all, but it does send a referer and an explicit accept -- so the proven shape
# is copied here rather than invented. Three profiles are tried in order and the LAST error is
# reported with the status code, so one run settles it instead of costing a round trip each time.
HEADER_PROFILES = [
    {'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'),
     'Accept': 'application/json, text/plain, */*',
     'Referer': 'https://www.espn.com/nfl/injuries',
     'Accept-Language': 'en-US,en;q=0.9'},
    {'accept': 'application/json', 'referer': 'https://www.espn.com/',
     'x-fantasy-platform': 'espn-fantasy-web', 'x-fantasy-source': 'kona'},
    {'Accept': 'application/json'},
]

ID_IN_HREF = re.compile(r'/id/(\d+)')


def get(url):
    """Try each header profile. Raise the LAST error, with its status code, if all fail."""
    last = None
    for hdrs in HEADER_PROFILES:
        try:
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return json.loads(r.read().decode('utf-8', 'replace'))
        except urllib.error.HTTPError as exc:
            last = f'HTTP {exc.code}'
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last = f'{type(exc).__name__}: {exc}'
    raise RuntimeError(f'{last} after {len(HEADER_PROFILES)} header profiles')


def athlete_id(ath):
    """The id out of any href on the athlete. Returns (id, how_it_was_found)."""
    for ln in (ath.get('links') or []):
        m = ID_IN_HREF.search(ln.get('href') or '')
        if m:
            return m.group(1), 'id'
    for key in ('id', 'uid', 'guid'):
        v = str(ath.get(key) or '')
        m = ID_IN_HREF.search(v) or re.fullmatch(r'\d+', v)
        if m:
            return (m.group(1) if m.re is ID_IN_HREF else v), 'id'
    return '', 'name+pos+team'


def rows_from(payload):
    out = []
    for team_block in (payload.get('injuries') or []):
        tm_abbr = (team_block.get('abbreviation')
                   or (team_block.get('team') or {}).get('abbreviation') or '')
        for e in (team_block.get('injuries') or []):
            ath = e.get('athlete') or {}
            det = e.get('details') or {}
            pid, how = athlete_id(ath)
            team = (((ath.get('team') or {}).get('abbreviation')) or tm_abbr or '')
            # [doc 414] A ROW WITH NOTHING IN IT IS NOT NEWS. ESPN's feed lists the whole injury
            # REPORT, cleared men included: on the first good run, 585 of 800 rows were status
            # "Active" with no injury, no detail and no return date. Unfiltered, the week sheet
            # printed the word "Active" in red beside Vele, Washington and Pineiro as though it
            # were a diagnosis. An Active man WITH an injury is kept -- he is playing through
            # something and that is worth knowing.
            _status = (e.get('status') or '').strip()
            _has = bool((det.get('type') or '').strip() or (det.get('returnDate') or '').strip())
            if _status.lower() in ('active', '') and not _has:
                continue
            _detail = (det.get('detail') or '').strip()
            if _detail.lower() in ('not specified', 'unspecified'):
                _detail = ''           # 160 rows carried this; it is a placeholder, not a fact
            out.append({
                'espn_id': pid,
                'player': ath.get('displayName') or ' '.join(
                    x for x in (ath.get('firstName'), ath.get('lastName')) if x),
                'pos': ((ath.get('position') or {}).get('abbreviation') or ''),
                'team': team,
                'status': _status,
                'injury': det.get('type') or '',
                'location': det.get('location') or '',
                'detail': _detail,
                'return_date': (det.get('returnDate') or '')[:10],
                'reported': (e.get('date') or '')[:16].replace('T', ' '),
                'source': how,
            })
    return out


def collect():
    """League-wide first, per-team if that comes back thin. Returns (rows, how, teams_seen)."""
    try:
        payload = get(LEAGUE_INJURIES)
    except Exception as exc:                                  # noqa: BLE001
        print(f'  could not reach the league injuries feed: {exc}')
        payload = {}
    blocks = payload.get('injuries') or []
    if len(blocks) >= MIN_TEAMS:
        return rows_from(payload), 'league-wide', len(blocks)

    print(f'  league-wide feed returned {len(blocks)} team block(s), under the {MIN_TEAMS} floor '
          f'-- falling back to the per-team endpoints')
    try:
        teams = get(TEAMS)
    except Exception as exc:                                  # noqa: BLE001
        print(f'  could not list teams either: {type(exc).__name__}: {exc}')
        return [], 'failed', len(blocks)

    ids = []
    for sport in (teams.get('sports') or []):
        for lg in (sport.get('leagues') or []):
            for t in (lg.get('teams') or []):
                tid = (t.get('team') or {}).get('id')
                if tid:
                    ids.append(str(tid))
    rows, seen = [], 0
    for tid in ids:
        try:
            rows += rows_from(get(TEAM_INJURIES.format(tid=tid)))
            seen += 1
        except Exception:                                     # noqa: BLE001
            continue
    return rows, f'per-team ({seen} of {len(ids)})', seen


def main():
    dry = '--dry' in sys.argv
    rows, how, teams_seen = collect()
    if not rows or teams_seen < MIN_TEAMS:
        print(f'REFUSING TO WRITE. Covered {teams_seen} team(s) via {how}, {len(rows)} row(s). '
              f'A news file that covers part of the league is worse than none, because the sheet '
              f'would print nothing beside a man who is actually hurt.')
        return 2

    rows.sort(key=lambda r: (r['team'], r['player']))
    print(f'  {len(rows)} injury rows, {teams_seen} teams, via {how}')
    by_key = sum(1 for r in rows if r['source'] != 'id')
    if by_key:
        print(f'  {by_key} row(s) carry no extractable id and fall back to name + position + team')

    if dry:
        for r in rows[:15]:
            print('   ', ' | '.join(
                (r['player'], r['team'], r['pos'], r['status'],
                 r['injury'], 'back ' + r['return_date'] if r['return_date'] else '')))
        print('  --dry: nothing written')
        return 0

    with open(OUT, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    # Verify the ARTIFACT, never the exit code (0.2).
    n = sum(1 for _ in open(OUT, encoding='utf-8')) - 1
    print(f'  written -> {os.path.normpath(OUT)}  ({n} rows on disk)')
    return 0 if n == len(rows) else 2


if __name__ == '__main__':
    raise SystemExit(main())
