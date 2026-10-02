# 150 — I said the board could not be rebuilt. It can. Here is the builder.

**2026-09-03, late.** Matt, twice: *"I'm still lost as to why the board can't be rebuilt. It was
built after all."*

**He was right and I was wrong.** Doc 62 (Aug 28) established a true fact — *no script produces
`board_v8_fixed.csv`* — and over the following week that fact hardened, in my telling, into a
much stronger claim: **that the board *could not* be rebuilt.** Those are different sentences.
The first is about what exists. The second is about what is possible, and it was never tested.
I repeated it to Matt three times in one evening. He kept saying it didn't add up. It didn't.

**Recovering the recipe took about ten minutes of measurement.** Every step below was measured,
not reasoned, and the whole thing reproduces.

---

## 1. THE RECIPE, AND THE MEASUREMENT THAT PROVES EACH STEP

| step | rule | proof |
|---|---|---|
| 1 | start from the spine, **skill positions only** | `code_universe_v5.csv` = 700 rows, 636 QB/RB/WR/TE. The 32 K and 32 D/ST are not on this board at all — they live in `board_v7_kdst_separate.csv` |
| 2 | drop every row with **no real projection** | `proj_missing == True` on exactly **144** of the 636. Not one is on the board; no on-board row has it set |
| 3 | drop the **twelve keepers** | 636 − 144 − 12 = **480, exact.** The twelve excluded rows that DO carry a projection are precisely the twelve names in `actual_keepers.csv` |
| 4 | `vbd = projection − §4.1 replacement`, by position | max error over all 480 rows: **0.000426** |
| 5 | `rank` = descending VBD rank | **455 of 480 identical**; the other 25 differ only *inside a VBD tie* |
| 6 | `eff_pick = adp_pick − gone_ahead` (§2.1e) | max diff **0.00** |
| 7 | re-apply the news overrides **last** | 479 of 480 projections equal the spine to 1e-6; the one exception is Josh Jacobs at 0.0 against the spine's 241.045 — `apply_news.py`, Aug 30 |

**THE SELECTION IS NOT A PROJECTION CUTOFF, and this is the trap a careless rebuild falls into.**
Drake Maye is excluded at **373.1** — higher than all but a handful of the board — because he is
another manager's keeper. On-board projections run down to **0.0**. Anything that sorted by
projection and took the top 480 would produce a different board and look entirely plausible.

## 2. THE 25 RANK DIFFERENCES ARE NOT DISAGREEMENTS

Every one is between rows with **identical VBD**: three players sitting exactly at replacement
(vbd 0.000 — Dart, Metcalf, Andrews) and 22 zero-projection players at rank 322+, hundreds of
picks past 161. Their order in the shipped board came from whatever row order the ad-hoc code
happened to have. It carries no information and is not worth recovering. `--verify` now separates
a tie-break from a real disagreement and fails only on the latter.

## 3. THE BUG I HIT ON THE WAY, WHICH IS §3 WORD FOR WORD

First run: **481 rows, not 480.** `actual_keepers.csv` says *"Travis Etienne"*; the spine says
*"Travis Etienne Jr."* My normaliser stripped punctuation but not the suffix, the keeper did not
resolve, and **another manager's keeper would have been sitting on the board as available.**
§3 says exactly this: *10% of this board's names carry a suffix, period or apostrophe.* The fix
was not a cleverer match — it was to **copy the normaliser the rest of the project already uses**
(`board_audit.py:111`, `keeper_swap.py:32`) instead of writing a new one, plus an assertion that
all twelve resolve. Loud, not silent.

## 4. WHAT THIS DOES AND DOES NOT CHANGE

**Changes:** doc 62's open question is closed, on its own terms — it asked for a builder that
reproduces the shipped board from the Aug-23 inputs before being pointed anywhere else. Done.
Post-draft, a real projection refresh is now possible instead of hypothetical.

**Does NOT change: the board stays frozen for Sept 7, and the reason is not mechanical.**
§4.1's replacement levels, §4.2's pick-8 dollars, §4.10's rule ranking and §4.12's noise fit were
every one of them **fitted against this projection set**. Swap the points and each of those
numbers describes a board that no longer exists, four days before it is used. The freeze was
always the right call; I was defending it with the wrong argument.

`make_board_file.py` therefore **refuses to write over the live board** and does not read a newer
pull. `--verify` is the default and writes nothing.

**Also worth recording: doc 62 §3 said "there is no rebuild path" for the 7:00 PM keeper swap.
That is now false too** — `keeper_swap.py` grew one (it archives the old board, rebuilds around
the actual keepers and re-applies the news overrides, and `draft_night.bat` gates it behind
`board_audit.py`). Nobody went back and corrected doc 62 when that shipped.

## 5. THE LESSON, AND IT IS THE SAME ONE AS DOC 149

**"No one has built it" is an observation. "It cannot be built" is a claim, and §0.2 governs
claims.** The stronger sentence was never tested, propagated into three replies and a directive
section, and would have survived into next season if Matt had accepted it. He asked the same
question twice and I answered around it twice before actually going and looking.

Add it to §0.2: **when a stated limitation starts doing real work in an argument, test it.**
The cost of testing this one was ten minutes; the cost of believing it was a year of an
unrebuildable board.
