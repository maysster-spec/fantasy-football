# 282 — The retraction that did not stick, and the sort key that caused it

**2026-09-10, week 1.** Matt: *"Brenton Strange — didn't we discuss him? Isn't he the one not
targeted in the red zone very frequently?"*

**Yes. We discussed him yesterday, I retracted him yesterday, and I recommended him again today.**
Doc 236 §0 item 1, 2026-09-09, opens with the words *"THE TE CALL IS RETRACTED AND HE WAS RIGHT
ABOUT WHY. Do not claim Brenton Strange."* Twenty-four hours later I put him at the top of a reply
and into `matt_todo.txt`. He caught it from memory, which is the only guard that fired.

---

## 1. WHY IT HAPPENED, AND IT IS NOT FORGETFULNESS — IT IS THE SORT KEY

Today's recommendation was produced by a measurement I ran fresh: best legal nine over fourteen
weeks, with and without each free tight end. Strange came out top at **+8.1** because he has the
highest ESPN projection of the free tight ends **and** a bye that is not week 6.

**Both of those are the wrong instrument, and doc 236 had already said so in terms.** §4.5 is the
only tight-end signal this project has ever measured as sticky from one season to the next:
**inside-10 targets r=+0.59 · red-zone target volume r=+0.51 · red-zone target share r=+0.48 ·
red-zone touchdown RATE r=+0.02, noise** (n=37, 2024→2025). A projection is a different object. The
arithmetic was right and the object was wrong — **§0.5(a2), for the fourth recorded time.**

**AND THE ARTIFACT AGREED WITH ME, WHICH IS THE REAL DEFECT.** `THE_WEEKLY_WIRE.html` ranks each
position's free pool by our value, which at tight end is the projection. **Strange was the top row
of the TE table on the page Matt reads.** A retraction that lives in a doc cannot survive a page
that keeps putting the retracted man first: **the top row of a sorted list reads as a
recommendation whatever the caption says.**

---

## 2. HIS MEMORY IS RIGHT, AND THE RAW COUNTS IN DOC 236 UNDERSTATE HALF OF IT

**POPULATION: every tight end free on the 09-10 wire, plus LaPorta and Hockenson. SOURCE:
`RedZone_Receiving_2025.csv`, 2025 regular season, joined to `form_2025.csv` for games played.
Doc 236 printed RAW COUNTS and flagged the caveat itself; this is the per-game version.**

| tight end | g | inside-20 a game | **inside-10 a game** | red-zone TDs |
|---|---|---|---|---|
| **Darren Waller** (CAR) | 9 | 0.78 | **0.56** | 6 |
| Colby Parkinson (LAR) | 14 | 1.43 | **0.71** | 6 |
| Dalton Schultz (HOU) | 17 | 0.65 | 0.35 | 3 |
| **AJ Barner** (SEA) | 17 | 0.71 | 0.35 | 5 |
| Mike Gesicki (CIN) | 12 | 0.58 | 0.33 | 2 |
| Pat Freiermuth (PIT) | 15 | 0.60 | 0.27 | 3 |
| **Brenton Strange** (JAX) | 12 | **0.75** | **0.25** | 2 |
| Michael Mayer (LV) | 13 | 0.46 | 0.23 | 1 |
| **T.J. Hockenson** (MIN) | 15 | 0.73 | **0.20** | 3 |
| Gunnar Helm (TEN) | 16 | 0.44 | 0.19 | 1 |
| **Sam LaPorta** (DET) | 9 | 0.44 | 0.33 | 2 |
| Evan Engram (DEN) | 16 | 0.62 | **0.00** | 1 |

**The honest reading splits two ways, and doc 236's raw counts only carried one of them.**
- **On inside-20 volume, per game, Strange is fine — 0.75, second on this table.** Doc 236's "9"
  looked mid-pack only because he played 12 games; his rate is not the problem.
- **On inside-10 looks — which §4.5 measures as the STRONGEST of the three, r=+0.59 — he is 0.25 a
  game, less than half of Waller's 0.56.** That is the thing Matt remembered, and it is the right
  thing to have remembered.
**So the sentence is not "Strange never sees the red zone." It is "Strange gets to the goal line
less than half as often as Waller does,"** and on this board that is the half that carries.
`[SOURCED, per-game rates computed here; not modelled]`

