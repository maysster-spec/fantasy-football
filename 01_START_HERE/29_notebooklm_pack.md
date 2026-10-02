# 29 — NOTEBOOKLM PACK: CORRECTED INSTRUCTIONS
**Aug 23, 2026.** Replaces section 1 of `claude/27_model_offload_plan.md`.
Verified against Google's own help page today, not from memory.

---

## THE AUDIT'S THREE POINTS — what I verified

**1. Missing files — correct, and fixed.** Everything referenced is in the zip.

**2. NotebookLM cannot output CSV — correct.** CSV is an accepted *input* source type. There is
no documented CSV export. Google's help page describes no export path at all. Asking for a
**strict Markdown table** is right, and it is what the rewritten prompt below does.
*Not verified:* the specific "Studio note → Export to Docs → Sheets" route. It is plausible and
costs nothing to try. If it is not there, select the table in the chat pane and paste it
straight into this chat — it is a few hundred rows and Markdown pastes cleanly.

**3. Transcript dependency — correct in premise, overstated in practice.**
Google's exact wording: *"Only public YouTube videos with captions, either user-uploaded or
**auto-generated**, are supported."* Auto-generated captions count, and essentially every
podcast on YouTube has them. The real failure modes are narrower:

- the video is private or unlisted
- it was uploaded **less than 72 hours ago**
- it has no speech
- captions exceed 500,000 words (not a risk for a podcast)

Also confirmed: **only the text transcript is imported**, never the audio. Limits are
**100 notebooks, 50 sources each, 500,000 words per source.**

Backups are still worth having. Two are named below.

---

## THE SOURCES TO ADD

**Primary — six shows, August 2024 and August 2025 episodes:**
```
Late-Round Fantasy Football        JJ Zachariason      "sleepers" "breakouts" "draft guide"
The Fantasy Footballers            Ballers             "Breakout Players" "Sleepers" "Busts"
Fantasy Life                       Dwain McFarland     "utilization" "breakouts"
Yahoo Fantasy Forecast             Matt Harmon         "Reception Perception" "breakouts"
Establish The Run                  Silva / Thorman     August draft-strategy episodes
The Action Network Fantasy         Chris Raybon        RB #3 on measured multi-year accuracy
```

**Backup 1 — Harris Football (Christopher Harris).** Long-running daily show, full YouTube
archive with captions, and he publishes an explicit annual sleepers list. Highest-reliability
substitute if a primary lacks captions.

**Backup 2 — FantasyPros Fantasy Football Podcast.** Their own YouTube channel is heavily
captioned and consistently posts a dedicated breakouts/sleepers episode each August. It also
gives you a control group: these are contest participants, so their calls should be *more*
conservative than the independents. **That contrast is itself the test of your theory that
breakout-callers avoid the contest.**

**If a video will not ingest:** open it on YouTube → `...` → **Show transcript** → copy → paste
into NotebookLM as a text source. Same result, one extra step.

---

## THE PROMPT — paste the standard header first, then this

```
From the sources in this notebook ONLY, extract every instance where a named analyst calls a
specific NFL player a breakout, sleeper, league-winner, or significantly undervalued relative
to his draft price. Ignore general praise. I need an explicit call.

Output a single strict Markdown data table and nothing else. No preamble, no commentary, no
bullet points after it. Save it as a Note.

Columns, in this exact order:

| analyst | show | episode_date | player | position | call_type | conviction | quote | timestamp |

Rules:
- episode_date is YYYY-MM-DD. If you cannot determine it from the source, write UNKNOWN.
  Do not guess a date.
- call_type is one of: breakout, sleeper, league-winner, undervalued, bust
- conviction is one of: strong, moderate, passing-mention. Judge it from the language used,
  not from your own opinion of the player.
- quote is verbatim, under 20 words.
- One row per call. If the same analyst names the same player in two episodes, that is two rows.
- Do NOT include a player unless a named analyst made the call inside one of these sources.
  If you are unsure who said it, write the analyst as UNKNOWN rather than attributing it.
- Escape any pipe characters inside a quote as \|

Sort by analyst, then episode_date.
```

**Then:** export the Note to Docs, or copy the table, and paste it back into the Claude chat.

---

## WHAT HAPPENS NEXT, AND WHY THIS IS WORTH THE EFFORT

You cannot score anyone's 2026 calls yet. You **can** score their 2024 and 2025 calls, because
those outcomes are already on disk here.

Claude then computes, per analyst:
- **hit rate** — share of their named calls that landed in the top decile of position-adjusted
  surplus that season
- **base rate** — what a random draftable player achieved, so the hit rate means something
- **lift** — hit rate divided by base rate
- **cost of being wrong** — average surplus of their misses, because an analyst who hits 3 of 10
  but whose misses were roster poison is not useful

**Only analysts whose lift clears the base rate get their 2026 calls onto the board.**

Two things to be honest about before you spend the evening on this:
1. Each analyst will have maybe 10–25 calls per season. Two seasons gets you 20–50 per analyst.
   That is enough to separate a 3× lift from a 1× lift. It is **not** enough to separate 1.3×
   from 1.0×. Expect a coarse answer.
2. Podcast calls are made with conviction language that varies by personality, not by
   confidence. The `conviction` column will be noisy. Treat "strong" as a weak signal.

It is still the only design available that measures breakout skill directly instead of
proxying it with an accuracy contest that is 97% blind to it.
