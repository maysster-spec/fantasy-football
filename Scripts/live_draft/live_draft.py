r"""
live_draft.py -- LIVE DRAFT BOARD, E-Discovery Keeper League 2026.
Polls ESPN for picks as they happen, re-runs the engine, rewrites the page.
Nothing to click. Leave the browser tab open; it refreshes itself.

    py live_draft.py --bridge        # LIVE DRAFT NIGHT.  Start bridge_server.py first.
    py live_draft.py --bridge --mock # an ESPN PRACTICE draft (no keepers in the room)
    py live_draft.py --replay 2025   # DRY RUN against last year's finished draft
                                     #   practice room on a different leagueId?  add
                                     #   --url "<paste the room URL, in quotes>"
                                     #   ESPN read API refusing it?  add --slot N --teams 12
    NOTE: plain `py live_draft.py` cannot work -- doc 136, ESPN publishes a draft only after
    it ends.  --bridge is the pick source.

FOLDER CONTRACT -- these five files, together, in one folder. Nothing else is needed:
    live_draft.py                    (this file)
    code_live_engine.py              (the engine)
    board_v8_fixed.csv               (the skill board -- carries espn_id, corrected eff_pick)
    board_v7_kdst_separate.csv       (the 64 streamers, D/ST block first)
    ESPN_prerank_with_ids.csv        (the ESPN id map / injector source)
"""
import argparse, html, json, os, re, sys, tempfile, time, webbrowser, pathlib
import datetime as dt
import requests
import code_live_engine as CLE
from code_live_engine import Engine, PC

LEAGUE_ID = 21985
SEASON    = 2026
MY_TEAM_ID= 9                      # JUG -- CONFIRMED 2026-08-29 from the ESPN team URL
_SLOTS_SEEN = False
READS     = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leagues/{lid}"
COOKIES   = {
    'swid':    '{A7217088-1F36-4F1F-AE73-67262BF763EF}',
    'espn_s2': '',
}
HEADERS = {'accept':'application/json','x-fantasy-platform':'espn-fantasy-web',
           'x-fantasy-source':'kona','referer':'https://fantasy.espn.com/'}
HERE = os.path.dirname(os.path.abspath(__file__))
# doc 211: THE PAGE DOES NOT LIVE IN GOOGLE DRIVE ANY MORE.
# It is rewritten about twice a second for three hours. HERE is `G:\My Drive\...`, which is a
# VIRTUAL drive, not a disk: it does not give a reader the clean file swap that write_page()'s
# os.replace() gives on a real filesystem, and Chrome twice showed ERR_FILE_NOT_FOUND on
# 2026-09-07 (11:24 and 12:08) on a page that was being written normally. Chrome's error page
# carries no auto-refresh, so it then SAT there until Matt reloaded by hand.
# Cause not proven -- but a file rewritten twice a second has no business on a synced drive
# whatever the cause, and moving it also stops Drive uploading 47 KB every half second all
# night. Nothing reads this file: it is write-only output, live_draft.py opens it itself, and
# no Desktop shortcut points at it (checked). Falls back to the old location if both roots fail.
def _board_out():
    for base in (os.environ.get('LOCALAPPDATA'), tempfile.gettempdir()):
        if base and os.path.isdir(base):
            d = os.path.join(base, 'JUG')
            try:
                os.makedirs(d, exist_ok=True)
                return os.path.join(d, 'live_board.html')
            except OSError:
                continue
    return os.path.join(HERE, 'live_board.html')

OUT  = _board_out()

REHEARSAL = False    # set by --reads. See stamp() -- doc 97.

def stamp(html):
    """doc 97, and this one was found the worst way: Matt read a REHEARSAL roster as the tool's
    real judgement and started reasoning about Josh Jacobs and J.J. McCarthy. The console banner
    was not enough -- he was looking at the PAGE, and the page looked exactly like the real one.
    Every page a fake feed produces now says so, on the page, in red, permanently."""
    if not REHEARSAL:
        return html
    bar = ('<div style="position:sticky;top:0;z-index:99;background:#5c1a17;color:#ffd9d5;'
           'border-bottom:2px solid #e2564d;padding:9px 14px;font:600 14px/1.35 system-ui,sans-serif">'
           'REHEARSAL &mdash; FAKE FEED. These players were dealt at random from ADP. '
           'This is <u>not</u> a draft, not a recommendation, and not this tool&rsquo;s judgement '
           'about anybody.</div>')
    i = html.find('<body')
    if i < 0: return bar + html
    j = html.find('>', i)
    return (html[:j+1] + bar + html[j+1:]).replace('<title>', '<title>REHEARSAL - ', 1)

def write_page(html):
    """doc 95: this file lives in a Google Drive folder and is open in a browser. Both can
    hold a lock. Write to a temp file and os.replace() it -- atomic on Windows, so the page
    is never served half-written -- and retry rather than letting a lock kill the poller."""
    html = stamp(html)
    # doc 210: the temp name is PER PROCESS. It used to be one fixed path, so two copies of
    # this board running at once (a false start, an orphaned window) shared one scratch file:
    # process A could truncate it while B was mid-replace, and the page the browser is holding
    # open is the thing that gets replaced. Matt's practice run showed live_board.html as
    # ERR_FILE_NOT_FOUND at 11:24 and back at 11:26 -- unproven cause, but a shared temp path
    # between two writers is a hazard with no upside, and the pid makes it impossible.
    tmp = '%s.%d.tmp' % (OUT, os.getpid())
    for attempt in range(3):
        try:
            with open(tmp, 'w', encoding='utf-8') as f:
                f.write(html)
            os.replace(tmp, OUT)
            return True
        except Exception as e:
            if attempt == 2:
                print(f"  !! could not write the page ({e}). The browser is showing the LAST")
                print(f"     good state. Polling continues; close anything holding {os.path.basename(OUT)}.")
                return False
            time.sleep(0.4)

# doc 137. THE BRIDGE.  Doc 136 proved ESPN's read replica publishes a draft only after it ENDS,
# so on draft night this endpoint is useless.  The picks are in the BROWSER the whole time -- which
# is why a FantasyPros extension can show them.  `--bridge` swaps the pick source for the file that
# `bridge_server.py` writes from the Chrome extension in .\espn_bridge\.  Everything downstream --
# engine, board, recommendations, render -- is untouched; only the pipe changes.
BRIDGE_FILE = None          # set by --bridge
_PROC_START = dt.datetime.now().isoformat()   # v1.8: nothing older than this is trusted


_BRIDGE_WARNED = [False]


def _bridge_picks():
    """Read what bridge_server.py has captured.  Same tuple shape fetch_picks returns.

    doc 137 v1.8: REFUSE A STALE FILE.  bridge_picks.json survives between sessions, and on
    2026-09-02 a leftover 179-pick file from a --replay run made the board render 'draft
    complete' one second after starting.  It looked exactly like a finished draft because, as
    far as the file was concerned, it was one.  A file-based handoff with no freshness contract
    is not a handoff."""
    try:
        with open(BRIDGE_FILE) as f:
            d = json.load(f)
        # v1.8b -- MY FIRST VERSION OF THIS CHECK WAS BACKWARDS.  It refused any file whose
        # listener started before this process -- but bridge_server.py is SUPPOSED to start
        # first, so the correct setup was rejected every time.  What actually needs catching is
        # a file left over from a PREVIOUS SESSION, which is a question of age, not of ordering.
        # doc 148, red team finding 3.  THIS MEASURED THE WRONG CLOCK.  `session_started` is
        # stamped when bridge_server.py STARTS, so a listener left running since lunchtime made
        # a perfectly live feed "stale" and every real pick was discarded, while a file whose
        # listener started a minute ago and then STOPPED RECEIVING was accepted forever.  The
        # question is how old the DATA is, so ask `updated` and fall back to the old field.
        started = d.get('updated') or d.get('session_started')
        stale = False
        age = 0.0
        if started:
            try:
                age = (dt.datetime.now() - dt.datetime.fromisoformat(started)).total_seconds()
                stale = age > 6 * 3600
            except (ValueError, TypeError):
                # doc 148, finding 16: `except ValueError` did not cover fromisoformat's
                # TypeError on a non-string, which escaped into the poll loop and printed a
                # poll error twice a second forever.
                stale = False
        if stale:
            if not _BRIDGE_WARNED[0]:
                _BRIDGE_WARNED[0] = True
                print()
                # doc 149, finding 6: this named session_started after the check moved to
                # `updated`, and printed a remedy for the old failure.
                print(f'  !! STALE BRIDGE FILE -- its newest pick is {age/3600:.1f} hours old.')
                print('     Either it is left over from an earlier session, or a listener that is')
                print('     still running stopped receiving a long time ago. Those picks are')
                print('     being ignored.')
                print('     Restart bridge_server.py (it resets and re-stamps the file), make sure')
                print('     the draft room tab is open in the Chrome with the extension, then')
                print('     restart this.')
                print()
            return [], False, {}
    except FileNotFoundError:
        return [], False, {}
    except (json.JSONDecodeError, OSError):
        return None, False, {}          # mid-write; caller keeps the previous state
    out = []
    for p in d.get('picks', []):
        # doc 148, finding 15.  The |pid| > 100 filter existed ONLY on the ESPN path, so a null
        # or sentinel pid from the browser reached set_taken and raised TypeError -- caught by
        # the loop, which then retried the same broken state every 0.5s, four console lines a
        # second, while the browser kept showing the last good board and looking healthy.
        try:
            pid = int(p.get('pid'))
        except (TypeError, ValueError):
            continue
        if abs(pid) <= 100:            # 0 / -1 / sentinels.  A D/ST rides as -16000-proTeamId.
            continue
        # doc 148, finding 9.  THE KEEPER FILTER WAS INERT ON THE ONLY PATH THAT RUNS SEPT 7.
        # This stamped keeper:False on every row unconditionally, so doc 58's fix -- the one
        # that stops 12 keeper rows advancing the clock -- could never fire from the bridge, and
        # the runbook's "confirm the first poll line reports the keeper-row count" was
        # unsatisfiable.  This league's keepers ride at round 15 / overall 169-180 (directive
        # 2.1b2, verified on the real 2024 and 2025 drafts).
        rnd, ovr = p.get('round'), p.get('overall')
        keeper = bool(p.get('keeper')) or (KEEPER_ROWS[0] and (
            rnd == 15 or (isinstance(ovr, int) and 169 <= ovr <= 180)))
        out.append({'pid': pid, 'overall': ovr,
                    'round': rnd, 'team': p.get('team'), 'keeper': keeper})
    out.sort(key=lambda x: x['overall'] or 0)
    return out, bool(d.get('done')), {'source': 'bridge', 'updated': d.get('updated'),
                                      'age': age}


_BRIDGE_LAST = [None]        # last COMPLETE read; what a failed read falls back to
_BRIDGE_SHRANK = [False]
# doc 148, finding 4.  THE WORST ONE FOUND, and it is the most likely startup failure there is.
# An unconnected bridge -- extension not loaded, wrong tab, listener not started -- returns an
# EMPTY list, not an error.  0 != last(-1), so step() ran, pick_no came out as len([])+1 = 1,
# and the board rendered a complete, authoritative, entirely correct-looking PICK 1 page:
# "ON THE CLOCK 1 / Cary (DUCK) / TAKE Jahmyr Gibbs".  Because the count then never changed it
# rendered ONCE and was never rewritten, so it also never went stale-looking.  The console said
# `0 real picks in` a single time, in the same format as a healthy line.
# An empty feed BEFORE the first real pick is not a draft state.  It is "not connected yet".
_SAW_PICKS = [False]
# doc 149, finding 4.  The round-15 / overall-169-180 keeper rule is TRUE OF THIS LEAGUE and false
# of an ESPN mock, which has no keepers at all.  Applied unconditionally it flagged 10-26 rows in
# every mock shape tested and put the clock that many picks BEHIND the room for the rest of the
# run -- and mocks are on the pre-Sept-7 list.  --mock turns it off; the real draft leaves it on.
KEEPER_ROWS = [True]
_KEEPER_SAID = [False]   # doc 149 finding 9: say the keeper-row count once, out loud, even if 0


def fetch_picks(season, lid):
    if BRIDGE_FILE:
        got = _bridge_picks()
        # doc 139.  THE COMMENT SAID "caller keeps the previous state" AND THE CODE RETURNED
        # AN EMPTY LIST.  That is not a no-op: an empty pick list tells the engine every
        # drafted player is available again, and it printed `0 real picks in` mid-draft on
        # 2026-09-02.  bridge_server.py now writes atomically so this should never fire, but
        # "should never fire" is exactly the class of guard this project keeps finding broken,
        # so hold the last COMPLETE state instead of inventing an empty one.
        if got[0] is None:
            return _BRIDGE_LAST[0] or ([], False, {})
        # A draft only ever gains picks.  A read that is well-formed but SHORTER than what we
        # already had is a reset handoff file or a restarted listener -- either way the picks
        # it dropped are still off the board in the room.  Holding is always safer than
        # handing drafted players back.
        # doc 148, finding 1.  `<` released at EQUAL length: a restarted listener refilled the
        # file to exactly the old count with a DIFFERENT set of picks, and the board silently
        # swapped in the wrong ones -- at a real 60-pick state it went on to recommend Gibbs and
        # Bijan as available at pick 120.  The test is not "how many", it is "does the new set
        # still contain everything already off the board".
        prev = _BRIDGE_LAST[0]
        if prev and not {q['pid'] for q in prev[0]} <= {q['pid'] for q in got[0]}:
            if not _BRIDGE_SHRANK[0]:
                _BRIDGE_SHRANK[0] = True
                print(f"  !! bridge file LOST PICKS ({len(prev[0])} -> {len(got[0])}; "
                      f"{len({q['pid'] for q in prev[0]} - {q['pid'] for q in got[0]})} players "
                      "dropped). Holding the set that already had them.")
                print("     If you restarted bridge_server.py mid-draft, restart this too --"
                      " the picks it missed are gone.")
            return prev
        _BRIDGE_LAST[0] = got
        return got
    url = READS.format(season=season, lid=lid) + "?view=mDraftDetail"
    r = requests.get(url, cookies=COOKIES, headers=HEADERS, timeout=8)
    r.raise_for_status()
    d = r.json()
    if isinstance(d, list): d = d[0]
    dd = d.get('draftDetail') or {}
    picks = dd.get('picks') or []
    out = []
    for p in picks:
        out.append(dict(overall=p.get('overallPickNumber'), team=p.get('teamId'),
                        pid=p.get('playerId'), round=p.get('roundId'),
                        keeper=bool(p.get('keeper'))))
    # ================== doc 123. THE BUG THAT WOULD HAVE COST DRAFT NIGHT ==================
    # ESPN pre-creates the WHOLE pick grid the moment a draft room opens -- 180 rows, one per
    # (round, team), each with a real overallPickNumber and an EMPTY playerId. They are slots,
    # not selections.
    #
    # The old filter was  `if p['pid'] and p['overall']`.  ESPN's empty-slot sentinel is a small
    # negative number, and IN PYTHON -1 IS TRUTHY. So every unfilled slot passed. On a mock room
    # that had not made a single pick the tool read 180 "picks", computed pick_no 180, hit the
    # `pick_no > 168` branch and rendered "Draft complete" with an empty roster -- instantly,
    # every time, on two different mock rooms with identical 179+1 counts.
    #
    # THE SAME THING WOULD HAVE HAPPENED AT 8:00 PM ON SEPT 7. The tool would have declared the
    # draft over before pick 1. It is doc 58's defect exactly -- counting rows that are not
    # selections -- and I did not re-check the other half of that filter when I fixed the keepers.
    #
    # THE RULE: a real ESPN playerId is 5-7 digits; a D/ST rides the wire as -16000 - proTeamId
    # (directive 8), so NEGATIVE IS NOT THE TEST -- dropping negatives would delete every defense.
    # An empty slot is 0 / -1 / None / missing. |pid| > 100 keeps every real player and every
    # defense and cannot keep a sentinel.
    def _real(v):
        try: n = int(v)
        except (TypeError, ValueError): return False
        return abs(n) > 100
    slots = [p for p in out if not _real(p['pid'])]
    out = [p for p in out if _real(p['pid']) and p['overall']]
    out.sort(key=lambda x: x['overall'])
    global _SLOTS_SEEN
    if slots and not _SLOTS_SEEN:
        _SLOTS_SEEN = True
        ex = sorted({p['pid'] for p in slots})[:5]
        print(f"  feed carries {len(picks)} pick rows; {len(slots)} are EMPTY SLOTS "
              f"(playerId {ex}) and are not selections. {len(out)} real picks.")
    return out, bool(dd.get('drafted')), dd




