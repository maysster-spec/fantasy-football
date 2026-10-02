# 203 — Age is real, and its name is availability

*2026-09-06, T−1. Matt: **"you can't honestly say age is not a factor for an RB... CTE, more prone
to re-injure, take longer to recover... performance does reach a typical high at age 27... the fact
that you haven't found the signals is the short coming instead of the fact players age."***

---

## 0. THE ANSWER

**n=735 player-seasons, 2021–2025, controlling for price, season and position:**

| | effect on beating your price | p |
|---|---|---|
| **age 28+** | **−3.8 pts** | **0.39 — null** |
| **played ≤12 games last season** | **−19.4 pts** | **0.00004** |

**He is right about the mechanism and wrong about where it shows up.** CTE, re-injury, slower
recovery, wear — **every one of those acts through availability**, and availability is the
strongest downside signal in this project: five times the size of age, at p<0.0001. Age *net of*
availability is indistinguishable from zero on 735 seasons.

**So "you haven't found the signal" is half right. The signal is found. It is called games played,
it has been on the board since doc 129, and it is bigger than he or I thought.**

## 1. NO BOARD REDO — THE BOARD ALREADY CARRIES IT

`make_board.py` prints the `12g` badge, shaded in three tones, for **any player** under 13 games in
2025 — 46 of 180 rows. That badge IS this finding. Nothing needs rebuilding.

**One directive correction does fall out.** §4.22(c) records the availability penalty as
**−16.2, "entirely a WR effect, RB null"** on n=45 receivers across two seasons. On five seasons
and 735 rows with position controls it is **−19.4, all positions**. The badge was already
position-blind, so **the code was right and the description was too narrow.** §4.22 updated.

## 2. THE INTERACTION HE ASKED FOR — TESTED, NOT RESOLVED

His framing is combination, not rule: *"I do need it to be a consideration in context and in
combination with other signals."* Correct instinct, so it was tested as an interaction rather than
a main effect.

| | games 13+ | games ≤12 |
|---|---|---|
| **RB** under 28 | −8.7 (n=138) | −26.2 (n=48) |
| **RB** 28+ | −21.5 (n=37) | −18.8 (n=9) |
| **WR** under 28 | −14.2 (n=163) | −28.9 (n=46) |
| **WR** 28+ | −13.1 (n=68) | **−36.3 (n=24)** |

**Interaction term: RB +19.7 (p=0.411), WR −9.6 (p=0.457), pooled −12.2 (p=0.370). All null.**
The WR cell he would care about — **old AND missed time, −36.3, the worst on the page** — has 24
rows behind it. That is a shape, not a finding, and it is **Terry McLaurin exactly**: 31 years old,
10 games in 2025, bottom-quartile snap share, live at pick 56.

**The RB interaction has NINE rows in the cell that would carry it.** No design resolves that
here. Naming it is honest; quoting it would not be.

## 3. WHAT IS STILL NOT TESTED, AND HE NAMED IT

**Randy Moss 2007.** Age effects conditional on a *situation change* — new team, new role, new
quarterback — are not measured anywhere in this project. §4.21 measured the team *environment*
(7.5% of variance) but never age × environment change. **That is a real gap and it is post-draft
work**; it needs the 2023 and 2025 preseason pulls to have enough old-player rows to cut on.

Also open: nothing predicts *which* early pick busts. §4.13 established you cannot predict which
player breaks out; the mirror has never been asked with the same rigour.

## 4. THE METHOD POINT, WHICH IS HIS

*"the fact that you haven't found the signals is the short coming instead of the fact players age."*

**That is the correct reading of an underpowered null and the directive already says so** — §4.24(b):
*"The RB version failed PREDICTION; this one failed POWER. Keep the distinction."* Doc 201 reported
age ≥28 at −12.1, p=0.209, and called it null. **The right report was: null, underpowered, and here
is what would resolve it.** The distinction matters because one of those sentences invites more
data and the other closes the file.

*Reproduce: nflverse weekly 2020–2025 (2020 supplies prior-season games for 2021) + rosters for
`birth_date`, joined to `Source\adp_registry\preseason_adp_YYYY.csv`; adp ≤ 180; beat = points minus
the within-season log(adp) fit; OLS with season, position and log(adp) controls.*
