# 65 — RED-TEAM HANDOFF: EVERYTHING THE AUG-28 SIDE SESSION DID

> **CLOSED 2026-08-28 by `claude/67_redteam_of_doc65.md`. C21 falsified; §6.4/6.5/6.9 judged
> overstated; §6.6 judged UNDERSTATED and is now the critical-path item. Read doc 67 with this.**
**Written 2026-08-28 by the side session, FOR the originating chat to attack.**
**Draft: Mon Sept 7, 8:00 PM ET. Keeper lock 7:00 PM. 10 days out.**

You are being asked to red-team this work, not to accept it. Every claim below carries its
measurement so you can falsify it. **§6 is the list of things I think are most likely wrong —
start there.** Where I retracted something mid-session I have said so; check whether the
retraction was itself correct.

---

## 1. WHAT TO READ, IN ORDER (all in the project store)

1. `claude/64_aug28_pull_and_freeze_verdict.md` — the live decision. Read first.
2. `claude/63_projection_drift_measured.md` — **its §2 test is SUPERSEDED by doc 64 §0. See §6.1.**
3. `claude/62_board_has_no_builder.md` — not mine; I verified it independently (C7).
4. `claude/61_chunk8_spine_audit_and_kit_checker.md` — the spine audit and the kit checker.
5. `claude/00_CALENDAR_TO_DRAFT.md` — the forward path and the canonical file map.

Do **not** re-read docs 40–59; nothing here contradicts them except where §5 says so.

---

## 2. CLAIM LEDGER — every quantitative claim made, with its test

Format: `ID · claim · [status] · how it was measured`. **Attack the [ASSUMED] and [PARTIAL] rows.**

### Chunk 8 — audit of `code_rebuild_spine_v5.py`

