# 107 — Matt's own strategy is the one the data supports, and the dots cap at two

**Date:** 2026-08-31 · **Matt:** *"When going late QB I tend to find good value and next year's
keeper at the flex spot (5th or 6th pick typically)… Keeping a RB or WR I suspect has better
upside than keeping a QB/TE."*

**Both halves of that are correct, and the second one is correct by a wider margin than he thought.**

## 1. WHERE KEEPERS ACTUALLY COME FROM — n=474 true selections, 2021→24

| round drafted | n | became next year's keeper |
|---|---|---|
| 1–4 | 156 | **0.0%** — ineligible by rule |
| **5–6** | 90 | **12.2%** |
| **7–8** | 96 | **17.7%** |
| 9–12 | 192 | 8.3% |
| 13–15 | 132 | 1.5% |

**Rounds 5–8 is the window, and 7–8 is its peak.** Matt's instinct to hunt his keeper at picks
56/65 is right; picks 80/89 are, if anything, better. 5–6 versus 9–12 alone is not significant
(Fisher p=0.385) — what is unambiguous is that both beat 9–12 and crush 13–15.

**This cuts against how I have been framing round 9.** §4.13's *breakout* value peaks at ADP
121–180; *keeper* value peaks two to four rounds earlier. Those are two different objectives and
they do not point at the same picks. The late darts are a 2026 lottery ticket; the audition window
is the 2027 asset.

## 2. RB OR WR OVER QB OR TE — right, and it is not close

Keep rate by position inside rounds 5–8, times what a keeper at that position is actually worth
(position rank 10, derived from the shipped board, not quoted):

| pos | kept | VBD if kept | **expected 2027 value** |
|---|---|---|---|
| **RB** | 19.1% (9/47) | +79.6 | **+15.2** |
| **WR** | 10.7% (9/84) | +39.3 | **+4.2** |
| QB | **25.0%** (6/24) | +2.3 | **+0.6** |
| TE | 14.3% (4/28) | +0.3 | **0.0** |

**Quarterback is kept the most often and is worth almost nothing when it is.** One starting slot
against twelve startable QBs compresses the value to zero — the same structure that makes QB1 worth
+80 and QB2 through QB12 worth 37 points in total. **An RB audition is worth about 3.6× a WR one
and 25× a QB one.**

So the late-QB plan is doubly right: it buys 2026 points at the flattest part of the board *and*
leaves the audition slots for the position where an audition is worth something.

## 3. THE DOTS CAP AT TWO, NOT THREE — I cut one after checking it

Matt asked whether there is a four-dot player. There is not, and there is no longer a three.

I had scored three "kinds": analysts, role, health. **Health was unearnable** — a NEUTRAL grade
exists only for the five players the injury sheet bothered to clear, so 207 of 212 could never
score it. A dot nobody can earn is not a scale. Dropped; it survives as the standalone `ok` badge.

**And the panel and the podcast calls are ONE kind, not two** — Harmon and Boone sit in both lists,
so counting them separately is the identical double-count I found inside the two CSVs themselves.

So there are **four states: nothing · ● · ●●**, where ● is one kind of side-evidence and ●● is
both — analysts *and* job situation. 13 players carry two. Cap is structural, not arbitrary.

---

**New:** `AUDITION_WINDOW.pdf` — every RB/WR/TE the board expects at picks 56/65/80/89, with
**STARTER** marked (he is RB1/WR1 on his own depth chart, which is the FLEX floor Matt asked for),
the 2027 audition value, and the analyst note where one exists.
