# 314 — THE ROOM BUYS THE JOB, NOT THE BOX SCORE — AND THE RIVAL-NEED MODEL DIES ON ITS OWN FALSIFIER

*2026-09-15. Matt: "I think we agree no harm in trying. If a player has significant value anyway,*
*very unlikely someone doesn't put in a claim because everyone tends to have players they would*
*shed for that anyway."*

---

## 0. WHAT TO DO

1. **Do not build the rival-need model. It is dead.** Doc 254 fixed the bar before anything ran:
   a positional-hole flag had to add **0.30 expected filers** over "how popular is this man."
   It adds **+0.20**, and held out by season it makes the prediction **worse**. Thread closed.
2. **§4.32's term 4 is now a lookup, not a model, and it is IN THE SHEET.** How many rivals file
   on a man is a function of ONE number: **targets plus carries in his last completed game.**
3. **The word in his sentence was wrong and it matters.** It is not value, it is **workload**.
   Points add nothing once the touches are known.
4. **Order the claim list by who else is racing you, not by who scores most.** Only the first
   winning claim of a run comes at his real priority (doc 226), so the contested man spends it.
5. **RE-RUN `py research\wk1\build_form.py` BEFORE THE NEXT `py wire.py`.** It now writes an
   `in_progress` column and the page reads "his last game" from it.
6. **Reproduce any of this with `py research\rival_need.py`.** Standard library plus numpy.

---

## 1. THE TESTABLE FORM, WRITTEN BEFORE THE TEST (§0.5a2)

> **POPULATION:** every waiver player-week in this league 2022–2025 — one man filed on in one run,
> **787** of them, **225 contested (28.6%)**, reproducing doc 254's feasibility count exactly.
> **PREDICTOR A, his:** what the player had DONE in the weeks before the claim.
> **PREDICTOR B, the model's:** whether the filing teams had a hole at his position.
> **OUTCOME:** how many teams filed.
> **HIS DIRECTION:** A carries it and B adds nothing.

**POPULATION, RESTATED BECAUSE IT IS INHERITED (§0.6).** The analysis population is the **403**
of those 787 that are **RB, WR or TE with a prior game on file**. It **EXCLUDES D/ST (193
player-weeks) and kickers (70)** — 263 of 787, and D/ST is the most churned lane in this league.
It also excludes **19 week-1 filings**, which have no prior game to read, and 15 men who had not
yet played. **The D/ST version of this is NOT YET RUN and the input is `dst_weekly_2021_2025.csv`.**

---

## 2. HE IS RIGHT, AND THE MODEL FAILS THE BAR IT WAS GIVEN

| model | expected filers it moves | out-of-sample MAE |
|---|---|---|
| player's workload alone | — | **0.693** |
| + how active that team is | — | 0.719 |
| **+ positional need** | **+0.201** | 0.716 |

**Doc 254's bar was 0.30, fixed in writing on 2026-09-09 before any of this existed. It clears
0.20.** And leave-one-season-out it is **worse than workload alone**. `[TESTED, n=5,671
team-decisions]`

**AND THE TEST WAS RIGGED IN THE MODEL'S FAVOUR.** Doc 254 specified need as a hole computed from
a rebuilt roster plus byes plus the injury report. I used **REVEALED need** — how often that team
had filed at that position in the prior three weeks — which is measured off the *same object as
the outcome*. A team that files at receiver every week scores as needing a receiver. **That is
circular in B's favour and it still failed**, so the specified version would have to beat a rigged
one to clear the bar. **Recording the direction of the bias rather than the caveat alone: this is
the strongest form of the null available, not the weakest.**

---

## 3. BUT THE WORD IS WORKLOAD, NOT VALUE — AND THAT IS A CORRECTION TO HIM

One population, RB/WR/TE, n=403, stated once:

| | r with number of filers |
|---|---|
| **targets + carries last game** | **+0.296** |
| half-PPR points last game | +0.233 |
| touches **net of** points | **+0.231** |
| points **net of** touches | +0.137 *(the p=.05 line is 0.098)* |

Permutation p on touches = **0.00005**, N=20,000. Positive in all four seasons (+0.27 / +0.43 /
+0.11 / +0.35) and at all three positions (RB +0.29, TE +0.35, WR +0.20). `[TESTED]`

**THE SHIPPING TABLE:**

| his touches last game | teams that file | contested |
|---|---|---|
| under 5 | 1.17 | 14% |
| 5 to 9 | 1.49 | 29% |
| 10 to 14 | 1.83 | 40% |
| **15 or more** | **2.27** | **56%** |

**AND THE CELL THAT SETTLES IT:**

| | 10+ touches | under 10 touches |
|---|---|---|
| **scored 12+** | **2.03** filers | 1.62 |
| **scored under 12** | **1.90** filers | 1.29 |

**The top row and the bottom row are the same number.** Scoring well on few touches draws **fewer**
claims than scoring badly on many. **The room is buying the job.** That is §4.20's "buy the job,
never the name" showing up in the other eleven managers' behaviour rather than in our board, and
doc 235's "the pop is the workload" reached from a completely different direction.

