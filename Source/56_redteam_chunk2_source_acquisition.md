# 56 — RED TEAM CHUNK 2 OF 7: SOURCE ACQUISITION (A1–A8)
**Aug 27, 2026.** Run under the doc-48 protocol: a fresh adversarial subagent produced verdicts,
a second independent subagent was tasked with **refuting** them, and every disputed number was
adjudicated here against source. The refuter overturned or corrected **four** of the first
agent's eight verdicts — which is the protocol working as designed.

---

## THE ANSWER, IN ONE LINE

**The pull script's only automated integrity check can never pass on real data, and therefore
only ever prints PASS when the pull is empty.** That single defect is why the 2023 disaster
shipped green, and it is still live in the script that will be run on **Sept 5**.

---

## RECONCILIATION — ALL EIGHT ROWS CARRY EXACTLY ONE VERDICT

| id | constraint | verdict | evidence |
|---|---|---|---|
| A1 | pull filters on `seasonId` | **CLEAN** | `if str(s.get("id")) == target_id` with `target_id = f"{src}{split}{season}"`; all 1,399 season-total ids in the raw payload encode the season in the suffix, **0 mismatches**. Parsing the 2023 payload as `--seasons 2024` yields `proj_2024` non-null = **0/700** — it fails safe |
| A2 | `statSourceId` 0/1 never transposed | **CLEAN** | `proj_2023` reproduces the `statSourceId==1` total on **700/700**; `actual_2023` reproduces `statSourceId==0` on **700/700**; cross-test matches only 2–33 of ~500. `corr(proj_2023, actual_2023) = 0.096` |
| A3 | hollow rows → NULL, never `0.0` | **CONFIRMED DEFECT** | `proj = cur.get("appliedTotal") if cur else None` — the row exists and ESPN reports `0.0`. **575/699 in `proj_2023`; 945 across current-season columns; 1,887 across all `proj_*` columns** |
| A4 | ADP sentinel never used to rank | **CLEAN in the live path · DEFECT in the stale spine** | Pull script passes ADP through without ordering. The **live board reads `espn_projections_2026_20260823.csv` directly** and matches it 480/480. But `code_universe_v5.csv` is sorted ascending by `adp_pick`, so **its file order is the sentinel order** for 492 rows, 144 of which have no fallback rank either |
| A5 | capture date on every derived file | **CONFIRMED DEFECT** | `captured_at` present 700/700 on all ten ESPN/universe CSVs. **`top_400_projections_2026.csv` has two columns and no date** |
| A6 | 700-row coverage, short pulls flagged | **CONFIRMED DEFECT — but the wrong invariant** | `LIMIT` never compared to `len(df)`. **However: all four 2023 pulls returned exactly 700 rows.** A row-count check would have caught none of them |
| A7 | `--raw` blocked for multiple seasons | **CONFIRMED DEFECT — corruption is metadata-only** | `for season in a.seasons: process_single_season(..., a.raw)`, no guard. Executed: three CSVs written. The wrong-season files carry **0/700 season values** but real `Player`, `pos`, `team`, `espn_adp` from the source payload |
| A8 | `--raw` says the prior-year columns are null | **CLEAN** | The first agent called this a defect. Refuted and adjudicated: the script prints `carry a {prior} PROJECTION : 0` and `carry a {prior} ACTUAL : 0` on every run. A count line, not a warning — but the constraint is met |

**Coverage: 8 of 8 rows carry a verdict. No holes.**

---

## THE FINDING THAT MATTERS — H3/S2 RESOLVED WITH A MECHANISM

### The integrity check is structurally incapable of passing

```python
if not scoring_err and not actual_err:
    print("  SCORING CHECK PASSED (12-component reconstruction verified).")
return df                      # <- no else. Failure prints nothing.
```

Reconstructing league points from the stored stat lines and comparing to ESPN's own totals,
2023 file:

| column | reconstruction matches ESPN within 1.0 pt | mismatches |
|---|---|---|
| `proj_2023` | 532 / 559 (95%) | **27, all kickers** — expected, the map is offence-only |
| `actual_2023` | 456 / 609 (**75%**) | **153 — of which QB 33, WR 23, RB 20, TE 7** |

