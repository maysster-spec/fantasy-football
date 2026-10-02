# 308 -- the page has never seen a snap of football

**15 September 2026, Tuesday, week 2 claim day.** Matt: *"This file can't be right since it doesn't
have but the same 3 players for Priority pickups."*

**He is right, and the cause is not the length of the list.** The list is short because of a cap, but
the cap is not what is wrong. **What is wrong is that no input to that section has seen a down of
2026 football, and it is saying so on the one week of the season where that costs the most.**

---

## 1. WHAT HE SAW, AND WHAT IS ACTUALLY UNDER IT

`WEEK_SHEET.html`, built 15 Sept, header **"Week 2 -- what to do"**. Priority pickups:

| # | name | why the page picked him | his week 1 |
|---|---|---|---|
| 1 | Jalen McMillan, WR TB | pedigree screen 3 of 3 | **no line. He did not play.** |
| 2 | Pat Bryant, WR DEN | pedigree screen 3 of 3, *verbatim the same sentence* | 6 tgt, 42 yds, 6.2 |
| 3 | Kaelon Black, RB SF | the McCaffrey seat, worth 302 | 43% snaps, 14 car, 7.5 |

Three layers, in the order I found them:

**(a) `sheet_engine.py` line 1108: `picks = ''.join(_mv(m, i+1) for i, m in enumerate(now[:3]))`.**
A hard cap of three. **But it did not bite this week** -- `now` held exactly three -- so the cap is
a latent defect, not this one.

**(b) The "sure" lane keeps exactly ONE man per position.** The loop at line 944 tracks a single
`best` per position and discards every other man at that position before anything downstream runs.
Six positions, six possible rows, ever. This week all three qualifying positions were bye fills
(TE week 6, K week 8, D/ST week 11) and were correctly routed to the calendar -- **so the "sure"
lane contributed nothing, and every row on the list is a bet.**

**(c) And every bet lane is frozen before week 1.** Enumerated by opening the scripts and listing
every file they read:

| input | vintage |
|---|---|
| `board_v8_fixed.csv` (`value`, the sort key) | preseason freeze, 07 Sept |
| `player_context.csv` | preseason news overrides |
| `pedigree_2026.csv` | columns are `g25 tgt25 ypt25 tpg25 ppg25` -- **all 2025** |
| `inherit_2026.csv` | preseason depth map |
| `pos_allowed_2025` · `redzone_te_2025` · `team_2025` · `team_shape_2025` | 2025 |
| `sched_2026` · `byes_2026` | fixed since May |

**`grep -niE "snap|stats_player|week_2026|form_2026" wire.py sheet_engine.py` returns nothing.**
Not one 2026 in-season input exists on any runtime path. **So the three names cannot change from
week to week except when a man is rostered or an ESPN designation moves.** It is a preseason list
wearing a weekly page's clothes, and that is exactly what Matt noticed from the outside -- 0.6
rule 4, a conclusion that contradicts his experience is a population question first.

**AND IT LANDS ON THE WORST POSSIBLE WEEK.** 4.31: a week-2 claim hits **34.6%**, a week-1 claim
**9.4%**, Fisher p=0.010, and the stated mechanism is that *a week-1 claim bets on a depth chart and
a week-2 claim bets on a snap count.* **The claim he files today is the week-2 claim, and the page
made it on a depth chart.** Doc 304 named this defect on 13 Sept -- *"the page led with a man who did
not play"* -- and on 15 Sept the page led with a man who did not play.

**This widens `AUDIT_LEDGER` row 29.** Row 29 says the week-1 backfield share is missing from the
SEAT PRICE. It is missing from the whole page, at every position.

---

## 2. THE MEASUREMENT: 19 FREE MEN PLAYED, AND THE PAGE NAMED NONE OF THEM

**POPULATION -- state it every time: the 280 rows of `WIRE_20260915.csv`, which is the free pool in
his league; 197 matched a week-1 nflverse line, 83 did not play or have no line.** nflverse's week-1
release is now the **full 32-team slate** (it was 30 of 32 when docs 302/303 ran -- doc 305 6 lists
that re-run as NOT YET RUN and this closes the input half of it).

