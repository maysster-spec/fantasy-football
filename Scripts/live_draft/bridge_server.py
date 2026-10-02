#!/usr/bin/env python
r"""
bridge_server.py -- the listener half of the ESPN Draft Bridge.  Doc 137.

WHY
    Doc 136: ESPN's REST read replica publishes a draft only after it ENDS.  The live picks are in
    the browser the entire time -- which is exactly why a FantasyPros extension can display them.
    So the extension in .\espn_bridge\ listens to the page and POSTs everything here, and this
    process turns it into a file live_draft.py can read.

    THE EXTENSION PARSES NOTHING ON PURPOSE.  Every guess about ESPN's message shape lives in this
    file, so it can be fixed by editing Python -- no extension reload, no browser restart, nothing
    to redo at 8pm on a Monday.

USAGE
    py bridge_server.py                 listen, print what arrives, write bridge_picks.json
    py bridge_server.py --recon         same, but ALSO dump every distinct message shape it sees
                                        (run this the first time and send me the output)

    Then, in the other window:
    py live_draft.py --bridge           read picks from bridge_picks.json instead of from ESPN

WRITES
    bridge_raw.jsonl    every event, raw, append-only -- the diagnostic record
    bridge_picks.json   {"picks":[{"overall":1,"round":1,"team":12,"pid":4429795}, ...]}

It listens on 127.0.0.1:8787 and talks to nothing else.  Ctrl+C stops it.
"""
import argparse, datetime as dt, json, os, re, sys, threading
from collections import Counter
from http.server import BaseHTTPRequestHandler, HTTPServer

# The draft socket URL carries the SWID in the query string:
#   wss://fantasydraft.espn.com/game-1/league-.../JOIN?...&4={A7217088-...}&5=1:...:{A7217088-...}
# That is an account credential.  §1's rule is that it is never read, stored or printed, and
# bridge_raw.jsonl is a file on disk that gets pasted into chats.  Scrub it on the way in.
SWID_RE = re.compile(r'\{[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}\}')


def scrub(x):
    if isinstance(x, str):
        return SWID_RE.sub('{SWID-REDACTED}', x)
    if isinstance(x, dict):
        return {k: scrub(v) for k, v in x.items()}
    if isinstance(x, list):
        return [scrub(v) for v in x]
    return x

HERE  = os.path.dirname(os.path.abspath(__file__))
RAW   = os.path.join(HERE, 'bridge_raw.jsonl')
PICKS = os.path.join(HERE, 'bridge_picks.json')
PORT  = 8787

STATE   = {}          # overall -> pick dict
SHAPES  = Counter()
LOCK    = threading.Lock()
RECON   = False


def real(v):
    """doc 123: an empty ESPN slot carries playerId -1, and -1 is TRUTHY.  All 32 D/ST ride the
    wire as -16000 - proTeamId, so negatives are NOT the test.  Magnitude is."""
    try:
        return abs(int(v)) > 100
    except (TypeError, ValueError):
        return False


# doc 137 v1.2.  ESPN's draft socket speaks a LINE PROTOCOL, not JSON:
#     PONG PING%201788390343249
#     CLOCK 4
#     AUTODRAFT 9 false
#     TOKEN 1:<league>:<team>:<swid>:<memberId>
#     INIT <base64 of a binary room-config blob -- league id, clocks, scoring. NOT picks.>
# 607 frames arrived in the first run and produced 0 picks because the parser only understood
# JSON.  Everything below reads the real format, and -- more importantly -- LOUDLY REPORTS ANY
# VERB IT DOES NOT KNOW, because the pick verb is the one thing we still have to learn.
VERBS_SEEN = Counter()
VERB_SAMPLE = {}
# v1.4 -- the real protocol, from a 872-event capture of a full ESPN practice draft, 2026-09-02:
#     SELECTED <teamId> <playerId> <roundId>   <-- THE PICK.  221 of them in a 12x16 draft.
#     SELECTING <teamId> <clockMs>             who is on the clock
#     AUTOSUGGEST <playerId>                   ESPN's own suggestion for YOU -- not a pick
#     CLOCK <n> <ms> · PONG · STATE <n> · JOINED <team> <swid> · AUTODRAFT <team> <bool> · INIT <b64>
KNOWN_NOISE = {'PONG', 'PING', 'CLOCK', 'TOKEN', 'INIT', 'AUTODRAFT', 'CHAT', 'MSG',
               'KEEPALIVE', 'STATUS', 'PAUSED', 'RESUMED', 'JOINED', 'LEFT', 'MEMBER',
               # each of these carries a playerId-sized number and is NOT a pick.  AUTOSUGGEST in
               # particular emitted 205 DISTINCT player ids in one draft -- it would have
               # auto-promoted itself and injected 205 phantom picks straight onto the board.
               'SELECTING', 'AUTOSUGGEST', 'STATE', 'SUGGEST', 'QUEUE', 'WATCH', 'ONDECK'}
