# 328. The biggest file was not the complete one

*16 Sept 2026, 23:30 UTC. Matt moved his nine Gemini Notebook exports into `10_Gemni\Takes\`.
Merging them tested doc 323's warning directly, and the warning was right. Plus: the corpus page
rebuilt to what is left, the per-year link lists flattened, and one new show queued.*

---

## 1. WHAT CHANGED

1. **The notebook's own progress count is not a record, and this is the proof.** Nine 2021
   exports. **The largest file contains not one row from the first two.** Keeping only it would
   have discarded **199 of 418 rows**.
2. **Merged: `10_Gemni\Takes\2021_MERGED_USE_THIS.csv`, 418 unique rows, 19 episodes, 4 shows.**
   Nothing lost. 2021 is about **29% covered** (19 episodes against 65 links).
3. **The link files are now pasteable.** `Source\takes_links\<year>_PASTE.txt`, one flat list per
   year, no headings and no hash marks. 65 / 55 / 62 / 89 / 51 URLs for 2021 to 2025.
4. **`Source\TAKES_CORPUS.html` rebuilt to only what is left**, with a copy button on every block
   including each year's URLs.
5. **One show queued: the Fantasy Life Show.** Its research prompt asks for the launch date before
   anything else, because the show may not have existed for two of our five seasons.
6. **Waiver: Kaelon Black, and he is not rostered by anyone in the league**, so the button decides
   whether it costs priority at all.

---

## 2. THE MERGE, AND WHY IT MATTERS BEYOND 2021

Doc 323 recorded that this notebook fabricated a citation. Doc 325's follow-up recorded its claim
to *"maintain a list of what has been done"* as a claim from the thing being checked. Matt's nine
files let that be tested rather than argued.

**POPULATION: the nine `fantasy_takes_2021*.csv` files in `10_Gemni\Takes\`, 16 Sept.
KEY: the full 14-column row, exact string match. OUTCOME: rows unique to each file.**

| file | rows | NEW after the files above it |
|---|---|---|
| `fantasy_takes_2021.csv` | 72 | **72** |
| `_v2` | 127 | **127** |
| `_v3` | 118 | **118** |
| `_v4` | 135 | 17 |
| `_v5` `_v6` `_v7` `_v8` | 135 each | **0** (byte-identical to `_v4`, one sha256 across all four) |
| `_v9` | 219 | **84** |
| **merged** | | **418 unique** |

**`_v9` is the biggest file and it contains zero rows from the base file or from `_v2`.** It does
contain all of `_v3` and `_v4`. So the exports are not cumulative, they are not monotone, and
their size does not order them. `[TESTED, n=9 files, 418 unique rows]`

**THE RULE THAT COMES OUT OF IT, and it generalises past this notebook: when a tool hands you
successive exports of one job, never take the latest or the largest. Merge them all and
de-duplicate on the full row.** The cost of merging is a minute; the cost of picking is half the
corpus, silently, with no error.

**It also vindicates the guard rather than the tool.** The instruction added earlier today, to ask
the notebook to NAME the sources it just processed, is the cheap version of this check run at
batch time instead of at merge time.

---

## 3. COVERAGE, STATED HONESTLY

`2021_MERGED_USE_THIS.csv`: **19 distinct episodes**, by show: The Fantasy Footballers 285 rows,
FantasyPros 84, Fantasy Football Today 32, Rotoworld Football Show 17. Weeks present: 3, 4, 5, 6,
7, 9, 11, 12, 14, plus preseason rows marked `SUPPLIED`.

**Two things worth naming.**
- **Fantasy Football Today is not one of our nine shows.** It came back anyway, presumably from a
  link that resolved to it. Not a defect, but the coverage file does not know about it.
- **The extraction carries `source_title` and no URL**, so the finished episodes cannot be
  subtracted from the 65-link list by join. 2021 therefore gets re-run whole, and the de-duplicate
  above is what makes that free. `[OPEN]` if a later pass wants per-URL coverage, the extraction
  schema needs a `source_url` column.

---

## 4. THE NEW SHOW, AND THE ONE QUESTION THAT GATES IT

**Fantasy Life Show**, `youtube.com/@MBFantasyLifeShow`, published by Matthew Berry's Fantasy Life,
hosted by Kendall Valenzuela, Peter Overzet and Dwain McFarland with Matthew Berry appearances.
**888 episodes, updated daily.** `[SOURCED: podcasts.apple.com/us/podcast/fantasy-life-show/id1642787926, read 16 Sept 2026]`

**THE GATE, AND IT IS STATED BEFORE THE RESEARCH RUNS RATHER THAN AFTER:** the show's Apple id
(1642787926) sits in a range consistent with a late-2022 registration, and the corpus covers 2021
to 2025. **If it launched in 2022 or 2023 it can cover at most three of our five seasons**, which
halves its value and changes nothing about the other nine shows. I did not find a published launch
date in two searches, so **the prompt's PART 0 demands it first, in one line, before any links.**
That is a claim I refuse to make on an id-range inference. `[NOT YET RUN]`

**AND A DAILY SHOW IS A DIFFERENT OBJECT.** Nine hundred episodes is not a source list; a Pro
notebook caps at 300 sources and retrieval dilutes long before that. The prompt therefore asks for
**one waiver episode per week, fourteen per season**, plus the preseason episodes, and names
everything else the show publishes as out of scope.

---

## 5. THE WAIVER CALL

Matt's standing claim is Dalton Schultz in, T.J. Hockenson out. It is right and it stays at
priority 1: **+6.1 to his starting nine and it fixes the week-6 hole.**

**THE SECOND MOVE IS KAELON BLACK (RB, SF), AND IT PROBABLY IS NOT A CLAIM.** Checked against
`LEAGUE_ROSTERS.csv`, 182 rows across all twelve teams: **he is on nobody's roster.** So if ESPN
shows an Add button it costs no waiver priority at all, and only a drop.

- **15 carries and targets in week 1**, the most of any unrostered back on the wire.
- **43% of San Francisco's snaps.**
- **`job_pays` 302**, the largest on the wire, and `inherit_2026.csv` carries a **live tag of
  questionable** on McCaffrey plus a week-1 note that the snaps split and Black led the carries.
- **Doc 314's band: 15+ opportunities means 2.27 filers and 56% contested**, the most-raced cell
  on the board. Owned elsewhere has gone free to 43.0% in two days.

**THE DROP IS SHOUGH**, measured at 0.05 a game over the best free quarterback (doc 259). It
leaves one QB against Hurts' week-10 bye, which is already a week-9 item on the list.

**AND THE HONEST SIDE OF IT (§4.19, doc 259): this adds nothing to his lineup this week and four
of five backs he adds never give him a startable stretch.** It is a bench bet on a job, priced by
doc 240's rule, not an upgrade.

**FALLBACK IF BLACK IS GONE: Chris Brooks (RB, GB).** Josh Jacobs has been on the Commissioner's
Exempt List since 30 Aug 2026, indefinitely, so that job is **already open and worth 241**, not a
seat waiting on an injury. Brooks took **56% of the snaps** in week 1 at **11.5% owned**, the
29%-contested band, so nobody is racing. Against him: he splits with MarShawn Lloyd, who is
rostered and out-carried him 13 to 7.

---

## 6. OPEN

- **The Fantasy Life launch date.** `[NOT YET RUN]`, gating its 2021 and 2022 rows.
- **A `source_url` column on the extraction schema**, so finished episodes can be subtracted from
  a year's link list. `[OPEN]`
- **Fantasy Football Today is in the 2021 rows and not in the coverage file.** `[OPEN]`
- **2022, 2023, 2024, 2025 notebooks not built.** Links ready: 55 / 62 / 89 / 51.
- Carried from doc 326: JOB 3, the §4.25b wording, the draft-capital column, the disagreement tell,
  catalog B4.
