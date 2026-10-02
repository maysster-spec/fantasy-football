# 154 — The ink was on the wrong column

*2026-09-04, T-3. Matt: "I forgot how I avoid a position drought AGAIN!!! Is position cliffs on
the lower part my only guide?" and "Cost vs #1 is now the only one that really stands out… Make
sure the most important information for my decision is given thought and correct treatment.
Red team how the board should look."*

---

## 0. FIRST, A CORRECTION TO DOC 153 — I MEASURED ON A STALE BOARD

`refresh_adp.py --write` **had already been run on Matt's machine at 13:18 on Sept 3.** The live
board carries the 09-03 ADP exactly (`|adp_pick − espn_adp|` median **0.00**, max **0.00**, 480
rows). My working copy did not. So:

- **Doc 153 §5's "D — re-timed" column was measuring a change that is already applied.** It is not
  a proposal; it is a description of what happened yesterday afternoon. Read it that way.
- **Doc 153 §5 and §8's margins were computed on the pre-refresh board.** §6 replaces them.
- **Doc 153 §3, §4 and §6 are unaffected** — they compare *ranks*, and `refresh_adp` does not touch
  rank (verified: rank is identical between the two boards, all 480 rows).
- The verdict is unchanged: **re-time yes, re-price no.**

I also nearly filed a second false alarm on top of it: `device_list_dir` reports **raw** file sizes,
`check_kit` pins **line-ending-normalised** ones, and `board_v8_fixed.csv` differs by exactly 481
bytes — its 481 CRLFs. I had the STALE banner half written. Recomputed properly: **41,092 /
`ba778ceadab825e0`, pin matches to the byte.** `§0.2 — reproduce the failure first.`

---

## 1. THE DROUGHT GUARD ALREADY EXISTED. IT WAS JUST IN THE WORST PLACE ON THE PAGE.

No — the cliffs panel was never the only guide. There are three layers, and Matt could reasonably
see only one of them:

| layer | what it answers | where it was |
|---|---|---|
| the starter strip `QB 0/1 …` | *am I short a starter?* | 12px mono, **bottom of the roster panel**, far corner |
| POSITION CLIFFS | *how much value evaporates before my next turn?* | its own panel, bold drop column |
| `code_live_engine.legal()` | *the board stops offering anything else* | **nowhere — invisible** |

**The third one is a hard guard and it works. `[TESTED by execution, 2026-09-04]`**

```
roster: 3 RB, 3 WR, no QB, no TE          roster: 3 RB, 1 QB, no TE
  4 turns left -> QB RB TE WR               3 turns left -> QB RB TE WR
  3 turns left -> QB RB TE WR               2 turns left -> QB RB TE WR
  2 turns left -> QB TE   <-- forced        1 turn  left -> TE   <-- forced
  1 turn  left -> QB TE
```

`recommend()` then returns only those positions — confirmed on the real object: with RB and WR at
their caps and no QB or TE, the twelve rows came back Allen, Bowers, McBride, Warren, Lamar,
Burrow. **Matt cannot finish this draft without a starting QB and a starting TE.** The tool takes
the choice away first. It just never said so, so the forcing would have arrived as a surprise in
round 11 with a 60-second clock running.

---

## 2. WHAT DESERVES THE INK — MEASURED, NOT DESIGNED

`emphasis.py`, 12 rooms drawn under §4.12's affine noise on the **current** board,
`rollout_inner=24`, all twelve skill picks, 144 board states. For the twelve rows actually
displayed: the spread of `cost vs #1` (the only bar on the page) against the spread of
`still there?`.

| pick | margin #1v#2 | **cost spread** | **p(next) spread** | rows tied to #1 | their p(next) gap |
|---|---|---|---|---|---|
| 8 | 13.56 | **44.61** | 77pp | 0.0 | — |
| 17 | 4.99 | 34.31 | 60pp | 0.4 | 2pp |
| 32 | 13.37 | 37.64 | 74pp | 0.2 | 6pp |
| 41 | 7.77 | 24.37 | 92pp | 0.2 | 1pp |
| 56 | 2.32 | 10.89 | 86pp | 0.3 | 56pp |
| 65 | 2.47 | 5.19 | 78pp | 1.7 | 40pp |
| 80 | 0.58 | 2.67 | 85pp | 3.7 | 50pp |
| 89 | 0.47 | 2.19 | 83pp | 5.0 | 51pp |
| 104 | 0.31 | 1.34 | 58pp | 6.1 | 50pp |
| 113 | 0.28 | 1.09 | 64pp | 6.0 | 48pp |
| 128 | 0.06 | **0.18** | 48pp | 7.0 | 41pp |
| 137 | 0.06 | **0.12** | 0pp* | 7.0 | 0pp* |

