# 416 — A negative drop cost is not a gain, and the holes became dates

*24 Sept 2026, the same hour doc 415 shipped. Both found by looking at the live page after a run,
not by a guard.*

## 1. THE CALL WAS DOUBLE-COUNTING, AND ITS FIRST LIVE RENDER SHOWED IT
The 11:00 build printed:

> Cade Otton TE +13.1 · you would drop Devaughn Vele · that costs **−1.6** · net **+14.7**

**The negative is real.** `drop_costs()` is the season WITH a man minus the season WITHOUT him, and
it goes below zero when the best free body at his position already outscores him. **What is wrong
is subtracting it.** `worth` ALREADY assumes the best free body takes the seat, so crediting the
negative again counts one upgrade twice, off a single roster spot.

**Fixed: `net = worth − max(0, cost)`.** The true cost is still printed, marked *below
replacement*, because it is information; replacing a man who is below replacement is a separate
decision and earns its own row. Asserted directly, since no row in today's data exercises the
negative path: `13.1 − max(0, −1.6) = 13.1`, not 14.7.

**This is the third arithmetic defect THE CALL has surfaced in one session** — after four tight
ends totalling an impossible +54.4, and a ruled-out man offered as a drop. None of them were new;
grouping them into one row is what made them visible. **Four scattered tables hid three bad
numbers, and a table that adds up is the guard.**

## 2. THE HOLES ARE FOUR DATES AND NOW LOOK LIKE FOUR DATES
Doc 369 catalogued this on 19 Sept and it sat: *"a calendar of holes buried in a paragraph of
prose. It is four dates and it should look like four dates."* It was one run-on clause inside the
standfirst. **It was also in the wrong place**: a week with nobody at a position is a claim
deadline, so it belongs beside the decision it drives.

Now dated chips directly under THE CALL: **week 6 TE · week 8 K · week 10 QB**, under the line
*"Weeks you have nobody at a position, which is when a claim stops being optional."*

## 3. THE STANDFIRST LEADS WITH THE ANSWER
~~"A free player is worth what he scores above the man he replaces, in the weeks he replaces him,
and nothing else."~~ That is the METHOD, which doc 369 named as the defect and doc 411 fixed one
instance of. Now: **"What to claim, what it costs you, and when."**

## [NOT YET RUN] — what is left of doc 369
The cards section is the longest block on the page and the least read · print and PDF have never
been looked at.
