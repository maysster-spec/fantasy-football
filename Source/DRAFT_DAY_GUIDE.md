# Draft Day Guide

> **This file is the master.** `DRAFT_DAY_GUIDE.pdf` is a build artifact regenerated from this
> source — don't hand-edit the PDF. Corrections go here first, then the PDF is rebuilt from this
> file and re-shared. Folds in doc 77's corrections (2026-08-29), the same-evening §2 fixes, and
> **doc 79's doc-vs-code drift pass (2026-08-30)** — §3, §4, §9 and §10 below were describing a
> version of the tool that no longer exists.

**Read this once, straight through, before draft night.** It explains what the tool does, how to
launch it, what its numbers mean, and the full 7:00–8:00 PM sequence. Keep the DRAFT_CARD beside
you *during* the draft instead — this document is for understanding, not for glancing at under a
60-second clock.

---

## 1. What this system is

You have two things: a **board** (`board_v8_fixed.csv`) — every draftable player ranked by
value-based points for this league's scoring — and a **live tool** (`live_draft.py`) that polls
ESPN's own draft feed on your machine roughly every 3 seconds and recommends the best available
pick, computed by simulating the rest of your draft thousands of times against a model of your
eleven opponents.

**It is advisory only.** It never clicks, types, or submits anything into ESPN. You make every
pick yourself, in ESPN's own draft room, on your own screen. The tool watches, recomputes, and
tells you what it would do — nothing more. If you let your 60-second clock run out, ESPN autodrafts
from a list you inject beforehand (the "prerank"). That's a safety net for a missed clock, not a
plan to rely on.

---

## 2. Before you trust it: the pre-launch timeline

