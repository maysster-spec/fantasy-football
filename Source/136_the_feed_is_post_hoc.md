# 136 — The feed is a post-hoc record, not a live one. And that is a fixable problem.

*2026-09-02, 08:07. The live-to-live test finally ran, on a real 12-team ESPN league that drafted
to completion with autopick.*

**The result is the most useful thing this project has learned about draft night, and it is not
the result the tool reported.**

---

## 1. WHAT HAPPENED

`live_draft.py --watch` polled `lm-api-reads` every 3 seconds for **16 minutes**, 300+ polls,
while the room visibly drafted on screen — the browser was on the clock at pick 7 while the watch
reported **0 of 192 slots filled, `drafted=False`**.

Then, at **08:07:24, all 192 picks arrived in a single poll.**

```
[08:07:20] 0 of 192 slots filled  drafted=False  |  nothing new for 989s  (300 polls)
[08:07:24] pick   1  rd  1  team 12  Jahmyr Gibbs
[08:07:24] pick   2  rd  1  team  6  Bijan Robinson
   ... all 192, same timestamp ...
```

**One poll. Every pick. After the room finished.**

## 2. WHAT IT MEANS — and it is NOT "the endpoint is broken"

`lm-api-reads.fantasy.espn.com` is, by its own name, a **read replica**. The draft writes
somewhere else, and this replica does not receive the picks until the draft closes. That single
fact reconciles everything the project has seen:

| observation | previously explained as | actually |
|---|---|---|
| `--replay 2025` reads a full draft perfectly | the parser works | it works **because 2025 is finished** |
| ESPN mock rooms served only opening state (docs 118–125) | mock rooms are special | **they were live, and live is invisible** |
| the live board never advanced in three attempts | cookies, league id, shape | **the source, all along** |

**The picks are real, complete and correctly parsed.** 156 of 192 resolved to names, 12 were D/ST
(negative ids, expected), and 24 were players outside the 480-row board — cosmetic only, since the
already-drafted filter keys on id, not name. **The reader is fine. The source is wrong.**

## 3. THE TOOL REPORTED THE OPPOSITE, AND THAT IS A DEFECT

On filling the grid, `--watch` printed **"FEED WORKS END TO END."** It does not. The grid filling
is consistent with two opposite worlds — a live feed, or a post-hoc dump — and the message asserted
the wrong one. Had this happened at 8:40 PM on Sunday it would have told Matt the chain was healthy
minutes after it had failed him.

**FIXED.** `--watch` now counts **how many different polls delivered new picks**:

- picks arriving across **many** polls → `THE FEED IS LIVE`
- everything in **one** poll → `*** THIS IS NOT A LIVE FEED. ***`

`ERROR_PATTERNS` class: a success message that cannot distinguish success from the failure it was
written to detect. Same family as the D/ST filter that "passed" on a differently-shaped object.

## 4. THE FIX PATH — `probe_sources.py`

If the picks exist and one replica lags, the question is simply **which URL carries them live**.
The new script polls **eight candidate sources at once** during a running draft and names the first
one whose count rises:

| source | why it might work |
|---|---|
| `lm-api-reads` + `view=mDraftDetail` | the current one — the control |
| same, `Cache-Control: no-cache` | if a CDN is serving a cached body |
| same, `&_=<timestamp>` cache-buster | same, via the query string |
| **`fantasy.espn.com` (primary host)** | **the strongest candidate — not a replica** |
| primary + cache-buster | belt and braces |
| `lm-api-writes` host | the write path may read back live |
| `view=mDraftDetail&view=mStatus` | a second view can force a fresh materialisation |
| `/communication/?view=kona_league_communication` | the draft room's own event stream |

```
py probe_sources.py --url "<a running draft room URL>"
```

**Use league 1608900294 with its draft RESET — not a lobby mock.**
`[CORRECTED 2026-09-02: my first instruction said "an ESPN mock from the lobby." That is wrong and
docs 118–120 already said so — the lobby runs an EPHEMERAL league whose id this endpoint returns
LEAGUE_NOT_FOUND_DELETED for. A lobby mock cannot test a read endpoint that cannot see it. The only
proven-readable test bed is a real league Matt owns, and 1608900294 has already demonstrated it
serves this league's picks.]**
That league is already built, already full with twelve claimed teams, and already on autopick, so a
draft reset is the whole setup. Let it run through 15–20 picks and Ctrl+C for the verdict.
Whatever moves, `live_draft.py`'s `READS` constant gets pointed at it.

`[NOT YET VERIFIED AGAINST ESPN — this container's egress blocks fantasy.espn.com, so the script is
checked for syntax and response shape only. The network path is Matt's to confirm.]`

## 5. IF NO SOURCE MOVES

Then ESPN publishes live picks only over the draft room's own transport, and the definitive
diagnostic is to **read what the draft room itself requests**. With a mock room open, the desktop
browser bridge can dump the page's network calls and name the real endpoint directly. That is a
20-minute answer, not a research project — but it is only worth doing if §4 comes back empty.

## 6. WHAT THIS CHANGES FOR SEPTEMBER 7

**Nothing about the plan, and everything about the confidence in it.**

`DRAFT_BOARD.pdf` was always the plan; the live tool was the upgrade. Going in, we did not know
whether the tool would work. Now we know exactly why it does not, we know the picks are readable,
and we have a five-day window and a two-minute test loop to find the source that carries them.

**If the probe finds nothing by Saturday, draft off paper and lose nothing you were counting on.**

## Assumptions

1. **One league, one draft.** The post-hoc behaviour is confirmed once, on a 16-round autopick
   league. A second observation would come free with any probe run.
2. **Autopick drafted this room in seconds per pick.** A slower human draft might expose a lag that
   is long but finite rather than absolute. The probe would show that as a rising count with a
   delay, which is still usable — the board would simply trail the room.
3. **The 24 unnamed ids are outside the board, not missing from it.** Checked: none of them appear
   in `board_v8_fixed.csv`'s 480 rows.
