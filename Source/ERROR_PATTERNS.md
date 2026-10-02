# ERROR PATTERNS — E-Discovery Keeper League 2026
**Purpose:** raise the next model's floor by naming the failure modes this project has
actually produced, with real numbers, root causes, and the check that catches each one.
**Read before doing analytical work. Append to it when you make a new one.**

**Schema, used for every entry:**
`SYMPTOM` what it looks like from the inside ·
`EXAMPLE` real numbers from this project ·
`CAUSE` why it happened ·
`CAUGHT BY` what surfaced it ·
`RULE` the imperative ·
`TRIGGER` when to run the check.

**Scoreboard through Sep 1, 2026:** 33 logged errors. **13 were caught by the user, not by
the model** — four of them in the Aug 31 / Sep 1 draft-tool week alone (**C4, D8, E8, A16**).
**C4 is the most expensive defect this project has produced**: it would have made the live draft
tool declare the draft finished before pick 1.02 on draft night, and it was found because the
user re-ran a failing command against a different room instead of accepting an explanation.

The three added Aug 22 (**A15, C3, E7**) were caught by a deterministic audit
script rather than by a person or by the model reading its own work — the first time that has
happened in this project. Of the 7 times the model told the user a data source was not worth supplying,
**it was wrong 5 times.**

**Transcription status:** the pre-Aug-20 backlog named at the foot of this file is now
transcribed — **A10–A14, B5, B6, D6, D7, E5, E6.** Nothing from the Cowork thread remains
untranscribed.

**If you read three entries, read E8, C4 and A11.** **E8** is the failure mode this project
produces most often now: a measurement, then a mechanism invented to explain it. **C4** is what E8 cost — four documents of theory while the real bug sat in an edited line. **A11** (a coefficient applied to a
population it was not fitted on — it moved a real availability number from 0.95 to 0.15) and
**B1** (an unidentified file overturning three findings). They are the same mistake in two
different places: *acting on something before establishing what it is.*

---

# BUCKET A — STATISTICAL INFERENCE
*The largest bucket, and the one that produced confident wrong answers rather than obvious
breakage. Every entry here shipped to the user before being caught.*

### A1 · Underpowered test reported as a refutation
**SYMPTOM** A null result on a small sample, written up as "X is dead."
**EXAMPLE** Tested whether defensive strength persists using 2024→2025, **n=32 teams**. Got
RB +0.26, WR −0.03, TE +0.27, all p>0.14. Declared strength of schedule's premise dead and
retracted a shipped recommendation. The project **already contained** the powered version:
2006–2025, **n=608 team-seasons**, RB +0.352 · QB +0.234 · WR +0.216 · TE +0.192, all
p<1e-5. At n=32 the power to detect r=0.25 is roughly **30%.**
**CAUSE** Ran the convenient test rather than the correct one, and did not compute power.
**CAUGHT BY** The user asking where the SOS numbers came from.
**RULE** Before writing "null," state the sample size and the effect size the test could
have detected. If power is below 80% for a plausible effect, the word is **underpowered**,
not null.
**TRIGGER** Any n below ~200 for a correlation, or any subgroup analysis.

### A2 · Statistic read off a pilot run
**SYMPTOM** A headline number from a small first pass, before the real run finishes.
**EXAMPLE** N=25 gave Spearman(week 1–14 points, dollars) = **−0.03**, reported as "the two
objectives disagree." N=1,250 gave **+0.852**. The standard error on the dollar mean at N=25
was ±$40 on a mean near $250.
**CAUSE** Treated a smoke test as a result.
**RULE** A pilot run verifies that code executes. It never produces a reported number.
Compute the standard error of the underlying means before reading any rank correlation.
**TRIGGER** Any simulation output before the full N has run.

### A3 · Shared-term artifact
**SYMPTOM** Two constructed variables correlate impressively; both contain the same term.
**EXAMPLE** Ranked analysts by `corr(ADP − ranker, ADP − finish)`. "GC" scored **+0.665** and
was reported as the best ranker on the board. Both sides contain ADP, so any ranker noisier
than ADP scores well by construction. The **partial correlation controlling for ADP is
−0.423** — following GC actively hurt.
**CAUSE** Difference scores sharing a component.
**CAUGHT BY** Self, while writing up. Nearly shipped.
**RULE** Never correlate two differences that share a term. Regress the outcome on both
inputs and read the partial coefficient.
**TRIGGER** Any variable defined as `A − B` compared to another containing A or B.

### A4 · Leverage point
**SYMPTOM** A clean regression slope on a small n, no residual inspection.
**EXAMPLE** Team-projection shrinkage reported at slope **0.697**. One row had
`actual_2025 = 0` and levered the fit. Correct on n=32: **0.371, SE 0.049, t vs 1 = −12.81.**
The corrected number was *stronger*, which is why nobody would have questioned the original.
**CAUSE** Fitted without plotting or filtering degenerate rows.
**RULE** Before reporting a slope, print the rows with the largest residuals and every row
where a variable is exactly zero.
**TRIGGER** Any regression with n below ~100.

### A5 · Unclustered inference on a group-level regressor
**SYMPTOM** A team-level variable assigned to every player on that team, then bootstrapped
over players.
**EXAMPLE** PROE is constant within a team. Assigning it to ~210 players gives roughly **32
independent values, not 210.** A player-level bootstrap would have produced a confidence
interval far too narrow and passed the metric spuriously. **Clustered by team, ΔOOS R² =
+0.00206, CI [−0.00200, +0.00559]** — correctly fails.
**CAUSE** Effective sample size ignored.
**RULE** When a regressor is constant within a group, resample **groups**, not rows. Say so
in the write-up.
**TRIGGER** Any team-level, coach-level, or scheme-level feature applied to players.

### A6 · Multiple comparisons unacknowledged
**SYMPTOM** A z-score above 2 in a wide scan, reported as a discovery.
**EXAMPLE** Franchise bias tested across ~12 managers × 32 teams = **384 combinations.**
z>2.3 occurs by chance at that width. Bonferroni threshold ≈ 3.6. **Only herman allen →
Washington (z=4.08) clears it**; Kam → Kansas City (3.46) is borderline; the other four are
inside the noise floor.
**CAUSE** Scanned wide, reported the top of the list.
**RULE** State the number of comparisons and the corrected threshold in the same sentence as
the result.
**TRIGGER** Any cross-tabulated scan.

