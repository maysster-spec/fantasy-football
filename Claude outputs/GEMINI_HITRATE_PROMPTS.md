# GEMINI PROMPTS FOR THE ANALYST HIT-RATE CORPUS

**13 September 2026.** Two prompts, for Matt's Gemini search step and his Gemini Notebook
processing step. Written to build a corpus that can be SCORED, which the existing one cannot be.

> **THIS IS NOT A DUPLICATE OF `Source\PODCAST_PROMPT.txt`, AND THAT FILE IS WHY WE NEED THIS ONE.**
> `PODCAST_PROMPT.txt` is a DRAFT-PREP summariser and it is good at that job. It contains the line
> **"Skip any player they only mention in passing."** For draft prep that is correct: Matt wanted
> the interesting names. **For a hit-rate test it is fatal, because the players an analyst mentioned
> and got wrong are the denominator.** A corpus of memorable takes measures nothing. Keep both
> files; they do different jobs and the difference is exactly this line.

---

## WHY THE EXISTING SAMPLE CANNOT BE SCORED, IN THREE FACTS

1. **No dates.** Doc 35: *"Episode dates are absent by design ... they are not recoverable from
   transcripts."* An undated call cannot be scored against what was knowable when it was made.
2. **No denominator.** The prompt above discarded passing mentions, so the corpus holds the names
   that sounded good, not every name called. That is `4.28`'s numerator-without-a-denominator
   defect at the collection stage.
3. **Wrong half of the calendar.** Doc 30's inventory is preseason sleeper episodes. **Matt is
   right: the waiver question needs IN-SEASON episodes**, which are almost absent.

Everything below is built to fix those three.

---

## PROMPT 1: EPISODE IDENTIFICATION (paste into Gemini with search enabled)

```
You are building a source list for a measurement, not a reading list. I need to score how often
named fantasy football analysts were RIGHT, so I need a complete, dated set of episodes across
five seasons, including the ordinary ones.

FIND, for each season 2021, 2022, 2023, 2024 and 2025, from these shows if they exist and any
other show that publishes on the same schedule:
  The Fantasy Footballers · Late-Round Fantasy Football (JJ Zachariason) · Harris Fantasy Football
  · Establish The Run · FantasyPros Fantasy Football Podcast · Fantasy Footballers Dynasty
  · The Athletic Fantasy Football · Rotoworld/NBC Fantasy Football Happy Hour

TWO KINDS OF EPISODE, AND I NEED BOTH. Most lists only give me the first kind.
  A. PRESEASON: the annual "sleepers", "breakouts", "busts", "post-hype", "draft targets" or
     "players I'm drafting" episode. Usually July or August. One to three per show per year.
  B. IN-SEASON WAIVER WIRE: the weekly waiver or add/drop episode, Monday through Wednesday,
     regular season weeks 1 through 14. This is the one I am missing and the one I care most
     about. I want EVERY week, not a selection.

FOR EACH EPISODE RETURN ONE CSV ROW, and return CSV only, no prose:

show,season,episode_title,episode_number,publish_date_ISO,nfl_week,kind,url,transcript_available

  publish_date_ISO  the actual publication date, YYYY-MM-DD. THIS FIELD IS MANDATORY. If you
                    cannot find a real date, put UNKNOWN. Never estimate one, never infer it from
                    the title, and never use the date you found the page.
  nfl_week          1 to 14 for kind=WAIVER; leave blank for kind=PRESEASON.
  kind              PRESEASON or WAIVER.
  transcript_available  YES if the page or its YouTube entry has captions or a written transcript,
                    NO if audio only, UNKNOWN if you could not check.

RULES:
- Load the page. Do not answer from a search snippet. If you only saw a snippet, put UNKNOWN in
  transcript_available and say so in a final line after the CSV.
- Do not skip an episode because it looks routine. Routine episodes are the denominator.
- Do not invent an episode number. Blank is fine.
- If a show changed name between 2021 and 2025, give both names in the show field separated by
  a slash, so I can join them later.
- At the end, after the CSV, give me one line per season: how many PRESEASON and how many WAIVER
  episodes you found, and which shows have gaps.
```

---

## PROMPT 2: NOTEBOOK PROCESSING (paste into Gemini Notebook, then add the transcript)