def parse_draft_url(u):
    """doc 124. Matt pasted the ESPN draft-room URL and asked "is that the info you feed it?" --
    yes, and there is no reason he should be transcribing three numbers out of it at 8:00 PM.

        https://fantasy.espn.com/football/draft?leagueId=910821995&seasonId=2026&teamId=9&memberId={...}

    leagueId -> --league,  seasonId -> the season,  teamId -> --team.

    memberId IS THE SWID -- an account credential. It is deliberately NOT read, NOT stored and NOT
    printed here. Nothing in this tool needs it; the cookies already carry identity.

    Draft SLOT is not in the URL (it is your position in the room's order), so --slot still applies.
    """
    import urllib.parse as _up
    q = _up.parse_qs(_up.urlparse(u).query)
    def _i(k):
        v = (q.get(k) or [None])[0]
        try: return int(v)
        except (TypeError, ValueError): return None
    got = dict(league=_i('leagueId'), season=_i('seasonId'), team=_i('teamId'))
    if not got['league']:
        raise SystemExit("  no leagueId in that URL. Paste the whole draft-room address, in quotes:\n"
                         '     py live_draft.py --url "https://fantasy.espn.com/football/draft?leagueId=..."')
    bits = '  '.join(f"{k}={v}" for k, v in got.items() if v is not None)
    print(f"  from the URL: {bits}"
          + ("   (memberId ignored -- that is your SWID, a credential)" if 'memberId' in q else ""))
    return got


def keep_evidence(tag, lid, season, status, text):
    """doc 122. The mock failure is unexplainable because the payload is gone -- the league stopped
    answering and nothing on disk had kept what it said. Every question since has been archaeology
    on a console log.

    So: the FIRST successful poll and ANY anomaly are written to disk, raw. A few hundred KB buys
    the ability to answer 'what did ESPN actually send' after the fact, which is the one thing this
    session could not do. Never fatal -- a logging failure must not take down the poller."""
    try:
        d = os.path.join(HERE, 'feed_evidence')
        os.makedirs(d, exist_ok=True)
        fn = os.path.join(d, f"{dt.datetime.now():%Y%m%d_%H%M%S}_{tag}_{lid}_{season}_{status}.json")
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(text if isinstance(text, str) else str(text))
        print(f"  evidence kept: {os.path.relpath(fn, HERE)}")
    except Exception as e:
        print(f"  (could not keep evidence: {e} -- polling continues)")



def watch(season, lid, team, interval):
    """doc 127. THE ONE QUESTION: does ESPN's read API carry picks while a draft is running?

    Every attempt to answer that so far has been tangled up in the board, the caps, the keeper
    logic and slot detection -- none of which matter to the question. This mode strips all of it.
    No board, no engine, no recommendations, no page. It polls one endpoint and prints what
    changed. It works on ANY league of any shape, so a throwaway test league answers the question
    for the real one.

    WHAT A PASS LOOKS LIKE: the count climbs, and each new pick prints within a few seconds of
    happening in the draft room.
    WHAT A FAIL LOOKS LIKE: the count never moves while the room drafts -- which is exactly what
    an ESPN MOCK does (doc 126), and the reason this test needs a REAL league.
    """
    print("  " + "="*70)
    print("  WATCH -- does the feed move? No board, no advice, no page.")
    print(f"  league {lid}  season {season}  every {interval:g}s   Ctrl+C to stop")
    print("  " + "="*70)
    names = {}
    try:
        import pandas as _pd
        _b = _pd.read_csv(os.path.join(HERE, 'board_v8_fixed.csv'))
        names = dict(zip(_b.espn_id.astype(int), _b.player))
    except Exception:
        pass
    seen, t0, polls, last_change = set(), time.time(), 0, time.time()
    batches = 0   # doc 136: how many DIFFERENT polls delivered new picks
    while True:
        try:
            picks, done, dd = fetch_picks(season, lid)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"  [{dt.datetime.now():%H:%M:%S}] poll error: {e}")
            if '404' in str(e):
                print("     404 -- if this is a MOCK room it has been deleted. Use a REAL league.")
            time.sleep(interval); continue
        polls += 1
        grid = len(dd.get('picks') or []) if dd else 0
        new = [p for p in picks if p['overall'] not in seen]
        for p in sorted(new, key=lambda z: z['overall']):
            seen.add(p['overall'])
            nm = names.get(int(p['pid']), f"playerId {p['pid']}")
            tag = '  (keeper)' if p['keeper'] else ''
            print(f"  [{dt.datetime.now():%H:%M:%S}] pick {p['overall']:>3}  rd {p['round']:>2}  "
                  f"team {p['team']:>2}  {nm}{tag}")
        if new:
            last_change = time.time(); batches += 1
        if polls % 20 == 0:
            quiet = int(time.time() - last_change)
            print(f"  [{dt.datetime.now():%H:%M:%S}] {len(picks)} of {grid} slots filled  "
                  f"drafted={done}  |  nothing new for {quiet}s  ({polls} polls)")
            if quiet > 180 and len(picks) < grid:
                print("     ^^ THREE MINUTES WITH NO NEW PICK while the grid is not full.")
                print("        If the room IS drafting, this endpoint is not carrying it.")
        if grid and len(picks) >= grid:
            # doc 136.  The 09-02 live test filled ALL 192 slots in ONE poll, after the room had
            # already finished.  "The grid filled" therefore does NOT mean the feed is live -- it
            # equally means the endpoint is a post-hoc record that materialises at the end.  Those
            # are opposite conclusions, and the old message asserted the wrong one.
            secs = int(time.time() - t0)
            if batches <= 1:
                print(f"  all {grid} slots appeared IN ONE POLL after {secs}s.")
                print("  *** THIS IS NOT A LIVE FEED. *** The endpoint published the whole draft")
                print("      at once, which is what a post-hoc record looks like. It cannot drive")
                print("      the live board on draft night.")
            else:
                print(f"  every one of {grid} slots is filled after {secs}s, arriving across "
                      f"{batches} separate polls -- THE FEED IS LIVE.")
            return
        if done:
            print("  ESPN says drafted=true -- FEED WORKS."); return
        time.sleep(interval)


def probe(season, lid, team):
    """doc 118. Matt's mock run reported `179 real picks in (+1 keeper rows ignored)` and went
    straight to Draft complete, then 404ed on every poll after. Two different faults, and the
    directive is explicit that a diagnosis is a claim: reproduce the failure before writing a fix.

    This prints exactly what ESPN is serving for that league and season -- nothing is inferred."""
    print(f"\n  PROBE  league {lid}  season {season}")
    url = READS.format(season=season, lid=lid) + "?view=mDraftDetail&view=mTeam&view=mSettings"
    try:
        r = requests.get(url, cookies=COOKIES, headers=HEADERS, timeout=10)
        print(f"  HTTP {r.status_code}  {len(r.content):,} bytes")
        keep_evidence('probe', lid, season, r.status_code, r.text)
        if r.status_code == 404:
            # doc 119. "cookies or wrong id" is a guess, and this tool can just ANSWER it: hit
            # the KNOWN-GOOD league with the SAME cookies, same host, same season. If that comes
            # back 200 the cookies are provably fine and the id is the problem. Matt spent a
            # cookie refresh on a 404 that had nothing to do with cookies.
            print(f"\n  404. Now testing the SAME cookies against the known league {LEAGUE_ID} ...")
            try:
                r2 = requests.get(READS.format(season=season, lid=LEAGUE_ID) + "?view=mTeam",
                                  cookies=COOKIES, headers=HEADERS, timeout=10)
                print(f"  league {LEAGUE_ID}: HTTP {r2.status_code}")
            except Exception as e:
                print(f"  league {LEAGUE_ID}: FAILED {type(e).__name__}: {e}"); return
            if r2.status_code == 200:
                # doc 121, Matt's question: "how do we know the cookies were good for THAT room?"
                # This test cannot know that. It proves the cookies are VALID; it cannot prove you
                # are AUTHORISED for some other league. ESPN returns 404 for both "no such league"
                # and "not yours", and those are different problems with the same status code.
                # The earlier wording asserted the league did not exist. It does not know that.
                print(f"\n  YOUR COOKIES ARE VALID -- league {LEAGUE_ID} answers with them right now,")
                print(f"  so a stale session is NOT why {lid} is failing.")
                print(f"\n  What this does NOT tell you: whether you are AUTHORISED for {lid}.")
                print("  ESPN returns 404 both for a league that does not exist AND for one that")
                print("  exists but is not yours. Valid cookies and league access are two different")
                print("  things, and this probe can only measure the first.")
                print(f"\n  For anything real, drop --league entirely -- it defaults to {LEAGUE_ID}:")
                print("      py live_draft.py")
                print("  To rehearse a CHANGING draft with no ESPN at all:")
                print("      py rehearsal.py --realtime")
            else:
                print("\n  Both ids failed, so this is NOT about which league. Cookies:")
                print("      py cookie_jar.py    then re-run this probe.")
            return
        r.raise_for_status()
        d = r.json()
        if isinstance(d, list): d = d[0]
    except Exception as e:
        print(f"  FAILED: {type(e).__name__}: {e}"); return
    print(f"  seasonId in the payload : {d.get('seasonId')}   (asked for {season})")
    print(f"  scoringPeriodId         : {d.get('scoringPeriodId')}")
    dd = d.get('draftDetail') or {}
    picks = dd.get('picks') or []
    ks = [p for p in picks if p.get('keeper')]
    print(f"  draftDetail.drafted     : {dd.get('drafted')}   inProgress: {dd.get('inProgress')}")
    print(f"  picks in the feed       : {len(picks)}   of which keeper=True: {len(ks)}")
    st = (d.get('settings') or {}).get('draftSettings') or {}
    print(f"  settings.draftSettings  : type={st.get('type')}  date={st.get('date')}"
          f"  keeperCount={st.get('keeperCount')}")
    if picks:
        rounds = sorted({p.get('roundId') for p in picks})
        print(f"  rounds present          : {rounds[:3]} ... {rounds[-3:]}")
        # doc 120. WHOSE picks are these? On 2026-09-01 a feed came back with 180 picks and the
        # 'Draft complete' page showed an EMPTY roster -- which means team 9 owned none of them.
        # That is the question the first probe could not answer, so it now always answers it.
        from collections import Counter
        by = Counter(p.get('teamId') for p in picks)
        print(f"  teams owning picks      : {sorted(k for k in by if k is not None)}")
        print(f"  picks per team          : "
              + '  '.join(f"{k}:{v}" for k, v in sorted(by.items(), key=lambda x: (x[0] is None, x[0]))))
        print(f"  YOUR team {team} owns      : {by.get(team, 0)} of these picks"
              + ("   <-- ZERO. This feed is not a draft you are in." if not by.get(team) else ""))
        tms = {t.get('id'): (t.get('abbrev') or '') for t in (d.get('teams') or [])}
        if tms:
            print(f"  mTeam says team {team} is  : {tms.get(team, '(not in this league)')}"
                  f"   ({len(tms)} teams)")
        for label, sl in (('first 3', picks[:3]), ('last 3', picks[-3:])):
            for p in sl:
                nm = ''
                try: nm = eng_name_hint(p.get('playerId'))
                except Exception: pass
                print(f"    {label:<8} overall {p.get('overallPickNumber'):>3}  round "
                      f"{p.get('roundId'):>2}  team {p.get('teamId'):>2}  keeper="
                      f"{bool(p.get('keeper'))}  playerId {p.get('playerId')} {nm}")
    print("\n  WHAT TO CONCLUDE")
    if len(picks) >= 150 and dd.get('drafted'):
        print("  * A COMPLETE draft is already in this feed. That is never a valid start state")
        print("    on Sept 1. Either ESPN is serving a PRIOR season's draft under this id, or")
        print("    this is not the league you meant.")
        print(f"  * This league carries {len(ks)} keeper row(s). Directive 2.1(b2) verified TWELVE")
        print("    on the real 2024 and 2025 drafts. One keeper row does not match this league's")
        print("    shape, which is more evidence that this is not the 2026 draft feed.")
    elif not picks:
        print("  * No picks yet -- that is the NORMAL state before a draft starts.")
    print("  * For an ESPN MOCK you must pass the MOCK room's own league id, not this one.")
    print("    Open the mock draft room and read leagueId= out of the browser address bar.")
    print("  * The tested way to rehearse without ESPN at all:  py rehearsal.py --realtime")


def eng_name_hint(pid):
    try:
        import pandas as _pd
        b = _pd.read_csv(os.path.join(HERE, 'board_v8_fixed.csv'))
        m = b[b.espn_id == int(pid)]
        return f"= {m.player.iat[0]}" if len(m) else ''
    except Exception:
        return ''


def confirm_team(season, lid, team_id):
    """doc 95 TRAP 8. MY_TEAM_ID is a hard-coded 9 and it is NOT the draft slot (8). If it is
    ever wrong the tool runs all night against SOMEONE ELSE'S roster -- every 'my roster'
    panel, every cap, every bye check -- and nothing on screen says so. One read, printed in
    words, so a wrong id is caught at 7:55 instead of at pick 89. Never fatal."""
    try:
        url = READS.format(season=season, lid=lid) + "?view=mTeam"
        d = requests.get(url, cookies=COOKIES, headers=HEADERS, timeout=8).json()
        if isinstance(d, list): d = d[0] if d else {}
        for t in (d.get('teams') or []):
            if t.get('id') == team_id:
                nm = (t.get('name') or ' '.join(filter(None,[t.get('location'),t.get('nickname')]))
                      or '').strip()
                ab = (t.get('abbrev') or '').strip()
                print(f"  team {team_id} = {ab or '?'}  \"{nm or '?'}\"   <- IS THIS YOU? "
                      f"if not, stop and use  --team N")
                return True
        print(f"  !! team id {team_id} is NOT in this league's team list. The roster panel and")
        print(f"     the position caps will be WRONG all night. Stop and use  --team N.")
    except Exception as e:
        print(f"  (could not confirm the team name: {e} -- continuing on team id {team_id})")
    return False