### A7 · Marginal test for a conditional claim
**SYMPTOM** A domain claim of the form "X, **in situation Y, for player type Z**" tested as
"does X predict outcomes on average."
**EXAMPLE** The breakout literature claims *high targets-per-route-run **on a limited snap
count** for a **young** player predicts a year-two leap*. It was tested as "does TPRR predict
next-year points." Null, correctly — but that is a different claim. The conditional cell
(elite TPRR + few routes + young) turned out to hold **n=10 with zero breakouts**, so the
honest answer was **underpowered**, not refuted.
**CAUSE** Simplified a three-way interaction into a main effect.
**CAUGHT BY** The user: *"if you are not finding characteristics then you're not looking at
the correct characteristics."*
**RULE** Restate the claim in its exact conditional form before designing the test. If the
cell has fewer than ~30 observations, say so up front.
**TRIGGER** Any hypothesis containing "when," "for," or "if."

### A8 · Floor/ceiling artifact
**SYMPTOM** A variable "predicts" outperformance, but it is confounded with the baseline.
**EXAMPLE** Cross-source ADP disagreement appeared to flag value: "agreed" players beat
their price by −36.4 spots, "most disputed" by +28.3. But **disagreement correlates 0.863
with ADP level** — nobody argues about Ja'Marr Chase. Early-ADP players can only fall; late
ones can only rise. **Controlling for ADP level the sign reverses: −0.244, p=0.0009.**
Disputed players finish *worse*.
**CAUSE** Did not control for the bounded baseline.
**RULE** When the outcome is "beat expectation," always control for the expectation.
**TRIGGER** Any outcome defined as actual-minus-projected or actual-minus-ADP.

### A9 · Mechanical regression to the mean read as signal
**SYMPTOM** A strong negative correlation between prior production and "surprise."
**EXAMPLE** Raw `corr(2024 TPRR, 2025 surprise) = −0.321`; same for targets (−0.305) and
points per game (−0.329). All mechanical: high prior production drives a high projection,
which makes a negative surprise more likely. **Partial correlation controlling for the
projection: −0.077, p=0.237.** Nothing.
**RULE** Report the partial correlation controlling for the projection. The raw one is
uninterpretable and should not appear in a summary.
**TRIGGER** Same as A8.

---

# BUCKET B — DATA PROVENANCE
*These caused the largest wasted effort. Two produced multi-day detours.*

### B1 · Unknown-provenance file used to overturn a finding
**SYMPTOM** A file appears, looks plausible, gets built on.
**EXAMPLE** `top_400_projections_2026.csv` was treated as a second independent projection.
Three findings were written on it, including "the board is fragile to the projection"
(Barkley +25.4, t=7.06 at pick 8, RB-RB-RB falling from 1st to 8th). It was actually an ESPN
pull whose script **never filtered on `seasonId`**, so it captured the **2025** projection
for anyone who had one: Conner 0.0→227, Willis 263→2.8, Dart 343→153, Brooks and Dell at 0.0.
All three findings were withdrawn.
**CAUSE** The directive says to flag incomplete provenance and proceed. The model flagged it
and then built conclusions on it anyway.
**RULE** A source with unknown provenance may **bound** a result. It may never **overturn**
one. Quarantine it until identified.
**TRIGGER** Any file whose origin is not documented in `00_START_HERE.md`.

### B2 · Silent default masking missing data
**SYMPTOM** Missing values become a plausible number instead of an error.
**EXAMPLE** The ESPN puller used `proj_pts = 0.0` as its default. A missing projection and a
genuine zero became indistinguishable, **hiding a whole-file staleness bug for days.**
Rewritten to `None`; the run now prints "missing a 2026 projection: 144 — these are NaN, not
0.0."
**RULE** Default to null and count the nulls out loud. Never default to a value inside the
plausible range.
**TRIGGER** Every parser and every join.

### B3 · Single-source generalisation
**SYMPTOM** A finding from one file stated as a general fact.
**EXAMPLE** "ESPN's ADP is the worst market of seven" — built on **183 players** from the
user's spreadsheet, where ESPN scored 0.078 against the 2025 finish. Replicated on an
independent **521-player** FantasyPros export: **ESPN 0.741, consensus 0.745, NFL 0.744** —
statistically tied, **2nd of 6** in the draftable range, **best of all at RB.** A coverage
artifact in one column. **The draft board's entire framing rested on it.**
**CAUSE** No replication attempted before building on it.
**RULE** Before a finding becomes load-bearing, replicate it on a second source. If none
exists, label it single-source in the ledger.
**TRIGGER** Any finding that changes a recommendation.

### B4 · Undated files
**EXAMPLE** `ESPN_projections_in_my_League.csv` — 200 rows, no capture date, and every
replacement level, tier, VBD and simulation score descended from it.
**RULE** Capture date in the filename and in a column. A file without one is quarantined.

---

# BUCKET C — JOINS AND IDENTITY
*Seven occurrences. The single most repeated mechanical failure in the project.*

### C1 · Joining on name strings
**SYMPTOM** Row counts change, or a nobody appears at the top of a ranking.
**EXAMPLES, all real:**
- Travis Hunter dropped — trailing "CB" in the name
- 405 rows from 357 — "J. Williams" collision
- **37 players dropped** — ESPN glues injury flags to surnames. This skewed WR replacement
  level **10 points low against RB's 2.8**, which is the defect the user's instinct detected
  when he said *"Hard to believe i'd leave myself that weak at the WR position."*
- `Travis Etienne` vs `Travis Etienne Jr.` — a keeper stayed in the draft pool all session
- **Occurrence 7:** first-initial + surname + position merged Javonte, Jameson and Josh
  Williams and produced **Josh Williams (RB, TB) as the league-leading value at VBD −168.5.**
  Adding team to the key cut matches from a phantom 280 to a real **166**.
