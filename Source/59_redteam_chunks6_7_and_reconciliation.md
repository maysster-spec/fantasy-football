# 59 — RED TEAM CHUNKS 6 AND 7, AND THE FULL RECONCILIATION
**Aug 27, 2026.** Export/injection (E1–E5) and the harness itself (H1–H5). **All 7 chunks and all
49 catalog rows now carry exactly one verdict. No coverage holes.**

---

## THE ANSWER, IN ONE LINE

**The harness was the worst part of the system.** Its headline check printed
*"SCORING CHECK PASSED (12-component reconstruction verified)"* **only when there was nothing to
verify**, its integrity module had zero callers, and its keeper guard was inverted — it passed the
broken state and failed the correct one. Every one is now repaired and **executed against the
defect that motivated it.**

---

## CHUNK 6 — EXPORT AND INJECTION

| id | constraint | verdict | evidence |
|---|---|---|---|
| E1 | `ESPN_ID` exact, int, no nulls, no dupes | **CLEAN** | 544 rows, `int64`, 0 nulls, 0 dupes; injector's `dropna().astype(int)` replayed → 544 in / 544 out. 10/10 ids spot-checked correct. 32 D/ST ids are negative, correctly encoded `−(16000 + proTeamId)`, 32/32 exact |
| E2 | row order IS the ranking | **CLEAN** | `prerank` == row index 1…544 exactly; 480 skill rows join the board with **0 adjacent inversions**; `vbd` monotonically non-increasing |
| E3 | K/D-ST last and correctly ordered | **CLEAN on the letter, WRONG ON THE PURPOSE** | D/ST ahead of K, both at the tail — but see below |
| E4 | keepers excluded | **CLEAN** | 0 of 12 present, checked by normalised name **and** by `espn_id` |
| E5 | count sane | **CLEAN** | 544 against 168 real selections = 3.2× coverage. Undersized is the dangerous direction; impossible here |

### The defect E3 passes on a technicality

The prerank list exists to protect Matt **if he times out** — ESPN then autodrafts his top
remaining ranked player. With all 64 streamers at ranks 481–544, that protection does not exist.

**Measured, 250 simulated drafts:** the best-ranked player still available *from this list* is

| his pick | p10 | median | p90 |
|---|---|---|---|
| 104 | 56 | 64 | 73 |
| 128 | 60 | 73 | 86 |
| **152** (D/ST slot) | **64** | **76** | **89** |
| **161** (K slot) | **65** | **77** | **90** |

Not 481. It plateaus around **rank 76**, because the board is VBD-ordered while the league drafts
on ADP — players Matt values above the market are still sitting there in round 13. **A timeout at
152 would have taken a skill player, and the draft would have ended with no D/ST and no K — two
empty starting slots every week.**

**Fixed by measurement, not by guessing.** Exactly **one** D/ST and **one** K are seeded at ranks
**74 and 75**. Re-measured:

| pick | P(a timeout takes a streamer) |
|---|---|
| 89 | **0%** |
| 104 | 4% |
| 128 | 31% |
| 137 | 38% |
| **152** | **53%** |
| **161** | **59%** |

Early picks are untouched; the designated streamer picks are now more likely than not to take the
right position; and because only one of each is seeded, a double-up is impossible. The other 62
stay at the tail as backup.

> **This cannot be made perfect.** No single ranking is simultaneously a good value board and a
> good full-autodraft fallback. Under *full* autodraft the position caps (RB 6, WR 6) still consume
> 14 picks before rank 74. The seed covers the realistic case — one or two timeouts — and that is
> the honest claim.

### The injector — every way it can corrupt

| line | issue |
|---|---|
| 64–68 | **A 200 is not verification.** The script never reads the response body, never counts what ESPN stored, never GETs the list back. Silent truncation or per-id rejection both print `"Success!"` |
| 62 | `requests.post` with **no timeout, no retry, no `raise_for_status`**. A hung socket at 7:05 PM on lock night is indistinguishable from success-in-progress |
| 43–44 | Blank-ID rows are dropped with a **print warning and the POST still fires** — and dropping a row shifts every subsequent rank up by one |
| 6 | Bare relative filename resolved against CWD, not `__file__`. Wrong CWD silently picks up an older copy |
| 56 | `"excludedPlayerIds": []` wipes any Do-Not-Draft list Matt set in the app, and leaves **3 flagged-unavailable players inside reachable range** (Alec Pierce OUT at 80, Zach Charbonnet OUT at 131, Jordyn Tyson DOUBTFUL at 175) |
| — | **Replace vs append is assumed, never verified.** Under append semantics a second run silently doubles the list, and the dedupe check would not fire — it inspects the CSV, never the server |

