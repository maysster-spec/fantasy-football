# 157 — The row shading never got doc 135's memo

*2026-09-04 container / Sept 3 evening Eastern. Matt, looking at the printed board: "remind why
are some rows shaded gold? Ashton Jeanty, Breece Hall, Jeremiyah Love… Christian McCaffrey is also
shaded gold."*

---

## 1. WHAT GOLD MEANT, AND WHY THREE OF HIS FOUR EXAMPLES WERE WRONG

`make_board.py` paints two row backgrounds: **pink `#fdeceb` = AVOID**, **gold `#fdf6e8` =
DISCOUNT**, both straight off the injury sweep's `grade`.

But **doc 135 already found that grade half-wrong** — Matt's own words then were *"DISC on Christian
McCaffrey can't be right, there is no taking him later."* The measurement behind that fix:
**11 of the 32 DISCOUNT rows carry `exp 17 gm` from the sweep itself**, i.e. the grade was firing on
load-management notes, not on risk. The fix put the expected-games number **on the badge** and
demoted a 17-game discount to a plain grey `note`.

**The row shading was never demoted with it.** `cls.append('d')` still fired on the raw grade, so a
third of the gold rows were warning about players the badge system had already stood down:

| still shaded gold | badge said | adp |
|---|---|---|
| **Christian McCaffrey** | `note` | 7.7 |
| **Ashton Jeanty** | `note` | 21.9 |
| Malik Nabers | `note` | 35.0 |
| **Breece Hall** | `note` | 36.1 |
| Quinshon Judkins | `note` | 49.0 |
| Christian Watson · Bo Nix · Jonathon Brooks · Patrick Mahomes · Alec Pierce · Daniel Jones | `note` | 89–160 |

**Three of the four players Matt picked out at a glance were in that list.** He found an 11-row
defect by asking what a colour meant.

**And the page was contradicting itself in print.** The legend at the foot of every page already
said *"note — flagged, but 17 games expected — not a discount"*, directly under a gold row that
said the opposite. Half a fix is how that happens.

**Jeremiyah Love was the one correct example** — `exp 15 gm`, badge `DISC 15`, and he stays gold.

---

## 2. THE FIX

The shading now follows the badge exactly: gold only when the badge really says `DISC`.
One condition, in the same place the badge's rule already lives.

**Measured before and after, on the real rendered page:** gold row-classes **64 → 42**
(each player carries the class on his row and his note row, so that is 32 → 21 players);
pink unchanged at 16 (8 AVOID players). Verified by rendering and screenshotting, not by reading:
Jeanty `class="b1"`, Hall `class="b2"`, McCaffrey `class="b1"` — no `d` on any of them —
and Love still `class="d b2"`.

**Not touched:** the AVOID shading, the badges themselves, any number, and the live draft board —
`live_draft.py` does not shade rows at all, so this was a paper-only defect.

---

## 3. THE DESK FOLDER, WHILE I WAS THERE

Matt asked how to get `HOW_TO_READ_IT.pdf` into `Desktop\FF2026 Draft`. That folder is not a
document folder — it is the generated shortcut folder: numbered `.bat` launchers and `.url` links
pointing at **dated** copies at the 2026 root. A loose PDF dropped in would have been the only file
not following that shape and would have gone stale on the next refresh.

So it got the same treatment as the other five documents: **`11 - How to read the board.url`**,
pointing at `HOW_TO_READ_IT_20260903.pdf` at the root, plus the regenerated `_what these are.txt`.
**And both generators now carry it** — `sync_desk_copies.py`'s DOCS list and `make_shortcuts.py`'s
LINKS — so *05 - Refresh printouts* re-dates the copy and the link re-points itself. Doc 146
records the alternative: two links in that folder pointed at documents that had stopped existing
and had been dead for days.

**Date note:** the copy is stamped **20260903** to match Matt's clock, not the container's, which
had already rolled past midnight UTC.
