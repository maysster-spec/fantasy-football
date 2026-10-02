# 97 — A real suspension, a fake roster, and what byes are actually worth

**Date:** 2026-08-30 (late) · **Trigger:** Matt read a rehearsal roster as the tool's judgement and,
in doing so, spotted a real event the system would have missed.

---

## 1. JOSH JACOBS IS OUT. THE BOARD HAD HIM AT RANK 20.

`[SOURCED: NBC Sports player news + DraftSharks, 2026-08-30]` The NFL placed Josh Jacobs on the
**Commissioner's Exempt List**. Indefinite; no fixed rules on duration and players "don't tend to
come off quickly." Consensus guidance is to draft as though he does not play in 2026.

On the shipped board Jacobs was **rank 20, VBD +72.5, eff_pick 32.42.** Matt's pick 32. The engine
would have put him on the clock, and `FALLBACK_BOARD.pdf` had him at #20 on paper.

`DRAFT_DAY_GUIDE` has said in writing since it was written that *"a late injury has no automated
catch."* That was true and it was about to cost the third round. It now has a fix, if not a detector:

- **`Scripts\news_overrides.csv`** — one row per event: `espn_id, player, action, dated, note`.
  `out` zeroes the projection (VBD → −replacement, the row survives so a late flyer stays priced);
  `remove` drops the row.
- **`py apply_news.py --write`** — archives the originals, rewrites board **and** prerank, re-sorts
  and renumbers both, and re-pins `check_kit`. ADP is deliberately untouched: a suspended player
  still costs the field a pick, and depletion is about keepers, not injuries.
- **`board_audit.py`** gained two checks per override and **fails loudly if one is missing** —
  because a Sept-5 REBUILD regenerates the board from the pull and would silently restore him.
  `[TESTED]` negative control: restoring the pre-news board drops the audit to **36 of 39** with
  `DO NOT DRAFT ON THIS BOARD`.
- **`py make_fallback.py`** — the paper board had **no builder at all**; it was made by hand in a
  chat, so the board could be fixed in seconds and the paper could not. Now it regenerates from the
  board, with a red **DO NOT DRAFT** block naming anyone news removed. A paper board is only ever
  read at the moment the live one has died and cannot be cross-checked; it must never be older than
  the board it backs up.

Applied and verified: board **39 of 39**, Jacobs at rank **435 of 480**, prerank #435 of 544, paper
board reprinted at 2 pages. **ESPN still holds the old prerank** — that needs
`py weekend_check.py --inject`, which is Matt's (it writes to ESPN).

## 2. THE ROSTER HE ASKED ABOUT WAS SYNTHETIC, AND THAT IS MY DEFECT

The 15 players were the **rehearsal's** fake feed — ADP dealt with noise — not a draft and not the
tool's judgement. Two of them (Payne Durham, Grant Calcaterra at picks 152/161) are verbatim from
my own test run. Matt reasoned about J.J. McCarthy's readiness and Josh Jacobs' character off
random draws.

The console banner said REHEARSAL. **He was looking at the page, and the page looked exactly like
the real one.** This is the same failure as doc 95's TRAP 5 — a plausible page mistaken for an
authoritative one — and I built it one message after fixing that. Fixed: `write_page()` now stamps
**every** page a fake feed produces with a red sticky bar and a `REHEARSAL - ` title prefix.
`[TESTED]` on-clock, D/ST, kicker and completion pages, banner absent when the flag is off.

## 3. BYES ARE PRICED. HE ASKED, AND THE ANSWER IS MEASURED, NOT ASSERTED.

`code_live_engine._lineup()` walks weeks 1–14, drops each player in his bye week and fills from the
bench at replacement. Every number the live board shows — `adds now`, `if I wait`, and the rollout
that orders the list — is computed through it. Byes are not an afterthought in the engine.

`[TESTED]` on that 14-player roster (**population: one roster; illustration, not a law**):

| | starting points, weeks 1–14 |
|---|---|
| as dealt — five players on bye 11 | **1200.5** |
| identical players, byes spread evenly | 1207.0 |
| **cost of the stack** | **−6.5** |

And swapping one bye-11 WR for an equal-projection bye-8 WR is worth **+3.8**.

**So the honest reading: the engine sees byes and prices them at a few points, which is real but
small — and a 6.5-point bye cost loses to a 20-point VBD gap almost every time.** That is why it
tolerated five on week 11. It will not refuse a stack and it does not warn. **The number is the
tool's; the tiebreak is Matt's.** Caveat: `_lineup` gives each player a flat per-week rate, so it
prices a bye week, not a player who is actually out for a stretch.

## 4. NO, THE PAGE DOES NOT NEED A REFRESH JOB

`render()` and `render_streamer()` already carry `<meta http-equiv="refresh" content="3">`, and the
startup placeholder carries a 4-second one. The poller rewrites the file, the browser re-reads it,
nothing to click. Verified in the source, not remembered.

## 5. FOURTH FALSE TEST FAILURE OF THE SWEEP, AND THEY ARE ALL THE SAME SHAPE

`board_audit` (hard-coded constants) → doc 95 (`VBD` in a CSS comment) → doc 96 (`ON THE CLOCK` vs
`YOU ARE UP`) → tonight (a header that CSS uppercases). **Every false failure in this sweep has been
a test reading the wrong object or the wrong string; not once has it been the code.** The harnesses
are younger than the code they check, and that is now the highest-density source of noise in this
project. Worth remembering the next time a check goes red at 7:50 PM.

---

**Files:** board + prerank corrected and re-pinned · `apply_news.py` (7,889B) ·
`news_overrides.csv` · `make_fallback.py` (6,222B) · `board_audit.py` 39 checks ·
`live_draft.py` (38,537B, rehearsal stamping) · `check_kit.py` (11,352B) ·
`FALLBACK_BOARD.pdf` reprinted · guide and COMMANDS updated.
