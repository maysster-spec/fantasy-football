# 291 · Batch 1, first half: Washington is back, every guard is shown firing, and the sheet stops repeating ESPN

*11 Sept 2026, 10:15 am to 12:30 pm ET. Batch 1 was due Saturday 9 am; it started early on Matt's word ("if you
have something left to run, then run it"). Items: A4 with A16, A15, A2, A6, D1-D3 (catalog doc 290 §4), plus A10's
week source and two bye-plan defects that had to be fixed for those sections to render at all.
Committed to the drive 11 Sept, verified by checksum (14 of 14 files). The Sunday 11:40 am scheduled run is the
first live run of this code.*

---

## 0. What changed, in one screen

1. **Washington is back on both pages.** All 17 Commanders rows with a projection are priced (they were dropped
   by a `WAS`/`WSH` mismatch). One team-code map now serves both scripts, and every loader that reads a team code
   refuses or bannerises a code that resolves to no team, naming it.
2. **Measured cost of the Washington hole on the 10 Sept pool: nothing Matt would have seen.** The nine free
   Washington skill players all price below the six shown at their position; the Commanders defence ranks 26 of
   31 on rate, 30 of 31 over weeks 2-5, and never better than 13th in any single week 2-11, even treating every
   defence as free; Drew Stevens ranks 22 of 31 kickers. The fix is the guard, not a player.
3. **The sheet is on the right scale (A2).** A season projection covers 17 games; the page divided by 14. On the
   corrected scale a screened receiver who hits clears Matt's receiver bar every week instead of only in bye
   weeks: "if it fires" rises from 1.3 to 8.7 points and "expected" from 0.4 to 2.9 (McMillan, Bryant).
