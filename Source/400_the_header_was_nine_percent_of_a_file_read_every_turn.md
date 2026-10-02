# 400 — The header was 9% of a file read every turn, and the outside read says the split was right all along

*23 Sept 2026. Doc 397 batch B, the last of the order Matt set. Directive v9.22 → v9.23. **No rule changed and no
number was retracted by this version.** Ledger row 175.*

---

## 1. MATT FOUND THIS WITH NO PROMPTING, AND NOTHING HERE COULD HAVE

> *"the project directive is now current v9.2, but i have to say, i don't recall seeing system directive structured
> this way. Maybe that's normal, i don't know, just looks different"*

Measured before touching it:

| | |
|---|---|
| header length | **42 lines, 1,332 words** |
| share of the file | **9.0%** |
| versions stacked in it | **nine** (v9.14 → v9.22) |
| nested bracket blocks | **seven** |

And this file is read **every turn, by every session.**

**No guard in §0.5(d) could have fired, because every individual addition looked like diligence.** Each version had a
real finding, each one wrote it where the last one was, and none was wrong on its own. That is the shape of defect
this project is worst at seeing — it is the one Matt catches, and it is the third time (the ladder page, the market
anchor, this).

---

## 2. THE OUTSIDE READ (§0.5(c)6), AND THE FIRST HALF OF THE ANSWER IS THAT THE SPLIT IS NORMAL

**Every red team this project has run before §0.5(c)6 existed was an internal-consistency check.** Those can only
find one file disagreeing with another. Matt's question — *is this normal?* — cannot be answered from inside.

