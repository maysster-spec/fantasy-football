# 411 — Three things a file already knew and no code read

*24 Sept 2026. Matt's red-team pass on the week sheet.*

## 1. THE VINTAGE BLOCK WAS AT THE TOP OF THE PAGE
*"why is this at the top? Do you know the objective for the page layout."* **Doc 369 set it and I
violated it:** the page opens with *"what to do, what changed since the last build, and what it
costs"*, and doc 369 names the exact failure in exact words — *"That is the method, not the
answer."* A table of where the page's own rates are stale is the method. **Moved below the
pickups, calendar and watch list.** The live warning still reaches him inline on the cost line.

## 2. THE HORIZONTAL SCROLL WAS A HEADER/CELL MISMATCH
The seat table's last column is headed **"his 2025"** and renders **`why`**. `best_2wk_2025` exists
in `inherit_2026.csv` and is read by NOTHING, so that column never had a source. One `why` note is
**900 characters**, which forced a scrollbar and pushed the numeric columns off the right of the
page. Matt hit the symptom before the mislabel. **Header now says `why`; text clipped to a sentence
with the full note in the tooltip. Longest visible cell: 900 to 88 characters.**

## 3. CHRIS BROOKS: THE CSV SAID SO IN ITS OWN NOTES
*"Chris Brooks is behind MarShawn Lloyd and is NOT behind Josh Jacobs. I've had this discussion
before and this bug snuck back in."*

`inherit_2026.csv`, GB row, in its own `why` field:
> *"CAVEAT: this seat is not an option any more, the job is already open"*

And `live_tag` said `out` in one word. **Neither was ever branched on.** `live_tag` only drew a
badge. Jacobs has been on the Commissioner's Exempt List since 30 Aug 2026, indefinitely — he is
not going to go down, he is down. A seat is an option on a job someone still HOLDS.

**Fixed:** a row whose starter is already in `GONE_FOR_WEEKS` drops out through the existing
`_seat_cut` mechanism and prints its reason: *"Chris Brooks (Josh Jacobs is already out, so this is
not a seat)."*

## THE SHAPE ALL THREE SHARE
**A fact sitting in a file that nothing branched on.** A caveat in a data file that no code reads
is a comment, not a guard. Same family as doc 407's `check_vintage` writing to a log nobody opens.
