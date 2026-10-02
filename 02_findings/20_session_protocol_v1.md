# 20 — SESSION PROTOCOL v1: token budget and integrity controls
**Written Aug 22 2026.** Two problems, one answer: *stop carrying numbers in prose.*
Prose is expensive to re-read and impossible to enforce. Files are cheap and checkable.

---

# PART A — TOKEN BUDGET

## A1. What this session actually cost, measured

All 32 data blobs — 2.2 MB of CSV — were pulled into the workspace for **~4,000 tokens total**.
`project_read` on a blob returns *a file path*, not the bytes. Then pandas reads it and only
the printed summary enters context. The same 32 files pasted as text would have cost
**≈600,000 tokens** and would not have survived compaction.

**Rule 1 — data never enters the conversation.** Not a pasted table, not a screenshot of a
sheet, not a CSV in a message. Upload the file. I read it with code and print ~40 lines.
This is the single largest saving available and it is roughly **150:1**.

## A2. The directive is the most expensive object in the project

`00_PROJECT_DIRECTIVE_v4.md` is ~4,500 tokens and is injected into **every turn of every chat
in this project**. Over a 60-turn session that is ~270k tokens spent re-reading constants —
and audit 19 shows those constants are wrong.

**Rule 2 — the directive holds rules, never numbers.**
Move §4.1 replacement levels, §4.7 structural percentages and the §2.1(c) effective-ADP table
into `constants_2026.csv`, and encode each as an assertion in `code_audit_v1.py`. The directive
keeps what cannot be computed: the objective function, the keeper mechanics, the output
contract, the standing rules. Target: **under 1,800 tokens.**

Corollary: **changing a project doc busts the prompt cache for every chat in the project.**
Batch edits. Do not churn.

## A3. Registers, not ledgers

`02_findings_ledger.md` is prose. A finding in prose cannot be sorted, filtered, diffed, or
checked for a missing sample size. Convert to `findings.csv` with mandatory columns:

`id, claim, verdict, statistic, baseline, population, sample_n, tested_on, superseded_by, downstream_uses`

This makes directive §3's BASELINE/POPULATION/SAMPLE requirement **structural instead of
aspirational** — a row with an empty `sample_n` is visibly broken. It is also ~5× denser than
the prose it replaces, and `superseded_by` is how the Aubrey-class error gets caught: one
retraction, every dependent row flagged.

## A4. What compaction destroys

Per Anthropic's compaction documentation, summarisation drops **tool-call sequences and
intermediate results** first, keeping only the narrative. That is exactly the wrong half for
this project. **Rule 3 — if a number matters, it is in a file before the next tool call.**
Never let a computed result live only in the transcript.

## A5. Can your input be compressed?

You asked. Honest split:

