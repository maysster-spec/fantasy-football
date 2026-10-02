# 417 — the weight was not reproducible, and the IR rule was backwards

**24 Sept 2026.** Three things shipped, one was retracted before it ever rendered a page, and one of
Matt's own plans for next Wednesday is dead.

---

## 1. THE BLEND. Every "he is worth" number was a preseason guess, and now it is not.

`rates()` priced the whole week sheet off `projection / 17`. Standing in week 3 of the season, with
three games of 2026 on file, the page was still quoting August. Dalton Schultz showed **+13.1 off
6.06 a week while actually measuring 12.8**. Matt caught the shape of it himself: *"Pretty odd that
those projection values were hard-coded and not updating. That's wild stuff."*

The blend was deferred twice in this project because I would not invent the weight (§0.2: a severity
estimate is a claim and must be measured, not reasoned). It is measured now.

| | |
|---|---|
| population | nflverse 2021–2025, `season_type` REG, RB/WR/TE, half-PPR; every player-season with a prior season and at least one game each side of the week |
| outcome | ppg over weeks W..14 — this league's regular season ends at 14 (§2) |
| fit | rest-of-season ppg ~ (ppg so far) + (prior-season ppg), OLS; the weight is the normalised coefficient on `ppg so far` |
| n | 846 to 1,254 player-seasons per week |

**THE BLEND BEATS THE BETTER SINGLE SIGNAL AT EVERY WEEK, by 1% to 15% RMSE. The crossover — the
week this season is worth more than the prior — is week 5.**

```
BLEND_W = {2: 0.23, 3: 0.36, 4: 0.43, 5: 0.51, 6: 0.54, 7: 0.61,
           8: 0.64, 9: 0.69, 10: 0.72, 11: 0.77, 12: 0.78, 13: 0.77, 14: 0.79}
```

**CAVEAT, and it bounds the number rather than decorating it.** The PRIOR in that fit is last
season's ppg, not ESPN's in-season projection. ESPN's is the better prior — it knows about injuries,
depth-chart moves and rookies — and a better prior earns more weight. **So the weight on THIS season
is an UPPER bound.** Not shaded down in production, because shading it would be the guess this
measurement exists to avoid.

RB/WR/TE only. `form_2026.csv` does not score passing or kicking (doc 375), so QB, K and D/ST stay
on the projection and say so in `vintage`.

### 1a. THE FIRST VERSION OF THIS TABLE WAS RETRACTED BEFORE IT RENDERED A PAGE.

> ~~`{2: 0.36, 3: 0.44, 4: 0.49, 5: 0.53, 6: 0.57, 7: 0.64, 8: 0.67, 9: 0.73, 10: 0.74, 11: 0.79,
> 12: 0.80, 13: 0.79, 14: 0.79}`~~ **RETRACTED. UNREPRODUCIBLE. Do not quote it, and do not quote
> "n=315 to 888" or "5% to 17%" either.**

It was fitted **inline**, in a session, from a population nobody wrote down. When I sat down to save
the script so the number could be re-run, nothing reproduced it: **18 population definitions were
tried** (minimum games each side 1, 2 or 3 × outcome window ending week 14 or 17), and **none returned
its numbers or even its sample sizes.** Its sample sizes fell monotonically with the week; every one
of the 18 rises then falls. Its week-2 value sat **0.13 outside the band all 18 agreed on.**

**This is doc 399's failure exactly** — a curve with no reproducible population — and it was two
commits away from being the number under every recommendation on the page. The honest part is only
that it was caught by trying to save the script, not by anyone noticing the numbers were wrong.

**`Scripts\research\blend_weight.py` now exists so this cannot recur.** `py blend_weight.py --check`
re-fits from the nflverse cache and **exits 1 if `sheet_engine.BLEND_W` has drifted**. It reproduces
the shipped table exactly.

**STABILITY, which is what makes the replacement quotable:** across all 18 definitions every week's
weight moves by **at most 0.07**, and the shape, the ordering and the crossover are identical in all
18. That band is the honest uncertainty and it is in the comment beside the table.

### 1b. AND IT SHIPPED DEAD ONCE — doc 146's trap in a new shape.

`rates()` takes the week as an argument. **`wire.py` called `rates(SRC)` with no week for its entire
life.** Every function-level test passed, the blend computed, and the page kept printing preseason
rates. A step that returns 0 while doing nothing and a feature that computes and reaches nothing are
the same defect. **`rates()` now prints a loud line when the blend is off** — no week, or no
`form_2026.csv` — rather than falling back silently.

Rendered before and after: the vintage block went from **14 rows to 2**.

### 1c. WHICH SURFACED A SECOND DEFECT THE MOMENT IT WENT LIVE.

THE CALL charged the Nth pickup the Nth cheapest drop, by rank, with no position check. With real
rates on the page, the cheapest man became **Sam LaPorta (TE)** — so the table offered *take Dalton
Schultz (TE) / drop Sam LaPorta (TE)* and called it **+11.1**.

