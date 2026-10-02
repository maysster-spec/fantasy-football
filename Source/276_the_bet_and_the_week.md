# 276 — The bet, and the week to make it

Matt, 2026-09-10: *"add to the sheet/page that short list of players with the top potential value.
I never know when is a good week to take that risk until I eval that one player who may have a
significant signal."*

The list is on the sheet. Getting it there needed three measurements, and the third one kills a gate
I shipped yesterday.

---

## 1. The question underneath the question, and it has an answer

"When is a good week" has two halves and only one of them moves.

**The pool's half does not move at all.** On this league's own four years of transactions, a
screened young receiver became a startable player at almost the same rate whenever he was added:

| when he was added | screened | unscreened |
|---|---|---|
| weeks 1–4 | **40.0%** (2/5) | 9.1% (1/11) |
| weeks 5–9 | **28.6%** (4/14) | 8.0% (2/25) |
| weeks 10–14 | **40.0%** (2/5) | 8.3% (1/12) |

**So there is no good week and no bad week on the wire's side.** What moves is the other half — what
the spot costs — and that is a fact about his own roster which the sheet already computes. The whole
decision is therefore one comparison, and the page now prints both sides of it next to each other.

---

## 2. The screen works in-season, and this is a different measurement from doc 248's

`[TESTED, n=108]`
**POPULATION — state it every time: every EXECUTED add in this league 2022–2025 of a receiver in his
first three NFL seasons who played at least one week afterwards. n=108. BASELINE: 9.62 half-PPR a
game, doc 12's measured WR replacement, from the add week through week 14.**

| archetype | n | hit | rate |
|---|---|---|---|
| every young WR add | 108 | 19 | 17.6% |
| **3 of 3 on last season** | **24** | **8** | **33.3%** |
| under 3 | 48 | 4 | 8.3% |
| rookie, NFL rounds 2–3 | 21 | 6 | 28.6% |
| **rookie, NFL round 1** | **6** | **0** | **0.0%** |

**3-of-3 against every other young WR add: +20.2 points, permutation p=0.0279.** The three signals
are §4.30's own — NFL rounds 1–3, yards per target over 7.13, targets per game over 3.20 — computed
on the prior season, which is exactly what `pedigree_2026.csv` already carries, so the number
transfers to the live column without re-deriving anything.

**WHY THIS HAD TO BE MEASURED SEPARATELY.** §4.30's 39.4% is a *next-season* rate. A waiver pickup
can never be a keeper (§2.1a), so next season is worth precisely nothing on an in-season add, and
putting a next-season rate on a weekly sheet is doc 275's Gate 2 error committed one day later.
`sheet_constants.json` now carries both under separate keys with the warning written into the file.

**THE FIRST-ROUND ROOKIE IS 0 FOR 6 IN-SEASON AND THAT IS NOT A REFUTATION.** Six is too small to
resolve anything, and five of the six were added in weeks 4 to 10 — a first-rounder sitting on a
mid-season wire is one the market has already given up on, which is a different population from
doc 251's rookies rostered all year. The page prints his odds as **not measured** and his expected
value as a **dash, never a zero**: the difference between "we measured nothing" and "we measured
nothing there" is the whole point of the column.

**ONE HIT SIZE FOR EVERY ROW.** Among the 19 adds that converted the mean was **12.71 half-PPR a
game over 6.4 weeks**. The first version of the section used a different hit size per archetype and
invented a distinction 19 hits cannot support. How big a hit is, is a property of *a young receiver
who became startable*; only the odds differ between rows.

---

## 3. Doc 275's fragility gate is dead — 46% of backfields open up, at every team

Doc 275, yesterday, gated the inheritance list on *the man ahead missed a game last season*. It was
§4.27's gate and I shipped it without testing it at the object it uses. Tested now.

**THE CLAIM IN ITS TESTABLE FORM: among running backs who led their own team's weeks-1–4 usage in
season Y and were on an NFL roster in Y−1, does having missed a game in Y−1 raise the chance of
missing a week-1-to-14 game in Y? POPULATION: 115 lead-back seasons, 2022–2025, same player both
years. BYE WEEKS EXCLUDED.**

| last season | n | misses a week 1–14 game this season |
|---|---|---|
| missed one or more games | 74 | **45.9%** |
| played every game | 41 | **46.3%** |

**Difference −0.4 points, permutation p=0.60.** `[TESTED, null]` By dose it is non-monotone as well
— 46.3% / 48.4% / 35.7% / 60.0% across 0, 1–2, 3–5 and 6+ games missed. **The gate carried nothing
and it is removed.**

