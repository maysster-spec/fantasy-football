# 234 — Your brother's second list, priced; and this morning's waiver call was wrong twice

**2026-09-08, evening.** Matt forwarded his brother's note: replace Xavier Worthy and "the
Tennessee RB"; try to trade Hurts and Jeanty for Nix / Love / Purdy plus a different back;
replace Worthy with a KC man, a Seattle man, a Miami receiver or a Baltimore receiver. Then:
*"let me know if you have feedback and what waiver options I have. do I need to put them in
tonight? I think so."*

**He is right about Spears and wrong about Worthy, and his read on Las Vegas is factually correct
and still does not make the trade work. Separately, checking it caught both halves of my own
morning recommendation being wrong.**

---

## 0. ACTIONABLE

1. **ONE claim tonight: Brenton Strange (TE, JAX, bye 7). Drop Tyjae Spears.** **+7.1 points of
   starting lineup over the season**, the largest available move on the board.
2. **DO NOT take T.J. Hockenson.** Minnesota's bye is week 6 and Detroit's is week 6. **He adds
   +0.00.** That was my morning recommendation and it is retracted.
3. **DO NOT drop Tyler Shough.** He is the only other quarterback; dropping him is **−19.1**. That
   was the other half of the morning recommendation and it is retracted.
4. **KEEP Worthy.** Every name the brother offered in his place loses: **−2.0 to −9.1**.
5. **Spears is worth exactly +0.00** to the lineup. The brother is right; he is the drop.
6. **The trade needs Gibbs, Bijan Robinson, McCaffrey or Jonathan Taylor coming back.** Henry
   breaks even (+1.9) and is ruled out by the standing rule; **James Cook and everyone below him
   lose.**
7. **A NUMBER THAT MUST NOT BE QUOTED — week 11 is 20.1, not 28.1 and not 13.1.** Third version
   in one day. **And week 8 is 9.7, not 0.0** — it is the kicker, and nothing had looked.
8. **`wire.py` was NOT patched tonight, deliberately** — see §6.

---

## 1. IDENTIFYING THE NAMES, BEFORE PRICING ANY OF THEM

The brother writes from memory (§0.5a — never correct the expression). Resolved against the
09-07 12:58 pull and this morning's available list:

| he wrote | who it is | available? | 2026 projection |
|---|---|---|---|
| "Tennessee RB" | **Tyjae Spears**, RB TEN | on Matt's roster | 129.5 |
| "Cyrus – KC" | **Cyrus Allen**, WR KC | yes, 4.5% owned | **43.1** |
| "Rasheed – Seattle" | **Rashid Shaheed**, WR SEA | **NO — rostered** | 123.0 |
| "Baltimore Wr J'kobi" | **Ja'Kobi Lane**, WR BAL | yes, 17.7% owned | 92.5 |
| "Miami wr" | no Miami receiver of consequence is free | Douglas / M. Washington / Tolbert | 70–95 band |
| — for comparison — | **Xavier Worthy**, WR KC | on Matt's roster | **145.2** |

**And one thing this resolved that had been an open thread since doc 233: Tyreek Hill.** He shows
in the wire's unpriced tail every week and looked like a board-universe gap. He is not.
**ESPN carries him at `proTeamId 0` — no NFL team — `injuryStatus OUT`, and no projection at all.**
The board is right to omit him. `[TESTED — the pull's own row]` **That open thread is closed.**

## 2. THE MEASUREMENT — PAIRED, ON HIS REAL 15-MAN ROSTER

**POPULATION:** Matt's actual roster, resolved by name against the 09-07 12:58 pull.
**BASELINE:** expected starting-lineup points, weeks 1–14, bye-adjusted (§0.3's fallback, stated
because a dollar figure is not computable here). A man's per-game rate is **ESPN's league-scored
season projection ÷ 16** — 17 NFL weeks minus his own bye. The lineup is the best legal nine
(1 QB, 2 RB, 2 WR, 1 TE, 1 FLEX, 1 D/ST, 1 K) recomputed **for every one of the 14 weeks**, with
that week's bye men removed. **A bye-free week is 120.1 points; the season is 1,632.6.**
`[TESTED — arithmetic on ESPN's projections, not a simulation]`

**What each man on the roster is actually worth to the lineup** (drop him, add nobody):

| player | worth | player | worth |
|---|---|---|---|
| Sam LaPorta | **121.6** | Jalen Hurts | 68.2 |
| Puka Nacua | 99.1 | Ashton Jeanty | 63.2 |
| Tyler Shough | **19.1** | Xavier Worthy | **9.1** |
| **Tyjae Spears** | **0.0** | **Mike Washington Jr.** | **0.0** |

