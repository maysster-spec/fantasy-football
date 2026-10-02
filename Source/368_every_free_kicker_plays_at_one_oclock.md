# 368. THE WAIT-AND-SEE PLAN ON PINEIRO IS DEAD: ALL SIX FREE KICKERS KICK OFF AT 1:00 AND HE KICKS OFF AT 4:25

*19 September 2026, Saturday morning ET. Written from a session opened on `00_START_HERE.md` v8 with the
v9.8 paste live in the project instructions. Every status below came from a page that was LOADED, with its
date stated; nothing here rests on a search-result snippet. Doc 367 is the previous number; 368 reserved by
listing the folder first.*

---

## 0. WHAT TO DO

1. **Matt, before 1:00 PM Sunday: drop Emari Demercado, add Chris Boswell, and start Boswell over Eddy
   Pineiro.** Pineiro is QUESTIONABLE and did not practice Friday with an illness. Keeper cost of the drop:
   **zero, and it is not a judgement call.** Demercado was not one of your 14 draft picks, so he is a
   waiver pickup and was never keeper-eligible.
2. **The reason it has to happen before 1:00 and not at 2:55 is the schedule, not the illness.** Pineiro
   plays at 4:25, inactives post at 2:55, and **every one of the six free kickers on your own sheet kicks
   off at 1:00.** Waiting to see the inactive list leaves you with nobody to add. That option is CLOSED.
3. **You need to be 93% sure Pineiro plays to justify starting him, and a Friday DNP is nowhere near it.**
   Derived from your own sheet: 8.5 divided by 9.1. Working in section 3.
4. **This is also the week-7 item on your list, done early and for free.** `matt_todo.txt` carries
   *"week 7 add a kicker for week 8"* against Pineiro's week-8 bye. The man you add today is that man.
5. **Nacua: nothing to do today, and do NOT drop Devaughn Vele this weekend.** Nacua did not practice
   Friday with a hip injury and the Rams play Monday night. Section 4 has the decision point, which is
   Sunday evening and not Monday.
6. **A defect, and it is the one that priced the drop:** `MY_ROSTER.csv` has Emari Demercado on Kansas
   City with a week-5 bye. He is a Dallas Cowboy. Section 5.

**Nothing for you to run.** `ff.bat` will not fix any of this, because the pull it reads is not the thing
that is stale.

---

## 1. THE DATE, AND WHAT THE PAGES CANNOT SEE

`ff.bat` last wrote at **Friday 18 September 08:57**. `WEEK_SHEET.html`, `LINEUP_CHECK.html`,
`MY_ROSTER.csv` and `WIRE_20260918.csv` all carry that timestamp. **Every Friday injury report in the NFL
lands Friday afternoon.** So the pages are not a little stale, they are stale in exactly the one way that
matters on a Saturday: they were built before the week's final injury designations existed.

`injuries_2026.csv` is worse and `00_START_HERE.md` section 1 already names it: last touched **13
September**, and it holds **week 1 only**, 182 rows, every row `week == 1`. It cannot answer a week-2
question and it does not say so on its face.

Both of Matt's men who appear in it, Xavier Worthy and Ashton Jeanty, are listed there as full
participants in week 1. That is a fact about week 1 and nothing else.

---

## 2. THE STATUS OF THE FIFTEEN, FROM LOADED PAGES

Primary source: **nfl.com/injuries**, the official league report, page states its coverage as **Week 2,
games 17 to 21 September 2026**. Loaded. Cross-checked against individual RotoWire player pages, loaded,
dates given below.

| man | team | week 2 kickoff ET | designation | practice |
|---|---|---|---|---|
| Jalen Hurts | PHI | Sun 1:00 at TEN | none | not on report |
| Ashton Jeanty | LV | Sun 4:05 at LAC | none | **full** |
| Quinshon Judkins | CLE | Sun 1:00 at TB | none | not on report |
| Rico Dowdle | PIT | Sun 1:00 at NE | none | not on report |
| J.K. Dobbins | DEN | Sun 4:05 vs JAX | none | not on report |
| Mike Washington Jr. | LV | Sun 4:05 at LAC | none | not on report |
| Emari Demercado | **DAL** | Sun 4:25 vs WAS | none | not on report |
| Davante Adams | LAR | **Mon 8:15 vs NYG** | none | **full** |
| George Pickens | **DAL** | Sun 4:25 vs WAS | none | not on report |
| Xavier Worthy | KC | Sun 8:20 vs IND | none | not on report |
| Devaughn Vele | NO | Sun 1:00 vs BAL | none | not on report |
| Sam LaPorta | DET | **played Thu 17 Sept** | none | n/a |
| **Eddy Pineiro** | **SF** | **Sun 4:25 vs MIA** | **QUESTIONABLE** | **DNP, illness** |
| Chiefs D/ST | KC | Sun 8:20 vs IND | n/a | n/a |
| Puka Nacua | LAR | **Mon 8:15 vs NYG** | **hip, DNP Friday** | **DNP** |

