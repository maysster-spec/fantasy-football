# 142 — Review of doc 140. It is sound, and it corrects doc 139 in the direction that matters.

**2026-09-03 · reviewing Fable's `140_pick32_in_dollars.md` against doc 139 §5 · T-4 days**

---

## The do-this list

1. **At pick 32, take the engine's #1 row.** Do not override it to a name the board shows
   "within a point" — that runner-up is a QB in 47 of 100 simulated states and is **$20–24
   behind**, not tied.
2. The five names that genuinely cannot be separated: **Bowers · McBride · Kyren · Judkins ·
   Lamar**, plus **Hall on sight** if he slips. Any of them, first one showing.
3. Nothing else. Two defects doc 140 found in passing are already fixed and committed.

---

## 1. Verdict

**Accept.** The design does what the prompt asked and more: 100 realistic pick-32 states from the
production `Engine` (not a re-implementation, §0.2 v5.5), N=2000 paired drafts on common random
numbers, dollars against the §2 table, a falsifier fixed before computing, both the unadjusted and
availability-adjusted orderings reported separately rather than merged. The limits section is
honest about the three ways its sim differs from the shipped engine and bounds the one that could
change a verdict.

**It answers Matt's question and it corrects mine.**

## 2. WHERE IT CORRECTS DOC 139 — and doc 139 was wrong to generalise

Doc 139 §5 measured pick 32 at **margin 0.15 points, converging** across sample sizes, and
concluded: *"pick 8 the engine decides; pick 32 Matt decides."* Doc 140 ran **100 states instead
of one** and found:

| | doc 139 | doc 140 |
|---|---|---|
| states examined | **1** (31 players off in ADP order) | **100** (§5 opponent model) |
| margin #1 over #2 | 0.15 | median **3.65**, IQR 2.05–7.98, min 0.20 |
| states with margin ≤ 1.0 | — | **9 of 100** |

**My 0.15 was one state, not the typical one.** I ran ten seeds against a single board position
and read the stability of that position as a property of the pick. It is not. Doc 140's own line
is exactly right: *"doc 139's 0.15 is one state; the tie is state-dependent."*

**And the practical conclusion inverts.** Doc 139 said the human decides at 32. Doc 140 shows the
engine's #1 is one of the six core names in **88 of 100 states** — it is not confused. The risk is
the opposite of what I described: **overriding it.** The engine's #2 row is a QB in 47 states
(Burrow 39), and in dollars Burrow is **−$24.0 [−32.3, −16.0]**, Hurts −$19.5, Daniels −$20.7,
Stafford −$22.8 — every one CI-clear. Egbuka, which doc 139 saw as the modal winner in its one
state, is **−$20.4** and loses head-to-head to Judkins by $18, Adams by $20 and Bowers by $32.

**The board's "coin flip" tag is right about whether to agonise and wrong about who is in the
flip.** That sentence is doc 140's best contribution and it is a correction to a directive entry
I wrote yesterday.

## 3. What survives from doc 139

- The tie itself. Five core names, policy spread **$2.7**, no head-to-head CI clear of zero.
- "Spend the 60 seconds on the analyst read and the UNSETTLED flag among the five" — doc 140
  reaches the same instruction, having priced it.
- Pick 8. Doc 140's state generator and the engine agree on St. Brown in **96 of 100**.

## 4. Where I would push back, and where I would not

**(a) The QB penalty rests on QB survival, and that is the least-supported number in the
document.** Doc 140 has Burrow on the board at 32 in **94%** of drafts and Hurts in **98%**.
§4.12 fits a **TE** effective-ADP shift of +15 picks and a Snyder-takes-Allen probability, and
**nothing for QBs generally** — so both the shipped engine and doc 140's sim let quarterbacks
survive on raw ADP plus noise. §5's own timing table says Ray, Kam, Snyder and Fleming take their
first QB in rounds 2.5–3.2, which is at or before pick 32. This is §4.15's failure mode in a new
place: *dispersion where a manager-specific read belongs.*

**But it does not change the verdict, and doc 140 already bounded it.** If the room runs QBs
earlier, waiting gets worse — capped by the QB2→QB6 plateau, **11.8 points total (§4.15)**. That
roughly halves a −15 to −18 point penalty and leaves Burrow-at-32 clearly behind. `[DERIVED, not
re-simulated]` The bound is the right move and I accept it.

**(b) Scoring the §4.22(e) haircut, which §4.22 says not to do.** §4.22 shipped availability
"SURFACED, NOT SCORED — one measurement on 45 receivers does not become a VBD coefficient." Doc
140 turns it into a coefficient. **This is fine, because it is reported as a separate column
against the unadjusted one rather than merged into the board** — which is what the prompt asked
for and what §4.22's own caution requires. The result is also the honest one: it changes exactly
one verdict (Nabers, 4 games, +$27 → +$3) at a 7.6% availability event.