# ------------------------------------------------------------------ rendering
CSS = """
:root{--bg:#0e1014;--pnl:#171a21;--pnl2:#1c2029;--ln:#272d38;--tx:#e8eaee;
      --dim:#98a0ae;--amb:#f0a91b;--gr:#3fb27f;--rd:#e2564d;--bl:#5b9dd9}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);
     font:16px/1.45 "IBM Plex Sans",system-ui,sans-serif}
.shell{max-width:1620px;margin:0 auto;padding:12px 14px}
/* clock, far left, where the eye lands first */
.clockrow{display:flex;align-items:stretch;gap:14px;margin-bottom:10px}
.clock{flex:none;width:196px;text-align:center;background:var(--pnl);
       border:1px solid var(--ln);border-radius:10px;padding:6px 10px 8px}
.clock .lbl{font:700 9px/1 "Chivo";letter-spacing:.16em;text-transform:uppercase;color:var(--dim)}
.clock .n{font:700 52px/1 "IBM Plex Mono",monospace;color:var(--tx);margin-top:2px}
.clock .who{font:600 11px/1.3 "IBM Plex Sans";color:var(--dim);margin-top:4px}
.clock.mine{border-color:var(--amb);background:#241d0c}
.clock.mine .n{color:var(--amb)}
.clock.mine .who{color:var(--amb);font-weight:700}
.feedwarn{background:#4a1512;border:1px solid #a1372f;color:#ffb3ac;font:700 15px/1.4 "Chivo",
   system-ui;padding:10px 14px;border-radius:6px;margin:0 0 10px;letter-spacing:.01em}
.runflag{display:inline-block;background:#3a2a08;border:1px solid #6b4d10;color:var(--amb);
         font:700 12px/1 "IBM Plex Sans";padding:6px 10px;border-radius:6px;margin-left:14px;
         vertical-align:middle}
.board-split{display:grid;grid-template-columns:232px minmax(0,1fr);gap:0;
             background:var(--pnl);border:1px solid var(--ln);border-radius:8px;overflow:hidden}
.gonecol{border-right:1px solid var(--ln);padding:11px 10px;background:#14171d}
/* doc 147.  The legend was ~150px of prose sitting between the board and the two panels
   that matter on the clock (cliffs, roster), pushing them under the fold on a 1600x1000
   window.  It is reference material -- it is read once, at the kitchen table, not at 60
   seconds a pick.  Closed by default, one click, and the guide carries the same words. */
details.legend{margin-top:10px}
details.legend summary{cursor:pointer;list-style:none;color:#5b9dd9;font-size:11.5px;
   padding:4px 0;font-weight:600}
details.legend summary::-webkit-details-marker{display:none}
details.legend summary:before{content:"\u25B8  "}
details.legend[open] summary:before{content:"\u25BE  "}
.legend{margin-top:10px;font-size:11.5px;color:var(--dim);line-height:1.6}
.legend b{color:var(--tx)}
.legend .row{padding:2px 0;border-top:1px solid #1e232c}
.wrap{max-width:1200px;margin:0 auto;padding:14px}   /* used by render_done / render_streamer */

/* ---------- left rail: the draft going by ---------- */
.gonecol ol{list-style:none;margin:0;padding:0}
.gonecol li{display:flex;align-items:center;gap:7px;padding:4px 5px;border-radius:4px;
            font-size:13px;line-height:1.3;white-space:nowrap}
.gonecol li:first-child{background:#22262f}
.gonecol li.gpad{visibility:hidden}          /* doc 147: holds the height, draws nothing */
.gonecol li.gpad:first-child{background:none}
.gonecol li .nm{flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;
                white-space:nowrap}
.gonecol li.fresh .nm{color:#fff;font-weight:600}
.gonecol li .agn{color:#5a6270;font-size:10px;font-family:"IBM Plex Mono",monospace;
                 flex:0 0 auto;padding-left:6px}
.gonecol li:first-child .agn{color:#fff;font-weight:700}

/* ---------- header ---------- */
.top{display:flex;align-items:center;gap:16px;margin-bottom:10px}
.top h1{font:700 17px/1 "Chivo",system-ui;margin:0;flex:none}
.top .meta{color:var(--dim);font-size:11.5px;line-height:1.4}
.pickbox{margin-left:auto;flex:none;text-align:center;background:var(--pnl);
         border:1px solid var(--ln);border-radius:10px;padding:4px 20px 6px}
.pickbox .lbl{font:700 9px/1 "Chivo";letter-spacing:.16em;text-transform:uppercase;
              color:var(--dim)}
.pickbox .n{font:700 46px/1 "IBM Plex Mono",monospace;color:var(--tx)}
.pickbox.mine{border-color:var(--amb);background:#241d0c}
.pickbox.mine .n{color:var(--amb)}
.pickbox .until{font:600 10px/1 "IBM Plex Sans";color:var(--dim);margin-top:3px}

/* ---------- hero ---------- */
.hero{background:var(--pnl);border:1px solid var(--ln);border-left:4px solid var(--amb);
      border-radius:8px;padding:12px 16px;margin-bottom:12px}
.hero .sub{color:var(--dim);font-size:11px;letter-spacing:.1em;text-transform:uppercase}
.hero .pick{font:700 28px/1.15 "Chivo",system-ui;margin-top:2px}
.hero .why{color:var(--dim);font-size:12.5px;margin-top:6px}
.big{font:700 32px/1 "IBM Plex Mono",monospace;color:var(--amb)}

/* ---------- tables ---------- */
table{width:100%;border-collapse:collapse;font-size:13.5px}
th{text-align:left;color:var(--dim);font-weight:600;font-size:10px;letter-spacing:.07em;
   text-transform:uppercase;padding:5px 6px;border-bottom:1px solid var(--ln);white-space:nowrap}
/* one rhythm for the board: numbers snug to their own header, gaps only where a
   column boundary actually means something. */
/* PROPORTIONAL widths, auto layout, no colgroup.
   - percentages so the table fills the panel instead of packing left and leaving
     a dead zone on the right (the spacer-column approach did that);
   - auto layout so no column can inherit a neighbour's width, which is what
     scrambled TM..VBD when a column was hidden under table-layout:fixed;
   - they scale together as the window narrows, so nothing crushes selectively. */
.boardwrap{overflow-x:auto}
table.board{min-width:860px}
table.board td,table.board th{padding-left:6px;padding-right:6px;white-space:nowrap}
table.board th:nth-child(1),table.board td:nth-child(1){width:3%}
table.board th:nth-child(2),table.board td:nth-child(2){width:19%;white-space:normal}
table.board th:nth-child(3),table.board td:nth-child(3){width:6%}
table.board th:nth-child(4),table.board td:nth-child(4){width:6%}
table.board th:nth-child(5),table.board td:nth-child(5){width:6%}
table.board th:nth-child(6),table.board td:nth-child(6){width:9%}
table.board th:nth-child(7),table.board td:nth-child(7){width:11%}
table.board th:nth-child(8),table.board td:nth-child(8){width:11%}
table.board th:nth-child(9),table.board td:nth-child(9){width:9%}
table.board th:nth-child(10),table.board td:nth-child(10){width:11%}
table.board th:nth-child(11),table.board td:nth-child(11){width:9%}
table.board td.vbd,table.board th.vbdh{padding-left:14px}   /* gap after bye */
table.board td.key,table.board th.key{padding-left:14px}    /* gap before delta */
th.num,th.key,th.vbdh,th.costh{text-align:right}   /* headers sit over their own numbers */
td{padding:5px 6px;border-bottom:1px solid var(--ln);overflow:hidden;text-overflow:ellipsis}
tr:hover td{background:var(--pnl2)}
.mono{font-family:"IBM Plex Mono",monospace}
.num{text-align:right;font-family:"IBM Plex Mono",monospace}
.rank{color:#5a6270;font:600 11px/1 "IBM Plex Mono",monospace;width:18px;text-align:right}

/* doc 147.  THE ONLY BAR ON THE PAGE BELONGS TO THE COLUMN THAT ORDERS THE LIST.
   Two bars used to be drawn and BOTH pointed the wrong way:
     - `wait cost` was the most saturated element in the table, and directive s7 says in
       terms that this column is NOT the sort key.  At pick 23 the longest green bar sat on
       row 5 and at pick 104 on row 12 -- rows the engine ranked LAST.  That is doc 79's
       defect ("the largest bar on the page belonged to a row the engine did not pick")
       recurring in a second place after being fixed in the first.
     - the VBD bar was drawn from abs(vbd), and from roughly pick 89 on EVERY vbd on this
       board is negative.  At pick 104 the longest blue bar marked Pat Freiermuth at -33.9,
       the worst player on the screen.
   Now: one bar, on `cost vs #1`, drawn as DISTANCE BEHIND ROW 1.  Long = worse, which is
   the only encoding that cannot be read backwards.  Row 1 is `free` and draws nothing. */
th.costh{color:var(--amb)}
th.key{color:var(--dim)}
td.key{font-family:"IBM Plex Mono",monospace;text-align:right;color:#c3c9d4}
td.vbd{font-family:"IBM Plex Mono",monospace;text-align:right}
td.cost{font-family:"IBM Plex Mono",monospace;text-align:right;font-weight:700;
        position:relative}
td.cost .bar{position:absolute;right:0;top:2px;bottom:2px;border-radius:2px;
             background:rgba(226,86,77,.20);z-index:0}
td.cost span.v{position:relative;z-index:1}
/* doc 139 fixed the words clear / slim / a coin flip at 6 and 1.5 and used them in the
   headline.  The BOARD never used them, so eleven rows all read as one shade of "worse".
   `tie` is the same threshold applied per row: inside 1.5 points of the recommendation the
   engine cannot separate them and Matt's own read is free. */
.free{color:var(--gr)}.tie{color:#7fd4a4}.cheap{color:var(--dim)}.dear{color:var(--rd)}
td.cost.tie:after{content:"tie";font:700 8.5px/1 system-ui;color:#5a8f74;margin-left:5px;
                  letter-spacing:.06em;vertical-align:1px}
tr.padrow td{color:transparent;background:none}
tr.padrow:hover td{background:none}
tr.tier.gh div{border-top-color:transparent}   /* holds the slot, draws nothing */
tr.tier td{border-bottom:none;padding:0}
tr.tier div{border-top:2px dashed #3a4150;margin:3px 0;position:relative}
tr.tier span{position:absolute;top:-8px;left:8px;background:var(--pnl);color:#5a6270;
             font:700 9px/1 "Chivo";letter-spacing:.1em;padding:0 6px}
.clash{color:var(--rd);font-weight:700;font-size:10px;margin-left:4px}

.pos{display:inline-block;width:30px;text-align:center;border-radius:3px;font-size:10.5px;
     font-weight:700;padding:1px 0;flex:none}
.QB{background:#3a2b4d;color:#c9a7ee}.RB{background:#173a2e;color:#6fd4a4}
.WR{background:#123246;color:#7cc0ef}.TE{background:#4a3418;color:#f0be6a}
.DST,.K{background:#333;color:#bbb}
/* doc 100: injury/context grades. Shown, never scored. */
.ctxA,.ctxD,.ctxN,.ctxS,.ctxY1,.ctxY2,.ctxY3,.ctxB,.ctxQ,.ctxF,.ctxM{font:700 9.5px/1 system-ui,sans-serif;padding:2px 4px;border-radius:3px;
  vertical-align:1px;letter-spacing:.03em;cursor:help}
.ctxA{background:#5c1a17;color:#ffb3ac;border:1px solid #a1372f}
.ctxD{background:#4a3408;color:#f0be6a;border:1px solid #7d5a12}
.ctxN{background:#17301f;color:#7fd4a4;border:1px solid #2d5c3e}
.ctxS{background:#1b2b45;color:#8fb8ee;border:1px solid #35547f}
/* doc 105: the SAME word at three intensities. One agreeing list is a whisper, three is a shout,
   and you should be able to tell them apart without counting anything. */
.ctxY1{background:#10281a;color:#5aa87a;border:1px solid #24523a}
.ctxY2{background:#12381f;color:#7fe0a4;border:1px solid #2f7a4c}
.ctxY3{background:#1c6b3d;color:#ecfff3;border:1px solid #46d98b;box-shadow:0 0 0 1px #1c6b3d}
.ctxB{background:#3a2a08;color:#f0c66a;border:1px solid #6b4d10}
.ctxQ{background:#2a2e36;color:#9aa3b0;border:1px solid #3a4048}
.ctxF{background:#3a1c2c;color:#e79ab8;border:1px solid #6e3350}
.ctxM{background:#6b4a08;color:#ffe6a8;border:1px solid #f0a91b}
.pip{letter-spacing:1px;margin-left:4px;font-size:8px;vertical-align:1.5px;opacity:.95}
#hold{display:none;position:fixed;right:14px;bottom:12px;z-index:99;
  background:#3a2a08;border:1px solid #6b4d10;color:#f0c66a;border-radius:6px;
  padding:6px 11px;font:600 12px/1.2 system-ui,sans-serif}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.panel{background:var(--pnl);border:1px solid var(--ln);border-radius:8px;padding:11px 13px}
.panel h2{font:700 10px/1 "Chivo";letter-spacing:.1em;text-transform:uppercase;
          color:var(--dim);margin:0 0 8px}
/* doc 154: the starter strip moved out of the roster panel to full width under the hero.
   It is ALWAYS one line -- the trailing status text changes, the height does not (doc 139). */
.pos-fill{background:var(--pnl);border:1px solid var(--ln);border-radius:8px;
          padding:7px 13px;margin:10px 0 0;display:flex;align-items:baseline;gap:14px;
          line-height:1.35;min-height:19px}
.pos-fill span{font-family:"IBM Plex Mono",monospace;font-size:12.5px;white-space:nowrap;flex:none}
.pos-fill span i{font-style:normal;font-size:8.5px;font-weight:700;letter-spacing:.06em;
                 margin-left:4px;color:#5a6270;vertical-align:1px}
.pos-fill .sdrift{margin-left:auto;color:#98a0ae;font-family:"IBM Plex Sans",system-ui,sans-serif;
                  font-size:12px;overflow:hidden;text-overflow:ellipsis;min-width:0;flex:0 1 auto}
.pos-fill .sdrift b{font-weight:700}
.ok{color:var(--gr)}.warn{color:var(--amb)}.bad{color:var(--rd)}
i.gof{font-style:normal;font:700 8.5px/1 system-ui;letter-spacing:.06em;color:var(--amb);
      margin-left:5px;vertical-align:1px}
i.rk{font-style:normal;font:700 8.5px/1 system-ui;letter-spacing:.06em;color:#7a828f;
     border:1px solid #3a4048;border-radius:2px;padding:1px 3px;margin-left:5px;
     vertical-align:1.5px;cursor:help}
@media (max-width:900px){
  .clockrow{flex-direction:column}
  .clock{width:100%}
  .board-split{grid-template-columns:1fr}
  .board-split>div:last-child{order:1}
  .gonecol{order:2;border-right:none;border-top:1px solid var(--ln);
           max-height:210px;overflow-y:auto}   /* never pushes the roster off screen */
  .grid{grid-template-columns:1fr}
}
"""

SLOTS = {1:'Cary (DUCK)', 2:'Fleming (FLEM)', 3:'Ray (AAT)', 4:'Brown/Collins (TURD)',
         5:'allen (WGTS)', 6:'Kam (BC)', 7:'Grenier (BATE)', 8:'YOU (JUG)',
         9:'Snyder (Boo)', 10:'Rychlicki (POT)', 11:'Taylor', 12:'Lobsinger (Tets)'}

def whose_pick(pick_no, teams=12):
    """Snake order -> draft slot -> manager. Verified: pick 8 and pick 17 both land on slot 8."""
    rnd = (pick_no - 1) // teams + 1
    idx = (pick_no - 1) % teams
    slot = idx + 1 if rnd % 2 else teams - idx
    return slot, SLOTS.get(slot, f'slot {slot}'), rnd

COLGLOSS = [
    ('VBD', 'Season points above a replacement-level starter at his position. The pure "how good is he" number, comparable across positions.'),
    ('adds now', 'Points this player adds to your STARTING LINEUP if you take him right now. Lower than VBD when you already have that position filled.'),
    ('if I wait', 'What the best player at the same position is expected to add if you skip him and take him at your NEXT turn instead.'),
    ('wait cost (&Delta;)', 'adds now minus if I wait. <b>A tempo number, not the ranking.</b> Big &Delta; = his position falls off a cliff before your next turn. Small &Delta; = that position can wait. The list is NOT sorted by this &mdash; see cost vs #1.'),
    ('cost vs #1', '<b>This is what orders the list, and it is the only bar on the page &mdash; a longer bar means further behind, and a FULL bar means 20 points or more behind, at every pick.</b> Every row is scored by simulating your whole remaining draft after taking him; this column is that score minus row 1&rsquo;s. <b>free</b> = row 1, the recommendation. <b>tie</b> = within 1.5 pts, which is closer than the engine can measure &mdash; take whichever you prefer, it costs nothing. Grey = under 6 pts, cheap. Red = it is not cheap.'),
    ('still there?', 'Chance he is still on the board at your NEXT turn. <b>80% = he probably lasts, so you can take someone else first. 10% = now or never.</b> Blank on row 1 &mdash; you are taking him now, so it does not apply. <b>goes first</b> = this row is a <b>tie</b> with the recommendation AND at least 20 points less likely to survive to your next turn. <b>It is not an argument that the engine is wrong.</b> The engine already simulates who will be gone, so a tie is a tie <i>after</i> counting that &mdash; the mark tells you which of the tied rows you can <b>only</b> get on this turn. Use it when you have something the board does not: a news line on the card, an analyst call, a badge. Deliberately rare &mdash; it needs a tie, a 20-point gap, and a player the market actually prices.'),
    ('R (beside a name)', 'Rookie &mdash; no 2025 NFL snaps and not in the 2023 or 2024 player pool, so it is not a veteran who missed a season (Tank Dell, Jonathon Brooks and MarShawn Lloyd all missed 2025 and are <b>not</b> marked). It is grey and borderless on purpose: it is a <b>fact, not a rating</b>. Nothing in this project computes a ceiling, and 4 of 5 players drafted this late never become startable at all &mdash; so this tells you who is a rookie, not that being one is good.'),
    ('the strip under the hero', 'Your NINE starting slots, not your roster size. The number on the left never exceeds the number on the right, because the right-hand number is <b>how many of that position start</b> &mdash; a surplus shows as <b>+n</b> beside it, which is your bench depth at that position. <b>full</b> = you are at this league\u2019s roster cap for that position and the board will stop offering it. The line on the right counts your remaining skill turns and warns you one turn BEFORE the board is forced to show you only a QB or only a TE.'),
    # doc 159.  Matt found the paper board explaining its badges in a footer key while the SCREEN
    # explained none of them -- the same "a visual encoding that is not in the key is noise with a
    # backstory" defect, one artifact over.  These four entries close it.  COLGLOSS feeds BOTH the
    # live legend and make_howto.py, so screen and paper cannot now drift apart on these.
    ('the marks beside a name', 'At most <b>two</b>, and they are different axes: a <b>caution</b> on the left, an <b>edge</b> on the right. They are never netted against each other. Cautions: <b>AVOID</b> the injury sheet says do not draft him here &middot; <b>OUT</b> / <b>IR</b> ESPN&rsquo;s own status &middot; <b>DISC</b> take him later than this rank &middot; <b>BYE</b> collides with your roster (worth at most 1.2 pts &mdash; never move a real pick for it) &middot; <b>FADE</b> analysts called him down and nobody up &middot; <b>Q</b>/<b>D</b> questionable or doubtful. Edges: <b>BUY</b> both panels ahead of his ADP, and it gets brighter as more independent kinds of evidence agree &middot; <b>CALLS</b> podcast target calls only &middot; <b>OPEN</b> direct backup into an unsettled backfield &middot; <b>DART</b> direct backup behind a settled job &mdash; only pays on an injury &middot; <b>ok</b> the sheet actively cleared him. <b>MINE</b> is your own call and outranks every list here. Hover any mark for the full reason; click the row for the whole card.'),
    ('the GONE column', 'The last 14 players taken, newest at the top. <b>NOW</b> is the pick that just happened, then <b>-1</b>, <b>-2</b> and so on counting back. The top three are brightened. <b>14 is not a round number.</b> From slot 8 exactly 8 or 14 picks happen between your turns, so this column always holds <i>everything taken since you last picked</i> &mdash; and on the long waits (32, 56, 80, 104, 128, 152) it is exactly that window, ending at <b>-13</b>. It is not trying to replace ESPN&rsquo;s full pick list.'),
    ('the dashed TIER BREAK line', 'A real cliff inside the twelve rows on screen &mdash; the number is how many VBD points drop across it. The threshold adapts to the spread actually showing, so a flat board draws none. <b>There are always exactly three slots for these lines</b>; when fewer cliffs exist the rest are invisible spacers, which is what stops the page changing height every refresh.'),
    ('RUN: 4 RB of the last 6', 'A position run, next to the recommendation. It only fires at <b>4 or more of the last 6</b> &mdash; three of six is the ordinary state of a 12-team draft, and a warning that is always on is not a warning. Only the position actually running is named.'),
]