The 83 skill-position mismatches are not K/D-ST spill. **65 of the 83 are explained exactly by
the two-point-conversion stat ids `19` / `26` / `44`, which appear only on ACTUAL stat lines and
are absent from the `SCORING` map** (the map carries `62`, the projection-side id, only). Josh
Allen 2023: ESPN 448.8, reconstruction 444.6, and his line carries `"19": 3.0`.

**Consequence, and this is the whole point.** `actual_err` is non-empty on **every** pull that
contains real actuals. So `if not scoring_err and not actual_err` is **False on every good pull**
and **True on every empty one**. Confirmed by execution: the two season-empty files produced by
the A7 defect both printed *"SCORING CHECK PASSED (12-component reconstruction verified)"*, and
the one file with real data did not.

> **The only automated integrity signal in the acquisition stage fires exclusively on failure.**

This closes chunk 1's open item **S2** ("204 points sit on the board unexamined" — two-point
conversions) with a cause, and it is the mechanism behind `ERROR_PATTERNS` **H3**.

**Fix (three lines):** add `19: 2.0, 26: 2.0, 44: 2.0` to `SCORING`, gate the reconstruction on
`pos in {QB,RB,WR,TE}`, and give the branch an `else` that prints the failures and exits non-zero.

---

## OTHER CONFIRMED DEFECTS, RANKED BY WHAT THEY COST

### 1. The historical API is nondeterministic and nothing detects it — `[TESTED]`

Four pulls of season 2023, same script, same cookies:

| capture | `proj_2023` non-null | `actual_2023` non-null |
|---|---|---|
| Aug 24, 23:49 | **699** | 700 |
| Aug 25, 07:22 | 96 | 436 |
| Aug 25, 08:14 | 96 | 436 |
| Aug 25, 08:52 | 124 | 609 |

The two 96-row files are **not duplicates** — they disagree on `proj_2023`, `actual_2023`,
`proj_2022` and `actual_2022`. All four were written silently. **Any conclusion drawn from a 2023
file depends on which pull produced it**, and docs 40/41's verdict that "2023 is dead" was reached
on the two worst captures. **The Aug 24 file has 699 projections and may be usable.** This should
be checked before Sept 5 — it would restore a fifth season to every backtest.

### 2. Same-day re-runs silently overwrite the CSV *and* the raw JSON backup

```python
out     = outdir / f"espn_projections_{season}_{dt.date.today():%Y%m%d}.csv"
rawpath = outdir / f"espn_raw_{season}_{dt.date.today():%Y%m%d}.json"
```

No timestamp, no collision check. Combined with defect 1, **a degraded second pull destroys a good
first pull.** The three Aug 25 files survive only because someone hand-renamed them. **This is
directly live for the Sept 5 refresh and the Sept 7 keeper-lock rebuild**, where a re-run is likely.

### 3. `SystemExit` escapes the prior-season fallback

`fetch()` ends with `raise SystemExit(...)`; the caller guards with `except Exception`.
`issubclass(SystemExit, Exception)` is **False**. The graceful-degradation path is unreachable — a
failed prior-season fetch kills a multi-season run mid-loop, after earlier seasons have written.

### 4. `COOKIES` is never assigned

Line 26 is commented out. AST scan: zero assignments, one reference. The script as it sits on
disk **cannot run**. It fails loudly (the `NameError` text is printed verbatim four times and the
final line names `COOKIES`), so there is no silent corruption — but Matt must paste the cookies
back in before Sept 5, and the copy in Drive is not the copy that works.

### 5. `top_400_projections_2026.csv` is the **2025** projection

Joined on player name, 400/400 matched: **355 rows equal `proj_2025`**, only **45 equal
`proj_2026`**. Gibbs 287.05 (2025) rather than 330.90 (2026). Nacua 245.97 rather than 294.82.
No capture date (A5).

**Blast radius: none, verified.** `code_universe_v5.csv` carries Gibbs at 330.896435 — the 2026
value — so the live spine does not consume this file. It is a stale artifact that should be
deleted before someone picks it up.