**CAUSE** Names are not identifiers.
**RULE** Join on `gsis_id` via `code_player_xwalk.csv`. Where an ID is unavailable, the key is
**name + position + team**, never less. Note that name-only keys collide **inside the
canonical crosswalk too** — there is a linebacker named Justin Jefferson and a cornerback
named Lamar Jackson.
**TRIGGER** Every merge. Assert row counts before and after.

### C3 · The probe was wrong, not the object — and it raised a FALSE ALARM
**SYMPTOM** A check reports a defect in a shipped file. The defect is in the check.
**WHY IT IS ITS OWN PATTERN** doc 80 already covers a test that runs on the wrong object and
gives a false **PASS** (§0.2 v5.5: *"build the real object, or you have tested nothing"*). This
is the same root cause with the opposite sign, and the opposite cost: a false **FAIL** makes you
rewrite a file that was correct, four days before it has to work.
**EXAMPLES — all three on 2026-09-04, inside one QC sweep (doc 165):**
1. **Badge audit.** A probe looked for quoted literals of every badge label in `live_draft.py`
   and reported four as "not in the key". Three were tooltip-only strings and one (`12g`) is
   built by `'%dg' % g25` and appears nowhere as a literal. **Fix the probe: import `COLGLOSS`
   and read `badges()`, do not grep for what you assume the source says.**
2. **Opponent filler.** A state generator sorted on `eff_pick + noise` and took the first N,
   which left the board's 3rd-best VBD (McCaffrey) available at pick 8 in **12 of 20 states**
   and reported the engine as unstable there — contradicting §4.2, a CLOSED finding. §5 forbids
   exactly that filler. Rerun to spec: **St. Brown 20/20.**
3. **Bridge guard.** A test called `_bridge_picks()` and concluded the LOST PICKS guard never
   fired. The guard lives one level up in `fetch_picks()`. Rerun against the production path:
   it fires on both the shorter-file and the same-count-different-set cases.
**RULE** When a check contradicts a finding the project has already CLOSED, the prior is that
**the check is wrong**. Before writing it up: name the object production actually builds, prove
the probe touches that object, and re-read the section being contradicted for a rule the probe
may be breaking. Only then report it. **A contradiction of a closed finding is a hypothesis
about your own instrument first.**

---

### C2 · Manifest and directory disagreement not reported
**EXAMPLE** `code_picks_with_adp.csv` appeared in the project manifest but not on disk. The
model reported "this file does not exist" and asked the user to go find it. **He spent time
searching for something that was listed the whole time.**
**RULE** Inventory reads the manifest **and** the directory. Any disagreement between them is
itself the finding and gets reported as such.

---

# BUCKET D — PROCESS AND REUSE

### D1 · A parameter fitted for one purpose reused for another
**SYMPTOM** A calibrated constant moved into a different part of the model.
**EXAMPLE** `USE_BREAKOUT` was fitted against **draft displacement** and then applied inside
the **scorer**, where it stacked a third variance source on top of the CV gamma draw and the
availability pool. Against 412 real league games the simulation's between-team spread was
**14.8 vs 10.1 — 46% too wide.** Turning it off lands at 10.8. **Every effect size produced
before Aug 20 is inflated by roughly that much at team level.** Orderings survive.
**RULE** A parameter validated against one quantity may not be reused for another without
re-validating against the second quantity.
**TRIGGER** Any constant used outside the module that fitted it.

### D2 · Not searching for an existing test before running a new one
**EXAMPLE** See A1. The powered SOS test was already in `claude_10_strength_of_schedule.md`.
**RULE** Before declaring a premise dead, grep the project docs for it.

### D3 · Downstream uses not enumerated when a metric is invalidated
**EXAMPLE** Producing the Aubrey keeper error. When `USE_BREAKOUT` was found wrong, the fix
required listing every consumer — F7, F38, F39, F46, F50, and every point magnitude in the
board doc — not just patching the site where it surfaced.
**RULE** When a finding invalidates a metric, enumerate every downstream use in the same
message.

### D4 · Computing on files that were never saved
**EXAMPLE** `picks_with_adp.csv` and `resid.csv` were computed in a workspace and never
written back. **F49 and F35 were unreproducible for weeks.**
**RULE** Anything a finding depends on is written to `Source` in the same session.

### D5 · Declining to request data
**EXAMPLE** The model told the user a source was not worth supplying **7 times and was wrong
5 of them.** One of those, the historical ADP he insisted was already there, produced F49 —
the TE lag correction that moved Warren at pick 41 from 0.95 to 0.15.
**RULE** Never tell this user a data source is not worth supplying. Ask for it.

---

# BUCKET E — COMMUNICATION
*These do not corrupt the analysis. They waste the user's time and money, which is the same
thing to him.*

### E1 · Reporting before testing
**EXAMPLE** Handed over strength-of-schedule player recommendations — "Jeremiyah Love swings
+7.65 into the playoff weeks, Philadelphia collapses" — with a caveat that it had not been
validated. The user's reply: *"i need you to act on it, not me."* The premise then failed
its test and the recommendations were withdrawn.
**RULE** Test first, then report. A caveat is not a substitute for a test.

### E2 · Jargon as the lead
**EXAMPLE** Opening a paragraph with "F51 — `USE_BREAKOUT` off changes one call at pick 8."
The user: *"i was lost with the first two words."* Worse, the variable name implied the model
had removed breakout-player analysis, when it had removed a random noise multiplier.
**RULE** Plain language first. Finding codes in parentheses, never as the subject.

### E3 · Announcing work instead of doing it
**EXAMPLE** Wrote "starting on steps 1–4 now" and ended the turn. The user had to ask again.
This happened repeatedly; he eventually wrote *"stop stopping"* and *"continue without pause
for the 100th time."*
**RULE** Scoped work starts in the same turn it is named. Report results, not intentions.

### E4 · Implying delivery that did not happen
**EXAMPLE** "Each one goes in both places" for files that were only chat attachments, never
pushed to Drive. **Root cause worth knowing:** the Drive tool takes file contents inline
only — there is no upload-from-disk. Under ~20KB a push is safe; above that a single write
risks truncating mid-file, which is worse than not writing.
**RULE** Mark every file **pushed** or **drag**. Never say "both places."

