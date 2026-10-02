# 101 — Three plain answers: the board on a keeper change, the Mahomes churn, and what to do with the range

**Date:** 2026-08-31

---

## 1. WHAT THE BOARD DOES WHEN A KEEPER TURNS OUT DIFFERENT

Forced two teams to keep someone other than predicted. **Measured, not described:**

| | |
|---|---|
| removed from the board (now kept) | Chase Brown, Breece Hall |
| **put back on the board** (no longer kept) | Chris Olave → **rank 27, VBD +41.2** · George Pickens → **rank 30, VBD +35.1** |
| rows whose **rank** moved | **44 of 478** — everyone between the two swapped players shifts up or down |
| rows whose **eff_pick** moved | **4 of 478** |
| biggest eff_pick move | −1.00 pick (A.J. Brown, Nico Collins, Bowers, Hampton) |

**Read it this way.** Two things change and they are different sizes.

- **Membership and rank change a lot.** A player who was invisible all summer reappears at his real
  value in the top 30, and forty-odd players slide one or two ranks around him. That is the part
  that matters on the clock: at 7:00 PM a name you have never considered can be sitting at rank 27.
- **`eff_pick` barely moves — by design.** `eff_pick` is "when does he actually get taken, given
  keepers are off the board," and swapping *which* player is kept only changes the count of keepers
  ahead of a given ADP. Here it moved 1 pick for 4 players. **So your survival odds are stable
  against keeper surprises; your board's contents are not.**

That is the honest shape of it: **a keeper surprise is a roster-composition event, not a timing
event.** The 7:00 PM rebuild exists to catch the first, and it is now proven to (39 of 39 on both
the identical and the divergent path).

## 2. MAHOMES — THE CHURN WAS MINE, AND HERE IS THE WHOLE OF IT

1. The injury sheet (built Aug 29 from a research prompt) graded him **DISCOUNT: late-2025 ACL/LCL.**
2. I read that and added a warning: *"this may be manufactured — the prompt told the researcher not
   to invent injuries."* **I wrote that without checking.** That was the mistake.
3. Aug 31 I checked. **The ACL/LCL is real**, and he is **cleared to practice at seven months and
   targeting Week 1.**

**Net: the sheet was right the whole time and I added one wrong warning, now removed.** The grade
stays DISCOUNT, but for a different reason — his rushing floor, not his availability. Nothing about
his row changed except my note on it. It should not have taken three moves and that is on me.

## 3. THE RANGE — WHAT TO DO WITH IT, AND WHAT MORE IS GETTABLE

**What it says.** Of late picks (ADP 121–180), 2022–24: 80% finish **below** replacement, 14% become
a real FLEX, 7% a weekly starter, **0% a league-winner.** Median 0.70× replacement. Early picks
(1–24): median 1.51×, only 8% below.

**Three things to actually do with it:**

1. **Your starters come from picks 8–89. Full stop.** Nothing in the late rounds is a plan for a
   starting job; it is a lottery ticket on one. This is the same conclusion as the position
   deadlines (WR dies at 65, everything else at 89) arrived at from a different direction.
2. **Cap the darts at 3–4 and stop.** The distribution says the 5th dart is worth what the 4th was
   — near zero — while the roster spot could hold an RB you cannot replace on waivers (RB adds hit
   **22%**; QB adds **62%**).
3. **Prefer a dart with a visible PATH to startable over one with "upside."** Upside is not a
   number anywhere. "Direct backup to a starting running back" is.

**What further research is actually gettable — I did the one that is.**

`2026_NFL_Depth_Charts_All_Teams.csv` has been in the project since the start and had never been
used. Parsed: **914 skill players with a depth-chart slot, matching 89% of the board's late band.**
That turns Matt's archetype — *"a backup behind an unsettled backfield"* — from a feeling into a
column. `late_darts.csv` is the result: **51 RBs and 71 WRs in ADP 100–175 who are the direct
backup at their position**, with bye, VBD, expected pick and injury grade.

The RBs reachable at 104 / 113 / 128 / 137: **Jonathon Brooks (CAR), Kenny Gainwell (TB), Kyle
Monangai (CHI), Rachaad White (WAS), Blake Corum (LAR), RJ Harvey (DEN), Woody Marks (HOU), Tyjae
Spears (TEN), Brian Robinson Jr. (ATL), Tyler Allgeier (ARI), Chris Rodriguez Jr. (JAX).**
Allgeier and Tyrone Tracy are on this list *and* were two of the fifteen historical late booms —
which is suggestive and is **not** a test.

**What is NOT gettable, and why — so it stops coming back:**

- **Backtesting the archetype.** We have 2026 depth charts and no historical ones. Without
  2021–2024 depth charts there is no way to score "was he the backup?" against outcomes.
- **Analyst breakout skill.** Needs per-player historical rankings by analyst. FantasyPros publishes
  per-analyst *positional accuracy ranks* only. Nobody in the project has the rest, and as far as I
  can find nobody publishes it. **Matt's read is right: the sample does not exist.** It is a real
  research project, not a pre-draft one.

---

**Files:** `late_darts.csv` (122 rows) · `player_context.csv` Mahomes row corrected · doc 100's
catalog item 4 closed.