CONTEXT = {}          # espn_id -> (grade, dart, why).  docs 100 / 102.

def load_context():
    """doc 100: INJURY_CONTEXT_SHEET's AVOID / DISCOUNT / NEUTRAL grades, on the live board.

    It was a paper artifact the tool knew nothing about, and that gap already produced a bad
    recommendation -- doc 98 put Tank Dell up as a pick-137 target while the sheet had him at
    2 expected games. This SHOWS the grade; it never changes a number. Doc 74 is explicit that
    the injury framework cannot be backtested in this project, so it breaks ties and stops you
    flinching at healthy players; it does not get to move VBD.

    Missing or malformed file = no badges, everything else unchanged. Never fatal."""
    path = os.path.join(HERE, 'player_context.csv')
    if not os.path.exists(path):
        print("  (no player_context.csv -- injury/context badges are OFF)"); return
    try:
        import csv as _csv
        with open(path, encoding='utf-8-sig', newline='') as f:
            for row in _csv.DictReader(f):
                try: eid = int(row['ESPN_ID'])
                except (KeyError, TypeError, ValueError): continue
                g = (row.get('grade') or '').strip().upper()
                if g not in ('AVOID','DISCOUNT','NEUTRAL'): g = ''
                def _i(k):
                    try: return int(float(row.get(k) or 0))
                    except (TypeError, ValueError): return 0
                dart, buy = _i('dart'), _i('buy')
                mine = _i('mine')
                up, dn = _i('calls_up'), _i('calls_down')
                # doc 112: the backfield label, stamped in by depth_map.py.  UNSETTLED means
                # ESPN cannot say who wins that job -- the one Matt actually wants to buy.
                rook = _i('rook')
                job = (row.get('job') or '').strip().upper()
                if job not in ('UNSETTLED', 'CONTESTED', 'LEAD BACK'): job = ''
                if g or dart or buy or up or dn or mine or job or rook:
                    CONTEXT[eid] = dict(grade=g, dart=dart, buy=buy, up=up, dn=dn, mine=mine,
                                        rook=rook,
                                        job=job, job_ceil=(row.get('job_ceil') or '').strip(),
                                        mine_note=(row.get('mine_note') or '').strip(),
                                        who=(row.get('who') or '').strip(),
                                        bull=(row.get('bull') or '').strip(),
                                        bear=(row.get('bear') or '').strip(),
                                        lean=(row.get('lean') or '').strip(),
                                        quote=(row.get('quote') or '').strip(),
                                        qsource=(row.get('qsource') or '').strip(),
                                        concrete=(row.get('concrete') or '').strip(),
                                        why=(row.get('why') or '').strip())
        n = sum(1 for v in CONTEXT.values() if v['grade']=='AVOID')
        d = sum(1 for v in CONTEXT.values() if v['dart'])
        y = sum(1 for v in CONTEXT.values() if v['buy'])
        c = sum(1 for v in CONTEXT.values() if v.get('up'))
        mn = sum(1 for v in CONTEXT.values() if v.get('mine'))
        print(f"  context: {len(CONTEXT)} players loaded ({n} AVOID, {y} BUY, {c} with analyst calls, {d} darts, {mn} of YOUR takes)")
    except Exception as e:
        print(f"  (could not read player_context.csv: {e} -- badges OFF, nothing else affected)")

def badges(eid, espn_flag, bye_clash, pick_no, cost=None):
    """doc 105. TWO MARKS PER ROW, and the right-hand one now carries a STRENGTH.

    Matt's question: 'buy' and 'BUY' are not the same thing, so how do I break a tie on the spot?
    The answer is a count of how many INDEPENDENT lists point the same way, shown as dots:

        BUY ..    our two residualised analyst panels are ahead of ADP, plus one more agreeing list
        CALLS .   no panel signal, but named analysts targeted him on a podcast
        DART .    he is the direct backup on the 2026 depth chart (only shown from pick 104)
        ok        the injury sheet says he is healthy -- stop flinching

    THE DOTS ARE A COUNT, NOT A PREDICTION. Nothing in this project measures any of these signals
    against outcomes -- SS 4.13d is explicit that no ceiling metric exists here. Two of the lists
    also share people (Harmon and Boone sit in both the panel and the podcast calls), so three dots
    is not three independent opinions. Use it ONLY when `cost vs #1` says the pick is already close;
    on a clear board the rollout is the answer and this is decoration.

    The left-hand mark is a separate axis and is NEVER netted against the right one -- that is how
    you end up with a three-dot badge on a player who is hurt."""
    c = CONTEXT.get(int(eid)) or {}
    grade = c.get('grade',''); dart = c.get('dart',0); buy = c.get('buy',0)
    mine = c.get('mine',0); mine_note = c.get('mine_note','')
    job  = c.get('job','');  job_ceil = c.get('job_ceil','')
    up = c.get('up',0); dn = c.get('dn',0); who = c.get('who',''); why = c.get('why','')
    fl = str(espn_flag or '')

    caution = None
    if mine < 0:                         caution = ('ctxA', 'MINE')   # doc 108: your own fade wins
    elif grade == 'AVOID':               caution = ('ctxA', 'AVOID')
    elif fl in ('OUT','INJURY_RESERVE'): caution = ('ctxA', 'OUT' if fl=='OUT' else 'IR')
    elif grade == 'DISCOUNT':            caution = ('ctxD', 'DISC')
    elif bye_clash:                      caution = ('ctxB', 'BYE')
    elif dn and not up:                  caution = ('ctxF', 'FADE')
    elif fl:                             caution = ('ctxQ', {'QUESTIONABLE':'Q','DOUBTFUL':'D'}.get(fl, fl[:3]))

    # doc 107: THREE KINDS of evidence, not a count of lists. The panel and the podcast calls
    # share people (Harmon and Boone sit in both), so they are ONE kind and score once -- counting
    # them twice is the same double-count I found inside the two CSVs. Max is therefore 3 because
    # there are only three independent kinds, not because of an arbitrary cap.
    parts = []
    if buy and up and not dn:
        parts.append(f'ANALYSTS: our panels are ahead of ADP AND {up} podcast target call(s) '
                     f'-- note these two lists share analysts')
    elif buy:
        parts.append('ANALYSTS: our two panels are ahead of ADP')
    elif up and not dn:
        parts.append(f'ANALYSTS: {up} podcast target call(s), no downgrades')
    if dart and pick_no >= 104:
        parts.append('ROLE: direct backup on the 2026 depth chart'
                     + (f' in an UNSETTLED backfield -- the job is worth {job_ceil} pts to whoever wins it'
                        if job == 'UNSETTLED' else
                        ' behind a LEAD BACK -- only pays on an injury' if job == 'LEAD BACK' else ''))
    # HEALTH was a third kind for about ten minutes. Dropped: a NEUTRAL grade exists only for the
    # five players the injury sheet bothered to clear, so it was unattainable for everyone else and
    # a dot you cannot earn is not a scale. It survives as the standalone `ok` badge instead.
    n = len(parts)          # 0-2 by construction: ANALYSTS, ROLE. There is no third kind.

    edge = None
    # doc 106: this used to be one if/elif chain and my first attempt to add `tier` cut it in
    # half, so `if buy:` overwrote the suppression above it and an AVOID player got a green mark
    # again. Written as an explicit guard-then-chain so that cannot happen twice.
    silenced = (grade == 'AVOID') or (fl in ('OUT','INJURY_RESERVE')) or (dn and not up) or (mine < 0)
    near = (cost is None) or (abs(float(cost)) <= 3.0)
    tier = min(3, max(n, 1) + (1 if n >= 2 else 0)) if near else 1   # 2 kinds -> brightest tier
    if mine > 0:                         edge = ('ctxM', 'MINE')   # doc 108: your call outranks
    elif silenced:                       edge = None                  # every list on the page
    elif buy:                            edge = (f'ctxY{tier}', 'BUY')
    elif up:                             edge = (f'ctxY{tier}', 'CALLS')
    elif dart and pick_no >= 104:        edge = ('ctxS', 'OPEN' if job == 'UNSETTLED' else 'DART')
    elif grade == 'NEUTRAL':             edge = ('ctxN', 'ok')

    tip = ' | '.join(x for x in (
        f"ESPN: {fl}" if fl else '',
        "bye clashes with your roster" if bye_clash else '',
        (f"YOUR TAKE: {mine_note}" if mine_note else ('YOUR TAKE' if mine else '')),
        ('AGREEING: ' + '; '.join(parts)) if parts else '',
        (f"analysts: {who}" if who else ''),
        (f"{dn} downgrade call(s)" if dn else ''),
        why) if x)

    # doc 156.  Matt: "I do want exciting rookies promoted."  This is deliberately NOT a third
    # badge -- doc 105 caps the row at two MARKS (a caution and an edge) and a third judgment
    # would compete with the two that were measured.  A rookie is not a judgment, it is an
    # attribute of the player, so it renders in grey with no border, reading as part of the name.
    # It moves no number.  SS4.13d: this project has no ceiling metric and the analyst panel
    # cannot supply one; SS4.13b measured that 4 of 5 players in the late ADP band never become
    # startable.  The mark says WHO is a rookie.  It does not say that being one is good.
    rk = ' <i class="rk" title="Rookie -- no 2025 NFL snaps, and not in the 2023 or 2024 player pool. A fact, not a ceiling estimate.">R</i>' if c.get('rook') else ''

    out = rk
    if caution:
        cls, lbl = caution
        out += f' <span class="{cls}" title="{html_attr(tip)}">{lbl}</span>'
    if edge:
        cls, lbl = edge
        # doc 106, measured: among flagged players, MORE dots goes with a WORSE player
        # (rho -0.35 on VBD) -- every signal feeding them is a late-round signal by construction.
        # So the strength only renders where it is actually a tie-breaker: when this row is within
        # 3 points of row 1. Elsewhere the word stays and the dots do not, because "three dots at
        # board rank 202" is a sentence that should never form.
        dots = ('<b class="pip">' + '&#9679;'*n + '</b>') if (n and near and lbl in ('BUY','CALLS','DART','OPEN')) else ''
        out += f' <span class="{cls}" title="{html_attr(tip)}">{lbl}{dots}</span>'
    return out

def card_data(eid, r):
    """doc 117. Matt: "i'd rather have player cards that could pop-up when a row is selected...
    just in case i wanted more context of what makes them a bull case."

    The badges are a two-mark summary by design (doc 105) and the hover is one line. Neither can
    hold a bull case AND a bear case AND an injury AND a backfield. This packs the whole profile
    into the row as a data attribute; the click handler in CARD_JS renders it. It costs one
    attribute per row and no extra requests -- draft night has no network to spare."""
    c = CONTEXT.get(eid, {})
    if not c: return ''
    parts = []
    def add(label, text, cls=''):
        if text and str(text).strip() and str(text).strip().lower() != 'nan':
            parts.append((label, str(text).strip(), cls))
    g = c.get('grade','')
    why = [w.strip() for w in str(c.get('why','')).split('||')]
    # "no injury news found | exp 17 gm | [low confidence]" is the absence of a finding. It was on
    # 107 of 143 rows and is not worth a line on a card you opened to learn something.
    why = [re.sub(r'\s*\|\s*(exp \d+ gm|\[(low|medium|high) confidence\])', '', w).strip(' |')
           for w in why]
    if why and why[0].lower().startswith('no injury news found') and g in ('', 'NEUTRAL'):
        why = why[1:]
    if g and g != 'NEUTRAL' and why:
        add('STATUS', f"{g} - {why[0][:260]}", 'bad' if g == 'AVOID' else 'warn'); why = why[1:]
    elif why:
        add('NOTE', why[0][:260]); why = why[1:]
    for extra in why[:2]:
        add('ALSO', extra[:220])
    if c.get('job') and r.get('pos') == 'RB':
        jc = str(c.get('job_ceil', '')).split('.')[0]
        j = c['job'] + (f" - the job is worth {jc} pts to whoever wins it" if jc else '')
        add('BACKFIELD', j, 'good' if c['job'] == 'UNSETTLED' else '')
    add('BULL', c.get('bull',''), 'good')
    add('BEAR', c.get('bear',''), 'bad')
    if c.get('lean'):
        LC = {'strongly bull': 'good', 'lean bull': 'good', 'genuinely split': '',
              'lean bear': 'bad', 'strongly bear': 'bad'}
        add('WHERE THE COMMENTARY SITS', c['lean'].upper(), LC.get(c['lean'], ''))
    if c.get('quote'):
        add('QUOTE', '"' + c['quote'] + '"' + (f"  - {c.get('qsource','')}" if c.get('qsource') else ''), 'quo')
    if c.get('who'): add('ANALYSTS AHEAD OF ADP', c['who'])
    if c.get('concrete'): add('CHANGED RECENTLY', c['concrete'])
    if not parts: return ''
    body = ''.join(f'<div class="cl {cls}"><span>{html_attr(l)}</span>{html_attr(t)}</div>'
                   for l, t, cls in parts)
    return ' data-card="%s"' % html_attr(f'<h3>{r["player"]} <em>{r["pos"]} {r["team"]}'
                                         f' &middot; bye {int(r["bye"])}</em></h3>{body}')


def html_attr(t):
    return (t or '').replace('&','&amp;').replace('"','&quot;').replace('<','&lt;').replace('>','&gt;')

CARD_CSS = """
tr.pr[data-card]{cursor:pointer}
tr.pr[data-card]:hover td{background:#1b2330}
#scrim{display:none;position:fixed;inset:0;background:rgba(8,11,16,.72);z-index:200}
#card{display:none;position:fixed;z-index:201;top:50%;left:50%;transform:translate(-50%,-50%);
  width:min(760px,92vw);max-height:86vh;overflow:auto;background:#121926;color:#e8edf5;
  border:1px solid #35405a;border-radius:10px;padding:18px 22px 20px;
  box-shadow:0 18px 60px rgba(0,0,0,.6);font-size:15px;line-height:1.45}
#card h3{margin:0 0 12px;font-size:22px;font-weight:700;color:#fff}
#card h3 em{font-style:normal;font-size:14px;color:#8b95a8;font-weight:400;margin-left:8px}
#card .cl{margin:0 0 11px;padding-left:11px;border-left:3px solid #2c3648}
#card .cl span{display:block;font-size:10.5px;letter-spacing:1.1px;color:#7f8ba0;margin-bottom:2px}
#card .cl.good{border-color:#1f9d63}
#card .cl.bad{border-color:#d0453a}
#card .cl.warn{border-color:#d99b1c}
#card .cl.quo{border-color:#3b82c4;font-style:italic;color:#bcd4ec}
#card .x{position:absolute;top:10px;right:14px;color:#7f8ba0;font-size:20px;cursor:pointer}
#cardhint{margin-top:14px;font-size:11.5px;color:#6f7a8d;border-top:1px solid #2c3648;padding-top:9px}
"""

CSS = CSS + CARD_CSS        # doc 117: CSS is a plain string, so this must be an
                            # append AFTER both exist -- an f-style {CARD_CSS}
                            # placeholder inside it renders literally.

CARD_JS = """<div id="scrim"></div><div id="card"><span class="x">&times;</span><div id="cardbody"></div>
<div id="cardhint">click anywhere, or press Esc, to close &mdash; the board is frozen while this is open</div></div>
<script>
/* doc 117. A row with a profile is clickable; the profile is already in the row as data-card,
   so opening one costs nothing and works with the network down. The board does NOT reload while
   a card is open -- that was the whole bug behind the tooltips (doc 103) and a card that vanishes
   mid-sentence is worse than no card. */
(function(){
  var card=document.getElementById('card'), scrim=document.getElementById('scrim'),
      body=document.getElementById('cardbody');
  function open(html){ body.innerHTML=html; card.style.display='block'; scrim.style.display='block';
                       window.__cardOpen=true; }
  function shut(){ card.style.display='none'; scrim.style.display='none'; window.__cardOpen=false; }
  document.addEventListener('click',function(e){
    var tr=e.target.closest?e.target.closest('tr.pr[data-card]'):null;
    if(tr){ open(tr.getAttribute('data-card')); return; }
    if(card.style.display==='block') shut();
  },false);
  document.addEventListener('keydown',function(e){ if(e.key==='Escape') shut(); });
})();
</script>"""

