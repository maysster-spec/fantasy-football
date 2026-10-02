# DIRECTIVE DRAFT BOOK: THE DRAFT-SIDE SECTIONS OF `00_PROJECT_DIRECTIVE.md`, MOVED WHOLE AT v9.8

*Moved out of the resident directive on 18 Sept 2026 (doc 367), word for word. The 2026 draft was on
7 Sept; nothing here is read in season and all of it is needed again in August 2027. Section numbers
are kept as they were so a cross-reference from the directive or a numbered doc still lands here.
Contents, in this order: §2.1 (b2) to (e) and the turn structure · SECTION 5, the opponent model ·
SECTION 6's draft-night QB2 and TE2 argument and doc 12's waiver table · SECTION 7, the output
contract · SECTION 8, the refresh schedule and the draft-night runbook · SECTION 9's two rows on the
draft-night kit.*

---

## FROM SECTION 2.1: (b2) THE KEEPER FEED, (c) THE DEPLETION TABLE, (d) IMPLEMENTATION, (e) `eff_pick`, AND THE TURN STRUCTURE

**[v5] (b2) ESPN puts the 12 keepers INSIDE the live pick feed at overall 169–180.** Verified on
the real 2024 and 2025 drafts (12 rows, round 15, picks 169–180, both years). Any tool reading
`draftDetail.picks` must **filter `keeper == True` before counting picks** — they mark players
taken but must not advance the clock. Counting them put the live board 12 picks ahead and it
never fired (doc 58).

**(c) Depletion timing.** All 12 keepers are on rosters when the draft opens and are never
available. The round-15 accounting is bookkeeping. **The pool is depleted from pick 1 onward.**

**[v5] Corrected table** — solved as a fixed point on the **08-23** keeper ADPs. Three rows of
the v4 table were wrong; the pick-32 row was wrong by 2:

| Pick | Rd | Keepers gone ahead | Effective ADP available | v4 said |
|---|---|---|---|---|
| 8 | 1 | 0 | ~8 | same |
| 17 | 2 | 0 | ~17 | same |
| **32** | 3 | **4** | **~36** | ~~5 / ~37~~ · v5 said 3 / ~35 |
| 41 | 4 | 10 | ~51 | same |
| 56 | 5 | 10 | ~66 | same |
| 65 | 6 | 10 | ~75 | same |
| **80** | 7 | **11** | **~91** | ~~10 / ~90~~ |
| **89** | 8 | **11** | **~100** | ~~10 / ~99~~ |
| **104** | 9 | **12** | **~116** | v5 said 11 / ~115 |
| **113** | 10 | **12** | **~125** | v5 said 11 / ~124 |
| 128 | 11 | 12 | ~140 | same |
| 137 | 12 | 12 | ~149 | same |
| 152 | 13 | 12 | ~164 | same |
| 161 | 14 | 12 | ~173 | same |

**The 32→41 jump is 4 → 10 keepers, steeper than v4 implied — but pick 32 is one pick shallower
than v4 claimed.** Anyone planning pick 32 off the v4 table was one player too deep.

**[v7.1] AND THE v5 TABLE WENT STALE THE SAME WAY, ONE REFRESH LATER.** It was solved on the
**08-23** keeper ADPs; `refresh_adp.py --write` re-froze the market on the **09-03** pull on Sept 3
at 13:18, and three rows moved: **32 (3→4 keepers, ~35→~36)**, **104 (11→12, ~115→~116)** and
**113 (11→12, ~124→~125)**. Re-solved as the same fixed point on the 09-03 keeper ADPs
`[28.2, 29.4, 29.4, 32.9, 41.0, 42.2, 42.4, 44.2, 45.1, 47.3, 78.7, 101.6]`; the other eleven rows
are unchanged. **This table is a FUNCTION OF THE ADP FREEZE and must be re-solved whenever
`refresh_adp.py` writes** — including after the Sept-5 refresh. `Scripts\research\audit_directive.py`
re-checks it, and everything else quoted below, against the shipping files.

**(d) Implementation.** Any simulation must remove all 12 keepers **before pick 1**, not at round 15.

**[v5] (e) `eff_pick` is the keeper-depleted coordinate** (`adp_pick − keepers ahead`) and is the
correct input to the opponent model, because §4.12's noise was fitted in depleted space. Do not
"correct" it back to raw ADP.

**Turn structure:** gaps alternate 9 then 15 picks. Two decisive windows: **17→32 is the longest
gap; 32→41 has the steepest attrition.** Plan both.

---

## SECTION 5 — OPPONENT MODEL

