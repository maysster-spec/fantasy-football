# 64 — THE AUG-28 2026 PULL: FREEZE CONFIRMED, AND A CORRECTION TO DOC 63's TEST

**2026-08-28.** `espn_projections_2026_20260828_0856.csv`, 700 rows, captured 08:56 ET.
Pulled with `--seasons 2026 --sort draft` after the season picker was corrected.

---

## 0. A CORRECTION I MADE MID-ANALYSIS, RECORDED BECAUSE IT WAS NEARLY SHIPPED

The doc 63 §2 test says: *"0 rows changed → FREEZE."* Run literally against this pull it returns
**482 of 593 rows changed**, and the mechanical readout said **"doc 62 §5 becomes live."**

**That readout was wrong and I retracted it before acting on it.** The threshold was too crude:

| |delta| | players |
|---|---|
| exactly 0 | 37 |
| **< 0.5 pts** | **434** |
| 0.5 – 3 | 19 |
| 3 – 10 | 14 |
| > 10 | 15 |

**Median delta −0.000. Mean +0.108.** The elite tier moved by *hundredths*: Josh Allen +0.024,
Lamar Jackson +0.033, Jalen Hurts +0.022.

**This doc originally attributed those deltas to the Aug-28 `SCORING` patch. THAT WAS FALSE —
falsified by doc 67 §1 and independently re-verified.** `proj_2026` is ESPN's server-side
`appliedTotal` (pull script line 219). `SCORING` is referenced only inside `verify_scoring()` and
the reconciliation print — **it can never move an exported column.** Empirically: 525 of 525 rows
match `appliedTotal` to 0.0000000000.

**The deltas are real. ESPN re-forecast, in small amounts.** FREEZE does not depend on the
explanation — its evidence is §1's board-order test — but the forward read changes: combined with
the zero movement across 08-20 → 08-23, **ESPN appears to re-forecast in discrete batches.**
The Sep 5 board test is mandatory, not a formality.

**Doc 63 §2's test is hereby replaced.** Counting changed rows is the wrong test once a scoring
patch perturbs every row. **The test is whether the BOARD ORDER moves.**

---

## 1. THE REPLACEMENT TEST — BOARD ORDER

Rebuilt the skill board from each pull independently (QB12/RB30/WR30/TE12, VBD sort).

**Replacement levels — §4.1 stands unchanged:**

| | Aug 20 | Aug 28 | delta |
|---|---|---|---|
| RB30 | 168.589 | 168.586 | **−0.003** |
| WR30 | 163.540 | 163.533 | **−0.007** |
| TE12 | 140.295 | 140.289 | **−0.006** |
| QB12 | 341.603 | 341.099 | −0.504 |

**Top 161 board order, n=161 matched, zero dropouts:**

| | result |
|---|---|
| rank unchanged | **100 of 161** |
| moved ≤ 2 slots | **150 of 161** |
| moved > 5 slots | **4** |
| max move | 58 (Tank Dell) |

**±2 window at Matt's picks:** 8 → **5/5** · 17 → **5/5** · 32 → **5/5** · 41 → 4/5 · 56 → 4/5 ·
65 → **3/5** · 80 → 4/5 · 89 → **5/5**.

## 2. VERDICT: FREEZE. Doc 62's rebuild question still does not arise.

Replacement levels are identical to three decimals. The top of the board — where picks 8, 17 and
32 are decided — is untouched. **No rebuild. `board_v8_fixed.csv` stands.**

## 3. BUT THERE IS REAL NEWS IN THE MID-BOARD — handle as overrides, per doc 62 Option A

Twenty-nine players moved more than 3 projection points. These are genuine, and doc 62 §5 Option A
anticipated exactly this: *"Handle Sep 5 news manually as overrides at the pick."*

