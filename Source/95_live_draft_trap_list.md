# 95 — Traps that could stop the live board firing: the list, checked twice

**Date:** 2026-08-30 (evening) · **Prompted by:** Matt — *"review and determine if additional
failsafe controls are needed. Make a list, and then check it twice. If the Live draft doesn't have
the info correct, or otherwise fail then all this work was for nothing."*

**Scope:** everything between `py live_draft.py` at 7:55 PM and the last pick. Not the board's
numbers (doc 94 / `board_audit.py`, 37/37), not the 7:00 PM keeper swap (doc 89).

**Method.** Pass 1 read the poll path line by line looking for anything that can raise. Pass 2 did
not re-read — it **executed** each fix against the failure it claims to prevent (§0.2: a guard that
has never been run is not a guard). Eight fixes, seventeen assertions, all green. Where a trap could
not be executed here, it is filed as ACCEPTED with the reason, not silently dropped.

---

## A. FOUND AND FIXED — 8

| # | trap | what it would have looked like on the night | fix | proved by |
|---|---|---|---|---|
| 1 | **`step()` sat OUTSIDE the poll `try`** | any exception inside the renderer — a bad feed row, a locked file, a bug — ends the poller at whatever pick it lands on. A crash at pick 41 costs the night. | the whole render is inside `try`; `last` is deliberately **not** advanced, so the next poll retries the same state | T1: injected two `ValueError`s mid-loop, loop survived and finished |
| 2 | **`webbrowser.open` unprotected** | no default browser / a Drive path it won't take → startup dies before the first poll | wrapped; prints the path to open by hand | T1: raised from a stubbed `webbrowser`, run continued |
| 3 | **non-atomic page write** | `live_board.html` sits in a **Google Drive folder** and is open in a browser. Either can hold a lock → crash, or a half-written page rendered as garbage | write `.tmp` → `os.replace()` (atomic on Windows), 3 retries, then give up **leaving the last good page** | T3: forced `OSError` on every write — returned False, previous page byte-identical |
| 4 | **`'file://' + OUT` is not a valid URI on Windows** | backslashes and the space in `My Drive` both break it. **This line has never executed on Matt's machine** — `--replay` returns above it, so the one path he has tested skips it | `pathlib.Path(OUT).as_uri()` → `file:///G:/My%20Drive/...` | T5: `PureWindowsPath.as_uri()`, escaped space, no backslashes |
| 5 | **a stale page shown at startup** | the browser opens **before** the first poll. On disk is whatever the last run left — after a `--replay` that is a finished **2025** board. If ESPN 401s at 7:55, that plausible-looking board is what he stares at | a `render_waiting()` placeholder is written first: amber, self-refreshing, no table, says *"Nothing on this page is a recommendation"* | T4: body contains no `<tr>`, no table, no VBD |
| 6 | **the team id was never confirmed in words** | `MY_TEAM_ID = 9` is **not** the draft slot (8). If it is ever wrong, every roster panel, position cap and bye check runs against **someone else's team**, all night, silently | `confirm_team()` reads `mTeam` at startup and prints `team 9 = JUG "…"  <- IS THIS YOU?`; an id not in the league is called out loudly; a network failure is never fatal | T7: right id names it, wrong id warns, dead network warns and continues |
| 7 | **the 401 hint didn't say to restart** | `py cookie_jar.py` in another window fixes the files but **not this process** — the running poller still holds the old cookies in memory | the hint now says: fix them, then Ctrl+C **here** and rerun, and that restarting is safe because it re-reads every pick and remembers nothing | T6 |
| 8 | **`live_board.html.tmp` would read as `EXTRA`** | a Ctrl+C at the wrong instant leaves the scratch file; `check_kit` would report a corrupted kit | added to `check_kit`'s RUNTIME ignore set | executed: run 1 clean, run 2 (one byte changed) fired `STALE` |

---

## B. CHECKED AND CLEAR — 9

1. **Non-ASCII inside `print()` → `UnicodeEncodeError` under Windows cp1252.** Scanned all 11
   draft-path scripts: **0 print/exit lines with non-ASCII**, every file.
2. **HTTP hangs.** Every `requests.get/post` in every draft-path script carries `timeout=`.
   A hung ESPN cannot freeze the poller.
3. **Unmapped player ids.** `set_taken` uses `.get()` and `in` on both sides — a kicker, a
   defense, a 2026 keeper or anyone outside the 480 cannot raise.
4. **`detect_shape()`'s `SystemExit`.** Only reachable via `--mock/--slot/--teams`. Draft night is
   plain `py live_draft.py`, which uses the hard-coded 12/8. **Not on the live path.**
5. **Missing board.** Explicit `SystemExit` at startup naming the folder contract, and it refuses
   to fall back to an older board.
6. **Keeper rows advancing the clock** (doc 58). Filtered; the replay proved 12 of 180 on real
   2025 data, and the count prints every poll.
7. **Packages.** `pandas` / `numpy` / `requests` are proven on his machine by the replay actually
   running, not by inspection.
8. **Two instances writing the page.** With `os.replace()` the worst case is two valid pages
   alternating — never a torn one.
9. **The board's own numbers.** `board_audit.py`, 37 checks re-derived from source, 37 pass.

---

## C. KNOWN, ACCEPTED, WITH THE REASON — 5

1. **ESPN could carry 2026's keepers differently.** The replay proves **2025's** shape only.
   Mitigation is human: the keeper-row count prints every poll and the 7:55 PM guide step is to
   eyeball it. If it isn't 12, use the paper board.
2. **`keeper_swap` writing the board while the poller runs.** Prevented by sequencing (7:00 then
   7:55), not by a lock.
3. **Google Drive hydration stall mid-draft.** Mitigated by "Available offline", not eliminated,
   and not testable from here.
4. **Cookies expiring mid-draft.** Cannot be repaired in-process. The poller survives, names the
   cause, and tells him restarting is safe.
5. **A total ESPN outage.** `FALLBACK_BOARD.pdf`.

---

## D. THE RESIDUAL RISK NO CODE CHANGE TOUCHES

**Nothing in this system has ever run against a live, in-progress ESPN draft.** The replay is real
data through the real feed, the real keeper filter and the real render path — but it is a finished
season replayed. Every fix above reduces the cost of a surprise; none of them removes the surprise.
That is what `FALLBACK_BOARD.pdf` and `DRAFT_CARD.pdf` exist for, and it is why the 7:55 PM eyeball
steps are on paper.

## E. ONE OF MY OWN CHECKS WAS WRONG, AGAIN IN THE SAME WAY

T4 first reported FAIL on *"no VBD text in the startup page"*. The page body is clean; the word
appears in a **CSS comment** inside the inlined stylesheet. Same class as the `board_audit` false
failures — the test asserted against the wrong object. Re-run against the body only: pass. Logged
because §0.2 says a diagnosis is a claim, and a failing test is a diagnosis.

---

**Files changed:** `live_draft.py` (36,754B, `8ad86c2dcbc77f2d`) · `check_kit.py` (10,603B,
`c436c9a77001e291`) · `DRAFT_DAY_GUIDE.md`/`.pdf` (the 7:55 PM row now names both eyeball lines).
Both scripts are committed to `Scripts\` and re-pinned; `py check_kit.py` should read PASS.
