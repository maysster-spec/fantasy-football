#!/usr/bin/env python3
r"""
waivers.py -- pull this league's TRANSACTION HISTORY out of ESPN.

    py waivers.py                # every season from 2022 through the one being played
    py waivers.py --live         # just this season -- the in-season run
    py waivers.py --season 2025  # just one
    py waivers.py --check        # prove the cookies, pull nothing

WRITES, into Source\ :
    waiver_report_<year>.csv   WAIVER and FREEAGENT rows -- SAME columns as before, so every
                               reader keeps working. Do not change this shape.
    trade_report_<year>.csv    TRADE rows. NEW 2026-09-08 and this is the point of the rewrite.

WHY IT WAS REWRITTEN (2026-09-08)
    The old version pulled `mTransactions2` and then kept only WAIVER and FREEAGENT. **The trades
    came back in that same response, four seasons running, and were thrown away.** Every trade
    claim in this project is therefore unmeasured -- including a week-11 trade I recommended.
    It also carried 2022 cookies and the espn_api library; it now uses the same requests +
    cookies path as wire.py, so `set_cookies.py` maintains it with everything else.
"""
import argparse, collections, csv, datetime as dt, json, os, sys

try:
    import requests
except ImportError:
    sys.exit("waivers.py needs `requests`, the same one live_draft.py uses.")

LEAGUE_ID = 21985
READS = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leagues/{lid}"
COOKIES = {
    'swid':    '{A7217088-1F36-4F1F-AE73-67262BF763EF}',
    'espn_s2': '',
}
HEADERS = {'accept': 'application/json', 'x-fantasy-platform': 'espn-fantasy-web',
           'x-fantasy-source': 'kona', 'referer': 'https://fantasy.espn.com/'}
HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.normpath(os.path.join(HERE, '..', 'Source'))
# 2026-09-10, doc 270: THE LIVE SEASON WAS NEVER IN THIS TUPLE. Every run wrote 2022-2025 and
# nothing at all for the season being played, so no file on the drive could answer "who dropped
# whom this week" -- which is the one question the in-season sheet actually needs. Derived from
# the date now, so it can never go stale again.
def _current_season(today=None):
    d = today or dt.date.today()
    return d.year if d.month >= 3 else d.year - 1


LIVE_SEASON = _current_season()
SEASONS = tuple(range(2022, LIVE_SEASON + 1))
WIRE_TYPES = ('WAIVER', 'FREEAGENT')


LAST = {}          # what the most recent call actually returned, for the diagnostics below


def _get(season, view, period=None):
    url = READS.format(season=season, lid=LEAGUE_ID) + '?view=' + view
    if period is not None:
        url += '&scoringPeriodId=%d' % period
    r = requests.get(url, cookies=COOKIES, headers=HEADERS, timeout=30)
    LAST.clear(); LAST['status'] = r.status_code; LAST['url'] = url
    if r.status_code == 401:
        sys.exit("\n  401 from ESPN. Run  py set_cookies.py  and try again.\n")
    r.raise_for_status()
    j = r.json()
    LAST['keys'] = sorted(j.keys()) if isinstance(j, dict) else ['<not a dict>']
    LAST['n_tx'] = len(j.get('transactions') or []) if isinstance(j, dict) else -1
    return j


def season_pull(season):
    teams, players = {}, {}
    try:
        for t in _get(season, 'mTeam').get('teams', []):
            nm = (t.get('name') or ' '.join(
                [t.get('location', ''), t.get('nickname', '')]).strip() or str(t.get('id')))
            teams[t.get('id')] = nm
    except Exception as exc:
        print(f"  {season}: could not read team names ({type(exc).__name__})")

    wire, trades, seen = [], [], set()
    census = collections.Counter()
    shown = False
    for wk in range(1, 19):
        try:
            d = _get(season, 'mTransactions2', wk)
        except Exception as exc:
            print(f"  {season} wk{wk}: {type(exc).__name__}: {exc}")
            continue
        # doc 342: 'nothing came back' used to be indistinguishable from 'nobody moved'.
        # Print, ONCE per season, exactly what the feed handed us.
        if not shown:
            shown = True
            print(f"  {season}: HTTP {LAST.get('status')} on mTransactions2 wk{wk}; "
                  f"transactions in the payload: {LAST.get('n_tx')}")
            if not LAST.get('n_tx'):
                print(f"         payload keys: {', '.join(LAST.get('keys') or []) or '<none>'}")
                if 'transactions' not in (LAST.get('keys') or []):
                    print("         *** THE PAYLOAD HAS NO `transactions` KEY AT ALL. ESPN answered")
                    print("         *** without the private view, which is what a dead session looks")
                    print("         *** like when it still serves public data. Run  py set_cookies.py")
        for pl in (d.get('players') or []):
            p = pl.get('player') or {}
            if p.get('id') is not None:
                players[p['id']] = p.get('fullName', 'Player %s' % p['id'])
        for t in (d.get('transactions') or []):
            # doc 342: this key used to be (id, wk). For a COMPLETED season ESPN returns each
            # transaction under its own scoring period only, so it never mattered. For the LIVE
            # season it returns the same set under EVERY scoringPeriodId, so every row landed 13
            # times and waiver_report_2026.csv held 624 rows for 48 transactions. The id alone is
            # unique; 2022-2025 are byte-identical under this key, which is the control.
            key = t.get('id')
            if key in seen:
                continue
            seen.add(key)
            ty = t.get('type')
            census[ty] += 1
            when = ''
            if t.get('proposedDate'):
                when = dt.datetime.fromtimestamp(t['proposedDate'] / 1000).strftime('%Y-%m-%d %H:%M')
            acts = []
            for it in (t.get('items') or []):
                pid = it.get('playerId')
                nm = players.get(pid, 'Player ID %s' % pid)
                bit = f"{it.get('type')} {nm}"
                # A trade has two sides: record who each player went TO and FROM.
                if ty and ty.startswith('TRADE'):
                    fr, to = it.get('fromTeamId'), it.get('toTeamId')
                    if fr or to:
                        bit += f" [{teams.get(fr, fr)} -> {teams.get(to, to)}]"
                acts.append(bit)
            row = {'Week': wk, 'Date': when, 'Team': teams.get(t.get('teamId'), 'Unknown Team'),
                   'Type': ty, 'Status': t.get('status'), 'Transaction': ' | '.join(acts)}
            if ty in WIRE_TYPES:
                wire.append(row)
            elif ty and ty.startswith('TRADE'):
                # doc 262: TeamB was read from memberId (a member GUID) against `teams`
                # (keyed by TEAM id), so it missed on every one of 100 rows and printed ''.
                # The counterparty is already in the item list -- every leg is [FROM -> TO],
                # and the two team names in there ARE the two sides. Take it from there.
                sides = []
                for it in (t.get('items') or []):
                    for tid in (it.get('fromTeamId'), it.get('toTeamId')):
                        nm = teams.get(tid)
                        if nm and nm not in sides:
                            sides.append(nm)
                me = row['Team']
                row['TeamB'] = ' + '.join(x for x in sides if x != me)
                trades.append(row)
    return wire, trades, census


