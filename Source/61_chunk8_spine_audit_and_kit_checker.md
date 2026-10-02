# 61 — CHUNK 8 AUDIT (`code_rebuild_spine_v5.py`) + THE KIT CHECKER
**2026-08-28. Two deliverables: `check_kit.py` (shipped, tested to fire) and the first audit of
the spine builder.**

---

## 0. TWO CORRECTIONS TO THE PRIOR SESSION, BOTH MATT'S CATCH

**C1. A provenance manifest cannot catch the Chunk 8 defect. The claim is withdrawn.**
A manifest verifies artifact↔builder consistency. Chunk 8 is a *builder-correctness* defect.
Re-run the builder, get the same output, hashes agree, checker prints PASS. It **certifies** the
defect. The prior session asserted the opposite and had not tested it.

**C2. "The single highest-value thing left" was an unmeasured severity claim.** Inherited from the
handover and repeated as an argument for a week of work. Nobody has priced the three Aug-27
stale-artifact defects. Per §0.2 that should have been stated, not used as urgency.

**Resolution of the cost question:** the cheap checker took ~30 minutes, so cost-benefit is moot at
that price. **The full stamp-and-re-run manifest is NOT recommended before the draft** — new code
nine days out, against an unpriced risk, and it does not cover the failure mode that actually bit
(stale copy *across locations*, which is a comparison, not a stamp).

---

## 1. `check_kit.py` — SHIPPED AND PROVEN TO FIRE

Compares every known copy of every draft-night file against a pinned size+sha256 manifest.
**Scope, stated honestly: it catches one failure mode — the same filename holding different bytes
in different places. It does NOT verify that any file is correct.**

### Adversarial test results — 6/6, the guard fires

| # | planted defect | expect | result |
|---|---|---|---|
| A | clean tree | exit 0 | **PASS** |
| B | **`live_draft.py` truncated to 14,636 B** (the real Aug-28 defect) | STALE, exit 1 | **PASS** |
| C | **`board_v8_fixed.csv` right size (41,127), one byte flipped** | STALE, exit 1 | **PASS** |
| D | sixth file dropped in the five-file kit | EXTRA, exit 1 | **PASS** |
| E | missing file | MISSING, exit 1 | **PASS** |
| F | missing folder | MISSING FOLDER, exit 1 | **PASS** |

**Case C is why byte *and* hash was the right call — a size-only check passes it.**

On the first run the harness's own assert fired on a bug in test B (the file was opened for write,
truncating it, before being read). Recorded because it is the same class of silent error the
project keeps finding: the test would otherwise have "passed" against a 0-byte file.

### Pinned manifest (hashes computed 2026-08-28 from the live Drive/OneDrive copies)

| file | bytes | sha256[:16] |
|---|---|---|
| `live_draft.py` | 15,391 | `752e2b4a8753a6c7` |
| `code_live_engine.py` | 15,308 | `6246a1e81cbb57e2` |
| `board_v8_fixed.csv` | 41,127 | `c65edcc41fff2507` |
| `board_v7_kdst_separate.csv` | 3,143 | `1b2e61d507f4a648` |
| `ESPN_prerank_with_ids.csv` | 33,216 | `899634df68e0e527` |
| `Espn_pull_projections.py` | 13,037 | `6043d5a1dfc7d328` |
| `espn_draft_injector_Gemini.py` | 4,616 | `00f4a093c6762378` |

