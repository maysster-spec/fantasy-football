# THE TAKES CORPUS: PROMPTS AND PROCEDURE

**14 September 2026, third version.** The live copy is a page:
**https://claude.ai/artifact/BwUBENtMAZzTdjfgq7kqCJ**   nine copy buttons and the procedure.
This file is the offline mirror and the provenance. The prompts below and the ones on the page
are generated from one source, so they cannot drift apart.

> **READ `claude/30_gemini_notebook_pack_v2.md` BEFORE TOUCHING THIS.** It is dated 23 Aug 2026
> and it already answered most of what versions one and two of this file got wrong. Matt had to
> point me at it: *"somewhere in that long as hell project directive there is list that provides
> what tools i have access to."* Listing the folder is section 0.2's own rule and I skipped it.

---

## WHAT DOC 30 ALREADY ESTABLISHED, AND WHAT I HAD WRONG

| doc 30 said, 23 Aug | my v1/v2 said | now |
|---|---|---|
| **The product is Gemini Notebook**, renamed from NotebookLM on 16 Jul 2026 | called it NotebookLM throughout | corrected; Matt's own screenshot says Gemini Notebook |
| **Configure Chat**, Custom style, 10,000 characters, applies to every turn in that notebook | told him to paste the whole rule block per batch | **the rules move into Configure Chat, once per notebook.** This is the single biggest reduction in his work and it was already on the drive |
| **Native code execution can export CSV** from the Studio panel, gated by tier; **Matt has Google AI Pro** `[SOURCED: user, 2026-08-23]`, which was "rolling out" as of 21 Jul 2026 | had him copying Markdown tables | the extraction prompt asks for the CSV first and falls back. **Still open: which branch fires.** He reports back and doc 30's conditional closes |
| Citations render as chips; check the first rows on a Note export | not mentioned | carried onto the page |
| Auto-generated captions count; failures are private, unlisted, under 72 hours old, or no speech | had the failure modes roughly right | unchanged |
| **"Native bulk-add is not confirmed"** | claimed 250 one-at-a-time pastes | **CLOSED by Matt's screenshot**: the Website and YouTube URLs dialog reads *"To add multiple URLs, separate with a space or new line."* One paste per season, not one per episode |
| Discover Sources "only confirms it searches the web generically, it does not say it can find or add YouTube videos" | n/a | this is the answer to his question about the highlighted **Search the web for new sources** box: it is not where Prompt 1 goes |

**AND TWO THINGS I INVENTED THAT HE CORRECTLY REFUSED.**
1. **The MP3 path.** He never asked for it, I never said where the files would come from, and it
   added a download per episode for nothing. Withdrawn entirely.
2. **The CSV as a source.** Gemini Notebook accepts CSV as an input type, so his instinct was
   sound, but the Prompt 1 CSV carries episode titles and dates and **no player calls**, so it
   gives the extraction nothing to read. It stays out of the notebook; the date join is mine.

**WHICH GEMINI, AND THE SETTINGS.** `gemini.google.com`, Google AI Pro, **Deep Research** on.
Deep Research plans, asks him to approve the plan, then browses and cites. That is the specific
fix for the failure below: plain chat answered from search snippets.

---

## WHY THE FIRST RUN CAME BACK THIN

29 episodes, `transcript_available` UNKNOWN on all 29, nine rows with no date, tag pages and
aggregator mirrors instead of episodes, one row whose title said week 3 while its URL said week
2, two YouTube links out of 29, and coverage of two week-1 episodes and five week-2 across five
seasons when week 1 against week 2 is the single question section 4.31 raises.

1. **No number to hit.** "Every waiver episode across five seasons" lets a model stop at 29.
   **The new prompt demands a five-by-fourteen grid with MISSING written into every hole.** A
   grid with gaps is visibly incomplete; a list is not.
2. **Snippets, not pages.** The prompt now says to open the show's own channel and search inside
   it, and Deep Research browses rather than answering from a snippet.
3. **A question only Notebook can answer.** `transcript_available` is deleted. Notebook decides
   it at ingest.
