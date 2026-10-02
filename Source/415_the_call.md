# 415 — The call, and three defects the grouping exposed

*24 Sept 2026. Matt: "consider the inputs i need to make an informed decision for who i should pick
up and who i should drop and when ... to me the info seems broken out all over the place ... the
most useful information needs to be grouped and at first read."*

## 1. THE UNIT CONFLATION HE STOPPED AT — "huh?"
The page said: *"The cheapest man you own is Jonah Coleman, at 0.0, but that is a preseason number
and this season disagrees. He has averaged 6.7."*

**0.0 is the DROP COST — what the starting nine loses. 6.7 is POINTS A GAME. They do not
contradict each other**, and "but ... disagrees" said they did. A man can average 6.7 and cost 0.0
to drop because he never enters the nine. **What is actually stale is the RATE the cost was
computed from**, his preseason 1.3 a week. Now compared like with like:

> That 0.0 is what your nine loses, and it is worked out from a **preseason** rate of 1.3 a week.
> He is averaging **6.7** over 2 games this season, so treat the 0.0 as a floor.

**This was my own "fix" from doc 410 and it introduced a worse error than the one it corrected.**

## 2. THE CALL — one row is one whole decision
Every number in it already existed, in four different places: the pickup's worth in Priority
pickups, the drop cost in the drop table, the week in the calendar, the injury in the drop table's
meta line. **Nobody holds four tables in their head.**

| take | he is worth | you would drop | that costs | net | when |
|---|---|---|---|---|---|
| Dalton Schultz TE · HOU · 44% | +13.1 | Jonah Coleman — Questionable, Ankle, back 09-27 | 0.0 | +13.1 | this week |
| Malik Washington WR · MIA · 8% | +7.7 | Devaughn Vele | 0.0 | +7.7 | this week |
| Tank Bigsby RB · PHI · 20% | +3.7 | Tre Tucker | 1.5 | +2.2 | this week |

**The Nth add is charged the Nth CHEAPEST drop**, because that is what taking N men costs. Nothing
is a new calculation.

## 3. THE FIRST BUILD PRINTED AN IMPOSSIBLE ANSWER, AND THAT IS THE FINDING
It showed **four tight ends in five rows, three at an identical +13.1**, and totalled them:
*"Taking all 5 nets +54.4."* He cannot have that. The league caps TE at 3 and §6's doctrine caps it
at 2, and more basically **every `worth` is priced against the bar AS IT STANDS** — the moment the
best tight end fills LaPorta's week-6 hole, that bar moves and the rest are worth a fraction of
what they claim.

**A table that adds up impossible rows is worse than four scattered tables, because it looks
decided** (§0.1(f2)). Fixed: one row per position.

## 4. I BROKE THE DO-NOT GUARD THIS MORNING AND THE CALL SURFACED IT
Row 3 first offered **Mike Washington Jr.**, of whom Matt has said *"0% chance i drop him."*

`load_donot()` reads `[ ] DO NOT ...` lines out of `matt_todo.txt`. **At 07:53 I rewrote that file
at his instruction, 1,504 lines to 43, and moved his never-drop rules into a plain
`## STANDING RULES -- not tasks, do not tick` block** — correctly, because a checkbox on a rule he
never ticks is the clutter he asked me to remove. **The rules were still there and the reader went
blind to them.**

**TIGHTENING A FILE CAN BREAK A READER OF IT.** This is §3's merge-collision corollary in a second
place: *when you change a file's format, grep every reader of that file.* `load_donot` now reads
the standing-rules block too, and a ruled-out man is never offered as a drop in the call, though he
still appears in the full drop table marked *"you have ruled this one out"* — knowing what he costs
is not the same as being asked to cut him.

## [NOT YET RUN] — doc 369's remaining catalog
The empty-slot calendar is four dates written as a paragraph · the cards section is the longest and
least-read block on the page · print and PDF have never been looked at · the opening standfirst is
method, same defect as the vintage block moved at doc 411.
