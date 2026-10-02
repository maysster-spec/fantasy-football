# 182 — The Jameson Williams bear case, the cushion at pick 8, and four contradictions cleaned

**2026-09-05 (T−2).** Matt raised a bear case on St. Brown — Jameson Williams rising and eating
targets — then asked for more plain-language maxims and for the directive to be cleaned of places
where his own prior instructions compete with a better-measured outcome. His standing instruction
for this session, verbatim: **"don't let my prior directives compete with better outcomes, always
challenge me. I much rather be proven wrong and get us right."**

---

## 1. The bear case is real, it is dated and named, and it is smaller than it sounds

`[SOURCED: Heavy / Dan Graziano (ESPN), 2026-09-02]` — Graziano projects **Williams passes
St. Brown in receiving YARDS** this season: *"I think this Lions offense is going to hum this
season, and Williams is the player poised to take the biggest leap."* Reasons given: an expanded
route tree under new OC **Drew Petzing**, and the schedule. 2025 actuals: **St. Brown 172 targets,
Williams 102**, with Williams at **11.0 yd/target** against St. Brown's **8.1**.

**What ESPN has already priced (09-05 pull, projection payload):**

| | targets | rec | rec yds | rec TD |
|---|---|---|---|---|
| St. Brown | 166.5 | 118.4 | 1426.2 | 10.4 |
| Jameson Williams | 102.0 | 64.4 | 1026.4 | 5.7 |
| Sam LaPorta | 102.0 | 78.5 | 787.1 | 5.4 |
| Jahmyr Gibbs | 85.9 | 67.9 | 546.4 | 3.4 |

**ESPN has already taken 5.5 targets off St. Brown's 2025 actual and left Williams flat at 102.**
The bear case is the claim that this is not enough.

**Sizing it, arithmetic not opinion.** For Williams to reach 1,430 yards at 11.0 yd/target he needs
**~130 targets, +28**. Charging **all 28** to St. Brown (an upper bound — LaPorta 102, Gibbs 86 and
TeSlaa 38 are also in the tree, and team volume itself moves ±11% a year, §4.21) takes him to
~131 targets: −25.6 receptions, −308 yards, −2.25 TD under §2 scoring = **−57 league points.**
Charging **half** to him = **−22 points.** So the honest range is **0 to 57, with a central case
near 20.**

**And the key structural point: Graziano's claim is about YARDS, and yards are 0.1/point.**
St. Brown's edge is built on **118 receptions** — 59 points of pure volume in 0.5 PPR that a
yards-title swap does not touch. Williams winning the yardage crown on efficiency is fully
compatible with St. Brown staying the better fantasy asset.

---

## 2. Testing it broke something else: the pick-8 cushion is not what the directive says

Built a modal pick-8 state (the seven lowest `eff_pick` skill players gone) and ran the production
`Engine.recommend(8, top=12, rollout_inner=60)`.

```
Amon-Ra St. Brown  WR  vbd 101.3   roll 1497.1   cost   0.0
Derrick Henry      RB  vbd  95.4   roll 1489.3   cost  -7.8
James Cook III     RB  vbd  93.0   roll 1488.9   cost  -8.2
De'Von Achane      RB  vbd  92.5   roll 1488.5   cost  -8.6
```

**Margin over the runner-up: 7.8, not the ~20 §4.2 quotes.** Sweeping St. Brown's projection down
in 2-point steps, **pick 8 changes to Derrick Henry at a cut of 10 points.**

The board's own arithmetic agrees and needs no simulation: **St. Brown +101.33 against Henry
+95.38 is a 5.9 VOR cushion.**

**Where the 20 came from.** Doc 139, measured on **ONE board state** — the identical defect doc 140
corrected at pick 32, where a 0.15-point "converging margin" became a median of 3.65 across 100
states, and the same caveat v6.7 already attached to doc 139's pick-56 number. Nobody applied it
to pick 8.

**What I could NOT establish, and it matters.** A 30-state generator (§5's rule: best VBD among the
top eight of a §4.12-noised board) **produced no state variation at pick 8** — the top seven are
too tightly clustered in `eff_pick` for the noise to reorder them, so thirteen "states" returned
the identical margin of 7.8 and the identical break-even of 10. **That is one state measured
thirteen times, which is exactly the error I am correcting.** So:

