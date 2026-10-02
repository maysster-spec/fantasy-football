# 340 THE BRANCH THAT HAD NEVER RUN, AND THE STALE PAGE BEHIND IT

**2026-09-17, 03:50.** Matt ran `py wire.py --html` and it died:

```
NameError: name 'E' is not defined
  wire.py line 1276, in write_page
```

**One character of mine, in a branch nothing had ever executed, hiding two days of a stale page and
one untrue sentence about him.**

---

## 1. THE DEFECT

Line 1276 called `E(", ".join(_wa))`. The escape helper in this file is `_esc`, defined at line 390
and used everywhere else, including thirteen lines above at `_esc(m)`. **One occurrence, one letter.**

**WHY IT HAD NEVER FIRED.** The line only runs when `waiver_ahead` is non-empty, which means only
when Matt is NOT first in the waiver order. Doc 311 wrote it. `--html` had not been run since.
Tonight ESPN returned `you are 7 of 12; ahead of you: TURD, DUCK, WGTS, POT, FLEM, ???` and the
branch executed for the first time in its life.

**AND IT CRASHED AFTER `WEEK_SHEET.html` WAS ALREADY WRITTEN**, so the run was half-successful and
the console said so, which is the honest behaviour. The week sheet is current; the wire page is not.

## 2. THE STALE PAGE THE CRASH REVEALED

`THE_WEEKLY_WIRE.html` on the drive is dated **15 September**, not 16. Doc 310 made the week sheet
build by default and left `--html` gating the wire page alone, correctly, and Matt has been running
the default. **So the wire page has been two days old and nothing said so.**

Reading it confirms the chain: it still carries **"you are near the back of the line"**, the exact
hard-coded string doc 311's comment says it must never say again. The replacement has never
rendered. `[SOURCED: THE_WEEKLY_WIRE.html, 15 Sept]`

## 3. THE SECOND ONE, FOUND BY LOOKING RATHER THAN BY THE CRASH

Doc 311 replaced one hard-coded claim about his waiver position and **left another**, at line 1140,
in the byes section: *"The wire for a position gets picked over the moment everybody needs it, and
you pick near the back."*

**He is 7 of 12. The middle.** And the order resets every week to inverse standings, so **any fixed
claim about where he picks is wrong by construction, not merely wrong this week.** Section 3's rule
is the one that was skipped: when a finding invalidates a metric, enumerate every downstream use
rather than patching the spot where it surfaced.

Rewritten to keep the advice and drop the claim: *"and the order resets every week to inverse
standings, so you cannot count on being early. The answer to a bye is bought two or three weeks
ahead, when nobody is bidding."*

## 4. HOW IT WAS FIXED AND PROVED (section 0.2)

1. **Negative control FIRST.** The original expression was evaluated on his exact data and does
   raise `NameError: name 'E' is not defined`. The crash is reproduced before the fix is written.
2. **The real object, not an equivalent one (doc 80).** His file tree was rebuilt in the container,
   `wire.py` and `sheet_engine.py` beside each other with `Source\` as their sibling so the module's
   own `SRC` resolves, the module imported, and the production `write_page` called on the real
   281-row `WIRE_20260916.csv` with his real order `(7, 12, [TURD, DUCK, WGTS, POT, FLEM, ???])`.
3. **Verified by NAME on the rendered artifact (section 0.5c5), not by exit code.** Three checks,
   three passes: the page contains `This week you are 7 of 12, and the 6 teams who pick before you
   are TURD, DUCK, WGTS, POT, FLEM, ???`; it does NOT contain `near the back`; and the bye advice
   survives. All five team codes present, and `???` survives escaping.
4. Archived, committed, re-pinned: **`wire.py` 109,683 / `61e044440478a1a6`**.

## 5. THE GUARD THAT IS STILL MISSING, WITH ITS FORM WRITTEN DOWN

**NOT YET RUN: a control in `redteam_controls.py` that renders the page with a NON-EMPTY
`waiver_ahead` and asserts the team codes reach the artifact by name, plus its negative control
(empty `waiver_ahead` must produce the "first of N" sentence, and a missing order must produce the
honest silence).** All three branches exist in the code and exactly one of them has ever been
executed. That is the pattern this project already has a rule for, applied to a rendered sentence
rather than to a step: **a branch that has never run is not a feature.**

**AND THE SEARCH THAT SHOULD BE PART OF IT:** a scan for any bare single-capital-letter call in
the page builders. There are now zero in `wire.py`; nothing checks that there stay zero.

## 6. WHAT IT COST

One command of his, at four in the morning, after he had already filed his claims. **This is the
section 0.4 failure in its most expensive form: he had to debug my code.** The two days of stale
page cost nothing he acted on, because the page he actually reads every week is the sheet.
