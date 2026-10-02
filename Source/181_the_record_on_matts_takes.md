# 181 — Fact-checking Matt against the record, and what "fill RB" actually says

> **BANNER, 28 Sept 2026 (doc 435).** This doc says forcing RB at pick 8 *"costs about 20 points"*. **The size was never established and must not be quoted (§4.2, doc 182); only the direction holds.** Kept as a dated record.

**2026-09-05 (T−2).** Matt asked to be fact-checked on two things he believes about himself and
this project: that his early takes were often wrong, and that we agreed filling RB drives
season-long success. He asked for a top recommendation instead of a menu. All three answered
from the ledger, not from impression.

---

## 1. "My early takes turned out to be wrong in several cases"

**Partly true, and the pattern is worth more than the verdict.** Sorted by what the tests said.

**WRONG — tested and killed:**

| his take | what the test said |
|---|---|
| "Barkley broke out two years after the injury" | §4.22(d), doc 130. Year-2 cohort **NULL** (C vs A +2.4, p=0.77). And Barkley 2022 went at ADP rank **19 against projection rank 36 — a 17-slot PREMIUM**, not a discount. |
| The offensive line drives QB production | §4.24, docs 132/133. Sack rate *is* the most persistent team trait measured here (r=+0.399) — but the payoff test is **r=+0.092, p=0.53**. Failed on power, not prediction. Opening-day OL injuries: **twelve tests, no p below 0.33.** |
| "Opportunity environment" should be a flag | §4.21, doc 128. Team pass volume is **7.5%** of the variance; the player's own share is **93%**. **No new flag.** |
| "Our league is more RB-heavy than average" | doc 175, this session. Keeper-adjusted, five seasons, n=680: **RB is NULL in every band.** It is **WRs** that go early (+3.5 / +6.6 / +5.8, all significant). Real as an experience, wrong as a mechanism. |
| "I'd rather have Brooks over Hubbard" | doc 179. Both QUESTIONABLE; Canales describes a series rotation; ESPN's Graziano picks **Hubbard** if healthy. Leans against him, and it is thin. |

**RIGHT — tested and held, or found a real defect:**

| his take | what happened |
|---|---|
| The market is anchored on last year's points, beyond the projection | §4.22(b), doc 129. **Confirmed** — last year loads +0.093/+0.263 after the projection — and fading it **LOSES** (rho −0.173, p<0.001, n=409). This led directly to the one injury signal this project can test, prior-season games played, which the board now carries as the `12g` badge. **His read produced a shipped feature.** |
| "Doc 92 never prices keeper value" | §4.18. He was right: the word "keeper" appears **zero times** in it. The gap was real. (It later measured at ≈ +0.7 rather than +8, so the *hole* was real and the *size* was not — but he found the hole.) |
| Josh Jacobs is a hard pass | This session. His reason was better than mine: an exempt-list player has **no IR designation**, so the best case still burns a bench spot all season. I had offered him a choice; he closed it correctly. |
| "His VOR is −90, lol. He's a starting RB for GB now" (Lloyd) | Correct. True range **+0 to +50 VOR**, and the paper could not show him at all (rank 184 past a 180-row cut). **This one call triggered batches 2–4, which found nine more defects.** |
| "Not much chance I take Davante at 32" | §7 has Adams at **−$14, CI-clear** behind the pick-32 tie. Right. |
| Value ladder page 2 is mostly empty | Real defect — the page-break estimator never counted the header block. 4 pages → 3. |
| "My ask wasn't RB vs WR, it was RB vs normalized ADP" | He was right and my test design was wrong; the contrast I ran cancels the shift the whole board shares. |
| "If you see one roach there could easily be 100" | Batches 2–4: a false OUT on Alec Pierce, three IR players showing Q/D, a fabricated age on Kittle, a 2025 article driving an AVOID on Dobbins, an AVOID keyed to the wrong body part on Brian Thomas, Monangai's knee unpriced, Kraft written off. **Nine.** |

**THE PATTERN, and it is the useful part.** When Matt says **a price is wrong or a process is
broken**, he has been right nearly every time — Lloyd, Jacobs, Adams, the ladder, the test design,
the market anchor, the keeper gap. When Matt proposes **a causal mechanism** — the line, the
environment, the year-two bounce-back, RB-heaviness — it has tested null nearly every time.

`ERROR_PATTERNS` **F4** already says *"his instinct has a track record — treat it as evidence."*
**It should say which instinct.** His pricing and process instincts are evidence. His mechanism
hypotheses are hypotheses, and the project has been good at testing them and honest when they died.

**So the self-assessment is too harsh.** "Rusty, stale ideas" does not describe someone whose
market read produced a shipped board feature and whose one-line challenge on Lloyd exposed nine
defects two days before a draft.

---

## 2. "I thought we both agreed filling RB would lead to season-long success"

**Half of this is established and the other half is the opposite of what the board says.**

**What IS established:**
- **§4.10:** the two winning pick rules open **RB-RB-RB in 64–65%** of drafts — an independent
  replication of the "RB in rounds 2 and 3" finding on a different simulator.
