# 343 -- the odds were the same for everyone, and the weeks I tried to change failed their own test

**17 September 2026, 21:30 ET.** Matt has asked three times for the seat lane to be joined to the
top of the page. **It already was** -- `sheet_engine.py` has folded every seat move into the same
ranked list as the screens since doc 295. **What he was actually seeing is that no seat ever gets
there**, and the page said why in its own words: *"Every seat is priced at that one rate, so the
ordering below is the job and nothing else."* This fixes that sentence. It does not make the lane
big.

---

## 1. THE ANSWER FIRST

1. **Every seat now carries its own odds**, from that back's share of his backfield in week one:
   **0.48 / 0.44 / 0.53 / 0.64** across the four bands, on 126 team-seasons. The flat **0.46** was
   the population average and is why the table could only rank the size of the job.
2. **The seat table is ordered by what it is worth**, not by what the job pays, and it prints the
   share it used. A man with no week-one line falls back to the average **and is starred**.
3. **On the live board that makes Kaelon Black the best free seat** -- 46% of San Francisco's
   week-one backfield, 64% odds, and he moves from about 1.1 to **1.5**. Chris Brooks is a band
   below him at 36%.
4. **AND IT DOES NOT PUT HIM IN THE TOP FIVE, WHICH IS THE HONEST HEADLINE.** The best screen on
   the page is **11.1** and the best seat is **2.8**. The lane is small for a reason that has
   nothing to do with the odds: a relief back scores **12.13** a game against an RB bar near ten,
   so three weeks of him is barely two points above what Matt already starts.
5. **I tried to make the lane bigger and the test killed it.** See section 3. The 3.02 weeks did
   not change.

---

## 2. WHAT SHIPPED, AND THE POPULATION IT RESTS ON (0.6)

**POPULATION -- state it every time:** every NFL team-season 2022-2025 whose week-1 RB usage
leader and second back both played in week one with combined RB work (carries + targets) of ten or
more. **n=126.**
**PREDICTOR:** the second back's share of his team's week-1 RB carries plus targets, **the leader
IN the denominator**. That is doc 300's measure. **It is NOT doc 292's T5**, which excludes the
leader and runs on snaps and is roughly double on a clean two-man room. Swapping them would put
every direct backup in the top band.
**OUTCOME:** the week-1 leader misses a game in weeks 2-14, byes excluded.

| his share of the week-1 backfield | n | P(the job opens) | startable wks 2-14 |
|---|---|---|---|
| under 20% | 42 | 0.476 | 4.8% |
| 20-30% | 32 | 0.438 | 15.6% |
| 30-40% | 30 | 0.533 | 36.7% |
| **40% or more** | **22** | **0.636** | **50.0%** |

Permutation at a 35% split, one-sided, 6,000 draws, on the **seats-only** population (below):
**P(open) +0.36, p=0.027 · startable +0.24, p=0.041.** `[TESTED, n=126]`

**TWO LIMITS, ON THE PAGE AND NOT ONLY HERE.**
- **It is an association, not a mechanism.** A room that splits the work in week one may be a room
  whose starter is already sore. That is knowable in week one and is exactly the point; it is not
  a claim that sharing carries causes injuries.
- **The seats-only top band is 1.000 on n=6 and that is NOT what shipped.** The unfiltered 0.636
  on n=22 is, because it is the larger sample and the conservative direction.

**doc 300's startable rate replicates**: 4.8 / 15.6 / 36.7 / 50.0 here against its published
7 / 11 / 39 / 50 on 2021-2025. Two populations, same shape.

---

## 3. THE CLAIM THAT DIED, AND IT WAS MINE

**Testable form, written before the run:** *if a seat is worth more than the page says, the number
of weeks the second back spends leading the room must be materially above the sheet's 3.02 in the
top band.*

**First pass: 1.24 / 1.91 / 4.20 / 6.00 weeks.** Twice the sheet's number in the top band. That
would have roughly doubled every good seat's price and it was ready to write.

**Then the object was checked, which is 0.5(a2) on my own work.** `weeks_held` counts every week
he led the room **including weeks before the starter ever missed one**. For a man at a 45% week-one
share that is largely *he was already half the backfield*, not *he inherited a job*. Those are
different events.

