# 473 · Five stragglers out of the store, and the two controls doc 457 was owed

*2 Oct 2026, 02:20 ET. Two items off `claude_todo.txt`, both small, both verified the usual way.*

## 1. The five docs outside `claude/` are out of the store

Doc 471 named five docs the 22 Sept and 1 Oct moves never listed because both moves listed `claude/` only. A subagent
read each one, wrote it verbatim (read-back asserted), and looked for a drive copy in six folders. **One has a drive copy:
`sources/FantasyPros_2024_Overall_ADP_Rankings.csv` is the registry's `Source\adp_registry\` page minus one trailing
newline, 343 rows identical.** The other four (`code/avail_pool.csv`, 113 KB, a pre-draft availability pool;
`01_league_and_managers.md`; `code_espn_pull_projections.py`; `code_league_real_schedule.py`, all August) **exist nowhere
else**, so the export is their only copy from here on. All five, with a README of hashes, are committed to
`_archive\store_20261002\`, staged back and hashed (6 of 6), then deleted from the store. The two CSVs were the ones 9
says the store must never hold; the pool alone was about 57,000 units.

## 2. P12 and P13, the two controls doc 457 asked for

**P12: a tight end on THE CALL this week whose team's tight-end target leader in the newest finished game is another man
with six or more targets and twice his.** Doc 457's Mayer-behind-Bowers case: the engine gives such a man no rate (a second
tight end has never cleared the screen), so he cannot reach THE CALL as a bet; P12 reads the leaders off `form_2026.csv`
without the engine and fails the build if one does. A calendar claim for a later week, or a row that says it fills a hole,
is not this and stays quiet.

**P13: the line under THE CALL, "Taking all N nets +X", counts only the rows marked "this week" and sums only their
nets.** Doc 457 made a bye-hole bet a calendar claim; doc 439 made the total count printed rows only; P13 holds both
with arithmetic on the printed cells.

Five controls in the selftest (72 of 72 now): the team's own leader on THE CALL is quiet; Mayer behind Bowers 13 to 3 this
week fires; the same man as a week-5 calendar claim is quiet; a total over the this-week row alone is quiet; a total that
counts the week-5 row fires. Quiet on tonight's live page and on the synthetic four-week page from doc 472.
`check_page_logic.py` is 71,332 B, 6109e8962d5d6446, pinned; the previous version is in `_archive\` with a 20261002_0210 suffix.

## 3. Open

- Doc 290 out of the store: still blocked on the copy route (doc 471).
- The 4.49 index row and the 9 rule 5 banner line at v9.40, one paste.
- The first four-week build: the matchup numbers, the blend at 0.43, and whether THE CALL chains a displaced starter (doc 472).