- **Zero RB, Hero RB and pop-and-trade are all dead.**
- **Bench RB to the cap, then WR** — §4.19, on **his own** waiver record: **four of five RBs he
  adds never give him a startable stretch.** League-wide, doc 12: waiver hit rate **RB 22%,
  QB 62%.** The argument is defensive: *an RB hole cannot be patched mid-season and a QB hole can.*
- **§4.17b:** his top-two drafted RBs are short **5.54 slot-weeks** a season.

**What CONTRADICTS "fill RB" as a rule:**
- **Pick 8 is a WR.** Amon-Ra St. Brown, **10/10 across ten seeds and three sample sizes, margin
  19.96 → 20.20** — the largest margin anywhere on this board by an order of magnitude, reached
  three independent ways (dollars, the rollout, doc 140's state generator agreeing 96/100).
- **§4.10 again:** static VBD **with no caps** drafts 1.46 WRs and **loses 8.7 points.** The rule
  that wins is *best player subject to caps* — not *load a position.*
- **doc 175:** in **his** league, WRs go **early** and RB is null in every band. That means RBs are
  relatively **available** at his picks and WRs relatively **scarce.**
- **§4.18b:** the "a hit RB dart is a +85 keeper" argument **died** — measured at **+6.7 VBD14**,
  so the option is ≈ **+0.7**. RB is not keeper gold either.
- **§4.23(a):** the RB-over-WR calibration tilt has a **CI including zero. "Do not tilt the board."**

**The honest synthesis: RB-RB-RB is an OUTPUT of the rollout, not an input to it.** The engine
drafts that way *when the board offers it*. At pick 8 the board does not, and forcing RB there
costs about 20 points against the engine's own recommendation.

**What survives, in one sentence:** take the best player the board offers early, expect that to be
RB in rounds 2–4 more often than not, and spend the **bench** on RB — because that is where the
waiver wire cannot save him.

---

## 3. "I'd much rather take your top recommendation for a VBD"

**VBD is not the top recommendation, and this is measured, not stylistic.** §4.10 raced the pick
rules: the **rollout beats static VBD by +4 to +9 points**, ≈ $15 of expected payout. VONA loses
8.8, the need-penalty loses 5.7, following ADP loses 24.5.

- **On the night: the live board's own ordering is the recommendation.** It sorts by the rollout.
  The visible form is **`cost vs #1`**, and **`free` is the pick.**
- **VOR (the `VBD` column) is the fallback** — for when the tool is down, or as a sanity check on
  a row that looks wrong.
- **The one number to distrust is Δ.** It is tempo, not the sort key; showing it as the headline
  once made the biggest bar on the page belong to a row the engine did not pick (doc 79).

**The plan, from the dollar studies that exist:**

| pick | what the work says |
|---|---|
| **8** | **St. Brown. Closed** — do not open it again (§4.2, docs 70/139/140). |
| **17** | **Henry if there (8%). Else Walker or Jeanty** — one of them is there in 65% of drafts, and Walker over Hall is **+$14–15, CI clear.** If none of the three (35%): **Love ≈ Hall, take whichever shows first.** Do **not** override for Chase Brown or Lamb. (doc 150) |
| **32** | **Take the engine's #1.** The tie is Bowers · McBride · Kyren · Judkins · Lamar, **plus Hall on sight** if he slips; policy spread across all five is **$2.7**. **Not** Burrow (−$24), Stafford, Daniels, Egbuka, Swift, Hurts, Warren, Adams or Smith — all CI-clear behind. The engine's #2 row here is a **QB in 47 of 100 states**; ignore it. (docs 140/142) |
| **41–89** | **No pick-specific study exists.** Follow the board. This is the honest gap. |
| **104 / 113** | If he still has no QB, **Bo Nix is the best one there** (+7.4 VOR, healthy, unquestioned starter — doc 179). If he already has one, §6's doctrine governs and the answer is the board's best RB/WR. |
| **128 / 137** | Darts. §4.13: risk **from round 9, never before.** |
| **152 / 161** | D/ST, then K. §4.8/§4.9. |

---

## 4. What is NOT established, said plainly

- **Picks 41 through 89 have no dollar study.** Only 8, 17 and 32 do. Four of his fourteen
  selections are backed by simulation; the rest are backed by the board.
- **Never quote a simulated absolute win probability** (§5) — the board and the scoring share one
  projection, so absolute numbers are artifacts. Relative comparisons only.
- **Season luck is 6× draft luck** (§4.13). Corrected for sampling error, the spread in title odds
  between one good draft and another is **zero**. The draft is worth getting right because it is
  the part he controls, not because it decides the season.

## 5. Standing

`[TESTED]` — every row in §1's two tables traces to a numbered doc.
`[MEASURED]` — §3's rule ranking is §4.10's race, not a preference.
`[OPEN]` — `ERROR_PATTERNS` F4 should be split: pricing/process instinct is evidence, mechanism
hypotheses are hypotheses. Post-draft edit.