| when | what | notes |
|---|---|---|
| **Today** | `py check_kit.py` | — |
| **This weekend (Sat–Sun)** | The four-test kit — §6 below. ~20 minutes. Includes `py fetch_keepers.py --dry` — untested until now, and testable today since keepers are already selected; the 7:00 PM lock only freezes them. | Do this by Sunday night, not in the last 48 hours. |
| **Sat Sept 5 (T-48h)** — **[AUTO]** | Injury/news sweep posts itself to `claude/66_sep5_news_pass.md` at 9 AM ET — push + email. **This one step happens on its own — nothing to launch, nothing to run.** | Heads-up only. |
| **Sat Sept 5 (T-48h)** — **[MATT]** | `refresh_pull.bat` fires at 8:00 AM on its own — it runs the pull AND then `sept5_check.py`, which IS doc 64 §1's board-order test (it swaps the new projections into the board, recomputes VBD on the shipped replacement levels, re-ranks the top 161, and prints **FREEZE** or **REBUILD**). It also re-derives the four replacement levels from the full pull and lists every projection that moved more than 25 points. **You do:** read the VERDICT line, then run `py check_kit.py`. That is the whole job. **The FantasyPros ADP re-download is OPTIONAL** — tested doc 79: no script in the draft path reads it. But **ESPN's own ADP is NOT optional and is now a separate step (doc 109).** `sept5_check.py` compares projections only, so the FREEZE/REBUILD verdict says nothing about the market. Measured Aug 23 → Aug 30: projections moved on 47 of the top 161; **ADP moved on 160 of 161**, and only 104 stayed within 2 slots of their old order. ADP drives every `eff_pick`, every "take at 104" on the paper sheets and every `p(next)` on the live board. **So after the verdict, whatever it says, run `.\sept5_after.bat`** — five gated steps in the required order (re-freeze the market → prove the board → rebuild the depth map → rebuild the three sheets → rebuild the paper board), then reprint. The individual commands are on COMMANDS.html section 4b if the batch stops on a gate. | **~10 minutes.** |
| **Before Sunday Sept 6 night** | Right-click **`Scripts\`** in Google Drive → **"Available offline."** Mark **`Source\`** too. | Cheap insurance against a Drive hiccup stalling a 60-second pick. **The kit folder alone is not enough** (doc 79): `draft_night.bat`, `check_kit.py`, `fetch_keepers.py` and `keeper_swap.py` all live in `Scripts\`, and `keeper_swap.py` reads two files out of `Source\` (`code_universe_v5.csv`, `espn_projections_2026_20260823.csv`). An unhydrated `Source\` fails the 7:00 PM keeper swap, not the 8:00 PM board. |
| **Mon Sept 7** | See §7, the full runbook. | |

---

## 3. Launching a mock or sandbox draft

Two modes, both in `live_draft.py`. (The script's top-of-file comment used to show a `--mock LEAGUE`
form that does not run; the comment was corrected in the file itself, doc 79.)

**A. Sandbox replay — no ESPN needed, replays last year's finished draft as if live:**
```
cd "G:\My Drive\_Fantasy\2026\Scripts\live_draft"
py live_draft.py --replay 2025
py live_draft.py --replay 2025 --speed 0.2      # faster
```
Touches nothing real. **The browser does NOT open by itself in replay mode** — the replay branch
returns before the `webbrowser.open()` call. (Re-verified doc 79. The line numbers this guide used
to quote were four rewrites out of date; behaviour is the durable claim, line numbers are not.)
When it finishes, open
`live_draft\live_board.html` yourself to see the final state. (In a real draft, the browser *does*
open automatically — this only applies to `--replay`.)

**B. Live ESPN mock draft — join a real mock room, point the tool at it:**
```
py live_draft.py --mock --league 123456 --slot N --teams N
```
Get the league id from the browser URL after joining. `--slot`/`--teams` auto-detect if omitted.

**What a mock can and can't tell you.** A public mock does not reproduce this league — it has no
keeper depletion (the single biggest structural feature of your real draft) and the opponents are
generic, not your eleven managers. Expect survival numbers from a public mock to run too
pessimistic early. What mocks *do* buy: an ADP-drift check against the current board, and reflex
practice on the pick-8 decision, which sits inside a narrow edge and shouldn't be made cold under
a clock. An ESPN-hosted mock specifically is the better test for where RJ Harvey goes, since it
samples the same market your opponents see.

**Log this per mock** (about a minute): who was gone at 8/17/32/41, what you took, what you wish
you'd taken, WRs taken in picks 1–7, TEs gone by 32 (and where Bowers/McBride went), RJ Harvey's
pick number. Four or five mocks is plenty.

---

## 4. Reading the recommendation

**These are the column names actually on the screen.** An earlier version of this guide named
`roll`, `mv` and `hold` — the internal variable names. They have not been on the page for several
rewrites, and the board carries a plain-English glossary under it that says the same thing.

| column | meaning |
|---|---|
| **VBD** | season points above a replacement starter at his position. The pure "how good is he", comparable across positions. |
| **adds now** | points he adds to your *starting lineup* if you take him now. Lower than VBD when that slot is already filled. |
| **if I wait** | what the best player at the *same position* is expected to add if you skip him and take that position at your next turn. |
| **Δ** | adds now − if I wait. **A tempo number: how fast that position is falling. It is NOT the ranking.** |
| **cost vs #1** | **this is what orders the list.** Every row is scored by simulating your whole remaining draft after taking him; this column is that score minus row 1's. `free` = row 1 = the recommendation. |
| **p(next)** | chance he survives to your next turn. |

**The big amber number in the TAKE panel is the margin over the row below it** — how much better
row 1 is than row 2, in rollout points. It used to show Δ, which is a different quantity and could
read `+2.0` while a row further down showed `+13.0` (doc 79). If that number is under ~1.5, the top
two are a coin flip and your own read is free.

**Override is free.** Pick whoever you want in ESPN's room — the next poll sees your real roster
and re-plans everything after it around what you actually have. `cost vs #1` is what any gut call
is worth giving up, priced in points, before you make it.

The engine takes 3.6–12.7 seconds to compute depending on lookahead depth, and it recomputes
during *other* managers' turns, not yours — so a recommendation should already be sitting there
by the time your clock starts.

---

## 5. Draft night runbook

**This is now scripted, not a manual sequence you run step by step.** Three things were built
after this guide was first written: `fetch_keepers.py` (reads the actual 12 keepers off ESPN),
`draft_night.bat` (runs the whole 7:00 PM sequence in order, pausing at each step for you), and
`setup_tasks.ps1` (registers the scheduled tasks below, one time, in one run).

