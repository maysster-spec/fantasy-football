"""
rehearsal.py -- a FULL DRESS REHEARSAL of draft night, with no ESPN involved.

WHY THIS EXISTS (doc 96)
    Everything about the live tool had been tested except the one thing that matters: the tool
    running, in a browser, against a draft that is CHANGING. `--replay 2025` proves the feed
    parser, the keeper filter and the render maths -- but it returns BEFORE the browser is ever
    opened, it never holds on a pick, and it never reaches the D/ST or K pages the way the night
    will. So the browser-open line, the on-clock page, the pick-152/161 pages and the completion
    panel had all never been seen on Matt's own screen.

    This starts a tiny web server on your own machine that answers in ESPN's exact shape, then
    starts the REAL live_draft.py against it. Same poll loop, same renderer, same browser, same
    Google Drive path. Nothing is written anywhere. Nothing touches ESPN. Ctrl+C ends it.

WHAT IT IS NOT
    The pick order is synthetic (ADP order with a little noise). It is a PLUMBING and EYES test.
    Do not read strategy off it -- live_draft prints a banner saying exactly that.

USAGE
    py rehearsal.py                 ~4 minutes, holds 5s on each of your 14 picks
    py rehearsal.py --realtime      ~25 minutes, 8s a pick -- what the night actually feels like
    py rehearsal.py --from 148      jump in just before the D/ST and K pages
    py rehearsal.py --keepers end   put the 12 keeper rows at 169-180 instead of at the start
"""
import argparse, json, os, random, subprocess, sys, threading, time
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
KIT  = os.path.join(HERE, 'live_draft')
PORT = 8899
MY_TEAM_ID = 9          # must match live_draft.MY_TEAM_ID
MY_SLOT    = 8
TEAMS, ROUNDS = 12, 14

# slot -> ESPN teamId. Only slot 8 -> 9 matters (it is the pairing live_draft assumes);
# the other ten are stand-ins, and the abbrevs come from the SECTION 5 opponent table so the
# startup identity line looks exactly like the real one.
SLOT_TEAM = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:9, 9:8, 10:10, 11:11, 12:12}
ABBREV = {1:'DUCK',2:'FLEM',3:'AAT',4:'TURD',5:'WGTS',6:'BC',7:'BATE',9:'JUG',
          8:'Boo',10:'POT',11:'TAYL',12:'Tets'}
NAMES  = {1:'Cary',2:'Fleming',3:'Ray',4:'Brown/Collins',5:'herman allen',6:'Kam',
          7:'Grenier',9:'Matt Mays',8:'Snyder',10:'Rychlicki',11:'Taylor',12:'Lobsinger'}