4. **That exposes A1, the missing injury model, as the next thing that matters.** With the tickets at 2.9, the
   cheapest thing Matt owns is Hockenson at 0.0, and the old verdict would have read "take the ticket". Two
   changes keep the page honest until A1 lands: a back he owns who is the direct backup to a job is priced by
   the seat arithmetic (Mike Washington Jr.: 0.0 becomes **3.1, priced as the handcuff to Ashton Jeanty**), and a
   zero-cost body sitting behind a healthier starter at his own position gets an insurance verdict ("it clears on
   paper, and the paper cannot see injuries") instead of a take.
5. **Sections that had never rendered now do.** The week was read from a payload that does not carry it, so the
   defence run, the weeks-ahead box, the bye plan and every "(yours)" marker were blank or bannered. The week now
   comes from the roster read.
6. **Two things those sections would have got wrong on first render, fixed before they shipped.** The bye plan told
   Matt to shop Jalen Hurts and Puka Nacua to cover the week-6 tight-end bye; a week whose only hole is one
   single-slot position now reads "one empty TE slot, a one-week pickup fills it" and the trade advice is kept for
   weeks that take out several positions (week 11: Adams, Nacua, Judkins). And the defence run averaged a bye week
   away, so the Chiefs' three games and a bye ranked third, ahead of four-game runs; a run with a bye now sits
   below every run without one.
7. **Matt's do-not rule (A15) is in.** A screened man ESPN lists out, doubtful, questionable or on IR is no longer
   named in the missing-row box; a DO NOT card for a man ESPN lists out or on IR is off the page; a card for a man
   another team claimed is off the page and the console names him. The guard stays for the case only the page can
   show: a healthy man with no projection (control C7).
8. **Every guard is now shown firing on every path that reaches a page (A16).** 33 checks in
   `Scripts\research\redteam\redteam_controls.py`. On the pre-291 code, 9 of 33 pass: seven behaviours that
   should survive, the one guard that already worked (team shape), and one ordering check that passes only
   because the old code rendered no defence run at all (its companion check fails).
9. **Retractions swept (D1-D3).** The last page survivors are gone (one sentence on the wire rewritten, two seat
   sentences on the sheet narrowed to what was measured); the two "measured replacement" labels are fixed; doc
   281 and the charter carry dated corrections on 11.2. `check_plain.py` now scans the week sheet, and
   `check_kit.py` had been reporting two stale pins nobody read (since 8 and 10 Sept).
10. **Nothing to run from Matt except one by-hand run before Sunday** (on his to-do): it is the first live test of
    all of the above, a day before the scheduled one matters.

---

## 1. How it was tested, and how far the harness can be trusted

The cloud workspace cannot reach ESPN (proxy 403), so both pages were rebuilt from a **recorded pool**: the
`kona_player_info` and `mRoster` reads are replaced with the 10 Sept free pool (`WIRE_20260910.csv`, 279 skill
players, no kickers or defences) and Matt's 15 from 11 Sept. Everything else is the production code path.

**Fidelity, checked before any fix:** the pre-291 code on the recorded pool reproduces the live 10 Sept
`WEEK_SHEET.html` line for line except (a) the date, (b) the kicker and defence tables, because the recorded pool
holds no kickers or defences and the harness treats every one Matt does not own as free (the generous direction
for any "would he have shown" question), and (c) five card passages that `cards_2026.csv` rewrote at 19:33, after
the page was built at 17:50 (A6). The drop-cost table and the verdict match exactly (Washington 0.0, Hockenson 0.0,
Dobbins 3.2, Dowdle 5.2; best ticket 0.4).

**Two synthetic statuses** drive the do-not controls: Pearsall `INJURY_RESERVE` (true: his card records
season-ending surgery) and McMillan `QUESTIONABLE` (a control, not a report about him).

---

## 2. A4 with A16: the team codes, and the guard on every path

**What was wrong.** Seven files spell teams three ways. The projection pull and ESPN's roster read say `WSH`/`LAR`;
`byes_2026.csv`, the board, `team_2025.csv`, `pos_allowed_2025.csv` and the depth map say `WAS` (and some `LA`);
`team_shape_2025.csv` uses PFF's `ARZ`/`BLT`/`CLV`/`HST`/`LA`/`WAS`; and `wire.py`'s own `PRO` map turned ESPN's
team 28 into `WAS`. `rates()` joined the pull to the byes on the raw string, so every `WSH` row fell out with no
error, and the only team-code assert anywhere (on `team_shape_2025.csv`) never saw that join.

**Fix.** `sheet_engine.py` holds the one map (`ESPN_TEAMS`, `TEAM_ALIAS`, `team_key()`, `unknown_teams()`);
`wire.py` imports it and refuses to start without it. `rates()` refuses unless the byes resolve to exactly the 32
teams, and refuses naming every pull code that resolves to none. `load_sched`, `load_team25` and `load_posallow`
normalise and report unknown codes into a LOAD PROBLEM banner printed at the top of the wire page.

**The path sweep.** Every input either page reads, fed one bad row, before and after:

| input | bad row | pre-291 | now | control |
|---|---|---|---|---|
| `byes_2026.csv` | a team code that is no team | silent: that team off the sheet | sheet refused, code named, banner on the wire | C1 |
| projection pull | one row's team code | silent: that player off the sheet | refused, `XXX (1 players)` | C1c |
| `team_2025.csv` | one code | silent: opponent strength missing | banner names file and code | C2 |
| `sched_2026.csv` | one opponent code | silent | banner | C3 |
| `pos_allowed_2025.csv` | one code | silent | banner | C4 |
| `team_shape_2025.csv` | one code | **fired** (the ARZ assert) | fires | C5 |
| `cards_2026.csv` | blank id, messy team code | shown | shown, matched on name + position + team | C9 |
| `cards_2026.csv` | wrong id | marked "no longer free" on the page | shown; console names the mismatch | C15 |
| `inherit_2026.csv` | holder spelled "Ashton Jeanty Jr." | **silent: Washington priced as "the seat behind" at 0.9 instead of the handcuff** | same 3.1 handcuff price | C13 |
| `inherit_2026.csv` | `next_man_id` off by one | **silent: Washington at 0.0** | same 3.1; console names the id | C14 |
| `board_v8_fixed.csv` | id not on the board | named ("not on our board") | named | (existing) |
| `sheet_constants.json` | missing | sections say missing | same | (existing) |
| `pedigree_2026.csv` | id mismatch | silent: a screened receiver loses his screen | **still silent** | open, A5 |
| `redzone_te_2025.csv` | id mismatch | silent: a tight end reads as zero inside-ten looks | **still silent** | open, A11 |
| `depth_map.csv` | id mismatch | silent: a backup drops out of the stash lane | **still silent** | open, batch 3 |

The two seat joins (C13, C14) were name joins on a file with no holder id: §3's defect, currently matching 100%,
and on the one row Matt has said he will never drop. Both now go id first, then normalised name AND team
(`norm_name()`, `roster_match()`), and every fallback prints.

**The measured cost, on the recorded pool** (population: every row in the 7 Sept pull with a projection, 32
defences, 32 kickers; free = the 10 Sept pool, with every kicker and defence Matt does not own treated as free):

- All 17 `WSH` rows now priced: Daniels 21.3 a game, McLaurin 10.6, Croskey-Merritt 8.9, White 8.5, Diggs 8.0,
  Stevens (K) 7.9, Okonkwo 5.6, the defence 4.2, and nine below 4.
- The nine Washington players in the 10 Sept free pool (eight priced, the best Antonio Williams at 3.8 a game;
  Jerome Ford has no projection) all rank below the sixth man shown at their position.
- Commanders D/ST: 26 of 31 on rate; 30 of 31 over weeks 2-5 (DAL, SEA, IND, NYG, who scored 26.5 a game);
  single-week rank 25, 29, 24, 13, 19, bye, 13, 29, 14, 18 in weeks 2-11. Never in the top two a week shows.
- Drew Stevens: 22 of 31 kickers, below the sixth shown (Butker 8.75 against his 7.86).

**So Matt's note held in the direction he feared and not in size:** defence is where a matchup edge is measured,
and an invisible defence could have mattered; this one would never have been on the page. What was worth fixing
was the join, because the next code drift would take out a team whose defence does matter.

**And the checker nobody read (doc 260 again).** `check_kit.py` pinned `check_plain.py` at 5,240 bytes while the
drive held 5,481 since 8 Sept, and `ff.bat` at 1,835 while the drive held 2,071 (normalised) since the WEEK_SHEET
line went in on 10 Sept. Every run since has reported two STALE files. Both re-pinned at the drive's bytes, with
`wire.py` and `sheet_engine.py` at their new ones.

---

## 3. A10's week source, and the two sections it switched on

`wire.py` read the week from `kona_player_info`, which carries no `scoringPeriodId`; `lineup.py` already read it
from `mRoster`. Week 0 meant: no defence run ("the week is unknown"), no weeks-ahead box, no bye headline, and no
"(yours)" on the tight-end box or the defence run. Now `data.get('scoringPeriodId') or rosters.get(...)`. Matt's
own defence now comes from the roster read (`mine_meta`), since the board has no D/ST rows; his tight ends take
their team from the board and fall back to the roster read.

**Bye plan, one hole.** With the week read, the first build told him to trade Hurts and Nacua for the week-6 bye.
Week 6 takes out LaPorta and Hockenson, two tight ends: one starting slot. `bye_plan` now sets `one_slot` when every
man off in the next live bye week plays one position with one lineup slot; the section is titled "Your bye weeks"
and says a one-week pickup fills it. The trade text stays for multi-position weeks: with the week set to 7, week
11 (Adams, Nacua, Judkins, 23 points) keeps "The trade that is sitting there" (control C12).

**Defence run, bye inside the run.** `dst_runs` averaged opponents' scoring over the weeks a defence plays, so a
bye simply dropped out of the average. The section's own argument is that holding one defence spares the claim;
a bye inside the run is a claim that week anyway. Runs now sort by (byes in the run, softness) and the table prints
**bye** in place of an opponent. Weeks 2-5 top five before: Saints, Browns (his), Chiefs (bye in week 5),
Ravens, Bears; now: Saints, Browns (his), Ravens, Bears, Falcons (control C10). **A10's modelling half (raw 2025 opponent scoring
against the slate model with form) is untouched and stays in batch 3.**