**The quantity carrying the only bar on the page collapses by 370× — 44.61 points of spread at
pick 8 to 0.12 at pick 137. The quantity carrying no treatment at all does not collapse: 48 to 85
percentage points, all night.** And from pick 80 on, **four to seven of the twelve rows** sit
inside 1.5 of the recommendation — the engine's own "I cannot separate these" — while those tied
rows differ by **40 to 51 points of survival**.

*\* pick 137 has no next skill turn, so every `p_next` is 1.00 and the column is meaningless
there. That is a real property, and it became a gate in §3.*

**This is the defect, stated plainly: from round 7 the board draws its loudest mark on noise and
leaves its only remaining signal in plain grey text.**

---

## 3. THE TWO CHANGES

**(a) The starter strip moves to full width, directly under the hero, and gains two facts.**
It was `QB 0/1 RB 2/2 WR 6/2 TE 0/1`. It is now, on one line, above the board:

```
QB 1/1   RB 3/2   WR 1/2   TE 0/1   FLEX 1/1              7 skill turns left · still no TE
QB 0/1   RB 4/2   WR 3/2   TE 0/1   FLEX 1/1   FORCED — only QB and TE from here. 2 turns left.
```

- **FLEX.** Nine starters, not eight. A strip that stopped at TE could not say whether the FLEX
  was covered.
- **`full`.** A small grey tag when a position is at this roster's cap (`CAPS = {'QB':2,'TE':2}`,
  RB/WR 6), because at that point the board stops offering it and never said why.
- **The forcing, announced one turn early.** Computed from the same rule §1 tested, so the page
  now tells the truth about its own behaviour instead of surprising him with it.

**(b) `still there?` gets a categorical mark — `goes first` — and no bar.**
Doc 147's entire lesson is that a second magnitude bar competes with the one that decided the
pick, so the answer to "should other columns get similar treatment" is **no bars, ever again**.
A mark is different: it fires rarely, it says one thing, and it cannot be read backwards.

It fires only when **all four** hold: the row is not row 1; the engine has already called it a
**tie** (`|cost| ≤ 1.5`); the row is **at least 20 points less likely to survive** than the
recommendation; and the player's `adp_pick` is **under 168** — §4.20's own dart gate, because past
it §4.14 says the ordering is fabricated and ink on a survival number there would be ink on an
invented one.

**Measured firing rate, 12 engine-driven rooms, 144 states: 0.43 marks per render overall — 0.00
at picks 8/17/32, and 0.5 to 1.2 per render at picks 80–128.** Silent exactly where the engine has
an opinion; present exactly where it does not. The adp gate costs **nothing** (identical counts
with and without) — a sentinel player cannot have a 20-point survival deficit, because they all
share one ADP.

**AND THE HONEST PART, which is in the legend too.** `rollout_scores()` already simulates who will
be gone, so **a tie is a tie *after* survival is counted.** `goes first` is *not* a tiebreaker that
beats the engine. It says: of these equally-good rows, this is the one available **only on this
turn** — which is what you act on when you hold something the board cannot see. Per doc 153 §8,
late in the draft those human inputs are the only tiebreakers there are.

**What it looks like at pick 65** (the case it was built for): the engine says Tucker Kraft by
**+0.2** — "a coin flip", and the whole `cost` column spans 1.5 points, i.e. nothing. Four rows now
read `goes first`: Dowdle **42%**, Warren **17%**, Pollard **20%**, Henderson **8%**. Kraft himself
is **71%** to still be there at pick 80. The board is no longer saying "take Kraft, the others are
worse"; it is saying "these five are the same, and four of them are gone if you wait."

---

## 4. WHAT I DELIBERATELY DID NOT DO

