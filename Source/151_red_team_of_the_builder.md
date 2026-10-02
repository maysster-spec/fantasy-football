# 151 — Red team of the builder. Eleven findings, none of them able to break anything.

**2026-09-03, late.** Matt: *"please please please red team your changes… we don't want to break
a board that can't be unbroken after a certain day."*

Right instinct, and the right thing to check first. `make_board_file.py` (doc 150) was written in
one sitting, by me, hours before a draft, and it is the only thing I have ever shipped that has
the word *board* in its write path.

---

## 1. THE ONLY QUESTION THAT MATTERED: CAN IT DESTROY ANYTHING? NO.

Traced with `strace -f -e trace=openat,unlink,rename,creat,truncate`, not by reading the source:

- **Default run: zero write syscalls** outside `/proc`, `/dev`, `/sys`.
- **`--write`: exactly one** — `board_v8_REBUILT.csv`, a path built from a hardcoded constant
  that **no argument can redirect**, and never the live board.
- `--write` is gated behind the verification passing; a corrupted spine plus `--write` exits 1
  and creates nothing. Confirmed under `python3 -O` as well, so a stripped assert cannot open it.
- Two `--write` runs give an identical sha256. Misdirected `--spine` / `--live` / `--keepers` all
  abort loudly with no write. Nothing in the draft path globs `board_*`, so the REBUILT file
  cannot be picked up by accident.

**And separately verified tonight: the live board on Drive still matches `check_kit.py`'s manifest
exactly** — `board_v8_fixed.csv` (41,092 B, `ba778ceadab825e0`) and `player_context.csv`
(76,431 B, `7ae4667a7c2a95bc`). Nothing shipped today touched it.

**One real operational hazard, fixed by documentation:** the kit folder is an EXACT SET to
`check_kit.py`. A stray copy of this script — or its output — in `Scripts\live_draft\` reports
EXTRA, `check_kit` exits 1, and `draft_night.bat` aborts at step 1 of 5, at 7:00 PM. The
docstring now says in the first three lines where this file lives and where it must never go.

## 2. THE VERIFICATION WAS WEAKER THAN THE RESULT — four ways it could print REPRODUCED over a wrong board

Each was **executed**, not reasoned:

| # | the hole | what it produced |
|---|---|---|
| 3 | the news loop **failed OPEN**: `col = next(…, None)` then `if col and …`, so with no column containing "action" **every row was zeroed whatever it said** | pointing `--news` at any CSV without that column zeroed the whole board — Gibbs to rank 434 — and still exited 0 |
| 4 | a news row whose `espn_id` is not on the board matched nothing, silently | a fat-fingered id, or a keeper's id, no-opped and the run still said REPRODUCED. The one silent failure that survived the entire verification, and exactly the doc-101 class step 7 claims to prevent |
| 5 | the 12-keeper assert counted **matched spine rows**, not distinct keepers | one unresolvable keeper plus one duplicate-normalising name cancelled out: **Chris Olave — another manager's keeper — sat on the rebuilt board at rank 29** and the guard stayed quiet. The comment above it called it "LOUD, NOT SILENT" |
| 6 | the comparison checked five numeric columns and **not `player`, `team_c` or `bye`** | a rebuild carrying "Bijan Rodriguez, ZZZ, bye 1" printed REPRODUCED. `bye` is load-bearing — §4.11's BYE CHECK reads it |
| 8 | a position outside QB/RB/WR/TE was dropped in silence | an `FB` row and a lowercase `rb` row both vanished with no message |

All five are now asserts or explicit comparisons. The verifier prints `player / pos / team_c /
bye` mismatch counts on every run.

## 3. THE FINDING THAT MADE THE REPRODUCTION EXACT

**§4.1's replacement levels are published to three decimal places, and I used them as if they
were the values the board was built with. They are not.** `proj − vbd` is a constant per position
across all 480 rows with a spread of **5.7e-14** — so the true levels are recoverable exactly:

```
QB 341.602860180   RB 168.588855840   WR 163.539573570   TE 140.294884170
```

The rounding was the **entire** 4.26e-4 VBD gap, and because the four offsets differ it
*deterministically re-ordered* the four-way tie at ranks 69–72. With the exact values in:

```
vbd   max|diff| = 5.68e-14   (tol 1e-9)
rank  458 of 480 identical; 22 differ ONLY inside a vbd tie (deepest rank 322+)
```

Those 22 are all zero-projection players in the tail, hundreds of picks past 161, whose order in
the shipped board came from whatever row order the ad-hoc code happened to have. **Everything
that carries information now reproduces to floating-point identity.**

## 4. TWO HONEST WEAKNESSES LEFT IN, AND LABELLED

- **The `eff_pick` check is circular.** `adp_pick` and `gone_ahead` are *copied* off the live
  board — `refresh_adp.py` owns them — so recomputing `eff_pick` from them tests that board's own
  consistency and nothing about the rebuild. Proof: setting every spine `adp_pick` to 999 still
  gave `max|diff| = 0.00`. The banner used to claim "same eff_pick". It now says the line is
  circular, in the output, every run.
- **Tie-breaking depends on the spine's row order**, which nothing versions. Shuffling the spine
  (identical data) moves ~31 ranks, all inside the zero-projection tail. Bounded, not fixed.

## 5. AND ONE THAT WAS JUST EMBARRASSING

`--verify` was documented in the docstring **and twice in doc 150** and argparse had never heard
of it. The first command anyone would type exited 2 with no output. It is now accepted.

---

**The lesson is doc 149's, one layer up.** Doc 149 said *a remedy is a claim too*. This says the
same about a **verifier**: the reproduction was substantively true, and the thing that proved it
was weak enough that four different wrong boards would have passed. **A test that only checks
what you expected to break is a test of your imagination.**