---

## 4. A15: the do-not rule

Matt's rule: a do-not line earns space only when the page is the only place that information exists.

- **Missing-row box:** a screened man with no projection is named only if ESPN lists no status for him
  (`ESPN_SHOWS_STATUS`: OUT, IR, SUSPENSION, DOUBTFUL, QUESTIONABLE, DAY_TO_DAY, PUP, NOT_ACTIVE). Pearsall is gone
  from the sheet (C0); Pearsall back to ACTIVE returns him (C6); a healthy man with a blanked projection is still
  named (C7) and the same man listed OUT is left to ESPN (C7b).
- **Cards:** a DO NOT card for a man ESPN lists as gone for weeks (`GONE_FOR_WEEKS`) is off the page; a card for a
  man no longer in the free pool is off the page (the NO LONGER FREE marker is removed) and `week sheet:` in the
  console names him (C8). The status travels in a new last column of `WIRE_<date>.csv`, written before the sheet is
  built in the same run.
- **The console lane 3** now prints ESPN's status beside a non-active name (it has no player card beside it), so
  "Ricky Pearsall ... [ESPN: injury reserve]" no longer reads as a clean stash.
- **To-do list sweep:** the Pearsall line was removed on 11 Sept; the "GONE TODAY" note is rewritten to match the
  new behaviour; the Dell and Strange do-not lines stay (ESPN does not show the IR mechanics or our own retraction).

