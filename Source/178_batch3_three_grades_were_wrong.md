# 178 — Batch 3: three AVOID grades were wrong, and one of them was a 2025 article

**2026-09-05 (T−2).** Batch 3 of the red team: the **40 AVOID / DISCOUNT grades inside the printed
180**, almost all stamped **2026-08-31** and therefore five days old. A grade here is not decoration
— `HOW_TO_READ_IT` defines **AVOID = "do not draft him at this price"** and **DISC = "worth taking
later than this rank"**, and `live_draft.py:875` **silences a player's analyst up-calls** whenever
his grade is AVOID. A wrong AVOID does not just mislead; it deletes the evidence that would correct
it.

Worked the eight closest to Matt's picks. Two ran as parallel verification agents under a fixed
protocol — **publication date established before any source is used**, verbatim quotes only,
"NO CURRENT SOURCE FOUND" permitted, disagreements reported rather than resolved. Every
pick-changing result was then re-checked by hand.

---

## 1. Three grades were wrong. All three are corrected in the file.

### George Kittle (TE, SF · adp 72.4 · live at picks 65 and 80) — **AVOID → DISCOUNT**
The card said *"Achilles, age 38, out right now."* **Both facts are false.**
- **He is 32.** Born **1993-10-09** (Wikipedia). Where "38" came from, nothing in this project can
  say. It is a fabricated number that survived onto a printed sheet.
- **He is not out.** Back in team drills **Aug 31**, flew to Australia with the club **Sept 2**.
  Ian Rapoport, Sept 2: *"Kittle is trending in the right direction to play."* GM John Lynch,
  Sept 1: *"Yesterday was the first time he got involved in team reps, and we plan to continue
  that moving forward."*
- **What survives:** the Achilles tore on **2026-01-11** in the Wild Card round. Eight months is
  fast, and early-season workload management is a real risk. **That is a DISCOUNT, not an AVOID** —
  wait on him, do not cross him off.
- One outlet (footballnationusa) still had him on PUP and unpadded on a page claiming a Sept 2
  update, against five corroborating Sept 1–2 sources. Recorded as a disagreement, not weighted.

### J.K. Dobbins (RB, DEN · adp 111.6 · live at picks 104 and 113) — **AVOID → DISCOUNT**
The card carried `NEWS 09-03: ... reported on September 2 that the injury could force him onto
Injured Reserve.` **There is an ESPN story with exactly that headline. It is dated 2025-11-15**
and describes a foot injury from a hip-drop tackle in a Thursday-night game against the Raiders —
**last season, a different injury.** No 2026 IR placement exists; Denver carried him through the
Aug 31 cutdown. Sean Payton, **Sept 2** (via Chris Tomasson, Denver Gazette): Dobbins is
**"moving well"** and expected for Week 1.
**This is the exact failure Matt warned about** — *"we have found more than once now"* that the
sweep repeats something wrong — **and it is the same failure I nearly committed twice myself
today** (a Chase piece from Sept 2024, a DeVonta Smith piece from Nov 2025). Three instances of one
defect in one day, in three different pipelines. `ERROR_PATTERNS`: **a fantasy injury headline is
almost year-agnostic; the date is the only thing that distinguishes them.**
What survives: ACL and Lisfranc history is real. DISCOUNT.

### Brian Thomas Jr. (WR, JAX · adp 113.6 · live at picks 104 and 113) — **AVOID → NEUTRAL**
Matt asked directly: *"Brian Thomas is both a buy and an avoid... Has it been the same ankle?"*
**There is no 2026 ankle injury.** The August issue is a **shoulder** — he landed on it catching a
40-yard touchdown in the joint practice with Tampa on Aug 25. Liam Coen, **Sept 2**:
*"B.T. was full go yesterday. No issues."* Coen, Aug 26: *"Just came down on his shoulder. Holding
him out was smart."* The only ankle on his record is **Nov 2, 2025, Grade 1, three games missed.**
So the answer to Matt's question is: **the AVOID was keyed to last season's injury, and the buy
signal was the honest half.** Grade removed.

---

## 2. Five grades hold. Two of them got worse, one got better.

