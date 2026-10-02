# 347 — THREE ROWS ON THE SEAT LIST ARE NOT SEATS, AND THE LIST MIXES TWO PRODUCTS

**2026-09-18.** Matt worked the rebuilt seat table and found four things. All four confirmed.
The table below is the page as it rendered at 03:49 today, after he ran `ff.bat`.

**THE GOOD NEWS FIRST: doc 343 LANDED.** The page now sorts by what a seat is worth to him, not by
what the job pays, and the per-man odds render (64%, 53%, 48%, 44%, and a starred 46% fallback where
there is no week-1 line). Doc 345 §4 and ledger row 105 are CLOSED by his run.

| # | be first to | behind | job | wk1 | fires | odds | exp | verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | Dylan Sampson CLE | Quinshon Judkins | 210.6 | 0% | 6.1 | 46%* | **2.8** | **not a potential play** |
| 2 | Kaelon Black SF | McCaffrey | 302.4 | 46% | 2.4 | 64% | 1.5 | **ROSTERED by DUCK** |
| 3 | Ty Johnson BUF | Cook | 262.3 | — | 2.4 | 46%* | 1.1 | free, no line |
| 4 | Ollie Gordon II MIA | Achane | 261.2 | — | 2.4 | 46%* | 1.1 | free, no line |
| 5 | Tank Bigsby PHI | Barkley | 251.6 | 5% | 2.4 | 48% | 1.1 | free |
| 6 | Emari Demercado **KC** | K. Walker III | 248.9 | 10% | 2.4 | 48% | 1.1 | **WRONG TEAM** |
| 7 | Samaje Perine CIN | Chase Brown | 239.4 | 27% | 2.4 | 44% | 1.1 | free |
| 8 | Chris Brooks GB | Josh Jacobs | 241.0 | 36% | 1.9 | 53% | 1.0 | **Matt already owns him** |
| 9 | DJ Giddens IND | J. Taylor | 291.0 | — | 2.0 | 46%* | 0.9 | **stale, see §3** |
| 10 | Jaydon Blue DAL | Javonte Williams | 241.0 | — | 2.0 | 46%* | 0.9 | free, no line |
| 11 | Brian Robinson Jr ATL | Bijan | 314.8 | 22% | 1.9 | 44% | 0.8 | free |

---

## 1. THE LIST FILTERS ON ESPN OWNERSHIP AND NOT ON THIS LEAGUE'S ROSTERS

The section's own preamble says *"because these men have never been rostered, there is no waiver run
to wait for and the first person to click gets him."* **Two of eleven rows are rostered in his
league: Kaelon Black (DUCK) and Chris Brooks (JUG, his own).** `LEAGUE_ROSTERS.csv` is written by
the same run that builds the page, so the join exists and is simply not made. **DEFECT. The seat
list must exclude every man on a league roster, and say so when it drops one.**

## 2. IT MIXES A HANDCUFF WITH AN UPSIDE SEAT AND SORTS THEM TOGETHER

**Sampson's 6.1 is the largest number on the page and it is not upside.** Judkins is MATT'S OWN
starter, so that seat is priced against the bar he would have WITHOUT Judkins: it is the size of the
hole, not a forecast of Sampson. Cleveland's job is the SMALLEST on the table at 210.6. **And
Sampson's week-1 share is 0.000, a population doc 343 measured at 0 of 41 on reaching the RB bar.**

**Matt's objection is correct and it is a design fault, not a preference:** *"one of the worst teams
in the league and he may end up in a time share. The potential value can be found elsewhere."* A
list that answers "insure a man you start" and "buy a job you do not have" with one sort key cannot
serve either question. **The two belong in separate blocks with separate headers.** `[OPEN]`

## 3. TWO ROWS ARE FACTUALLY STALE, AND OUR OWN WEEK-1 DATA ALREADY DISAGREES WITH ONE

