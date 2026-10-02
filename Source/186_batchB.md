# 186 — Batch B: picks 80 / 89 / 104 / 113

**2026-09-06 (T−1).** Archetypes and method: doc 185. Window: adp 86–132 (effective ADP at those
turns is ~91 / ~100 / ~116 / ~125 per §2.1c). 40 skill players.

---

## 1. FIRST, A JOIN FAILURE — and it cost a real row

The Pro-Football-Reference files carry no `espn_id`, so §3 forces a name key. Batch A matched
**131 of 131** live rushers and I reported that as clean. Batch B found the one it missed:

> **The board says "Kenny Gainwell." Pro-Football-Reference says "Kenneth Gainwell."**

One row, and it was a row that matters. This is §3's identity rule exactly: *a name join is a
defect even when it currently matches 100%.* Patched by alias, and it is the reason Batch A's
"zero unmatched" should be read as "zero unmatched **among receivers**" — I checked receivers and
inferred rushers. **Two positions, one control run, reported as if it covered both.**

---

## 2. THE FINDING: Tampa's backfield is on the board twice, 43 picks apart

§4.20's flag says the Buccaneers' job is **UNSETTLED and worth 189 points**, and §4.20 also
measured — `[TESTED, n=19 team-seasons]` — that the flag has **no opinion on who wins it**
(incumbent − challenger +8.2, **p=0.604**). *Buy the job, never the name.* Both men are live:

| | Bucky Irving | Kenny Gainwell |
|---|---|---|
| ADP / VOR | **56.7** / +20.03 | **99.9** / −16.86 |
| 2025 carries | 173 | 114 |
| **yards per carry** | **3.40** | **4.71** |
| **success rate** | **41.6%** | **55.3%** |
| **inside-5 carries / TDs** | **0 / 0** | **8 / 4** (29.6% team share) |
| 2025 targets / receptions | 35 / 30 | **85 / 73** |
| 2026 projected targets | 45.4 | **64.0** — highest RB in either batch |
| games 2025 | 10 | 17 |
| archetype signals | 2 | **3** |

**Irving costs 43 more picks for the same 189-point job, and every 2025 per-touch number favours
the other man.** Two honest caveats, both stated rather than buried: they were on different teams
in 2025, and Irving's 3.4 ypc comes from an injury-shortened 10-game year — though note that
**§4.22(c)'s availability penalty is a WR effect; at RB it measured null (+5.7, p=0.63)**, so our
own data does not let me discount Irving for the missed games either.

This is not "take Gainwell over Irving." It is: **the same job is available at pick 104 that the
market charges pick 56 for**, and §4.20 says the flag cannot tell you which one gets it.

---

## 3. THE QB QUESTION AT 104/113 IS ANSWERED, AND THE ANSWER IS A NULL

§4.18's draft-night rule sends Matt to a QB2 at 104/113 if one of Goff's tier or better is there.
The rushing-QB archetype (A4: ≥5.5 projected rush attempts per game → 18.7 ppg and **30 of 34 QB1
finishes**; rush rate persists at **r=0.89**) is the sharpest published QB signal there is.

**Not one QB in the Batch B window clears the bar.** Projected rush attempts per game:

| QB | adp | VOR | rush att/g |
|---|---|---|---|
| Caleb Williams | 88.3 | −9.66 | 4.18 |
| Matthew Stafford | 93.3 | **+21.19** | 1.59 |
| Trevor Lawrence | 101.6 | −3.83 | 4.32 |
| **Bo Nix** | 103.6 | **+7.39** | 4.84 |
| Patrick Mahomes | 109.1 | +2.26 | 3.12 |
| Brock Purdy | 110.2 | +4.79 | 3.85 |

**The only rushing QB anywhere near Matt's board is Jaxson Dart at adp 83** (5.93/game, first-round
capital, 66.3% rushing success rate in 2025) — a Batch A name at pick 80, not a 104/113 name.
**So the archetype changes nothing at 104/113: Bo Nix is still the QB there, on VOR, not on profile.**
Stafford's +21.19 is the largest QB VOR in the window and §7 already names him as pick 56's
best-available — he is a different decision, 40 picks earlier.

---

## 4. RED-ZONE ROLE WITHOUT THE TOUCHDOWNS — six fire, two are worth the ink

A2 is our own §4.5 (inside-10 targets persist at **r=+0.59**; **RZ TD rate is r=+0.02, noise**).

- **Mark Andrews (TE BAL, adp 126.5, VOR 0.00)** — **14 inside-20 targets, 9 inside-10, 2 TDs**,
  17 games, 17% target share. The biggest inside-10 role of any tight end past pick 90, sitting at
  exactly replacement level. §6's TE2 verdict does **not** rest on Andrews any more (that premise
  was retracted in v5.6 — the measured TE waiver return is 5.53 ppg against his 8.25), so as an
  emergency TE1 at 126 this is a real signal rather than a filler pick.
- **Wan'Dale Robinson (WR TEN, adp 112.7, VOR −27.96)** — **28.0% target share, the highest number
  in either batch**, 8.75 targets a game, 11 inside-20 and 5 inside-10 targets, **zero touchdowns**,
  16 games. He is also the carrier of a standing open thread: an **unsourced QUESTIONABLE** on his
  player card that nobody has ever traced. That should be resolved before he is drafted, not after.

Also firing, weaker: **Michael Wilson** (ARI, 15 inside-20, 0 inside-10 TDs, but VOR −22.3 behind
Marvin Harrison Jr.), **Brian Thomas Jr.** (JAX, ADOT 14.5 — one of the three grades corrected in
doc 178), **Jordan Addison** (MIN), and **Travis Hunter**, whose VOR of **−72.3** and 62.3
projected targets make the signal irrelevant.

---

## 5. THE ROUND-9+ DART SHELF (§4.13: risk from round 9, never before)

Ranked by signal, not by my preference:

1. **Blake Corum (RB LAR, adp 125.8, VOR −17.58)** — **5.1 ypc and a 59.3% success rate on 145
   carries, the best efficiency pair in either batch**, 9 inside-5 carries at a 31% share, and the
   **largest job ceiling of any backfield on the board at 215.**
2. **Kyle Monangai (RB CHI, adp 123.9, VOR −5.25)** — 2 signals, best VOR of the dart shelf, and
   still carrying the **AVOID** grade from the knee hyperextension I flagged on Sept 5. The flag
   stands; the profile is why he was on the list in the first place.
3. **RJ Harvey (RB DEN, adp 126.0, VOR −43.45)** — **62.1 projected targets against only 77.8
   projected carries.** A pure receiving back with round-2 capital. The VOR is a hard number to
   look past.
4. **Aaron Jones Sr. (RB MIN, adp 114.4)** — 60.8 projected targets, age 31.

---

## 6. WHAT BATCH B DOES NOT CHANGE

- No board edits. Surfaced only, per doc 185 §4.
- **The §4.18 draft-night rule at 104/113 is untouched** — the archetype had nothing to add and
  said so.
- **Batch C (picks 128 / 137, adp 132–168) is not run.**
