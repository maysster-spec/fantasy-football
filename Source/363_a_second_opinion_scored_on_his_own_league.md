# 363 - A second opinion, scored on his own league, and the one thing it is actually good for

**2026-09-18. Matt asked whether I can read FantasyPros MyPlaybook: *"might help us fact check if you
could."* I can, through his Chrome, and the answer to what it should fact-check is narrower than the
pages make it look.**

---

## 1. WHAT IS AND IS NOT REACHABLE, CHECKED RATHER THAN ASSUMED

**Open web: no.** `WebFetch` on `available-players.php` returns a login wall. Loaded, not inferred:
the page renders *"Find the best available players in your league"* and a **Sync Your League** button
and no player data at all.

**Through his Chrome: yes, fully.** One browser connected (Windows), the account is signed in, and
the league is synced as **E-Discovery Keeper League / The Poetry of Junkyard Juggers**, host ESPN,
`leagueId=21985 teamId=9`. Both pages render completely.

**THE CONSTRAINT THAT LIMITS WHAT CAN BE BUILT ON IT: this runs through HIS browser.** It needs
Chrome open and the session live. **It cannot go in `ff.bat` and nothing scheduled can depend on it.**
Treat it as an on-demand check, never as a pipeline input.

---

## 2. WHAT THE TWO PAGES ACTUALLY HOLD

**`available-players.php`, the free pool in his league:** 44 QB, 90 RB, 99 WR, 61 TE, 37 K, 18 DST.
Rows carry a `data-pid` and are cleanly classed, so extraction is trivial. Three views per position:
ECR with opponent and matchup, a season stat table, and a **week-by-week grid out to week 17**.

**AND IT PRINTS THE BAR WITHOUT BEING ASKED.** The first row of each position table carries the class
`my-player-row my-player-row__top-player`: **his own best player at that position, shown as the
comparison.** Jalen Hurts heads the QB table for that reason and not because the sync is broken. That
is our own THE BAR (doc 259, §4.33) computed by an outside source on his scoring.

**`cheat-sheets.php`:** full positional ECR, every player rather than only the free ones, **with
injury status inline** (Q, O, D, IR next to the name).

**Both are scored on HIS custom settings**, which the page states in terms: *"RANKINGS ARE BASED ON
OUR EXPERT CONSENSUS RANKINGS AND THE CUSTOM SCORING SETTINGS FOR THIS LEAGUE."*

---

## 3. THE CRITIC'S PART: ECR IS NOT A BETTER PROJECTION AND THIS PROJECT HAS MEASURED THAT

Before anyone starts following these ranks, §4.13d already establishes, on this project's own data:
- the six-ranker panel is **one opinion measured six times**, mean pairwise r **0.81**;
- the FantasyPros accuracy contest is **structurally blind to breakout skill**, where being 10%
  tidier on ordinary players scores 2.80x as much as perfect foresight on every breakout;
- and **expert disagreement, controlling for ADP level, predicts finishing WORSE**: −0.244, p=0.0009.

**So ECR is a DIFFERENT opinion, not a better one, and "FantasyPros ranks him higher" is not an
argument.** §4.4 already carries the preseason divergence between our board and ECR
(TE +18.0 · QB +15.7 · RB +8.1 · WR −8.3) and that is a calibration fact, not a reason to defer.

**What it is legitimately good for is DISAGREEMENT DETECTION, which is a different job from ranking.**

---

## 4. THE ONE RECOMMENDATION: USE IT ON INJURY STATUS, NOT ON RANKS

**The highest-value cross-check is the cheat sheet's Q / O / D / IR flags against
`Source\injuries_2026.csv`.** Three reasons, and all three are already measured here:
1. **`injuries_2026.csv` is the file this project itself flags as most likely to be a day stale**
   (`00_START_HERE.md` §6). A second source on the same fact is exactly what a staleness check needs.
2. **Availability is the strongest downside signal in the project**: played ≤12 games last season
   measures **−19.4 points, p=0.00004** on n=735 (§4.22, §4.25b). Being wrong about who is available
   costs more than being wrong about who is better.
3. **It is a FACT check, not an opinion check.** Whether a man is listed Out is observable; whether
   he is the 14th best receiver is not. §4.13d's objections do not touch it.

**Second, and cheap: the free-pool list against `FREE_UNRANKED_<date>.csv` and `WIRE_<date>.csv`.**
Not to re-rank anything, only to catch a name our ESPN pull has on the wrong side of the owned line.

**NOT YET RUN, form stated (§0.5a2): for every player on his roster and on the wire, does the
FantasyPros status flag agree with `injuries_2026.csv`? Filter `my-player-row` out of the pool first;
see §5's retraction. POPULATION: the ~350 free players plus his
15. OUTCOME: count of disagreements, split by which source is more recent. BASELINE: zero.** The
extraction is a dozen lines of JavaScript and the join is on name plus team, since FantasyPros uses
its own `data-pid` and we key on `espn_id` (§3: no id in common, so name + position + team is the
key, never less).

**NOT a new scheduled job.** It needs his browser, so it belongs in the Sunday-morning read where he
is at the machine anyway, and it is worth running on exactly one question: has anybody's status
changed since our file was written.

---

## 5. THERE IS NOTHING TO SCRAPE AND NOTHING TO BUILD. THE DATA IS ALREADY JSON IN THE PAGE.