**The names in the bottom-right of that table are the archetype:** Tyrone Tracy 13 touches for 6.3
points and 7 filers; Charbonnet 21 for 9.9 and 5; Kareem Hunt 17 for 9.5 and 5; Gainwell 18 for 9.4
and 4.

---

## 4. HIS FLOOR CLAIM IS QUALIFIED, NOT CONFIRMED — AND THIS IS THE LANE

*"Very unlikely someone doesn't put in a claim."* **True of the season, false of the week.**

**56** men had a 10+ touch game while **provably undrafted and never rostered by anyone**.
**18 of them — 32% — went at least one more full week before a single team filed.**

| | first 10+ touch game → claimed | then |
|---|---|---|
| Hassan Haskins 2022 | week 2 → week 17, **15 weeks** | 1 filer |
| Chris Rodriguez Jr. 2025 | week 3 → week 14, 11 weeks | 1 filer |
| Samaje Perine 2022 | week 3 → week 12, 9 weeks | 1 filer |
| **Isaac Guerendo 2024** | **week 6 → week 14, 8 weeks** | **7 filers at once** |
| Parker Washington 2025 | week 3 → week 11, 8 weeks | 2 filers |

**Guerendo is the whole finding in one row.** Eight weeks of a real workload sat there, and when the
room finally noticed, seven teams filed in the same run and six of them lost.

**THE BIAS, NAMED AND POINTING THE WRONG WAY FOR ME (§3):** this joins to the draft list **by
name**, because the draft history carries no ids. A man I fail to match reads as free when he was
rostered, so the honest reading is **"up to a third," not "at least a third."**

**THE OPERATIONAL CONSEQUENCE.** Doc 252 measured that a week-1 claim hits 9% and a week-2 claim
hits 35%, because one bets on a depth chart and the other on a snap count. **This says the window
does not slam shut after week 2.** The room is slow on a confirmed workload roughly a third of the
time, and that is doc 224's 56%-uncontested lane with a trigger attached to it for the first time.

---

## 5. WHAT SHIPPED

- **`Source\sheet_constants.json`** — a `contest` block: the bands, the nulls, and the reason the
  rival model is not being built. Numbers live in one place.
- **`Scripts\wire.py`** — `load_form()` now returns the **last completed game** as well as the
  cumulative row, and `touches` rides onto every free row. *In week 2 those two rows are identical,
  which is exactly how reading the season total instead would have shipped invisible and broken
  from week 3 on.*
- **`Scripts\sheet_engine.py`** — a `contest()` helper and a tag on every pickup.
- **`Scripts\research\wk1\build_form.py`** — writes `in_progress`, so "his last game" is **read**
  rather than inferred from row counts.
- **`Scripts\research\rival_need.py`** — reproduces all of the above. Stdlib + numpy (§0.4).

**WHO GETS THE SENTENCE, AND THE FIRST VERSION HAD IT BACKWARDS.** It went to the top two rows —
which tells him to put first the man who is already first. The decision it serves is **reordering**,
so the sentence now follows the **contested** man wherever he sits. Rank four is exactly where he
is easiest to lose.

**NEGATIVE CONTROLS, ALL RUN AND ALL FIRED (§0.2):** 18 touches → "put him first"; 2 touches →
"nobody is racing you"; blank, missing and non-numeric touches → **silent**, because a man with no
game log is no information and a default of zero would print *"nobody wants him"* about a man
nobody has measured; the whole `contest` block deleted from the constants → silent, page still
renders. **And the missing-row check (§0.5c5): a planted 18-touch row was verified to reach the
rendered page BY NAME, with its tag and its sentence, at rank 3.**

---

## 6. TWO DEFECTS THIS FOUND IN MY OWN WORK, BOTH BEFORE ANYTHING SHIPPED

**(a) THE YEAR CAME OUT OF THE PATH, NOT THE FILENAME.** `re.search(r'(\d{4})', f)` against
`G:\My Drive\_Fantasy\2026\Source\waiver_report_2022.csv` matched **2026**, so the `if yr == 2026:
continue` guard dropped **every row**. The same code had worked minutes earlier from inside the
directory, where the path carried no year. **Caught only by "zero is not a result."** Now
`os.path.basename`, with an assert.

**(b) READING WAIVER ROWS ONLY INFLATED §4's HEADLINE FROM 32% TO 46%.** A man added off **free
agency** in week 3 and dropped in week 6 was invisible to a waiver-only scan, so he read as
"never rostered." The contest analysis is correctly waiver-only; the sat-untouched analysis needs
**every executed transaction**. Two questions, two populations, one file — §0.6 again, inside a
single script.

---

## 7. OPEN

- **The D/ST version.** 193 excluded player-weeks, the most churned lane, and §2 now carries the
  scoring rules that used to block it. `dst_weekly_2021_2025.csv` is the input. **NOT YET RUN.**
- **The kicker version**, 70 player-weeks. Almost certainly noise, but it is 70 rows and unstated.
- **Whether the touch bands survive 2026.** Four seasons fitted, none held out into a live year.
- **The legibility test from doc 252** — of the free-and-usable pool in week W, what share is
  claimed within two weeks. §4's sit-time table is half of it and the other half is unbuilt.
- **`seat_moves_l` rows carry no touch count**, so the inheritance lane prints no contest tag.
  The game log exists; the join does not. **NOT YET RUN.**
