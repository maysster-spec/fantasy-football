# 385. THE 2021 AND 2025 FILES WENT IN AS FULL-PPR, ALL FIVE YEARS ARE HALF-PPR NOW, AND ON FOUR SEASONS THE RISER IS +36, CARRIED BY TWO OF THEM

> **BANNER, 28 Sept 2026 (doc 435), reproduced cold from `J4_rows_main_halfppr5.csv` and the registry.** The riser numbers reproduce to the decimal (+35.6, se 11.7; interval floor 8.6 to 9.3 by bootstrap seed; startable 54% / 30%; 2021 minus 11 per ten; the shares rebuild exactly from the nflverse cache). **One registry claim does not: 2021's AVG column is NOT the mean of its Yahoo, Sleeper and RTSports columns. RTSports is empty, 200 of 495 rows carry an AVG with no site value at all, and where Yahoo and Sleeper both exist the AVG differs on 207 of 215 rows. It is a real fractional ADP (not a rank), but its composition is FantasyPros' own, not derivable from the export.** 2022 to 2025 AVGs equal the site means row for row; 2025's Real-Time column is NOT in the AVG, so `MANIFEST.csv`'s "AVG of ... Real-Time" label is wrong (the label is a header echo, never checked). A guard, AVG within 0.05 of the site mean on every row with a site value, would have caught both. n=138 is the band; each tercile arm is 46.

