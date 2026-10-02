# 267 — Two defences, a tired one, and the receivers I should have named

2026-09-10. Answers Matt's five points of 2026-09-09/10. Written in ordinary sentences on purpose:
he said of doc 266's headings, *"I wouldn't put that in all caps if i was writing it, lol."* He is
right, and §0.1's plain-English rule never had a house style attached. This is it.

---

## 1. The correction I owe first: his potential instruction was not about defences

His words, 2026-09-09: *"We are not just looking at current market value, but POTENTIAL value as
well."* I turned that into a general claim — "the wire is a potential instrument" — and then applied
it to the Cleveland defence, which is exactly the wrong object. His own follow-up:

> *"I wasn't even thinking of D/ST when i mentioned it. At the time I was thinking of running backs
> that are the next man up. Same with WR (the potential candidates)."*

Two named archetypes, both already measured in this project, and I widened them into a slogan. That
is §0.5(a2) — a correct answer to a question he did not ask — and the fix is not an apology, it is a
column. See §5 below: `pedigree_2026.csv` and a new lane in `wire.py`.

The one thing worth keeping from the wider version is narrower than I wrote it: potential is the
right sort key **for the two lanes where a job or a pedigree is the asset**, and current board value
is still the right sort key for "who can start for me this Sunday." Those are different lanes and
`wire.py` now prints them as different lanes.

---

## 2. Holding two defences works, and essentially all of the value is in the pairing

His claim, in his words, stated before the test (§0.5(a2)):

> *"The trick later in the year, is to hold more than one D/ST because you can marry the two
> schedules so that a tough week for one is a good week for the other and vice versa. Good defenses
> will be out there for pick up but the sacrifice is holding two spots on the roster."*

**Population.** All 32 defences on the 2026 schedule. **Baseline.** The best single defence over the
same window. **Weekly value.** `max(A, B)` on the shrunk forward model of doc 264 — the opponent's
generosity shrunk by 0.325 and the defence's own quality by 0.269, so this is an ex-ante number, not
hindsight. A bye counts as a blank, never a zero. Script: `pairs.py`.

| window | best single | best pair | gain from the second spot | a random pair |
|---|---|---|---|---|
| weeks 2–14 (13 wks) | SEA 73.19 (5.63/wk) | DEN + SEA 83.48 (6.42/wk) | **+10.30, +0.79 a week** | −1.54 vs the best single |
| weeks 15–17 (3 wks) | PIT 18.15 (6.05/wk) | DEN + PIT 20.26 (6.75/wk) | **+2.11, +0.70 a week** | −1.46 vs the best single |

`[TESTED]` **He is right that it works, and the sharper finding is the counterweight: the median
pair scores *less* than the best single defence, so a second body chosen carelessly is worth below
zero.** 115% of the gain over the regular season and 169% of it in the playoffs comes from choosing
complementary schedules rather than from owning two defences. Two draws from the same urn buy
nothing; the marriage is the whole product.

**What it is worth against the roster spot.** +0.79 a week. Held from week 9 through week 17 that is
about **+7 points**. Doc 240's method prices a bench spot against its best alternative use, and on
his roster that alternative is a body who fills a broken week — the tight end that patched week 6
measured **+7.1**. So the pair and the fill are a coin flip against each other, and the pair wins
outright against the third case, which is the one that actually happened last time: Spears, a sixth
back who never entered the lineup, measured about **−5**.

**Two honest limits.** Taking the better of two forecasts each week borrows a little optimism from
the forecast's own noise, so treat +0.79 as the top of the range. And DEN is the partner in both
windows, which is a single-input result: the generosity term rests on one season (2025) of opponent
offences and no 2026 games have been played.

---

## 3. His tired-defence mechanism: the effect is real and the channel he named is not

His words: *"the offence could [crater] and then the defense is on the field too much and gets tired
by the last quarter. Think, the longer the opposing team's offence on the field the greater chance
that team will score."*

That is two claims and they separate cleanly, so both were stated before running (`tired.py`,
`tired2.py`).

**Population.** 2,576 defence-games, 2021–2025 regular season, from nflverse play-by-play joined to
`dst_weekly_2021_2025.csv`. **Controls.** Both the team-season *and* the opponent-season are swept
out, because inside one season the games where a team's offence looks good are the games against
weak opponents, and a weak opponent is also why its defence scored. Score margin entering the fourth
quarter is controlled too — garbage time is the other confound.