# doc 148, red team finding 7.  Five of the eight words here were GUESSES, and one of them was
# proved to inject picks: `ONCLOCK 9 60000` -- a team and a 60-second clock in milliseconds --
# was captured as "team 9 drafted player 60000", one phantom pick per message, and the pick
# counter never recovers.  A phantom pick is the doc 58 defect with a different cause.
#
# THE FIX IS THE VERB LIST, NOT A NUMBER RANGE.  The obvious tightening -- "a real playerId is
# 5-7 digits" -- was measured against the shipped board before being written and would have
# DELETED THIRTEEN REAL PLAYERS: espn_id runs from 8,439 up, and four ids sit in the 16,000s,
# the same magnitude as the -16001..-16032 a D/ST rides on.  Magnitude cannot separate a clock
# from a player here.  Grammar can: a PAST-TENSE verb reports an event that has happened.
#
# CONFIRMED by the 2026-09-02 capture (872 events, 179 picks captured live end to end):
PICK_VERBS = {'SELECTED', 'PICKED', 'DRAFTED', 'AUTOPICK'}
# Present tense / ambiguous.  These announce a STATE, not a completed selection, and each was
# observed or is expected to carry a clock, a timer or a suggestion.  Watched and reported as
# candidates, never trusted.  `--loose` puts them back if ESPN changes its wording on the night.
LOOSE_VERBS = {'SELECT', 'PICK', 'DRAFT', 'ONCLOCK'}

# v1.3 -- AUTO-PROMOTION.  I do not know what ESPN calls its pick message, and waiting to be told
# makes draft night depend on a round trip through me.  So: any unknown verb that produces THREE
# DISTINCT playerId-sized numbers is, on the evidence, the pick verb -- nothing else in a draft
# room emits a growing set of six-digit ids.  It promotes itself, says so, and back-fills the
# candidates it had already set aside.  If it promotes something wrong, the verb name is printed
# and the fix is one line in PICK_VERBS.
CANDIDATES = {}          # verb -> {pid: line}
PROMOTE_AT = 3
# doc 148, finding 8.  Promotion existed because the pick verb was UNKNOWN.  It is not unknown
# any more -- SELECTED is confirmed on an 872-event capture -- and leaving it armed means any
# unknown verb carrying three large numbers plus one number in 1-32 can still inject picks onto
# the board with nothing but a line in the OTHER window to say so.  Verified: four NOMINATED
# lines promoted NOMINATED and back-filled three ids.  Off unless --loose.
PROMOTE = False
REPLAYING = False        # v1.7: segment the append-only log by session
SESSION_START = dt.datetime.now().isoformat()   # v1.8: freshness stamp for the handoff file


