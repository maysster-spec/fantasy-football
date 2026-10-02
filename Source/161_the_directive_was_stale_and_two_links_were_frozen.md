# 161 — Auditing the directive against the files, and two desk links nobody was re-dating

*Sept 3 night. Matt: "verify project directive is correct · any recent changes that could use a
red team · prior we did stepped go through, would that help?"*

---

## 1. THE DIRECTIVE, CHECKED AGAINST THE SHIPPING FILES — 6 of 35 CLAIMS WERE WRONG

`Scripts\research\audit_directive.py` recomputes every load-bearing number in the doc from the
files that actually ship. Nothing is read off the doc. First run: **29 ok, 6 FAIL.**

**What passed** (worth stating, because it is most of it): the fourteen pick numbers against
`CLE.MY_PICKS`; all four §4.1 replacement levels to 3 dp; the eleven quoted VBDs — Gibbs 162.31,
Nacua 131.28, McCaffrey 134.94, Bowers 51.20, McBride 47.65, Andrews 0.00, St. Brown 101.33,
Allen 80.31, Lamar 33.02, Stafford 21.19, Warren 28.08; `CAPS = {QB:2, TE:2}`; the nine-file kit
plus the five-file extension; and `Espn_pull_projections.py` at exactly 15,194 bytes.

**What failed, and it is all one cause: `refresh_adp.py --write` re-froze the market on the 09-03
pull at 13:18 on Sept 3, and §2.1(c) had been solved on the 08-23 ADPs.** Re-solved as the same
fixed point on the current keeper ADPs
`[28.2, 29.4, 29.4, 32.9, 41.0, 42.2, 42.4, 44.2, 45.1, 47.3, 78.7, 101.6]`:

| pick | keepers ahead | effective ADP available | the doc said |
|---|---|---|---|
| **32** | **4** | **~36** | 3 / ~35 |
| **104** | **12** | **~116** | 11 / ~115 |
| **113** | **12** | **~125** | 11 / ~124 |

The other eleven rows are unchanged. Also corrected: §4.14's sentinel counts, **327 of 480** rows
(not 323) with **~153** carrying a real draft position (not 157) — the blob moved from ADP ~158 to
~170 with the new freeze.

**The irony is in the doc itself.** §2.1(c) closes with *"Anyone planning pick 32 off the v4 table
was one player too deep."* One refresh later the v5 table was one player **shallow** at the same
pick, for the same reason. **This table is a function of the ADP freeze and must be re-solved
whenever `refresh_adp.py` writes — including after Sept 5.** That sentence is now in the doc, and
the audit script is the check. Directive is at **v7.1**; re-run: **51 ok, 0 FAIL.**

**A defect in my own audit, caught before I reported it.** My first pass read the board's
`gone_ahead` column as if it were the table and reported a false failure at pick 41. That column is
**per player** — how many keepers are ahead of *him* — not per pick. §2.1(c) says in terms that the
table is a fixed point; solving it the way the doc says it was solved is what made pick 41 pass.
**A wrong measurement of a right number is still a wrong finding.**

---

## 2. THE RED TEAM THAT MATTERED WAS THE ONE ON THE DESK FOLDER

Tonight's code changes were each verified as they were made — the live board through the render
harness after every edit, `make_board.py` by measuring the rendered pixels, `apply_research.py` and
`mark_rookies.py` against their own guards. What had **not** been checked was the pair that runs on
Saturday morning: `sync_desk_copies.py` and `make_shortcuts.py`.

**Cross-checking every numbered link against what sync actually re-dates found two that nothing
regenerates:**

```
   ok    06 - Draft board          -> DRAFT_BOARD_*.pdf
   STALE 07 - Value ladder         -> VALUE_LADDER_*.pdf
   ok    08 - Draft card           -> DRAFT_CARD_*.pdf
   STALE 09 - Override card        -> OVERRIDE_CARD_*.pdf
```

`make_shortcuts.py` has linked both since they were built; neither was ever added to
`sync_desk_copies.py`'s DOCS. **They are not dead links — which is the problem.** A dead link you
notice. These open a real document, frozen at whatever date it was last built by hand, sitting
beside four links that re-date on every refresh.

**It was live tonight:** `VALUE_LADDER_20260903.pdf` at the root is the **18:12** build — the one
*without* the fifteen news rows added at 19:40 (doc 155 §2). Every time Matt clicked *07 - Value
ladder* this evening he opened the ladder without the news.

**Fixed** — both added to DOCS, so they are generated and swept like the rest. **And made a test:**
`Scripts\research\audit_desk.py` cross-checks every link prefix against that list and exits
non-zero if one has no generator. Doc 146 found the first version of this defect (two links to
documents that had stopped existing); this is the second; the check exists so there is not a third.

---

## 3. YES — AND THE STEP-THROUGH IS ONE COMMAND, NOT FIVE

**`01 - Check everything`** (`weekend_check.bat` → `weekend_check.py`) already is the stepped
go-through, and it covers one of the two remaining open items:

| step | what it proves |
|---|---|
| `board_audit.py` | the VBD, ranks and engine rules are arithmetically right |
| `check_kit.py` | every file is the one it should be — **this is where tonight's re-pins get confirmed** |
| `cookie_jar.py --check` | the ESPN cookies will survive to Sept 7 |
| `verify_prerank.py` | ESPN holds what the file says, row by row |
| **`fetch_keepers.py --dry`** | **§8 open item #2 — the poll against live data** |

Then **`rehearsal.bat`** is the other half and the one that shows tonight's work on his own screen:
it starts a local server answering in ESPN's exact shape and runs the **real** `live_draft.py`
against a draft that changes — same poll loop, same renderer, same browser. It reaches the pick-152
and pick-161 pages and the completion panel, which `--replay` returns before ever seeing. Nothing
touches ESPN.

**So: `01 - Check everything`, then `rehearsal.bat`, then `py live_draft.py --replay 2025`.**
Those three between them close everything except a live draft room.