**Claim A, tiredness: null, and bounded.** Quarter-four points allowed against scrimmage plays faced
in quarters one to three: **+0.018 points per play, CI [−0.015, +0.051], p=0.28**. Per standard
deviation of extra work (6.2 plays) that is **+0.11 quarter-four points, at most +0.32 at the top of
the interval** — under a sixth of a fantasy point through §2's bands. This is not a power failure
(§4.24b's distinction): the interval itself rules out anything that would matter.

Worth recording because it nearly shipped the other way: with only the team-season swept out the
same coefficient is **+0.033, p=0.034** — significant, and entirely opponent quality. One extra
control moved it to null. Doc 265's D/ST baseline did the same thing yesterday.

**And the reason the channel cannot work is structural.** Defensive plays faced barely varies between
teams at all: across quintiles of own-offence quality it runs **61.3, 62.2, 61.9, 62.6, 61.9** plays
a game — a 2% spread. A bad offence does not leave its defence on the field more. The NFL's play
count is close to a constant.

**Claim B, the crater: confirmed, and it does not run through snap count.** D/ST fantasy points
against his own offence's EPA per play in quarters one to three: **+3.22 per unit, CI [+2.08, +4.31],
p<0.0001**, which is **+0.65 D/ST points per standard deviation**. Own three-and-outs: **−0.35 each,
p=0.0001**. Plays faced, whole game: **−0.015, p=0.32 — null**, and adding it to the EPA model leaves
EPA untouched at +3.19. So the mechanism is field position and score state, not fatigue.

**It is a floor effect, not a gradient**, which is the useful shape:

| own offence that day | D/ST points | points allowed |
|---|---|---|
| worst fifth | **4.08** | **24.24** |
| second | 5.66 | 21.82 |
| middle | 5.85 | 21.12 |
| fourth | 5.72 | 21.28 |
| best fifth | 5.99 | 21.63 |

Only the bottom fifth is punished, and it is punished by **−1.73** against the other four pooled.

**Between teams the same thing holds and this is the version that decides a hold.** Across 160
team-seasons, own-offence EPA against the defence's own D/ST average: **r=+0.304, p=0.0001**. Bottom
quintile of offences average **4.61** D/ST points a week; top quintile **6.36**. League mean 5.43,
replacement 5.99 (doc 265).

`[TESTED, n=2,576 defence-games and 160 team-seasons]`

**Not yet run, input named (§0.5a4).** His health point — *"We will need to follow health checks along
both sides of the ball"* — is the right extension and it is one release away: nflverse's weekly
injury report, already used in doc 133, keyed to the same team-weeks. The testable form is *does a
defence's own starting quarterback being out move its D/ST output, over and above the offence-EPA
term above*. Queued, not run.

---

## 4. Red team of the Cleveland conclusion, since he asked for one

Doc 266 said: hold Cleveland, its best stretch is weeks 9–14 and its worst is the playoffs. Four
things are wrong with the confidence of that, and one new thing is wrong with the conclusion.

**The model is small.** The two terms are shrunk by 0.325 and 0.269, so the week-to-week spread it
predicts for one defence is roughly **two points** against a measured weekly standard deviation of
**6.28** (doc 265). On any single week the schedule read is a third of the noise. It only shows up
over a long horizon, which is doc 264's own finding read honestly.

**Its week-to-week ordering rests entirely on the weaker term.** Cleveland's own-quality number is a
constant added to every one of its weeks, so the *ranking* of week 9 above week 16 comes only from
the opponent-generosity term — one season of input, 2026 rosters changed, no 2026 games played.

**A rank is not a margin.** "Rank 4 in week 5, rank 13 in the playoffs" reads like a cliff. The
predicted gap between those two weeks is about a point and a half.

**And the new strike, which doc 266 did not have.** Cleveland was the **fifth-worst offence in the
league by EPA per play in 2025** (rank 28 of 32), and §3 above measures a bottom-quintile offence at
**−0.8 D/ST points a week** relative to the league mean. That cuts against holding them.

**Two things push back, and this is why the verdict survives rather than flips.** Cleveland's defence
scored **6.69 a week in 2025** — above the league mean of 5.43 and above replacement — *with that
same bad offence already in place*, so subtracting the offence penalty again is partly double
counting; doc 266's own-quality term is measured on outcomes that already contain it. And the
alternative is not better: on his roster the best free body is below his worst startable man at every
position (doc 259).

**Verdict, honestly labelled.** Hold Cleveland, and hold it as a **default rather than a finding**.
The whole decision is worth one to two points a week against a weekly spread of six, and the thing
that would actually change it is not a schedule table — it is a second defence with a complementary
calendar, which is §2.

**Still open.** Doc 10 puts the whole 32-team weeks-15–17 spread at ≤5.5 points and says it is not a
playoff-planning tool; §4.26(b) puts the tight-end draw at +3.39 per standard deviation. Same window,
same position, different methods. That contradiction is still unresolved and doc 266 leaned on the
second one without saying so.

---

## 5. The receivers, which is what he actually asked about

His question: *"For WR i think you said young and high pedigree was the upward trend. Are any of
those still out there that could rise? I guess not since you mentioned first round picks?"*

He is right about the screen and wrong to assume it is empty. Two measured screens, from §4.28 and
§4.30:

- **A first-round rookie receiver behind an incumbent.** 9 of 15 out-targeted the incumbent in year
  one against 7.4% for everyone else (Fisher p=0.000001), and 6 of those 9 were startable — 40% of
  all first-round rookies in that spot. It is a round-1 event: NFL rounds 2–3 measured 3.3%.
- **The three-signal screen on young non-startable receivers.** NFL rounds 1–3, yards per target
  above 7.13, targets per game above 3.20. Clearing all three: **39.4% became startable**, against
  0–7% for two or fewer, p=0.0000.

Scored against the free pool as of the Sept 8 snapshot — this is a snapshot, not live ownership, and
`py wire.py` is what confirms it:

| screen | player | what it rests on |
|---|---|---|
| first-round rookie | **Omar Cooper Jr.** (NYJ, NFL pick 30) | draft capital is the whole signal; no NFL line yet |
| three of three | **Ricky Pearsall** (SF, pick 31, year 3) | 10.34 yards a target on 5.89 targets a game, 8.09 ppg in 9 games |
| three of three | **Pat Bryant** (DEN, pick 74, year 2) | 7.71 and 3.77, 4.56 ppg in 13 games |
| three of three | **Jalen McMillan** (TB, pick 92, year 3) | 11.87 and 3.75 — but on **4 games**, so both rates are thin |

**Pearsall is the one.** He is the only free player clearing both halves of the pedigree story — a
first-round pick *and* three of three — and 8.09 points a game sits just under the 9.62 startable bar,
which puts him squarely inside the population where the 39.4% was measured. The honest counterweight
is on the same row: nine games in 2025 is the `12g` warning, and §4.22 measures a receiver who missed
time at −19 points the following year. §4.25b's qualifier applies in his favour — the penalty is
carried by players who wash out, and a year-3 first-rounder has not yet been filtered — but it is a
two-sided row and I am not going to print only one side of it.

Five first-round rookie receivers exist on the board; four are rostered (Tate, Tyson, Lemon,
Concepcion). Nine receivers clear three of three; five are rostered, and one of those is **Xavier
Worthy, who is his** — worth knowing that his own week-one starter is on the screen.

**What shipped, so this is a column and not a paragraph.** All committed to his drive:

- `Scripts\research\build_pedigree.py` — writes `Source\pedigree_2026.csv` from the board spine,
  nflverse draft picks, 2025 receiving built from play-by-play, and `games_2025.csv`. Standard library
  only, paths resolved against the script, and it **refuses to write** if fewer than 150 board rows
  match a draft pick, because a broken join and a thin draft class look identical in the output.
  Ambiguous name matches are skipped, not defaulted (§3, and doc 251's `?` rows).
- `Source\pedigree_2026.csv` — 291 of 482 board rows now carry an NFL round and pick. 14 carry a
  screen.
- `Source\nfl_draft_picks.csv`, `Source\rec_2025.csv` — the two static inputs, committed so this
  reproduces without network.
- `Scripts\wire.py` — gains **lane 3, "potential, not today's value"**, printed above lane 1, plus
  the screen appended to any lane-1 row that carries one. Its loader was run against three controls
  before shipping: file present (14 rows), file absent (names itself missing), and file present but
  screening nobody (also names itself). §0.2 — a guard that has never fired is not a guard.

---

## 6. Two pins that have been failing since draft night

While re-pinning `wire.py` I checked the two kit files a keeper swap rewrites:

| file | pinned | actual |
|---|---|---|
| `board_v8_fixed.csv` | 41,100 / `0798189eb807c11d` | **41,583 / `724b9a3ce17ad565`** |
| `player_context.csv` | 109,468 / `96f92c5fa2ea9d70` | **109,734 / `05cf588eb81e9947`** |

Both were rewritten by the 7:00 PM keeper swap on Sept 7 and neither pin was updated, so
`check_kit.py` has reported two mismatches on every run since draft night and nobody read them. That
is doc 260's failure again, three days later, on the two most important files in the tree. Both
re-pinned, `wire.py` added to the manifest and to the scanned list.

Also on the drive and not addressed: `Source\00_PROJECT_DIRECTIVE-1.md`, byte-identical to the live
directive at 155,691. A second name for one file, which is the collision §0.5(c)4 keeps naming.

---

## 7. Open threads, by name

- **Not yet run:** the health extension to §3 — nflverse weekly injury reports against D/ST output,
  both sides of the ball, testable form written above.
- **Not yet run:** the realistic pairing test. `pairs.py` measures the *ceiling* — the best pair among
  all 32. What Matt described is choosing a partner from the defences other managers drop, which needs
  the week-by-week free pool doc 252 already rebuilt.
- **Open:** doc 10 versus §4.26(b) on the weeks-15–17 tight-end draw. Settle before any
  playoff-planning tool leans on either.
- **Matt's, on his list:** `py wire.py` (confirms whether Cooper, Pearsall, Bryant and McMillan are
  still free, and prints lane 3 for the first time), `py waivers.py --check`, and confirming the PFF
  extension is read-only.
- **Directive change owed and still held:** §4.33 should carry the corrected version of his potential
  instruction — potential is the sort key on the job and pedigree lanes, current value on the
  start-this-week lane. Held until the §6/§7/§8 phase split, because the paste is already at the
  limit of his clipboard.