---

# BUCKET F — INPUT HANDLING
*Process improvements for how user-supplied material is taken in. Not user error — these are
the model's handling gaps.*

### F1 · A named hypothesis narrows the search
When the user names a specific factor, the model has tended to test **only** that factor and
report back. His standing complaint: *"you only use the specific examples I call out."*
**RULE** Test what he named, then name and test two adjacent things he did not.

### F2 · An arriving file needs identification before use
`top_400` (B1) and the 2025 board both arrived without provenance. One produced three
withdrawn findings; the other produced a real one.
**RULE** On arrival: print shape, columns, date range, and cross-check against a known file.
Identify before analysing.

### F3 · Deletion requests need a reproducibility check
The model advised archiving `Boone_Rankings_HalfPPR_2026-08-04.csv` as superseded. Boone
later turned out to be the one ranker with a measured edge. It also advised deleting files
before confirming nothing depended on them.
**RULE** Before advising deletion, list what depends on the file. Prefer labelling STALE over
removing.

### F4 · His instinct has a track record — treat it as evidence
He questioned RB-RB-RB on the grounds it left him weak at WR. A silent bug was later found in
exactly that comparison. He rejected the "monoculture" claim; it turned out to be an
averaging artifact. He said his own draft sheet was worth keeping; it was.
**RULE** When he disagrees, look for the defect before defending the result.

---

### A10 · Aggregate statistic read without inspecting its members
**SYMPTOM** A summary number for a group looks anomalous and is used to overturn a model.
**EXAMPLE** Standard deviation of draft residuals at board ranks 1–12 measured **25.5**, which
looked non-monotone against the higher bands and was used to replace a proportional noise
model with a constant one (F23). That 25.5 was **two observations**: +123 (Kam, TE, 2024) and
+126 (Lobsinger, RB, 2025). Drop those two and the band's sd is **4.89**, on the line; the
other 26 residuals run −3 to +23. The refit gives **sd = 0.1255 × rank + 5.31, r = 0.991,
n = 271** — within 1% of the original `0.135 × ADP` that was discarded. The wrong model then
propagated into every survival probability, the strategy ranking and the pick-8 decision.
**CAUSE** Read a band statistic off a table without printing the rows underneath it.
**CAUGHT BY** The user supplying an unrequested file — FantasyPros Mock Draft Wizard — whose
own dispersion column disagreed. **Not caught by the model.**
**RULE** Before a group statistic overturns anything, print every observation in the group.
**TRIGGER** Any binned or banded summary with fewer than ~50 observations per cell.

### A11 · Population not filtered to the one the effect was measured on
**SYMPTOM** An effect measured on a subgroup gets applied to the whole class.
**EXAMPLE** The tight-end draft lag was fitted at **+16 picks** and applied to every TE in the
simulator. Measured directly on 63 true TE selections: **ADP ≤ 40 → median +14.9 (n=8)** ·
**ADP 61–120 → median −3.7 (n=24)** · **all TEs → median 0.0.** The lag exists only at the top
of the board. Applying it everywhere pushed mid-round TEs 16 picks later than reality:
**Tyler Warren's availability at pick 41 read 0.95 when the corrected value is 0.15**, and
Fannin at 65 read 0.71 against a corrected 0.19.
**CAUSE** Fitted on the population that mattered, then deployed on the population that did not.
This is directive §0's own instruction — *filter to the population that matters* — applied in
reverse.
**CAUGHT BY** Self, but only because the user insisted the historical ADP was already in the
project (see D5) and it was.
**RULE** State the population a coefficient was fitted on in the same line as the coefficient,
and gate its application on that population in code, not in a comment.
**TRIGGER** Any constant applied to a whole position, team or class.

### A12 · Small-n correction overriding a larger-n prior
**SYMPTOM** A new, smaller test contradicts an existing estimate and is adopted immediately.
**EXAMPLE** The elite-TE lag was re-measured at **+4.3 from n=3** and the user was told that
Bowers and Warren were far less available than the board said. Re-fitting properly against four
years of pace at four checkpoints returned **+16**, confirming the original +15. The board's
own numbers had been closer to right than the "correction."
**CAUSE** A newer number was treated as a better number.
**RULE** A correction must beat the prior on sample size or on design, and the write-up must
say which. Three observations correct nothing.
**TRIGGER** Any revision where the new n is smaller than the old n.

### A13 · Estimand not matched to the decision
**SYMPTOM** A paired comparison reports a clean effect for an option that is usually unavailable.
**EXAMPLE** The pick-8 comparison forced each candidate at pick 8 and fell through to the greedy
policy when the player was gone. Puka Nacua reaches pick 8 about **22%** of the time, so
"Nacua at 8" was really *Nacua 22% of the time, greedy otherwise* — and the +12.35 attached to
him came from that 22%. Re-run conditioned on both players actually being available, the table
changes shape: **St. Brown +34.3 (se 15.9, n=200 paired), Allen −18.2 (se 8.7).**
**CAUSE** The treatment was not deliverable in most of the trials being averaged over.
**RULE** In any paired simulation, condition on the treatment being available, and report the
conditioning rate alongside the effect.
**TRIGGER** Any forced-choice comparison where availability is itself stochastic.

### A14 · Convention-dependent count reported without its convention
**SYMPTOM** The same statistic returns different values to different people, and nobody says why.
**EXAMPLE** "TEs taken before round 3" has been reported as **1 of 43**, **2 of 45** and
**3 of 48** by three different passes. All three are arithmetically correct — they differ on
whether the keeper round is subtracted. Keepers occupied round 1 in 2022–23 and round 15 in
2024–25. On raw round numbers Cary's Travis Kelce (2022, **overall pick 30**, raw Rd 3) is
excluded; on the keeper-adjusted round the directive mandates, it is included. **The operational
conclusion flips: "herman allen is the league's only early-TE manager" is false — Cary did it
too, and Cary holds 1.01.**
**CAUSE** A round-based statistic in a league where "round" is ambiguous.
**RULE** Do not count in rounds in this league. Count in overall pick numbers, which are
unambiguous. First TE off the board: **pick 30 (2022) · 20 (2023) · none early (2024) ·
22 (2025).**
**TRIGGER** Any statistic whose unit is a round.

