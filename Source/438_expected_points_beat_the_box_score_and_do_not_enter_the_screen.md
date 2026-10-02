# 438. EXPECTED POINTS BEAT THE BOX SCORE OVER TWO GAMES, AT EVERY POSITION, AND STILL DO NOT ENTER THE SCREEN

*29 Sept 2026. Claude (Cowork), item 1 of doc 437's wiring list, on Matt: "Continue with your top recommendation."
438 reserved by listing `Source\` at 01:55. Script and full output: `Scripts\research\wk1\xfp_backtest.py` and
`run_xfp_backtest.txt` beside it; standard library plus pandas and numpy, paths against the script. No em dashes.*

---

## 0. WHAT TO DO

1. **Read a claim candidate's last two games as EXPECTED points, not actual points.** Measured, 2021 to 2025, 9,999
   claimable RB, WR and TE weeks: the two-game expected predicts the next four weeks better than the two-game actual
   at every position and in every one of the five seasons. Given the expected, the points a man scored over it are
   worth almost nothing (+0.08 a point).
2. **Two flags are on the wire page from the next build, and they say what to do.** `box-score mirage` (8+ actual on
   under 5 expected over his last two games): he is WORSE than the pool he came from, startable over the next four
   weeks 12% against 17%, spike 3% against 4.3%. Do not claim him on those two games. `quiet volume` (8+ expected on
   under 5 actual): startable next four 28%, 7.2 a game against 5.5, on half the points. He is the cheap one.
3. **Neither flag enters the workload count, and the falsifier is why.** As a fourth signal beside targets, snaps and
   share, expected points moved the screen's spike rate by +0.1 points (permutation p=1.0). The three signals and
   the expected number are the same week's workload seen four ways. Display, never sort, exactly as doc 437 fixed in
   advance.
4. **Today's flags, 2026 through week 3, from the rebuilt form file.** Mirage: Josh Palmer BUF (10.4 actual on 4.3
   expected), Deebo Samuel SF (10.2 on 3.5), Ryan Miller MIA (8.4 on 2.0). Quiet volume: J.K. Dobbins DEN (4.7 on
   13.4), Ryan Flournoy DAL (4.0 on 10.7), Jadarian Price SEA (2.6 on 8.9), Jared Wayne HOU (3.4 on 8.8), KC
   Concepcion CLE (3.6 on 8.4). Ownership is not checked here; the wire run checks it.
5. **Paste v9.33 when convenient.** One index row, finding 4.37. On your list.
6. **Nothing to run.** `build_form.py` and `wire.py` carry the two numbers from Monday night's run onward; the form
   file on the drive is already rebuilt with them.

---

## 1. THE TEST, STATED BEFORE IT RAN

**THE CLAIM (doc 437 §6 item 1):** does expected fantasy points over the last two games predict a claimable man's next
four weeks better than his actual points, and does it lift the wire's three-signal screen as a fourth signal?

**POPULATION.** RB, WR and TE player-weeks, regular season 2021 to 2025, weeks 2 to 16, NOT startable in week w on
§4.13b's bar (season-to-date half-PPR average through w below RB 9.92, WR 9.62, TE 8.25 a game), at least one target
or carry in w, a game row in w-1 so that "last two games" exists, a snap line, and played in w+1. That is doc 389's
claimable pool extended to backs and required to have two games: **9,999 player-weeks, WR 4,666, RB 2,735, TE
2,598.** Base rates: spike in w+1 (18.0+) 4.3%, startable in w+1 20.5%, startable over the next four weeks 17.4%,
5.48 a game over the next four.

**PREDICTORS**, all measured through week w. ACT2: mean actual half-PPR over games w-1 and w. XFP2: mean EXPECTED
half-PPR over the same two games, from ffverse's ffopportunity model (`ep_weekly_2021..2025.csv`, full PPR converted
by subtracting half a point per expected reception; the join on gsis id covered 100% of 23,097 touch-weeks, and
ffverse's own actual agrees with ours at r=0.9993, the gap being fumbles). The three-signal count in week w, as
`wire.py` computes it: targets 8+, snaps 80%+, target share 20%+.

**OUTCOMES.** Spike in w+1. Startable in w+1 (at or above the bar). NEXT4: mean half-PPR over the games he plays in
w+1 to w+4 (two or more games, n=9,393), and startable over those four (NEXT4 at or above the bar).

**FALSIFIER, fixed in doc 437 before any of this ran:** under +2 points of spike rate over the three-signal count,
expected points stay a display column.

---

## 2. TEST 1: WHICH TWO-GAME NUMBER PREDICTS THE NEXT FOUR WEEKS

| pool | rho with NEXT4, ACT2 | rho with NEXT4, XFP2 | top fifth by ACT2: startable next four | top fifth by XFP2 |
|---|---|---|---|---|
| all, n=9,999 | .417 | **.497** | 33.3% (7.93 a game) | **38.9% (8.57)** |
| RB, n=2,735 | .454 | **.526** | 38.9% (8.86) | **46.3% (9.57)** |
| WR, n=4,666 | .389 | **.473** | 29.7% (7.73) | **35.3% (8.38)** |
| TE, n=2,598 | .406 | **.493** | 32.5% (6.79) | 32.0% (6.98) |

**By season, rho with NEXT4: 2021 .402 against .445, 2022 .385 against .476, 2023 .448 against .540, 2024 .431
against .503, 2025 .416 against .511.** Expected wins five of five. On the spike outcome the top fifth by XFP2 runs
10.1% against 8.5% by ACT2, +1.6 points (se about 0.9); on the four-week outcome +5.6 points. The four-week outcome
is the one a claim is made for, and it is the case for the rule.

**The regression is the cleanest statement.** NEXT4 on both, whole pool: XFP2 +0.532 (se .018), ACT2 +0.081 (se
.016). Rewritten as expected plus points over expected: **XFP2 +0.613 (se .012), over-expected +0.081 (se .016).**
A point of expected production is worth seven and a half points of production over expected. RB +0.62 against
+0.02; WR +0.60 against +0.11; TE +0.60 against +0.08.

**The cells that decide a claim, whole pool:**

| his last two games | n | spike w+1 | startable w+1 | startable next four | next four, a game |
|---|---|---|---|---|---|
| top fifth by BOTH | 1,238 | 10.8% | 38.7% | **41.5%** | 8.87 |
| top fifth by XFP2, not by ACT2 | 762 | 8.9% | 33.2% | **34.5%** | 8.07 |
| top fifth by ACT2, not by XFP2 | 775 | 4.8% | 24.6% | **20.0%** | 6.42 |
| the pool | 9,999 | 4.3% | 20.5% | 17.4% | 5.48 |

**A man in the top fifth on points but not on expected points is a base-rate man.** A man in the top fifth on expected
points but not on points is nearly as good as one in the top fifth on both.

**Mean reversion, fifths of two-game points over expected (2+ games ahead):**

| fifth | ACT2 | XFP2 | NEXT4 | startable next four |
|---|---|---|---|---|
| most under expected (n=1,870) | 4.31 | 7.77 | **6.79** | **25.1%** |
| under | 3.74 | 5.17 | 5.37 | 15.2% |
| middle | 3.62 | 4.11 | 4.86 | 13.6% |
| over | 5.00 | 4.52 | 5.16 | 14.3% |
| most over expected (n=1,905) | 8.67 | 5.74 | 5.95 | 18.9% |

**The fifth that scored 4.3 a game on 7.8 expected outscores the fifth that scored 8.7 on 5.7 expected over the next
four weeks, 6.8 to 6.0, and is startable 25% against 19%.** Both fifths land within a point of their expected number.

---

## 3. TEST 2: THE SCREEN, AND EXPECTED POINTS AS A FOURTH SIGNAL

WR and TE, the screen's gate, n=7,264, base spike 3.7%. The screen reproduces on this pool (doc 308's was week 1 only):
0 of 3 spikes 1.9%, 1 of 3 6.4%, 2 of 3 10.0%, 3 of 3 10.2%; the jump is still one signal to two.

| on the operative bar, 2+ of 3 | n | spike w+1 | startable w+1 | startable next four | next four |
|---|---|---|---|---|---|
| 2+ of 3 | 906 | 10.0% | 37.4% | 37.8% | 8.34 |
| 2+ of 3 AND XFP2 in the pool's top fifth (7.71+) | 659 | 10.0% | 38.7% | 40.7% | 8.73 |
| 2+ of 3 and NOT | 247 | 10.1% | 34.0% | 29.8% | 7.28 |
| XFP2 top fifth alone, fewer than 2 of 3 | 794 | 6.2% | 30.9% | 29.4% | 7.32 |

**Gain in spike rate from the fourth signal on the 2+ bar: 0.0 points (se about 1.5), permutation p=1.000.** The
week-w expected number alone does the same: +0.1. **The falsifier holds and expected points do not enter the count.**
The reason is in the first column: 659 of the 906 men on the 2+ bar already clear the two-game expected bar, and
761 clear the week-w one, because targets, snaps and share are what the model is built from. On the four-week outcome the fourth signal does split the
bar, 40.7% against 29.8%, and a 0-of-4 to 4-of-4 count runs 8.9% to 46.1% startable next four against 10.0% to 44.2%
for 0-of-3 to 3-of-3. That is real and it is small, and the rule was fixed on the spike rate before the run.

**Against the best single signal we had (doc 389's WOPR), same WR/TE pool, top fifths:** WOPR spike 7.7%, startable
next four 31.2%; XFP2 spike 7.9%, startable next four **34.5%**. Top fifth on WOPR but not on XFP2: 22.4% startable
next four. Top fifth on XFP2 but not on WOPR: 30.3%. Expected points are the better four-week read; WOPR is not
worse on the spike.

---

## 4. TEST 3: RUNNING BACKS, WHERE THE SCREEN DOES NOT APPLY

RB claimable pool, n=2,735, top fifths: ACT2 startable next four 38.9%; touches 43.9%; snap share 45.0%; **XFP2
46.3%**; XFP2 and touches together 48.3%. Expected points and snap share are the same instrument at running back
(9.57 a game next four for both), and both beat the box score by seven points of startable rate. Doc 434's "snap
percentage beats snap count" and this agree: the role, not the result.

---

## 5. THE TWO FLAGS, PRICED ON FIXED BARS

Fixed bars rather than pool quantiles, because the live free-agent pool is not this population:

| flag | rule, last two completed games | n | spike w+1 | startable w+1 | startable next four | next four |
|---|---|---|---|---|---|---|
| **box-score mirage** | 8+ actual, under 5 expected | 101 | 3.0% | 14.9% | **12.0%** | 4.88 |
| **quiet volume** | 8+ expected, under 5 actual | 172 | 5.8% | 27.9% | **28.2%** | 7.23 |
| the pool | | 9,999 | 4.3% | 20.5% | 17.4% | 5.48 |

Both cells are small and both are a screen, not this man's forecast. The mirage is worse than the pool on every
outcome; the quiet-volume man is better than the pool on every outcome. Neither sorts anything.

---

## 6. WHAT CHANGED, AND WHAT DID NOT

- **`research\wk1\build_form.py`:** the cumulative row carries `act2` and `xfp2`, mean actual and mean expected over
  his two NEWEST completed games (one game if he has one). Expected is blank, never zero, when either game lacks a
  model row. Rebuilt `form_2026.csv` through week 3: 4,774 rows, every earlier column byte-identical. **The ffverse
  file lagged one game at build time: Chicago and Philadelphia's week 3 has no model row yet, so their men carry
  `xfp_g` 2 and a blank `xfp2` until it lands.**
- **`wire.py`:** `act2` and `xfp2` on every wire row and every free row; the two flags in `flags` for RB, WR and
  TE; re-pinned in `check_kit.py`. The workload count is untouched.
- **Finding 4.37** in `DIRECTIVE_FINDINGS.md`; one index row in the directive, v9.33.
- **Did not change:** the screen, its bars, its ordering (doc 389's cross stands), and doc 437's display rule for
  `xfp` and `fp_oe`, which the flags satisfy for the wire page only.

---

## 7. OPEN, BY NAME

- **Mine:** doc 437's wiring list, items 2 to 7, in order (air-yards threshold, red zone, daily depth chart and
  practice status, routes on history, Vegas lines, RB opportunity share). The season-to-date `xfp` and `fp_oe` are
  still not printed as columns on any page; the flags are. The week sheet's bet lane receives `act2`/`xfp2` and
  prints neither yet.
- **NOT YET RUN, form written:** the same two-game comparison on the DELTA (Matt's 27 Sept claim, on the list):
  among non-startable men, does a rise in expected points from w-1 to w predict the next four weeks over and above
  the level?
- **Matt's:** paste v9.33.
