# 323 — The notebook cited a page that does not say it

*16 September 2026. Matt forwarded Gemini Notebook's own offer to drive the extraction with a
`Next` command, and asked whether to take it. Answer: yes, with one guard. But the message it came
wrapped in contains a fabricated citation, and that is the part worth writing down.*

---

## 0. DO THIS

1. **Take the `Next` offer.** It removes the re-paste and the re-ticking, which is the whole cost
   of the job.
2. **THE GUARD: every batch must name every source it says it did.** Its bookkeeping is a state
   claim, not a feature. The CSVs are the record; its count is not.
3. **Tick the batch anyway**, even though it says you need not.
4. **Keep saving per-batch CSVs.** Do not let it append into one growing note.
5. **A claim that must not be quoted: that Google's documentation recommends smaller source
   subsets. It does not.**
6. **Fixed on your side:** the link block is a fenced code block now, so the `##` no longer rides
   along when you bulk-paste URLs.

---

## 1. THE FABRICATED CITATION

Gemini Notebook told Matt:

> *"Google's documentation highlights that while a notebook can store up to 50+ sources, asking
> the model to perform dense, multi-field extractions across dozens of long transcripts
> simultaneously dilutes retrieval accuracy. The recommendation from both Google's usage
> guidelines and model architecture best practices is to run granular extraction tasks across
> smaller, targeted subsets."*

**I read both Google pages in full the same morning, for doc 322. Neither says any of that.**

| what it claimed | what the pages say |
|---|---|
| Google documents a dilution effect across many sources | **No such statement.** The source page says only that sources are *"always used in either the entire set or the subset you select."* `[SOURCED: support.google.com/notebooklm/answer/16269187]` |
| Google recommends smaller subsets for extraction | **No such recommendation exists on either page.** |
| "a notebook can store up to 50+ sources" | 50 is the FREE tier. Matt is on Pro: **300**. `[SOURCED: support.google.com/notebooklm/answer/16213268, change notice dated 2 Sept 2026]` |

**AND THE HONEST OTHER HALF, because this is not a claim that it is wrong about the world.** The
context-rot literature it gestures at in its first paragraph is real and published, and doc 322
already conceded that output truncation is a mechanical risk. **Its conclusion may well be
correct. Its evidence is invented.** Those are different failures and only the second is
disqualifying: a right answer with a fake citation cannot be checked, extended, or safely reused,
and the next reader has no way to know which half to trust.

**It is also the exact failure mode Matt named as his own standing rule** — say whether a claim
came from a loaded page or a snippet, and name the intermediary and its date. He was handed a
snippet-shaped assertion wearing Google's name.

---

## 2. THE OFFER ITSELF IS GOOD, AND THE RISK IS ONE SENTENCE

> *"I track progress automatically... we have completed 15 sources... I maintain a list of what
> has been done and what remains."*

**That is a state claim about its own memory across turns, and nothing documents it.** If it
drifts, the output is a repeated episode or a missing one — **and there is no error either way**,
which is the same silent-degrade shape as every defect this project has caught in its own code
this week.

**So the guard is not "distrust it," it is "make the output self-checking."** Every row carries
its source. Every batch names the sources it claims to have finished. The per-batch CSVs are the
record. At the join I detect a duplicate or a gap in seconds, and a miscount costs one re-run of
one batch. **On those terms its bookkeeping does not have to be reliable to be useful.**

**One internal contradiction, flagged because it is the tell.** The same message says selection is
optional (*"leave all sources selected if you wish"*) and that retrieval across many sources
dilutes accuracy. Both cannot be true. Ticking the batch costs one click.

---

## 3. THE `##` DEFECT WAS MINE

Matt: *"the file you gave me has these markdown indicators, ##, those block me from pasting all of
the YouTube links at once."*

PROMPT 1 asked for the URLs *"under a heading that is just the year"* — so the model emitted
`## 2021` above each block, and the heading came along with the bulk paste into Add source.
**The spec was already careful about bullets, numbers and titles inside the block, and then put a
markdown heading directly above it.**

Fixed: **one fenced code block per season, the year as plain text on the line ABOVE the fence,
never a heading and never inside the fence.** A fence also gives him the one-click copy.

---

## 4. WHAT CHANGED ON DISK

- `GEMINI_HITRATE_PROMPTS.md`: the fenced link block; the `Next` workflow with its guard and the
  tick-anyway correction; the manual ten-at-a-time path kept as the fallback; the fabricated
  citation recorded so no future session inherits it.
- `TAKES_CORPUS.html`: step 4 rewritten to the `Next` workflow in plain English, and the last two
  "three to five sources" lines removed. The page carries the instruction and the plain warning,
  no doc numbers and no provenance, per the scope rule.
- `matt_todo.txt`: the batch A/B re-scoped to his actual controls, `Next 1` against `Next 5`.

**NOT YET DONE, and it needs him:** the corpus page still shows the coverage grid from the first
run. **2021 is in progress at 15 sources and the rest are not submitted**, so there are no new
rows to render. When the `<season>_<batch>.csv` files land I rebuild it.

---

## 5. THE RULE

**A model's citation of another company's documentation is a claim like any other, and it is
cheap to check.** Two page reads settled this one. Treat any "the documentation says" from a chat
model the way this project treats a number with no population: unusable until someone opens the
page.
