# 168 — The page was right, the verdict is real but narrow, and one pin was stale

**Date:** 2026-09-05 (Sat, ~11:00 ET) · **Trigger:** Matt: *"you wanted me to run them in this
order (`refresh_pull.bat` → `sept5_after.bat` → `make_shortcuts.py`), but the commands file
doesn't show them in that order. What am i missing?"*

**Answer: nothing. My reminder was wrong and `COMMANDS.html` is right.**

---

## 1. THE ORDERING — the page is CONDITIONAL, my reminder was SEQUENTIAL

`COMMANDS.html` section 6 lists four cards in this order:

| # | card | command | when |
|---|---|---|---|
| 1 | Read what the 8:00 AM download found | `Get-Content pull_log.txt -Tail 40` | always |
| 2 | **Rebuild everything the new numbers touch** (marked primary) | `.\sept5_after.bat` | always |
| 3 | Run the download yourself **if the computer did not** | `.\refresh_pull.bat` | only on failure |
| 4 | Is the 8:00 AM job actually set? | `Get-ScheduledTask …` | only on doubt |

Card 3's own title carries the condition. The page's section header says it outright:
*"your computer downloads the new projections by itself at 8:00 AM. You read one line, then run
one command."* The pull is a **scheduled task** (`setup_tasks.ps1`), not a step Matt performs.

**My scheduled reminder listed all three as a sequence and told him to start with the pull.** That
is the defect. Two pull files exist for today —
`espn_projections_2026_20260905_0800.csv` and `..._1040.csv` — so the download had already
happened before he read my reminder, and running it again cost nothing but did not need doing.

`ERROR_PATTERNS` class: **a reminder that restates a procedure instead of pointing at it goes
stale the moment the procedure changes, and nothing checks it.** The reminder was written before
the 8:00 AM task existed. Same shape as §7.1's stale pick table and §8's stale ADP vintage line:
prose that duplicates a shipping artifact. **The reminder should have said "open COMMANDS.html
section 6", not restated it.**

## 2. THE VERDICT IS **REBUILD** — and it is real, but it is entirely below rank 120

`sept5_last.txt`: `VERDICT: REBUILD. Only 97/161 held within 2 slots` (threshold 150).

Decomposed by band — this is the number that matters and the script does not print it:

| board rank | n | held within 2 slots | median move |
|---|---|---|---|
| 1–24 | 24 | **24 (100%)** | 0 |
| 25–48 | 24 | **24 (100%)** | 0 |
| 49–84 | 36 | 28 (78%) | 2 |
| 85–120 | 36 | 18 (50%) | 2 |
| **121–161** | 41 | **3 (7%)** | 4 |

**The entire REBUILD verdict is bought by ranks 121–161**, which is §4.14's known-unsound region —
the ESPN undrafted-sentinel blob at adp ≈ 170 where there is no real draft position. Of the 28
board rows whose projection moved ≥15 points, **24 sit at adp 170.0–171.2** — sentinel rows ESPN
simply filled in. They are not information.

`sept5_check.py`'s own per-pick windows agree: picks **8 / 17 / 32 / 41 are 5/5 unchanged**;
56 and 65 are 4/5; 80 and 89 are 3/5.

**And none of it is new.** Measured directly: **0 of 700 projections changed between the 09-03
pull and the 09-05 pull.** The drift is all 08-23 → 09-03, which doc 153 already ruled on
(*"re-time yes, re-price no"*). ESPN re-forecasts in batches; it has not re-forecast since Sept 3.
`[TESTED — full 700-row join, both pulls]`

**What DID move is the market: 172 of 700 ADP rows changed in those same two days.** That is
`refresh_adp.py --write`'s job and it is step 1 of `sept5_after.bat`. §8's standing instruction —
*run it whatever the verdict says* — is correct and is what today proves.

## 3. THE OVERRIDE CARD IS SIX NAMES. THREE OF THEM MATTER.

Ran `mkoverride.py`'s exact filter (`rank ≤ 175 or new_rank ≤ 175`, `|Δproj| ≥ 15`) against the
09-05 pull. It will print these six — the same six as 09-03, necessarily, since no projection moved:

| player | pos | tm | adp | rank → | proj → | Δ |
|---|---|---|---|---|---|---|
| **Josh Jacobs** | RB | GB | 72.0 | 435 → 93 | 0.0 → 152.5 | **+152.5** · *news override holds* |
| Isiah Pacheco | RB | DET | 159.7 | 143 → 208 | 114.9 → 66.6 | −48.3 |
| **MarShawn Lloyd** | RB | GB | 120.4 | 184 → 131 | 78.2 → 124.4 | +46.2 |
| Kayshon Boutte | WR | NE | 170.6 | 188 → 143 | 72.3 → 113.4 | +41.1 |
| **Kyler Murray** | QB | MIN | 137.3 | 141 → 90 | 289.3 → 327.2 | +37.9 |
| De'Zhaun Stribling | WR | SF | 138.9 | 145 → 116 | 109.0 → 134.1 | +25.1 |

Boutte's adp 170.6 is the sentinel — ignore. Pacheco is a fade at a pick Matt does not reach.

**Kyler Murray is a coupled move and the pull proves the mechanism:** J.J. McCarthy fell
46.3 → 12.0 in the same batch. Minnesota's QB job resolved to Murray. At **327.19** he is now
within **0.15 points of Jared Goff (327.04)** at essentially the same price (adp 137.3 vs 136.5).
**§4.18's draft-night rule at 104/113 asks for "Goff's tier or better" — that tier now has two
bodies instead of one.** It does not change the rule; it makes it easier to execute. Both still
price out as **128/137** picks, not 104/113.
`[SOURCED: 09-03 and 09-05 ESPN pulls; team confirmed MIN on board and pull]`