4. **theScore was never on the list, and that was my omission.** Justin Boone's own show ran
   there twelve years, **609 episodes, ending with the farewell show on 14 May 2025**, covering
   2021 through 2024 in full `[SOURCED: Apple Podcasts listing and theScore's own farewell post,
   retrieved 14 Sep 2026]`. Matt's read that Boone's takes were hotter at theScore is a
   `[HYPOTHESIS]` this corpus can settle: same analyst, two employers, one scoring rule.

---

## THE PROCEDURE

1. **Gemini, nine runs.** Deep Research on. One prompt per show. Returns a coverage grid, then
   one block of bare URLs per season.
2. **One notebook per season.** Create notebook, rename `FF Takes 2021`. Add sources, Websites,
   paste that season's whole URL block from all nine shows, Insert. Pro is 300 sources a
   notebook and 500 notebooks, so a season fits. **Never mix two seasons in one notebook**: the
   season is the join key to the outcome data and it is the one thing that cannot be undone.
3. **Configure Chat, once per notebook.** Custom style, the block below, response length Longer.
4. **Extract. Gemini Notebook can now drive this itself, and that is the faster path.**
   It offered, on 16 Sept: leave the sources selected, and reply `Next`, `Next 3` or `Next 5`
   instead of re-pasting the prompt and re-ticking the panel. **Take the offer, with one guard
   and one correction.**
   - **THE GUARD, and it is the whole of it: every row it returns must name its source, and the
     batch must name every source it claims to have done.** Its offer rests on it remembering
     which sources are finished across turns. That is a state claim, not a documented feature,
     and if it drifts you get a repeated episode or a silent gap with no error. **Never take its
     progress count on trust: the file is the record.** Save each batch as its own CSV to
     `10_Gemni\Takes\<season>_<batch>.csv` rather than letting it append into one growing note,
     and I check for duplicates and gaps at the join. Nothing is lost if it miscounts.
   - **THE CORRECTION, UPDATED 16 Sept 18:45 after its second message: ASK IT TO NAME THEM.**
     It has now said outright *"leave all sources selected... you do not need to check or uncheck
     them between turns"*, and that it is tracking progress itself: **15 sources done, 14 processed
     YouTube episodes plus 1 URL with no transcript.** Leaving everything ticked is fine, but it
     destroys the guard above, because ticking was how the batch got identified. So the batch has
     to identify itself: **in the same reply as `Next 5`, ask it to list the five it just
     processed, by episode title and publication date.** Paste both to me. One extra line from you,
     and duplicates and gaps become checkable instead of invisible.
   - **THE SOURCE WITH NO TRANSCRIPT IS NOT "DONE", IT IS PROCESSED AND EMPTY.** Get its name.
     A source that yields nothing has to be recorded as a zero in the coverage file; counted as
     done it silently reduces coverage, and counted as pending it gets retried forever.
   - **If you would rather not trust its bookkeeping at all, the manual path still works:
     TEN ticked sources at a time, and let the output tell you if that is too many.**
   The short prompt below. Save each result to `10_Gemni\Takes\` as `<season>_<batch>.csv`.

   > **WHICH FOLDER, BECAUSE THERE ARE THREE AND MATT HIT THIS ON 16 SEPT.** He opened
   > `10_Gemni\Takes\` and found it empty. It was empty correctly, but nothing in the folder said
   > so, and two other places hold takes work:
   > - **`10_Gemni\Takes\`** is the EXTRACTION output. This one. It now carries a README saying so.
   > - **`The Takes Corpus\`** (at the 2026 root) is the raw LINK hunting, nine markdown files,
   >   finished 15 Sept. Input, not output.
   > - **`Source\takes_links\*.txt`** plus `Source\takes_coverage.csv` are those links cleaned per
   >   season, and the count of what each show is missing.
   > - **`Fantasy Analysts Takes.csv`** at the 2026 root is a 29-row early link list saved to the
   >   wrong place on 14 Sept. SUPERSEDED. It is not extraction output and nothing reads it.
   >
   > **AND BEFORE THE NEXT BATCH: GET THE FIFTEEN ALREADY-PROCESSED SOURCES ONTO DISK.** The
   > notebook says it has done 15. Nothing from them is in any folder, so that work exists only
   > inside a chat. One query: *"re-emit every source you have processed so far as one CSV in the
   > agreed schema."* Save it as `2021_batch0_recovered.csv` and check it before asking for more.
   **THE CHECK, and it is why the number stopped being a guess: the CSV must carry at least one
   row for EVERY source you ticked.** If a ticked episode is missing from the output entirely,
   the response ran out of room. Halve the batch and re-run that batch only. If ten comes back
   complete twice in a row, try fifteen.

> **AND ONE THING THE NOTEBOOK SAID THAT IS NOT TRUE, recorded so nobody inherits it (doc 323).**
> On 16 Sept it told Matt that *"Google's documentation highlights that... asking the model to
> perform dense, multi-field extractions across dozens of long transcripts simultaneously dilutes
> retrieval accuracy"* and that a smaller-subset rule is *"the recommendation from both Google's
> usage guidelines and model architecture best practices."* **Both Google pages were read in full
> that morning and neither says anything of the kind.** It also said a notebook stores "50+"
> sources; Pro is 300. **The underlying context-rot research it gestures at is real and published,
> so the direction may well be right, but the citation is invented, and an invented citation is
> the one thing this project treats as worse than no answer.**
>
> **WHY TEN, HONESTLY (doc 322).** The file used to say "three to five" with no reason attached and
> nothing measured behind it, and Matt asked for the backing. There is none, and there was none for
> five either. Here is what is actually known:
> - **Google documents no limit on how many sources one chat query may use** and no limit on the
>   length of one response. Its own help page says only that sources are *"always used in either
>   the entire set or the subset you select."* `[SOURCED: support.google.com/notebooklm/answer/16269187, undated, read 16 Sept 2026]`
> - **The documented caps are per NOTEBOOK and per DAY, not per query:** Pro is **300 sources a
>   notebook, 500 notebooks, 500 chat queries a day**. `[SOURCED: support.google.com/notebooklm/answer/16213268, change notice dated 2 Sept 2026, read 16 Sept 2026]`
>   **So batch size does not spend quota here.** At 250 episodes, five at a time is 50 runs and ten
>   is 25, both far inside 500. **It spends MATT'S TIME, and that is the only thing it spends.**
> - **What is real and unmeasured:** a long CSV can be truncated by an output ceiling, and a bad
>   batch costs its own size in re-runs. Both are mechanical; neither was measured on this task.
> - **What was a hunch with nothing behind it:** that the model's attention dilutes across many
>   transcripts. Still a hunch. Do not repeat it as a reason.
>
> **So the number is not the finding. The CHECK is.** Ten halves the paste-and-wait cycles against
> the old instruction, and the completeness check catches the one failure mode that actually
> matters. **The A/B that would settle it is on the to-do list and takes ten minutes:** tick 5, run
> PROMPT 2, save; tick 15 including those 5, run PROMPT 2, save; send me both. I compare rows per
> source and the share of rows carrying a citation.

---

## THE NINE SHOWS

1. **The Fantasy Footballers**   youtube.com/@thefantasyfootballers. Very active video channel. The easiest of the nine.
2. **theScore Fantasy Football Podcast with Justin Boone**   audio only, check YouTube Music. 609 episodes, ran 12 years, ended 14 May 2025. Covers 2021 to 2024 in full.
3. **Late-Round Fantasy Football (JJ Zachariason)**   youtube.com/@LateRoundQB. Weekly '15 Transactions for Week N' is the waiver episode.
4. **Harris Fantasy Football (Christopher Harris)**   578 episodes, daily show. Daily, so the waiver episode is Tue or Wed.
5. **Establish The Run**   youtube.com/@EstablishTheRun. Titles are literally 'Waiver Wire Week N'.
6. **FantasyPros Fantasy Football Podcast**   youtube.com/@FantasyProsFootball. Also publishes a written waiver article every week.
7. **Yahoo Fantasy Forecast**   youtube.com/@YahooFantasy. Justin Boone's post-theScore home. Same analyst, second employer.
8. **The Athletic Fantasy Football**   audio first, check YouTube Music. Weakest video presence of the nine.
9. **Rotoworld Fantasy Football Happy Hour**   youtube.com/@RotoworldFootball. Renamed from Rotoworld; search both names.

---

## PROMPT 1, ONE RUN PER SHOW

Identical for all nine except the SHOW line at the top. The Fantasy Footballers version, in
full; swap the show name for the others, or use the page's copy buttons.

```
SHOW: The Fantasy Footballers