**[v8.5, 2026-09-09 — THREE SLOTS WERE WRONG AND TWO TEAMS RENAMED AFTER THE DRAFT. Corrected
against Matt's own League Members screen and the 2026 draft recap's first picks (§3: an uploaded
source is ground truth). Slots 1, 4 and 5 were a three-way rotation. Doc 238.]**

| Slot | Manager | 2026 team name | 1st pick | Read |
|---|---|---|---|---|
| **1** | **herman allen (WGTS)** | We Got This Sh!t | 1 (Gibbs) | Checked out by midseason. **The only CURRENT manager who has ever taken a TE in round 1 or 2** — Bowers at 22 in 2025. **HOLDS 1.01. Picks 1, 24, 25** — ~~"picks 20, 29"~~ was wrong and came from the bad slot. |
| 2 | Fleming (FLEM) | NickCannonFanClub | 2 (Bijan) | **Weakest** — bottom-3 four straight years |
| 3 | Ray (**ART**, not AAT) | Seasick of Losing | 3 (McCaffrey) | Very active, poor results |
| **4** | **Cary (DUCK)** | **CeeDees Nuts** *(was `ChatCTE` on draft night)* | 4 (Chase) | Hyperactive, volatile. ~~Holds 1.01~~ — **he does not; allen does.** ~~Graded LAST in 2026, −109.6.~~ **[v9.4] Void: the grade's back half is retracted (§4.29).** Picks 4, 21, 28, 45, 52, 69, 76, 93, 100, 117, 124, 141 |
| **5** | **Brown/Collins (TURD)** | Window is Always Open | 5 (Cook) | Declining. **Picks 5, 20, 29** |
| 6 | Kam (BC) | Bloodied Castaways | 6 (J. Taylor) | Low churn, won 2024 |
| 7 | Grenier (**LOOP**, was BATE) | **Lamar's Loops** *(was `Jaxson Bates`)* | 7 (Achane) | Most active, mediocre results |
| **8** | **MATT (JUG)** | The Poetry of Junkyard Juggers | 8 (Nacua) | — |
| 9 | **Snyder (Boo)** | Send'em Packin | 9 (Josh Allen) | **Most predictable. Bills homer — Allen 4-for-4 at his turn when available (2.21, 2.23, 2.21, then 1.01 OVERALL in 2025); the 2024 miss was a two-pick snipe [v5.4, doc 70].** Picks 9, 16 |
| 10 | Rychlicki (POT) | The Kunning Stunts | 10 (JSN) | Trending up. TE keeper locked — not a TE threat |
| 11 | Taylor (???) | Multiple Scorgasms | 11 (St. Brown) | **Best manager**, never worse than 5th |
| 12 | Lobsinger (Tets) | **Tets Out For The Boys** *(was `Breece up those Tets`)* | 12 (Barkley) | Reigning champion. ~~Graded 1st in 2026, +128.5~~ [v9.4] the grade past round 6 is void (§4.29) |

**NEVER MATCH A MANAGER BY TEAM NAME. Match on the ABBREVIATION, or on the first pick of the
draft.** Three teams renamed between the draft and Sept 9, and two of them changed abbreviation as
well. The mapping above was rebuilt from the recap's first picks, which cannot be renamed.

**Nobody autodrafts. All twelve are engaged.**

**[v7.2] THE EARLY-TE PICTURE, RE-DERIVED — doc 180 `[TESTED, n=45 manager-seasons, true
selections only, 2022–2025]`.** §5's herman-allen line is correct **for rounds 1–2** and
misleading **at Matt's pick 32, which is round 3.** First TE taken, by OVERALL pick:

| overall | manager | year | player |
|---|---|---|---|
| 20 | Pierce *(departed — not in the 2026 league)* | 2023 | Kelce |
| **22** | **herman allen** | 2025 | Bowers |
| **30** | **Cary** | 2022 | Kelce |
| 35 | *Matt himself* | 2025 | Kittle |
| 37 | Rychlicki | 2022 | Pitts |
| **41** | **Wilson Kam** | 2024 | Kelce |
| 45 | Brown/Collins · Grenier | 2024 · 2025 | Andrews · LaPorta |

