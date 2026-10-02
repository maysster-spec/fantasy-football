# 180 — The correction needed correcting, and the auditor disagreed with the doc it audits

**2026-09-05 (T−2), Matt at the gym and unable to run anything.** Everything here is
research and file edits — no command he has to run for any of it to be true.

---

## 1. The keeper red team: all twelve predicted keepers are clean. That is a NULL and it matters.

`predicted_keepers_v5.csv` was solved around Aug 21 and **drives §2.1(c)'s entire depletion
table**, which drives every "who is available at my pick" number in the project. Two weeks is long
enough for a keeper to break, get suspended, or lose a job — and a changed keeper changes the pool,
the table, and the board.

Checked all twelve against September reporting, with particular attention to **suspensions and the
Commissioner's Exempt List**, which is the event class an injury search misses and the one that
already cost this project a player (Josh Jacobs).

**Result: no keeper-changing event on any of the twelve.** `[TESTED, 12 of 12]`
- **Rashee Rice** — knee recovery on schedule, full practice Aug 18. The 2025 suspension is
  served; the NFL closed its personal-conduct investigation with no violation found. Rapoport,
  Aug 12: *"I don't expect... anything new there disciplinary-wise."* A civil suit is pending and
  is not a league matter.
- **Zay Flowers** — the only amber. Quad contusion, in and out of practice for a month, first
  practice in two weeks on Sept 3. Matt Zenitz, Sept 1: *"the full expectation is that he'll be
  good to go for Week 1."* Not a reason to change a keeper.
- **Chris Olave** — situation **improved**: Jordyn Tyson, his rookie target competition, is on IR
  for ~two months (doc 177). More targets, not fewer.
- **Javonte Williams** — Dallas, and **more** secure since cutdown: Jaydon Blue was waived.
- **Cam Skattebo** — cleared, named the Giants' clear lead back (Sept 3). Revealed he considered
  retiring during rehab; backstory, not a playing risk.
- **Rhamondre Stevenson** — Patriots.com's 53-man breakdown lists the room *"Stevenson, Henderson,
  Kiner."* **This closes doc 177's OPEN item: Stevenson has the job; Henderson is the rotational
  piece.** The market disagrees with the team — Henderson goes ahead of Stevenson in ADP — but that
  is a market split, not a reporting one.
- **Stefon Diggs** — Washington, not New England. Acquitted on all counts May 5, 2026; the NFL took
  no personal-conduct action. **Our pull already has him as WSH**, so nothing downstream is wrong.
  His ADP has moved 130.8 → 101.9 since the prediction, which is the largest keeper ADP move of the
  twelve and is already absorbed by the 09-05 re-solve.
- **Rice, Pickens, McMillan, Loveland, Maye, Etienne** — clean, no injury designation, roles secure.
  Two fabricated "suspended indefinitely" social posts (Pickens, Maye) were found and **discarded** —
  no reputable outlet carries either, and both contradict same-week reporting.

**§2.1(c) re-checked on the 09-05 freeze: all fourteen picks pass, 28 of 28 assertions.**

---

## 2. `audit_directive.py` disagreed with the directive — and it was the auditor that was stale

Ran it: **49 ok, 2 FAIL.** Both failures were §4.14's sentinel counts, off by one against the
09-05 board (327→**328** inside the blob, 153→**152** with a genuine ADP).

Fixed the directive. **Re-ran. Still 2 FAIL.** The two expectations were **hardcoded constants
inside the checker**, hand-copied from the doc — so correcting the doc made the doc and its own
auditor disagree, and the audit kept saying FAIL against a now-correct file.

That is the **one-number-in-two-places defect the naming rule exists to prevent, living inside the
tool built to catch it.** The script's own docstring says *"Nothing here is read off the doc"* —
true of the measurements, false of the expectations.

**Fixed properly:** §4.14's two numbers are now **parsed out of the directive**, with a fallback to
the constants that **prints a loud warning** if the wording moves. Both negative controls run
first, per §0.2: directive missing → warns and falls back; wording changed → warns and falls back.
**Now 51 ok, 0 FAIL.**

---

## 3. Doc 176's §4.7/§5 audit was wrong in three ways. I wrote it this morning.

Doc 176 reported *"two claims are wrong"* — that §4.7's TE-before-round-3 count was **3× understated**
and that §5's herman-allen line was **FALSE**. Re-derived from `draft_history_2021_2025.csv`:

**(1) Wrong convention — `ERROR_PATTERNS` A14.** It counted TE picks in **rounds 1–3** and reported
them against a directive claim about **before round 3**, which is rounds 1–2.

