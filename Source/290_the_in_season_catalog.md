# 290 · The in-season catalog: 50 candidates, before any test

*10 Sept 2026, late evening ET. First deliverable under `Source\IN_SEASON_REDTEAM_HANDOFF.md` §4 step 1.
**Nothing in this file has been tested.** Every number quoted from a doc is `[INHERITED, doc N]` until its
batch re-derives it. The things checked directly on the files are listed in §6 and are the only
exceptions.*

**Revised 11 Sept, 8 am ET, after Matt's reply.** (1) Pat Bryant was an example for mining the room, not a
claim: nothing here prices him, and batch 1 no longer has a Tuesday clock. (2) A2 now states the scale problem
as one defect. (3) A4 is confirmed from ESPN. (4) New A15: Matt's do-not rule, starting with the Pearsall block.
(5) New family F: the three receiver indicators he asked for. (6) Batch 1 splits at Sunday's 11:45 rebuild, and
B3 moves to batch 2. Still nothing tested.

**Revised again 11 Sept, 8:30 am ET, after re-reading the handoff (now 33,344 bytes; §1-§8 match the copy read on
10 Sept, §9-§11 are new).** (1) New A16: guards shown firing on one path and trusted on the rest (charter §9(1));
it runs with A4. (2) New family G: testimony, meaning the quote ledger and the cards (charter §10). (3) Two
corrections to this catalog: F3's live trigger cannot be read from snap counts, which carry no alignment; and the
charter's §11(2)(c) restates Matt's alignment example with the alignments swapped (§2 item 7). (4) Matt's
tea-leaves read was tracked as MOSTLY NO on a stability table that never tested it; it is NOT YET RUN under G1.
(5) §4 carries the charter's post-compaction rules as standing steps. (6) D8 adds the scheduled prompts as a
fourth place a kill has to reach, and the kill ledger in §5 gets a fourth box. Still nothing tested.

**Revised again 11 Sept, 8:55 am ET, after Matt's three corrections to his reads file.** (1) New G2: whether a
coach cuts a player's role after a lost fumble or a multi-drop game, in Matt's testable form, with a matched
control and an injury screen added; drops are not blocked for 2022-2025, because nflverse carries FTN's
play-by-play charting with a drop flag (checked, §6). The cards become G3, and family G is now "the coach: what he
says and what he does". (2) New D9: preferences carry reopening conditions, but nothing watches them, and the one
with a number is priced on the engine that cannot see injuries. (3) The upside retraction joins D2 (the directive
quotes the old line as a confirmed read of his in two places), and B6 also tests his reason: potential against the
projection on the same rows. Still nothing tested.

**Revised again 11 Sept, 10:15 am ET, after Matt's reply; batch 1 started early on his word ("if you have something
left to run, then run it").** (1) New E4: the edge is lead time. After a team shock (an injury, a benching for poor
play, other changes), which indicators name the beneficiary before a rival in this league claims him. Matt conceded
"nothing" was too strong: the projection may already carry potential and role, so B6's added comparison now asks
what the composite adds to the projection. (2) D9's proposed limit is dropped at his instruction: nothing of his is
exempt from challenge, scope calls included, science view first. (3) The upside line is out of the directive
(v9.4) along with the six body retractions in D2, which is partly closed; `Source\AUDIT_LEDGER.md` is open. (4) G2's
injury screen has its data and a first count (§6, checks 23 and 24).

**Revised again 11 Sept, 12:30 pm ET: batch 1's first half has landed (doc 291).** A4, A16, A15, A2, A6 and D1-D3
are done and on the drive, with A10's week source and two bye-plan defects fixed because those sections could not
render without them. 33 negative controls in `Scripts\research\redteam\redteam_controls.py`; the pre-291 code
passes 9 of them. D7 is closed. Three silent id joins remain from the A16 sweep (A5, A11, batch 3). **A1 moves to
the front of the second half**, because on the corrected scale a zero-cost bench body looks droppable and some of
them are insurance (doc 291 §5). The first live run of the new code is Matt's by-hand run or Sunday 11:40 am.

**Revised again 11 Sept, 1:30 pm ET, after Matt's reply on performance metrics, the stash and pedigree (doc 292).**
Three new items, so 53. (1) A9 gains the clear path, TESTED: the backup's share of his team's backup RB snaps
predicts what he does in the first game the lead back misses. (2) New A17: six gates in the page code hide risers,
counted; the fix is ranking terms plus a pedigree-blind usage lane. One piece landed early, because Thursday 17 Sept
is the first waiver run with usage in it: `FREE_UNRANKED_<date>.csv` from `wire.py`, and a latent whole-run crash on a
missing ownership number fixed with it; controls C16, 39 of 39. (3) New
B11: performance metrics beyond the projection; most do not repeat at a backup's volume, the added value is
UNDERPOWERED, separation and win rate are BLOCKED for backups. (4) E4 gains the usage lane as the baseline every
indicator has to beat, and no indicator may be gated on pedigree. (5) New E5: stash shapes beyond the handcuff.
(6) `AUDIT_LEDGER.md` row 19: section 4.6's after-contact line, retracted by doc 190 on 6 Sept, never left the directive.

**Revised again 11 Sept, 2:30 pm ET (stamp corrected by doc 294; it first read 4 pm), after Matt asked for Chuba Hubbard and other late picks to be researched (doc 293).**
New E6, so 54. Its first batch (R1) landed: late picks need a door (38% of their rises came through an absence ahead of
them against 22% for early picks; 55% against 32% at running back), and three signals (last-two-games snap share,
points per snap, a light special-teams load) stack so that a late pick with all three takes the role 36% of the time,
level with an early pick's 38%. No signal reads measurably more clearly for late picks. The Tuesday read's prompt
gains the three-signal count; R2c (does a late pick keep the role when the man ahead returns) is next, in batch 2.

**Revised again 11 Sept, 4:45 pm ET: E6's R2c ran early, on Matt's standing instruction (doc 294).** (1) Directive
4.27 (doc 244) was rebuilt first, because its script was never committed: its replacement is the designated backup
(the number two by weeks 1-4 usage, over weeks 1-14), its central result reproduces, and it replicates on 2015-2020
(+14.0, p=0.001). Two of its sentences do not survive: "a back who does not produce LOSES ground" is mostly backups who
never got the work, and "a short absence is more dangerous" does not replicate (`AUDIT_LEDGER.md` rows 20 and 21).
(2) R2c is UNRESOLVED: over the full season late picks who produced keep the same share as early picks (+12.1 against
+11.6), inside our season 3 to 13 points less on seven or eight early-pick events; late picks are less often startable
afterward (8 of 39 against 5 of 11). (3) SUGGESTIVE and found after looking: a producer out-used a returning late-pick
starter 7 of 10 times and a returning round 1-3 starter 4 of 26 (starter back by week 14, p=0.003); the fixed re-test
is 2026's own returns. (4) A9 gains a count: the designated backup got the work in 57 of 88 first absences. (5) Doc
293's stamp is corrected to 2:30 pm. The Tuesday read's prompt gains the return.

**Legend.** OBSERVED = seen in a file tonight (code, page, data or doc); it still needs its test before any
number moves. SUSPECTED = inferred from reading; the test decides. "Code sweep" = read by a helper pass over
the scripts and not yet re-checked by me line by line.
**Kind:** `guard` a step that reports success while doing nothing · `retraction` a kill that did not reach
code, page or directive · `object` right arithmetic on the wrong object · `population` population drift or
selection on the outcome · `small-n` small sample or a result picked after looking · `units` scale mismatch ·
`frame` something the model leaves out entirely.
**Size:** S under an hour · M a few hours · L a day or more.

---

## 1. The shape in one paragraph

The charter's nine are real, and most of them sit inside a larger frame the charter did not name. **The engine
behind both pages Matt reads models a season with bye weeks and no injuries (A1), puts players on a different
scale from everything they are measured against (A2), and runs on a preseason projection pulled 7 September that
nothing refreshes (A3).** Those three explain most of the 0.0s on the sheet, including a drop cost of 0.0 for a
backup tight end whose starter played 9 games last season. The second frame is the record: retractions reach the
docs but not the code, the rendered page or the directive (D1-D3), and the charter itself carries one (D3). The charter's later sections add two narrower
ones: guards shown to fire on one path and trusted on the rest (A16), and a testimony ledger whose outcome input
does not measure what its test names (G1).

## 2. Where I disagree with the charter before testing anything

1. **§6(2) aims at a gate that is already gone.** Docs 275-276 removed the 11.2 production gate;
   `build_inherit.py:53` keeps 11.2 as a label only. The live defect is prose: directive §4.27 still gives both
   gates as "the applied form", and doc 281 describes 11.2 as "the rate at which a fill-in back kept the job"
   (it is the median of scoring *during* the absence, doc 244). The proposed 6-to-16 sweep is on the wrong
   variable, and doc 275 already swept the right one (rho +0.006, n=39).
