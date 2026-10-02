# 281 — The seat that was not there, and the tight end that covers nothing

**2026-09-10, week 1.** Matt came back with seven questions. One of them was a contradiction he
caught in my own output, and chasing it found a defect, a bad recommendation, and a measurement
that reverses a roster move.

---

## 1. THE CONTRADICTION, AND HE WAS RIGHT TO ASK

> *"you said nothing on waivers but on the other hand you provide that i could move add Tank Dell
> and move to IR. Which is it? I'd have to drop Hockenson, or other to add him first else there is
> no room on my roster to add him in the first place."*

**Both halves of mine were true at different moments and I never said which moment.**

- *"Nothing is on waivers that you want"* is about the WAIVER lane — doc 269's plan was entirely
  free agents, added with the green +, no priority spent. Still true.
- *"IR-stash Tank Dell — free option, no cost, no drop"* was written when his roster was **14 of
  15**, the morning after the Spears drop. With a seat open it cost nothing. **On a full roster it
  is not free, and his mechanic is the correct one: ESPN has no add-straight-to-IR.** The sequence
  is drop a man → add Dell → move Dell to IR → the seat comes back. The seat comes back; the man
  does not.

**So the rule that was missing from the item: an IR stash costs zero roster spots and exactly one
drop, and the drop is only free while a seat is already open.** The item said "no drop" as though
it were a property of IR stashing. It was a property of that morning.

---

## 2. THE DEFECT UNDER IT — THE MISSING-ROW CHECK ON HIS OWN ROSTER

`wire.py --html` built the week sheet's roster like this:

```python
myrows = [dict(rate[pid]) for pid in mine if pid in rate]
```

`rates()` skips any player ESPN prices at zero (`if not pid or pr <= 0 or tm not in byes: continue`)
— **which is exactly what an injury designation looks like.** So a man he owns with an IR or OUT tag
is dropped from the page, and `drop_costs()`, which infers an open seat from `len(roster) < 15`,
then **invents a seat that is occupied.** The page prints `the open spot — 0.0` and tells him a
lottery ticket is free when it would cost a drop.

**This is `ERROR_PATTERNS` §0.5(c)5 for the third time on the same shape:** MarShawn Lloyd was rank
184 against a 180-row cut and was not on the paper (doc 174); Ricky Pearsall carried both receiver
signals and was silently dropped from this same page yesterday (doc 277); now it is **his own
roster**, and the thing that went missing was not a player but a *constraint*.

**THE FIX, AND ITS NEGATIVE CONTROLS WERE RUN FIRST (§0.2).**
`drop_costs(roster, cap=15, used=None)` takes the count from the roster READ, never from the rows
that survived pricing. `render()` and `write()` carry `unpriced` and `seats_used`. `wire.py` builds
`unpriced_mine` and prints it to the console as well as the page.

| control | expected | got |
|---|---|---|
| 15 seats used, 1 unpriced | no open-spot row; the man NAMED | pass — named, row gone |
| the OLD call (14 rows, no count) | open-spot row present | **pass — reproduces the live defect** |
| 14 used, none unpriced | open-spot row present | pass |
| 15 used, none unpriced | "your roster is full" box, no open-spot row | pass |

