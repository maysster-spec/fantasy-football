# 313 - The seat he already said yes to, and two numbers the ledger killed

*Tuesday read, 15 September 2026, 8:05am ET. Week 1 is the only week on file.*
*Population note (0.6): every usage figure below is ONE GAME. nflverse `snap_counts_2026.csv`,
`roster_weekly_2026.csv`, `stats_player_week_2026.csv` and `draft_picks.csv`, downloaded 15 Sept
12:11 UTC; latest week in each is **week 1**. Free = in `WIRE_20260915.csv` or
`FREE_UNRANKED_20260915.csv` and not on `MY_ROSTER.csv`.*

---

## 1. THE RUN IS CLEAN

`ff_log.txt`, block `======== TUE ==== Tue 09/15/2026 6:00:01.26`, ends
`RESULT: TUE -- lineup exit 0, wire exit 0`. `PAGE OK` on all three of LINEUP_CHECK.html,
THE_WEEKLY_WIRE.html and WEEK_SHEET.html. No `*** NO ... ON DISK`, no `NOT written`, no
`LOAD PROBLEM`. `FREE_UNRANKED_20260915.csv` written, 70 rows.

**One thing the log does not contain.** `WEEK_SHEET.html`, `MY_ROSTER.csv`, `WIRE_20260915.csv`
and `FREE_UNRANKED_20260915.csv` all carry mtime **11:29:47Z (7:29am ET)**, an hour and a half
after the 6:00 run, and `ff_log.txt` has no block at that time. That is Matt's hand-run of
`py wire.py` from the to-do, and it is the build that matters: it is the one carrying the week-1
snap columns. Audit ledger row 51 is exactly this hole - nothing in the sequence records that an
artifact moved - and here it cost nothing, but the log and the pages disagreed about what happened
and only the mtimes said so.

## 2. THE POOL BARELY MOVED, WHICH IS CORRECT FOR TODAY

280 rows on the wire, **0 new and 0 gone since 14 Sept**. Ten names entered across the whole week
(0908 → 0915), the live ones being **Juwan Johnson** (TE, NO, 51.6% owned), **Tyjae Spears**
(RB, TEN, 55.5%) and **Chris Rodriguez Jr.** (RB, JAX, 30.6%). `FREE_UNRANKED` moved by one row:
Jarquez Hunter in, one out. This is a league before its first waiver run, not a quiet league.

## 3. TWO NUMBERS THE AUDIT LEDGER HAS KILLED SINCE THIS PROMPT WAS WRITTEN

Both are carried by the Tuesday read's own text, and the ledger says so in terms.

**(a) Ledger row 29, OPEN - the second-back band.** The prompt's "7% / 11% / 39% / **50%**,
base rate 24%, n=143, p=0.0003" is **retracted**. The published top band held 14 already-rostered
men in 28 rows. On the CLAIMABLE population the five-season table is **5 / 7 / 37 / 64%, n=114,
+36 points, p=0.0008** - and the decomposition matters more than the headline: **if the job never
changes hands the top band is 27% and not separated (p=0.256).** The share says WHICH seat; the
job-opens term says WHETHER it opens; **the price multiplies them and must never substitute one
for the other.** Doc 303. Do not quote 50%, do not quote 24%, do not quote n=143.

**(b) Ledger row 27, OPEN - the Denver arrival squeeze.** "A veteran arrival squeezes the 3rd and
4th receivers, −0.044, p=0.005, and Denver 2026 is that cell" is **denominator dilution**: doc 299
left the arrival in this season's denominator. Over the holdover pool, same men both sides,
2021-2025, 54 arrivals against 73 controls, the 3rd+4th effect is **−0.008, p=0.158 - gone.**
The prompt's instruction to leave the screen and the squeeze "both standing" on Pat Bryant is
therefore stale: **the caution comes off Bryant** (his own slot is −0.001, p=0.32) and a WATCH
line, not a finding, goes on **Troy Franklin**. What survives is the 2nd receiver at −0.031,
p=0.078, `[SUGGESTIVE]`.

**(c) And the drop-cost box was not rebuilt.** Ledger row 25 is OPEN. `WEEK_SHEET.html` still
prints `T.J. Hockenson … 0.0` in the cost table, with the correction only in prose. Use doc 297's
measured figures: **Washington −0.98 · Browns D/ST 1.48 · Shough 3.05 · Hockenson 3.73 ·
Worthy 4.86**, and Washington's −0.98 is itself superseded by his handcuff price, **+3.84 at the
relief rate or +10.02 at the job**.