Matt asked whether a Chrome extension would help, the way `espn_bridge` did for the draft. **It
would not, and the reason is that the problem is already solved twice over.** `espn_bridge` existed
because ESPN's read replica published the draft only after it ended (doc 136), so there was no other
way to see live picks. Nothing here is hidden like that.

**Checked on the live page: there is no export button anywhere** (one link to FantasyPros'
commercial API in the footer, nothing else). **But two window objects hold the whole thing already:**

```js
window.playerPool          // every player the page RENDERS, by position, as FantasyPros ids
window.fp_injuries_data    // { sport, count, injuries[], covids }
```

**~~`playerPool` is the free pool.~~ RETRACTED WITHIN THE HOUR, AND THIS IS THE CORRECTION.**
`playerPool` is **everything the page displays, which is Matt's own players PLUS the free agents.**
Proved rather than argued: Mike Washington Jr. is on Matt's roster and his FantasyPros id `28108`
**is in `window.playerPool.RB`**, and all six of Matt's backs sit at the top of the RB table carrying
the class `my-player-row`. Counts are QB 44 · RB 89 · WR 98 · TE 60 · K 36 · DST 17 and those are
DISPLAYED counts, not free counts.

**AND §2 OF THIS DOC UNDERSTATED THE SAME THING.** The `my-player-row` block is not one player as a
bar; it is **every player Matt owns at that position**. I read rows 2 to 7 of the RB table as the
top of the free pool and they were his own roster. **Filter on `my-player-row` before treating any
of this as the wire**, which is the whole point of using it as a cross-check and would have inverted
the answer if it had gone out unchecked.

**`fp_injuries_data.injuries` is 332 records and is RICHER THAN OUR OWN FILE.** One record, verbatim
from the page:

```json
{"name":"Nico Collins","player_id":20130,"team_id":"HOU","position_id":"WR",
 "status":"OUT","status_short":"O","injury_type":"Hamstring",
 "injury_update_date":"2026-09-18 00:00:00","probability_of_playing":"0",
 "practice_1":"Limit","practice_2":"DNP","practice_3":"DNP","ir_weeks":[]}
```

**The two fields that matter and that we do not have:**
1. **`injury_update_date`.** Our freshness problem is that `injuries_2026.csv` carries a file mtime
   and not a per-player update time. This carries one per record, so a stale ROW can be caught
   inside a fresh FILE, which no mtime check can do.
2. **`practice_1/2/3`.** The three practice reports are the leading indicator; a status flips to OUT
   after two DNPs, not before them. **We have the verdict and they have the evidence.**

**SO THE EXTRACTION IS ONE LINE, NOT A PROJECT:** run
`JSON.stringify({pool:window.playerPool, inj:window.fp_injuries_data.injuries})` in the page through
Claude in Chrome, and commit the result to `Source\`. **No extension, no scraping, no parser, no
maintenance.**

**THE JOIN IS THE ONLY REAL WORK, AND §3 GOVERNS IT.** FantasyPros keys on its own `player_id`
(and carries a `yahoo_id`); we key on `espn_id`. **There is no id in common, so the key is name +
position + team, never less, and the alias table must be generated rather than hand-maintained.**
332 records is small enough that unmatched rows should be asserted on, not defaulted away, which is
the doc 251 failure this project has already paid for once.

---

## 6. THE COMMENTARY, WHICH IS WHAT MATT ACTUALLY WANTS, AND WHERE IT LIVES

Matt: *"I find it useful to have everything in one place... If I have the commentary I think easier
to point out when the model got something wrong as well."* **That second reason is the strong one
and it is this project's own method applied to players: a numbered doc is the EVIDENCE and the
directive is the CLAIM. Commentary is the evidence layer our sheets do not have.**

**WHAT IS THERE, CHECKED:**
- **A per-player teaser in the NEWS / NOTES column**, roughly 60 to 80 characters, **truncated
  SERVER-SIDE** (the ellipsis is in the HTML, so no amount of CSS or scrolling reveals more). Each
  carries the FantasyPros player id, so it joins cleanly to everything else on the page.
- **The full note sits behind an on-demand player card**, one fetch per player. **350 fetches is the
  wrong shape** for a nightly job.
- **A bulk feed exists at `/nfl/player-news.php`** and loads. **NOT YET EXTRACTED:** two passes at
  its DOM returned the navigation notifications rather than the feed, so it lazy-loads or classes
  its items in a way the first attempt missed. **That page, not the player cards, is the right
  target.**

**TWO KINDS OF CONTENT ARE MIXED IN ONE COLUMN AND IT SHOWS IN THE PROSE:**
- **FantasyPros staff analysis, first person:** *"I know Rico Dowdle had only ten touches and 21
  total yards in Wee..."*
- **Syndicated wire copy, headline shaped, ending in a »:** *"Mike Washington Jr. sees seven touches
  in Week 1 win »"*

**HIS QUESTION WAS WHO SOURCES WHAT, AND THAT IS STILL OPEN.** The » items read as wire and the
first-person ones as staff, but **no attribution string was captured and the network URLs are not
visible to this session**, so calling either one RotoWire would be a guess. `[NOT ESTABLISHED]`

**AND WHETHER IT DUPLICATES ESPN IS NOT CHECKED AT ALL.** Nobody looked at ESPN's notes this
session. `Source\player_context.csv` already exists and `apply_research.py` stamps dated news onto
it, so **the comparison starts there, against what we already hold, before any new pull is built.**
`[NOT YET RUN]`
