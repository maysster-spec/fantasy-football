# 153 — Two levers, three words, and what actually cascades

*2026-09-03, T-4. Written because Matt has now said three times that the frozen/rebuild
explanation does not land. That is my failure, not his. This doc replaces the explanation.*

> **CORRECTION, 2026-09-04 (doc 154 §0). I MEASURED §5 AND §8 ON A STALE BOARD.**
> `refresh_adp.py --write` had already run on Matt's machine at 13:18 on Sept 3, so the live board
> already carried the 09-03 ADP and my working copy did not.
> **Two consequences, and only two.** §5's **D** column is not a proposal — it describes a change
> that is already applied; and the **margins in §5 and §8 are superseded** by doc 154 §2, measured
> on the current board (they moved, but the shape did not: 44.6 points of spread at pick 8 down to
> 0.12 at 137).
> **§3, §4 and §6 are unaffected** — they compare *ranks*, and re-timing does not touch rank
> (verified identical, all 480 rows). **The verdict stands: re-time yes, re-price no.**

---

## 1. THE WORD "REBUILD" HAS BEEN DOING THREE JOBS. HERE ARE THREE WORDS.

I have been using one word for three different things, which is why nothing I said made sense.

**REPRINT.** Re-run the scripts that produce the paper — the board PDF, the ladder, the cards.
Same players, same order, fresher ink. This happens every time news lands and it is free.
Nothing about who is better than whom changes.

**RE-TIME.** Update ADP — the market's guess at when each player comes off the board. This is
`refresh_adp.py`. It does **not** change the order of the board. Chase Brown going at 14
instead of 19 does not make him a better player; it changes whether he is still sitting there
when Matt's turn comes. It moves `eff_pick`, every survival number, and `p(next)` on the live
board. It does **not** touch VBD or rank, so the ESPN prerank never needs re-injecting for it.

**RE-PRICE.** Replace the point projections, which changes VBD, which changes rank, which
changes the **order players are listed in**. This is the one Matt means when he says "rebuild",
and it is the only one that can break anything.

The rest of this doc uses those three words and never the fourth.

---

## 2. THE FRACTIONS. "4/5" MEANT "FOUR OF THE FIVE."

In the earlier table, `4/5` at a pick meant: *of the five players who would have been at the top
of my list at that pick on the frozen board, four are still in the top five after the change,
and one has been replaced.* `5/5` meant nothing changed. `2/5` meant three of the five were
swapped out.

It was a bad way to show it, because "still in the top five" is not the same as "still first",
and only the first one gets taken. **Section 5 replaces that test with the one that matters:
run the real engine on each board and see if the name it says out loud changes.**

---

## 3. "SO WHICH IS IT — REBUILD OR FREEZE?" THE GATE SAID REBUILD, AND IT WAS RIGHT TO, ABOUT A PART OF THE BOARD MATT NEVER DRAFTS FROM

`sept5_check.py` asks one question: *did enough of the top 161 stay within 2 rank slots?* Its
threshold is 150. The Sept-3 run scored **97**, so it printed REBUILD.

That is a single number for the whole top 161, and it hides where the movement is. Re-priced
against the 09-03 pull with §4.1's replacement levels held, rank stability by band:

| old rank | n | within 2 slots | | biggest move |
|---|---|---|---|---|
| **1–24** | 24 | **24** | **100%** | 2 |
| **25–48** | 24 | **24** | **100%** | 2 |
| 49–84 | 36 | 28 | 78% | 17 |
| 85–120 | 36 | 22 | 61% | 11 |
| 121–161 | 41 | 17 | 41% | 65 |
| 162–480 | 319 | 110 | 34% | 198 |

*(115 of 161 on my measure against sept5_check's 97 — the two compute rank differently; the
shape, not the number, is the point. Both fail the threshold.)*

**Nothing in the top 48 moves more than two slots.** Picks 8, 17, 32 and 41 draw from that
range. The gate fires on ranks 85–161 — the region §4.14 already says rests on a fabricated
ordering and §7 already calls a coin flip.

