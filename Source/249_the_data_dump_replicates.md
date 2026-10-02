# 249 — Ray Garvin's Week-1 data points replicated on our own rows: two land within 2–3 points, and the number Matt half-remembered is 28%

**2026-09-09.** Matt sends the *Yahoo Fantasy Forecast* Week 1 Data Dump transcript (Matt Harmon
and Ray Garvin), noting the transcript is an **AI-corrected** capture and that some errors may
survive — and asks: *"IIRC he's quoting a 30% or so success rate for the bids on week 1. Correct me
if i'm wrong... I think that lines up to the amount of success you saw."*

---

## 1. THE NUMBER HE IS REMEMBERING IS **28%**, AND HE IS RIGHT ABOUT WHAT IT MEANS

**Nothing in the transcript quotes a success rate for BIDS.** The 28% is Ray's Data Point 1:

> *"Only 28% of those surprise Week 1 stars — those surprise Week 1 starters — have a resume that
> warrants long-term sustainability."*
> *"51% of prior-year fantasy starters who disappoint in Week 1 return to starter status very
> quickly after that."*

**It is about the PLAYER, not the bid — but that player is precisely what a Week-1 bid buys, so the
recollection is sound and the figure is 28%, not 30%.** `[SOURCED: Yahoo Fantasy Forecast, Week 1
Data Dump transcript supplied 2026-09-09]`

---

## 2. TWO OF RAY'S FIVE ARE DIRECTLY TESTABLE HERE, AND BOTH REPLICATE

**POPULATION — state it every time (§0.6): all QB/RB/WR/TE player-weeks, 2021–2025, weeks 1–14,
scored under §2 (half-PPR, 6-pt passing TD), nflverse weekly. Rest-of-season = weeks 2–14.**

**(a) DATA POINT 2 — do Week-1 top-24 finishers stay top-24?**

| | Ray | **ours** | by season |
|---|---|---|---|
| **wide receivers** | **39%** | **37%** | 42 · 42 · 50 · 29 · 21 |
| **running backs** | **52%** | **55%** | 54 · 42 · 42 · 67 · 71 |

`[TESTED, 5 seasons]` **Within two and three points, on data he has never seen.**

**(b) DATA POINT 5 — volume with no touchdown, against a touchdown with no volume.**
High volume = top third of his position by week-1 touches (carries + targets); low = bottom third.
Start rate = share of weeks 2–14 at or above his position's **measured** replacement ppg
(QB 20.09 · RB 9.92 · WR 9.62 · TE 8.25, doc 12).

| | Ray | **ours** |
|---|---|---|
| high volume, **no** Week-1 TD | 10.9 ppg · 51% start rate | **10.24 ppg · 40.3%** (n=351) |
| low volume, **with** a Week-1 TD | 6.5 ppg · 17% | **3.24 ppg · 8.4%** (n=18) |

`[TESTED]` **Same direction, and the gap is WIDER on our rows than on his.** The low-volume cell is
**n=18** — thin, and I am saying so rather than leaning on it.

**THIS IS THE COMPOSITE'S VOLUME LEG, ARRIVING FROM OUTSIDE.** Doc 248 measured targets per game at
**+18.5 points, p=0.000** on a completely different population (young non-startable receivers across
a season boundary). Ray measures the same thing on one week of one season. **Two objects, two
samples, one answer: buy the touches, not the box score.**

---

## 3. THE ALIGNMENT MATT ASKED ABOUT IS REAL — BUT IT IS A DIFFERENT PAIR THAN HE GUESSED

**His 28% does NOT line up with doc 248's 11.4% base rate, and it must not be read that way (§0.6).**
Different populations: Ray's 28% is conditioned on **one big Week-1 game**; our 11.4% is conditioned
on **a whole prior season under replacement**. A player selected on one week and a player selected on
a season are not the same object, and their rates should not agree.

**WHERE IT DOES LINE UP IS STRIKING, AND IT IS RAY'S DATA POINT 1 AGAINST OUR §4.26(a):**

| | the "surprise / cheap" side | the "established / expensive" side |
|---|---|---|
| **Ray**, Week-1 surprise vs prior-year starter | **28%** sustain | **51%** bounce back |
| **§4.26(a)** (doc 229), cheap vs expensive top-12 finisher, repeat next season | **22.7%** (n=44) | **56.0%** (n=91) |

