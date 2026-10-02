# 460. THE TAIL, NOT THE MEAN: WHICH BENCH TICKET WINS A MONTH

*1 Oct 2026, 07:45 ET. Claude (Cowork). Matt, 1 Oct 07:30: "Just because the average of backups doesn't hit or return for
extended time doesn't mean it can't happen and strike big ... Consider 2017 when Kareem Hunt took over the backfield for KC
... 9th in points is not going to cut it this season. I need to take this chance now before it is too late ... I don't feel
we are measuring the right thing the right way. The goal is to take a chance before it is too late." 460 reserved by
listing `Source\` (459 is the open-job doc). No em dashes.*

---

## 0. WHAT TO DO

1. **Claim Emanuel Wilson (RB, SEA), drop Devaughn Vele. Place it today; he clears Friday about 03:00.** He is the fattest
   free ticket on the measured table (section 1): the second back in a real split, 11 touches a game, and the man ahead of
   him, Jadarian Price, is questionable with a chest injury for Sunday. Your priority is 11 of 12 and resets Tuesday, so the
   claim spends almost nothing. The take contract is in section 2.
2. **Add Tyler Allgeier (RB, ARI) as a free agent now, drop Malik Washington, if you are willing to make Sunday's seat for
   Nacua out of the Bengals D/ST or Barner instead.** He is the second ticket: the only back behind Jeremiyah Love with
   Conner and Benson both on injured reserve, and he had 19 touches the one week Love was eased in. The add also answers a
   question no file holds: you carry six backs counting the two on IR, so if ESPN refuses the add on the RB limit, IR men
   count against the cap and the Wilson claim will fail the same way. Tell me which happened.
3. **Do not drop J.K. Dobbins for any ticket. He is the best ticket on the table and you already hold him.** A lead back
   with the touches but not yet the points (19 last game, 4.3 a game so far) is the shape that most often turns into a
   league-winning month: 28% of 32 such men over five seasons, against 14% for a committee partner, 6% for a handcuff and
   0 of 249 for a third-string back. His exact cell (12 to 15 touches a game) is 20% of 15. Nothing on the wire is close.
4. **The rule that comes out of this, for the sheet: when you are behind in points, the bet lane ranks tickets by the odds
   of a BIG hit, not by expected points.** The seat list's expected value is the mean (relief points times weeks), which is
   the right unit for a team ahead and the wrong one for a team ninth in points. A lane of under-the-bar free men ranked by
   the measured big-hit odds of their shape goes on the page next (section 4).
5. **Two things that are measured and lean against the words, said plainly.** A third-string back bought before anything
   has happened is 0 for 249 on six startable weeks and 0 for 249 on a big month, five seasons. And the Hunt shape is a
   draft-day handcuff whose starter fell in August; by week 4 that man is a starter and off the wire, which is why 78% of
   the backs who gave six or more startable weeks from here on were already startable in September. The ticket that catches
   Hunt is the one the draft book buys at 104 and 113, and Mike Washington behind Jeanty is it on this roster.

---

## 1. THE MEASUREMENT

**The claim in testable form (his words: "a high end backup CAN hit, and some actually do hit big ... When backups do hit,
they stand to gain more than what is currently sitting on my bench"):** among men a manager could hold on a bench at the end
of week 4 (under the position's startable bar on weeks 1 to 4), the chance of a BIG hit over weeks 5 to 14 differs by the
shape of the ticket, and the backup behind a real job has the fattest tail. Not the mean: the share who give six or more
startable weeks of the next ten, or a four-week window at 15 or more a game (a league-winning month).

**Population.** nflverse 2021 to 2025, regular season, backs and receivers, half-PPR under our rules. Shape from the team's
own touches per game on weeks 1 to 4. Receivers' marks from doc 453's builder at week 4. `Scripts\research\wk1\tail_tickets.py`.

| the ticket at the end of week 4 | n | mean pts, wks 5-14 | 4+ startable wks | 6+ startable wks | a 15+ month |
|---|---|---|---|---|---|
| lead back under the bar, 12+ touches a game | 32 | 77.2 | 46.9% | 18.8% | **28.1%** |
| lead back under the bar, under 12 a game | 9 | 72.5 | 55.6% | 0.0% | 22.2% |
| RB committee partner, the #2 with 8 to 14 a game | 59 | 56.3 | 23.7% | 8.5% | **13.6%** |
| RB handcuff behind a top-12 job | 35 | 32.4 | 5.7% | 0.0% | 5.7% |
| RB handcuff behind any other job | 36 | 44.2 | 19.4% | 5.6% | 5.6% |
| RB third string or lower | 249 | 14.3 | 1.2% | **0.0%** | **0.0%** |
| WR young, 3 of 3 on the in-season screen | 22 | 67.5 | 36.4% | 4.5% | 4.5% |
| WR young, 2 of 3 | 42 | 43.1 | 14.3% | 4.8% | 9.5% |
| WR young, 0 or 1 of 3 | 68 | 24.8 | 2.9% | 0.0% | 0.0% |
| WR veteran, 2+ targets a game | 285 | 36.8 | 10.9% | 1.4% | 2.5% |

**The handcuff when the starter does go down (his case):** one handcuff in four (17 of 71) saw his lead back miss three
or more of the ten weeks. Those 17: 35% gave four or more startable weeks, 12% six or more, 6% a big month, 52 points on
average. The 54 whose starter stayed up: 6%, 0%, 6%, 34 points. So the handcuff is two coin flips in a row and the second one
is still only one in three, which is why his mean is low; the tail is real and it is 3% unconditional.

**Where the league-winning stretches come from.** Of the 67 backs who gave six or more startable weeks over weeks 5 to 14,
52 (78%) were already startable on weeks 1 to 4; 6 were lead backs under the bar; 5 were committee partners; 2 were
handcuffs (Kenneth Walker 2022, Tyrone Tracy 2024); none was third string. Receivers: 54 of 66 (82%) already startable.

**The dependence of the lead-back cell, because Dobbins is at its bottom:** 12 to 15 touches a game, n=15: 40% four-plus
weeks, 7% six-plus, 20% a big month. 15 or more, n=17: 53%, 29%, 35%. Under 6 points a game so far, n=4: 0 of 4 on every
column, too thin to lean on either way.

**The one thing this cannot see:** the measurement is "could be held", not "was free in a 12-team league". A lead back
with 12+ touches is almost never on the wire (today: none), and committee partners sometimes are (today: Wilson on waivers,
Allgeier free). That is the population header for every number above.

## 2. THE TAKE CONTRACT

**Emanuel Wilson, RB, SEA (claim, Friday run).** Vintage: 2026, 3 games, touches 2, 22, 9; 3.6 points a game. Population:
the committee-partner cell, n=59, 8.5% six-plus weeks and 13.6% a big month, a screen and not his forecast; the man ahead
questionable is on top of that and unmeasured as an interaction. The man ahead: Jadarian Price, 0 games missed, questionable
(chest), return date 4 Oct; 12, 15, 8 touches. The rule: "bench RB to the cap", which this obeys; after the move, RB
Jeanty, Judkins, Dobbins, Washington, Wilson plus Coleman and Dowdle on IR; WR Adams, Pickens, Raymond, Malik Washington
plus Nacua on IR; whether the two IR backs count toward the cap of six is NOT ESTABLISHED, and a claim that fails on a
position limit is doc 435's category. Counterfactual: Vele, worth 0.0 above your bar in every week on the sheet and already
the drop you named on the Gordon claim; your priority for the rest of this week at 11 of 12.

**Tyler Allgeier, RB, ARI (free agent, now).** Vintage: 2026, 3 games, touches 19, 7, 6; 4.6 points a game. Population:
the handcuff cell behind a job outside the top 12 (Love's 17.7 a game ranks 15th), n=36, 5.6% six-plus and 5.6% a big
month; when the starter misses three-plus of the ten, 35% four-plus and 12% six-plus (n=17). The man ahead: Jeremiyah Love,
0 missed, no designation, 26 touches last game; behind Allgeier nobody, Conner and Benson on IR. Rule and roster as above
with Allgeier in Malik Washington's seat, which makes Sunday's seat for Nacua the Bengals D/ST (a bye-week hold; the line
rule re-streams it) or Barner (re-claimable in week 5). Counterfactual: Malik Washington, 0.0 above the bar on the sheet.

**Closed, with the reason:** MarShawn Lloyd (GB, on waivers) is the only free lead back and his touches read 14, 8, 7 in a
three-way split; a fall at a given level is a caution (4.38) and 54% of the league just let him go. Tank Bigsby and Chris
Rodriguez are handcuffs behind healthy men; Kendre Miller is third behind Etienne and Kamara, the 0-for-249 cell.

## 3. THE POSTURE, HONESTLY

You are 2-1 and fifth seed on the lowest points against in the league (264.8), ninth in points for (293.6 against a
median of 334). The best nine on ESPN's rest-of-season projection ranked third (doc 456), so the deficit is men scoring
under their rate, not a roster without a ceiling: Nacua 3.3 a game against 17.4 projected (hip, questionable, back Sunday),
Pickens 7.7 against 11.7, Judkins 7.4 against 11.7, Dobbins 4.3 against 10.7. Those four returning to rate is worth more
than any ticket on the wire, and it costs nothing. That does not argue against the ticket; Vele and Malik Washington are
worth nothing, so a ticket for them is free. It argues against paying a real player for one, and it is why item 3 says
Dobbins stays.

Variance over mean is the right posture for a team behind in points, and this doc is the first time the page's unit has
been the tail. Measured, the fat tails are in the lead-with-touches and the committee partner, not in the pure handcuff and
never in the third string. A Wally Pipp is real (4.27) and its trigger is production in relief, which is why the wire's
relief lane buys him AFTER the game that shows it; bought before, the third-string man is 0 for 249 in five seasons.

## 4. WHAT CHANGES ON THE PAGE

A lane under the seat list: under-the-bar free backs and receivers, each with his shape and the two big-hit odds from the
table above, ranked by the month column; the standings line decides whether it leads the seat list (behind in points) or
follows it. `tail_tickets` block in `sheet_constants.json` carries the cells. Shipped with this doc or the next.

## 5. OPEN, BY NAME

- **Matt's:** the Wilson claim before Friday 03:00 and the Allgeier add; which way the RB cap went; Sunday's Nacua
  move; Thursday's pair; the week-5 tight end; the routes purchase; the D/ST box score; the Opus chat and the podcasts.
- **Mine:** the lane (section 4); directive v9.38 with 4.48 (this doc) beside 4.44 to 4.47; the handcuff cell against the
  starter's prior-season availability (4.22), NOT YET RUN; the lead-back cell on the latest game's touches rather than the
  four-week average (4.38's level), NOT YET RUN.