def parse_line_protocol(text):
    """Return (picks_found, notes).  Shape-agnostic: any verb whose arguments contain something
    playerId-sized is reported as a CANDIDATE even if the verb is unknown to us."""
    found, notes = {}, []
    for line in text.replace('\r', '').split('\n'):
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        verb = parts[0].upper()
        args = parts[1:]
        VERBS_SEEN[verb] += 1
        if verb not in VERB_SAMPLE:
            VERB_SAMPLE[verb] = line[:180]
            if verb not in KNOWN_NOISE:
                notes.append(('NEW VERB', line[:180]))
        nums = []
        for a in args:
            try:
                nums.append(int(a))
            except ValueError:
                pass
        big = [x for x in nums if abs(x) > 100]

        # SELECTED <team> <playerId> <round> -- parse it exactly rather than by heuristic
        if verb == 'SELECTED' and len(nums) >= 2 and abs(nums[1]) > 100:
            found[len(found) + 1] = {'overall': None,
                                     'round': nums[2] if len(nums) > 2 else 0,
                                     'team': nums[0], 'pid': nums[1],
                                     '_verb': verb, '_line': line[:180]}
            continue

        if verb in PICK_VERBS and big:
            # best guess at ordering: the playerId is the biggest magnitude; a small int is a team
            pid = max(big, key=abs)
            small = [x for x in nums if abs(x) <= 100]
            found[len(found) + 1] = {'overall': None, 'round': 0,
                                     'team': small[0] if small else 0, 'pid': pid,
                                     '_verb': verb, '_line': line[:180]}
        elif big and verb not in KNOWN_NOISE:
            pid = max(big, key=abs)
            seen = CANDIDATES.setdefault(verb, {})
            if pid not in seen:
                seen[pid] = line[:180]
                notes.append(('CANDIDATE', f'{line[:150]}   [{verb}: {len(seen)} distinct ids]'))
            small_here = [x for x in nums if 0 < abs(x) <= 32]
            if not small_here:
                continue        # no team id -- a suggestion or a clock, never a selection
            if PROMOTE and len(seen) >= PROMOTE_AT and verb not in PICK_VERBS:
                PICK_VERBS.add(verb)
                notes.append(('*** PROMOTED', f'{verb} is the pick verb -- {len(seen)} distinct '
                                              f'player ids seen. Back-filling.'))
                for i, (p_, ln) in enumerate(seen.items(), 1):
                    sm = [x for x in re.findall(r'-?\d+', ln) if abs(int(x)) <= 100]
                    found[f'bf{i}'] = {'overall': None, 'round': 0,
                                       'team': int(sm[0]) if sm else 0, 'pid': p_,
                                       '_verb': verb, '_line': ln}
    return found, notes


def _first(d, *keys):
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return None


def harvest(obj, found):
    """Walk anything and collect dicts that look like a draft pick, whatever they are nested in.
    Shape-agnostic by design -- we do not yet know ESPN's live message format."""
    if isinstance(obj, dict):
        pid = _first(obj, 'playerId', 'player_id', 'playerid', 'pid', 'plyrId')
        ov  = _first(obj, 'overallPickNumber', 'overall', 'pickNumber', 'overallPick',
                     'pick', 'pickNo', 'selectionNumber')
        if pid is not None and ov is not None and real(pid):
            try:
                found[int(ov)] = {
                    'overall': int(ov),
                    'round':   int(_first(obj, 'roundId', 'round', 'roundNumber', 'rd') or 0),
                    'team':    int(_first(obj, 'teamId', 'team', 'teamid', 'tmId') or 0),
                    'pid':     int(pid),
                }
            except (TypeError, ValueError):
                pass
        for v in obj.values():
            harvest(v, found)
    elif isinstance(obj, list):
        for v in obj:
            harvest(v, found)


