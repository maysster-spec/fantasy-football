# 32 — LIVE BOARD SPEC: HANDOFF PACKAGE FOR "TRULY LIVE"
**Aug 23, 2026.** Target file: `JUG_live_board_2026.html` (already in the Drive Source folder).
"Truly live" = drafted players get crossed out / removed from availability in real time during
the Sept 7 draft, without Matt hand-editing a spreadsheet between picks. Paste this whole doc
into Gemini (or any coding model/agent) to build it. Two tiers — build tier 1 first, ship it,
only attempt tier 2 if there's time to test it before Sept 7.

## TIER 1 (recommended, build this) — manual mark, zero external dependency

- The board is a static HTML page holding all 317 players (use `prerank_board_full_v1.csv` as
  the data source) with an in-memory JS array — no localStorage (this file may be viewed in a
  context that doesn't persist it reliably; keep drafted-state in a plain JS variable for the
  session).
- Clicking a player row (or a small checkbox) marks them DRAFTED: greys out the row, moves it
  to a collapsed "drafted" section or strikes it through in place, and re-renders any
  tier-remaining / survival counts that depend on the live pool.
- One text input at the top: paste or type the last pick number; auto-advances an "on the
  clock" indicator using the known snake order (reverse standings, 12 teams, so pick→team is
  computable) — this is optional polish, not required for the core loop.
- Undo button (mis-clicks happen at 60 sec/pick).
- **Why tier 1 first:** 60 seconds per pick means a scraping glitch mid-draft costs more than it
  saves. A one-click manual mark is fast, has no failure mode worse than "I forgot to click,"
  and needs no credentials.

## TIER 2 (optional stretch) — auto-detect picks from the ESPN draft room

- Reads the live ESPN draft room DOM (the pick history table) via a browser extension /
  bookmarklet / Tampermonkey userscript running in the same browser tab as the draft, and pushes
  each new pick into tier 1's drafted-state as it appears — Matt never clicks anything.
- **Security note, must be in the build brief verbatim:** any approach that authenticates to
  ESPN's private draft API directly (rather than reading the already-logged-in draft room page
  in the browser) needs the `espn_s2` session cookie. `HANDOFF_v2.md` §9 already flags that a
  live `espn_s2` token was pasted into a prior chat and should be **rotated** (log out and back
  into ESPN Fantasy to invalidate the old one) before it's used in any new integration — and it
  should never be pasted into a chat/notebook again. The DOM-reading approach (extension reads
  the rendered page, not the API) avoids handling the cookie at all and is the safer of the two
  if tier 2 gets built.
- Test this against a real or mock ESPN draft room **before Sept 7**, not live. If it isn't
  proven working by Sept 5, ship without it — tier 1 alone is a complete, reliable board.

## WHAT TO HAND GEMINI, EXACTLY

1. This file.
2. `prerank_board_full_v1.csv` (the 317-row data source).
3. The current `JUG_live_board_2026.html` (pull from Drive) if it should be edited in place
   rather than rebuilt from scratch — cheaper if its existing layout/CSS is worth keeping.

Say so if this session should build tier 1 directly instead of handing it off — it's a small
enough job to do here if that's the faster path.