I am building a source list for a measurement, not a reading list, and I will paste your links
straight into Gemini Notebook. Completeness is the only thing I am grading you on.

FIND, for this show only, for each of the 2021, 2022, 2023, 2024 and 2025 NFL seasons:

  A. Every WAIVER WIRE or add/drop episode for regular season weeks 1 through 14. These
     publish Monday to Wednesday. I want EVERY week of EVERY season, not a selection.
  B. Every PRESEASON sleepers, breakouts, busts, post-hype or draft-targets episode, usually
     July or August.

HOW TO LOOK, and this is exactly where the last attempt failed:
- Open the show's own YouTube channel and search inside it, then filter by upload date.
  Do not answer from a web search snippet. If you have not loaded the page, you have not
  found the episode.
- Check YouTube Music as well. A podcast that publishes no video is usually still there,
  because Google ingests podcast feeds into it.
- If the show changed its name between 2021 and 2025, search both names.

THE LINK RULE:
- ONE LINK PER EPISODE. A channel, a playlist, a show page or an archive index is useless.
- Give me youtube.com/watch?v=... or music.youtube.com/watch?v=... . If the episode is on
  neither, give me the show's own page for that episode, or its written waiver wire article
  for that week.
- NEVER give me Apple Podcasts, Spotify, iHeart, Podchaser, Goodpods, Deezer, Podcast
  Republic, Metacast or Musixmatch. I cannot use any of those.