def ingest(ev):
    kind = ev.get('kind')
    pay  = ev.get('payload') or {}
    if RECON:
        key = kind
        if kind in ('ws-msg', 'fetch', 'xhr'):
            u = scrub(pay.get('url') or '')[:70]
            key = f'{kind} {u}'
        SHAPES[key] += 1
        # print the first few of EVERY kind, verbatim, so the format is visible without
        # shipping a log file anywhere.
        if SHAPES[key] <= 2 and kind in ('ws-other', 'ws-error'):
            d = scrub(str(pay.get('data') or ''))[:400]
            b = ' [BINARY %s bytes]' % pay.get('bytes') if pay.get('binary') else ''
            print(f'  --- SAMPLE {kind}{b} #{SHAPES[key]} ---')
            print(f'      {d!r}')
    if kind == 'ws-open':
        print(f'  [{dt.datetime.now():%H:%M:%S}] WEBSOCKET OPENED -> '
              f'{scrub(pay.get("url") or "")[:120]}')
        return
    if kind == 'hooked':
        # a new page = a new draft room.  On replay, close the previous segment and start clean,
        # or the counts silently span two different leagues.
        if REPLAYING and STATE:
            print()
            print('  --- end of a captured session ---')
            audit()
            print('  --- new page hooked, starting a fresh segment ---')
            print()
            STATE.clear()
            CANDIDATES.clear()
        print(f'  [{dt.datetime.now():%H:%M:%S}] page hooked: {scrub(pay.get("href",""))[:100]}')
        return
    data = pay.get('data')
    if not data:
        return
    # line protocol first -- this is what the draft socket actually speaks
    if kind in ('ws-msg', 'ws-send') and isinstance(data, str) and not data.lstrip().startswith(('{', '[')):
        found, notes = parse_line_protocol(data)
        for tag, line in notes:
            print(f'  [{dt.datetime.now():%H:%M:%S}] {tag}: {scrub(line)}')
        if found:
            with LOCK:
                # v1.5 -- DEDUPE BY PLAYER, NOT BY ARRIVAL ORDER.
                # The 09-02 capture holds 221 SELECTED messages for a 12x16 = 192-pick draft.
                # The socket reconnected three times and ESPN RE-SENT history each time, so 29
                # were repeats.  Numbering by arrival would have put the board 29 picks ahead of
                # the room -- precisely the doc 58 defect that made the live tool never fire, and
                # it would have looked perfectly healthy: 221 picks "known", counter climbing.
                # A player can only be drafted once, so playerId is the identity.
                added = 0
                for v in found.values():
                    if any(x['pid'] == v['pid'] for x in STATE.values()):
                        continue
                    v['overall'] = (max(STATE) if STATE else 0) + 1
                    STATE[v['overall']] = v
                    added += 1
                if not added:
                    return
                dupes = len(found) - added
                if not REPLAYING or len(STATE) % 25 == 0:
                    print(f'  [{dt.datetime.now():%H:%M:%S}] {len(STATE):>3} picks known  '
                          f'(+{added}{f", {dupes} repeat" if dupes else ""})')
                _write_picks()
        return
    try:
        js = json.loads(data)
    except Exception:
        # some feeds wrap JSON in a prefix; grab the first {...} or [...] and retry once
        m = re.search(r'[\[{].*[\]}]', data, re.S)
        if not m:
            return
        try:
            js = json.loads(m.group(0))
        except Exception:
            return
    found = {}
    harvest(js, found)
    if not found:
        return
    with LOCK:
        # doc 148, finding 6.  THE LINE-PROTOCOL PATH DEDUPES BY PLAYER AND THIS ONE DID NOT.
        # `STATE.update(found)` keys on overall pick number, so the same player arriving twice
        # under two different pick numbers -- which is exactly what ESPN does when the socket
        # reconnects and it re-sends history -- was counted twice, and every duplicate puts the
        # board one pick ahead of the room.  v1.5 fixed this for one path and left the other.
        # A player can only be drafted once; playerId is the identity on BOTH paths.
        before = len(STATE)
        dupes = 0
        for k, v in found.items():
            if any(x['pid'] == v['pid'] for x in STATE.values()):
                dupes += 1
                continue
            STATE[k] = v
        if len(STATE) != before:
            newest = max(STATE)
            print(f'  [{dt.datetime.now():%H:%M:%S}] {len(STATE):>3} picks known '
                  f'(latest overall {newest}, +{len(STATE)-before} this message'
                  f'{f", {dupes} repeat" if dupes else ""})  via {kind}')
            _write_picks()



