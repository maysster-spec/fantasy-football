# 220 — The draft, graded: second of twelve, and the one instrument we never loaded

**2026-09-07, post-draft.** Matt: *"hate my bench since i didn't get what i'd consider the players
with 'upside' potential to really take over later in the season"* and, minutes later, the real
diagnosis: *"i never used that csv file to provide you the tags for my personal favorites. part of
the problem i realized is that they are far down and wont show on the live draft board."*

**He is right about the cause. He is wrong about the draft.**

---

## 0. ACTIONABLE

1. **This roster finished 2nd of 12 in value — +121.4, behind only the defending champion's
   +128.5.** Third place is 10 points back.
2. **On six of his first seven picks he took the literal best player on the board.** Gap: 0.0.
3. **`my_takes.csv` was EMPTY all night and the console said so at every launch** —
   `0 of YOUR takes`. I read that line at least four times today and never once said anything.
   **That is mine, not his.**
4. **Week 11 is a three-starter hole** — Nacua, Judkins and Adams all off. Plan waivers around it.
5. **He got Mike Washington Jr. AND Jeanty.** That is the strongest possible form of the bet he
   said his gut wanted.

---

## 1. THE DRAFT ITSELF

| pick | took | pos | VOR | best on the board was | gap |
|---|---|---|---|---|---|
| 8 | **Puka Nacua** | WR | **+131.3** | Puka Nacua | **0.0** |
| 17 | Ashton Jeanty | RB | +79.6 | Ashton Jeanty | **0.0** |
| 32 | Quinshon Judkins | RB | +41.8 | Quinshon Judkins | **0.0** |
| 41 | Davante Adams | WR | +35.0 | Davante Adams | **0.0** |
| 56 | Jalen Hurts | QB | +25.3 | Jalen Hurts | **0.0** |
| 65 | Sam LaPorta | TE | +9.1 | Matthew Stafford | 12.1 |
| 80 | Rico Dowdle | RB | +2.8 | Rico Dowdle | **0.0** |
| 89 | J.K. Dobbins | RB | −4.3 | Patrick Mahomes | 6.5 |
| 104 | Tyjae Spears | RB | −38.9 | Dallas Goedert | 40.4 |
| 113 | Xavier Worthy | WR | −18.0 | Dallas Goedert | 19.4 |
| 128 | Mike Washington Jr. | RB | −107.6 | Dallas Goedert | 109.1 |
| 137 | Tyler Shough | QB | −34.8 | Jake Ferguson | 24.5 |

**PICK 8 IS THE STORY OF THE WHOLE PROJECT.** Doc 200 exists because Matt read the DRAFT BOARD GRID
for the first time and asked why his pick-8 cell said Nacua — which exposed that every published
pick-8 run had removed Nacua, McCaffrey and Taylor *by construction*. The rule was rewritten two
days ago to **"take the highest-VOR player on the board."** Nacua fell to 8. He took him. **That
single question was worth about 30 points over the alternative the old rule would have produced.**

**AND THE LATE "GAPS" ARE MOSTLY AN ARTIFACT — state it plainly (§0.2).** At 104, 113 and 128 the
board's "best available" was **Dallas Goedert, a second tight end**, which §6's cap forbids and
which he would never have started behind LaPorta. **A raw VOR gap ignores roster caps; the engine's
own `cost vs #1` does not.** The honest read of rounds 9–12 is that the board had nothing left it
wanted him to have.

**DOCTRINE COMPLIANCE — PERFECT, and this is not nothing given what autodraft did to him in the
afternoon mock:** QB 2 · TE 1 · **RB 6, exactly the cap**. §4.19's "bench RB to the cap, then WR",
executed. §6's "never three QBs, never three TEs", honoured. And Derrick Henry never appeared.

## 2. THE BENCH HE HATES

Dobbins · Worthy · Spears · Mike Washington Jr. · Shough. **Four of his picks sit inside ADP
121–180**, the only band where §4.13 found breakouts live (17.0% against 2.1–6.2% at 25–84).

- **Mike Washington Jr. is the bet he told me his gut wanted**, and he got the good version of it:
  **he owns Jeanty.** Doc 217 §3 laid out the two cases — with Jeanty, Washington is insurance on a
  first-round back with a live ankle on a **247-point job**; without him he is a lottery ticket on a
  stranger. He has the first one.
- **Dobbins** is Denver's lead back at **205 projected carries** in a backfield `depth_map` flags
  **UNSETTLED**. Not a dart — a starter-shaped hold.
- Spears and Worthy are ordinary late shots, which is what late shots are.

**THE UNCOMFORTABLE PART, AND IT IS NOT ABOUT HIM: §4.13b measured that in this band only 20.5% of
players ever become startable at all.** Four of five do not. **A bench that feels short on
league-winners is what every bench in this league looks like**, and the disappointment is a correct
reading of the position, not of his drafting. §4.13 also measured that season luck is **6× draft
luck**, and that corrected for sampling error the spread in title odds between a good draft and an
ordinary one is **zero**.

## 3. THE INSTRUMENT WE NEVER LOADED — AND I OWN THIS

Matt: *"i never used that csv file to provide you the tags for my personal favorites."*

**`my_takes.csv` and `my_take.py` exist for exactly this. The file was empty.** And
`load_context()` printed it on **every single launch**, all day:

```
context: 265 players loaded (6 AVOID, 36 BUY, 66 with analyst calls, 122 darts, 0 of YOUR takes)
```

**`0 of YOUR takes`.** I read that line in my own test output at least four times today — in the
D/ST fix, in the watch-strip tests, in the replay of his mock — and never once said "your own
tags are empty, do you want to fill them?" **That is a §0.5(c)5 missing-row failure of the plainest
kind: a field that should have had rows, had none, the tool announced it, and nobody looked.**

**And his second observation is the sharper one.** Even tagged, his favourites sit far down the
board and **the live board only ever shows twelve rows**. A tag on row 90 is invisible at pick 104.

**The fix already exists and I aimed it at the wrong list.** At 17:00 I built the
**"Still on the board?"** strip precisely because he could not tell whether Luther Burden was gone
— and then I populated it with **thirty names of my choosing** off the board's value order. *That
was the moment to ask him for his list and I did not.* Had the strip carried his favourites, this
entire complaint would not exist.

**POST-DRAFT, FIRST ITEM:** `WATCH` becomes a read of `my_takes.csv`, not a hard-coded list, and
`check_kit` or the launch banner **fails loudly when that file is empty** rather than printing a
zero nobody reads.

## 4. THE ONE REAL ROSTER PROBLEM

**Week 11: Nacua, Judkins and Adams are all off.** Three of his top four. §4.11 measured a bye
*collision* at ≤1.2 points, but that was pairs — this is three starters in one week and the finding
does not stretch to cover it. **Plan the week-9 and week-10 waiver runs around week 11**, and note
his own record says QB adds hit for him at 35.7% (best in the league) while four of five RB adds
never produce a startable stretch (§4.19).

## 5. OPEN

- `WATCH` from `my_takes.csv`, plus a loud failure on an empty takes file — **top of the list**.
- The D/ST page had a bug he reported at pick 152 and did not describe; pull the log.
- `board_audit.py` carries four stale assertions (480 rows, 12-keepers-in-spine, the ADP vintage
  string, prerank composition) that all fired tonight as false alarms because two keepers were a K
  and a D/ST. Fix before next September.
- `make_prerank.py` belongs in `sept5_after.bat`, and §0.5(d)'s trigger table should name the
  prerank as a downstream artifact of any board rewrite.
- Everything on docs 216 §4, 217 §4, 218 §5 and 219 §5 still stands.