2. **§6(1)'s deflation mixes units.** §4.23's ratios are season totals over season totals, and §4.23(b) says the
   gradient tracks games played; multiplying a per-game bar by them charges missed games twice. Its proposed
   test also conditions on "players who actually occupied a starting slot", which selects on the outcome. And
   the live page's bar is Matt's own lineup, not 20.09 / 9.92 / 9.62 / 8.25; those define the *research* hit
   rates. Re-aimed as B1.
3. **§7's "cleanest measurement" is the highest of six week bands.** Week 2's 34.6% is the top band; the contrast
   fixed in advance would be week 1 against every other week: 9.4% against 23.6%, p=0.083 on doc 252's own
   numbers, meaning a gap that size would show up about 1 time in 12 even if week 1 were no different. Screened
   receivers show no week effect at all (doc 276). B3.
   **What the timing rested on, stated plainly (Matt asked):** the first version of this catalog gave batch 1 a
   "before Tuesday's claims" deadline because the to-do list placed Bryant at week 2, and the to-do placed him
   there because of this same week-1 rule. The deadline was borrowed from the thing being doubted. Bryant is not a
   move, so nothing in batch 1 has a Tuesday clock. The only real clock is the Sunday 11:45 am rebuild, which
   republishes whatever the code says. On claim timing itself, nothing measured says wait for week 2; the only
   reason is that a week-1 claim is made before any snap counts exist, and that is a judgement, not a number.
4. **§7's "the wire cannot upgrade a working slot" is true by construction** in a model where a working slot only
   breaks on a bye (A1). It is a statement about the model before it is one about the wire.
5. **§4 step 4's next free number is stale.** Doc 289 was written after the charter, so this is 290.
6. **Doc 288 §6's kill path is still open.** One recommendation in §5.
7. **§11(2)(c) swaps the alignments in Matt's example.** His words: "If Waddle takes the slot and Bryant is on the
   boundary, then Sutton going down is my event." The charter's: "If Waddle takes the boundary and Bryant is the
   slot, then Sutton going down is Matt's event." With Bryant in the slot, a one-step alignment reading makes the
   slot man's absence his event, not Sutton's (82% wide last season); Sutton's absence reaches him only through a
   chain, a hybrid like Franklin (55% wide) sliding outside. The trigger follows the configuration, so F3 quotes
   Matt's words and names no trigger until Denver's 2026 alignment is actually read.
8. **§10 is right in kind, and three of its reasons need work (G1).** (a) The intake filter logs "a rep, snap or
   route count" and justifies itself with a stability table that puts route rate at 0.01, its very bottom. How much
   a stat repeats between seasons is not whether a sentence about it comes true; the line that holds is a usage
   decision the speaker controls against a skill outcome nobody controls, and the ledger is the test of it.
   (b) §10(3)'s outcome is route share, and the queued puller reads nflverse snap counts, which carry snaps and snap
   share only (checked, §6); at tight end, snaps and routes are different objects. (c) §10(4)'s "a quote is worth
   more the less a player is used and owned" and §10(5)'s "measured warning" rest on a preseason price test and a
   team pass-rate test; neither measured a quote. Both are sensible defaults, carried here as hypotheses.

---

## 3. The catalog

### A · The pricing engine: what the two pages compute every week

**A1 · No injuries anywhere in the pricing** · OBSERVED · frame · M · *used by: every drop cost and "worth now" on the sheet* · *first in batch 1's second half: A2 exposed it (doc 291 §5)*
Where: `sheet_engine.week_points` removes a player only when `bye == week`. The bar, "what he adds", the drop
cost, the bet value and the wire's bye table all run through it, and the page footer says so. §4.18c deferred an
absence model to "post-draft"; it was never built.
Test: Matt's 15, weeks 1-14; each player's weekly availability drawn from measured absence rates for his
position and role (nflverse weekly lines 2021-2025 re-derived, or §4.17b's 2.98 QB weeks and 5.54 RB
slot-weeks declared `[INHERITED, doc 111]`); outcome the 14-week best-nine total with and without each cheapest
body. Direction: drop costs rise for depth behind starters who miss time. Report whether the cheapest-drop order
or the "take the ticket" verdict changes.

