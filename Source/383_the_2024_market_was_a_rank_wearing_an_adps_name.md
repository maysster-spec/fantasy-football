# 383. THE 2024 MARKET WAS A RANK WEARING AN ADP'S NAME, MATT HAD THE REAL ONE SINCE 19 AUGUST, AND §4.34 IS RESTATED ON IT

*22 Sept 2026, 01:20 ET. Fable, answering Matt's question on doc 382 ("What does this refer to, 'without the
2024 rank-proxy registry'? More importantly, can I fix it?"). Doc 382 is the previous number; 383 reserved
by listing the folder at 23:xx and the store.*

---

## 0. WHAT TO DO

1. **Paste directive v9.11.** One number moved and it is quoted in the resident set: the rounds-5-to-8
   riser gap is **+42 VBD14 (11 to 71, n=101)**, startable **56% against 32%**, not +52 (26 to 78) and 56%
   against 25%. The rule is unchanged. On your list.
2. **A number that must not be quoted: +52 [26, 78] from doc 382 and v9.10.** It was measured on a 2024
   market that was a consensus RANK, not an ADP. The true-ADP figure is the one above.
3. **What a "rank proxy" is, in one sentence:** a ranking is a list where every man is exactly one place
   behind the last, so the 50th name is "50" whether the room drafts him 44th or 61st; an ADP is where the
   room actually took him, averaged, with the gaps left in. The 2024 registry file was the first kind
   labelled as the second, since 26 Aug (doc 53), because that was the only 2024 board the session that
   built the registry could find.
4. **You already fixed it, on 19 August.** `sources\FantasyPros_2024_Overall_ADP_Rankings.csv` in the
   project store is a genuine 2024 preseason ADP (Yahoo, Sleeper and RTSports averaged; McCaffrey 1.0,
   Barkley 11.0, Nacua 14.7, 343 rows). The registry builder never used it. It is the 2024 registry now:
   `Source\adp_registry\preseason_adp_2024.csv` rebuilt from it, the raw file placed beside it, the
   MANIFEST and `code_adp_guard.py` say so, the proxy is in `_archive`.
5. **Seven findings were measured on the proxy and are queued for re-run, none retracted:** 4.12's noise
   refit (doc 53), 4.18b's NFL-wide arm (doc 138), 4.20 (docs 110, 141), 4.22 (docs 129, 130, 203), 4.25
   (doc 201), 4.26 (doc 229) and 4.34 (done tonight). Section 3 says why the expected movement is small.
6. **Two housekeeping items you asked about, both mine and both done:** `todo_page.py` is pinned in
   `check_kit.py` (it builds a page you read and nothing watched it); fifteen data and prompt files were
   removed from the project store, every one with a copy on the drive, to give the store room. Section 4.
7. Nothing to run.

---

## 1. WHAT WAS WRONG, MEASURED

The registry's `MANIFEST.csv` said it in its own words: *"FantasyPros-consensus-rankings 2024 :: consensus
rank (rank proxy, not ADP)"*. Doc 53 flagged it the day it was built and doc 129 flagged it again; both
judged it "correlates tightly" and moved on. Measured tonight against the true ADP on the 280 names both
files hold: **Spearman 0.949**, median difference 0.3 places, interquartile range −14 to +13, and a tail
where the proxy is a different instrument entirely. The proxy pushed quarterbacks and kickers deep (Justin
Fields 307 against 183 ADP; Russell Wilson 278 against 183; Chris Boswell 322 against 145) because a
consensus ranking orders by projected points across positions and a draft room does not.

**Where it bites this project's rules:** seven men cross the round-5 line (ADP 50) between the two files
(Amari Cooper, Anthony Richardson, George Pickens, Trey McBride, Stefon Diggs, Alvin Kamara, C.J. Stroud)
and twelve cross the round-9 line (ADP 97), among them Jayden Daniels, Jaxon Smith-Njigba, Brian Thomas
Jr., Chase Brown, Xavier Worthy and Nick Chubb. Every band-cut finding built on 2024 was drawn with those
men on the wrong side.

**The file's own provenance, stated because B7 requires it:** captured from FantasyPros' 2024 ADP archive
on 19 Aug 2026, three sites, an AVG column that is the mean of the sites present (25 men carry one site
only, mostly kickers and deep receivers, and their AVG is that single value). Team labels on the file are
2026 teams (A.J. Brown "NE", Josh Jacobs "GB"), which is how FantasyPros renders an archive page; the
numbers are 2024's, as the top of the board proves. Transcribed into the drive registry from the store
copy, and checked row by row: 343 rows, ranks 1 to 343 unbroken, and every AVG equals the mean of its site
columns to one decimal, zero exceptions.

---

## 2. JOB 4 ON THE TRUE 2024 ADP

Same script, same population definition, the registry swapped. n = 322 (was 334); 2024 contributes 90
(was 92).