| player | pos | proj Aug 20 → Aug 28 | board rank |
|---|---|---|---|
| **Tank Dell** | WR | 125.1 → **78.6** (−46.5) | **134 → 192** |
| Deshaun Watson | QB | 140.4 → 89.2 (−51.2) | 453 → 425 |
| Shedeur Sanders | QB | 112.6 → **163.4** (+50.8) | 456 → 422 |
| Tyrone Tracy Jr. | RB | 58.6 → 34.9 (−23.7) | 232 → 312 |
| Najee Harris | RB | 45.9 → 72.2 (+26.3) | 265 → 210 |
| De'Zhaun Stribling | WR | 109.0 → 125.4 (+16.4) | 158 → **135** |
| Kayshon Boutte | WR | 72.3 → 90.0 (+17.6) | 201 → 174 |

**Tank Dell is the one that matters** — a 58-slot fall out of the range Matt drafts in.
The Cleveland QB swing (Watson down, Sanders up) is a depth-chart event, both far outside the
draftable range. **None of these is sourced yet, and doc 67 §1 makes them MORE important — they are confirmed re-forecasts, not artifacts.** — they are ESPN's projection changes, not news.
The Sept 5 news pass should confirm each with a citation before any of them moves a pick.

## 4. WHY THE JOIN WAS 593/700, NOT 700/700

Different universe, not missing players. The Aug-20 pull carried 556 rows with a projection; this
one carries 520, and the two pulls select a different tail (`--sort draft` vs whatever produced
Aug 20). The new file also carries two columns the old one lacks — `actual_2026` and
`raw_actual_stats` — because it was produced by the Aug-28 patched script.
**Every one of the Aug-20 top-161 is present in the new pull. Zero dropouts.** The join shortfall
is entirely in the undraftable tail and does not affect any conclusion above.

## 5. THE SEASON GUARD — Matt's suggestion, built and tested

`Espn_pull_projections.py` is now **14,992 bytes** (`16807f98494b4d5d`). Two changes:

- `DEFAULT_SEASONS = [2026]` — was `[2022, 2023, 2024]`. The bare command now pulls the draft season.
- `confirm_seasons()` runs before any network work and refuses a completed season unless a human
  types `historical`, or `--yes` is supplied for scripted runs.

| test | expected | result |
|---|---|---|
| `--seasons 2026` | proceed silently | **PASS** |
| `--seasons 2022 2023 2024`, non-interactive, no `--yes` | **REFUSE** | **PASS** |
| `--seasons 2024 --yes` | proceed | **PASS** |
| `--seasons 2024 2026` (mixed) | **REFUSE** | **PASS** |

## 6. HOUSEKEEPING

- `check_kit.py` — docstring made raw; the `SyntaxWarning: invalid escape sequence '\M'` is gone.
  Manifest re-pinned to the new pull-script hash. Now **4,270 bytes**.
- **`gone      G:\My Drive\Fantasy\Scripts` is a PASS, not an error.** That folder exists inside
  Google Drive but is not synced to a local path, so nothing can be executed from it. The
  handover's "third script location" is a Drive-side folder only. Noted in the script.
- **8 stragglers remain** in `Source\live_draft\` and `OneDrive\Fantasy\Scripts\`. This session can
  write files but cannot delete them; no delete capability is available on this bridge.

---

## ASSUMPTIONS

1. ~~The sub-0.5-point shift is the `SCORING` patch.~~ **FALSIFIED (doc 67 §1).** The shifts are
   genuine ESPN re-forecasts. Replaced by: **ESPN re-forecasts in discrete batches, not
   continuously** — zero movement 08-20 → 08-23, real movement by 08-28. **Invalidated by:** a
   Sep-5 pull showing either continuous drift or another zero-change interval.
2. `--sort draft` selects a superset of the draftable universe. Supported by zero dropouts in the
   Aug-20 top 161, not proven for the tail.
3. ESPN's projection changes for Dell, Watson and Sanders reflect real events. **Unsourced** —
   the Sept 5 news pass must confirm before any of them moves a pick.

**Most valuable missing input: a source for the Tank Dell change.** It is the only movement inside
the draftable range large enough to alter a decision.
