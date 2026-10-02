# 304 -- week one landed, and the page led with a man who did not play

**Sunday 13 September 2026, 9:45pm ET.** Matt, tonight: *"Jalen McMillan is still listed as the top
pickup on the WEEK_SHEET.html."* He is right, it is a real defect, and it is fixed below.

**POPULATION WARNING, and it governs every number here (0.6): nflverse's 2026 file holds 693 rows
across 20 TEAMS -- the Thursday opener and the 1pm window only.** The late slate, Sunday night and
Monday are not in it. **Not yet scored: ARI DAL DEN GB KC LV MIA MIN NYG PHI LAC WAS.** That is
eight of Matt's fifteen, including Jeanty, Hurts, Worthy, Dobbins, Hockenson and Washington.
**Nothing here is a final read on the week. Re-run when the file carries 32 teams.**

---

## 1. THE DEFECT HE CAUGHT

The page rendered, in order: **1. Jalen McMillan, WR TB, "Out", 2.9 expected · 2. Pat Bryant, WR
DEN, 2.9 · 3. Kaelon Black, RB SF, 1.1.**

`sheet_engine.py` already KNEW. There is a sentence under the call for exactly this case: *"ESPN has
him Out. Let the week start before you spend the drop on him."* **The status was read, printed, and
never used to order anything.** So the page recommended a man who could not play and then explained
underneath why he could not play.

**That is doc 296's rule on a different list.** Doc 296 fixed `next_man_up()` so the man who
inherits a backfield must be PLAYING. The pickup list was never given the same rule. And it is
0.1(f): a recommendation, not a menu with a footnote.

**FIXED:** `moves.sort()` now keys on `GONE_FOR_WEEKS` membership first, so a man ESPN lists OUT,
on IR, suspended, on PUP or NOT_ACTIVE is demoted below every man who can play. He is not deleted --
he stays visible, because a stash is a real lane -- he simply cannot be rank 1.
**QUESTIONABLE is deliberately NOT in that set:** a questionable man may play and keeps his rank.
**NEGATIVE CONTROL RUN FIRST, on the live ordering:** the old key returns McMillan / Bryant / Black
and the new key returns Bryant / Black / McMillan, and on a slate where nobody is out the two keys
agree exactly. `[TESTED]` It is not yet in `redteam_controls.py`; that file needs Matt's tree and
goes in the batch doc 303 section 8 already names.

**AND THE SECOND HALF OF HIS COMPLAINT IS THE ONE THAT MATTERS MORE.** Even with McMillan demoted,
**Black ranks third, behind two receivers, because his seat is priced off the generic 46% job-opens
figure and the page cannot see that he took 45% of San Francisco's backfield work.** That is
`AUDIT_LEDGER` row 29, still OPEN, and it is now costing a live recommendation rather than a
hypothetical one.

---

## 2. WHAT WEEK ONE ACTUALLY SAYS, SCORED UNDER SECTION 2

**His roster, the seven already scored** (half-PPR, 6-pt passing TD, his rules, computed here):

| player | pos | pts | work | startable? |
|---|---|---|---|---|
| **Tyler Shough** | QB NO | **29.2** | 4 | yes |
| Puka Nacua | WR LA | 9.9 | 9 | yes |
| Sam LaPorta | TE DET | 7.3 | 8 | no |
| Quinshon Judkins | RB CLE | 6.0 | 14 | no |
| Davante Adams | WR LA | 4.1 | 6 | no |
| Rico Dowdle | RB PIT | 3.1 | 13 | no |
| Eddy Pineiro | K SF | 0.0 | 0 | -- |

**The QB2 he wants to drop had the best game on the roster.** Reported first because it cuts against
the recommendation, not after it.

**TWO SHARES ON HIS OWN ROSTER, and they are the doc 300 instrument pointed inward:**
**Judkins took 78% of Cleveland's backfield work** (Sampson 0, and QUESTIONABLE). **Dowdle took 45%
of Pittsburgh's**, behind Jaylen Warren at 55%. **Dowdle is in doc 303's top band on a man Matt
already owns.** On the claimable population that band is 64% startable. That is an argument to hold
Dowdle through a bad box score, not to add anybody.

---

