# 315 — THE MAN WITH THE BIGGEST WORKLOAD WAS THE ONE ROW THE PAGE SAID NOTHING ABOUT

*2026-09-16, hours after doc 314 shipped. Matt: "i don't see KAELON BLACK as a priority pick up on*
*the week sheet" and "i'm not sure how to break the tie at TE. Hockenson i could argue is on a*
*better offense."*

---

## 0. WHAT TO DO

1. **RE-RUN `py wire.py`.** The seat lane now carries its own contest tag. Nothing else to run.
2. **Black is on the sheet and always was — in "the seat", not in Priority pickups.** Two separate
   things were true and only one of them is a defect. Both are below.
3. **THE TE CALL: HOLD HOCKENSON. Do not make the Schultz swap this week.** One sentence: LaPorta's
   availability is the largest measured risk on the roster and Hockenson is the only cover for it,
   while everything Schultz offers is either one week of data or a week-6 problem that is cheaper
   to solve in week 5.
4. **AND THE REASON YOU GAVE IS BACKWARDS, on the one week we have.** Minnesota threw **23** times
   in week 1, **28th of 32**. Houston threw **37**, **4th**. Right answer, wrong axis.
5. **THE FALSIFIER, SO THIS COMES BACK ON ITS OWN:** if Minnesota is still under about 25 pass
   attempts a game at week 5, the volume argument stops being one week of noise and this flips.

---

## 1. THE DEFECT: THE BAND EXISTS AND THE ROW IN IT WAS SILENT

Doc 314 measured, four hours earlier, that last-game touches predict how many rivals file: **1.17 /
1.49 / 1.83 / 2.27 claims and 14% / 29% / 40% / 56% contested.** The 15 Sept sheet then printed:

| Priority pickup | touches | tag |
|---|---|---|
| Dalton Schultz | 8 | 29% contested |
| Malik Washington | 8 | 29% contested |
| Devaughn Vele | 9 | 29% contested |
| Caleb Douglas | 7 | 29% contested |
| Kalif Raymond | 9 | 29% contested |
| **Kaelon Black** | **15** | **nothing at all** |

**The five identical tags are CORRECT** — all five are pass-catchers in one band, which is what a
receiver-heavy list looks like. **Black is the only man on 280 wire rows in the 56% band, and he is
the one the page had nothing to say about.**

**Why:** he renders in the seat lane, fed by `inherit_2026.csv`, which carries no game log. So I
shipped `'touches': ''` there **and wrote a comment defending it**. The blank was right about the
join and wrong about the lane: `WIRE_20260915.csv` already holds his touch count and the two sets
join on a normalised name. **Doc 314's own section 7 listed this as open and I filed it as a
nicety. It is the row the entire finding exists to flag.**

