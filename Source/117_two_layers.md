# 117 — The board has two jobs and they fight; player cards; the take that shouldn't have been there

**Date:** 2026-09-01.

---

## 1. THE DESIGN ANSWER MATT ASKED FOR

*"Is combining the right move for an at-a-glance reference?"* Combining was right. **One document
was not quite the right unit.** The board is doing two jobs and they pull in opposite directions:

| | the SCAN job | the READ job |
|---|---|---|
| when | on the clock, 60 seconds | between picks, or before the draft |
| question | who is the best player left that fits my caps | why do I feel uneasy about this guy |
| needs | density, ranking, **two or three signals per row** | prose, both sides of the argument, sources |
| prose is | a liability — it pushes the next row off the screen | the entire point |

Five sheets failed because they split by **subject** (RBs here, injuries there, analysts over
there) — so answering one question meant three documents. **The right split is by JOB, not by
subject.** One list, two layers:

- **the scan layer** — the row: rank, player, VBD, goes-at, and a small fixed set of marks
- **the read layer** — everything else, available *on demand*

On paper the read layer has to be always-visible, because paper has no on-demand. That is the
compromise the printed board makes, and it is why the note line is deliberately one line and gets
its boilerplate stripped. **On screen there is no compromise to make — which is exactly what
Matt's own instinct pointed at, and it is now built.**

**What I would NOT do:** add columns. Every column costs every row, forever, to serve the handful
of rows that need it. The `lean` column earns its place because it is one word and 34 players
carry one. A "bull case" column would be blank on 126 of 180 rows and unreadable on the other 54.

---

## 2. PLAYER CARDS — click any row on the live board

`card_data()` packs the whole profile into the row as a `data-card` attribute; a click renders it
in an overlay. **Status, backfield, bull, bear, where the commentary sits, the quote with its
source, and what changed recently** — colour-coded, bull in green, bear in red, the quote in blue.

Three things it does on purpose:
- **The board does not reload while a card is open.** That was the doc-103 bug in a new costume: a
  card that vanishes mid-sentence is worse than no card. `window.__cardOpen` freezes the 3-second
  refresh; Esc or any click closes it and the clock resumes.
- **No network.** The profile is already in the page. Draft night has no requests to spare and the
  card has to work when ESPN is the thing that broke.
- **Only rows with something to say are clickable.** A card that opens to say nothing trains you
  not to click.

`parse_takes.py --write` now also stamps `bull / bear / lean / quote / qsource / concrete` into
`player_context.csv` — update-only, asserting no other column moved, same discipline as the
backfield stamp. **54 players carry a bull case.**

*Verified by execution:* rendered in headless Chromium, clicked, screenshotted; the overlay shows,
Esc dismisses it, `display` goes `block` → `none`.

---

## 3. THREE FIXES FROM MATT'S READ OF THE PRINTED BOARD

**(a) The lean column was greyscale and understated.** It is now a coloured pill —
**BULL** (solid green) · bull (pale green) · split (grey) · bear (pale red) · **BEAR** (solid red).
Blank still means nobody has said anything, which is not agreement.

**(b) "I forget what OPEN means" — asked from page 4, where there was no key.** The key was on
page 1 only. I tried `--footer-html` and a repeating `<thead>`; **this build of wkhtmltopdf
silently ignores both** — it printed the warning for one and simply dropped the other, and page 4
came out with no key AND no column headers. The key is now **injected as a real row every 30
players**, which cannot be ignored because it is just more rows. *Verified by rendering page 4.*

**(c) THE TAKES SHOULD NEVER HAVE BEEN ON THIS DOCUMENT.** Matt: *"none of my random thoughts need
to be included... I only want to see the analyst unbiased takes and not my takes."*

He is right, and the board itself proved it: **D'Andre Swift's row carried BUY and FADE at the same
time** — BUY because both analyst panels rank him ahead of ADP, FADE because I had seeded a
down-take from a sentence he wrote in conversation. A row cannot be evidence and opinion at once
and stay readable.

The three seeded takes are **cleared** (Monangai, Brooks, Swift — all mine, paraphrased from his
messages, none of them things he actually asked to record). `make_board.py` now **omits takes by
default**; `--mine` puts them back for anyone who wants that.

**The split I have applied, which Matt should overrule if it is wrong:** the printed board carries
evidence only. The **live board still shows a MINE badge and your words on hover** — that is a
nudge at the moment of picking, which is what doc 108 was built for and what he asked for on
Aug 30. If he wants his own voice off that screen too, it is one flag.

---

## ASSUMPTIONS

1. **A row is clickable enough to be discovered.** It gets a pointer cursor and a hover highlight,
   and nothing says "click me". The mock is the test.
2. **The card's fixed section order is the right order.** Status first, argument second, quote
   third. Untested.
3. **Evidence-only on paper, opinion allowed on screen.** A judgement, not a finding. Stated here
   so it can be reversed in one line rather than discovered on draft night.
