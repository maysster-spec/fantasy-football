# 202 — Is the projection age-blind? And did we ever look at downside?

*2026-09-06, T−1. Matt: **"I don't think players produce more as they age. if anything it should
move his projection down... You've been telling me that players don't improve on the same team
under certain constraints and I don't see why Henry would be treated any differently by your own
measure. I only mentioned because Henry is not relevant to me but other players are and if they
have the wrong forecast I want that rescoped. we were looking at upside but did we take a careful
look at downside?"***

---

## 0. ACTIONABLE FIRST (§0.1 v7.8)

1. **The age effect is REAL at WR and NULL at RB — the opposite of where he aimed it.**
   ESPN over-projects older **receivers** (rho −0.175, p=0.045, n=132). At RB the same test is
   flat: rho **+0.042, p=0.665**, and the 30+ band actually beats the 28–29 band.
2. **It is a SLOPE, not a cliff, and one measurement.** The 28+ vs under-28 band cut is
   **−0.112, p=0.102, CI [−0.243, +0.016] — spans zero.** Do not treat it as a rule.
3. **Two live names it touches, and only two are worth naming:**
   **Terry McLaurin** (31.0, live at pick 56) — age joins his **70% BOTTOM snap share (−10)** and
   his §4.22 **10-games** badge; three independent downside reads on one player at the thinnest
   turn on the board. And **Courtland Sutton** (30.9) — **a direct conflict**: I moved him UP this
   session on snap share (85% TOP), and age says down. **Snap share is the far better measurement
   (p<0.0001 vs p=0.045); Sutton's UP stands.**
4. **NOT applied to TE.** TE is null and slightly positive (rho +0.091, p=0.572). Kittle, Kelce,
   Andrews and Goedert are untouched by this.
5. **Nothing new prints on the board.** The ages are recorded in `player_context.csv`; no badge.
   A finding whose band cut spans zero does not get ink (his own rule: *"don't add noise that
   can't be measured"*).

---

## 1. WHAT WOULD HAVE TO BE TRUE (§0.5(a2))

His claim is about the **projection**, not the price. **Doc 201 measured beat-vs-PRICE and that is
a different object** — §4.22(b) established that the market and the projection disagree and the
market is the better predictor, so a null against price says nothing about the projection.
**He found a real gap in my own test, one message after I published it.**

**Testable form.** POPULATION: drafted players (§1.1 preseason ADP ≤ 180) in the **2022 and 2024**
ESPN pulls — the only two usable ones (§4.21; 2023's raw_stats are empty). OUTCOME: **ratio =
ESPN actual ÷ ESPN projection**, the §4.23 instrument, applied to a dimension §4.23 never cut on.
DIRECTION he predicts: ratio falls with age. FALSIFIER fixed first: if the 28+ ratio sits inside
the bootstrap CI of the under-28 ratio, the claim dies at that position.

## 2. RESULT BY POSITION — n=326 player-seasons

| position | <24 | 24–25 | 26–27 | 28–29 | 30+ | rho(age, ratio) | 28+ vs <28 |
|---|---|---|---|---|---|---|---|
| **WR** (132) | 0.962 | 0.902 | 0.783 | 0.834 | **0.735** | **−0.175, p=0.045** | −0.112, p=0.102, CI [−0.243, +0.016] |
| **RB** (109) | 0.832 | 0.980 | 0.972 | 0.775 | **0.930** | **+0.042, p=0.665** | −0.112, p=0.356, CI [−0.339, +0.117] |
| TE (41) | 0.863 | 0.885 | 0.889 | 0.883 | 1.052 | +0.091, p=0.572 | +0.059, p=0.589 |
| QB (41) | 0.760 | 0.865 | 1.133 | 0.881 | 0.794 | +0.003, p=0.987 | −0.107, p=0.344 |
| **ALL** (326) | 0.895 | 0.926 | 0.920 | 0.842 | 0.823 | −0.040, p=0.477 | −0.080, p=0.085 |

**WR declines monotonically from 0.96 to 0.74. RB does not decline at all** — its worst band is
28–29 and the 30+ band recovers to 0.930, above the under-24 band.

**HIS SPECIFIC CASE, MEASURED.** *"I don't see how he has any potential to outdo what he's done in
years past."* Henry's ESPN ratios: **1.15 at age 28.7 (2022)** and **1.53 at age 30.7 (2024)** —
he beat his own projection by 53% at thirty. That does not make passing on him wrong; doc 201 shows
the pass costs **0.0**. It makes the *reason* wrong, and the reason is what would carry to another
player.

## 3. WHY RB DOESN'T SHOW IT AND WR DOES — the honest read

**Not proven, stated as the shape.** The RB 28+ list is bimodal on the same names: McCaffrey 2024
at **0.13**, Henry 2024 at **1.53**. A back either keeps the job or loses it, and the ratio goes to
one extreme or the other, so the mean cancels. A receiver's decline is gradual — routes, separation,
target share erode a slice at a time — which is what a monotone slope looks like. **This is §4.20
again: buy the job, never the name.** RB age is a job question; WR age is a rate question.
`[HYPOTHESIS — the mechanism is not tested, only the slope]`

## 4. DID WE EVER LOOK AT DOWNSIDE? MOSTLY NO — AND THE BIGGEST NUMBER WAS ALREADY THERE

He is right that the project leaned upside. §4.13 is a ceiling study; §4.13b, §4.22 and §4.23 are
the only downside work, and none was framed that way. The most important downside fact in the
project has been sitting inside §4.23 unlabelled:

**The average drafted player returns about 0.89 of his ESPN projection — not 1.00.** By ADP band:
0.977 at 1–12 · 0.955 at 13–24 · 0.944 at 25–48 · 0.849 at 49–84 · 0.839 at 85–120 · 0.887 at 121+.
**And §4.23 established the gradient tracks GAMES PLAYED (15.04 → 12.28), not scoring rate.**

**So the dominant downside in this project is availability, not decline** — which is why §4.22's
games-played badge is on the board and nothing else is. The age slope at WR is a second, weaker
dimension of the same story: an older receiver misses more and produces less per game.

**What is still not measured, and should be named rather than implied:** nothing here predicts
*which* early pick busts. §4.13 says you cannot predict which player breaks out; the mirror
question has never been asked with the same rigour. **Post-draft.**

## 5. WHAT SHIPPED

`player_context.csv` gains an `AGE 2026:` segment for the **13 WRs aged 28+ inside pick 168**, with
the caveat in the text. **It does not print on the board** — `note()` renders segment 0 plus the two
extracted signal segments, and the age line is deliberately not among them. Recorded, not scored.
New pin `109640 / b6ec39ac05f8bbdc`; `check_kit.py` re-pinned in the same commit.

*Reproduce: `espn_projections_{2022,2024}_20260824.csv` (`proj_YYYY`, `actual_YYYY`) joined to
`Source\adp_registry\preseason_adp_YYYY.csv` and to nflverse rosters for `birth_date`, on a
suffix-stripped name key; adp ≤ 180, proj > 30.*