- Never give me a tag page, a category page, a page-2 listing, or a third party blog
  recapping the show.

RETURN THREE PARTS, IN THIS ORDER, AND NOTHING ELSE.

PART 1, THE COVERAGE GRID. Five rows, one per season, and fourteen columns for weeks 1 to 14.
Put the episode title in the cell, or the word MISSING if you could not find that week. Add a
final row per season for the preseason episodes. I am going to read this grid to see what you
skipped, so write MISSING rather than leaving a cell blank or dropping a season.

PART 2, THE LINKS. One FENCED CODE BLOCK per season. Write the year on the line ABOVE the
fence as plain text, NEVER as a markdown heading and never inside the fence. Inside the fence:
one URL per line and nothing else on the line, no bullets, no numbers, no titles, no commentary,
no blank lines, no ``` inside. I paste the fence's contents straight into Gemini Notebook's Add
source box, so anything that is not a URL breaks the bulk paste.

PART 3, ONE LINE PER SEASON: how many of the fourteen weeks you found, and whether the show
existed at all that season.

Do not curate, rank, filter or recommend. Do not tell me which episodes are good. If an
episode looks routine, that is the reason to include it: routine episodes are the denominator
and skipping them is the one thing that ruins this.
```

---

## THE CONFIGURE CHAT BLOCK, PASTED ONCE PER NOTEBOOK

1,421 characters against a 10,000 character limit.

```
You are converting fantasy football podcast transcripts into rows of a dataset that will be
scored against what actually happened. These rules apply to every answer in this notebook.

1. You are not summarising and you are not selecting the interesting parts. Completeness
   matters more than insight. A player an analyst mentioned and was WRONG about is the most
   valuable row in this file, because without those rows there is no hit rate to compute.
2. Never add a player an analyst did not name. Never quote a number they did not say.
3. If you cannot tell who spoke, write UNATTRIBUTED rather than guessing.
4. Speech to text mangles player names. When a token is probably a garbled name, correct it
   and say so. If you cannot identify it, write UNKNOWN rather than a plausible player. A
   wrong name is worse than a missing one, because a wrong name joins to the wrong outcome.
5. Do not rank, order or editorialise rows. Emit them in the order they were discussed.
6. Every row names the source it came from, spelled exactly as the source panel spells it.
7. Output preference, in this order: if you have code execution, run it and export a CSV.
   If you do not, output a strict Markdown table and nothing else, and save it as a Note.
8. This league is half PPR with six-point passing touchdowns. Almost every public ranking
   assumes full PPR and four-point passing touchdowns. Say so whenever you use one.
```

