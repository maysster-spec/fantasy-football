# 329. Three numbered rules beat one unnumbered bullet

*17 Sept 2026, 00:20 UTC. Matt: "the model steered me to players who don't have that upside
potential as keeper candidates because they are not risers. That value was never measured."
He is right on both halves. The steering is demonstrable on his own roster; the value is
NOT YET RUN, and it is not blocked.*

---

## 1. WHAT CHANGED

1. **CONFIRMED BY INSPECTION: the keeper-audition logic selects against risers, by construction.**
   Every rule that decides who becomes an audition is a PRICE or a ROUND. The one trajectory rule
   has no number and therefore never binds.
2. **His own 2026 roster is the proof.** The audition band section 6 points at holds **Hurts,
   LaPorta, Dowdle and Dobbins**, two of them sixth-year backs. The two players whose roles are
   actually expanding sit in **rounds 10 and 11**, where section 6 demotes them to darts.
3. **NOT YET RUN, not blocked: whether a riser is worth more as a keeper at equal price.** Testable
   form written below and queued as **JOB 4**. Inputs named, all on the drive.
4. **JOB 4 is a separate job from JOB 3, on purpose.** Different population, different outcome.
   Merging them would be section 0.6's error.
5. **A live consequence tonight, not next August:** the audition is a bench spot he is paying for
   NOW, so this is the same argument as the Dobbins one and it points the same way.

---

## 2. THE STEERING, TRACED

Three rules decide who is a keeper audition. **All three are price or round. None is trajectory.**

| rule | what it says | what it selects |
|---|---|---|
| section 6 | concentrate auditions in **rounds 5 to 8** | the more expensive half of the eligible pool |
| section 4.26(a) | among eligible candidates prefer the one drafted **closest to round 5** | the single most expensive eligible player |
| section 4.18b | a **round 9+** keep returned **minus 2.5** (n=7) | pushes the cheap picks out of audition status |

Against those, section 6 carries one bullet: *"Between equal projections, prefer the plausible 2027
role, young, ascending, secure."* **No population, no baseline, no sample size, no number.**

**Section 0.1 already diagnosed this failure mode in a different place and the diagnosis transfers
exactly: when a specific mandatory rule and a general aspirational one apply to the same sentence,
the specific mandatory one wins every time.** Three measured rules against one unmeasured bullet is
not a tiebreak, it is a rout. Matt did not need to be overruled; the bullet simply never reached
the argument.

---

## 3. HIS ROSTER, WHICH IS THE CASE HE IS MAKING

Keeper-eligible for 2027 means drafted round 5 or later and rostered all season (section 2.1a).
From `2026 draft results.csv`:

| round | pick | player | what he is |
|---|---|---|---|
| 5 | 56 | Jalen Hurts, QB | established star. **Section 4.18b: a kept QB returned minus 55.7 (n=9).** |
| 6 | 65 | Sam LaPorta, TE | year 4. 17 then 16 then 9 games. |
| **7** | **80** | **Rico Dowdle, RB** | **sixth-year back** |
| **8** | **89** | **J.K. Dobbins, RB** | **sixth-year back** |
| 9 | 104 | Tyjae Spears, RB | dropped 12 Sept, cost nothing in any of 14 weeks |
| 10 | 113 | Xavier Worthy, WR | year 3 |
| **11** | **128** | **Mike Washington Jr., RB** | **2026 rookie, NFL round 4 pick 122** |
| 12 | 137 | Tyler Shough, QB | year 2 |

**The audition band is rounds 5 to 8. Three of its four are established or declining, and the
fourth is a tight end with an injury record.** The two players on this roster with an expanding
role, Washington and Worthy, are in rounds 10 and 11, which section 6 calls darts and not
auditions.

**That is exactly the sentence he wrote, arrived at from the files rather than from the complaint.**

---

## 4. THE TESTABLE FORM, WRITTEN BEFORE THE TEST (0.5a2)

His claim splits the same way doc 326's did.

**CLAIM A, about the instrument: the audition logic selects against risers.**
**TESTED, by inspection, in sections 2 and 3 above. CONFIRMED.**

**CLAIM B, about the world: at equal price, a riser is worth more as a keeper than a flat or
declining player.** **NOT YET RUN.** Queued as JOB 4 in `Source\REDTEAM_TASKING_PROMPT.md`:

