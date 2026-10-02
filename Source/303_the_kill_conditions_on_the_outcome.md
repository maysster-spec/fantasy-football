# 303 -- the kill conditions on the outcome, and the blocker was the wrong release

**14 September 2026. Third reader, answering `REDTEAM_REPLY_302.md` and doc 302.** Six of their
findings stand, two of the three headline ones do not survive being run on five seasons, and the
one thing they put on Matt's to-do list was never blocked.

**Nothing on this page asks Matt to run anything.** Both of their scripts were run here, on all five
seasons, and the numbers below are mine, not theirs carried forward.

---

## 1. THE ANSWER FIRST

1. **Their BLOCKED item was not blocked.** They read the retired `player_stats` release, which stops
   at 2024. The live release is `stats_player`, and `stats_player_week_2025.csv` downloads from it
   at 8.66 MB. That is the file docs 297, 299 and 300 already ran on. **Their two Matt-to-do lines
   are deleted, not deferred.**
2. **Their kill of doc 300's startable rate does not stand, because their filter conditions on the
   outcome.** Keeping only the rows where the labelled lead back still led weeks 2-14 deletes every
   case where the second back took the job -- which is the event the week-1 share predicts.
3. **Their own D1 filter is the right one, and it makes the rate bigger, not smaller.** On the 114
   claimable rows over five seasons the top band is **64% startable**, against doc 300's published
   50% and their proposed 20%.
4. **BUT THEIR EDIT 2 IS RIGHT, AND FOR A STRONGER REASON THAN THEY GAVE.** The payoff *is* the
   takeover. Multiply the week-1 share by the job-opens term; never substitute one for the other.
5. **The tie-break defect is real and one twenty-fifth the size they reported.** Three rows of 143,
   not nine. Reversing all three moves the headline from 50% to 46%, p unchanged at 0.0000.
6. **Their replacement finding weakens on the fifth season and must not be written as published.**
   The 2nd-receiver squeeze is **-0.031, p=0.078** on their own conservative null, not -0.045 at
   p=0.011. `[SUGGESTIVE]`, not confirmed. Their own section 2.1 warned this could happen.
7. **Their worst-case live defect is not live, and there is a real one underneath it.** The page
   never printed "this page prices byes and not injuries" after 12 Sept -- that sentence sat in a
   dead duplicate of the cost box, overwritten before render. The duplicate is deleted.
8. **Their two shipping constants are confirmed wrong and both are fixed**, one of them more
   seriously than they said.

---

## 2. THE BLOCKER WAS THE WRONG RELEASE

Doc 302 section 2.1: *"`stats_player_week_2025.csv` ... The 2025 asset returns HTTP 404. I verified
this by listing the assets, not by inferring from one failed download."* The listing was honest and
the conclusion was wrong, because it was a listing of the **`player_stats`** release. nflverse
retired that name; weekly player rows now ship in **`stats_player`**.

```
stats_player/stats_player_week_2021.csv  200  8,477,784
stats_player/stats_player_week_2022.csv  200  8,408,729
stats_player/stats_player_week_2023.csv  200  8,332,874
stats_player/stats_player_week_2024.csv  200  8,470,040
stats_player/stats_player_week_2025.csv  200  8,656,387   <-- the "blocked" file
player_stats/player_stats_2025.csv       404              <-- what they checked
```