---

## THE EXTRACTION PROMPT, PER BATCH OF TICKED SOURCES

Short because the standing rules now live in Configure Chat.

```
Process only the sources I have ticked in the source panel. Work through them one at a time,
in the order they appear, and finish one before starting the next.

FIRST, a name correction table. Speech to text mangles player names. Real examples from a
previous pass: "Davian Wicks", "Cam Scaboo", "Amarian Hampton", "Jaylen Coker".

  source_title, heard_as, corrected_to, confidence_HIGH_MED_LOW, why

THEN one row per player per analyst per episode. Include the players they praised, the ones
they dismissed in half a sentence, and the ones they listed and moved past.

  source_title, show, publish_date_ISO, nfl_week, analyst, player, position, team,
  call_type, direction, strength, horizon, verbatim, reason

  call_type   SLEEPER | BREAKOUT | BUST | WAIVER_ADD | WAIVER_FADE | HANDCUFF | STASH |
              START | SIT | RANKING_ONLY
  direction   UP | DOWN | NEUTRAL, relative to where the market has him
  strength    STRONG | MODERATE | HEDGED. Use HEDGED whenever they qualified it. Do not
              convert a maybe into a take. "I could see it going either way" is HEDGED and
              it still gets a row.
  horizon     THIS_WEEK | REST_OF_SEASON | NEXT_SEASON | DYNASTY
  verbatim    the sentence they actually said, quoted. Trimmed is fine, paraphrased is not.
  reason      the mechanism in a few words if they gave one: target share, the man ahead of
              him, a scheme change, red zone work, a snap count. Blank if they gave none.
              "They like him" is not a reason, leave it blank.
  publish_date_ISO and nfl_week   take them from the source title if it states them,
              otherwise write SUPPLIED and I will fill them in.

If an episode lists ten names and only discusses three, all ten get rows, with call_type
RANKING_ONLY for the seven. If a ticked source has no usable transcript, say so BY NAME and
move on. Do not silently drop it and do not tell me it was low value.

FINISH with five lines:
  1. one line per source: its title and how many rows came from it
  2. how many distinct players, and how many rows in total
  3. how many rows are HEDGED and how many RANKING_ONLY. If both are near zero you have
     filtered, and you should go back
  4. any name from the correction table you could not resolve
  5. anything you deliberately did not emit, and why
```

---

## HOW THE ROWS GET SCORED

**The join key is `player` normalised plus `season`**, against `stats_player_week_<season>.csv`,
which this project holds for 2020 through 2026.

* **PRESEASON call, horizon NEXT_SEASON or REST_OF_SEASON**: outcome is half-PPR per game over
  weeks 1 to 14 against the position's replacement rate, and against what his preseason ADP
  predicted using the section 1.1 registry price. Direction UP scores a hit if he beat the price.
* **WAIVER_ADD, horizon REST_OF_SEASON**: outcome is section 4.31's own bar, points per game from
  that week onward reaching replacement. The week is what makes this scoreable, which is why
  `source_title` is mandatory: the week comes off the episode and the episode off the title.
* **The denominator is every row.** That is the whole reason the prompt refuses to filter.
* **`strength` separates a conviction call from a name on a list**, which the accuracy contests
  cannot do (section 4.13d) and is the only reason this corpus could beat them.

**FALSIFIER, fixed before any of it runs:** if the top-quartile analyst's hit rate does not beat
the bottom quartile's by more than the sampling interval on the number of calls collected, the
answer is that analyst identity does not predict, and that is a finding worth having. Section
4.13d's four independent measurements all point that way already, so **expect a null and collect
the sample that could show one honestly.**
