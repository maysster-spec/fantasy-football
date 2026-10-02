# 337 FOUR TIMES I DESCRIBED THE ARTIFACT INSTEAD OF OPENING IT

**2026-09-17, overnight.** Matt: *"You have taken several flights of fancy lately. I can't even make
sense of this, can you?"* He was quoting a sentence of mine about how his three waiver claims would
process. It was nonsense, and it was the fourth instance in one session of a single fault.

---

## 1. THE FOUR

| # | what I asserted | what was true | the artifact I did not open |
|---|---|---|---|
| 1 | *"There is not one defence on the wire page. Zero rows."* | The page has a defence section heading ten teams over weeks 2 to 5, with his Browns marked `(yours)` at second | `THE_WEEKLY_WIRE.html`. I grepped `WIRE_20260916.csv` |
| 2 | Week 2 defence ranks quoted as current | `dst_week1_2026.csv` is built from `play_by_play_2025.csv.gz` alone, written 11 Sept, and holds no 2026 football | `Scripts\research\build_dst.py`, eight lines of which say so |
| 3 | *"the tooling missed the week 6 tight end pair"*, then a claim recommended to fix it | The page flagged it four weeks out: *"one empty TE slot, and a one-week pickup fills it. No trade is needed for a single hole"*, priced at 9 points | the same page, a few hundred bytes further down |
| 4 | *"only the first claim that clears will happen, Brooks and Schultz do not process"* | Ranking decides which claim gets his real priority. **The DROP decides which claims can happen.** Two claims naming the same drop are one bet; a claim naming a different drop is a separate transaction and can land as well, at worse priority | the same page again: *"in a hedge the first one that lands is also the one that eats the seat"* |

**All four are the same fault: I described an object from a proxy rather than from the object.**
A CSV standing in for a page. A file name standing in for its builder. Memory standing in for a
paragraph I had quoted correctly forty minutes earlier.

## 2. WHY THE EXISTING RULES DID NOT CATCH IT

Section 0.5(c)5 already says *"after any build that produces a printed or rendered artifact, verify
that the rows which must be on it ARE on it, by name."* **It is scoped to builds.** Three of the
four above happened while READING, with no build in sight, so the rule never applied.

Section 0.2's *"an exit code is not a result"* is the same shape and is also scoped to a step that
ran. Section 1.1 is about ADP provenance specifically. **None of them covers "I am about to tell
Matt what an artifact says."**

## 3. THE GUARD, AND IT IS BEHAVIOURAL BECAUSE THERE IS NOTHING TO EXECUTE

**BEFORE ASSERTING WHAT AN ARTIFACT CONTAINS OR LACKS, OPEN THAT ARTIFACT.** The page, not the
CSV behind it. The builder, not the output's filename. The paragraph, not the memory of it.
**Specifically:**
1. **A claim that something is MISSING requires opening the thing it is missing from.** A grep on a
   sibling file is not evidence about a page.
2. **A number quoted to Matt carries the date of the DATA, not the date of the file.** `build_dst.py`
   reads one season. That belongs in the sentence.
3. **"The tooling missed X" is a claim about the tooling and needs the tooling's output in hand.**
   Three times out of three this session the tooling had not missed it.
4. **A mechanic that is written down is quoted, never paraphrased.** Section 0.5(a2) already says
   this about Matt's words. It applies to our own pages too.

## 4. WHAT IT COST AND WHAT IT DID NOT

**Cost:** four corrections in one night, each one arriving after he had already read the wrong
thing, and one of them after he had filed on it. **Not cost:** any of the four changed a decision
that survived correction. Start the Browns, spend no defence claim, cancel Schultz, hold Vele and
Brooks are all the same recommendations after the corrections as before, which is luck rather than
method.

**The pattern Matt named is real and it is the one to watch: the errors were all confident, all
specific, and all about things sitting in a file I could have opened in one command.** An unmeasured
severity claim is section 0.4's named defect; this is its reading-side twin.

## 5. ERROR_PATTERNS ENTRY

**A20 THE PROXY READ.** Describing an artifact's contents from a neighbouring file, a filename, or
memory. Four instances 2026-09-17. Distinct from A19 (one board state quoted as general) because A19
is about generalising a real measurement and this is about not having made one. Guard is section 3
above, behavioural, no code.
