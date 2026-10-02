"""
claim_order_log.py -- does ESPN expose the ORDER of my pending waiver claims?
                      And if it does, log it, because the outcome arrives 2 days later.

Doc 403.  Unblocks the item doc 401 left open.

WHY THIS EXISTS
    Doc 401 retracted the 61.1/29.1/11.2 claim-order gradient: the statistic was
    degenerate, and separately the mechanic is UNMEASURABLE from
    waiver_report_*.csv because every claim in a run carries one identical
    timestamp.  ESPN's own page says a winner "will move to the end of the waiver
    order ... until all waiver claims are processed", and that Matt can "reorder
    claims by dragging them into your preferred priority".  So the missing input
    is the ORDER HE SET, paired with which claim won.  That pairing has to be
    captured BEFORE the run, because afterwards the order is gone.

WHAT IT DOES, AND WHAT IT DELIBERATELY DOES NOT
    It is a PROBE FIRST and a logger second, because the schema is unknown.
    On every run it:
      1. asks ESPN for the pending-transaction views,
      2. prints what came back, including the key names of a pending item, so the
         schema is learned from the payload and not guessed,
      3. appends any pending waiver claim it can see to Source\\CLAIM_ORDER_LOG.csv,
         append-only, no state comparison, so there is no silent-skip path
         (same shape as STATUS_LOG.csv, doc 393).
    It does NOT touch wire.py, it writes no page, and nothing in the Sunday path
    reads its output.  If it is wrong it costs one CSV, not a lineup.

    "No pending claims" and "this league does not expose an order field" are both
    LEGITIMATE RESULTS and exit 0.  Failing to REACH ESPN is a failure and exits
    non-zero (directive 0.2: a step that cannot do the thing it is named after
    must fail, and an exit code is not a result).

CREDENTIALS
    Imported from wire.py, never copied.  wire.py guards its main, so importing
    it is side-effect free, and there stays ONE place to rotate cookies.

DEPENDENCIES
    Standard library plus `requests`, which wire.py already uses on his machine
    (directive 0.4 / doc 144: never ship a dependency that is not confirmed there).

USAGE
    py claim_order_log.py            probe and log
    py claim_order_log.py --pair     THE OTHER HALF (29 Sept): join the log to the result and
                                     append Source\\claim_order_outcomes.csv, one row per claim
    py claim_order_log.py --selftest run the negative controls, touch nothing

THE PAIRING (--pair). The log holds the order he set, BEFORE the run. The result lands in
    Source\\waiver_report_2026.csv (py waivers.py --live) AFTER it: Week, Date, Team, Type, Status,
    and "ADD Player ID x | DROP Player ID y". Nothing joined the two, so the one input that would
    settle whether ranking the contested man first pays (doc 401, 0.5(a4)) was being captured and
    never read. The join is the smallest one that works:
      * from the log: per week, the LAST read (the final order he set), one row per claim, order =
        the order field ESPN served or, failing that, the list order as seen;
      * from the report: his team's WAIVER rows for that week with the same ADD id, the row that
        reached the run (not PENDING, not CANCELED), the newest if he re-placed it;
      * outcome: executed / outbid (his failed INVALIDPLAYERSOURCE and another team's claim on the
        same man EXECUTED) / failed (reason) / canceled; a claim with no result row yet is printed
        and NOT written, so the next --pair after py waivers.py --live picks it up;
      * contested: any other team's claim on the same man reached the same run; winner: who got him.
    The report names teams, not ids, so his team name is read from todo_page.TEAM (one copy,
    already on the drive), or given with --team.  Rows already in the outcomes file are not
    written twice (key: week, add id, drop id).
"""
import csv
import datetime as dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import wire  # noqa: E402  -- config only; wire.py guards __main__, import is inert

import requests  # noqa: E402

VIEWS = ('mPendingTransactions', 'mTransactions2')
LOG = os.path.join(wire.SRC, 'CLAIM_ORDER_LOG.csv')
FIELDS = ['read_at', 'run', 'view', 'txn_id', 'seen_order', 'order_field', 'order_value',
          'scoring_period', 'add_player_id', 'drop_player_id', 'status', 'bid']
