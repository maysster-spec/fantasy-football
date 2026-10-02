# 472 · The matchup number beside the rate, and the week nflverse has not posted

*2 Oct 2026, 02:00 ET. Doc 468 measured the term and left the page column NOT YET RUN. This is the column, its guard, and
the reason nothing prints on it yet.*

## 1. What is on the page now

**On the roster table (section 5) and the drop ladder, every running back and tight end carries `matchup vs OPP +0.4`
beside his rate: the coefficient from doc 468 (0.10 at RB, 0.11 at TE) times the opponent's half-PPR points allowed per
game to the position this season, centred on the league average.** Points a week, one decimal, signed. Nothing is sorted on
it (finding 4.49: a tiebreak within a point, never a reason to move a man off a better rate). A receiver never carries it,
a man on bye never carries it, and a defense with fewer than four finished weeks of record prints nothing, because the
measurement started at week 5 for that reason and a three-week average of a defense is mostly its opponents.

`sheet_engine.matchup_terms(src, week)` reads `form_2026.csv` (every finished week's RB and TE rows, `in_progress` rows
skipped) and `sched_2026.csv` (who played whom, and who plays whom in the week being priced; a team absent from the week's
rows is on bye). `matchup_text(pl, mu)` prints it. `write()` builds the term once a run and hands it to `render()`.

**On a synthetic fourth week (week 3's rows copied as week 4), the live roster printed sixteen numbers: Jeanty and Mike
Washington vs NE +0.2, Judkins vs NYJ +0.1, Dowdle vs IND +0.5, Allgeier vs DET minus 0.2, Dobbins vs LAC minus 0.1,
LaPorta vs ARI +0.0, Barner vs SF minus 0.4.** The spread across the league on that synthetic file ran from about minus
0.8 to +1.1 at RB, the size doc 468 measured between the hardest and softest quarter.

## 2. The guard, and its negative control on the real object

**`check_page_logic.py` P11 recomputes the term from the two files with its own code (no engine import, like P4 and P9)
and fails the build when a matchup number sits on a row that is not a back or a tight end, when a printed number is more
than 0.06 from the files' arithmetic, when it names a defense without four weeks of record, or when a roster back or tight
end whose opponent has the record carries no number at all.** Four controls in the selftest on a four-team synthetic
league: the files' own number is quiet; the sign flipped fires; a receiver with a number fires; a roster back with a priced
opponent and no number fires. 67 of 67.

The negative control that matters is the one on the production object: **the previous engine (pinned at doc 470) rendered
on the synthetic four-week file, and P11 fired on it, "Ashton Jeanty LV vs NE", because that engine prints no column.** The
new engine on the same file is quiet. On the real three-week file both engines are quiet, which is correct: no defense has
the record, so no number is owed.

## 3. Why nothing prints tonight, and it is not the pipeline

**`form_2026.csv` on the drive holds weeks 1 to 3. The nflverse weekly file it is built from held weeks 1 to 3 at 01:40 on
2 Oct as well** (fetched fresh from the release path `build_form.py` uses; 1,487,226 bytes; 1,118, 1,107 and 1,114 rows by
week). Week 4 ended on Monday 28 Sept. nflverse has not posted it, or has posted it somewhere the kit does not read; the
release API that would say which returns 403 through this container's proxy, so I cannot tell which from here. **What it
means on the page: every "this season (3 g)" cell, the blend's weight, the two-game expected and now the matchup column are
all standing on three weeks until that file moves.** Nothing in the kit is wrong about it; `build_form.py` re-fetches on
every run and will pick week 4 up the morning it lands. The first build after that is the one to read (section 4).

## 4. What the synthetic fourth week showed about THE CALL, and it is a watch item, not a fix

On the synthetic file THE CALL took Gesicki in for Bryant, then **named Sam LaPorta as Tank Bigsby's drop**, and P5 fired
(a starter offered as the drop, doc 462). The engine's reasoning is internally consistent: once Gesicki is on the roster at
9.7 a week, LaPorta at 9.0 is a bench tight end by value and the cheapest man, so he is below replacement and the ticket
clears. The slot file still has him as the starting tight end, which is what P5 reads. **The same chain fired on the
previous engine on the same file, so the matchup column did not cause it; the data did.** I am not changing the rule on
synthetic data. If the real four-week build does the same, the decision is whether a man displaced earlier in the same card
may be a later drop. Doc 462's rule says never a man who starts, and the slot file is the authority until Matt says
otherwise. It is on my list by name.

## 5. Shipped, pinned, open

`sheet_engine.py` (282,389 B, 9dc486fdf3b43f97), `check_page_logic.py` (63,930 B, b5f842f3e61cd22c), `check_kit.py` with
both pins; the three previous versions in `_archive\` with a 20261002_0150 suffix; every commit staged back and hashed.
Finding 4.49's NOT YET RUN clause is struck in `DIRECTIVE_FINDINGS.md` with this doc's line; the index row in the pasted
directive still says NOT YET RUN and changes at the next version with the banner rule from doc 471, one paste.

- NOT YET RUN: read the first four-week build (projections, the blend weight at 0.43, the matchup numbers, P5).
- Index row 4.49 and 9 rule 5 at v9.40.