`sheet_engine.py` 36730 → 38747 (`fddbc207b44f2ab5`), `wire.py` 63720 → 64485
(`7a7a717daeedc3cb`), both re-pinned in `check_kit.py`, both previous copies in `2026\_archive\`
with a `_20260910` suffix.

---

## 3. THE MEASUREMENT THAT REVERSES THE MOVE — HOCKENSON IS ON LAPORTA'S BYE

He named Hockenson as the man he would drop to make room. Whether or not Hockenson is on the roster
yet, **the arithmetic on that name is worth printing, because the reason the seat would have been
spent on a tight end at all was to fix the empty week-6 slot** (doc 234, +7.1).

**Minnesota's bye is week 6. Detroit's bye is week 6.** `byes_2026.csv`, 14 sources agreeing on MIN
and 12 on DET.

**POPULATION / METHOD — state it every time:** his fourteen bodies as of the 09-10 roster read,
league-scored season projections from `espn_projections_2026_20260907_1258.csv` divided by 14, best
legal nine solved for each of weeks 1–14 with byes removed. Gain = the fourteen-week total with the
man, minus the same total without him.

| the free tight end | his bye | gain over all fourteen weeks |
|---|---|---|
| **T.J. Hockenson (MIN)** | **6** | **+0.0** |
| **Brenton Strange (JAX)** | 7 | **+8.1** |
| Pat Freiermuth (PIT) | 9 | +7.6 |
| Dalton Schultz (HOU) | 8 | +7.4 |
| Gunnar Helm (TEN) | 9 | +7.0 |
| AJ Barner (SEA) | 11 | +6.5 |
| Michael Mayer (LV) | 13 | +4.5 |

**Hockenson adds nothing in any week.** He is behind LaPorta (10.7 a week against 8.6) in the
thirteen weeks LaPorta plays, and in the one week LaPorta is out he is out too. `[TESTED]`

**THIS IS §6's SAME-BYE TRAP, MEASURED A THIRD TIME AND FOR THE FIRST TIME AT TIGHT END.** §6
recorded "a same-bye second QB/TE doubles the hole instead of covering it" as a *preference*;
§4.18c measured a same-bye QB2 at **+0.00** and said the doctrine's reason was right. Here it is on
his live roster, at the other position, at the same number. **His own doctrine has now earned the
stronger statement: the bye week is not a tiebreak on a second QB or TE, it is the entire value of
the pick.** Off-bye: +8.1. On-bye: +0.0.

---

## 4. AND ONE TRAP IN THE DROP TABLE ITSELF

The cheapest-body table reads, on the 14-man roster: open spot 0.0 · **Mike Washington Jr. 0.0** ·
Dobbins 7.2 · Dowdle 9.3 · Worthy 10.4 · **Shough 21.9**.

**Shough's 21.9 is a bye artifact and must not be read as value.** Hurts' bye is week 10; Shough
(bye 8) is the only other quarterback, so dropping him leaves the QB slot **empty** in week 10 and
the table charges the whole week. Doc 259 measured the same spot the other way — Daniel Jones 21.87
against Shough 21.92, **0.05 a game** — because that comparison *replaced* him off the wire and this
one does not. **Both are right about different questions.** The honest form: dropping Shough costs
about nothing **provided a quarterback is added for week 10**, and that conditional is now a dated
line on his to-do rather than a number on a page.

Washington Jr. prices at 0.0 and stays regardless — *"0% chance i drop him"*, his standing call,
and §6's bench-RB-to-the-cap rests on his own waiver record, not on Washington's projection.

---

## 5. WHAT `floor` MEANS IN `inherit_2026.csv` — he asked

> **[CORRECTION, 11 Sept 2026, doc 291 / catalog D3.] Three statements below are wrong as written;
> the conclusion (a label, never a ranking) stands.**
> 1. **11.2 is not from this league.** It is §4.27's median relief scoring across **40 running-back
>    takeover events in NFL team-seasons 2021–2025**.
> 2. **11.2 is not "the rate at which a fill-in back actually kept the job."** It is the middle of what
>    fill-in backs scored while the starter was out. What §4.27 found about keeping the job is a
>    different number: a back who produced in relief kept about a fifth of the job (+12.4 points of
>    share); one who did not lost ground.
> 3. **rho +0.006, p=0.97, n=39 was measured in doc 275, not doc 276.** Doc 275's population was 62
>    absence events, 39 of them with a prior-season line to test.

`floor` is one of **`clears` / `thin` / `no NFL weeks`**, and it answers only this: *in 2025, did
this backup ever put together two weeks in a row at the rate a relief back typically scores?*

The bar is **11.2 half-PPR points a game**, which is doc 244's **median relief scoring across the 40
measured takeover events** in this league's five seasons — the rate at which a fill-in back actually
kept the job. `best_2wk_2025` is his best consecutive two-week average; `clears` means it reached
11.2, `thin` means it did not, `no NFL weeks` means there is nothing to measure (a rookie, or a man
who never played).

**It is a LABEL AND NEVER A RANKING, and doc 276 is why:** across 62 measured absences, nothing
about the backup predicted what he scored in relief — best-two-weeks against relief scoring is
**rho +0.006, p=0.97, n=39**. So the file sorts by `job_pays` — what the job itself is worth — and
`floor` is there to tell him whether the man has ever done it at all, not to order the list.
Brian Robinson at **11.15** reads `thin` by five hundredths of a point; that is the column being
honest about a bar, not a judgement about Robinson.

---

## 6. THE TO-DO LIST WAS A BRIEFING, NOT A LIST

> *"the to do list is a bit cluttered"* · *"I scanned the to do list but didn't see any commands to
> run or discussions needed with us. Did i miss anything."*

**He missed nothing; the file hid it.** 9,744 bytes, fifteen open items, and `py wire.py --html`
appeared **twice as two separate items** with different justifications. Of the fifteen, **two were
commands** and the rest were findings wearing a checkbox — doc 278's news result, doc 279's volume
result, doc 276's section-3 description, doc 275's new list. All of those belong in the docs and on
the sheet, which is where they already are.

Rewritten to 4,424 bytes under five headers: **RUN THESE** (two commands), **ROSTER MOVES — NOW**,
**DATED**, **STANDING**, **closed**. One line an item, the note after a `#`.

**THE RULE THAT COMES OUT OF IT:** an item belongs in `matt_todo.txt` only if it names something
**he** does — a command, a click, or a date. **A finding is not a to-do, and putting it in the
to-do file is how the two commands became invisible.** §0.1 says detail belongs in a pushed
document; this is the same rule applied to the tracker, and the tracker had been exempt from it.

---

## OPEN AFTER THIS

- **`py wire.py --html` has still not been run by him** — every fix in docs 275, 277 and this one is
  on staged copies until it does. It is item one on the new list.
- **His live roster is still unread by me.** `MY_ROSTER.csv` is written by that same run and does
  not exist yet, so whether Hockenson is actually on the roster, and whether the seat is open, is
  his answer and not mine. **Everything in §3 above is conditional on that and is stated as such.**
- **Is the Dell stash worth anything at all if a seat IS open?** `NOT YET RUN`. The testable form:
  P(he is activated and startable in weeks 5–14) × his rate above Matt's WR bar. Houston's room is
  thin — Higgins on a torn ACL, Noel still limited `[SOURCED: 4for4, 30 Aug 2026]` — so the role is
  real if he returns. His ESPN tag is `INJURY_RESERVE` and he is 34.4% owned league-wide, so the
  rest of the format thinks the stash is live.