**A caveat that matters and is not a hedge:** a man who does not appear on the official report has no
practice row at all, so "not on report" means no limitation was reported, not that a full practice was
observed. Only Jeanty and Adams have an affirmative full-participation row; only Pineiro and Nacua have an
affirmative DNP.

**LaPorta's week is already over.** Detroit played Thursday and lost 41 to 31. He caught six of seven
targets for 52 yards and a touchdown. RotoWire, updated 17 September 22:34, loaded.

**Two men outside the fifteen who move a decision.** Denver's RJ Harvey is questionable with a hamstring
and limited in practice, which is the man taking touches from Dobbins. Las Vegas tight end Brock Bowers is
doubtful with a knee, which pushes work toward Jeanty in the 4:05 game.

---

## 3. THE KICKER, WORKED THROUGH

**The wait-and-see plan fails on the clock and it was decidable before anyone read a word of it.**

Pineiro is San Francisco and San Francisco hosts Miami at **4:25**. Inactive lists post 90 minutes before
kickoff, so Pineiro resolves at **2:55**. The six free kickers on `WEEK_SHEET.html`, and their week-2
kickoffs from the loaded nfl.com week-2 schedule:

| free kicker | sheet rate | week 2 game | kickoff |
|---|---|---|---|
| Trey Smack | 8.5 | GB at NYJ | **1:00** |
| Chris Boswell | 8.4 | PIT at NE | **1:00** |
| Will Reichard | 8.4 | MIN at CHI | **1:00** |
| Chase McLaughlin | 8.4 | CLE at TB | **1:00** |
| Evan McPherson | 8.3 | CIN at HOU | **1:00** |
| Nick Folk | 8.3 | CAR at ATL | **1:00** |

**All six. At 1:00. Every one of them has already kicked off by the time Pineiro's status is known.**

**THE BREAK-EVEN, DERIVED FROM THE SHEET'S OWN TWO NUMBERS AND LABELLED DERIVED, NOT MEASURED.** Starting
Pineiro is worth his rate times the chance he plays: 9.1 times p. Starting the best free kicker is worth
8.5, and a healthy kicker plays. Setting those equal gives **p = 8.5 / 9.1 = 0.934**. Matt would have to
be **93% confident** Pineiro suits up. A Friday DNP carrying a questionable tag does not reach 93%, and
**I have not measured what it does reach**, so that is a judgement call and is labelled one. The point is
that the bar is high enough that the judgement does not have to be precise to clear it.

**Why Boswell over Smack, against the sheet's own order.** The sheet ranks Smack first by 0.1 points,
which is inside the noise of a single kicker week and is not a reason to prefer anybody. Outside the
model, Boswell is the steadier leg and Pittsburgh at New England is the friendlier game script for
attempts. **That is a judgement and it is mine, not a measurement**, so if Boswell is gone take Smack and
nothing is lost.

**THE ADD MUST BE A FREE-AGENT ADD, NOT A WAIVER CLAIM, AND THIS IS THE TRAP.** A claim does not process
until the next waiver run, which is after Sunday. **A claim would spend one of the two runs and still
leave the slot empty on Sunday.** If ESPN shows one of these men as a claim rather than a free add, he is
the wrong man, so take the next one on the list who can be added outright.

**One option named and killed so it is not reconsidered at 2:00 on Sunday: Pineiro cannot be stashed on
IR.** ESPN needs an OUT or IR designation and questionable is neither.

---

## 4. NACUA, AND THE DECISION POINT IS SUNDAY EVENING