**(a) Emari Demercado is on DALLAS.** `WIRE_20260918.csv` has him at DAL with the flag *"moved to
DAL"*; the seat row has him at KC behind Kenneth Walker III. `inherit_2026.csv` is built off the
**7 September pull** and never re-reads team. So the row Matt singled out as attractive names the
wrong team and the wrong man ahead, and Dallas is already on the list at row 10 through Jaydon Blue.
**The two rows are the same backfield.**

**(b) DJ Giddens fell behind Seth McGowan, and we could have seen it.** Matt's source says so.
**Our own week-1 Colts rows: Jonathan Taylor 89% of snaps, 19 carries · Seth McGowan 11%, 1 target ·
DJ Giddens NO LINE AT ALL.** The usage re-rank (doc 320, controls C18 and C19) fires only on TWO
completed weeks by design, so with one week the chart order stands and the page prints Giddens.
**The design lags the depth chart by a week, and a man with zero snaps should not hold a seat while
a man with snaps sits below him.** `[OPEN]` The cheap guard is doc 304's shape: a seat holder with
no week-1 line loses the row to whoever on that team has one.

## 4. AND THE HONEST ANSWER TO "WHO IS MOST ATTRACTIVE" IS NOBODY

After removing the rostered two, the wrong-team one, the stale one and the handcuff, the free upside
seats are **Bigsby, Perine, Brian Robinson, Ty Johnson, Ollie Gordon and Jaydon Blue.**
**Every one is worth 0.8 to 1.1 expected points, and the sort between them is inside its own noise.**
The one measured discriminator, doc 343's band, does not fire on any of them: the elevated cells are
30-40 (53%) and 40+ (64%) and no free man is in either. The two cells they do sit in are 47.6% on
n=42 and 43.8% on n=32, which do not separate.

**Brian Robinson's 1.9 against the others' 2.4 is about MATT'S ROSTER, not about Robinson.** He is
priced against a bar that is already deep at back. He was top of the list before only because the
old sort was by job worth and Bijan's 314.8 is the biggest job on the board. Matt's read that he
does not catch passes is right and is a second reason, not the reason the number moved.

**SO THE RECOMMENDATION IS TO LEAVE THE SEAT LANE ALONE THIS WEEK** and take potential value where
this project has actually measured it: **§4.30's receiver screen, 39.4% against an 11.4% base rate,
p=0.0000.** Free and clearing 3 of 3 today: **Pat Bryant (DEN, 4.6% rostered, 59% of snaps and a
22.2% target share in week 1)**, plus Jalen McMillan (TB, 28.1%) and Ricky Pearsall (SF, 2.6%), and
Omar Cooper Jr (NYJ) on the first-round-rookie cliff (§4.28, 60% on n=15).
**A 39% screen against a 1.1-point seat is not a close call.** It is a screen and not a forecast
(§4.13d); Bryant's week 1 was 6.2 half-PPR, which is not startable.

## 5. WEEK 2 HAS STARTED AND I SAID IT HAD NOT

`form_2026.csv`, rebuilt by Matt at 04:52 today, holds **72 week-2 rows, all BUF and DET, all
flagged `in_progress=1`**. Thursday night was Buffalo at Detroit. **My "neither has anyone" was
wrong**, and it is the third calendar assertion I have made from inference in one night. Ledger row
102 already carries the first two. `load_form` correctly ignores in-progress weeks, so the sheet is
not wrong, only I was.

**AND THE RUN ORDER MATTERS: he ran `ff.bat` at 03:49 and `build_form.py` at 04:52**, so the sheet
was built against the older form file. It changes nothing today, because every week-2 row is
in-progress and the sheet only reads completed weeks. **Re-run `ff.bat` after Monday night, not now.**

## 6. OPEN

- Exclude league-rostered men from the seat list. `[OPEN]`
- Split the seat list into handcuff and open-seat blocks. `[OPEN]`
- Re-read team and the man ahead from the current wire, not the 7 Sept pull. `[OPEN]`
- A seat holder with no week-1 line should lose the row to a teammate who has one. `[OPEN]`
- The already-open-job repricing from doc 346 §3. `[NOT YET RUN]`