---

## CHUNK 7 — THE HARNESS ITSELF

| id | constraint | verdict | evidence |
|---|---|---|---|
| H1 | every guard fires on its motivating defect | **CONFIRMED DEFECT** | `assert_keepers_removed` was **inverted**: fed the broken universe → PASS; fed the correctly depleted pool → FAIL on all 12 |
| H2 | no threshold passes a known past failure | **CONFIRMED DEFECT** | `mincount={'D/ST':20}` — C3's surviving count was **29**. The gate passed the exact defect it was written for, and a sibling file *documented the hole* |
| H3 | failure branches print | **CONFIRMED DEFECT** | `anomalies` appended and **never printed, never returned**. `scoring_err`/`actual_err` appear only inside `if not scoring_err and not actual_err:` — a −38 point error produced **total silence** |
| H4 | counters distinguish present from non-zero | **CONFIRMED DEFECT** | `"SCORING CHECK PASSED"` printed when **zero players were verified**, including on C3's 29 defenses all at 50.0 |
| H5 | checkers point at the current spine | **CONFIRMED DEFECT** | `assert_replacement` → `KeyError: 'TOT'`; `assert_keepers_removed` → `KeyError: 'full'` |

**The overriding finding:** `code_integrity.py` had **zero importers**, and `report()` — the only
thing that turns failures into a non-zero exit — had **zero callers**. Its docstring read *"Runs
BEFORE any analysis. Every check raises, not warns."* Both clauses were false. The mechanical
cause is almost funny: the file is stored as **`code_integrity (1).py`**, which Python cannot import.

### False-confidence ranking

1. **`"SCORING CHECK PASSED (12-component reconstruction verified)"`** — prints PASS on zero
   checks, prints nothing on failure, and passes the literal C3 payload. The only guard in the
   codebase that makes an affirmative verification claim with no verification behind it.
2. `assert_keepers_removed` — inverted.
3. `code_integrity.py` as a module — strongest docstring, zero callers, no `raise`.
4. `assert_coverage` D/ST ≥ 20 — hole written down in a sibling file, never closed.

### Repaired, and executed

```
py code_integrity.py     ->  20 checks, ALL PASS, exit 0
```

Every repair was verified by **making the guard fire**:

| guard | repair | fires on its defect? |
|---|---|---|
| `assert_replacement` | `'TOT'` → `'proj_leaguepts'`, **and drop nulls/zeros/synthetic before sorting** | yes — it was returning `nan` because `np.sort` puts NaN last and `[::-1]` put it first. **The guard itself violated V2.** |
| `assert_keepers_removed` | inverted to `leaked = [k for k in keepers if in pool]`, pointed at the **board** not the spine | yes — leaked keeper → `1 keeper(s) STILL IN THE POOL: ['Travis Etienne']` |
| `assert_coverage` | D/ST and K gates 20 → **32** (both pools are exactly 32 NFL teams) | yes — 29 defenses → `only 29 (expect >= 32)` |
| `report()` | returned `None`, so the exit code contradicted the printed message | yes — exit 0 on pass, 1 on fail |
| new `run_all()` | the module is now runnable and checks the board and prerank too | 20 checks |

---

## TWO MORE LIVE DEFECTS FOUND AND FIXED

**1. The engine loaded the wrong file as the streamer list — and I caused it.**
`board_csv.replace('board_v7_2026.csv','board_v7_kdst_separate.csv')` is a **no-op for any other
board filename**. When I renamed the board to `board_v8_fixed.csv` in doc 58, the engine loaded the
*skill board* as the streamer list: 480 rows, `streamers('D/ST')` → `[]`, and picks 152/161 would
have rendered an empty table under "take the top one left." The surrounding
`except Exception: <empty DataFrame>` swallowed the other half.
**Fixed:** resolved by directory, explicit `kdst_csv` parameter, an assert that the file contains
only K and D/ST, and a minimum count of 12 each. No bare `except`.

**2. `board_v7_kdst_separate.csv` on disk was still the pre-fix artifact.** Doc 57 fixed the
*builder*; the CSV was never regenerated. 26 kickers still sat ahead of the best defense.
**No guard compares an artifact to its builder** — that is the general lesson.
**Fixed:** regenerated D/ST-first.

**3. `code_league_sim.py` had 10 of 12 keeper bye weeks wrong** — my own hand-typed table rather
than a read from the spine. Zay Flowers 7 vs 13, Javonte Williams 5 vs 14, Rashee Rice 10 vs 5.
It gave Pickens (DAL) bye 14 and Javonte Williams (DAL) bye 5 — internally impossible.
**Fixed from the spine, and doc 55 re-run.** The conclusions hold:

