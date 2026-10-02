# 134 — The Bills bias is real, the reach doesn't pay, and where the value actually sits

> **BANNER, 28 Sept 2026 (doc 435).** The line below that endorses *"PUP/NFI/suspension stashes cost nothing"* is dead: **suspended players are NOT IR-eligible in ESPN football (doc 394, v9.19), and PUP and NFI are not established.** The slot takes Out or IR only. Kept as a dated record.

*2026-09-02. Four questions from Matt: a Buffalo bias in the league's draft history; whether
drafting IR-eligible players to free roster spots is a real edge; whether his own analyst-sourced
"hot takes" have paid; and a round-by-round list of players with a path to beat ADP.*

---

## 1. THE BILLS BIAS IS REAL AND IT SITS DIRECTLY BEHIND YOU  `[TESTED, n=680 true selections]`

`draft_history_2021_2025.csv`, keepers excluded (§4.7), joined to the preseason ADP registry.
**reach = preseason ADP − actual pick.** Positive means taken earlier than the market.

| manager | picks | Bills taken | reach on Bills | reach on everyone else | difference |
|---|---|---|---|---|---|
| **Rychlicki (POT, slot 10)** | 56 | **5** | **+19.9** | −2.9 | **+22.8** |
| **Snyder (Boo, slot 9)** | 70 | **6** | **+20.1** | +6.8 | **+13.3** |
| Brown/Collins | 70 | 2 | +13.5 | +7.8 | +5.7 |
| Lobsinger | 56 | 3 | +9.7 | +5.4 | +4.2 |
| **Matt Mays** | 56 | **0** | — | +0.2 | — |
| Fleming | 56 | 3 | −12.7 | +2.7 | −15.4 |

**League-wide: Bills go 8.9 picks early against 2.1 for everyone else — a +6.9 pick premium,
Welch p=0.143 on 27 Bills selections.** Not significant, and n=27 across five years is why. But
the two managers with a real sample are **Snyder (6) and Rychlicki (5)**, and the direction is
unambiguous for both.

**The part that matters: they pick at 9 and 10, and again at 15 and 16 — the whole of your 8→17
gap.** §2.1 already flags 17→32 as the longest gap and 32→41 as the steepest attrition; this adds
that any Buffalo player you want is exposed to two documented homers before your next turn.

Biggest single reaches on record: **Cole Beasley to Snyder at 69 against ADP 134** (2021), Gabriel
Davis at 123 vs 168, **Josh Allen to Snyder at 1.01 overall in 2025 against ADP 25**, Keon Coleman
twice at +26 and +21.

**2026 Bills inside the drafted range:** James Cook III (adp 11.4), **Josh Allen (20.8)**,
**DJ Moore (62.5)**, Dalton Kincaid (131.2), Khalil Shakir (132.5, AVOID).
**Practical read: DJ Moore at ADP 62 is a pick-56 target, and he is the one exposed.** If you want
him, 56 is the pick — waiting to 65 runs him past both homers' turns. Allen is already a
pick-8-or-nobody decision under §4.2 and this does not change that.

## 2. THE IR STASH: the idea is right, the eligible pool is much smaller than it looks

**Already project policy.** §6: *"3 IR slots are separate from the bench. PUP/NFI/suspension
stashes cost nothing."* So the concept is endorsed; the question is size and eligibility.

**The eligibility trap, and it is the whole answer.** ESPN's IR slot requires an official
**OUT / IR / PUP / NFI / Suspended** designation. **QUESTIONABLE and DOUBTFUL do not qualify.**
Most of the "injury discount" names on the board are QUESTIONABLE — Nabers, LaPorta, Kraft,
Kincaid, Sadiq, Fannin — so drafting them consumes a **bench** spot, not an IR spot, and the
manoeuvre does not happen. And Boone said it out loud on the 08-31 show: **a Commissioner's
Exempt List player cannot be placed on IR in most leagues**, which removes Josh Jacobs from this
plan entirely.

**Who is actually eligible today, from the 08-31 sweep:**

| player | adp | board# | designation |
|---|---|---|---|
| **Zach Charbonnet** | 154 | 130 | **PUP**, ACL reconstruction — the textbook stash |
| **Kyle Monangai** | 126 | 76 | **OUT_WEEKS**, knee hyperextension |
| Jordyn Tyson | 167 | 174 | major hamstring, Boone says possibly midseason |

**Size of the edge, honestly.** The freed roster spot buys you roughly **one extra speculative
waiver claim in the first weeks**. Doc 12 prices a waiver add at 5.4–15.3 ppg depending on
position with hit rates of 22–62%; §4.19 prices *your* RB adds at 20.5% with four of five never
producing a startable stretch. So the spot is worth something real and modest — and the pick that
buys it is nearly free, because §4.13b says **only 20.5% of players at ADP 121–180 deliver a
startable season anyway.** You are converting a lottery ticket that probably fails into a lottery
ticket that probably fails *plus* a roster spot.

