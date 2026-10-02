# 24 — ANALYST ACCURACY, THE POWERED TEST
**Aug 23, 2026.** Run on the five full FantasyPros tables you loaded into the project
(2022 n=247, 2023 n=236, 2024 n=225, 2025 n=212, multi-year n=157).
**This supersedes `claude/22` and retracts its headline.**

---

## RETRACTION FIRST

`claude/22` concluded: *"accuracy persists weakly and it stopped working last year"* — because
the 2024→2025 top-30 overlap test returned 3 repeaters against 3.8 expected, p=0.78.

**Wrong. That test was underpowered.** On the full table, matched expert to expert:

| pair | matched n | Spearman | p |
|---|---|---|---|
| 2022 → 2023 | 205 | **+0.496** | <0.0001 |
| 2023 → 2024 | 193 | **+0.378** | <0.0001 |
| 2024 → 2025 | 173 | **+0.268** | **0.0004** |

2024→2025 is not nothing. It is a real, significant relationship that a 30-name cutoff could
not see. Two-year gaps behave as decaying skill should: 2022→2024 +0.410, 2023→2025 +0.276,
2022→2025 +0.325 — all weaker than the adjacent pair in the same era, none at zero.

**Accuracy persists. My proxy was the problem, not the contest.** This is the second time in
two days a top-N overlap shortcut produced a false null (`ERROR_PATTERNS` A1).

---

## THE FINDING THAT MATTERS: ACCURACY IS NOT ONE SKILL

Per-position Spearman, same matched-expert method:

| position | 2022→23 | 2023→24 | 2024→25 | verdict |
|---|---|---|---|---|
| **RB** | **+0.480** | **+0.364** | **+0.270** | **persists, every year, all p<0.05** |
| **WR** | +0.330 | +0.235 | +0.144 | persists, decaying, last year not significant |
| **QB** | −0.089 | −0.097 | −0.126 | **negative all three years** |
| **TE** | +0.033 | +0.061 | +0.081 | zero |

Bonferroni threshold across these 12 tests is p<0.0042. RB clears it in 2022→23 and 2023→24.

**Being accurate at quarterback one year predicts being slightly *worse* the next, three years
running.** QB ranking is noise plus luck. Same for TE.

### And "the most accurate analyst" is not a real category

Within the multi-year table (n=157), how an expert's positional accuracies relate to each other:

| | QB | RB | WR | TE |
|---|---|---|---|---|
| **QB** | — | **+0.01** | +0.01 | +0.07 |
| **RB** | | — | **+0.63** | +0.30 |
| **WR** | | | — | +0.32 |

**RB skill and QB skill are completely unrelated (rho +0.008, p=0.92).** RB and WR travel
together (+0.63) — same underlying ability. TE is loosely attached. QB is its own island.

And the overall leaderboard is mostly one thing:

`RB explains 76% of overall rank (rho +0.874) · WR 66% · TE 23% · QB 7%`

**The FantasyPros overall draft-accuracy leaderboard is, to three-quarters, an RB leaderboard.**
Nobody appears in both the RB top five and the WR top five.

| position | who is actually persistent |
|---|---|
| **RB** | Jody Smith (Draft Sharks) · Ryan Weisse (Club Fantasy FFL) · Chris Raybon (Action Network) · Kev Wheeler (Wheel Route FF) · Nick Zylak (Fantasy Football Advice) |
| **WR** | Jeff Bell (Footballguys) · Donald Gibson (FantasyPros) · Tal Malachovsky (The Fantasy Scout) |
| **QB** | nobody — the skill does not repeat |
| **TE** | nobody — the skill does not repeat |

---

## YOUR ANALYSTS, AND WHY THIS SUPPORTS YOU RATHER THAN CONTRADICTS YOU

**Matt Harmon — Yahoo:** 2022 **#99/247** · 2023 **#195/236** · 2024 **#49/225** ·
2025 **#176/212** · multi-year **#90/157**. Mediocre and violently unstable.

**Justin Boone — Yahoo:** 2025 **#114/212** on draft accuracy. The board's old organising
principle was one analyst's deviation from ADP, and that analyst ranks in the bottom half of
preseason accuracy. A second, independent reason the Boone spine had to go.

**Scott Pianowski — Yahoo:** #27, #25, #63, #108; multi-year #42/157. The best of the three,
and fading.

**Absent from every draft-accuracy table, every year:** Zachariason, Siegele, McFarland, Silva,
Gretch, Hartitz, Thorman, Smyth, Winks, Norris.

**Read this the right way.** Doc 23 established that being 10% tidier on ordinary players is
worth **2.80×** as much accuracy score as perfect foresight on every breakout. Harmon being
#176 in 2025 is therefore *not evidence he is bad at finding breakouts* — the metric cannot
see that skill in either direction. What it does mean: **you cannot use the accuracy contest
to justify following him, and you cannot use it to dismiss him either.** Your judgment is the
only instrument in the room pointed at that question.

---

## WHAT THIS CHANGES ON THE BOARD

The six rankers currently powering the EDGE column — Boone, Smyth, Harmon, Pianowski, Winks,
Norris — include **nobody** from the persistent-RB or persistent-WR lists. They are the panel
we happen to have, not the panel the evidence endorses.

That is fixable in one page and it is the single highest-value thing left before the draft.
See the instruction at the end.

---

## NAME COLLISION, OCCURRENCE 10

`Harmon` matched **two** experts: **Matt Harmon (Yahoo)** and **Mike Harmon (Swollen Dome)**,
present in all four years. My first pass reported eight Harmon results per name lookup and
would have averaged two different people into one record.

Caught by printing the matched rows instead of the count. `ERROR_PATTERNS` C1 again — the
tenth occurrence, and the second in two days. **Substring matching on a surname is not a join.**

---

## LIMITS

- Four seasons, three adjacent pairs. The per-position table is 12 tests; only RB's first two
  pairs clear Bonferroni.
- Matched on the displayed `Name - Site` string, so an analyst who changed employer reads as
  two people. Every persistence figure above is a **lower bound**.
- The multi-year table verifiably covers **2023–2025** — all 157 of its experts appear in each
  of those years and none appears only in 2022. Any comparison between it and 2025 is partly
  circular; it bounds a result, it never proves one.
