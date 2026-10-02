# 42 — INJURY AND AVAILABILITY: IS THERE A PER-POSITION NUMBER, AND DOES THE PROJECTION ALREADY HAVE IT?
**Aug 25, 2026.** Matt asked how the model handles players like Jonathon Brooks, who was drafted at
pick 88 in 2024 with a projection of 128.1 and returned 6.0 points, and whether a probability could
be computed that applies per position. **Both halves are answerable. The first is yes; the second is
mostly no, and the reason matters.**

## 1. YES, AVAILABILITY IS DIRECTLY MEASURABLE — WE ALREADY HAVE THE DATA

ESPN stat id **210 is games played**, and it is present in both the projection row and the actual
row of every pull. No new data was needed.

**[TESTED] Games played, drafted-range players only (ESPN ADP < 169), 2021 + 2022 + 2024.**
**POPULATION:** players with a real projection and a measured games-played value. **SAMPLE:** n=670.

| pos | n | mean GP | median | P(GP ≤ 13) | P(GP ≤ 8) |
|---|---|---|---|---|---|
| QB | 86 | 14.0 | 15.5 | 33% | 10% |
| RB | 180 | 13.9 | 15.0 | **35%** | 10% |
| WR | 224 | 14.0 | 15.0 | 32% | 9% |
| TE | 78 | 14.8 | 16.0 | **22%** | 5% |
| K | 46 | 15.4 | 17.0 | 20% | 7% |
| D/ST | 56 | 17.0 | 17.0 | 0% | 0% |

Two things worth noting. **The RB-vs-WR gap is far smaller than folklore says** — 35% vs 32% for
losing a month or more, and 10% vs 9% for losing half a season. Running backs are not dramatically
more fragile than receivers in this sample. **Tight ends are the genuinely safer position** (22%),
and defenses never miss a game, which is worth remembering when comparing their projections to a
skill player's.

## 2. BUT ESPN ALREADY PRICES MOST OF IT — DO NOT APPLY A HAIRCUT ON TOP

This is the part that changes the answer. **[TESTED]**

- **ESPN projects 15.32 games on average, not 17.** Its projections are already expected-value
  numbers that discount for injury risk. Actual average is **14.46**.
- Players who went on to play **all 17 games beat their projection by 20.5%** (actual/proj = 1.205,
  median 1.154, n=182).
- Players who played **≤13 games came in at 71.8%** of it (median 0.615, n=176).
- Correlation between games played and the actual/projection ratio: **r = +0.345**.

Those numbers are exactly what you would see if the projection embeds an availability discount:
the healthy overshoot it, the hurt undershoot it, and the average lands near the middle.

**Therefore: applying a position-level availability multiplier would double-count.** The residual
bias is only **15.32 − 14.46 = 0.86 games, about 5.6%**, and it is close to uniform across QB, RB
and WR (33/35/32% month-plus-miss rates). **A correction that is both small and roughly equal
across the positions you are choosing between does not change a single pick.** This is directive
4.6's rule — TD regression and rushing efficiency are already priced, and so is this.

`[TESTED — and it kills the hypothesis]` A per-position injury haircut is measurable, real, and
**not actionable**, because the projection already contains it.

## 3. WHERE THE REAL GAP IS — THE FLAG, NOT THE POSITION

The Jonathon Brooks case is not a position-rate problem. It is a **known-injury-at-draft-time**
problem, and the board has never surfaced it.

Audit 19 found **32 players carrying an ESPN injury flag inside ADP 170 appearing on zero shipped
artifacts** — the HTML board contained the string "injury" zero times. Ten sat inside ADP 50. Audit
19 also established that **none of the 32 had their projection zeroed**, so ESPN's projection does
not price its own flag — this is genuinely unpriced information, unlike the position rate above.

**Fixed in `board_v7`:** `injury_status` is now a column, and 36 flagged players inside the top 150
are marked. Including, right now, **Christian McCaffrey (QUESTIONABLE) at board rank 3 and Puka
Nacua (QUESTIONABLE) at rank 4 — both live candidates at pick 8.**

**Surfaced, deliberately not scored.** An August "QUESTIONABLE" is a low bar with untested
predictive value in this project, and turning it into a VBD haircut would be inventing a
coefficient. It is a red dot on the board for Matt to price, not a number the model applies.

**What would make it scoreable, and why it cannot be done yet:** the historical pulls carry
`injuryStatus` **as of the 2026 capture date, not as of each season's preseason** — a player who
retired shows his current state, not his 2021 status. So "do August flags predict underperformance"
**cannot be tested on this data at all.** It would need preseason-dated injury snapshots, which
nothing in the project has. Labelled `[HYPOTHESIS]`, not finding.

## 4. WHAT THE MODEL DOES WITH THESE PLAYERS TODAY, PLAINLY

1. The projection already assumes ~15.3 of 17 games, so ordinary injury risk **is** in the number.
2. No extra position-level penalty is applied, and none should be — it would double-count.
3. A current injury flag is shown on the board and is **not** in the number. That one is yours to
   judge.
4. Nothing in the model can currently distinguish "questionable, will play week 1" from "torn ACL
   in July." That distinction is worth more than everything else on this page and it needs the news
   check already scheduled for Sept 5 (T-48h).

## LIMITS

1. n=670 across three seasons in one league's drafted range. 2023 is absent (no usable projections).
2. Games played is a proxy for availability, not for effectiveness — a player who plays hurt at 60%
   counts as available here.
3. The healthy-player overshoot (1.205) partly reflects survivorship: staying healthy correlates
   with the same things that produce good seasons. It is not purely an availability effect, and no
   attempt was made here to separate the two.
4. `actual/proj` ratios are unstable for low projections; the population is restricted to ADP < 169
   and a positive projection, but no further trimming was applied.
