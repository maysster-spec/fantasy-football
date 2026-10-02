# 218 — The prerank was eight days stale and nothing was going to rebuild it

**2026-09-07, 18:00 ET. Keeper lock T−60m.** Matt: *"Is the espn player pre-ranking overdue. It
seems a bit off to me, but that could be a separate issue and more due to the model using Cost vs
#1."* **He is right on the first half and right to separate the second half. Both answered below.**

---

## 0. ACTIONABLE

1. **`draft_night.bat` now rebuilds the prerank before injecting it.** New step **4a**,
   `py make_prerank.py --write`, placed after the keeper swap and after `check_kit`.
   **`draft_night.bat` = 6,405 / `633b10b91385af1e`; `check_kit.py` re-pinned for it.** Both committed.
   **Nothing extra for Matt to run — it is inside the 7:00 command.**
2. **The board refresh rate must NOT be lowered, and ESPN cannot kick you for it.**
3. **The prerank and `cost vs #1` are different orderings ON PURPOSE. They should not match.**

---

## 1. THE PRERANK WAS BUILT AUG 30. THE BOARD HAS BEEN RE-FROZEN TWICE SINCE.

| | last written |
|---|---|
| `ESPN_prerank_with_ids.csv` | **Aug 30, 16:58 ET** |
| `board_v8_fixed.csv` | Sep 7, 12:59 ET *(and Sep 3 before that)* |

**And neither `sept5_after.bat` nor `draft_night.bat` ran `make_prerank.py` — zero references in
either file.** So the ordering stored at ESPN, the one its autodraft uses when a clock expires, was
built on the **08-30** ADP. `refresh_adp.py --write` has fired twice since and nothing downstream
knew.

**This is §0.5(d)'s own milestone rule failing on a file it did not name.** The rule says anything
that rewrites the board triggers a re-solve and a re-pin; the prerank is downstream of the board and
was never on the list. **Matt found it by looking at the ESPN page, which is the third time this
project has been saved by him reading a shipped artifact rather than a doc.**

## 2. HOW BAD — MEASURED, NOT ASSERTED

Rebuilt `make_prerank.py` against today's board and diffed the two files, 544 rows in common:

| | |
|---|---|
| median move | **0 slots** |
| mean move | 2.7 |
| moving 10+ | 60 of 544 |
| moving 25+ | 10 |
| **inside the new top 60** | **13 move 6+ slots, largest 14** |

Biggest movers where an expired clock would actually reach: **Marvin Harrison Jr. #74 → #60**,
**Kittle #65 → #54**, **Breece Hall #16 → #27**, Pitts #60 → #51, Odunze #43 → #50.

**So: real, worth fixing, and not a catastrophe.** The order is broadly intact; the worst case was an
autodraft taking a player about eleven slots off. **Fixing it is free, so it is fixed** — and it now
rebuilds on the **post-keeper-swap** board, which is strictly better than anything a rebuild today
could have produced, because the swap rewrites the board at 7:00.

**Sequencing matters and is the reason for step 4a's position:** `check_kit` (step 1) must pass
against the file as it stands, so the rebuild has to come after it; and the swap rewrites the board,
so the rebuild has to come after that too. Between `board_audit` and the injector is the only
correct slot.

## 3. AND HIS SECOND HALF IS ALSO RIGHT: THE TWO ORDERINGS SHOULD NOT MATCH

*"that could be a separate issue and more due to the model using Cost vs #1."*

**Correct, and it is not a defect.** They answer different questions:

- **The prerank** is a static list. It cannot know who has been taken or what Matt's roster needs. It
  exists for one case — the clock expires — and `make_prerank.py` deliberately orders it by *"the
  later of what he is worth and what he costs"* rather than by raw value, because §4.4 measures this
  board at **QB +15.7 and TE +18.0** against consensus and a naked value sort front-loads exactly
  those two positions. That correction is why Stafford sits at #72 with a value that would put him
  at #40.
- **`cost vs #1`** is the live rollout: who is gone, what Matt already has, and what the board will
  look like at his next turn.

**A list that cannot see the room and a list that can will disagree, and the second one is the one
he drafts from.** The prerank is a seatbelt, not a plan.

## 4. THE REFRESH RATE — LEAVE IT, AND THE REASON IS NOT THE ONE HE ASSUMED

Matt: *"the board updates a bit slow... fine and safe not to adjust the refresh rate that ESPN may
kick out anyway."* **Right conclusion, different reason.**

**In `--bridge` mode ESPN is not polled at all.** Picks arrive from the Chrome extension into a local
`bridge_picks.json`; the 0.5-second poll is a local file read. **There is nothing for ESPN to rate
limit and nothing to be kicked from.**

**The delay he sees is the engine thinking, not fetching** — doc 139 measured it: **3–4 seconds on
the clock, 0.4 waiting**, down from 16–20 seconds before `_lineup` was rewritten. The on-clock cost
is `rollout_inner=60`, and doc 139 chose 60 *because* 24 produced **three different winners at pick
32** across ten seeds. **Lowering it to save two seconds would destabilise the single turn where
Matt most needs a stable answer**, and §4.18c forbids changing the objective before the draft
anyway. **No change.**

## 5. OPEN

- **`make_prerank.py` should be in `sept5_after.bat` too**, not only in `draft_night.bat` — any
  future `refresh_adp --write` outside draft night will strand the prerank again. Post-draft.
- **§0.5(d)'s trigger table needs a row**: "anything that rewrites the board" should name the
  prerank explicitly among its downstream artifacts. Post-draft directive edit.
- Everything on doc 216 §4 and 217 §4 still stands.
