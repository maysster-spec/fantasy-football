# 396. Rank the contested man first. Each banked win roughly halves the next one.

> **CORRECTED IN PLACE BY DOC 401, 23 Sept 2026 (directive v9.24). THE GRADIENT IN THIS DOC IS RETRACTED.**
> **61.1% / 29.1% / 11.2% is arithmetic, not a mechanic.** The bucket is *other wins by that team in that run*,
> which equals the team's total wins minus this claim's own result, so **a winner sits one bucket below a loser
> from the same team-run by construction**. Permuting which contested claims won, holding each team-run's win
> count fixed, over 3,000 draws, **reproduces all three cells exactly with ZERO variance** — the real data cannot
> be told apart from reshuffled data. The cells also shipped with no sample sizes (§3): n = 211 / 223 / 152.
> **The mechanic cannot be measured from this source at all**: every claim in a run carries one identical
> timestamp, so within-run order is unobservable and *"prior wins that run"* was never a quantity this data could
> express. **BLOCKED**, missing input: his own claim ordering recorded at placement, forward-going.
> **WHAT SURVIVES: the 28.6% contested rate, the ~3-in-4 uncontested win rate, and ESPN's sourced text.**
> **"Rank the contested man first" STILL STANDS — as a DOMINANCE argument with no effect size**, the same footing
> as the Sunday-night rule. Do not quote a number with it.
> **Also: this doc's population was rebuilt with `(-?\d+)`. A `(\d+)` regex drops every D/ST, 27% of waiver rows.**


**23 Sept 2026. Closes the open item doc 395 left at the top: ESPN's claim-ordering mechanic, and
whether winning claim 1 drops priority before claim 2 is evaluated.** Matt: *"if there is an open
item then run it down."* Two channels, the vendor's pages and his own five seasons, and they agree.

---

## 1. ESPN, VERBATIM, FOOTBALL PAGES, READ AS PAGE TEXT

***Waivers Overview*** (ESPN Fan Support > Fantasy Football > Trades and Waivers):
> "When the waiver period expires, the player will be awarded to the team with the highest waiver
> priority that made a claim, and **that team will move to the end of the waiver order. This process
> continues until all waiver claims are processed**, after which all players not added via waivers
> become free agents"

***Claim a Player Off Waivers***, same section:
> **"Managing Pending Claims** ... Inside Pending Moves, you can: **Reorder claims by dragging them
> into your preferred priority.**"
> "Waivers are typically processed **daily around 3:00 AM ET**."
> "Free Agents can be added immediately on a first-come, first-served basis, and **adding them does
> not affect your waiver position**."

**So: the drop to the bottom happens MID-RUN, and he controls the order of his own claims.** That
makes the ordering a real decision rather than a detail.

---

## 2. AND IT IS NOT THE SIMPLE STORY. MEASURED ON HIS OWN LEAGUE

**Population: every WAIVER-type event in `waiver_report_2022..2026.csv` that reached a decision,
this league, grouped into player-runs (one man, one processing batch) and team-runs (one team, one
batch). 745 player-runs, 543 team-runs, five seasons.**

**First, the naive reading of the rule is WRONG.** If a win simply ended your run, nobody would ever
win twice. Among the 275 team-runs entering two or more claims, **49.1% won two or more.** So a win
does not cap you.

**It does not cap you because most claims are uncontested.**

```
how many teams claimed the same man in the same run
  1 team   532   71.4%      <- uncontested
  2 teams  125
  3 teams   56
  4+        32              <- contested, 213 of 745 = 28.6%

win rate, uncontested                      415/532 = 78.0%
win rate per claim, contested              211/575 = 36.7%
```

**THE MECHANIC SHOWS UP EXACTLY WHERE THE RULE SAYS IT SHOULD: on contested men only.**
Contested claims, n=586, split by whether that team had already won something else in the same run:

```
  no other win that run     n=211    won this contested man   61.1%
  one other win             n=223                             29.1%
  two or more other wins    n=152                             11.2%
```

**Each win banked in a run roughly halves the odds on the next contested man.**

**THE CONFOUND RUNS THE RIGHT WAY, so the effect is conservative.** Priority resets weekly to
inverse standings, and the first contested man in a run goes to the highest-priority claimant. So
the teams sitting in the "already won" rows are **disproportionately the high-priority teams**, who
should win more. They win far less. The drop to the bottom is overwhelming their starting advantage.

---

## 3. THE RULE

**RANK THE CONTESTED MAN FIRST.** Uncontested claims come in at 78% whether or not you have already
won something, so they cost nothing by going second. A contested man is a 61% shot if he is your
first win of the run and a 29% shot if he is your second. **Spend the top of your order on the man
other people want, and let the quiet one ride behind him.**

**Two corollaries that fall straight out:**
- **A free agent is not a claim at all.** ESPN: adding one "does not affect your waiver position",
  and `wire.py` already writes ESPN's own token in the `avail` column. **Check that column before
  ordering anything: a green-button man needs no claim and no priority, and the ordering question
  disappears for him.**
- **`own_chg` is how you tell which is which before the run** (doc 395). It is a format-wide demand
  signal, not a measurement of this league, but a man at +22 is being taken everywhere and a
  defence at +3 is not.

---

## 4. WHAT IS STILL NOT ESTABLISHED, AND I AM NOT GUESSING IT

- **That `own_chg` predicts contention IN THIS LEAGUE.** Section 2's 28.6% is measured; that a high
  format-wide +/- maps onto those 12 managers is not. `own_chg` only starts being recorded on the
  next run, so this is answerable in a few weeks and not today. **Do not quote it as a rule.**
- **The exact processing algorithm.** ESPN says the winner moves to the end and the process
  continues; it does not publish whether it sweeps player-by-player or team-by-team. **The
  measurement in section 2 does not depend on knowing, which is why the rule above is safe.**
- **His own waiver position is not a thing to quote from memory.** `wire.py` already reads
  `waiverRank` off `mTeam` and computes both his rank and who sits ahead of him, and it refuses to
  guess when ESPN does not serve it. Read it off the run.