### 6. `actual_2026` is 700 fabricated zeros

`espn_projections_2026_20260823.csv` carries an `actual_2026` column that is `0.0` on 700/700 rows
with `raw_actual_stats == '{}'` on 700/700, for a season not yet played. Same mechanism as A3
applied to a column that should not exist.

---

## WHAT THE REFUTATION PASS OVERTURNED

Recorded because the protocol's value is in this column, not in the verdicts.

| first agent said | adjudicated |
|---|---|
| A8 CONFIRMED DEFECT — "prints no statement" | **Wrong.** It prints `carry a {prior} PROJECTION : 0`. A8 is CLEAN |
| A3 — "945 zeros, **zero legitimate**" | **Overstated.** 945 is current-season columns only; all `proj_*` columns give **1,887**. And two zeros are legitimate — Nick Bellore (16 non-scoring stat keys) and Scott Matlock — both non-fantasy players. Defect stands, absolute claim does not |
| A7 — wrong-season files hold "byte-for-byte the 2023 payload's values" | **Overstated.** Season columns are 0/700; only metadata carries over. Still a corruption vector via filename, but a different remediation |
| A4 CLEAN | **Split.** Clean for the pull script and for the live board; the stale spine's file order *is* the sentinel order |
| — | **Refuter found the headline** (the vacuous PASS) that the first agent missed |

Conversely, the refuter overreached once: it reported the live spine as carrying 3-day-stale ADP.
**Checked here: `board_v7_2026.csv` matches the Aug 23 capture on 480/480 rows and its injury
flags match Aug 23 exactly** — including Ashton Jeanty as QUESTIONABLE at ADP 16.6. The staleness
is real in `code_universe_v5.csv` and **inert for the board.**

---

## WHAT THIS CHANGES

1. **Patch `SCORING` and the check branch before Sept 5.** Three lines; without them the pull
   self-certifies on exactly the failures you need to catch.
2. **Timestamp the output filenames** to the minute, or refuse to overwrite. The Sept 5 and Sept 7
   refreshes are the exact scenario this destroys.
3. **Paste `COOKIES` back into the Drive copy** — the archived script cannot run.
4. **Re-examine the Aug 24 2023 pull.** 699 projections against 96–124 in the files that condemned
   2023. If it holds up, five seasons of backtest become available instead of four.
5. **Delete `top_400_projections_2026.csv`.** Wrong season, no provenance, not consumed.
6. **Add a `--raw` multi-season guard** and change the coverage check from row count to
   *non-null projection count* — row count is the wrong invariant and would have caught nothing.

## LIMITS

1. Two subagents plus adjudication here. Both agents shared the same file set; a defect requiring
   a file not staged would be invisible to both.
2. The A2 verdict rests on ESPN's id-string format (`{src}{split}{season}`) being stable. The code
   never reads the `seasonId` field sitting beside it. Correct today, unasserted.
3. The Aug 24 2023 file's 699 projections have **not** been validated here — only counted. Docs
   40/41's conclusion is questioned, not overturned.
4. No verdict was reached on whether ESPN's nondeterminism is rate-limiting, cookie expiry, or
   genuine data loss.

## §7 CLOSE-OUT

**Top 3 assumptions:**
1. **The script on Drive is the one that will run Sept 5.** *Invalidated by:* Matt having a working
   copy elsewhere with cookies pasted in — which he must, since these files were produced. **The
   audited artifact may not be the operational one**, and that gap should be closed by pointing at
   one canonical file.
2. **A3's false zeros do not touch the 2026 board.** *Verified:* all 31 zeros in `proj_2026` sit at
   ADP ≥ 169.9. Historical files are corrupted; the draft board is not.
3. **The two-point ids are 19/26/44 at 2.0 each.** *Invalidated by:* the residual — they explain 65
   of 83 mismatches exactly, leaving 18 unexplained. Something else is also missing from the map.

**What would most improve this:** the **league settings export**, so the `SCORING` map can be
reconciled line by line against ESPN's own scoring rules rather than inferred from reconstruction
residuals. That is also chunk 1's S4 ("no component is MISSING entirely"), which cannot be closed
without it.