**The gate is not wrong. It is answering "has the board changed?" when the question is "has
anything I will actually pick changed?"** Those diverge, and this is the first time anyone has
measured the difference.

---

## 4. RE-PRICING DOES NOT TILT RB AGAINST WR — BUT RE-DERIVING THE LEVELS WOULD

Projection drift 08-23 → 09-03, players who go inside pick 170:

| pos | n | mean | median | sd |
|---|---|---|---|---|
| QB | 69 | +0.10 | −0.01 | 10.74 |
| RB | 112 | +1.86 | 0.00 | 12.05 |
| WR | 193 | +1.34 | 0.00 | 6.48 |
| TE | 106 | +0.52 | 0.00 | 2.85 |

**RB minus WR = +0.51 points.** §4.1b calls ±1.5 VBD the level that matters on an RB-vs-WR
near-tie, so holding the replacement levels keeps the re-price positionally neutral.

Re-deriving the levels from the new pull does **not**: RB30 falls 14.27 and WR30 falls 8.67, a
net **+5.60 VBD to every RB in every RB/WR near-tie** — 3.7× the level §4.1b says matters, off
one week of projection noise. §4.1b's "do NOT make this self-refitting" is exactly this. That
option is dead and stays dead.

The only sizeable individual moves inside the top 110:

| player | pos | rank | proj |
|---|---|---|---|
| George Kittle | TE | 65 → **48** | 141.9 → 155.1 (+13.2) |
| Tucker Kraft | TE | 59 → **72** | 145.0 → 138.2 (−6.7) |
| Chuba Hubbard | RB | 92 → 83 | +7.4 |
| Jaylen Warren | RB | 71 → 63 | +2.3 |
| Jonathon Brooks | RB | 86 → 78 | +7.1 |
| David Montgomery | RB | 53 → 47 | +7.0 |

Everything else in the top 110 moves five slots or fewer.

---

## 5. THE FACTORIAL: FOUR BOARDS, THE REAL ENGINE, THE SAME ROOMS

`reprice.py` / `multi.py`. Four boards — **A** frozen · **P** re-priced only · **D** re-timed
only · **PD** both — each run through the production `Engine` at all twelve skill picks against
six opponent rooms drawn under §4.12's affine noise, `rollout_inner=20`.

| pick | A: margin #1 vs #2 | P changes | D changes | PD changes |
|---|---|---|---|---|
| 8 | 10.03 | 0 of 6 | 1 of 6 | 3 of 6 |
| 17 | 10.57 | 2 | 4 | 2 |
| 32 | 6.87 | 5 | 2 | 3 |
| 41 | 11.43 | 4 | 3 | 4 |
| 56 | 3.22 | 4 | 4 | 4 |
| 65 | 1.42 | 6 | 4 | 5 |
| 80 | **0.53** | 4 | 4 | 4 |
| 89 | **0.53** | 6 | 5 | 5 |
| 104 | **0.32** | 6 | 6 | 6 |
| 113 | **0.22** | 6 | 4 | 5 |
| 128 | **0.00** | 6 | 5 | 5 |
| 137 | **0.17** | 6 | 5 | 6 |

**CAVEAT, stated because it changes how the table reads:** only the **P** column is a clean
board-versus-board comparison. P leaves ADP alone, so its rooms are identical to A's and every
change is the board's doing. D and PD move ADP, which moves who is already gone — their changes
mix "the board reordered him" with "somebody else took him", and that mixing is not a defect,
it is what re-timing *is*.

**The margins are the finding, not the change counts.** From pick 80 on, the engine's first and
second choices are inside 0.6 points of each other, and at 128 they are identical. At that
distance *any* perturbation flips the name, so "P changed 6 of 6" at pick 128 does not mean the
re-price is powerful — it means there was nothing there to change. `[The absolute margins are
inflated by the winner's-curse doc 139 identified at low `rollout_inner`; the SHAPE — large
early, zero late — is what carries.]`