```
You are converting a fantasy football podcast transcript into rows of a dataset that will be
scored against what actually happened. You are not summarising and you are not selecting the
interesting parts. Completeness matters more than insight here.

STEP 1. RED TEAM THE TRANSCRIPT BEFORE YOU READ IT FOR CONTENT.
Speech-to-text mangles player names. Go through the transcript and list every token that is
probably a garbled player, team or analyst name, with your best correction and your confidence.
Real examples from a previous pass: "Davian Wicks", "Cam Scaboo", "Amarian Hampton",
"Jaylen Coker". Output this as a correction table FIRST:

  heard_as,corrected_to,confidence_HIGH_MED_LOW,why

If you cannot identify a garbled name, put UNKNOWN in corrected_to rather than guessing a
plausible player. A wrong name is worse than a missing one, because it will silently join to the
wrong outcome.

STEP 2. EXTRACT EVERY PLAYER CALL. Every one.
Include the players they praised, the players they dismissed in half a sentence, and the players
they listed and moved past. A player they mentioned and were WRONG about is the most valuable row
in this file, because without those rows I cannot compute a hit rate at all. Do not filter.

ONE CSV ROW PER PLAYER PER ANALYST. CSV only, no prose:

show,episode_title,publish_date_ISO,nfl_week,analyst,player,position,team,call_type,direction,strength,horizon,verbatim,reason

  analyst       the individual who said it, not the show. If two people say it, two rows.
                If you cannot tell who spoke, put UNATTRIBUTED.
  call_type     SLEEPER | BREAKOUT | BUST | WAIVER_ADD | WAIVER_FADE | HANDCUFF | STASH |
                START | SIT | RANKING_ONLY
  direction     UP | DOWN | NEUTRAL, relative to where the market has him
  strength      STRONG | MODERATE | HEDGED. Use HEDGED whenever they qualified it. Do not convert
                a maybe into a take. If they said "I could see it going either way", that is HEDGED
                and it still gets a row.
  horizon       THIS_WEEK | REST_OF_SEASON | NEXT_SEASON | DYNASTY
  verbatim      the sentence they actually said, quoted. Trimmed is fine, paraphrased is not.
  reason        the MECHANISM in a few words, if they gave one: target share, the man ahead of
                him, a scheme change, red zone work, a snap count. Blank if they gave none.
                "They like him" is not a reason; leave it blank.

RULES, AND THESE ARE THE ONES THAT MATTER:
- Quote a number only if they said it. Never estimate one for them.
- Do not add a player they did not name.
- Do not rank, order or editorialise the rows. Emit them in the order they were discussed.
- If the episode gives a list of ten names and only discusses three, all ten get rows, with
  call_type RANKING_ONLY for the seven.
- publish_date_ISO is mandatory on every row. If the transcript does not carry the date, I will
  supply it; put SUPPLIED and I will fill it.

STEP 3. SELF-CHECK, and report it after the CSV in four lines:
  1. how many distinct players you emitted, and how many rows
  2. how many rows are HEDGED, and how many are RANKING_ONLY (if both are near zero you have
     filtered, and you should go back)
  3. any name from STEP 1 that you could not resolve
  4. anything in the episode you deliberately did not emit, and why
```

---

## HOW THE ROWS GET SCORED ONCE HE HAS THEM

So the schema above is not arbitrary. **The join key is `player` normalised plus `season`**, against
`stats_player_week_<season>.csv`, which this project now holds for 2020 through 2026.

* **PRESEASON call, horizon NEXT_SEASON or REST_OF_SEASON**: outcome is half-PPR per game over
  weeks 1 to 14 against the position's replacement rate, and against what his preseason ADP
  predicted, using the §1.1 registry price. Direction UP scores a hit if he beat the price.
* **WAIVER_ADD, horizon REST_OF_SEASON**: outcome is §4.31's own bar, points per game from that
  week onward reaching replacement. The week field is what makes this scoreable and it is why
  `publish_date_ISO` is mandatory.
* **The denominator is every row**, which is the whole reason for STEP 2.
* **`strength` lets the test separate a conviction call from a name on a list**, which is the
  thing the accuracy contests cannot do (§4.13d) and is the only reason this corpus could beat
  them.

**FALSIFIER, fixed before any of it is run:** if the top-quartile analyst's hit rate does not beat
the bottom quartile's by more than the sampling interval on the number of calls collected, the
answer is that analyst identity does not predict, and that is a finding worth having. §4.13d's four
independent measurements all point that way already, so **expect a null and collect the sample that
could show one honestly.**