| time | action |
|---|---|
| **6:45 PM** | Calendar alert. Be at the desk. |
| **6:55 PM** | Scheduled task **FF2026 - DRAFT NIGHT** opens `draft_night.bat` by itself. **It pauses at every step — you are the gate, not a spectator.** It runs: `check_kit.py` → `fetch_keepers.py --dry` (review the 12 names) → `--write` → `keeper_swap.py --check` → `--write` only if changed → injector → live board. |
| **7:55 PM** | Live board is up. **Two lines to eyeball, both printed for you:** `team 9 = JUG "..."  <- IS THIS YOU?` and the first poll line reporting **12 keeper rows.** |
| **8:00 PM** | Draft. 60 sec/pick. Your picks: **8, 17, 32, 41, 56, 65, 80, 89, 104, 113, 128, 137, 152, 161.** |

**If the batch file fails at any step, every command above still runs by hand, in that same
order.** An automation with no documented manual fallback is a single point of failure, so here it
is: `check_kit.py`, then `fetch_keepers.py --dry` then `--write`, then `keeper_swap.py --check`
then `--write` if it says anything other than IDENTICAL, then the injector, then
`cd live_draft && py live_draft.py`.

**You still don't need to rebuild the board from scratch at 7:00 PM** — availability comes
straight off ESPN's live feed by `espn_id`, not from the board file, so a wrongly-predicted keeper
never shows as available by mistake. **One exception, and it's the reason `keeper_swap.py`
exists:** if a team keeps someone we did *not* predict, the player we wrongly *removed* from the
board is genuinely draftable this year but was never put back — invisible to the engine all night
unless something re-adds him. `keeper_swap.py` is that something: it re-adds him and re-ranks. If
`--check` reports IDENTICAL, all 12 predictions were right and there's nothing to do. **This also
means `board_v8_fixed.csv` has a real, working builder again for this one purpose** — see §8.

---

## 6. The test kit — verify before you rely on it

**Test 1 — Injector, two runs:**
```
py espn_draft_injector_Gemini.py
```
Must show both lines:
```
ESPN reports 544 players stored (sent 544).
count matches. first stored id = 4429795 (expect 4429795).
```
Run it again immediately — second run must also say **544** (confirms it replaces, not appends).

| you see | meaning | do |
|---|---|---|
| `512 stored` | all 32 D/ST rejected (negative ids) | not fatal, but note it |
| any other count | list truncated | note the number |
| `Update Failed`, 401/403 | cookies expired | `py set_cookies.py` — see §12 |
| `(read-back failed)` | unverified — re-run once; repeat = treat as fail | |
| "Pre-draft rankings updated." with **no** "ESPN reports…" line above it | the write was never verified — this is the silent-success trap | treat as fail |

**Test 2 — Live board replay:**
```
cd live_draft
py live_draft.py --replay 2025 --speed 0.2
```
Must print near the top: `replay: 180 rows fetched (12 flagged keeper).`
`(0 flagged keeper)` or `168 rows` means the keeper filter is broken — the board would run 12
picks ahead of reality all night. Stop and fix before Sept 7.

**Test 3 — ESPN-side confirmation:** Draft → Pre-Draft Rankings on ESPN shows #1 = Jahmyr Gibbs,
defenses present somewhere in the list, and the list ends at Chad Ryland (K).

**Test 4 — Keeper fetch, dry run:**
```
py fetch_keepers.py --dry
```
Pass = 12 rows, matching the names on your actual ESPN league page. `0 rows` = ESPN doesn't expose
keepers before lock — fall back to typing them in by hand on draft night. `401/403` = cookies
stale — run `py set_cookies.py` (§12). Better to find that out this weekend than at 7:02 PM.

All four pass = the stack is verified end to end.

---

## 7. Nuances that only surface on draft night

- **ESPN cookie expiration (401/403).** **FOUR** files carry cookies, not two, and as of Aug 30
  `Espn_pull_projections.py` was carrying a *different* `espn_s2` from the other three. Do not
  hand-edit them. Run `py set_cookies.py` — §12 has the whole procedure. It tests the new values
  against ESPN **before** it writes anything, and fixes all four at once.
- **The keeper-row count at 7:55 PM is the single most consequential thing to eyeball.** If it
  isn't 12, stop and use DRAFT_BOARD rather than trust the live recommendations.
- **A Google Drive hydration stall on the board CSV mid-draft is untested** — mitigated, not
  eliminated, by "Available offline" (§2). If the board ever seems to freeze or lag mid-pick,
  don't wait it out past your clock — go to DRAFT_BOARD.
