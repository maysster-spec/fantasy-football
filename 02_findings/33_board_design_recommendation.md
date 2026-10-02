# 33 — DRAFT BOARD DESIGN: GRID vs. RANKINGS vs. LIVE vs. HYBRID
**Aug 23, 2026.**

## THE THREE ARTIFACTS AND WHAT EACH IS ACTUALLY FOR

- **Pre-rank list** (`prerank_board_full_v1.csv`, this round's deliverable) — ESPN pre-draft
  input and the tiebreak reference. List-native; ESPN's tool is list-native. Not a snap-decision
  tool by itself.
- **Grid** (`JUG_draft_grid_2026_1.xlsx`) — tier/position blocks. Deferred to a later round per
  your own instruction; not rebuilt this pass.
- **Live board** (`JUG_live_board_2026.html`) — real-time drafted-player state. Spec in `32`.

## IS THE GRID BETTER FOR SNAP DECISIONS? YES.

60 sec/pick means the question at the table is never "what's my exact rank order" — it's "what
tier am I in, how many are left in it, does it survive to my next pick." A tier-block grid
answers that in under 5 seconds by position. A long ranked list requires scanning or searching,
which is slower under a clock. **4.10** already establishes the underlying reason: talent falls
off in jagged cliffs, not a smooth curve — a grid's whole design is showing cliffs, a list's
isn't.

## IS A HYBRID BETTER? YES — but not the "merge into one big table" version.

Gemini's Optimization doc (`Fantasy_Football_Draft_Optimization.md`) recommends merging the
HTML and Excel artifacts into one combined tier-column table. That solves the wrong problem.
The actual risk in the current three-artifact setup isn't that the views are separate — it's
that **the drafted-player state can drift out of sync** between them if each is updated by hand
independently. Two people (or two files) tracking "who's gone" separately is how a stale grid
recommends an already-drafted player mid-draft.

**Recommendation: one shared live-state layer, two view modes on top of it, not one merged
table.** Concretely: the grid and the live board should read from the same drafted-state (the
tier 1 mechanism in `32`) so marking a pick drafted once updates both the tier grid and the
scrollable list simultaneously. A toggle switches which view is on screen; neither view is ever
allowed to show a player the other has already crossed out. That is the hybrid that's worth
building — shared truth, not shared table.

## UI / LOOK, FEEL, FUNCTION

- **Dark background, high contrast** — draft runs into the evening (8:00 PM start), likely a
  laptop or tablet screen in a room with other people; avoid a bright white sheet.
- **Tier blocks color-coded by position**, not by rank number — color is the fastest signal a
  human parses under time pressure, faster than reading a number.
- **Pick-number / on-the-clock indicator** always visible, large font — this is the one piece of
  state that changes every ~60 seconds and needs zero scrolling to find.
- **Survival probability shown only at the two decisive windows** — 17→32 (longest gap) and
  32→41 (steepest attrition, per Section 2.1) — not on every player every pick. Showing it
  everywhere buries the two moments it actually changes a decision.
- **Bye-week collision badge** inline on any player who'd stack a bye with Pickens (wk 14) or
  create a start-week gap with a roster piece already drafted (4.11) — this is exactly the kind
  of thing that's easy to miss at pick speed and costless to surface automatically.
- **Big touch targets** on the "mark drafted" control specifically, in case the fallback device
  on the night is a phone or tablet rather than the primary laptop.

## BOTTOM LINE

Grid = primary screen during the draft. Pre-rank list = tiebreak reference and the ESPN input,
open in a second tab/window. Live board = the shared state under both, per `32`. Build the
shared live-state layer before touching the grid's visual redesign — a good-looking grid
showing stale data is worse than a plain one showing correct data.
