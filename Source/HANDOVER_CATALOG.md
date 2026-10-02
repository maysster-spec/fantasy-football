# THE HANDOVER CATALOG, and the test that decides it

*18 Sept 2026. Shipped on its own before any of it is investigated, so Matt can see the shape and
re-order it (0.5(c)1).*

## 0. THE CLAIM IN ITS TESTABLE FORM, STATED BEFORE THE WORK

> A handover works if a session holding **only** it, plus this project's custom instructions,
> (1) reaches Matt's files without asking him how, (2) does not spend a waiver claim or propose a
> drop on its own, (3) does not re-derive a question this project has closed, and (4) does not
> quote a number this project has retracted.

All four are observable in a transcript. **So the test is to run one and count**, not to read the
document and feel good about it.

---

## 1. WHAT THE RESEARCH SAYS, DATED, AND WHERE IT DISAGREES WITH ITSELF

**OUTSIDE (B7, dates stated before use):**
- **Rahul Garg, Thoughtworks, "Knowledge Priming", 24 Feb 2026.** Treat project context as
  versioned infrastructure, not a habit. Seven sections; store it where it loads automatically
  rather than being pasted. **Named failure modes: outdated documentation creating misalignment,
  missing anti-patterns, and over-long documents.** Its length rule is blunt: **"if a priming doc
  is longer than 3 pages, consider" whether all of it is necessary**, target 1 to 3 pages.
- **Bouchard, 18 Aug 2026** (already cited in doc 351): compacting a long-lived context by
  rewriting it took recall from **92% to 38%**. Summarising is not free.

**These two pull in opposite directions** and the resolution is the split this project already
uses: **the SHORT thing is the priming doc, the LONG thing is the corpus it points at.** The
handover must be short because it is read every time; the 355 numbered docs stay long because they
are read on demand.

**INSIDE, and this is the evidence that counts:**
- **Doc 288, 11 Sept, is the most important finding about handovers in this project and it argues
  against the obvious design.** The directive contains at least eight sentences whose literal
  function is to stop a reader re-opening a question. *"A stranger reading them arrives
  pre-committed against questioning exactly the things that most need questioning ... not that
  context is lost in the handover, but that the WRONG context survives it perfectly."*
- **MEASURED on the handover I replaced today** (written 1 Sept, updated 5 Sept, read 18 Sept):
  it asserts the directive is **v7.1**. It is **v9.5**. Eight versions.
- **And it documents its own predecessor failing the identical way:** *"Its own previous version
  was four directive versions out of date and pointed at five paper sheets that had been retired,
  which is the exact failure it was written to prevent."* **Two generations, same defect, in
  writing.** That is not a risk to guard against; it is the base rate.

---

## 2. THE CATALOG. Twenty items in seven groups.

### A. SCOPE, because "new chat" is three different documents
- **A1** State WHICH handover this is: a chat inside this project (inherits v9.5 automatically), a
  chat outside it (inherits nothing), or another model. Name what the reader already has.
- **A2** Say what to do when this file is stale, in the file, at the top.

### B. CAPABILITY: can the reader act on turn one?
- **B1** Reach Matt's files without asking him how. Tools named, both folder paths, no prose map.
- **B2** The one command he runs, and the ones he does not.
- **B3** The pages he reads, by filename.
- **B4** How to verify a commit, and why the commit result is not the verification.

### C. SAFETY: what must it never do?
- **C1** The four categories that stop and ask, with the reason each is irreversible.
- **C2** Style constraints that are his, not taste: no em dashes, numbered list first, the page
  carries the number and not the provenance.
- **C3** Standing personal boundaries he has stated, quoted rather than paraphrased.

### D. EPISTEMICS: the doc-288 problem, and the group most likely to be got wrong
- **D1** Does NOT hand our conclusions down as instructions.
- **D2** Says explicitly that the directive's "do not re-open" clauses are **claims with evidence
  behind them**, names where the evidence is, and says a fresh reader is allowed to test them.
- **D3** States his record on his own hunches honestly: 12 confirmed or partly confirmed, 1
  underpowered his way, 7 null. **Never opens with the assumption his idea will die.**
- **D4** The three answers he is owed: TESTED with the number, NOT YET RUN with the form written,
  BLOCKED naming the exact missing input.

### E. STALENESS: the measured failure, twice over
- **E1** Zero bare dates, byte counts, row counts and version numbers, except where a version IS
  the fact.
- **E2** Every "what is true right now" claim replaced by a pointer to the thing that GENERATES
  the truth.
- **E3** One command the reader can run to find out the current state for itself.
- **E4** Under three pages.

### F. TRAPS: the anti-patterns Garg says are the most-omitted section
- **F1** The recurring defect shapes, each with a doc number as EVIDENCE rather than as authority.

### G. VERIFICATION, and this is the part the old process did not have
- **G1** **THE LIVE TEST.** A fresh agent, given only the handover and a real task, judged on the
  four criteria in section 0. Reading the document is not testing it.
- **G2** The missing-row check: every catalog item above found in the artifact **by name**.
- **G3** The staleness scan re-run on the final artifact, against the old one as the control.

---

## 3. WHAT I EXPECT TO FAIL, WRITTEN DOWN BEFORE THE TEST

Pre-registering this so the result cannot be read generously afterwards.

- **D1 and D2 are where I expect my own draft to fail.** What I shipped this morning has a section
  called "the four traps this project keeps falling into", which is exactly the shape doc 288
  warns about: conclusions handed down, evidence left behind.
- **B4 I expect to pass**, because it is mechanical.
- **E1 I expect to pass**, because the scan already shows 0 bare dates against the old file's 12.
- **C3 I expect to FAIL**: what I shipped has no standing personal boundaries in it at all.
