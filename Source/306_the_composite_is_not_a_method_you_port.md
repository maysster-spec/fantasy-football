# 306 -- the composite is not a method you port, and at running back it is two signals not three

**13 September 2026.** Matt: *"Only one stack has ever been measured here: the receiver composite.
My read is that this is a shortcoming in our projections. What can we do about this?"* And:
*"when can this come out of the queue and be run?"*

**Answer to the second one first: now. It is run and it is below.**

---

## 1. THE OBJECT IS NOT THE PROJECTIONS, AND THAT MATTERS BECAUSE THE FIX IS DIFFERENT

**Two separate things are true and only one of them is what he named.**

**(a) The projections are not the problem.** §4.23(c) already verified the board reconciles to §2
scoring at **r=0.9914, median absolute error 0.30 points**, and doc 302 confirmed the week-1 lines
independently. The projection is a decent estimate of points. It was never supposed to carry a
signal.

**(b) But he is right that something is missing, and it is one level down.** The board's `value`
column is a projection minus a replacement level, and **not one of the signals in the catalog is an
input to it.** The pedigree screen is a TAG printed beside the number, not a term inside it. So the
page cannot stack anything, because nothing is in there to stack. That is `AUDIT_LEDGER` rows 26 and
29 and it is a real shortcoming, fixable, and separate from the projection.

**(c) And the reason only one stack has been MEASURED is neither of those. It is power, plus a
method we only ever used once.** Every interaction test in this project has been a hand-specified
pair on a small cell: doc 191's were 9 and 24 rows. §4.30's composite is different in kind. It does
not estimate an interaction coefficient at all. **It counts how many of N binary signals fire and
reads the rate by count**, which needs no more data than the signals themselves. That method is
cheap, it is the one that worked, and **it had never been tried at any position but receiver.**

**So the fix is not a better projection. It is: run the count-composite at the other positions.**
Started below, at running back.

---

## 2. THE RUNNING-BACK COMPOSITE, RUN

**TESTABLE FORM, written before the run:** *the count-composite method that separated at receiver
also separates at running back, using the same three signal SHAPES: draft capital, efficiency, and
volume.*

**POPULATION, stated because it is a deliberate analogy to §4.30's: RB seasons 2021-2024, NFL years
1 to 3, who were NOT startable (under 9.92 half-PPR per game, weeks 1-14), played 4+ games, and
played 4+ games again the next season. n = 158. OUTCOME: startable the following season.
BASE RATE 15.2%** (24 of 158). Permutation, 6,000 draws, one-sided, seed fixed.
Thresholds taken at the population MEDIAN so the cut is not chosen: yards per touch 4.89, touches
per game 5.86. Script: `Scripts\research\wk1\rb_composite.py`.

### 2a. THE THREE-SIGNAL COMPOSITE DOES NOT TRANSFER

| signals | n | startable next season |
|---|---|---|
| 0 of 3 | 30 | 6.7% |
| 1 of 3 | 70 | 11.4% |
| 2 of 3 | 48 | 22.9% |
| **3 of 3** | **10** | **30.0%** |

**3 of 3 against under 3: +15.8 points, p=0.1823.** `[TESTED, null]` And it fails the cut-point
check that doc 302 taught: swept from the 35th to the 65th percentile the p runs **0.041, 0.069,
0.114, 0.170, 0.405, 0.343, 0.283**. That is a result that depends on where you cut, which means it
is not a result.

### 2b. WHY, AND IT IS THE USEFUL PART: ONE OF THE THREE MEASURES BACKWARDS

Each signal alone, same population, same test:

| signal | n | effect on startable next season | p |
|---|---|---|---|
| **touches per game > 5.86** | 79 vs 79 | **+20.3 points** | **0.0002** |
| **NFL rounds 1-3** | 38 vs 120 | **+18.1 points** | **0.0113** |
| NFL round 1 only | 6 vs 152 | +36.2 points | 0.0435 |
| **yards per touch > 4.89** | 79 vs 79 | **-10.1 points** | **0.977** |

**Efficiency is a RECEIVER signal and an ANTI-SIGNAL at running back.** At receiver yards per target
measured **+14.4, p=0.004** (§4.30). At running back yards per touch measures **-10.1** and the
permutation runs the other way. So counting it into a composite does not add information, it
subtracts it, and that is exactly why the three-count table above is mush.

**A plausible mechanism, and it is an INFERENCE not a measurement: a back with few touches and good
yards per touch is a change-of-pace specialist, and the role that produces the efficiency is the
role that caps the volume.** Not tested. Flagged as such.

