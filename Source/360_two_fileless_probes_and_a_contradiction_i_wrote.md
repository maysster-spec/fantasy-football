# 360 - Two fileless probes, and a contradiction I wrote into the handover

**2026-09-18. Matt: *"I thought we needed another fable run. Please look back and verify."* He was
right, doc 358 says so in its own text, and the verification turned up more than the missing run.**

---

## 1. VERIFIED: THE RUN IS OWED, AND DOC 358 SAYS SO IN WRITING

`358_the_reader_is_a_tool_list_not_a_name.md`, line 63, carries `[OPEN]`:

> **What the pass does NOT establish: that a reader with no bridge and no directive succeeds.**
> Fable had both. **The untested population is a chat outside this project, and it is the one Matt
> is most likely to open from his phone.**

**And a second reason doc 358 does not state: Fable tested VERSION 2. Version 3 has never been
tested by anyone.** Eight edits to a document read by strangers, and §0.2's rule is that a fix which
has not been exercised is not verified.

**Why neither surfaced: the to-do item `[x] SEND FABLE THE HANDOVER TEST` is ticked, so from Matt's
side the job reads as finished, and `open_threads.py` (which scrapes `[OPEN]` markers out of docs)
has not been run since 9 September.** The marker existed, the scraper that would have surfaced it
was idle, and the tracker said done. Matt caught it from outside. **That is §0.5(e)'s tracker
failing in the one way §0.5(e) did not anticipate: not a missing marker, an unread one.**

---

## 2. SO I RAN THE FILELESS HALF MYSELF (§0.4). TWO PROBES, SIX DEFECTS.

**POPULATION: a fresh session on its first turn holding ONLY `00_START_HERE.md` v3, with no drive,
no bridge, no project docs and no directive. Explicitly told to call no tool.** That is doc 358's
`[OPEN]` population exactly, and it is the one Fable cannot test because Fable has the bridge.
Two probes, two different roster questions, marked against the same five questions.

**BOTH PROBES INDEPENDENTLY NAMED THE SAME WORST SENTENCE.** Section 1 of v3:

> *"The freshest `WIRE_<date>.csv` and `FREE_UNRANKED_<date>.csv` name today."*

**They do not. They carry the day `ff.bat` last ran**, which with four scheduled runs can be four
days back, and on a Sunday morning the freshest wire is usually Thursday's. **The sentence sits four
lines above the freshness rule that contradicts it.** A reader following it literally answers a
Sunday question against a Thursday pool, with confidence, having obeyed the file. Probe B: *"the
warning and the defect are adjacent and the defect is the half written as a method."*

**THE THREE I COULD VERIFY, AND ALL THREE VERIFIED:**

| probe finding | check | result |
|---|---|---|
| §0's no-bridge fallback says use the Google Drive connector | directive SECTION 9 step 3, line 2177 | **CONFIRMED CONTRADICTION.** It says *"Do **not** reach for the Google Drive connector for file work, it pulls whole files into context and is the most expensive channel available."* **I wrote a fallback the governing document forbids, into the branch aimed at the reader who has no other option** |
| §6 calls `MY_ROSTER.csv` *"his fourteen"* while §2 says roster 15 | `wc` on the file | **15 data rows.** "Fourteen" was the draft-selection count leaking into a roster description. It lands on the exact question it breaks: a reader who believes he has 14 concludes a spot is free and no drop is needed |
| *"a drop can cost the player AND his 2027 keeper eligibility"* over-applies | directive line 610 | **CONFIRMED.** *"Trade and free-agency acquisitions are ineligible regardless of draft round."* A dropped waiver pickup costs nothing in 2027, so the blanket warning defends bodies with no keeper value |

**THE ONE THAT MATTERS MOST TO MATT, AND NEITHER FABLE NOR THE CLAUDE PROBES FOUND IT.** Probe B,
on its own reply: it correctly refused to name a drop, and then handed Matt a rule for picking one
himself.

> *"The document draws its boundary at EXECUTING a write to ESPN, not at RECOMMENDING one, and those
> are not the same thing... **Nothing in the document says 'do not name the drop.'** I inferred it.
> A less cautious reader would not have."*

**It is right, and §3's "do not wait for a go" plus §10's "one recommendation, not a menu" actively
push the other way.** A fresh reader produces a bench name from memory, Matt drops him, and the
file's boundary was never technically crossed. **v4 closes it in terms.**

**TWO MORE, BOTH REAL:** a fileless reader has **no date route at all** (§1's only method needs the
bridge, and probe A guessed the week off its own clock and said so); and §9's *"anything you ask him
to run goes in `matt_todo.txt` the moment you say it"* is **impossible without write access** and
had no carve-out, so probe A flagged it and probe B wrote *"if I go quiet, that item is lost."*

**AND A CREDIT, because the null is a result:** both probes refused to name a player, both stated
their file access plainly, neither invented a path, and both used §6's file table to ask for exactly
the right four files. Probe A: *"that table is the single most valuable thing in the document for a
reader in my position."* **Criteria 2, 3 and 4 pass on the fileless population too.**

---

## 3. WHAT SHIPPED: v4

`Source\00_START_HERE.md` is **version 4**. v3 archived to `2026\_archive\00_START_HERE_20260918_v3.md`.
Nine changes: the six above, plus the IR block (three slots, and this project has never written down
what they cost, including whether IR time breaks "rostered all season"), plus the waiver mechanic now
flags BOTH halves rather than one (an unmarked sentence beside a marked one reads as verified), plus
§4's four commit rules cut because they went into the directive's SECTION 9 this afternoon and were
duplication I created six hours earlier.

**LENGTH, STATED BECAUSE IT WENT THE WRONG WAY: 1,978 words, against v3's 1,707 and v2's 1,974 that
Fable called too long.** Six fixes cost about 466 words and I cut about 195 back. **I did not cut a
section to make room, because the two probes are a roster-shaped population and the sections they
did not use (§7 live-vs-dead numbers, §9 what is open) serve a research-shaped one. Cutting on their
silence would be the §0.6 error.** `[NOT YET RUN, form stated: does a reader at ~2,000 words miss
something a reader at ~1,700 catches? The next test measures it by giving one reader each.]`

---

## 4. THE ANSWER TO HIS QUESTION

**Yes, a Fable run is still owed, and it must come AFTER v4, not before.** Sending a tester a
document with six known defects spends its run re-finding them.

**And the kit needs rewriting first, because it is stale in four places** and `FABLE_HANDOVER_TEST.md`
is still the v2 article: its PART C lists eleven already-found gaps when there are now 25; its PART D
asks whether 1,970 words is too long, which v3 already answered; its opening tells Fable *"you have
no bridge to Matt's Windows drive... you cannot test the criterion"* which was **false on the day**
(doc 357 records Fable running it WITH the bridge); and its PART B question 4 asks *"which of the
three kinds of reader in section 0 are you"* when v4 has no three kinds of reader, it has a tool-list
test. **Rewritten kit is the next thing, and pasting it is Matt's.**