### B5 · Synthetic values generated to fill a gap and left unlabelled
**SYMPTOM** A complete-looking dataset where part of it was invented.
**EXAMPLE** The ESPN export held **200 rows**; the player universe held **494**. The other 294
projections were filled with a linear ramp and carried no flag. The signature is a constant
consecutive difference: **RB step 3.4485 with sd 0.0000** across 15 players, eight of them
clamped to the identical value 28.84; WR step 0.608, TE 1.281, QB 4.260. **39% of the board's
point projections were fabricated for weeks without a marker.** Containment was real but
accidental — every synthetic row sits at ADP ≥ 157.6, and the last flexible pick is 137.
**CAUSE** A gap-filling step with no provenance column.
**CAUGHT BY** Self, on Aug 19, while auditing something else.
**RULE** Any generated value carries a boolean column naming it as generated, in the same file.
Never rank, tier or score on a row without checking that flag.
**TRIGGER** Any time an output has more rows than its source.

### B6 · One source class labelled as the market
**SYMPTOM** "The field says X," where the field is one kind of source.
**EXAMPLE** RJ Harvey was reported as a **48-spot arbitrage** because a four-platform ADP
average put him at **69.8** against ESPN's **118**. The six-expert panel put him at **106.5** —
siding with ESPN, not the platforms. The claim was withdrawn. A later fourth source, the
FantasyPros mock population, said 81.8, which is a *drafting behaviour*, not an evaluation, and
does not restore the claim.
**CAUSE** Averaged one class of source and called the result consensus.
**RULE** Name the sources, never the word "field." Distinguish evaluations (rankers) from
behaviours (ADP, mock drafts) — they answer different questions.
**TRIGGER** Any sentence containing "the market," "the field," or "consensus."

### D6 · A parameter assumed when it was measurable from data already held
**SYMPTOM** A plausible constant is chosen by judgment while the data to measure it sits unused.
**EXAMPLE** In-season streaming value was assumed at **QB 17.8 / RB 7.7 / WR 8.5 / TE 6.8**.
Measured from **951 real adds** in the league's own waiver reports: **QB 15.25 / RB 5.43 /
WR 6.54 / TE 5.53** — over-valued by roughly 25%. The correction flipped a roster-shape
conclusion: the second TE went from **+0.4 to −13.4**, while the second QB survived at **+10.1**.
**CAUSE** No inventory step before choosing a constant.
**RULE** Before assuming a parameter, grep the project for a file that would measure it.
**TRIGGER** Every hand-set constant.

### D7 · Requesting data that is already in the project
**SYMPTOM** A "please supply X" list that the user answers by pointing at the project.
**EXAMPLE** A prioritised six-item fetch list was issued. **Five of the six were already in the
project** — the 400-row projections, PFF receiving for three seasons, PFF rushing, the league
weekly scoreboard, and the 2021 draft results. Separately, historical ADP for 2022–25 was listed
as the **top missing item in three documents** while `picks_with_adp.csv` derivable sources sat
in the project. Using them produced F49.
**CAUSE** The request was written from memory of the conversation rather than from a directory
listing.
**CAUGHT BY** The user, every time.
**RULE** No data request is sent without a fresh, complete inventory in the same turn. Pair with
C2 — read the manifest and the directory, and report disagreements.
**TRIGGER** Any message containing a request for a file.

### E5 · Echoing user text without checking it
**EXAMPLE** The user's message opened "Roman, did we factor strength of schedule?" The model
answered as though addressed correctly. It also once said "each one goes in both places" for
files that only ever went one place (see E4).
**RULE** Read the user's own words as input to be verified, not as ground truth about the model.
**TRIGGER** Any name, filename or claim about prior state that appears first in the user's message.

### E6 · A standing instruction not applied to routine output
**SYMPTOM** A written workflow rule is acknowledged and then not followed for a whole session.
**EXAMPLE** The project's custom instructions say to save updated source files directly to the
Google Drive `Source` folder, archive the outgoing version first, and **"don't produce a zip
file for this unless explicitly asked."** Eight zips were delivered across the session and
nothing was written to Drive until the user asked whether the instruction had been seen.
**CAUSE** The instruction lives in the project prompt; delivery habits are per-message. Nothing
re-checked the former against the latter.
**RULE** Standing output instructions are part of the definition of done for every deliverable,
not a preference to honour when convenient. Re-read them before the first file of a session.
**TRIGGER** The first file produced in any session.

---


---

# ADDED Aug 22, 2026 — found by `code_audit_v1.py`, not by reading

### A15 · An ordinal stored under the name of a cardinal
**SYMPTOM** A column named for a measurement actually holds a rank, and every consumer treats
it as the measurement.
**EXAMPLE** `code_universe.csv` column `ADP`. **Zero of 341** matched rows equal ESPN's real
`espn_adp`; median gap inside the draftable range **7.6 picks**; through the top ~60 players
`ADP` is **exactly the dense rank** of `espn_adp`, drifting deeper (mean gap by band:
−2.2, −6.6, −13.0, −10.4, −3.7, +15.9). Consumers: the §2.1(c) effective-ADP table, the
§4.12 noise term `0.135 × ADP`, every `p_available`, and
`keeper_eligibility_VERIFIED.ESPN_ADP` — which is the column the *"ADP-based keeper prediction
beat projection-based 3-for-3"* finding was measured on. **HANDOFF §9.6's "every manager
drafts ~5 picks ahead of ADP" is almost certainly this artifact, not manager behaviour** — the
mean gap across the relevant range is ≈ −5.
**CAUSE** A rank and a pick number are both small positive integers, so nothing breaks loudly.
**CAUGHT BY** The integrity harness, comparing the column against its own upstream source.
**RULE** Name the unit in the column: `adp_pick`, `adp_rank`, `proj_leaguepts`. A merge that
mixes two units must be unspellable, not merely discouraged.
**TRIGGER** Any column whose name is a measurement but whose values are all integers.

