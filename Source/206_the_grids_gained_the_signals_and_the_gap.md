# 206 — The grids gained the measured signals, and then the gap between them

*2026-09-06. Two requests from Matt, one page each, both on `make_gridboard.py`.*

---

## 0. WHAT CHANGED

1. **Both grids now carry this session's two MEASURED signals**, which were on the board and the
   tier sheet but not here: **`3/3`** (RB with all three composite signals, doc 191) · **`1/3`**
   (one or none) · **`N% snaps`** (WR/TE in the bottom quarter of 2025 snap share, doc 197).
   9 · 18 · 18 cells respectively. Only the decision-relevant half of the snap signal is drawn —
   top-quartile is confirmatory and would cost a chip slot.
2. **Both grids print the gap between the two orderings**, so no diffing by eye:
   **`+30`** = the room takes him thirty picks LATER than our board ranks him (wait) ·
   **`−14`** = he goes fourteen picks EARLIER (reach or lose him). Drawn at 10 or more only:
   25 positive, 23 negative, 48 of 168 cells. Same number, same meaning, on both pages.
3. **`BOARD_GRID`** exists — `make_gridboard.py --board`, the same snake filled by our VOR order.
   **One script, one flag, two outputs.** A second FILE for one job is the §0.2 defect; the only
   things that differ are the sort key and the words at the top.

**Both still fit 2 pages.** Negative control run: the default `ADP_GRID` output was byte-identical
to the previous build before the chips were added.

## 1. THE LABELLING DEFECT MATT FOUND ON THE WAY

Sheet 1 was headed **"ROUNDS 1–8, WHERE THE BOARD DECIDES"** on a page that is not the board and is
not in the board's order. He read it as a defect and he was right about the confusion even though
the ordering itself was correct by design. It now reads **"IN THE ORDER THE ROOM TAKES THEM"**, and
the subtitle says out loud that the two orders differ on purpose, that this page answers WHEN and
the board answers WHO, and that the tier sheet is our own order.

**And "market order" was jargon** — his words: *"is that how i go grocery shopping."* §0.1 forbids
jargon without a gloss and I used it four times. Every instance is now plain English: *"each cell
is where the other eleven managers are expected to take that player."*

## 2. ONE MORE DEFECT, FOUND THE SAME WAY

The grid's subtitle was printing **"pick 8 is closed (three unrelated routes, margin 20 points)"** —
and **§4.2 v7.2 RETRACTED that 20**. It was the only place in the shipping files still quoting it.
Corrected to what is actually established: St. Brown is the engine's #1 in every board state anyone
has run, and the SIZE of the edge is not established.

**`make_gridboard.py` was also never pinned in `check_kit.py`** despite building a desk sheet and
being step 9 of `sept5_after.bat`. A stale copy would have gone unnoticed. Pinned.

## 3. THE PHONE PAGE

Matt asked to read it on his phone, where a 12-wide landscape grid is unusable. **"Slot 8, Both
Ways"** is a published artifact: his twelve flexible turns stacked vertically, each read twice —
the room's man on the left, the board's slot value on the right, the gap on the spine — plus the
two divergence lists and the short read on the turns that actually decide something.

*Files: `make_gridboard.py` · `sept5_after.bat` (step 9b) · `sync_desk_copies.py` (BOARD_GRID joins
the desk) · `check_kit.py` re-pinned for all three.*
