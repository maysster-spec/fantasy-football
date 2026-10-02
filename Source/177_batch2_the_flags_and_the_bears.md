# 177 — Batch 2: the 23 stale flags, verified one at a time

**2026-09-05, Saturday night (T−2).** Batch 2 of the red-team sweep Matt called for after the
MarShawn Lloyd miss: *"If you see one roach there could easily be 100."*

Scope set in the prior turn and unchanged: the **23 rows inside the printed 180 whose board flag
disagrees with ESPN's own 09-05 feed**, worked in pick order, each one confirmed against a
**primary report with its date read out loud** before it was used.

---

## 0. The two near-misses, recorded first

Both were caught only because the fetch prompt demanded the publication date.

- A CBS piece, *"NFL Week 1 injury report: Ja'Marr Chase limited in return to practice"* — dated
  **September 4, 2024.** Two years old. Not cited.
- An SI item, *"Eagles Wednesday practice report: DeVonta Smith absent again"* — dated
  **November 26, 2025**, and about a shoulder, not the hamstring. Not cited.

`ERROR_PATTERNS`: a search engine ranks by relevance, not recency, and a fantasy injury headline
is nearly year-agnostic in its wording. **Every fetch in this batch asked for the date first.**

---

## 1. What actually changed — four rows, and only four

| player | board said | truth on 09-05 | source |
|---|---|---|---|
| **Alec Pierce** (adp 107.8, rank 79) | **OUT** | Ankle. **Practiced Tue Sept 1.** GM Chris Ballard on Week 1: *"That's the plan."* | NBC Sports 09-01; Yahoo/Ballard 09-01 |
| **Isiah Pacheco** (adp 161.6, rank 143) | QUESTIONABLE | **On IR since Sept 1** (back). Min. four games. Lions only *"hope"* he returns this season. | ESPN 09-01; Detroit News 09-02 |
| **Tank Dell** (adp 164.8, rank 121) | QUESTIONABLE | **IR, designated for return** (Aug 30). Min. four games, can come back. | 4for4 08-30 |
| **Jordyn Tyson** (adp 168.1, rank 174) | DOUBTFUL | **On IR** (Saints). Garafolo/Rapoport: **~two months**, hamstring. | NFL.com |

**Pierce is the one that could have cost a pick.** `live_draft.py:875` *silences* a player's
analyst up-calls when his flag is `OUT` or `INJURY_RESERVE`. Pierce sat at rank 79 with a false
OUT, one pick-104 neighbourhood away, with his calls suppressed — a live receiver made invisible
by a stale sweep verdict, exactly the Lloyd failure mode in a different column.

**FIXED, in the file, four cells:** `board_v8_fixed.csv` flags set to what ESPN's own 09-05 feed
says — Pacheco / Dell / Tyson → `INJURY_RESERVE`, Pierce → blank. Nothing else in the file was
touched (`diff` shows exactly four lines). `check_kit.py` re-pinned to `41107 / 9edc35badec8e2d7`.
On the live board those three now paint the grey **IR** mark (`live_draft.py:843`) instead of
`Q`/`D`, and Pierce's calls come back.

---

## 2. The fix I nearly shipped, and the test that killed it

The obvious move was `refresh_flags.py`: rewrite the whole `flag` column from the newest pull. It
touches no projection, so `board_audit.py`'s 1e-6 spine equality is safe. I wrote the plan.

Then I ran the check §0.2 demands **before** writing it: does `flag` currently equal the 08-30
pull's `injuryStatus`?

**435 of 480. It disagrees on 45 rows — against the pull the board was built from.**

`flag` is **not** ESPN's feed. It is the **injury sweep's verdict** (docs 112/115), hand-curated
with beat-writer detail ESPN's four-value enum cannot carry. Overwriting it from the pull would
have deleted the better information on 45 rows to fix 23. **A diagnosis is a claim; this one was
wrong, and one query killed it before the fix existed.**

Hence the four-row cut instead: **ESPN's IR placement is a roster fact, not an opinion**, and
Pierce's OUT is demonstrably false. The other nineteen are the sweep's judgement against ESPN's
coarse enum, and the sweep is the better witness. They are left alone; their nuance is going onto
the cards instead (§4).

---

## 3. The second roach Matt predicted — and it is a Bear

**Kyle Monangai (RB, CHI, adp 123.9, board rank 76, VOR −5.3).**
Right knee **hyperextension**, Aug 16. Ben Johnson on **Sept 1**: still **"week-to-week,"** minimal
progress despite the knee being structurally sound, **Week 1 in serious question.**
ESPN's feed says QUESTIONABLE. **ESPN's projection does not: 162.2 on 09-05 against 163.3 on the
board — a 1.1-point move.** The market has not moved either (adp unchanged).

That is the Lloyd shape exactly: **a job-status fact the projection has not priced.** Monangai
was a doc 176 dart candidate — `UNSETTLED`, job worth 196. **He comes off the dart list.**

Two consequences, both already in the file:
- **D'Andre Swift is the clear lead back to open the year.** He left practice Sept 3; Schefter
  reported **cramping only**. `player_context` already carried the 09-03 starter note.
- **Roschon Johnson is next up — and ESPN has NO projection for him at all** (`proj_2026` = NaN,
  adp 169.97, 1.5% owned). He is unrosterable on this board by construction, and a NaN projection
  is the one input doc 139 warns can break `_lineup()`'s pure-Python equivalence. Not a draft
  target; recorded so nobody is surprised by his absence.

---

## 4. Everything else: no change, and here is why that is worth writing down

