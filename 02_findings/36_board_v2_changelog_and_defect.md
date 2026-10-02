# 36 — BOARD v2: DEFECT FOUND, AND WHAT CHANGED
**Aug 23, 2026.** `prerank_board_full_v2.csv` supersedes v1 (built earlier today).

---

## DEFECT: a predicted keeper was sitting on the draftable board

**`Travis Etienne Jr.` was ranked 24th overall on v1. He is Snyder's predicted keeper.**
He will never be available at any pick, and a top-25 slot on the board was reserving a
decision for a player who cannot be drafted.

**Root cause — name-join collision, the class of error `ERROR_PATTERNS.md` already tracks.**
`predicted_keepers_v5.csv` stores him as `Travis Etienne`; `code_universe_v5.csv` and
`board_edges_v6.csv` store him as `Travis Etienne Jr.`. The keeper-removal step matched on
exact string, so the suffix defeated it. The other eleven keepers matched and were correctly
removed, which is why the failure was invisible — the board *looked* keeper-depleted.

**Fix.** v2 matches on a normalized key (case, punctuation and Jr/Sr/II/III/IV suffixes
stripped) and re-verifies that **zero** predicted keepers remain on the board. v2 is 316 rows,
v1 was 317.

**Enumerating downstream uses, per Section 3.** Any artifact built from `board_edges_v6.csv`
without normalized keeper matching carries the same error: `prerank_board_full_v1.csv`
(superseded), `prerank_names_only_v1.txt` (superseded), and any survival or simulation output
that took its pool from that file — Etienne would have been modeled as an available body,
slightly deflating everyone else's survival odds around picks 41–56. Magnitude is small (one
player of 316) but the direction is known, and the effective-ADP table in Section 2.1c is
unaffected because it counts keepers, not names.

**Confirmed correct, for the avoidance of doubt:** the other eleven predicted keepers —
Rashee Rice, George Pickens (Matt's own), Chris Olave, Javonte Williams, Zay Flowers,
Tetairoa McMillan, Cam Skattebo, Colston Loveland, Drake Maye, Rhamondre Stevenson,
Stefon Diggs — are all correctly absent from the board. **Drake Maye in particular is not a
data gap**: projected 373.1 league points and VBD +31.5, which would place him around board
rank 34, but he is allen's keeper and unavailable. He was checked because his absence looked
like a defect; it is not.

**Live risk to carry to Sept 7.** These are *predicted* keepers. If any prediction misses, that
player is missing from the board entirely and will not surface during the draft. Keeper lock is
7:00 PM Sept 7 and the rebuild at that point is mandatory, not optional. Until then the twelve
names above are the hold-out list — if one of them is announced as *not* kept, they slot back
in at the VBD rank their row implies.

---

## WHAT ELSE CHANGED IN v2

**New column `analyst_2026_UNSCORED`** — from the expanded 180-call corpus, counted by distinct
analyst rather than distinct show. Values: `TARGET n` (3+ analysts, no dissent) · `target n`
(1–2) · `CONTESTED nT/nD` · `DOWNGRADE n` (2+ downgrades, no defenders) · `downgrade 1`.

**New column `ranker_vs_espnADP`** — `n/6` rankers ahead of ESPN's ADP; `AHEAD adj+N` when all
six agree *and* the player beats his own position's median gap; `BEHIND` when none do. Blank
where ADP is censored, because the comparison is meaningless there. Full method and the test
of whether this signal means anything: `35_consensus_signal_test.md`.

**Sort logic is unchanged from v1 and both new columns are annotation only.** Neither drives
rank. Blending an untested signal into the ordering would violate Section 0, and the test in
`35` deliberately stops short of claiming these predict outcomes.

**One hand-moved player, unchanged:** Josh Allen at rank 9 per TESTED 4.2.

---

## ALSO SHIPPED

- **`prerank_top120_v2.txt`** — the first 120 names only. Entering all 316 into ESPN's
  drag-and-drop tool is not worth an evening: past roughly pick 140 the board is ordered by
  projection because ADP is censored, and Matt's last flexible pick is 137 (effective ~149).
  120 covers every pick that is actually a decision.
- **`espn_pull_draft_history.py`** — sanitized replacement for
  `Espn_league_scoredraft_2021_2024.py`. Credentials moved to environment variables, and the
  `SEASONS = [2022]` / `historical_draft_results_2021.csv` filename mismatch fixed so an export
  can no longer mislabel itself. **The uploaded 2021 file is a duplicate of 2022 — 2021 was
  never pulled.** Re-run with `SEASONS = [2021]` if that season is wanted.

## VERIFIED, NOT CHANGED

`historical_draft_results_2022_2025.csv` (720 picks, ESPN API, `Keeper Status` boolean)
independently confirms Section 4.7's keeper-round structure from an authoritative source:
keepers occupy **round 1 in 2022 and 2023, round 15 in 2024 and 2025**, twelve every year.
This is the accounting Section 2.1b depends on and it is now sourced from the API rather than
inferred from draft recaps. No finding changes; a load-bearing one gets firmer.