**3 of 45 at overall ≤32; 6 of 45 at ≤41.** On 2026 slots the picks between Matt's 17 and his 32
belong to **Kam (19, 30), allen (20, 29) and Cary (24, 25)** — and all three of those managers
have taken a TE at overall 41 or earlier. **Six picks by three TE-capable managers sit between
Matt's turns, and §7's pick-32 tie contains Bowers and McBride.** Rychlicki is not a threat this
year — his keeper is a TE (Loveland), so he cannot keep one and draft one early. Treat the
survival of a premium TE to 32 as materially less certain than "one early-TE manager" implies;
this is a reason to take the tie's TE **on sight at 32**, not to reach at 17.
**Doc 176 reported this as "§5 is FALSE" on a count of round-3-or-earlier picks read against a
round-1-or-2 claim. The concern was right, the arithmetic was mislabelled, and the correction is
the table above, not the retraction.**

**QB timing (avg round of first QB):** early — Ray 2.5, Kam 2.8, Snyder 3.0, Fleming 3.2. Late —
Rychlicki 5.2, Lobsinger 6.0, allen 7.2, Taylor 7.8.
**Ray, Kam and Fleming pick at 22, 19 and 23 — all after pick 17. Snyder is the only early-QB
manager inside the 8→17 window.**

**[v5] Simulated opponents** must draft from a cheat sheet, not blindly down ADP: take the best
VBD among the ~22 nearest the top of their noisy board. Calibrated against doc 41's finding that
a VBD rule is statistically level with these managers. **Never quote a simulated absolute win
probability** — Matt's board and the scoring share one projection, so absolute numbers are
artifacts. Relative comparisons only.


---

## FROM SECTION 6: THE DRAFT-NIGHT QB2 AND TE2 ARGUMENT AND DOC 12'S WAIVER TABLE (they followed the Spears block)

**[v6.6] THE MEASUREMENTS NOW DISAGREE WITH THE LAST BULLET, AND THAT IS MATT'S CALL, NOT MINE.**
§4.18b (doc 138) and §4.18c (doc 139) between them say that at picks **104 and 113 specifically**,
a Goff-tier-or-better QB2 beats the RB — the keeper option that used to justify the RB is ≈ +0.7,
and the board's apparent tie exists only because the rollout cannot see missed weeks. **Everything
else in this doctrine survives untouched and is REINFORCED, not challenged:**
- **Never three QBs, never three TEs** — untouched; `CAPS = {'QB':2,'TE':2}` verified holding in
  200 of 200 engine-driven drafts (doc 139 §6).
- **Complementarity, and NOT the same bye week** — now MEASURED, not just preferred: a same-bye
  QB2 adds **+0.00** to the lineup because he never starts (§4.18c).
- **Bench RB to the cap, then WR** — untouched; it rests on §4.19 (Matt's own waiver record), which
  doc 138 does not touch.
The single point of conflict is *when* the second QB comes, and only at 104/113. **Surface it, do
not silently apply either side.** If Matt says the doctrine governs, the doctrine governs — it is
his roster and the measured edge is ~+4 to +10 points on one measurement per side.

**[v5.7] TE2 — doc 92 measured +4.07 ± 2.54, contradicting doc 12's −13.4.** It is 1.6 sd from
zero on machinery whose FLEX handling is unstated, against a shipped-board FLEX comparison where
the best RB/WR out-projects the best TE by 24.0 / 37.6 / 4.8 / 16.7. **Not actionable. Matt's §6
doctrine governs the night. Filed for post-draft review.**

**TE is a different question and must not be answered by analogy to QB.** **FLEX is RB/WR/TE**
(settings line 39), so a TE2 has a lineup path a QB2 never has. ~~and the best late TE (Andrews)
sits at exactly 0.0, not below it.~~ **[v5.6 — that clause is VOID, same broken premise: TE12 is
not the TE streaming baseline either. Measured TE waiver return is 5.53 ppg; Andrews is 8.25, so
he is +2.72/week over a real streamer, ~+8 over three starts, NOT zero.]** **But a FLEX slot compares RAW PROJECTED POINTS, not
position-relative VBD** — and on the shipped board the best FLEX-eligible RB/WR beats the best TE at
all four bench picks by **24.0 / 37.6 / 4.8 / 16.7**. So TE2 loses *on this board*, not in principle.
**Re-check if a REBUILD verdict changes the late-TE bodies.**

**[v5.6] The TE2 CONCLUSION survives; one of its stated REASONS does not.** What carries it is the
FLEX opportunity cost above, plus doc 12's measured **−12 to −13** for TE2 and §4.13 (TE's edge is
floor, and floor is the wrong thing to buy after round 9). It is NOT carried by "Andrews is
replacement level" — that was the retracted premise. Cite the right reason.

**[v5.6] It WAS measured, and I said it was not — doc 12 (F34), 951 executed adds:**