---

## 5. A2: the scale, and what it exposed

`rates()` and `bye_plan()` now divide by `PROJ_GAMES = 17.0`. Weeks priced stay 14. The footer says so.

**Why it moves the verdict** (population: Matt's 15 on 11 Sept, the recorded pool; same arithmetic as the page):

| | pre-291 (÷14) | now (÷17) |
|---|---|---|
| Matt's receiver bar, most weeks | about 14.2 | 11.7 |
| a screened hit, "if it fires" (12.7 a game for 6.4 weeks) | 1.3 | 8.7 |
| best screened ticket, "expected" (33% odds) | 0.4 | 2.9 |
| cheapest body he owns | Washington 0.0, Hockenson 0.0 | Hockenson 0.0 |
| Washington | 0.0 | 3.1, as the handcuff to Jeanty |
| Dobbins / Dowdle | 3.2 / 5.2 | 2.6 / 4.3 |
| verdict | "it clears by almost nothing ... drop nobody for it" | "it clears on paper, and the paper cannot see injuries" |

The hit size is a per-game number measured on real weeks, and the bar was a season projection spread over 14: the
old page compared a real game against a 21% inflated one. The correction is not a new finding; it removes a units
error. What it does expose is A1: on the right scale, zero-cost bench bodies look droppable, and some of them are
insurance. **The handcuff seat price and the insurance verdict are stopgaps, not the fix.** A1 moves to the front
of the second half.

**Re-derived, not inherited:** the handcuff price uses the seat constants already on the page (backup scores 12.13
a game in relief, plays 3.02 weeks, the job opens 46% of the time), priced week by week against the bar Matt would
have without Jeanty. Those constants are themselves `[INHERITED]` under D4.

---

## 6. A6: stale pages, and a stamp so it is visible next time

Both pages now end with the code that built them: file name, bytes, modified time and a 10-character hash, for
`wire.py` and `sheet_engine.py`. The sheet is written to a temp file and swapped in, so a crash cannot leave half a
page. The offline rebuild's sentence diff (pre-291 code against new, same pool) changes the verdict box, the cost
table, the bet table, the missing-row box, the cards section, the defence and kicker footer, and on the wire page
the routine box, the rules box, the drop table, the bye section, the defence run and the stash-lane close.

---

## 7. D1-D3: the retraction sweep

**Page and code survivors removed** (grep on both scripts and both rebuilt pages; the only hit left is the word
"Spears" in a code comment explaining why the drop table was rebuilt, and his row in the free-player tables):

| sentence as it stood | where | why it went | now |
|---|---|---|---|
| "Priority resets every week ... using it costs you nothing" | wire routine | docs 226/255/280: the first winning claim sends you to the back for that run | the man you most want goes first |
| "Always claim. Never wait ... a plain free-agent add did not beat him at all" | wire routine | doc 205's own caveat: the claim pool is the fresh pool by construction; sits beside "Do every Add first" | the mechanical reason: claims settle early Thursday, and the two busiest free-agent hours of the week are the two after |
| "stream the defence and the kicker on matchup ... not season-long holds" | wire routine | contradicted "The defence to HOLD" on the same page (doc 230) | kicker on matchup; hold a defence through a soft run |
| "Hit rates are flat from week 1 to week 14 ... Volume is not the lever" | wire rules | doc 252 (week 1 is the worst week), doc 279 (volume is the lever) | "The wire thins but does not dry up" |
| the draft-night drop table (Spears listed, Hockenson missing) | wire | typed once, never rebuilt | built from the roster every run, keyed on ESPN id |
| the Nacua handcuff note ("the pick at 41", Atwell) | wire | a draft-night note | removed |
| "on 62 measured absences" | sheet seat box | beside a constant that says 51 | removed |
| "That rate is the same at every team: it does not go up because the starter missed time last year" and "a starter who missed time last season was no likelier to miss time" | sheet | doc 276's test counted only backs healthy through week 4 (catalog B4) | narrowed to what was measured; B4 re-tests it |

**Labels (ledger row 8, now closed):** `research/build_pedigree.py:29` and `sheet_constants.json`'s in-season
baseline both said "doc 12's measured WR replacement"; both now say derived (the board's WR30 season total ÷ 17).
The JSON change was checked to alter that one string and no number.

**D3, the record:** doc 281 §5 carries a dated correction (11.2 is NFL team-seasons, not this league; it is the
middle of relief scoring, not "the rate at which a fill-in back kept the job"; rho +0.006 was doc 275's). The
charter's §6(2) carries a note that its target gate was already gone. Both originals archived.

**D7 closed:** `check_plain.py` now lists `WEEK_SHEET.html`, and a planted "n=39, p=0.97 per doc 275" line on it
fires three hits. Both rebuilt pages scan clean.

---

## 8. For G2: an injury can be told apart from a coach's reaction

Matt asked whether injuries can be separated from a benching. They can, from nflverse's weekly injury reports and
roster status. **POPULATION:** RB/WR/TE regular-season player-games 2021-2025 with 5+ carries plus targets.
**EVENT:** a lost fumble. **OUTCOME at the team's next game:** on the injury report / Out or Doubtful / roster
status not active / no offensive snaps.

| | n | on report | Out or Doubtful | not active | no snaps |
|---|---|---|---|---|---|
| lost a fumble | 448 | 11.2% | 4.9% | 6.7% | 7.8% |
| no lost fumble | 10,488 | 8.5% | 2.6% | 5.6% | 6.7% |

So the injury screen removes between one fumble event in twenty (Out or Doubtful) and one in nine (any
injury-report listing) before G2 measures the role change. The excess over games without a fumble is 1 to 3
points depending on the measure, and that excess is exactly what a role test with no injury screen would misread
as a coach's reaction. Script:
`Scripts\research\injury_overlap.py`. `[TESTED, descriptive only; G2 itself NOT YET RUN]`

---

## 9. What held, what is open

**Held:** the team-shape assert (it did fire on its own path); the missing-row guard's purpose (C7); the
defence-run and bye-plan arguments themselves, which only needed their inputs read.

**Open, carried to the second half and later batches:**
1. **A1, the injury model: now first in the second half.** Order: A1, F2, F1, F3, B5, B9.
2. Three silent id joins (pedigree → A5, red-zone tight ends → A11, depth map → batch 3).
3. The wire page's "Why the gem must be claimed early" box still carries docs 224-226's skill-only population
   ("five of every six", "22% against 24%"); doc 250 re-read the first and §0.6 the second. Added to D1's
   remainder; it goes with B-family retesting, not a wording patch.
4. The wire's bye table is still built from the board, so Pickens, Pineiro and the Browns defence are "not on our
   board" and week 14 is missing (A5, batch 3). The sheet, which uses the pull, already shows all three holes.
5. `Source\00_PROJECT_DIRECTIVE-1.md` was a byte-identical copy of v9.3 sitting beside v9.4, the naming rule's
   exact defect; its bytes are in `_archive\00_PROJECT_DIRECTIVE_v93_20260911.md`, so the file now holds a
   one-paragraph pointer to the canonical directive. Deleting it needs a delete permission this session does not
   have.
6. The first live run. The harness cannot see ESPN's real kicker and defence availability or live statuses.