# the schema is unknown, so look for any of these rather than assuming one
ORDER_KEYS = ('waiverOrder', 'waiverRank', 'processDate', 'priority', 'sortOrder', 'id')


def fetch(view, get=None):
    get = get or requests.get
    url = wire.READS.format(season=wire.SEASON, lid=wire.LEAGUE_ID) + '?view=' + view
    r = get(url, cookies=wire.COOKIES, headers=dict(wire.HEADERS), timeout=30)
    if getattr(r, 'status_code', 200) == 401:
        raise SystemExit("\n  401 from ESPN. Cookies expired. Run  py set_cookies.py  first.\n")
    r.raise_for_status()
    return r.json()


def pending_items(payload):
    """Every pending transaction belonging to MY team, however ESPN nests it."""
    out = []
    for key in ('transactions', 'pendingTransactions'):
        for t in (payload.get(key) or []):
            if t.get('teamId') != wire.MY_TEAM_ID:
                continue
            if str(t.get('status', '')).upper() not in ('PENDING', ''):
                continue
            if str(t.get('type', 'WAIVER')).upper() not in ('WAIVER', 'WAIVER_ERROR', ''):
                continue
            out.append(t)
    return out


def describe(item):
    """What order-ish field does this item actually carry? Learn, do not guess."""
    for k in ORDER_KEYS:
        if k in item and item[k] is not None:
            return k, item[k]
    return '', ''


def rows_for(view, items, run):
    now = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
    rows = []
    for i, t in enumerate(items, 1):
        ok, ov = describe(t)
        add = drop = ''
        for it in (t.get('items') or []):
            if str(it.get('type', '')).upper() == 'ADD':
                add = it.get('playerId', '')
            elif str(it.get('type', '')).upper() == 'DROP':
                drop = it.get('playerId', '')
        rows.append({'read_at': now, 'run': run, 'view': view, 'txn_id': t.get('id', ''),
                     'seen_order': i, 'order_field': ok, 'order_value': ov,
                     'scoring_period': t.get('scoringPeriodId', ''),
                     'add_player_id': add, 'drop_player_id': drop,
                     'status': t.get('status', ''), 'bid': t.get('bidAmount', '')})
    return rows