| ID | claim | status | measurement |
|---|---|---|---|
| C1 | Input filename hardcoded to `espn_projections_2026_20260820.csv` while the pull now writes `..._YYYYMMDD_HHMM.csv` | **[CONFIRMED]** | read both files; pull script line 292 |
| C2 | `assert len(s)==pre` after a LEFT merge cannot fire on a broken join | **[MEASURED]** | constructed a trailing-whitespace key: matched **0 of 3** rows, assert **passed** |
| C3 | Cross-position `vbd` for K/D-ST: best D/ST would rank **34**, best K **39** on a naive sort | **[MEASURED]** | real projections, repl(K12)=144.00, repl(D/ST12)=95.88 vs skill vbd max +162.3 |
| C4 | The shipped board is unaffected — `board_v8_fixed.csv` holds **480 rows, 0 K, 0 D/ST** | **[MEASURED]** | direct read; `code_integrity.py` enforces "board no K/DST" |
| C5 | `isin` on the synthetic flag silently returns all-False if `espn_id` is object/str | **[MEASURED]** | dtype sweep: int64 OK, float64 OK, float+NaN OK, **str → 0 matched** |
| C6 | `s['captured_at']=e['captured_at']` is **NOT** a defect | **[KILLED]** | pandas aligns Series assignment on index label, not position. My own hypothesis, disproved |
| C7 | Doc 62 is correct: **zero** scripts write `board_v8_fixed.csv`; `code_build_board_v7.py` line 30 hardcoded to the **Aug-23** pull | **[CONFIRMED]** | 19 `.py` files staged and grepped, not sampled |
| C8 | `code_rebuild_spine_v5.py` **did not exist** in `Source\` — the spine artifact had no builder beside it | **[CONFIRMED]** | full directory listing. Now committed |
| C9 | `code_integrity.py` does **not** compare the spine's projections to the board's | **[MEASURED]** | it checks: board no null vbd, board no K/DST, unique+non-null `espn_id`. Nothing cross-checks projections |

### Market and projection measurements

| ID | claim | status | measurement |
|---|---|---|---|
| C10 | Projections did not move **at all** between the 08-20 and 08-23 pulls | **[MEASURED]** | 700/700 join on `espn_id`; `proj_2026` changed on **0** rows; `rank_std`/`rank_ppr` also 0 |
| C11 | ADP is what moves: `espn_adp` changed on **504 of 700**, max **36.21** picks, over 3 days | **[MEASURED]** | same join |
| C12 | ESPN drafters take RBs ~**10 picks later** than the Yahoo/Sleeper/RTSports field (median +10.0, mean +15.4); WR +6.8, QB +4.6, TE +1.9 | **[PARTIAL]** | n=151, K/DST excluded. **NAME JOIN, 88.5% match (262/296)** — §3 says a name join is a defect. Fine for comparison, must not feed the board |
| C13 | ESPN's API ADP carries real values to **169.17**; only **4** of 151 FP top-161 skill rows sit in the sentinel | **[MEASURED]** | **This RETRACTED my own earlier claim** that FantasyPros was needed as a deep-board fix. Matt's picks top out at eff ADP ~149 (pick 137); 152 → ~164; only 161 (~173) is censored, and that is the kicker |
| C14 | FantasyPros' ESPN column vs the API: **Spearman 0.9496**, Pearson 0.8029, top-100 median −5.5 | **[MEASURED]** | n=369. They agree on ORDER but are different UNITS — FP is a rank to 500, the API is an ADP |
| C15 | FantasyPros exports "3" and "4" are **byte-identical** (same sha256, 36,552 B) — the source picker does not affect the download | **[MEASURED]** | `cmp` + sha256 |
| C16 | The bare pull command produces a **2024** file whose `espn_adp` is the §1.1 contaminated field | **[MEASURED]** | `DEFAULT_SEASONS = [2022, 2023, 2024]` at line 23. Output: Barkley **3.36** (true preseason **17**), Kamara **8.28** (true ~50) — the exact doc-53 values |

### The Aug-28 pull and the FREEZE decision

| ID | claim | status | measurement |
|---|---|---|---|
| C17 | **FREEZE.** Board order is stable: **100 of 161** ranks identical, **150 of 161** within 2 slots, 4 moved >5, **zero dropouts** | **[MEASURED]** | boards rebuilt independently from each pull, QB12/RB30/WR30/TE12, VBD sort |
| C18 | Replacement levels unchanged: RB30 **−0.003**, WR30 **−0.007**, TE12 **−0.006**, QB12 −0.504 | **[MEASURED]** | §4.1 stands |
| C19 | ±2 window at Matt's picks: 8 → 5/5 · 17 → 5/5 · 32 → 5/5 · 41 → 4/5 · 56 → 4/5 · **65 → 3/5** · 80 → 4/5 · 89 → 5/5 | **[MEASURED]** | |
| C20 | The raw "482 of 593 rows changed" readout was **RETRACTED** | **[RETRACTED]** | median delta **−0.000**; 434 of 519 moved <0.5 pts; Josh Allen +0.024, Hurts +0.022 |
| C21 | ~~Sub-0.5 deltas are the `SCORING` patch~~ | **[FALSIFIED — doc 67 §1]** | `proj_2026` is ESPN's `appliedTotal`; `SCORING` only feeds the diagnostic. 525/525 exact. The deltas are real re-forecasts. **FREEZE survives on C17/C18** |
| C22 | Real mid-board movement: **Tank Dell −46.5 pts, board 134 → 192**; Watson −51.2; Sanders +50.8; Tracy −23.7; Najee Harris +26.3 | **[MEASURED, UNSOURCED]** | ESPN projection deltas only. **No news citation for any of them** |

### File-system findings

| ID | claim | status | measurement |
|---|---|---|---|
| C23 | A **fourth** script location exists: `G:\My Drive\_Fantasy\2026\Scripts` — directive v5.2 §9 says it does not | **[CONFIRMED]** | `device_list_dir`; injector + pull script present, hash-identical to the OneDrive copies |
| C24 | `G:\My Drive\Fantasy\Scripts` exists in Google Drive but is **not synced to a local path** | **[PARTIAL]** | Drive connector lists it with current files; `check_kit.py` reports the local path as absent; a folder-access request for it was refused by the platform |
| C25 | The two `ESPN_prerank_with_ids.csv` copies were byte-identical before the move | **[MEASURED]** | `cmp` clean, same sha256 |

---

## 3. ARTIFACT MANIFEST — what is on disk now, with hashes

**Canonical tree, set 2026-08-28:**

| path | file | bytes | sha256[:16] |
|---|---|---|---|
| `...\2026\Scripts\` | `Espn_pull_projections.py` | **14,992** | `16807f98494b4d5d` |
| | `espn_draft_injector_Gemini.py` | **4,660** | `26df3a398d48b651` |
| | `code_rebuild_spine_v5.py` | **8,079** | `917cdb488e960c4f` |
| | `check_kit.py` | 4,270 | (not self-pinned) |
| | `smoke_spine.py` | 3,457 | (not pinned) |
| `...\2026\Scripts\live_draft\` | `live_draft.py` | 15,391 | `752e2b4a8753a6c7` |
| | `code_live_engine.py` | 15,308 | `6246a1e81cbb57e2` |
| | `board_v8_fixed.csv` | 41,127 | `c65edcc41fff2507` |
| | `board_v7_kdst_separate.csv` | 3,143 | `1b2e61d507f4a648` |
| | `ESPN_prerank_with_ids.csv` | 33,216 | `899634df68e0e527` |

`...\2026\Source\` — documents, findings, data. **Nothing runs there.**
**Superseded, still on disk (8 files):** `Source\live_draft\` (5), `OneDrive\Fantasy\Scripts\` (3).
This bridge has **no delete capability**; Matt has the PowerShell commands.

---

## 4. CODE CHANGES — what was modified and whether it was EXECUTED

| file | change | executed? |
|---|---|---|
| `code_rebuild_spine_v5.py` | **P-D5** input pinned + refuses if a newer pull exists · **P-D2** `vbd` nulled for K/D-ST at source · **P-D3** `pd.to_numeric` coercion on the synthetic join · **P-D1** prints crosswalk match rate, warns <80% | **GATE ONLY (4/4 tests fire). The body past the gate has never been run — syntax check only** |
| `Espn_pull_projections.py` | `DEFAULT_SEASONS = [2026]`; new `confirm_seasons()` refusing completed seasons unless a human types `historical` or `--yes` is passed | **Guard tested 4/4 in isolation. The script itself was NOT re-run after patching** |
| `espn_draft_injector_Gemini.py` | `CSV_FILENAME` repointed from `Source\live_draft\` to `Scripts\live_draft\`; stale error text corrected | **NOT EXECUTED. Never run against ESPN's write API** |
| `check_kit.py` | rewritten for the canonical tree; straggler detection added; raw docstring (SyntaxWarning fixed); manifest re-pinned | **Ran clean on Matt's machine. Adversarial suite 5/5** |
| `smoke_spine.py` | new; runs the spine in a temp scratch dir, refuses if scratch resolves inside `Source\`, diffs against the shipped artifact | **NOT RUN — needs `code_universe.csv`, which is not in `Source\`** |

---

## 5. WHAT CHANGED IN THE PROJECT'S OWN RULES

1. **Doc 63 §2's test is superseded** by doc 64 §0. Counting changed rows is wrong once a scoring
   patch perturbs every row. The test is **board order**. Doc 63 has not been edited — see §6.1.
2. **Directive v5.2 §9 is wrong on two points:** `2026\Scripts\` exists (C23), and the canonical
   tree has moved there. §9's file map needs rewriting.
3. **Handover §3 is stale:** it says the injector reads the prerank "by bare relative filename."
   It uses **one absolute path**. That path was changed this session.
4. **Doc 61 corrected the handover's claim** that the board is clean "only because a runtime guard
   nulls vbd." It is clean by **separation** — 0 K/DST rows — which is stronger.
5. The Sept 5 news task was **deleted and recreated** (device-bound tasks cannot be edited).
   Fires 2026-09-05 09:00 ET and writes `claude/66_sep5_news_pass.md`.

---

## 6. WHERE I THINK THIS IS MOST LIKELY WRONG — ATTACK THESE FIRST

**6.1 Two docs now give different tests, and the wrong one is easier to find.**
Doc 63 §2 still says "0 rows changed → FREEZE." Doc 64 §0 replaces it. A Sept-5 session reading
63 first applies the superseded test and concludes doc 62 is live. **Doc 63 was not edited.**
*Falsify:* read doc 63 §2 cold and see which test you'd run.

**6.2 C21 is load-bearing and unmeasured.**
FREEZE rests on the sub-0.5-point deltas being the 2-pt-conversion scoring patch rather than a
genuine micro-reforecast. I did not test it. *Falsify:* re-parse the Aug-20 raw JSON
(`espn_raw_2026_20260820.json`, in `Source\`) with the patched `SCORING` map. If the deltas
reproduce, C21 holds. If they do not, FREEZE needs re-deriving. **This is the single highest-value
check you can run.**

**6.3 Matt hand-edited the pull script this morning; I may have overwritten that edit.**
He changed the year picker to run 2026. I patched from a copy staged **before** his edit and
committed over it. My patch supersedes his change functionally (`DEFAULT_SEASONS = [2026]`), but
**anything else he changed is gone.** *Falsify:* diff `Scripts\Espn_pull_projections.py` against
whatever produced `espn_projections_2026_20260828_0856.csv` and confirm nothing else was lost.

**6.4 The universe shrank and I explained it away.**
`proj_2026` non-null: Aug-20 **556** → Aug-28 **520**. The join was **593/700**, not 700/700.
I attributed this to `--sort draft` vs whatever produced Aug-20, and noted zero dropouts in the
top 161. **Not proven.** *Falsify:* re-pull with `--sort owned` and compare universes. If `draft`
truncates a region that matters, replacement levels are computed on a different pool.

**6.5 I recommended `--sort draft` from the script's help text, not from evidence.**
The help says `owned` is "recommended for closed seasons," so I inferred `draft` for an open one.
The Aug-20 file's sort mode is **unknown** — its row order matches neither ADP nor ownership.

**6.6 Three changed scripts have never been executed end to end.**
The injector (repointed path), the spine builder (body past the gate), and the patched pull script.
The injector matters most: Matt's weekend test is the first real run, and it now exercises a path
**I** changed. If that path string is wrong, it fails at run time.

**6.7 C12's 88.5% name join.**
34 of 296 unmatched. I asserted the misses are not concentrated in players who matter.
*Falsify:* list the 34 and check whether any sit in the 80–140 band.

**6.8 C22 is unsourced.**
Tank Dell −46.5 points and a 58-slot fall is the only movement inside the draftable range large
enough to change a pick, and it rests entirely on ESPN's projection delta. No citation.

**6.9 The `check_kit.py` manifest is now self-referentially fragile.**
It pins hashes for files I generated this session. If any of my patches is wrong, the checker
will happily certify the wrong file as correct. **A manifest verifies consistency, not correctness**
— the same error doc 61 §C1 already caught me making about provenance manifests.

---

## 7. THE PATH FORWARD, AS IT STANDS

| when | who | task |
|---|---|---|
| now | Matt | clear 8 stragglers; re-run `check_kit.py` |
| this weekend | Matt | `live_draft.py --replay 2025` · injector mock test (negative playerIds? replace or append?) · re-inject prerank |
| Sep 1–4 | — | buffer |
| **Sep 5, 9:00 ET** | **auto** | news + injury sweep, writes `claude/66_sep5_news_pass.md` |
| Sep 5 | Matt | re-pull `--seasons 2026 --sort draft`; run the **doc 64** test, not doc 63's; refresh FantasyPros half-PPR |
| Sep 7 7:00 PM | Matt | keeper lock, swap actual keepers, re-inject prerank |
| Sep 7 7:55 PM | Matt | `py live_draft.py`, confirm keeper-row count on first poll |

**Open and unowned:** doc 62's reconstruct path if FREEZE ever breaks · the 34 unmatched FP names ·
whether `Scripts\live_draft\` needs "Available offline" before draft night (untested judgment).

---

## 8. WHAT I WANT FROM YOU

1. Run **§6.2** — it is the one check that could overturn the live decision.
2. Adjudicate **§6.1** and **§6.3**; both are cheap and both can silently mislead a Sept-5 session.
3. Tell me which of §6.4–§6.9 you think is overstated. **I would rather be told a defect is
   smaller than I claimed than have it confirmed politely** — this project has twice measured an
   "obvious" severity at 1/100th of the asserted value.
4. Name anything in §7 that should not be on the list, or is missing from it.

**Do not re-derive docs 53–60.** Do not rebuild the board. If you disagree with FREEZE, say so with
a measurement.