| counted how | <20 | 20-30 | 30-40 | 40+ | permutation |
|---|---|---|---|---|---|
| every week he led | 1.24 | 1.91 | 4.20 | 6.00 | -- |
| **only from the first absence onward** | 2.05 | 3.21 | 3.12 | **4.71** | +1.15, **p=0.081** |
| **and dropping men who already led before it** | 2.13 | 3.50 | 2.33 | **4.50** | +0.75, **p=0.286** |

**The gradient was mostly co-leadership. 3.02 stands.** `[UNDERPOWERED, NOT DISPROVED -- n=6 in
the top band.]` **Do not quote 6.00 weeks.** The constants file now carries that sentence so the
next session cannot re-find the raw number and ship it.

**And the other correction runs the same way but against me.** Adding a *"does HE get the job"*
term can only ever LOWER a seat, because it replaces an implicit 100%. What pulls the other way is
the weeks. **I told Matt those two would fight and I did not know which would win. Neither did:
one shipped, the other failed.**

---

## 4. THE LIVE BOARD

25 of the 32 rows on `inherit_2026.csv` now carry a week-one share; seven have no week-one line and
are blank, **never zero** -- a zero would price them as the bottom band, and a man with no line is
no information (section 3, doc 251). A share of **exactly zero** also falls back, because every row
the bands were fitted on had a second back who touched the ball.

| free, and what he is | share | band |
|---|---|---|
| **Kaelon Black**, behind McCaffrey | **46%** | 40+ |
| **Tyjae Spears**, behind Pollard | **44%** | 40+ |
| **Chris Brooks**, behind Jacobs | **36%** | 30-40 |

**Spears is the useful case for the frame.** He is in the top band on the share and his backfield
is the smallest job we have looked at -- Tennessee's `job_ceil` is 171, doc 240 -- so he is the man
Matt himself called negative value on a bench. **The share says which seat; the job says how big.
Neither one is the answer alone**, which is why the table multiplies them.

**FOUR OF THE SEVEN TOP-BAND MEN OUT-WORKED THE MAN THE DEPTH CHART CALLS THE STARTER** (Allgeier
56%, Mason 52%, Price 48%, Harvey 47%). The bands were fitted on second backs, so reading a
55% man off them is the top band and no further. That is doc 320's finding -- the usage order and
the depth chart disagree -- showing up in a new place.

---

## 5. CONTROLS

**17 on the odds, all run.** Each band maps to its measured number; a missing band, an unknown
band, an absent table and **a share of exactly zero** each fall back to the average **and return a
reason**, never silently; two different bands must price differently, which is the defect being
replaced; the file's blank rows are blank and not 0.0; and the three men the decision is about are
on the file **by name** with the band they should have (0.5(c)5).

**And the whole harness runs again: 44 of 44.** It had been dying on its own base control since doc
320 -- see doc 342 and `AUDIT_LEDGER` rows 85 and 86. `form_2026.csv` is now on its copy list, so
the doc-308 workload lane is exercised by a control for the first time.

---

## 6. FILES

`Scripts\sheet_engine.py` 110,676 -> 115,530 (`e951cbd7dbceae3c`) ·
`Source\sheet_constants.json` (`seat.p_opens_by_band` + the note recording section 3's death) ·
`Source\inherit_2026.csv` (`wk1_share`, `wk1_band`) ·
`Scripts\research\wk1\job_opens.py` **new** ·
`Scripts\research\redteam\redteam_controls.py` (`form_2026.csv` added to the copy list) ·
`Scripts\check_kit.py` re-pinned. Archived first; every commit verified by reading the drive copy
back. **Nothing was written to ESPN, no claim was filed, nobody was dropped.**

---

## 7. OPEN

* **NOT YET RUN, form written:** the same four bands on **2021**, which would take the top band from
  22 to about 28 and is the only thing that resolves the weeks question. `stats_player_week_2021.csv`
  is in the live `stats_player` release; the cache holds 2022-2025 only.
* **NOT YET RUN:** doc 292's T5 measure (share of NON-leader snaps) as a second, independent band
  on the same rows. If the two disagree about a man, that is worth knowing before either is trusted.
* **[OPEN]** The seat lane is small because **12.13 a game is barely above an RB bar near ten**, not
  because of the odds. Nothing here tested whether the relief rate should be per-man. Doc 292 says
  nothing measured about the backup predicted what he scored in relief, so that is the prior --
  but it was measured on first games of an absence, not on whole spells.