- **Structured data — yes, heavily and losslessly.** CSV over pasted tables. Drop columns
  nothing consumes (HANDOFF §5 already says skip FantasyPros' FPTS). Numbers to 1 decimal.
  One file per export, date in the filename.
- **Your prose — no.** Compressing intent is lossy in exactly the way that produces the
  defects we are trying to prevent. Your long messages are cheap; a 900-word instruction is
  ~1,200 tokens, less than one careless dataframe print.
- **Real saving is in tool output, not your input.** One batched analysis call printing a
  40-line summary beats eight calls printing dataframes. That is on me, not you.

## A6. Working rules

| # | rule |
|---|---|
| 1 | Data enters through files. Never paste a table. |
| 2 | Batch independent checks into one call; print summaries, never raw dataframes. |
| 3 | Write results to disk immediately; assume the transcript will be summarised away. |
| 4 | Start each session with `code_audit_v1.py`, then read the register. Do not re-read source docs to "get oriented." |
| 5 | One deliverable per session, saved to the project. New chat when the objective changes, not when it gets long. |
| 6 | A long fan-out search (e.g. "find every use of ADP across 44 docs") belongs in a subagent — its context is discarded and only the answer returns. Say the word and I will use one. |

---

# PART B — INTEGRITY CONTROLS

Grounded in the current agent-reliability literature, checked against directive v4 for conflict.
**No conflict found. Every control below implements a rule v4 already states but cannot enforce.**

## B1. The core result, and why this project keeps failing

Measured across models: **execution-time guardrails beat instructions by 2.2–5.3 points;
adding instructions to the system prompt gained +0.4.** And when an agent verifies its own
output, it **rationalises errors rather than flagging them** — validation has to move off the
generating model onto a deterministic oracle.

Directive v4 is ~4,500 tokens of excellent instruction. Section 3 already says *"never state a
statistic not present in a source"* and *"every finding must carry baseline, population,
sample size."* Those rules were in force the whole time, and audit 19 still found 18 failures.
**That is the +0.4 result, observed live.** The rules are not wrong; instructions are the wrong
delivery mechanism.

## B2. Controls now implemented

**1. Deterministic oracle — `code_audit_v1.py`.** 22 assertions, exit code 1 on any FAIL.
Every numeric claim the directive makes is encoded with a tolerance. It does not ask me whether
the constants are right; it recomputes them. **Run it first, every session.** It found both
CRITICAL defects.

**2. Verifier instrumentation.** Catch rate, fix rate and false-alarm rate are three separate
numbers. This run: **22 checks · 18 FAIL · 1 false alarm** (the `NaN == NaN` duplicate-ID
artifact, logged in audit 19). Tracking the false-alarm rate is what stops a noisy checker from
being ignored.

**3. Unit-tagged column names.** CRITICAL 1 exists because a column called `ADP` holds a rank.
Rename on the next spine rebuild: `adp_rank` / `adp_pick` / `proj_leaguepts`. A join that
mixes `adp_rank` with `adp_pick` should be unspellable, not merely discouraged.

**4. Join contracts.** Key on `gsis_id`, else `name+pos+team` — never name alone, never
first-initial+surname. **Assert the match count before and after every merge and fail on a
drop.** Both CRITICALs and all eight historical name-join errors would have been caught by
one assertion. The D/ST failure dropped 32 of 32 rows silently.

**5. Provenance header on every derived file** — source file, capture date, generating script.
Undated files cost this project three days once already.

## B3. Controls proposed, not yet built

| control | what it buys | falsifier |
|---|---|---|
| **2025 holdout backtest** — run the current board logic on 2025 inputs, compare its picks to what you actually drafted and to what actually scored | HANDOFF §6 calls this *"the strongest available self-red-team and it has never been done."* It is the only test that scores the whole pipeline rather than its parts | if the model's 2025 board beats your actual 2025 draft by less than its own stated error bars, the model is decoration |
| **Turn-depth checkpointing** — planning depth degrades performance about twice as fast as tool count | forces state to disk before the degradation window | none needed; it is free |
| **Stopping rule instead of retry count** — stop when the verifier's false-rejection rate exceeds a threshold, not after N attempts | prevents the "test until it passes" pattern that produced the GC and shrinkage-slope artifacts | — |
| **Directive assertion sync** — a check that fails if a number in the directive has no matching assertion | makes stale constants structurally impossible | — |

## B4. Where the human stays in the loop

You are right that this needs one, and right about where. Three places:

1. **Anything with no falsifier.** If I cannot state the result that would kill a claim, it is
   labelled `[HYPOTHESIS]` and it is yours to accept or reject, not mine to act on.
2. **Behavioural reads.** Snyder–Buffalo was found by you first and only later fell out of the
   data — ranked *sixth* by z-score. A model that had never heard your read would have buried it.
   The 5-of-7 rule in HANDOFF §11 ("do not tell Matt a source is not worth supplying") is the
   same lesson: **your priors have a measured track record and it beats my dismissals.**
3. **The objective function.** Weeks 1–14 vs championship equity is still open. Your losses are
   entirely in weeks 15–17 and the model does not point there. That is a judgment call about
   what you are playing for, and it is not mine.
