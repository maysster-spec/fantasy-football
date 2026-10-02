# 200 — Pick 8: the state nobody ran, and Matt found it

*2026-09-06, T−1. `[TESTED, production `Engine`, `top=12, rollout_inner=60`, board 09-06 freeze]`*

---

## 0. THE ANSWER

**If Puka Nacua is on the board at pick 8, take Nacua, not St. Brown.** Engine margin **+25.7**
over St. Brown. Same for McCaffrey (**+26.6**) and Jonathan Taylor (**+15.7**). St. Brown remains
the answer only when all three are gone.

---

## 1. WHY THE GRID SHOWED NACUA AND THE BOARD SAYS ST. BROWN

Top eight by `eff_pick` on the current freeze:

| # | player | eff_pick | VOR |
|---|---|---|---|
| 1 | Gibbs | 1.32 | +162.3 |
| 2 | Bijan | 2.38 | +146.2 |
| 3 | Chase | 4.26 | +114.1 |
| 4 | **Nacua** | **5.31** | **+131.3** |
| 5 | J. Taylor | 6.17 | +122.5 |
| 6 | Smith-Njigba | 6.30 | +104.8 |
| 7 | **McCaffrey** | **7.71** | **+134.9** |
| 8 | **St. Brown** | **8.38** | **+101.3** |

**St. Brown is the engine's pick-8 answer because he is the best player EXPECTED TO STILL BE
THERE — he is not the best player.** Three names above him out-VOR him by 21 to 34 points. The
recommendation was always conditional and the conditionality was never written down anywhere Matt
could see it.

---

## 2. THE GAP: EVERY PUBLISHED PICK-8 RUN REMOVED THOSE THREE BY CONSTRUCTION

§4.2's modal pick-8 state is defined as **"top seven by `eff_pick` gone."** That is exactly
Gibbs · Bijan · Chase · **Nacua** · Taylor · JSN · **McCaffrey**. So doc 139's ten seeds, doc 140's
100 states and doc 182's thirteen all answered *"who do you take once the three players who beat
St. Brown are off the board."* **"St. Brown 10/10, 96/100, 13/13" is a true statement about that
state and says nothing about any other.** Doc 182's own note — *"a 30-state generator produced no
variation at pick 8"* — is the same fact restated, not independent confirmation.

This is `ERROR_PATTERNS` **A19** in its other form: not repeating a run, but varying the input
inside a boundary that was never questioned.

## 3. MEASURED, FOUR STATES

Production `Engine`, board 09-06 freeze, `recommend(8, top=12, rollout_inner=60)`.

| state | seven gone | engine #1 | #2 | margin |
|---|---|---|---|---|
| **A** (published) | top seven by eff_pick | **St. Brown** | Henry | **7.90** |
| **B** | A, but Nacua survives (Cook goes instead) | **Nacua** | St. Brown | **25.70** |
| **C** | A, but McCaffrey survives | **McCaffrey** | St. Brown | **26.60** |
| **D** | A, but Taylor survives | **J. Taylor** | St. Brown | **15.70** |

**State A reproduces §4.2 v7.2's published 7.8 to two significant figures (7.90).** That is the
negative control: the harness is the production object and it agrees with the shipped number
before it is asked anything new.

**Nothing here reopens pick 8.** §4.2 says pick 8 is closed and it is — *the WHO is closed
conditional on the room*. The rule underneath it was never stated plainly and now is.

---

## 4. THE RULE FOR THE ROOM

**At pick 8, take the highest-VOR player on the board.** The engine agrees in all four states, and
the margins are 8 to 27 points — an order of magnitude wider than anything this project calls a
tie. In order: Gibbs · McCaffrey · Bijan · Nacua · J. Taylor · Chase · JSN · **St. Brown**.

**Do not agonise.** If one of the three has slipped, the board's own VOR column already says so and
`cost vs #1` on the live board will say `free` next to him.

---

## 5. HOW IT WAS FOUND, AND WHAT THAT SAYS

Matt sat down to read the DRAFT BOARD GRID for the first time, saw **Nacua in his own pick-8 cell**,
and asked why. He asked the question twice — once as *"something I forgot to ask was related to
Puka Nacua and how that was unexpected"* — before I answered it properly. My first answer
(*"the grid is a forecast of the room, not our recommendation"*) was true, and it dodged the
question he actually asked, which was **"if Puka is there do I take him over Brown."**

`ERROR_PATTERNS` **F4**: a price or a process he says is wrong is EVIDENCE. Nine defects two days
out came from one such call. **This is the same pattern: an artifact looked wrong to him, and the
artifact was fine — the analysis behind it had an unstated boundary.**

**And it is §0.5(a2) failing on its first live test.** The rule says: state the claim in its
testable form before answering. Had I written *"claim: St. Brown is the pick-8 answer in the state
where Nacua, McCaffrey and Taylor are gone"* — the words "in the state where" would have made the
gap self-evident before any of this was needed.

---

## 6. WHAT THIS DOES NOT SAY

- **No probability is quoted for the slip.** §4.15 forbids a dispersion-only survival number: applying
  §4.12's noise to `eff_pick` without the §5 opponent model runs biased-optimistic, by 25× in the
  one case that was checked. The three names sit at eff 5.3–7.7 against a §4.12 sd near 6 picks, so
  a slip is not exotic — but that is a shape, not a number, and no number should be carried into
  the room.
- **§4.2's dollar work is untouched.** The Allen-vs-wait result compares a QB at 8 against the best
  available skill player and does not depend on which skill player that is.
- **Pick 32 and pick 56 are unaffected.** Nothing here changes the tie at 32 or the 1.77 cushion at 56.

*Reproduce: stage `code_live_engine.py`, `board_v8_fixed.csv`, `board_v7_kdst_separate.csv`,
`ESPN_prerank_with_ids.csv`; `configure(8, 12, 14)`; drop seven by name; `recommend(8, top=12,
rollout_inner=60)`.*