### C3 · A join that drops 100% of a class, silently — occurrence 8
**SYMPTOM** A whole position looks like missing data. It is a failed join.
**EXAMPLE** Open thread #12 read *"D/ST projections are all exactly 50.0 for 29 defenses.
Pick 152 is uninformed."* The projections were never missing. ESPN's pull carries **32 real,
differentiated D/ST projections** spanning **55.4 to 128.4** with
`corr(proj, espn_adp) = −0.823`, and `proj_2025` reconciles against `actual_2025`. The
universe held 29 rows keyed `"Houston Texans"` against ESPN's `"Texans D/ST"`,
`proj_src = v2_carryover`, `TOT` hard-set to **50.0**, `VBD` null, **Falcons, Saints and Colts
absent entirely.** A 73-point spread — about 5.2 a week — was discarded and then written up as
an absence in the source. **Nineteen of forty-four kickers were stale carryover too.**
**CAUSE** Name join across two different naming conventions, with no row-count assertion, and
a constant default that looked like data (compare B2).
**CAUGHT BY** The integrity harness comparing class counts between the source and the spine.
**RULE** Assert the row count of every class before and after every merge and fail on a drop.
A join that returns zero matches for an entire position must raise, never fill.
**TRIGGER** Every merge, and any position whose values are all identical.

### E7 · Correcting a document that already contained the correction
**SYMPTOM** A confident correction issued against a file that had already resolved the point.
**EXAMPLE** The Aug 22 audit told the user that `HANDOFF_v2` §0 had cited the wrong evidence
for Cary as an early-TE manager, on the grounds that overall pick 30 in 2022 is round 3.
**A14 in this file already says not to count in rounds** — keepers occupied round 1 in 2021–23
and round 15 in 2024–25, so on the keeper-adjusted convention the directive mandates, Cary's
Kelce counts and the handoff was right. The audit was correct that the directive's *"1 of 43,
allen only"* is false, and wrong about which document had erred.
**CAUSE** D2, committed against the file that documents D2. `ERROR_PATTERNS.md` was not in the
session when the audit ran.
**CAUGHT BY** The user supplying the file.
**RULE** `ERROR_PATTERNS.md` is loaded before the first analytical claim of a session, not
after. Any statistic whose unit is a round is checked against A14 before it is written down.
**TRIGGER** The first analytical claim in any session.

---

# ADDED Sep 1, 2026 — the draft-tool week

### C4 · Half a filter fixed, the other half never questioned — occurrence 9
**SYMPTOM** A filter is repaired for one class of non-row, and nobody asks what ELSE in the
array is not a row.
**EXAMPLE** Doc 58 established that `draftDetail.picks` carries rows that are not selections —
this league's 12 keepers — and the fix filtered `keeper == True`. **It never asked what else was
in that array.** ESPN pre-creates the ENTIRE pick grid the moment a draft room opens: 180 rows,
one per (round, team), each with a real `overallPickNumber` and an EMPTY `playerId`. The
surviving half of the filter read `if p['pid'] and p['overall']`, and **ESPN's empty-slot
sentinel is a small negative number, which is truthy in Python.** Every unfilled slot passed.
On a mock that had made zero picks the tool read **180 picks**, computed `pick_no = 180`, hit its
`pick_no > 168` branch and rendered **"Draft complete" with an empty roster — instantly, on two
different mock rooms, with identical 179+1 counts.** It would have done exactly that at 8:00 PM
on Sept 7, before pick 1.02. The same defect was live downstream in `fetch_keepers.from_draft()`,
which matched on `keeper` alone and would have returned a keeper with no player in it at the
7:00 PM lock.
**CAUSE** D3 (enumerate every downstream use) applied to one member of a class. And a truthiness
test standing in for a validity test.
**CAUGHT BY** The user, by running the same command against a DIFFERENT mock room and noticing
the counts were identical. Two rooms cannot hold the same completed draft.
**RULE** When you learn that an array contains rows that are not what its name says, enumerate
every kind of non-row before writing the filter — and never test an id for truthiness. `-1`, `0`
and `-16016` are all "truthy or falsy" by accident; only a range test is a validity test.
**NOTE ON THE FIX** `playerId > 0` would have been a second bug inside the first: **all 32
defenses ride the wire as `-16000 - proTeamId`.** The rule is `abs(pid) > 100`.
**TRIGGER** Any filter on an identifier, and any time a defect is found in one member of a class.

### D8 · A test harness kinder than the thing it stands in for
**SYMPTOM** A UAT lane runs green for weeks and catches nothing, because it serves a shape the
real source never produces.
**EXAMPLE** `rehearsal.py` was built (doc 96) specifically to drive the live tool through a
changing draft without ESPN. It served **only picks that had happened.** Real ESPN serves the
whole pre-created grid from the moment the room opens. **So the harness could never have produced
C4, and did not**, across every rehearsal run in the project. The harness now emits the empty
slots; against the fixed tool it reads `0 real picks in`, then 1, then 2. Against the old tool
that same feed says 180 and quits.
**CAUSE** The harness was written from how the draft is *conceived* (picks accumulate) rather
than from a captured real payload.
**CAUGHT BY** The user, via C4.
**RULE** Build a harness from a **captured payload**, not from a mental model of the source.
Directive §0.2 already says a test must exercise the object production builds — that applies to
the fake feed as much as to the DataFrame. **A UAT lane that has never failed is not evidence.**
**TRIGGER** Any harness, mock or fixture that a human wrote by hand.