| rule | P(1st) before | P(1st) after | E$ after |
|---|---|---|---|
| **rollout + LATE tilt (rd 9+)** | 18.5% | **19.0%** | **$169** |
| rollout | 17.8% | 17.5% | $157 |
| upside tilt everywhere | 14.2% | 16.0% | $146 |
| static VBD + caps | 14.8% | 12.5% | $136 |

Ordering unchanged; "risk late, never early" survives. The penalty for tilting everywhere shrank
(−$22 → −$11 at the smaller N) but stayed negative.

---

## FULL RECONCILIATION — ALL 7 CHUNKS, 49 ROWS

| chunk | rows | clean | defects | doc |
|---|---|---|---|---|
| 1 · scoring conversion | 10 | 9 | 1 | 49 |
| 2 · source acquisition | 8 | 3 | 5 | 56 |
| 3 · replacement and VBD | 7 | 2 | 5 | 57 |
| 4 · identity and joins | 6 | 1 | 5 | 58 |
| 5 · board assembly | 6 | 4 | 2 | 58 |
| 6 · export and injection | 5 | 5 | 0* | 59 |
| 7 · the harness | 5 | 0 | **5** | 59 |
| **total** | **49** | **24** | **23** | |

\* E3 passes the constraint as written and fails its purpose — recorded as a purpose defect, fixed.

**Every row carries exactly one verdict. No coverage holes.**

### What the seven chunks actually taught

1. **The harness was the weakest link, not the model.** Chunk 7 had a 0% clean rate. Every other
   stage was at least partly sound; the thing meant to protect them was not.
2. **Slicing by mechanism worked.** The K/D-ST defect surfaced in five separate files across
   chunks 3, 5, 6 and 7. A per-file review would have judged each locally reasonable.
3. **Adversarial agents find defects and misprice them.** Three times an agent identified a real
   defect and overstated its cost by one to two orders of magnitude (doc 57: "78 points" measured
   at **+0.26**). **Every severity in these documents that matters was re-measured here.**
4. **Two of the worst defects were in code written during this red team.** The engine's streamer
   path and the raw-points rollout sort were both mine, both introduced while fixing other things.
   Fixes need the same adversarial treatment as the original code.
5. **The most dangerous defects were silent.** The keeper-pick count, the name join, the vacuous
   SCORING PASS — none produced an error message. Every fix in these documents converts a silent
   failure into a loud one, which matters more than the individual numbers.

---

## WHAT THIS CHANGES

1. **Re-inject the prerank file.** It changed again — one D/ST and one K now sit at ranks 74–75.
2. **Run `py code_integrity.py` before every rebuild.** It works now, and exits non-zero on failure.
3. **Before Sept 5:** patch `SCORING` with ids 19/26/44, add the `else` branch, timestamp output
   filenames to the minute.
4. **Before Sept 7:** `--replay 2025`, and test the injector against a throwaway mock to settle
   whether ESPN accepts negative D/ST ids and whether the POST replaces or appends.
5. **Adopt directive v5** — it carries every corrected constant.

## LIMITS

1. Three claims remain **CANNOT VERIFY** without a live ESPN call: keeper rows in the live feed,
   negative-id acceptance, replace-vs-append. All three are testable by Matt in minutes.
2. `code_rebuild_spine_v5.py` was never in any audit set. The spine's own `vbd` for K/D-ST is still
   poisoned at source; the board is clean only because a runtime guard nulls it in memory.
3. `top_400_projections_2026.csv` is still in `Source/` — wrong season, no provenance, unquarantined.
4. The seven chunks audited the pipeline as it stood. Five of seven chunks changed it.
   **A re-run of chunks 1–5 against the current code has not been done.**

## §7 CLOSE-OUT

**Top 3 assumptions:**
1. **The repaired guards now fire on every defect class this project has seen.** *Invalidated by:*
   the next defect. Twenty-three were found in seven chunks; the rate of new discovery had not
   fallen by chunk 7, which suggests the catalog is incomplete rather than exhausted.
2. **Seeding one streamer at rank 74 is net positive.** *Rests on* a timeout at 128/137 costing
   less than an empty D/ST slot all season. Reasonable, unmeasured.
3. **The artifacts now match their builders.** *Invalidated by:* the fact that this exact
   assumption failed twice today. **Nothing in the pipeline compares an output to the code that
   claims to produce it** — that is the highest-value guard still missing.

**What would most improve this:** a **build manifest** — every artifact stamped with the script,
the input hashes and the timestamp that produced it, and a checker that refuses any artifact whose
stamp does not match a re-run. Three of today's defects were stale artifacts, not bad code.
