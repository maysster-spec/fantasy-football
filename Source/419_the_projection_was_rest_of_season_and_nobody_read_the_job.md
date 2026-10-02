# 419 — the projection was rest-of-season, and nobody read the job that pulls it

**24 Sept 2026.** Matt, while I was fixing the box that describes the numbers:

> *"yes, keep in mind projections were built for pre FF draft. Probably other numbers to check as
> well. **You need to know what the job actually runs before you assume you can use it.**"*

He was right, it had not been done, and the thing it would have caught had been wrong since week 1.

---

## THE FINDING

**`proj_2026` is a REST-OF-SEASON total. The page divided it by 17 every week of the season.**

Measured on the two pulls on the drive, 7 September and 24 September, 208 backs and receivers
projected over 40 preseason:

| | median |
|---|---|
| 24 Sept projection ÷ 7 Sept projection | 0.891 |
| **(24 Sept projection + points already scored) ÷ 7 Sept projection** | **0.997** |

**It reconstructs the preseason number almost exactly**, which is only true if what is left is what
is left. 99.1% of those men moved between the two pulls, by a median of −6.7 points, and **the move
does not track what they have done**: r = 0.031 against points scored so far. ESPN is burning off
elapsed games, not re-rating players.

**THE DIVISOR AGREES.** The ratio that makes the 24 Sept per-game rate match the 7 Sept one is
**15.15 games**. Two weeks are gone. 17 − 2 = **15**.

`PROJ_GAMES = 17.0` therefore understated **every projected rate on the page by about 11%**, and it
compounds: by week 12 it would be spreading a five-game remainder over seventeen. `proj_games(week)`
returns `17 − elapsed` now, and `rates()` says out loud which divisor it used.

Games, never weeks — a man plays 17 in an 18-week season. And elapsed weeks LEAGUE-WIDE, not the
man's own games played: a man who missed week 1 has the same schedule ahead of him as everyone else.

**What it moves, at week 3:** Adams 10.85 → 12.29 a week, Schultz 6.38 → 7.23, Waller 4.00 → 4.54.
Through the blend, Adams' printed rate goes 14.07 → 15.00. **The drop costs rise with them**, so the
nets on THE CALL fall: Malik Washington was +6.0 over dropping Dobbins and is +2.3. That is the
honest direction. Pickups were being priced against bench men the page undervalued.

## THE REASON IT SURVIVED THREE WEEKS, WHICH IS THE PART WORTH KEEPING

Doc 409 killed a `(proj − actual) / weeks remaining` rate because it measured anti-correlated, and it
recorded WHY: *"ESPN's proj_2026 barely moves, so the subtraction is just mean reversion wearing a
forecast's clothes."*

**The conclusion was right and the reason was wrong.** `proj − actual` was **double-subtracting**:
ESPN had already removed the elapsed games, and taking the man's banked points out again is exactly
why it punished whoever had produced. Same for the comment two lines above the divisor, which called
`pr` *"ESPN's FULL-SEASON forecast"* — **that is the sentence `/ 17` rested on.** Both are corrected
in place.

**A conclusion that is right for the wrong reason leaves the wrong reason in the file, and the next
thing built on it inherits the error.** Here the wrong reason sat directly above the line it
invalidated, and two sessions read past it.

## WHAT THE JOB ACTUALLY RUNS — read, not assumed

`Espn_pull_projections.py`, last modified **28 August**, ten days before the draft, untouched since:

- **`proj_2026`** is ESPN stat row id `102026`: season split, source 1. In season that is the rest of
  it. Mechanism and measurement agree.
- **`actual_2026`** is id `002026`, the season to date, and it is **not** contained in `proj_2026`.
- **the default sort is `--sort owned`**, so the 700 rows are the 700 most-owned, not the top 700 by
  preseason draft rank. That default is in-season-correct; the `draft` branch would not be.
- **the same file also carries `espn_adp`, `rank_std`, `rank_ppr`, `pct_owned` and `injuryStatus`,
  and every one is a draft-era or stale field.** `espn_adp` re-pulled after a draft is the
  contaminated market §1.1 forbids; the two ranks are STANDARD and full PPR, neither of them this
  league's 0.5 PPR; `injuryStatus` is hours old where `wire.py` has it live.
  **GREPPED: the week sheet reads none of them.** It takes `proj_2026`, `actual_2026` and
  `raw_actual_stats`, and everything live comes from `wire.py`. Keep it that way.

**And the 72 "available and not on our board" players in `ff_log.txt` are not this job's fault** —
Wentz, Higgins, Dillon, Aiyuk, Mixon, Chubb, Ekeler, Jonnu Smith and Hunt are all nine in the pull.
The board is a separate draft-era file.

## OPEN

- **[OPEN]** The board `wire.py` checks availability against is a draft-era file and **72 available
  skill players are not on it**, so they are absent from the sheet entirely. The pull has them.
  **NOT YET RUN**, and it is the largest remaining in-season gap.
- **[OPEN]** `Espn_pull_projections.py` holds Matt's ESPN `swid` and `espn_s2` in plaintext, a second
  copy of the credentials `wire.py` owns. Mine to consolidate; **not touched tonight** because it is
  a live script he runs and a broken pull on a Wednesday costs a week.
- **[OPEN]** `BLEND_W` was fitted with last season's ppg as the prior and its weight on this season
  recorded as an UPPER bound, because ESPN's projection is the better prior. **Reading that
  projection correctly makes it better still, so the bound is looser, not tighter.** The weight is
  not shaded to suit; that would be the guess the measurement exists to avoid. **NOT YET RUN**: the
  re-fit needs a per-week projection archive, and only two snapshots exist (7 and 24 September).
