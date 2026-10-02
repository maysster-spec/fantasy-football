# 77 — DRAFT_DAY_GUIDE: WHAT NEEDS UPDATING

**Aug 29, 2026.** The guide is good and mostly current. Five changes, one of them urgent.
**Hand this to the scratch-pad to regenerate the PDF — it owns the layout.**

---

## URGENT — §3 CONTAINS A FACTUAL ERROR THAT WILL WASTE YOUR WEEKEND

§3A says of `--replay 2025`: *"A browser page opens and auto-refreshes as picks come in."*

**It does not.** `live_draft.py` calls `webbrowser.open()` at line 229, and the replay path
**returns at line 227**, before it. Verified by reading the file.

Consequence: Matt runs the replay, sees no browser, and concludes the test failed when it passed.

**Replace that sentence with:**
> Touches nothing real. **The browser does NOT open by itself in replay mode** — the replay path
> exits before the browser call. When it finishes, open `live_draft\live_board.html` yourself to
> see the final state. (In a real draft the browser *does* open automatically.)

---

## 2. §5 IS NOW OBSOLETE — THE 7:00 PM SEQUENCE IS SCRIPTED

The guide describes a manual runbook. Since it was written, three things were built:

| file | in | what it does |
|---|---|---|
| `fetch_keepers.py` | `...\2026\Scripts\` | reads the 12 ACTUAL keepers off ESPN and writes `actual_keepers.csv`. Refuses to write unless it finds exactly 12 |
| `draft_night.bat` | `...\2026\Scripts\` | runs the whole 7:00 PM sequence in order with a human gate at each step |
| `setup_tasks.ps1` | `...\2026\Scripts\` | registers both scheduled tasks (Sept 5 pull, Sept 7 draft night) in one run |

**Replace §5's table with:**

| time | action |
|---|---|
| 6:45 PM | Calendar alert. Be at the desk. |
| 6:55 PM | Scheduled task **FF2026 - DRAFT NIGHT** opens `draft_night.bat` by itself. It pauses at every step — you are the gate, not a spectator. |
| — | It runs: `check_kit.py` → `fetch_keepers.py --dry` (review the 12 names) → `--write` → `keeper_swap.py --check` → `--write` only if changed → injector → live board. |
| 7:55 PM | Live board is up. **Confirm the first poll line reports 12 keeper rows.** |
| 8:00 PM | Draft. Picks: 8, 17, 32, 41, 56, 65, 80, 89, 104, 113, 128, 137, 152, 161. |

**If the batch file fails at any step, every command above still runs by hand in that order.**
Say so in the guide — an automation with no documented manual fallback is a single point of failure.

---

## 3. §5's "NO REBUILD NEEDED" IS RIGHT BUT INCOMPLETE

The guide correctly says the board is static and availability comes off the live feed. **What it
misses:** if a team keeps a player nobody predicted, the player we *wrongly* predicted is genuinely
draftable but **is not on the board at all** — invisible to the engine all night.

`keeper_swap.py` closes exactly that hole, and it also means **doc 62 is out of date in the
guide's §8**: the board has a builder again — `keeper_swap.py` reproduces the shipped 480-row
board exactly from the 12 predictions.

**Add after the existing paragraph:**
> One exception. If a team keeps someone we did not predict, the player we wrongly removed is
> genuinely draftable and invisible to the engine. `keeper_swap.py` re-adds him and re-ranks —
> that is what `draft_night.bat` step 3 is for. If `--check` says IDENTICAL, all 12 predictions
> were right and there is nothing to do.

---

## 4. THE INJURY SECTION DOES NOT EXIST AND SHOULD

Nothing in the guide covers it. **Add a short §10:**

> **10. Injury tags — what the red word actually means**
>
> ESPN carries two injury fields and the board uses the weaker one. In your top 180, **only three
> players are genuinely injured** (`injured = True`): George Kittle, Alec Pierce, Zach Charbonnet.
> Thirty-three more are tagged `QUESTIONABLE` while ESPN's own boolean says they are healthy —
> McCaffrey, Nacua, Breece Hall, Jeremiyah Love, Malik Nabers among them. **A red QUESTIONABLE tag
> is a roster-status marker, not an injury. Do not flinch at it** (doc 74).
>
> The flag is display-only: it never enters `vbd`, the rollout, or any recommendation, and it is
> frozen as of the board build.
>
> Print **`INJURY_CONTEXT_SHEET.xlsx`** and keep it beside the card. Sixteen players in ADP order
> with expected games in weeks 1-14, form on return, recurrence rate, and how far each moves on
> your board once that is priced in. Four rows change a pick: **Josh Jacobs ↓89** (possible
> six-game suspension the board knows nothing about), **Kittle ↓60**, **Kraft ↓53**,
> **Tyson ↓57**. One row — **Mahomes** — is flagged as possibly fabricated research; verify before
> acting on it.

---

## 5. SMALL ONES

- **§2 timeline:** add `py fetch_keepers.py --dry` to the weekend list. It has never run, and it
  is testable now — keepers are already selected; the 7:00 PM lock only freezes them.
- **§2:** add the two scheduled tasks and note they are created by `setup_tasks.ps1`.
- **§6:** add a **Test 4** — `py fetch_keepers.py --dry`. Pass = 12 rows matching the ESPN league
  page. `0 rows` = ESPN does not expose them pre-lock, fall back to typing them. `401/403` =
  cookies stale, and finding that out today rather than at 7:02 PM is the entire point.
- **Appendix:** add docs 73, 74, 75, 76 and this one.

---

## 6. SEPARATE AND MORE IMPORTANT THAN THE GUIDE — THE TREE MOVED AGAIN

`G:\My Drive\_Fantasy\2026\` now contains **`01_START_HERE`, `02_findings`, `03_data`,
`04_source_data`, `05_code`** alongside the existing `Source\` and `Scripts\`. Some session
restructured the tree today and nothing was told about it.

`01_START_HERE\` holds `RESTART_PROMPT.md` and `ERROR_PATTERNS.md` — files the handover lists as
**traps that pre-date the red team**, now sitting in a folder whose name invites a new session to
read them first.

**Nobody should touch anything else until `py check_kit.py` is run and its STRAGGLER list is
read.** This is the fourth reorganisation in two days, and the directive's own §9 rule applies:
do not read a file map out of any document, including this one — run the checker and be told.
