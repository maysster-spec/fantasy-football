# 288 — THE CHARTER FOR A STRANGER
### Matt asked whether a new chat in this project should red-team the in-season work. Yes — and here is why my own red team cannot do it, plus the first thing the audit found before it started.
*2026-09-11. Decision doc. The charter itself is `Source\IN_SEASON_REDTEAM_HANDOFF.md`.*

---

## 1. THE QUESTION

Matt, verbatim: *"what if we have another chat within this same project and can red team the work or
just be the new director?... my concern now is that stuff gets lost in the handover. my concern now is
that we covered so much that I'm not sure if you're on red team job will do the same trick as a
another check. completely new to the project I do that doesn't start by using our evaluations but by
judging them... you do a good job of catching stuff, but it's only after revisiting."*

**Recommendation: yes, a fresh chat, with a written charter — not a fresh chat alone.** A fresh chat
alone would make the problem worse, for a reason he did not name and I would not have volunteered.

## 2. WHY A FRESH CHAT ALONE FAILS: THE DIRECTIVE IS AN INSTRUCTION, NOT A BODY OF EVIDENCE

A new session in this project reads `00_PROJECT_DIRECTIVE.md` as its system prompt. **That file
contains at least eight sentences whose literal function is to stop a reader re-opening a question:**

> *"PICK 8 IS CLOSED — open no further sensitivity on it"* · *"Do not rebuild it"* · *"Do not
> re-derive this"* · *"Do not re-audit this"* · *"Do not chase it"* · *"Do not re-derive any of this
> at the draft"* · *"Do not tilt the board"* · *"Do not add an environment column"*

Every one was written for a good reason and most of them saved real hours. **But a stranger reading
them arrives pre-committed against questioning exactly the things that most need questioning.** That
is a stronger version of the risk Matt named: not that context is lost in the handover, but that the
*wrong* context survives it perfectly. A fresh chat would inherit our conclusions as instructions and
our evidence as footnotes — the opposite of what he asked for.

**So the charter does three things a fresh chat cannot do by itself:** it voids those clauses for the
duration of the audit, it scopes the audit to the in-season work so the draft-side ones are moot, and
it says in terms *read the numbered docs as evidence and the directive's §4 as claims.*

## 3. THE SELF-ASSESSMENT. HE IS RIGHT, AND IT IS 7 OF 7.

**Every one of the last seven docs was triggered by a question Matt asked, not by my own review.**
281 the phantom roster seat · 282 the Strange retraction that did not reach the code · 283 LaPorta ·
284 the receiver room · 285 the other three receivers · 286 Sutton · 287 Bryant and Franklin.

My red team in this session re-checked arithmetic, populations and sample sizes **inside the frame I
had already chosen.** It did not once question the frame unprompted. That is not modesty; it is the
measured pattern, and it is why the answer to his question is yes.

## 4. AND THE AUDIT FOUND SOMETHING BEFORE IT STARTED — I GOT ITS BIGGEST NUMBER WRONG TWICE IN ONE HOUR

Writing the charter's "where is the ice thinnest" section required stating the in-season bar for
"startable". Verified against the spine this session: `code_universe_v5.csv` reproduces §4.1 exactly
(QB12 Dart 341.603 · RB30 Warren 168.589 · WR30 Metcalf 163.540 · TE12 Andrews 140.295; Allen 421.9
confirming §2's 6-point passing TD). **Those are full-season 17-game projections. And doc 12's
per-game replacement rates are those same totals divided by 17, to four significant figures at all
four positions** — 20.094/20.09, 9.917/9.92, 9.620/9.62, 8.253/8.25, implied divisor 16.99–17.01.

**Four independent measurements do not share a divisor to four figures. Doc 12's rates are a
DERIVATION of §4.1, not a measurement**, which is why §4.17 could not reproduce doc 12's sample
sizes. §4.19, §4.31 and the sheet all call them *"measured"*. **That label is false and §3 forbids
it** — the same defect as §6's doctrine being labelled "in his own words" when it was a paraphrase.

**The substantive half is bigger.** The bar is what ESPN projected in August, and §4.23 measured what
those projections are worth: actual ÷ projected **QB 0.905 · RB 0.917 · WR 0.858 · TE 0.928.**
Deflated by this project's own ratios the bar becomes **QB 18.18 · RB 9.10 · WR 8.25 · TE 7.66** —
**8 to 14 percent lower than the bar the wire is using.** If that holds, every "not startable" verdict
inside that band told Matt a free agent could not help him when he could. **`[NOT YET RUN — the
testable form is written in the charter §6(1); population, baseline and direction all stated.]`**

**My two wrong versions, kept because the shape is the point.** First: *"§4.1 ÷ 14 disagrees with doc
12, so the project runs two systems"* — wrong, I had invented the ÷14 system by assuming §4.1 was a
weeks-1–14 total. Second: *"the bar may be high or low, unknown"* — also wrong, because §4.23 had
already measured the sign and I had not looked. **Both mine, both inside an hour, and neither would
have been caught by the red team I run on my own work.**

## 5. WHAT THE CHARTER CONTAINS

Scope (docs 223–287, `wire.py`, `sheet_engine.py`, `build_inherit.py`, `width_study.py` and their
CSVs; the draft explicitly out) · the voided clauses · the 7-of-7 count · the three error shapes that
actually occurred (a guard that passes while doing nothing · a retraction that never reached the code
· right arithmetic on the wrong object) · §0.5(c)'s catalog-first protocol · the standing rules that
DO bind, including Matt's verbatim instructions · **nine named thin-ice items, ranked** · and a short
§7 of things I do NOT believe are wrong, so the auditor has something to aim at.

**The nine, in order:** the startable bar above · `inherit_2026.csv`'s 11.2 gate being a median used
as a pass/fail bar on n=40 · `team_shape_2025.csv` shipped on one season at persistence r=+0.294 ·
doc 284 leading with a player-level figure where the clustered p is 0.064 on a team constant · doc
251's 60% resting on n=15 · doc 287's 14 of 141 · the 33.3%-vs-8.3% screen quoted four times without
its n · Sutton's "median" on one season when three are on the drive · **and the process defect that
may outrank all of them: grep every retraction in 223–287 against the code and report which ones live
only in prose.** Doc 282 is proof that class exists.

## 6. THE OPEN THREAD THIS CREATES

**The audit's findings have to come back into the directive, and nothing in this project has a working
path for that.** `OPEN_THREADS.md` scrapes doc markers and `matt_todo.txt` catches what I ask Matt to
run, but neither catches *a claim the auditor kills*. **`[OPEN]` — decide, before the audit ships its
catalog, who edits §4 and how the kill is recorded.** Doc 282 exists because that path was missing one
level down.