- **Team ID is confirmed as 9** (matches your ESPN team URL, verified Aug 28). As of Aug 30 the
  tool no longer asks you to take that on faith: at startup it reads your team from ESPN and
  prints `team 9 = JUG "..."  <- IS THIS YOU?`. If that name is not yours, stop — every roster
  panel, position cap and bye check would be running against someone else's team all night. The
  fix is `py live_draft.py --team N`.
- **A late injury still has no automated *detector*, but it now has a one-command *fix*.** When you
  hear something — a suspension, a season-ending injury, a trade — add a row to
  `Scripts\news_overrides.csv` and run `py apply_news.py --write`. It sinks the player to the
  bottom of the board *and* the prerank, archives the originals, and re-pins check_kit. Then
  `py make_board.py` reprints the paper board (it names the removed player in red at the top),
  and `py weekend_check.py --inject` pushes the corrected prerank to ESPN — **that last step is not
  optional; until you re-inject, ESPN's queue still rates him where he was.** `board_audit.py`
  fails loudly if a rebuild ever wipes an override. This was built on Aug 30 because Josh Jacobs
  went on the Commissioner's Exempt List at board rank 20, with an effective pick of 32.4 — your
  pick 32 almost exactly. The Sept 5 news sweep is still the only automated check, and it only runs
  once. Anything that happens between Sept 5 and the
  draft — including during the draft itself — isn't watched by anything in this system. The board
  being "frozen" doesn't mean news is being ignored; it means the *rankings* don't get rebuilt.
  New information is always meant to be a manual override at the pick, same as Tank Dell in §8 —
  but for a real injury, you have to be the one who catches it. ESPN's own draft room shows a live
  injury tag next to each name; that tag, not this board, is your actual safety net for anything
  that surfaces after Sept 5.

---

## 8. Settled — do not re-litigate these on draft night

- The injector's file path points at `Scripts\live_draft\ESPN_prerank_with_ids.csv`, confirmed by
  a direct read of the file that actually runs, Aug 28.
