# 242 — The gem finder does not exist, and the draft grade had six answers for sixty-two picks

**2026-09-09.** Matt: *"Jordyn Tyson, I think I heard that and forgot to take note. I was very busy
trying to define how to find those gems in the draft and to do research I should have."*

And earlier the same session, which this doc now confirms by measurement:
*"Cary got a bad draft grade from you, but i think that's since you don't have a meaningful way to
measure upside players."*

**He was right, and the mechanism is worse than he guessed.**

---

## 0. THE TESTABLE FORMS, STATED BEFORE THE RUNS (§0.5(a2))

1. *Is Jordyn Tyson in our own files, and if so what did our numbers say about him?*
2. *Does the sheet's dart flag (`dart_shape`) cover more than one archetype?*
3. *Can a "gem" be recovered from `depth_map.csv` by ranking depth-1 players on the size of the
   job they hold?*

All three ran. **The answer to 3 is no, three different ways, and the reason is a missing column.**

---

## 1. TYSON WAS IN THE FILE, AND BOTH OF OUR NUMBERS SAID NO

`Scripts\depth_map.csv`, row for Jordyn Tyson — WR, NO, depth-chart slot **1**, nobody listed
ahead of him, team job pie 339, `adp_pick` **168.06**, `dart_shape` **blank**.

So the chart said he was New Orleans' starting receiver. But:

- **His ESPN projection is 82.0 points.** WR replacement is **163.540** (§4.1). He is **81.5 BELOW
  replacement** on our own board — the worst kind of no.
- **Devaughn Vele out-projects him, 99.0 to 82.0.** He is not even the team's top-projected WR.
- **`adp_pick` 168.06 sits inside §4.14's sentinel blob** (~170 on the 09-05 freeze), where ESPN
  supplies no real draft position at all. His price is fabricated ordering.

**He was not a gem our files found and failed to print. Our files priced him as worthless.** That
is a harder failure to fix than a missing row, and it is the honest version of the answer.

New Orleans' WR room as `depth_map.csv` has it:

| proj rank | player | chart slot | proj | adp |
|---|---|---|---|---|
| 1 | Devaughn Vele | 1 | 99.0 | 171.6 |
| **2** | **Jordyn Tyson** | **1** | **82.0** | **168.1** |
| 3 | Bryce Lance | 2 | 32.0 | 170.0 |
| 4 | Mason Tipton | 2 | 14.0 | 170.0 |
| 5 | Barion Brown | 2 | 10.9 | 170.0 |
| 6 | Trey Palmer | 3 | 0.0 | 170.0 |

---

## 2. AND CARY TOOK HIM — AT OVERALL 117, ROUND 10

From `drafted.json` and `draft_analysis.json`: **`ChatCTE`** — Cary, slot 4, now *CeeDees Nuts*
(doc 238) — **took Jordyn Tyson at overall 117** and **Jonah Coleman at overall 141**. Both of the
players Matt named this session as the ones he wanted. Cary's full graded draft:

| overall | rd | player | pos | our VOR | gap charged | our "best available" |
|---|---|---|---|---|---|---|
| 4 | 1 | Ja'Marr Chase | WR | +114.1 | 17.2 | Puka Nacua |
| 21 | 2 | CeeDee Lamb | WR | +78.3 | 1.2 | Breece Hall |
| 28 | 3 | Breece Hall | RB | +79.5 | 0.0 | — |
| 45 | 4 | David Montgomery | RB | +8.3 | 17.1 | Jalen Hurts |
| 52 | 5 | Tucker Kraft | TE | +4.7 | 20.7 | Jalen Hurts |
| 69 | 6 | Brock Purdy | QB | +4.8 | 0.0 | — |
| 76 | 7 | MarShawn Lloyd | RB | −90.4 | **94.9** | Kyle Pitts Sr. |
| 93 | 8 | De'Zhaun Stribling | WR | −54.6 | **56.0** | Dallas Goedert |
| 100 | 9 | Blake Corum | RB | −17.6 | 19.0 | Dallas Goedert |
| **117** | **10** | **Jordyn Tyson** | **WR** | **−81.6** | **83.0** | **Dallas Goedert** |
| 124 | 11 | Kyler Murray | QB | −52.3 | 53.8 | Dallas Goedert |
| **141** | **12** | **Jonah Coleman** | **RB** | **−102.9** | **92.6** | **Jake Ferguson** |

**455.5 charged in total, 399.3 of it (88%) in rounds 7–12.** The two picks Matt wishes he had
account for **175.6** of Cary's deficit on their own.

---

## 3. THE GRADER HAD SIX ANSWERS FOR SIXTY-TWO PICKS, AND FIVE OF THE SIX WERE TIGHT ENDS

`[TESTED, n=62 picks, rounds 7–12, all 12 managers, `draft_analysis.json`]`

Every "gap" in the grade is *this player's VOR minus the best available VOR at that moment*. Across
the entire back half of the draft the grader named **six** players as best-available:

| best available | times | pos |
|---|---|---|
| **Dallas Goedert** | **34** | TE |
| Patrick Mahomes | 11 | QB |
| Jake Ferguson | 8 | TE |
| Kyle Pitts Sr. | 7 | TE |
| Kenyon Sadiq | 7 | TE |
| T.J. Hockenson | 3 | TE |
| Rico Dowdle | 1 | RB |

**50 of 62 (81%) are a tight end.** The grade's answer to the entire second half of every draft in
this league was *"you should have taken a backup tight end"* — the one move §6's doctrine forbids,
§4.3 says carries no premium past TE4, and §4.18 prices at a **+6 to 0** keeper ceiling.