**Verdict: do it at 128 or 137 with Charbonnet or Monangai, not earlier, and check the slot count.**
§2 records **IR 3**; you said "at least two." That is worth confirming in the league settings before
you plan around it — a third slot is a third free claim.
`[NOT MEASURED — no paired experiment exists for this in the project. The eligibility rules and
the waiver-return table are sourced; the "one extra claim" figure is arithmetic on them, not a test.]`

## 3. YOUR OWN REACHES HAVE NOT PAID — and the A8 trap nearly hid it

The testable half of *"sourcing takes from Boone has kept me high on the leaderboard"* is whether
your draft-day divergence from ADP produced better finishes. Five seasons, weeks 1–14, §2 scoring
computed from nflverse, positional finish rank against ADP-implied positional rank.

**The raw answer looked great and was mostly an artifact.** League-wide, corr(reach, beat) =
**+0.223, p<0.0001, n=670** — reaching pays. But `reach = adp − pick` and `beat = adp_rank −
fin_rank` **both rise with ADP** (corr +0.483 and +0.423). That is `ERROR_PATTERNS` A8: the
expectation is the confound.

**Controlled for log(ADP), the coefficient falls to +0.064 (se 0.021, p=0.002)** — real, and about
a third the size. **Within ADP bands, where the confound cannot operate:**

| ADP band | n | corr(reach, beat) | p |
|---|---|---|---|
| 1–36 | 154 | +0.087 | 0.29 |
| 37–72 | 162 | +0.076 | 0.34 |
| 73–120 | 214 | +0.016 | 0.82 |
| **121+** | **140** | **+0.223** | **0.008** |

**Reaching pays only in the late rounds.** That is §4.13's "risk from round 9, never before"
arriving from a completely independent direction, and it is the strongest replication of it the
project has.

**And for you specifically:** n=48 selections with a preseason ADP. **Controlled reach coefficient
−0.100, p=0.31.** Your reaches beyond 15 picks (n=7) came in at **−2.9 positional slots against
+6.4 for the other eleven managers.** The only manager with a significant positive coefficient is
**Lobsinger at +0.121, p=0.008** — the reigning champion.

**What this does and does not say.** It says that *taking a player earlier than his ADP* has not
worked for you. It does **not** measure Boone, and it does not measure a take that you expressed by
drafting a player at his market price rather than above it. **You asked me to keep your bias in
check, so: on the one version of this claim that is measurable, the record runs against it.**

**The test that would settle it, and what I need.** Correction to something you assumed — **I hold
preseason ADP for all five seasons, 2021–2025.** What exists for only two years (2022 and 2024) is
the ESPN *projection*. So if you supply **Boone's preseason rankings for 2022, 2023 and 2025**
(2024 would help too), I can run the real test: does Boone-minus-ADP predict positional finish,
controlled for ADP level and clustered where needed? That is n≈600 and well powered. It is the one
open question in this project where more data from you changes the answer.

## 4. THE VALUE LADDER — `VALUE_LADDER.pdf`

49 players across picks 17–137, each carrying **two or more independent reasons** to beat his ADP,
gated to players you can realistically get (survival ≥ 0.50 at that pick under §4.12's noise).

**It is an agreement count, not a model.** Four of the five signals are unpriced and unmeasured:
§4.13 retired three draft-day divergence signals, doc 129 replicated the failure at ρ −0.173 on an
independent market, and §4.13d found analyst disagreement predicts finishing **worse** (−0.244,
p=0.0009). What the sheet gives you is where several sources independently point the same way —
a research shortlist, not a ranking to obey.

- **BOARD** — our VBD is more than 12 slots ahead of his price
- **ANALYSTS** — Boone and Harmon average ≥25 slots ahead of ADP (the ~75th percentile; the median
  gap in the 100–170 band is 2 slots, and 43% of that band has both ahead, so only magnitude counts)
- **BUY** — both analyst panels ahead of ADP in the existing sweep
- **JOB** — UNSETTLED or contested with a job worth ≥150 points (§4.20, the 93% half of §4.21)
- **INJURY-OPENED** — a teammate at his position is OUT, PUP or exempt. This is the Mike-Evans-in-SF
  shape you asked for, computed rather than recalled.

**Pick 8 is deliberately absent.** §4.2 closed it and nothing here reopens it.

**The densest rows**, four signals each: **D'Andre Swift at 32** (path opened by Monangai),
**Jonathon Brooks at 80**, **Jayden Reed and Croskey-Merritt at 104**, **Jordan Mason at 113**.

**This is a research sheet and it does not go to the draft table.** Doc 116 consolidated five paper
artifacts into one board precisely so you are not flipping between sheets at 60 seconds a pick.
Use this before Sunday to build your own takes; draft from `DRAFT_BOARD.pdf`.

## Assumptions

1. **§1's Bills test is 27 selections.** The two managers with a real sample carry it; the rest of
   the table is one or two picks and should be read as noise.
2. **§2 is not measured.** No paired experiment exists. The rules constraint is the firm part.
3. **§3 measures reach, which is a proxy for a take.** A take expressed as a fade, or as taking a
   player at market, is invisible to it.
4. **§4's survival numbers are dispersion-only** and §4.15 is explicit that this runs optimistic —
   every `p` is a ceiling.