### 2c. DROP IT, AND THE TWO THAT SURVIVE ARE STRONG AND STABLE

Draft capital and volume only, swept across every threshold:

| touches/game cut | 0 of 2 | 1 of 2 | **2 of 2** | difference | p |
|---|---|---|---|---|---|
| p40 (4.5) | 3.5% (n=57) | 17.1% (n=70) | **32.3% (n=31)** | +21.2 | **0.0057** |
| p45 (5.3) | 3.1% (n=65) | 19.0% (n=63) | **33.3% (n=30)** | +22.4 | **0.0042** |
| **p50 (5.9)** | **4.2% (n=71)** | **19.0% (n=58)** | **34.5% (n=29)** | **+23.6** | **0.0037** |
| p55 (6.3) | 3.9% (n=77) | 22.6% (n=53) | **32.1% (n=28)** | +20.6 | **0.0107** |
| p60 (7.2) | 4.8% (n=84) | 23.4% (n=47) | **33.3% (n=27)** | +21.9 | **0.0073** |

`[TESTED, n=158]` **Every cut separates, p between 0.004 and 0.011, and the bottom cell is 3 to 5%
against a top cell of 32 to 35%.** That is close to a ten-fold spread and it does not move when you
move the knife. **The two-signal version is the finding; the three-signal version is not.**

**The 2-of-2 cell that converted** (median cut): Brian Robinson, Najee Harris, Miles Sanders,
D'Onta Foreman, Travis Etienne, Devin Singletary, Rachaad White, Zach Charbonnet, Rashaad Penny,
James Cook. **And the cell that did not**, which is the honest half: Javonte Williams twice,
AJ Dillon twice, Tyjae Spears twice, Cam Akers, Kareem Hunt, Clyde Edwards-Helaire, Zack Moss.
**It is a one-in-three screen, not a prophecy**, exactly like §4.30's 39%.

---

## 3. THE METHOD LESSON, WHICH IS THE REAL ANSWER TO HIS QUESTION

**A composite is not a general method you port to a new position. It is a set of signals that each
carry independent information at THAT position, counted.** §4.30 got three that fired at receiver
and the count worked. At running back only two fire, and including the third actively destroys the
result: p goes from **0.0037 to 0.1823** purely by adding a signal that points the wrong way.

**THE PROCEDURE, and it is now the standing one:**
1. **Test every candidate signal ALONE at that position first**, on the same population and the
   same outcome. Report the sign.
2. **Keep only the ones that fire in the right direction.** A backwards signal is not a weak signal,
   it is a subtraction.
3. **Then count, and sweep the threshold.** If the p depends on where you cut, there is nothing
   there.
4. **Say which of substitution and amplification the number showed** (§0.5a3), and do not assume
   either.

**AND THE STANDING WARNING SURVIVES:** the only interaction COEFFICIENT ever significant in this
project is doc 191's, and it is negative. The count method sidesteps estimating one, which is
precisely why it is the affordable route at these sample sizes.

---

## 4. WHAT THIS CHANGES

* **A new screen exists for backs on the wire and at late picks: NFL rounds 1 to 3 AND at least
  about six touches a game, on a young back who is not yet startable.** One in three of those became
  startable the next season against a 15% base. It is the receiver composite's sibling and it uses
  two columns the board could carry tomorrow.
* **Yards per touch must not be used as a positive signal at running back**, and any sheet that
  prints efficiency next to a back should say it is descriptive.
* **Doc 235's "the pop is the workload" is confirmed on a new object**: volume is the strongest of
  the four, p=0.0002.
* **Draft capital fires for a third time**, after §4.28's first-round receivers and §4.30's rounds
  1-3. It is free, public, and the board still does not carry it.

## 5. OPEN

* **NOT YET RUN:** the same procedure at tight end. Population is thinner and it may not support it;
  the honest expectation is an underpowered null, and that is worth knowing.
* **NOT YET RUN:** the concentration test (starters drafted rounds 1-4, the manager's actual lineup
  loss in the weeks they missed, QB and TE against RB and WR). Needs `draft_history_2021_2025.csv`
  staged. **Next.**
* **NOT YET RUN:** slot rate and targets per route run added to the RECEIVER composite from the PFF
  files, run through step 1 above first so a backwards signal is caught before it is counted.
* **[OPEN]** the board carries no NFL round or overall pick column, so two of the four strongest
  signals in this project cannot reach the page.