*(Method note, because the first cut of this was garbage: it returned 100% in both arms, because a
bye week reads as a missed game. A result that extreme is a confound, not a finding. Byes are now
derived per team-season and excluded.)*

**WHAT THE SAME NUMBER SAYS INSTEAD IS BETTER THAN WHAT THE GATE CLAIMED.** Forty-six percent of
lead backfields open up in weeks 1–14, every year, everywhere. The risk is near-universal, so it
cannot rank teams — and every backfield with a claimable direct backup belongs on the list, sorted
by what the job pays. **The list went from 8 rows to 14, and the three it had been excluding are the
three biggest jobs on the board: Bijan Robinson (315), Christian McCaffrey (302), Jonathan Taylor
(291).** A gate that drops the top of your own list is worse than no gate.

A **live** injury tag is a different object — this week's information, not last season's — and it
survives as its own column, untested and labelled as such.

---

## 4. The seat, priced in the sheet's own currency

The first version of this section printed a job's season total (302.4) in the same table as a
gain-above-the-bar (0.3). Same page, two units, and the verdict box invited the comparison outright.
That is §0.1's scope rule broken by my own hand, so the seat is now priced the same way as
everything else, from three measurements:

- **the relief rate:** the direct backup scores **12.13 half-PPR a game** while the starter is out
  (n=51 events, NFL team-seasons 2022–2025, weeks 5–14)
- **the duration:** the starter is out **3.3 weeks** and the backup plays **3.0** of them
- **the odds:** **46%**, from section 3, and identical at every team

The job's season total is still what orders the table — it is printed under each starter's name as a
label, and never in a column beside the two numbers it must not be compared with.

**AND THE HANDCUFF IS PRICED AGAINST THE RIGHT BAR.** If the man holding the job is on Matt's own
roster, his going down *lowers Matt's bar* — that is the entire point of a handcuff — so a seat
behind one of his own backs is priced against the bar he would actually have, with that man removed.
Dylan Sampson behind Judkins is the live case, and it is the one row on the table that is not the
same as every other. It is also the row an arbitrary top-ten cut had silently dropped at rank 11.

---

## 5. What the page now says about his roster, and it is not what he hoped

Everything on it is worth **0.0 to 0.4 points**. The screened receivers, the eleven seats, the
handcuff to his own starter — all of it, near zero.

That is not a failure of the section; it is the section working. His receiver room is Nacua, Pickens,
Adams and Worthy and his backfield is Jeanty, Judkins, Dowdle and Dobbins, so **a 12.7-a-game hit
does not beat a starter he already owns in any week except 11**, when three receivers are on bye
together. Even the Judkins handcuff clears by only 0.3, because Dowdle at 12.4 already covers that
hole. It is §4.33 and doc 259 arriving at a third place: **the wire cannot upgrade a working slot.**

So the verdict box says what the arithmetic supports and not more — *it clears, and it clears by
almost nothing; take the ticket if the spot is free and drop nobody for it.* The one number that
would move is conditional on an injury, which is why the seat table is labelled insurance rather
than upgrade.

---

## 6. What shipped

| file | what changed |
|---|---|
| `Scripts\sheet_engine.py` | new section 3 on the week sheet: the screened bet, what the spot costs, the seats. Three new functions — `drop_costs` (doc 240's method, every rostered body priced by removal), `bet` (the signal priced instead of the man), `load_seats` |
| `Source\sheet_constants.json` | `potential.in_season` (new, and the one the page uses) · `potential.next_season` (the old numbers, relabelled with a warning) · `seat` (relief rate, duration, odds) |
| `Scripts\research\build_inherit.py` | the fragility gate removed; `live_tag` added as its own column; the printed list is now every claimable seat |
| `Source\inherit_2026.csv` | 14 claimable seats, was 8 |
| `Scripts\check_kit.py` | `sheet_engine.py` re-pinned |

**Negative controls run before shipping, each against the failure it exists to prevent:** no
`inherit_2026.csv` → the section names the missing file instead of rendering an empty table · no
screened player in the free pool → "that is an answer, not a gap" instead of a blank · empty roster
→ still raises · unmeasured odds → a dash, and the row sorts on what it is worth if it fires rather
than reading as a zero.

**NOT YET RUN, input named:** whether a backup's snap or route share in the two weeks before an
absence predicts his relief scoring — the last candidate doc 275's four did not cover. It needs the
nflverse weekly snap-count release, which this project has pulled once (doc 133) and does not keep.