**(c) No pushback on the tie.** §3c's nine head-to-head pairs all span zero at n=43–271, and doc
140 says plainly that resolving them needs 6,000–12,000 drafts and is not worth chasing. Correct,
and it resists the obvious temptation to report a point estimate as a lead.

## 5. Two real defects it found in passing — both fixed and committed

**(a) `Source\games_2025.csv` carried `espn_id` 4568024 TWICE** (Josh Williams, RB, g25 = 2 and 8).
`make_board.py` line 159 left-merges that file onto the board on `espn_id`. **A left merge on a
non-unique right key adds a row, silently** — the 480-row board becomes 481 and nothing says so.
This is §3's merge-collision class, on the draft path, in the file that feeds the `12g` badge.
- The ambiguous id is **dropped**, not guessed: two different game counts, no reachable source to
  say which is right, and a wrong caution badge is worse than no badge. 481 → 479 rows, id unique.
- `make_board.py` now **asserts on both sides**: the key must be unique, and the merge must not
  change the row count. A comment would not have caught this; the assert will.

**(b) `Source\94_picks_17_and_32_2322.md` is a byte-identical stray copy of doc 94.** Left alone —
`tidy_docs.py` territory, and deleting is Matt's call (§0.4).

**(c) Doc 140 also corrects doc 94 §1:** its pick-8 arm took St. Brown even in the ~4% of drafts
where a higher-VBD elite slipped past 7. Both arms shared the flaw, so no doc 94 delta moves.

## 6. THE THING BURIED IN A PARENTHETICAL, AND IT IS ABOUT PICK 17

Doc 140 §2, in an aside about its state generator:

> *"the rollout takes **Jeremiyah Love** in ~40% of states over Hall/Lamb by 2–4 roll points; the
> harness takes top VBD. Noted, not this task's question."*

**Pick 17 is Matt's second pick and it has never been priced in dollars.** Pick 8 has (doc 70,
and doc 139's ten-seed replication). Pick 32 now has (doc 140). Pick 17 has doc 94, which ran on a
**pre-news board and the 08-23 ADP**, and which doc 140 supersedes for pick 32 — leaving its pick-17
half standing on inputs that have since changed, against a rollout that disagrees with it 40% of
the time by a margin (2–4 roll points) larger than pick 32's median.

**That is the next question, and it is bigger than anything left on my list.** It is also the one
Matt cannot resolve at the table: §2.1 calls 17→32 the longest gap in his draft.

## 7. One correction to the directive that this exposed

Doc 140 states its ADP vintage as `espn_projections_2026_20260830_0142.csv`. §8 says *"`adp_pick`
is ESPN's own `espn_adp` frozen at the **08-23** pull."* **The directive is stale** —
`Scripts\live_draft\adp_vintage.txt` reads `espn_projections_2026_20260830_0142.csv`, so the board
was re-frozen on 08-30 (doc 109 / `refresh_adp.py`) and the directive was never updated. Fixed in
v6.7.

**A second-order note, not chased:** §2.1(c)'s keeper-depletion table (`eff` 8/17/**35**/51/…) was
solved as a fixed point on the **08-23** keeper ADPs and has not been re-solved on 08-30. Seven days
of drift on twelve keeper ADPs is unlikely to move a row, but it is unverified. `values.py` and
doc 140 both use the 08-23 `EFF` list.

---

## 8. Close (§7)

**Top 3 assumptions → what would invalidate each**
1. *Doc 140's opponent model depletes the board like the real room.* Its own §7 assumption 1
   answers this well: the core is the set of top-VBD survivors, so a faster or slower room changes
   *who* is in the tie, not that there is one. The separated names are separated at every
   availability.
2. *QB survival on raw ADP + noise.* The weakest link (§4(a) above), bounded at 11.8 points and
   surviving the bound. Invalidated by an actual QB run in rounds 2–3, which §5's timing table
   says is plausible — watch the room, not the board, for this one.
3. *Doc 139's own pick-8 and pick-56 stability numbers.* Those were also single-state, and doc 140
   only re-checked pick 8 (96/100). **Pick 56's "10/10 at margin 2.77" now carries the same
   one-state caveat as the retracted 0.15.** Not corrected here; flagged.

**The missing input that would most improve this:** pick 17 in dollars, on the current board, with
the same harness. Second: the actual keeper list at the 7:00 PM lock — doc 140 names it too, and
three keepers gone ahead of 32 is what sets the whole slate.
