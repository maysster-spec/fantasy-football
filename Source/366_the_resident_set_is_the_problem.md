# 366. THE RESIDENT SET IS THE PROBLEM: 42,000 TOKENS OF SYSTEM PROMPT EVERY TURN, MOST OF IT FOR A DRAFT THAT IS OVER

*18 Sept 2026, 21:00 ET. Fable, at Matt's request: "I wonder if further gains can be had and not just
in the area of a defrag. Perhaps re-architecture and reimagining of the project is in order from the
ground up ... my thoughts go to how RAM in a PC works." Measured on the drive as it stands tonight:
`00_PROJECT_DIRECTIVE.md` v9.7, `Source\` (549 files), `OPEN_THREADS.md` (regenerated 20:25 ET),
`matt_todo.txt`. Token figures are bytes divided by four, an estimate, and are labelled as such.*

---

## 0. WHAT TO DO

1. **Do not start over.** Split what exists by how often it is READ, and move text rather than rewrite
   it: the same proof the defrag used (identical line multiset before and after) applies. A rewrite is
   the one method the project's own evidence argues against.
2. **Cut the directive from 168 KB to about 30 KB by moving three things out of it:** the 42 findings
   (77 KB) into their own indexed file, the draft-night material (§5, §7, §8: 23 KB) into an archived
   draft book, and the case histories in §0 (roughly 19 KB of "the case that earned it") into the
   changelog that already exists. What stays is the operating spec: rules, environment, doctrine, the
   file protocol, and a 42-line index of the findings.
3. **Generate a page table for the corpus:** one script-built `DOC_INDEX.md` (number, title, date,
   first line, which findings it cites, its open markers). The doc numbers stay; nothing is renumbered
   or merged.
4. **Split the to-do into tasks and notes**, and give tasks a status field. Tonight it is 45 open
   items of which about a third are "READ ONLY" notes and seven carry dates already passed.
5. **Measure before and after with the test we already have:** the two fileless probes and Fable's
   Part A, run against the new spine. Pass means criteria 1 to 6 hold with a resident set under 8k
   tokens. Fail means a probe re-finds a defect that lived in moved text, and that line comes back.
6. **Sequence:** the new chat's first job, or Fable's next; items 2 and 3 first (one session), then
   your paste of the 30 KB directive, then the probes, then item 4. Nothing to run tonight.

---

## 1. WHAT WAS MEASURED

**The directive, v9.7, 168,480 bytes, about 42,000 tokens, loaded as the system prompt of every turn
of every chat in this project:**

| section | bytes | share | read every turn in season? |
|---|---|---|---|
| header and changelog | 5,917 | 3.5% | no: history |
| §0 output rule, validation, critic | 37,628 | 22.3% | the RULES yes; the case histories no |
| §1 preconditions | 1,430 | 0.8% | draft-side |
| §2 fixed environment | 5,919 | 3.5% | yes |
| §3 data integrity | 2,293 | 1.4% | yes |
| §4 the 42 findings | 77,340 | 45.9% | on demand: about 42 KB of it is draft-side, 35 KB in-season |
| §5 opponent model | 4,829 | 2.9% | draft only |
| §6 late-round and keeper doctrine | 9,391 | 5.6% | the bullets yes; the QB2 argument no |
| §7 output contract, pick 32, pick 8, pick 56 | 7,575 | 4.5% | draft only |
| §8 refresh schedule and draft-night runbook | 10,979 | 6.5% | draft only |
| §9 file access protocol | 5,179 | 3.1% | yes |

Lines carrying a version tag or a "the case that earned it" narrative: about 19 KB, 11% of the file.
The draft was 7 September. **Roughly two thirds of what every in-season turn reads first is either
about a draft that is over or about how a rule came to exist.**

**The corpus:** `Source\` holds 549 files, 58 MB; 328 of them are `.md`, 3.46 MB. The project doc
store holds 411 docs and hit its size cap once today (my JOB 2 writes were refused for an hour).
`OPEN_THREADS.md` is 220 KB after tonight's run, thirteen times the handover. `matt_todo.txt` is 86 KB
with 45 open items. `AUDIT_LEDGER.md` is 158 KB, 148 rows.

**The consequence you named, "new chats don't even last very long", follows from the arithmetic:**
every turn begins by reading about 42,000 tokens before the conversation itself, and the model's
recall of any one line falls as the window fills. That is not a guess about attention; it is the
published finding below, and the defrag's own measured gain was of the same kind: fewer conflicting
copies of one thing in the resident set.

---

## 2. THE RAM ANALOGY, CORRECTED, AND WHAT THE OUTSIDE SOURCES SAY

Your instinct is right and the mechanism is slightly different from an allocator. A PC's memory
manager optimises PLACEMENT because the CPU touches only the addresses it needs. A model does not: it
reads the whole resident set, every turn, front to back. So the cost is linear in resident BYTES, and
ordering inside the resident set matters only for salience (rules first). **The actionable half of the
analogy is the hierarchy, not the allocator: a small hot set that is always loaded, a cold store that
is fetched by reference, and an index that maps a subject to an address.** Right now the whole book
is in the hot set, and the only index is filename grep.

Outside, dated (B7), all three loaded pages rather than snippets:
- **Anthropic, "Effective context engineering for AI agents", 29 Sept 2025:** *"As the number of
  tokens in the context window increases, the model's ability to accurately recall information from
  that context decreases."* The recommended design is *"just in time"*: agents *"maintain lightweight
  identifiers ... and use these references to dynamically load data into context at runtime."*
  System prompts should sit at an altitude *"specific enough to guide behavior effectively, yet
  flexible enough to provide the model with strong heuristics."* And for long work, *"specialized
  sub-agents can handle focused tasks with clean context windows"*, which is what Fable's jobs
  already are.
- **Bouchard, 18 Aug 2026** (already cited in doc 351): compacting a long-lived context by REWRITING
  it took recall from 92% to 38%. That is the measurement against "from the ground up".
- **Garg, Thoughtworks, 24 Feb 2026:** a priming document past three pages stops being read. The
  handover is now 2,823 words and the directive is about 60 pages.

---

## 3. WHY NOT START OVER, IN ONE PARAGRAPH

The corpus's value is its retraction trail. Every number the project has killed is struck through
next to the number that replaced it, with a doc number as evidence, and the ledger's 148 rows exist
because the trail was the only thing that let anyone tell a live number from a dead one (section 7
of the handover, the best sentence in it, depends on that trail existing). A rewrite from scratch
would carry the live numbers forward and drop the dead ones, which sounds like a gain until the next
session quotes "about 20 points" at pick 8 because nothing in the new spine says it was retracted.
Bouchard's 92 to 38 is that loss, measured. **So: move, index, archive. Never rewrite the words.**

---

## 4. THE SPLIT, BY READ CADENCE

Three tiers, and every existing line goes to exactly one of them.

**Tier 1, resident, the paste: `00_PROJECT_DIRECTIVE.md`, target under 30 KB.** §0's rules with the
case histories moved out (keep each rule, its one-line reason, and the doc number; the story goes to
the changelog) · §2 as is · §3 as is · §6's doctrine bullets · §9's protocol · and a **42-line index
of §4**: id, one-line claim, status (live, qualified, retracted), the doc numbers. The index is the
only new text in the whole exercise.

**Tier 2, fetched by reference: `02_FINDINGS.md` (§4 moved whole, index at the top, the strike-through
trail untouched) and `01_ENVIRONMENT.md` (the durable spine: §2, the roster shape, the ids, the
waiver mechanics, the schedule files).** A session reads a finding when a question touches it, by id,
through `project_search` or the index. `audit_directive.py` is re-pointed at the findings file so the
numbers it checks do not move out from under it.

**Tier 3, archived until July 2027: `03_DRAFT_BOOK.md`: §5, §7's draft parts, §8, the keeper-depletion
table.** Nothing is deleted; the draft-night runbook is the single most tested artifact in the project
and will be needed again.

**The corpus stays where it is.** What it lacks is a page table, and that is a script, not a rewrite:
`DOC_INDEX.md` generated from each doc's own header (number, title, date, first line, the §4 ids it
cites, its markers), regenerated by `ff.bat`. `open_threads.py` already scrapes the markers; the
index is the same scan writing a second file. **"When new sections get written they get written to
the correct place"** is then a rule with a tool behind it: a finding goes to `02_FINDINGS.md` and
gets an index line; a rule change goes to tier 1 and its story to the changelog; a doc gets a number
and an index row; a task goes to the to-do with a status.

**The trackers.** `matt_todo.txt` carries two kinds of line and should carry one: tasks (a command, a
click, a date) and notes ("READ ONLY, NOTHING TO RUN"). Move the notes to the week sheet's to-do page
or a `NOTES_FOR_MATT.md`, give each task a status and a date, and let the existing `close_check.py`
expire dated items. `OPEN_THREADS.md` then shrinks to the tasks and the queue.

---

## 5. THE PROOF STANDARD, SO IT IS NOT ANOTHER DEFRAG THAT "CALLED THE JOB DONE"

1. **Moves are proved by multiset.** Concatenate tiers 1, 2, 3 and the changelog after; the line
   multiset equals v9.7's plus the index lines. The defrag did this and it is the reason its claim
   survived a red team.
2. **The resident set is measured, not described:** bytes of the paste, before and after, in the
   ledger row that closes this.
3. **The regression test is the one that exists:** the two fileless probes on `00_START_HERE.md`
   plus Fable's Part A questions, against the new tier 1. Pass: criteria 1 to 6 hold. The interesting
   failure: a probe re-finds a defect whose fix lived in moved text, which means the index line was not
   enough and that rule comes back into tier 1.
4. **`audit_directive.py` runs green against the findings file** before the old directive is archived.

---

## 6. WHAT THIS BUYS, DERIVED, NOT MEASURED

Resident set 168 KB to about 30 KB: roughly 42,000 tokens to 7,500 per turn, a factor of five to six.
Every turn of every in-season chat stops re-reading pick 32 and the draft-night runbook. The window is
fixed, so the conversation gets the tokens the book was using, and the recall penalty above shrinks
with the set. The number that will tell you whether it worked is not a token count; it is whether a
fresh chat answers "catch me up" from the files without getting lost, which is the test doc 365 ran
and can run again.

**What it does not fix:** the to-do list's asks-not-completions problem (doc 365 C1) and the
transaction file's hand pull (row 145) are pipeline defects and stay open whatever the spine looks
like.

---

## 7. THE ONE THING I WOULD PUSH BACK ON

"Reimagining from the ground up" is the phrase to drop, and the reason is the project's own record
rather than caution: every time this project rewrote a long-lived thing it lost something it had
measured (the handover's own versions 1 to 3 re-found defects the old file had already closed). The
architecture you are describing is right: a hot set, a cold store, an index, a rule for where new
text lands. It is reached by moving, not by starting again, and the first two moves are one session's
work.

Ledger row 149.
