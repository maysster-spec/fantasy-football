# 199 — The directive gains (a2), and yes, five sheets needed reprinting

*2026-09-06, T−1. Closes the two things Matt was right about in his last message.*

---

## 0. WHAT HE ASKED, AND WHAT HAPPENED

> *"1. …'before testing what you propose, state what would have to be true for you to be right,
> and test that.' Can that be a directive by chance without muddying the waters?
> 2. '4. Nothing to run. Everything is built, verified and pinned.' you mean after all that
> discussion there are no sheets to update and reprint with those corrections and refinement we
> just discussed? That's hard to believe"*

**Both correct. Both fixed.** Point 2 was a straight error on my part: I had three files edited and
sitting uncommitted on my side of the bridge, and I read "the code is done" as "the paper is done."
That is `ERROR_PATTERNS` A-class — reporting a state I had not checked.

---

## 1. THE DIRECTIVE — §0.5(a2), and the header bumped in the same commit

`Source\00_PROJECT_DIRECTIVE.md` is now **v7.6** (109,014 bytes, sha16 `454a737b64e48564`).
v7.5 archived to `_archive\00_PROJECT_DIRECTIVE_v75_20260906.md`.

**The new rule, in one line:** before running a test on anything he proposes or I propose, write
one line naming the claim in its **testable form** — population, outcome, direction — and put it in
front of him **before** the result.

**Why it is not a duplicate of §0.2.** §0.2 catches a claim asserted *without* a test. (a2) catches
a test run against the *wrong object* — correct arithmetic, wrong question, p-value attached, which
is far harder to spot. Three instances on 2026-09-06 alone:

| his claim | what I tested | what he meant | doc |
|---|---|---|---|
| why boom/bust exists | season-to-season variance | **week-to-week** variance | 195 |
| why only three signals combine | a wider regression | **find the subgroup where they stack** | 191 |
| vacated targets must matter | the **mean** (null) | the **tail** (real: 29% do gain) | 196/198 |

**And it is one line, not a protocol.** The directive says so explicitly, because the risk of
adding a step at T−1 is that it becomes a round trip. If the claim is unambiguous, say so in the
same line and keep going.

**Placement, deliberately minimal:** the block lives in §0.5 as **(a2)**; §0.2 gets a single
cross-reference sentence and nothing else. Nothing else in the file moved.

---

## 2. THE SHEETS — he was right, five of them change

Three files were edited and never committed. They are committed now:

| file | pin (normalised bytes / sha16) | what it carries |
|---|---|---|
| `Scripts\live_draft\player_context.csv` | **107365 / `5f0b8c29e8477140`** | 2025 snap share + air-yard share on **61 of 62 live WR/TE**, plus the rewritten Burden and Odunze cards |
| `Scripts\make_tiers.py` | **13203 / `03ffb9ed8a97b53d`** | snap-share marks at top and bottom quartile on the TIER_SHEET |
| `Scripts\check_kit.py` | **21826 / `ca48d33e935ce92c`** | re-pinned for both of the above |

**Verified by re-staging after the write, not by the commit's exit code** (§0.2): all four files
hash to their intended values on his disk.

**Which printed artifacts actually change.** Checked by reading each builder, not assumed —
`player_context.csv` is read by five of them:

- **DRAFT_BOARD** (`make_board.py`) — the composite badge and the snap/target numbers **— see the correction in §5**
- **TIER_SHEET** (`make_tiers.py`) — new snap marks; Burden prints `40% snaps` in red
- **ADP_GRID** (`make_gridboard.py`) — caution marks
- **FALLBACK_BOARD** (`make_fallback.py`) — grades
- **VALUE_LADDER** (`mkvalue.py`) — the `why` column

`parse_ladder.py` does not read it directly but feeds `mkvalue`.

---

## 3. WHAT HE RUNS

```
cd "G:\My Drive\_Fantasy\2026\Scripts"
.\sept5_after.bat          <- answer N at "Write the new draft positions into the board?"
py check_kit.py
py make_shortcuts.py
```

