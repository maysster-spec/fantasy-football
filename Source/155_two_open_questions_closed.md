# 155 — Two write-path questions closed, and the ladder had no channel for news

*2026-09-04 (Sept 3 evening Eastern), T-4.*

---

## 1. §8's OPEN WRITE-PATH QUESTIONS ARE ANSWERED — by Matt's `verify_prerank.py` run

```
local file : ESPN_prerank_with_ids.csv  (544 rows)
ESPN stored: 544 rows   [teams/ID mTeam -> draftStrategy.draftList]
  ORDER MATCHES exactly for all 544 positions.
  K / D-ST inside ESPN's top 250: 0
  PASS: ESPN holds exactly what the file says.
```

**(a) ESPN ACCEPTS NEGATIVE playerIds.** `[TESTED]` All 32 defenses go over the wire as
`-16000 − proTeamId` (Broncos `-16007`). §8's risk was a silent rejection that still prints
"Success!" — which `verify_prerank.py` is written to catch as *"32 short = the negative D/ST ids
were rejected."* **544 stored, not 512.** They are accepted, and the read-back proves it rather
than inferring it from a 200.

**(b) THE POST REPLACES; IT DOES NOT APPEND.** `[TESTED]` Two facts together settle it. The count
is **544, not 1,088**. And the **order matches at every one of the 544 positions** — if the write
appended, positions 1–544 would still hold the *previous* list, and the previous list was not this
one (doc 60: the pre-Aug-27 prerank had kickers at 481 and D/ST at 507, **473 of 544 rows
different**). A matching order at every position is only possible if the new list replaced the old.
**So re-injecting after the 7:00 PM keeper swap on Monday is safe and is the correct move.**

**(c) And the autodraft fallback is armed correctly.** Zero kickers or defenses inside ESPN's top
250, so if the clock ever expires, ESPN takes a skill player off Matt's VBD order — not a kicker.
This is what makes the "should the extension pick for me?" question moot: the sanctioned fallback
already exists and now provably points at the right list.

**Only §8 item 1 remains untested: `py live_draft.py --replay 2025`.**

---

## 2. THE VALUE LADDER HAD NO CHANNEL FOR A DATED FACT — and 15 of its 49 players had one

Matt asked whether the Gemini research had already reached the ladder. **It had not, for two
independent reasons, and only the first is a timing problem.**

**Timing.** `VALUE_LADDER.pdf` and `values.csv` were both built at **18:12** on Sept 3.
`player_context.csv` received the news stamp at **19:40**. The ladder is 88 minutes older than the
research.

**Structural, and the real reason.** Rebuilding it would not have helped. `values.py` reads
`player_context`'s `why` column for exactly one purpose — a regex (`EXEMPT|PUP|OUT_WEEKS|torn|
Achilles|season-ending|placed on`) that computes `opened_by`. The rendered *"why he is on this
sheet"* column is built from `opened_by` + the job label + the Boone/Harmon gap and **nothing
else**. There was no path from a dated news line to the page. Doc 153 §9 said "a finding in a CSV
nobody reads is not a finding"; this is the same defect one artifact over.

**Measured: 15 of the 49 ladder players carry a dated line, and three of them CONTRADICT the reason
the player is on the sheet.**

| player | pick | on the sheet because | the news |
|---|---|---|---|
| **Rico Dowdle** | 65 | JOB — "UNSETTLED job, worth 171 pts" | **Backup; listed behind Jaylen Warren after cutdowns** |
| **J.K. Dobbins** | 80 | ANALYSTS + JOB + BOARD | **Foot injury; Sept 2 report says it could force him to IR** |
| **Kyle Monangai** | 89 | JOB | **Hyperextended knee, week-to-week, not practising** |
| Jonathon Brooks | 80 | ANALYSTS + BUY + JOB + BOARD | soreness, questionable for Week 1 |
| Chuba Hubbard | 80 | BUY + JOB + INJURY-OPENED + BOARD | hamstring, *ahead of schedule* |
| D'Andre Swift | 32 | BUY + JOB + INJURY-OPENED + BOARD | **confirms it — workhorse to open the year** |
| Jadarian Price | 41 | JOB + INJURY-OPENED + BOARD | **confirms it — lead back after Charbonnet's PUP** |
| David Montgomery | 41 | BUY + JOB | confirms — RB1 on the updated depth chart |

Plus Tuten, Burden, Gainwell, Aaron Jones, Croskey-Merritt, Kincaid, Jordan Mason.

**SHIPPED.** `values.csv` gains a `news` column, joined on **name + position** (§3's fallback key —
`values.csv` carries no `espn_id`), and `mkvalue.py` prints it as its **own row beneath the
player**, spanning the table. A row, not a column: it cannot squeeze the ten existing columns, and
a player with no news costs nothing because the row is not emitted. The page-break estimate was
corrected to count these rows — left uncounted it under-counts by up to one row per player and the
last table on a page runs off it.

**Red team of my own change — one defect, caught by screenshotting.** `tr.nw td:before` applies to
*every* cell in the row, so "NEWS" printed twice: once in the empty gutter cell and again inside
the sentence. Reading the CSS would not have shown it. Narrowed to `td:first-child:before` — label
in the gutter, clean sentence in the body. Verified after: 15 news rows, 2 page breaks, no
duplicate label.

**Note the standing caveat is unchanged:** the ladder's `still there` is dispersion-only and §4.15
says that runs optimistic. The news rows are facts with dates; they are not scored and they do not
move VBD, exactly as §4.22's `12g` badge is surfaced and not scored.
