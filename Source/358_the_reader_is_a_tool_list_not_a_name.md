# 358 - The reader is a tool list, not a name

**2026-09-18. Doc 357 was Fable's independent read of `00_START_HERE.md` v2. This is what v2 got
wrong, what v3 does about it, and the one finding that corrects a correction I made an hour
earlier in the same file.**

**POPULATION, because it is the whole point of the exercise (SS0.6): one handover document, read by
one outside model that had the local drive bridge and the project directive but had never seen this
conversation. Not a review of the prose. A RUN.** Doc 356 records the method: two Claude subagent
probes on v1 found 11 gaps, Fable found 8 more on v2. A handover is tested by being used.

---

## 1. THE FINDING THAT CORRECTS MY OWN CORRECTION

v1 said there were two kinds of reader. Matt caught the contradiction against my own catalog, which
said three, and I fixed it by adding a third row. **Fable found the fix was wrong in the same way
the original was wrong: my three rows sort by MODEL NAME.**

The row said, in effect, "if you are Fable or Gemini, SECTION 4 does not apply to you." Fable read
that row while holding the bridge, with `device_stage_files` one call away. **The row was false for
the reader it was addressed to, and it was false because it asked who you are instead of what you
can do.**

v3 sorts on the only thing that is observable from inside the session:

> Are `mcp__remote-devices__*` tools in your list? Then section 4 applies to you, whatever you are
> called.

**This is SS0.5(a2) at the level of a document rather than a test: the object was the model, and the
question was about the tools.** I had already made that error once in this file and did not
recognise it when I made it a second time in the fix.

---

## 2. THE SEVEN OTHERS, AND WHAT CHANGED

| # | what Fable found | v3 |
|---|---|---|
| 2 | **the bridge-down fallback was dishonest.** v2 said "work from the project doc store." The store holds the DOCS and not the DATA | names the gap: no roster CSV, no wire, no snap counts; for data, the Google Drive connector (no grant needed) or name the exact file and ask Matt to attach it |
| 3 | **the freshness rule covered the pages and not the data files** | extended to every data file, with the trap named: `injuries_2026.csv` written Sunday night shows a man healthy who got hurt on Monday |
| 4 | **the spine had no roster mechanics**, so a reader could recommend an add that needs a drop and never know | roster 15 / 9 starters / 6 bench / 3 IR, the position caps, "a full roster means any add needs a drop", and the waiver mechanic flagged as Matt's own fact and not verified against ESPN |
| 5 | **section 8 stated doc 288's claim as measured.** It is not | "Doc 288 argues, and does not measure, that a stranger reading them arrives pre-committed" |
| 6 | **the re-open licence had no gate.** It invited a new session to spend an afternoon reopening a closed question | gated: "Before spending an afternoon on one, ask: does a decision Matt faces THIS WEEK still depend on it?" |
| 7 | **1,974 words against Garg's 1-to-3-page target** | 1,700 words. Cut the standalone four-defect-shapes section; merged the pages list into the data-layer table |
| 8 | **nothing told a second session that another session may be writing the same files** | new rule in section 4: re-stage `AUDIT_LEDGER.md` and `matt_todo.txt` immediately before editing, never from a copy taken earlier in the turn |

Finding 8 is Matt's instruction from the same hour, arrived at independently from the outside. Two
sessions wrote to `Source\` simultaneously this afternoon and the doc numbers collided twice (349
then 352). **The concurrency hazard was live while the document that fails to mention it was being
written.**

---

## 3. THE FOUR CRITERIA ALL PASS

Fable's run, doc 357: reaches the files without asking Matt where they are; does not spend a waiver
claim or propose a drop; does not re-derive a closed question; does not quote a retracted number.
**Rating 7/10, and the seven above are why it is not higher.** `[SOURCED: doc 357, 2026-09-18]`

**What the pass does NOT establish: that a reader with no bridge and no directive succeeds.** Fable
had both. **The untested population is a chat outside this project, and it is the one Matt is most
likely to open from his phone.** `[OPEN]`

---

## 4. THE METHOD POINT, AND IT IS THE REUSABLE PART

**A handover cannot be reviewed into correctness.** Every defect above is invisible to reading:
each sentence is true in isolation, and each one is wrong about the reader who receives it. Row
three was a correct sentence about Fable-the-model and a false one about Fable-the-session. The
fallback was a correct sentence about what the store contains and a false one about what a reader
needs.

**The only instrument that finds these is an outside session that has to USE the document, and the
only honest report is the list of things it could not do.** That is doc 356's finding and this is
its replication on a different reader.

**Cost: one tasking file (`FABLE_HANDOVER_TEST.md`, 6.5 KB), one run, eight defects.** Cheaper than
any of the three red-team passes I ran on the prose myself, which found the length problem and none
of the other seven.

---

**Files:** `Source\00_START_HERE.md` v3 (10,238 bytes, 1,700 words). v2 archived to
`2026\_archive\00_START_HERE_20260918_v2.md`. Fable's report is doc 357.
