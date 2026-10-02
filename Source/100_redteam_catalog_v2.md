# 100 — Red team, round two: two draft-losing bugs, and the catalog for the last seven days

**Date:** 2026-08-31 · **Matt's instruction:** *"Red Team, this is still number one priority and
let's not think we are done here… create another catalog / wish list and see what could bear the
most fruit in the time we have."*

**Three bugs found tonight. Both were created by last night's own fixes, both were REPRODUCED before
being fixed, and one of them would have cost the third round.**

---

## 1. THE 7:00 PM KEEPER SWAP SILENTLY REVERTED THE JACOBS REMOVAL

`keeper_swap.py --write` rebuilds the board **from the spine**, not from the current board. So the
news override applied last night was wiped. Reproduced exactly:

```
BEFORE keeper_swap --write:  Josh Jacobs rank 435  proj 0.0
  ... "IDENTICAL to the current board -- keepers match the build."
AFTER  keeper_swap --write:  Josh Jacobs rank  20  proj 241.0
```

It even printed **"IDENTICAL to the current board"** while doing it — that message compares keeper
*membership*, not the file it just wrote. This would have fired at 7:00 PM on Sept 7, one hour
before the draft, and put a suspended player back at board rank 20 with an effective pick of 32.4.

**Fixed three ways:** `keeper_swap` now re-applies `news_overrides.csv` itself and says loudly if it
cannot; `draft_night.bat` gained **step 3b — `py board_audit.py`, gated** (nothing proceeds on a
failed audit); and `refresh_pull.bat` now prints the same instruction for a Sept-5 REBUILD.
**Verified: the full 7:00 PM sequence now ends 39 of 39, with Jacobs still at 435.**

## 2. THE AUDIT WOULD HAVE CRIED WOLF AT 7:05 PM ANYWAY

`keeper_swap` computed VBD from the directive's **3-decimal** replacement quotes; the shipped board
was built at full precision. Every VBD moved by up to **4.26e-04** — numerically nothing, and
enough to fail `board_audit`'s "VBD = projection − replacement, every row" an hour before the
draft. **A gate that cries wolf on draft night is worse than no gate**, because the correct
response to it and to a real failure look identical at 7:05 PM. `keeper_swap` now derives
replacement from the same frozen pull the board and the audit use.

*Both of these existed only because the board became something that can be edited after it is
built. That is a new class of failure this project did not have 24 hours ago, and it is the reason
Matt's instinct — "don't think we are done" — was right.*

## 2b. AND A THIRD, FOUND BY FORCING THE REALISTIC CASE

Tonight's first test used keepers **identical** to the predictions, so the interesting path was a
no-op. Forcing a divergent set — two keepers changed, two players coming back onto the board —
exposed that `keeper_swap` **rewrites the board and never touches the prerank.** The prerank then
still contained the newly-kept players and was **missing the two who returned**, and step 4 of
`draft_night.bat` would have pushed that list to ESPN. Now rebuilt from the new board (480 skill +
64 K/D-ST), with the K/D-ST tail carried untouched.

**Verified both ways: divergent keepers → 39 of 39; identical keepers → 39 of 39.** (The rebuilt
prerank differs from the shipped one in 31 tie positions, max move 9 ranks — VBD ties broken
differently. Harmless, and step 4 re-injects regardless.)

**Note what this says about testing:** a passing test on the easy path hid the bug. The rule is
already in `ERROR_PATTERNS` — exercise the object production builds — and it needed a third
application tonight.

## 3. THE BOARD NOW CARRIES THE INJURY SHEET — because its absence already cost us

`player_context.csv` joins the kit as the 6th file: the sheet's **AVOID / DISCOUNT / NEUTRAL**
grades, rendered as coloured badges beside each name on the live board, with the reason on hover,
and as an `!` column on the paper board. **They never move a number** — doc 74 is explicit that the
injury framework cannot be backtested here, so it breaks ties and stops him flinching at healthy
players. Missing file = no badges, never fatal.

**Why this was urgent:** doc 98 put **Tank Dell** up as a pick-137 target off an NFL.com sleeper
list, while this project's own sheet had him at **2 expected games and ↓231 ranks.** I had both
documents and did not cross them. Doc 98 is corrected; the badge is the structural fix.

**And one retraction:** I flagged the sheet's **Patrick Mahomes** row as possibly fabricated. It is
**real** — ACL/LCL, verified against three outlets. He is also **cleared to practice at seven
months and targeting Week 1**, so the risk is his rushing floor, not his availability. Row and card
corrected.

---

## 4. THE CATALOG — seven days, ranked by (chance it is broken × what it costs) ÷ effort

| # | item | who | why it ranks here |
|---|---|---|---|
| **1** | **ESPN mock draft** — `py live_draft.py --mock --league <id>` | **Matt** | The only thing that can exercise a real clock with real humans. `--mock` and `detect_shape()` have **never executed**. Ten seconds tells us whether ESPN even exposes mock leagues on the reads API. |
| **2** | **A `--realtime` rehearsal, watched end to end** | **Matt** | 25 minutes. The live loop has never run longer than four. Watching it while doing something else is the point — that is the draft-night condition. |
| **3** | **Should `adp_pick` be re-frozen on Sept 5?** | me | The board's ADP is **frozen at the 08-23 pull**, so every survival number and every `eff_pick` is two weeks stale — and Jacobs going out will move the RB market this week. §8 says ADP is not a runtime input; that was decided before a top-20 RB was removed. **Open question, and it is the biggest unexamined assumption left.** |
| ~~4~~ | ~~dry run against different keepers~~ | **done** | Done tonight — it found bug 2b above. Both keeper paths now end 39 of 39. |
| **5** | **Cookies, once more on Sept 5 and again Sept 7** | Matt | Nothing has changed here; it is just the thing that most often breaks between now and then. |
| **6** | **A second news sweep on the shortlist, Sept 5** | me | Jacobs proved eight days is long enough for the board to be wrong. The Sept 5 sweep is the only scheduled one. |
| **7** | **Fable on picks 17 and 32** | Matt to launch | Still the last open *strategy* question. Everything above is plumbing; this is points. |
| **8** | **`--keepers end` rehearsal** | me | Tests the other shape ESPN might use for keeper rows. Cheap, and it is the one accepted risk that a test can actually reduce. |

**Deliberately NOT on this list:** anything about run buttons, the COMMANDS page, or further UI.
The page is done. Every item above either changes what the tool says or proves it will still be
saying it at 8:00 PM.

**And the honest note on my own testing:** five false failures this sweep, every one a test reading
the wrong string or the wrong object — never the code. Tonight added a sixth of a new kind: a patch
to `draft_night.bat` that inserted a handler **inside** the success path, which I caught only by
parsing the labels afterwards. **Verify batch edits structurally, not by eye.**