**De'Zhaun Stribling** — the player Matt asked about on Sept 4 as a late stash — was raised
**+25.1 by ESPN itself** and moved rank 145 → 116. ESPN moved toward Matt's read, independently.

## 4. JOSH JACOBS — OUR BOARD IS NOW STRICTER THAN ANYONE ELSE

`news_overrides.csv` zeroes him (`action=out`, dated 2026-08-30), note: *"draft as if he does not
play in 2026."* That was right on Aug 30. Six days later the world has moved and we have not:

| source | as of | says |
|---|---|---|
| our board | 08-30 | proj 0.0, **rank 435 of 480 — undraftable at any price** |
| ESPN projection | 09-03 → today | **241.0 → 152.5**, `injuryStatus` QUESTIONABLE → **DAY_TO_DAY** |
| ESPN ADP | 08-30 → today | 38.6 → 72.0 → **81.8**, still falling |
| SI (Aug 31) | — | *"highest-risk player in all of fantasy football"*; **not before round 10**; rounds 11–12 as a bench RB; **RB37**; ~6 games missed, highly variable |
| Packers (Sept 1) | — | expect him to play this season, prepared if he does not |
| legal | Sept 4 | initial court appearance rescheduled; no resolution |

ESPN's 152.5 is **63% of his 241.0** — it is ESPN pricing roughly six missed games, which is the
same number SI reached independently. **Nobody has him at zero. We do.**

**This is a live gap, and it lands exactly in §4.13's dart window (128/137).** Two things are true
at once and must not be collapsed:
- The override is **right about the ORDERING** — Jacobs must never be the engine's recommendation
  at pick 80, which is where an un-zeroed 152.5 would put him. `mkoverride.py` printing
  `NEWS OVERRIDE HOLDS, IGNORE THE PULL` is correct for the board.
- The override's **NOTE is now stronger than the evidence.** "Draft as if he does not play in
  2026" is not what ESPN, the Packers, or the consensus say today.

**RECOMMENDATION — Matt's call, not mine, and NOT a board change.** Leave `news_overrides.csv`
alone (changing `action` rebuilds the board 48 hours out and re-opens `board_audit`). Carry it as
a one-line rule on paper instead:

> **Jacobs: never before pick 128. At 128 or 137, if he is still there, he is a legitimate dart —
> the board's zero is a safety rail, not a projection.**

MarShawn Lloyd is the same bet from the other end and is the consensus-preferred one (SI: RB33,
"mid-to-late 20s" overall, i.e. earlier than Jacobs). Our board has Lloyd at rank 184 on a
projection ESPN has since raised **+46.2**. He is live at **104 / 113 / 128**.

## 5. §2.1(c) DOES NOT MOVE ON THIS FREEZE — re-solved, with a negative control

§7.1 says the keeper-depletion table is a function of the ADP freeze and must be re-solved
whenever `refresh_adp.py` writes. Re-solved as the same fixed point on the 09-05 keeper ADPs:

```
09-03  [28.2, 29.4, 29.4, 32.9, 41.0, 42.2, 42.4, 44.2, 45.1, 47.3, 78.7, 101.6]
09-05  [28.2, 29.4, 29.4, 32.6, 40.4, 42.3, 42.3, 44.0, 45.0, 47.1, 78.0, 101.9]
```

**All fourteen rows unchanged.** 8→0 · 17→0 · 32→4 · 41→10 · 56→10 · 65→10 · 80→11 · 89→11 ·
104→12 · 113→12 · 128→12 · 137→12 · 152→12 · 161→12. **No directive edit needed after today's
refresh.** `[TESTED]`

**Negative control run first:** the same solver on the **09-03** ADPs reproduces directive v7.1's
published table at all fourteen rows exactly. A solver that could not reproduce the known answer
would not be allowed to certify the new one.

**§3 IDENTITY TRAP, CAUGHT IN FLIGHT.** The first solve came back one keeper short from pick 41
down (9/10/11 instead of 10/11/12) and looked like a real table move. It was a **name join**:
`predicted_keepers_v5.csv` says `Travis Etienne`, the pull says **`Travis Etienne Jr.`** The
missing 41.0 in the ADP list is exactly the value §7.1 publishes. §3's rule — *a name join is a
defect even when it currently matches 100%* — for the second time this week, and this one would
have shifted every pick from 41 to 161 by one in a directive edit.

## 6. ONE STALE PIN, FOUND AND FIXED

`check_kit.py`'s manifest still pinned `sync_desk_copies.py` at **5,674 / c3d8fae0aed3e8d7**. The
file on disk is **7,863 / ae420c15c4c1e550** — I restored its doc-146 staleness guard on Sept 4
and never re-pinned it.

`check_kit.py` runs **inside `draft_night.bat` at 6:55 PM Monday.** It would have gone red against
a file that is correct. That is doc 97 §5's exact failure mode — *"every false failure in this
sweep has been a test reading the wrong object; not once has it been the code"* — and a false
STALE at 6:55 PM is worse than no checker, because it teaches you to wave the next one through.

Fixed and committed. Verified against the whole draft path: `sept5_after.bat` (7,388) and
`draft_night.bat` (5,873) both match their pins exactly — their larger raw sizes on disk are CRLF,
which `check_kit.sha()`/`size()` normalise away by design. `mkoverride.py`, `make_howto.py` and
`to_pdf.py` all match. **`sync_desk_copies.py` was the only real mismatch in the kit.**

---

**Files:** `Scripts\check_kit.py` 20,274 → 20,689 (`4d846e685032710b`).
Nothing else written — no board change, no override change, 48 hours out.

**Open, and Matt's:** the Jacobs paper rule above, and whether to carry Lloyd as the preferred
Green Bay bet at 104/113.