*22 Sept 2026, 06:55 ET. Claude (Cowork), on Matt's handover message "source\00_START_HERE.md" at 06:32. Doc 384 is the
previous number; 385 reserved by listing `Source\` at 06:5x. No em dashes.*

---

## 0. WHAT TO DO

1. **Paste directive v9.13.** One number in the resident set moved: the rounds-5-to-8 riser gap is **+36 VBD14 (9 to 56,
   n=138)** on four seasons, not +51 (19 to 73, n=100) on three. The rule is unchanged. On your list. (v9.12 is already
   pasted: this session's instructions read v9.12.)
2. **A number that must not be quoted any more: +51 [18.5, 73.4], n=100** (doc 384, v9.12). Also doc 384's "the verdict
   has now held on three instruments" without the next sentence: on those same rows, dropping 2022 alone put the
   interval through zero, and nobody ran it.
3. **Your 2021 and 2025 exports are in the registry, from the half-point files.** The 06:30 build had used the `_ppr`
   files (ESPN, CBS, Fantrax: a different scoring and a different instrument) under a half-PPR label. Rebuilt at
   06:36; the builder now refuses the full-PPR page. Nothing for you to run.
4. **Week 2 is in `form_2026.csv` now** (06:43, from nflverse, 32 of 32 clubs). The 07:30 `ff.bat` run is the first
   sheet that sees week 2. Read that one, not the 06:00 one, before filing a claim.
5. **Puka Nacua sat out Monday night (groin) and the 06:00 lineup page says "all clear".** Check his practice report
   Wednesday to Friday before the Sunday 13:00 lock. On your list.
6. Nothing else to run.

---

## 1. THE REGISTRY: WHAT LANDED, WHAT WAS WRONG, WHAT IT IS NOW

**What landed (read from the drive, not assumed).** Four exports at the 2026 root, 06:21 to 06:24: `..._2021_..._half_point.csv`
(Yahoo, Sleeper, RTSports, 494 rows), `..._2021_..._ppr.csv` (ESPN, Sleeper, CBS, RTSports, Fantrax, 485 rows), and the same
pair for 2025 (half: Yahoo, Sleeper, RTSports, Real-Time, 388 rows; PPR: six sites, 980 rows). None is a rank.

**What the 06:30 build did, from the archive stamps.** 2021 was built three times: 06:28 and 06:29 from the half-point file
(the two archived copies are content-identical to a half-point build), then 06:30 from the PPR file. 2025 was built twice
inside the 06:30 minute, half-point then PPR (its `_0630` archive copy is content-identical to a half-point build). The registry's raw copies were byte-identical to the two `_ppr` exports, and `MANIFEST.csv` called both
"FantasyPros half-PPR archive page", because the builder wrote that label on whatever it was given.

**Why half-PPR and not the PPR page, science first.** The registry exists to put every year on one market so a cut at ADP 50
or 97 means the same thing in each. 2022 to 2024 are the half-PPR page and no PPR page is held for 2022 or 2023. The PPR page
also prices pass-catchers under a scoring this league does not use. Its one attraction is the ESPN column, and that is the
thing doc 53 warns about only for post-season pulls; a preseason ESPN column would be fine, but it would be fine in all five
years or none. **Measured, so the choice is not only an argument:** Spearman half against PPR 0.990 (2021, 469 shared) and
0.972 (2025, 340 shared); two men cross the round-5 line and seven the round-9 line in each year; JOB 4's band gap is +35.6 on
half and +43.1 on PPR (section 2). If you ran the PPR files on purpose, say so and I will lay the two side by side for every
finding; they are both archived.

**What it is now.** 2021: 495 rows, ADP 1.0 to 464.0. 2025: 389 rows, 1.0 to 374.0. Against the files they replaced before
today: 2021's rank proxy (200 rows) Spearman 0.966, six men across the round-5 line and ten across the round-9 line.
`code_adp_guard.py` names both years' sources. Every write verified by staging back and hashing (25 of 25).

**The original 2025 file is not on the drive.** The builder stamped its archive copy to the minute. The first 06:30 run
archived the original rounded nine-site file as `preseason_adp_2025_replaced_20260922_0630.csv`; the second run, in the same
minute, archived the half-point build under the same name and replaced it. It was superseded and nothing live reads it; its 2025 prices for doc 384's matched men survive as `adp_N1` in
`J4_rows_main_halfppr3.csv`. Drive's own version history of `preseason_adp_2025.csv` may still hold it; not tried.

---

## 2. JOB 4 ON FOUR SEASONS

**Testable form, unchanged from the job (script docstring):** year-N player-seasons at QB/RB/WR/TE, preseason ADP 50+ in N,
priced again in N+1, 4+ games in N+1; the riser is weeks 10 to 14 share minus weeks 1 to 5 share; outcome N+1 VBD14 net of log
ADP and position; falsifier: a band gap whose interval floor is ten or more says the riser carries it, one whose top is under
ten says strike it, one spanning ten says name the n. **New this run: N = 2021** (the nflverse 2021 weekly file, 150 columns,
last modified 13 Aug 2026, fetched into `Scripts\research\_nflverse_cache\`). The band numbers now come from inside the
script, and they reproduce doc 384's band row exactly on doc 384's own rows file (+51.0 [18.5, 73.4], n=100), which is the
control.

| | doc 384, three seasons | three seasons, new 2025 file | **four seasons, half-PPR** | four seasons, 06:30 PPR files |
|---|---|---|---|---|
| n pooled (by N) | 333 (110/133/90) | 377 (110/133/134) | **496 (119/110/133/134)** | 512 |
| **band 50 to 96: gap net of price** | +51.0 [18.5, 73.4], n=100 | +53.8 [21.2, 74.1], n=102 | **+35.6 [9.3, 56.0], n=138** | +43.1 [18.5, 61.7], n=137 |
| band: riser per +10 share | +17.2 (se 3.4) | +17.3 (se 3.4) | **+13.6 (se 3.3); +13.5 (se 3.3) with season fixed effects** | +15.7 (se 3.1) |
| band: startable, top third against bottom | 56% / 29% | 56% / 26% | **54% / 30%** | 57% / 26% |
| band: price (log ADP) | −31.6 (se 28) | −31.6 (se 28) | **−20.3 (se 24)** | −26.6 (se 23) |
| round 9+: per +10 | −0.1 (se 2.0), n=233 | −0.2 (se 1.9), n=275 | **+0.2 (se 1.7), n=358** | −0.2 (se 1.7), n=375 |
| round 9+: gap | +6.5 [−7.9, 23.0] | +13.4 [−2.0, 27.7] | **+12.5 [−0.8, 24.2]** | +11.1 [−3.2, 22.2] |
| youth x riser, pooled / band | −0.4 (3.9) / +13.8 (10.3) | +1.2 (3.7) / +13.8 (10.3) | **−1.3 (3.2) / −6.8 (8.1)** | −1.3 (3.2) / +1.8 (8.1) |

**Why N=2024 grew from 90 to 134 with no change to 2024's own file:** "priced again in N+1" reads the 2025 registry, and the
old rounded 2025 file had 183 rows, so any 2024 man it did not list failed the condition. The deeper file lets them in.

**THE LEAVE-ONE-SEASON-OUT CHECK, run for the first time (`j4_band_loo.py`):**

| season | band n | that season alone, per +10 | band gap WITHOUT that season |
|---|---|---|---|
| 2021 | 36 | **−11.0 (se 9.2)** | +53.8 [21.2, 74.1] |
| 2022 | 34 | +17.2 (se 4.2) | **+17.8 [−8.9, 42.8]** |
| 2023 | 40 | +18.7 (se 7.2) | +27.2 [−14.9, 49.6] |
| 2024 | 28 | +9.3 (se 10.0) | +35.8 [12.9, 63.9] |

On doc 384's own three-season rows the same check gives: without 2022 +29.1 [−8.0, 60.5], without 2023 +44.0 [−2.2, 75.1].
**So the fragility was there before 2021 arrived; adding 2021 made it visible in the headline.**

**THE VERDICT, with its confidence stated.** The riser still decides inside rounds 5 to 8 on the pool: the slope is four
standard errors from zero with or without season fixed effects, the startable split holds (54% against 30%), and price inside
the band is still nothing. **The size is +36, not +51, and it is uneven: two of four seasons carry it, 2021 runs the other way
on 36 men, and the interval's floor (9.3) now sits on the falsifier's ten-point edge.** That is "measured, not uniform", one
step below where v9.12 put it. Round 9+ stays a dart on the slope; its tercile gap (+12.5, floor −0.8) is not resolved and is
not a reason to change §4.18b. Youth stays withdrawn.

**A HYPOTHESIS, NOT YET RUN, and post hoc so it is labelled that way.** Two of 2021's highest-VBD "fallers" are role moves
the opportunity definition cannot see: Deebo Samuel (WR, share −0.27; his late-2021 work moved to carries, which the WR
definition does not count) and Jalen Hurts (QB, −0.24; attempts fell as Philadelphia ran more). Testable form: counting
carries in the WR and QB opportunity (WR: targets plus carries; QB: attempts plus carries) changes the band slope on
N = 2021 to 2024 by more than one standard error. It came from looking at the rows, so a hit would need a season it was not
fitted on.

---

## 3. WEEK 2: THE FORM FILE, AND TWO THINGS IT SHOWS

**`form_2026.csv` rebuilt at 06:43 from the cloud** with `build_form.py` unchanged (it reads only nflverse; team codes via
`sheet_engine.TEAM_ALIAS`): weeks 1 and 2, 32 of 32 clubs each, 3,533 rows. **Control:** all 1,117 shared week-1 rows are
identical to the 19 Sept file. **Gap:** nflverse had not posted week-2 snap counts for LA and NYG (the Monday game), so 22
skill rows have a blank snap share; carries and targets are complete. Re-running after nflverse posts them fills it in. The
Sept 19 file is at `_archive\form_2026_20260922_0645_wk1only.csv`.

**Nacua.** No week-2 row at all while Davante Adams has one (10 targets, 33% share). Loaded pages: Sports Illustrated, 19 Sept
2026, *"a little bit of soreness in that groin"*, did not practice Friday, questionable; NFL.com (undated page, same game),
inactive Monday against the Giants. **`LINEUP_CHECK.html` at 06:00 said "All clear. Everybody in your lineup is expected to
play."** It reads ESPN's designation, which was blank on Tuesday morning. That sentence is now in `00_START_HERE.md` section 1
as a Tuesday trap.

**Coleman, and the page's cheapest drop.** The 06:00 sheet names Jonah Coleman the cheapest man to drop at 0.0. The five lines:
1. VINTAGE: the 3.9 a week is a preseason projection (7 Sept). This season, 2 games: week 1 6% of snaps, no touches; week 2
   40% of snaps, 10 carries, 3 targets, 13.3 points (rushing and receiving only).
2. POPULATION: none. One man's two games, not a rate.
3. THE MAN AHEAD: J.K. Dobbins, 2026, 2 games: 43% then 34% of snaps, 8 and 10 carries, 3.6 points each week. Games missed
   and current status: not checked.
4. THE STANDING RULE: "A bench running back earns his spot by the job he would inherit and the fragility of the man ahead of
   him, never by his own projection" (§6). Roster after a Coleman-for-tight-end swap: RB 5 of 6, TE 2 of 3, 15 of 15. The
   sheet's own calendar says the week-6 TE hole is claimed in week 5.
5. THE COUNTERFACTUAL: the page's top pickup is 11.1 expected points, a rate over 45 men, not his forecast; Coleman's 0.0 is a
   projection week 2 contradicts, and his share of Denver's job is not on the page. Keeper cost of dropping him: none, he is a
   waiver pickup.
**THE CALL, made at 07:45 on the 07:30 sheet (built 07:30:05, form file of 06:43, vintage table on two games): NO CLAIM
TONIGHT; KEEP COLEMAN.** The 07:30 sheet leads with four tight ends (Hunter Henry, Dalton Schultz, Cade Otton, Michael Mayer)
at an identical 11.1, which is the definition of a base rate, and still names Coleman the cheapest drop at 0.0. The five lines,
completed:
1. VINTAGE: the 11.1 is 38% of the 45 men who cleared two of three week-one marks (NFL-wide 2022 to 2025) times 29 points;
   Coleman's 0.0 is proj. Coleman, 2026, 2 games: as above.
2. POPULATION: a screen on week-one work, not any of the four men's forecast; four men print it.
3. THE MAN AHEAD: two men. J.K. Dobbins (on this roster): 10 of 17 games in 2025, 13 in 2024, 1 in 2023 (nflverse); both 2026
   games. RJ Harvey: hamstring, inactive in week 2, limited in practice by the end of the week (RotoWire, 20 Sept 2026, page
   loaded); in week 1, with Harvey playing, Coleman had 6% of snaps. **So the week-2 pop is Harvey's absence, not a new role.**
4. THE STANDING RULES: *"A second QB or TE is taken only after landing on the wrong end of a drought at the position"*
   (LaPorta scored 7.3 and 14.2, no drought; his one hole is the week-6 bye, and the sheet's own calendar says claim for it in
   week 5); *"Bench priority is RB to the cap"* (Coleman is RB6 of 6); and *"a bench running back earns his spot by the job he
   would inherit and the fragility of the man ahead"*: Coleman is the Denver insurance behind your own starter. Roster after:
   unchanged, 15 of 15.
5. THE COUNTERFACTUAL: the claim buys a base-rate 11.1 and spends this week's priority; it gives up the Dobbins/Harvey
   insurance, which the sheet prices at zero and says itself is "above zero and not on this page". Keeper cost of dropping
   Coleman: none (waiver pickup, 19 Sept).
**Confidence: a judgement call, not a measurement.** A measured group rate is being weighed against an unpriced option, and
the doctrine tips it. Second option, if he wants the bet anyway: the sheet's order is Schultz first (14 targets in week 2, 40%
of his claim band contested), dropping Coleman.

**AND THE SHEET'S SENTENCE ABOUT COLEMAN IS WRONG.** *"It holds only while Ashton Jeanty stays healthy, because that is the man
he covers"* and *"Make the swap only if you trust Ashton Jeanty's health."* Coleman plays in Denver; Jeanty plays in Las Vegas.
`sheet_engine.py` picks "the man he covers" as the highest-projected man at the same position on Matt's roster
(`ahead_of_fp`, around line 1723), never checking the NFL team, so it names the wrong man and hands him the wrong criterion.
The fix is to prefer a roster man on the same NFL team (`tm`), which here is Dobbins, and otherwise to say "your backs ahead of
him" without a name. **NOT YET RUN:** the engine is pinned by `check_kit.py` and only a page build on Matt's machine exercises
the object production builds (§0.2); an untested edit to the page he decides from, in claim week, is the larger risk. Ledger
row 162.

**08:10, MATT: *"i think i want to see more from hunter henry first"*, with a note in the 2026 folder (`do you have a tie
breaker btw these listed TEs_.md`, written 08:06, author not stated) that ranks Schultz first, Henry second.** His hunch holds
and it is the list's own standing plan (doc 370 point 4: no tight end now; decide in week 5 on four weeks of targets). Henry,
2026, 2 games: 3 then 5 targets, 76% then 91% of snaps; his claim band was contested 29% of the time, so waiting is cheap.
**The call stays: no claim this week.** Checked before agreeing, because doc 370 is the record of this exact trade going the
other way once (a Schultz-for-Coleman claim, argued, then retracted on 19 Sept). The note, fact-checked: its ORDER matches the
sheet's (Schultz is the contested one), but it prices only the gain, never the drop, and four of its specifics are wrong or
unchecked. "40% of leagues contest" is this league's own claim history for that workload band, 40%, not "almost certainly";
Schultz's 14 looks were 14 targets and no carries; "Otton ... meager target upside" meets an 18% target share and 89 to 98% of
snaps in both games, which is not meager for a tight end; the Stroud and Bowers lines are not checked here. Cost of waiting:
Schultz may be claimed by someone else (his band, 40%); the screen's hit rate is flat all season (4.31), so the bet itself does
not expire with him.

---

## 4. THE BUILDER'S TWO DEFECTS, AND THEIR CONTROLS

1. **It labelled any export "half-PPR".** Now it reads the site columns: a page carrying ESPN, CBS, Fantrax or NFL and no Yahoo
   is the full-PPR page, and so is a file named `ppr` without `half`. Refused unless `--allow-ppr`, and then the manifest says
   FULL-PPR. Negative controls, run first: the 2021 PPR file, the 2025 PPR file, and the 2025 PPR file renamed `..._half_point.csv`
   (content wins over name) all refuse; the 2022, 2023 and 2024 registry raw files read as half.
2. **Its archive stamp was to the minute and overwrote.** Now to the second, never overwriting (a `_2` suffix), and the copy is
   compared to its source before the new file is written. Control: two runs in the same second left two archive files.

Both are the job's own instructions (§0.5(f)): the fix is in the tool and in `00_START_HERE.md` section 6, not only in the ledger.

---

## 5. OPEN, BY NAME

- **Matt's:** paste v9.13; Nacua's practice report before Sunday's lock.
- **Done 07:45:** the 07:30 sheet read; no claim, keep Coleman (section 3).
- **Mine:** the `sheet_engine.py` covers-the-wrong-man fix, re-pin and a page build (section 3, ledger row 162).
- **Mine, one batch:** 4.12, 4.18b, 4.20, 4.22, 4.25 and 4.26 on the five-year half-PPR registry; NOT YET RUN, and its old
  blocker (no 2021 weekly file) is gone.
- **Mine:** `build_form.py` again once nflverse posts the LA and NYG week-2 snaps; the WR/QB carries hypothesis (section 2);
  the keeper-riser line on the week sheet (doc 382 §5, Fable's); doc 374 batch A; the directive read by someone with no stake.
- **Not a thread:** the original 2025 rounded file (section 1), unless something needs it.

Ledger row 161. Directive v9.13. Registry: `Source\adp_registry\` 2021 and 2025, MANIFEST, `code_adp_guard.py`; the 06:30
builds are `_archive\preseason_adp_2021_ppr_build_20260922_0630.csv` and `..._2025_...`. Builder:
`Scripts\research\adp_registry_from_fp.py` (old copy `_archive\adp_registry_from_fp_20260922_0650.py`). JOB 4:
`Scripts\research\j4\*_halfppr5*`, `run_j4_with2021_fullppr2125.txt`, `j4_band_loo.py`, `run_j4_band_loo_halfppr5.txt`.