---

## 6. VERDICT: RE-TIME YES, RE-PRICE NO, AND CARRY TWO NAMES BY HAND

**Do re-time.** `refresh_adp.py` on the Sept 5 pull. It is already written, dry-run by default,
archives the old board, re-pins `check_kit`, and refuses rather than writing a wrong `eff_pick`
if a keeper name fails to resolve. It cannot change rank, so the prerank stays valid. Doc 109
measured the market moving on 160 of the top 161 in one week; this is the lever that is actually
doing work.

**Do not re-price.** Measured, it buys almost nothing where Matt drafts — the top 48 is frozen
solid at 100% within two slots — and everything it *does* change sits at picks whose margins are
under a point, where §7 already says Matt decides and the engine does not. Against that, it
rewrites the one file that must not be wrong at 8:00 PM Monday. **The trade is bad.**

**Carry the two real moves by hand.** George Kittle **+17 ranks** (65 → 48) and Tucker Kraft
**−13** (59 → 72) is a 20-point swing between two tight ends who sit right on top of pick 65.
That is worth a line on the card. Nothing else in the top 110 moves more than 9.

**What I got wrong, and where.** Doc 150 argued against re-pricing on the grounds that §4.1's
levels, §4.2's pick-8 dollars, §4.10's rule race and §4.12's noise were all fitted to this
projection set. That reason is weaker than I made it sound: §4.12 is fitted on **ADP**, not
projections; §4.10 is a comparison of rules on one board, so it survives any board; and §4.2's
pick-8 conclusion is unchanged because pick 8 does not move under any option tested. **The right
reason to hold the price is the band table in §3, not the fitted-constants argument.** Same
verdict, different and better evidence.

---

## 7. THE CASCADE: THE FIRST PICK DOES NOT PROPAGATE

`cascade.py`, 40 rooms per arm, `rollout_inner=24`. Arm 1 lets the engine take its own pick 8;
arm 2 forces an RB there. Position mix at each of Matt's picks:

| pick | *engine's own 8* QB/RB/WR/TE | *forced RB at 8* QB/RB/WR/TE | margin #1v#2 |
|---|---|---|---|
| 8 | 0 / **72** / 28 / 0 | 0 / 100 / 0 / 0 | 13.7 |
| 17 | 20 / **62** / 18 / 0 | 20 / 58 / 22 / 0 | 6.9 |
| 32 | 5 / **65** / 22 / 8 | 5 / 65 / 22 / 8 | 13.2 |
| 41 | 8 / 42 / **45** / 5 | 8 / 35 / **55** / 2 | 5.2 |
| 56 | **48** / 18 / 30 / 5 | **52** / 15 / 28 / 5 | 4.5 |
| 65 | 20 / 12 / 35 / 32 | 15 / 12 / 42 / 30 | 2.5 |
| 80 | 28 / 38 / 15 / 20 | 30 / 30 / 15 / 25 | 0.6 |
| 89 | 48 / 12 / 8 / 32 | 42 / 18 / 10 / 30 | 0.9 |
| 104 | 22 / 40 / 20 / 18 | 22 / 38 / 22 / 18 | 0.3 |
| 113 | 2 / 50 / 8 / 40 | 5 / 50 / 5 / 40 | 0.1 |
| 128 | 0 / 70 / 10 / 20 | 0 / 68 / 10 / 22 | 0.0 |
| 137 | 0 / 58 / 22 / 20 | 0 / 58 / 22 / 20 | 0.1 |

**Three things fall out.**

**(a) Forcing the first pick changes essentially nothing downstream.** The only column that
moves is pick 41 — WR 45% → 55%, because the forced RB at 8 leaves one more WR wanted. Picks 56
onward are within sampling noise of each other. **The engine self-corrects inside two picks.**
There is no "if WR first, then X" chain to plan around.

