# 137 — The bridge works. ESPN's draft protocol, decoded.

*2026-09-02. Matt: "does Google Chrome still let you make your own extensions? maybe I'm
overthinking this."* **He was not overthinking it. That question ended a week of chasing the wrong
source, and the live board now has a working pick feed five days before the draft.**

---

## 1. THE REASONING THAT SOLVED IT

Doc 136 established that ESPN's REST read replica publishes a draft only after it ends. The stuck
point was "then where do live picks live?" Matt supplied the answer from a completely different
direction: **he already runs a FantasyPros browser extension that shows the ESPN draft board live.**

An extension cannot see ESPN's servers. It can only see **the page**. Therefore the picks are in
the browser the entire time, and the whole API question was a dead end. **The correct move was to
stop asking ESPN's server and listen to the room.**

## 2. WHAT ESPN ACTUALLY SPEAKS

`wss://fantasydraft.espn.com/game-1/league-<id>/JOIN?...&8=KONA` — a dedicated draft socket,
separate from everything the project had been polling. It is **not JSON**. It is a line protocol:

| message | meaning |
|---|---|
| **`SELECTED <teamId> <playerId> <roundId>`** | **THE PICK.** 221 of them in a 12×16 practice draft. |
| `SELECTING <teamId> <clockMs>` | who is on the clock |
| `AUTOSUGGEST <playerId>` | ESPN's suggestion **for you** — not a pick |
| `CLOCK <n> <ms>` · `PONG` · `STATE <n>` · `JOINED <team> <swid>` · `AUTODRAFT <team> <bool>` | housekeeping |
| `INIT <base64>` | room config, decoded: big-endian int32s — league id ×7, clocks 180000/30000/25000/10000/2000, scoring doubles 0.65 / 1.1 / 0.4. **Not picks.** |

**221 picks recovered from a real capture.** The feed problem is solved.

## 3. THREE DEFECTS FOUND ON THE WAY, IN ORDER

**(a) The hook threw binary frames away.** v1.0 logged only a byte count for any non-string frame
and returned. That code path printed nothing, so *"ESPN sends binary"* and *"no picks arrived"*
looked **identical** in the console. Fixed: binary is decoded as UTF-8 and carried as base64
alongside.

**(b) The sampler keyed on the URL, so it only ever showed the first three frames of the entire
socket** — always handshake noise. 607 frames arrived and the operator saw PONG, CLOCK and INIT.
Fixed: sample **per verb**, and report every unknown verb with a live example.

**(c) Re-sent picks would have put the board 29 ahead of the room.** The capture holds **221
`SELECTED` messages for a 12×16 = 192-pick draft.** The socket reconnected three times and ESPN
**re-sent history on each reconnect**. Numbering picks by arrival order counted the 29 repeats as
new selections — which is exactly the doc 58 defect that made the live tool never fire, and it
would have looked perfectly healthy the whole time: a climbing counter and 221 picks "known".
**Fixed by keying on playerId** — a player can only be drafted once, so arrival order is not an
identity. It also settles doc 137 §5.2: ESPN *does* re-send on reconnect, so restarting the
listener mid-draft is now safe.

**(d) `AUTOSUGGEST` would have injected 205 phantom picks.** v1.3 auto-promoted any unknown verb
producing three distinct playerId-sized numbers — reasonable, and `AUTOSUGGEST` emitted **205
distinct player ids in one draft**. It would have promoted itself and poured ESPN's suggestions
onto the board as selections. **Caught only because the capture came from a real draft.**
Fixed two ways: an explicit noise list, and a structural rule — **a pick names both a team and a
player, so a verb with no team-sized argument can never be promoted.**

**All four were invisible in the console.** Each one produced output that looked like success:
silence that looked like "no picks yet", handshake frames that looked like "the only frames",
a climbing counter that looked like a working feed, and 425 picks that looked like more data.
**Every one of them was caught only by checking a number against something independent** — the
byte count, the verb list, 12×16=192, and 221≠425.

`ERROR_PATTERNS` classes: (a) a failure path that prints nothing and is therefore invisible;
(b) a diagnostic whose sampling key hides the thing it was built to find; (c) arrival order used
as an identity; (d) a heuristic that generalises from a property the target does not uniquely have.

## 4. WHAT SHIPPED

| file | role |
|---|---|
| `espn_bridge\` (5 files) | unpacked Chrome extension. Hooks WebSocket, fetch and XHR in the page and forwards frames to `127.0.0.1:8787`. **Parses nothing** — deliberately, so every guess lives in Python where it can be changed without an extension reload. |
| `bridge_server.py` | the listener. Speaks the line protocol, writes `bridge_picks.json`, logs everything raw. `--recon` shows verbs live; `--replay` re-reads a capture with no draft needed. |
| `live_draft.py --bridge` | reads `bridge_picks.json` instead of ESPN. **Engine, board, recommendations and render are untouched — only the pipe changed.** |

Verified by execution: four synthetic message shapes, then the real protocol, then the live
`--watch` loop against a file being appended to (picks appeared at 6 / 3 / 3 second intervals and
`4429795` resolved to Jahmyr Gibbs). The empty-slot trap (`playerId -1`, doc 123) and the D/ST
trap (`-16000 − proTeamId`) both still behave correctly through the new path.

## 5. WHAT IS STILL UNTESTED

1. **The full board has never run off the bridge during a live draft.** Every part has been
   exercised, but not end to end at once. One practice draft with `py live_draft.py --bridge`
   closes it, and that is the last thing worth doing before Sunday.
2. ~~**Restarting `bridge_server.py` mid-draft** loses `STATE` and renumbers picks from 1.~~
   **RESOLVED, and it was the source of defect (c) above.** ESPN re-sends pick history on every
   socket reconnect — that is what the 29 excess messages were. With v1.5's playerId dedupe, a
   restart is idempotent: the re-sent history rebuilds `STATE` and repeats are discarded.
3. **`SELECTED` carries no overall pick number**, so overall is assigned by arrival order. Correct
   in every observation so far; would break if ESPN ever sent picks out of order.

## Assumptions

1. **One protocol capture, one practice draft.** The verb table is complete for that draft; a
   keeper league might add a verb, and the unknown-verb reporter would surface it immediately.
2. **The extension must be loaded and the listener running before the room opens**, or the
   pre-draft handshake is missed.
3. **This is Chrome-specific** and depends on Google continuing to allow unpacked extensions.