**A2 · One scale defect: players on season ÷ 14, everything they are measured against per game** · OBSERVED · units · S · *used by: the bet, the seat, the D/ST and K rows* · **LANDED 11 Sept, doc 291**
Where: the page puts every player on his 17-game season projection divided by 14 (`sheet_engine.py:720`,
`wire.py:532`). The startable bar is the same season projections divided by 17, exactly, at all four positions
(the charter's measurement), and every measured rate the page compares players with is per game: the bet's 12.71
hit, the seat's 12.13 relief rate, the D/ST 5.99 replacement, the kicker gap. **One quantity on two scales is one
defect, with one fix: put the page on per game.** Comparisons between two projected players do not change,
because both sides move together; the defect bites only where a projection meets a per-game number. Earlier docs
used 17, 16 and 14 as the divisor for the same thing (226, 233, 234, 240).
Test: rebuild the bar grid per game; re-price the bet, the seat, and the D/ST and K rows. Direction: the WR bar
falls from 14.2 toward 11.7, under the 12.71 hit rate, so the bet and the seat both rise. Report every verdict
that flips.

**A3 · A preseason projection runs the whole season** · OBSERVED · frame · S, plus one command from Matt · *live: every row from week 2*
Where: `rates()` reads the newest `espn_projections_2026_*.csv` (7 Sept 12:58); `ff.bat` never refreshes it; the
page does not print its date. Injury tags come from the same file (LaPorta still QUESTIONABLE on the sheet after
he was cleared).
Test: after a fresh pull, count starters whose weekly rate moves more than 10% and bar-grid verdicts that change.
Needs his ESPN session, so it goes on `matt_todo.txt` when batch 3 starts, not before.

**A4 · Washington does not exist on the sheet** · CONFIRMED (Matt, on ESPN, 11 Sept) · guard · S · **LANDED 11 Sept, doc 291** (cost on the 10 Sept pool: nothing shown; the Commanders defence never enters)
Where: the pull codes Washington `WSH`, `byes_2026.csv` codes it `WAS`; `rates()` silently drops every Washington
player with a projection: 17 rows, among them the Commanders D/ST and kicker Drew Stevens (checked, §6), plus 2
`FA` rows. The wire page has the mirror image (`WAS`/`WSH`, `LA`/`LAR`) in the December tight-end draw, the
defence run and the look-ahead (code sweep). The charter's §9(1) explains why no guard fired: the team-code assert
added to `wire.py` on 10 Sept checks the 32 codes read from `team_shape_2025.csv`, never the code on a player row.
Both readings are diagnoses until reproduced, and the code is re-read before any fix (§4).
**Matt's note, and it sets the priority:** defence is the one position where this project measures a real
matchup edge, so an invisible D/ST is a live cost, not cosmetic. The fix measures that cost instead of asserting
it: with Washington restored, does the Commanders defence enter any of Matt's defence weeks (week 11 is empty) or
the free-defence rankings in any week.
Test: count rows lost per team at each join; negative control with one code renamed; after the fix, every
Washington row with a projection is on the sheet by name.

**A5 · Two pricing universes on two pages** · OBSERVED · object · S
Where: the wire prices from the draft board (keepers removed, no K or D/ST); the sheet from the projection pull.
Matt's own keeper Pickens is "not on our board", so the wire's bye table has no week 14 and counts no D/ST or K.
The same Green Bay job is 241 on the wire (`depth_map.csv`) and 152.5 on the sheet (Jacobs in the 7 Sept pull).
The wire's "71 not on our board" list includes Tyreek Hill, Aiyuk, Mixon and Chubb.
Test: diff both universes on the 10 Sept pool; list every row and number that disagrees.

**A6 · The pages Matt reads are older than the code** · OBSERVED · retraction · S · **LANDED 11 Sept, doc 291** (code stamp on both pages; the drive pages rebuild at the next run)
Where: both pages built 10 Sept 17:50; the tight-end sort fix, the room column, the card rewrites and the
stale-card marker landed between 18:03 and 19:33. The rendered TE table still leads with Strange; Bryant's card
still says "a third receiver in Denver has to survive two people getting hurt". The Sunday scheduled runs will
publish the newer code before any of it is audited.
Test: rebuild both pages offline from the staged inputs and list every sentence that changes; stamp the code
version on the page.

**A7 · "PAGE OK" means only that a file exists** · OBSERVED · guard · S
Where: `ff.bat:42-44` (`if exist`); `wire.py` catches a sheet failure and leaves yesterday's page with no banner;
`fail_page` swallows its own exception (code sweep).
Test: force a sheet failure; the log and the page must both say so.

**A8 · "In doubt this week" picks the wrong man** · OBSERVED · population · S
Where: `wire.py:604-646` triggers on any rostered back with a status at any depth, prints the lead back's job and
takes the shallowest free man below. Rendered example: "Jacob Saylors, because Isiah Pacheco is Injury Reserve,
job pays 331". Pacheco is Detroit's backup (`inherit_2026.csv`), and 331 is Gibbs's job.
Test: re-derive the 7 rendered rows from the depth chart and statuses; count rows where the hurt man is not the
starter or the pick is not the direct backup.

**A9 · The seat and bet constants are one number for every team, and "the backup" is known only afterwards** · SUSPECTED · population · M
Where: `sheet_constants.json`: p(job opens) 0.46, relief 12.13 a game for 3.02 weeks, hit 12.71 for 6.4 weeks.
The relief population takes whoever got the work; Matt can only claim the depth-chart backup before the injury
(Jordan James against Kaelon Black is the live case).
Test: NFL 2022-2025 lead-back absences, weeks 5-14; backup = the week-1 depth-chart number two; outcome his
half-PPR per game in those weeks; compare with 12.13 and report how often he was the man who got the work.
**Clear path, TESTED 11 Sept (doc 292, T5), Matt's term:** *"a clear path to the next man up soaking up enough of that
volume."* 154 first games of a lead-back absence, 2019-2025: the number two's share of the backup RB snaps before it,
under 50% → 25.0% scored at the RB bar, 50-70% → 31.6%, 70-85% → 45.7%, 85%+ → 64.7% (median 15.5, led the room 88%);
70%+ against under 55.1% vs 29.4%, p=0.0017; same direction on 2019-2021 alone (p=0.10). **The remaining A9 test
should use this measure, not only the depth chart,** and run over the whole absence, not the first game.
**Doc 294 (usage version, first absences 2015-2025):** the designated backup, the number two by weeks 1-4 usage, got
the most work in 57 of 88 (65%), late and early picks alike; passed over, his share fell 7.0 points after the return.

**A10 · The defence run did not render on Thursday, and ranks the weaker model when it does** · OBSERVED · guard · S · *week source fixed early and a bye inside a run now ranks below runs without one (doc 291); the model comparison stays in batch 3*
Where: the page says "the week is unknown" (`wire.py:449`; per the code sweep the week is read from the
player-pool payload, while `lineup.py` got week 1 from rosters). `dst_runs` ranks raw 2025 opponent scoring over
four weeks; the project's own slate model shrinks it (0.325) and adds unit form (0.269), and doc 230's own
(unresolved) table has four-week windows as the weakest.
Test: check the week source on a stored payload; rank weeks 2-5 by both models; report disagreements.

**A11 · The tight-end sort key was changed on a claim its own doc marks open** · OBSERVED · object · M · *live: the week-5 Waller or Barner call*
Where: `wire.py:793-794` sorts free tight ends by 2025 inside-ten targets a game (doc 282), and doc 282 marks
"role vs projection as the ordering" `[OPEN]`. The stickiness behind it (r=+0.59) was 37 players with 10+
red-zone targets in both years, not low-volume free tight ends; a measured zero ties with a missing row.
Test: tight ends 2022-2025 with a preseason projection; outcome weeks 1-14 half-PPR per game; rank correlation of
prior-season inside-ten targets a game against the preseason projection, and both together. Direction: the
projection wins alone.

**A12 · IR slots count as roster seats** · OBSERVED (latent) · guard · S
Where: `wire.py:1162` passes `seats_used=len(mine)`, and `mine` takes every roster entry, IR slot included. Doc
281's phantom seat, pointed the other way.
Test: a roster fixture with one IR entry.

**A13 · Only the 400 most-owned free players exist** · OBSERVED · guard · S
Where: `wire.py:983` (`limit 400`, sorted by ownership). A week-1 breakout owned under the cut is invisible to
every table on both pages.
Test: after week 1, count free players above Matt's bar who sit outside the 400.

**A14 · "Who else is short" is counted off draft-day rosters** · OBSERVED · population · S, needs the 2026 transaction pull
Where: section 4 of the sheet says so; term 4 of the claim calculation uses it; `waivers.py --live` has never run.
Test: rebuild from the 2026 transactions once pulled.

**A15 · A do-not line earns space only when the sheet is the only place that information exists** (Matt's rule, 11 Sept) · OBSERVED · object · S · **LANDED 11 Sept, doc 291**
His words: "Anything ESPN already tells me does not belong there." Pearsall has been on his do-not list four
times, and ESPN shows his status the moment he looks at him.
Where: the week sheet's "On the wire with a signal, and NOT priced above" block and Pearsall's DO NOT CLAIM card;
the "NO LONGER FREE" markers on cards for players another team has rostered (ESPN shows that too); and the
to-do list's Pearsall line (removed 11 Sept). Care point: that block is also doc 277's missing-row guard, and
the guard is still needed for a player dropped for a reason ESPN cannot show (a team-code mismatch like A4, or a
blank projection on a healthy player).
Test: suppress any do-not or no-longer-free row whose reason ESPN already displays (OUT or IR status, rostered
elsewhere); keep the guard for everything else. Negative controls: Pearsall gone; a healthy screened player with a
blank projection still printed; a rostered carded player gone. Then sweep every do-not line on both pages and
the to-do list against "does ESPN show this".

**A16 · Guards shown firing on one path and trusted on the rest** (charter §9(1)) · CONFIRMED · guard · S · **LANDED 11 Sept, doc 291** (15 inputs swept; `pedigree_2026.csv`, `redzone_te_2025.csv` and `depth_map.csv` id joins still silent, carried to A5, A11 and batch 3)
Where: by the charter's account the `wire.py` team-code assert was shown firing on `ARZ` and then called done,
while Washington rows fell out through a path it never sees (A4). The charter asks for the same check on every
assert added in the four days before 11 Sept, and nothing has listed them. Dated copies of the scripts sit in
`_archive\` (`wire_20260910*.py`, `sheet_engine_20260910.py`, `depth_map_20260910.py`) to diff against.
Test: list every assert, refusal and forced exit added to in-scope scripts from 7 to 10 Sept, with the input each
was shown firing on; then feed one bad row down every other path that reaches either page and record whether it
fires. Report each guard that stays silent on a path, and the rows that path can lose.

**A17 · Six gates in the page code hide risers** (Matt, 11 Sept: *"We don't want rules that create blind spots"*) · OBSERVED, counted · population · M · *one piece LANDED 11 Sept, doc 292: `FREE_UNRANKED_<date>.csv`, the missing-ownership crash, controls C16*
Where (doc 292 §1): the 400 most-owned pool (the cut falls inside the 0.0% block; A13); every lane priced only off
the draft board (71 free skill players named on the page, first 30 shown); lane 3 receivers-only, drafted-only, three
of three needs NFL round 3 or earlier (14 screened players on the whole board); lane 2 RBs only, the 8 Aug depth
chart's number two, `free` read from the board-only WIRE file (latent: 0 of 32 next men off the board today);
`rates()` pricing only a positive 7 Sept projection (199 skill rows at or below zero; A3); the bet's two archetypes.
What the gates cost, measured (doc 292 §2-3): 2019-2025, a rounds 1-3 gate discards 53% of 355 mid-season risers;
undrafted players were 60 of them, more than the first round's 44; once a team uses a player (35%+ of snaps before
his first starter-level week) undrafted converts 17.8% against drafted 22.2%, p=0.37; the emergency spike is the
exception, 5.5% against 14.8%, p=0.031.
Fix direction: every gate becomes a ranking term; one pedigree-blind usage lane across RB, WR and TE (snaps and
points first, rotation players at the snap line next, spikes last with pedigree as the tiebreak); lane 2 reads the
clear path from 2026 snap counts, not the August chart.
Test before the page changes: the lane's weekly names on 2026 data against the four-season rates, and the page's
required rows by name after the rebuild. Runs in batch 3 with A13 and A5, after batch 1's rebuild verifies.

### B · The research bars and populations under the rules

**B1 · The startable bar is labelled "measured" and is a projection** (charter §6(1), re-aimed; its unit half is now A2) · OBSERVED · object · M
Where: 20.09 / 9.92 / 9.62 / 8.25 are §4.1 divided by 17, called "measured" in §4.19, §4.31 and on the sheet.
They define every hit rate the rules quote: week 1's 9.4%, the screen's 33%, the rookie's 40%, the stash-lane
table, the handcuff's "startable". Whether a projected replacement rate matches what replacement players actually
score per game has never been checked.
Test: all QB/RB/WR/TE weekly lines 2021-2025, weeks 1-14, §2 scoring; realized QB12 / TE12 / RB30 / WR30 by
points per game among players with 8+ games (no starting-slot condition); plus per-game realized over per-game
projected on the 2022 and 2024 pulls. Direction open. Then re-score the three live rates and report any
ordering that flips.

**B2 · Availability in the outcome season is used as a filter** · OBSERVED · population · M
Where: "4+ games next season" (docs 246, 248, 269, 287); "played at least one week afterwards" (276); "100+
routes both years" (284). A player who got hurt or lost the role leaves the denominator.
Test: rerun each headline with the filter removed, counting a vanished player as a miss; report the change.

**B3 · Week 1 against week 2 is the highest of six bands** (charter §7, challenged) · OBSERVED · small-n · M · *used by: the page's standing rule on week-1 claims; moved to batch 2*
Where: doc 252: 9.4% of 32 against 34.6% of 52 (Fisher p=0.010); week 1 against all other weeks is 9.4% against
23.6%, p=0.083. Doc 276: screened receivers 40% / 29% / 40% by week band (cells of 5, 14 and 5), no effect.
Test: executed QB/RB/WR/TE adds 2022-2025, weeks 1-14; outcome startable over the next four weeks under B1's bar;
permutation test of week 1 against every other week, with every band-against-rest contrast reported. Direction:
week 1 lower.

**B4 · The fragility null was measured on backs who were healthy at the start** · OBSERVED · population · M
Where: doc 276 (45.9% against 46.3%, n=115) counts only backs who led their team's usage in weeks 1-4 *of the
outcome season*, so a back hurt in September is out of the sample. It removed gate 1 and put "a starter who
missed time last season is no likelier to miss time" on the page, against §4.22(c)'s r=+0.50 games-to-games
recurrence on 1,806 pairs.
Test: every team's preseason lead back (depth chart or ADP, fixed before the season) 2022-2025; outcome games
missed weeks 1-14; predictor games missed the prior season as a dose; cluster by player. Direction: positive
recurrence.

**B5 · The room finding is selected on its outcome, clustered at the wrong level and one season old** (absorbs charter §6(3) and §6(4)) · OBSERVED · population · M · *used by: the wire's room column; F1 and F3 build on it*
Where: doc 284's "promotion" is moving up the target order, which is the outcome; it is clustered by team-season
though the trait persists by team (clustered p=0.064); `team_shape_2025.csv` is one season (persistence
r=+0.294) applied to 2026 rosters (Denver's 2025 room predates Waddle).
Test: promotion defined before the season (a teammate above him left or was lost before week 1); outcome change
in team target share; cluster by team; room from a 2022-2025 mean. Report which receivers'
room reading changes.

**B6 · The receiver composite has no holdout** · OBSERVED · small-n · M
Where: doc 248's three cutoffs are in-sample medians of the same 152 rows, and the three legs were chosen after
the single-signal results (the stronger round-1 and team-share signals were left out). It also carries Matt's
currency claim: potential value is the right currency at the bottom of the roster. He refined it on 11 Sept:
"Nothing is to strong of a word. The projection may be higher on those with more potential and a higher role on the
team." So the question is what the composite adds on top of the projection, and his real target is E4.
Test: leave one season out: pick cutoffs and legs on three seasons, score the fourth; report the out-of-sample
3-of-3 rate. Then, on the rows with a preseason projection for the outcome season (the 2022 and 2024 pulls),
measure what the composite adds to the projection against the same outcome, with B2's filter removed.

**B7 · 60% on 9 of 15, from a population the wire does not draw from** (charter §6(5)) · OBSERVED · population/small-n · S · *used by: Cooper's card*
Where: doc 251 (exact interval roughly 32% to 84%; its own table sums to 16). The first-rounders actually free
on the wire in-season are 0 for 6 (doc 276).
Test: state the interval at every use; re-price Cooper at its low end and at 0 for 6; report whether any call
changes.

**B8 · 14 of 141 replaced the 60% on a different population** (charter §6(6)) · OBSERVED · population · S
Where: doc 287 (drafted years 1-3, 4+ games in the outcome season) replaced a year-one first-rounder rate.
Test: report the cells; rerun under B2.

**B9 · The in-season screen is quoted with the wrong contrast and three different sizes** (charter §6(7)) · OBSERVED · small-n · S · *used by: the odds column on the week sheet*
Where: 8 of 24 against 4 of 48, but the p=0.028 compares against every other young receiver (about 13%); 36 of
the 108 adds sit in neither cell; doc 285 calls it n=152; the page prints 40 / 29 / 40 from cells of 5, 14 and 5.
Test: rebuild the 108 from the waiver reports; restate the cells, the right contrast and the missing 36.

**B10 · The stash-lane table multiplies two populations** · OBSERVED · population · M
Where: the wire's TE 4.0% / 19.6% (and the other rows) is Matt-only 2024-2025 access (pending claims counted as
losses) times league-wide 2022-2025 hit rates; "you lose five of six contested" is the same Matt-only rows; he
was 5th in the week-1 waiver order, not last (doc 238).
Test: league-wide 2022-2025 access by waiver position, pending rows excluded.

**B11 · Performance metrics beyond the projection, where circumstances change first** (Matt, 11 Sept: *"broken tackles, yards after contact, win rate, yards after catch, separation, and other performance metrics mater when determining potential value that likely lies outside of ESPN projections"*) · TESTED in part 11 Sept, doc 292 · object · M
Preseason form: TESTED NULL on 6 Sept (doc 190; seven measures, n=699, nothing under p=0.30).
In-season form (doc 292 §4, 2019-2025): (a) at a backup's volume most do not repeat, odd weeks against even weeks:
broken tackles a touch +0.21 (RB, 10-30 carries a half), yards a target +0.14 and broken tackles +0.15 (WR, 5-15
catches), against volume at +0.59 to +0.65; RB yards after contact a carry is the exception at +0.55. (b) Added to
usage at the first snap-line week: 16 splits, 10 lean his way, two in both independent periods (receiver broken
tackles with the bar, pooled p=0.020; tight-end yards a target with the bar, p=0.025), none under 0.05/16:
UNDERPOWERED. (c) BLOCKED for backups: separation (NGS lists about 68 receivers a week, all with volume) and win
rate (ESPN Analytics' receiver scores are season-level with a 22-target minimum and no export; PFF route grades
need a subscription export).
Next test: the two cells on 2026 at season's end; and B11(a)'s one stable number, RB yards after contact, inside
E4's shock population, where the question is whether it names the back who holds a job he inherits.

### C · Player reads and schedule calls (live, but later than week 2)

**C1 · Sutton's "median" is one season, and one line contradicts the project's stability table** (charter §6(8)) · OBSERVED · small-n · S
Where: doc 286 uses 2025 only; "contested catch is his skill" against the 0.02 stability doc 284 prints;
Bryant's 8.04 yards a target on 47 targets ranked against a 90+-target median.
Test: 2022-2025 PFF lines; restate.

**C2 · The hot-kicker rule rests on 15 correlated swaps** · OBSERVED · small-n · S · *live: around week 6*
Where: doc 272 (+1.25 a week; three swaps a season sharing one comparator; the 4-to-5-point trigger untested;
"cost of being wrong is zero", though a dropped kicker goes onto waivers per doc 280).
Test: cluster by season; measure the gap against the kicker actually held.

**C3 · Defence plans made months ahead rest on last year's offences** · SUSPECTED · object · M · *live: weeks 9 and 14*
Where: hold Cleveland through week 13, a second defence from week 9, Indianapolis for weeks 15-17; "planning
ahead triples the signal" compares a four-week sum to one week; per the code sweep the D/ST scoring build omits
blocked kicks and fumbles lost (the 18-21 band as 0 is already flagged in §2).
Test: 2022-2025, correlation of the shrunk slate model with realized D/ST points at horizons of 1, 4, 8 and 12
weeks, clustered by team-season.

**C4 · The December tight-end draw is open in the directive and printed as measured** · OBSERVED · small-n · M
Where: §4.33 marks doc 10 (spread of 5.5 or less) against §4.26(b) (+3.39 per sd, one significant cell of ten)
as `[OPEN]`; the wire prints the second as fact, "measured on five seasons" (the population is four).
Test: both methods on the same rows, multiplicity stated.

**C5 · LaPorta's share and his watch trigger** · OBSERVED · object · S
Where: doc 283 divides his 9-game per-game targets by Detroit's 17-game average, applies receiver displacement
and receiver slot-stability numbers to a tight end, and sets an untested "under about 22 routes" trigger.
Test: share in the games he played; tight-end route persistence 2022-2025.

### D · The retraction path and the record (charter §6(9), widened to three stages)

**D1 · Retracted sentences are typed into the page code** · OBSERVED · retraction · M · **LANDED 11 Sept, doc 291**, except the wire's "Why the gem must be claimed early" box (docs 224-226's skill-only population), which moves with the B-family retests
Where: `wire.py:174-217` prints every run: "Volume is not the lever" and "hit rates are flat from week 1 to week
14" (docs 279, 252); "priority... costs you nothing" (226, 255); "Always claim. Never wait for a man to clear to
free agency" beside "Do every Add first"; "stream the defence... not season-long holds" beside "The defence to
HOLD"; the draft-night drop table (Spears listed, Hockenson missing); the Nacua handcuff note ("the pick at 41",
Atwell). Also the sheet's "62 measured absences", where its own constant says 51 and §4.27 says 40.
Test: grep every retraction's tokens from docs 223-289 across `Scripts\`, `Source\*.csv` / `.json` and both
rendered pages; list survivors by stage (code, data, page).

**D2 · Retractions that never reached the directive** · OBSERVED · retraction · S
Where: §4.27 still gives gates 1 and 2 as "the applied form"; the §4.28 / §4.30 BLOCKED lines are still in the
body; §4.31 "the D/ST version (blocked)"; §4.33 "the trade lane is nearly closed"; §5 "Graded LAST, −109.6";
§4.32 "two runs a week" against doc 280's single Thursday 03:00-05:00 batch in all four seasons; §4.19 and
§4.31 call the derived replacement rates "measured". And the upside line Matt retracted on 11 Sept sat in
§0.5(a2)'s count and in §4.29.
**Partly closed 11 Sept, directive v9.4:** the upside line is out, and the gates, the slot-rate and D/ST BLOCKED
lines, the trade lane, §5's grade ranks and the "measured" labels now carry their retractions in the body. §4.32's
"two runs a week" stays until E3 measures it. One row each in `Source\AUDIT_LEDGER.md`; the code, page and prompt
boxes close in D1.
Test: the same grep against `00_PROJECT_DIRECTIVE.md`.

**D3 · The charter carries a retraction miss of its own** · OBSERVED · retraction · S · **LANDED 11 Sept (record), doc 291**
Where: its §6(2) (see §2 above) and doc 281's description of 11.2.
Test: none; a record fix.

**D4 · The page's constants were built from scratch files that are not on the drive** · OBSERVED · guard · M
Where: `research/sheetdata.py`, which writes `sheet_constants.json`, reads `/home/claude/dst/dist_3of3.npy`,
`dist_rook1.npy`, `games.csv`, `drafted.json` and `wire_now.json`; `kick.py` reads
`/home/claude/k_weekly_2021_2025.csv`. Those were a past session's scratch space. Docs 275 and 276 name no script
for the in-season screen and seat numbers.
Test: re-derive each printed constant from raw files, or mark it `[INHERITED]` on the record; report which
reproduce.

**D5 · The trackers stopped** · OBSERVED · guard · S
Where: `OPEN_THREADS.md` last generated 9 Sept 18:23 (about 26 docs since); `ERROR_PATTERNS.md` last changed
5 Sept (none of the three in-season error shapes recorded); `matt_reads.md` not scraped.
Test: run `open_threads.py` on the current docs; diff.

**D6 · Docs 242-244 exist only in the project store** · OBSERVED · guard · S
Where: `Source\` jumps from 241 to 245; doc 244 is the source of 11.2 and in scope; doc 289 counts about 16
such docs and plans a store cleanup.
Test: diff store against `Source\` and `_archive\` by number; commit every store-only doc before any delete.
*(11 Sept, doc 294)* Doc 244's test is rebuilt and reproduces (`Scripts\research\late_picks\keep_role.py`); the doc
itself is still store-only.

**D7 · The plain-language guard does not see the week sheet** · OBSERVED · guard · S · **CLOSED 11 Sept, doc 291** (a planted doc-voice line on the sheet fires three hits)
Where: `check_plain.py`'s page list omits `WEEK_SHEET.html`; `ff.bat` never runs it.
Test: run it on both pages.

**D8 · Scheduled reads are tested by construction only** · SUSPECTED · guard · S
Where: the Tuesday 8:05am read and the Sunday 11:40am check have never fired; doc 261's two old Windows tasks may
still double-run `ff.bat`. Their prompts are also a fourth stage of the retraction path (checked 11 Sept): the
Tuesday read is told to flag anyone who clears "a screen the project already measured", naming the first-round
rookie rate (B7), the three-signal screen (F2, B6) and a backup behind a flagged starter (B4), and it reads the
`screen` column that F2 found was built once on board rows only. A kill that stops at the page leaves the prompt
quoting it. (11 Sept: a caveat was added to the Tuesday prompt, telling it not to quote a screen's rate as a rule
or recommend a claim on a screen alone while these items are open. That is a patch, not the fix.)
Test: list the scheduled tasks from here; read `ff_log.txt` for duplicate stamps; grep both prompts for every
claim this audit kills or qualifies.

**D9 · Preferences now carry reopening conditions, but nothing watches them, and one is priced on the engine that cannot see injuries** · OBSERVED · guard · S · *Matt's rule, 11 Sept*
Where: his rule, applied to his reads file on 11 Sept: a preference stands today and names what would bring it
back to him, the way a test names its falsifier. Washington's row has three triggers; Bryant's and Shough's got
theirs the same morning. Neither scheduled read's prompt checks any of them (the Sunday check watches the starters
of free backups and his own players, not the man ahead of Washington; the Tuesday read watches newly free
players). And Washington's third trigger, "the best alternative use of that seat prices above +3", is read off the
drop cost that prints 0.0 for a backup behind a flagged starter, which is A1's example. A limit proposed here on
11 Sept (scope instructions stand until he changes them) is dropped at his instruction: "I want you to challenge me
so I don't overlook better options... I prefer the science view first. My opinions will always be up to change as
well as circumstances." Nothing of his is exempt from challenge. What stays with him is executing a claim, a drop,
an ESPN write or anything with money. The charter's §5 still carries the Washington line with no trigger. `wire.py` and `sheet_engine.py` hard-code no player preference by name (checked, §6).
Test: list every preference in the reads file, the charter and both pages with its trigger; name the page or
scheduled read that checks each, and add the check where none exists; after A1 and A2, re-price Washington's seat
and its best alternative.

### E · The frame above all of it

**E1 · The in-season objective is 14 equal weeks of projected points; the project's objective is payout** · SUSPECTED · frame · L
Where: every sheet total weights weeks 1-14 equally; weeks 15-17 decide $525 / $225 / $150 (§2); a point in a
week already won is worth less; nothing in-season converts points to playoff odds (§0.3).
Test: from the 2022-2025 scoreboard, the change in playoff odds from one extra point, by week; whether that
weighting changes any live call.

**E2 · "Swing more often" is a cross-section of five managers** · OBSERVED · object · M · *live: a standing to-do line*
Where: doc 279 (Taylor 89 adds, Matt 23). Off-Thursday adds are 36% of adds and 34% of hits (the doc's own
null on timing); extra swings cost drops that A1's model prices at zero.
Test: team-seasons 2022-2025, startable weeks gained from adds against number of adds, manager fixed effects.
Direction: positive, smaller than the cross-section.

**E3 · The waiver mechanic itself is unsettled** · OBSERVED · object · S
Where: "two runs a week" (§4.32, Matt's fact) against "one Thursday 03:00-05:00 batch" (doc 280) against
"Wednesday" (docs 273, 274); the claim-order calculation depends on which.
Test: count distinct processing batches per week in the 2022-2025 waiver timestamps.

**E4 · The edge is lead time: after a team shock, which indicators name the beneficiary before a rival claims him** · NOT YET RUN · L · *Matt's goal, 11 Sept*
His words: "What I am intrigued by is the potential change when team dynamics change such as injuries or poor
performance and other factors. I'm looking for the edge to find valuable indicators before other teams do. The goal
is to play waivers and FAs to our advantage."
Where: every in-season test here asks whether an indicator predicts an outcome; none asks whether it predicts it
before the market acts. The market that matters is this league's own adds (`waiver_report_2022-2025.csv`, with
timestamps). §4.31's legibility test (what share of the free-and-usable pool is claimed within two weeks) is the
nearest thing and is NOT YET RUN.
Testable form: population, every team-season 2022-2025 where a player misses a game (injury report or roster
status) or loses his role without an injury (G2's detector), and each same-team teammate at that position who was
free in this league that week (the pool rebuilt from the draft and the add/drop log, doc 252's method). Indicators
measured at the moment of the shock: depth-chart spot, alignment match (F3), relief production (§4.27), draft
capital, the three-signal screen, the size of the job, his prior snap share. Outcomes: (a) startable over the next
three games; (b) the week a rival adds him. Direction, his: at least one indicator names the beneficiary a waiver
run or more before a rival claims him, and adds to what his prior usage already said. Clustered by team-season;
report each indicator's hit rate and its lead in weeks, not a pooled score.
**Added 11 Sept (doc 292).** The usage lane is now the baseline an indicator has to beat, priced on 2019-2025, weeks
3-13: a first week at the starter snap line with the bar converts 26.0%, the snap line alone 16.0%, neither 3.8%.
A shock alone adds nothing measurable (the position's snap leader sat out the jump game: 17.6% vs 13.8%, p=0.35).
No indicator in this test may be gated on pedigree or on the draft board; tier enters as a term. Matt's metrics join
the indicator list with B11's caveat: most do not exist, or do not repeat, for the man before his jump.

**E5 · The stash menu has one shape** (Matt, 11 Sept: *"other scenarios apply that are worth considering for stash and potential value"*) · OBSERVED · frame · M
Where: the pages carry the RB handcuff (lane 2) and two receiver screens (lane 3); nothing else a stash can be.
Doc 292 §5 lists twelve shapes with status. Three are new and NOT YET RUN: (1) a quarterback change moving the target
tree (nflverse play-by-play: the new passer's prior target shares by alignment and depth); (2) a trade or release that
opens a job without an injury (T5's clear-path measure on events found in weekly rosters); (3) a hurt starter parked
on IR until he returns (return-to-role rate after four or more weeks out, nflverse injuries plus snaps; A12 covers
the seat). Test each in its own testable form before it earns a lane. Batch 2, after E4.

**E6 · What moves a late pick into a job** (Matt, 11 Sept: *"Research his example, other lower drafted players that became relevant and those signals should be easier to parse because petagree no longer drowns out the other signals"*) · R1 TESTED 11 Sept, doc 293 · R2c TESTED 11 Sept, doc 294, UNRESOLVED · population · L
Design: the unit is the chance, not the player. Every late pick (NFL round 4 or later, or undrafted) who got an opening
is compared with the ones who got the same opening and faded; examples like Hubbard generate the hypotheses only.
R1, 2015-2025 (doc 293): 794 risers labelled by how the role opened; 826 absence openings; 1,131 rotation backups with
nobody hurt ahead. Late picks rose 10.8% against 20.2% after an absence and 7.0% against 20.6% without one. With all
three signals a late pick took the role 29 of 81 against an early pick's 43 of 112 (p=0.76); with one or none, 40 of
472. Holds in both eras and on the absence openings. The efficiency gap over a struggling starter (Hubbard 2023's
shape) leaned his way and did not resolve (p=0.089). Interaction terms null to negative: Matt's claim is PARTLY right.
R2c, 2015-2025 (doc 294): backs who produced while filling in kept +12.1 points of the backfield's touches after the
starter returned as late picks and +11.6 as early picks (the man who got the work; +9.8 against +11.7 for the designated
backup); inside our season the gap is -3.5 to -13.1 on seven or eight early-pick events: UNRESOLVED. Startable afterward
8 of 39 against 5 of 11. The returning starter's pedigree looked larger (7 of 10 against 4 of 26 with the starter back
by week 14, SUGGESTIVE; re-test on 2026's returns).
Next, in order: R2a the preseason route, 125 late
picks startable from week 1 (depth charts, OverTheCap contracts, our preseason pulls) · R2b the coach's words before a
flip, against non-risers (joins G1) · R2d coaching changes and trades (BLOCKED from this session on `nfldata/games.csv`;
play-by-play carries coach names). Batch 2, after E5.

### F · Receiver indicators Matt asked for (added 11 Sept)

His framing, quoted so no test drifts from it: "Bryant was an example, not a plan... I was using that room to mine
for indicators... What I want is to be paying attention if Denver shakes up." **None of these prices a player.**

**F1 · A veteran arrival squeezes the room below him** · NOT YET RUN · M · *Matt's mechanism*
His claim: "the arrival compresses everyone below him, not just the man at the top. If that's right, Waddle hurts
Bryant more than Sutton does, and my watch trigger is Waddle's snaps, not Sutton's."
Testable form: every team-season 2021-2025 where a receiver with 60+ targets for another team the year before
joined a team that already had a returning 60+-target incumbent. Outcome: change in share of team targets from
last season to this one for (a) the incumbent and (b) the returning receivers who ranked 3rd and 4th on that team
by last season's targets (rank fixed before the outcome, not re-ranked afterwards). Baseline: the same changes on
team-seasons with a returning 60+ incumbent and no veteran arrival. Direction: the 3rd and 4th men lose share, and
lose more in proportion to their share than the incumbent does. Controls: vacated targets (an arrival often
replaces a departed receiver, which pushes shares up and would hide the squeeze); clustered by team. Shares are
per game played, 4-game minimum, with the number removed by that filter reported (B2).
Inputs: nflverse weekly player stats 2020-2025 (downloadable here); team codes mapped with an assert (A4's
lesson; PFF files use their own codes, Houston is `HST`).

**F2 · The three-signal screen on today's free receivers** · OBSERVED (provenance) · S · *Matt asked: run, or only quoted?*
**Run once, on a narrower population, then quoted.** `research/build_pedigree.py` wrote `pedigree_2026.csv` on
9 Sept (291 rows). It screens only receivers on the draft board, drops §4.30's 4-game minimum, compares
receiving-only points with 9.62, and joins draft picks on name and position. It has not been re-run since the
pool changed. The page's "3 of 3" tags (McMillan, Bryant, Pearsall) all come from that one run. A receiver off
the board is never screened: Jayden Higgins (HOU), whom doc 248 scored above all three cutoffs `[INHERITED, doc
248]`, is on the wire's "not on our board" list and is not in `pedigree_2026.csv` (checked), so neither page has
ever screened him.
Test: every free receiver on the current wire, not only board rows; §4.30's own filters (NFL years 1-3, under 9.62
half-PPR a game in 2025 on full scoring, 4+ games, NFL rounds 1-3, yards a target over 7.13, targets a game over
3.20); joined on player ids with the join rate asserted. List who clears 3 of 3 with each signal's value, Bryant
included. Inputs on the drive: `pff_receiving_2025.csv`, `nfl_draft_picks.csv`, `rec_2025.csv`.

**F3 · Whose absence opens his job: alignment, not rank** · NOT YET RUN · M · *Matt's indicator; doc 287 left the alignment column open*
His words: "If Waddle takes the slot and Bryant is on the boundary, then Sutton going down is my event and Waddle
going down is not."
Premise check on last season's file (checked, §6): Waddle ran 77% of his routes wide at Miami and 23% from the
slot; Bryant 58% slot; Sutton 82% wide; Franklin 45% slot. That is the reverse of the example.
**Correction, 11 Sept:** the first version said Denver's 2026 alignment could be read once week-1 snaps exist. It
cannot. nflverse snap counts carry snaps and snap share only, and play-by-play participation lists who was on the
field and the targeted man's route, never where anyone lined up (checked, §6). The free weekly stand-in is the
share of a receiver's targets thrown to the middle of the field, usable only after it is checked against PFF's
season slot rate for 2022-2025. If it tracks poorly, the live trigger is BLOCKED on a weekly PFF alignment file
from Matt's login; the historical test below still runs. The charter restates this example with the alignments
swapped (§2 item 7); this item uses Matt's words.
Testable form: every game 2022-2025 where a receiver who ran 100+ routes that season was absent, and each healthy
receiver teammate in that game. Outcome: the teammate's targets and snap share in the absence games minus his
rate in games the absent man played. Predictor: whether the teammate's main alignment (slot or wide, from PFF's
season slot rate) matches the absent man's, set against his rank by targets. Direction: alignment match predicts
who gains better than rank does. Clustered by team-season. Limitation: alignment is a season trait here, because
weekly alignment is not on the drive. A one-step test also
misses a chain, a hybrid like Franklin sliding outside when a boundary man is out; where a hybrid is on the roster,
report that case separately.
If it holds, the output is the Denver watch trigger: whose absence, and which snap number to watch.

### G · The coach: what he says and what he does (charter §10 and Matt, added 11 Sept)

Matt cannot watch games, so news is his only channel to what a box score does not hold, and "quotes are not
measurable" is not an answer. The charter's standing rule, kept as a rule rather than a measurement: a quote says
where to look, and it never appears on a page beside a point total. G1 is what a coach or a writer says. G2 is
what the coach does after a fumble or a bad-hands game, and needs no news at all (Matt, 11 Sept).

**G1 · Quotes are not logged, and the ledger's outcome input does not measure what its test names** · NOT YET RUN · M · *the testimony half of the Denver watch; F3 is the snap half; shares its data with C5*
Where: charter §10(2)-(3) sets the intake rule (log a quote only if it names a role, an alignment, a personnel
package, a snap, rep or route count, a depth-chart spot or a named competitor; bin hands, effort and adjectives)
and the record (date, speaker and role, exact words, the usage it predicts, usage at the time, checked one to three
weeks later). Nothing is logged yet, and the weekly snap puller it relies on is still NOT YET RUN on the open list.
Three fixes before the first row: the outcome must be a number the puller returns (snap share; route share only
where a source gives routes, and never read from snaps at tight end); "hit" must be fixed before logging, for
example a move of 10 or more points of snap share in the predicted direction; and the filter's reason should be
control, not stability (§2 item 8). Matt's tea-leaves read is split (11 Sept): separation and attitude sightings
belong here; drops and fumbles are G2, because his claim there is the coach's reaction, not what a writer saw.
Test (the charter's, tightened): every logged quote, 2026 weeks 1-14; baseline snap share in the two games before
the quote; outcome the next three games; hit fixed in advance; quotes that pass the filter against quotes that do
not, and head coaches against beat writers. Report cells, not rates, until each cell holds 10.

**G2 · After a lost fumble or a multi-drop game, does the coach cut the role?** · NOT YET RUN · M · *Matt's mechanism, 11 Sept; needs no news*
His claim: "A coach reacts when there are multiple drops or a fumble, and the reaction moves the role... It won't
always work out, but it's a real thing and it's measurable." The old verdict missed it because 0.14 measures
whether a player's drop rate repeats, a question about the player; his claim is about the coach, and role sits at
the stable end of the same table.
His testable form, in his words: "population: every player-game 2021–2025 with a fumble lost, or with 2+ drops;
baseline: his snap and route share over the prior three weeks; outcome: the same share 1–3 weeks later;
direction: it falls, and harder at RB on a fumble than at WR on a drop."
**Drops are not BLOCKED (checked, §6).** nflverse carries FTN's play-by-play charting with a per-play drop flag for
2022, 2023, 2024 and 2025; 2021 was not charted, so the drops half runs on four seasons, joined to play-by-play for
the targeted man. Fumbles lost are weekly in nflverse player stats (rushing, receiving and sack fumbles lost) for
all five. Snap share comes from nflverse snap counts; route share has a stand-in from play-by-play participation
(on the field for a dropback), all five seasons, sound for receivers and weak for backs and tight ends, whose
blocking snaps count as snaps. Carry share at running back is read alongside.
Three additions so the test measures the coach and not something else: (1) a matched control of player-games with
no lost fumble and fewer than two drops, same position, similar prior share, similar touches or targets in the game,
same part of the season, because shares drift on their own and fumbles come with touches; the answer is the event
group's fall minus the control's. (2) An injury screen: the bad-hands game is often the game a player gets hurt, and
an injury also cuts snaps, so games missed and next-week injury-report status are reported as their own outcome,
never folded into share. The data exists (checked, §6): nflverse weekly injury reports and weekly roster status for
2021-2025, and the roster file carries the gsis-to-pfr id crosswalk. First count: after a lost fumble, 4.9% of
backs, receivers and tight ends were Out or Doubtful at the next game, against 2.6% for similar games without one,
so a fumble game is more often an injury game and the screen is needed. (3) Each position and event against its own control before RB fumbles are compared with
WR drops, because backs' and receivers' shares move by different amounts week to week. Ids joined through the
nflverse player table with the join rate asserted (A4's lesson); clustered by player and team-season; every horizon
reported with its count of events.

**G3 · The cards order testimony by who spoke and print claims with no source** · OBSERVED · object · S
Where (checked on `cards_2026.csv`, 10 Sept 19:33, §6): Bryant's card, the example and not the target, leads with
Payton on catching ("rarely does he have to leave his feet") ahead of the Sports Illustrated line about role
("will see the field often"); prints "the coach who decides his snaps has spent a career feeding big possession
receivers" and "Mims is a deep threat and Bryant is a possession receiver, so they are not competing for the same
snaps" with no source; and calls him "the only slot receiver in Denver's room" in one field while another says he
"has to take the slot from TROY FRANKLIN" (Franklin ran 45% of his routes from the slot last season). The same
field states Waddle's squeeze on Franklin as fact, which is F1's untested mechanism.
Test: every card: tag each quote by G1's rule and order by what it describes; source or strike every tendency
claim; flag every pair of fields that disagree, and every mechanism stated as fact that an open item tests.

---

## 4. Batches, in the order Matt accepted (11 Sept)

**Batch 1 · started early, 11 Sept, 10:15 am ET, on Matt's word** (it was set for Saturday 9 am).
*First half, landed before the Sunday 11:45 am rebuild:* A4 with A16 (Washington, and every guard shown firing on
one path only), A15 (the do-not rule and the
Pearsall block, fix), A2 (the one scale defect), A6 (stale pages), D1-D3 (the retraction sweep).
**First half LANDED 11 Sept, 12:30 pm (doc 291).**
*Second half:* A1, F2, F1, F3, B5, B9. (A1 moved to the front: doc 291 §5.)
Why the split: Sunday's rebuild is the only real clock, and everything in the first half changes what that page
says. B3 moves to batch 2 because the week-1 rule stops binding once week 1 is over.
**Batch 2 · The research bars, before the week-5 tight-end call:** B1, B2, B3, B4, A9, A11, B6, B7, B8, C5, G1,
G2, E4, then B11, E5 and E6's R2a, R2b (R2c landed early, doc 294; its re-test waits for 2026's returns) (G1 and C5 share the weekly snap puller; G2 runs on past seasons and needs none; E4 builds on G2's
detector and F3's alignment, so it runs after them; B11 and E5 use E4's shock population). A9's clear path is already
measured (doc 292).
**Batch 3 · Plumbing and the record:** A3 (one command from Matt, added to his list then), A5, A7, A8, A10, A12,
A13, A17's page lane (its file landed early, doc 292), A14, D4-D9, G3.
**Batch 4 · The frames and the calendar:** E1, E2, E3, B10, C1, C2, C3, C4.
**Standing steps in every batch (charter §11(3)).** This conversation compacts, and after a compaction it holds a
summary of the charter and of the code, not the files. So: re-read the charter and this catalog after any
compaction; re-read a script before patching it, because a remembered cause is an unverified one; and treat any
number that cannot be pointed at a file as `[INHERITED]`. Batch 1 is the heaviest. If its second half cannot
finish, it stops at a whole item and the overview names what moved.

## 5. The kill path (doc 288 §6): one recommendation

**One file, `Source\AUDIT_LEDGER.md`, one row per claim the audit kills or qualifies:** the directive paragraph ·
the sentence as it stands · the replacement · the grep tokens · four boxes (code clean · page clean · directive
edited · scheduled prompts clean). A row closes only when a grep ticks all three, not a reading. **No directive edit lands row by row; they
land in one pass with doc 289's trim**, which doc 289 already sequences after this catalog. `open_threads.py`
scrapes the ledger, so an unclosed kill shows as an open thread.
Rejected: editing §4 after each batch (two passes over the same text, which doc 289 warns against); leaving kills
in the batch docs only (that is how doc 282 happened).

## 6. What I checked directly on the files (the only numbers here not inherited)

1. The 7 Sept pull is a 17-game projection: rushing yards over rushing yards a game is 17.00 on each of the top
   six rows (Gibbs 1,389.5 over 81.73).
2. `sheet_engine.py:720` and `wire.py:532` divide by 14.0.
3. `rates()` drops 17 `WSH` rows with a projection and 2 `FA` rows; `byes_2026.csv` spells it `WAS`.
4. `week_points` removes a player only when `bye == week`.
5. Both pages were built 10 Sept 17:50; `wire.py` changed 18:36, `sheet_engine.py` 18:51, `cards_2026.csv`
   19:33; the rendered TE table leads with Strange at +8.1.
6. `wire.py:174-217` carry the sentences quoted in D1.
7. `FLOOR = 11.2` is a label only (`build_inherit.py:53, 181`).
8. `research/sheetdata.py` reads `/home/claude/dst/*.npy` and other scratch paths that are not on the drive.
9. `ff.bat`'s PAGE OK is `if exist`.
10. `check_plain.py`'s page list has no `WEEK_SHEET.html`.
11. nflverse weekly player stats download from this session (`player_stats_2024.csv`, HTTP 200), so no batch-1
    or batch-2 test is BLOCKED on data.
12. `OPEN_THREADS.md` was modified 9 Sept 18:23; `ERROR_PATTERNS.md` 5 Sept.
13. `Source\` has no 242, 243 or 244; Jacobs is 152.5 in the 7 Sept pull and his job is 241 in `depth_map.csv`.
14. *(11 Sept)* The 17 `WSH` rows include the Commanders D/ST (70.8) and kicker Drew Stevens (133.6).
15. *(11 Sept)* `pedigree_2026.csv` has 291 rows built from the draft board; Jayden Higgins is not in it; Bryant is
    in it at NFL year 2, round 3, 7.71 yards a target, 3.77 targets a game.
16. *(11 Sept)* `pff_receiving_2025.csv`: Waddle (MIA) 416 routes, 76.5% wide, 23.0% slot; Bryant 309 routes, 57.8%
    slot; Sutton 81.5% wide; Franklin 45.1% slot; Mims 30.7% slot. Houston's code in that file is `HST`.
17. *(11 Sept, 8:20 am)* The handoff on the drive is 33,344 bytes; its §1-§8 match the 19,865-byte copy read on
    10 Sept except for one trailing blank line.
18. *(11 Sept)* Matt's sentence in this conversation reads "If Waddle takes the slot and Bryant is on the boundary";
    the charter's §11(2)(c) reads "If Waddle takes the boundary and Bryant is the slot".
19. *(11 Sept)* nflverse `snap_counts_2025.csv` holds game, player, position, team, opponent, and offense, defence
    and special-teams snaps and shares; no route or alignment column. `pbp_participation` exists for 2024 and 2025
    and lists the players on each play, formation, personnel and the targeted man's route; no alignment.
20. *(11 Sept)* `cards_2026.csv` (10 Sept 19:33), Bryant's row: the Payton quote comes first; "spent a career
    feeding big possession receivers" and "Mims is a deep threat ... not competing for the same snaps" carry no
    source; the signal field says "the only slot receiver in Denver's room" and the bear field says "has to take the
    slot from TROY FRANKLIN".
21. *(11 Sept, 8:46 am)* nflverse `ftn_charting` exists for 2022-2025 (2021 returns not found) and carries
    `is_drop` and `is_catchable_ball` per play; weekly `player_stats` carries rushing, receiving and sack fumbles
    lost; `pbp_participation` exists for 2021-2025.
22. *(11 Sept, 8:50 am)* Matt's corrected reads file (8:38 am, 9,315 bytes) marked the drops half BLOCKED and the
    upside row CONFIRMED; both were changed, with reasons in the rows. `wire.py` (10 Sept 18:36) and
    `sheet_engine.py` (18:51) contain no player name or drop-list term that hard-codes a preference.
23. *(11 Sept, 10:15 am)* Injury overlap, fumbles half. POPULATION: backs, receivers and tight ends in regular-season
    games 2021-2025 with 5+ carries plus targets, outcome at the team's next game (nflverse weekly stats, injury
    reports, weekly rosters, snap counts; gsis-to-pfr join 99.25%). Lost a fumble, n=448: on the injury report
    11.2%, Out or Doubtful 4.9%, not active 6.7%, no snaps 7.8%. No lost fumble, n=10,488: 8.5%, 2.6%, 5.6%, 6.7%.
    By position, Out or Doubtful: RB 4.9% (266) against 2.9%; WR 5.9% (135) against 2.4%; TE 2.1% (47) against 2.4%.
    `Scripts\research\injury_overlap.py`.
24. *(11 Sept, 10:10 am)* nflverse `injuries` and `weekly_rosters` exist for 2021-2025 and `snap_counts` for 2026;
    the old `player_stats` release stops at 2024 and `stats_player_week_2025.csv` replaces it (same fumble columns).
    Python 3.12 is available here, so scripts Matt runs can be checked on his version.
25. *(11 Sept, 12 pm)* The pre-291 code on the recorded 10 Sept pool reproduces the live 10 Sept week sheet line for
    line except the date, the kicker and defence tables (the recorded pool has none) and five card passages
    rewritten after the page was built. So the offline harness is trusted for everything but K/D-ST availability.
26. *(11 Sept)* `check_kit.py` pinned `check_plain.py` at 5,240 bytes (drive 5,481 since 8 Sept) and `ff.bat` at
    1,835 (drive 2,071 normalised since 10 Sept): two STALE reports on every run. Re-pinned (doc 291).
27. *(11 Sept)* `Source\00_PROJECT_DIRECTIVE-1.md` was byte-identical to `_archive\00_PROJECT_DIRECTIVE_v93_20260911.md`;
    replaced with a pointer to the canonical file.
28. *(11 Sept, 1 pm)* `WIRE_20260910.csv` holds 279 board rows (WR 111, RB 62, TE 60, QB 46); 28 are owned 0.0%, so
    the 400-row pool, sorted by ownership, ended inside the zero-owned block. The page named 71 free skill players
    off the board.
29. *(11 Sept)* `build_inherit.py:183` sets `free` from the newest `WIRE_*.csv`; all 32 `next_man_id` values in
    `inherit_2026.csv` are on `board_v8_fixed.csv`, so the off-board mislabel is latent.
30. *(11 Sept)* The 7 Sept pull has 700 rows; 199 skill rows project at or below zero (WR 71, TE 51, RB 41, QB 36).
    `pedigree_2026.csv` screens 14 players (9 three-of-three, 5 first-round rookies).
31. *(11 Sept)* nflverse NGS weekly receiving lists a median of 68 receivers a week in 2025 (56 to 80); it already
    holds 8 rows for 2026. ESPN Analytics' receiver scores page (undated, read 11 Sept) is season-level, 2017-2025,
    with a 22-target minimum for WR/TE in 2025.
32. *(11 Sept)* nflverse `draft_picks` carries a PFR id for about 100% of RB/WR/TE picks since 2010 (99.4% in
    2010-2014); weekly rosters for 2018-2020 carry a draft number on under 60% of rows, so tiers join on the PFR id.
33. *(11 Sept, 3 pm)* nflverse `draft_picks`: Chuba Hubbard, 2021, round 4, pick 126, CAR, Oklahoma St.
34. *(11 Sept)* The 2014-2025 RB/WR/TE snap rows join to a player id for 62,336 rows, by normalised name + team + season
    + position for 7,066 more, and 532 stay unjoined (0.8%; 1.5% of undrafted players' snaps, 0% of drafted).
35. *(11 Sept)* `github.com/nflverse/nfldata/raw/master/data/games.csv` is refused from this session (repository
    access not enabled); nflverse-data release downloads work.
36. *(11 Sept, 4:15 pm)* `Scripts\research\` holds no script for doc 244, and doc 244's text names its population,
    guard, baseline, outcome and split but not which player is "the replacement".
37. *(11 Sept)* The nflverse release's `snap_counts_2012.csv` is a header with no rows; `snap_counts_2013.csv` is 2.1 MB.
38. *(11 Sept)* `Source\293_the_late_pick_needs_a_door.md` carried a drive modified time of 2:32 pm ET against its
    "4 pm ET" stamp; `Source\` had no 294 before doc 294.

## 7. Inputs, listed rather than assumed

- On the drive and staged: docs 223-289, both pages, `wire.py`, `sheet_engine.py`, `research\*.py`,
  `waiver_report_2022-2025.csv`, `trade_report_*`, `pff_receiving_2024-2025`, `code_universe_v5.csv`, the
  7 Sept pull, every sheet input.
- On the drive, not yet staged: `pff_receiving_2022-2023`, `pff_rushing_*`, the 2022 and 2024 pulls (for B1).
- From this session: nflverse weekly stats, rosters, depth charts, draft picks; and for doc 292, 2018-2025 weekly
  stats, rosters and snap counts, PFR weekly advanced rushing and receiving 2019-2025, and NGS weekly receiving.
- Only from Matt's machine: a fresh 2026 projection pull (A3) and the 2026 transaction pull (A14). Not requested
  yet.
- For family F: nflverse weekly stats 2020-2025 and snap counts (downloadable here); the alignment columns in
  `pff_receiving_2022-2025` (on the drive); nflverse play-by-play pass location for F3's weekly stand-in.
- For family G: nflverse snap counts for 2026 (check that the file updates weekly) and 2026 play-by-play
  participation (check that a 2026 file exists); a weekly PFF alignment or route file only from Matt's login, and
  only if the free stand-ins fail. For G2: nflverse weekly player stats, snap counts, play-by-play and participation
  for 2021-2025, FTN charting for 2022-2025, weekly injury reports and weekly roster status (which also carries
  the id crosswalk). For E4: the same, plus `waiver_report_2022-2025.csv` and the draft recaps for the weekly pool.
- Not recoverable: the scratch files in D4.
