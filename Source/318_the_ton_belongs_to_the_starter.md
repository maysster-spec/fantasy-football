# 318 — THE TON BELONGS TO McCAFFREY, NOT TO THE SEAT BEHIND HIM

*2026-09-16. Matt: "I'm still confused about the potential to get a lead back worth a ton with*
*Black (depends on CMC injury), over a 2nd string WR on a less productive offense that appears to*
*be sputtering."*

**He is asking the one question the page cannot answer, and he is right that it cannot: the seat
model prices EVERY backfield at one relief rate and has no opinion about San Francisco.**

---

## 0. WHAT TO DO

1. **Nothing to run.** This settles a question, it does not change a file.
2. **The answer is Washington, and not by a little: +3.7 against +1.1.**
3. **The reason is not that Black is bad. It is that your backfield is your deepest room.** At the
   measured relief rate he is **+0.78 a week over your own bar**; Washington on a hit is **+1.36**.
4. **THE NUMBER TO HAVE AN OPINION ABOUT IS 14.0.** That is what Black must average in relief to
   draw level with Washington. The measured rate for a relief back is **12.13**.
5. **A retraction inside this doc: my first run said Matt was right, at r=+0.32, p=0.008. It was
   the wrong predictor.** On the right one the effect is null. Both are below.

---

## 1. THE TESTABLE FORM, AND I GOT THE OBJECT WRONG ON THE FIRST PASS (§0.5a2)

His claim: a lead back **worth a ton** makes the seat behind him worth more.

> **POPULATION:** every team-season 2021–2025 where the weeks-1–4 RB usage leader missed a game in
> weeks 5–14 and the next back by weeks-1–4 usage had a line in those weeks. **n=71.**
> **OUTCOME:** the replacement's half-PPR per game in the weeks the leader was out.
> **DIRECTION:** a bigger job pays the replacement more, so 12.13 understates Kaelon Black.

**FIRST RUN, PREDICTOR = THE WHOLE BACKFIELD'S SEASON POINTS. It confirmed him.**

| backfield size | n | replacement scored |
|---|---|---|
| 238–283 | 17 | 10.06 |
| 284–318 | 17 | 8.99 |
| 318–351 | 17 | 13.73 |
| **351–459** | **20** | **14.90** |

**r = +0.316, permutation p = 0.0076.** Top decile 16.46 a game. `[TESTED]`

**AND IT IS THE WRONG OBJECT.** The page's `job worth` is **the lead back's own projection**
(§4.20), not the backfield's total. McCaffrey's 302.4 is one man. I had compared his one-man
number against a whole-room number and would have shipped it.

**SECOND RUN, PREDICTOR = THE LEAD BACK'S OWN PACE, which is what 302.4 measures:**

| the lead back's own season pace | n | his backup scored in relief |
|---|---|---|
| 56–148 | 17 | 10.33 |
| 148–189 | 17 | 13.80 |
| 189–230 | 17 | 13.23 |
| **232–392** | **20** | **11.02** |

**r = −0.069, permutation p = 0.573. NULL, non-monotone, and the top band is the SECOND WORST.**
`[TESTED, n=71]`

**McCAFFREY'S OWN BAND — lead back 270 to 340, where his 302.4 sits — is four events and they
averaged 8.51 a game, BELOW the 12.13 the page already uses:**

| | lead back | his backup in relief |
|---|---|---|
| 2022 CAR | Christian McCaffrey, 288 | D'Onta Foreman **13.0** over 7 weeks |
| 2024 HOU | Joe Mixon, 270 | Cam Akers 11.7 over 1 |
| 2024 IND | Jonathan Taylor, 286 | Trey Sermon 7.9 over 3 |
| 2021 NO | Alvin Kamara, 276 | Tony Jones 1.5 over 2 |

n=4, so this band is a sighting and not a finding. The n=71 null is the finding.

**THE MECHANISM, and it is why the two runs disagree.** What flows to a backup is **how much
running-back work the offence spreads around**, not how good the man in front is. A great lead
back is often a sign of a backfield built around ONE man, which is the opposite of what a
replacement wants. **And §4.20 already closed the other door: the team RB pie varies only ±6%
across 32 teams, IQR 317–355.** So even on the predictor that does work, there is no room for San
Francisco to be special. **12.13 is the right number for Black.**

