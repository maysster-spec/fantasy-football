# 367. THE SPLIT: FOUR FILES BY READ CADENCE, EVERY LINE ACCOUNTED FOR, AND THE PASTE IS 2.9 TIMES SMALLER, NOT 5

*18 Sept 2026, 23:15 ET. Fable, on Matt's go ("one word") to doc 366. Everything below is measured on
the files as committed tonight to `G:\My Drive\_Fantasy\2026\Source\`, verified byte for byte after
the commit. Token figures are bytes divided by four and are labelled estimates.*

---

## 0. WHAT TO DO

1. **Matt: paste the new `Source\00_PROJECT_DIRECTIVE.md` (v9.8) into the project's custom
   instructions, replacing v9.7 in full.** It is on your to-do list. That is your whole part.
2. **The number changed: the paste is 168,480 bytes to 57,739, a 2.92 times cut (65.7%), about
   42,000 to 14,400 tokens a turn.** Doc 366 derived "five to six times" and a 30 KB target. Moves of
   whole paragraphs do not get there; what is left is SECTION 0's rules, and cutting further means
   rewriting rules, which doc 366 itself argued against. Section 3 says why and what the choice is.
3. **A cross-reference from a numbered doc still resolves.** `§4.x` is in `DIRECTIVE_FINDINGS.md`
   under the same id; `§5`, `§7`, `§8` and the depletion table are in `DIRECTIVE_DRAFT_BOOK.md`
   under the same headings. Nothing was renumbered.
4. **`py Scripts\research\audit_directive.py` reads §4.14 from the findings file now** and prints
   which file it read. Four negative controls run; section 5.
5. **Not yet run: the regression test doc 366 set** (the two fileless probes and Fable's Part A
   against the new paste). It needs the paste to exist in the project first, so it is the next job
   after item 1.
6. Nothing else to run tonight.

---

## 1. WHAT MOVED WHERE

| file | bytes | what it holds |
|---|---|---|
| `00_PROJECT_DIRECTIVE.md` v9.7 (before, archived) | 168,480 | everything |
| **`00_PROJECT_DIRECTIVE.md` v9.8 (the paste)** | **57,739** | header · WHERE THINGS LIVE · §0 rules · §1 · §2 with 2.1(a)(b) · §3 · §4 as a 42-line index · §6 doctrine and the Spears block · §9 |
| `DIRECTIVE_FINDINGS.md` (new) | 78,107 | SECTION 4 whole, 42 findings, v9.7 order |
| `DIRECTIVE_DRAFT_BOOK.md` (new) | 32,679 | §2.1 (b2) to (e) and the turn structure · §5 · §6's QB2/TE2 argument and doc 12's waiver table · §7 · §8 · §9's two kit rows |
| `DIRECTIVE_CHANGELOG.md` (before → after) | 25,083 → 39,663 | plus the v9.8 entry, the v9.5 to v9.7 header entries, and ten case-history blocks from §0 |

The ten blocks moved out of §0 to the changelog, each labelled there by the rule it belongs to: the
[v8.2] "why the plain-English rule keeps losing" explanation (the SCOPE RULE stays) · the three "THE
CASE THAT EARNED IT" paragraphs under (f2), (f) and (g) · (a2)'s three cases of 2026-09-06 · the [v7.7]
collision with the retired handover's rule 7 · (a4)'s "THE HOLE THIS CLOSES" · 0.5(f)'s incident.io
paragraph and its 18 Sept transition case · 0.6's doc 228 case. Every rule sentence stayed.

What stayed resident on purpose although it is long: 0.5(a)'s struck bar and Matt's block quote
(the rule's authority), "His record says WHERE to aim" with the 12/1/7 count ((f2) cites it), (a3),
(c) and (d) whole, and §6's Spears block (the in-season bench rule lives inside it).

---

## 2. THE PROOF

Standalone script, no knowledge of the build: multiset of non-blank lines across the four new files
(the changelog counted net of its previous lines) against v9.7.

```
v9.7 non-blank lines: 1946   in the four new files: 2093
LOST (in v9.7, not in any new file): 3
  x1  # SYSTEM DIRECTIVE — E-DISCOVERY KEEPER LEAGUE DRAFT STRATEGIST (v9.7)
  x1  *Full history: **`Source\DIRECTIVE_CHANGELOG.md`**, 39 entries, v5.4 through v9.4.*
  x1  | **any doc corrects an earlier doc, or any directive number is edited** | `Scripts\research\audit_d
ADDED (in a new file, not in v9.7): 150 lines
old changelog: every line present in the new changelog. OK
```