**Nacua (hip) did not practice on Friday 18 September.** NBC Sports player news, URL dated 2026-09-18,
loaded, though only the headline and metadata rendered, so the body is unread. RotoWire's player page,
loaded, lists him questionable with an estimated return of 9/21 and carries two items dated 18 September:
he practised in full on Thursday and missed Friday. The older conduct-policy review is still unresolved
and separate from the hip. Pro Football Rumors, 6 September, loaded.

**The Rams play the Giants Monday 21 September at 8:15, so the hip does not cost him Sunday.** For a
Monday game the final injury report lands **Saturday**, which is today, and Nacua's official designation
should exist by tonight.

**THE TRAP IS THE SLOT, NOT THE MAN.** If Nacua sits in the lineup on Monday and is ruled out at 6:45, the
only replacements whose games have not started are Rams and Giants players. **Xavier Worthy kicks off
Sunday at 8:20 and is gone by then.** So the real decision point is **Sunday before 8:20**, not Monday:
start Nacua and accept a zero if he is out, or start Worthy in that slot on Sunday night and let Nacua go.

**And this is why Devaughn Vele stays.** `WEEK_SHEET.html` puts Vele's drop cost at 0.0 and then says in
its own words that the zero *"only means he never starts while Puka Nacua is healthy."* That condition is
not met this weekend. Vele is not the cheapest drop right now. Demercado is.

---

## 5. THE DEFECT THAT PRICED THE DROP: A NAME JOIN PUT A COWBOY ON KANSAS CITY

`MY_ROSTER.csv`, built by `ff.bat` Friday 08:57, row for Emari Demercado:

```
2026-09-18,4362478,Emari Demercado,RB,KC,5,-112.7
```

**Team KC, bye 5.** `LINEUP_CHECK.html`, built by the same run, from the same pull, says **DAL**. RotoWire,
14 September 2026, loaded: *"Two carries in Cowboys debut."* A wibw.com piece dated **5 August 2026** has
him signing with Kansas City, which is the stale fact the join appears to have latched onto and is
superseded by his Dallas debut.

**Two files from one run disagree about one man**, which is the signature of the name-join defect the
directive's SECTION 3 warns about: `LINEUP_CHECK` carries ESPN's own team field and `MY_ROSTER` joins team
and bye from elsewhere by name. **`MY_ROSTER.csv` is the one that is wrong.** Check ledger row 108 before
quoting either; `00_START_HERE.md` names it as the live example of exactly this.

**The consequence is not cosmetic.** `WEEK_SHEET.html` prices Demercado as *"the seat behind Kenneth Walker
III"*, and Kenneth Walker III is a Seattle Seahawk. **A Dallas running back cannot be the backup in
Seattle.** The only argument the sheet ever made for holding Demercado rests on a seat he does not sit in.
That is what makes him the drop rather than Vele, and it is the second time this project has found the
sheet pricing a bench back by a broken link rather than by the job (the first was Mike Washington Jr.).

**Also in that file: three rows carry a blank position, team and bye** - George Pickens, Eddy Pineiro and
Chiefs D/ST. Pickens is a keeper and a starting receiver, and his row has no team on it. Pickens is
Dallas, Pineiro is San Francisco, both from loaded pages.

**NOT YET RUN:** the same check across `LEAGUE_ROSTERS.csv`. If the join drops team and bye for three of
fifteen on Matt's own roster, the other eleven teams are suspect at the same rate, and the seat list reads
that file.

---

## 6. WHAT THIS SESSION DID NOT DO

**NOT YET RUN: the regression test doc 366 set and doc 367 listed as its item 5**, the two fileless probes
plus Fable's Part A against the new paste. **Its blocker is cleared**: doc 367 item 1 asked Matt to paste
v9.8 and the paste is live, since this session opened with the v9.8 header in its instructions. The item
is still open on `matt_todo.txt` and can be ticked.

**BLOCKED: whether the six free kickers are still free.** The ownership column is from Friday 08:57 and
only Matt's ESPN session can see the pool now. Tried: `WIRE_20260918.csv` holds no kickers at all, so the
wire file cannot answer it either.

**OPEN, and it is a conflict between two of Matt's own instructions, not a defect:** the directive's
§0.5(e) says anything Matt is asked to run goes into `Source\matt_todo.txt` the moment it is said, and the
header of `matt_todo.txt` says *"I maintain it; you never edit it."* **I did not edit it.** The Sunday
kicker move is in section 0 above and was sent to him directly. Matt settles which rule wins.
