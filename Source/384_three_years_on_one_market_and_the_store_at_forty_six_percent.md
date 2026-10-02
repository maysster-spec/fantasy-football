# 384. THREE OF THE FIVE REGISTRY YEARS ARE ON ONE MARKET NOW, THE RISER HOLDS ON IT, THE YOUTH LINE DOES NOT, AND THE STORE IS AT 46%

*22 Sept 2026, 06:30 ET. Fable, on Matt's three instructions of 23:30: "YES please do the house keeping", "bifurcating
the pre-draft data is fine, unless too intertwined", and "historical adp can be found here as well correct? ... other
years same method i presume." Doc 383 is the previous number; 384 reserved by listing `Source\` at 05:50.*

---

## 0. WHAT TO DO

1. **Paste directive v9.12.** Three things in the resident set moved: the rounds-5-to-8 riser gap is **+51 VBD14
   (19 to 73, n=100)** with all three JOB 4 years on one market; the "young riser is worth about three times an older
   one" line is **struck**; and a store-capacity trigger is in the milestone table. The rule is unchanged. On your list.
2. **Download two FantasyPros pages the way you did 2024** (the Export button, logged in) and drop them in the 2026
   folder: `half-point-ppr-overall.php?year=2021` and `?year=2025`. Your Chrome gave me 2022 and 2023 tonight before it
   disconnected; my own browser is shown a five-row preview because it is not logged in. On your list with the URLs.
3. **Numbers that must not be quoted any more:** "+42 (11 to 71)" from v9.11 and doc 383, "+52 (26 to 78)" from
   v9.10 and doc 382, "youth amplifies (interaction +8.5, se 3.9)", and doc 383's "removing docs 1 to 199 buys a
   season of room". Section 3 has the replacement for each.
4. **Answer to your ADP question: yes, and it is the better instrument.** The FantasyPros archive page with `?year=`
   serves the preseason ADP for any past season, from the same three sites for every year (Yahoo, Sleeper, RTSports;
   2022 has no RTSports column). 2022, 2023 and 2024 are on it now. **2021's registry file was a rank in disguise
   (its values are exactly 1 to 200 with no gaps, the doc 383 defect a second time) and 2025's is a nine-site ADP
   rounded to whole picks;** both wait on item 2.
5. **The store is at 927,293 of 2,000,000 (46%), from 98% at 00:30.** 200 items moved to the drive, every one
   hash-verified before it left. **That is about five weeks at the season's writing pace, not a season**, so the
   trigger in item 1 exists.
6. Nothing else to run.

---

## 1. THE STORE, MEASURED

