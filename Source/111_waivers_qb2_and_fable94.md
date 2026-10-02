# 111 — Your own waiver record, the QB2-vs-RB-spot question, Fable's doc 94, and the committee flag

**Date:** 2026-08-31. Four things Matt asked in one message. Every number below is measured this
session from the raw files; the one place I could not measure, I say so.

---

## 1. YOUR WAIVER RECORD — measured on your team alone `[TESTED, n=88 of your adds]`

Built from `waiver_report_2022–2025.csv` (EXECUTED adds only, 1,230 rows), teams mapped through
`manager_identity_map.csv` (you are *Ekeler's Edge* → *Long Arm of the Lamar* →
*Ja'Marracle Whip Juggernauts* → *The Poetry of Junkyard Juggers*), joined by normalised name to
nflverse weekly stats 2022–2025 scored under this league's rules (§2). 831 of 1,230 adds resolve to
a skill player; the rest are K and D/ST, which have no rows in the stat file.

**Definition — and it is NOT doc 12's.** A "hit" here is: from the week you added him through
week 14, his points-per-played-week ≥ the position's replacement rate (QB 20.09 · RB 9.92 ·
WR 9.62 · TE 8.25, doc 12's own VBD levels). Doc 12's bar is unrecoverable from its text — its
QB hit rate of 0.62 cannot come from this bar — so I measured **both you and the league under one
bar of my own** rather than compare across two definitions. That is why the league RB number below
is 17%, not doc 12's 22%. **The two are not in conflict; they are different questions.**

| pos | league (all 12) | **you** | your mean ppg | league mean ppg |
|---|---|---|---|---|
| QB | 26.5% (n=113) | **35.7%** (n=14) | 17.27 | 17.38 |
| RB | 17.2% (n=233) | **20.5%** (n=39) | 6.59 | 6.50 |
| WR | 20.1% (n=219) | 12.5% (n=24) | 6.45 | 7.18 |
| TE | 26.1% (n=142) | 18.2% (n=11) | 6.63 | 6.80 |

**RB, you vs the other eleven: 20.5% (8/39) against 16.5% (32/194). Fisher p = 0.64.** Your mean
rest-of-season ppg is 6.59 against their 6.48, Mann-Whitney **p = 0.98**. You are at the top of the
per-manager table — but so is the noise; with n=39 you would need roughly a 2× difference to
resolve anything.

**The one place your stated method shows up.** You said you try to get there before the player
hits. On player-seasons that **two or more managers** added, you are **1.05 weeks earlier than the
field median at RB, and first to the player 57% of the time against the league's 42%**
(all positions: 0.51 weeks earlier, p=0.22). Real in the direction you claimed, **not significant**,
and it does not convert: the 3-weeks-before vs 3-weeks-after lift on your RB adds is **+0.39 ppg**
against the league's **+0.74** — i.e. being early does not mean you caught more of the rise.

**Your eight RB hits in four years:** Khalil Herbert and Jamaal Williams (2022 wk 2), AJ Dillon
(2022 wk 13, one game), De'Von Achane (2023 wk 4), Rico Dowdle (2024 wk 1), Woody Marks,
TreVeyon Henderson and Kyle Monangai (2025). Achane and Henderson are the two that mattered.

**BOTTOM LINE: four of every five RBs you add off waivers never give you a startable stretch.**
That is not a knock on your process — nobody in this league beats it. It is the argument for
drafting RB depth rather than planning to buy it, and it is the same conclusion §6 already
reaches, now measured on *your* record instead of the league's.

---

## 2. QB2 VERSUS ONE MORE RB BENCH SPOT

You asked the right question and it had not been asked this way: doc 92 priced QB2 **against
nothing**. It never asked what the roster spot would otherwise hold.

**New measurement — how often the slot is actually needed** `[TESTED, n=48 team-seasons]`.
From `draft_history_2021_2025.csv` joined to nflverse game logs, weeks 1–14:

| | missing-starter weeks per season |
|---|---|
| your drafted starting QB | **2.98** (median 1, p75 5) |
| your top-2 drafted RBs (slot-weeks short) | **5.54** (median 4, p75 8) |
| your top-3 drafted RBs | 8.81 |

**The QB2 side, re-derived:** Goff projects 19.20 ppg. A waiver QB delivered **17.38 ppg** on my
measurement (doc 92 said 16.65, doc 12 said 15.25). 1.8–2.6 ppg × 2.98 weeks = **+5.4 to +7.6
points**. Doc 92's paired sim says **+11.04 ± 3.08**, and the gap is explained: the sim also
charges you for the weeks the streamer *fails to be available*, which a mean-ppg calculation hides.
**Treat QB2 as +5 to +11, and the low end of that range is now the better-supported one.**

**The RB side.** The honest answer is that the *sixth* RB is not the one covering those 5.54 weeks
— your RB3, RB4 and RB5 cover them. The sixth body plays only when three are out at once, which is
rare. **So the extra RB spot is not worth much as insurance.** What it is worth is what §4.18
already priced: a late RB that hits is a **+80 to +95 VBD keeper**, realised 10.0% of the time from
rounds 9–12, ≈ **+8.5 expected 2027 points**. A QB kept is worth ≈ +0.5.

**So: QB2 ≈ +5 to +11 points in 2026 and zero keeper value. The RB dart ≈ small 2026 value plus
≈ +8 in 2027. They are within noise of each other, which is exactly what the directive's
draft-night rule already says — take the better player, not the better position.**
Your instinct that "the QB2 just sits there" is right about the lineup and wrong about the price:
it sits there for about three weeks a year, and those three weeks are worth roughly what the RB
dart's keeper option is worth. **No change to the rule at 104/113.**

---

## 3. FABLE'S DOC 94 — conclusions hold; it ran on a stale board, and the bye finding should change the directive

**Two provenance defects, both mine to have prevented by shipping it a pinned board.**

**(a) It ran on the pre-news board.** Doc 94's pick-32 table reads
*"Jacobs | 0.09 avail | engine already takes him on sight."* On the **shipped** board
`apply_news.py` has zeroed Josh Jacobs (proj 0, rank 435) — he cannot be taken at all. So Fable's
control arm spends pick 32 on a player who is out indefinitely in ~9% of drafts, and its pick-17
Jacobs arm (−$15.9 / −$23.7) tests a player who no longer exists on the board.
**Bounded impact:** doc 94's own finding is that the pick-32 cluster is flat within **±$1.5**, so
removing a 9%-frequency arm from a flat cluster moves the control by roughly **$0.1–0.2**. Burrow
(−$13.30) and Warren (−$14.00) stay clearly negative; their magnitudes are very slightly
overstated because the control they lost to contained a phantom. **Do not re-run it.**
**Do delete Jacobs from the pick-32 co-optimal list** wherever that list is quoted.

**(b) It used the 08-23 ADP, not the 08-30 refreeze.** `adp_vintage.txt` now reads
`espn_projections_2026_20260830_0142.csv`; between the two pulls, 160 of the top 161 players moved
and only 104 of 161 stayed within two slots of their old order (median move 1.43 picks). Doc 94's
availability probabilities are therefore keyed to the older market. Same bound applies — a flat
cluster does not care about 1.4 picks — but **any survival number quoted from doc 94 should be
labelled 08-23 vintage.**

**What survives, unchanged and worth having:**
- **Pick 17: take the best board player.** Forcing Henry was identical to the control in 1500/1500.
- **Pick 32 is a genuine coin flip**, and Burrow and Warren are the two clear *negatives* in it.
- **No 17→32 pairing effect** — availability at 32 moves ≤2.5pp whatever you do at 17.
- **Allen at 17 is dead** — survival 0.026, −17.7 points even conditional on him being there.
- **Bowers −$39 / McBride −$46 at 17.**

**THE BYE RESULT SHOULD CHANGE THE DIRECTIVE.** Doc 94 measured that a bye collision costs **at
most 1.2 points, ever** — the worst case in the whole board is Lamb + Pickens in week 14 at
**1.16 points**. §4.11 lists bye traps as a live planning constraint and the draft card carries a
BYE CHECK line on every pick. **On this measurement byes are a tiebreaker of last resort and
nothing more.** They should never move a pick that has any real margin behind it.
`[TESTED, Fable doc 94, N=1500]`

---

## 4. THE COMMITTEE FLAG — you were right, and it was polarised backwards

Your objection: *"Jonathon Brooks is a real threat if Chuba Hubbard goes down. Same dynamic with
Swift and Monangai... those players could still hold significant value where they go in the draft."*

**I measured the second axis you implied and it does not exist.** I computed each team's RB "pie" —
the sum of its top three RB projections — from the source pull. **It barely varies: IQR 317–355
projected points, ±6% across all 32 teams.** There is no such thing here as a big backfield versus
a small one. ESPN gives every backfield about the same total and only differs on how it splits it.

**Which means the gap was never measuring what the label said.** A 2-point gap is not ESPN saying
"this is a stable committee." It is ESPN saying **"we do not know who wins this job"** — which is
precisely the situation you want to buy. The old `COMMITTEE / contested / clear job` labels told
you to skip your own archetype.

**Changed in `depth_map.py` and on the LATE RB SHEET:**

| new label | rule | meaning |
|---|---|---|
| **UNSETTLED** | gap < 60 | job to be won — **your target** |
| contested | 60–150 | — |
| **LEAD BACK** | gap ≥ 150 | starter owns it; the backup pays only on an injury |

Two further fixes in the same patch:
- **The gap is now computed from the SOURCE pull, not the board.** The board has the 12 predicted
  keepers removed, which deletes Javonte Williams, Cam Skattebo and Rhamondre Stevenson — so
  Dallas, the Giants and New England looked like empty backfields and their gaps were fiction.
  *(That check also confirmed the board itself is correct: those three are absent because they are
  keepers, not because anything dropped them.)*
- **New `job worth` column** — what ESPN projects for the man currently holding the job, i.e.
  roughly what the winner inherits. This is the closest thing to a ceiling number this project has
  (§4.13d says there is none), and it separates two backfields the old flag treated identically:
  **Brooks/Hubbard is unsettled but the job is only worth 154; Monangai/Swift is unsettled and the
  job is worth 196.**
- Darts are now gated to `adp_pick < 168`, inside the real-ADP region (§4.14). Twelve RBs qualify:
  **Gainwell, Brooks, Monangai, White, Harvey, Mason, Spears** (UNSETTLED) and
  **Pacheco, Allgeier, Washington, Lloyd, B. Robinson** (LEAD BACK).

**Still not testable, and I am not going to pretend otherwise:** whether the man who wins an
unsettled job is worth having. Doc 110's wall stands — no historical depth charts, "unsettled
backfield" is not a coded variable. The record is consistent with your rule (5 of 8 late RB booms
were takeovers, and the two misses were exactly the TD-vulture shape you said to avoid) and that
is the strongest thing that can be said.

