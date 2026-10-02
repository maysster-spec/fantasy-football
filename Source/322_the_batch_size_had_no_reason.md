# 322 — The batch size had no reason, and the cap is not where I put it

*16 September 2026. Matt, twice: "what is the reasoning again to ask Gemini Notebook to only process
5 video/podcast files at a time. What was the risk and can you back up that claim? How many are safe
to run at once?" The second asking is the defect: doc 318 had already answered the first half and I
did not surface it.*

---

## 0. DO THIS

1. **The instruction changed: TEN ticked sources at a time, not three to five.**
2. **And the number is no longer the rule. The CHECK is: the CSV must carry at least one row for
   every source you ticked.** A ticked episode missing from the output means the response ran out
   of room. Halve that batch, re-run it alone. Two clean tens in a row, try fifteen.
3. **A number that must not be quoted any more: "three to five." It never had a source.**
4. **Batch size does not spend your quota. It spends your evening.** Pro is 500 chat queries a day
   and 250 episodes at five a batch is 50 runs. The old instruction was costing time, nothing else.
5. **Ten-minute A/B on your to-do list** and it settles this properly.

---

## 1. WHAT THE CLAIM WAS, AND WHAT WAS BEHIND IT

`GEMINI_HITRATE_PROMPTS.md` said *"Extract, three to five ticked sources at a time"* with no reason
attached, in the file or anywhere else. **Doc 318 already found that and said so in terms: "there is
no measurement behind it. I cannot back it up."** It is an unsourced instruction of exactly the class
§0.2 forbids, sitting inside a procedure Matt runs by hand.

Separated by what each rests on:

| the reason | what it is |
|---|---|
| a long CSV can be truncated by an output ceiling | **mechanically real, never measured here** |
| a bad batch of five costs five re-runs, not fifty | **true by arithmetic, needs no measurement** |
| attention dilutes across many transcripts | **a hunch with nothing behind it** |
| the first corpus run stopped at 29 links against a 5x14 grid | **adjacent, not about batch size** — a model under-delivering on a large open-ended ask, which is why the prompt now demands a grid with MISSING in every hole |

---

## 2. THE PRIMARY SOURCE SAYS THERE IS NO SUCH CAP

Both pages read in full on 16 Sept 2026, not from search snippets (his standing rule).

- **No documented limit on sources per query and none on response length.** Google's own help page
  says only that sources are *"always used in either the entire set or the subset you select."*
  `[SOURCED: support.google.com/notebooklm/answer/16269187, page carries no date]`
- **The documented caps are per NOTEBOOK and per DAY.** Pro: **300 sources a notebook, 500
  notebooks, 500 chat queries a day, 20 audio overviews a day.** Free is 50/100/50/3 and Plus is
  100/200/200/6. `[SOURCED: support.google.com/notebooklm/answer/16213268, change notice dated 2 Sept 2026]`

**AND THIS KILLS THE ARGUMENT I WAS ABOUT TO MAKE.** I had started writing that small batches burn
his daily query allowance. On the free tier that would be true and close to binding, 50 runs against
50 queries. **He is on Pro, which the procedure file itself records, so the cap is 500 and the
quota argument is worth nothing.** Caught before it shipped, by reading his own file.

Every SEO page returned by the first search (elephas.app, superlore.ai, sourclip.com, notebooktoolkit
and five more, all titled "NotebookLM Limits 2026") was skipped unread. They are the dated-
intermediary failure mode, and Google publishes the numbers itself.

---

## 3. WHAT REPLACES IT

**A fixed batch size is the wrong shape of answer, because the thing that can go wrong is
observable in the output.** The prompt already instructs the model to name any ticked source it
cannot read. So the instruction is now: **ten at a time, and the CSV must name every source you
ticked.** Missing source means the response was truncated, and the fix is local to that batch.

That is §0.2's own rule applied one level up: a step that cannot do the thing it is named after must
fail visibly, or the step after it must check the artifact rather than trust the run.

**Ten rather than five is not a measurement either, and it is not presented as one.** It halves the
paste-and-wait cycles, it is bounded by a check that catches the one real failure mode, and nothing
known argues against it.

---

## 4. NOT YET RUN, WITH THE TESTABLE FORM AND THE COST

> **CLAIM IN ITS TESTABLE FORM:** on one season notebook with the shipped PROMPT 2, rows returned
> PER SOURCE and the share of rows carrying a real citation are the same for a batch of 15 as for a
> batch of 5.
> **FALSIFIER, fixed first:** if 15 returns fewer rows per source, or drops sources by name, or
> carries a lower citation share, the batch ceiling is real and lands between 5 and 15.

**Cost: two chat queries and about ten minutes**, not the evening doc 318 estimated. Tick five, run
PROMPT 2, save. Tick fifteen including those same five, run PROMPT 2, save. Both files to me; the
comparison is mine. On `matt_todo.txt` as of today.

---

## 5. THE PROCESS POINT, WHICH IS THE LARGER ONE

He asked this question twice. The first time it arrived mid-turn while I was in the middle of a
claim-order answer, and I folded it into prose instead of answering it. **Doc 318 had the honest
answer written down a day earlier.** An answer that exists in a doc and does not reach him when he
asks is the same defect as not having it, and §0.5(a4) is explicit that a mechanism gets one of
three labels. This one had label two, NOT YET RUN, and he was never handed it.