**(2) It counted KEEPERS as draft selections.** In **2021–2023 the keeper was charged to round 1**
(2024–25 moved it to round 15). So every "round 1 TE" in those years is a keeper, and §4.7's stated
population is *"true draft selections only, keepers excluded."* Doc 176's "2021 Buffalow r1 Kelce"
and "2023 Pierce r1 Kelce" are keeper rows — and not even the right players: those slots hold
Andrews, Knox and Schultz.

**(3) Two rows it listed are not in the file — `ERROR_PATTERNS` B5.** "2021 Brown/Collins r3 Waller"
and "2023 Wilson Kam r3 Andrews" do not exist. There are exactly **nine** TE picks in rounds 1–3
across all five seasons, and neither is among them.

**The complete, correct list — every TE selected in rounds 1–3, keepers excluded, 2021–2025:**

| year | manager | rd | overall | player |
|---|---|---|---|---|
| 2021 | *(unattributable — see below)* | 2 | 22 | Kelce |
| 2021 | Wilson Kam | 3 | 35 | Kittle |
| 2022 | **Cary** | 3 | **30** | Kelce |
| 2023 | Pierce *(departed)* | 2 | 20 | Kelce |
| 2025 | **herman allen** | 2 | **22** | Bowers |
| 2025 | *Matt Mays* | 3 | 35 | Kittle |

**2021 cannot be attributed at all.** Six of that season's twelve `Manager` values are TEAM names,
not people. Every manager-level statement is therefore 2022–2025 only. §3's identity rule, showing
up in the history file rather than the board.

**§5's line SURVIVES.** On rounds 1–2, herman allen is the only *current* manager who has ever done
it — the other two instances are a departed manager and an unattributable row. **Doc 176's
retraction was wrong; the directive keeps the line.**

**§4.7's number does NOT survive.** "1 of 43 team-seasons" is not reproducible under any convention
I can construct on this file. Replaced with **2 of 48 manager-seasons (2022–2025)**, with the
convention and the 2021 attribution gap stated.

---

## 4. But the concern under doc 176 was right, and this is the version that decides pick 32

**Matt's pick 32 is round 3.** The round-1–2 framing is the wrong lens for his decision. First TE
by **overall pick**, true selections, 2022–2025, n=45:

**3 of 45 at overall ≤32. 6 of 45 at ≤41.**

The picks between Matt's 17 and his 32 belong to **Wilson Kam (19, 30) · herman allen (20, 29) ·
Cary (24, 25)**. Of those three: **allen has gone TE at overall 22, Cary at overall 30.** Kam's
earliest is 35. **Brown/Collins is NOT a threat — earliest first-TE is overall 45**, contrary to
doc 176. Rychlicki is out regardless: Loveland is his keeper, so he cannot keep a TE and draft one
early.

**Two of the three managers holding the six picks before Matt's 32 have taken a TE at or before
overall 30.** Weaker than doc 176 claimed, and real.

**What it changes:** nothing about §7's rule, which is *any of the five, first one showing*. It
changes the **prior on which one shows** — treat Bowers or McBride surviving to 32 as materially
less likely than "one early-TE manager in the league" implies, and take one **on sight** if it does
survive rather than deliberating. **It is not a reason to reach at 17.**

---

## 5. `ERROR_PATTERNS` gains B7

**B7 · A retrieved source used without reading its publication date.** Nine instances on Sept 5
across three independent pipelines, one of which had already **shipped onto a player card** and was
driving an AVOID grade that suppressed the very analyst calls that would have corrected it
(J.K. Dobbins, from an ESPN article dated **2025-11-15**). The rule is one line — *state a
retrieved source's publication date before using it; if the date cannot be established, or comes
back implausible for the content, find another source* — and the place to enforce it is **inside
the fetch prompt**, because the model answering a fetch will supply the date if asked and will
never volunteer it if not.

---

## 6. Shipped, and none of it needs a command

- `00_PROJECT_DIRECTIVE.md` — §4.7 count corrected, §4.14's two sentinel counts corrected, §5's
  herman-allen line reworded with the full early-TE table added under the manager table.
- `Scripts\research\audit_directive.py` — §4.14's expectations now parsed from the directive, with
  a loud fallback. **51 ok, 0 FAIL.**
- `176_tendencies_and_my_guys.md` — PART 3 replaced with the re-derivation and a correction notice.
- `ERROR_PATTERNS.md` — B7 added.
- Pre-edit copies of all four archived to `_archive\` with today's date.

## 7. Standing

`[TESTED]` — 12 of 12 keepers; §2.1(c) 28 of 28; audit 51 of 51; the early-TE table on n=60.
`[CORRECTED]` — doc 176's §4.7/§5 audit (three defects, all mine, found by re-deriving rather than
re-reading); §4.14's counts; the auditor's hardcoded expectations.
`[OPEN]` — 2021's manager identities are unrecoverable from this file; any manager-level history
claim must say "2022–2025."
