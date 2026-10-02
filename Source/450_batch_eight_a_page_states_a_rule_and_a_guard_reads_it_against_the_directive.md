# 450. BATCH EIGHT: A PAGE STATES A RULE, AND A GUARD NOW READS IT AGAINST THE DIRECTIVE

*29 Sept 2026, 22:05 ET. Claude (Cowork), batch eight: the guard doc 449 named (the wire page said "Tuesday night: put in
claims" for a week after v9.26 set Wednesday, and nothing read it). 450 reserved by listing `Source\` (no doc has landed
since 449). No em dashes.*

---

## 0. WHAT TO DO

1. **`check_page_rules.py` runs in `ff.bat` after the logic check** (`rules` on the RESULT line). It reads the visible text
   of the four pages for twelve retracted phrases and numbers (the Tuesday-night and Sunday-night claim rules, a Tuesday
   run, an unsourced processing day, the two-run week, 5.99 and 5.46, 6.1%, the 96% QB2 capture, the seat curve, the
   claim-order ladder, the 92% Out timing, "stashes cost nothing") and holds the wire page to four live sentences (the
   claim day is Wednesday night, claims execute Thursday morning, a drop on every claim, Add before Claim).
2. **It fired on the drive's wire page as it stands tonight** (two dead phrases, three live sentences missing), and is
   quiet on the trimmed page doc 449 shipped and on the other three pages. Four selftest controls: the 29 Sept routine
   fires, the fixed one does not, a retracted number on the week sheet fires, the live number and day do not.
3. **The first `ff.bat` run on the trimmed builders clears it**; until then `rules 1` is the correct reading of a stale
   page. It is the same `.\ff.bat` already on your list.
4. Nothing else changed: `ff.bat` and `check_locals.py` (its scan list) re-pinned; the new guard pinned from birth.

---

## 1. WHAT IT COVERS AND WHAT IT DOES NOT

The dead list is the directive's DO-NOT-QUOTE table in the page's register, plus the two rules v9.26 replaced. A number is
matched as a whole token (5.99, 6.1%, 73.8%) so an unrelated 15.99 does not fire; a phrase is matched loosely enough to
catch the wording the page used and its obvious rephrasings. The live list is short on purpose: the four sentences the
routine exists to state. A rule that changes in the directive has to be added here by hand, which is the same maintenance
the DO-NOT-QUOTE table already needs; the guard makes the page's copy fail rather than drift.

What it cannot see: a rule stated in a builder's Python comment or docstring (not on a page), a rule paraphrased past the
regex, and a page that is simply not rebuilt (that is `check_pages.py`'s C5 and the RESULT line). It reads pages, not
`sheet_constants.json`; the constants file carries the D/ST bar the sheet prints, and `check_vintage.py` reads the
printed rate against it.

## 2. OPEN, BY NAME

- **Matt's:** `.\ff.bat`; the v9.35 paste; go or no on v9.36; the claim-order runs; the routes purchase; the D/ST box
  score; the Opus chat (blocked).
- **Mine, waiting on events:** the first run after docs 448 to 450 (wire 0, locals 0, rules 0, a sheet on the new engine);
  the Wednesday and 6 October runs; the status pairs from about 20 October; the 4.34 column from week 10; wiring item 7.
- **Mine, runnable:** nothing tonight. Every line on `claude_todo.txt` now waits on a date, an event, or Matt.