## 4. THE USAGE LANE (2b) - 37 free men reached the starter snap line in week 1

Week 1 is the only week on file, so there is **no "average before"** for anybody, and the context
rates (snaps-and-points 26%, snaps alone 16%) were measured **from week 3 on**. A week-1 flag sits
outside that window. Snaps and points first, then rotation men at the line, backs weighted above
receivers.

| player | pos | team | snaps wk1 | half-PPR (bar) | NFL round | owned |
|---|---|---|---|---|---|---|
| Devaughn Vele | WR | NO | 91% (82) | **16.40** (9.62) | rd7 2024, pick 235 | 12.9% |
| Dontayvion Wicks | WR | PHI | 91% (50) | **14.30** | rd5 2023, pick 159 | 10.1% |
| Pat Freiermuth | TE | PIT | 73% (49) | **13.10** (8.25) | rd2 2021, pick 55 | 14.6% |
| Juwan Johnson | TE | NO | 84% (76) | **12.90** | undrafted | 51.6% |
| Evan Engram | TE | DEN | 63% (32) | **12.30** | rd1 2017, pick 23 | 3.0% |
| Caleb Douglas | WR | MIA | 91% (51) | **11.90** | rd3 2026, pick 75 | 15.5% |
| Kendrick Bourne | WR | ARI | 67% (50) | **11.50** | undrafted | 0.1% |
| Brenton Strange | TE | JAX | 68% (39) | **9.30** | rd2 2023, pick 61 | 22.6% |
| Tyjae Spears | RB | TEN | 50% (25) | 3.40 (9.92) | rd3 2023, pick 81 | 55.5% |
| Chris Brooks | RB | GB | 56% (38) | 2.90 | undrafted | 11.5% |
| Malik Washington | WR | MIA | 98% (55) | 4.80 | rd6 2024, pick 184 | 7.7% |
| Dalton Schultz | TE | HOU | 66% (52) | 5.50 | rd4 2018, pick 137 | 19.7% |

Spears is the only back at the line who is genuinely free and genuinely in a job: 17 pass routes to
Tony Pollard's 8 (Lindy's, 14 Sept), 43.8% of Tennessee's backfield work, and he carries the wire's
own `back signals 3 of 3` tag.

## 5. THE ROTATION BAND (2c) - before week 4, so outside the measured window

Fourteen free men carry all three late-pick signals. Named because the prompt asks, **not** because
three-of-three means anything in week 1: the 36%-against-8.5% context was measured from week 4.

Backs first: **Kaelon Black** (SF, 43% of snaps, 0.268 points a snap, 0% special teams, behind
McCaffrey, rd3 2026 pick 90) · **Devin Singletary** (NYG, 36%, 0.472, 11.8 half-PPR, behind
Skattebo) · **Kendre Miller** (NO, 29%, 0.346, 9.0, behind Etienne). Then Kalif Raymond (CHI, 12.4),
Demarcus Robinson (SF, 12.0), Noah Fant (NO, 11.3), Cole Kmet (CHI, 10.5), Jack Bech (LV, 9.8),
David Njoku (LAC, 8.3), Elic Ayomanor (TEN, 7.6), Eli Raridon (NE, 6.7), Jonnu Smith (GB, 6.0),
Adam Trautman (DEN, 2.0), Foster Moreau (HOU, 2.5).

**The return case (doc 294) does not exist yet.** No lead back has missed a game, so no back has
come back from one. It reopens the first week a starter returns.

## 6. THE SHARE BEHIND A HEALTHY STARTER (2c2) - one game, and read section 3(a) first

Second back's share of his team's RB carries + targets, week 1, teams at 30%+:

| team | second back | share | lead back | free? |
|---|---|---|---|---|
| DEN | RJ Harvey | 46.7% (7 of 15) | J.K. Dobbins | rostered |
| **SF** | **Kaelon Black** | **45.5% (15 of 33)** | Christian McCaffrey | **FREE, 15.4%** |
| PIT | Rico Dowdle | 44.8% | Jaylen Warren | Matt's |
| MIN | Aaron Jones | 44.8% | Jordan Mason | rostered |
| ARI | Jeremiyah Love | 44.1% | Tyler Allgeier | rostered |
| **TEN** | **Tyjae Spears** | **43.8% (7 of 16)** | Tony Pollard | **FREE, 55.5%** |
| CHI | Kyle Monangai | 38.7% | D'Andre Swift | rostered |
| **GB** | **Chris Brooks** | **36.4% (8 of 22)** | MarShawn Lloyd | **FREE, 11.5%** |
| **SEA** | **George Holani** | **36.0% (9 of 25)** | Jadarian Price | **FREE, 4.2%** |
| LA | Blake Corum | 33.3% | Kyren Williams | rostered |
| NYG | Devin Singletary | 32.3% | Cam Skattebo | free, 0.3% |