**(b) Pick 8 is an RB 72% of the time in a real room.** §4.2 and doc 139 pick Amon-Ra St. Brown
from the *undepleted* board; across 40 rooms where seven managers pick first, the top receivers
are often already gone and the best remaining player is a back. **Both are right and they answer
different questions.** The plan "best board player at 8" is unchanged — it simply resolves to an
RB more often than not.

**(c) There is no modal draft.** The most common opening-six shape appears in **3 of 40** rooms
(`RRRWQW`). Anyone planning a fixed sequence is planning for a room that will not happen.

---

## 8. SO WHERE IS THE EDGE?

Not in the position order. In the margin column, which splits the night in two:

**Picks 8 · 17 · 32 · 41 · 56 — margins 3 to 13 points. The board decides.** Matt's job here is
to *not* override it. The one exception the project already recognises is pick 32, where doc 139
showed the margin converging to 0.15 as compute rises — more compute does not find a winner
there, it becomes consistent about there not being one. **Pick 32 is Matt's.**

**Picks 65 through 137 — margins 2.5 falling to 0. The board has no opinion.** Everything it says
here is a tie broken by rounding. This is where every human input in the project lives and it is
the *only* place any of them can pay: the analyst calls, the `12g` availability badge (§4.22),
the UNSETTLED backfield flag and `job worth` (§4.20), the §4.18 keeper audition, the §4.18b/c
QB2 rule at 104/113 — and now the dated news from §9 below.

**And the two halves meet in an uncomfortable place.** The engine's most-taken late names across
40 rooms are **J.K. Dobbins at 104 and 113**, **Jacory Croskey-Merritt at 137**, **Aaron Jones /
Kyle Monangai at 128**. Those are, almost exactly, the players whose news got worse in the last
week. The board cannot see news, and its margins there are zero, so it defaults to whoever ESPN
still projects. **That is the structural reason the research matters and it only matters after
round 6.**

---

## 9. THE RESEARCH IS NOW ON THE BOARD — `apply_research.py`

Gemini's 23 dated facts had nowhere to go: `player_context.csv` is the only file the live board
reads for notes (doc 100) and every note column was already owned — `why`/`concrete`/`bull`/
`bear` by the analyst and injury sweep, `job`/`job_ceil` by `depth_map.py`, `mine`/`mine_note`
reserved for Matt. **A finding in a CSV nobody reads is not a finding.**

`apply_research.py` **prepends** one segment to `why`, formatted `NEWS 09-03: <fact>`.
`live_draft.py` splits `why` on `||`, renders segment 0 as the row's STATUS/NOTE and the next two
as extras — so the fact becomes the top line of the player card and everything already there
moves down one slot intact. **22 of 23 landed** (Brenton Strange is not among the 265 context
rows). Verified by *rendering* the production `card_data()`, not by reading the CSV:

> **J.K. Dobbins** — STATUS · AVOID — NEWS 09-03: Foot/soft tissue injury; reported on
> September 2 that the injury could force him onto Injured Reserve.

**Red team of my own change, before it shipped — two defects, both found and fixed:**

1. **`live_draft.py:903` drops a leading "no injury news found" segment only when it is
   `why[0]`.** Prepending pushes it to position 1, where that guard cannot see it — so that
   string would have come *back* onto cards it had been cleaned off. **87 rows** were exposed.
   Fixed by applying the same strip, on the same condition, inside the stamper. Verified: 0 rows
   carry it after the write.
2. **It stacked.** Run again tomorrow with a new date and a row carries two NEWS segments, the
   superseded one rendering as an extra beside the current one. Fixed by dropping any prior
   `NEWS dd-dd:` segment first. Verified by running it twice with different dates: max NEWS
   segments per row = 1.

Guard copied from `depth_map.py`: it exits non-zero if any column other than `why` differs, or
if the row count changes. Verified: 0 other columns changed, 265 rows in and out. The old file
is archived to `_archive\player_context_20260903.csv` and `check_kit.py` is re-pinned to
`(78698, '5ffce5f7851f6ff0')`.