### E8 · An explanation offered in place of an experiment that was available
**SYMPTOM** A failure cannot be reproduced, so it gets a mechanism instead of a test — repeatedly,
in writing, with confidence.
**EXAMPLE** The mock failure produced **four documents (118–121) in one night**, each proposing a
cause: "ESPN serving a prior season," "the mock room was torn down," "the league does not exist
any more." **None was tested and the last two were unsupported by the timeline the user then
pointed out** — every 404 used as evidence had been collected *after* the mock ended, at the
model's own request. The actual defect (C4) sat in a line the model had itself edited, and the
experiment that found it — **run the same command against a second mock room and compare the
counts** — cost one command and was available from the first hour.
**CAUSE** The gap between "I have a measurement" and "I have an explanation" was filled by
narrative. The tell is always the same: the sentence stops describing an observation
("21985 returns 200") and starts describing a mechanism ("the room was torn down").
**CAUGHT BY** The user, three times in one thread: *"we still don't know what happened, or do
we?"*, *"how do we know the cookies were good for that one off draft room?"*, and by re-running
the mock himself.
**RULE** When you cannot reproduce a failure, **ask for the artifact** — the URL, the raw payload,
one more run under changed conditions — and say plainly that you do not know until you have it.
Never publish a mechanism you have not tested. If a document must be written before the test,
its conclusion is "unknown," not a candidate cause.
**TRIGGER** Any write-up of a failure that the model has not reproduced itself.

### A16 · A flag built without checking that its two ends mean what the user wants
**SYMPTOM** A derived label is shipped with its polarity assumed rather than tested, and it flags
the opposite of what the user is looking for.
**EXAMPLE** The RB backfield flag was emitted as `COMMITTEE (gap < 50) / contested / clear job`,
with COMMITTEE meaning *avoid*. The user's actual rule is that he **targets** unsettled
backfields. When the second axis he implied — how much the backfield is worth — was finally
measured, it **does not exist**: the team RB "pie" is nearly constant, **IQR 317–355 projected
points, ±6% across 32 teams.** What the RB1−RB2 gap actually measures is **ESPN's uncertainty
about who wins the job**, which is his target, not his avoid. The flag was telling him to skip
his own archetype. Re-emitted as `UNSETTLED / contested / LEAD BACK`. Separately it was computed
from the keeper-depleted board, which had deleted Dallas's, New York's and New England's lead
backs and made those gaps fiction.
**CAUSE** A label was named from an intuition about what a small gap means, and the intuition was
never tested against either the data or the user's stated rule.
**CAUGHT BY** The user: *"I think those players could still hold significant value."*
**RULE** Before shipping a derived label, state in one sentence what each end of it means and
what a user should DO at each end — then test that the data supports the split. A three-bucket
flag whose middle bucket holds most of the population is describing noise.
**TRIGGER** Any new categorical column with a value that reads as advice.

---

### A17 · A summary statistic chosen without asking what contaminates it
**SYMPTOM** The arithmetic is right and the quantity is the wrong one, so a published number is
off by a factor while the conclusion it supports happens to survive.
**EXAMPLE** Doc 129 published *"NFL defences barely persist — r = +0.113 season to season"* and
used it to close down a mechanism. The measure was **season-TOTAL EPA allowed** over **three**
transitions. A season total is contaminated by pace and by how many plays a team faced. On
**per-play rates over 2020–2025, n=160**, the answer is **r = +0.204** (TDs allowed +0.271;
offence, for contrast, +0.382). **Wrong by nearly 2×.** The conclusion held only because the
chain behind it — mechanism R²=0.041, pass rate 7.5% of target variance, +2 points with perfect
foresight — was weak at every link.
**CAUSE** A rate question was answered with a total. No one asked what else moves the numerator.
**CAUGHT BY** The user: *"We can't predict strong defenses is what you indicated earlier?"*
**RULE** Before publishing a correlation, name the denominator the quantity should have had and
say why the one you used is not contaminated by it — pace, plays, games, opportunity.
**TRIGGER** Any r or persistence figure computed on a season total rather than a per-play,
per-game or per-opportunity rate.

---

### A18 · Conditioning on an outcome-correlated filter and reading the result as a bias
**SYMPTOM** A filter that sounds neutral ("players who stayed healthy") also selects for success,
and the resulting gap gets attributed to the thing being measured.
**EXAMPLE** Doc 131 first measured ESPN as **under-projecting rushing yards by 20.7%** among
players with 15+ games — a number that, if real, would have tilted the whole RB-vs-WR board. But
a bust loses snaps and drops below the cutoff, so the filter selects on outcome. The same split
gives a ratio of **1.13 at 15+ games and 0.63 under 15, at BOTH positions.** The 20% was the
selection, not the projection. Measured with no games filter, the RB−WR gap is **+5.8pp with a
bootstrap CI of [−0.035, +0.150]** — not resolved, and not shipped.
**CAUSE** "Strip out injuries" was treated as a nuisance control when playing time is itself an
outcome of performance.
**CAUGHT BY** Self, on the second pass — the 1.13-vs-0.63 split at both positions was the tell.
**RULE** Never filter on games played, snaps, or any usage variable and then interpret the
residual as a property of the projection. If availability must be removed, model it; do not
subset on it.
**TRIGGER** Any population defined by a minimum of games, snaps, targets or carries in the SAME
season as the outcome being measured.

---

### C5 · Attribute access on a DataFrame column whose name collides with the pandas API
**SYMPTOM** `df.<col>` silently returns a bound method or an indexer instead of the column, and
the failure surfaces as a type error far from the cause — or, worse, does not surface at all.
**EXAMPLE** Twice in one session: `s.div` returned `DataFrame.div` (the division method) rather
than a column named `div`, and `d.at` returned the `.at` indexer rather than a column named `at`.
Both raised, but only because the next operation happened to be arithmetic. Renamed to `cheap`
and `patt`/`pcar`.
**CAUSE** Convenience attribute access used for a column name that is also a pandas attribute.
**CAUGHT BY** Self, via the traceback.
**RULE** Use `df['col']` for any column, and never name a column `div`, `at`, `all`, `any`, `min`,
`max`, `sum`, `size`, `shape`, `index`, `pop`, `T`, `count` or `mean`.
**TRIGGER** Writing a column name that is a short common English word.

---

### B7 · A retrieved source used without reading its publication date

**SYMPTOM** A web article is fetched, its content is plausible and on-topic, and it is used as
current status without anyone establishing WHEN it was published. Fantasy injury and depth-chart
headlines are nearly year-agnostic in their wording, and search engines rank by relevance, not
recency — so a 2024 article about the same player's same body part sorts to the top and reads as
today's news.

