# 344 -- THE HARNESS THAT SHIPPED WAS THE OLD ONE, THE FLOOR WAS A ROUNDING, AND TWO OF THE EIGHT TARGETS WERE NEVER WRITTEN

*17 September 2026, 22:50 UTC. Second reader on docs 314 to 321 (section A of `REDTEAM_TASKING_PROMPT.md`,
with the 22:00 box), plus Matt's mid-run correction: 316 and 317 do not exist, item 2 runs against
`drop_costs()`, doc 327 section 3 and the two 16 September to-do entries, and a seventh item, every
reference in the project that points at a file nobody wrote. Every result below was run, not read.
Scripts and outputs in `Scripts\research\rt344\`. No claim filed, nobody dropped, nothing written to ESPN.*

---

## 0. WHAT TO DO

1. **`py research\redteam\redteam_controls.py` now says 56 of 56, not 44.** The file on the drive was the
   16 Sept 08:05 harness plus one line; C18 to C21 (the usage re-rank, the both-ways fill, the touches
   column reaching both artifacts) had been lost. Restored from `_archive\redteam_controls_20260916_1915.py`,
   the 20,578-byte copy archived as `_archive\redteam_controls_20260917_2245.py`, and both harnesses run
   against the shipping code here: 44 of 44 and 56 of 56 pass. The code kept every feature; only the
   guard had reverted. Your to-do line 389 should read 56.
2. **Doc 316's cap rule is not in `sheet_engine.py`.** The 16 Sept 03:00 archive holds it (keep five, then
   re-admit any row whose contest band says put him first); the 08:05 archive and everything since have a
   plain `now[:5]`. Your to-do marks it `[x] DONE`. Kaelon Black is cut at sixth on today's page and his
   warning cannot print. Not patched here, because that file is open in the other session tonight; the
   eleven lines are quoted in section 2b for a one-minute restore.
3. **Read the contested percentage from your seat, not the page's.** The page's 14 / 29 / 40 / 56 is the
   share of claimed men who drew two or more claims. The question you ask is "if I file, does anyone
   else", and on the same rows that is **30 / 56 / 68 / 82** per cent. The 5-to-9 band, where Schultz and
   Mayer sit tonight with "nobody is racing you for him", is a majority from your seat, not a 29 per cent
   minority. The order of the bands is unchanged; the sentence's threshold is not.
4. **Doc 314's bands survive the zero-filer test, and get stronger.** With every free RB, WR and TE
   nobody filed on put back in (14,789 free player-weeks, weeks 2 to 14), mean filers go 0.01 / 0.12 /
   0.47 / 1.12 across the four bands and the correlation is +0.316, permutation p=0.0002. Item 1 is a
   null on the falsifier.
5. **The word "floor" is wrong on the very row printed tonight, by rounding.** Browns D/ST: the page
   prints 8.5 and "2.5 against the ordinary defence"; the unrounded arithmetic is 8.0 and 2.0, and 2.0 is
   exactly the simulated arm C. `bar_grid()` rounds the Chiefs' 5.95 down to 5.9 and `price()` rounds each
   week's 0.16 up to 0.2, twelve times. Say "about", never "floor".
6. **The drop ladder prices K and D/ST, and the code comment says it does not.** Pineiro 8.4, Chiefs D/ST
   -2.0, both on tonight's page. And the D/ST pair double counts: the page shows "add Browns +8.5" and
   "drop Chiefs -2.0", a reader nets +10.5, the actual swap is +2.0.
7. **The commit bug in ledger row 89 reproduces and is now bracketed:** a re-commit of edited bytes from
   the same container path within about 2.5 minutes of the previous commit sends the previous bytes
   (26-byte and 35 KB files alike, `force` or not, mtime advances); by 4.5 minutes it is fresh; a
   `device_stage_files` of the destination in between clears it at once (fresh after 30 seconds). That is
   the residual row 89 could not explain: `check_kit.py` was re-staged between its three commits.
8. **Seven document numbers are cited and were never written: 60, 102, 108, 169, 311, 316, 317.** Doc 60
   is cited twice by the directive itself (section 4.12 and section 8); 102 is `depth_map.py`'s own
   header; 311 is cited by two ledger rows and `wire.py`; 316 and 317 by the tasking prompt, the code's
   provenance comments and docs 319 to 327. Two files are cited and are on no listing: `manager_identity_map.csv`
   (directive 4.19) and `draft_analysis.json` (directive 4.29).
9. **Nothing else to run.** Item 3 finds no case at the skill positions; item 4 leaves both p-values
   standing with a caveat each; item 5 reproduces the contest block exactly and the seat constants only
   roughly, because no script in the tree computes them.

---

## 1. THE SEVEN ITEMS, EACH WITH ITS TESTABLE FORM FIRST

### Item 1. Doc 314's contest bands, with the men nobody filed on

> Among every free RB/WR/TE with a prior regular-season game, in the free pool rebuilt week by week from
> the draft plus every executed add and drop 2022-2025, mean waiver filers (zero for the unfiled) and the
> share drawing two or more claims still rise with last-game targets plus carries. Falsifier: the 15+ band
> is not above the under-5 band once the zeros are in.

**CONTROL FIRST.** The claimed-only rows of my join reproduce doc 314 to the digit: 1.17 / 1.49 / 1.83 /
2.27 filers, 14 / 29 / 40 / 56 per cent contested, n 88 / 180 / 94 / 41, r=+0.296, n=403. **Only when
weeks 15 to 18 are included.** Doc 314's population takes in playoff-week claims (53 of its 403 rows) and
does not say so; the page applies it to regular-season decisions. On weeks 2 to 14 alone: 1.20 / 1.54 /
1.84 / 2.40, 16 / 32 / 42 / 57 per cent, n=350, r=+0.316. Slightly stronger, same shape. Not a kill,
a population line that belongs in the doc (0.6).

**THE TEST.** Free pool = every RB/WR/TE with a nflverse line before week w who is on nobody's roster at
the week's last waiver run (rosters from the draft by name, then 1,230 executed transactions in date
order; 5 of 611 drafted skill names failed to match). 14,789 free player-weeks, weeks 2-14:

| last-game carries + targets | free men | mean filers | any claim | 2+ claims | 2+ given any |
|---|---|---|---|---|---|
| under 5 | 12,442 | 0.01 | 0.6% | 0.1% | 16% |
| 5 to 9 | 1,938 | 0.12 | 7.9% | 2.5% | 32% |
| 10 to 14 | 334 | 0.47 | 25.7% | 10.8% | 42% |
| 15 or more | 75 | 1.12 | 46.7% | 26.7% | 57% |

r(touches, filers) = +0.316, permutation p=0.0002 (5,000 draws). By position RB +0.34, WR +0.25, TE +0.35.
`[TESTED, n=14,789]` **The bands survive. The selection the prompt named (filers conditioned on at least
one filer) leaves the conditional column exactly where doc 314 put it and adds two columns the page did
not have: a 15+ touch free man draws a claim from anybody in under half of his weeks.**

**THE SELECTION DOC 314 DID NOT NAME, AND IT IS THE ONE THAT MATTERS FOR THE SENTENCE.** "Contested" on
the page is P(2+ filers | somebody filed), one row per player-week. Matt's question is P(somebody else
files | I file). If his filing behaves like the other eleven's, the second is the claim-weighted rate,
because a week with seven filers is seven times as likely to be one he is in:

| band | page prints | from the claimant's seat (one row per claim, n=569) |
|---|---|---|
| under 5 | 14% | **30%** |
| 5 to 9 | 29% | **56%** |
| 10 to 14 | 40% | **68%** |
| 15 or more | 56% | **82%** |

`contest()` prints "Put him first" at 38 per cent and above and "Nobody is racing you for him" below it.
On the claimant's rate only the under-5 band is a minority. `[TESTED; the exchangeability assumption is
stated, not measured. Section 4.19 has him earlier to the player than the field at RB, which cuts the
other way for backs only.]` The ORDER of the bands is untouched, which is what the sort uses.

**Smaller selections, all checked and none material:** filers include CANCELED and PENDING claims (80 of
787 player-weeks change count; the bands move to 1.22 / 1.57 / 1.82 / 2.35 and 18 / 33 / 39 / 56 without
them); two runs in one week are merged into one player-week; the 15+ band is a running-back band (70 of
75 free men, and 5 receivers); the touch count is the last game the man played, however long ago.
`Scripts\research\rt344\rt1_zero_filers.py`, outputs beside it.

### Item 2. The drop ladder: `drop_costs()`, doc 327 section 3, the two 16 September entries

> For each of Matt's fifteen, the page's ladder (netted against the best free body at his position)
> differs from the same-currency cost (nobody, or a streamer body, takes the seat) by more than 0.5 for the
> drops the page calls 0.0. And: the page either prints a number for K and D/ST or prints "not priced".

**CONTROL.** The ladder recomputed from `sheet_engine.py` reproduces tonight's page to the tenth for all
fifteen rows (Chiefs -2.0 ... Nacua 114.0).

**(a) THE 0.0 ROWS ARE 0.0 UNDER EVERY COUNTERFACTUAL.** Brooks, Vele and Washington never enter the nine,
so nobody-replaces (doc 240), best-free-body (the page), streamer-replaces and next-best-after-the-add all
give 0.0. **The falsifier does not fire on the rows the prompt named.** Where the counterfactual does
bind it is large: LaPorta 26.6 on the page against 37.0 with a streamer in the seat and 114.4 with nobody;
Chiefs D/ST -2.0 against -6.5. **The page's number assumes a second transaction at that position that the
add in question does not make.** Drop Vele for Schultz and nobody at receiver is added; the ladder has
priced the drop as if Shaheed were.

**(b) THE DOUBLE COUNT, ON TONIGHT'S PAGE.** The add row prices a man against the bar; the drop row nets
the victim against the best free body, who may be the same man. Add Browns D/ST (+8.5) and drop Chiefs
D/ST (-2.0): a reader nets +10.5; `season()` says the swap is worth +2.0. Add Trey Smack (+8.5) and drop
Pineiro (8.4): reader +0.1, actual -8.4. Skill positions: add Henry, drop LaPorta reads -19.4 against an
actual -20.8; add Shough, drop Hurts reads -36.9 against -46.1. **The one number that is right for a swap
is doc 327's matrix cell, and it is not on the page.** `[TESTED, deterministic, byes only]`

**(c) K AND D/ST ARE PRICED, AND THE COMMENT SAYS THEY ARE NOT.** `sheet_engine.py` line 1550: *"K and
D/ST carry no free rows on this wire (4.8/4.9 keep them off it), so they are NOT priced rather than priced
wrong."* `freerows` is ESPN's available list, which carries both; the page prints Pineiro "replaced by Trey
Smack at 8.5, costs 8.4" and Chiefs D/ST "replaced by Browns D/ST at 6.1, costs -2.0". The kicker is a
projection gap times fourteen weeks with no absence term (the constants carry no kicker rate, doc 302),
which section 4.8 says is not a realisable value; the defence prints a negative cost, which reads as a
gain and is the same object as the +8.5 fill above it. **Priced, and priced wrong.**

**(d) DOC 316's FIVE-ROW CAP.** `sheet_engine_20260916_0300.py` lines 1216-1230 keep five and re-admit any
row below the cut whose contest sentence says put him first. `sheet_engine_20260916_0805.py` and every
version since, including the shipping 115,530 bytes, read `picks = ''.join(_mv(m, i + 1) for i, m in
enumerate(now[:5]))`. The to-do entry marks it DONE. The 08:05 `sheet_engine.py` is doc 321's own restore session, built on a
base older than 03:00: the trap of ledger row 59 one file over, and no control covered the rule. `Scripts\research\rt344\rt2_ladder.py`.

### Item 3. Is the printed second figure a floor?

> For at least one free player, `tot - len(empty) * min(his rate, streamer)` exceeds the paired simulation's
> arm C by more than two standard errors.

Run on the page's own free pool (every priced man on nobody's roster, 297 men, D/ST included), 1,500
paired draws, control arm A reproducing `price()` to 0.05. **One row exceeds arm C, and it is the row the
page prints tonight: Browns D/ST, printed 2.5, arm C 1.99, unrounded arithmetic 1.99.** The excess is
the page's tenth-rounding: the Chiefs' 5.948 becomes a bar of 5.9, the Browns' 6.104 minus that becomes
0.2 a week instead of 0.156, and twelve weeks of it is +0.5. The headline 8.5 is 8.0 for the same reason.
At QB, RB, WR and TE no row exceeds arm C (the candidate's own drawn absence more than pays for the
rounding). Against the one-currency arm U (a streamer body always in the pool, doc 327), the same Browns
row is 1.48, because the Chiefs at 5.95 sit under the 5.99 streamer in all thirteen weeks and the
deterministic figure credits the gap to the candidate. **"Floor" is false by 0.5 on the printed row and
the cause is rounding, not the absence model. Bound the rounding at +-0.05 a week, so +-0.65 a season,
and say "about".** `Scripts\research\rt344\rt3_floor.py`, `RT3_floor_vs_sim.csv`.

### Item 4. Comparisons made, and what survives

**Doc 314:** four correlations (touches, points, two partials), one permutation p on the pre-named
predictor, one pre-registered falsifier (need adds 0.30), three leave-one-season-out errors, and two
descriptive tables. **p=0.00005 on touches survives any correction on offer** (times 48 for every
correlation, season and position cut it ever reports is 0.0024). The band cut points 5 / 10 / 15 were
chosen after seeing the data; the table is descriptive and the page uses it as such.

**Doc 320 (Fable, mine):** one pre-registered primary (carries plus targets to date vs the week-1 chart,
McNemar), four alternative predictors, step and no-step for each, two subgroups, four week bands, five
seasons. **The primary was fixed before the run and stands alone at p=0.043; treated as one of five
predictors it is 0.22.** What carries the rule is the settled-backfield cell, +16.2 points at p=0.001,
which survives a two-subgroup correction, and the shipped instruction (switch from the week-3 sheet,
nothing moves this week) rests on the week-2 tie, not on the 0.043. **Fragile as a headline, sound as
a rule.**

**Doc 315** reports no new test (its p-values are sections 4.26b and 4.25b restated). **Doc 318** ran two
regressions on one hypothesis and reports both, the first as the wrong object; the surviving null
(r=-0.069, p=0.573, n=71) needs no correction. **Doc 319** claims no inference. **Doc 321** has none.

### Item 5. The constants: `contest` reproduced exactly, the seat constants only roughly

**Every number in the `contest` block reproduces from `Scripts\research\rival_need.py` on the files in
`Source\`:** r 0.296, p 0.00005, n 403, the four bands with n 88 / 180 / 94 / 41, filers 1.17 / 1.49 /
1.83 / 2.27, contested 0.14 / 0.29 / 0.40 / 0.56, the 2.03 / 1.90 / 1.62 cell, need +0.201 against the
0.30 bar, MAE 0.716 against 0.693, the 56-and-18 sit-time count, r_points 0.233, the two partials 0.231
and 0.137, and the 0.098 line. `rival_need_bands.json` was regenerated at 20:51 tonight and matches.
**The population mismatch is the one item 1 found: the constants say "2022-2025 grouped by (week,
player)" and the rows run to week 18; the page runs in weeks 1-14.**

**`relief_ppg` 12.13 (n=51) and `weeks_played` 3.02 come from doc 276 section 4 and no script in the tree
computes them** (`build_inherit.py` carries 11.2 as a label, `a1_injury_sim.py` uses 11.2, `job_opens.py`
takes 3.02 as an input). Re-derived from the stated population (weeks-1-4 RB usage leader misses a
team game in weeks 5-14; the second back by the same usage has a line in those weeks; nflverse
2022-2025): **n=50, per-event mean 12.97, median 12.07, pooled per-game 11.76; the starter is out 3.08
weeks and the backup plays 2.82 of them.** Doc 276's 12.13 / 3.3 / 3.0 sit inside that spread and cannot
be pinned to a definition. `[REPRODUCED TO ABOUT 10 PER CENT; the exact figures are SOURCED to doc 276
with no script]`. Two things the population does not match on the page: the rate is measured on the man
who actually got the work, and the page applies it to the man `inherit_2026.csv` names before the
absence, who is passed over in about a third of events (doc 320: chart 62 per cent, usage 72 per cent),
so the seat rate should carry a P(he is the man) that the odds column does not; and the page multiplies
a per-event mean by a mean duration, where the pooled per-game figure (11.76) is the one that multiplies.
Section B's JOB 2 is the right place for the first; the second is a 10 per cent overstatement of a lane
worth two points. Doc 318 quotes 12.13 against an n=71, 2021-2025 population whose own table means 12.05.

### Item 6. The code and the controls

**THE NEXT INPUT THE HARNESS DOES NOT SUPPLY IS `matt_todo.txt`.** `sheet_engine.py` reads it three times:
the to-do box (doc 342), the to-do page, and **`load_donot()`, the DO NOT rulings applied at selection**
(doc 295; tonight "DO NOT CLAIM BRENTON STRANGE" and "DO NOT IR-STASH TANK DELL"). The harness copies no
`matt_todo.txt`, so every control runs with the do-not lane switched off and the to-do lane withheld, and
a regression in either passes 56 of 56. Next after it: `waiver_report_2026.csv`, read by the sheet and not
copied; and `LEAGUE_ROSTERS.csv`, written by `wire.py` on a live run and absent in the mock.

**THE NEXT CHANGES WITH NO CONTROL:** the drop ladder (no check names "if you drop him" in any harness
version), doc 316's cap rule (lost without a check firing), doc 343's per-band odds (the doc says 17
controls ran; none is in the tree, and `ctl_307.py` is the only control file beside the harness), and doc
342's twelve to-do controls (same). A control that ran once in a container and was not shipped is a
control Matt cannot re-run, which is section 0.4 in the other direction.

**THE HARNESS ITSELF WAS THE FIRST FINDING (section 0, item 1).** Its version history on the drive:
16 Sept 08:05, 20,159 bytes, 44 checks; 16 Sept 19:15, 29,356 bytes, 56 checks with `form_2026.csv`
already on the copy list; 17 Sept 21:30, the 08:05 bytes again, hash-identical, then plus one line.
What sat on the drive between 19:15 and 21:30 the next day is not archived; a re-commit from a container
path that first held the 08:05 bytes is the row-89 mechanism and fits. Ledger rows 85 and 86 then
diagnosed the reverted file and re-did doc 321's fix on it. `check_kit.py`'s doc-330 comment cites C22 and C22c at
65 of 65; no archive holds that version and the drive never did. Restored the 56-check file; the
65-check one is gone.

**Row 89's control, reproduced and bracketed.** Eight throwaway files in `_archive\_rt_probe*.txt`:
same path re-committed 11 seconds after the first commit, 26 bytes and 35 KB, `force` on: old bytes,
mtime advanced, `written` returned (probes 1, 3). Same at 45 seconds and at 2 minutes 30 (probes 7, 8).
Fresh at 4 minutes 35 with nothing in between (probe 6). Fresh at 30 seconds after a `device_stage_files`
of the destination (probe 5). **So: keyed on the container path, refreshed by a stage of the destination
or by roughly three to four minutes.** The ledger's own rule (a fresh path every commit, verify by content)
is sufficient and was used for everything written tonight.

**ONE MORE ARTIFACT CHECK (0.5d):** `WEEK_SHEET.html` on the drive at 22:14 prints 46 per cent on every
seat and no week-one share; row 87's page column says FIXED. The to-do entry says the next `py wire.py
--html` picks it up, which is right; the ledger column is a claim about code until then.

### Item 7. References that point at nothing

Every `doc N` citation in `Source\*.md`, `matt_todo.txt`, the ledger and `Scripts\*.py`, checked against
the drive, the project store and `_archive`:

| cited | where | exists |
|---|---|---|
| doc 60 | directive 4.12 header, directive section 8 | no. The noise recalibration is doc 53 |
| doc 102 | `depth_map.py` line 9 (its own provenance), `check_kit.py` | no |
| doc 108 | `check_kit.py` | no |
| doc 169 | `00_START_HERE.md`, `check_kit.py` twice | no |
| doc 311 | ledger rows 79 and 80, `wire.py`, `OPEN_THREADS.md`, `check_kit.py` | no |
| doc 316 | docs 320, 321, `matt_todo.txt`, `check_kit.py`, `wire.py` | no; content is the 16 Sept to-do entry |
| doc 317 | docs 319, 325, the tasking prompt, `check_kit.py`, `sheet_engine.py` line 1536 | no |

Files: `manager_identity_map.csv` (directive 4.19, "teams resolved through") and `draft_analysis.json`
(directive 4.29) are on no listing of `Source\`, `Scripts\`, `Scripts\live_draft\`, `Scripts\research\`
or `_archive\`. `REDTEAM_REPLY_302.md`, answered by doc 303, is not on the drive or in the store. Also
noted, not phantoms: two files carry number 193 (`193_the_red_zone_test.md` on the drive,
`claude/193_weekend_injury_sweep.md` in the store), and 94, 150, 293 and 326 each have two files.

---

## 2. FILES

**Restored:** `Scripts\research\redteam\redteam_controls.py` 20,578 -> 29,356 (the 16 Sept 19:15 file,
verified on the drive by content: seven C20/C21 checks present). Archived first as
`_archive\redteam_controls_20260917_2245.py`. `check_kit.py` does not pin this file (doc 321 section 5,
still open), so no pin moved.
**Not touched:** `sheet_engine.py`, `wire.py`, `sheet_constants.json`. The cap rule (2b) is eleven lines;
the archive at 03:00 has them; restore them into the file the other session is holding, not from here.
**New:** `Scripts\research\rt344\` -- `rt1_zero_filers.py`, `rt2_ladder.py`, `rt3_floor.py`, `rt5_relief.py`,
their run logs and CSVs. Stdlib plus numpy and the production `sheet_engine`.
**Ledger:** rows 90 to 96, one per finding above. **Probes:** eight `_archive\_rt_probe*.txt`, 26 to 35,017
bytes, deletable.

---

## 3. OPEN

- **NOT YET RUN:** the contest sentence re-cut on the claimant's-seat rate (item 1), which is a one-line
  change to `contest()`'s 0.38 threshold and a constants entry; it needs the exchangeability assumption
  stated on the page or tested on Matt's own 88 adds against the field's.
- **NOT YET RUN:** doc 316's cap rule restored to `sheet_engine.py` and a control for it (plant a
  15-touch man at sixth on worth; assert he prints).
- **NOT YET RUN:** `matt_todo.txt` on the harness copy list with a planted DO NOT line and a check that the
  named man is off the priority list; `waiver_report_2026.csv` likewise.
- **NOT YET RUN:** the seat rate as a per-game pooled figure times P(he is the man), which is section B's
  JOB 2 with one more term.
- **BLOCKED, input named:** the exact 12.13 and 3.02. The script that produced them is not in the tree;
  doc 276 names none. Whoever has it should commit it to `Scripts\research\`.
- **[OPEN]** the 65-check harness with C22/C22c (doc 330) exists in no archive; if it was only ever in a
  container it has to be rebuilt from doc 330's description.
