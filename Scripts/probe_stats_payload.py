"""probe_stats_payload.py -- ONE read-only probe. Answers a single question and writes nothing.

    Does the kona_player_info payload wire.py ALREADY downloads every day carry this season's
    ACTUAL points and a CURRENT projection, per player?

WHY THIS IS A PROBE AND NOT A FIX (directive 0.2). The claim above is a HYPOTHESIS. It is read
off the shape of ESPN's API and off wire.py line 1552, which binds the whole player object and
keeps only `ownership`. It has not been seen on a live payload, and doc 395 is the precedent that
cuts the other way too: a field being in the payload is exactly the sort of thing this project has
been wrong about in both directions. So: look first, build second.

WHY MATT RUNS IT AND NOT ME (directive 0.4, category 1). It needs his ESPN session. It takes about
five seconds.

    py probe_stats_payload.py

COOKIES ARE NEVER COPIED. Config and the fetch helper are imported from wire.py, which is the only
file that holds swid/espn_s2. Nothing here reads, prints or writes a cookie.

EXIT CODES (an exit code is not a result -- doc 146 -- so these mean what they say):
    0  the payload carries season ACTUALS. The fix is small and needs no new ESPN call.
    1  the payload carries projections but NO actuals. A separate pull is needed; say so.
    2  could not reach ESPN at all. NOT a finding about the payload.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))     # doc 144: resolve against the script,
sys.path.insert(0, HERE)                              # never the shell's cwd

try:
    import wire                                        # cookies + endpoint live here, and only here
except Exception as exc:                               # noqa: BLE001
    print(f"cannot import wire.py from {HERE}: {type(exc).__name__}: {exc}")
    print("this probe must sit in the same folder as wire.py.")
    raise SystemExit(2)

# ESPN's stat-row coordinates. statSourceId 0 = what happened, 1 = what was forecast.
# statSplitTypeId 0 = a single scoring period, 1 = the season to date.
SOURCE = {0: 'ACTUAL', 1: 'projected'}
SPLIT = {0: 'week', 1: 'season'}

WATCH = ('Xavier Worthy', 'Rico Dowdle', 'Dalton Schultz', 'Tre Tucker', 'Harrison Mevis')


def main():
    # The filter is carried HERE, not imported: wire.py builds it as a local (line ~1371), so
    # `wire.PLAYER_FILTER` does not exist and importing it would die on his machine (doc 144).
    # filterStatus is left OFF on purpose -- the watch list below is mostly ROSTERED, and the
    # free-agent filter wire.py uses would hide every one of them.
    xf = {"players": {"limit": 400, "offset": 0,
                      "sortPercOwned": {"sortAsc": False, "sortPriority": 1}}}
    try:
        data = wire._get('kona_player_info', xf)
    except Exception as exc:                            # noqa: BLE001
        print(f"COULD NOT REACH ESPN ({type(exc).__name__}). This says nothing about the "
              f"payload -- it is a connection result, not a finding.")
        return 2

    pool = data.get('players') or []
    if not pool:
        print("ESPN RETURNED AN EMPTY LIST. Not a result. Nothing below would mean anything.")
        return 2

    print(f"players in payload: {len(pool)}")
    print(f"scoringPeriodId   : {data.get('scoringPeriodId')}\n")

    seen_kinds, any_actual, shown = set(), False, 0
    for entry in pool:
        p = entry.get('player') or {}
        name = p.get('fullName') or ''
        stats = p.get('stats') or []
        for s in stats:
            kind = (s.get('statSourceId'), s.get('statSplitTypeId'))
            seen_kinds.add(kind)
            if s.get('statSourceId') == 0 and s.get('statSplitTypeId') == 1:
                if (s.get('appliedTotal') or 0) > 0:
                    any_actual = True
        if name in WATCH and shown < len(WATCH):
            shown += 1
            print(f"--- {name} ---   stat rows: {len(stats)}")
            for s in stats:
                src = SOURCE.get(s.get('statSourceId'), f"src{s.get('statSourceId')}")
                spl = SPLIT.get(s.get('statSplitTypeId'), f"split{s.get('statSplitTypeId')}")
                tot = s.get('appliedTotal')
                tot = f"{tot:.1f}" if isinstance(tot, (int, float)) else str(tot)
                print(f"      {src:<10} {spl:<7} period {str(s.get('scoringPeriodId')):<4} "
                      f"seasonId {s.get('seasonId')}  appliedTotal {tot}")
            print()

    print("stat row kinds present (statSourceId, statSplitTypeId):")
    for k in sorted(seen_kinds, key=lambda x: (str(x[0]), str(x[1]))):
        print(f"      {k}   {SOURCE.get(k[0], '?')} / {SPLIT.get(k[1], '?')}")

    print()
    if any_actual:
        print("RESULT: the payload CARRIES season actuals. The week sheet can be fixed inside "
              "wire.py with no new ESPN call and no new pull script.")
        return 0
    print("RESULT: NO season actuals with a non-zero total in this payload. A separate pull is "
          "needed, and the week sheet cannot be fixed from this view alone.")
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
