# 104 — The two analyst CSVs: what they actually contain, and what came out of them

**Date:** 2026-08-31 · Matt found `favorite-analysts-calls-2026.csv` (42 rows) and
`raw-analyst-calls-v2.csv` (180 rows) and put them at the 2026 root. These are the sources
footnoted 1 and 2 throughout the Gemini report audited in doc 103.

---

## 1. THE PROVENANCE, MEASURED

| | |
|---|---|
| rows, both files | **222** |
| **rows that are the same call counted twice** (the files overlap) | **42 (19%)** |
| **rows with NO episode date at all** | **189 (85%)** |
| dated rows from **2025**, not 2026 | 8 of 33 |
| rows with analyst = `UNKNOWN` | 36 |
| distinct players named | 94 |
| **player names mis-transcribed from audio** | **11 (12%)** |

The mis-transcriptions are audio artifacts: *Amarian Hampton* → Omarion Hampton · *Casey
Concepcion* → KC Concepcion · *Deon Stribbling* → De'Zhaun Stribling · *Devonte Adams* → Davante
Adams · *Harold Fannon* → Harold Fannin Jr. · *Roshan Johnson* → Roschon Johnson · *Terrence
Ferguson* → Terrance Ferguson, and four more. I repaired them by spelling proximity — **those are
inferences, not facts**, and the quotes still contain the raw artifacts ("Cuba Hubard", "dobs",
"Casey Conception", "TJ Hawinson").

**One Sean Koerner sentence — "I'm not drafting Hockenson, Njoku or Engram in any leagues" —
appears as three separate downgrade rows.** Anyone counting rows as independent opinions triples it.

**So the root cause of doc 103's errors is not only that an old notebook was left checked.** These
files are 85% undated by construction. No notebook, fresh or stale, can tell a 2024 take from a
2026 one inside them. The old-sources box made it worse; the file design made it possible.

## 2. WHAT SURVIVES — and it is worth having

Joined to the board on a repaired name key: **94 players named → 70 on the board, 8 predicted
keepers, 16 unmatched.** After de-duplication, **180 distinct calls on 78 draftable players.**

`ANALYST_CALLS.pdf` is the usable residue: every player **inside the range Matt can actually
reach**, with the target/downgrade counts, who said it, and the verbatim quote — sorted by the pick
he is expected to go at, not by national ADP.

The most-called players he can reach, after de-duplication:

| player | goes at | calls | who |
|---|---|---|---|
| **Josh Downs** WR IND | 120 | 6 target | Justin Boone, Matt Harmon |
| **Dontayvion Wicks** WR **PHI** | 159 | 6 target | JJ Zachariason, Matt Harmon, Terrell Furman |
| **J.K. Dobbins** RB DEN | 107 | 5 target | Justin Boone, Terrell Furman |
| **Rico Dowdle** RB **PIT** | 94 | 5 target, 1 down | Derek Brown, Hayden Winks + 2 |
| **Jonathon Brooks** RB CAR | 108 | 4 target | Mike Wright |
| **Tyjae Spears** RB TEN | 149 | 3 target | Boone, Fitzmaurice + 1 |

**The Wicks and Dowdle calls survive the report's team errors.** The analysts were talking about
real players; the report attached them to the wrong rosters. Wicks is Philadelphia, not Green Bay,
and Dowdle is Pittsburgh, not Dallas — the enthusiasm is sourced, the stated mechanism is not.

## 3. THE CORRECTION I HAD TO MAKE TO MY OWN OUTPUT

My first version of this sheet counted 9 target calls on Josh Downs and 8 on Wicks. Both were
inflated by the file overlap; the true figures are 6 and 6. **I built the sheet before checking
whether the two files were disjoint** — the same failure as reading a source without joining it to
anything. Caught by grouping on the quote text, which took one command.

---

**Files:** `ANALYST_CALLS.pdf` (one page) · `analyst_calls_joined.csv` (78 players, machine
readable). Nothing on the board changed.
