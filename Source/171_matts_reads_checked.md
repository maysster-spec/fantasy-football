# 171 — Matt's roster-construction reads, checked one at a time

**Date:** 2026-09-05 (Sat evening ET) · **Trigger:** Matt used the new grid to lay out his actual
decision process and asked to be corrected where he was wrong.

**Two of his reads are right, three are wrong, one is a NULL — and testing his RB question found a
defect in the grid I had shipped him an hour earlier.**

---

## 1. "IS OUR LEAGUE MORE RB-HEAVY, SO WRs FALL TO ME?" — **NULL** `[TESTED, n=274, 2 drafts]`

The most actionable thing he asked, and §4.12 left it open: *"RB/WR pace gaps rest on 2 drafts —
left uncorrected, `[HYPOTHESIS]`."*

**POPULATION:** `picks_with_adp.csv`, true selections only (`Keeper == False`), **consensus ADP
only** — never `adp_espn`, per §1.1. **BASELINE:** `resid = Pick − ADP`; negative = this league
takes him earlier than the market. Controlled for `log(ADP)`, because a top-5 ADP player cannot
have a large negative residual. Reference position = WR.

| position | vs a WR at the same price | se | t |
|---|---|---|---|
| RB | **−1.58 picks** | 3.48 | −0.45 |
| TE | −5.92 | 4.83 | −1.22 |
| QB | −4.45 | 4.87 | −0.92 |

Raw means are near-identical too: RB +4.93, WR +5.18. **No RB bias. His intuition is not supported.**

**AND THE SAMPLE DID NOT GROW.** `ADP_source == 'consensus'` covers **2022 (n=130) and 2023
(n=140); 2024 has 3 rows and 2025 has 1.** So this is the same two drafts §4.12 already flagged.
`[UNDERPOWERED — an effect under ~7 picks is invisible here.]` **Do not plan on WRs falling.**

## 2. BUT THE QB EFFECT IS REAL, AND IT FILLS A GAP THE DIRECTIVE NAMES

Restricting to **ADP ≤ 60**, where Matt actually picks, and controlling for price:

| | vs a WR at the same price | se | t | n |
|---|---|---|---|---|
| **QB** | **−14.71 picks** | 5.02 | **−2.93** | 11 |
| TE | −8.02 | 5.69 | −1.41 | 8 |
| RB | −3.57 | 3.23 | −1.11 | 40 |

**Inside ADP 60, a quarterback goes about 15 picks EARLIER than a receiver at the same price.**

**This is exactly the hole doc 142 §4a named:** *"QB survival rests on raw ADP plus noise — §4.12
fits a TE shift and Snyder-on-Allen and **nothing for QBs generally** — while §5's timing table has
four managers taking their first QB in rounds 2.5–3.2."* Two independent things now agree: the
behavioural table, and the residuals.

`[TESTED, n=11, 2 drafts — UNDERPOWERED on its own. What carries it is the corroboration and a
clean t, not the sample.]` Bounded by §4.15's QB2→QB6 plateau of 11.8 points, so the cost of being
wrong about it is small in both directions.

**What it does NOT do is resurrect "target pick 41."** That number was a draft-card artifact with
no source until doc 82 removed it, and §4.15's structure is unchanged: one cliff at QB1, then a
plateau. Measured on the shipped board, best QB still available at each of his turns:

**41 → Burrow +28.9 · 56/65/80 → Stafford +21.2 · 89 → Nix +7.4.**

**The QB cliff is 80 → 89, not 41.** Waiting from 41 to 80 costs ~7.7 VOR; waiting from 80 to 89
costs 13.8. Take one when value shows; do not schedule it, and do not count on Stafford at 80 now
that the drain is measured at 15 picks faster than the price implies.

## 3. THE TEST FOUND MY OWN DEFECT: THE TE SHIFT IS BANDED, NOT FLAT

Doc 170 applied §4.12's **TE +15** to all 19 tight ends on the grid. Checking it against the same
data says that was wrong:

| ADP band | TE mean resid |
|---|---|
| 1–24 | +14.9 |
| 25–60 | +6.4 |
| 61–120 | +2.2 |
| **121+** | **−19.3** |

And the sharper cut — **§4.7 is about the FIRST TE, not all TEs.** The first tight end off the board:
**Kelce +16.0 (2022), +13.8 (2023)**. That reproduces §4.12's fitted +15 almost exactly, *at the
top of the draft*, and the sign **inverts** past ADP 120.

**One number, two opposite signs.** The shift is now gated to `adp_pick ≤ 60`. Adjusted cells drop
from **20 to 8** (3 TE, 4 QB, 1 Snyder) — every one of them now sits where its number was fitted.

**This is the §0.2 pattern in a place I created it:** I quoted a directive parameter as a flat
positional law without checking the population it was fitted on, and shipped it.

