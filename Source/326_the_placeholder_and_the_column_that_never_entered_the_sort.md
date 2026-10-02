# 326. The placeholder, and the column that never entered the sort

*16 Sept 2026, 22:40 UTC. Matt's four-part message. His claim about young backups and rookies,
taken seriously, stated in its testable form, and priced against what this project has actually
measured. One live defect found on the way.*

---

## 1. WHAT CHANGED

1. **His methodological point is right and it corrects one of our own sentences.** Section 4.25b's
   "age 28+ is null net of availability" is a null about **mispricing**, not about decline. The
   directive's gloss, *"do not fade a player for being old,"* is the stronger claim and it is not
   what was measured.
2. **On his mechanism the honest count is three underpowered cuts, all leaning his way, none
   significant.** That is not "tested and dead". It is not tested.
3. **The Dobbins case is measured and he is right about it.** Our board had Dobbins 39.2 points
   above Harvey. In the only week played, before the hamstring, Harvey out-snapped him 51 to 43 and
   outscored him 6.1 to 3.6.
4. **The real finding is about the instrument, not the world, and section 4.28 already ordered the
   fix.** v8.9 says PUT NFL ROUND AND OVERALL PICK ON THE BOARD. It was written for receivers, it
   was never extended to backs, and in neither case was it made part of the **sort**.
5. **LIVE DEFECT: `Source\inherit_2026.csv` has the Denver backfield the wrong way round.** It names
   Dobbins as holding the job and Harvey as the next man. Week 1 says the reverse.
6. **JOB 3 queued for Fable**, testable form written below, before the run.

---

## 2. THE CLAIM, IN ITS TESTABLE FORM, BEFORE ANY TEST (0.5a2)

His words, 16 Sept: *"Better to take chances on younger talent but i never got any traction in that
during draft strategy... In short, high value backups and rookies are important!! I don't think we
value them correctly here."*

There are **two** claims inside that and they need different instruments.

**CLAIM A, about the world.**
POPULATION: running backs with a section 1.1 preseason price in the bench band, ADP 90 to 180,
2021 to 2025, who were not the highest-projected back on their own team.
SPLIT: NFL experience, years 1 to 2 against years 4 and up, at equal price.
OUTCOMES, both: (i) half-PPR weeks 1 to 14 minus what `log(preseason ADP)` predicts, fit within
season, the beat-against-price scale section 4.25 uses; and **(ii) the one that matters more,
whether he reached RB replacement at all, 9.92 half-PPR a game, which is section 4.13b's absolute
definition and answers "was he ever startable".**
DIRECTION HE PREDICTS: the young man wins on both, and by more on (ii) than on (i).

**CLAIM B, about our instrument.** The board's ranking is blind to it. This needs no simulation. It
is an inspection and it is done in section 5 below.

Claim A is **NOT YET RUN** with the form written down, which is one of section 0.5(a4)'s three
answers. Claim B is **TESTED**, by reading the files.

---

## 3. THE METHODOLOGICAL CORRECTION HE IS OWED

Section 4.25b reports **age 28+ = -3.8, p=0.39** against **games played 12 or fewer = -19.4,
p=0.00004**, and concludes age acts through availability.

The outcome in both is **beat against preseason price**. So a null on age says: *the market already
discounts old backs by about the right amount.* It does **not** say old backs do not decline. If
the market prices decline correctly, a null is exactly what a correct market produces, and the
same null would appear whether decline is large or zero.

That distinction was never stated, and the directive's plain-English gloss, *"do not fade a player
for being old; fade him for having missed time,"* reads as a claim about decline. **It is a claim
about price.** Corrected here; the section 4.25b text should carry it.

The practical consequence is the opposite of how it has been used. If the market prices age
correctly at the top of the board, that says nothing about pick 128, where section 4.14 records that
two thirds of the board sits inside ESPN's undrafted sentinel and there is no real market price at
all. **A market-calibration result cannot be carried into a region with no market.** That is where
Matt drafts his backups.

---

## 4. THE HONEST COUNT ON HIS MECHANISM

His mechanism: a young man behind an older starter takes the job, so at equal price the young man is
worth more.

| measurement | population | result | reading |
|---|---|---|---|
| doc 141, incumbent vs challenger in an unsettled backfield | n=19 team-seasons | **+8.2, p=0.604**, CI [-22.9, +38.1] | null, **point estimate leans his way** |
| 4.27, "younger than the starter" keeps the job after relief | n=40 RB events | **+10.8 pp, p=0.079** | suggestive, **his direction** |
| 4.27, rookie deal, 3 years or less | same | +2.1 pp, p=0.73 | null |
| 4.28 / doc 251, first-round rookie receivers displace | n=364 pairs | **60.0% vs 3.3%, p=0.000001** | **confirmed, and it is the draft-capital version of his claim** |

**Three of four lean his way and the one that is properly powered is the one that confirms him.**
Doc 251 is the same claim at a different position: youth alone was null (entering year 3, -3.1,
p=0.46), and **youth plus draft capital was a factor of eighteen.** Every indicator either of us
tried to out-scout the NFL draft with came back null; the draft's own verdict did not.

**What that suggests, and it is a hypothesis not a finding: "young" is the wrong variable and
"young with draft capital, behind a fragile starter" is the right one.** That is JOB 3.

**AND SECTION 4.27's OWN NULL IS UNDER RE-CHECK ALREADY.** Catalog B4 records that doc 276's
fragility split, 45.9% against 46.3%, n=115, was run on a population holding only backs who were
healthy through week 4, which removes much of the fragility it was testing for.

---

## 5. CLAIM B: THE INSTRUMENT. THIS IS THE PART HE IS SIMPLY RIGHT ABOUT