**EXAMPLE** Sept 5, 2026, in one day, across three independent pipelines — my own fetches, three
verification subagents, and a note already shipped on a player card:
- CBS, *"NFL Week 1 injury report: Ja'Marr Chase limited in return to practice"* — **Sept 4, 2024**.
- SI, *"Eagles Wednesday practice report: DeVonta Smith absent again"* — **Nov 26, 2025**, and
  about a shoulder, not the hamstring.
- **The one that shipped:** J.K. Dobbins' card carried `NEWS 09-03: ... could force him onto
  Injured Reserve.` ESPN has an article with that headline. It is dated **Nov 15, 2025** and
  describes a foot injury from a hip-drop tackle the previous season. Denver never placed him on
  IR in 2026; Sean Payton on Sept 2 said he was *"moving well."* The player was graded **AVOID**
  on that basis, and `live_draft.py:875` silences a player's analyst up-calls when the grade is
  AVOID — so the stale article did not merely mislead, it **suppressed the evidence that would
  have corrected it.**
- SI on Khalil Shakir, *"head coach shares good news on Shakir timeline"* — **Aug 7, 2025**;
  identifiable only because it referenced a Week 1 opener against Baltimore, which was the 2025
  schedule.
- A Wan'Dale Robinson ankle piece dated **"November 27"** with no year, whose content was his
  Giants era.
- A Draft Sharks page whose extracted date came back **Aug 15, 2022** on content discussing
  2026 facts — a bad date, which is its own failure mode and must also mean "do not use."
Nine instances in a single day.

**CAUSE** The relevance signal and the recency signal are independent, and only one of them is
what the reader wants. Nothing in the text of a fantasy injury article says which season it is
about; the tell is usually an opponent, a coach's name, or a schedule detail, none of which the
reader is looking at.

**CAUGHT BY** self, after two near-misses in the same hour; then by an explicit instruction to
three subagents, which caught six more.

**RULE** **State a retrieved source's publication date before using it. If the date cannot be
established, or the date that comes back is implausible for the content, do not use the source —
find another.**

**TRIGGER** Any WebFetch or WebSearch result used as a claim about the present. Put the demand
for the date in the fetch prompt itself, not in the reader's head — the model answering the fetch
will supply the date if asked and will not volunteer it if not.

### A19 · Repeating a run instead of varying the input, and reading the stability as strength

**SYMPTOM** A number is produced N times, comes back nearly identical every time, and the low
spread is reported as confidence in the ESTIMATE. But the N repetitions varied only the estimator's
internal randomness, not the real-world thing that actually differs between one occasion and the
next. What was measured is the estimator's self-consistency; what was reported is the size of an
effect.

**EXAMPLE** Doc 139 ran the shipped rollout at pick 8 **ten times, under ten seeds and three
Monte-Carlo sample sizes**, and got a margin of **19.96 → 20.20** every time. That tightness is
what made it quotable, and "about 20 points" entered §4.2, the maxims card and Matt's memory.
**All ten runs used the SAME board** — the same seven players already gone. The seeds shuffled the
engine's dice, not the draft. Re-run on a modal board state (doc 182) the margin is **7.8**, and the
board's own arithmetic — St. Brown +101.33 against Derrick Henry +95.38 — says **5.9**. The pick
never changed; the size was wrong by 2.5×.

**The project had already solved this and did not apply it backwards.** Doc 140 caught the identical
error at pick 32 — a "0.15-point converging margin" from one board state became a **median 3.65
across 100 states** — and v6.7 wrote the correction into §7. Pick 8 was never re-checked, because
its number *looked* more robust, not less: ten identical answers reads as stronger evidence than one
answer, and it is the same evidence.

**CAUSE** Two different quantities share the word "variance": the estimator's noise, and the
world's. Repeating a run collapses the first and says nothing about the second. A tight spread
across seeds is therefore evidence the CODE is deterministic enough, and no evidence at all about
the DECISION.

**CAUGHT BY** user challenge — Matt raised an unrelated bear case on the player, which forced the
engine to be run at that pick on a fresh board.

**RULE** **Before quoting a margin, name the thing that varies in reality and vary THAT.** Seeds,
sample sizes and repeat runs are a code check, never a measurement. If the real-world variation
cannot be generated, say the number rests on one realisation — and if a generator produces
identical output across states, that is a broken generator, not a stable answer (doc 182's own
30-state attempt failed exactly this way and was reported as failed).

**TRIGGER** Any sentence of the form "N out of N times" or "the margin was X every time." Ask
immediately: N times over what? If the answer is seeds, it is A19.

# APPEND TEMPLATE — use this exact shape for new entries

```
### [BUCKET][n] · [short name]
**SYMPTOM**
**EXAMPLE**   real numbers, named files, actual magnitudes
**CAUSE**
**CAUGHT BY** self · user challenge · replication · integrity harness
**RULE**      imperative, one sentence
**TRIGGER**   the condition that should fire the check
```

**Transcription complete as of Aug 21, 2026.** The pre-Aug-20 backlog — F23's band statistic,
the unconditioned pick-8 comparison, the 39% fabricated projections, the +4.3 TE lag from n=3,
the assumed streaming values, the "field" mislabel, and the "Roman" echo — is now carried as
**A10, A13, B5, A12, D6, B6, E5**. Two patterns were found during transcription that were not
on the backlog list and are new: **A11** (population mismatch) and **A14** (convention-dependent
counts). **E6** covers a standing instruction ignored for a full session.

**Aug 22 status of the D/ST and ADP defects.** Both are fixed in
`code_universe_v5.csv`, rebuilt by `code_rebuild_spine_v5.py` on the dated ESPN pull with
`adp_pick` / `adp_rank` split, D/ST and K rejoined on `espn_id`, `injury_status` surfaced, and
row counts asserted at every step. The old `code_universe.csv` is **STALE, not deleted** (F3).

**One consequence of B1 that must not be lost.** `top_400_projections_2026.csv` is a bad file —
an ESPN pull that never filtered on `seasonId`, so it carries 2025 projections for anyone who
had one. **`RESTART_PROMPT.md` step 3 instructs the next session to rebuild the projection spine
on that file.** That step is void. Corrected there on Aug 21; if you are reading an older copy
of the restart prompt, ignore its step 3.
