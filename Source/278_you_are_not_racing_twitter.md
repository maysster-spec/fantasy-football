# 278 — You are not racing Twitter, you are racing Thursday

Matt, 2026-09-10, correcting his own typo so the sentence reads the way he meant it:

> *"ESPN does NOT update as quick as 3rd party sites such as sleeper and others. plus there is
> twitter and specific people to follow for live updates. I don't think this makes a difference
> when waivers are mostly FA."*

**The premise about ESPN is right. The question he asked — what would make the news faster — has an
answer that is not a faster feed.**

---

## 1. The reframe, and it comes off this league's own transaction file

Doc 275 measured when this room actually acts. **POPULATION: every executed add in this league
2022–2025 that carries a timestamp, n=1,230, nothing excluded.**

- waiver claims: **86% fire on Thursday**, in a 3–5am batch settled on priority order
- free-agent adds: **48% on Thursday**, then Sunday 20%, Saturday 16%, Friday 14%
- **inside a live game window: 36 of 616 free-agent adds — 5.8%.** For waiver claims, **0.0%**
- **Matt himself: 41 executed adds, 31 on a Thursday, 0 ever inside a live game window**

So the gap he is trying to close is not the one he named. **Sleeper and Twitter buy minutes over
ESPN. The room buys him three days.** Nobody here is racing, which is why the edge is unclaimed
rather than worthless — and it also means a faster feed on its own converts nothing, because the
thing he lacks is not the news, it is **being anywhere near his phone with a decision already
made** at a time other than Thursday.

**And the speed only ever pays on one lane.** A waiver claim is a sealed auction settled Thursday
morning on priority; filing it Tuesday afternoon and filing it Wednesday at midnight settle
identically. **A never-rostered backup has no waiver period at all** — he is first-come,
first-served, and that is the only place on the board where a minute is worth anything.

---

## 2. What no app can do, which is why the answer is a task and not a download

The consumer apps all alert on **your own roster**. Sleeper's injury notifications cover *"every
starter and key bench piece on your roster"* `[SOURCED: lordskunk.com guide, updated 7 June 2026]`
— and nothing in its documentation describes following a player you do not roster. ESPN's app does
the same thing for the ESPN league he actually plays in.

**So the case that is already covered is the one that matters most: if one of HIS starters goes
down, his phone tells him.** That is also the highest-value case on the whole page, because his own
bar drops the moment his man is out — a handcuff to Judkins is worth real points where a random
inherited back is worth 0.1.

**The case nothing covers is the other eleven backfields.** No app will tell him that Cincinnati's
Chase Brown left a game, because Chase Brown is not his player — and Samaje Perine, the man who
would inherit, is free at 12.9% owned. That is the entire uncovered surface, and it is exactly what
`inherit_2026.csv` enumerates.

---

## 3. Shipped: a Sunday-evening sweep, 7:30pm Eastern

**`Sunday evening — did a job open up?`** — a scheduled task, first firing Sunday 13 September,
push notification on, bound to his computer so it can read the drive.

It reads `inherit_2026.csv` for the fourteen backfields whose direct backup is still free, reads
`MY_ROSTER.csv`, then web-searches that day's games for any of those starters leaving a game, being
ruled out, or going for imaging. If nothing happened it says so in one line and stops — **a quiet
Sunday is the most likely outcome and the task is instructed not to manufacture a recommendation.**
If a job did open it names the man to add, what the job pays, and whether he is a free agent tonight
or sits inside a waiver period until Thursday.

**Why 7:30pm and not Sunday morning.** The inactive list is final **90 minutes before kickoff**
`[SOURCED: legionreport.com, 26 August 2026]`, so an 11:15am check runs before the news exists and
an 11:45am check catches only the one-week absences. **The multi-week absences — the ones that make
a backup a season asset — happen during the games**, and by Wednesday everyone knows. Sunday
evening is the widest part of the gap between the injury and the room noticing it.

**Boundaries written into the task and absolute:** no waiver claim, no drop, nothing written to
ESPN, no priority spent. It recommends; he executes.

**It runs alongside the Tuesday task, as a SEPARATE task** — the same reason §0.1's own case study
gives: one task per occasion, so a failure names which occasion failed.

---

## 4. What is NOT recommended, and why

**A faster feed, on its own.** Measured above: the room is not racing, so minutes are not the
binding constraint. Buying an app to shave two minutes off a gap he is currently losing by three
days is optimising the wrong end.

**A Sleeper install for non-roster alerts.** Not recommended because I could not verify the feature
exists — its documented notifications are roster-scoped. Saying "install Sleeper and follow these
fourteen" would be a claim about how a product works, made without testing it, which is the same
class of defect as an unmeasured severity claim (§0.2). **If he wants the phone layer anyway, the
honest version is: his own players are already covered by the ESPN app he has.**

**More frequent polling.** A task every hour on a Sunday would catch an injury an hour sooner and
would fire twelve times to say nothing. Against a room that acts on Thursday, the marginal hour is
worth nothing and the noise is worth less than nothing.

---

## 5. What would change this answer

**If the room ever starts racing.** The 5.8% figure is what makes "beat Thursday" sufficient. If a
future season's `waiver_report_*.csv` shows in-game adds climbing, the constraint moves from *when
he looks* to *how fast he hears*, and the app question becomes live. **NOT YET RUN, and the input
is named: re-measure the in-game share on `waiver_report_2026.csv` once `py waivers.py --live` has
written it.** That file has never been generated and is already on his to-do list.