HOLD_JS = """<div id="hold">holding &mdash; move the mouse off the board to resume</div>
<script>
/* doc 103, found by Matt: the page reloaded every 3 seconds, so a tooltip died before you could
   read it. The badges are useless if you cannot hover them.

   The <meta refresh> above is now a 20-second SAFETY NET for the case where this script does not
   run at all. If it does run, it cancels the meta and takes over: reload after 3s, but never
   while the pointer is over the board -- with a 25-second cap so a mouse left on the table can
   never freeze the night's most important screen. */
(function(){
  try{
    var m=document.querySelector('meta[http-equiv="refresh"]'); if(m) m.parentNode.removeChild(m);
  }catch(e){}
  var over=false, due=Date.now()+3000, held=0, chip=document.getElementById('hold');
  /* target the board table BY ID, not by document order -- adding any table above it would
     silently move the hold zone somewhere useless. */
  var zone=document.getElementById('board')||document.querySelector('table')||document.body;
  zone.addEventListener('mouseenter',function(){over=true;},true);
  zone.addEventListener('mouseleave',function(){over=false;held=0;if(chip)chip.style.display='none';},true);
  /* doc 149, findings 2 and 3.  My first version of this held the reload while the legend was
     open, sharing `held` with the hover branch -- and `mouseleave` resets `held` to 0, so moving
     the mouse on and off the table (the ordinary motion of reading a glossary that sits directly
     under it) renewed the hold forever: MEASURED AT ZERO RELOADS IN TWO MINUTES.  The 25s cap at
     :976 exists precisely so a mouse left on the table can never freeze the night's most
     important screen, and I defeated it.
     THE BOARD MUST NEVER STOP REFRESHING.  So there is no hold at all now -- only the open state
     survives, and the page keeps its 3-second rhythm underneath it.
     `location.hash` and not `history.replaceState`: the page is opened as a file:// URI, where
     Chrome refuses replaceState with a URL argument, and the catch(e){} made that failure silent.
     Setting the fragment is a plain navigation, allowed on every origin, and location.reload()
     carries it. */
  var g=document.getElementById('gloss');
  if(g){
    if(location.hash==='#gloss') g.open=true;
    g.addEventListener('toggle',function(){
      try{ location.hash = g.open ? 'gloss' : ''; }catch(e){}
    });
  }
  setInterval(function(){
    if(Date.now()<due) return;
    if(window.__cardOpen){ due=Date.now()+400; return; }   /* doc 117: never reload under a card */
    if(over && held<25000){ held+=400; due=Date.now()+400;
      if(chip) chip.style.display='block'; return; }
    location.reload();
  },400);
})();
</script>"""

def _waiting_hero(top, who, fut, nxt, cliffs, runflag):
    """doc 147.  The waiting panel said the same thing three times -- "planning for pick 32",
    "Your next turn is pick 32", and the clock box's "you in 9" -- and said nothing Matt could
    use.  Waiting is the only time in the hour he has time to read, and the two facts worth
    reading are already computed: WHO he would take if the board froze (row 1 of the table he is
    looking at) and WHICH position falls off a cliff before he gets there (eng.cliffs).  Both are
    displayed elsewhere on the page; this only promotes them to where his eye already is."""
    nx = fut[0] if fut else None
    if not top:
        return ('<div class="hero" style="flex:1;border-left-color:#5b9dd9">'
                '<div class="sub">WAITING</div>'
                f'<div class="pick" style="font-size:19px">{who} is picking{runflag}</div>'
                '<div class="why">No candidates on the board right now.</div></div>')
    # doc 148, red team finding 1 -- I SHIPPED A WRONG NUMBER THIS AFTERNOON.  The sentence
    # said the drop happened "between now and then", and the clause before it binds "then" to
    # nx, Matt's NEXT pick.  It does not: `cliffs` is computed at `ref` and Engine.cliffs uses
    # `p > pick_no` (strictly greater), so the drop it returns spans now -> the turn AFTER the
    # next one.  Measured at pick 30: the page said "the RB board drops 23.4 between now and
    # then" while you are up at 32, and 23.4 is the decline to pick 41.  The right pick number
    # was already being passed in as `nxt` and was never used.  Say what the number IS.
    worst = cliffs[0] if cliffs else None          # Engine.cliffs already sorts by -drop
    warn = (f' If you pass on <b>{worst["pos"]}</b> at {nx or "-"}, that board is '
            f'<b>{worst["drop"]}</b> pts worse by pick {nxt or "-"}.') if (worst and nxt) else ''
    return ('<div class="hero" style="flex:1;border-left-color:#5b9dd9">'
            f'<div class="sub">IF THE BOARD HELD, YOU TAKE</div>'
            f'<div class="pick">{top["player"]} '
            f'<span class="pos {top["pos"]}">{top["pos"]}</span>{runflag}</div>'
            f'<div class="why">{who} is on the clock; you are up at '
            f'<b>{nx or "-"}</b>.{warn}</div></div>')