**N, not Y, at the ADP prompt.** `refresh_adp.py --write` already re-froze the board this morning
(`board_v8_fixed.csv` and `adp_vintage.txt` both stamped 09-06). A second freeze at T−1 buys a few
hours of ADP drift and costs a re-solve of §2.1(c)'s keeper-depletion table plus an
`audit_directive.py` pass. **Verified that N does not halt the run:** `sept5_after.bat` line 40 is
`if /i "%DOADP%"=="N" goto :skipadp`, which skips the write and continues to step 2.

`check_kit.py` should come back clean. It was **stale before tonight** — it still pinned
`player_context.csv` at 90,303 bytes, two stamp-generations behind what was already on his disk, so
it would have gone red at 6:55 PM on draft night against a file that was correct. That is the
`00_START_HERE` lesson — *edit a pinned file, re-pin it in the same breath* — and I had not.

---

## 4. OPEN THREADS (§0.5e) — carrying doc 193's list plus tonight's

Unchanged and still open:

- **Pick 56's single-state margin** (`ERROR_PATTERNS` A19, §7) — the last unfixed instance
- The pick-8 margin disagreement (doc 182: 7.8 vs 19.96–20.20)
- `py fetch_keepers.py --dry` — the one genuinely untested thing in §8, and only Matt can run it
- Whether ESPN's IR slot accepts reserve/PUP, which decides Charbonnet
- Carolina's lead back
- `after_pull.bat` is a deletable stub, not yet deleted
- `ERROR_PATTERNS` F4 should be split; §4.6's "after-contact underweighted" wording needs
  correcting; doc 188 needs re-scoping as an RB-only finding

New tonight:

- **Doc-number collision: `Source\193_the_red_zone_test.md` vs the project store's
  `claude/193_weekend_injury_sweep.md`.** I checked `Source\` for the next free number and did not
  check the project store. §0.2's folder-listing rule covers one folder and there are two.
  **Post-draft: extend the rule to both, and renumber.** (`Source\` also still holds two 150s and
  two 94s.)
- **The (a2) rule has never been executed.** Per §0.2, a guard that has not fired is not a guard.
  Its first real test is the next thing either of us proposes.

---

*Written 2026-09-06. Directive v7.6. Draft is tomorrow 8:00 PM; keeper lock 7:00 PM.*

---

## 5. CORRECTION, SAME NIGHT — the board was NOT printing what §2 said it was

**Matt asked which sheets he can print. Checking that found the defect.** `note()` in
`make_board.py` does `str(r.get('why','')).split('||')[0]` — **`why` is a MULTI-SEGMENT field and
the card printed segment 0 only.** Every stamp this session appended lands in a later segment, so
**0 of 42 RB target-share numbers and 0 of 61 snap-share numbers reached the card**, while §2 of
this doc said they had. The badge fired correctly (it regexes the full field), and the TIER_SHEET
was right, so nothing looked wrong.

**This is exactly §0.5(c)5** — the check for a row that SHOULD be on the paper and is not — and it
took his question, not my verification, to fire it. I verified the file, not the artifact.

**FIXED** in `make_board.py` (30,953 / `b95d901f14e17b22`), compactly, because the badge already
says what it means and the card should carry the number:

- RB: `tgt 16.3% TOP`
- WR/TE: `snaps 88% TOP (+4) · air 38%`

Rendered and verified by extracting each player's own note row: **40 of 42** target-share segments
and **61 of 61** snap segments now print (the missing 2 are outside the 180-row cut), Burden reads
`snaps 40% BOTTOM · air 12%`, and **the board is still 8 pages.**

A second defect inside the first: my initial regex required the `(+N vs 2024)` delta, which 5 of
the 61 stamps do not carry (a rookie has no 2024 baseline) — and it dropped exactly those five,
**Burden among them**, the single most decision-relevant one. Delta is now optional.

**The red-zone segment is deliberately NOT printed.** It tested null (doc 193). Null signals do not
get board ink.

**Directive is v7.7:** §0.5(a2) gains the collision resolution Matt asked for —
`00_HANDOVER_READ_ME_FIRST.md` §7 rule 7 (*"Do not take his framing as the task... Act on intent"*)
is a real near-neighbour, is RETIRED on the drive but STILL LIVE in the project doc store, and
points the other way. Rule 7 says translate his framing; (a2) says show him the translation.
**Rule 7 without (a2) is inference with no check — which is what produced all three misses.**