Verified ACTIVE-or-better, no pick moves:

- **Quinshon Judkins** (pick-32 tie member) — the ankle was **precautionary**, not a setback.
  Todd Monken, Aug 20: *"out of precaution, I think it was smart with where he was at."* ESPN
  ACTIVE. **Doc 176's pick-32 read holds.**
- **Ja'Marr Chase** (rank 6) — left knee, landed awkwardly Sept 1, sat a day, limited since.
  Zac Taylor *"feels good about where Chase is right now."* ESPN's QUESTIONABLE is the accurate
  one here; the board's blank is the stale one. No pick-8 implication (§4.2/§4.10 close pick 8 on
  St. Brown regardless).
- **Rome Odunze** (adp 65.4, live at Matt's pick 65) — left practice Sept 3, right leg. Dan
  Wiederer, The Athletic: *"Preliminary indications are that Bears WR Rome Odunze should be all
  good."* **Scare, not an injury.** He still carries the §4.22(c) `12g` badge; that is unchanged
  and remains the real reason for caution.
- **Tee Higgins** — heel contusion, DNP Wed Sept 3, *"did run up the hill"* (Ben Baby). Expected
  for the opener.
- **TreVeyon Henderson** (adp 77.3) — right ankle, slipped Aug 27. **DNP Sept 1 AND Sept 3.** A
  league source says he should be good; he has not practised since. Sources also **disagree on
  the depth chart** (985 The Sports Hub has him RB2 behind Stevenson; SI has Stevenson the
  backup) — flagged as contested per doc 166's two-report rule, not resolved. Matt already had no
  appetite here; nothing in this batch argues against him.
- **Carnell Tate** (TEN, not CHI) — Aug 19 concussion cleared; DNP Sept 1, Saleh: *"working out
  some stiffness."*
- **Bhayshul Tuten** — the QUESTIONABLE is an **illness**, sent home Sept 2. Still co-starter with
  Chris Rodriguez Jr.
- **DeVonta Smith**, **Parker Washington**, **Xavier Worthy**, **Quentin Johnston**, **Makai
  Lemon**, **Cade Otton** — the board's QUESTIONABLE is stale-pessimistic; ESPN has all six ACTIVE
  and no September report contradicts it.

**All fifteen verified facts are now dated, sourced and on the player cards**:
`Source\redteam_batch2.csv` → `apply_research.py`, which prepends `NEWS 09-05:` to `why` and
refuses to write if any other column moves. **Dry-run against the real
`player_context.csv`: 15 rows updated, 0 unmatched.**

---

## 5. The Rhamondre Stevenson false alarm — caught before it was reported

Stevenson is **absent from a 480-row board** while being a real RB with adp 78. I had the finding
half-written. He is **Ray's predicted keeper** (`predicted_keepers_v5.csv`, Sentinel Sea
Stallions) and §2.1(d) removes all twelve keepers before pick 1. **Correct behaviour, not a
defect.** Same check on Sione Vaki and Corey Kiner: in the pull, adp ≈170, ~0% owned, nothing.

That is twice in two days that "a name is missing from the board" turned out to have a boring
correct explanation, and once (Lloyd) that it did not. **The check is cheap; run it every time.**

---

## 6. Matt's other question: has the VOR moved for anyone else, like it did for Lloyd?

Measured, not reasoned. Board `proj_leaguepts` against the **09-05** pull, all 180 printed rows:

**Exactly three rows differ by 15+ points, and all three are already on `OVERRIDE_CARD.pdf`** —
Kyler Murray **+37.9**, De'Zhaun Stribling **+25.1**, Isiah Pacheco **−48.3**. The override card
is doing its job. The two that are *invisible* are **Lloyd (rank 184)** and **Kayshon Boutte
(188)**, both past the 180-row print cut — which is the paper defect already logged, not a new one.

**So: no second Lloyd on the projection side.** The second roach was on the *status* side
(Monangai, Pierce), which is a different column and a different pipeline.

---

## 7. Also found, and fixed while I was in there

`check_kit.py` was pinning `board_v8_fixed.csv` at **41092 / ba778cea…** while the shipping file
was **41100 / c38cb1a6…** — `refresh_adp.py --write` rewrote its ADP columns this morning at 11:20
and nothing re-pinned it. The checker would have shown **STALE on the board** at 6:55 PM Monday
for an entirely benign reason, which is the cry-wolf failure the checker exists to avoid. Re-pinned
to the post-edit bytes. The pin method was proved first by recomputing two pins that already match
(`live_draft.py`, `board_audit.py`) — both exact.

---

## 8. What Matt runs

```
cd "G:\My Drive\_Fantasy\2026\Scripts"
py apply_research.py --findings ..\Source\redteam_batch2.csv --write
py check_kit.py
```
Then rebuild the paper so the printed board carries the IR marks and the new card lines
(`make_board` → `mkvalue` → `to_pdf` → `sync_desk_copies`, i.e. the tail of `sept5_after.bat`).

**Already done for him, in the files:** the four flag cells, the `check_kit` re-pin, the findings
CSV, and the pre-edit board archived to `_archive\board_v8_fixed_20260905.csv`.

---

## 9. Standing

`[TESTED]` — 4 flag corrections, each against a dated primary report.
`[TESTED]` — flag ≠ pull on 45/480 rows, which is why the column-wide rewrite was abandoned.
`[TESTED]` — 3/180 rows with 15+ projection drift, all already on the override card.
`[SOURCED]` — 15 dated facts, publication date read on every one.
`[OPEN]` — Henderson's depth-chart position: two outlets, two answers, unresolved.
