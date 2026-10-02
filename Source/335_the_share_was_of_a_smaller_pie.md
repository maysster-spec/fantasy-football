# 335 THE SHARE WAS OF A SMALLER PIE, AND LOSING A CLAIM IS FREE

**2026-09-17, overnight, before the Thursday morning waiver run.** Matt read a Rotowire note on
Malik Washington (three of eight targets, 53 yards, a lost fumble) and said he did not feel
encouraged. He was right, the page's own workload screen said the opposite, and the variable that
separates them is on neither screen.

---

## 1. WHAT HE ASKED, IN ITS TESTABLE FORM (section 0.5a2)

*Does Malik Washington's week 1 line support the workload screen's 3-of-3 rating, or does it
support Matt's read that the offence and the hands are both a problem?*

**POPULATION:** the two receivers actually on the claim list, Washington (MIA) and Devaughn Vele
(NO), week 1 of 2026, from `form_2026.csv` and `pedigree_2026.csv`.
**BASELINE:** section 4.30's receiver composite bar of 7.13 yards per target, and the week-1
workload screen of targets at or above 8, snaps at or above 80%, target share at or above 20%.

## 2. THE MEASUREMENT

| | Washington | Vele |
|---|---|---|
| team targets, week 1 | **27** | **52** |
| his targets | 8 | 9 |
| his share | **29.6%** | 17.3% |
| snaps | 98% | 91% |
| yards per target, week 1 | **6.63** | **7.67** |
| yards per target, 2025 | **4.98** | **7.51** |
| targets per game, 2025 | 3.82 | 4.33 |
| NFL draft round / pick | 6 / 184 | 7 / 235 |
| **workload screen** | **3 of 3** | 2 of 3 |
| **section 4.30 composite** | **1 of 3** | **2 of 3** |
| half-PPR, week 1 | 4.8 | 16.4 |

**THE TWO SCREENS DISAGREE ON ONE PLAYER AND THE REASON IS TEAM PASS VOLUME, WHICH NEITHER CARRIES.**
Washington's 29.6% is the largest receiver share in this week's data and it is a share of a pie half
the size of New Orleans'. Vele's smaller share is a larger NUMBER of targets. A target share is a
ratio and the workload screen treats it as a quantity. `[TESTED, n=2, descriptive]`

**This is section 0.6 in a new place.** The screen states its population correctly (one team's
targets) and then the reader carries the number across teams as though the denominators matched.
**RULE: a target share must never be compared across teams without its denominator beside it.**

**THE ARITHMETIC OF THE 4.8, because it also answers a second question Matt asked.** Three catches
at 0.5 is 1.5, 53 yards at 0.1 is 5.3, a lost fumble is minus 2. Total 4.8, which is exactly what
`form_2026.csv` carries. **His 73 return yards contributed zero**, and that is correct:
`2026_League_Settings.txt` lines 74 to 81 list kickoff return TD, punt return TD, interception
return TD, fumble return TD and blocked kick return TD, all at 6, and **no return yardage line of
any kind**. Our twelve-component scoring map carries ids 101 and 102 at 6.0 and nothing for yards,
and it reconstructs ESPN's own applied totals to a maximum error of 0.197 across 461 players
including high-volume returners. `[SOURCED: 2026_League_Settings.txt, lines 74-81]` `[TESTED]`

## 3. THE MECHANIC I HAD AND DID NOT APPLY

Section 4.32 term 5 has said since it was written that **losing a claim delays a player, it rarely
removes him**, and the wire page says in terms that only the FIRST winning claim comes at his real
priority. Both mean the same thing: **a claim that fails costs nothing and preserves his position
for the next claim in the same run.**

I had nonetheless been steering him toward low-ownership names on the grounds that he wins 56% of
uncontested claims and 10 of 63 contested ones. **That reasoning is wrong given the mechanic.**
Contestedness changes the probability of winning, not the price of trying. **The claim list is a
strict preference ordering and nothing else: the man he would be most annoyed to miss goes first.**

This is docs 255, 256 and 257 repeating. Twice before I ruled on the VERDICT of the claim list
instead of filling in its terms, and this is the third time, in the opposite direction.
**FILED AS A STANDING CORRECTION: never rank a claim list by probability of winning.**

## 4. WHAT WENT IN

Vele, Chris Brooks, Dalton Schultz, the same drop named on the first two. Washington off the list.
**NOT the ordering I gave him an hour earlier**, which had Washington on it on the strength of the
workload screen alone.

## 5. NOT YET RUN, WITH THE FORM WRITTEN DOWN (section 0.5a4)

**Jordyn Tyson is on injured reserve and Vele holds the New Orleans WR2 snaps.** Rotowire's note
attributes the role to the absence. **The snap counts do not support that framing:** Vele played
91% of New Orleans snaps, MORE than Chris Olave's 86%, and the next receiver in the room is Bryce
Lance at 69% and four targets. I repeated Rotowire's causal sentence to Matt before checking it and
he pushed back; he was right.

**THE TEST, and it is already on the board as doc 292's E5, "a hurt starter parked on IR until he
returns".** POPULATION: every team-season 2021-2025 where a receiver drafted in NFL round 1 missed
four or more of his team's first games and a teammate took the vacated WR2 snaps. PREDICTOR: the
teammate's snap share and target share while the rookie was out. OUTCOME: his target share in the
first four weeks after the rookie returns, minus his share before. **BLOCKER: none. nflverse
injuries plus weekly snaps, both already used elsewhere in this project.**
Section 4.27 is RB-only and about a two-week cameo; section 4.28 is about a season boundary. **This
is a third object and borrowing either number for it would be section 0.5(a2) again.**

## 6. WHAT THIS DOES NOT SAY

It does not say Vele is good. Both men are long shots by the composite, in the 5.0% and 7.1% bands.
Section 4.30 is under re-check as catalog item B6/F2 and its 7.13 bar should be quoted with that
attached. What is measured here is only that **the two screens disagree on Washington, and the
disagreement resolves against him on the one signal section 4.30 measured at p=0.004.**