def render(eng, pick_no, on_clock, recs, cliffs, taken_recent, my_roster, status):
    c = eng.counts
    # doc 154.  Matt: "i forgot how i avoid a position drought AGAIN. Is position cliffs on the
    # lower part my only guide?"  It was not -- this strip already existed -- but it lived at the
    # bottom of the ROSTER panel, in 12px mono, on the far side of the page from everything he
    # reads on the clock.  The one line that says "you are about to be short a starter" was the
    # least visible thing on the board.  It moves up, and it gains the two facts it was missing:
    #   * FLEX.  Starters are 1/2/2/1 plus a FLEX, and a strip that stops at TE cannot tell him
    #     whether nine slots are covered or eight.
    #   * WHEN the engine takes the choice away.  code_live_engine.legal() returns ONLY the
    #     missing positions once picks_left <= how many are missing -- verified by execution:
    #     0 QB + 0 TE goes QB/TE-only with 2 turns left; TE alone goes TE-only with 1.  The page
    #     never said so, so the forcing arrived as a surprise.  Now it is announced a turn early.
    # HEIGHT IS FIXED (doc 139): this is always exactly one line, whatever it says.
    need = []
    for p,n in (('QB',1),('RB',2),('WR',2),('TE',1)):
        have=c.get(p,0)
        cap = CLE.CAPS.get(p)
        cls = 'ok' if have>=n else ('warn' if have>=n-1 else 'bad')
        full = '<i>full</i>' if cap is not None and have>=cap else ''
        # doc 160.  This used to print `RB 3/2` and Matt read it the only way it can be read --
        # "three out of two", which is nonsense.  The denominator is STARTING SLOTS, so the
        # numerator must never exceed it: the slots fill to n and the surplus is stated
        # separately as `+k`, which is the bench depth and a thing he actually wants to see
        # (SS6: bench RB to the cap, then WR).  Same colour rule, same one line, no new width.
        extra = f'<i>+{have-n}</i>' if have > n else ''
        need.append(f'<span class="{cls}">{p} {min(have,n)}/{n}{extra}{full}</span>')
    flex = max(0, c.get('RB',0)-2) + max(0, c.get('WR',0)-2) + max(0, c.get('TE',0)-1)
    need.append(f'<span class="{"ok" if flex else "bad"}">FLEX {min(flex,1)}/1</span>')
    _left  = [p for p in list(CLE.MY_PICKS) if p >= pick_no]
    _miss  = [p for p in ('QB','TE') if c.get(p,0)==0]
    if _miss and len(_left) <= len(_miss):
        _sd = (f'<b class="bad">FORCED &mdash; only {" and ".join(_miss)} from here.</b> '
               f'{len(_left)} turn{"s" if len(_left)!=1 else ""} left.')
    elif _miss and len(_left) == len(_miss)+1:
        _sd = (f'<b class="warn">{len(_left)} turns left and no {" or ".join(_miss)} &mdash; '
               f'next turn the board can only offer {" and ".join(_miss)}.</b>')
    else:
        _sd = (f'{len(_left)} skill turn{"s" if len(_left)!=1 else ""} left'
               + (f' &middot; still no {" or ".join(_miss)}' if _miss else ''))
    need.append(f'<span class="sdrift">{_sd}</span>')
    top = recs[0] if recs else None
    # doc 149, finding 5.  This was MY_PICKS-only, which ends at 137 -- so from pick 138 the hero
    # said "you are up at -" and the footer said "your picks done" for roughly 22 consecutive
    # picks while the D/ST and kicker turns were still ahead.  The red team was right that doc
    # 148's `ref` change did NOT fix those two symptoms: recommend() and cliffs() derive their own
    # next-turn from MY_PICKS and are unchanged (deliberately -- MY_PICKS feeds the survival maths
    # and 4.12's calibration, and is not something to widen four days out).  What IS fixable
    # without touching the engine is what the page SAYS about your remaining turns.
    fut=[p for p in list(CLE.MY_PICKS) + [CLE.DST_PICK, CLE.K_PICK] if p>=pick_no]
    nxt = fut[1] if len(fut)>1 else None
    slot, who, rnd = whose_pick(pick_no)

    # ---- position run, shown UP TOP next to the recommendation --------------
    # doc 147.  THIS FIRED ON A NON-EVENT.  The bar was 3 of the last 6 at one position, which
    # is the ORDINARY state of a 12-team draft -- at pick 8 it announced "RUN: 3 RB, 3 WR in the
    # last 6", i.e. all six picks, as a warning.  A warning that is always on is not a warning,
    # and it sat in the headline next to the recommendation.  4 of 6 is a real run; and only the
    # position actually running is named, because "3 RB, 3 WR" is just the draft.
    runs={}
    for i in taken_recent[-6:]: runs[eng.pos[i]]=runs.get(eng.pos[i],0)+1
    hot=[f'{v} {k}' for k,v in sorted(runs.items(), key=lambda z:-z[1]) if v>=4]
    runflag = (f'<span class="runflag">RUN: {hot[0]} of the last 6</span>') if hot else ''

    # ---- the gone list, now a column of the board itself --------------------
    # doc 147.  doc 139 pinned the BOARD to one shape and left the column beside it free to
    # grow from 0 rows to 18 -- so the page still changed height for the first two rounds, for
    # the same reason and with the same cost.  Fixed at GONE_ROWS, padded.
    #
    # doc 163: 8 -> 14, and 14 is not a taste.  From slot 8 the gaps between Matt's turns are
    # 9 and 15 picks alternating (8, 17, 32, 41, ...), so the number of picks made by OTHER
    # managers since his previous turn is exactly 8 or exactly 14.  At 14 rows this column
    # ALWAYS holds everything taken since he last picked, on every one of his fourteen turns.
    # At 8 it holds all of them only on the short gaps and truncates the long ones by 6 --
    # including pick 32, the longest-gap and most decisive turn on the board (SS2.1).
    # Measured: the LEFT side still governs the page height at 14, so doc 139's fixed shape
    # is untouched.  Going past 14 buys nothing -- there is no question it answers.
    GONE_ROWS = 14
    gone=''
    for k,i in enumerate(reversed(taken_recent[-GONE_ROWS:])):
        gone+=(f'<li class="{"fresh" if k<3 else ""}">'
               f'<span class="pos {eng.pos[i].replace("/","")}">{eng.pos[i]}</span>'
               f'<span class="nm">{eng.name[i]}</span>'
               f'<span class="agn">{"NOW" if k==0 else f"-{k}"}</span></li>')
    for _ in range(GONE_ROWS - min(len(taken_recent), GONE_ROWS)):
        gone += '<li class="gpad"><span class="nm">&nbsp;</span></li>'
    if not taken_recent:
        gone = ('<li><span class="nm" style="color:#5a6270">nothing yet</span></li>'
                + '<li class="gpad"><span class="nm">&nbsp;</span></li>' * (GONE_ROWS-1))

    # ---- board ---------------------------------------------------------------
    myb = {int(eng.bye[i]) for i in my_roster}
    # doc 148, red team finding 2.  The bar was normalised to the WORST ROW ON SCREEN, so the
    # bottom row drew a full bar at every pick and a full bar meant 40 points at pick 17 and 4.6
    # points at pick 89 -- and on a flat board nine rows tagged "tie" carried bars from 18% to
    # 82%, the graphic contradicting the label beside it.  A FIXED scale instead: full = 20 pts
    # behind, at every pick, all night.  A tie (<=1.5) now draws 8% -- visually nothing, which
    # is the honest picture.  The number is on the legend so the length can be read.
    BAR_FULL = 20.0
    # A tier break marks a real cliff, not every small step. Threshold adapts to the
    # spread actually on screen: 1.5x the median gap, floored at 8 VBD so a flat board
    # never draws lines and a steep one never hides them.
    gaps = [recs[k-1]['vbd'] - recs[k]['vbd'] for k in range(1, min(12, len(recs)))]
    gaps = [g for g in gaps if g > 0]
    TIER = max(8, 1.5 * (sorted(gaps)[len(gaps)//2] if gaps else 0))
    # doc 139.  THE BOARD MUST HAVE THE SAME SHAPE ON EVERY REFRESH.  Matt: "the draft board
    # changes how many rows are displayed. That can be distracting."  He is right, and on a
    # 60-second clock it is worse than distracting -- everything below the board slides up and
    # down between refreshes, so the row your eye was on is not where you left it.  Two causes:
    # the candidate list runs short late in the draft, and the number of dashed tier lines
    # varies with the spread.  Both are now pinned: exactly BOARD_ROWS player rows (padded) and
    # exactly BOARD_TIERS divider rows (the biggest breaks; invisible spacers make up the rest).
    # Fixing the STRUCTURE rather than setting a min-height means the height is identical by
    # construction -- no pixel estimate to get wrong.
    BOARD_ROWS, BOARD_TIERS = 12, 3
    shown = recs[:BOARD_ROWS]
    brk = []
    for k in range(1, len(shown)):
        d = shown[k-1]['vbd'] - shown[k]['vbd']
        if d >= TIER:
            brk.append((d, k))
    brk.sort(reverse=True)
    brk = dict((k, d) for d, k in brk[:BOARD_TIERS])   # keep only the biggest cliffs
    rows=''; prev=None; used_tiers=0
    for n,r in enumerate(shown, 1):
        if (n-1) in brk:
            used_tiers += 1
            rows += ('<tr class="tier"><td colspan="11"><div>'
                     f'<span>TIER BREAK &nbsp;-{brk[n-1]:.0f} VBD</span></div></td></tr>')
        prev = r['vbd']
        # the rec dict carries the board ROW index, not the id; look the id up rather than
        # widening the engine's contract days before the draft.
        try:    eid = int(eng.b.ESPN_ID.iloc[r['i']])
        except Exception: eid = -1
        flag = badges(eid, r['flag'], int(r['bye']) in myb, pick_no, r['cost'])
        clash = ''
        cost = r['cost']
        # doc 147: same thresholds doc 139 fixed for the headline -- 1.5 and 6 -- applied per row.
        # doc 148, red team finding 3: `cost` is rounded to 1dp, so a row within 0.05 of the best
        # becomes -0.0, and `-0.0 == 0` is True -- TWO rows rendered green "free" in 6 of the
        # states swept, against a legend that had just been made to promise only one can.  Row 1
        # is the recommendation BY POSITION, not by arithmetic; everything else is at best a tie.
        ccls = ('free' if n == 1 else 'tie' if abs(cost) <= 1.5
                else 'cheap' if abs(cost) <= 6 else 'dear')
        cw = 0 if n == 1 else min(100, abs(cost)/BAR_FULL*100)
        cd = card_data(eid, r)
        # doc 147: "still there?" on ROW 1 answered a question nobody is asking -- he is being
        # taken NOW -- and an 8% next to the recommendation reads as a warning about it.
        # doc 148, red team finding 4: that is only true ON THE CLOCK.  While waiting, row 1 is
        # the player the hero headlines as "IF THE BOARD HELD, YOU TAKE", and blanking it deleted
        # his survival odds from the entire page -- a 24%-to-last player presented as the plan
        # with no number anywhere.  Blank it only when he is actually being taken.
        stil = '&mdash;' if (n == 1 and on_clock) else f'{r["p_next"]*100:.0f}%'
        # doc 154, MEASURED (12 rooms, the current board).  The spread of `cost vs #1` across the
        # twelve rows collapses from 44.6 points at pick 8 to 0.12 at pick 137 -- so the one bar
        # on the page is measuring noise by round 7.  The spread of `still there?` does NOT
        # collapse: it stays 48-85 percentage points all the way to pick 128.  And from pick 80 on,
        # 4 to 7 of the twelve rows sit inside 1.5 of the recommendation -- the engine's own "I
        # cannot separate these" -- while their survival differs by 40 to 51 points.
        # So: no second BAR (doc 147's whole lesson is that a second magnitude bar competes with
        # the one that decided the pick).  A CATEGORICAL mark instead, and only where the engine
        # has already admitted the tie: among rows tied with #1, the ones that will be GONE first.
        # HONESTY, and it belongs in the legend too: rollout_scores() ALREADY simulates who will
        # be gone, so a tie is a tie AFTER survival is counted.  The mark is therefore not a
        # tiebreaker that beats the engine -- it says which of the equally-good rows is available
        # ONLY NOW, which is what you act on when you hold something the board cannot see: the
        # news line on the card, an analyst call, a badge (doc 153 s8 -- late, those are the only
        # tiebreakers there are).
        # THREE GATES, all of them refusals:
        #   * only when row 1 has a survival number to compare against (not the last skill pick,
        #     where nxt is None and every p_next is 1.00 -- measured: spread 0pp at 137);
        #   * only inside 4.20's adp_pick < 168 window.  Past it 4.14 says the ordering is
        #     fabricated, and marking a survival number there would put ink on an invented one;
        #   * only on a gap of 20 points or more, so it fires on a real difference.
        gof = ''
        # NOT `nxt` -- that is the display's next turn and includes the D/ST and K picks, so at
        # 137 it is 152 and the gate would not fire.  The engine's own next turn comes from
        # MY_PICKS and is None at 137, where every p_next is 1.00 and the column means nothing.
        # (Harmless today -- a 20-point gap cannot exist among twelve 1.00s -- but the comment
        # above claimed a guard the code did not have, which is doc 149's whole lesson.)
        _snx = next((q for q in CLE.MY_PICKS if q > pick_no), None)
        if (n > 1 and _snx is not None and abs(cost) <= 1.5
                and float(r.get('adp', 999)) < 168
                and (top['p_next'] - r['p_next']) >= 0.20):
            gof = ' <i class="gof">goes first</i>'
        stil += gof
        rows+=(f'<tr class="pr"{cd}><td class="rank">{n}</td>'
               f'<td><b>{r["player"]}</b>{flag}{clash}</td>'
               f'<td><span class="pos {r["pos"]}">{r["pos"]}</span></td>'
               f'<td class="mono">{r["team"]}</td><td class="num">{int(r["bye"])}</td>'
               f'<td class="vbd">{r["vbd"]}</td>'
               f'<td class="num">{r["mv"]}</td><td class="num">{r["hold"]}</td>'
               f'<td class="key">{r["delta"]:+}</td>'
               f'<td class="cost {ccls}"><div class="bar" style="width:{cw:.0f}%"></div>'
               f'<span class="v">{"free" if n==1 else f"{cost:+}"}</span></td>'
               f'<td class="num">{stil}</td></tr>')
    if not rows:
        rows = ('<tr><td colspan="11" style="color:#98a0ae;padding:14px">'
                'No candidates returned.</td></tr>')
        used_tiers = BOARD_TIERS          # nothing to pad against; keep the block flat
    else:
        for _ in range(BOARD_ROWS - len(shown)):
            rows += '<tr class="padrow"><td colspan="11">&nbsp;</td></tr>'
    for _ in range(BOARD_TIERS - used_tiers):
        rows += '<tr class="tier gh"><td colspan="11"><div></div></td></tr>'

    cl=''
    for x in cliffs:
        cl+=(f'<tr><td><span class="pos {x["pos"]}">{x["pos"]}</span></td>'
             f'<td class="num">{x["now"]}</td><td class="num">{x["at_next"]}</td>'
             f'<td class="num"><b>-{x["drop"]}</b></td></tr>')
    cl = cl or '<tr><td colspan="4" style="color:#98a0ae">no cliff before your next turn</td></tr>'
    ros=''
    for i in my_roster:
        ros+=(f'<tr><td><span class="pos {eng.pos[i].replace("/","")}">{eng.pos[i]}</span></td>'
              f'<td>{eng.name[i]}</td><td class="mono">bye {int(eng.bye[i])}</td>'
              f'<td class="num">{eng.vbd[i]:.0f}</td></tr>')
    ros = ros or '<tr><td style="color:#98a0ae">empty</td></tr>'

    clock = (f'<div class="clock {"mine" if on_clock else ""}">'
             f'<div class="lbl">{"YOU ARE UP" if on_clock else "ON THE CLOCK"}</div>'
             f'<div class="n">{pick_no}</div>'
             f'<div class="who">{who}<br>round {rnd}'
             + ('' if on_clock else f' &middot; you in {fut[0]-pick_no}' if fut else '') +
             '</div></div>')

    # doc 79: the rows are sorted by ROLL (the full-draft rollout), not by delta. The headline
    # number must be the one that decided the pick -- directive s7. Roll is a raw EV and means
    # nothing alone, so show its interpretable form: the margin over the runner-up.
    marg = round(-recs[1]['cost'], 1) if top and len(recs) > 1 else 0.0
    mtag = 'clear' if marg >= 6 else ('slim' if marg >= 1.5 else 'a coin flip')
    hero = ('<div class="hero" style="flex:1"><div class="sub">TAKE</div>'
            f'<div class="pick">{top["player"]} '
            f'<span class="pos {top["pos"]}">{top["pos"]}</span> '
            f'<span class="big">+{marg}</span>{runflag}</div>'
            f'<div class="why">Best by <b>{marg}</b> pts over the next row &mdash; {mtag}. '
            f'Adds <b>{top["mv"]}</b> lineup pts now; the best {top["pos"]} '
            f'expected to survive to pick {nxt or "-"} adds <b>{top["hold"]}</b> '
            f'(&Delta; {top["delta"]:+}). He is {int(top["p_next"]*100)}% to last to your next turn.'
            '</div></div>') if top and on_clock else _waiting_hero(
                top, who, fut, nxt, cliffs, runflag)

    # doc 148, finding 2: `status` was a dead parameter after this afternoon's rewrite.  It now
    # carries the one thing the page could not say about itself -- that its own input stopped.
    # doc 149, finding 10: interpolated raw. Nothing today can reach it with metacharacters, but
    # a warning string is exactly the kind of thing that later gets an error message pasted into it.
    banner = (f'<div class="feedwarn">&#9888; {html.escape(str(status))}</div>') if status else ''
    gl=''.join(f'<div class="row"><b>{k}</b> &mdash; {v}</div>' for k,v in COLGLOSS)

    return f"""<!doctype html><html><head><meta charset="utf-8">
<meta http-equiv="refresh" content="20"><title>JUG board - pick {pick_no}</title>
<link href="https://fonts.googleapis.com/css2?family=Chivo:wght@600;700&family=IBM+Plex+Mono&family=IBM+Plex+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="shell">

{banner}
<div class="clockrow">{clock}{hero}</div>

<div class="pos-fill">{''.join(need)}</div>

<div class="board-split">
  <div class="gonecol">
    <h2 style="font:700 10px/1 Chivo;letter-spacing:.1em;text-transform:uppercase;color:#98a0ae;margin:0 0 8px">Gone &mdash; newest first</h2>
    <ol style="list-style:none;margin:0;padding:0">{gone}</ol>
  </div>
  <div style="padding:11px 13px;min-width:0">
    <h2 style="font:700 10px/1 Chivo;letter-spacing:.1em;text-transform:uppercase;color:#98a0ae;margin:0 0 8px">
      Board &mdash; row 1 is the pick. The amber <b>cost vs #1</b> column orders the list and is what taking any other row would cost you; <b>tie</b> means the engine cannot separate them.</h2>
    <div class="boardwrap"><table id="board" class="board">
    <tr><th></th><th>player</th><th>pos</th><th>tm</th><th class="num">bye</th>
    <th class="vbdh">VBD</th><th class="num">adds now</th><th class="num">if I wait</th>
    <th class="key">wait cost</th><th class="costh">cost vs #1</th><th class="num">still there?</th></tr>{rows}</table></div>
    <details class="legend" id="gloss"><summary>what do these columns mean?</summary>{gl}</details>
  </div>
</div>

<div class="grid" style="margin-top:12px">
  <div class="panel"><h2>Position cliffs before your next pick</h2>
    <table><tr><th>pos</th><th class="num">best now</th><th class="num">best at next</th>
    <th class="num">drop</th></tr>{cl}</table></div>
  <div class="panel"><h2>Your roster</h2>
    <table>{ros}</table></div>
</div>

{render_watch(eng, pick_no)}

<div class="sub" style="color:#5a6270;font-size:11px;margin-top:10px">
  your picks {', '.join(str(p) for p in fut) or 'done'} &middot; D/ST {CLE.DST_PICK}
  &middot; K {CLE.K_PICK} &middot; updated {dt.datetime.now():%H:%M:%S}</div>
</div>{CARD_JS}{HOLD_JS}</body></html>"""


def verify_slot(season, lid, team_id):
    """doc 125. Read ESPN's published draft order and check it against the compiled slot.
    Never fatal: on draft night a failed check must not stop the tool from running."""
    try:
        u = READS.format(season=season, lid=lid) + "?view=mSettings"
        d = requests.get(u, cookies=COOKIES, headers=HEADERS, timeout=8).json()
        if isinstance(d, list): d = d[0]
        order = ((d.get('settings') or {}).get('draftSettings') or {}).get('pickOrder') or []
        if not order:
            print("  (ESPN has not published a draft order yet -- slot unverified)"); return
        if team_id not in order:
            print(f"  !! team {team_id} is NOT in ESPN's draft order {order}. Check --team."); return
        s_true = order.index(team_id) + 1
        # the configured slot IS the round-1 pick in a snake, and MY_PICKS[0] is always round 1
        cfg = CLE.MY_PICKS[0] if CLE.MY_PICKS else None
        if s_true == cfg:
            print(f"  draft order confirms your slot: {s_true} of {len(order)}")
        else:
            print("  " + "!"*68)
            print(f"  !! SLOT MISMATCH. The tool is planning for slot {cfg}; ESPN's published")
            print(f"     order puts team {team_id} at slot {s_true}. Order: {order}")
            print(f"     EVERY turn is being planned for the wrong picks. Restart with")
            print(f"     --slot {s_true} before the draft starts.")
            print("  " + "!"*68)
    except Exception as e:
        print(f"  (could not verify slot: {e} -- not fatal, continuing)")


def detect_shape(season, lid, team_id, teams=None, slot=None):
    """Ask ESPN how big the league is and where you pick."""
    # doc 209. IF THE OPERATOR HAS TOLD US BOTH, BELIEVE HIM AND DO NOT CALL ESPN AT ALL.
    # The failure branch at the bottom prints "Pass both explicitly: --slot N --teams N" as the
    # remedy for a GET that has already failed -- but the GET ran first, unconditionally, so
    # obeying that instruction re-issued the same failing request and printed the same line
    # forever. An ESPN PRACTICE draft is exactly the case: doc 126 measured that ESPN deletes
    # the practice league, so this read can 404 while the browser bridge is happily forwarding
    # picks. Verified by executing the branch with the GET stubbed to raise.
    # Mock-only: the real draft takes the else-branch (verify_slot) and never enters this.
    if teams and slot:
        print("  shape supplied on the command line: %d teams, slot %d "
              "(ESPN not consulted)" % (teams, slot))
        return teams, slot
    url=READS.format(season=season,lid=lid)+"?view=mTeam&view=mSettings&view=mDraftDetail"
    try:
        d=requests.get(url,cookies=COOKIES,headers=HEADERS,timeout=8).json()
        if isinstance(d,list): d=d[0]
        n=teams or len(d.get('teams') or []) or 12
        # doc 125. ESPN PUBLISHES THE DRAFT ORDER. `settings.draftSettings.pickOrder` is a list
        # of teamIds in slot order and it is present BEFORE pick 1 -- it was in the very first
        # payload this tool ever captured. Slot detection was reading it out of the picks that had
        # already happened, which is why it could not work in an empty room and why --slot had to
        # be typed by hand. It also means a WRONG --slot can now be caught instead of trusted:
        # a wrong slot silently mis-plans every turn of the night.
        order=((d.get('settings') or {}).get('draftSettings') or {}).get('pickOrder') or []
        s_true=None
        if team_id in order:
            s_true=order.index(team_id)+1
            if slot is None:
                print(f"  draft order from ESPN: your slot is {s_true} of {len(order)}")
            elif slot != s_true:
                raise SystemExit(
                    f"  SLOT MISMATCH -- you passed --slot {slot}, ESPN's pickOrder says team "
                    f"{team_id} drafts at slot {s_true}.\n"
                    f"  Order: {order}\n"
                    f"  A wrong slot mis-plans every turn of the night and nothing else would say\n"
                    f"  so. Drop --slot and let it read the order, or fix the number.")
        s=slot or s_true
        if s is None:
            picks=(d.get('draftDetail') or {}).get('picks') or []
            first={}
            for p in sorted(picks,key=lambda z:z.get('overallPickNumber',0)):
                first.setdefault(p.get('teamId'), p.get('overallPickNumber'))
            s=first.get(team_id)
            if s and s>n: s=None
        if s is None:
            # doc 80: this used to silently return slot 1 here and slot 8 from the
            # except branch -- two different guesses for the same unknown, neither
            # announced. A mock room before pick 1 has no picks, so the NORMAL case
            # was the silent one: MY_PICKS computed for slot 1, every survival number
            # wrong, one unchallenged line of output as the only tell. Mocks exist to
            # build reflexes; the wrong slot builds the wrong ones.
            raise SystemExit(
                f"  CANNOT DETECT YOUR SLOT in league {lid} (team {team_id}: "
                f"{len(picks)} picks in the feed, {n} teams).\n"
                f"  ESPN does not expose draft order until the room starts picking.\n"
                f"  Re-run with it explicitly:  py live_draft.py --mock --league {lid} "
                f"--slot N --teams {n}\n"
                f"  Your slot is the position shown in the mock room's draft order.")
        return n, s
    except SystemExit: raise
    except Exception as e:
        raise SystemExit(
            f"  SHAPE DETECTION FAILED ({e}).\n"
            f"  Pass both explicitly:  py live_draft.py --mock --league {lid} "
            f"--slot N --teams N\n"
            f"  (This path is mock-only -- the real draft never calls it.)")

# doc 212: THESE TWO PAGES USED TO ORDER BY ESPN'S SEASON PROJECTION, WHICH HAS NO SCHEDULE
# IN IT. Measured on 2,718 team-weeks under this league's own D/ST rules: who a defence PLAYS
# explains 15.6 per cent of its week, who it IS explains 9.4. Across the 32 defences the spread
# over the FIRST FOUR WEEKS is 11.7 points; over week 1 alone it is only 3.6 -- so the useful
# horizon is the opening month, not the opener, and drafting it is what keeps Matt off the wire
# in week 2. Kickers get the same table for symmetry, but their four-week spread is 6.3 and
# five sixths of a kicker week is noise: the ordering is nearly free there, and the page says so.
# ---------------------------------------------------------------------------
# doc 216.  Matt, during the Sept-7 practice draft: "i couldn't tell in either the espn
# window or in the live draft board if he was available or taken. If available he was too
# far down the page."  The board shows twelve rows.  A name he is holding in his head for
# a LATER turn -- Burden at 56, Godwin at 104 -- is invisible until it climbs into those
# twelve, and by then the question has already been answered for him.
#
# This strip answers one question and no others: IS HE STILL THERE.  No value, no advice,
# no ordering -- those are the board's job and duplicating them here would invite reading
# this instead of the board.
#
# FIXED CONTENT, FIXED HEIGHT (§7): the same thirty names every refresh, so the page never
# changes shape underneath him.  Groups for turns already past go dim; nothing is removed.
#
# SAFETY: render_watch() can never take the page down.  Every path is inside one try, and
# the failure return is an empty string -- a missing strip, not a missing board.
# A name that is not on the board renders as a visible grey "?" rather than vanishing,
# which is the §0.5(c)5 missing-row defect this very session found in the D/ST page.
# All thirty were verified against board_v8_fixed.csv before shipping.
WATCH = [
    ('17',      ['Kenneth Walker III', 'Chase Brown', 'Breece Hall',
                 'Brock Bowers', 'Trey McBride', 'Malik Nabers']),
    ('32-41',   ['Kyren Williams', 'Quinshon Judkins', 'Lamar Jackson',
                 'Jaylen Waddle', 'Tee Higgins', 'Ladd McConkey']),
    ('56-65',   ['Rome Odunze', 'Terry McLaurin', 'Luther Burden III',
                 'Matthew Stafford', 'TreVeyon Henderson', 'Marvin Harrison Jr.']),
    ('80-89',   ['Christian Watson', 'Brian Thomas Jr.', 'Parker Washington',
                 'Bucky Irving']),
    ('104-113', ['Chris Godwin Jr.', 'Josh Downs', 'Jared Goff', 'Mark Andrews']),
    ('128-137', ['Jayden Reed', 'Jordan Mason', 'Jacory Croskey-Merritt',
                 'Mike Washington Jr.']),
]


def render_watch(eng, pick_no):
    """One line per turn: green = still on the board, struck through = gone."""
    try:
        idx = {}
        for i, n in enumerate(eng.name):
            idx.setdefault(str(n), i)
        lines = []
        for label, names in WATCH:
            last = 0
            for part in label.split('-'):
                try: last = max(last, int(part))
                except ValueError: pass
            past = pick_no > last
            chips = []
            for n in names:
                i = idx.get(n)
                if i is None:
                    chips.append('<span style="color:#5a6270">%s&nbsp;?</span>' % html.escape(n))
                elif bool(eng.avail[i]):
                    chips.append('<b style="color:#5fd08a">%s</b>' % html.escape(n))
                else:
                    chips.append('<span style="color:#5a6270;text-decoration:line-through">'
                                 '%s</span>' % html.escape(n))
            lines.append(
                '<div style="margin:3px 0;opacity:%s"><span style="display:inline-block;'
                'min-width:62px;color:#98a0ae;font:700 10px/1.6 Chivo;letter-spacing:.08em">'
                '%s</span>%s</div>' % ('.45' if past else '1', html.escape(label),
                                       ' &middot; '.join(chips)))
        return ('<div class="panel" style="margin-top:12px"><h2>Still on the board?</h2>'
                '<div style="font:13px/1.5 system-ui,sans-serif">%s</div></div>'
                % ''.join(lines))
    except Exception:
        return ''


# DATA ONLY. A team not in the table keeps the old ordering and sorts last.
# BLAST RADIUS: picks 152 and 161. Nothing else calls render_streamer.
OPEN4 = {
 'D/ST': {'SEA':(1,25.8,'vs NE'), 'JAX':(2,23.9,'vs CLE'), 'PIT':(3,23.8,'vs ATL'), 'CHI':(4,23.1,'@ CAR'), 'TB':(5,23.0,'@ CIN'), 'HOU':(6,22.8,'vs BUF'), 'NO':(7,22.2,'@ DET'), 'LAC':(8,22.0,'vs ARI'), 'CLE':(9,22.0,'@ JAX'), 'MIA':(10,22.0,'@ LV'), 'GB':(11,21.8,'@ MIN'), 'PHI':(12,21.8,'vs WAS'), 'DET':(13,21.5,'vs NO'), 'ATL':(14,21.2,'@ PIT'), 'DEN':(15,21.2,'@ KC'), 'MIN':(16,21.1,'vs GB'), 'LA':(17,21.0,'vs SF'), 'KC':(18,20.9,'vs DEN'), 'LV':(19,20.7,'vs MIA'), 'BAL':(20,20.3,'@ IND'), 'NE':(21,20.1,'@ SEA'), 'CAR':(22,19.8,'vs CHI'), 'BUF':(23,19.1,'@ HOU'), 'IND':(24,18.7,'vs BAL'), 'TEN':(25,18.5,'vs NYJ'), 'SF':(26,18.1,'@ LA'), 'NYG':(27,18.1,'vs DAL'), 'ARI':(28,17.5,'@ LAC'), 'DAL':(29,16.0,'@ NYG'), 'WAS':(30,15.7,'@ PHI'), 'CIN':(31,15.3,'vs TB'), 'NYJ':(32,14.1,'@ TEN')},
 'K': {'HOU':(1,36.0,'vs BUF'), 'SEA':(2,35.1,'vs NE'), 'DAL':(3,34.2,'@ NYG'), 'CHI':(4,33.8,'@ CAR'), 'LAC':(5,33.6,'vs ARI'), 'SF':(6,33.2,'@ LA'), 'MIN':(7,33.1,'vs GB'), 'IND':(8,33.1,'vs BAL'), 'BAL':(9,32.7,'@ IND'), 'JAX':(10,32.7,'vs CLE'), 'KC':(11,32.5,'vs DEN'), 'DET':(12,32.5,'vs NO'), 'ATL':(13,32.5,'@ PIT'), 'TB':(14,32.5,'@ CIN'), 'TEN':(15,32.1,'vs NYJ'), 'PIT':(16,31.9,'vs ATL'), 'MIA':(17,31.9,'@ LV'), 'GB':(18,31.7,'@ MIN'), 'NYJ':(19,31.7,'@ TEN'), 'NO':(20,31.6,'@ DET'), 'NE':(21,31.6,'@ SEA'), 'LA':(22,31.5,'vs SF'), 'CIN':(23,31.2,'vs TB'), 'WAS':(24,31.1,'@ PHI'), 'DEN':(25,30.7,'@ KC'), 'NYG':(26,30.6,'vs DAL'), 'ARI':(27,30.5,'@ LAC'), 'LV':(28,30.4,'vs MIA'), 'CLE':(29,30.2,'@ JAX'), 'PHI':(30,30.1,'vs WAS'), 'CAR':(31,29.9,'vs CHI'), 'BUF':(32,29.7,'@ HOU')},
}
_TEAMFIX = {'LAR': 'LA', 'LA': 'LA', 'WSH': 'WAS', 'JAC': 'JAX'}


def _open4(pos, team):
    t = _TEAMFIX.get(str(team).upper(), str(team).upper())
    return OPEN4.get(pos, {}).get(t)


SHOW_STREAMERS = 6

def render_streamer(eng, pick_no, pos, top):
    # order by the opening month, not by the season projection, THEN cut to six.
    # doc 215: cutting first was the defect -- the Jaguars are 22nd of 32 by ESPN's
    # season projection and 2nd by the opening month, so the six best projections
    # never contained the row the recommendation names, at any depletion level.
    top = sorted(top, key=lambda t: (_open4(pos, t.get('team')) or (99, 0, ''))[0])
    top = top[:SHOW_STREAMERS]
    cells=[]
    for t in top:
        o=_open4(pos, t.get('team'))
        rk = ('<b style="color:#f0a91b;font-size:17px">' + str(o[0]) + '</b>') if o \
             else '<span style="color:#5a6270">-</span>'
        nx = o[2] if o else ''
        f4 = ('%.1f' % o[1]) if o else ''
        cells.append(f'<tr><td class="mono" style="text-align:center">{rk}</td>'
                     f'<td><b>{t["player"]}</b></td><td class="mono">{t["team"]}</td>'
                     f'<td class="mono">{int(t["bye"])}</td><td class="mono">{nx}</td>'
                     f'<td class="mono">{f4}</td><td class="mono">{t["proj"]}</td></tr>')
    rows=''.join(cells)
    best=top[0]['player'] if top else '—'
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta http-equiv="refresh" content="20">
<title>JUG live board</title><style>{CSS}</style></head><body><div class="wrap">
<h1>JUG live draft board</h1><div class="sub">pick {pick_no} — {pos} slot</div>
<div class="hero"><div class="sub">ON THE CLOCK — PICK {pick_no}</div>
<div class="pick">{best} <span class="pos {pos.replace("/","")}">{pos}</span></div>
<div class="why">You stream this position all season, so this pick is only worth the first
few weeks. Take the lowest number in the table and move on.</div></div>
<div class="panel"><h2>Best {pos} remaining — take the lowest number</h2><table>
<tr><th>#</th><th>name</th><th>tm</th><th>bye</th><th>week 1</th><th>first 4 wks</th>
<th>season</th></tr>{rows}</table>
<p class="sub" style="margin-top:8px">The amber number ranks all 32 by their FIRST FOUR WEEKS,
not by the season column. Who a defence plays decides more of its week than who it is, and the
season projection has no schedule in it.</p></div>{CARD_JS}{HOLD_JS}</div></body></html>"""

def render_done(eng):
    ros=''.join(f'<tr><td><span class="pos {eng.pos[i]}">{eng.pos[i]}</span></td><td>{eng.name[i]}</td>'
                f'<td class="mono">bye {int(eng.bye[i])}</td></tr>' for i in eng.mine)
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>JUG live board</title>
<style>{CSS}</style></head><body><div class="wrap"><h1>Draft complete</h1>
<div class="panel"><table>{ros}</table></div></div></body></html>"""

def render_waiting(season, lid, team):
    """doc 95 TRAP 5. Shown for the ~3 seconds before the first poll lands, and for as long
    as ESPN keeps refusing. It must be impossible to mistake for a board -- the failure this
    replaces is a stale REPLAY page sitting there looking authoritative."""
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>JUG live board</title>
<meta http-equiv="refresh" content="4">
<style>{CSS}</style></head><body><div class="wrap">
<h1 style="color:#e0a93b">Waiting for ESPN&nbsp;&hellip;</h1>
<div class="panel" style="border-left:4px solid #e0a93b">
<p style="font-size:17px;margin:2px 0 14px">No picks have been read yet. <b>Nothing on this
page is a recommendation.</b></p>
<p style="margin:2px 0">This page refreshes itself every 4 seconds and will fill in on its own
the moment the first pick arrives.</p>
<p style="margin:14px 0 2px;color:#8a929e">league {lid} &middot; season {season} &middot; team {team}</p>
<p style="margin:2px 0;color:#8a929e">If it still says this after a minute, look at the black
command window &mdash; it is printing the reason.</p>
</div></div></body></html>"""

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--replay',type=int,help='dry run against a finished season')
    ap.add_argument('--league',type=int,default=LEAGUE_ID)
    ap.add_argument('--team',type=int,default=MY_TEAM_ID)
    ap.add_argument('--interval',type=float,default=None)
    ap.add_argument('--speed',type=float,default=1.0,help='replay: seconds per pick')
    ap.add_argument('--mock',action='store_true',help='ESPN mock: no keepers, auto-detect shape')
    ap.add_argument('--url', help='paste the ESPN draft-room URL IN QUOTES; leagueId, seasonId '
                                  'and teamId are read out of it')
    ap.add_argument('--watch',action='store_true',
                    help='poll a draft and print picks as they land -- no board, no advice')
    ap.add_argument('--bridge',nargs='?',const='bridge_picks.json',
                    help='read picks from the Chrome-extension bridge file instead of ESPN '
                         '(doc 137). Optional path; defaults to bridge_picks.json.')
    ap.add_argument('--probe',action='store_true',
                    help='print exactly what ESPN is serving for this league, then exit')
    ap.add_argument('--slot',type=int,help='your draft slot (mocks: auto-detected if omitted)')
    ap.add_argument('--teams',type=int,help='league size (auto-detected if omitted)')
    ap.add_argument('--rounds',type=int,default=14)
    # doc 96: the ONLY hook the rehearsal harness needs. Default is unchanged, so nothing on
    # the draft-night path can reach this. When it IS set the banner below makes that
    # impossible to miss -- a tool pointed at a fake feed must never look like the real one.
    ap.add_argument('--reads',help=argparse.SUPPRESS)
    a=ap.parse_args()
    # doc 139.  3s was set for an ESPN HTTP poll, where the interval is politeness.  In bridge
    # mode the "poll" is a 20 KB local file read costing microseconds, and Matt's mock ran the
    # clock forward two picks between refreshes with the board visibly lagging the room.  Poll
    # fast when it is free; keep 3s when it is a request to ESPN.
    if a.interval is None:
        a.interval = 0.5 if a.bridge else 3.0
    if a.url:
        # PowerShell: the URL MUST be quoted -- & splits the command and {} is a script block.
        _u = parse_draft_url(a.url)
        a.league = _u['league']
        if _u['team']:   a.team = _u['team']
        if _u['season']: a.replay = a.replay or None   # season stays SEASON unless --replay says so
        if _u['season'] and _u['season'] != SEASON:
            print(f"  NOTE: that URL is season {_u['season']} but this tool is built for {SEASON}.")
    # doc 137: --bridge must take effect BEFORE any mode dispatches, for the same reason --reads
    # does (doc 127) -- otherwise a mode calls the real ESPN while the operator believes it is
    # reading the browser bridge.  That exact defect has already happened once in this file.
    if a.bridge:
        global BRIDGE_FILE
        BRIDGE_FILE = a.bridge if os.path.isabs(a.bridge) else os.path.join(HERE, a.bridge)
        print("  " + "="*68)
        print("  BRIDGE MODE -- picks come from the Chrome extension, not from ESPN.")
        print(f"  reading {BRIDGE_FILE}")
        if not os.path.exists(BRIDGE_FILE):
            print("  (file not there yet -- start bridge_server.py and open the draft room)")
        print("  " + "="*68)
    if a.reads:
        print("  " + "!"*68)
        print("  REHEARSAL: reading from a FAKE local feed, not ESPN.")
        print(f"  {a.reads}")
        print("  The pick order is synthetic. THE RECOMMENDATIONS ARE NOT STRATEGY.")
        print("  " + "!"*68)
    # doc 118: --probe answers "what is ESPN actually serving" and exits. It runs BEFORE the
    # board loads, so it still works when the board or the context file is the broken thing.
    # doc 127: --reads has to take effect BEFORE --probe and --watch, or those two modes call
    # the real ESPN while the operator believes they are pointed at a test feed. Found by the
    # watch mode's own first run doing exactly that.
    if a.reads:
        global READS, REHEARSAL
        READS = a.reads
        REHEARSAL = True

    if a.probe:
        probe(a.replay or SEASON, a.league, a.team)
        return
    if a.watch:
        try:
            watch(a.replay or SEASON, a.league, a.team, a.interval)
        except KeyboardInterrupt:
            print("\n  stopped. Nothing was written to ESPN.")
        return

    # doc 60: defaulted to board_v7_2026.csv, which lacks espn_id (forcing the J1 name join)
    # and carries the pre-fix eff_pick. board_v8_fixed.csv is the shipped board.
    _board = os.path.join(HERE, 'board_v8_fixed.csv')
    if not os.path.exists(_board):
        raise SystemExit(f"board_v8_fixed.csv not found in {HERE} -- see the FOLDER CONTRACT "
                         f"at the top of this file. Do NOT fall back to an older board.")
    eng=Engine(_board,
               os.path.join(HERE,'ESPN_prerank_with_ids.csv'))
    load_context()
    season = a.replay or SEASON
    if a.mock or a.slot or a.teams:
        teams, slot = detect_shape(season, a.league, a.team, a.teams, a.slot)
        CLE.configure(slot, teams, a.rounds, dst_round=a.rounds-1, k_round=a.rounds)
        print(f"  shape: {teams} teams, slot {slot}, {a.rounds} rounds -> your picks {CLE.MY_PICKS}")
        if a.mock:
            KEEPER_ROWS[0] = False        # doc 149 finding 4: a mock has no keeper rows to find
            print("  mock mode: keeper ROW detection off as well as keeper depletion")
            eng.adp_opp = eng.b.adp_pick.values.astype(float) + \
                          (eng.pos=='TE')*CLE.TE_SHIFT      # mocks have no keepers
            eng.adp     = eng.b.adp_pick.values.astype(float)
            print("  mock mode: keeper depletion removed, raw ADP in use")
    else:
        # doc 125. The REAL draft never called detect_shape -- slot 8 is compiled in. But ESPN
        # publishes `pickOrder` before pick 1, so the compiled slot can be CHECKED for free, and
        # a wrong slot is the one error that would corrupt every turn of the night in silence.
        # Draft order can change (reverse standings), so this is not a formality.
        verify_slot(season, a.league, a.team)
    print(f"[{dt.datetime.now():%H:%M:%S}] league {a.league} season {season} team {a.team}")
    confirm_team(season, a.league, a.team)

    if a.replay:
        print("  " + "="*68)
        print("  REPLAY: THIS YEAR'S BOARD AGAINST LAST YEAR'S PICK ORDER.")
        print("  It is a plumbing test of the feed, the keeper filter and the render path.")
        print("  The RECOMMENDATIONS ARE NOT STRATEGY -- 2026 players and 2026 values are")
        print("  being scored against a %d draft. Ignore them." % season)
        print("  " + "="*68)
        picks,_,_ = fetch_picks(season, a.league)
        nk=sum(1 for p in picks if p.get('keeper'))
        unmapped=[p for p in picks if int(p['pid']) not in eng.by_eid]
        print(f"  replay: {len(picks)} rows fetched ({nk} flagged keeper). "
              f"unmapped player ids: {len(unmapped)}")
        if len(picks)!=180 or nk!=12:
            print(f"  !! EXPECTED 180 rows and 12 keeper rows. Got {len(picks)} and {nk}.")
            print(f"  !! On the real draft this would put the pick counter out by {12-nk}.")
        # doc 84: 'draft complete shows 11 players and no QB' -- the roster panel can only
        # show players who are on THIS year's board, so a K, a D/ST, a 2026 keeper or anyone
        # outside the 480 silently vanishes. Say so instead of leaving it to be discovered.
        mine_rows=[p for p in picks if p['team']==a.team]
        shown   =[p for p in mine_rows if int(p['pid']) in eng.by_eid]
        dropped =[p for p in mine_rows if int(p['pid']) not in eng.by_eid]
        print(f"\n  your team ({a.team}): {len(mine_rows)} rows in the {season} feed, "
              f"{len(shown)} will appear on the 'Draft complete' panel.")
        for p in dropped:
            print(f"    not shown: playerId {p['pid']}  round {p['round']}  keeper={p['keeper']}"
                  f"  -- not on board_v8_fixed.csv (a K, a D/ST, a {SEASON} keeper, or outside the 480)")
        print(f"    NOTE: your {SEASON} keeper is carried in the lineup MATH as an extra slot and is")
        print(f"    never listed on that panel, in a replay or on draft night.\n")
        for n in range(len(picks)+1):
            step(eng, picks[:n], a.team); time.sleep(a.speed)
        print("  replay complete ->", OUT)
        print("  Nothing was written to ESPN. Ctrl+C is safe at any point; just close the tab.")
        return

    # doc 95 TRAP 5: the browser opens BEFORE the first poll, and live_board.html on disk is
    # whatever the LAST run left there -- after a --replay that is a finished 2025 board. If
    # the first fetch 401s, that stale board is what stays on screen all night, and it looks
    # entirely plausible. Overwrite it with an unmistakable placeholder first.
    write_page(render_waiting(season, a.league, a.team))

    # doc 95 TRAP 6: 'file://' + a Windows path is NOT a valid URI -- backslashes and the
    # space in "My Drive" both break it, and this line has never run on Matt's machine
    # (--replay returns above it). Path.as_uri() produces file:///G:/My%20Drive/...
    print("  " + "="*68)
    print("  THE BOARD PAGE IS AT:")
    print(f"    {OUT}")
    print("  It opens by itself. If it ever says the file cannot be accessed, press F5 --")
    print("  do NOT restart anything. Bookmark it once and the bookmark keeps working.")
    print("  " + "="*68)
    try:
        webbrowser.open(pathlib.Path(OUT).as_uri())
    except Exception as e:
        print(f"  (could not open a browser: {e})")
        print(f"  Open this yourself:  {OUT}")

    # doc 95: step() used to sit OUTSIDE the try. Any exception inside it -- a render bug,
    # an odd row in the feed, a locked file -- ended the poller at whatever pick it happened
    # on, with no restart. A crash at pick 41 would have cost the night. Nothing in this loop
    # is now allowed to be fatal except Ctrl+C.
    # doc 118. `done` on the very first poll is not a finished draft, it is the WRONG FEED --
    # a prior season's completed draft served under this id, or the wrong league entirely. The
    # tool used to render "Draft complete" and exit, which reads as a successful run.
    first_poll = True; bogus_complete = False; kept_ok = False; kept_err = False
    polls = 0; grid_total = 0
    _feed_warn = ''   # doc 148: bound before the loop so a first-poll failure cannot NameError
    _warn_flip = False
    _warned_page = [False]   # doc 149 finding 1: what the PAGE currently says, not what we know
    last=-1; fails=0
    while True:
        try:
            picks, done, _dd = fetch_picks(season, a.league)
            # doc 148, finding 2.  `updated` was returned by _bridge_picks and consumed by
            # nothing.  A feed that simply STOPS -- the Chrome tab closed, hook.js detached,
            # the socket dropped -- kept rendering a normal board one pick-count behind reality,
            # forever, with nothing on screen to say so.  The page's own "updated" line is the
            # RENDER time, which keeps ticking, so both went stale together.
            _age = (_dd or {}).get('age') or 0
            _feed_warn = ''
            # doc 149, finding 8.  90s is inside one ESPN pick clock -- a manager who lets it run
            # out, or a brief pause, would have tripped this.  180s cannot be a single pick.
            if BRIDGE_FILE and _SAW_PICKS[0] and _age > 180:
                _feed_warn = (f'THE BRIDGE HAS NOT RECEIVED A PICK IN {_age/60:.1f} MINUTES. '
                              'This board may be behind the room. Check the listener window and '
                              'that the draft room tab is still open in Chrome.')
                if polls % 40 == 1:
                    print(f"  !! {_feed_warn}")
            polls += 1          # doc 139: this was NEVER incremented, so the every-40-polls
                                # evidence snapshot below has never once run.  s0.2: a guard
                                # that has never executed is not a guard.
            grid_total = len(_dd.get('picks') or []) if _dd else 0
        except KeyboardInterrupt:
            raise
        except Exception as e:
            fails += 1
            msg = str(e)
            if not kept_err:
                kept_err = True
                body = ''
                try: body = e.response.text if getattr(e, 'response', None) is not None else ''
                except Exception: pass
                keep_evidence('pollfail', a.league, season, 'err', f"{msg}\n\n{body}")
            hint = ""
            if '404' in msg:
                hint = ("\n     ^^ 404 = ESPN will not serve this league for this season.\n"
                        "        Most likely COOKIES (a private league can 404 instead of 401):\n"
                        "        in ANOTHER window  py cookie_jar.py  then Ctrl+C here and re-run.\n"
                        "        Otherwise the league id is wrong for this season -- an ESPN MOCK\n"
                        "        has its OWN league id and your real one will never show it.\n"
                        "        Diagnose it:  py live_draft.py --probe --league <id>")
            elif '401' in msg or '403' in msg:
                hint = ("\n     ^^ COOKIES EXPIRED. In ANOTHER window:  py cookie_jar.py\n"
                        "        then Ctrl+C HERE and run  py live_draft.py  again -- this\n"
                        "        window is still holding the old ones. Restarting is safe:\n"
                        "        it re-reads every pick from ESPN, it remembers nothing.")
            print(f"  poll error ({fails} in a row): {e}{hint}")
            if fails == 5:
                print("  !! Five failures running. The board on screen is FROZEN at the last")
                print("     good state -- do not trust it. Use the printed fallback board.")
            try:
                time.sleep(a.interval)
            except KeyboardInterrupt:
                print("\n  stopped. Nothing was written to ESPN."); return
            continue
        fails = 0

        # doc 125: the FIRST poll alone could not answer "did picks ever appear". Snapshot again
        # every 40 polls so a feed that goes quiet mid-draft is evidence, not a memory.
        # doc 139: these snapshots hit ESPN over the network.  In bridge mode ESPN is not the
        # source, the poll runs 6x faster, and an 8-second timeout inside the loop is the
        # single worst thing that can happen to board latency.  Skip them entirely.
        if not BRIDGE_FILE and kept_ok and polls and polls % 40 == 0:
            try:
                _u = READS.format(season=season, lid=a.league) + "?view=mDraftDetail"
                keep_evidence(f'poll{polls}', a.league, season, 200,
                              requests.get(_u, cookies=COOKIES, headers=HEADERS, timeout=8).text)
            except Exception:
                pass
        if not kept_ok and not BRIDGE_FILE:
            kept_ok = True
            try:
                _u = READS.format(season=season, lid=a.league) + "?view=mDraftDetail&view=mTeam"
                keep_evidence('firstok', a.league, season, 200,
                              requests.get(_u, cookies=COOKIES, headers=HEADERS, timeout=8).text)
            except Exception as _e:
                print(f"  (evidence snapshot skipped: {_e})")
        # doc 148, finding 4.  Hold the "waiting" page until a pick has actually been read.
        # Once ANY pick has arrived, an empty read is a different problem (a reset file), and
        # the LOST PICKS guard above owns that -- so this latch only ever gates the start.
        # doc 149, finding 1.  The banner was gated behind `len(picks)!=last`, and a stalled feed
        # is BY DEFINITION one whose pick count stops changing -- so it rendered only when the
        # feed was demonstrably alive and never when it had stopped.  Measured: 30 polls at a
        # frozen count with the age climbing to 39 minutes produced zero pages carrying it.
        # Render once on the transition into a stall, and once on the way out.
        _warn_now = bool(_feed_warn)
        _warn_flip = (_warn_now != _warned_page[0])
        _warned_page[0] = _warn_now
        if picks:
            _SAW_PICKS[0] = True
        elif _SAW_PICKS[0]:
            # doc 149, finding 7.  The latch only guarded the START.  Once any pick had been seen,
            # an empty read fell straight through to step() and rendered the finding-4 pick-1 page
            # in the MIDDLE of the draft.  On the bridge path _BRIDGE_LAST already holds the last
            # complete set, so this only ever fires on the ESPN path -- which has no equivalent.
            if polls % 20 == 1:
                print(f"[{dt.datetime.now():%H:%M:%S}] the feed just came back EMPTY mid-draft "
                      f"({last} picks were in). Holding the last board; not re-rendering.")
            time.sleep(a.interval)
            continue
        else:
            if polls % 20 == 1:
                print(f"[{dt.datetime.now():%H:%M:%S}] no picks read yet -- NOT rendering a "
                      "board." + ("  Is bridge_server.py running, and is the draft room open "
                                  "in the Chrome that has the extension loaded?" if BRIDGE_FILE
                                  else "  Waiting for ESPN."))
            write_page(render_waiting(season, a.league, a.team))
            time.sleep(a.interval)
            continue
        if len(picks)!=last or _warn_flip:
            try:
                step(eng, picks, a.team, feed_warn=_feed_warn)
                last=len(picks)
            except KeyboardInterrupt:
                raise
            except Exception as e:
                # deliberately do NOT advance `last`: the next poll retries this same state
                print(f"  !! render error at {len(picks)} picks: {type(e).__name__}: {e}")
                print(f"     Polling continues and will retry. If this repeats every poll,")
                print(f"     the page is stuck -- use the printed fallback board.")
            nk=sum(1 for p in picks if p.get('keeper'))
            # doc 149, finding 9.  Directive 8 says "confirm the first poll line reports the
            # keeper-row count", and this line lives behind the pick-count gate -- so with the
            # new waiting latch it might not print until well after 7:55 PM.  Say it explicitly,
            # once, the first time any picks are read, INCLUDING when the answer is zero.
            if not _KEEPER_SAID[0]:
                _KEEPER_SAID[0] = True
                print(f"  KEEPER ROWS IN THE FEED: {nk}  "
                      + ("(12 expected for this league)" if KEEPER_ROWS[0] else "(mock: none expected)"))
                if nk == 0 and KEEPER_ROWS[0]:
                    print("     0 is usually fine -- ESPN often does not expose keepers until")
                    print("     picking starts, and they are already off the board file. The real")
                    print("     tell is the pick number running 12 ahead of ESPN's once it does.")
            print(f"[{dt.datetime.now():%H:%M:%S}] {len(picks)-nk} real picks in"
                  + (f"  (+{nk} keeper rows ignored)" if nk else ""))
        if done and first_poll and len(picks) > 24:
            print("\n  !! THIS FEED IS ALREADY A COMPLETE DRAFT ON THE FIRST POLL.")
            print("     That is never a valid start state -- it means the wrong league id, or")
            print("     ESPN serving a prior season's draft under this one. NOT rendering a")
            print("     'Draft complete' page, because that looks like a successful run.")
            print(f"     Diagnose it:  py live_draft.py --probe --league {a.league}")
            print("     Rehearse without ESPN at all:  py rehearsal.py --realtime")
            print("     STILL POLLING -- if the feed flips to a live draft this picks it up.")
            print("     Exiting here would be the worse mistake on Sept 7: a tool that quits")
            print("     because ESPN served something odd once is a tool that is not there.")
            bogus_complete = True
        first_poll = False
        # Once the guard has fired, `done` is not trustworthy for THIS feed, so it never ends
        # the run again -- the poller stays up and Ctrl+C is the way out.
        # doc 125: `drafted` did not flip on Matt's mock and the poller ran forever after the
        # room finished. A grid with every slot filled is a finished draft whatever the flag says.
        if grid_total and len(picks) >= grid_total and not bogus_complete:
            print(f"  every one of {grid_total} slots is filled -- draft complete.")
            break
        if done and not bogus_complete:
            print("  draft complete"); break
        if done and bogus_complete:
            time.sleep(a.interval); continue
        time.sleep(a.interval)

def step(eng, picks, my_team, feed_warn=''):
    # J/B-chunk fix (doc 58): ESPN carries this league's 12 keepers INSIDE draftDetail.picks,
    # at overall 169-180 (verified on the 2024 and 2025 drafts). They are roster facts, not
    # selections. Counting them put pick_no 12 too high, so `on_clock` never fired at pick 8.
    # Keepers still mark players TAKEN -- they just do not advance the clock.
    real = [p for p in picks if not p.get('keeper')]
    ids  = [p['pid'] for p in picks]                       # everyone off the board
    mine = [p['pid'] for p in picks if p['team']==my_team]  # incl. my own keeper
    eng.set_taken(ids, mine)
    pick_no=len(real)+1
    if pick_no in (CLE.DST_PICK, CLE.K_PICK):
        pos = 'D/ST' if pick_no==CLE.DST_PICK else 'K'
        # doc 215: ask for EVERY available streamer, not the six best by SEASON
        # projection. render_streamer orders by the opening month and cuts to six --
        # so the six SHOWN must be chosen after that sort, not before it.
        top = eng.streamers(pos, [p['pid'] for p in picks], n=32)
        write_page(render_streamer(eng, pick_no, pos, top)); return
    if pick_no > 168:
        # doc 123. A guard on the branch the bug came out of. "The draft is over" is only true if
        # players were actually selected; 180 empty slots must never reach this page again. The
        # filter in fetch_picks is the fix -- this is the check that it stayed fixed.
        if not ids:
            print("  !! 'draft complete' reached with ZERO players selected. That is the doc 123")
            print("     empty-slot defect, not a finished draft. NOT rendering it; still polling.")
            return
        write_page(render_done(eng)); return
    on_clock = pick_no in CLE.MY_PICKS
    # doc 148, finding 13.  MY_PICKS ends at 137, so from pick 138 on this fell through to
    # MY_PICKS[-1] and the board planned for a turn ALREADY TAKEN: survival came back all-ones,
    # every row read "100% still there", cliffs came back empty, and the footer said "your picks
    # done" while 152 and 161 were still to come.  The two remaining turns are real picks.
    _turns = list(CLE.MY_PICKS) + [CLE.DST_PICK, CLE.K_PICK]
    ref = pick_no if on_clock else next((p for p in _turns if p >= pick_no), CLE.K_PICK)
    # doc 139.  `top` WAS 10 ON THE CLOCK AND 8 WHILE WAITING -- that, not the tier lines, is
    # the main reason Matt saw the board change height: it lost two rows every time it was not
    # his pick and grew them back on his turn.  A constant 12 costs nothing now that _lineup is
    # ~10x faster (pick 8 on the clock: 19.9s -> 1.9s at top=12, measured in bench_lineup.py),
    # so the board is the same shape all night AND arrives sooner than the old short one did.
    # doc 139, MEASURED (not assumed): rollout_inner is a Monte-Carlo sample count, and 24 was
    # chosen when a run cost 16 seconds.  Re-run 10x per pick under different seeds:
    #   pick  8  inner 24 -> 10/10 same #1 (St. Brown), margin 19.96 +-0.55
    #   pick 32  inner 24 ->  7/10, THREE different winners, margin 0.31 +-0.35
    #            inner 60 ->  9/10, margin 0.15 +-0.07
    #            inner 150-> 10/10, margin 0.15 +-0.07
    #   pick 56  inner 24 -> 10/10, margin 2.77 +-0.18
    # So 24 was fine everywhere EXCEPT pick 32 -- the longest-gap turn -- and it also
    # OVERSTATES the margin (max of noisy estimates: 0.31 shrinks to 0.15, 19.96 grows to
    # 20.20).  60 costs 4.0s against 1.7s and is still 4x faster than the 16s this used to
    # take.  NOTE WHAT THIS DOES NOT DO: it does not break the pick-32 tie.  The margin
    # CONVERGES to 0.15 points -- that turn is a genuine coin flip between two players and
    # more samples only make the engine more consistent about saying so.
    recs=eng.recommend(ref, rollout_inner=(60 if on_clock else 8), top=12)
    cl=eng.cliffs(ref)
    recent=[eng.by_eid[int(p['pid'])] for p in real[-18:] if int(p['pid']) in eng.by_eid]
    write_page(render(eng,pick_no,on_clock,recs,cl,recent,eng.mine, feed_warn))

if __name__=='__main__':
    # doc 139.  Ctrl+C is the DOCUMENTED way to stop this tool, and it dumped a KeyboardInterrupt
    # traceback -- twelve lines of red on the screen Matt is running the draft from.  A traceback
    # means "something broke"; nothing broke.  Every inner handler already prints the reassurance
    # that matters, so this one only has to stop the noise.
    try:
        main()
    except KeyboardInterrupt:
        print("\n  stopped. Nothing was written to ESPN.")
        try:
            sys.stdout.flush()
        except Exception:
            pass
        sys.exit(0)
