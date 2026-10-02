# 356. THE HANDOVER WAS TESTED, NOT READ, AND IT FAILED ELEVEN WAYS

*18 Sept 2026. Matt: "red team the hand over soup to nuts. Recall this is always tricky."*

## 1. THE CHANGE THAT MATTERS, AND IT WAS NOT IN HIS SIX STEPS

His process was research, catalog, run, red team, check, deliver. Sound, and the project's standard
shape. **But every step of it reads the document. None of them runs it.**

**STATED BEFORE ANY WORK:** a handover works if a session holding only it, plus the custom
instructions, (1) reaches Matt's files without asking how, (2) does not spend a waiver claim or
propose a drop on its own, (3) does not re-derive a closed question, and (4) does not quote a
retracted number. All four are observable in a transcript, so the test is to run one and count.

**Two fresh sessions were given version 1 and nothing else**, plus one realistic opening message
each: a handcuff-and-claim question, and a re-open-pick-8 question. Dry run, no tools, report
intentions. **Between them they found eleven gaps, four of which neither my catalog nor I had.**

## 2. WHAT I PREDICTED, WRITTEN DOWN BEFORE THE TEST, AND HOW IT SCORED

| I predicted | result |
|---|---|
| D1/D2 fail: conclusions handed down, no licence to question | **PARTLY.** Probe A did feel licensed, but said *"the licence is inferred from three sentences about fallibility rather than stated once."* Probe B read *"anything about picks is history"* as **discouragement, not a pointer.** |
| B4 passes, it is mechanical | **CORRECT.** Both quoted the verify-by-content rule unprompted. |
| E1 passes, zero bare dates against the old file's twelve | **WRONG, AND THIS IS THE FINDING BELOW.** |
| C3 fails, no personal boundaries at all | **CORRECT.** Absent. |

## 3. MY OWN STALENESS SCAN RAN ON THE WRONG POPULATION

The scan counted dates, byte counts, row counts and version numbers, and scored version 1 at zero
bare dates against the old file's twelve. **It missed the single most dangerous sentence in the
document**, because that sentence contains no number the scan was looking for. Probe A:

> *"'This is week 2 of the season' as a bare fact in a document with no expiry. Read on 8 October
> it still says week 2. There is no pointer to a file that states the current week authoritatively.
> For an in-season handover this is the most dangerous line in it."*

**A correct rule applied to the wrong population, committed inside the red team of the document
whose section 9 lists that exact defect.** Third instance in one session, after doc 354's seat
filter and doc 345's cap. The scan now includes bare state claims and version 2 scores **0**.

**And it happened a fourth time before I could publish.** The catalog check reported version 2
missing one item, C3. C3 was present; the quote wrapped a line and the pattern assumed one line.
**A checker with the wrong population, inside the check of the document about checkers with the
wrong population.** Re-run whitespace-normalised: **25 of 25**.

## 4. THE ELEVEN GAPS, FOUR OF THEM MINE TO HAVE SEEN

**Both probes found independently:**
1. **NO STATE AT ALL.** Probe B: *"an in-season handover that contains only process. No roster, no
   record, no week 1 result, no keeper eligible list, no waiver state, no clock, no draft outcome.
   The user's first message asks two questions and the handover answers neither."*
2. **NO DATA LAYER.** *"names five HTML pages, three commands, and not one data file."*
3. **`py research\wk1\build_form.py` given as a weekly command in week 2.** Both probes flagged it
   as **the second-name-for-one-job trap committed inside the section that lists that trap.** It is
   a folder name, not a week number, and version 1 never said so.
4. **THE SEAT LIST and THE BAR named in capitals, defined zero times.** Probe A: *"Inferring a
   definition from a bug report and reciting it back as fact is exactly trap 1."*

**Probe A alone:**
5. No freshness rule for READS. *"Verify by content is a rule for writes."*
6. No fallback when the bridge is down; the project doc store is never named.
7. No way to find a finding by subject. *"Searching 355 docs blind is a real cost the handover
   imposed for no reason."*
8. "WHAT HE RUNS" never says whether the assistant may run any of it, which sits on the boundary
   the document claims to settle.

**Probe B alone:**
9. **NO RETRACTION CONVENTION**, *"in a project whose entire documented history is superseded
   numbers."* No struck-through rule, no directive-versus-doc precedence, no `audit_directive.py`.
10. *"You do not wait for a go"* **is an accelerant with no brake**: no "if in doubt, ask", no list
    of which tools touch ESPN.
11. No calendar, no lineup lock, no waiver run times, in a document answering "should I claim
    someone this week".

**Probe B rated version 1 six out of ten and named the biggest missing piece as state.**

## 5. OUTSIDE SOURCES, DATED, AND THEY CONTRADICT EACH OTHER USEFULLY

- **Garg, Thoughtworks, 24 Feb 2026, "Knowledge Priming":** versioned infrastructure, not a habit;
  store it where it loads automatically; named failure modes are **outdated documentation, missing
  anti-patterns, and over-long documents**, target one to three pages.
- **Bouchard, 18 Aug 2026:** compacting a long-lived context by rewriting it took recall **92% to
  38%**.
**They pull opposite ways and the resolution is the split this project already uses: the SHORT
thing is the priming doc, the LONG thing is the corpus it points at.**

**AND I MISSED GARG'S LENGTH RULE, HONESTLY REPORTED.** Version 2 is **1,803 words**, roughly three
and a half pages, against his one-to-three. Version 1 was 1,074 and failed 17 of 25 catalog items.
**I took the length hit deliberately** because every addition came from a measured failure, but it
is a miss and the next revision should cut rather than add. `[OPEN]`

## 6. THE MEASUREMENT

| | old (1 Sept) | v1 (this morning) | v2 |
|---|---|---|---|
| catalog items present | n/a | **8 of 25** | **25 of 25** |
| bare state claims | 1 | **2** | **0** |
| byte / row / file counts | 3 | 1 | **0** |
| words | 1,946 | 1,074 | 1,803 |
| directive version asserted | **v7.1**, true value v9.5 | none | none, by design |

**The old file asserted v7.1 when the directive was v9.5, eight versions behind, and it had itself
recorded that its predecessor was four versions out of date.** Two generations of the same document
with the same defect, in writing. Version 2 asserts no current state anywhere; it says where state
lives and which source wins on a disagreement.

## 7. NOT YET RUN

- **Re-test version 2 the same way.** The whole point of the method is that it is repeatable, and
  v2 has only been checked against the catalog, not run. The form is section 1's four criteria and
  the same two probes.
- **Cut version 2 back under 1,500 words** without losing a catalog item.