- `Source\live_draft\` no longer exists — it was verified byte-for-byte against
  `Scripts\live_draft\` and trashed Aug 28. Any document still describing it is out of date.
- The pull script's completed-season guard (`confirm_seasons()`) is real and active.
- Team ID = 9.
- No board rebuild is required at keeper lock (§5).
- **The board passed its freeze test on Aug 28** (doc 64): rebuilt from that day's pull and
  compared to `board_v8_fixed.csv`, replacement levels matched to 3 decimals and the top 161
  matched within 2 slots for 150 of 161 players — including full agreement at picks 8, 17, 32, and
  89. No rebuild was triggered; the file stands as-is. **Update, doc 77: `board_v8_fixed.csv` now
  *does* have a builder, but only for one specific job** — `keeper_swap.py` reproduces the shipped
  480-row board exactly from the 12 keeper predictions, so it can correctly re-add a player who was
  wrongly predicted as kept (§5). That is not the same as doc 62's original question — rebuilding
  the whole board from a *fresh projection pull* — which still has no script. The Sept 5 re-check
  in §2 is still mandatory, not a formality, because ESPN appears to re-forecast in irregular
  batches rather than continuously.
- **Tank Dell (WR) still carries a pre-injury projection on the board, but he is now marked.**
  He went on IR on Aug 30, out at least four weeks (ESPN). The board shows him AVOID with the
  reason on his row, so the number is stale and the row is not. **He is not a pick; he is a
  free IR stash at 152 or 161** — the three IR slots make that cost nothing (directive §6).

---

## 9. If something breaks: the failure procedure

Every serious defect this project has found so far has been **silent** — no error message, no
warning, just a plausible-looking number. Assume the tool can fail quietly, and know the response
before you need it:

- **Tool prints nothing, or hangs** → switch to DRAFT_BOARD. Take the highest VBD player who
  fits your roster caps and doesn't stack a bye you're already carrying.
- **The pick number on screen disagrees with ESPN's** → trust ESPN. If the gap is exactly 12, the
  keeper filter has failed — use DRAFT_BOARD.
- **The engine recommends a K or D/ST before pick 152** → can no longer happen: kickers and
  defenses are not on `board_v8_fixed.csv` at all, they live in a separate streamer file the tool
  only opens at picks 152 and 161. If you somehow see one early, the tool has loaded the wrong
  board — stop and run `py check_kit.py`.
- **At 152 or 161 the streamer page offers someone already drafted** → this failed silently until
  Aug 29 (the filter needed an `ESPN_ID` column the file didn't carry). It is fixed and the filter
  is proven to fire, but it is a quiet failure mode: cross-check the top name against ESPN's room
  before you click.
- **The engine recommends a player ESPN already shows as drafted** → the feed is stale. Refresh.
  If it repeats, use DRAFT_BOARD.
- **Anything else unexpected** → take the best available player by VBD, respecting roster caps and
  byes. The board is worth roughly six times more than any pick rule — losing the rule for a pick
  or two is survivable; losing the board is not.

---

## 10. Injury tags — what the red word actually means

ESPN carries two injury fields, and the board's `flag` column uses the weaker one. In your top
180, **only three players are genuinely injured** (ESPN's own boolean `injured = True`): George
Kittle, Alec Pierce, Zach Charbonnet. Thirty-three more are tagged `QUESTIONABLE` while that same
boolean says they're healthy — McCaffrey, Nacua, Breece Hall, Jeremiyah Love, and Malik Nabers
among them. **On the live board this now renders as a small red `Q`** (hover for the full word;
`D` = doubtful, `OUT`, `IR`). **A red `Q` is a roster-status marker, not an injury. Don't flinch at
it** (doc 74).

**The flag is display-only.** It never enters `vbd`, the rollout, or any recommendation, and it's
frozen as of whenever the board was built.

**Print `INJURY_CONTEXT_SHEET.xlsx` and keep it beside the card.** Sixteen players in ADP order,
with expected games in weeks 1-14, form on return, recurrence rate, and how far each moves on your
board once that's priced in. Four rows change a pick: **Josh Jacobs, down to 89** (a possible
six-game suspension the board knows nothing about), **Kittle down to 60**, **Kraft down to 53**,
**Tyson down to 57**.

**CORRECTION, 2026-08-30 — the Mahomes row was wrongly dismissed, and this guide is what dismissed
it.** Earlier versions said the row looked fabricated and told you not to act on it. **That
instruction is retracted.** The ACL tear is real and well sourced (torn against the Chargers, late
2025), and as of Aug 20–26 Schefter and the team both have him **on track to start Week 1**. The
only live question is the sheet's 90% form haircut, not whether the injury happened. The one thing
that was genuinely unverifiable — Carson Wentz as the named hedge — has been blanked on the sheet.

The general lesson stands and is worth more than the row: **a flag saying "this might be made up"
is a claim like any other, and it has to be checked before it changes a decision.** This one was
never checked, and for two days it told you to ignore accurate information about a quarterback.

---

## 11. Off-field risk — the board has no field for it at all

The injury flag is weak (§10). For **suspensions, legal matters and holdouts there is no field
whatsoever** — not in `proj_2026`, not in `vbd`, not on the board. The only trace is ESPN's
analyst blurb, and that is not carried onto the board either.

Searching those blurbs across your top 180 turns up **exactly two**:

| ADP | player | what ESPN's own outlook says |
|---|---|---|
| **36** | **Josh Jacobs** | *"a potential suspension makes him less valuable on draft day"* — and the projection does not discount him for it. He is still the 20th-highest VBD on the board. On the injury sheet he falls **89 ranks** if the suspension holds. |
| **55** | **Quinshon Judkins** | rookie year *"bookended by missed time early because of an **off-field issue** and late because of a season-ending leg injury"* — two independent absence risks, only one of which the injury sheet prices. |

**Judkins is the quieter problem.** He reads clean on the board and appears on the injury sheet at
only ↓9, because that adjustment covers the leg injury alone. Nothing anywhere accounts for the
off-field absence repeating.

**Both are "potential", neither is confirmed. Checked 2026-08-30: Jacobs' suspension is STILL
UNRULED, and the Packers are publicly bracing for it (Schefter).** So the risk is live and, if
anything, firmer than when this was written — but there is still nothing to price against. The
Sept 5 sweep carries the same question, plus Judkins.
Until then, treat both as unpriced risk rather than as ruled out: if Jacobs' suspension evaporates
he is a legitimate RB1 at pick 36, and passing on him costs real value.

**Two limits on the search above.** It reads ESPN's blurbs, so it finds what ESPN chose to write
up — a quiet legal matter ESPN has not covered will not appear. And it ran against the Aug-20
pull, so anything that surfaced since is invisible to it. Same shape as §7's late-injury gap: the
system does not watch for this, you do.

### A third unpriced class: concussion history

The injury sheet's taxonomy is **ACL · Achilles · ankle · high-ankle · back · hamstring · knee ·
suspension**. There is **no concussion category**, and that is not an oversight in the sheet so much
as the same hole one level down. Every other class on that sheet is a *current condition* — ESPN
flags it, or a search finds it, and the sheet prices it. **Concussion risk is a property of a
player's history, not of his status today.** A player with three documented concussions who is
fully healthy right now reads as: ESPN `injured` = False, `injuryStatus` = ACTIVE, board `flag`
blank, projection undiscounted, injury sheet absent. Nothing in this system has a field for it.

**Checked for you: Tua Tagovailoa is board rank 442 of 480, VBD −206, effective ADP ~158.** He is
not a decision you will face. No other concussion-history name could be sourced inside your
draftable range, and the Sept 5 sweep now carries the question explicitly — but treat "nothing
found" as "not looked for very hard", not as "nobody qualifies".

**QBs and TEs are on the sheet** — 5 WR, 5 RB, **4 TE**, **2 QB**. Position coverage is not the gap;
the missing risk *class* is.

---

## 12. Cookies — the one manual repair you may actually need

Every script that talks to ESPN authenticates with two cookies copied out of your browser:
**`SWID`** and **`espn_s2`**. They expire. When they do, everything fails the same way —
**HTTP 401 or 403**, or the injector printing `Update Failed` — and nothing else fixes it.

**Four files carry them**, which is the part that used to be wrong in this guide (it said two):

```
Scripts\Espn_pull_projections.py
Scripts\espn_draft_injector_Gemini.py
Scripts\fetch_keepers.py
Scripts\live_draft\live_draft.py
```

### The procedure

**1. Get the values.** In Chrome, signed in at `fantasy.espn.com`:

> **F12** → **Application** tab → left sidebar **Storage → Cookies → `https://fantasy.espn.com`**
> Find the two rows and copy the **Value** column:
> - **`SWID`** — copy it *including* the curly braces: `{A7217088-1F36-…}`
> - **`espn_s2`** — long, 300+ characters, ends in `%3D%3D`