def _atomic_write(payload):
    """v1.9 (doc 139): NEVER LEAVE A HALF-WRITTEN HANDOFF FILE ON DISK.

    live_draft.py --bridge polls this file continuously.  A plain open(PICKS,'w') truncates
    it to zero bytes and holds it empty for the whole json.dump; a poll landing in that
    window read an unparseable or empty file.  On 2026-09-02 that printed
    `[20:00:14] 0 real picks in` in the middle of a live draft -- and zero picks means the
    engine is told every drafted player is available again.  It corrected itself on the next
    poll only because the render happened to be cheap.

    Write a sibling .tmp and os.replace() it.  The rename is atomic on Windows and POSIX
    alike, so a reader gets the previous complete file or the new complete file, never a
    partial one.  This removes the failure mode instead of coping with it -- live_draft.py's
    last-good cache is the second line of defence, not the fix."""
    tmp = PICKS + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(payload, f)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, PICKS)


def _write_picks():
    _atomic_write({'picks': [STATE[k] for k in sorted(STATE)],
                   'session_started': SESSION_START,
                   'updated': dt.datetime.now().isoformat()})


class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_POST(self):
        n = int(self.headers.get('Content-Length') or 0)
        body = self.rfile.read(n)
        self.send_response(200); self._cors(); self.end_headers(); self.wfile.write(b'ok')
        try:
            msg = json.loads(body)
        except Exception:
            return
        msg = scrub(msg)
        with open(RAW, 'a') as f:
            f.write(json.dumps({'t': dt.datetime.now().isoformat(), 'body': msg}) + '\n')
        for ev in msg.get('events', []):
            try:
                ingest(ev)
            except Exception as e:
                print('  ingest error:', type(e).__name__, e)

    def log_message(self, *a):
        pass


def audit():
    """v1.6 -- SAY WHETHER THE CAPTURE IS COMPLETE, rather than leaving a bare count to be
    interpreted.  221 SELECTED messages produced 179 unique picks; whether that is 42 re-sends of
    a finished draft or 42 re-sends of an unfinished one is not something a total can answer, and
    a number nobody can check is not a result."""
    if not STATE:
        print('  no picks to audit.')
        return
    picks = [STATE[k] for k in sorted(STATE)]
    rounds = Counter(p['round'] for p in picks)
    teams  = Counter(p['team'] for p in picks)
    known  = [r for r in rounds if r]
    nteams = len([t for t in teams if t])
    print()
    print('  CAPTURE AUDIT')
    print(f'    unique players : {len({p["pid"] for p in picks})}')
    print(f'    teams seen     : {nteams}')
    if known:
        lo, hi = min(known), max(known)
        print(f'    rounds         : {lo} to {hi}')
        full = [r for r in range(lo, hi + 1) if rounds.get(r, 0) == nteams]
        short = [(r, rounds.get(r, 0)) for r in range(lo, hi + 1) if rounds.get(r, 0) != nteams]
        print(f'    complete rounds: {len(full)} of {hi - lo + 1}')
        if short:
            print(f'    SHORT ROUNDS   : ' + ', '.join(f'rd {r} has {c}/{nteams}' for r, c in short[:8]))
            last = short[-1]
            if last[0] == hi:
                print(f'    -> round {hi} is partial, so the DRAFT WAS STILL RUNNING when this was')
                print(f'       captured. {len(picks)} of an expected {nteams} x {hi} = {nteams*hi}.')
            else:
                print('    -> a MIDDLE round is short. That is a real gap, not an unfinished draft.')
                print('       Most likely the extension attached after the room opened.')
        else:
            print(f'    -> every round complete. {len(picks)} picks, clean capture.')
    dupes = len(picks) - len({p['pid'] for p in picks})
    if dupes:
        print(f'    !! {dupes} duplicate playerIds survived dedupe -- that is a bug, tell me.')