The three lost lines are the title (now v9.8), the history pointer (now "v5.4 through v9.7"), and one
row of §0.5(d)'s milestone table, reworded in place because its old wording, *"it reads §4.14's numbers
out of the directive now"*, became false tonight; it now names the findings file and says what it said
before. That is the one sentence in the whole exercise that was reworded rather than moved. The 150
added lines, by class, counted from the build: the v9.8 header entry, 14 lines, present twice because
the changelog's own rule puts the newest entry at its top as well (28) · the reworded row (1) · the title, twice (2) · the
history pointer (2) · the WHERE THINGS LIVE block (17) · the findings index, 7 header lines and 42
rows (49) · three pointer blocks left where text was removed, §2.1, §6 and §9 (6) · the findings
file header (8) · the draft book header and its three section labels (13) · the changelog headings,
intro and map lines (8) · the ten case-history labels (10) · separators (6). The full list is in
`_archive\367_split_proof.txt`. Blank lines were not counted; the byte totals above are the whole files.

Sum of the three directive files: 168,525 bytes against v9.7's 168,480. The 45-byte difference is
the three replaced lines and blank-line handling, and it is why the multiset, not the byte count, is
the proof (v9.5's own lesson).

---

## 3. WHY 2.9 AND NOT 5, AND WHAT THE CHOICE IS NOW

The paste by section after the move: header and map 3.9 KB · §0 30.6 KB · §1 1.4 KB · §2 3.3 KB ·
§3 2.3 KB · §4 index 6.6 KB · §6 5.6 KB · §9 4.0 KB. **SECTION 0 is 53% of what is left**, and
it is rules: (f), (f2), (g), the four guardrails, §0.2's nine method rules, §0.4, (a) to (e), (f),
0.6. Moving those is moving the instruction, not the story.

Doc 366's "five to six times" was derived from "roughly 30 KB of rules" in its own table, and that
row was an estimate of what a rule-only rewrite would produce, not of what whole-paragraph moves
produce. The measured answer is 57.7 KB. **Getting to 30 KB is a different operation: condensing
the rules themselves. Bouchard's 92% to 38% recall loss (doc 351, doc 366) is the measured cost of
that class of operation, and it is the reason doc 366 said "never rewrite the words".** So it is a
decision, not a next step: leave the paste at 57.7 KB and take the 2.9 times, or commission a
rule-condensing pass with a red team behind it. My recommendation is the first, and the reason is
that the second buys about 7,000 tokens a turn against a known way of losing rules.

---

## 4. THREE DEPARTURES FROM DOC 366, EACH FOR A REASON

1. **Names.** Doc 366 said `01_ENVIRONMENT.md`, `02_FINDINGS.md`, `03_DRAFT_BOOK.md`. The collision
   check (§0.5(c)4) found `01_league_and_managers.md`, `02_findings_ledger.md` and
   `02b_LEDGER_CORRECTIONS_v5.md` already in `Source\` from August. `02_FINDINGS.md` beside
   `02_findings_ledger.md` is two names for one job. The new files are `DIRECTIVE_FINDINGS.md` and
   `DIRECTIVE_DRAFT_BOOK.md`, the family `DIRECTIVE_CHANGELOG.md` already started.
2. **No environment file.** Doc 366 put §2 in tier 1 ("§2 as is") and also in a tier-2
   `01_ENVIRONMENT.md`. Both cannot hold it without a copy. §2 is 3.3 KB and is read every turn, so
   it stays resident and no second file exists.
3. **One index, not two.** Doc 366 put the index in the directive and at the top of the findings
   file. Two copies of a 42-row table is the maintenance defect this project keeps paying for, so
   the index is in the directive only; the findings file says so and its headers are greppable by id.

---

## 5. WHAT ELSE CHANGED

- **`Scripts\research\audit_directive.py`:** `from_directive()` reads `DIRECTIVE_FINDINGS.md` first,
  then the directive, and prints which file each number came from. Negative controls: post-split
  folder reads 328 and 152 from the findings file; a pre-split folder (v9.7 only) reads the same two
  from the directive; the new directive without the findings file falls back loudly ("wording
  moved"); an empty folder falls back loudly ("could not read"). Standard library only; compiles
  clean with warnings as errors on 3.12's escape check. Not pinned by `check_kit.py`.
- **`00_START_HERE.md` v8:** the line *"The directive's SECTION 4 holds all 37 findings"* would have
  been false from tonight. Section 7 now names the two files, and section 8's stop signs are said to
  live there. Header cites doc 367.
- **`DIRECTIVE_CHANGELOG.md`:** its own WHAT LIVES WHERE list gains the two new files.
- **Ledger:** row 149 closed with the measured numbers; row 150 records doc 366's three defects
  (the name collision, §2 in two tiers, the 5 to 6 times gain derived from a rewrite it argued
  against).

---

## 6. OPEN, BY NAME

- The regression test (item 5 above), after the paste.
- `DOC_INDEX.md` and its generator (doc 366 item 3): not started.
- The to-do split into tasks and notes with a status field (doc 366 item 4): not started.
- Doc 366's `OPEN_THREADS.md` count is inflated by READ ONLY notes and dated-expired items; same fix.

Ledger rows 149 (closed) and 150.
