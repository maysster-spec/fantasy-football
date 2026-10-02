# 98 — What FREEZE means, what a "swing" means, and who the late darts are

**Date:** 2026-08-30 (late) · **Answers Matt's questions 1, 4 and 5.**

---

## 1. FREEZE HAS NOTHING TO DO WITH ROUNDS 1–4, AND IT DOES NOT BLOCK A REMOVAL

Two different things had got tangled together:

- **FREEZE / REBUILD** is the **Sept 5 verdict only**. `sept5_check.py` re-pulls ESPN's projections
  and asks: *of the top 161 players, how many stayed within 2 slots of where they were?*
  **≥150 → FREEZE** (the board stands, don't rebuild). **<150 → REBUILD.** On Aug 29 it was
  **151 of 161** — one player from a rebuild. That is all it is: a decision about whether a fresh
  projection pull justifies regenerating the board. It is not a lock on any part of the board.
- **"Rounds 1–4"** is a separate, unrelated fact (§4.7): historically **83.3%** of picks in rounds
  1–4 in this league are RB or WR. A tendency, not a freeze.

**Removing a player is neither of those and is never blocked.** There is **no automatic job** — no
detector watches the news, and there never has been. What exists as of tonight is a one-command
manual fix: add a row to `Scripts\news_overrides.csv`, run `py apply_news.py --write`, then
`py make_fallback.py` and `py weekend_check.py --inject`. Roughly two minutes. If a REBUILD later
wipes it, `board_audit.py` fails loudly rather than quietly restoring the player.

## 2. "TAKE YOUR SWINGS LATE" IS NOT A POSITION RULE

It confused Matt because it sits under BENCH on the card and reads like it is about QBs. It is not.

**A swing = when two players are close, take the higher ceiling instead of the safer floor.**
Any position. The reason it is a *late* rule is §4.13, measured:

| where the player is going (ADP) | chance he returns >1.35× projection |
|---|---|
| 25–84 | **2.1–6.2%** |
| **121–180** | **17.0%** |

Each such breakout roughly **doubles** title odds (0 → 4.7%, 1 → 14.4%, 2 → 26.8%). But applying
the tilt across the whole draft **costs $22–41** of expected payout (p=0.003); applied from round 9
it is free and mildly positive, though **not statistically resolved** — a costless option, not a
proven edge. So: **from pick 104 on, break near-ties toward upside. Before 104, never.**

Roster math leaves roughly **3–4** true darts, not "all the late picks."

## 3. NO, THE ENGINE DOES NOT GET RISKIER LATE. THAT PART IS MATT'S.

`[TESTED]` The engine carries **no variance term at all** — the only `sd` in `code_live_engine.py`
is the *opponent* ADP noise (how other managers pick), not player-outcome spread. Every column on
the live board — VBD, adds now, if I wait, and the rollout that orders the list — is an
**expected-points** number. It will never prefer a boom/bust player, and it will never warn that
its top row is the boring one. **The swing is a human override on a near-tie, and only from 104.**

## 4. THE LATE DARTS, AS OF AUG 30

**Read the `eff` numbers with §4.14 in mind: past about pick 120 the board's ADP is ESPN's
undrafted sentinel, i.e. a fabricated ordering.** Those are not real market prices; they say
"nobody" more than they say "pick 150."

**§4.18 says prefer RB.** A dart that hits at RB is worth **+80 to +95** VBD as a 2027 keeper; a QB
that hits is worth **+2 to +5**. Same swing, twenty times the option value.

| player | pos | board `eff` | why he fits Matt's own description |
|---|---|---|---|
| **MarShawn Lloyd** | RB GB | 158.5 | The exact archetype. Jacobs out indefinitely; Lloyd was the presumed starter. But Green Bay just acquired Kaleb Johnson, which reads as doubt about him. One game played since being drafted in 2024. **His price will move fastest of anyone here this week.** |
| **Kaleb Johnson** | RB GB (was PIT) | 158.1 | Newly acquired, into an unsettled backfield, competing with a back as unproven as he is. SI's advice is to dart at both him and Lloyd. |
| **Jonathon Brooks** | RB CAR | 107.7 | Reachable at **104/113**. A 2024 first-round back whose lost time was injury, not talent. The one on this list that is a real pick rather than a lottery ticket. |
| **Jordan Mason** | RB | 129.8 | Right at **pick 128**. PFF late-round value. Note: our board says MIN, PFF says SF — check the team before you take him. |
| **Tyjae Spears** | RB TEN | 149.2 | Right at **pick 137**. PFF late-round sleeper. |
| ~~Tank Dell~~ | WR HOU | 147.3 | **RETRACTED 2026-08-31.** I put him here off an NFL.com sleeper list without checking this project's own `INJURY_CONTEXT_SHEET`, which grades him **AVOID: catastrophic multi-ligament knee, 2 expected games weeks 1–14, falls 231 ranks.** He is a pure recovery lottery ticket at 128/137 and nothing more. This is exactly the gap doc 100's badges close. |
| **Chris Rodriguez Jr.** | RB JAX | 154.3 | NFL.com's round-10 name; strong rush-yards-over-expected. Probably past 137 — a waiver target more than a pick. |
| **Denzel Boston** | WR CLE | 154.1 | Rookie, camp reviews suggest he could end up the team's top receiver. |
| **Ja'Kobi Lane** | WR BAL | 154.9 | Rookie, 6'4"/205 with a 40-inch vertical — a red-zone profile the current room lacks. |

**Cross-check every name here against `INJURY_CONTEXT_SHEET` before acting.** I did not, and
Tank Dell above is what that cost.

**Refresh this on Sept 5**, with the news sweep. Eight days is long enough for half of it to move,
and Jacobs is proof.

---

**Sources:** NFL.com late-round sleepers · PFF RB sleepers/breakouts · SI/onSI Packers backfield ·
DraftSharks Jacobs report. All `[SOURCED]`; none of the projections here are ours.