| player | adp / Matt's pick | verdict | the line that decides it |
|---|---|---|---|
| **Jeremiyah Love** RB ARI | 25.9 · 17→32 | **WORSE** | Still not practising Sept 1 — present in street clothes. Mike Garafolo, Sept 1: **"I'll put it at about 50-50"** for Week 1, *"Nobody really knows right now."* |
| **Emeka Egbuka** WR TB | 44.9 · 41 | **WORSE (and the note was the oldest on the board, Aug 18)** | Todd Bowles, **Sept 3**: *"They're headed in the right direction — I don't know how fast. I'll have a better gauge next week."* Two days before Matt drafts, Tampa still cannot say. One outlet says sprained toe, not turf toe. |
| **Ashton Jeanty** RB LV | 21.8 · 17 | **BETTER** | Klint Kubiak, **Sept 3**, asked if he is optimistic for Week 1: **"Yes."** GM John Spytek, Sept 1: *"I think he's in a good spot... It's hard to knock him down."* Not a full practice participant yet; low-vs-high ankle still unresolved between outlets. |
| **Breece Hall** RB NYJ | 36.0 · **32** | **HOLDS, one caveat** | As of **Sept 2 he had still not returned to practice.** Aaron Glenn says he *"will be ready"*; NYJets.com expects him starting at Tennessee. §7's *"Hall on sight if he slips"* stands — **eyes open, not blind.** |
| **Malik Nabers** WR NYG | 35.1 · 32 | **HOLDS** | Harbaugh calls Week 1 *"reasonable to assume."* **Nabers himself, Sept 1:** *"there are still some things that you're going to have to check off the box for you to participate."* The team is more confident than the player. Doc 140's availability sensitivity already moved him +$27 → +$3; this is why. |

---

## 3. What this means for Monday, in pick order

- **Pick 32** — the tie is unchanged (Bowers · McBride · Kyren · Judkins · Lamar, Hall on sight).
  **Judkins is clean** (doc 177: the ankle was precautionary, Monken on record). **Hall carries a
  no-practice caveat.** **Nabers is a hedge, not a name in the tie.** Nothing here reorders it.
- **Pick 41** — **Egbuka is the one to be careful with.** He was already CI-clear behind the pick-32
  tie at −$20; now his own coach will not commit two days out.
- **Picks 65 / 80** — **Kittle comes back onto the board as a wait-for-him**, not a cross-off. He is
  still TE and §4.3 still says do not pay for TE5–TE10; this changes the reason, not the ranking.
- **Picks 104 / 113** — **two names come back**: Dobbins (no IR, "moving well") and Brian Thomas Jr.
  (healthy, and the analyst buy is real). Both were being silenced by a wrong AVOID. This is the
  same neighbourhood where doc 177 put **Alec Pierce** back on the board and took **Kyle Monangai**
  off it. **The 104/113 window moved more than any other on this board today.**
  §4.18's draft-night rule is untouched: a Goff-tier QB2 still comes first there if one is present.

---

## 4. Standing and honesty

`[SOURCED]` — 23 dated facts across docs 177 and 178, publication date read on every one.
`[TESTED]` — 3 grades changed, each against at least two independent September reports.
`[CORRECTED]` — one fabricated age (Kittle, 38 → 32), one stale-article citation (Dobbins),
one mis-keyed injury (Thomas, ankle → shoulder).
`[OPEN]` — Jeanty's ankle severity (low vs high) is contested; Love is a genuine coin flip;
Egbuka is unresolved and may stay unresolved past the draft.
**Not done:** 32 of the 40 AVOID/DISCOUNT rows are still on their Aug-31 stamp. The eight worked
here were chosen by proximity to a pick, and three of eight were wrong — **so the base rate on the
untouched 32 is not zero.** The ones nearest a pick are done; the rest are a post-draft job.

---

## 5. Shipped

- `player_context.csv` — 5 cells: three grades, and two `why` texts stripped of the false claims.
  Pre-edit copy archived to `_archive\player_context_20260905.csv`.
- `Source\redteam_sept5.csv` — **all 23 dated facts, docs 177 and 178 merged into one file.**
  Dry-run against the live context file: **23 rows updated, 0 unmatched.**
  (`redteam_batch2.csv` was the intermediate and is superseded by it.)
- `check_kit.py` — re-pinned for both `board_v8_fixed.csv` and `player_context.csv`.

**One command:**
```
cd "G:\My Drive\_Fantasy\2026\Scripts"
py apply_research.py --findings ..\Source\redteam_sept5.csv --write
```
then rebuild the paper, then `py check_kit.py`.