def main():
    global RECON, PROMOTE
    ap = argparse.ArgumentParser()
    ap.add_argument('--recon', action='store_true', help='also summarise every message shape seen')
    ap.add_argument('--replay', metavar='FILE', nargs='?', const=RAW,
                    help='do not listen -- read an existing bridge_raw.jsonl and report the verbs. '
                         'Use this on a log you already captured; no draft needed.')
    ap.add_argument('--port', type=int, default=PORT)
    # doc 148, findings 7 and 8.  The escape hatch, and it is deliberately one flag and not the
    # default: if ESPN has changed its wording on the night, the board will say "no picks read
    # yet" (it no longer invents a pick-1 page) and the CANDIDATE lines here will name the verb.
    # THEN use this.  It re-arms the four present-tense verbs and auto-promotion together.
    ap.add_argument('--loose', action='store_true',
                    help='trust the ambiguous pick verbs and re-arm auto-promotion. Only if the '
                         'strict list captured nothing and the CANDIDATE lines name a new verb.')
    a = ap.parse_args()
    RECON = True if a.replay else a.recon
    if a.loose:
        global PROMOTE
        PICK_VERBS.update(LOOSE_VERBS)
        PROMOTE = True
        print('  --loose: also trusting ' + ', '.join(sorted(LOOSE_VERBS)) +
              ' and re-arming auto-promotion.')
        print('  A clock or a timer carried by one of those words becomes a PHANTOM PICK and')
        print('  puts the board ahead of the room. Watch the pick count against ESPN.')
    if a.replay:
        global REPLAYING, PICKS
        REPLAYING = True
        PICKS = os.path.join(HERE, 'bridge_picks_REPLAY.json')   # never the live file
        path = a.replay
        print('=' * 72)
        print(f'  REPLAY -- reading {path}, no listening, no draft needed')
        print('=' * 72)
        n = 0
        with open(path, encoding='utf-8', errors='replace') as f:
            for ln in f:
                try:
                    body = json.loads(ln).get('body') or {}
                except Exception:
                    continue
                for ev in body.get('events', []):
                    n += 1
                    try:
                        ingest(ev)
                    except Exception:
                        pass
        print()
        print(f'  {n} events replayed.  Final segment:')
        audit()
        if VERBS_SEEN:
            print()
            print('  DRAFT-SOCKET VERBS IN THAT LOG:')
            for k, v in VERBS_SEEN.most_common(60):
                mark = '   <-- UNKNOWN, send me this' if k not in KNOWN_NOISE and k not in PICK_VERBS else ''
                print(f'    {v:>5}  {k:<14} {scrub(VERB_SAMPLE.get(k, ""))[:100]}{mark}')
        return
    print('=' * 72)
    print(f'  ESPN DRAFT BRIDGE -- listening on http://127.0.0.1:{a.port}')
    print(f'  raw log : {RAW}')
    print(f'  picks   : {PICKS}')
    print('  Load the extension, open the draft room, and watch this window.')
    print('=' * 72)
    # doc 137 v1.8: a new listener means a new draft.  Reset the handoff file and stamp it with
    # this session's start time, so live_draft.py can refuse a file left over from last night.
    _atomic_write({'picks': [], 'session_started': SESSION_START,
                   'updated': dt.datetime.now().isoformat()})
    print(f'  reset {os.path.basename(PICKS)} -- this session starts from zero picks')
    srv = HTTPServer(('127.0.0.1', a.port), H)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print()
        if VERBS_SEEN:
            print('  DRAFT-SOCKET VERBS SEEN  --  THIS IS WHAT I NEED:')
            for k, v in VERBS_SEEN.most_common(40):
                mark = '   <-- unknown' if k not in KNOWN_NOISE and k not in PICK_VERBS else ''
                print(f'    {v:>5}  {k:<12} {scrub(VERB_SAMPLE.get(k,""))[:110]}{mark}')
        if RECON and SHAPES:
            print()
            print('  transport shapes:')
            for k, v in SHAPES.most_common(15):
                print(f'    {v:>5}  {k}')
        print(f'  {len(STATE)} picks captured.  raw log: {RAW}')


if __name__ == '__main__':
    main()
