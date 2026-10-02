# 78 — RED-TEAM CATALOG, AND PASS 1 FINDINGS

**Aug 30, 2026. Draft in 8 days.** Doc 48's protocol: slice by failure MECHANISM, not by file.
Pass 1 (mechanical checks) is executed below. Passes 2-5 are catalogued but not yet run.

**Why now:** `live_draft.py` was rewritten six times today and `check_kit.py` four. Three new
scripts and two scheduled tasks were added. Every change was inspected but almost none was
adversarially attacked. That is exactly the state this project has repeatedly found defects in.

---

## THE CATALOG

| # | mechanism | what would fail | status |
|---|---|---|---|
| **1** | **Dangling references** — a script, batch file or doc naming something that moved | draft_night.bat calls a script that isn't there; a doc sends a session to a dead path | **DONE — §1** |
| **2** | **Duplicate files** — the same name holding different bytes in two places | the wrong copy runs; the thing this project has been bitten by more than any other | **DONE — §2** |
| 3 | **Render paths never exercised** — the board has 4 output states (clock / waiting / streamer / done) and only 2 get looked at | a blank or broken page at pick 152, 161, or after the last pick | catalogued |
| 4 | **The checker checking itself** — check_kit's manifest is self-referential and it does not watch its own file | a stale checker certifies a stale tree | **PARTIAL — §3** |
| 5 | **Automation chain end-to-end** — task → .bat → .py → output, never run as a whole | a step fails silently at 6:55 PM and the next step runs anyway | catalogued |
| 6 | **Never-executed code** — fetch_keepers.py, keeper_swap.py --write, draft_night.bat | first execution is on draft night | catalogued (2 are Matt-only) |
| 7 | **Doc-vs-code drift** — the guide asserts behaviour nobody re-verified after today's rewrites | Matt follows an instruction that is no longer true | catalogued |
| 8 | **Numbers that moved** — replacement levels, board order, the manifest hashes | a stale number in a doc drives a live decision | partly covered by sept5_check.py |

---

## §1 — DANGLING REFERENCES: CLEAN

Every script referenced by `draft_night.bat`, `refresh_pull.bat`, `sync_desk_copies.bat` and
`setup_tasks.ps1` resolves to a real file. Both PDFs `sync_desk_copies.bat` copies exist
(`DRAFT_CARD.pdf` 3,423B and `DRAFT_DAY_GUIDE.pdf` 98,611B, both in `Source\`). No dead paths.

## §2 — DUPLICATE FILES: SIX FOUND, ONE OF THEM IS THE CHECKER ITSELF

`Source\` is documented as "documents, findings, data. **Nothing runs here.**" It currently holds
runnable duplicates:

| file | Source\ | Scripts\ | verdict |
|---|---|---|---|
| **`check_kit.py`** | **3,324 B** | **6,739 B** | **the stale-copy detector has a stale copy of itself.** Run the wrong one and it certifies a tree it does not understand |
| `smoke_spine.py` | 3,409 B | 3,457 B | different bytes, same name |
| `code_rebuild_spine_v5.py` | 8,079 B | 8,079 B | same size; still a second copy in a "nothing runs here" folder |
| `board_v8_fixed.csv` | 41,127 B | (kit) 41,127 B | same; but this is THE board, and two copies is how the wrong one gets loaded |
| `board_v7_kdst_separate.csv` | 3,143 B | (kit) 3,143 B | same |
| `ESPN_prerank_with_ids.csv` | 33,216 B | (kit) 33,216 B | same. The injector reads the kit copy by ABSOLUTE path, so this one is inert — but it is the exact shape of the Aug-28 defect |

**check_kit does not watch itself, and does not watch `Source\` at all.** Both are gaps in the
detector, not in the tree.

**Naming-rule violations found in the same sweep:** `FABLE_TASKING_PROMPT.txt` *and*
`FABLE_TASKING_PROMPT_v3.txt`; `ERROR_PATTERNS_1.md`; `test_check_kit.py` (a test file living
beside canonical documents).

## §3 — WHAT PASS 1 DID NOT COVER

Chunks 3, 5, 6 and 7 are the ones that bite on draft night, and none has been run:

- **The streamer render (picks 152 and 161) has never been looked at.** It uses `.wrap`, the class
  I deleted and restored today. If it is broken, it breaks at pick 152 with no warning.
- **`draft_night.bat` has never been executed end to end.** Its first real run is at 6:55 PM on
  Sept 7, gating five steps.
- **`fetch_keepers.py` has never run at all.**
- **The guide asserts things about a `live_draft.py` that has since been rewritten six times.**

---

## RECOMMENDED ORDER, AND WHY

1. **Fix §2's duplicates first** — cheap, and it is the failure mode with the worst track record here.
2. **Then chunk 3 (render paths)** — I can force every state offline in minutes; no ESPN needed.
3. **Then chunk 7 (doc-vs-code)** — re-read the guide against the current code, line by line.
4. **Chunk 5 and 6 need Matt** — the weekend test kit already covers most of it.
5. **Smoke test last:** run `check_kit.py`, `--replay 2025`, and `fetch_keepers.py --dry` in one
   sitting and confirm the catalog above is closed.
