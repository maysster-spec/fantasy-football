# 266 — Cleveland's calendar, and the sort key that prices potential at zero

**Date:** 2026-09-10. Two questions and one standing instruction from Matt, and the instruction is
the bigger of the three.

---

## 1. THE BROWNS: IT IS NOT A DURATION, IT IS A CALENDAR

**HOLD HIM THROUGH WEEK 13. Re-decide for the playoffs, and do not assume he is your December
defence — his worst stretch of the season is weeks 15–17.**

**METHOD: `slate.py`'s two terms on Cleveland alone. Opponent generosity shrunk at r=+0.325,
Cleveland's own 2025 form shrunk at r=+0.269 (doc 212's measured persistences), against the 2026
schedule. Rank is among every defence playing that week.**

| wk | opp | value | rank |   | wk | opp | value | rank |
|---|---|---|---|---|---|---|---|---|
| 2 | TB | 5.20 | 13 | | 10 | HOU | 4.96 | **15** |
| 3 | CAR | 5.81 | 9 | | 11 | — | BYE | — |
| 4 | PIT | 5.21 | 11 | | **12** | **LV** | **7.15** | **2** |
| **5** | **NYJ** | **6.75** | **3** | | **13** | **CIN** | **6.20** | **3** |
| 6 | BAL | 5.09 | **16** | | 14 | ATL | 5.43 | 13 |
| **7** | **TEN** | **6.85** | **2** | | 15 | NYG | 5.60 | 8 |
| 8 | PIT | 5.21 | 12 | | 16 | BAL | 5.09 | **16** |
| **9** | **NO** | **6.38** | **4** | | 17 | IND | 5.12 | 15 |

**Cleveland is never elite and never a liability — it oscillates.** Five top-four weeks (5, 7, 9,
12, 13) against four bottom-half ones (6, 10, 16, 17), and the bad ones are the AFC North games
plus Houston.

**THE STRETCH AVERAGES ARE THE ANSWER:**

| window | mean rank |
|---|---|
| weeks 2–5 | 9.0 |
| weeks 6–10 | 9.8 |
| **weeks 9–14** | **7.4 — his best** |
| **weeks 15–17** | **13.0 — his worst** |

**He gets BETTER as the season goes and then falls off exactly at the playoffs.** That inverts the
intuition that you hold a defence for December. **Weeks 12 and 13 — Las Vegas then Cincinnati, ranks
2 and 3 — are the single best reason to keep him**, and they arrive right before the window where
he is at his weakest.

**And doc 264 says holding is the right default anyway:** over a multi-week hold the UNIT is 65% of
the movable spread, and Cleveland's unit term is **+0.44 a week above league average**. Modest,
positive, and it applies every week — which is more than a schedule edge can say.

**WHAT THIS DOES NOT ANSWER:** whether something better is free. That is `py wire.py` against his
own league, and it is on `matt_todo.txt`. This is Cleveland's own calendar, not a comparison.

## 2. HIS STANDING INSTRUCTION, AND HE IS RIGHT — WITH ONE MEASURED CAVEAT

Matt: *"We are not just looking at current market value, but POTENTIAL value as well. Just like at
the bottom of draft, that doesn't matter as much. Well now we are at the bottom of the bottom."*

**CONFIRMED, AND THE REASON IS ALREADY MEASURED IN THIS PROJECT — doc 259: the best FREE body is
below his worst startable man at EVERY position.** Best free RB **6.51** against Dowdle **12.24**;
best free WR **8.94** against Worthy **10.40**. **So current value off his wire is not merely small,
it is negative by construction. Ranking the wire by current value ranks it by the one quantity
already proven to lose.** His frame is not a preference — it is the only variable left.

**AND IT LANDS ON A LIVE LINE OF CODE.** `wire.py` line 989: *"LANE 1 — best available now, ranked
by our value."* That lane sorts on board VOR. **The board prices potential at zero by
construction** — §4.14 puts two thirds of its rows inside ESPN's fabricated ADP blob, below
replacement, which is exactly where an unproven player sits. §4.28 has the case in the file already:
**Jordyn Tyson, the 8th overall pick of the 2026 NFL draft, sat on our board at 81.5 BELOW receiver
replacement.** LANE 1 would sort him to the floor.
*(The stash lanes are already right: they sort on `job_ceil`, which IS potential. It is the headline
list that uses the wrong key.)*

**THE CAVEAT HE SHOULD HAVE, BECAUSE IT IS THE HONEST HALF (§4.13b).** Potential at the bottom is
real and it is **thin**. On the ratio definition, breakout rate is **17.0% at ADP 121–180** against
2.1–6.2% at 25–84 — his read exactly. On the ABSOLUTE definition — did the player become startable
at all — the same band is **20.5%**, and **four of five never do.** **So the bottom of the bottom is
where the upside lives AND where most of it dies.** What makes it correct anyway is §4.31: the claim
is free. No FAAB, no limit, order resets weekly. **A lottery with a measured ticket price of zero is
worth playing; the same lottery with a real price is not, and that is why this rule belongs to the
WIRE and not to rounds 1–4.**

**THE THREE POTENTIAL SCREENS THIS PROJECT ALREADY HAS, and they should be the sort key:**
- **§4.30's receiver composite** — NFL rounds 1–3 · yards per target > 7.13 · targets per game
  > 3.20. **39.4% at three of three against an 11.4% base.**
- **§4.28's first-round rookie receiver** behind a returning 60-target incumbent — **60.0% against
  a 7.4% base, Fisher p=0.000001.**
- **§4.27's two gates for a back** — the man ahead's fragility × the backup's best two-week stretch
  at 11.2 half-PPR a game.

## 3. QUEUED, NOT SHIPPED — AND SAYING WHY (§0.4)

**`wire.py`'s LANE 1 should rank on the potential screens, with board value shown beside it rather
than as the sort key.** Not done tonight: it is a 57 KB file that drives his Tuesday run, the change
touches the one table he actually reads, and doc 251 is the standing warning about what a rushed
edit to that list produces. **NOT YET RUN, testable form stated: rank LANE 1 by screen count (0–3 at
receiver, 0–2 at back), tie-broken on board value, and keep the current sort available so the two
orderings can be read against each other before the old one is retired.**

**AND A DIRECTIVE CHANGE IS OWED BUT DELIBERATELY HELD.** §4.33 carries doc 259's "the wire cannot
upgrade a working slot"; it should also carry **"therefore the wire is a POTENTIAL instrument and
current value is the wrong sort key on it."** Held until the §6/§7/§8 phase split, so he pastes
once rather than twice — his clipboard caps at well under the current 153,537 characters and the
paste cost him two attempts on 2026-09-09.