def build_order(keepers_at_end):
    """168 real picks in noisy ADP order + the 12 keeper rows, in ESPN's shape."""
    import csv
    rows = []
    with open(os.path.join(KIT, 'board_v8_fixed.csv'), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            try:
                rows.append((float(r['adp_pick']), int(float(r['espn_id'])), r['player'], r['pos']))
            except (ValueError, KeyError):
                continue
    rng = random.Random(2026)
    rows.sort(key=lambda x: x[0] + rng.gauss(0, 0.111*min(x[0], 200) + 5.40))   # SS 4.12
    pool = [r for r in rows if r[1]]
    real, keeps = pool[:168], pool[168:180]

    picks = []
    for i, (_, pid, name, pos) in enumerate(real):
        overall = i + 1
        rnd = i // TEAMS + 1
        j = i % TEAMS
        slot = (j + 1) if rnd % 2 else (TEAMS - j)
        picks.append(dict(overallPickNumber=overall, roundId=rnd, playerId=pid,
                          teamId=SLOT_TEAM[slot], keeper=False, _n=name, _p=pos))
    keeper_rows = [dict(overallPickNumber=169+i, roundId=15, playerId=k[1],
                        teamId=SLOT_TEAM[(i % TEAMS)+1], keeper=True, _n=k[2], _p=k[3])
                   for i, k in enumerate(keeps)]
    return picks, keeper_rows, keepers_at_end


class Feed:
    """Everything the handler reads. `n` is how many REAL picks have happened."""
    def __init__(self, picks, keeper_rows, keepers_at_end):
        self.picks, self.keeper_rows, self.at_end = picks, keeper_rows, keepers_at_end
        self.n = 0
        self.lock = threading.Lock()

    def payload(self):
        with self.lock:
            n = self.n
        out = list(self.picks[:n])
        if self.at_end:
            if n >= len(self.picks): out += self.keeper_rows
        else:
            out = self.keeper_rows + out
        # doc 123. THIS IS WHY THE REHEARSAL LANE NEVER CAUGHT THE WORST BUG IN THE PROJECT.
        # It served only picks that had HAPPENED. Real ESPN pre-creates the ENTIRE grid the
        # moment the room opens -- every (round, team) slot present, with an empty playerId --
        # and the tool counted those as selections and declared the draft over before pick 1.
        # A harness that is kinder than reality tests nothing. It now emits the empty slots too.
        made = {p['overallPickNumber'] for p in out}
        total = len(self.picks) + (len(self.keeper_rows) if self.at_end else 0)
        for ov in range(1, total + 1):
            if ov not in made:
                out.append(dict(overallPickNumber=ov, roundId=(ov - 1)//TEAMS + 1,
                                playerId=-1, teamId=SLOT_TEAM[((ov - 1) % TEAMS) + 1],
                                keeper=False))
        out.sort(key=lambda p: p['overallPickNumber'])
        return {'draftDetail': {'drafted': n >= len(self.picks), 'inProgress': True,
                                'picks': [{k: v for k, v in p.items() if not k.startswith('_')}
                                          for p in out]}}


def make_handler(feed):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a): pass          # the poller hits this every 3 seconds
        def do_GET(self):
            if 'mTeam' in self.path:
                body = {'teams': [{'id': SLOT_TEAM[s], 'abbrev': ABBREV[SLOT_TEAM[s]],
                                   'name': NAMES[SLOT_TEAM[s]]} for s in range(1, TEAMS+1)]}
            else:
                body = feed.payload()
            b = json.dumps(body).encode()
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.send_header('content-length', str(len(b)))
            self.end_headers()
            self.wfile.write(b)
    return H


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--realtime', action='store_true', help='8s a pick (~25 min)')
    ap.add_argument('--pace', type=float, help='seconds per pick (overrides --realtime)')
    ap.add_argument('--hold', type=float, help='extra seconds on YOUR picks')
    ap.add_argument('--from', dest='start', type=int, default=0, help='skip ahead to this pick')
    ap.add_argument('--keepers', choices=['start', 'end'], default='start')
    a = ap.parse_args()
    pace = a.pace if a.pace else (8.0 if a.realtime else 1.2)
    hold = a.hold if a.hold is not None else (25.0 if a.realtime else 5.0)

    for n in ('live_draft.py', 'board_v8_fixed.csv'):
        if not os.path.exists(os.path.join(KIT, n)):
            raise SystemExit(f"{n} not found in {KIT} -- run this from Scripts\\, next to live_draft\\")

    picks, keeper_rows, _ = build_order(a.keepers == 'end')
    feed = Feed(picks, keeper_rows, a.keepers == 'end')
    feed.n = max(0, min(a.start, len(picks)))

    srv = HTTPServer(('127.0.0.1', PORT), make_handler(feed))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{PORT}/apis/v3/games/ffl/seasons/{{season}}/segments/0/leagues/{{lid}}"

    mine = [8,17,32,41,56,65,80,89,104,113,128,137,152,161]
    print("="*72)
    print("  REHEARSAL -- no ESPN, nothing written, Ctrl+C ends it")
    print(f"  {len(picks)} picks at {pace:g}s each, holding {hold:g}s on YOUR picks")
    print(f"  keeper rows: {'at 169-180, appearing at the end' if a.keepers=='end' else 'in the feed from the start (12 of them)'}")
    print("\n  WATCH FOR, in order:")
    print("   1. the black window says  team 9 = JUG \"Matt Mays\"  <- IS THIS YOU?")
    print("   2. a browser opens BY ITSELF on the amber 'Waiting for ESPN' page")
    print("      (that page and that automatic open have NEVER run on this machine)")
    print("   3. it fills in, and the keeper-row count reads 12")
    print("   4. at picks 8/17/32... the header turns amber -- YOU ARE ON THE CLOCK")
    print("   5. pick 152 is the D/ST page and 161 is the kicker page, both different")
    print("   6. it ends on the 'Draft complete' roster panel")
    print("="*72 + "\n")
    time.sleep(1.5)

    p = subprocess.Popen([sys.executable, 'live_draft.py', '--reads', base, '--interval', '1.0'],
                         cwd=KIT)
    try:
        while feed.n < len(picks):
            time.sleep(pace + (hold if (feed.n + 1) in mine else 0))
            with feed.lock:
                feed.n += 1
            row = picks[feed.n - 1]
            tag = '   <<< YOUR PICK' if row['teamId'] == MY_TEAM_ID else ''
            print(f"  feed: {feed.n:>3}  {ABBREV.get(row['teamId'],'?'):<5} "
                  f"{row['_n'][:26]:<26} {row['_p']}{tag}")
        print("\n  feed: all picks in. The board should show 'Draft complete'. Ctrl+C to stop.")
        p.wait()
    except KeyboardInterrupt:
        print("\n  stopping.")
    finally:
        try: p.terminate()
        except Exception: pass
        srv.shutdown()


if __name__ == '__main__':
    main()
