# 105 — One tie-breaker mark, and why it is a count and not a score

**Date:** 2026-08-31 · **Matt:** *"there is a difference between 'buy' and 'BUY'… is there a way to
add a consolidated confidence level so it's easier to make a tie-breaker call on the spot."*

He is right that there was a problem. By this morning a player could carry four unrelated
positives — our two residualised panels, named analyst calls, a depth-chart backup role, a clean
injury grade — with nothing telling him whether one of them or all four were true.

## WHAT I BUILT

The right-hand mark now carries **dots for how many separate lists point the same way**, and the
badge gets brighter with them: `BUY ●` is dim, `BUY ●●●` is bright. Same word, three intensities,
so it reads without counting. Hover lists exactly what agreed.

Current spread across 212 graded players: **53 at one dot, 24 at two, 4 at three**
(Jonathon Brooks, Tyler Allgeier, Chris Rodriguez Jr., De'Zhaun Stribling). A top tier of four is
the right shape — if it were forty it would mean nothing.

## WHAT I DELIBERATELY DID NOT BUILD

**A confidence score.** A 0–100 number would have been easy and it would have been the most
dangerous artifact in this project. §4.13d is explicit: **nothing here measures any of these
signals against outcomes.** A score implies calibration that does not exist, and it would arrive
at the one moment — 60 seconds on the clock — where he cannot audit it. A count of agreeing lists
is honest about being a count.

Two further honesty constraints are baked into the code:

1. **The dots are capped at 3 and two of the lists share people.** Matt Harmon and Justin Boone
   sit in both the panel and the podcast calls, so three dots is not three independent opinions.
   That sentence is in the docstring and on the card.
2. **Red silences green.** An AVOID or an ESPN OUT removes the positive badge entirely, and a
   player analysts are fading shows no green either. Netting a positive against a negative is how
   you get a bright mark on a player who is hurt — that is exactly the Tank Dell failure from
   doc 97, and this closes it structurally.

`[TESTED]` 15 assertions: never more than two marks on a row; AVOID silences the edge on Kittle,
Kraft, Charbonnet, Dell and Love; an ESPN OUT does the same; healthy BUY players keep their mark;
DART stays invisible before pick 104 and appears at 104; the tooltip names both the agreeing lists
and the analysts.

## AND THE OTHER THING HE LIKED — reachability, made explicit

He singled out the *"goes at 20 — gone before your pick 32"* framing from doc 103. Both paper
sheets now carry a **your move** column that converts `eff_pick` into an instruction: **take at
89 · take at 104 · take at 113 · … · waiver.** Nothing to work out on the clock, and it makes
"you can wait" visible rather than inferred.

---

**Files:** `live_draft.py` · `player_context.csv` (now carries `calls_up`, `calls_down`, `who`) ·
`DRAFT_CARD.pdf` legend rewritten · `LATE_RB_SHEET.pdf` and `ANALYST_CALLS.pdf` gain **your move**.
