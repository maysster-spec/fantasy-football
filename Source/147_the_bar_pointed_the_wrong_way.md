# 147 — The bar pointed the wrong way, twice

**2026-09-03, evening. T-4 days.** Matt: *"clean up and simplify the layout of the live board as
we did with the ladder. Red team the layout and see if it can be made more fit for purpose and
user friendly."*

**Scope discipline, stated first: every change in this doc is inside `render()` and `CSS`.
Nothing touched the engine, the ordering, the rollout or the recommendation.** Proof is in §4 —
the same twelve players in the same order with the same costs at five draft states, before and
after.

---

## 1. METHOD — look at it before saying anything about it

A layout claim is a claim (§0.2). So the first step was to build the real page, not to reason
about the source: a harness that constructs the production `Engine`, synthesises a plausible room
(everyone takes the best remaining by keeper-depleted ADP, Matt takes the engine's own #1) and
calls **`live_draft.step()` — the production path** — at picks 8, 23, 32, 104, 128 and 152, then
screenshots each at 1600×1000.

That is §5.5's rule applied to a page instead of a DataFrame. Reading the render code would not
have found the two defects below; both are only visible once the pixels exist.

---

## 2. THE TWO REAL DEFECTS — both are doc 79 recurring

Doc 79 caught this once already, in these words: *"Showing Δ there let the largest bar on the page
belong to a row the engine did not pick."* It was fixed in the headline. **It was still true in
the table, in two separate places.**

**(a) The `wait cost` bar. `[MEASURED on the rendered page]`** Directive §7 says in terms that
this column is *"Tempo. NOT the sort key."* It was drawn as a filled green bar — the most
saturated element in the table. On the rendered pages the longest green bar sat on:

| state | longest `wait cost` bar | that row's rank |
|---|---|---|
| pick 23 | Quinshon Judkins −21.9 | **row 5** |
| pick 104 | Pat Freiermuth −13.6 | **row 12, last** |

The eye goes to the biggest bar. The biggest bar was on the row the engine ranked last.

**(b) The VBD bar was drawn from `abs(vbd)`.** From roughly pick 89 on, **every VBD on this board
is negative** — that is what replacement level means. `abs()` therefore inverted the encoding:
at pick 104 the longest blue bar marked Pat Freiermuth at **−33.9**, the worst player on screen,
and Jared Goff at −15.2 (the recommendation) had one of the shortest.

**FIX: one bar on the page, on `cost vs #1`, drawn as distance behind row 1.** Long = worse.
That is the only encoding of this quantity that cannot be read backwards. Row 1 is `free` and
draws nothing.

**(c) And the heading named the wrong column.** It read *"ordered by cost vs #1 … the amber column
is what your own call would cost."* The amber-styled header was `wait cost`. Whichever half Matt
believed, one of them was wrong. `cost vs #1` is now the amber one and the sentence matches it.

---

## 3. FIVE MORE, IN ORDER OF WHAT THEY COST ON A 60-SECOND CLOCK

**3.1 The legend cost ~150px on every refresh and pushed the panels under the fold.** Six
paragraphs of reference prose sat between the board and the two panels that are actually used on
the clock — position cliffs and the roster. At 1600×1000 both were cut off. It is now a closed
`<details>`; one click, and the guide carries the same words. **Measured: the cliffs and roster
panels are fully on screen at 1600×1000 after the change and were not before.**

**3.2 The RUN flag fired on a non-event.** The bar was ≥3 of the last 6 at one position — the
*ordinary* state of a 12-team draft. At pick 8 it announced **"RUN: 3 RB, 3 WR in the last 6"**,
i.e. all six picks, styled as a warning, in the headline beside the recommendation. A warning that
is always on is not a warning. Now ≥4 of 6, and only the position actually running is named.
After the change it correctly stays silent at picks 8, 23 and 32 in the harness.

**3.3 doc 139 pinned the board and left the column beside it free to grow.** The `gone` list ran
from 0 rows to 18 over the first two rounds, so the page still changed height for the same reason
and at the same cost the board used to. Fixed at 8 rows, padded — the same by-construction fix.
Eighteen names was more than the room needs anyway: ESPN's own draft room lists every pick, and
what this column is *for* is the last few, which is what the RUN flag reads.

**3.4 `still there?` on row 1 answered a question nobody is asking.** Row 1 is being taken now.
An **8%** sitting next to the recommendation at pick 8 reads as a warning about the pick. Now `—`.

**3.5 The waiting screen said the same thing three times and nothing useful.** *"planning for pick
32"* + *"Your next turn is pick 32."* + the clock box's *"you in 9"*. Waiting is the only time in
the hour Matt has time to read, and the two facts worth reading were already computed and already
on the page: **who he would take if the board froze** (row 1) and **which position falls off a
cliff before he gets there** (`eng.cliffs`). The panel now promotes both. Nothing new is computed.

---

## 4. THE TIE BAND — the one addition, and it is doc 139's own number

doc 139 fixed the words **clear ≥ 6 · slim ≥ 1.5 · a coin flip** below that, and used them in the
headline. The board never used them, so eleven rows all read as one shade of "worse". The same
threshold now applies per row: inside **1.5** points of the recommendation the engine cannot
separate them, and the row is marked `tie`.

`[TESTED — where it fires, across all twelve of Matt's picks in the harness]`

| pick | 8 | 17 | 32 | 41 | 56 | 65 | 80 | **89** | 104 | **113** | **128** | 137 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rows marked tie | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **1** | 0 | **3** | **6** | 0 |

It is silent at pick 8 (margin 12.3) and fires only in the late rounds — which is exactly what
doc 139 measured when it said more compute does not find a winner there. At pick 128 the headline
reads *"a coin flip"* and six rows carry the tag: the board saying **this one is yours, not mine.**

---

## 5. EQUIVALENCE — the engine did not move

Five draft states, rendered through `step()` before and after:

| state | pick | row 1 | order identical | shape |
|---|---|---|---|---|
| clock_08 | 8 | Amon-Ra St. Brown | **YES** | 12 + 3 |
| wait_23 | 23 | Jeremiyah Love | **YES** | 12 + 3 |
| clock_32 | 32 | Kyren Williams | **YES** | 12 + 3 |
| clock_104 | 104 | **Jared Goff** | **YES** | 12 + 3 |
| dst_152 | 152 | Broncos D/ST | **YES** | streamer page |

All twelve names, in order, with identical `cost vs #1` strings, at every state. §7's fixed shape
(12 player rows + 3 tier rows) holds everywhere.

Incidental confirmation, not a finding: at pick 104 the engine takes **Jared Goff** unprompted,
which is what §4.18's v6.6 draft-night rule says to do.

---

## 6. ONE MISTAKE MADE AND CAUGHT IN THE SAME HOUR

The collapsed legend's arrow was written as `content:"\25B8 "` in a non-raw Python string. **`\25`
is a valid Python OCTAL escape**, so Python produced a control character and left `B8` behind, and
the summary rendered as `⊟B8 what do these columns mean?`. It shipped into the first screenshot.

This is the exact trap written into `00_START_HERE.md` §5 an hour earlier — *"use raw strings in
docstrings that contain Windows paths"* — in a place that rule did not name. **Widen it: any
backslash inside a non-raw Python string is a bug waiting for a digit.** Fixed by using `▸`,
which Python resolves to the character itself so the CSS never sees a backslash. Verified with
`python3 -W error::SyntaxWarning`.

Caught because the page was screenshotted rather than reasoned about — the same reason §1 exists.

---

## 7. WHAT WAS DELIBERATELY NOT DONE

- **No column was removed.** `adds now`, `if I wait` and `wait cost` are arithmetically redundant
  (Δ = adds now − if I wait) and a case can be made for dropping one. Not four days out: they are
  in the guide, on the card and in Matt's head, and the cost of them is a little width, not a
  wrong read. Post-draft.
- **No threshold in the engine was touched**, including `TIER`, `rollout_inner` and the 1.5 / 6
  words — 1.5 and 6 were *reused*, not chosen.
- **`_lineup` still has no absence model.** §4.18c's instruction stands: post-draft.
