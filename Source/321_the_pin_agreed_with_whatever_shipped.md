# 321 — The pin agreed with whatever shipped

*16 September 2026, 08:05. Written after landing the two code changes Fable held (docs 319 item 5
and 320 section 4) and finding, on the way in, that the file I was about to edit had lost a
feature I shipped eight hours earlier and told Matt to go and use.*

---

## 0. DO THIS

1. **Re-run `py wire.py`.** The sheet you built at 3:11 this morning has no claim-order bands on
   it. That is my defect, not a data problem, and it is fixed.
2. **Nothing about your three claims changes.** Schultz at priority 1 is still the recommendation
   and the reason is unchanged: +6.1 to your starting nine and it fixes week 6.
3. **A number you can now read off the page: what a bye-week fill is worth against the man you
   would claim instead.** The tight ends the page priced at 6.1 to 6.7 are worth 1.2 to 2.0 that
   way. Fill week 6; do not agonise over which body fills it.
4. **From the week-3 sheet the depth charts re-rank themselves** on carries plus targets. Nothing
   moves this week, by design.
5. Optional, one minute: `py research\redteam\redteam_controls.py` — 56 of 56.

---

## 1. WHAT HAPPENED

Doc 314 shipped on 15 September: the room files on **workload**, and the one number that predicts
how many rivals claim a man is targets plus carries in his **last completed game**. It went into
`wire.py` in three places and into `sheet_engine.py` as the contested band.

At 02:01 on 16 September I applied doc 316's four fixes to `wire.py`. The base I edited was a
staging copy that had already reverted — ledger row 56, the fifth occurrence of the same trap.
Doc 316's work landed. **Doc 314's work was deleted.** The file went to the drive at 101,831
bytes, I recomputed its pin, and `check_kit` reported OK.

Matt ran it at 03:11. `WIRE_20260915.csv` has no `touches` column. `WEEK_SHEET.html` contains the
word "contested" **zero times**.

**Nothing fired, and the reason nothing fired is a rule I wrote.** `contest()` returns two empty
strings when a man has no workload on file, because a missing number must never print as
"nobody is racing you for him" (doc 251). That is correct and it stays. It also means the entire
feature can vanish and the page will look normal.

---

## 2. THE PIN IS NOT A CONTENT CHECK, AND ITS COMMENT SAID SO OUT LOUD

`check_kit.py` carried this beside the pin, from 02:02 this morning:

> *doc 314: `load_form()` now returns the LAST COMPLETED GAME beside the cumulative row, and
> `touches` rides onto every free row*

Of a file that contained none of it. **Re-pinning after an edit makes the checker agree with
whatever I shipped.** A pin proves a file has not changed since I pinned it; it proves nothing
about what is in it, and a comment written from intent rather than from the file is worse than no
comment, because it reads as verification.

What found this was **reading the artifact** (§0.2, §0.5c5): the CSV header, and a `grep -c` on the
page. Fifteen seconds, and I had not done it.

---

## 3. THE GUARD, AND THE HOLE IT CAME OUT OF

`redteam_controls.py` has run a full tree against a recorded pool since doc 291. Its
`PAGE_INPUTS` list has eleven Source files in it, and **`form_2026.csv` was never one of them**.

**A control tree that omits an input cannot see a defect in the code that reads it.** Every check
passed all morning on a page whose workload lane was switched off, because the harness never gave
it a form file to read.

`form_2026.csv` is a page input now, and **C21** asserts, on the real object:

| check | what it catches |
|---|---|
| the wire file carries a `touches` column at all | the exact regression above |
| it is filled on 20+ rows | a column of blanks, which is the same defect one step later |
| the sheet prints a contested band on at least one pickup | the join dying between the two files |
| planted 40 for the season and 3 in the last game — the column says **3** | reading the cumulative row, which would put a man two bands too high |

**Run against the shipped code, C21 fails all four.** `[TESTED]`

---

## 4. THE TWO CHANGES FABLE HELD

**Doc 319 item 5 — the week-6 fill prints both ways.** `tot` charges an empty slot at zero, which
is what put four tight ends inside 0.6 points of each other and made the choice among them look
like a decision. The sentence now names the second figure, netted at the position's measured
waiver rate (doc 12, in the constants' absence block). Schultz: **6.1 against nobody, 0.6 against
the tight end you would claim instead.**

**IT IS A FLOOR AND IT IS NOT DOC 319's NUMBER.** Fable's 1.2 also credits Schultz for the weeks
LaPorta is absent, drawn at the measured rates. The page sees byes only, so it cannot count those
weeks. Same direction, smaller. Guarded by **C20**, which compares the two figures in the same
sentence — the first version of that check asserted "under 6", which is doc 319's tight end and
nothing else, and it failed on correct output when the first such row turned out to be a defence
at 19.6. A hard-coded expectation taken from the example that motivated a change is not a test
of it.

**Doc 320 section 4 — `usage_depth()`.** Shipped as written, with two corrections, both the same
shape: **a team with no usage signal must come out untouched.** Fable's draft took `lead` as `''`
when no man on the team had a usage row and then wrote it over every row's `ahead`, deleting the
man ahead for a whole backfield — a printed column and the gate on §4.27's inheritance list — and
renumbered the chart depths before that check. Both now sit inside an early `continue`.

**And doc 320's own control could not have passed as specified.** It says *"assert `next_man_up()`
names the depth-3 man"*. It cannot: a man who leads his team in touches becomes depth 1, and
`next_man_up()` filters to depth ≥ 2. The object doc 320 measures is the **inheritor**, so the
fixture makes him second. Indianapolis, planted: Taylor 25 touches, McGowan 14, Giddens 2.

| arm | what the page names at IND |
|---|---|
| one completed week | **DJ Giddens** — the chart's depth 2, and no re-rank announced |
| two completed weeks | **Seth McGowan** — the usage order's depth 2 |

`[TESTED]` C19 and C18. Today the file holds one completed week, so **nothing moves until the
week-3 sheet**, which is what doc 320's own week-2 tie (62.5%, n=8) says it should do.

---

## 5. WHAT IS OPEN

- **`redteam_controls.py` is not pinned.** `check_kit` scans `Scripts\` and `Scripts\live_draft\`
  and nothing else, so the harness that guards both pages is itself unguarded. **NOT YET RUN.**
  Testable form: a third folder group in the manifest, run against his tree before it ships —
  a false FAIL on his machine is the §0.4 failure this project keeps paying for.
- **The lanes are still mixed in one sort.** Doc 319 makes the tight-end fill an empty-slot
  number; the drop costs and the bet lane are streamed numbers; Priority pickups ranks all three
  together. Item 5 fixes the sentence, not the sort. Neither doc covers it. **NOT YET RUN.**
- Fable's own list: the bet-lane version of B1, the RB drop-versus-add swap table, and whether the
  inheritor's *share* is predicted better by usage than his *name*.
- Unchanged from doc 315: the D/ST and kicker versions of the contest bands, and whether the bands
  survive into 2026.

---

## 6. THE RULE THIS ADDS

**After any edit to a file that another file reads, check the CONSUMER's artifact by name, not the
producer's exit code and not its pin.** The pin and the comment beside it both agreed with a file
that had lost a feature. One `head -1` on the CSV it writes would have caught it before Matt ran
anything.