**Four free backs at 35% or more: Black 45.5%, Spears 43.8%, Brooks 36.4%, Holani 36.0%.**

Three caveats, and they are not decoration. **(i)** One game is one game. **(ii)** The band rate is
64% on the claimable pool and only through a takeover - with the job intact the top band is 27%
and not separated. **(iii)** The man is the second back *by the work he got*, so the coach's choice
sits inside the predictor, and the top of the measured list holds Carlos Hyde at 3.3 a game beside
Jahmyr Gibbs. **(iv)** Green Bay and Seattle are not clean cells at all: GB's nominal starter is on
the Commissioner's Exempt List and SEA's is out, so their "lead back" is already a fill-in.

## 7. THE CLEAR PATH - share of the team's BACKUP running-back snaps, week 1

| man | team | backup snaps | share | behind |
|---|---|---|---|---|
| Brian Robinson Jr. | ATL | 15 of 15 | **100%** | Bijan Robinson (job 315) |
| Kaelon Black | SF | 28 of 28 | **100%** | Christian McCaffrey (job 302) |
| Tyjae Spears | TEN | 25 of 25 | **100%** | Tony Pollard (job 171) |
| Keaton Mitchell | LAC | 17 of 21 | 81% | Omarion Hampton (job 236) |
| **Mike Washington Jr.** | **LV** | **13 of 23** | **56.5%** | **Ashton Jeanty - Matt's** |
| Tank Bigsby | PHI | 6 of 16 | 37.5% | Saquon Barkley (job 252) |
| Tyrone Tracy Jr. | NYG | 2 of 27 | 7.4% | Cam Skattebo (job 205) |
| Ty Johnson · Ollie Gordon II · Emari Demercado · Jaydon Blue · DJ Giddens · Dylan Sampson | BUF MIA KC DAL IND CLE | 0 | **0%** | - |

**Washington's 56.5% understates him and the doc-296 reading fixes it.** The other ten Las Vegas
backup snaps are Dylan Laube's, and Laube took **zero carries on 77% special teams**. Washington took
**all seven backup carries** (41 yards, 5.9 a carry). On snaps he is under the 70% line where the
first-game rate falls to 29%; on carries he is at 100%. One game, and I would not carry either
number far.

**And six of the page's own seat rows have no path at all.** Ty Johnson, Ollie Gordon II, Emari
Demercado, Jaydon Blue, DJ Giddens and Dylan Sampson took **zero offensive snaps** in week 1. The
seat list ranks by what the job pays and by nothing else, by design - but a seat behind a job the
man is not dressed for is a name, not a path. That is doc 296 applied to the page that doc 296 was
written about.

## 8. A REAL GAP IN THE FORM FILE, AND IT DOES NOT MOVE A ROW

131 of 280 wire rows carry an empty `snap_pct`. Two whole teams are empty - **DEN, 8 of 8, and KC,
8 of 8** - and those are the two clubs in Monday night's game. Their target and target-share
columns ARE populated, so `form_2026.csv` was built after nflverse posted Monday's box scores and
before it posted Monday's snap counts. nflverse has them now (my 12:11 UTC pull carries Pat Bryant
at 59%, Troy Franklin 33%, Marvin Mims 18%).

