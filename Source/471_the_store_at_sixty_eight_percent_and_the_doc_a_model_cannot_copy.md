# 471 · The store at sixty-eight percent, and the doc a model cannot copy

*2 Oct 2026, 01:30 ET. The milestone in 0.5(d): `project_info` reports `knowledge_size` above 1,600,000 of 2,000,000,
so the oldest numbered docs move out of the store. Matt's screenshot read 81% of project capacity; he asked whether that
was fine. It was not: the directive's own trigger sits at 80%.*

## 1. What moved

**Docs 200 to 299, 98 of them, out of the project store and into `_archive\store_20261001\claude\` on the drive, each
one hash-verified at three points before it was deleted.** 801,724 bytes of prose. The store went from 1,583,727 knowledge
units at doc 467 (plus docs 468 to 470 and the day's script pushes, unread) to **1,359,582, 68.0%**, 268 docs. Doc 384's
method, repeated: export from the store, compare against `Source\`, commit to the archive, stage the archive back and
compare again, then `project_delete`, then `project_info`.

The three comparisons, every one by SHA-256 on the bytes:

| step | result |
|---|---|
| store export against `Source\NNN_*.md` | 96 of 98 identical; one differs (doc 255, below); 222 and 290 have no export (below) |
| archive on the drive against the export | 98 of 98 identical, plus the README |
| store after the deletes | 268 docs; none of the 98 remain; 290 still present |

**The one that differs: doc 255.** The `Source\` copy carries the 28 Sept retraction banner from doc 435 (the two-runs-a-week
claim). The store copy never got it, because 9's rule 5 said correct the originating doc in place and nothing said re-push it.
The archive holds the store's copy, which is what was deleted; `Source\` holds the live one. No reader was wrong, because
every session since v9.8 reads the drive mirror when the bridge is up, but the store copy was stale for three days and I
only know because the move compares bytes. **The rule that follows: a banner applied to a doc in `Source\` is pushed to the
store in the same turn, like any other edit to a file the store holds.** Added to 9 rule 5 at the next directive version;
in `claude_todo.txt` until then.

## 2. The one that stays, and why

**`claude/290_the_in_season_catalog.md` (72 KB, about 23,000 units, 1.2% of the store) is still in the store and was not
deleted.** The export route runs the bytes through a model's reply, because `project_read` returns a document inline and the
only way to a file is to write what came back. Three subagents tried that document; a content classifier stopped each one
mid-write, and the harness then forbids the retry. Nothing in the document is sensitive that I can see; it is a catalog of
fifty research items from 10 Sept, and the same route copied 98 siblings without incident.

What I could verify without the bytes: the store copy has the same sixteen headings as the drive copy in the same order,
about 800 lines against the drive's exactly 800, and the same last three lines. That is strong and it is not a hash, and
the standard doc 384 set for this move is a hash. So it stays. **A session where `project_read` hands back a local file
path instead of inline text (the tool does that above some size) can finish it in one call**; the check is the hash
against `Source\290_the_in_season_catalog.md`, then `project_delete`.

## 3. Two things the move turned up

**A duplicate on the drive.** `Source\293_the_late_pick_needs_a_door-1.md` (19,479 bytes) sits beside
`293_the_late_pick_needs_a_door.md` (19,531 bytes). Google Drive writes a "-1" when two files of one name sync at once; the
unsuffixed copy is the one the store held and the one the export matches. I cannot delete or rename on the drive from here
(no shell on his machine this session), so the one-click delete is on Matt's list. 0.5(c)4: two names for one job.

**Three docs outside `claude/` that the 22 Sept move did not touch**, because that move listed `claude/` only:
`sources/FantasyPros_2024_Overall_ADP_Rankings.csv`, `code/avail_pool.csv` (two CSVs as text docs, which 9 says never to
hold in the store) and `01_league_and_managers.md`, plus two scripts at the root. Not moved tonight: I have no drive
location to hash them against without reading each one into context first. They are the first candidates for the next
move, and the registry already holds the 2024 FantasyPros page under `Source\adp_registry\`, so the CSV is almost certainly
a duplicate.

## 4. What this costs to run, measured

Six subagents, counting the three retries on 290 and the deletion, spent about 1.4 million tokens, roughly 13,000 a document
exported, none of it in this chat's context. The 22 Sept move did 200 items; this one did 98 in about two hours of wall time including the three retries on 290.
The season writes about 100 KB of docs a day (doc 384), prose at 0.32 units a byte, so **the store gains about 30,000 units
a day and the next trigger is roughly eight days out, about 10 Oct**, when docs 300 to 349 would be the next tranche.

## 5. Open

- NOT YET RUN: finish 290 from a session where the read lands as a file; hash, then delete.
- NOT YET RUN: the three non-`claude/` docs and two root scripts, hashed against the drive, next move.
- The 293 duplicate: Matt's one click.
- The banner rule for 9 rule 5: at the next directive version.