**LaPorta at 121.6 is not a typo and it is the whole story of the waiver claim.** He is the only
tight end, so his absence does not cost his margin over a backup — it empties the slot. He is also
the roster's worst availability risk: **9 games in 2025**, which is §4.22(e)'s 7–9 band (mean beat
−27.1, n=30), and ESPN listed him **QUESTIONABLE** in yesterday's pull.

## 3. THE CLAIM, RANKED — AND WHY HOCKENSON IS ZERO

Every candidate, dropping Spears, against the same baseline:

| add | tm | bye | season lineup | vs now |
|---|---|---|---|---|
| **Brenton Strange** | JAX | **7** | 1,639.7 | **+7.06** |
| Terrance Ferguson | LAR | 11 | 1,639.7 | +7.04 |
| Pat Freiermuth | PIT | 9 | 1,639.3 | +6.64 |
| Dalton Schultz | HOU | 8 | 1,639.1 | +6.44 |
| Darren Waller | CAR | 5 | 1,638.4 | +5.81 |
| **T.J. Hockenson** | **MIN** | **6** | 1,632.6 | **+0.00** |
| Brian Robinson Jr. | ATL | 11 | 1,632.6 | +0.00 |
| Bateman · Ridley · Jeudy · D. Jones · Bigsby | — | — | 1,632.6 | +0.00 |

**Everything that is not a tight end is +0.00, and Hockenson is +0.00 because he is a tight end on
the wrong week.** The second tight end has exactly one lineup path on this roster: week 6. The FLEX
slot is already worth 10.9 (Dowdle) and no available tight end reaches that, so a TE2 never enters
the lineup except when LaPorta is out — and Minnesota is off in week 6 with Detroit.

**THIS IS §6's SAME-BYE TRAP AND §4.18c's +0.00, ON A TIGHT END.** §4.18c measured a same-bye
second quarterback at exactly +0.00 and said the trap "does NOT apply to TE2, because FLEX is
RB/WR/TE so `_lineup` gives a second TE a path in all 14 weeks." **That reasoning is correct in
general and false on this roster**, because the FLEX path is closed by his own running-back depth.
The exemption was written against the draft board's replacement level, not against a real
fifteen-man roster. `[CORRECTS §4.18c's scope]`

**Strange over Ferguson is a coin flip (0.02 points) broken on the bye** (§4.11 as a last-resort
tiebreaker, which is exactly what a 0.02 margin is): a bye-7 backup is available in week 11 if a
receiver goes down; a bye-11 one is not. Strange is also **23.2% owned against Hockenson's 60.5%**,
so he is far likelier to survive the claim run.

**Honest discount:** a tight end can be streamed in week 6 for about 5.5 points a week (doc 12's
measured TE waiver return). So Strange's edge over *doing nothing and streaming that week* is
nearer **+2.6** than +7.1 — but it costs a claim in week 6 to get it, and the week-6 slot is the
one place a stream competes with a rostered man.

## 4. THE TRADE

**The QB leg alone, Shough staying as the backup:**
Hurts → **Nix −14.8** · Purdy **−36.0** · Love **−42.4**.
**Purdy is the worst of the three for a reason the projection does not show:** San Francisco's bye
is week 8 and **Shough's is week 8**, so a Purdy roster has no quarterback at all that week. §6's
complementarity rule, firing on the brother's suggestion.

**The RB leg, replacing Jeanty, with the QB downgrade included:**

| back coming back | proj | for Jeanty alone | **with Hurts → Nix** |
|---|---|---|---|
| Jahmyr Gibbs | 331.6 | +69.2 | **+54.4** |
| Bijan Robinson | 314.8 | +52.7 | **+38.0** |
| Christian McCaffrey | 302.4 | +45.4 | **+30.6** |
| Jonathan Taylor | 291.0 | +36.1 | **+21.4** |
| Derrick Henry | 267.0 | +16.7 | **+1.9** |
| James Cook III | 262.3 | +12.8 | **−2.0** |
| Achane · Barkley · K. Walker · Hall | 248–261 | +1.4 to +12.0 | **−2.8 to −13.4** |

**Break-even sits between Henry and Cook.** Henry is ruled out by the standing rule (§4.25, and
honouring it measured at 0.0 cost on draft night). **So the trade is a gain only if the back coming
back is one of four men, and nobody trades one of those four for a discounted back plus a
quarterback.**

