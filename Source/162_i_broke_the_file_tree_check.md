# 162 — I broke the file-tree check, and one edit went onto a stale base

*Sept 3 night. `weekend_check.py` → **`file tree   FAIL`**.*

---

## 1. FOUR STALE PINS, ALL MINE

`check_kit.py` pins a size and sha256 for every file in the draft-night kit and for 46 scripts.
Two of tonight's edits re-pinned themselves automatically — `live_draft.py` (by hand, after each
change) and `player_context.csv` (`mark_rookies.py` re-pins on write, like `depth_map.py`).
**The four I edited by hand did not:**

| file | pinned | actual |
|---|---|---|
| `make_board.py` | 27,179 | **28,930** |
| `mkvalue.py` | 12,768 | **13,987** |
| `sync_desk_copies.py` | 6,767 | **5,674** |
| `make_shortcuts.py` | 8,098 | **8,234** |

All four re-pinned; the whole tree now verifies — **18 of 18 files match**, kit and Chrome
extension included.

**The lesson is the one this project keeps relearning in a new place.** `depth_map.py`,
`refresh_adp.py`, `apply_research.py` and `mark_rookies.py` all re-pin what they write, *because
they write it*. A human editing a pinned file has no such habit, and the checker is the only thing
that notices — at 7:00 PM on draft night, where `draft_night.bat` step 1/5 aborts on it.
**Editing a pinned file and re-pinning it are one action, not two.**

---

## 2. AND ONE OF THOSE FOUR IS WORSE THAN A STALE PIN

**`sync_desk_copies.py` got SMALLER — 6,767 → 5,674 — while I was adding two entries and seven
lines of comment to it.** That can only mean I edited a copy that was already older than the one on
Matt's disk: the container's `uploads/` mirror held a version from a previous session, I never
re-staged it, and I committed that base plus my change over the newer file.

**I could not recover the 6,767-byte version.** It is not in `_archive`, not in `Source_Backup`,
not in the retired `OneDrive\Fantasy\Scripts`. So the honest statement is: **I cannot prove nothing
was lost.**

**What I can prove is that the file now on disk does everything it claims**, by running it rather
than reading it. In a mirrored tree it: swept 3 stale copies including a `RETIRED` pattern and a
`Copy of DRAFT_CARD.pdf`; wrote all six dated documents (`DRAFT_BOARD_`, `DRAFT_CARD_`,
`DRAFT_DAY_GUIDE_`, `HOW_TO_READ_IT_`, and the two added in doc 161, `VALUE_LADDER_` and
`OVERRIDE_CARD_`); left `COMMANDS.html` undated as a stable bookmark; and its own "copied but is
only N bytes — that is not a PDF" guard fired correctly on the stub inputs. Nothing in its
docstring or comments describes behaviour it does not have.

**If something does turn out to be missing from it, this is where to look.**

**THE RULE THAT WOULD HAVE PREVENTED IT, and it already exists for data files:** *the staged copy
is a point-in-time snapshot; re-check before deriving an output from it.* I applied that to
`board_v8_fixed.csv` earlier tonight — caught it stale, re-staged, and corrected doc 153 — and then
did not apply it to a script four hours later. **Stage the file you are about to edit, every time.
The mirror is not the machine.**
