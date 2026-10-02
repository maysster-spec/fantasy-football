# 144 — I tried to fix the board. Its own audit rejected it, and that is the real answer.

**2026-09-03 late · Matt: "why can't you just fix the board?" · T-4 days**

---

## The do-this list

1. **Nothing on the board.** The override card stands. I built the fix, ran it, and the board's
   own 39-check audit refused the result — details below, and it is a better reason than the one
   I gave you earlier.
2. `py parse_ladder.py` then `py mkvalue.py` — both now run with no scipy, no pdftotext, and
   from `Scripts\`. **Kyren Williams moved from your pick 32 to pick 17 on the new ADP.**
3. `refresh_proj.py` ships **quarantined** — it is the measurement that produced this finding,
   not a tool to run before Monday.

---

## 1. Matt was right that it looked fixable. He was right.

The challenge was fair, so I checked instead of repeating myself. Measured on the shipped board,
480 rows:

| | result |
|---|---|
| `vbd` = `proj_leaguepts` − §4.1 replacement | max error **0.000426** — i.e. exactly |
| `rank` = vbd rank descending | **480 of 480** rows |
| the pull's `proj_2026` vs the board's `proj_leaguepts` | **45.2%** identical to 0.1 pts, 83.8% within 5, **r = 0.9925**, median diff **0.15** |

**The board is a pure function of (projection, position).** The pull already carries the
league-scored projection — the expensive part, with §2's scoring map and §3's stat-id traps, is
done by `Espn_pull_projections.py`. So swapping projections in and re-deriving VBD and rank is
about thirty lines. **My "there is no builder" answer was wrong** — doc 62's finding is about the
SPINE, and I over-applied it to the board.

I wrote `refresh_proj.py`, the exact sibling of `refresh_adp.py`: swap the column, re-derive what
depends on it, hold the replacement levels fixed per §4.1b, re-apply `news_overrides.csv` **before**
anything derives from the projection, archive, re-pin. It ran clean. Josh Jacobs was correctly
forced back to 0.0 against a pull that wanted him at rank 93. The override card dropped from six
movers to **one — the Jacobs row that is supposed to persist.**

## 2. Then I ran `board_audit.py`, and it said no.

| | checks passed |
|---|---|
| the board as it stands today | **39 of 39** |
| after `refresh_proj.py --write` | **35 of 39** |

The four failures, and only one of them is cosmetic:

- **`projections match the spine exactly` — max diff 5.35e+01.** This is the one that matters.
  The audit merges the board against **`code_universe_v5.csv`** — the spine — and requires the
  projections to be **equal at 1e-6**, with a deliberate exemption for news overrides. Its own
  comment: *"projections must equal the spine's, not a re-derivation."*
- **`VBD = projection − replacement, every row`.** The audit does not use §4.1's constants; it
  **derives the replacement levels from the pull** and checks the identity at 1e-6.
- **`rank is 1..N with no gaps`.**
- **`prerank skill order matches board rank`** — real and expected: `ESPN_prerank_with_ids.csv`
  is ordered by VBD rank, so re-ranking desyncs the file that gets injected into ESPN.

**The board is not a free-standing artifact I am allowed to recompute. It has a provenance
contract with the spine, and 39 checks exist to enforce it.** Writing pull projections straight
onto the board is exactly the "re-derivation" that check was written to catch — someone
anticipated this move and left a tripwire on it.

**So doc 62's conclusion survives, for a sharper reason than doc 62 gave.** Not "there is no
builder." It is: **the board's projections must come from the spine, and it is the SPINE that has
no current builder.** `code_rebuild_spine_v5.py` exists and is the right layer — but rebuilding
the spine four days out, to fix six players who are all rank 90+, is doc 62 §5's rushed rebuild.

**Take Option A. The override card is the answer, and now it is the answer for a reason I can
show you rather than one I inherited.**

`refresh_proj.py` ships **quarantined in `Scripts\`, not in the kit and not pinned.** Keep it: run
against a refreshed spine after the draft, it is most of the real fix.

## 3. Three more of my own bugs, all the same mistake

`parse_ladder.py` shelled out to **`pdftotext`** — not on your machine, `WinError 2`. Same class as
the scipy import: **I used tools my container has and never checked yours did.** The PDF parse was
only ever a one-time recovery of a lost `values.csv`; that file now lives in `Scripts\`, so the
script reads it directly and only touches the PDF if it is missing.

Both scripts also used **bare filenames** — they only worked in the container that built the sheet.
The board is in `Scripts\live_draft\` and you run from `Scripts\`. Now resolved against the
script's own location, and the sheet writes to `Source\` with the other artifacts.

And **§3's merge collision caught me in my own code.** On the first run `values.csv` came from the
PDF and had no board columns; on every run after, it is the file the script itself wrote, so it
already carried `team_c` — pandas suffixed both sides to `_x`/`_y` and `v.team_c` raised. The
board-derived columns are dropped before the merge now, and I ran it twice to prove it.

**The ADP refresh moved 13 of the 49 ladder players between pick groups.** The one to know:
**Kyren Williams, adp 39 → 35 — he moves from your pick 32 to your pick 17, and his survival goes
55% → 95%.** He was one of doc 140's core five at 32; he may now be gone before you get there.

## 4. FantasyPros real-time ADP — no for the board, yes for one specific thing

**Not as a market.** §8 tested this: FantasyPros ADP is not a runtime input, nothing in the draft
path reads it, and it is a §4.4 divergence check only. More important, **§4.12's noise model
(`sd = 0.111 × ADP + 5.40`) is fitted on ESPN's ADP because your league drafts inside ESPN.**
Substituting a different market's numbers breaks the calibration that pick 8, 17 and 32 all rest
on. FantasyPros measures FantasyPros drafters; your opponents are eleven specific people in an
ESPN room.

**But there is one FantasyPros product the directive already asks for by name.** §7: *"Survival
odds: use FantasyPros **Pick Predictor** numbers when supplied."* And doc 140's own closing lists
it as the second most valuable missing input — *"FantasyPros pick-predictor survival numbers for
the core five, which would replace the simulated availability column with a measured one."*

That matters because §4.15 measured what the simulated version costs: on Josh Allen it read **74%**
where the calibrated answer was **3%**. Every "still there" number on the ladder and the live board
is a ceiling for that reason. **Pick Predictor numbers for Bowers · McBride · Kyren · Judkins ·
Lamar would replace the weakest number in the whole system.** If you can pull those five, send
them.

*(I could only fetch this page's footer, not its body — so I cannot tell you whether that URL is
the Pick Predictor or just an ADP table. The distinction above is the one that matters.)*

---

## 5. Close (§7)

**Top 3 assumptions → what would invalidate each**
1. *The spine is the right authority for projections.* It is what `board_audit.py` enforces at
   1e-6. Invalidated if the spine itself is shown stale in a way that matters — which it is, by
   construction; that is the post-draft job.
2. *Six movers, all rank 90+, is a cost worth absorbing.* Bounded, not measured (doc 62 §4 still
   stands). Re-run `py mkoverride.py` after the Sept-5 pull; if a top-40 name appears, re-open this.
3. *Holding §4.1's replacement levels fixed is right.* §4.1b's instruction. Note the audit
   disagrees — it re-derives them from the pull — so these two rules only agree while the board and
   the pull agree. Worth reconciling after the draft.

**The missing input that would most improve this:** a spine rebuild from the current pull that
reproduces `code_universe_v5.csv`'s structure, so `board_audit.py`'s spine check passes on fresh
projections. That is doc 62 Option B done at the correct layer, and it is a post-draft job.
