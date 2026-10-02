# 299 -- F1: the arrival does squeeze the room below, and Denver is the live case

**12 September 2026.** Catalog item F1, Matt's own mechanism. Tested. **Confirmed in the half that
matters, and unresolved in the half he stated more strongly.** Denver 2026 is the population this
was measured on, which makes it the first of his mechanisms to arrive with a live row attached.

---

## 1. His claim, and the two tests it needs

> *"the arrival compresses everyone below him, not just the man at the top. If that's right, Waddle
> hurts Bryant more than Sutton does, and my watch trigger is Waddle's snaps, not Sutton's."*

Those are **two** claims and they get different answers, so they were tested separately (0.5a2):

1. **the room below loses share when a veteran arrives** -- against teams with no arrival;
2. **it loses MORE than the incumbent does** -- his "hurts Bryant more than Sutton".

---

## 2. The design

**POPULATION -- restated, not inherited (0.6):** team-seasons **2021-2025** with a receiver who had
**60+ targets** for that team last season and is still on it. **TREATMENT:** a receiver who had 60+
targets for **another** team last season is on this team now. **CONTROL:** the same incumbent
condition, no arrival. **43 treatment team-seasons, 68 control.**
**OUTCOME:** each man's share of his team's receiver targets, **per game played**, this season minus
last. 4-game minimum in both seasons; **15 player-seasons removed by it, reported (B2)**.
**THE ROOM BELOW:** the men ranked **3rd and 4th by LAST season's targets**, fixed before the
outcome and never re-ranked on it.
**CONTROL FOR VACATED SHARE**, because an arrival usually replaces a departure, which lifts everyone
and would hide a squeeze. **CLUSTERED BY TEAM (A5):** the permutation shuffles the arrival label
within each team, so a team that signs veterans every year cannot carry the result.
Source: nflverse weekly, 2020-2025, regular season. Stdlib only.

---

## 3. Result

| | incumbent | 3rd + 4th | vacated share |
|---|---|---|---|
| **arrival** | −0.022 | **−0.017** | 32.3% |
| no arrival | +0.003 | **+0.027** | 22.1% |
| **difference** | **−0.025** | **−0.044** | |

**CLAIM 1 IS CONFIRMED. The room below a returning incumbent loses 4.4 points of team target share
when a veteran arrives, against teams where none does. Permutation clustered within team, 4,000
draws, one-sided in his direction: p = 0.005.** `[TESTED, n=43 vs 68 team-seasons]`
And the sign flips rather than merely shrinking: **without an arrival that group GROWS (+0.027); with
one it shrinks.** In proportion to the share they already held, +0.16 becomes −0.07.

**IT IS NOT THE VACATED-TARGETS STORY.** The squeeze is present in every band and is largest in the
middle one: under 20% vacated, −0.022 · 20-35%, **−0.116** · 35%+, −0.037.

**CLAIM 2 IS SUGGESTIVE AND NOT RESOLVED.** His exact words are a within-team comparison, so the
right object is (3rd+4th minus incumbent) inside each team-season, which cancels the team
denominator entirely -- when a receiver arrives, team targets rise and every share falls a little
for reasons that are not a squeeze. **Arrival +0.005, no arrival +0.024, difference −0.019,
p = 0.101.** `[SUGGESTIVE]` **The room below is hurt, and that it is hurt MORE than the man at the
top is not established at this sample.**

**So the watch trigger is BOTH, not instead.** His instinct to watch the arrival is supported; the
part that said to stop watching the incumbent is not.

**The ten largest squeezes are recognisable, which is the check that the measure is measuring the
thing:** Keenan Allen arriving in Chicago (room below −0.160), Diggs to Houston (−0.141), Davante
Adams to the Jets (−0.109) and to the Rams (−0.088), Deebo to Washington (−0.119).

---

## 4. DENVER 2026 IS EXACTLY THIS POPULATION

`[SOURCED: the 7 Sept ESPN pull for the 2026 roster; nflverse for 2025 targets]`

| | 2025 targets | 2025 team | 2026 |
|---|---|---|---|
| Courtland Sutton | 124 | DEN | the returning incumbent |
| **Jaylen Waddle** | **100** | **MIA** | **the arrival** |
| Troy Franklin | 104 | DEN | 2nd by last year's targets |
| Marvin Mims Jr. | 51 | DEN | **3rd** |
| **Pat Bryant** | **49** | **DEN** | **4th** |

**Bryant sits in the 3rd-and-4th group, on a team that has just added a 100-target receiver.** That
is the exact cell measured above at −0.044, p = 0.005.

**This is a caution on the page's 3-of-3 tag for him, and it is not a price.** Doc 298 lists him as
one of four free receivers clearing 4.30's screen; that screen is built on his 2025 rate and knows
nothing about who arrived since. **The screen and this finding point opposite ways on the same man,
and both are measured.** Per the standing instruction he is not priced here, and the two results are
left side by side for Matt rather than collapsed into one number.

---

## 5. What this does not say

* **Not a forecast for one man.** It is a group mean over 43 team-seasons, and the spread inside the
  treatment group runs from −0.187 to positive.
* **The levels are denominator-sensitive**, the difference between groups is not; that is why claim
  2 was run within team.
* **Alignment is not in this test at all.** Whether Waddle takes the slot that Bryant plays is F3,
  still NOT YET RUN, and its live half may be blocked on a weekly PFF alignment file.

**Reproduce:** `Scripts\research\f1\squeeze.py`, stdlib only, nflverse weekly 2020-2025.