**ONE CONTRADICTION IS NOW VISIBLE ON A CARD AND IT IS REAL.** Rico Dowdle's card reads
`NOTE — Backup; listed behind Jaylen Warren` directly above `BACKFIELD — UNSETTLED, the job is
worth 174 pts`. The `job` label comes from `depth_map.py` run against the **Aug-23** projections;
Pittsburgh's backfield has since resolved. `sept5_after.bat` step 3 re-runs `depth_map.py`, which
will fix it. **Until Sept 5 the backfield labels are one pull stale — read the NEWS line over the
BACKFIELD line where they disagree.**

---

## 10. LIMITS

- Six rooms in §5 and forty in §7. The margin *shape* is stable across both; individual change
  counts are not, and I do not quote them as rates.
- `rollout_inner` is 20–24 here against 60 on the clock. Doc 139 showed low inner inflates
  margins through a winner's curse. Every margin above is an upper bound; the late ones are
  already at zero and cannot be inflated below it.
- The four boards in §5 are built by `reprice.py`, which is a research script, not
  `make_board_file.py`. Its P board holds §4.1's exact levels and re-applies the news overrides
  last, matching the builder's steps 4–7; it does not re-derive `gone_ahead` for the P arm
  (unnecessary — P does not move ADP) and does re-derive it for D and PD from the 09-03 keeper
  ADPs. **Nothing here has been written to `board_v8_fixed.csv`.**
- §7's cascade forces a *position*, not a *player*. "What if I take a specific WR at 8" is a
  different and narrower question.
- The claim in §8(c) — that the engine's late favourites are the players whose news soured — is
  an **observation on 40 rooms**, not a test. It is not evidence that the board is biased toward
  injured players; it is evidence that the board is blind to news and indifferent late, which is
  already established.

---

## 11. ASSUMPTIONS, FALSIFIERS, AND THE MISSING INPUT (§7)

**Assumption 1 — the 09-03 pull is a fair picture of the market and the projections.**
*Invalidated by:* the Sept-5 pull landing materially different from the Sept-3 one. The 09-03
file carries 414 of the board's 480 rows; the 66 without a new projection all sit at
`eff_pick ≈ 158`, inside §4.14's undrafted sentinel, so none of them is live at a pick. If the
Sept-5 pull moves the top 48 at all — this one did not move it by more than 2 slots — §6's
verdict has to be re-run, and `reprice.py` re-runs it in about two minutes.

**Assumption 2 — margin between the engine's #1 and #2 is a fair proxy for "how much does this
pick matter".** *Invalidated by:* a case where the engine is nearly indifferent between two
players whose *season outcomes* are far apart. That is possible — the rollout scores expected
starting-lineup points, not variance, and §4.13's whole finding is that late variance is where
the titles are. **A zero margin means the board cannot separate them on expectation; it does not
mean they are the same bet.** This is the single biggest caveat on §8 and it argues for Matt's
judgement late, not against it.

**Assumption 3 — the opponent rooms are realistic.** They are drawn from §4.12's affine noise on
`eff_pick`, which is the best-calibrated object in this project (RMSE 0.89) — but §4.15 is
explicit that dispersion alone is not a survival model, and these rooms use no manager model at
all. They are fine for "does the board's answer change", which is a paired comparison where the
room cancels. They would be wrong for any absolute survival number, and none is quoted here.

**The missing input that would most improve this: a second projection source.** Every number in
§§3–6 is ESPN's projection compared against ESPN's projection one week later. That measures
*drift*, not *error*. With a second board (FantasyPros ECR is already on disk as a §4.4
divergence check, and Boone's Sept-1 file is in `Source\`) the question changes from "did ESPN
change its mind?" to "was ESPN's number the odd one out?" — which is the question a re-price
should actually be gated on. That is a post-draft build; there is not time before Monday, and
§4.4's measured divergences are the stopgap.
