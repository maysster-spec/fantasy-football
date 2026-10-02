# 173 — Red team, T−2. The roach count, measured.

**Date:** 2026-09-05 (Sat night ET) · **Trigger:** Matt, on the Lloyd miss: *"If you see one roach
there could easily be 100."*

**There are not 100. There are two that move a pick, one that is worse than Lloyd, and one whole
LAYER that is stale — the injury flags.** Counted, not swept.

---

## LADDER A — THE BOARD'S OWN DATA vs TODAY'S PULL. **All six run, tonight, no research needed.**

| # | check | result |
|---|---|---|
| A1 | projections | 27 rows moved ≥15 pts, 12 ≥30, **6 cross the 180-row printed cut** |
| A2 | teams | 27 differ — but **22 are `WAS` vs `WSH` notation**. 13 real changes, **all rank 188+, none inside the printed board** |
| A3 | positions | **0.** Clean |
| A4 | **injury flags** | **23 rows INSIDE the printed 180 disagree. Three are now on IR.** ← the real finding |
| A5 | missing players | **0** non-keepers with a real ADP are absent. The board's roster is complete |
| A6 | ADP | **CORRECT AND VERIFIED.** `check_adp_vintage.py`: 0 rows disagree, max 0.00. My earlier claim that it was stale was measured off a stale local copy of the board and is RETRACTED — see doc 172 |

### A1 — the six that cross the printed-board cut

| player | board rank | true rank | Δ proj | verdict |
|---|---|---|---|---|
| **MarShawn Lloyd** | 184 | **131** | **+46.2** | **missing from the paper, belongs on it** |
| **Isiah Pacheco** | 143 | **208** | **−48.3** | **ON the paper and should not be — and he is now on IR** |
| Kayshon Boutte | 188 | 143 | +41.1 | missing, but ADP 170.6 = §4.14 sentinel, ordering is fiction there |
| Erick All Jr. | 192 | 180 | +7.9 | boundary, sentinel ADP |
| Tyler Allgeier | 179 | 181 | +1.2 | boundary noise |
| Xavier Legette | 180 | 183 | −0.001 | boundary noise |

**Pacheco is worse than Lloyd.** Lloyd is absent — you notice absence when you go looking, as Matt
did. Pacheco is *present*, ranked 143, sitting in the pick-128 neighbourhood, and the board would
offer him. **A wrong row that looks right beats a missing row for damage.**

### A4 — the layer nobody was checking

The board's `flag` is Aug-23 vintage. Against today's pull, **23 of the top 180 have changed**:

**Got worse (9):** Ja'Marr Chase **rank 6 → QUESTIONABLE** · D'Andre Swift · Bhayshul Tuten ·
Rome Odunze · Tee Higgins · TreVeyon Henderson · Carnell Tate · Jonathon Brooks ·
Wan'Dale Robinson · Josh Downs · Terrance Ferguson · Keaton Mitchell
**Now on IR (3):** **Isiah Pacheco** · **Tank Dell** · **Jordyn Tyson**
**Got better (7):** Quinshon Judkins · DeVonta Smith · **Alec Pierce (OUT → ACTIVE)** ·
Parker Washington · Xavier Worthy · Quentin Johnston · Makai Lemon · Cade Otton

**Seven of those sit at picks 8–65.** This is a bigger surface than the Lloyd projection miss and
nothing in the kit compares these two columns.

**IR IS NOT AUTOMATICALLY A REMOVAL, and this is Matt's call not mine.** §6: the three IR slots are
separate from the bench and a PUP/IR stash costs nothing. Doc 115 already ruled that **Tank Dell is
AVOID as a draft pick and still a legitimate IR stash at 152 or 161.** So do **not** blanket-zero
the three. Pacheco is the one that actually misprices a pick.

## LADDER B — THE NEWS LAYER. Needs external checking, so it batches.

**BATCH 1 is his own trusted list**, cross-checked against the board tonight before any searching:

| "My Guy" | host | board says | flag raised |
|---|---|---|---|
| **Colston Loveland** | Mike | — | **KEEPER (Rychlicki). Not draftable in this league at any price.** Mike's #1 guy is unavailable |
| **Carnell Tate** | Jason | ACTIVE | **ESPN says QUESTIONABLE** — one of A4's 23 |
| **De'Zhaun Stribling** | Andy | VOR −55 | **really −29** (+26 stale), already LADDER + DISCOUNT |
| Kenneth Walker III | Mike | +81.2, rank 13 | clean |
| Christian Watson | Mike | −5.9, LADDER, DISCOUNT | clean, flags already carried |
| Garrett Wilson | Jason | +36.4, rank 30 | clean |
| Omarion Hampton | Jason | +67.3, rank 21 | clean |
| Caleb Williams | Andy | −9.7 | clean |
| Ladd McConkey | Andy | +17.7, rank 45 | clean |

**Three of nine raise something, and one of them is fatal to the recommendation** — no amount of
Loveland analysis matters if Rychlicki keeps him. **Six are clean**, which is the useful half of a
red team: it says where not to spend Sunday.

**B2 — the 23 stale flags, in pick order**, verified against beat reporting, not aggregators.
**B3 — every AVOID/DISCOUNT grade's date**, since the sweep that set them is 08-31.
**B4 — the Gemini-sourced claims re-checked** (Matt's point 3: the Nacua contamination was Gemini's,
found by him; doc 166's two-primary-report rule now applies to anything legal or disciplinary).

## LADDER C — WHAT WE CHANGED THIS WEEK THAT MAY NOT HAVE CARRIED

C1 the grid's three adjustments and the override marker · C2 `sync_desk_copies` now owns
`ADP_GRID.pdf`, and `tidy_docs` derives its protected list from it · C3 `audit_directive.py`
against the shipping files · C4 the pins re-set today (`sync_desk_copies`, `mkvalue`, `tidy_docs`).

## THE ORDER, AND WHY

1. ~~Fix ADP first~~ — **already correct. Verified, nothing to do.**
2. **A1 and A4's live rows**, because they misprice real picks: Pacheco and the 23 stale flags.
3. **Then batch B1**, already scoped above.

## WHAT THIS RED TEAM DID *NOT* FIND

No missing players. No position errors. No team errors inside the drafted board. ADP drift ≤2 picks
where it is printed. **The board's structure is sound; its NEWS is a week old.** That distinction is
the finding — it says fix the news layer and leave the machinery alone at T−2.