**AND HOCKENSON IS NOT THE ANSWER EITHER: 0.20 inside the ten a game, third-worst on the table.**
He is a fine one-week blanket and he is not a goal-line tight end.

---

## 3. THE FIX — THE PAGE NOW CARRIES THE SIGNAL AND SORTS ON IT

A retraction list would have been the wrong repair: the page was not quoting a doc, it was sorting
on a number. **So the number changed.**

- **`Source\redzone_te_2025.csv`** — new, committed, static: `espn_id, player, tm_2025, g25, in20,
  in10, rz_td, in20_pg, in10_pg` for **137 tight ends**, built by joining the red-zone export to
  `form_2025.csv` on a normalised name (no id exists in the export) and emitting `espn_id` so every
  runtime join is an id join (§3).
- **Two population decisions, both stated because either could mislead.** The source lists only
  players who drew a red-zone target, so **35 tight ends have no row and are written as 0 — a
  measured zero, not a missing value.** Dropping them would have hidden exactly the men with no
  goal-line role, which is §0.5(c)5 inverted. And **rates are blank under four games**, so a man
  with one target in one game cannot top the table at 1.00 a game.
- **`wire.py`** now ranks the TE block on **inside-10 targets per game** and prints the three
  numbers beside each man, with the caption saying it is a targeting list and that touchdowns
  themselves do not carry. Every other position is untouched.

**NEGATIVE CONTROLS, RUN ON THE PRODUCTION RENDERER (§0.2), not an equivalent:**

| control | expected | got |
|---|---|---|
| file present | TE block led by Waller/Parkinson, goal-line column drawn | pass |
| **file missing** | the page SAYS the ranking fell back to projected points | **pass — named in red** |
| file present/absent | column appears / disappears | pass |
| under 50 rows | treated as missing, with the row count named | pass by construction |

`wire.py` 64485 → 67801 (`edc11d0be87b852a`), re-pinned.

---

## 4. AND HIS SECOND QUESTION WAS ALSO ALREADY ANSWERED BY OUR OWN DOC

> *"do i really need two TE on my roster now, or can it wait? I only picked up Hock as a safety
> blanket to see of Sam makes it through this first week unscathed."*

**Doc 236 item 2 says wait, in his words and on our numbers, and I contradicted that today too.**
The reason I contradicted it is the same reason: I measured Hockenson as a *week-6 bye fix*, which
is not what he bought him for. **He told me the object and I priced a different one.**

**Priced for what he actually said — one week of insurance on LaPorta — the seat is free.** Every
free body on his page prices at **0.0 to 0.4** against his starting nine (doc 276), so the seat has
no better use this week, and `drop_costs` puts Hockenson at **0.0**: dropping him whenever he wants
the seat back costs nothing in any of the fourteen weeks. **The only wrong move available is
holding him *as* the week-6 answer**, because Minnesota and Detroit are both on bye in week 6 and
that is a measured **+0.0** (doc 281).

**ROSTER CONFIRMED, from `MY_ROSTER.csv` written by his own run at 16:30:** 15 of 15, LaPorta **and**
Hockenson at tight end. His *"there is no room on my roster"* was correct and my open-spot row was
the artefact doc 281 fixed. The rebuilt sheet now prints **"your roster is full"** — the guard from
doc 281 firing on live data, which is what verifies it.

---

## OPEN AFTER THIS

- **`py wire.py --html` needs one more run** to pick up the TE sort. Until then the page still
  leads that table with Strange.
- **News check on Waller and Barner is NOT YET RUN and deliberately so** — the decision is week 5,
  and a dated check four weeks early is a stale check. Waller is 34 with 9 games in 2025; the
  `12g` reading (§4.22, doc 204) makes that close to noise on a ten-year veteran but the role is
  the question, not the age.
- **Colby Parkinson tops the goal-line table at 1.1% owned and −79 value.** A pure role sort
  surfaces backups; the value column is printed beside it on purpose. Whether role-over-projection
  is the right *ordering* at tight end, or only the right *tiebreak*, is `[OPEN]` — §4.5 measured
  stickiness, never that it beats the projection out of sample.
- **`py waivers.py --live`** still unrun; 2026 has no waiver report.