| pos | waiver ppg | **hit rate** | VBD replacement ppg |
|---|---|---|---|
| **QB** | 15.25 | **0.62** | 20.09 |
| TE | 5.53 | 0.42 | 8.25 |
| WR | 6.54 | 0.31 | 9.62 |
| **RB** | 5.43 | **0.22** | 9.92 |

**This is the most decision-relevant table in the project and it points the opposite way from the
usual intuition.** QB is the position Matt CAN replace off waivers — 62% of QB adds returned a
startable week, the best rate of any position. RB is the one he CANNOT — 22%.

**So "bench RB to the cap, then WR" is correct, but not for the reason either of us gave.** It is
not that RB2s outscore QB2s. It is that **an RB hole cannot be patched mid-season and a QB hole
can.** Draft the position waivers will not save you at.

**And that same table is the argument AGAINST QB2:** the +10 assumes a *generic* streamer. Doc 11
already flagged that a manager who streams QB well shrinks it further, and a 62% hit rate is what
streaming well looks like. **The honest verdict: QB2 is worth roughly +10 under generic streaming,
less for Matt, against a round-9 dart whose §4.13 upside is real but unpriced. A genuine coin flip
— NOT a closed question, and NOT something to re-derive at the draft.**

---

## SECTION 7 — OUTPUT CONTRACT

**Every reply obeys §0.1 first.**

**PREP MODE** — per pick:
```
PICK [overall] — Round [n]
PRIMARY:   [player] | pos | VBD | bye | p(avail) | one-line why
FALLBACK:  [player] | pos | VBD | bye | p(avail)
THIRD:     [player] | pos | VBD | bye | p(avail)
CLIFF:     [tier breaking before next turn, or none]
BYE CHECK: [conflicts with current roster]
```

**RANKINGS MODE** — ESPN custom rankings are drag-and-drop only. Output **divergences from
ESPN's default board**. Lead with block moves. Under ~40 moves. Apply §4.4's ESPN column.

**LIVE MODE** — under 60 words. Best available, one alternative, one cliff warning. No preamble.

**[v5.5] The live board's ACTUAL columns — this had been wrong since the UI rewrite and both the
guide and the draft card inherited the error (docs 79, 82). Internal names are `roll`/`mv`/`hold`;
NONE of them appear on screen. Never name them to Matt.**

| on screen | internal | what it is |
|---|---|---|
| **VBD** | `vbd` | points above a replacement starter |
| **adds now** | `mv` | what he adds to the STARTING lineup today |
| **if I wait** | `hold` | best same-position player at the next turn |
| **Δ** | `delta` | `mv − hold`. **Tempo. NOT the sort key.** |
| **cost vs #1** | `roll − best` | **this orders the list.** `free` = the recommendation |
| **p(next)** | `p_next` | survival to the next turn |

**The rows are sorted by `roll`, and `roll` is never displayed** — `cost vs #1` is its only visible
form. The headline number must be the one that decided the pick: it is the **rollout margin over
the runner-up**, not Δ. Showing Δ there let the largest bar on the page belong to a row the engine
did not pick (doc 79).

**[v6.6] THE LIVE BOARD IS A FIXED SHAPE — doc 139.** Exactly **12 player rows and 3 tier rows**,
every refresh, from pick 1 to the end. It used to render 10 rows on Matt's turn and 8 while
waiting, so it changed height every pick and everything below it moved. Verified across 73 draft
states: one shape, `[(12, 3, 0)]`. **If it ever renders a different count, something is wrong —
say so rather than explaining it.** Render cost is now **0.4s waiting / 3–4s on the clock** (was
4s / 16–20s), and the bridge polls every **0.5s**.

**[v6.7] PICK 32 — THE TIE IS REAL, AND IT IS NARROWER THAN THE BOARD'S. TAKE THE ENGINE'S #1;
DO NOT OVERRIDE IT — doc 140 (Fable), reviewed doc 142. THIS CORRECTS v6.6.**
v6.6 said "pick 8 the engine decides; pick 32 Matt decides," from doc 139's **0.15-point converging
margin**. That was measured on **ONE board state**. Across **100 states** from the §5 opponent
model, run through the production `Engine` at `top=12, rollout_inner=60`: median margin **3.65**
(IQR 2.05–7.98), only **9 states under 1.0**, and the engine's #1 is one of six core names in
**88 of 100**. The engine is not confused at 32. `[TESTED, N=2000 paired drafts, in dollars]`
- **THE TIE (any of them, first one showing):** Bowers · McBride · Kyren Williams · Judkins ·
  Lamar — plus **Hall on sight** if he slips. Policy spread across all five: **$2.7**. All nine
  head-to-head pairs span zero and resolving them needs 6,000–12,000 drafts. **Do not chase it.**
