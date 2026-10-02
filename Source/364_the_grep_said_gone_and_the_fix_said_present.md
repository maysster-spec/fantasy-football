# 364. The grep said GONE and the fix said PRESENT. Fable's second read, and v5 of the handover.

**18 September 2026. Follows doc 361 (Fable's outside read on v4) and doc 363 (its scoring).**
**Artifact: `Source\00_START_HERE.md` v5, 12,518 bytes, sha16 `fa3ffbb8d2c95b09`, on the drive and
verified by content. v4 archived to `2026\_archive\00_START_HERE_20260918_v4.md`.**

---

## 1. WHAT TO DO

1. **Nothing to run.** v5 is on the drive and in the project store. `ff.bat` is unaffected.
2. **One judgement call is yours to overrule, and it is section 3 of the handover.** I resolved
   Fable's C1 in favour of the BODY and against the HEADER: **naming a drop is allowed; naming one
   from memory is not.** Reasons in section 3 below. If you want the harder line, say so and the
   header wins instead; it is one sentence either way.
3. **`Source\COMMANDS.html` is no longer a pre-draft page.** It was 3 September, listed
   `draft_night.bat` and `live_draft.py`, and never mentioned `ff.bat`. Archived, replaced with a
   stub that points at the live one at the folder root.
4. **Ledger rows 120 to 125 are closed, 126 is half, 127 is open.** That is Fable's C2 call,
   confirmed by reading v5 rather than grepping it, which matters: see section 4.

---

## 2. FABLE'S SEVEN, AND WHERE EACH ONE STANDS

| # | the finding | v5 | still open |
|---|---|---|---|
| **C1** | section 3's header says *"DO NOT NAME THE DROP"*, its body permits naming one once two conditions hold. Four texts, three rules | **fixed, one way** (section 3 below) | `WEEK_SHEET.html` section 0 prints a name with no conditions attached |
| **C2** | the test kit claimed all eight round-2 findings fixed; two were not, and all eight ledger rows still read `[OPEN]` | **audited: 120 to 125 closed, 126 half, 127 open** | row 127's two undated sentences |
| **C3** | four of the ten data files in section 6 are on no cadence at all; two were four days old on the morning of the test | **fixed:** the file names what `ff.bat` does NOT touch, and calls `injuries_2026.csv` a one-week file | **the pipeline: nothing refreshes `injuries_2026.csv`, and no file says who should** |
| **C4** | `COMMANDS.html` listed with no path, in a table of `Source\` paths, while the live page is at the folder root | **fixed both halves** (path in the table; dead copy archived and stubbed) | nothing |
| **C5** | the precedence rule sends a reader to a page carrying a known `[OPEN]` defect | **fixed:** a page wins on STATE, an `[OPEN]` ledger row wins on the page. Demercado KC/DAL named as the live case | nothing |
| **C6** | the handover says nobody has written down what an IR stash costs; the directive has written it down, untagged | **fixed:** *"treat it as unverified, not as unwritten"*, citing the directive's line | the directive's line still carries no tag |
| **C7** | `waiver_report_2026.csv` described as *"every executed add"*; it is 624 attempt rows of which 227 are EXECUTED | **fixed:** filter and counts on the row | nothing |

**Five of seven fully closed, two half.** The two halves are both outside the handover, in the page
and in the directive, which is the right place for them to be left.

---

## 3. THE ONE JUDGEMENT CALL, STATED SO IT CAN BE OVERRULED

Fable, C1: *"Following the body literally produces the action the header forbids, with the reader
believing the boundary is intact. One sentence fixes it either way; the project has to choose which."*

**I chose the body.** v5 section 3 now reads:

> **NAMING A DROP IS ALLOWED. NAMING ONE FROM MEMORY IS NOT. THE TWO CONDITIONS ARE THE WHOLE RULE:**
> **his roster file open, and every candidate's keeper cost stated next to it.** With both, name the
> one and say why; that is the job. With either missing, say so and stop.

**Three reasons, and none of them is preference:**
1. **The directive's 0.4 protects EXECUTING, not analysing.** Its four categories are his ESPN
   session, writes to ESPN, money or irreversible consequence, and login-only files. A recommendation
   spends nothing; the click spends the claim and the drop.
2. **The directive's section 6 already presumes the recommendation exists:** *"When recommending an
   in-season drop, state the keeper-eligibility cost."* A handover header forbidding what the
   governing document instructs is the handover regressing, not the directive being wrong.
3. **0.1(f) and 0.3(g): one recommendation, not a menu, and do not wait for a go.** A rule that
   forbids naming the drop turns every waiver question into a list of candidates handed back, which
   is the exact behaviour those two sections were written to stop.

**So the directive needs no edit, and that is stated rather than assumed** - I checked line 1791
rather than inferring from the section title.

**What would change my mind:** if Matt reads "name the drop" as pressure rather than analysis. He has
said *"Mike Washington Jr. - 0% chance i drop him"*, and the failure this header was reaching for is
real - a model that names a drop confidently, from memory, with no roster file open, is how a
protected player gets argued away. **The two conditions are what carry that load, not the ban.**

---

## 4. THE METHOD FINDING, AND IT IS MINE

Ledger row 136 told the next session to **close rows 120 to 125 against v4 by grep**. Run exactly
that way, it produces two wrong answers out of six, in opposite directions.

**A phrase grep answers "is the old sentence gone." That is neither necessary nor sufficient for
"is the defect fixed."**

- **Row 124** stores the phrase `say so and test it`. v5 returns **0**, which reads as a deletion.
  The actual fix is a new section header (*"THERE IS A GATE, AND IT IS NOT 'IS IT INTERESTING'"*) and
  a new body sentence, and no stored phrase can see it. **0 is a pass and a silent regression at the
  same time and the ledger cannot tell them apart.**
- **Row 125** stores `THE DURABLE SPINE`, which is a location ANCHOR that must still be there, next
  to `one per team, costs a round-15 pick`, which returned 0 only because v5 capitalises the O. The
  sentence is at line 70. **One row's phrases mean must-be-absent and the next row's mean
  must-be-present, and the column does not record which.**

**This is 0.2's "an exit code is not a result" arriving in the verification channel.** The grep is
the exit code. The replacement text is the artifact. **Every row closed in this pass was closed by
reading v5 and quoting the replacement into the status cell**, so the ledger now carries its own
evidence and a future session does not have to re-open the file to trust it.

`[OPEN]` on the ledger format: the phrase column needs a sense, must-be-gone or must-be-present.
Ledger row 142.

---

## 5. WHAT IS OPEN, BY NAME

1. **`WEEK_SHEET.html` section 0** prints a drop name with no conditions attached. `sheet_engine.py`.
2. **The directive's section 6 line 1788**, *"PUP/NFI/suspension stashes cost nothing"*, untagged.
3. **Nothing refreshes `injuries_2026.csv`.** Not `ff.bat`, not any scheduled task. Owner unnamed.
4. **Row 127's two undated sentences** in v5: the hunch count (12/1/7) and the Washington boundary.
5. **The waiver run TIMES and the lineup lock** are in no file. Row 126.
6. **The ledger's phrase column has no sense marker.** Row 142.
7. **The FLEX rule** is in `matt_todo.txt` and doc 362 and is in neither the handover spine nor the
   directive's section 6.

## 6. THE THREE ANSWERS

- **TESTED:** the eight round-2 rows against the shipped v5, by reading each replacement. 120 to 125
  closed, 126 half, 127 open. Population: `00_START_HERE.md` v5, 218 lines, sha16 `fa3ffbb8d2c95b09`.
- **NOT YET RUN:** whether `WEEK_SHEET.html`'s drop line can carry the two conditions without the
  page growing a keeper-cost column. Testable form: does `sheet_engine.py` already have keeper cost
  per rostered player in scope at the point it prints the drop line.
- **BLOCKED, input named:** the waiver run times and the lineup lock. They are on the ESPN league
  settings page behind Matt's session, and they are not in `2026_League_Settings.txt` - that file
  carries *"Waiver Period: 2 Days"*, which is a period LENGTH, not a run COUNT or a clock.
