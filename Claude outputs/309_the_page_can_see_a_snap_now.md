# 309 -- the page can see a snap now, and the file he built was three quarters wrong

**15 September 2026, Tuesday.** Matt ran `py research\wk1\build_form.py` and asked what else could be
done to repair the week sheet. **Three things, and the first is that his build was wrong and it was
my bug.**

---

## 1. HIS `form_2026.csv` HELD TWENTY OF THE THIRTY-TWO CLUBS

`Source\form_2026.csv` came back at 81,468 bytes against the 130,556 the same script produced here.
**693 week-1 rows against 1,118, and 20 clubs against 32.** Missing: **ARI DAL DEN GB KC LAC LV MIA
MIN NYG PHI WSH.** Three of the six names the screen exists to surface live on those teams
(Green Bay, Denver, Miami), so the screen would have found half of what it should.

**THE CAUSE, and it is one line I wrote yesterday:**

```python
if os.path.exists(p) and os.path.getsize(p) > 1000:
    return p                      # serve any cached file over 1 KB
```

`Scripts\research\wk1\` already held a `stats_player_week_2026.csv` from **13 September**, a partial
mid-week-1 download left by an earlier session. The fetch never ran. **The script printed a row
count and exited 0, and the row count looked entirely reasonable** -- which is section 0.2's
"an exit code is not a result" in a new place: not a step that did nothing, but a step that did its
job perfectly against the wrong input.

**FIXED THREE WAYS, and each guard was run against the specific defect that motivated it (0.2):**
1. **Always re-fetch.** The cache is now reachable only when the network call FAILED, and that path
   prints the cached file's date and says in terms that it may be stale.
2. **A completed week has 32 clubs.** A week short of 32 that is BEHIND a newer week exits non-zero
   and names the missing count. The newest week short of 32 is treated as still in progress and
   kept out of the cumulative row rather than quietly averaging a half-played Sunday.
3. **The artifact must be usable.** If every week is in progress the cumulative row is empty and the
   page would join against nothing, so that exits too.

**CONTROLS, all three fired and the good path is unchanged:**

| control | planted | result |
|---|---|---|
| C1 | the exact 20-club file, network blocked | WARNS with the file's date, marks the week in progress |
| C2 | a 20-club week 1 behind a 32-club week 2 | **exit 1**, names 12 missing clubs and the file to delete |
| C3 | a 20-club week 1 as the only week | **exit 1**, "the cumulative row would be empty" |
| good | the real 32-club feed | 2,236 rows, 32 of 32, unchanged |

## 1b. AND ONE COLUMN WOULD HAVE SILENTLY LOST TWO TEAMS

nflverse writes **`LA`** and **`WAS`**. `sheet_engine.TEAM_ALIAS` maps those the OTHER WAY, to
**`LAR`** and **`WSH`**. `build_form.py` shipped with its own literal map pointing at nflverse's
spelling, so every Rams and Washington row would have failed the join with **no error at all** --
section 3's identity rule, and the same shape as doc 307's `team_c`. It now imports the project's
own `TEAM_ALIAS` and prints which map it used; the literal is a standalone fallback only.
Verified after the fix: LAR 35 rows and WSH 36 rows in `form_2026.csv`, both joining.

---

## 2. THE PAGE NOW READS IT. THREE EDITS.

**`wire.py`** gains `FORM`, `load_form()` and `form_signals()`, mirroring `load_pedigree()` exactly:
it returns `({}, why)` when the file is absent and the caller NAMES that on the page rather than
printing a lane that found nothing. Every row gets `snap_pct`, `w1_targets`, `tgt_share` and
`form_sig` with a **blank** default, never a zero, because a man with no week-1 line did not play and
"0 of 3" would read as a measured miss. The join is asserted: it says so if the file loads and
matches nothing, and if an implausible share of RB/WR/TE rows have no line.

**`sheet_engine.py`** gains a second bet lane beside the two screens. **`sheet_constants.json`**
carries its rate, with its population written into the file next to it, because it is NOT the
population of the two rates above it and must never be compared with them (0.6): those come from
this league's own executed adds (n=108); this one is NFL-wide (n=517).

**LIVE, on his real roster and the real 15 Sept wire, built through the production writer:**

| # | | pos | own | expected |
|---|---|---|---|---|
| 1 | **Dalton Schultz** | TE HOU | 20% | **11.1** |
| 2 | Malik Washington | WR MIA | 8% | 3.7 |
| 3 | Devaughn Vele | WR NO | 13% | 3.3 |
| 4 | Caleb Douglas | WR MIA | 16% | 3.3 |
| 5 | Kalif Raymond | WR CHI | 0% | 3.3 |

**Jalen McMillan, who did not take a snap in week 1, is no longer on it.** That is the whole point:
the page's number one on the 15 Sept sheet was a man with no week-1 line, and doc 304 had named
exactly that defect two days earlier.

**AND THE CAP IS FIVE, NOT THREE.** It was `now[:3]`. Doc 308 recorded the cap as the smallest of the
three reasons his list was short, and it was: this week `now` held exactly three anyway. **With the
workload lane in, there are real rows below three for the first time, so the cap now genuinely
bites.** Five rather than ten, because a long list is a ranking he has to adjudicate and that is the
work this page exists to do for him.

---

## 3. A NUMBER ON THE LIVE PAGE HAS BEEN OVERSTATED BY 6.4x, AND IT IS NOT NEW

Chasing Schultz's headline figure (29.3, and no tight end scores 29 a week) found a defect that
**predates every change above and is on the sheet he read this morning.**

`bet()` returns `per_week_gain * weeks_of_hit` -- a **TOTAL over the hold**. The sentence rendering
it said **"He would be worth {fires} a week to your lineup"**. On the 15 Sept page that made
Jalen McMillan and Pat Bryant read *"worth 8.7 a week"* when the measured figure is **1.4 a week for
6.4 weeks**. Schultz's 29.3 is likewise **4.6 a week**, and his is larger than a receiver's for a real
reason: tight-end replacement is 8.8 against a receiver's 11.7, and his week 6 is Matt's empty slot.

**The arithmetic was right and the word was wrong**, which is 0.1's scope rule on a printed page.
Rewritten to *"worth about 29 points to your lineup over the 6 weeks a hit lasts, 4.6 a week"*. The
bet TABLE was already correct: its column is headed "if it fires", which is neutral, so only the
prose sentence carried it. `AUDIT_LEDGER` row 48.

---

## 4. WHAT THIS DOES NOT DO

- **It is WR and TE only.** The measured population is pass-catchers. The running-back version is
  `week1_share.py`'s backfield share, a different predictor on a different outcome, and it is NOT
  wired in. `AUDIT_LEDGER` row 29 stays open.
- **38% is "reaches replacement over weeks 2-14", not "beats LaPorta"** (doc 305 3.1).
- **One week is one week.** After week 2 posts, the cumulative row moves and the same screen should
  be re-read, not re-argued.
- **The wire's sort key is still the frozen preseason VOR** (ledger row 42). This adds a lane; it
  does not reorder the wire.

## 5. OPEN

**NOT YET RUN:** whether the week-1 signal survives into weeks 2 and 3, which decides whether this is
a week-2 screen or a season-long one. **NOT YET RUN:** the RB composite on the full 32-team slate.
**NOT YET RUN:** a negative control that plants a 2-of-3 row and asserts it reaches the rendered page
by NAME (0.5c5) -- the end-to-end build above was run by hand this session and is not yet in
`redteam_controls.py`, which is ledger row 32's gap widening by one.
**STILL OPEN, untouched:** the frozen VOR sort key - `p_opens` on an already-open job - the analyst
hit-rate test - the concentration test - slot rate into the 4.30 composite.