`Source\code_universe_v5.csv`, the spine the draft board sorts, carries these columns:

```
espn_id, player, pos, team_c, bye, injury_status, proj_leaguepts, proj_src, proj_missing,
synthetic, adp_pick, adp_rank, adp_censored, deep_rank_by_proj, vbd, gsis_id, fantasypros_id,
pff_id, sleeper_id, pfr_id, k2, captured_at, built_at, built_by
```

**There is no age, no NFL draft round, no NFL year, and no depth-chart position.** The sort key is
`vbd`, which is `proj_leaguepts` minus a positional replacement constant. A projection is a
weighted average over a season that has not happened; it cannot distinguish a man who will hold a
job for seventeen weeks from a man who is keeping a seat warm, and nothing downstream of it can
either.

Section 4.20's `depth_map.py` emits UNSETTLED / contested / LEAD BACK and a `job worth` column, and
section 4.28 v8.9 ordered the draft-capital column outright:

> **PUT NFL ROUND AND OVERALL PICK ON THE BOARD.**

That was written on 9 September, for receivers, in a receiver document. `Source\pedigree_2026.csv`
does carry `nfl_round`, `nfl_pick`, `nfl_year`, and it was built **9 September, after the draft**,
as an in-season file. It was never joined to the spine.

**His sentence is the correct diagnosis and it names the mechanism:** *"I may have gotten a flag on
the page for it but i need to the model to factor that in because it already figures out where the
value is, and if no other value indictor, that player looks just fine."*

**A flag that does not enter the sort loses to the sort.** That is doc 240's Spears error and doc
251's job_ceil error in a third place, and in this one it is upstream of both: it is in the board
itself.

---

## 6. THE CASE HE BROUGHT, MEASURED

`Source\code_universe_v5.csv`, the shipped board:

| | board projection | VOR | ADP |
|---|---|---|---|
| J.K. Dobbins | 164.31 | **-4.28** | 122.55 |
| RJ Harvey | 125.14 | **-43.45** | 135.81 |

**The board rated Dobbins 39.2 points above Harvey. The market rated them 13 picks apart.**

`Source\form_2026.csv`, week 1, the only completed week:

| | snap % | carries | targets | half-PPR |
|---|---|---|---|---|
| RJ Harvey | **51** | 3 | 4 | **6.1** |
| J.K. Dobbins | 43 | 8 | 0 | 3.6 |
| Jonah Coleman | 6 | 0 | 0 | 0.0 |

**Harvey led the backfield in snaps and in points in week 1, before the hamstring.** Dobbins never
held the job the board was projecting. His 164 was a placeholder number and there was no column that
could say so.

`Source\pedigree_2026.csv` has what the board did not: **Harvey, 2025 NFL draft, round 2, pick 60,
year 2.** Section 4.28's cliff is at round 1, on receivers, on a one-year event; pick 60 is not that
cell and this document does not claim it is. What it claims is narrower and sufficient: **the fact
existed, in a file on the same drive, and the ranking could not see it.**

**ONE WEEK IS ONE WEEK.** This is a single case and it is Matt's own case, which is the weakest
possible sampling frame. It is here as an existence proof for the instrument gap in section 5, not
as evidence for claim A. Claim A gets a test or it gets nothing.

---

## 7. THE LIVE DEFECT FOUND ON THE WAY

`Source\inherit_2026.csv`, built 14 Sept:

```
DEN, holds_the_job = J.K. Dobbins, starter_g25 = 10, job_pays = 164.1,
     why = "missed 7 games in 2025", next_man = RJ Harvey, best_2wk_2025 = 19.35, floor = clears
```

**It has the two men the wrong way round.** Harvey out-snapped and outscored Dobbins in week 1. The
row is built from the depth chart plus the preseason pull, both of which say Dobbins, and doc 320's
`usage_depth()` is the thing that corrects a chart from usage. **It will not fire until the week-3
sheet**, because `min_weeks=2`.

**THAT THRESHOLD SHOULD NOT BE LOWERED, AND THE REASON IS DOC 320'S OWN CONTROL.** Fixture C18/C19,
Indianapolis: Taylor 25 opportunities, McGowan 14, Giddens 2. **One completed week names Giddens.
Two name McGowan.** One week was demonstrated to name the wrong man, and Denver is a case where it
would have named the right one. Both are true. The answer is not a lower bar.

**RECOMMENDED, and it is small:** when the chart's lead man and the usage leader disagree and there
are too few weeks to re-rank, the row should say so rather than print the chart's answer silently.
One field, one sentence on the page, no change to the ordering. Queued, not shipped, because
shipping it tonight is exactly the untested change doc 321 is about.

---

## 8. WHAT THIS DOES NOT SAY

- It does **not** say Harvey is better than Dobbins. It says the board's 39-point gap had nothing
  behind it that week.
- It does **not** say age predicts decline. Nothing here measured decline.
- It does **not** say young backups beat veterans at equal price. **That is claim A and it is NOT
  YET RUN.**
- It does **not** license dropping Dobbins. Section 4.19 is untouched: four of five backs Matt adds
  never give him a startable stretch, and the wire cannot patch a running-back hole.

---

## 9. OPEN

- **JOB 3**, claim A, queued in `Source\REDTEAM_TASKING_PROMPT.md`. `[NOT YET RUN]`
- **The section 4.25b wording**, price versus decline, needs the correction in section 3 above.
  `[OPEN]`
- **The draft-capital column on the spine**, section 4.28 v8.9's order, extended to backs and made
  part of the sort rather than a badge. Post-season, because the spine has no builder, doc 143.
  `[OPEN]`
- **The disagreement tell** in section 7. `[NOT YET RUN]`
- **Catalog B4**, doc 276's fragility null, still under re-check. `[OPEN]`