**Recomputed by hand, it changes nothing.** Every free DEN and KC pass-catcher scores 0 or 1 of the
three workload marks with the real snaps attached; the best is Pat Bryant at 1 of 3 (59% of snaps,
6 targets, 22.2% of the team's targets). So the gap is genuine and it costs a row's *display*, not
the ranking. It heals on the next `build_form.py`.

**The one thing it hides is worth a line anyway:** Bryant **led Denver in targets** with six, ahead
of Sutton's five and Waddle's three, on 59% of the snaps, at 1.9% rostered.

## 9. WHAT THE NEWS CHANGED ON HIS FIFTEEN

Every source dated (B7). Nobody on the roster is on the week-2 injury report [FantasyPros, 14 Sept].

- **Puka Nacua** - played, 5 of 9 for 74 yards. **No discipline issued**; the personal-conduct
  review is still open, the civil trial is set for **27 March 2028**, no criminal charges.
  [therams.com, 10 Sept; FantasyFootballCalculator, 10 Sept; trial date Fox/OutKick, 2 Sept]
- **Sam LaPorta** - cleared, off the 9 Sept injury report, played, 5 of 8 for 48. **Start him**;
  our own pull still says QUESTIONABLE because it is dated 7 Sept. [Heavy, 10 Sept; FantasyPros, 14 Sept]
- **J.K. Dobbins** - the one that got worse. 8 carries, 36 yards, **0 targets**, 19-22 snaps against
  **RJ Harvey's 25-26 and 14 routes to Dobbins' 5**. A runner/receiver split with Dobbins on early
  downs. **No Sean Payton quote published since 8 Sept** - this is one game of snaps, not a coach
  statement. [RotoWire box score breakdown, 15 Sept]
- **Rico Dowdle** - out-snapped Jaylen Warren **39 to 25** and lost the production badly, 8 carries
  for 15 yards. Role up, output down. No McCarthy comment since 8 Sept. [NBC Sports, 13 Sept;
  Steelers Depot snap counts, 15 Sept]
- **Xavier Worthy** - the good kind of bad game. 3 of 6 for 18 yards, but **52 snaps (78%) and 28
  routes (88%)**, level with Rashee Rice. Mahomes threw five completions to receivers all night.
  [FantasyFootballCalculator, 12 Sept; RotoWire, 15 Sept]
- **George Pickens** - he is a **Dallas Cowboy** in 2026. 3 of 6 for 28, **17.6% target share,
  second on the team behind Lamb**. Role intact, production poor. [FantasyPros, 14 Sept; DraftSharks, 14 Sept]
- **Ashton Jeanty** - 23 carries, 102 yards, 6 of 6 for 45 and **two receiving TDs**. Ankle cleared.
  [FantasyFootballCalculator, 13 Sept]
- **Quinshon Judkins** - lead back, 65% of snaps, but 12 for 33. Late-August knock resolved.
  [FantasyFootballCalculator, 13 Sept]
- **Jalen Hurts** - healthy, 203 and 3 TDs plus 48 rushing. [NBC Sports Philadelphia, 14 Sept]
- **Davante Adams** - 3 of 6 for 26, no injury, no role change. [NBC Sports, 10 Sept]
- **T.J. Hockenson** - played, 4 of 5 for 36 and a TD, no designation. [FantasyPros, 14 Sept]
- **Tyler Shough** - confirmed the starter; 35 of 56, 410 yards, 3 TD, 2 INT. [FantasyPros, 14 Sept]
- **Browns D/ST** - beaten 34-10 by Jacksonville, one sack, no takeaways. Nothing to do: he is
  holding it for the weeks 2-5 run (TB CAR PIT NYJ), which is a schedule argument and week 1 was
  not in it. [Athlon, 14 Sept]
- **Eddy Pineiro** - San Francisco, 2 of 3 FG, no injury. [FantasyPros, 14 Sept]
- **Mike Washington Jr.** - 7 carries, 41 yards, active. No snap figure in any dated source; the
  19% above is nflverse. [FantasyPros, 14 Sept]

**One data note, not a move:** `MY_ROSTER.csv` carries no `value` and no `bye` for Pickens, so his
row is unpriced in that file. The week sheet's bar table *does* know his week-14 bye (the WR bar
drops to 10.2 there), so the gap is in the roster CSV's join and not in the page's arithmetic.

## 10. WHAT THE CANDIDATES' NEWS SAYS

- **Kaelon Black** - 14 carries for 65 yards, **outcarried McCaffrey 14 to 10**, 43.1% of snaps.
  Jordan James was inactive with a rib fracture, so Black is the only backup. **Shanahan's only
  word is that McCaffrey "played through cramps"** - a managed workload, not a designation, and
  **no coach has said anything about how the split goes from here.** [Lindy's, 14 Sept; NBC Sports
  player news, 11 Sept; SI/Onsi, 11 Sept]
