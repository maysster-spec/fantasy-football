# 217 — Nothing was written, the QB-injury hunch is a null, and Matt's share number was better than my correction

**2026-09-07, 17:25 ET. Keeper lock T−1h35m, draft T−2h35m.**

---

## 0. ACTIONABLE

1. **The early `draft_night.bat` run changed NOTHING. Do not reprint anything.**
   `board_v8_fixed.csv` is still 12:59 ET · `actual_keepers.csv` is still **Aug 28** · nothing was
   written. **Run `.\draft_night.bat` again at 7:00 as planned.**
2. **"Short 2 keepers" is expected, not a fault** — the lock is 7:00 PM and two managers had not set
   theirs at 5:10. The board already has all twelve *predicted* keepers removed, verified.
3. **RESTART `bridge_server.py` AT 7:50 — THIS IS THE ONE THAT CAN STILL BITE.** `bridge_picks.json`
   currently holds **this afternoon's practice picks (16:29 ET)** and at 8:00 PM it will be about
   3.5 hours old — **under the six-hour refusal, so the board would ACCEPT it.** The reset happens
   on listener startup, not on board startup. Closing the windows is not enough by itself.
4. **His QB-injury hunch: measured, and it is a NULL** — about a third of a point a game.
5. **CORRECTION TO MY OWN CORRECTION: Matt's "30% of the share" for Mike Washington was closer
   than the number I answered with.** ESPN projects him **24.1% of Las Vegas carries**. I quoted
   20%, which was his share of *projected points*, not carries. He asked about share. He was right.

---

## 1. WHAT THE EARLY RUN ACTUALLY DID — nothing, and here is the evidence

| file | last written | meaning |
|---|---|---|
| `board_v8_fixed.csv` | **Sep 7 12:59 ET** | the keeper swap never wrote |
| `actual_keepers.csv` | **Aug 28 23:58 ET** | `fetch_keepers.py --write` never ran |
| `player_context.csv` | Sep 7 12:59 ET | untouched |
| `bridge_picks.json` | Sep 7 16:29 ET | from the practice draft, not the batch |

**And the twelve predicted keepers are all absent from the board** — checked by name, 0 of 12 still
present. **Nothing to reprint.** The batch gated exactly where it should have: it read ESPN, found
fewer than twelve keepers set, and stopped before writing. That is the design working.

## 2. THE QB-INJURY QUESTION — Matt: *"it's based on the starting QB getting injured. Are you sure that is priced?"*

**He is right that `job worth` does not price it. `job worth` is ESPN's projection for the man
holding the job, and that projection assumes his quarterback plays.** So the question is fair and
the answer needed measuring rather than asserting.

**WHAT WOULD HAVE TO BE TRUE (§0.5(a2)):** *a team's lead running back scores meaningfully less in
the weeks his season-opening QB1 does not play.*
**POPULATION:** team-weeks 2021–2025, regular season, lead RB on the field for ≥25% of snaps
(otherwise the test measures the RB's own absence). QB1 = most offensive snaps that team-season;
"out" = under 25% of snaps that week. **OUTCOME:** the lead RB's half-PPR points.

| | n | lead RB half-PPR |
|---|---|---|
| QB1 out | 380 | **12.27** |
| QB1 playing | 1,937 | **13.14** |
| raw difference | | **−0.87** |

**Paired within the same back in the same season** (removes "bad teams have bad quarterbacks *and*
bad running backs"), n=93 RB-seasons that had both kinds of week:
**−0.37 points per game, 95% CI [−1.52, +0.79], p=0.54.** `[TESTED]`

**NULL, direction slightly Matt's way, and this one is not a power failure** — the interval rules
out anything larger than about 1.5 points a game, which is 21 points across weeks 1–14. **Losing the
starting quarterback costs the lead back roughly 5 points over a season, against a job worth 151.**

**So: the mechanism is real in shape and negligible in size. It is not priced, and it does not need
to be.** This is §4.21 again — the team environment barely moves the back, the job does.

## 3. THE THREE DARTS, IN CARRIES AND TARGETS — the answer to "how much of a share"

From the **09-07 12:58 pull**, `raw_stats` ids 23 (carries) and 58 (targets):

| | carries | share | targets | share | proj |
|---|---|---|---|---|---|
| **Jacory Croskey-Merritt** (WSH) | **196** | **57.1%** | 21 | 28.6% | 151.0 |
| Rachaad White (WSH) | 135 | 39.3% | **46** | **64.3%** | 144.1 |
| Kaytron Allen (WSH) | 12 | 3.6% | 5 | 7.1% | 13.7 |
| **Jordan Mason** (MIN) | **195** | **53.9%** | 17 | 18.8% | 144.9 |
| Aaron Jones Sr. (MIN) | 150 | 41.6% | **61** | **68.7%** | 154.3 |
| **Mike Washington Jr.** (LV) | **89** | **24.1%** | 12 | 11.1% | 62.6 |
| Ashton Jeanty (LV) | 278 | 74.8% | 86 | 83.6% | 246.5 |

**Croskey-Merritt is already ESPN's lead rusher in Washington — 196 carries, 57%.** What he is NOT
is the pass-catcher: Rachaad White owns 64% of the backfield targets. **That is the whole risk**, and
it is the same risk the Aug-18 write-up named — *he must improve his pass-catching to hold the role*.
**Jordan Mason is the identical shape**: 54% of carries, 19% of targets, with Aaron Jones taking 69%
of the targets. **These two are the same bet twice.**

**AND THIS IS WHY MATT'S GUT ON MIKE WASHINGTON IS DEFENSIBLE — state it in his terms.**
Croskey-Merritt and Mason each have to hold off a veteran pass-catcher who already owns two thirds
of the targets. **Washington does not have to beat anybody.** ESPN already banks him 89 carries with
Jeanty healthy; what he needs is the thing that is already live — the ankle. And doc 207 priced that
event: **a back who inherits the job scores 12.0 against 6.1, roughly double**, and the job he would
inherit is 278 carries and 86 targets, the biggest of the three by far.
**§4.13c is the historical echo he is reaching for:** 8 of the 15 late boom seasons in five years
were backs who inherited a backfield. Achane is that archetype and so is this.
**The honest counterweight, once:** it needs an injury to a 22-year-old whose coach has already said
he expects to play, and the flag says Las Vegas is a LEAD BACK team, not an open job. **It is the
lowest floor and the highest ceiling of the three, and §4.13 says round 9+ is exactly where that
trade is free.** His call, and the numbers do not argue with it.

## 4. OPEN

Everything on doc 216 §4 still stands. **New:** the QB-injury null above should join §4.21's
family of team-environment measurements post-draft — it is the same finding a third time.