**19 free skill players took 55% or more of their team's snaps with 5+ touches. None appeared.**
Six of them scored above his own positional bar in week 1: Vele 16.4 · Freiermuth 13.1 ·
Juwan Johnson 12.9 · Raymond 12.4 · Caleb Douglas 11.9 · and Bourne at 11.5 just under.

---

## 3. SO I TESTED THE SIGNAL INSTEAD OF ASSERTING IT

`week1_share.py` already measured this **at running back** (+29.1pp startable, p=0.0003). It had
never been asked at receiver, and 4.27 gives a real reason to doubt it transfers: *a backfield is
ONE job and a receiver room is three to five.*

**THE CLAIM IN ITS TESTABLE FORM, written before the run (0.5a2):** among pass-catchers who were NOT
startable the previous season -- men you could have had off a wire -- his share of his team's WEEK 1
targets predicts his weeks 2-14 half-PPR scoring, and a high share marks a receiver who reaches
replacement more often than the rest.

**POPULATION: every WR and TE, 2022-2025, who played week 1 with 1+ target, averaged BELOW his
position's replacement rate the prior season, and played 4+ of weeks 2-14. n=517.
BASELINE: the population's own 13.9% startable rate. OUTCOME: half-PPR ppg over weeks 2-14 reaching
WR 9.62 / TE 8.25** (doc 12, and per 9.4 these are 4.1 / 17, derived and not measured).
Permutation, 4,000-6,000 draws. `Scripts\research\wk1\wr_week1_share.py`, `wk1_wr_composite.py`.

**IT TRANSFERS.** Target share alone, on the wider 2021-2025 cut (n=707): **4% / 13% / 19% / 37%**
across the four bands, +24.7pp, **p=0.0002**. Each of the three measures is monotone on its own:

| week-1 measure | bottom band | top band |
|---|---|---|
| raw targets | 6% at 1-3 | **49% at 8 or more** |
| snap share | 3% under 40% | **39% at 80%+** |
| target share | 4% under 10% | **37% at 20%+** |

**THE COMPOSITE, count of three -- 8+ targets, 80%+ snaps, 20%+ of team targets. n=517, 2022-2025:**

| signals | n | wks 2-14 ppg | reached replacement |
|---|---|---|---|
| 0 of 3 | 322 | 3.95 | **6%** |
| 1 of 3 | 119 | 6.86 | 19% |
| **2 of 3** | **45** | **8.11** | **38%** |
| 3 of 3 | 31 | 8.26 | 42% |

**3-of-3 minus under-3: +29.8 points, permutation p=0.0002.** `[TESTED, n=517]`

**AND THE SHAPE IS SUBSTITUTION, NOT COMPOUNDING -- 0.5(a3), and it is the opposite of 4.30.**
The doubling is from ONE signal to TWO (19% -> 38%); the third adds four points on n=31. 4.30's
receiver composite went 5.0 -> 7.1 -> **39.4**, a factor of five at the third signal. **Two
composites, both at receiver, opposite shapes** -- because 4.30's signals are pedigree and career
rate, which are three near-independent facts, while these three are three views of one week's
workload. **So the operative bar here is TWO of three, and do not port 4.30's "you need all three"
across.** Matt's frame is right in both directions and that is the fourth time the direction has had
to be measured rather than assumed.

**THE TRAP I NEARLY SHIPPED, and it is 4.23's, third time.** The first run used 2021-2025 and gave
7% / 22% / 45% / 52% -- and its 3-of-3 cell was **Cooper Kupp, Justin Jefferson, Tyreek Hill,
Stefon Diggs, Keenan Allen, DeAndre Hopkins, A.J. Brown**. With no 2020 season on file, every 2021
player passed the not-startable filter, so the top cell was simply the league's WR1s. **Dropping
2021 costs 179 rows and moves the top cell from 52% to 42%.** Never let a filter that is supposed to
select wire men run on a season whose prior year is missing.

---

## 4. THE SIX FREE MEN THE SCREEN ACTUALLY NAMES TODAY

`WIRE_20260915.csv`, WR and TE, 2 or 3 of 3. Base rate 13.9%.

