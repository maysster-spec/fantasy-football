# 63 — PROJECTION DRIFT, MEASURED. AND THE SPINE BUILDER WAS NOT ON THE MACHINE.

**Aug 28, 2026. Answers the question doc 62 §4 said must not be guessed.**

---

## 1. THE MEASUREMENT

Doc 62 §4 priced FREEZE as costing "whatever two weeks of projection drift is worth —
unmeasured." **Measured on the only interval available:** the 08-20 and 08-23 pulls, both 700 rows,
joined on `espn_id`, 700/700 matched.

| column | rows changed of 700 | max delta |
|---|---|---|
| **`proj_2026`** | **0** | **0.000** |
| `rank_std` | 0 | — |
| `rank_ppr` | 0 | — |
| `proj_2025`, `actual_2025` | 0 | — |
| `injuryStatus` | 31 | — |
| **`espn_adp`** | **504** | **36.21 picks** |
| `pct_owned` | 526 | 17.01 |
| `captured_at` | 700 | — |

Rebuilt the skill board from each pull independently (QB12/RB30/WR30/TE12 replacement, VBD sort):

- **All four replacement levels identical to 2 dp** (341.60 / 168.59 / 163.54 / 140.29).
- **Top 161: 0 of 161 rows changed projection. 0 moved a single board slot. 0 players swapped in.**
- The ±2 window around picks 8, 17, 32, 41, 56 and 65 was **5/5 unchanged at every pick.**

**ESPN's season-long projections did not move at all. What moved was ADP, ownership and injury
status.** Doc 62's cost was framed on the one axis that turns out to be static.

## 2. SUPERSEDED — DO NOT USE THE TEST THAT WAS HERE

**This section contained a "count changed `proj_2026` rows; 0 → FREEZE" test. It has been deleted,
not annotated, because leaving it on the page is how a future session runs the wrong test.**

Counting changed rows is wrong once anything perturbs every row by a fraction. Run against the
Aug-28 pull it returned "482 of 593 changed" and pointed at RECONSTRUCT, when the correct answer
was FREEZE.

**The test is board ORDER. It lives in `claude/64_aug28_pull_and_freeze_verdict.md` §1.**

The §1 measurement below (0 of 700 rows moved between the 08-20 and 08-23 pulls) stands as a
finding. **It does not generalise:** by Aug 28 ESPN had re-forecast in small amounts, so its
projections move in discrete batches rather than continuously (doc 67 §1). The Sep 5 board-order
test is therefore mandatory, not a formality.

## 3. A SECOND ARTIFACT WITH NO BUILDER — ONE LAYER ABOVE DOC 62

**`code_rebuild_spine_v5.py` was not in `2026\Source\` at all.** It existed only in the project
doc store, while its output `code_universe_v5.csv` (144,587 bytes) sat in `Source\` with nothing
beside it that could remake it. Same defect class doc 62 found for the board, one layer up.
**Now committed to `Source\`.**

Doc 62's central claim was re-verified independently rather than taken on trust — 19 `.py` files
staged and grepped:

- scripts writing `board_v8_fixed.csv`: **zero**. Three read it. ✓
- every board `to_csv` target in Source: **`board_v7_2026.csv`** only — the trashed trap. ✓
- `code_build_board_v7.py` line 30 reads hardcoded `espn_projections_2026_20260823.csv`. ✓

**New, and it is why the patch below refuses instead of auto-globbing:** `code_integrity.py`
checks `board no null vbd`, `board no K/DST`, and unique/non-null `espn_id` — **it does not compare
the spine's projections to the board's.** A spine rebuilt on fresh projections beside a frozen
board would pass all 20 checks silently.

*(That same check, `board no K/DST`, independently confirms doc 61 D2: the board is clean by
separation and the harness enforces it.)*

## 4. THE PATCH — `code_rebuild_spine_v5.py`, 8,079 bytes

Four changes, each traced to a measured defect, each marked `[P-…]` in the source.

| tag | change | why |
|---|---|---|
| **P-D5** | input pinned to `PINNED`; **refuses to run if a newer pull exists** | doc 61 D5 |
| **P-D2** | `vbd` nulled at source for K and D/ST | doc 61 D2 |
| **P-D3** | `pd.to_numeric(..., errors='coerce')` on both sides of the synthetic join | doc 61 D3 |
| **P-D1** | prints the crosswalk **match rate**; warns under 80% | doc 61 D1 |

**P-D5 deliberately does NOT auto-glob to the newest pull.** That was the obvious fix and it is the
wrong one: given §3, an auto-globbing spine would silently desync from a frozen board and the
harness would not catch it. It stops instead, prints the §2 test, and makes a human decide.

**P-D1 is a warning, not an assert.** The true expected match rate has never been measured on real
inputs; an assert at a guessed threshold could fail spuriously nine days before the draft.

### Gate tested — it fires only where it should

| test | expect | result |
|---|---|---|
| pinned pull only | pass through | **quiet** ✓ |
| pinned + `..._20260905_1830.csv` | refuse | **PULL/SPINE MISMATCH, exit 1** ✓ |
| pinned + an *older* pull | pass through | **quiet** ✓ |
| pinned + the real `..._20260823.csv` | refuse | **PULL/SPINE MISMATCH, exit 1** ✓ |

**The patch is not otherwise executed.** Its real inputs (`src/code_universe.csv`) were not staged,
so the body past the gate is unverified beyond a syntax check. **It should not be run for the first
time on Sep 5.** Run it once against `Source\` before then, or leave it unrun and frozen.

## 5. WHAT CHANGES

1. **Nothing needs rebuilding before Sep 5.** On the measured evidence the board is not stale.
2. **Sep 5: run the §2 diff first.** It is five lines and it decides doc 62 outright.
3. **The reconstruct work in doc 62 §5 Option B stays unstarted** unless that diff is non-zero.
4. **ADP/injury refresh is a separate live question** and is not answered here.

**Assumptions.** (a) ESPN's `proj_2026` update cadence is slower than 3 days — one interval, and
final cuts are not in it. (b) Freezing the board is acceptable if projections are unchanged, i.e.
nothing else in the board depends on the pull date. (c) The Sep 5 pull will join cleanly on
`espn_id` at 700/700 as both prior pulls did.
**What would invalidate (a):** the Sep 5 diff itself. **Most valuable missing input: a pull from
before Aug 20** — a second interval would turn one observation into a cadence.
