# 359 - The trigger had a dead calendar in it

**2026-09-18. Matt: *"I thought I requested that red team jobs are run after significant milestones
and I count this as one... I still want shortest path for me so I don't need to repeat requirements
and get it wrong time after time."* He is right, it is measurable, and the cause is not what either
of us would have guessed.**

**STATED BEFORE TESTING (§0.5a2): the claim in its testable form is (1) the red team in this project
has fired unprompted at some rate, measurable from each catalog doc's own header, and (2) §0.5(d)'s
trigger table contains, or does not contain, a row that would have fired on today's event.** Both
are countable. Neither needs an opinion.

---

## 1. THE RATE. 0 OF 4.

**POPULATION: every red-team catalog doc in `Source\`, read at its own opening lines, where each one
states its trigger. n=6.**

| doc | date | trigger, in the doc's own words |
|---|---|---|
| 78 | 30 Aug | **self** - *"Why now: `live_draft.py` was rewritten six times today"* |
| 100 | 31 Aug | Matt, quoted: *"Red Team, this is still number one priority"* |
| 173 | 5 Sept | Matt, quoted: *"If you see one roach there could easily be 100"* |
| 227 | 8 Sept | Matt, quoted: *"this is what I meant by you researching strategies"* |
| 305 | 13 Sept | *"Matt asked for three things"* |
| 356 | 18 Sept | Matt, quoted: *"red team the hand over soup to nuts"* |

**§0.5 was added 2026-09-05 (v7.3). Since the rule has existed: four catalogs, four of them his,
zero mine.** The one that ever fired on its own predates the rule by six days. `[TESTED, n=6]`

§0.5's own opening sentence is *"He should never have to ask for the red team. If he is asking, the
trigger below was missed."* **It has been missed every time, and nobody counted until now.**

---

## 2. THE CAUSE, AND IT IS NOT NEGLIGENCE. THE TABLE HAD A DEAD CALENDAR IN IT.

§0.5(d) holds six trigger rows. Five fire when a SCRIPT runs: `refresh_adp --write`, a doc
correcting a doc, a research batch closing, a printed artifact rebuilding, and me claiming something
is done. **Nothing in this project runs a script when a document ships.**

The sixth row, the only time-shaped one, read:

> **a milestone date arrives** (T-7 / T-2 / T-1 / lock / draft)

**Every one of those five dates passed on 7 September.** From 8 September onward the table had no
row that could fire on the passage of time, and it said nothing about being empty. **Eleven days,
two canonical files shipped, no trigger.**

**THE RULE THAT COMES OUT OF IT: A TRIGGER NAMES AN EVENT, NEVER A DATE.** A date-shaped trigger
expires on its own and takes the rule with it. An event-shaped one cannot.

**OUTSIDE, DATED (B7): ekline.io, 20 May 2026**, on runbook decay, and it names the same failure in
different words: link a runbook line to a live system fact *"so that when systems change, the
breakage becomes visible rather than silent."* It prices a 10% stale-step rate at doubling incident
recovery time. **Our stale-step rate in that table was one row in six, and the cost was the whole
rule.** It also recommends **game days**: run the runbook end to end rather than reading it, which
is doc 356's finding about the handover arriving from outside on a different object.

---

## 3. HIS SECOND ASK: THE OUTSIDE CHECK, AND WHY EVERY RED TEAM HERE HAS BEEN HALF A RED TEAM

*"That red team should include standard and optimal best practices."*

**§0.5(c)'s five steps are all internal: catalog, batch, overview, collision check, missing-row
check. Every one compares this project to itself.** They can find a file disagreeing with another
file. They cannot find a thing nobody here has thought of. The only outside-facing rule anywhere was
B7, which governs DATING a source already fetched, not going to get one.

**§0.5(c) gains step 6, and its own record argues for it:** §4.30's receiver composite came off a
PlayerProfiler article; the handover rewrite came off Bouchard and Garg; this section's fix came off
ekline. **Three of the project's better recent moves came from one search each.**

**BLOCKED, input named (§0.5a4):** Red Hat Emerging Technologies, *"Building skills for AI agents:
pitfalls and best practices"*, 28 July 2026, is directly on point and would not fetch (too many
redirects). Not retried by another route, per the fetch rules. Worth one attempt next session.

---

## 4. HIS THIRD ASK: THE FIX GOES IN THE INSTRUCTION, NOT THE LEDGER

*"Examples of errors while performing transition to a new chat are also in need of consideration...
That is if that information is implemented and not left in the chat or otherwise not fired."*

**Seven errors were made today while writing the handover. Four reached `00_START_HERE.md`. Three
were file-handling lessons with nowhere to go, because SECTION 9 had no rules about writing at all,
and they were about to end the session as chat:** verify a commit by content and not by its result;
a fresh container path per commit, because re-committing different content from the same path inside
about two and a half minutes sends the old bytes with no error; and preserve line endings, because a
read/write round trip silently turned `ff.bat` from CRLF to LF. **All three are in SECTION 9 now,
alongside the concurrency rule.**

**OUTSIDE, DATED (B7): incident.io, 16 April 2026**, on why post-mortem action items fail. Five
named causes; this project has hit three: no named owner, **the wrong tracking tool, where *"actions
in separate documents get forgotten when isolated from daily workflow"***, and **zero follow-up
cadence, where *"actions silently expire after the debrief ends."*** Its recommended fix is not a new
ceremony but review at an existing one, *"just two minutes."* Ours already exist and none of them is
the ledger: this directive, `matt_todo.txt`, and `ff.bat`.

**§0.5(f) is new and says it in one line: the ledger is the RECORD, the instruction is the FIX. If
the only artifact of a mistake is a ledger row, it did not fire.**

---

## 5. THE RED TEAM THAT WAS OWED, RUN. ONE DEFECT, ONE CLEAN PASS.

The milestone is the v9.5 defrag plus `00_START_HERE.md` v3. Neither had been adversarially checked.

**PASS: every cross-reference survived the defrag.** Eight references to SECTION 6 exist in the
file; six sit outside it and all six point at doctrine that STAYED in SECTION 6 (the QB/TE doctrine,
the audition rule, the same-bye trap, TE-is-a-different-question). No reference points at a finding
that moved. No finding heading is duplicated. `[TESTED]` Two references, §4.22e and §4.23a, name
lettered subsections that are not themselves headings; cosmetic, recorded, not fixed.

**DEFECT: the v9.5 header quoted three byte counts and all three were wrong.** It claimed SECTION 4
= 77,146, SECTION 6 = 9,067, and a total *"unchanged at 155,833."* Measured on the shipped file:
**77,340, 9,391 and 157,141.** Nothing was tampered with. **The counts were taken before the
paragraph was written, and then the paragraph was added to the file it was describing.**

**A SELF-DESCRIBING FILE CANNOT QUOTE ITS OWN SIZE.** That is SECTION 8's *"never quote a count from
prose"* arriving in a second place, and the shape of it is §0.2's: the claim was true when made and
false when shipped, and nothing re-checked it. **The line-multiset equality is the proof that
actually carries the defrag and it is untouched.** The three numbers are removed from the header and
the correction is recorded there.

**This is exactly the class of thing the trigger existed to catch, and it sat in the file for five
hours because the trigger could not fire.**

---

## 6. WHAT SHIPPED

`Source\00_PROJECT_DIRECTIVE.md` is **v9.6**. v9.5 archived to
`2026\_archive\00_PROJECT_DIRECTIVE_v95_20260918.md`.

1. **§0.5(c) step 6** - the outside check, one batch of every catalog.
2. **§0.5(d)** - the dead calendar row replaced by three event rows: a canonical file ships, a week
   of the season closes, Matt asks something already answered in the file. Plus the rule above the
   table: a trigger names an event, never a date.
3. **§0.5(f)** - new. Where a lesson goes, as a table, with the case that earned it.
4. **SECTION 9** - four rules for writing to Matt's drive.
5. **The v9.5 header** - three byte counts removed and the correction recorded.

**NOT YET RUN, form stated:** `audit_directive.py` fires on any edited directive number (§0.5d).
The numbers edited here are the header's own byte counts, not §4.14's, which is what that script
reads, so it would pass vacuously. **The gap is that no checker reads the header's self-claims.**
The testable form: a check that recomputes every byte count and section size the directive asserts
about itself and fails on mismatch. Queued, not built.