- **POPULATION:** player-seasons 2021 to 2024, all four positions, with a section 1.1 preseason ADP
  of 50 or higher in season N (the keeper-eligible band) and priced again in N+1.
- **PREDICTOR:** share of team opportunity in weeks 10 to 14 minus the same share in weeks 1 to 5,
  computed from the season that just ended, because that is what is knowable in August when the
  keeper is declared.
- **CONTROL: log(preseason ADP), mandatory.** Section 4.26(a) already measured that price predicts
  repeating, so an uncontrolled riser test re-finds the price effect and calls it trajectory.
- **OUTCOMES, both:** season N+1 VBD14 on section 4.18b's baseline, and whether he was startable at
  all (section 4.13b's absolute bar).
- **FALSIFIER, fixed first, and it cuts both ways.** Nothing over price with a CI excluding a
  10-point gap means the "ascending" bullet is noise and should be STRUCK from section 6 so it stops
  competing. Ten points or more net of price means section 4.26(a)'s "closest to round 5" is the
  wrong instruction here and the audition band has to be re-cut.

---

## 5. WHY IT IS NOT BLOCKED, AND WHY IT WAS NEVER RUN

**Not blocked.** The riser variable is computable from nflverse weekly data, four seasons of which
are already cached in `Scripts\research\_nflverse_cache\`, joined to the section 1.1 price registry.
Nothing needs buying and nothing needs a login.

**Why it was never run: every keeper measurement in this project is conditioned on price or on a
past finish, and neither of those is trajectory.**
- Section 4.26(a)'s population is **top-12 finishers**, split by **price**. It asks whether a hit
  repeats, not whether a rising role continues.
- Section 4.18b's population is **kept players** and **ADP 97+ hits**. Price again.
- Section 4.13's three retired draft-day signals were all **price** divergence, and "the market is
  sleeping on him" was the worst of them at rho minus 0.079.

**So the honest statement is not that the riser hypothesis lost. It is that it was never on the
field.** Section 4.18b's finding that *"a late hit is, on average, a role that existed for one
year"* pools a one-year fluke with a genuine role expansion, because its population was defined by
price. **Separating those two is the whole of JOB 4, and if the run ends up re-measuring 4.18b it
has measured the wrong object.**

**AND ONE MEASUREMENT ALREADY LEANS HIS WAY AT ONE POSITION.** Section 4.30's composite is
riser-shaped in everything but name: young non-startable receivers, draft rounds 1 to 3, yards per
target and targets per game, **0% / 5.0% / 7.1% / 39.4%** as the signals stack, p=0.0000. It
predicts becoming startable next season. **Nobody has ever joined it to a keeper outcome.**

---

## 6. WHAT THIS DOES NOT SAY

- It does **not** say risers make better keepers. That is claim B and it is unrun.
- It does **not** retract section 4.26(a). Its result stands on its own population: among players
  who already hit, the expensive hit repeats at 56.0% against the cheap hit's 22.7%, n=135.
- It does **not** say Dowdle and Dobbins were bad picks. It says the reason they became the
  audition band was their round, not a measured property.
- It does **not** license dropping anybody. Section 4.19 is untouched.

---

## 7. THE LIVE PART, BECAUSE THIS IS NOT ONLY A 2027 QUESTION

The keeper is declared next August, but **the audition is a bench spot he pays for every week of
this season.** That makes this the same argument as doc 326's Dobbins case, from the keeper end
instead of the draft end, and both land on the same instruction:

> **A bench player earns his spot by the job he would inherit and the fragility of the man ahead of
> him, never by his own projection and never by the round he was taken in.**

That is doc 240's rule. **Section 6's audition band is the one place in the directive that still
allocates a bench spot by ROUND**, and doc 240 already replaced that logic everywhere else.

---

## 8. OPEN

- **JOB 4**, claim B. `[NOT YET RUN]`, testable form above, inputs named.
- **Section 6's "ascending" bullet**: either give it a number or strike it. JOB 4 decides which.
  `[OPEN]`
- **Section 4.30's composite has never been joined to a keeper outcome.** `[OPEN]`
- Carried: doc 326's JOB 3, the section 4.25b wording, the draft-capital column on the spine, the
  chart-versus-usage disagreement tell, catalog B4.
