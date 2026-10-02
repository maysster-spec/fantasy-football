# 339 THE EXPORTS ARE RE-EXTRACTIONS, NOT BATCHES

**2026-09-17.** Matt, looking at eight identically named `ff_takes_2023.csv` rows in the Gemini
Notebook: *"i can't tell if they are batches are not, but i guess i'll download and hand you all of
them."* He should not have to download 40 files to find out, and he does not have to.

---

## 1. THE TEST, AND HE SET IT UP HIMSELF

While this was being looked at he downloaded three copies of the 2025 export. That is the
experiment: same year, same notebook, three exports minutes apart.

| file | bytes | sha256 | rows | unique rows | sources |
|---|---|---|---|---|---|
| `fantasy_football_takes_2025.csv` | 71,060 | 9ea854ef08 | 244 | 244 | 51 |
| `fantasy_football_takes (1) 2025.csv` | 71,060 | **9ea854ef08** | 244 | 244 | 51 |
| `fantasy_football_takes (2) 2025.csv` | 70,979 | 2a468e6e03 | 244 | 244 | 51 |

**`(1)` is byte-identical to the base: a double download.**
**`(2)` holds the SAME 244 rows from the SAME 51 sources, of which 22 are different takes.**
Twenty-two out, twenty-two in, on different players: the base carries Dylan Sampson and a
Christopher Harris line, `(2)` carries Marquise Brown, Elic Ayomanor and Juwan Johnson.

**So the notebook re-runs the extraction each time and lands on a slightly different sample of the
same sources.** Source coverage does not grow. Row coverage grows about 9% per export, with
diminishing returns. Union of the three: 266 against 244 in any one. `[TESTED, n=3 exports]`

## 2. THIS CORRECTS DOC 328's REASON, NOT ITS RULE

Doc 328 measured that the largest 2021 export was not the superset and concluded: **merge every
export and de-duplicate on the full row.** That rule is right and stands. **The reason given for it
was wrong.** It read as though the exports were sequential batches whose union completes the job.
They are repeated samples. The practical difference is the stopping rule: **two or three exports a
year is worth it and eight is waste.**

## 3. AND THE THING MORE EXPORTS CANNOT FIX

Coverage, source titles normalised (a leading `12. ` stripped before counting):

| season | exports held | rows | sources | notebook sources | coverage |
|---|---|---|---|---|---|
| 2021 | 10 | 418 | **19** | 65 | **29%** |
| 2022 | 2 | 197 | 53 | 55 | 96% |
| 2023 | 1 | 170 | 61 | 62 | 98% |
| 2024 | 1 | 107 | **47** | 89 | **53%** |
| 2025 | 3 | 266 | 51 | 51 | 100% |
| **TOTAL** | | **1,158** | **231** | **322** | **72%** |

**One 2023 export already holds 61 of 62 sources, so the other seven can add one source at most.**
That is the answer to his question and it is why the download was not worth doing.

**2021 is the case that looks like it should have been fixed by merging and was not.** Each 2021
export carried 4 to 9 sources; the union across all ten is 19. Merging worked exactly as doc 328
said: 5 sources to 19, 219 rows to 418. **It cannot reach the other 46, because the notebook never
processed them.** Same shape at 2024, 47 of 89. **Those two need the notebook re-run with the
current prompt. No number of downloads gets there.**

## 4. SHIPPED

`10_Gemni\Takes\TAKES_2021_2025.csv` , 1,158 takes, 472 players, 46 analysts, five seasons, the
14-column schema plus `season`, de-duplicated on the full row across every export present.
Call types: WAIVER_ADD 525 · START 124 · SLEEPER 98 · STASH 88 · RANKING_ONLY 81 · BREAKOUT 75 ·
BUST 60 · WAIVER_FADE 58 · HANDCUFF 24 · SIT 3. Direction UP 927 / DOWN 123 / NEUTRAL 86.

`10_Gemni\Takes\COVERAGE - read before using the corpus.txt` sits beside it and carries the table
above, because section 0.6 says the population goes in every doc that uses an inherited dataset and
a sidecar is the only way a CSV can carry one.

**TWO BYTE-IDENTICAL DUPLICATES ARE IN THAT FOLDER AND CAN BE DELETED:**
`ff_takes_2022_scored (1).csv` (sha 90d543710b85) and `fantasy_football_takes (1) 2025.csv`
(sha 9ea854ef0878).

## 5. WHAT THIS DOES NOT SAY

It does not say the extraction is accurate, only that it is non-deterministic. Nothing here has
checked a single `verbatim` against its source video. **The corpus is a list of claims, not a list
of verified claims**, and the analyst hit-rate work that motivated it has to treat it that way.
