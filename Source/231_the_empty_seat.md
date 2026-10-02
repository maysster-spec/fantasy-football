# 231 — THE EMPTY SEAT: KAM'S READ CONFIRMED, AND THE COST LANDED ON US

*2026-09-08. Matt: "Wilson kam I know for sure leaves empty spots, maybe to save on waivers, dunno."*
*The observation is right and it is exactly him. The mechanism does not work in this league. And the
mechanism that DOES work has been costing Matt claims, not Kam.*

---

## 1. THE LIST

1. **KEEP ONE ROSTER SPOT OPEN.** Twenty-four waiver claims in four seasons died league-wide because
   the roster was full. **Ten of them were ours** — two in 2024, eight in 2025, across five separate
   weeks.
   **[CORRECTED 2026-09-08, same day, by Matt: *"my strategy was to hold the player I had since he
   had standalone value and if I miss the waiver pickup. if I do miss on waivers then I can keep."*
   That is a HEDGE, and it is not what this row measured.** The ten roster-full failures all carried
   NO drop, and **in four of the five weeks a seat DID open from another claim of his** — so the
   design was sound and only the timing missed. Seven of the ten were quarterbacks and defences he
   can replace off the wire anyway. **The habit reading was too harsh: the live residue is 2025
   week 10, where eight claims ran, one executed, no seat opened at all, and three quarterback
   claims died together.** Keep the seat open when a no-drop claim is for somebody he actually
   wants; otherwise this is a cheap option that costs nothing when it misses.]
2. **The damage so far was mostly cheap, and that is luck rather than design.** Seven of the ten
   were quarterbacks or defences — the two positions we have measured as replaceable. Two were
   receivers. The claim this will eventually eat is a running back, which is the one the wire
   cannot replace.
3. **A read that is now confirmed:** Kam leaves seats empty deliberately. §5's "low churn" line is
   right and can be sharpened — he is the only manager in five drafts to come out short, and he did
   it three years running.
4. **A mechanism to stop repeating:** "to save on waivers" cannot be the reason. This league is
   standard priority, not FAAB — there is no budget to save, and priority is spent by WINNING a
   claim, not by having to drop somebody.
5. Nothing to run for this one.

---

## 2. THE OBSERVATION — CONFIRMED, AND IT IS ONLY HIM

**POPULATION: all 900 draft rows, 2021–2025, `draft_history_2021_2025.csv`.**

| season | managers drafting fewer than 15 |
|---|---|
| 2021 | none |
| **2022** | **Wilson Kam — 13** |
| **2023** | **Wilson Kam — 13** |
| **2024** | **Wilson Kam — 13** |
| 2025 | none |

`[TESTED]` Nobody else, in any season. And in **2024 he was the only manager in five years to draft
no kicker at all** — the year he won the league. **n=1, and season luck is 6× draft luck (§4.13), so
that is an observation and not a mechanism.** In 2022 and 2023 he still took both a kicker and a
defence and simply drafted two fewer skill players.

**His transaction volume is consistent with it and modest, not extreme:** executed adds against the
field median, 19 v 24.5 · 16 v 22 · 20 v 24 · 18 v 25. Below the middle every year, never lowest.

## 3. THE MECHANISM MATT GUESSED — WRONG HERE, FOR A RULE REASON

*"maybe to save on waivers."* §2: **standard waiver order, resets weekly to inverse standings, NOT
FAAB.** There is no budget. And an open seat does not preserve priority either — under this format
priority is consumed when a claim SUCCEEDS, whatever the roster looked like.

**What an empty seat actually buys is optionality: you can add without cutting somebody you would
rather keep.** Real, but it is not a waiver saving.

## 4. THE MECHANISM THAT DOES BITE, AND IT IS OURS

ESPN records a claim that fails for want of room as `FAILED_ROSTERLIMIT`. **Twenty-four across four
seasons, league-wide. Ten are Matt's.**

| season | week | claim that never happened |
|---|---|---|
| 2024 | 9 | Patriots D/ST · Xavier Legette |
| 2025 | 2 | Darnell Mooney · Rams D/ST |
| 2025 | 4 | Marcus Mariota · Jaxson Dart |
| 2025 | 5 | Sam Darnold |
| 2025 | 10 | Justin Fields · Mac Jones · Marcus Mariota |

`[TESTED, n=24 league-wide]` **Five distinct weeks, two seasons — a standing habit.** Seven of the
ten are QB or D/ST, so most of what it cost was small by our own measurements. **The exposure is
that the same full bench blocks the running-back claim, and §4.19 says that is the hole the wire
cannot patch by any other route.**

**It also joins up with two things measured today.** 41% of his waiver claims go to a defence
(doc 230 §5), and he carries a fuller bench than the room. Holding one defence through a soft run
instead of shopping weekly frees the claims AND relieves the seat pressure at the same time.

## 5. STILL OPEN

Whether Kam's seats are empty *mid-season* as well as at the draft — the draft only shows how he
starts. `lineups.py` reports each team's roster week by week and answers it directly. `[OPEN — one
command away]`

---

## 6. THE OTHER HALF OF THIS DOC WAS ALSO TOO HARSH — AND THE TEST IS 31 FOR 31

*Added 2026-09-08 after Matt explained the design. This belongs here because a sister finding, sent
to him in chat and briefly PRINTED ON THE WEEKLY SHEET, called his repeated-drop claims a typing
error.*

**HIS CLAIM, IN TESTABLE FORM:** if naming the same man to drop on several claims is a deliberate
hedge — *give this man up, but only if one of these lands* — then every `FAILED_PLAYERALREADYDROPPED`
row of his should sit in the SAME WEEK as a successful claim of his that dropped that same man.

**POPULATION: his executed and failed transactions, 2024 + 2025, `waiver_report_*.csv`. n = 31.**

**RESULT: 31 of 31. Zero orphans.** `[TESTED]` Every single one landed in a week where one of his
claims succeeded and took that seat. **The hedge did exactly what it is for, every time, for two
seasons. Nothing to change and nothing was lost.**

**WHAT I HAD WRITTEN, AND IT IS RETRACTED:** *"31 died because two claims named the same man to
drop… every claim needs its OWN distinct drop."* **Wrong.** Giving each claim its own distinct drop
would force him to give up several players to land one, which is the opposite of what he wants.
The sheet has been corrected; the wrong text was live for roughly twenty minutes.

**THE PATTERN THIS MAKES, AND IT IS THE SECOND TIME TODAY (`ERROR_PATTERNS` F4).** A process of his
that looks like an error from the transaction log is a design whose intent the log does not record.
Doc 230 §2 was the same shape: his objection to the defence measurement was right about the
direction and wrong about the mechanism, and testing it produced a better answer than either of us
started with. **The rule that failed here is §0.5(a2) — I should have written down what would have
to be true for "these are mistakes" BEFORE putting it on his sheet.** A failure code is not an
intent, and I read one as the other.