**So the grade measures dart count, not drafting.** Share of each manager's charged gap that falls
in rounds 7–12:

| manager | total | rds 7–12 | share |
|---|---|---|---|
| **ChatCTE (Cary)** | 455.5 | 399.3 | **88%** |
| Multiple Scorgasms | 326.6 | 273.3 | 84% |
| **The Poetry of Junkyard Juggers (Matt)** | 212.0 | 199.9 | **94%** |
| Breece up those Tets | 186.3 | 95.0 | 51% |

**RETRACTION — a number that must not be quoted again (§0.1):** Cary's draft grade, his last-place
finish, and every other manager's back-half grade. The front half (rounds 1–6, against real ADP and
real replacement) survives. **Rounds 7–12 of the grade are void.**

---

## 4. THE FLAG COVERS ONE ARCHETYPE, AND THREE REPLACEMENTS ALL FAIL FOR ONE REASON

`dart_shape` is set on **12 of 471** players. All twelve are **backup running backs** with a lead
back listed ahead of them: Monangai, Jonathon Brooks, Rachaad White, Jordan Mason, Spears,
RJ Harvey, Pacheco, Brian Robinson Jr., Allgeier, MarShawn Lloyd, Jonah Coleman,
Mike Washington Jr.

**That is doc 224's archetype exactly — "one injury away" — and it is the only one the sheet can
see.** A man who already holds a big job at a fabricated price is invisible to it by construction.
Doc 224 built the lane around the shape Matt named and I never asked whether there was a second
shape. **Tyson is the second shape.**

Three candidate replacements, run today:

1. **Rank depth-1 players by `job_ceil`.** FAILS. `job_ceil` is a **team constant** — every DET row
   reads 332, every ATL row 315, every SF row 302. Ranking by it surfaces whole offences, and the
   top 14 came back Goff, TeSlaa, Dotson, Zaccheaus, Penix, Deebo, Kirk, **Juszczyk**. No Tyson.
2. **"His team's top projection at his position AND priced past 120."** FAILS. 32 names, and
   **Tyson is not one of them** — Vele out-projects him.
3. **"Chart slot 1 but NOT his team's top projection"** — the contradiction itself. FAILS. 83 names,
   and **eleven are fullbacks** (Juszczyk, Ricard, Ingold, Beck, Prentice, Bredeson, Luepke,
   Nowakowski, Gilliam, Burton, Heyward), because `depth` is a chart-slot field polluted by
   position-group granularity: a fullback is slot 1 at his own listed spot.

**THE COMMON CAUSE: `depth_map.csv` carries the SIZE of the job (team constants) and a chart slot.
It carries nothing that says how much of that job is HIS.** Every instrument above is an attempt to
infer a per-player share from two fields that do not contain one.

---

## 5. THE RED TEAM ON THE IDEA ITSELF (§0.5a) — AND WHY TYSON SURVIVES IT

**The signal class Matt was reaching for at the table is one this project already measured and
retired.** §4.13 tested "the market is sleeping on him" (ADP rank minus projection rank) on 324
player-seasons: it was the **worst** of three signals, **rho −0.079**, and its coldest quintile broke
out at 3.1% against a ~11% base. §4.22(b) replicated it on a different market at **−0.173,
p<0.001, n=409**. **When the market and the projection disagree, the market is the one that is
right.** A finder built on cheap-versus-projection loses money, measured twice.

**But Tyson is not that shape, and that distinction is the whole point.** Cheap-vs-projection needs
the two numbers to disagree. On Tyson they **agree** — 82.0 points and a sentinel price, both
saying no. What says yes about him is something neither number carries.

**THE TESTABLE FORM, STATED AND NOT YET RUN (§0.5a2) — needs Matt's yes before I spend it:**

> *A rookie wide receiver taken in the first two rounds of the NFL draft who is listed as his
> team's week-1 starter beats what his preseason fantasy price predicts.*
> **POPULATION:** rookie WRs, 2021–2025, with a §1.1 registry preseason ADP.
> **BASELINE:** half-PPR weeks 1–14 minus what `log(preseason ADP)` predicts, fit within season.
> **DIRECTION:** positive. **Falsifier fixed in advance:** under +15 points → the shape is dead and
> I say so.

This is **draft capital plus role**, which is §4.13's own live RB composite (`NFL rounds 1–3`) — a
component the project already trusts at running back and **never extended to receivers**. n is
roughly 10–14 rookie WRs a year inside the drafted range, so **50–70 seasons: thin, and I am saying
so before the run, not after.** nflverse's draft-picks release is reachable from here.

---

## 6. WHAT THIS DOES NOT EXCUSE

Matt's self-criticism was *"I was very busy trying to define how to find those gems ... instead of
research I should have."* **Defining the finder was the right use of his time. The finder we shipped
was mine, and it flagged twelve backup running backs.** The research gap is real and secondary;
the instrument gap is mine and is primary.

---

## 7. OPEN THREADS THIS ADDS

- **The Aug-8 depth chart is a month stale** (carried from docs 236, 241) and it is the input to
  every claim in §1 and §4. New Orleans' WR room in particular may have moved.
- **`draft_analysis.json`'s back half needs a real comparator** — not the next-best VOR, since 81%
  of the time that is a tight end nobody should take. Post-season work, not now.
- **Jordyn Tyson's actual NFL draft round is not in any project file.** It is the load-bearing input
  to §5's test and I have not fetched it.
- Whether `depth_map.csv` can carry a per-player share at all, or whether that needs a target-share
  source outside the ESPN pull.