---

## 5. `my_take.py` — it is not a CSV

```
py my_take.py "Kyle Monangai" up   "better blocker, grows into the job"
py my_take.py "D'Andre Swift"  down "injury history, not getting younger"
py my_take.py "Kyle Monangai" clear
py my_take.py --list
```
Command line, one player per call. It writes `mine` / `mine_note` into
`live_draft\player_context.csv` and re-pins `check_kit.py`. On the live board a take shows as a
gold **MINE** badge, which outranks BUY, CALLS, DART and the injury grades — it is the one mark
that nothing else can silence. It is on COMMANDS.html under section 2c.

---

## ASSUMPTIONS, AND WHAT WOULD KILL EACH

1. **The name join to nflverse is clean.** 831 of 1,230 adds resolved; the shortfall is K/D/ST,
   which is expected, but a systematically-missed name class would bias section 1. *Killed by:* a
   list of unresolved add names showing real skill players.
2. **"Startable" = rest-of-season ppg above replacement.** A manager who adds for one good matchup
   and drops looks like a miss under this bar. *Killed by:* scoring adds on their single best week
   instead — on that bar (one week ≥ 15 points, i.e. a usable spot start) your RB adds reach
   **41%** against the league's 36%, the same ordering.
3. **Doc 94's flatness bound is real**, which is what lets me say the stale board does not matter.
   *Killed by:* re-running pick 32 on the current board and finding a spread wider than $1.5.

**Most valuable missing input:** historical depth charts, 2021–2025. They would convert §4 from
"consistent with the record" into an actual test of the takeover rule — the single largest
unmeasured thing left in this project.