**What was removed, in two batches.** First, the 153 numbered docs 1 to 199 that were in the store (doc 383 said
143; the store held ten more than the drive's `Source\` did, all pre-draft). Second, 47 pre-draft items: the six
`sources\` and `code\` CSVs, the pre-draft prompts and handovers (`NEXT_PROMPT_*`, `SCRATCHPAD_INIT`,
`00_HANDOVER_READ_ME_FIRST`, `GEMINI_PROMPT`, `FABLE_TASKING_PROMPT`), the draft-only scripts (`rehearsal`,
`sept5_check`, `fetch_keepers`, `espn_draft_injector_Gemini`, the backtests, the audit) and the 2026 draft board and
mock log. Every one was exported from the store, committed to `_archive\store_predraft_20260922\` in its original
layout, staged back and compared by SHA-256 (153 of 153, then 47 of 47), and only then deleted. Eleven of the
exports had a drive twin of identical size; all eleven matched byte for byte, which is the check on the export
method itself.

**What stayed, on purpose.** The resident set and its companions, every doc from 200 on, every live script, the
2024 ADP source file (a live finding depends on it), `01_league_and_managers.md`, `code_espn_pull_projections.py`,
`code_rebuild_spine_v5.py`, `anchor_study.py` and `env_study.py` (queued for the re-run in section 4), and
`code/avail_pool.csv`, whose read came back inline rather than as a file and was not worth transcribing 50 KB by hand.

**What the units are.** `knowledge_size` is not bytes. The 153 docs were 1,287,687 bytes and cost 412,917 units,
**0.32 a byte for prose**; the 47 items were 1,072,292 bytes and cost 542,864 units, **about 0.5 a byte, because
0.94 MB of them were CSV**. Two files, `code/player_xwalk.csv` (518 KB) and `code/cv_pool.csv` (113 KB), held roughly
a quarter of the whole store. A CSV never goes into the store as a text doc again; §9 says so.

**What the room is worth.** Docs 200 to 383 are 1,633,015 bytes over 15.4 days, **106 KB a day, 96 KB over the last
seven**; at 0.32 that is about 31,000 units a day against 1,072,707 free, **thirty-five days**, less as the ledger
and the to-do file grow. Doc 383 said "a season". It was reasoned, not measured, and it was wrong by a factor of
three. The fix is the trigger in §0.5(d): when `project_info` reports more than 1,600,000, the oldest numbered docs
move out the same way, and the ledger records the count.

**Your bifurcation idea.** A second claude.ai Project holding `_archive\store_predraft_20260922\` would let a
session without the bridge search the pre-draft work. Only you can create a Project and upload a folder; I have
not put it on your list because nothing this season has needed a pre-draft doc that the findings file does not
already carry. If a session ever does, the folder is there and the ask is ten minutes.

---

## 2. THE REGISTRY, YEAR BY YEAR

| year | was | is now | how it was read |
|---|---|---|---|
| 2021 | `ADP#` from `Combined_Rankings_rankings_with_adp.csv`: **exactly 1 to 200, no gaps, a rank** | unchanged, flagged in `MANIFEST.csv` and `code_adp_guard.py` | on your list |
| 2022 | `FP_ADP` from an xlsx, 196 rows, whole numbers | FantasyPros half-PPR archive, 291 rows, Yahoo and Sleeper | your Chrome, 358-row table read in 20-row chunks, checksummed |
| 2023 | Underdog best-ball, 311 rows | FantasyPros half-PPR archive, 358 rows, three sites | same |
| 2024 | true half-PPR since doc 383 | unchanged; your PPR download sits beside it as `FantasyPros_2024_Overall_ADP_Rankings_PPR.csv`, a second instrument (948 rows, ESPN column present, Spearman 0.967 against the half-PPR file); your half-point download differs from the registry's raw file only in current-team labels and two tail rows, so it was not copied | |
| 2025 | nine-site ADP rounded to whole picks, 183 rows | unchanged, flagged | on your list |

**The transcription was checked three ways**: the row count, the sum of the rank column and the sum of the AVG column
matched the browser's own totals for both years; every AVG equals the mean of its site columns to one decimal, 649 of
649 rows; and the raw pages are in `Source\adp_registry\` as `FantasyPros_2022_...` and `FantasyPros_2023_...` beside
the registry files, in the 2024 file's format. The old 2022 and 2023 files are in `_archive`.

**Against the old files.** 2022: Spearman 0.971 on 176 shared names, median difference +1.5 places, **five men cross
the round-5 line and six the round-9 line**. 2023: 0.967 on 243 shared, median +9.1 (best-ball drafts run deeper than
redraft, so the old file put the tail higher), **ten cross the round-5 line and fourteen the round-9 line**. Same
lesson as doc 383: a different market is right on average and wrong at the lines, and the rules cut at the lines.

**Two team labels are 2026's.** FantasyPros renders an archive page with each man's current team (Josh Jacobs "GB",
Stefon Diggs "WAS" on the 2023 page). The numbers are the year's; the registry keeps player and ADP only.

---

## 3. JOB 4 ON THE THREE-YEAR REGISTRY

Same script, same population definition (year-N player-seasons 2022 to 2024, ADP 50 or later, priced again in N+1,
4+ games), the 2022 and 2023 files swapped. n = 333 (was 322).

| | doc 382, rank proxy | doc 383, true 2024 only | **doc 384, half-PPR 2022 to 2024** |
|---|---|---|---|
| pooled riser per +10 share points, net of price | +6.0 (se 1.8) | +5.7 (se 1.8) | **+4.3 (se 1.8)** |
| pooled gap, top third against bottom | +18.0 [4.0, 29.4] | +16.6 [2.6, 29.2] | **+17.8 [4.7, 31.8]** |
| **rounds 5 to 8: gap net of price** | +52.1 [26.3, 78.3], n=107 | +41.9 [11.2, 70.6], n=101 | **+51.0 [18.5, 73.4], n=100** |
| rounds 5 to 8: riser per +10 | | +10.5 (se 3.2) | **+17.2 (se 3.4)** |
| rounds 5 to 8: startable, top against bottom | 56% against 25% | 56% against 32% | **56% against 29%** |
| rounds 5 to 8: price inside the band (log ADP) | +2.2 (se 30) | −17.6 (se 31) | **−31.6 (se 28)** |
| round 9+: riser per +10 | +1.4 (se 2.0), n=227 | +1.8 (se 2.2), n=221 | **−0.1 (se 2.0), n=233** |
| round 9+: gap | | +6.5 [−8.4, 21.5] | **+6.5 [−7.9, 23.0]** |
| without "priced again", band gap | 44.8 [17.7, 72.1] | | **+53.8 [27.6, 79.0], n=102** |
| missing window scored zero, band gap | 47.9 [21.3, 73.9] | | **+55.2 [28.9, 78.7], n=110** |
| youth × riser, pooled | +8.5 (se 3.9) | +6.8 (se 4.0) | **−0.4 (se 3.9)** |
| youth × riser, inside the band | | +24.9 (se 10.7) | **+13.8 (se 10.3)** |

**The rule holds on its third instrument and the band number is back near where doc 382 had it.** Twelve men changed
side of the round-9 line between doc 383's registry and this one, which is the whole difference between 42 and 51:
the effect is concentrated, so who sits just inside the band decides the point estimate, and the interval has never
excluded ten on any of the three files. Round 9 and later is a dart on all three.

**The youth line dies.** +8.5, +6.8, −0.4 across three market files, with the same standard error each time, is a
number that depends on which men the market file puts in the population, not on youth. Inside the band it fell from
+24.9 to +13.8 at se 10, which is 1.3 standard errors and nothing to build a tiebreak on. §6's "about three times"
is struck; the riser is the tiebreak and youth is not.

**The population line, restated (§0.6):** the "priced again in N+1" condition drops about 40% of the band and the gap
is larger without it; the registries' name join lost 237 rows to no nflverse match, most of them kickers, defences
and men who never played. Doc 382's caveats stand.

---

## 4. OPEN, BY NAME

- **Matt's:** paste v9.12; the 2021 and 2025 FantasyPros half-PPR exports (item 2).
- **Mine, one batch:** 4.12, 4.18b, 4.20, 4.22, 4.25 and 4.26 on the three-year registry (doc 383's list, now on a
  better file; NOT YET RUN). When 2021 and 2025 arrive, JOB 4 gains a fourth year and 4.18b's NFL-wide arm gains a
  clean 2025.
- **Mine:** the keeper-riser line on the week sheet (doc 382 §5); doc 374 batch A; the directive read by someone with
  no stake in it.
- **Not a thread:** the pre-draft Project (section 1), unless a session needs it.

Ledger row 160. Directive v9.12. `Source\adp_registry\` rebuilt for 2022 and 2023; the old files are
`_archive\preseason_adp_2022_fpadp_xlsx_20260922_0630.csv` and `_archive\preseason_adp_2023_underdog_20260922_0630.csv`.
JOB 4 outputs for this run: `Scripts\research\j4\*_halfppr3.*`.