**HIS READ ON THE SITUATION IS RIGHT, AND IT IS ALREADY IN THE PRICE.** Team projected rushing +
receiving touchdowns, 2026, from the 09-07 pull's `raw_stats` (ids 25 + 43, the projection ids —
§3's stat-id rule): league median 41.8, and **Las Vegas is 28th of 32 at 30.5.** Cleveland, where
Judkins plays, is **31st at 26.4**. Both of his backs are on bottom-five scoring offences and he
should know that. **But doc 221 already tested the general form of this claim — "a back behind a
bad offence beats his price less" — and it died the moment the input was varied.** And §4.6: ESPN's
projection already carries touchdown regression. Jeanty's 246.5 *is* the number after Las Vegas is
charged for. Selling him at that price buys the discount twice.

**One thing that argues the other way and should be said:** ESPN listed Jeanty **QUESTIONABLE**
yesterday. But he played **17 of 17 games in 2025**, so the one downside signal this project
trusts (§4.22c / §7.9: ≤12 games last season, −19.4, p=0.00004) says nothing against him.

## 5. THE BYE TABLE, CORRECTED — THIRD VERSION TODAY, AND I OWN BOTH ERRORS

Doc 233 replaced this morning's "about thirteen points" with **28.1** and called that the fix.
**28.1 is also wrong, in both directions at once:**
- it divided each man's season projection by **14** rather than 16, inflating every weekly number
  by 14%; and
- it priced **Pickens, the Browns and Pineiro at zero** because they are not on the 480-row board.
  Pickens is his second-best receiver at 199.3. Zeroing him made losing Nacua and Adams look far
  worse than it is.

Resolved by pricing all fifteen from the pull:

| week | who is off | **lineup cost** | doc 233 said |
|---|---|---|---|
| **11** | Nacua, Judkins, Adams, Browns D/ST | **20.1** | 28.1 |
| **8** | Shough, **Pineiro** | **9.7** | **0.0** |
| **6** | LaPorta | **9.4** | 10.7 |
| 13 | Jeanty, M. Washington | 4.6 | 6.0 |
| 10 | Hurts, Dobbins | 3.8 | 4.3 |
| 14 | Pickens | 1.6 | 0.0 |
| 5 · 9 | Worthy · Dowdle, Spears | 0.0 | 0.0 |
| | **season** | **48.8** | 49.6 |

**Week 8 was reported as costing nothing and it costs 9.7 — every point of it the kicker**, whose
bye nobody had priced because he sits outside the board. Both week 8 and the defence half of week
11 (6.5 of the 20.1) are streamed anyway under §4.8, so **the skill-position holes are week 11 at
13.6 and week 6 at 9.4.**

**After the recommended claim, week 6 falls from 9.4 to 2.3 and the season from 48.8 to 41.7.**

## 6. WHY `wire.py` WAS NOT PATCHED, AND THAT IS A CHOICE NOT AN OMISSION

The page on the drive was generated at 07:33 and still carries the **pre-doc-233** prose ("13.1 in
week 11", "week 6 costs another 8.8", "31.6 this season"). Re-running `wire.py` now replaces that
with `bye_plan()`'s **28.1 / 10.7 / 49.6** — which §5 just corrected. So both the stale page and the
fresh one print a wrong number tonight.

**I did not patch it, on purpose.** `bye_plan` needs two changes — the divisor, and a projection
source for the three men who are not on the board — and there is **no `device_bash` on this
session**, so I cannot execute the patched file on his machine before he runs it tonight. §0.4:
*a script that runs in my container is not a script that runs.* Shipping an untested edit to the one
tool driving his week, on the night he uses it, is the more expensive mistake.
**`[OPEN — patch `bye_plan` to /16 and to price the off-board men, with the negative controls run
first: an empty roster, a roster whose kicker is off, and week 8 reading 9.7 rather than 0.0]`**

## 7. OPEN

- `bye_plan`'s divisor and off-board pricing (§6). **First item.**
- **§4.18c's TE2 exemption needs its scope narrowed in the directive** — the FLEX path it relies on
  is closed by a roster with six backs (§3).
- The section-presence guard for the two in-season pages (doc 233 §2b) — still absent, and the
  07:33 page carrying retracted prose is the second instance in two days.
- The gem lane is unbought: Brian Robinson Jr. and the eight "one injury away" backs are all
  +0.00 today and are the claim for a week when nothing is bleeding.
- Whether the week-11 trade is worth making at 13.6 skill-position points rather than 28.1 — the
  answer probably changes, and doc 233's trigger fires on the old number.