**SOURCE 1. *Keep a Changelog* 1.1.0** (keepachangelog.com; spec dated 2019-02-15, site maintained through
2024-09-27; §0.5(d)'s B7 date rule). Its guiding principles: one file, **"the latest version comes first"**, the
release date displayed, and **"there should be an entry for every single version."** Under *Inconsistent Changes* it
warns that a partial second copy makes readers **"mistakenly think that the changelog is the single source of truth.
It ought to be."**

**We had already drifted exactly that way.** The header asserted what v9.18 changed while `DIRECTIVE_CHANGELOG.md`
held no v9.18 entry at all — two sources of truth, and the wrong one was the resident one.

**SOURCE 2. Anthropic, *Effective context engineering for AI agents*** (2025). It names the mechanism the header
was feeding:

- **"context rot"** — *"as the number of tokens in the context window increases, the model's ability to accurately
  recall information from that context decreases."*
- a finite **"attention budget"**, where *"every new token introduced depletes this budget by some amount."*
- the target: *"the smallest possible set of high-signal tokens that maximize the likelihood of some desired
  outcome"* — and, importantly, *"minimal does not necessarily mean short."*
- an explicit warning against *"hardcoding complex, brittle logic"* in prompts, which *"creates fragility and
  increases maintenance complexity over time."*

**WHERE WE ALREADY MATCH PUBLISHED PRACTICE, WHICH IS THE BIGGER HALF OF THE ANSWER TO HIS QUESTION.** The v9.8 split
into four files by read cadence is not an oddity — it is the recommended pattern: *"maintain lightweight identifiers
(file paths, stored queries, web links, etc.) and use these references to dynamically load data into context at
runtime."* Markdown headers to delineate sections is also the recommendation. **So: the structure is normal. The
header was not.**

**WHERE WE DIFFER ON PURPOSE, and differing on purpose is an answer (§0.5(c)6):** the file is
`DIRECTIVE_CHANGELOG.md` rather than `CHANGELOG.md`, because several canonical files share one folder and the naming
rule demands the subject be in the name; entries are narrative rather than Added/Changed/Fixed groups, because each
one has to carry the measurement that made or killed a rule; and no Semantic Versioning claim is made, because the
version numbers here track editions of a document, not a released API.

---

## 3. WHAT CHANGED

The header is now the version line, **two short paragraphs**, the pointer to the changelog, and a **DO-NOT-QUOTE
table of the twelve live retractions.**

**The retractions stay resident on purpose.** §0.1 says a number that must not be quoted any more is actionable — it
belongs where a session will see it without going looking. What does *not* belong there is the story of how each one
was found, and that is now in the changelog in full, word for word.

| | before | after |
|---|---|---|
| header prose | 42 lines, 1,332 words | **14 lines, 183 words** |
| retractions a session can see at a glance | scattered through nine blocks | **one table, twelve rows** |
| whole file | 85,277 chars | **80,400 chars before §9 rule 7 was added** |

**The file is 4,877 characters smaller than it was this morning despite gaining the table.**

**NEW §9 RULE 7, and it is a budget rather than a style note.** The header carries the version line, at most two
paragraphs, the pointer and the table. A new version **appends its entry to the changelog and REPLACES the header's
paragraphs** — it never nests inside the previous version's block, which is what six consecutive versions did. **Past
~20 header lines, the oldest narrative moves out before the new one is written, measured and not eyeballed.**

---

## 4. B2: CLOSED WITHOUT AN EDIT, AND THAT IS THE POINT

`check_kit.py`'s pin comments carry the same accretion — the `wire.py` line is a single run-on with six stacked
*"Before that"* clauses recording superseded hashes.

**Rewriting them would be surface work on my own output.** That is precisely what §0.5(a) was amended for on 22 Sept,
when a session went into 134 lines of em-dash edits while a real item sat open and Matt killed it: *"There really is
no material difference to even mention. And certainly no benefit in changing any files."* A comment on a script Matt
runs is not read by a model every turn; the attention-budget argument that justifies the header fix does not reach
it.

**So the substantive question was asked instead: is the guard CORRECT?** Both staged pins were verified against the
real files, CRLF-normalised:

| file | pinned | actual |
|---|---|---|
| `wire.py` | 118,276 / `ba63a3b7e7ef45ef` | **matches** |
| `sheet_engine.py` | 146,614 / `8bbfacd2345a4c33` | **matches** |

The guard is sound. Rule 7's last bullet binds at the next re-pin, when the comment is being touched anyway.

---

## 5. TWO THINGS THAT ARE MINE

**(1) I catalogued this defect and then fed it twice before fixing it.** Doc 397 measured the header at 42 lines and
847 words. By the time I came to fix it, it was 42 lines and **1,332** words, because v9.21 and v9.22 each added a
block. **Cataloguing a defect is not containing it**, and a catalog entry is not a freeze.

**(2) I broke the every-version rule again while fixing it.** v9.21 wrote three missing changelog entries and made a
point of the rule. **Two hours later v9.22 shipped with no entry at all**, and I only noticed when I opened the file
to add v9.23. Both are written now.

That second one is the argument for rule 7 having a **measured threshold** rather than an instruction to be careful.
I was careful. I had just written the rule. It did not help.

---

## 6. WHAT DOC 397 LEAVES OPEN

Batches A, B and D1 are closed. Still open and not worked today:

- **C** — `own_chg`, `own_start`, `own_asof`, `clears` and `STATUS_LOG.csv` have never run in production; the first
  `ff.bat` run writes them. **That run is also what settles D1's proxy** (ESPN's own `injuryStatus` against the
  no-designation-and-dark heuristic), so re-run `ir_seat_validity.py` after it.
- **D2** — the 61.1 / 29.1 / 11.2 claim-order gradient is unmodelled against waiver rank; the confound runs the
  right way, but it is not priced.
- **D3** — whether `own_chg` predicts contention in **this** league. **[NOT ESTABLISHED]**: the 28.6% contested rate
  is measured here, the mapping from a format-wide +/- onto these twelve managers is not.
- **E** — ledger rows 162, 163, 165; the doc 383 batch (§4.12, 4.18b, 4.20, 4.22, 4.25, 4.26 on the five-year
  registry); §4.33's TE playoff draw; `Auto Reactivate: No`; the position-cap and keeper-eligibility interactions
  with IR.
- **§4.23a**, cited in `DIRECTIVE_FINDINGS.md` with no index row and no body (carried from batch A).

---

## 7. PROVENANCE

Archived to `2026\_archive\` before overwriting, committed from a fresh container path with `expectedMtimeMs`, then
staged back and compared by CRLF-normalised sha256 — content, never the commit result (§9 rules 1 and 2). Every edit
asserted its occurrence count before applying (§9 rule 6). Both outside sources were read **as page text in the
browser**, not through `WebFetch`, per the method rule added at v9.19 after a summariser's rendering was quoted into
this directive inside quotation marks.

**Sources:** [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) ·
[Effective context engineering for AI agents, Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
