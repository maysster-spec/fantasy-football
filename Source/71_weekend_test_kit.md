# 71 — WEEKEND TEST KIT
**Three tests, ~15 minutes total. Each has the exact command, the exact PASS line, every known
way it can lie to you, and what to do on failure. Run them in this order. Before anything:**

```
cd "G:\My Drive\_Fantasy\2026\Scripts"
py check_kit.py
```
Expect `PASS: canonical tree matches the manifest`. If STALE/MISSING appears, stop and tell me —
you would be testing the wrong files.

---

## TEST 1 — INJECTOR (negative playerIds + replace-vs-append). Two runs, one minute.

```
cd "G:\My Drive\_Fantasy\2026\Scripts"
py espn_draft_injector_Gemini.py
```

**PASS — you must see BOTH lines:**
```
  ESPN reports 544 players stored (sent 544).
  count matches. first stored id = 4429795 (expect 4429795).
```
544 = 512 players + **32 defenses as negative ids**. 4429795 = Jahmyr Gibbs, prerank #1.
Seeing 544 means ESPN accepted the negative ids — that is the whole question (i).

**Now run the exact same command a second time.** Second run says `544` again → the POST
**replaces**. PASS, question (ii) closed. Says `1088` → it **appends** — tell me; the fix is
clearing the list in ESPN's UI and injecting exactly once on draft night.

**FAIL modes:**
| you see | it means | do |
|---|---|---|
| `ESPN reports 512` | all 32 defenses rejected | tell me — draft plan survives, prerank loses D/ST autodraft cover |
| any other count | list truncated (tail dies first; last row is Chad Ryland, 4363538) | tell me the number |
| `Update Failed. Status Code: 401` (or 403) | ESPN cookies expired | tell me; fresh `espn_s2`/`swid` go into the script — and `live_draft.py` uses the same cookies, so both need it |
| `(read-back failed: …)` | POST unverified — **this is the silent-failure trap**; a 200 alone proves nothing | re-run once; if it repeats, treat as FAIL |

**The one lie to watch for:** "Pre-draft rankings updated." printing WITHOUT the "ESPN reports"
line above it. No read-back = not verified = not a pass.

## TEST 2 — LIVE BOARD REPLAY. Five minutes.

```
cd "G:\My Drive\_Fantasy\2026\Scripts\live_draft"
py live_draft.py --replay 2025 --speed 0.2
```

**PASS — the line that matters, near the top:**
```
  replay: 180 rows fetched (12 flagged keeper).
```
**12 is the number.** 180 = 168 real picks + 12 keepers at slots 169–180. The browser page opens,
steps through the whole 2025 draft, and ends with `replay complete -> …`.

**FAIL modes:**
| you see | it means | do |
|---|---|---|
| `(0 flagged keeper)` | keeper filter broken or feed changed — **the board would run 12 picks ahead on draft night.** This is the exact doc-58 defect this test exists for | STOP. Tell me |
| `replay: 168 rows` | feed no longer includes keeper rows — same risk, different symptom | tell me |
| a traceback | — | send me the last 5 lines |
| 401 in the fetch | cookies (same fix as Test 1) | tell me |

**Silent-failure check, 30 seconds:** while it plays, glance at the board around pick ~30 —
no recommended player should be someone already drafted. One stale name = id mismatch, tell me.

## TEST 3 — PRERANK LANDED, CONFIRMED FROM ESPN'S SIDE. Two minutes.

Test 1's read-back is the API-side proof. This is the belt-and-braces UI check, because the one
thing the API cannot prove is what the draft room will actually display.

Open ESPN → your league → **Draft** → **Pre-Draft Rankings / Edit Rankings**. Confirm:
1. **#1 is Jahmyr Gibbs** — if it shows ESPN's default order instead, the injection did not land
   no matter what the script printed.
2. Scroll or search: **defenses are present in the list** (e.g. a team D/ST somewhere mid-list,
   not absent). Absent D/STs with a 544 read-back would mean ESPN stores but won't display
   negative ids — tell me, that is new information.
3. The list ends at **Chad Ryland (K)** — the tail survived.

## TEST 4 — KEEPER-SWAP DRILL (optional, one minute — new tool, shipped Aug 28)

```
cd "G:\My Drive\_Fantasy\2026\Scripts"
py keeper_swap.py --check
```
**PASS:** `IDENTICAL to the current board -- keepers match the build.` That proves the rebuilt
board-from-scratch equals the shipped one (it is the board's recovered builder — doc 62 closed).

**The real 7:00 PM drill on draft night:** edit `actual_keepers.csv` (12 names, exact spelling —
a typo refuses with a suggestion), `py keeper_swap.py --check` to read the diff, then `--write`
(archives the old board automatically), then restart `live_draft.py`. If all 12 predictions were
right, `--check` says IDENTICAL and you skip `--write` entirely.

**That's the kit.** Three passes = the draft-night stack is verified end to end and nothing else
is on your plate until Sept 5. Any fail: copy me the exact line — every one above has a known
next step, and none of them is fatal ten days out.
