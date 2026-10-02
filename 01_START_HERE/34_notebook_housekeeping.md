# 34 — GEMINI NOTEBOOK HOUSEKEEPING
**Aug 23, 2026.** Answers to the three admin questions from this round.

## 1. WHAT TO KEEP FROM THE 3 UPLOADED FILES

- **`analystbreakoutcalls.xlsx` — KEEP, this is the authoritative version.** Clean two-sheet
  structure (Raw Calls, Ranked Summaries), correct headers, correctly labeled source counts.
  Saved to Drive as `03_data/analyst_breakout_calls_2026.xlsx`.
- **`rawanalystcalls.csv` — KEEP, it's not redundant.** 126 rows, proper headers, includes the
  2026-specific downgrade calls (Levitan, Silva, Daigle, Mahserejian, Koerner) that aren't in
  the other file's raw sheet. This is the auditable raw-quote layer under the xlsx's summary.
  Saved to Drive as `04_source_data/raw_analyst_calls_2026.csv`.
- **`youtube_links__Sheet2.csv` — DROP, do not keep as a project source.** Malformed header row,
  76 rows, 2026-specific downgrade analysts missing — it's a subset of `rawanalystcalls.csv`
  with less in it. Not saved to Drive. If Gemini Notebook produces this export again, tell it to
  skip that export format.

## 2. THE DATE/TIMESTAMP EXTRACTION FAILURE — DIAGNOSIS

**[SOURCED: Google's own NotebookLM product blog, partial]** — for video/audio sources,
NotebookLM's citations link to a location in the **transcript**, not to the video's timestamp
overlay or its upload/publish date. The chat model only sees transcript text; a video's upload
date is page metadata that isn't part of that transcript, so it isn't in the model's visible
context. **[HYPOTHESIS beyond that point]** — but it matches exactly what happened: episode_date
came back UNKNOWN for nearly every row, timestamp for all of them, except the handful where the
date was likely spoken aloud in the audio itself.

**Fix for the next extraction pass:** stop asking the model to infer episode_date/timestamp from
the transcript — it structurally can't. Instead, hand it a short manifest pairing each source URL
with its known upload date before running the extraction prompt, and drop the timestamp column
from the schema entirely. It isn't retrievable this way.

## 3. NOTEBOOK WIPE / OFFLOAD

**Safe to wipe the chat now, keep the notebook and sources.** Gemini Notebook's persistent
"Configure Chat" custom instructions and the sources both live at the notebook level, independent
of chat history — clearing the chat doesn't lose either, so the standard header doesn't need
re-pasting unless the notebook itself gets deleted and recreated. Recommend wiping before the
next extraction pass regardless, so the model isn't anchored on the old prompt's framing when
given a revised one — same blind-extraction principle as not showing it `26_breakout_economics.md`
earlier this session.

Nothing else needs to be fed to the model for this round — the pre-rank board used data already
on hand (`board_edges_v6.csv`), no new sources required.

## 4. SECURITY FLAG, CARRIED FORWARD FROM HANDOFF_v2.md §9

A live `espn_s2` ESPN session cookie was reportedly pasted into a prior chat. That doc flags it
for rotation. Flagging again here because it also matters for the live-board tier 2 build in
`32`: **log out and back into ESPN Fantasy to rotate it before it's used anywhere**, and don't
paste it into a chat or notebook again. Not accessed, used, or acted on by this session.