- **Dalton Schultz** - 8 targets, second on Houston behind Nico Collins' 10. **His volume is
  structural: Jayden Higgins tore an ACL in the summer and is out for the season.** That also
  closes the prompt's FREE_UNRANKED watch item on Higgins - he is not a claim and not a watch this
  year. [Lindy's, 14 Sept]
- **Devaughn Vele** - 7 of 9 for 69 and a TD on 90%+ of snaps, second-most-targeted Saint behind
  Olave. Top-listed week-2 add. [Lindy's, 14 Sept; Heavy, 14 Sept]
- **Malik Washington (55 of 56 snaps) and Caleb Douglas (51 of 56)** - **not injury, roster
  turnover.** Tyreek Hill and Jaylen Waddle are off Miami, Atwell traded, Reagor released; Hafley:
  "we believe those guys deserve to start". Their snap share is durable, which is the part that
  matters. [ProFootballRumors, 13 Sept; SI/Onsi via Yahoo, 14 Sept]
- **Tyjae Spears** - quiet box score, **17 routes to Pollard's 8**. **No dated report that Pollard
  is hurt**; the widely-quoted "roughly equal split" line traces to CBS Sports, **6 September 2024**
  - stale, do not use it. [Lindy's, 14 Sept; FantasyFootballCalculator, 12 Sept]
- **Green Bay** - a committee, not a lead back. Brooks 38 snaps and 7 carries, Lloyd 30 snaps and
  **13 carries**, Kaleb Johnson 0. No coach quote naming one. [Acme Packing Company via Yahoo, 14 Sept]
- **Pat Freiermuth** - 5 of 5 for 46 and a TD. [FantasyPros, 14 Sept]
- **Juwan Johnson** - 54 yards and a TD; targets and snap share not in any dated source, the 7 and
  84% above are nflverse. [Yahoo, 13-14 Sept]

## 11. THE ORDER, AND WHERE I DISAGREE WITH THE PAGE

The page's section 0 reads Schultz 11.1 · Malik Washington 3.7 · Vele 3.3 · Douglas 3.3 ·
Raymond 3.3. **Among the pass-catchers that order is right and I would not touch it.** Schultz
leads because the tight-end bar is 8.8 against a receiver's 11.7 and week 6 is an empty slot, and
because his eight targets have a structural cause. Vele had the best line on the wire and prices
third because a 12.7-a-game receiver clears a 11.7 bar by a point. That is the arithmetic working,
not failing.

**Where I depart is that the page has no running back on the list at all, and the best thing in the
pool this morning is a backfield seat.** Kaelon Black prices at 1.1 because the seat model charges
**every** seat the same 46% job-opens rate and multiplies it by a small in-lineup gain. It cannot
see the share, by construction, and the share is the whole of what changed on Sunday: 45.5% of the
work and 100% of the backup snaps while the starter was on the field. I have not recomputed his
seat price and I am not going to invent one - but the input the page uses is an average and Black
is not an average seat, so **1.1 is a floor and not an estimate.** Where 2c2 and the page disagree,
I follow 2c2 here.

**The two do not compete, and that is the cleanest part of it.** Black costs Tyler Shough at 3.05;
Schultz costs Hockenson at 3.73. Different seats.

**Shough is the right seat to spend and the reason is measured:** doc 259 put Daniel Jones at 21.87
a game against Shough's 21.92 - five hundredths - and Jones is free at 34.9% owned. §4.16's table
says quarterback is the position this wire *can* replace, at a 62% hit rate, the best of any
position, while a back is 22%. Draft the position waivers will not save you at; drop the one they
will. The cost of the seat is the week-10 Hurts bye, and the to-do already carries a week-9 QB add
for it.

**Black as the sixth back is the one honest objection, and doc 240 answers it.** Spears never
entered the lineup in fourteen weeks because his job paid 171 and Pollard had missed one game in
two years. The rule that came out of it is that a bench back earns his spot by the **job he would
inherit and the fragility of the man ahead**, never by his own line. Black's job pays 302, the
second largest on the free board, and he already holds 45% of it. That is the Mike Washington side
of doc 240's comparison, not the Spears side.

## 12. OPEN THREADS THIS READ LEAVES

- Ledger rows 25, 27 and 29 all still say **NO** against the page, and rows 27 and 29 say **NO**
  against the directive too. The Tuesday read's own prompt text carries row 29's retracted band.
- `form_2026.csv` is a Monday-night snap short for DEN and KC. Heals on the next build.
- Row 51's hole showed itself today: the 6:00 log and the 7:29 pages disagreed and only the mtimes
  said so.
- The doc-294 return lane cannot open until a lead back misses and comes back.
- `py check_kit.py` has not been run since this morning's hand-built wire.