**Two independent sources, two different windows — one week against one season — and the split lands
within about five points on both sides.** `[TESTED here, SOURCED there]` **The shape is the same one
this project keeps finding: the market's established player is the safer bet, and fading him loses
(§4.22b).** Matt's instinct that it "lines up to full-season stats" is correct; it lines up to a
different number of ours than the one he had in mind, and more closely.

---

## 4. HE IS RIGHT ABOUT THE FAB CAVEAT, AND THE TRANSLATION MATTERS

Matt: *"some of the things Ray may provide toward caution may only apply to those leagues on a FAB
budget."* **Correct — and our league has no budget at all (§2: standard waiver order, resets weekly
to inverse standings, NOT FAAB).**

**But the caution does not vanish, it changes currency. Our cost is WAIVER PRIORITY, and doc 224
measured what that is worth: he wins 51 of 91 claims nobody else made (56%) and only 10 of 63
contested ones (16%). Five of every six contested players go to somebody else.**
**So Ray's "don't blow your FAAB on a Week-1 mirage" becomes, for us: do not spend your position on
a contested Week-1 mirage — because the week a surprise star emerges is exactly the week the whole
league claims him, and it is the week Matt is least likely to win.** He is **5th of 12** this week.
**Doc 224's rule already covers it and this sharpens the reason: the claims he reliably wins are the
ones nobody else has made yet, which is an argument for Tucker/Pearsall-type names (doc 248) over
whoever explodes on Sunday.**

---

## 5. THE OTHER THREE OF RAY'S, AND WHAT THEY TOUCH HERE

- **DP3, rookie opportunity growth:** RB and WR **+55%**, TE **+80%**, QB **+87%** from Week 1 to
  weeks 10–17. **This is doc 246's curve from the other end** — rookie → year 2 is the only
  significant positive step we measured (+0.62 ppg, CI [+0.11, +1.14]) and target share climbs
  16.4% → 20.1% → 22.8%. **And doc 245: nine of fourteen rookie displacers were first-round picks.**
  Same story, different instrument. **Not independently re-tested here.**
- **DP4, team scoring:** 30+ in the opener → **59%** finish top-12 scoring (25.1 ppg after); under 20
  → **29%**. `[SOURCED, not tested here]` It bears on §4.21, which found team pass VOLUME is only
  7.5% of a pass-catcher's variance against 93% for his own share — **so a hot team is a weak reason
  to buy a receiver, even if the team signal itself is real.**
- **DP2's mechanism is ours.** Ray explains WR volatility as inherent; **doc 244 gives the
  structural reason — a backfield is ONE job and a receiver room is three to five**, which is also
  why the Wally Pipp event is real at RB (+12.4 points when the fill-in produces, p=0.006) and null
  at WR.

**AND ONE LIVE CONFIRMATION FROM HARMON'S SIDE.** His Data Point 1 is the Jacksonville room:
**Parker Washington 3.14 YPRR and a 35% target share against Brian Thomas Jr. at 1.38 and 18%.**
**Doc 245's displacement table already recorded it: 2024→25 JAX, Parker Washington out-targeted
Brian Thomas Jr. 95 to 91.** We measured the takeover from usage; he is describing the same room
from film and route data a season later. **Thomas is owned in our league; Parker Washington is not.**

---

## 6. WHAT I WOULD NOT TAKE FROM IT

- **"Only 39% stay top-24" is not a reason to avoid Week-1 receivers — it is a reason not to PAY for
  them.** 37–39% against a 24-slot field is far above any base rate; the point is the price, not the
  player, which is §4.22(b) again.
- **DP4's 59% is a team statistic and this project has twice measured that team environment barely
  moves an individual** (§4.20's ±6% RB pie, §4.21's 7.5%). **Do not convert it into a player call.**
- **The transcript is an AI-corrected capture and Matt flagged it.** Every figure above is quoted as
  it appears there; two of the five are now independently replicated on our own rows, which is the
  only real check available.

---

## 7. OPEN THREADS

- **Ray's DP1 in our form is NOT yet run** — "a player who has a big Week 1 and was not a prior-year
  starter" is computable on the same rows and would put our own number next to his 28%. **NOT RUN.**
- **DP3's rookie growth curve by WEEK** (1 → 10–17) rather than by season is also computable and
  would sharpen doc 246. **NOT RUN.**
- Carried: draft capital on the board (doc 245 §5, still the highest-value build, not started) ·
  Breakout Age / College Dominator / slot rate / TPRR all BLOCKED with sources named (doc 248 §4) ·
  the 2022 Fantasy Footballers rates unreplicated · the Aug-8 depth chart is a month stale ·
  the hypothesis register is unbuilt.
