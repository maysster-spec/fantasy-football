# 312 -- the list he works from is 43% finished work, and the tracker is 48 docs behind

**15 September 2026.** Matt: *"we've had to go back and grab several things we discussed prior. If
you still have the catalog let's red team that."*

**He is describing a symptom and the cause is measurable. Three defects, all the same shape as doc
310's flag: a mechanism exists and nothing invokes it.**

**THE CLAIM IN ITS TESTABLE FORM, written before the measurement (0.5a2):** the catalog and
`OPEN_THREADS.md` record items but nothing picks them back up, so NOT YET RUN is a terminal state
rather than a queue. **Measured: every open item's state against the live artifacts.**

---

## 1. TWELVE OF THE TWENTY-EIGHT OPEN LEDGER ROWS ARE ALREADY DONE

`AUDIT_LEDGER.md` carries **51 rows: 23 CLOSED, 28 OPEN.** Checked against the shipping files he
rebuilt this morning:

| row | what it claimed | state in the artifact today |
|---|---|---|
| 22, 24 | the wire names an OUT man as the inheritor | fixed; Jordan James is ACTIVE now, so naming him is correct |
| 28 | section 0 sorted on season points | THIS WEEK and the CALENDAR are both on the page |
| **38** | the wire's team came off the frozen board | **7 rows read "moved to X", none carries a job number** |
| **39** | Green Bay's job worth 152 | **reads 241; no file anywhere carries 152** |
| **40** | the starter's status rendered on the BACKUP's row | **"questionable now" sits beside McCaffrey, "out now" beside Jacobs** |
| **43** | the bye followed the old club | **all seven corrected: Kaleb Johnson GB 11, Dortch BUF 7, Demercado DAL 14** |
| 46, 47, 49 | no in-season input; the 20-club build; the page cannot read it | all three verified this session |
| 48 | "worth 8.7 **a week**" | the phrase is gone from the page |
| 50 | the sheet behind `--html` | the sheet rebuilt at 11:29 from plain `py wire.py` |

**Twelve of twenty-eight. Every one of them said "OPEN: closes on Matt's next run." He ran it.
Nothing re-read the condition.** A close condition nobody evaluates is not a condition.

**So the list he works from is 43% finished work**, which is precisely why the live items get
found by memory in conversation instead of by reading the list. His symptom, explained.

**The sixteen that are genuinely open:** 19, 20, 21, 25, 26, 27, 29, 32, 33, 34, 36, 37, 41, **42**,
45, 51. Row 42 is confirmed live by measurement, not assumption: `WIRE_20260915.csv` is still sorted
strictly descending on the frozen preseason VOR.

## 2. THE OTHER TRACKER IS SIX DAYS AND FORTY-EIGHT DOCS BEHIND

`OPEN_THREADS.md` was **generated 9 September 18:23** and its highest referenced doc is **260**.
`Source\` now holds **doc 311**. **Docs 264 through 311 are not in it at all.**

**And it has no trigger.** 0.5(e) describes `open_threads.py` as *the* tracker; **0.5(d)'s milestone
table, which is where triggers actually live, does not list it.** Nothing in the weekly sequence
runs it. `matt_todo.txt` renders at the TOP of that file, so his own to-do list has not reached the
rendered tracker since 9 Sept either, even though I have been writing to the source file all week.

## 3. THE LEDGER HAS A COLUMN BUILT FOR EXACTLY THIS AND NOTHING HAS EVER READ IT

Its fifth column is headed **`grep tokens`**. Its entire purpose is mechanical re-checking. **No
script in this project reads the ledger.**

**And when I wrote rows into it today I broke the one thing that would make it readable.** Row 46
carried an unescaped `|` inside a quoted grep expression, splitting it into **13 cells against a
10-column header** -- so the first checker ever written would have mis-parsed my own row first.
Fixed; 51 of 51 rows now parse.

---

## 4. SHIPPED: `Scripts\research\close_check.py`

Reads the ledger, takes each OPEN row's grep tokens, searches the **shipping artifacts** and sorts
every open row into three buckets:

- **CANDIDATE CLOSED** -- the defect text is gone from every artifact. **Never an automatic close**:
  it names the row and a human decides. Doc 305 records what happens when I rule on a verdict
  instead of filling in the terms.
- **STILL THERE** -- found, and the file is named.
- **NO GREP TOKENS** -- the cell is `n/a`; it needs judgement and says so.

**IT SEARCHES CODE AND PAGES, NOT PROSE.** Every doc in `Source\` *describes* the defect it
retracted, so grepping the `.md` files would find every token inside the very document that killed
it. Scripts, HTML, CSV, JSON and TXT only.

**THREE GUARDS, ALL RUN AGAINST THE DEFECT THAT MOTIVATED THEM (0.2):**

| planted | result |
|---|---|
| a row whose token is absent | reported CANDIDATE CLOSED |
| a row whose token is live in `Scripts\live.py` | reported STILL THERE, file named |
| **a row broken by an unescaped pipe** (row 46's defect) | named, with its cell count, never skipped |
| **a corpus of 0 searchable files** | **exit 1.** A checker that searched nothing must not report all clear, and that is the single most dangerous output this script could produce |

It also reports `OPEN_THREADS.md`'s staleness against the newest doc number in `Source\`, so the
second tracker's silence stops being invisible.

## 5. WHAT THIS DOES NOT FIX

- **It names candidates; it does not close them.** Deliberate, and the human step is the point.
- **It cannot run `open_threads.py` for him.** The regeneration still needs a command, and nothing
  in the weekly sequence fires it. **The real fix is a trigger, and that is a directive edit**
  (0.5d's table), which doc 289 holds for one pass.
- **`open_threads.py` scrapes docs for markers; the ledger is a table.** Two trackers, two formats,
  neither reading the other. Merging them is a bigger job and is NOT YET RUN.

## 6. OPEN

**NOT YET RUN:** the trigger for both trackers in 0.5(d)'s table. **NOT YET RUN:** term 4 of 4.32,
the rival-need model, testable form on paper in doc 254 since 9 Sept and untouched since.
**NOT YET RUN, raised by Matt today and smaller than term 4:** the page ranks a claim by what the
man adds and says nothing about which hole the wire can refill later, where 4.16's table measures
QB at 62% against RB at 22%. **STILL OPEN, unchanged:** rows 19, 20, 21, 25, 26, 27, 29, 32, 33,
34, 36, 37, 41, 42, 45, 51.