- **NOT IN THE TIE, though the board may show them within a point:** Burrow **−$24**, Stafford
  −$23, Daniels −$21, Egbuka **−$20**, Swift −$20, Hurts −$20, Warren −$15, Adams −$14, DeVonta
  Smith −$10 — all CI-clear. **The engine's #2 row at 32 is a QB in 47 of 100 states (Burrow 39).**
  Points and dollars agree on every one, so the payout convexity is not what separates them.
- **The availability haircut does not reorder the tie** (§4.22(c) as a sensitivity, not merged): it
  moves one name — Nabers, 4 games in 2025, **+$27 [+6, +49] → +$3 [−16, +24]** — and pushes
  Burrow and Daniels to −$30.
- **On-clock `rollout_inner` is 60** (was 24); that also removed a winner's-curse bias that
  inflated small margins.
- **The one soft spot (doc 142 §4a):** QB survival rests on raw ADP plus noise — §4.12 fits a TE
  shift and Snyder-on-Allen and **nothing for QBs generally** — while §5's timing table has four
  managers taking their first QB in rounds 2.5–3.2. A real QB run makes waiting worse, **bounded
  by the QB2→QB6 plateau at 11.8 points (§4.15)**, which halves the penalty and leaves the verdict
  intact. Watch the room for a QB run; do not re-derive the number at the table.
**Still true, and now priced rather than asserted: spend the 60 seconds on the analyst read and the
UNSETTLED flag AMONG THE FIVE.** The board's "coin flip" tag is right about whether to agonise and
wrong about who is in the flip.
**[v6.6, retained] Pick 8 replicates a third time:** ten seeds at three sample sizes, St. Brown
10/10, margin 19.96 → 20.20; doc 140's independent state generator agrees in **96 of 100**.
**[v7.8] AND ALL OF THAT WAS ONE STATE — THE PICK-8 RULE IS "HIGHEST VOR ON THE BOARD" — doc 200.**
§4.2 defines the modal pick-8 state as *"top seven by `eff_pick` gone"*, and the top seven **are**
Gibbs · Bijan · Chase · **Nacua** · Taylor · JSN · **McCaffrey**. So every published pick-8 run —
doc 139's ten seeds, doc 140's 100 states, doc 182's thirteen — removed the three players who beat
St. Brown **by construction**. St. Brown is #1 because he is the best player *expected to still be
there* (eff 8.38), not the best player: Nacua **+131.3**, McCaffrey **+134.9** and Taylor **+122.5**
all out-VOR his **+101.3**. Measured on the production `Engine`, `top=12, rollout_inner=60`:

| state | engine #1 | over | margin |
|---|---|---|---|
| top seven gone (published) | St. Brown | Henry | **7.90** *(reproduces v7.2's 7.8 — the control)* |
| Nacua survives | **Nacua** | St. Brown | **25.70** |
| McCaffrey survives | **McCaffrey** | St. Brown | **26.60** |
| Taylor survives | **J. Taylor** | St. Brown | **15.70** |

**AT PICK 8 TAKE THE HIGHEST-VOR PLAYER ON THE BOARD:** Gibbs · McCaffrey · Bijan · Nacua ·
J. Taylor · Chase · JSN · **St. Brown**. The engine agrees in all four states at margins of 8 to 27
— an order of magnitude outside anything this project calls a tie. **Pick 8 is still closed; what
was never written down is that it was closed CONDITIONAL ON THE ROOM.** Quote no survival
probability for the slip (§4.15). Found by Matt reading the DRAFT BOARD GRID for the first time and
asking why his pick-8 cell said Nacua.
**[v7.5] PICK 56 IS THE LAST UNFIXED INSTANCE OF THIS DEFECT — `ERROR_PATTERNS` A19.**
Doc 139's pick-56 number ("10/10 at margin 2.77") was measured the same single-board way as the
retracted pick-8 "20" and the retracted pick-32 "0.15". **It has still not been re-checked.**
What CAN be said without a simulation, from the board itself: at pick 56 the best available by VOR
is **Stafford +21.19**, then **Odunze +19.42** — a cushion of **1.77**, against 14.19 at pick 17
and 5.9 at pick 8. **Pick 56 is the thinnest turn on the board and the live board decides it, not
a plan.** Do not carry a pick-56 preference into the room; read `cost vs #1` and take `free`.

**Survival odds:** use FantasyPros Pick Predictor numbers when supplied. Otherwise report
simulated probabilities and **label them simulated.** Simulated numbers have run low against
every checkable observation — **treat them as lower bounds.** **[v5] And never past pick ~120
without the §4.14 caveat.**

**Every prep session ends with:** top 3 assumptions, what would invalidate each, and which missing
input would most improve the analysis.

---

## SECTION 8 — REFRESH SCHEDULE AND DRAFT-NIGHT RUNBOOK

- **Sep 5 (T-48h):** re-export projections and ADP; news search on shortlist; **record the
  capture date**. **[v5.2] The `SCORING` patch (ids 19/26/44), the minute-stamped filenames, the
  `PULL REJECTED` gate and the reconciliation `else` are DONE and verified live in both script
  locations on Aug 28 — the file is 13,037 bytes. Verify that size; do not re-patch.** **[v5.4] Superseded: the pull script now also carries the completed-season guard and writes its CSVs to `Source\` — current size 15,194 bytes. `py check_kit.py` is the verifier; never a byte count quoted in prose.**
- **[v5.5] The Sep 5 VERDICT is GATED (doc 81).** `PULL REJECTED` only *prints* — the pull script
  still writes the CSV and still exits 0, so an ungated `sept5_check.py` would take the corrupt
  file (it picks the newest) and print an authoritative FREEZE on garbage. `refresh_pull.bat` now
  branches on the exit code **and** on the rejected string, and `sept5_check.py` re-checks the
  ≥400-live-projections invariant itself. If either fires, the answer is "run it again" — never
  "read the verdict anyway."
- **[v6.8] A REBUILD VERDICT HAS NOTHING TO RUN, AND THAT IS THE ANSWER — docs 143 + 144.**
  `sept5_check.py` contains no `to_csv` and imports no builder: **it only reports.** And the board
  cannot simply be re-derived from the pull either — that was tested. The arithmetic is trivial
  (`vbd` = proj − §4.1 replacement to 0.0004; `rank` = vbd rank 480/480; the pull's `proj_2026`
  is the same league-scored quantity, r=0.9925) — **but `board_audit.py` goes 39/39 → 35/39**,
  because it requires `proj_leaguepts` to equal **`code_universe_v5.csv`, the SPINE**, at 1e-6:
  *"projections must equal the spine's, not a re-derivation."* **It is the SPINE that has no
  current builder, and that is doc 62's finding stated correctly.**
  **So: take doc 62 §5 Option A, and run `py mkoverride.py`** — it prints every player inside pick
  175 whose projection has moved 15+ points, recomputed onto one scale, with any
  `news_overrides.csv` row flagged as HOLDING against the pull. On 09-03 that was six names, all
  rank 90+, and the top of the board had not moved. `refresh_proj.py` exists, is QUARANTINED, and
  is most of the real fix once the spine is rebuilt post-draft.
- **[v6.6] A REBUILD verdict also means RE-RUN `py bench_lineup.py`** (doc 139). `_lineup()` is
  now pure Python and is bit-identical to the numpy original over 18,728 production calls — but
  the one input that could break that equivalence is a **NaN projection**, which numpy sorts last
  and Python does not order at all. Nothing on the shipped board has one; a rebuilt board could.
  The check takes about a minute and prints `EXACT AGREEMENT`.
- **[v5.5] A REBUILD verdict invalidates THREE files, not one** (doc 82): `board_v8_fixed.csv`,
  `FALLBACK_BOARD.pdf` (its 180 rows) and `DRAFT_CARD.pdf` (its QB and TE tiers). The Aug-29 margin
  was **151/161 against a threshold of 150** — one player. Do not treat FREEZE as the default.
  **[v6.9] It is FIVE now (doc 146):** add `DRAFT_BOARD.pdf` — the board Matt actually drafts from,
  which doc 116 made the desk copy and which nothing in the Sep 5 sequence was rebuilding — and
  `VALUE_LADDER.pdf`. `sept5_after.bat` rebuilds all of them; `py to_pdf.py --check` names any that
  are still behind their page.
- **[v6.9] AFTER THE REFRESH THERE IS ONE COMMAND: `.\sept5_after.bat` (doc 146).** Ten steps, in
  dependency order, about three minutes: `refresh_adp` (look → prompt → `--write`) → `board_audit`
  → `depth_map` — **these three are gates and stop the run** — then `make_board` → `make_fallback`
  → `mkoverride` → `parse_ladder` → `mkvalue` → `to_pdf` → `sync_desk_copies`. Run it **whatever
  the verdict says**: FREEZE/REBUILD is about projections, and between the Aug-23 and Aug-30 pulls
  the projections moved on 47 of the top 161 while ADP moved on **160 of 161**. Steps 4–8 do not
  halt the run; they record which printout failed and the run ends naming what is now stale.
  Finish with `py make_shortcuts.py`, which re-points the dated Desktop links. **`after_pull.bat`
  was my duplicate of this file and is now a stub that calls it; it can be deleted.**
  Two corrections folded in: it was running `make_sheets.py` (the three sheets doc 116 retired)
  and **never running `make_board.py`**, the builder of the board Matt actually drafts from.
- **[v6.9] `wkhtmltopdf` IS NOT INSTALLED ON MATT'S MACHINE, AND EVERY PDF BUILDER DEPENDS ON IT
  (doc 146).** Verified from his own console, not inferred. `make_board`, `make_fallback`,
  `mkvalue`, `mkoverride` and `make_sheets` all write an `.html` and then shell out; four of the
  five print a line and **exit 0**. So the page rebuilt, the PDF did not, and `sync_desk_copies`
  copied the old PDF to the desk with an `OK` and a byte count. **`py to_pdf.py` makes them with
  Chrome instead — no install** — and `sync_desk_copies.py` now **refuses** any PDF older than the
  page it came from. Chrome maps 1 CSS px to 1/96 in where wkhtmltopdf assumes 1024px, so the
  renderer injects a **measured zoom of 0.78**, which reproduces wkhtmltopdf's page count exactly:
  board 7=7, ladder 3=3, backup 2=2 (at 1.0 the board is 12 pages). `DRAFT_CARD` and
  `DRAFT_DAY_GUIDE` are deliberately excluded — `card.html` declares landscape while the PDF on the
  desk is portrait, so rebuilding would silently rotate the card Matt has already read.
- **Sep 7, 7:00 PM:** keeper lock — swap predicted for actual, rebuild the board, **re-inject the
  prerank file**, restart the live tool. **[v5.5] `draft_night.bat` defaults the rebuild prompt to
  Y**: rebuilding an identical board is a verified no-op, skipping a needed one leaves a
  wrongly-removed player invisible all night. The costly direction must never be what a fumbled
  keypress picks.
- **[v6.6] Sep 7, 7:50 PM — START `bridge_server.py` FIRST, and load the Chrome extension.**
  Doc 136 proved ESPN's read replica publishes a draft **only after it ends**, so the plain
  `py live_draft.py` path CANNOT work on the night. The order is: `py bridge_server.py` → open the
  draft room in Chrome with the `espn_bridge` extension loaded → `py live_draft.py --bridge`.
  The listener resets `bridge_picks.json` on startup and stamps it, and the board refuses a file
  older than six hours. Confirmed end to end on 2026-09-02 (179 picks captured live).
- **[v6.6] `bridge_picks.json` is now written ATOMICALLY and the board holds its last complete
  read** (doc 139). If you ever see `bridge file went BACKWARDS`, the listener was restarted
  mid-draft — **restart the board too**, the picks it missed are gone.
- **[v6.9] `draft_night.bat` NOW DOES ALL OF THAT ITSELF — it did not, and that was live (doc 146).**
  Its step 5 was still `cd live_draft` + `py live_draft.py`: the old board, against the feed doc 136
  proved is empty until the draft ends. It would have shown nothing all night and said nothing about
  it. Step 5 is now three sub-steps — start the listener in its own window, load the extension and
  open the draft room, then `py live_draft.py --bridge`. **`draft_night.bat` and `sept5_after.bat`
  are now PINNED in `check_kit.py` for the first time**: a batch file that drives a whole evening is
  exactly the wrong-file-gets-run failure the checker exists for, and neither had ever been hashed.
- **Sep 7, 7:55 PM:** `py live_draft.py --bridge`. Confirm the first poll line reports the
  keeper-row count.
- **Sep 7, 8:00 PM:** draft.

**[v7.0] TWO OF THE FOUR ARE NOW CLOSED — doc 155, from one `verify_prerank.py` run.**
```
ESPN stored: 544 rows   [teams/ID mTeam -> draftStrategy.draftList]
  ORDER MATCHES exactly for all 544 positions.   K / D-ST inside ESPN's top 250: 0
```
2. ~~Whether ESPN's write API accepts **negative playerIds**~~ — **IT DOES.** `[TESTED]` 544 stored,
   not 512, so all 32 defenses (`-16000 − proTeamId`, Broncos `-16007`) survived the write. The
   read-back proves it; a 200 never did.
3. ~~Whether the prerank POST **replaces or appends**~~ — **IT REPLACES.** `[TESTED]` 544 stored, not
   1,088, AND the order matched at every one of the 544 positions — impossible under an append,
   because the previous list differed in 473 of its 544 rows (doc 60). **So re-injecting after the
   7:00 PM keeper swap is safe, and is the correct move.**
   Bonus from the same run: **zero K or D/ST inside ESPN's top 250**, so if the clock ever expires
   ESPN's own autodraft takes a skill player off Matt's VBD order.

**STILL UNTESTED, AND ONLY MATT CAN RUN IT — ONE thing, not two. [v7.3 — corrected.]**
~~1. `py live_draft.py --replay 2025`~~ **PASSED 2026-09-04 08:51 EDT (doc 163): 180 rows fetched,
12 flagged keeper, 181 renders, no traceback, and the `len(picks)!=180 or nk!=12` guard did not
fire.** §2.1(b2) is now verified against a REAL ESPN feed, not a mock. **This entry sat here
claiming to be untested for two days after it passed** — found by §0.5's milestone check, and it is
the reason that check exists.
1. `py fetch_keepers.py --dry` — see below. **This is the only one left.**

**[v5.4] Exact commands, PASS lines and failure modes: `claude/71_weekend_test_kit.md`.**
**[v5.5] `py fetch_keepers.py --dry` is the most valuable of them** — docs 79–82
verified the render paths, the streamer filter, the shape detector, the board builder and the
board-order test by execution, but every ESPN response in those tests was mocked. **Nothing has run
the poll → engine → page loop against live data.**

**[v5.5] "Available offline" covers `Scripts\` AND `Source\`, not just `Scripts\live_draft\`**
(doc 79). `keeper_swap.py` reads `code_universe_v5.csv` and `espn_projections_2026_20260823.csv`
out of `Source\`; an unhydrated `Source\` fails the 7:00 PM keeper swap, not the 8:00 PM board.
The kit's "five files, nothing else is needed" contract is true **of `live_draft.py`** — it was
read as true of draft night, and it is not. **[v6.6] And the count itself is now wrong: the kit is
NINE files plus the five-file `espn_bridge\` extension. Never quote a count from prose — run
`py check_kit.py`.**

**[v5.5] FantasyPros ADP is NOT a runtime input** (doc 79, tested). Nothing in the draft path reads
it; `adp_pick` is ESPN's own `espn_adp`. **[v6.7 — THE VINTAGE IS 08-30, NOT 08-23.
`Scripts\live_draft\adp_vintage.txt` reads `espn_projections_2026_20260830_0142.csv`; the board was
re-frozen by `refresh_adp.py` (doc 109) and this sentence was never updated. Read the file, never
this line.** Second-order and NOT chased: §2.1(c)'s keeper-depletion table was solved on the
**08-23** keeper ADPs and has not been re-solved on 08-30 — seven days of drift on twelve ADPs,
unlikely to move a row, unverified.] It is a §4.4 divergence check.
Never put it on Matt's Sept 5 list as required work.


---

## FROM SECTION 9: THE DRAFT-NIGHT KIT ROWS OF THE CANONICAL-LOCATIONS TABLE

| what | where |
|---|---|
| **the draft-night kit** — **[v6.6] NINE files plus `espn_bridge\`, not five.** `bridge_server.py`, `bench_lineup.py` and `probe_sources.py` joined it, and the five-file Chrome extension in `espn_bridge\` is now pinned too — it was invisible to the checker, and a stale `hook.js` fails SILENTLY (it connects, prints nothing, forwards no picks) | **`G:\My Drive\_Fantasy\2026\Scripts\live_draft\`** — moved there Aug 28; `Source\live_draft\` is trashed. **[v5.3] Do NOT read a file map out of this table. Run `py check_kit.py` and be told.** It pins names, byte counts and sha256 for the whole tree, and reports stragglers. Three sessions moved this tree in one day and every prose map went stale within hours — the checker is the map |
| **[v7.0] built since v6.9** | `make_howto.py` regenerates HOW_TO_READ_IT from `live_draft.COLGLOSS` **and the board's own stylesheet** — it refuses to write if a badge label vanished from `live_draft.py`, so the key cannot describe a mark the board no longer draws. `mark_rookies.py` derives rookie status (no 2025 snaps AND absent from the 2023 **and** 2024 pulls — `g25 == -1` alone also catches Tank Dell and Brooks). `apply_research.py` stamps dated news onto `player_context.csv`. All three write through the `depth_map.py` guard: refuse if any unowned column or the row count changes, archive first, re-pin `check_kit` |