**RESOLVED — the WHO.** St. Brown is the engine's #1 in every state anyone has ever run:
10/10 (doc 139), 96/100 (doc 140's independent generator), 13/13 (here). **Take him.**
**OPEN — the SIZE.** 7.8 and ~20 disagree, both are single-state, and **"about 20 points" must not
be quoted.** §4.2 corrected accordingly.

**Consequence for the bear case:** both the −22 and the −57 scenarios exceed a 10-point break-even.
**So the bear case is live in the sense that it could move pick 8 — but only through a projection
ESPN would have to revise, and ESPN will not revise it before Monday.** The board Matt drafts from
prices St. Brown at 265 points, and that is what the engine will see. **Nothing changes at the
table. What changes is the confidence label he carries.**

`[TESTED, single state, break-even 10 pts]` · `[SOURCED, Graziano 2026-09-02]` ·
`[OPEN, the margin]`

---

## 3. Four contradictions cleaned out of the directive

Per Matt's instruction. Edits made, each flagged `[v7.2]` in place.

**(a) §6's header claimed a quote it does not have.** It read *"confirmed 2026-08-30, in his own
words."* There is no verbatim source; it is a paraphrase written in an earlier session and labelled
as a quote, which **§3 forbids** — the same rule that bans attributing a claim to a named analyst
without the words. Substance unchanged, label corrected, and the header now carries his 09-05
instruction: a preference a measurement contradicts must be **surfaced at the moment it binds**,
not silently obeyed.

**(b) §6's audition window fought §4.18b and lost.** It said *"concentrate auditions in rounds
5–9."* §4.18's own table splits at exactly that seam — rounds 5–8 become keepers **15.1%** of the
time, rounds 9–12 only **8.3%** — and §4.18b then measured what a round-9+ keep is worth: a kept RB
drafted round 9 or later returned **−2.5 VBD14** (n=7), a kept QB **−55.7** (n=9). **Frequency
halves and value goes to zero at the same seam.** Narrowed to **rounds 5–8**; a round-9+ pick is a
2026 dart, not an audition. Rounds 5–8 were never separately measured and keep the benefit of the
doubt.

**(c) §4.2's pick-8 margin.** §2 above.

**(d) Two different sections both numbered 4.11** — the [v5.9] bye downgrade and the bye-trap list.
The second is now **4.11b**. Trivial, and exactly the ambiguity the naming rule exists for.

`audit_directive.py` after all four: **51 ok, 0 FAIL.**

**Deliberately NOT changed: §6's `CAPS = {'QB':2,'TE':2}`.** It is tighter than the league's QB3/TE3
limit on purpose. Nothing has measured whether a third would help, and in a one-QB league the
question is close to academic — it stays a stated preference, correctly labelled as one.

**Still live and unresolved by design: §4.18's draft-night rule versus §6's last bullet at picks
104/113.** Matt said on 09-05 he does not expect to draft two quarterbacks. **There is a resolution
neither side had noticed: if he still has no QB at 104, the quarterback there is his QB1 and the
rule does not apply at all** — §4.2's plan is "best board player at 8, QB later," so this is the
likely branch. The conflict only bites if he already holds one, and Bo Nix (+7.4 VOR, healthy,
doc 179) is the name if it does.

---

## 4. `Slot Eight Maxims` — the fog-clearing card

Matt: *"any other maxims like that to clear my fog."* Sixteen of them, each carrying the number it
rests on, grouped by **where they bite** rather than numbered — a pick coordinate is the coordinate
he will actually reach for at the table. Published as an artifact so it opens on his phone without
his PC, which he cannot reach until Monday.

The two corrected items lead the card in a flagged block, because a maxim he has already memorised
wrong is worse than one he never learned: **"pick 8 is still St. Brown; 'about 20 points' is not,"**
and **"auditions are rounds 5–8."**

---

## 5. The lesson worth keeping

**Matt's bear case did not move the pick. It moved a number the whole project had been quoting for
two days.** He asked about Jameson Williams; the answer is that the Lions target tree is roughly
where ESPN has it. But testing it required running the engine at pick 8, and that is what exposed
a 20-point cushion that is really 6 to 8.

`ERROR_PATTERNS` already carries the parent pattern (**A2**, a statistic read off a pilot run) and
doc 140 already carried the specific cure. **Neither was applied to the most-cited decision in the
project, because "pick 8 is CLOSED — open no further sensitivity on it" reads as *stop asking*
rather than *stop re-deciding*.** It should mean the second. **A closed decision still has to
survive a new fact; what it does not have to survive is being re-litigated on the old ones.**
