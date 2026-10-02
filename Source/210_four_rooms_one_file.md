# 210 — four practice rooms, one pick file

**2026-09-07, 11:10–11:26 ET.** Matt ran the practice draft, saw the board disagree with the room,
saw McCaffrey missing from his roster, and saw the page go ERR_FILE_NOT_FOUND. He asked me to read
the logs and warned that his false starts may have left something running.

**He was right about the cause and it is worse than orphaned processes: FOUR different ESPN
practice leagues fed ONE `bridge_picks.json` inside seventeen minutes.** Everything he saw follows
from that, and every number below is reproduced from `bridge_raw.jsonl`, not inferred.

---

## 1 — THE FOUR ROOMS

`ESPN GIVES A PRACTICE DRAFT A NEW LEAGUE ID EVERY SINGLE TIME.` From today's traffic:

| time | leagueId | what happened |
|---|---|---|
| 11:10:01 | **1239245449** | room 1 hooked. 5 picks, then abandoned |
| 11:17:31 | **1503346219** | room 2 hooked. no picks |
| **11:19:35.152** | **762726020** | room 3 hooked — **and immediately replayed 7 SELECTED lines of its own history** |
| 11:19:35.563 | **621412010** | room 4 — the one he actually drafted in |

`bridge_server.py` had started at **11:19:35.052**, 100 ms before room 3 was hooked. So its reset
did clear room 1, and then room 3's join-replay landed in the fresh file, 400 ms before room 4
opened. **The seven poison rows are room 3's.**

---

## 2 — WHY McCAFFREY WAS ON ESPN'S ROSTER AND NOT ON THE BOARD'S

`bridge_server.py` v1.5 dedupes **by player id, first write wins** — deliberately, and the comment
says why: on a socket reconnect ESPN re-sends history, and numbering by arrival put the board 29
picks ahead on the 09-02 capture. **A player can only be drafted once, so playerId is the identity.**
That is correct for one room and wrong across two.

```
11:19:35.152   SELECTED 5 3117251 …     room 3   -> McCaffrey recorded to TEAM 5
11:20:39.482   SELECTED 9 3117251 …     room 4   -> Matt's real pick, DROPPED as a duplicate
```

`bridge_picks.json` still says **McCaffrey belongs to team 5.** Matt is team 9. The board was right
about what it had been told and the file was wrong. Nothing anywhere printed a word about it.

---

## 3 — THE PICK COUNTER, REPRODUCED TO THE PICK

The board read **ON THE CLOCK 37** while ESPN read **PICK 39**. Replaying the server's own dedupe
over today's raw stream from its 11:19:35 session start:

```
picks the board held at 11:21:26 : 36  -> next pick 37     (board)
ESPN said                        : PICK 39
phantom rows from the dead room still counted : 7
```

Seven phantoms in, nine of room 4's genuine picks dropped as duplicates of them — net two behind.
**Exact reproduction, so the mechanism is not a guess.**

---

## 4 — GEORGE PICKENS WAS NOT A DEFECT

He is on the ESPN practice roster in slot 4 with **no SELECTED message at all** — the practice room
pre-placed the keeper. And he is not on the board: `board_v8_fixed.csv` has the twelve keepers
removed by construction (§4.20). **Both sides are behaving correctly and they will never agree
about that one row.** Do not chase it tonight.

---

## 5 — AND THE FOURTH TOKEN IS NOT THE ROUND

`bridge_server.py` parses `SELECTED <team> <playerId> <n>` and calls `n` the **round**. It is the
**roster slot**, 1-based in ESPN's own slot order. Team 9's captured values were
2, 3, 7, 5, 1, 10, 11, 6, 12, 13, 14, 15, 8, 9 — not chronological, and they line up exactly with
his roster panel: 1 QB Burrow · 2 RB McCaffrey · 3 RB Walker · **4 WR Pickens (never sent)** ·
5 WR Adams · 6 TE Goedert · 7 FLEX Kyren · 8 D/ST · 9 K · 10+ bench.

It looks like a round because 12 teams × 15 slots gives ~12 of each. **Nothing downstream reads
this field** — the board orders by arrival, not by it — so it is a mislabel, not a live defect.
**Do not rename it before the draft**; the file is the draft-night pick source. Post-draft.

---

## 6 — THE PAGE THAT VANISHED

`live_board.html` was ERR_FILE_NOT_FOUND at 11:24:40 and present again at 11:26:38.

`write_page()` is already atomic — temp file then `os.replace`, with a retry, because the folder is
Google Drive and both Drive and Chrome can hold a lock. **Cause NOT established.** Two candidates,
neither measured: Drive's virtual filesystem does not guarantee a reader sees `os.replace` as
atomic; or two copies of the board were running and **sharing one fixed temp path**, so one could
truncate the scratch file while the other was mid-replace.

**FIXED the half of it that is provable from the code, not from the event:** the temp name is now
`live_board.html.<pid>.tmp`. A shared scratch path between two writers is a hazard with no upside.
One line, inside `write_page`, exercised after editing; the page writes, replaces and leaves no
stray file. `live_draft.py` → **125374 / `1e336538aa4666c1`**, `check_kit.py` re-pinned.

---

## 7 — WHAT THIS MEANS FOR TONIGHT

**One rule, and it is the whole of it: CLOSE TODAY'S LISTENER WINDOW.**

`bridge_server.py` clears `bridge_picks.json` when **it** starts, not when a new room is hooked —
in live mode a page hook deliberately does **not** clear state, because on draft night a browser
refresh fires that same event and wiping the real picks would be unrecoverable. So if today's
listener is still running at 8:00 PM, tonight's real picks merge into today's 169 practice ones and
**every one of those 169 players reads as already drafted.**

Start the listener fresh at 7:50 as the runbook says and the file resets. The board also refuses a
bridge file older than six hours, which is a backstop and not the guard — it would still accept a
listener that has been up since 3 PM.

**Do not change the dedupe.** First-write-wins is right for the case that actually happens tonight
(a rejoin replays the *same* room's picks, so the repeat is identical). It failed today only
because two different leagues shared one file, and tonight there is one league.

**The five-second check at 7:56 PM:** the board's first poll line prints the pick count. It must be
**0**, and the room must be at pick 1. If it prints anything else, the file is carrying yesterday.
