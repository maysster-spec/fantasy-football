# 125 — The evidence file answered it. ESPN publishes the draft order, and that mock is a clone of your league.

**Date:** 2026-09-01. First time in this project a failure was diagnosed from a captured payload
instead of from reasoning. Doc 122's evidence capture paid for itself in fourteen hours.

---

## 1. WHAT THE PAYLOAD SAYS — all of it observed, none of it inferred

`feed_evidence\20260901_061227_firstok_629362362_2026_200.json`, 78,745 bytes:

| field | value | what it means |
|---|---|---|
| `status.createdAsLeagueType` | **21985** | **the mock room is a CLONE of the real E-Discovery league** |
| `teams` | 12, ids **1–7, 9–13** | **there is no team 8.** Team ids are NOT contiguous |
| `settings.draftSettings.pickOrder` | `[13,11,7,12,4,6,5,9,3,1,2,10]` | **team 9 is 8th. Slot 8, published, before pick 1** |
| `draftSettings.keeperCount` | **1** | the room keeps keepers |
| pick at overall 176 | `playerId 4426354, roundId 15, roundPickNumber 8, teamId 9, keeper: true, reservedForKeeper: true` | **George Pickens, in his real keeper slot** |
| `draftDetail.drafted` | **false** | and it stayed false after the room finished |
| `timePerSelection` | 30 | the mock is 30s; the real league is 60 |

**So `--mock` was the wrong flag.** It exists to say *"this room has no keepers, use raw ADP."*
This room has his keeper in it, `keeperCount: 1`, and every real team name. Running it as a mock
threw away the keeper-depletion the room actually needs and forced 14 rounds onto a 15-round grid.

---

## 2. ESPN PUBLISHES THE DRAFT ORDER AND WE WERE GUESSING AT IT

`pickOrder` is a list of teamIds in slot order, **present before a single pick is made.** It was in
the very first payload this tool ever captured.

`detect_shape` was deriving the slot from *picks that had already happened* — which is why it could
not work in an empty room (doc 80 records that failure and its guess-slot-1 bug), and why `--slot`
had to be typed by hand every time.

**Three changes, all verified by execution:**
- **`--slot` is no longer needed.** The order is read: `draft order from ESPN: your slot is 8 of 12`.
- **A supplied `--slot` is CHECKED against it.** `--slot 3` now hard-stops with the order printed.
  A wrong slot mis-plans every turn of the night and nothing else on screen would have said so.
- **The real-draft path checks too.** Bare `py live_draft.py` never called `detect_shape` — slot 8
  is compiled in — so it now prints `draft order confirms your slot: 8 of 12`, or shouts if not.
  **Draft order is reverse final standings; the compiled 8 is an assumption with a date on it.**

---

## 3. THE POLLER RAN FOREVER BECAUSE `drafted` NEVER FLIPPED

Matt: *"when the draft completes the command is still looping instead of ending gracefully."*
The payload shows why — `drafted: false` while `inProgress: true`, and it stayed that way.

**A grid with every slot filled is a finished draft whatever the flag says.** The poller now ends
on that condition. Verified against a feed that fills 0 → 180 without ever setting `drafted`:
`every one of 180 slots is filled -- draft complete.`

---

## 4. ONE SNAPSHOT WAS NOT ENOUGH

The capture saved the **first** successful poll only, so it can prove what the room looked like at
06:12:27 and **cannot prove whether picks ever appeared afterwards.** That is the one question left
about this mock and the evidence cannot answer it.

Snapshots now repeat every 40 polls. A feed that goes quiet mid-draft will be a file, not a memory.

**What is still unknown:** whether ESPN wrote the mock's picks into `mDraftDetail` at all while the
room was live. The next mock answers it with no extra effort — the files will be there.

---

## 5. THE MOCK ROSTER, SCORED

| slot | player | pos | VBD | goes at | flags |
|---|---|---|---|---|---|
| QB | Matthew Stafford | QB | 21 | 75 | |
| RB | Christian McCaffrey | RB | **135** | 8 | DISC · split |
| RB | Kenneth Walker III | RB | **81** | 24 | |
| WR | George Pickens | — | keeper | — | |
| WR | Malik Nabers | WR | 39 | 31 | DISC · split |
| TE | Tyler Warren | TE | 28 | 41 | |
| FLEX | Emeka Egbuka | WR | 31 | 38 | DISC · split |
| BE | TreVeyon Henderson | RB | 9 | 69 | DISC |
| BE | Rico Dowdle | RB | 3 | 89 | |
| BE | J.K. Dobbins | RB | −4 | 103 | **AVOID** |
| BE | Jacory Croskey-Merritt | RB | −17 | 122 | DISC |
| BE | KC Concepcion | WR | −38 | 133 | |
| BE | Rashid Shaheed | WR | −41 | 145 | |

**Shape: 1 QB · 6 RB · 4 WR · 1 TE.** That is the directive's target almost exactly — RB to the
cap, then WR, no QB2, no TE2 (§6). **The structure is right.**

**Three things to look at:**
1. **Stafford at pick ~65 when he goes at 75.** §4.14: QB1→QB2 is a 47-point cliff and then
   **QB2–QB6 spans 11.8 points total.** There is no correct target pick for QB — Stafford at 21 VBD
   and Goff at −15 are nearly the same asset, so paying two rounds early for the plateau is the one
   clear leak here. **Take the QB when the board offers nothing else, not on a schedule.**
2. **Four of the six RBs carry a grade, one is AVOID.** Dobbins has ACL, MCL and Lisfranc history;
   Henderson and Croskey-Merritt are both current. The bench is deep in bodies and thin in
   available bodies.
3. **Warren at 41 is exactly the §4.3 trap.** Only Bowers (+51) and McBride (+48) carry a TE
   premium; Warren is +28 and then a flat tail. Takeable, but the FLEX comparison is raw points and
   the best RB/WR beat the best TE at that pick.

**"Stafford kept showing up as top pick"** — the live board was frozen at pick 1 for the whole mock
(§3 above), so whatever it was showing was a still frame, not a recommendation. Nothing on a page
that is not advancing means anything; that is what the amber WAITING banner is for.

## ASSUMPTIONS

1. **`pickOrder` is stable once published.** It is reverse standings and set at league setup. If
   ESPN reorders it after the fact the check catches that too, which is the point.
2. **A full grid means finished.** True unless ESPN leaves a slot empty on a forfeited pick, which
   has not been seen in 2024, 2025 or any mock.