Copy both **verbatim**. Do not decode `%2F` back to `/`, do not trim, do not "clean up". The
percent-escapes are part of the value.

**2. Run the tool.**
```
cd "G:\My Drive\_Fantasy\2026\Scripts"
py set_cookies.py
```
It prints which file holds which cookie, prompts for both values, **tests them against your league
before touching anything**, then updates all four and backs up the originals to `2026\_archive\`.

**If the test fails it writes nothing and says so.** That is the whole point — four files full of
bad cookies at 7:02 PM is worse than one 401. Re-copy from Chrome and run it again.

**3. Re-run whatever failed.** Nothing else needs restarting except the live tool, if it was up.

### Two things to expect afterwards

- **`check_kit.py` will report all four files STALE.** That is correct — their bytes changed.
  Re-pin the manifest when things are calm, **not** during the 7:00 PM sequence.
- To check the cookies *without* changing anything: `py set_cookies.py --check`.

**Do this once this weekend even if nothing is broken** — `--check` costs ten seconds and tells you
whether you will be doing this under a clock.

---

## Appendix — source documents

`00_PROJECT_DIRECTIVE.md` (v5.4) · `00_CALENDAR_TO_DRAFT.md` · `00_HOW_TO_RUN_IT.md` ·
`00_HANDOVER_READ_ME_FIRST.md` · `SCRATCHPAD_INIT.txt` · `71_weekend_test_kit.md` ·
`72_ops_brief_corrections.md` · `73_injury_and_keepers_plain.md` · `74_the_flag_is_not_injury.md` ·
`75_injury_sheet_design.md` · `76_automation_plan.md` · `77_guide_corrections.md` ·
`54_live_draft_engine.md` · `47_espn_prerank_injection_contract.md` · `37_pre_draft_runbook.md` ·
`04_mock_draft_log.md` · `62_board_has_no_builder.md` · `espn_draft_injector_Gemini.py` and
`live_draft.py` (read directly, including a live Google Drive check against the actual files,
Aug 28-29).