def append(rows, path=None):
    path = path or LOG
    new = not os.path.exists(path)
    with open(path, 'a', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if new:
            w.writeheader()
        for r in rows:
            w.writerow(r)
    return path


def run_once(get=None, log_path=None):
    run = os.environ.get('FF_WHO', 'manual')
    total, reached = [], 0
    for view in VIEWS:
        try:
            payload = fetch(view, get=get)
        except SystemExit:
            raise
        except Exception as exc:
            print(f"  {view:22} NOT AVAILABLE -- {type(exc).__name__}: {exc}")
            continue
        reached += 1
        items = pending_items(payload)
        print(f"  {view:22} reachable, {len(items)} pending claim(s) for team {wire.MY_TEAM_ID}")
        if items:
            keys = sorted(items[0].keys())
            print(f"      item keys: {', '.join(keys)}")
            ok, ov = describe(items[0])
            print(f"      order field found: {ok or 'NONE OF ' + '/'.join(ORDER_KEYS)}  value={ov!r}")
        total += rows_for(view, items, run)
    if not reached:
        # doc 146: a step that cannot do the thing it is named after must FAIL.
        # Caught by control 1, which this script was ALREADY claiming to handle.
        print("\n  REACHED NO ESPN VIEW. This is a FAILURE, not an empty result --")
        print("  it cannot tell 'no claims pending' from 'could not ask'.")
        return 2
    if not total:
        print("\n  No pending waiver claims visible. That is a legitimate result, not a failure.")
        print("  Run this again AFTER placing claims and BEFORE they process.")
        return 0
    path = append(total, log_path)
    print(f"\n  appended {len(total)} row(s) to {path}")
    if all(not r['order_field'] for r in total):
        print("  NOTE: no order-ish field on any item. The list ORDER as returned is logged as")
        print("  seen_order; whether that reflects his dragged priority is NOT ESTABLISHED.")
    return 0


# ----------------------------------------------------------------------------- the pairing
REPORT = os.path.join(wire.SRC, f'waiver_report_{wire.SEASON}.csv')
OUT = os.path.join(wire.SRC, 'claim_order_outcomes.csv')
OUT_FIELDS = ['week', 'order', 'player_id', 'player', 'drop_id', 'drop', 'contested', 'outcome', 'winner',
              'rivals', 'logged_at', 'settled_at']
RAN = ('EXECUTED', 'FAILED_INVALIDPLAYERSOURCE')     # a rival's claim that reached the run
_ID = re.compile(r'(ADD|DROP) Player ID (-?\d+)')


def my_team_name(given=None):
    """The team name as the report spells it. One copy lives in todo_page.TEAM; never a third."""
    if given:
        return given
    try:
        import todo_page
        return todo_page.TEAM
    except Exception:
        return ''


def _ids(txn):
    d = {k: v for k, v in _ID.findall(txn or '')}
    return d.get('ADD', ''), d.get('DROP', '')


def read_report(path=None):
    path = path or REPORT
    if not os.path.exists(path):
        return None
    rows = []
    with open(path, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            add, drop = _ids(r.get('Transaction'))
            rows.append({'week': (r.get('Week') or '').strip(), 'date': (r.get('Date') or '').strip(),
                         'team': (r.get('Team') or '').strip(), 'type': (r.get('Type') or '').strip().upper(),
                         'status': (r.get('Status') or '').strip().upper(), 'add': add, 'drop': drop})
    return rows


def final_claims(log_rows):
    """One row per claim per week: the LAST read of that week (the final order he set), one view,
    deduped on txn_id. order = ESPN's order field when it served one, else the list order seen."""
    by_week = {}
    for r in log_rows:
        by_week.setdefault(r.get('scoring_period', ''), []).append(r)
    out = []
    for wk, rows in by_week.items():
        last = max(r['read_at'] for r in rows)
        rows = [r for r in rows if r['read_at'] == last]
        view = next((v for v in VIEWS if any(r['view'] == v for r in rows)), rows[0]['view'])
        seen = set()
        for r in rows:
            if r['view'] != view:
                continue
            k = r.get('txn_id') or (r['add_player_id'], r['drop_player_id'])
            if k in seen:
                continue
            seen.add(k)
            try:
                order = int(float(r['order_value'])) if r.get('order_field') else int(r['seen_order'])
            except (TypeError, ValueError):
                order = int(r['seen_order'])
            out.append({'week': wk, 'order': order, 'add': r['add_player_id'], 'drop': r['drop_player_id'],
                        'logged_at': r['read_at']})
    return sorted(out, key=lambda c: (int(c['week'] or 0), c['order']))


def names(src=None):
    """espn_id -> player name, from the roster files and the newest wire, for the printed table."""
    src = src or wire.SRC
    out = {}
    files = [os.path.join(src, 'LEAGUE_ROSTERS.csv'), os.path.join(src, 'MY_ROSTER.csv')]
    wires = sorted(f for f in os.listdir(src) if f.startswith('WIRE_') and f.endswith('.csv')) if os.path.isdir(src) else []
    if wires:
        files.append(os.path.join(src, wires[-1]))
    for p in files:
        if not os.path.exists(p):
            continue
        with open(p, newline='', encoding='utf-8-sig') as fh:
            for r in csv.DictReader(fh):
                if r.get('espn_id') and r.get('player'):
                    out.setdefault(str(r['espn_id']).strip(), r['player'].strip())
    # a defense is -16000 minus ESPN's pro-team id, and wire.PRO already maps those ids
    for tid, code in getattr(wire, 'PRO', {}).items():
        out.setdefault(str(-16000 - tid), f'{code} D/ST')
    return out


def pair_one(claim, report, team):
    """Outcome, contested, winner, rivals and settled_at for one logged claim."""
    wk = claim['week']
    same = [r for r in report if r['type'] == 'WAIVER' and r['add'] == claim['add'] and r['week'] == wk]
    week_note = ''
    if not any(r['team'] == team for r in same) and wk.isdigit():
        nxt = [r for r in report if r['type'] == 'WAIVER' and r['add'] == claim['add'] and r['week'] == str(int(wk) + 1)]
        if any(r['team'] == team for r in nxt):
            same, week_note = nxt, f' (matched in the report under week {int(wk) + 1})'
    mine = [r for r in same if r['team'] == team]
    ran = [r for r in mine if r['status'] not in ('PENDING', 'CANCELED')]
    rivals = [r for r in same if r['team'] != team and r['status'] in RAN]
    won = [r for r in same if r['status'] == 'EXECUTED']
    winner = 'you' if any(r['team'] == team for r in won) else (won[0]['team'] if won else ('nobody' if same else ''))
    contested = 'yes' if rivals else 'no'
    if not mine:
        return None, contested, winner, len(rivals), '', 'no row in the report yet: run  py waivers.py --live  after the run, then --pair again'
    if not ran:
        st = sorted(mine, key=lambda r: r['date'])[-1]['status']
        if st == 'CANCELED':
            return 'canceled before the run', contested, winner, len(rivals), '', ''
        return None, contested, winner, len(rivals), '', 'still PENDING in the report: it was pulled before the run'
    r = sorted(ran, key=lambda r: r['date'])[-1]
    if r['drop'] and claim['drop'] and r['drop'] != claim['drop']:
        week_note += f' (the report shows drop {r["drop"]}, the log {claim["drop"]}: he changed it after logging)'
    if r['status'] == 'EXECUTED':
        out = 'executed'
    elif r['status'] == 'FAILED_INVALIDPLAYERSOURCE':
        out = 'outbid' if any(w['team'] != team for w in won) else 'failed (INVALIDPLAYERSOURCE: nobody won him, he was not on waivers at the run)'
    elif r['status'].startswith('FAILED_'):
        out = 'failed (' + r['status'][7:] + ')'
    else:
        out = r['status'].lower()
    return out + week_note, contested, winner, len(rivals), r['date'], ''


def pair(log_path=None, report_path=None, out_path=None, team=None, src=None):
    """The --pair mode. Returns the exit code; prints the table; appends new rows to the outcomes file."""
    log_path, report_path, out_path = log_path or LOG, report_path or REPORT, out_path or OUT
    team = my_team_name(team)
    if not team:
        print('  cannot pair: the team name is unknown (todo_page.py not importable). Give --team "name".')
        return 2
    if not os.path.exists(log_path):
        print(f'  no log at {log_path}: nothing has been captured yet. Run this after placing claims.')
        return 0
    report = read_report(report_path)
    if report is None:
        print(f'  {report_path} is missing: run  py waivers.py --live  first. Nothing paired.')
        return 2
    with open(log_path, newline='', encoding='utf-8') as fh:
        claims = final_claims(list(csv.DictReader(fh)))
    if not claims:
        print('  the log has no claims in it.')
        return 0
    newest = max((r['date'] for r in report), default='')
    print(f"  report: {os.path.basename(report_path)}, modified "
          f"{dt.datetime.fromtimestamp(os.path.getmtime(report_path)):%Y-%m-%d %H:%M}, newest row {newest}")
    print(f"  team: {team}\n")
    nm = names(src)
    have = set()
    if os.path.exists(out_path):
        with open(out_path, newline='', encoding='utf-8') as fh:
            for r in csv.DictReader(fh):
                have.add((r['week'], r['player_id'], r['drop_id']))
    rows, pending = [], []
    for c in claims:
        outcome, contested, winner, rivals, settled, why = pair_one(c, report, team)
        row = {'week': c['week'], 'order': c['order'], 'player_id': c['add'],
               'player': nm.get(c['add'], ''), 'drop_id': c['drop'], 'drop': nm.get(c['drop'], ''),
               'contested': contested, 'outcome': outcome or why, 'winner': winner, 'rivals': rivals,
               'logged_at': c['logged_at'], 'settled_at': settled}
        (rows if outcome else pending).append(row)
    fmt = '  {week:>4} {order:>5}  {player:<24} {drop:<24} {contested:<9} {outcome:<44} {winner}'
    print(fmt.format(week='week', order='order', player='claim', drop='drop', contested='contested',
                     outcome='outcome', winner='winner'))
    for r in rows + pending:
        show = {k: (str(v) if v != '' else '-') for k, v in r.items()}
        show['player'] = r['player'] or r['player_id']
        show['drop'] = r['drop'] or r['drop_id'] or '(none)'
        print(fmt.format(**show))
    new = [r for r in rows if (r['week'], r['player_id'], r['drop_id']) not in have]
    if new:
        first = not os.path.exists(out_path)
        with open(out_path, 'a', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=OUT_FIELDS)
            if first:
                w.writeheader()
            for r in new:
                w.writerow(r)
    print(f"\n  {len(new)} new row(s) appended to {out_path}"
          + (f"; {len(rows) - len(new)} already there" if len(rows) - len(new) else '')
          + (f"; {len(pending)} NOT written (no result yet)" if pending else ''))
    return 0


class _Resp:
    def __init__(self, payload, code=200):
        self._p, self.status_code = payload, code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code}")

    def json(self):
        return self._p


def selftest():
    import tempfile
    print("--- NEGATIVE CONTROLS (directive 0.2: a guard never executed is not a guard) ---")

    # 1. ESPN unreachable must FAIL, not quietly succeed
    def dead(*a, **k):
        raise requests.ConnectionError("no route to host")
    tmp = os.path.join(tempfile.mkdtemp(), 'x.csv')
    rc = run_once(get=dead, log_path=tmp)
    assert not os.path.exists(tmp), "control 1 FAILED: wrote a log despite reaching nothing"
    # the artifact here IS the exit code, so assert it (directive 0.2 / doc 146).
    # The first cut of this script returned 0 here and printed "legitimate result".
    assert rc != 0, "control 1 FAILED: returned success while reaching nothing"
    print(f"  1. ESPN unreachable      -> reported, no file, exit {rc}      OK")

    # 2. reachable but nothing pending: legitimate, writes nothing
    empty = lambda *a, **k: _Resp({'transactions': []})
    rc = run_once(get=empty, log_path=tmp)
    assert not os.path.exists(tmp), "control 2 FAILED: wrote a log with no pending claims"
    assert rc == 0, "control 2 FAILED: an empty pool is a result, not an error"
    print("  2. reachable, 0 pending  -> reported, no file written       OK")

    # 3. two pending claims WITH an order field: must log both, in order
    payload = {'transactions': [
        {'id': 'txA', 'teamId': wire.MY_TEAM_ID, 'status': 'PENDING', 'type': 'WAIVER',
         'waiverOrder': 1, 'scoringPeriodId': 4,
         'items': [{'type': 'ADD', 'playerId': 111}, {'type': 'DROP', 'playerId': 222}]},
        {'id': 'txB', 'teamId': wire.MY_TEAM_ID, 'status': 'PENDING', 'type': 'WAIVER',
         'waiverOrder': 2, 'scoringPeriodId': 4,
         'items': [{'type': 'ADD', 'playerId': 333}]},
        {'id': 'txC', 'teamId': 99, 'status': 'PENDING', 'type': 'WAIVER', 'waiverOrder': 1,
         'items': [{'type': 'ADD', 'playerId': 444}]},
    ]}
    run_once(get=lambda *a, **k: _Resp(payload), log_path=tmp)
    got = list(csv.DictReader(open(tmp, encoding='utf-8')))
    mine = [r for r in got if r['view'] == VIEWS[0]]
    assert len(mine) == 2, f"control 3 FAILED: expected 2 of my claims, got {len(mine)}"
    assert [r['add_player_id'] for r in mine] == ['111', '333'], "control 3 FAILED: wrong players"
    assert [r['seen_order'] for r in mine] == ['1', '2'], "control 3 FAILED: order not preserved"
    assert mine[0]['order_field'] == 'waiverOrder', "control 3 FAILED: order field not detected"
    assert all(r['add_player_id'] != '444' for r in got), "control 3 FAILED: logged another team"
    print("  3. 2 pending + 1 other   -> logged mine only, order kept    OK")

    # 4. THE PAIRING, on a synthetic log against the REAL report. Week 2 of 2026 is the case the
    #    join exists for: JUG placed five claims, two executed, two failed as already-dropped, and
    #    one lost to another team (-16025: Tets Out For The Boys executed, JUG and Lamar's Loops
    #    failed INVALIDPLAYERSOURCE); and -16012 was CONTESTED AND WON (Tets Out failed on it).
    #    The log had no entries on 29 Sept, so the order below is invented; every OUTCOME is read
    #    off the real file and asserted.
    team = my_team_name()
    assert team, "control 4 FAILED: no team name (todo_page.py not beside this script)"
    assert os.path.exists(REPORT), f"control 4 FAILED: {REPORT} is not there"
    d = tempfile.mkdtemp()
    log, outp = os.path.join(d, 'log.csv'), os.path.join(d, 'out.csv')
    stamp = '2026-09-16 23:45'
    synth = [('4569559', '4360689'), ('-16025', '-16005'), ('3149687', '4360689'),
             ('-16003', '-16005'), ('-16012', '-16005'), ('4040715', '4569603')]   # the last one is fake
    rows = [{'read_at': stamp, 'run': 'test', 'view': VIEWS[0], 'txn_id': f'tx{i}', 'seen_order': i,
             'order_field': 'waiverOrder', 'order_value': i, 'scoring_period': 2,
             'add_player_id': a, 'drop_player_id': dr, 'status': 'PENDING', 'bid': ''}
            for i, (a, dr) in enumerate(synth, 1)]
    # an EARLIER read the same week with a different order must be ignored (the last read wins)
    rows.insert(0, dict(rows[0], read_at='2026-09-16 20:00', seen_order=9, order_value=9))
    append(rows, log)
    rc = pair(log_path=log, out_path=outp, team=team)
    assert rc == 0, f"control 4 FAILED: pair returned {rc}"
    got = {r['player_id']: r for r in csv.DictReader(open(outp, encoding='utf-8'))}
    want = {'4569559': ('executed', 'no', 'you', '0'), '-16012': ('executed', 'yes', 'you', '1'),
            '3149687': ('failed (PLAYERALREADYDROPPED)', 'no', 'nobody', '0'),
            '-16003': ('failed (PLAYERALREADYDROPPED)', 'no', 'nobody', '0'),
            '-16025': ('outbid', 'yes', 'Tets Out For The Boys', '2')}
    for pid, (o, c, w, n) in want.items():
        r = got.get(pid)
        assert r, f"control 4 FAILED: {pid} not written"
        assert (r['outcome'], r['contested'], r['winner'], r['rivals']) == (o, c, w, n), \
            f"control 4 FAILED on {pid}: {r}"
    assert got['4569559']['order'] == '1', "control 4 FAILED: the earlier read's order leaked through"
    assert '4040715' not in got, "control 4 FAILED: a claim with no result was written"
    assert len(got) == 5, f"control 4 FAILED: {len(got)} rows, expected 5"
    print("  4. pair vs real report   -> 5 outcomes right, 1 unresolved held   OK")

    # 5. running --pair twice must not write the same claim twice
    pair(log_path=log, out_path=outp, team=team)
    assert len(list(csv.DictReader(open(outp, encoding='utf-8')))) == 5, "control 5 FAILED: duplicated rows"
    print("  5. pair run twice        -> no duplicate rows                OK")
    print("\nSELFTEST PASSED. Nothing was written outside a temp directory.\n")
    return 0


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    if '--pair' in sys.argv:
        tm = sys.argv[sys.argv.index('--team') + 1] if '--team' in sys.argv else None
        sys.exit(pair(team=tm))
    sys.exit(run_once())
