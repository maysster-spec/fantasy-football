# 390. THE IR SLOT IS A HELD SEAT, MY CLAIM COUNT WAS WRONG BECAUSE NO FILE CARRIED IT, AND THE ROSTER FILE CARRIES IT NOW

*22 Sept 2026, 16:55 ET. Claude (Cowork), on Matt at 16:45: "Puka is in the IR spot. Remember that option. If called
out before game then status stays as out until further info. The trick is to put the waivers in before the status
changes or then you won't be able to add anyone. This way even if the player does end up playing, you can hold an
extra spot. But if you really need to play him then you can drop whoever you want. I have either option." Doc 389 is
the previous number; 390 reserved by listing `Source\` at 16:47. No em dashes.*

---

## 0. WHAT TO DO

1. **Correction, mine: three adds need TWO drops, not three.** Nacua in the IR slot does not occupy one of the
   fifteen, so the active roster is 14 with a seat free. Doc 388 section 1 counted him as active. Corrected in place.
2. **The advice does not change, and the reason is your own mechanic.** Put a drop on each claim anyway:
   **a claim that carries its own drop leaves the free seat free**, and that seat is what you want the day Nacua has
   to come off IR. A claim without a drop spends it.
   - **Schultz, drop Worthy. Tucker, drop Coleman. Cut the Bengals.** Result: 14 active, one seat still open, Nacua
     on IR.
3. **Fixed so the next session cannot make my mistake: `MY_ROSTER.csv` now writes `slot_id` and `status`.** Both were
   in the payload `wire.py` already reads and neither reached the drive. `check_kit.py` re-pinned, and the old pin was
   shown failing first. The columns appear on the next `ff.bat` run.
4. **Your mechanic is in the directive (§2) in your words, and in `00_START_HERE.md` section 2**, so it is read every
   turn rather than remembered. It went into v9.14 before you pasted it, so it is still one paste.
5. Nothing to run.

---

## 1. WHAT I GOT WRONG, AND WHY THE FILE COULD NOT HAVE TOLD ME

`MY_ROSTER.csv` lists fifteen men with name, position, team, bye and value. **It lists every man on the roster,
including one in the IR slot, and nothing in it says which.** I read fifteen rows, wrote *"Fifteen of fifteen"* and
built the claim arithmetic on it. The payload behind that file carries `lineupSlotId` on every roster entry and
`injuryStatus` on every player; `wire.py` was keeping neither.

**That is the same shape as ledger rows 108 and 162: a fact that exists upstream, is dropped on the way to the file,
and then gets guessed at downstream.** Ledger row 166.

**What changed in the code:** the roster loop keeps `(lineupSlotId, injuryStatus)` per player, and the writer adds two
columns. No script reads `MY_ROSTER.csv`, so nothing downstream breaks on the wider header. `check_kit.py` re-pinned
to 113,803 bytes and `e88f5f3e78b4eeda`; the old pin was run against both files first and reported STALE on the old
one, which is the control. **Untested against a live pull, because that needs your ESPN session: the first `ff.bat`
run is the test, and the thing to look at is Nacua's `slot_id`.**

---

## 2. THE MECHANIC, AS YOU STATED IT, AND WHAT IT IS WORTH

**Your words are the rule; the arithmetic under them is mine.** A man ruled out before the game sits in the IR slot,
his status holds until there is new information, and the claims go in before that status can change. **The value is a
seat, and the seat has two uses:** hold it empty and you can activate him the moment he is cleared, or spend it and
you are choosing, under time pressure, between dropping someone and leaving him on IR.

| what you file | active roster after | free seat |
|---|---|---|
| Schultz with a drop, Tucker with a drop | 14 | **yes** |
| Schultz with a drop, Tucker with no drop | 15 | no |
| all three, two drops | 15 | no |

**So the drops are not a cost here, they are what preserves the option.** Worthy and Coleman are the two spares
either way (doc 387 §2, doc 388 §2), and neither carries a keeper cost.

**What is still unverified and is not asserted anywhere:** which ESPN designations this league accepts for the slot,
whether a man in it counts against a position cap, and whether time there breaks *"rostered all season"* for keeper
eligibility. Nacua was a first-round pick, so he is not keeper-eligible either way and none of that binds this week.

---

## 3. OPEN, BY NAME

- **Matt's:** the two claims and their drops before the run on 24 Sept; Nacua's practice report Wed to Fri; paste
  v9.14 when convenient; the Tuesday task prompt paste (doc 387 §6).
- **Mine:** confirm from the first run which `slot_id` is the IR slot; ledger rows 162, 163, 165; the LA and NYG
  week-2 snap shares; the doc 383 batch on the five-year registry.
