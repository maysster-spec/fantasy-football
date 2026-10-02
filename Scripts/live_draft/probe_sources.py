#!/usr/bin/env python
"""
probe_sources.py -- WHICH ESPN ENDPOINT CARRIES A DRAFT WHILE IT IS HAPPENING?  (doc 136)

THE PROBLEM THIS EXISTS TO SOLVE
    On 2026-09-02 a real 12-team league drafted while `live_draft.py --watch` polled
    lm-api-reads every 3 seconds for 16 minutes.  It reported 0 of 192 picks the entire time --
    and then delivered ALL 192 IN A SINGLE POLL once the room finished.

    So the picks are real and readable; we are reading a source that only publishes at the end.
    `lm-api-reads` is, by its own name, a READ REPLICA.  This script asks the obvious next
    question: does some OTHER url carry the picks live?

HOW TO USE IT
    1. Start any live draft you can watch -- an ESPN mock from the lobby is fastest, it fills
       with bots and begins on demand.
    2. Copy the draft-room URL.
    3. py probe_sources.py --url "<paste it>"
    4. Let it run through 15-20 picks.  It prints one line per source per poll and, at the end,
       a verdict naming the FIRST source that moved.

    Anything that shows a rising count while the room is still drafting is the answer, and
    live_draft.py's READS constant gets pointed at it.

IT ONLY READS.  Nothing is written to ESPN, no file is changed, Ctrl+C ends it.
"""
import argparse, datetime as dt, json, re, sys, time, urllib.parse
import requests

# same credentials live_draft.py already uses -- settled, approved, not re-litigated here
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
try:
    from live_draft import COOKIES, HEADERS, parse_draft_url
except Exception:
    sys.exit("run this from Scripts\\live_draft (it borrows the cookies from live_draft.py)")

READS   = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{s}/segments/0/leagues/{l}"
PRIMARY = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/{s}/segments/0/leagues/{l}"
LM      = "https://lm-api-writes.fantasy.espn.com/apis/v3/games/ffl/seasons/{s}/segments/0/leagues/{l}"

def sources(season, lid):
    """Every plausible live source, cheapest and most likely first."""
    r = READS.format(s=season, l=lid); p = PRIMARY.format(s=season, l=lid); w = LM.format(s=season, l=lid)
    return [
        ('reads  (current)',      r + "?view=mDraftDetail",            {}),
        ('reads  + no-cache',     r + "?view=mDraftDetail",            {'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}),
        ('reads  + cachebust',    r + "?view=mDraftDetail&_={ts}",     {}),
        ('PRIMARY host',          p + "?view=mDraftDetail",            {}),
        ('PRIMARY + cachebust',   p + "?view=mDraftDetail&_={ts}",     {}),
        ('writes host',           w + "?view=mDraftDetail",            {}),
        ('reads  + mStatus',      r + "?view=mDraftDetail&view=mStatus", {}),
        ('league communication',  r + "/communication/?view=kona_league_communication", {}),
    ]

def count_picks(js):
    """Real selections only -- doc 123: an empty slot carries playerId -1, which is TRUTHY."""
    if not isinstance(js, dict): return None
    dd = js.get('draftDetail') or {}
    picks = dd.get('picks')
    if picks is None:
        # the communication view nests differently; count anything that looks like a pick event
        topics = js.get('topics') or []
        n = sum(1 for t in topics for m in (t.get('messages') or []) if m.get('messageTypeId') in (0, 1, 2))
        return n if topics else None
    def real(v):
        try: return abs(int(v)) > 100
        except (TypeError, ValueError): return False
    return sum(1 for p in picks if real(p.get('playerId')))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', help='paste the ESPN draft-room URL in quotes')
    ap.add_argument('--league', type=int); ap.add_argument('--season', type=int, default=2026)
    ap.add_argument('--interval', type=float, default=4.0)
    a = ap.parse_args()
    if a.url:
        info = parse_draft_url(a.url); lid = info['league']; season = info.get('season') or a.season
    elif a.league:
        lid, season = a.league, a.season
    else:
        sys.exit('need --url "<draft room url>" or --league <id>')
    srcs = sources(season, lid)
    print('=' * 74)
    print(f'  PROBE -- league {lid}, season {season}, {len(srcs)} sources, every {a.interval}s')
    print('  Start this while a draft is RUNNING.  Ctrl+C to stop.')
    print('=' * 74)
    first = {}
    base = {}
    t0 = time.time()
    try:
        while True:
            line = f'  [{dt.datetime.now():%H:%M:%S}]'
            for name, tmpl, extra in srcs:
                url = tmpl.format(ts=int(time.time() * 1000))
                try:
                    h = dict(HEADERS); h.update(extra)
                    r = requests.get(url, cookies=COOKIES, headers=h, timeout=8)
                    n = count_picks(r.json()) if r.status_code == 200 else None
                    cell = 'ERR' if n is None else str(n)
                    if n is not None:
                        base.setdefault(name, n)
                        if n > base[name] and name not in first:
                            first[name] = (int(time.time() - t0), n)
                except Exception:
                    cell = 'ERR'
                line += f'  {name}={cell}'
            print(line)
            time.sleep(a.interval)
    except KeyboardInterrupt:
        print()
        print('=' * 74)
        if not first:
            print('  NO SOURCE MOVED while you watched.')
            print('  If the room was genuinely drafting, none of these carry a live draft and the')
            print('  next step is reading the picks out of the open draft room itself.')
        else:
            for name, (secs, n) in sorted(first.items(), key=lambda kv: kv[1][0]):
                print(f'  *** {name} MOVED after {secs}s (reached {n} picks) ***')
            print()
            print('  Point live_draft.py\'s READS constant at the first one and re-run --watch.')
        print('=' * 74)

if __name__ == '__main__':
    main()