| player | pos | tm | bye | sig | tgt | snap% | tsh% | wk1 pts | own% | board VOR |
|---|---|---|---|---|---|---|---|---|---|---|
| **Malik Washington** | WR | MIA | 6 | **3/3** | 8 | 98 | 29.6 | 4.8 | 7.7 | -70.3 |
| Devaughn Vele | WR | NO | 8 | 2/3 | 9 | 91 | 17.3 | 16.4 | 12.9 | -64.5 |
| Kalif Raymond | WR | CHI | 10 | 2/3 | 9 | 60 | 34.6 | 12.4 | 0.2 | -125.2 |
| **Dalton Schultz** | **TE** | HOU | **8** | 2/3 | 8 | 66 | 21.6 | 5.5 | 19.7 | -36.8 |
| Kendrick Bourne | WR | ARI | 14 | 2/3 | 8 | 67 | 21.6 | 11.5 | 0.1 | -124.6 |
| Caleb Douglas | WR | MIA | 6 | 2/3 | 7 | 91 | 25.9 | 11.9 | 15.5 | -70.1 |

**Washington scored 4.8 and is the only 3-of-3. That is the finding, not a flaw in it** -- doc 235,
tier 2 of doc 305: the workload is the thing that predicts and the box score is not. Washington and
Caleb Douglas are the same receiver room and cannibalise each other; only one of them can be right.

---

## 5. THE RECOMMENDATION, AND IT IS A TIGHT END

**DROP T.J. HOCKENSON, ADD DALTON SCHULTZ.** Four reasons, three of them measured:

1. **Hockenson shares LaPorta's week-6 bye.** 6's doctrine calls a same-bye second the specific trap;
   **4.18c MEASURED it at +0.00**, because he never enters the lineup. His only job as a TE2 is the
   one he structurally cannot do, and the page already names him the cheapest real drop.
2. **Schultz's bye is 8**, so he actually covers week 6 -- the hole the calendar is holding a week-5
   claim open for.
3. **Schultz clears 2 of 3**, the operative bar: 38% reach replacement against a 13.9% base.
4. **19.7% rostered**, so if the button says Add it costs no priority at all.

**Second: Devaughn Vele** -- 9 targets on 91% of the snaps, same drop, if he would rather bet the
receiver. **Third: stand pat**, which is honestly defensible: doc 259 measured that the wire cannot
upgrade a working slot, and none of these six beats his starting nine this week.

**WHAT I AM NOT CLAIMING.** 38% is *reaches replacement over weeks 2-14*, not *beats LaPorta*, and
doc 305 3.1 already caught me treating a season outcome as a claim decision. On the frozen board
Juwan Johnson is still 8.4 VOR ahead of Schultz; what the board cannot see is that Johnson is 1 of
3 on week-1 workload and is 51.6% rostered against Schultz's 19.7%. **These are two different
objects and the honest statement is that they are close and the workload is the input we did not
have before tonight.** One week is one week.

---

## 6. SHIPPED, AND WHAT IS STILL OPEN

**SHIPPED:** `Scripts\research\wk1\build_form.py` writes **`Source\form_2026.csv`** -- 2,236 rows,
one per player per completed week plus a cumulative week-0 row: `snap_pct, targets, carries,
tgt_share, car_share, touches, half_ppr`. It FAILS rather than exits 0 when a feed is missing or the
snap join breaks (0.2, doc 146), and reports the 24 skill rows with no snap line rather than
defaulting them (doc 251). Stdlib only, paths off `__file__`, 3.12-clean (0.4, doc 144).

**NOT YET RUN, and it is the whole point: nothing reads `form_2026.csv` yet.** The next batch is
three edits -- `wire.py` joins it and emits a `form` column; `sheet_engine.py` opens a third bet
lane on 2-of-3; and a control that refuses to render a page whose newest form week is behind the
newest wire. **Until that lands the page is still blind and the table in 4 is the workaround.**

**NOT YET RUN:** the RB version of the composite on the full 32-team slate (`week1_share.py` ran on
30 of 32). **NOT YET RUN:** whether the week-1 signal survives to week 2 and beyond, which is the
question that decides whether this is a week-2 screen or a season-long one.

**STILL OPEN from before, untouched tonight:** the wire's frozen VOR sort key · `p_opens` as one
constant on an already-open job · the four missing negative controls in `redteam_controls.py` ·
doc 305 6's analyst hit-rate test, the concentration test, and slot rate into the 4.30 composite.