### Verified live on 2026-08-28
- `Source\live_draft\` — exactly five files, **all byte counts and hashes match.**
- `OneDrive\Fantasy\Scripts\` — prerank, pull script and injector all match.
- **The two `ESPN_prerank_with_ids.csv` copies are byte-identical** (`cmp` clean, same sha256).
  Same size was not assumed to mean same content; it was checked.
- `G:\My Drive\Fantasy\Scripts\` — **NOT verified.** Outside the two granted folder roots.
  The script covers it; this session could not. **Run `check_kit.py` to close that gap.**

**Install to `...\2026\Source\`, NOT into `live_draft\`** — a sixth file in the kit folder is
itself a defect and the checker would flag its own presence.

---

## 2. CHUNK 8 — FIRST AUDIT OF `code_rebuild_spine_v5.py`

Five claims tested. **Two confirmed, one confirmed at far lower severity than the prior framing,
one latent, one killed.**

### D5 — CONFIRMED, HIGHEST VALUE. Hardcoded input vs minute-stamped pull output.

```
spine reads : SRC + 'espn_projections_2026_20260820.csv'                  # hardcoded
pull writes : outdir / f"espn_projections_{season}_{now:%Y%m%d_%H%M}.csv" # line 292
```

**The Aug-28 pull-script patch introduced this.** Minute-stamped filenames were the fix for a
different defect; they broke the spine's hardcoded read.

**On Sep 5 the pull writes `espn_projections_2026_20260905_HHMM.csv`, the spine reads the Aug-20
file, and rebuilds the entire player universe on 16-day-old projections — stamped
`built_at = 2026-09-05`.** No error. The only tell is `proj_src`, still reading `espn_20260820`,
and nothing asserts it.

**Fix before Sep 5:** glob the newest matching file, assert its date is within N days of today.
Three lines. This is the one item that must not slip.

### D1 — CONFIRMED. `assert len(s)==pre` is a vacuous guard.

Measured: a left merge on a key with trailing whitespace matched **0 of 3 rows** and the assert
**passed**. A left merge always preserves left length, so the guard cannot fire on a broken join.
It only catches duplicate right keys, which the preceding assert already covers.

*(A dtype mismatch — int vs str — raises `ValueError` loudly. Whitespace is the silent case, and
whitespace is exactly the ERROR_PATTERNS C1 failure that made the #1 player undraftable.)*

**Fix:** assert a match *rate* — `assert s['gsis_id'].notna().sum() >= 0.95*len(s)`.

### D2 — CONFIRMED, BUT THE PRIOR FRAMING WAS WRONG IN BOTH DIRECTIONS.

The spine writes cross-position `vbd` for K and D/ST. Real. The severity is not what either the
handover or the prior session said.

**Handover correction.** §3 says the board "is clean only because a runtime guard nulls `vbd` in
memory." **Measured: `board_v8_fixed.csv` holds 480 rows and ZERO K, ZERO D/ST** — they live in
`board_v7_kdst_separate.csv`. The board is clean by *separation*, a stronger property than a
runtime null.

**Magnitude, measured on the real projections:**

| | value |
|---|---|
| repl(K12) | 144.00 · K vbd range −22.3 … **+27.7** |
| repl(D/ST12) | 95.88 · D/ST vbd range −40.5 … **+32.5** |
| skill vbd | max +162.3 · median −117.0 |

On a naive cross-position sort of the poisoned spine, the **best D/ST ranks 34th and the best K
39th** — round 3, inside the pick-41 window. 12 K/D-ST rows outrank the 50th skill player, 49
outrank the 100th, all 64 outrank the 168th.

**An earlier draft of this audit claimed the poison "surfaces kickers at the top of the board." A
constructed test killed that** (K +23.0 vs WR +101.5), and the real-data measurement put it at
rank 34–39 instead. Material, inside the drafted region, **not** top-of-board.

**Blast radius: zero on the current draft-night path** — nothing in the shipped kit reads the
spine's `vbd` for K or D/ST. Exposure is any *new* consumer reading `code_universe_v5.csv`
directly. **Fix at source:** `s.loc[s['pos'].isin(['K','D/ST']), 'vbd'] = np.nan`.

### D3 — LATENT, NOT LIVE. `isin` on the synthetic flag.

`s['espn_id'].isin(set(syn))` with `syn` cast to `int`. Measured across dtypes:

| dtype of `s['espn_id']` | matched |
|---|---|
| int64 | OK |
| float64 | OK |
| float64 with NaN | OK |
| **object / str** | **0 — silently all-False** |

`board_v8_fixed.csv` carries `espn_id` as **int64**, so this is not firing today. It is one
`dtype=str` read away from silently disabling the synthetic flag with no error.
**Fix:** coerce both sides with `pd.to_numeric(..., errors='coerce')`.

### D4 — NOT A DEFECT. Hypothesis killed.

`s['captured_at'] = e['captured_at']` after a merge was suspected of positional misalignment.
Tested: pandas aligns Series assignment on **index label**, not position, so a reordered or
non-default index still lands correctly. **No defect. Recorded so nobody re-raises it.**

### §1.1 ADP provenance — noted, low severity.

The spine sets `adp_pick = espn_adp` and never calls `code_adp_guard.load_preseason_adp()`. For a
2026 **preseason** pull that is the correct market, and the input filename is pinned to a preseason
file, so it is not currently wrong. An unguarded path, not a live defect — **but D5's fix must not
turn the pinned filename into a glob that could reach a historical pull.**

---

## 3. WHAT THIS CHANGES

1. **D5 must be fixed before Sep 5.** The only finding that silently corrupts draft-night inputs,
   and the Sep 5 refresh is exactly when it fires.
2. **The full provenance manifest is deprioritised**, on C1 and C2 above.
3. **`check_kit.py` covers the failure mode that actually bit**, is tested to fire, and is done.

**Top three assumptions.** (a) The Sep 5 refresh runs the pull script *then* the spine builder — if
the spine is not re-run, D5 does not fire. (b) `board_v8_fixed.csv` is the only board the live kit
reads. (c) No unlisted consumer reads `code_universe_v5.csv`.
**What would invalidate each:** (a) the actual Sep 5 command sequence; (b) a grep of the kit for
board filenames; (c) a grep of all scripts for `code_universe_v5`.
**Most valuable missing input: confirmation of the exact Sep 5 command sequence.**
