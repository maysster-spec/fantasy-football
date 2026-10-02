# 96 — The UAT lane that doesn't need ESPN's feed

**Date:** 2026-08-30 (late) · **Prompted by:** Matt — *"I haven't yet done an ESPN mock draft,
would that help test it? … a UAT lane that doesn't have the real feed. I guess a mock feed won't
work, or is there such a thing."*

**Answer: yes, both, and they test different things.** A mock feed absolutely works — ESPN owns the
API, but nothing stops us serving its *shape* from localhost. Built, tested, shipped.

---

## 1. WHAT WAS ACTUALLY UNTESTED

Doc 95 closed with the residual: *"nothing in this system has ever run against a live,
in-progress draft."* Being precise about what that means, because `--replay 2025` covers more than
it looks like it does and less than it needs to:

| exercised by `--replay 2025` | **never exercised by anything** |
|---|---|
| the feed parser, on real ESPN JSON | the browser opening by itself (replay `return`s above that line) |
| the keeper-row filter, on real keeper rows | the amber startup page |
| the render maths, 180 times | the identity line (`team 9 = JUG`) |
| the engine's recommendations | a board that is **changing while you watch it** |
| | the on-clock page appearing *at* your pick |
| | the D/ST page at 152 and the kicker page at 161 |
| | the completion panel |

Everything in the right column is the part Matt actually *looks at*. It had all been proven by
assertion, never by eye.

## 2. `rehearsal.py` — a fake ESPN on 127.0.0.1

`py rehearsal.py` starts an `http.server` that answers `mDraftDetail` and `mTeam` in ESPN's exact
shape, then launches **the real `live_draft.py`** against it via a hidden `--reads` override. Same
poll loop, same renderer, same browser, same Google Drive path, same 3-second cadence. Pick order
is ADP with §4.12 affine noise; the 12 keeper rows sit in the feed from pick 1 (`--keepers end`
puts them at 169–180 instead, the other shape ESPN might use). Default pace ~4 minutes;
`--realtime` is 8s a pick and feels like the night; `--from 148` jumps to the D/ST and K pages.

`live_draft.py` prints a `!!!!` banner whenever `--reads` is set. A tool pointed at a fake feed
must never be mistakable for the real one.

**Measured, on the rehearsal feed with 12 keeper rows present throughout:**

| state | result |
|---|---|
| all 12 skill picks (8, 17, 32 … 137) | **fire `YOU ARE UP` with the amber clock box** |
| pick 21 (not his) | planning page, correctly not on-clock |
| pick 152 / 161 | distinct D/ST page and kicker page |
| after 168 | Draft complete panel |
| all five page types | distinct renders |
| keeper rows | counted as taken, never advance the clock |

That first row is a live regression test for doc 58's bug — the one that put the board 12 picks
ahead so `on_clock` never fired. It now has a test that would catch it, run in the real loop.

## 3. AND STILL DO AN ESPN MOCK

The rehearsal cannot fake one thing: **ESPN's own clock, and other humans picking.** So the mock
lobby is still worth twenty minutes — `py live_draft.py --mock --league <id from the draft-room
URL>`. Whether ESPN exposes mock leagues on `lm-api-reads` is **unknown and not worth researching**
— one attempt answers it in ten seconds. If it 401s or 404s, that is information, not a failure,
and the rehearsal already covers the same ground.

## 4. MY TEST STRING WAS WRONG AGAIN — THIRD TIME THIS SWEEP

T8 first reported FAIL on *"pick 8 renders an ON THE CLOCK page."* The page was right; the label
is **`YOU ARE UP`** when it's your turn and `ON THE CLOCK` when it isn't, so my assertion was
looking for the *opposite* state's string. Same class as doc 95's `VBD`-in-a-CSS-comment and
`board_audit`'s first two failures. **Every false failure this sweep has been my test reading the
wrong thing, never the code being wrong** — which is its own signal about where the remaining risk
is: the harnesses are younger than the code they check.

---

**Files:** `Scripts\rehearsal.py` (8,314B, `f8eb2868640304ee`) + `rehearsal.bat` ·
`live_draft.py` (37,387B, `2d9b0709973acc48`, hidden `--reads`) · `check_kit.py` (10,896B,
`96654cba1bb3f4d0`, rehearsal pinned) · `COMMANDS.html` (three new cards in section 3).
