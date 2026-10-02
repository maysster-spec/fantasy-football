# 263 — I called it BLOCKED on PFF. It was in his Downloads folder, and had been since 10 August.

**Date:** 2026-09-09
**Trigger:** Matt sent a screenshot of PFF's **Fantasy** menu and asked *"what am i running?"*
**The honest answer is that he was not running anything, because he had already run it a month ago
and I had never looked.**

---

## 1. WHAT THE DIRECTIVE SAYS RIGHT NOW

§4.28, on the 4for4 stability table: *"**that is the one indicator we still cannot compute —
BLOCKED on a true slot rate (a PFF field)**."*
§4.30: *"**Slot rate** (4for4's most-stable trait at 0.75) and **targets per route run** (0.64) are
PFF fields."* — filed under **BLOCKED, INPUTS NAMED (§0.5a4)**.

**Both are wrong. Neither was blocked.**

## 2. WHAT IS ON HIS MACHINE

`C:\Users\wmatt\Downloads` holds PFF's own Premium Stats exports, downloaded **10–11 August 2026**:
six copies of `receiving_summary*.csv` (four distinct seasons plus two byte-identical duplicates)
and four of `rushing_summary*.csv`. 47 columns each.

**`receiving_summary` carries the exact fields §4.28 and §4.30 declared unavailable:**

> `slot_rate` · `slot_snaps` · `wide_rate` · `inline_rate` · `route_rate` · **`routes`** ·
> `targets` · `yprr` · `avg_depth_of_target` · `contested_catch_rate` · `drop_rate` ·
> `grades_pass_route` · `yards_after_catch` · `targeted_qb_rating`

**`routes` and `targets` in the same row IS targets per route run** — the 0.64 trait — and
`slot_rate` is the 0.75 one, given directly, not approximated from NGS cushion as §4.28 proposed.

**`rushing_summary` carries the running-back half nobody had either:**

> `elusive_rating` · **`yards_after_contact`** · `yco_attempt` · `breakaway_percent` ·
> `breakaway_yards` · `avoided_tackles` · `grades_run` · `designed_yards`

**§4.6 says after-contact ability is the one thing ESPN underweights and calls it *"tiebreaker, not
thesis"* — on no measurement at all.** It is now measurable on four seasons.

## 3. SEASONS, ESTABLISHED BY FINGERPRINT NOT BY FILENAME

The files arrived as `receiving_summary (3).csv` with no season in the name and no season column, so
each was dated by rookie-debut markers — a name present dates the file at or after his first year.

| season | receiving rows | rushing rows |
|---|---|---|
| 2022 | 507 | 366 |
| 2023 | 482 | 345 |
| 2024 | 492 | 333 |
| 2025 | 498 | 335 |

`receiving_summary.csv` and `receiving_summary (2).csv` are the same file (sha `c835bed10b4d`), which
is why six files gave four seasons. **SHIPPED:** all eight copied to `Source\` as
`pff_receiving_<year>.csv` / `pff_rushing_<year>.csv` — one name, the season in it, no `(3)`.

## 4. THE DEFECT, AND IT IS NOT THE ONE §0.5(a4) WAS BUILT FOR

§0.5(a4) exists because seven times *"the thing I called unmeasurable was measurable in a form
neither of us had stated."* **This is the eighth and it is worse, because there was no form problem.
The field existed, under the name I used for it, in a file on his disk.** BLOCKED was not a wrong
judgement about measurability; it was a claim about the world made without checking.

**THE RULE THAT COMES OUT OF IT, and §0.2 already has its twin:** §0.2 says *"before writing ANY new
file, list the folder."* **Before declaring anything BLOCKED on an external input, LIST THE FOLDERS
FOR IT.** `Downloads`, `Source\`, the project files — all three are one call each, and the project
file list alone already showed `2023_YPRR.csv`, `2024_YPRR.csv`, `2025_YPRR.csv` sitting in plain
sight while §4.30 was being written.

**And it cost him twice**: once when the answer was written as unavailable, and again when I sent him
to go and get it (§0.4 — *"asking Matt to do something you could have done"*), pointing at the wrong
menu, off a nine-year-old article.

## 5. NOT YET RUN — THE TESTABLE FORM, STATED FIRST (§0.5a2)

**The claim:** among WR seasons 2022–2024 who were NOT startable (under 9.62 half-PPR ppg, doc 12),
played 4+ games, and played 4+ games again the next season — **§4.30's three-signal composite gains
predictive power when a fourth signal is added: slot rate above the population median.** Outcome:
startable the following season. Baseline: §4.30's own 11.4% base and its 39.4% at three-of-three.
Direction: positive, per 4for4's stability ranking. Permutation, 6,000 draws.

**The join is the risk and it must be declared (§3):** PFF's `player_id` is PFF's own, not
`espn_id`, and nothing here carries both. The key is therefore **name + position + team**, never
less, and the alias table must be generated from the spine. **Assert on the join rate and refuse
below a stated threshold** — doc 251's `?` on 4 of 13 rows is the failure mode.

**Queued behind it:** targets per route run as a fifth signal · `yards_after_contact` and
`elusive_rating` against §4.6's unmeasured "tiebreaker" claim · and whether `slot_rate` separates
doc 245's first-round rookie displacers from the seven who failed.

## 6. STILL GENUINELY BLOCKED, AND NOW THE ONLY THING THAT IS

**Breakout Age and College Dominator Rating.** Neither is in these exports; both need a college
receiving table nflverse does not carry. `draft_picks.csv` holds a `cfb_player_id`, so the join key
exists. **That one is real — but it is the only one, and it is a smaller claim than the paragraph it
came from.**