**It is not +11.1. `worth` is priced against the bar AS IT STANDS, which includes the man being
dropped.** A same-position pair is a straight swap wearing an add's price tag. The ladder now walks
to the next cheapest man at a **different** position. Same-position pairings on the rendered page: 0.

---

## 2. THE IR SLOT. Matt's plan for Rico Dowdle does not work, and no file said so.

Matt, 24 Sept: *"i can wait on Rico and put him on IR."*

**He cannot.** §2 carries ESPN's sourced football rule (doc 394, read as page text) and it is **two
different rules that this project has been conflating**:

- the slot **ACCEPTS** only a man whose status is **Out (O) or Injured/Reserve (IR)**
- a man **already in** the slot who is upgraded to **Questionable or Doubtful keeps his seat** — the
  roster stays valid, claims still process, the lineup still moves

**The rule that lets a man STAY after an upgrade is not the rule that lets him ENTER.** Dowdle is
QUESTIONABLE. So is Dobbins. So is Coleman. **The slot will take none of them today.**

Read off `MY_ROSTER.csv` this morning:

| | |
|---|---|
| parked | Puka Nacua (Questionable) — **safe where he is**, this is the upgrade case |
| slot would take today | **nobody** |
| slot refuses | J.K. Dobbins, Jonah Coleman, Rico Dowdle — all Questionable |
| free slots | 2 |

**THE FIX IS THAT THE PAGE COMPUTES IT NOW, by name, every run.** `ir_picture()` reads the roster's
`slot_id` and `status`; `ir_box()` prints it in plain words above the drop table, leading with what
to do. This mattered because the rule lived in the directive, and **the directive is not what Matt
reads on a Wednesday night.** A rule that only exists in a file he does not open at decision time is
a rule that has not fired.

It also prints the freeze case: a man in the slot with **no designation at all** invalidates the
roster and locks the lineup until someone is cut. That is the Sunday check already on his list, now
visible on the page that prices the claim.

**NOT YET OBSERVED, and named rather than assumed (§0.5(a4)):** this league's `STATUS_LOG.csv` has
only ever recorded ACTIVE and QUESTIONABLE, so the exact string ESPN sends for Out and for IR is
**unconfirmed here**. `IR_TAKES` carries every spelling the API is documented to use and the match is
case-folded, so **an unknown spelling shows up as REFUSED, never as a silent eligible** — the safe
direction, because a wrong "you can park him" is a frozen lineup.

---

## 3. §9 RULE 2 FIRED AND DID NOT CATCH THIS.

**`check_kit.py` went to the drive carrying a pin for a `sheet_engine.py` that was already two
versions old, and the commit reported success.**

Rule 2 says: *a fresh container path for every commit* — re-committing different content from the
same path within about two and a half minutes sends the OLD bytes with no error. I obeyed it: every
push went into a new timestamped directory. **The collision was not two commits from one path. It
was two WRITES to one path inside a single push directory**, five minutes apart, and the commit
picked up the first. The rule's intent covers that; its wording does not.

**Caught only by the content check (rule 1).** The commit result said `written`. The bytes on the
drive were 43,540 where 43,632 went out, and the pin inside them would have reported the live engine
as STALE on Matt's next run.

**Amendment going into §9 rule 2: the fresh path is per WRITE, not per push.** If a file is edited
again after it has been placed in a staging directory, it moves to a new directory before it is
committed.

---

## WHAT SHIPPED

| file | |
|---|---|
| `Scripts\sheet_engine.py` | 182,871 · `125ab6bc0304effc` |
| `Scripts\wire.py` | 118,466 · `17bc872fd49a5a70` |
| `Scripts\research\blend_weight.py` | new — reproduces and guards `BLEND_W` |
| `Scripts\check_kit.py` | both pins re-verified against the bytes on the drive |
| `Source\matt_todo.txt` | Dowdle hold with the corrected reason; the OUT-downgrade watch; the stale directive-paste item ticked |

Pre-417 copies of all of them are in `2026\_archive\`.

## OPEN

- **[OPEN]** The prior in the blend fit is last season's ppg, not ESPN's in-season projection.
  Re-fitting against ESPN's projection as the prior would tighten the weight and remove the
  upper-bound caveat. **NOT YET RUN** — it needs a per-week archive of ESPN's projections, and
  `Espn_pull_projections.py` has only been writing one since 20 Aug. It accumulates on its own.
- **[OPEN]** The exact ESPN status string for Out and for IR on this league's feed. **BLOCKED** on
  a man on this roster actually being ruled out. `STATUS_LOG.csv` will record it the first time it
  happens; `IR_TAKES` fails safe until then.
- **[OPEN]** Doc 369's catalog still has two items nobody has looked at: the cards section is the
  longest and least-read block on the page, and print/PDF have never been checked since the
  regroup.