---

## 2. THE HALF THAT IS ABOUT MATT'S ROSTER, NOT ABOUT BLACK

Priced against the lineup he will have after the two claims he is keeping (Schultz in, Washington
in, Hockenson and Shough out):

| | rate if the tail lands | **over HIS bar** | weeks | odds | expected |
|---|---|---|---|---|---|
| **Kaelon Black** | 12.13 | **+0.78 a week** | 3.02 | 46% | **+1.1** |
| **Malik Washington** | 12.71 | **+1.36 a week** | 6.4 | 42% | **+3.7** |

**The odds are nearly the same. The gap is the bar and the duration.**

- **RB:** Jeanty 14.5 · Judkins 12.4 · Dowdle 10.2 · Dobbins 9.7. A 12.1 back is his **RB3**.
- **WR:** Nacua 17.2 · Pickens 11.7 · Adams 11.7 · Worthy 8.5. A 12.7 receiver is his **WR2**.

Doc 259 in one line: *the wire cannot upgrade a working slot, it can only fill a broken one.*
Matt's backfield is the least broken thing he owns.

**THE SENSITIVITY, which is the honest way to leave it with him:**

| if Black actually plays at | he is worth |
|---|---|
| 12.1, the measured relief rate | +1.1 |
| **14.0** | **+3.7 — level with Washington** |
| 17.8, the ENTIRE San Francisco job | +9.0 |

**So his case is not absurd, it is a bet that Black is two points a game better than the average
relief back.** Week 1 is the evidence for it: 14 carries to McCaffrey's 10, all 28 of the backup
snaps, Jordan James a healthy inactive. The evidence against is that n=71 says the job's size does
not carry that, and n=4 in McCaffrey's own band says 8.51.

---

## 3. WHAT THE MODEL STILL CANNOT SEE, NAMED (§0.5a4)

- **p_opens is 46% for every seat on the board.** The constants file says so itself and flags the
  null behind it as UNDER RE-CHECK (catalog B4, ledger row 2): doc 276's population held only backs
  healthy through week 4, so "it does not vary by history" may be a selection artefact. McCaffrey
  is 30, carries a live questionable tag, and played all 17 last season. **Our number cannot tell
  him from anybody.** It does not change the verdict — at 12.13 Black needs p above 100% to catch
  Washington — but it is the input most likely to be wrong.
- **The relief rate is one constant for every backfield.** Section 1 is the test of whether it
  should vary and the answer on the lead man's worth is no. **Whether it should vary with the
  BACKFIELD pie is a live question** (r=+0.316 above), and §4.20 says the pie barely varies, so the
  expected gain from building it is small. **NOT YET RUN**, deliberately, and this is why.

---

## 4. UNRELATED, AND IT IS A RETRACTION OF MY OWN INSTRUCTION

Matt: *"what is the reasoning again to ask Gemini Notebook to only process 5 files at a time. What
was the risk and can you back up that claim?"*

**`GEMINI_HITRATE_PROMPTS.md` line 71 reads "Extract, three to five ticked sources at a time." There
is no reason given, in that file or in any other, and there is no measurement behind it. I cannot
back it up.** It is an unsourced instruction of exactly the class §0.2 forbids, and it has been
sitting in a procedure he runs.

**What I can say honestly, separated by what it rests on:**
- **Mechanical, and real:** a long CSV can be truncated by an output limit, and a bad batch of five
  costs five re-runs rather than fifty. Neither was measured here.
- **Adjacent evidence, not a measurement of batch size:** the first corpus run was asked for
  "every waiver episode across five seasons" and **stopped at 29 links against a 5x14 grid.** That
  is a model under-delivering on a large open-ended ask, which is why the prompt now demands a grid
  with MISSING written into every hole. It says nothing about five versus fifteen.
- **A hunch with nothing behind it:** that attention dilutes across many transcripts.

**THE FALSIFIER, and it costs one evening: run one batch of 5 and one of 15 in the same notebook
with the same prompt, and compare rows returned PER SOURCE and the share of rows carrying a real
citation.** Until that is run the instruction stays in the file marked as a guess, not a finding.
