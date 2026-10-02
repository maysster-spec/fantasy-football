# 172 — **RETRACTED.** The board was never stale. I measured a stale copy of it.

**Date:** 2026-09-05 (Sat night ET) · **Retracted the same evening, before it changed a pick.**

> ## THE FINDING IN THIS DOC WAS WRONG.
> I reported that `board_v8_fixed.csv` carried **09-03** ADP while `adp_vintage.txt` claimed
> **09-05**, and called it a provenance defect. **It is not true. The board was correctly frozen on
> the 09-05 pull the whole time.** `refresh_adp.py --write` worked this morning exactly as designed.
>
> **`py check_adp_vintage.py` against the real file: `rows that DISAGREE: 0, max difference 0.00 —
> PASS`.**
>
> Matt found it by running `py refresh_adp.py` and saying *"I don't see Lloyd on the list."* He was
> right, and the reason is the honest one: **there was nothing on the list, because there was
> nothing to change.**

---

## 1. WHAT I ACTUALLY DID — THE STALE MIRROR, FOR THE THIRD TIME IN THIS PROJECT

`device_stage_files` copies a file from Matt's Drive into `/mnt/user-data/uploads/…`. **That copy
does not update itself.** I staged `board_v8_fixed.csv` early in the session — *before* Matt ran
`sept5_after.bat` at 11:20 — and then, hours later, ran every comparison against **that local copy**
while reading the freshly-staged `adp_vintage.txt` next to it.

So I compared a **pre-refresh board** against a **post-refresh stamp** and correctly found they
disagreed. Both files were real. **The pairing was fiction.**

`device_list_dir` even told me the truth and I read past it: it reported `board_v8_fixed.csv` at
**41,573 bytes**, and the fresh stage tonight returns **41,581**. Eight bytes. I had the evidence in
hand and did not check the one thing that would have caught it — **re-stage before you compare.**

**This is the same defect this project has already paid for twice, in its most seductive form.**
The previous two were *writes* from a stale mirror, which destroy work and get noticed. This was a
*read*, which produces a confident, well-evidenced, entirely false finding — and I wrote 5 KB of
analysis, shipped a tool, and put it in front of Matt at T−2.

**THE RULE, and it belongs in `ERROR_PATTERNS` as a C-class pattern:**
**A staged file is a SNAPSHOT WITH A TIMESTAMP, not a live view. Before any comparison that could
produce a finding, re-stage every file in the comparison IN THE SAME CALL, or the mismatch you find
may be between two moments rather than two files.** Mixing one fresh file with one old one is
strictly worse than using two old ones.

## 2. WHAT SURVIVES

**The tool is good and it stays.** `check_adp_vintage.py` does exactly what it should: it compares
the numbers rather than trusting the stamp. Its negative control was real — it FAILS on a board
whose ADP does not match its stamp and PASSES when it does. It has now been run against the true
board and passes. **Keep it; it is the check that would have caught me in one command.** The
reasoning behind it also stands on its own: *the artifact that records what happened is not
evidence that it happened.* That principle was sound; I just applied it to a phantom.

**The Green Bay research is unaffected** — it came from the web and the pull, not the board:

- **Kaleb Johnson was traded PIT → GB on Aug 30** `[SOURCED: Yahoo Sports]`, and **our board still
  lists him as PIT.** Rank 423, deep in §4.14's sentinel, so it moves no pick — but it is real and
  it is recorded.
- **ESPN priced a committee, not a succession:** Lloyd 78.2 → **124.4**, Chris Brooks 30.1 → **61.2**.
  124.4 is still **below** RB30's 168.589, so Lloyd's true VOR is **−44**, not −90 and not positive.
- Depth chart: Jacobs (exempt) → Lloyd "primary option for early-season production" → Brooks
  (special teams) → Johnson. Lloyd is "recovering from two years of injuries."

**And Matt's ADP instinct was right, just already fixed:** Lloyd's board ADP **is** 111.86 and his
`eff_pick` **is 99.86**. **He is a pick-89 decision, not a pick-104 one.** That conclusion is
unchanged — it simply came from the board being correct, not from me correcting it.

## 3. WHY LLOYD IS NOT IN `refresh_adp.py`'s MOVER LIST — the real answer, and a live caveat

Nothing is, today: the board already matches the pull, so the dry run reports zero movers.

**But there is a genuine limitation worth keeping.** The report is built from `top = d[d['rank'] <=
161]` — it only ever shows movers inside the top 161 **by the board's own rank**. Lloyd's rank is
**184** because of the stale *projection* (his true rank is 131). So on a day when his ADP *did*
move, he would still have been invisible in that report, filtered out by a rank that is itself
wrong. `[NOT a defect I have measured a cost for — on 09-05 the largest move outside the top 161
was Jacobs at 9.85 picks, and he is rank 435 and news-zeroed anyway.]` Recorded, not patched: it is
T−2 and `refresh_adp.py` is pinned.

## 4. WHAT THIS COSTS

Nothing was written to the board, the engine or any draft-path file on the strength of the false
finding. `check_adp_vintage.py` is a new, unpinned, standalone file. **Doc 173's Ladder A survives
intact except its A6 row** — the projection, team, position, injury-flag and missing-player checks
never touched the ADP column and were run against data that was not stale in the relevant way.
A6 now reads: **ADP is correct and verified.**

**The cost was Matt's attention at T−2, which is the resource this project is least able to spare.**