**The lesson is not "they were careless", it is 0.5(a4) turned on its own answer.** They named the
missing input, which is what the rule asks for. What the rule does not yet say is that **a BLOCKED
verdict is itself a claim and gets one falsification attempt before it is written down** -- here,
one sibling release, thirty seconds. Their falsifier register even lists this one ("Nothing. This
one is just arithmetic and the 2025 file settles it") without trying it.

---

## 3. DOC 300 ON FIVE SEASONS

**POPULATION -- restated because it is inherited (0.6): team-seasons 2021-2025 whose week-1 RB usage
leader and second back both played in week 1 with combined RB work >= 10, and whose second back
appeared in 4+ of weeks 2-14. n = 143.** PREDICTOR: RB2's share of team week-1 RB carries plus
targets. OUTCOME: half-PPR per game over weeks 2-14, and whether that reached 9.92
`[INHERITED: 4.1's RB30 season total / 17, derived not measured -- 4.13b]`. Permutation, 4,000
draws, one-sided, seed fixed. Script: `Scripts\research\wk1\wk1_redteam2.py`.

### 3a. The four populations, side by side

| cut | n | <20% | 20-30% | 30-40% | **40%+** | 35% split, startable |
|---|---|---|---|---|---|---|
| **F0** everything (doc 300 as published) | 143 | 7% | 11% | 39% | **50%** | **+29 pt, p=0.0000** |
| **F1** claimable only (their D1) | 114 | 5% | 7% | 37% | **64%** | **+36 pt, p=0.0008** |
| **F2** labels held only (their E1) | 95 | 3% | 8% | 19% | 27% | +8 pt, **p=0.2560** |
| **F3** claimable AND labels held | 77 | 3% | 4% | 18% | 33% | +9 pt, **p=0.3050** |

Their four-season E1 gave +2 points at p=0.5553; on five it is +8 at p=0.2560. **Same verdict, and
their replication holds.** So does F3: the intersection does not rescue the rate either, which kills
the easy answer that E1 only removed already-rostered stars.

### 3b. WHY E1 KILLS IT, AND WHY THAT IS NOT A RETRACTION

**Testable form, written before the run:** *if E1 kills the startable half because it conditions on
an outcome the week-1 share exists to predict, then it should delete the hits themselves, and the
preseason-knowable filter should leave them in.*

**It deletes fifteen claimable rows at 35% or more, and eleven of them were startable:**

> Bijan Robinson 47% 12.6 - Rhamondre Stevenson 45% 14.0 - Kyren Williams 44% 19.3 - Devin
> Singletary 43% 10.2 - Alexander Mattison 42% 8.8 - Jamaal Williams 42% 12.9 - Jerome Ford 41%
> 11.9 - Tony Pollard 40% 16.7 - Travis Etienne 38% 10.7 - Rico Dowdle 38% 11.7 - Javonte Williams
> 37% 8.9 - Bucky Irving 36% 12.2 - Latavius Murray 36% 6.4 - Roschon Johnson 35% 4.0 - Chuba
> Hubbard 35% 14.9

**Every one of those is a back you could have claimed who then took the job.** Doc 302's testable
form was *"if a high week-1 share identifies a backup breaking through, the man labelled the lead
back should still be the lead back"* -- and a backup breaking through is precisely the man ahead
**not** keeping the lead. The condition contradicts the hypothesis it was written to test. **This is
4.23's trap: never condition on an outcome-correlated filter and read the result as a bias in the
predictor.** Same shape as the 20.7% rushing-yards "projection bias" that was selection on games
played.

**What E1 IS, and it is worth having.** It is a decomposition, not a population. It answers *"if the
job never changes hands, is a big week-1 share still worth claiming?"* -- and the answer is **no:
27% startable in the top band, not separated from the rest at p=0.26.** That is a real and useful
null and it belongs in the ledger. It is not a reason to retract a rate measured on a population
that includes the takeovers.

### 3c. WHAT TO QUOTE INSTEAD OF 50%

**Quote 64%, on the claimable population, n=14 in the band, +36 points at p=0.0008.** Their
claimability proxy -- RB2 was not a startable fantasy back the prior season -- is preseason-knowable
and does not touch the outcome, so it is the honest filter and it is theirs. Doc 300's 50% was
measured on a population where **14 of the 28 top-band rows were men already rostered in every
12-team league** (Gibbs, Conner, Ezekiel Elliott, Aaron Jones, David Montgomery, Gus Edwards and
the rest). **The published number was too LOW for the decision it serves and too high for the
population it named.** Both of us had it wrong in opposite directions.

### 3d. AND IT IS NOT A STANDALONE TERM -- their edit 2, confirmed harder

Of the **14 claimable top-band rows, 13 had a lead back who missed time.** Split at 35%:

| population | n | 35%+ startable gap | p |
|---|---|---|---|
| claimable AND the man ahead missed time | 68 | **+33 pt** | **0.0092** |
| claimable AND the labels held (the job never moved) | 77 | +9 pt | 0.3050 |

**So the share tells you WHICH seat is worth owning and the job-opens term tells you WHETHER it
opens, and the startable payoff needs both.** Doc 302 reached "multiply, do not replace" from a
correlation -- the top band's lead back misses time 68% of the time against 49-58% elsewhere. The
stronger statement is mechanical: **the payoff IS the takeover, so a seat price that does not carry
a job-opens probability is pricing an event it has excluded.** `[TESTED, n=143]`

### 3e. Two of their smaller objections, sized

**The tie-break.** `lst.sort(reverse=True)` on `(work, player_id)` consults the id **only on an
exact tie**. Doc 302 counted "nine rows at 45% or above" as exposed; a 45/55 split is not a tie and
the id never enters it. **Exact ties: 3 of 143** -- 2021 JAX (Hyde/Robinson), 2021 ARI
(Conner/Edmonds), 2025 KC (Hunt/Pacheco). Reversing all three: top band **46%** against 50%, split
+27 points against +29, **p=0.0000 either way.** Real defect, one twenty-fifth of the stated reach,
and **it does not touch Kaelon Black**, who is at 45% behind a man at 55%.

**The outcome keyed on `player_id` alone.** Re-keyed on `(team, player_id)`: 140 rows against 143,
top band **50%**, split +29 points, p=0.0008. **Right in principle, null in effect.** Both of their
section 13 items are closed.

---

## 4. DOC 299 ON FIVE SEASONS -- THE KILL STANDS, THE REPLACEMENT WEAKENS

Their design 2 is correct and I accept it without reservation: a share is a share of one hundred
percent, and comparing shares across two seasons whose denominators hold different men measures
arithmetic. Run on 2021-2025, 127 team-seasons, 54 arrivals against 73 controls:

| slot | arrival | none | difference | p within team | p within season |
|---|---|---|---|---|---|
| 1st, the incumbent | +0.002 | -0.015 | +0.017 | 0.87 | 0.84 |
| **2nd** | **-0.025** | **+0.007** | **-0.031** | **0.078** | **0.020** |
| 3rd alone | +0.007 | +0.021 | -0.013 | 0.18 | 0.19 |
| 4th alone | +0.022 | +0.023 | -0.001 | 0.32 | 0.54 |
| **3rd + 4th (doc 299's cell)** | +0.013 | +0.022 | **-0.008** | **0.158** | 0.263 |

**Doc 299's claim 2 is dead: -0.008 at p=0.158.** Confirmed on five seasons.

**Their replacement is SUGGESTIVE, not established.** Their four-season figure was -0.045 at
p=0.011; the fifth season moves it to **-0.031 at p=0.078 on the within-team null they themselves
called the conservative and correct one.** Their proposed 4.28 text quotes p=0.011. **Do not write
it.** The honest label is: a reallocation exists and it concentrates at the second receiver, at
p=0.078, `[SUGGESTIVE]`.

**Denver, unchanged in direction:** take the arrival caution off **Pat Bryant** -- his slot measures
-0.001 at p=0.32 and the caution was never established there -- and put a **watch** line, not a
finding, on **Troy Franklin**.

**And a caveat neither doc states.** Both designs measure SHARE. What pays is TARGETS, and share
times team targets is targets. A man can lose share and gain targets on a team that throws more.
**Design 2 settles the mechanism question Matt asked; neither design answers the fantasy question,
and nothing here should be quoted as points.** `[OPEN, inputs named: team target totals are in the
same weekly file.]`

---

## 5. THE CONSTANTS -- both confirmed, one worse than reported

`Source\sheet_constants.json`, archived before overwriting.

**`absence.rate.K` was 0.137, which is the QB and TE number.** Doc 297 measured kickers at **21.3%**
and said in terms that the row *"should not be quoted"* because 14 of 48 prior-year top-12 kickers
were out of the league the next season. **And the note claiming the cell "is not used" is not safe:**
`real_price()` is called on `fp`, the cheapest body Matt owns, and with two kickers rostered that is
a kicker. **`absence.streamer.K` was 7.5 with no source anywhere** -- directive 3's `[NO SOURCE]`.

**Fixed by DELETING both keys rather than correcting one.** With the key absent the lookup returns
None and `real_price()` returns None, so the page declines to price a kicker instead of pricing him
on a borrowed rate and an invented streamer. Setting rate.K to 0.213 while leaving streamer.K
unsourced would have made the arithmetic fire on a number with no provenance, which is worse.

Also fixed in the same write, all theirs: the population written two ways is now one sentence
("selectors 2021-2024, outcomes 2022-2025, four transitions"); `[INHERITED]` on RB/WR/TE now reads
`[INHERITED from doc 12, n irreproducible per 4.17]`; `seat.p_opens_note` now carries "under
re-check, catalog B4"; `seat.relief_ppg` 12.13 is declared canonical and doc 244's 11.2 recorded as
superseded, **so doc 297's handcuff bracket is about 8% low**; and the `potential.next_season`
30.2% now states that it is a different population from 4.30's 39.4%, not a competing figure.

---

## 6. THE DEAD COST BOX -- their item 5, settled, and it is not what they feared

They could not settle whether the `absence` block is consumed and flagged the worst case: *"if the
page now uses it, the printed disclaimer is false, which is worse than either alternative."*

**One grep settles both halves.** `sheet_engine.py` line 1009 reads the block and line 1046 calls
`real_price(fp, floor)`, **so the block IS consumed and doc 297 section 6's "no code change shipped
today" is false.** But the disclaimer sentence sat in a **first, dead build of `cost_line`**, at
lines 994-1001, unconditionally overwritten by the real build at 1047-1063 before the only read at
1090. **It never reached the page.** Ledger row 32's worst case is not live.

**The real defect is that it existed at all:** two constructions of one string inside one function,
0.5(c)4 one level below where that rule usually bites, with a sentence that stopped being true on
12 Sept sitting in the unreachable one. **Deleted, not corrected** -- there is one cost box and it
is built below. A reordering, a returned early, or a future edit to the second block would have put
a false sentence on the page Matt reads.

---

## 7. WHAT SURVIVES OF THEIRS, STATED AS READILY AS WHAT DID NOT

* **Design 2 is the right object** for doc 299 and the kill of claim 2 is correct and confirmed.
* **Every constants defect they found is real** and every one is fixed above.
* **The control gap is real and is the most important thing in their report.** The controls file was
  last written 12 Sept 13:09:08 and every production file at 16:48:5x. Four changes have no negative
  control, and their C16 finding is the sharpest: the recorded pool has **zero** off-board free
  players while the live pool has 71, **so doc 298's entire mechanism has never run against a
  realistic population.** Not fixed here. Named as the next batch, section 8.
* **Their multiple-comparison audit is right and boring** and the recommendation not to add a
  multiplicity rule to 0.2 is correct.
* **Their 5.2, 5.3 and 5.4 all make A1 more urgent**, and 5.4 is the one to act on: the streamer
  column should come from `wire.py`'s live free pool, not a four-year average add.
* **Their self-caught denominator bug**, reported before quoting the number it produced, is the same
  discipline doc 296 showed and is why this report is worth the read.

---

## 8. OPEN THREADS

* **NOT YET RUN, and it is the next batch:** the four missing negative controls -- the section-0
  THIS WEEK / CALENDAR split, the `absence` block, the drop-cost box position, and the ESPN team
  name (which needs a harness change first, because `fake_get('mRoster')` carries no name field).
  Plus refreshing `WIRE_20260910.csv` to an 11 Sept snapshot so the off-board path runs against 71
  rows instead of zero. **Each must be shown failing on the pre-12-Sept tree before it counts.**
* **NOT YET RUN:** the streamer column read from the live free pool instead of doc 12 (their 5.4).
* **NOT YET RUN:** the 2nd-receiver result with TE pooled into "receiver", and on raw share rather
  than per-game rate. Their section 13, and now it matters more, because the result is at p=0.078.
* **NOT YET RUN:** the squeeze in TARGETS rather than share (section 4's caveat, mine).
* **[OPEN]** `Source\` holds `293_the_late_pick_needs_a_door.md` **and**
  `293_the_late_pick_needs_a_door-1.md`, and `00_PROJECT_DIRECTIVE.md` **and**
  `00_PROJECT_DIRECTIVE-1.md`. Two more live naming collisions, alongside the two the directive
  already names as standing examples.
* **For the directive:** 0.5(a4) gains a fourth line -- **a BLOCKED verdict is a claim and gets one
  falsification attempt before it is written down.** Section 2.

**Files written:** `Source\303_the_kill_conditions_on_the_outcome.md` (new) ·
`Scripts\research\wk1\wk1_redteam2.py` (new, folder listed first) ·
`Scripts\research\wk1\run_wk1_redteam_5yr.txt`, `run_wk1_redteam2_5yr.txt` (new) ·
`Scripts\research\f1\run_squeeze_5yr.txt` (new) · `Source\sheet_constants.json` and
`Scripts\sheet_engine.py` (archived to `2026\_archive\` first). Nothing was written to ESPN, no
claim was filed, nobody was dropped.