def write(path, rows, cols):
    if not rows:
        # doc 342: returning 0 left the PREVIOUS file on the drive and printed '0 rows', which
        # reads as 'nobody moved' when it means 'this run wrote nothing'. Say which file is stale.
        if os.path.exists(path):
            import datetime as _dt
            when = _dt.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M')
            print(f"  NOT REWRITTEN: {os.path.basename(path)} still holds its {when} contents.")
        return 0
    with open(path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--season', type=int, help='just this one')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--live', action='store_true',
                    help='just the season being played (%d)' % LIVE_SEASON)
    a = ap.parse_args(argv)

    if a.check:
        # doc 342: this used to call mTeam, which ESPN will serve on a session it no longer
        # honours. A green check on a dead cookie is worse than no check. Prove the view this
        # script actually needs.
        _get(LIVE_SEASON, 'mTeam')
        print("  mTeam answered      HTTP %s" % LAST.get('status'))
        _get(LIVE_SEASON, 'mTransactions2', 1)
        ok = 'transactions' in (LAST.get('keys') or [])
        print("  mTransactions2      HTTP %s   transactions key present: %s   rows wk1: %s"
              % (LAST.get('status'), ok, LAST.get('n_tx')))
        if not ok:
            print("\n  *** COOKIES ARE NOT GOOD ENOUGH. ESPN served the league but withheld the")
            print("  *** transaction view. Run  py set_cookies.py  and check again.\n")
            return 2
        print("  cookies OK -- the private view answered for league %d." % LEAGUE_ID)
        return 0

    os.makedirs(SRC, exist_ok=True)
    total_t = 0
    ALL_TYPES = collections.Counter()
    picked = [a.season] if a.season else ([LIVE_SEASON] if a.live else SEASONS)
    for season in picked:
        wire, trades, census = season_pull(season)
        ALL_TYPES.update(census)
        nw = write(os.path.join(SRC, f'waiver_report_{season}.csv'), wire,
                   ['Week', 'Date', 'Team', 'Type', 'Status', 'Transaction'])
        nt = write(os.path.join(SRC, f'trade_report_{season}.csv'), trades,
                   ['Week', 'Date', 'Team', 'TeamB', 'Type', 'Status', 'Transaction'])
        total_t += nt
        print(f"  {season}:  {nw:>4} wire rows -> waiver_report_{season}.csv"
              f"   |   {nt:>3} trade rows -> trade_report_{season}.csv")

    # SECTION 0.2 -- an empty result is not a result, and a GUESS about why is not a diagnosis.
    # 2026-09-09: the run wrote zero trades while Matt remembers at least one. Rather than guess
    # the constant, print every transaction type the feed actually returned. One run settles it.
    print("\n  ================ EVERY TRANSACTION TYPE THE FEED RETURNED ================")
    for ty, n in ALL_TYPES.most_common():
        mark = '   <-- captured as a TRADE' if (ty or '').startswith('TRADE') else ''
        print(f"    {str(ty):28} {n:>5}{mark}")
    print("  =========================================================================")

    if total_t == 0:
        # doc 342: this said "ACROSS EVERY SEASON" on a --live run that looked at ONE season, two
        # weeks old, while trade_report_2022-2025.csv on the drive already hold 45 proposals. It
        # read as a failure. Name the seasons actually examined.
        which = ', '.join(str(x) for x in picked)
        if len(picked) == 1:
            print(f"\n  No trades in {which}. That is the only season this run looked at;"
                  f" trade_report_*.csv on the drive hold the earlier ones.")
        else:
            print(f"\n  *** ZERO TRADES ACROSS {which}. That is either true of this league or the")
            print("  *** feed does not carry them. Do not read it as 'nobody trades' until it is")
            print("  *** checked against one trade you remember happening.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