| | rank proxy (doc 382) | true 2024 ADP (tonight) |
|---|---|---|
| pooled riser, per +10 share points, net of price | +6.0 (se 1.8) | **+5.7 (se 1.8)** |
| pooled gap, top third against bottom third | +18.0 [4.0, 29.4] | **+16.6 [2.6, 29.2]** |
| **rounds 5 to 8: gap net of price** | +52.1 [26.3, 78.3], n=107 | **+41.9 [11.2, 70.6], n=101** |
| rounds 5 to 8: startable, top against bottom | 56% against 25% | **56% against 32%** |
| rounds 5 to 8: price inside the band (log ADP) | +2.2 (se 30) | **−17.6 (se 31)** |
| round 9+: riser per +10 | +1.4 (se 2.0), n=227 | **+1.8 (se 2.2), n=221** |
| round 9+: gap | not resolved | **+6.5 [−8.4, 21.5]** |
| RB, all bands, per +10 | +16.4 (se 5.3) | **+16.0 (se 5.4)** |
| availability held out, per +10 | +6.6 (se 2.4) | **+6.5 (se 2.5)** |
| youth × riser | +8.5 (se 3.9) | **+6.8 (se 4.0)** |
| without "priced again in N+1", band gap | 44.8 [17.7, 72.1] | (n=105, true ADP) |
| missing window scored zero, band gap | 47.9 [21.3, 73.9] | (n=111, true ADP) |

**The verdict does not move.** Inside rounds 5 to 8 the riser's gap has a floor of 11 on the job's own
population and 18 to 21 on the two wider ones, so the falsifier's second branch (ten or more, net of
price) still holds; price inside the band is still nothing; round 9+ is still a dart. The point estimate
fell from 52 to 42 because the seven men who crossed the round-5 line were, on the proxy, on the wrong side
of a cut the rule is about. **That is the reason a rank proxy is not an ADP: it is right on average and
wrong at the lines.**

---

## 3. THE SEVEN FINDINGS BUILT ON THE PROXY, AND WHY NONE IS RETRACTED TONIGHT

§3: when a finding invalidates a metric, enumerate every downstream use. The findings file names the
preseason registry or a §1.1 ADP with 2024 in the population in: **4.12** (doc 53's five-season noise
refit; 2024's residual was one of five), **4.18b** (doc 138, the NFL-wide arm, ADP 97+ against 1 to 48),
**4.20** (docs 110 and 141, 2022 and 2024), **4.22** (docs 129, 130, 203, the availability signal, ADP as
the control), **4.25** (doc 201, the age cliff), **4.26** (doc 229, cheap against expensive hits at ADP 60,
n=135), and **4.34**.

Expected movement: small, for the reason the correlation is 0.949 and the effects are measured on
log ADP or on bands 40 places wide. Where a finding cuts at a line (4.26 at 60, 4.18b at 48 and 97) a
handful of 2024 men change sides, as they did here, and the number will move by a few points without
changing sign. **Each is NOT YET RUN on the true ADP, and each stays live until it is.** The scripts are
on the drive (`anchor_study.py`, `env_study.py`, `research\late_picks\`, `code_backtest_*`); the two that
need the 2021 nflverse weekly file cannot run in this container.

---

## 4. THE TWO HOUSEKEEPING ITEMS

**`todo_page.py` pinned.** `check_kit.py` now carries it (3,583 bytes, `bae0db33217a6a89`) in `SCRIPTS`
and the manifest. Before tonight a reverted or edited copy would have built `MY_TODO.html` with no sound,
the same gap `lineup.py` had until doc 380.

**The project store was at 98% of its 2,000,000-character knowledge limit** (1,957,862 measured at
00:30 ET; the number in Matt's screenshot). At 100% `project_write` fails and the "everything a model
reads goes to the store" rule breaks silently. Fifteen items were deleted from the store, each verified to
have a twin on the drive by name and folder before deletion: `take_contract_scores.csv` (124 KB, doc 378's
data; the doc stays), `GEMINI_HITRATE_PROMPTS.md`, `FABLE_TASKING_PROMPT_2_picks_17_32.txt`,
`FABLE_TASKING_PROMPT_4_pick32.txt`, `GEMINI_OPEN_JOBS.txt`, `constants_2026.csv`, `predicted_keepers_v5.csv`,
`backtest_2025_pickbypick.csv`, `backtest_2025_all_managers.csv`, `B1_order_changes.csv`, `J1_orderings.csv`,
`B2_live_2026_backfields.csv`, `RT2_ladder_four_ways.csv`, `RT1_summary_w14.json`, `RT3_summary.json`.
**The bulk of the store is the numbered docs**: on the drive, docs 1 to 199 are 143 files and about 1.2 MB,
all from before the draft and all in `Source\` and `_archive\`. Removing them from the store is the one
move that buys a season of room; it is Matt's call because the store is the only channel a session
without the drive bridge can read, and it is proposed in the reply, not done.

---

## 5. OPEN, BY NAME

- The seven findings above on the true 2024 ADP: NOT YET RUN, mine, one batch.
- The keeper-riser line on the week sheet (doc 382 §5): NOT YET RUN, mine.
- Doc 374 batch A, the vintage correction on the page.
- The directive read by someone with no stake in it.

Ledger row 159. Directive v9.11. `Source\adp_registry\` rebuilt; the proxy is
`_archive\preseason_adp_2024_rankproxy_20260922.csv`.