- **No second bar.** Not on VBD, not on Δ, not on survival. Doc 148 found the VBD bar drawn from
  `abs(vbd)` marking the *worst* player on the screen with the longest bar from pick 89 on; doc 147
  found the bar on Δ, which is not the sort key. Two bars is that defect waiting to recur.
- **No colour on `adds now` / `if I wait` / `Δ`.** They are the *why* behind the pick, read after
  the decision, not during it. Emphasis there competes for nothing.
- **No change to any number.** Not one line of engine code was touched. `code_live_engine.py`,
  `board_v8_fixed.csv` and `player_context.csv` are byte-identical to this morning.
- **No conditional block that changes page height.** See §5.

---

## 5. RED TEAM OF MY OWN CHANGE — THREE DEFECTS, ALL MINE, ALL BEFORE IT SHIPPED

**1. The gate used the wrong "next turn".** I wrote `nxt is not None` and a comment claiming it
guarded pick 137. `nxt` is the *display's* next turn and includes the D/ST and K picks, so at 137
it is **152, not None**, and the gate would not have fired. Harmless today — a 20-point gap cannot
exist among twelve 1.00s — but **the comment claimed a guard the code did not have**, which is doc
149's lesson word for word. Replaced with the engine's own
`next((q for q in CLE.MY_PICKS if q > pick_no), None)`.

**2. `float:right` inside `overflow-x:auto` can grow a scrollbar**, which changes the strip's
height between refreshes — the exact class of defect doc 139 fixed by pinning the board's shape.
Rewritten as flex with `margin-left:auto`. **Verified by measuring the rendered box, not by
looking:** strip height **33px** and board top **199px**, identical across the plain state, the
`full`-tag state, the four-mark state, the warning state and the FORCED state, and at viewport
widths 1500 / 1100 / 880.

**3. My first legend implied the mark overrides the engine.** It does not — see §3(b). Rewritten
before shipping.

**And one defect in the harness, which is why the numbers in §2 can be trusted.** My first render
sweep printed `0 skill turns left` at pick 128. The strip was right; my test rig was adding Matt's
own players to the pick feed twice, so by round 11 the feed was ten picks long and `pick_no` had
run past 137. Fixed, and the turns then counted 12 → 1 correctly. **A test rig that lies produces a
bug report about working code.**

---

## 6. VERIFICATION LOG — everything below was executed, nothing was read

| check | result |
|---|---|
| board shape across all 12 picks, engine-driven room | `[(12, 3)]` — one shape, doc 139 holds |
| starter strip present at every pick | 12 of 12 (pick 152/161 use `render_streamer`, which has no board — unchanged) |
| all three strip branches | plain count · one-turn warning · FORCED — each forced by roster and pick number, each fires at the turn count `legal()` actually changes at |
| strip height / board top | 33px / 199px at 5 states × 3 viewport widths |
| `goes first` firing rate | 0.43 per render; 0.00 at picks 8/17/32; 0.5–1.2 at 80–128 |
| adp<168 gate cost | zero — identical counts gated and ungated |
| engine untouched | `code_live_engine.py`, board and context byte-identical |
| `check_kit` re-pinned | `live_draft.py → (117942, '25b4b61babd4d497')` |

---

## 7. LIMITS

- **12 rooms.** The *shape* of §2's table — cost spread collapsing, survival spread not — is
  monotone and large (370×), so it is not a sampling artifact. The individual per-pick numbers are.
- **`rollout_inner=24` against 60 on the clock.** Doc 139 showed low inner inflates small margins
  through a winner's curse, so §2's margins are upper bounds. They are already near zero late.
- **§4.15 stands: `p_next` is simulated and biased optimistic**, and this change gives it *more*
  visual weight. That is why the mark needs a **20-point** gap and the adp<168 gate — it fires on
  differences far larger than the model's own error, and never in the region §4.14 calls
  fabricated. It is still a simulated number and the legend says so.
- **`goes first` has not been shown to improve a decision.** It surfaces a fact the engine has
  already priced. The argument for it is doc 153 §8 — late, the margins are zero and the human
  inputs are the only tiebreakers — not a measured gain in points. `[HYPOTHESIS]`, and labelled as
  one; nothing was tuned to it.