## 4. THE GRID NOW SHOWS WHEN ITS OWN VOR IS STALE — Matt's Lloyd question

He asked whether MarShawn Lloyd was missing or a keeper. **Neither: cell 93, round 8, DART,
UNSETTLED job worth 152.** But his VOR reads **−90**, and on the current pull he is **−44** — the
board's projections are the Aug-23 spine and cannot be rebuilt before the draft (docs 62/143/144).

A 46-point error at his pick 89, invisible. The grid now prints the corrected number in blue
(`−90 →−44`), read from **`override_card.csv`** — `mkoverride.py`'s own output, so the page and the
printed OVERRIDE CARD cannot disagree. Four cells inside the drawn range carry it, and one of them
is a correction **downward** in Matt's own pick-128 cell: **Isiah Pacheco −54 → −102.**

## 5. HIS OTHER READS

| his read | verdict |
|---|---|
| **Not taking Davante Adams at 32** | **Right, wrong reason.** §7 already has him **−$14 CI-clear behind** the five it ranks there. The age-injury premise is not testable here, and what *is* measured cuts against the general form: mean games played is **12.94 RB vs 12.95 WR** (§4.23) and Adams played **14 games in 2025**, so he carries no availability flag. Pass on the dollars, not the birthday |
| **James Cook at 8** | Cook is **+93.0 VOR** against St. Brown's **+101.3**, and goes ~2 picks later. Pick 8 is closed by three unrelated routes and the largest margin on the board (**20 points**, 10/10 seeds). An 8-point VOR gap is consistent with that; it is not a live question |
| **"WR nose-dives after 65"** | **Nearly right, one turn late.** Best WR still there at **65 is Sutton +6.2**; at **80 it is Pierce −7.1**. The cliff sits *between* his 65 and 80 — he can still take a startable receiver at 65 |
| **Burden in round 5** | His `eff_pick` is **65.2** — likelier at **65 than 56**. And see below |
| **Burden AND worried about Odunze** | **These are the same bet, twice.** Both are Bears. `[SOURCED: SI, Sept 2026]` Odunze sits behind **Burden and Colston Loveland** in the target pecking order but still holds *the highest target share of the trio*. **The rookie he is worried about is not on Chicago — Carnell Tate went to Tennessee.** Loveland is Rychlicki's keeper, so he eats Bears targets without ever being draftable |
| **TreVeyon Henderson "boom or bust"** | **Cannot confirm or deny.** §4.13d: nothing in this project computes a ceiling or a floor, and the analyst panel cannot stand in for one. Henderson is **+9.3 VOR to Burden's +4.8** and carries DISCOUNT (has not practised since Aug 24). "Big-play dependent" is a human read with no metric behind it — which is a legitimate reason to pass, as long as it is called that |
| **Pollard / Dowdle / Warren** | All three inside **3 VOR**: Warren **0.0**, Pollard **+2.3**, Dowdle **+2.8** — noise. Note ESPN projects **Dowdle above Warren** while the depth chart lists Dowdle behind him. §4.20: **buy the job, never the name** — measured on 19 unsettled backfields, the flag has no opinion on who wins |
| **Brooks over Hubbard at 7** | **Board agrees, marginally.** Brooks **−14.2**, Hubbard **−16.3**, and it is **Hubbard** carrying the QUESTIONABLE flag now, not Brooks |
| **Brian Thomas Jr. — "repeated ankle injuries"** | **Not supported.** `[SOURCED: DraftSharks injury history]` **One** ankle event on record: Nov 2 2025, Grade 1, three games missed. No prior ankle. Listed **Active**, ~1.9 projected games missed. **The AVOID on his card is not the ankle — it is a LEFT SHOULDER dated 08-31** plus "history of multiple 2025 injuries". He also played 14 games in 2025, so no availability badge. The BUY and the AVOID are about different body parts |
| **Does the rollout solve roster construction?** | **Largely yes, and it is the measured winner** — rollout + `CAPS` beats static VBD by **+4 to +9 points** and opens RB-RB-RB in 64–65% (§4.10). Two blind spots to hold: it models **byes and no other absence** (§4.18c), and `CAPS = {QB:2, TE:2}` encodes his QB/TE doctrine but nothing else about his preferences |
| **Is DRAFT_BOARD's "PLAN FOR THE PAPER" current?** | **Yes as of today** — it was rebuilt this morning off the 09-05 ADP. It stops being current at **7:00 PM Monday**, when the keeper swap changes the pool |

## 6. WHAT DID NOT CHANGE

No change to the board, the engine, `news_overrides.csv`, or any draft-path file. Everything above
is the grid (a reference sheet) and this doc. §4.18c stands: **do not change what the objective
measures before Sept 7.**