**FIXED:** `_touch_by` is built from the same priced free pool the rest of the page already uses and
looked up on `norm_name(next_man)`, still BLANK on a miss (§4.27's join rule). Six join controls —
exact name, suffix and case mismatch, blank value, missing key, name absent from the wire, empty
pool — plus an end-to-end render against the **real** `inherit_2026.csv` row. All fired. Black now
reaches the page by name at 56% with **"Put him first"**, and claims nothing at all when the wire
has no line for him.

## 2. THE OTHER HALF IS NOT A DEFECT, AND IT IS THE OLDEST OPEN ITEM ON THE LIST

**Black is absent from Priority pickups because that list ranks on what a man adds to the starting
nine, computed from ESPN's AUGUST projection — and Black's is `-112.1`.** Fifteen touches on Sunday,
43% of the snaps, all 28 of San Francisco's backup-back snaps, a job the depth map prices at 302,
and the sort key still says he is the 112th-worst thing you could do with a roster spot.

**The page cannot see what he did when it ranks him.** That is exactly doc 314's finding turned
around on our own sheet: the other eleven managers file on last week's touches, and we rank on a
number frozen in August. `AUDIT_LEDGER` rows **29** (the RB half of the workload screen) and **42**
(the frozen VOR sort key) are that hole, and they stay open. An earlier session already wrote the
right sentence into the code and it is worth keeping: *"do not fix a missing column by demoting the
rows it would have outranked."*

Three of 280 wire rows have 10+ touches: **Black 15 · Emmett Johnson 10 · Devin Singletary 10.**
Their sort values are **-112.1, -126.2 and -168.6.**

## 3. THE TIGHT END, AND THE TIEBREAK THAT ACTUALLY RESOLVES

**His claim, in his words:** *"Hockenson i could argue is on a better offense."*
**The testable form:** does the team's passing environment separate these two at tight end?

**WEEK 1 ROLES ARE THE SAME PLAYER TWICE:**

| | snaps | targets | target share | half-PPR |
|---|---|---|---|---|
| T.J. Hockenson (MIN) | 66% | 5 | **21.7%** | 11.6 |
| Dalton Schultz (HOU) | 66% | 8 | **21.6%** | 5.5 |
| Sam LaPorta (DET) | 81% | 8 | 20.5% | 7.3 |

**Identical snap rate, identical share, and Schultz had MORE targets.** What makes Hockenson look
better is 11.6 against 5.5, and doc 314 measured **that morning** that scoring is the half which
carries nothing once the workload is known. `[TESTED]`

**AND THE TEAM VOLUME POINTS AT SCHULTZ, NOT HOCKENSON.** Week-1 team pass targets: **MIN 23, rank
28 of 32. HOU 37, rank 4.** League mean 29.4. **One week, so it is suggestive and not a finding** —
but it is the opposite sign to the premise, and §4.21 already puts team volume at **7.5%** of the
variance in a pass-catcher's target change against **93.4%** for his own share. So the axis he
reached for is both small and, this week, backwards.

**THE ONE MEASURED TE TIEBREAK IS THE PLAYOFF DRAW, AND IT SAYS HOCKENSON.** §4.26(b): weeks 15–17,
**+3.39 points per sd of easier draw, p=0.031, n=70** — the only schedule effect that measures at
any position, and null at all four positions over weeks 1–14. Computed from `pos_allowed_2025.csv`
and `sched_2026.csv` (TE points allowed: mean 10.66, sd 2.30):

| | wk 15 | wk 16 | wk 17 | mean | vs league |
|---|---|---|---|---|---|
| **Hockenson (MIN)** | DET 11.1 | WAS 13.4 | NYJ 12.6 | **12.33** | **+0.73 sd, easier** |
| Schultz (HOU) | JAX 11.7 | PHI 6.4 | GB 9.3 | 9.15 | −0.66 sd, harder |
| LaPorta (DET) | MIN 8.4 | NYG 8.9 | CHI 10.2 | 9.19 | −0.64 sd, harder |

A 1.39 sd gap, **about +4.7 points to Hockenson across the three weeks.**
**CAVEAT, AND IT IS IN THE DIRECTIVE ALREADY:** §4.33 records this as **`[OPEN]`** — doc 10 puts the
whole 32-team weeks-15–17 spread at ≤5.5 points and says in terms that it is not a playoff-planning
tool. **So this is a tiebreak between two tight ends you rate the same, which is exactly the
situation, and never a reason to move off a better player.**

**THE REAL ARGUMENT FOR HOCKENSON IS LAPORTA, AND IT IS ALREADY MEASURED — doc 283.** LaPorta's
games played went **17 → 16 → 9**; back surgery ended his 2025 in November and a hip cost him three
weeks of camp in August 2026. §4.22/doc 203: playing ≤12 games last season is worth **−19.4 points
against the price, p=0.00004, n=735**, the strongest downside signal in this project, and doc 204
says it still reads as a warning rather than noise for a player in year 4. **Hockenson is not a bye
fix. He is the cover on the single largest measured risk on the roster.**

**THE HONEST COST OF HOLDING, because it is real:** LaPorta and Hockenson **share bye week 6**,
which is §6's own same-bye trap, so Matt has no tight end that week and must claim one. The sheet's
calendar already prices that: **claim in week 5, best free tight end today 6.7.** Swapping to
Schultz (bye 8) removes the collision outright. That is the case for the swap and it is not
nothing — it is simply smaller than the LaPorta cover plus the playoff draw, and it is a week-5
decision, not a week-2 one (§4.31's scope note: the free pool in week 5 is not empty).

## 4. THE PROCESS DEFECT, RECORDED BECAUSE IT NEARLY DELETED TWO LEDGER ROWS

`device_stage_files` writes to a fixed path, so pulling a file down from the drive **to archive it**
silently reverted my working copy to the pre-edit version while the drive held the new one. It
happened three times in one session — `sheet_engine.py`, `sheet_constants.json`, `AUDIT_LEDGER.md` —
and the third came within one write of dropping ledger rows 53 and 54 off the file. Caught by a byte
count that came out **44,895 against the 47,077 written an hour earlier**. Nothing reached the drive
wrong. **Rule, now in the ledger: after committing an edited file, the authoritative copy is the one
under `outputs/`, never the staging path.**

## 5. OPEN

- **Rows 29 and 42: the sort key.** Black at `-112.1` with 15 touches is the standing example. The
  input exists (`form_2026.csv` has touches for every player, every week); what is missing is a
  decision about how a week of workload is allowed to move a season projection. **NOT YET RUN.**
- **Whether the week 15–17 TE effect is real at all** — §4.26(b) against doc 10, flagged `[OPEN]` in
  §4.33 and now load-bearing on a live decision. Worth settling before it decides a second one.
- **Minnesota's pass volume**, the falsifier in item 5 of the do-this list, re-read at week 5.
- Still from doc 314: the D/ST and kicker versions of the contest bands, and whether the bands
  survive into a live season.
