# 116 — One board replaces five sheets; both Gemini sweeps landed; the desk is a command now

**Date:** 2026-09-01, small hours.

---

## 1. THE TWO SWEEPS

**The breadth pass did exactly what it was asked.** 40 players, every one with BULL / BEAR / LEAN /
QUOTE, and **17 of 40 said NONE FOUND** where no real quote existed. That is the anti-fabrication
instruction working — the previous Gemini report invented quotes rather than admit it had none.

**The delta pass reverted to prose** but stayed honest: 20 player blocks, 9 explicit NONE FOUNDs, a
works-cited list. Usable, just not parseable the easy way.

`parse_takes.py` reads **both shapes** and emits `analyst_takes.csv`: 54 unique players, **34 with a
lean, 32 with a real quote.** It never infers a lean that is not stated, and a block that said
NONE FOUND stays empty rather than being back-filled from the surrounding prose — the absence is
the finding.

Lean distribution: **strongly bull 6 · lean bull 11 · genuinely split 9 · lean bear 8.**
The one worth noticing before a mock: **James Cook III is lean bear** and he is a live pick-8
option; **Amon-Ra St. Brown, Derrick Henry, Jonathan Taylor, Breece Hall, CeeDee Lamb** are the
strongly-bulls inside reach.

---

## 2. ONE BOARD — `make_board.py` → `DRAFT_BOARD.pdf`

Matt: *"these all carry player based information. Is there a way to condense into one draft board
listing without losing valuable information?"* Yes, and the thing that made five sheets fail was
never the information — it was that a 60-second clock does not survive flipping between documents.

**What folded in, and what each contributed:**

| was | held | now |
|---|---|---|
| FALLBACK_BOARD | the ranking, no reasons | the rows and their order |
| LATE_RB_SHEET | backfields, RB only, picks 104–137 only | the UNSETTLED / LEAD BACK / job-worth clause |
| AUDITION_WINDOW | the keeper view, picks 56–89 only | the pick strip at the top |
| ANALYST_CALLS | who is high on whom, 78 players | the BUY mark, the lean column, the quote |
| INJURY_CONTEXT | the grades, in a spreadsheet nothing could read | AVOID / DISC and the injury line |

**180 players, 6 pages, one row and one note-line each.** Sorted by **VBD, not ADP** — on the clock
the question is "best player left that fits my caps," which is a VBD question — with `goes at` as a
column so a player who will keep is still visible.

**Two things were cut in review because they were noise, not information:**
- *"no injury news found | exp 17 gm | [low confidence]"* appeared on **107 of 143 rows**. It is the
  absence of a finding, not a finding. Suppressed unless the player carries a grade.
- The backfield label was printing **"LEAD BACK, job worth 331" next to Jahmyr Gibbs.** The label
  describes a job someone might take; it belongs on the backup, not on the man holding it. Now
  restricted to depth ≥ 2 or an UNSETTLED backfield.

**The five sheets still build.** They are just no longer desk copies. `DRAFT_DAY_GUIDE` had six
references routing failures to FALLBACK_BOARD — **all six now point at DRAFT_BOARD**, and the
guide's stale Tank Dell paragraph was replaced with the IR facts and the stash note.

**On the second live board idea:** it is the same content twice, and two screens is the five-sheet
problem with a mouse. The better version of it is what the note line already does — if a row needs
more, the live board's hover holds the full text. **Not worth building before Sept 7.**

---

## 3. THE DESK IS A COMMAND — `py tidy_docs.py --root`

Dry run by default. Raw Gemini output → `10_Gemni\`, finished analysis → `Source\`, one-off prompts
and spreadsheet leftovers → `_archive\` with a date suffix. **Nothing is deleted, ever.**
`sync_desk_copies.py` now also sweeps the five retired dated PDFs from the root, so the desk drops
from eight dated files to **three: DRAFT_BOARD, DRAFT_CARD, DRAFT_DAY_GUIDE.**

Staying put by name: **COMMANDS.html** (undated on purpose — a changing filename breaks a bookmark)
and Matt's own To Do List.

---

## ASSUMPTIONS

1. **VBD order is the right sort for a paper board.** It matches how the live engine ranks and how
   the old fallback worked. If the draft-night experience says otherwise, `--n` and the sort are
   one line each.
2. **54 players with a take is enough coverage to be worth a column.** 126 of 180 rows have a blank
   lean. A mostly-empty column is a real design risk; it is there because a blank lean is honest
   and a guessed one is not.
3. **Six pages is scrollable and printable.** Untested at a real table. The mock is the test.
