# 432 — A share is a share of something, and the bet lane never looked at the denominator

*25 Sept 2026. Matt spot-checked two players in one evening and both takes died, on two different
mechanisms with one cause. He asked for the first one and found the second himself.*

---

## 1. THE TWO HE FOUND

**CADE OTTON, the number one name on THE CALL.** His question: *"this cade otton, the 28th ranked TE.
Does he get in zone targets or not?"* **No, and it is measured.**

| Otton, inside the 20 | targets | inside 10 | RZ TD | share of Tampa's RZ targets |
|---|---|---|---|---|
| 2024 | 14 (rank 31 of 363 receivers) | 8 | 4 | 18.2% |
| 2025 | **5 (rank 146)** | 2 | 1 | **8.5%** |

**45th of 137 tight ends in 2025**, in 15 games. §4.5 already holds that red-zone volume is STICKY
and red-zone TD rate is noise, so the collapse is the predictive half.

**MALIK WASHINGTON**, promoted to number one after Otton fell. Matt: *"There is so little volume and
they feed waddle a crazy share of it."* **The name is wrong (Jaylen Waddle is on Denver in 2026) and
the conclusion is right for a worse reason.** Washington's 26.0% is the LARGEST share in Miami, ahead
of Achane 22% and Caleb Douglas 20%. He already won the competition. **Miami throws 25 targets a game,
28th of 32.** Houston throws 44.

---

## 2. THE CAUSE, AND IT IS ONE SENTENCE

**The bet lane prices every candidate at ONE archetype hit rate, 12.71 a game, and never asks whether
his own offence throws enough for that to be reachable.** The screen counts targets, snaps and target
share. A share is a share OF something and the denominator was nowhere in the page.

**§0.5(a6) says it in Matt's own frame** — *targets on one offence are zero sum, find the resource
that constrains him* — and the page shipped two takes that ignored it.

---

## 3. THE CEILING, MEASURED RATHER THAN GUESSED

**TESTABLE FORM, stated before the run:** among WR/TE six-week windows where the man averaged the hit
rate or better under our scoring, what share of his team's targets did he hold? **POPULATION:**
nflverse REG 2021-2025, windows inside one season, **n=854**.

| | median share held | p90 | **p99** | max ever | his team threw |
|---|---|---|---|---|---|
| **WR** (n=748) | 27.0% | 33.1% | **37.8%** | 41.2% | 33.8 a game |
| **TE** (n=106) | 24.5% | 30.0% | **32.7%** | 33.1% | 34.8 a game |

`[TESTED]` **Men who produce at that rate are on offences throwing about 34 a game. Miami throws 25.**
RB was not measured and is not gated.

---

## 4. WHAT IT DOES TO TODAY'S LANE

The gate is `need = his targets a game x (hit rate / his own points a game)`, then `need / his team's
targets a game`. **A CONSTRAINT, NOT A FORECAST.** It does not say he will hit; it says he cannot.

| player | needs, as a share of his whole offence | verdict |
|---|---|---|
| Malik Washington | **57%** | out of reach |
| Michael Mayer | 48% | out of reach |
| Luther Burden III | 47% | out of reach |
| Cade Otton | 45% | out of reach |
| Pat Bryant | 41% | out of reach |
| Kalif Raymond | 34% | passes, at the edge |
| Xavier Worthy | 34% | passes, at the edge |
| Germie Bernard | 25% | passes |

**Five of nine killed.** The odds beside those five were true of the archetype and false of the man.

**AND THE ROW THAT PRINTS IT SAYS "out of reach", NEVER "not measured".** Those are different states
and this project has conflated them before (§0.5). The required share is printed so the reader can
check the arithmetic without the doc.

## 5. ONE CORRECTION I OWE, CAUGHT BY THE GATE ITSELF

**My first hand-computed version of the table used `half_ppr` out of `form_2026.csv`, which is standard
half-PPR, not this league's scoring.** It put Germie Bernard at 18.5 targets needed, and the engine on
our own scoring puts him at 9.2 and passing. **The two headline numbers survive** (Washington 57%,
Otton 45%) but the reply that carried the first table overstated one man. `measured` off the rates dict
is ESPN's actual under our rules and is the right column. §0.6: the population was wrong before the
arithmetic was.

## ASSUMPTIONS

1. "At his own catch rate and yards per catch, with no touchdown" is deliberately generous to the
   candidate in one direction (a TD lowers the targets needed) and honest in the other (his efficiency
   is his own). A man who adds a touchdown role beats his gate. That is the red-zone term, not this one.
2. Two games is a thin denominator for a team's targets a game. It gets better weekly and the gate
   only bites at large multiples, where two games is enough to see a 25 from a 44.
3. The p99 is a ceiling on what has been SUSTAINED for six weeks, not on a single week.