## 3. THE FREE POOL, HIS LEAGUE, NOT THE NATIONAL SHEET

Every free player who played in the early slate, scored under section 2 and joined to
`WIRE_20260913.csv`. **Ownership is his league's.**

| player | pos | pts | work | share | owned | note |
|---|---|---|---|---|---|---|
| C.J. Stroud | QB HOU | 20.5 | -- | -- | 25.8% | startable |
| **Devaughn Vele** | **WR NO** | **16.4** | 9 | **17% of team targets** | **12.9%** | Olave hurt |
| **Mike Gesicki** | **TE CIN** | **16.3** | 7 | 21% | **1.5%** | |
| Pat Freiermuth | TE PIT | 13.1 | 5 | 14% | 14.6% | |
| Juwan Johnson | TE NO | 12.9 | 7 | 13% | 51.9% | |
| Kalif Raymond | WR CHI | 12.4 | 9 | **35%** | 0.2% | |
| Demarcus Robinson | WR SF | 12.0 | 3 | 9% | 0.1% | |
| Noah Fant | TE NO | 11.3 | 8 | 15% | 0.1% | |
| Kendre Miller | RB NO | 9.0 | 9 | 29% | 0.9% | |
| **Kaelon Black** | **RB SF** | **7.5** | **15** | **45% of the backfield** | **15.4%** | |

**THE NATIONAL SHEETS' TOP NAME IS ALREADY GONE HERE.** Both outlets read tonight led with **Jalen
Coker (WR CAR, 29.8 pts)**; he is **rostered in this league**, as are Bryce Young (37.4), Raheim
Sanders and Kenyon Sadiq. **Reading the national wire without joining it to his own pool produces a
list of men he cannot have** -- doc 292's lesson in a new place.

**OUTSIDE, DATED (B7).** Two usable, both **13 September 2026**: Yahoo Sports (*"Jalen Coker, Kaelon
Black lead players to add"*) and DK Network. Yahoo on Black: *"The rookie outcarried the vet 14-10
... it's very clear Shanahan trusts Black to take some heat off CMC."* **Their 14-10 matches the
number computed here independently from nflverse, which is the corroboration that matters.**
**REJECTED AS STALE:** SI's *"Dylan Sampson and 3 more week 2 waiver wire running backs"* is dated
**9 September 2025** and names a 2025 slate. It reads as current and is a year old.

---

## 4. MATT'S MONANGAI CLAIM, TESTED

His words: *"Kyle Monangai turned out to be better than the model expected even when i argued
otherwise. I'd rather have him than swift."*

**Testable form: on week 1, did Monangai out-score Swift, and did he beat what his price implied?**
Two different questions and they split.

| | work | share of CHI backfield | pts |
|---|---|---|---|
| D'Andre Swift | 19 | **61%** | **31.9** |
| Kyle Monangai | 12 | 39% | **19.4** |

**HE IS HALF RIGHT, AND THE HALF HE IS RIGHT ABOUT IS THE ONE THAT GENERALISES.** Monangai at 19.4
cleared the 9.92 bar comfortably on a projection that had him as a backup, so **the claim "the model
under-rated him" is supported.** The claim "I'd rather have him than Swift" is **not** supported on
this week: Swift took 61% of the work and outscored him by 12.5. It is a real committee, not a
takeover, and on one game neither reading is resolved.
**Both are rostered in his league, so nothing here is claimable.** The value of the answer is to the
BOARD, not to a waiver: a back projected as a backup who takes 39% of a real backfield is exactly
the row doc 300's share table was built to find, and the board had no column for it.

---

## 5. OPEN

* **NOT YET RUN, and it is the first thing tomorrow:** every table here on the full 32-team slate.
  `stats_player_week_2026.csv` is committed to `Scripts\research\wk1\` and will be re-pulled.
* **[OPEN]** `AUDIT_LEDGER` row 29: the seat price still cannot see the weekly share, and tonight it
  put the measured name third.
* **NOT YET RUN:** the ordering fix has a control that was run by hand here and is not yet in
  `redteam_controls.py`. It joins doc 303 section 8's batch.
* **[OPEN]** doc 301's Kaleb Johnson question: the wire still lists him PIT.
