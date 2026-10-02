# 275 — The seat, not the man

2026-09-10, week 1. Matt: *"ESPN does [not] update as quick as 3rd party sites such as sleeper and
others. plus there is twitter and specific people to follow for live updates. I don't think this
makes a difference when waivers are mostly FA"* — then, naming the exception himself: *"the back
up player who may become the starter."*

Three things came out of that. His conclusion holds; the mechanism he gave for it is backwards.
The list he asked for is built and shipped. And building it found a live defect in `depth_map.csv`
that had a fullback holding the running back's job on twelve of thirty-two teams.

---

## 1. The lane split is 50/50, not "mostly FA" — and that inverts where speed pays

Population: every executed add in this league 2022–2025 that carries a timestamp, n=1,230. Nothing
excluded — D/ST is in it this time (§0.6, doc 228's lesson).

| lane | n | share |
|---|---|---|
| free agency | 616 | 50.1% |
| waivers | 614 | 49.9% |

By season: FA 56% / 50% / 49% / 46%. Weeks 5–18 only: still 50.0%. So the premise "waivers are
mostly FA" is not what the file says. `[TESTED, n=1230]`

**But the correction does not change his answer, and the reason is worth writing down.** The two
lanes fire at completely different times:

| lane | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|---|---|---|---|---|---|---|---|
| waivers | 0% | 0% | 0% | **86%** | 2% | 7% | 4% |
| free agency | 2% | 0% | 0% | **48%** | 14% | 16% | 20% |

A waiver claim is a sealed-bid auction settled Thursday morning at 3–5am on priority order.
**Being first to the news is worth exactly nothing there** — the claim you file Tuesday afternoon
and the one you file Wednesday at midnight are settled identically. That is half the lane.

The other half is a footrace, and that is precisely where a Twitter alert would convert. So the
honest form of his sentence is the reverse of the one he said: **speed is worthless on the waiver
half and decisive on the FA half.** His conclusion survives anyway, because of this:

- Only **36 of 616** free-agency adds in four seasons landed inside a live game window — **5.8%**.
- For waiver claims the same window is **0.0%**.
- **Matt himself: 41 executed adds, 12 free agency, 29 waivers, and zero in a live game window.**
  The field is at 1.5%.

**Nobody in this room runs the race.** The FA adds cluster across the business day — 6am to 6pm,
fairly flat — which is the shape of people checking their phone between other things, not of people
reacting to an alert. So the live-news edge here is **unclaimed rather than worthless**, and that
is a different sentence from the one either of us started with.

---

## 2. Where it converts: a backup who has never been rostered

Matt's own exception is the right one and it is the only clean case. A player nobody owns has never
been through waivers, so claiming him is pure first-come-first-served. When the starter's news
breaks, the seat behind him is the one asset in this league where minutes matter.

**`Source\inherit_2026.csv` is now that list**, built by `Scripts\research\build_inherit.py`.
Eight seats are both at risk and still claimable, ordered by what the job pays:

| | team | the job at risk | pays | why | be first to | owned |
|---|---|---|---|---|---|---|
| 1 | SF | Christian McCaffrey | 302 | listed questionable | Jordan James | 2.2% |
| 2 | MIA | De'Von Achane | 261 | missed 1 game in 2025 | Ollie Gordon II | 1.6% |
| 3 | PHI | Saquon Barkley | 252 | missed 1 game in 2025 | Tank Bigsby | 19.8% |
| 4 | DAL | Javonte Williams | 241 | missed 1 game in 2025 | Jaydon Blue | 0.7% |
| 5 | LAC | Omarion Hampton | 236 | missed 8 games in 2025 | Keaton Mitchell | 22.5% |
| 6 | CLE | Quinshon Judkins | 211 | missed 3 games in 2025 | Dylan Sampson | 19.9% |
| 7 | NYG | Cam Skattebo | 205 | missed 9 games in 2025 | Tyrone Tracy Jr. | 6.1% |
| 8 | GB | Josh Jacobs | 153 | missed 2 games in 2025 | Chris Brooks | 10.3% |

**The rest of the league's handcuffs are already gone.** Kamara, Blake Corum, TreVeyon Henderson,
Rico Dowdle, RJ Harvey, Jordan Mason, Rachaad White, Kenny Gainwell, Kyle Monangai, Braelon Allen
and Jonathon Brooks all sit on somebody's bench. There is nothing to be fast about on those.

**Provenance gap, flagged (§1):** the injury tag comes from the 07 Sept projection pull, which is
three days old and pre-dates week 1. Only McCaffrey's row rests on it; the other seven are driven
by 2025 games missed, which does not go stale.

---

## 3. Gate 2 was measured forward for the first time, and it is null

§4.27 gave the list two gates. Gate 1 is fragility — the man ahead missed a game or carries a flag.
Gate 2 was the backup's best consecutive two-week half-PPR stretch, bar 11.2.

Before shipping, the testable form (§0.5 a2): *among direct RB backups whose starter later missed a
week, does a prior-season best-two-week of 11.2 or better predict better production in the weeks the
starter is out?*

**Population: NFL team-seasons 2022–2025. The weeks-1–4 usage leader at RB is the starter, the
second man is the direct backup, and the event is any later week the starter has no line and the
backup does. n=62 events, 39 with a prior-season line. Outcome: the backup's half-PPR per game in
those weeks.**

| candidate sort key | rho | p | n |
|---|---|---|---|
| his best two weeks the season before | **+0.006** | 0.97 | 39 |
| his own weeks 1–4 rate this season | +0.094 | 0.46 | 62 |
| his share of the backfield, weeks 1–4 | +0.184 | 0.15 | 62 |
| what the starter he backs up scores | −0.056 | 0.66 | 62 |

`[TESTED, null]` The above/below split at 11.2 is +2.91 points a game (p=0.14), and a bar sweep
shows why that is not a finding: at 8 it is +3.17, at 15 it is −0.05, at 20 it is −2.85. The gap
lives entirely at the bottom — it separates *has played NFL football* from *has not* — and it does
not scale. Thirty of the thirty-nine backups with any prior line clear 11.2, so as a screen it
passes 77% of the population. That is not a gate.

**What went wrong, and it is my error, not the gate's.** Doc 244 measured Gate 2 *retrospectively*:
a back who produced during the absence kept a fifth of the job afterwards. That result stands. Doc
251 then put the same number into a wire list, where it silently became a *forward* claim — that a
man who produced last year will produce in relief next year. Same object-versus-question failure as
§0.5(a2), one step removed, and it took a falsifier to see it.

**So the list sorts by the job and never by the backup.** The two-week number survives as a label
in the `floor` column and carries no ranking weight. This is §4.20 arriving from a third direction:
**buy the job, never the name.** The corollary Matt can act on is that the list does not need the
news to be built — the seats are knowable now, and Thursday's speed is only about being first to a
name already on the paper.

**Not yet run, input named:** whether a backup's *snap or route share* in the two weeks before the
absence predicts his relief scoring. Weekly snap counts are an nflverse release this project has
pulled once (doc 133) and does not keep. That is the one candidate the four above do not cover.

---

## 4. The defect: a fullback held the job on twelve teams

`depth_map.csv` is what `wire.py` reads for "the man ahead" and for the whole next-man-up lane.
Checked against the published depth chart, its top two agreed on only **18 of 32** backfields.

The cause is one entry in one dictionary. `POS_OF` maps `'FB': 'RB'`, and the scraped chart gives
every team a separate FB row whose Player 1 is slot 1 — so after `sort_values('slot')` the fullback
kept slot 1 and outranked the actual starter:

> SF Kyle Juszczyk · DAL Hunter Luepke · LAC Alec Ingold · DEN Adam Prentice · LV Connor Heyward ·
> CLE Michael Burton · MIN Max Bredeson · NYJ Andrew Beck · PIT Riley Nowakowski · NE Reggie
> Gilliam · NYG Patrick Ricard · HOU British Brooks — **all at depth 1.**

On NE, NYG and DAL that meant `in_doubt()` was reading a fullback as the starter whose job is at
risk, and on SF the man listed as next in line was Kaelon Black, the third back, because Juszczyk
had taken the second slot.

**Fixed with `FB_OFFSET = 10`** — the FB chain is pushed below every real back rather than dropped,
so no row disappears. Verified against the specific historical defect (§0.2), same ADP vintage, one
variable changed:

```
rows before 471   after 471
columns that changed: depth
rows that changed: 12  — every one a fullback, depth 1 -> 11
chart agreement on the top two: 18/32 -> 28/32
```

The four still disagreeing are Stevenson, Etienne, Skattebo and Javonte Williams — the keeper-
removed starters §4.20 already names. Their `ahead` fields are correct; they simply have no board
row. **That is exactly why `inherit_2026.csv` is built off the source pull and the published chart
rather than off `depth_map.csv`.**

`Scripts\depth_map.py` is patched, the old copy is in `2026\_archive\depth_map_20260910.py`, and
`check_kit.py` is re-pinned to the new hash. `depth_map.csv` was regenerated: note that the copy on
the drive could not be reproduced from any pull still on disk, so its ADP-driven columns moved too
— it is reproducible now, for the first time.

---

## 5. What the builder refuses to do

`build_inherit.py` is standard library only, resolves every path against itself, and five negative
controls were run before it shipped — each one against the failure it exists to prevent:

| removed | what happened |
|---|---|
| the depth chart | STOP, exit 2 |
| `form_2025.csv` | STOP, exit 2 |
| a pull truncated to 19 backs | STOP, "that is not a full pull" |
| the WIRE file | runs, ownership reported unknown, no rows dropped |
| a top-two name from both the pull and the wire | that team is dropped and named — **the third man is not promoted** |

The last one is doc 251's rule with teeth. Removing Dylan Sampson from both files drops Cleveland
from the list entirely rather than quietly presenting Raheim Sanders as the man who inherits.

**New static input: `Source\form_2025.csv`** — 610 rows, all four skill positions, games played and
best two-week rate for 2025. It exists because `games_2025.csv` is derived from the keeper-removed
board and therefore has no row for Javonte Williams, Rhamondre Stevenson, Travis Etienne or Cam
Skattebo, four of the eight seats on the list above.
