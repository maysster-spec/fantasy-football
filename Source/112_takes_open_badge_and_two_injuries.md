# 112 — Takes by sheet, the OPEN badge, and two injuries the board did not know about

**Date:** 2026-08-31, later. Six of Matt's questions, three of which turned into code and one of
which turned into a miss I should have caught two weeks ago.

---

## 1. THE 20-SECOND COUNTDOWN WAS NEVER PART OF THE WORK

`sync_desk_copies.bat` ended with a bare `timeout /t 20`. **The copying is finished before that
line runs** — the hold exists only so the window stays readable, and `timeout` was chosen over
`pause` on purpose (doc 84: a `pause` in an unattended window waits forever and leaves a scheduled
task stuck reporting "Running"). **Any keypress has always closed it early; nothing said so.**
Now it prints `Done. Press any key to close, or this window closes on its own in 20 seconds.`
`refresh_pull.bat` and `sept5_after.bat` hold for **600** seconds for the same reason and are
correct as they are — those two you may genuinely walk away from.

**The lesson is small and keeps recurring: a silent wait reads as work.** If a window is waiting
for the reader rather than for the machine, it has to say so.

---

## 2. `my_take.py` NOW TAKES A SHEET — Matt was right about the interface

He expected `my_take.py "filename.csv"`. He was right; one-at-a-time was the wrong shape for a
man entering a dozen takes at 7:40 PM.

```
py my_take.py --file            reads my_takes.csv beside the script
py my_take.py --file other.csv  any path
```
Three columns: **player, direction, note**. Direction is `up` / `down` / `clear`; **blank skips the
row**, so a half-filled sheet is a valid sheet. `#` lines are comments.

**Every name is resolved against the board BEFORE anything is written, and one bad row aborts the
whole file.** This is deliberate: a partial apply at 7:50 PM is unrecoverable in the time
available, and "NotARealGuy" or an ambiguous `Brooks` (5 matches on this board) is exactly the
kind of thing a hurried sheet contains. Verified both failure modes.

**The sheet ships seeded with the three takes Matt has already given me in conversation** —
Monangai up, Jonathon Brooks up, Swift down, in his own reasoning — plus seven blank rows for the
other late RBs. They are applied and live on the board now. **They are his words paraphrased by
me, which makes them mine until he reads them; `clear` removes any.**

---

## 3. UNSETTLED ON THE LIVE BOARD — a changed word, not a third badge

Matt: *"UNSETTLED is a good thing to stand out, but you be the judge."*

The two-marks-per-row rule was hard-won (docs 105/106) and a third badge would break it. So the
label rides in the slot that already fires for these players: **at picks 104+ a direct backup
showed `DART`; it now shows `OPEN` when the backfield is UNSETTLED and stays `DART` when he is
behind a LEAD BACK.** Same slot, same colour, one word that says which kind of dart it is. The
hover carries the rest — *"direct backup on the 2026 depth chart in an UNSETTLED backfield — the
job is worth 196 pts to whoever wins it."*

**Plumbing:** the kit is exactly six files and `depth_map.csv` is not one of them, so `depth_map.py`
now stamps `job` and `job_ceil` into `player_context.csv`, which is. That write is **update-only
and asserts that no other column changed** before saving — Matt's own takes live in that file and
clobbering them at 7:50 PM would be silent and unrecoverable. It re-pins `check_kit` afterwards.

**Caught by rendering it:** the first version stamped the label on every position, which made
**Patrick Mahomes a "LEAD BACK."** The label is a property of a team's backfield and now only
touches RB rows. `[FIXED — 74 rows carry a label, all RB]`

---

## 4. TWO INJURIES, ONE OF WHICH WE MISSED

**Kyle Monangai hyperextended his knee on Aug 16 and the MRI landed Aug 17** — out multiple weeks,
his preseason is over, Week 1 possible but not assured. **Our injury sheet, built Aug 30, does not
mention it.** ESPN flags him QUESTIONABLE and that Q was the only thing on his row. He is now
graded **DISCOUNT** with the date and source in the hover, so on the live board he reads
`DISC` + gold `MINE` — Matt's take, with the knee visible beside it, which is the only honest way
to show both.

**This is the doc 98 failure with the sign flipped.** There I recommended Tank Dell while our own
sheet said avoid; here the sheet was silent about a real injury and the board had nothing to say.
**A grade sheet is only as good as its last refresh, and it has one job on Sept 5: a news sweep
over the shortlist, not just a re-pull.** `[ACTION for Sept 5]`

**Jonathon Brooks, for the record, since Matt's take rests on his profile:** 46th overall in 2024,
the first back off the board that year. **He has torn the same right ACL twice** — Nov 2023 at
Texas, then again Dec 8 2024 after nine NFL carries — and missed all of 2025. Cleared for the
offseason programme in April, first full-contact padded practice in late July, and he ran with the
ones through the preseason while Chuba Hubbard's hamstring healed. **Canales has not named a
starter and describes the plan as a rotation** — lead back on base downs, the other man on third
down — with the call coming closer to the Sept 13 opener.
So Matt's read is supported on draft capital, age and current usage, and the thing it does not
price is two ACLs on one knee. Our own sheet already grades him DISCOUNT and calls him "the
cleanest recovery dart," which is the same judgement with the risk left in.

---

## 5. JOSH JACOBS IS NOT ON THE BOARD — plainly

He was zeroed by `apply_news.py` on Aug 30 and sits at rank 435 with a projection of 0. **The
engine cannot recommend him and the printed board does not carry him.** The only place he still
appears is inside Fable's doc 94, which ran on a copy of the board taken before that correction —
that document, not the board, is the stale thing.

**Status re-checked today:** still on the Commissioner's Exempt List, no return date, and LaFleur
said on the record that he cannot say whether Jacobs is available for the Sept 13 opener. **The
override stands.** To reverse it, delete his row from `news_overrides.csv` and run
`py apply_news.py --write`.

---

## ASSUMPTIONS

1. **ESPN's projections are the only ceiling proxy available**, so `job worth` inherits whatever
   ESPN thinks a backfield is worth. *Killed by:* a backfield where ESPN's total is obviously
   wrong — Green Bay's is currently 108 because Jacobs is zeroed, which is correct for 2026 but
   makes GB's `job worth` read 241 off the source pull instead.
2. **The seeded takes represent Matt's actual views.** *Killed by:* him reading them and
   disagreeing, which is one `clear` away.
3. **The injury sheet is otherwise complete.** Monangai says it is not. Nothing has re-swept it
   since Aug 30 and the Sept 5 pass must do so.
