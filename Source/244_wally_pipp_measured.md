# 244 — Wally Pipp, measured: it is real at running back, absent at receiver, and the trigger is production not age

**2026-09-09.** Matt, giving the mechanism in full:

> *"teams in a lot of cases would much rather have promising young players on the team who can rise
> that cost less on that rookie contract. They will sit behind that star/veteran player and eagerly
> attempt to gain trust and respect... When that older player performance starts to decline, gets
> to expensive, doesn't like the team dynamic, lack of wins, (please fill in here) then the coach
> and GM want to have the next man up planned for at all positions. The goal is to find the areas
> where that dynamic has more of an urgency or likelihood of occurring."*

> *"To be 'Wally pipped' means to lose your job, spot, or position permanently because a temporary
> replacement performed so well that they took over your role."*

**He named a testable event and it had never been run.** Doc 236 measured what the next man scores
*while* the starter is out. **It never asked whether he keeps the job after the starter comes back.**

---

## 0. THE TESTABLE FORM, STATED BEFORE THE RUN (§0.5a2)

> *When a lead skill player misses time and a backup fills in, does the backup hold a larger share
> of that job AFTER the starter returns than he held before?*
> **POPULATION:** every team-season 2021–2025 where the man with the most weeks-1–4 usage at a
> position group later missed at least one week **and then came back** (if he never comes back the
> job was vacated, which is a different event). **88 events.**
> **BASELINE:** the replacement's share of his team's position usage — carries + targets at RB,
> targets at WR/TE — in the weeks BEFORE the absence.
> **OUTCOME:** his share in the first 4 weeks after the starter returns, minus that.
> **DIRECTION:** positive.
> **FALSIFIER FIXED IN ADVANCE:** under +5 percentage points and it does not carry a pick.

---

## 1. THE FIRST RUN WAS WRONG AND THE GUARD MATTERS — §0.2 IN ACTION

The first pass gave **RB +9.8 pp, CI [+4.4, +15.4]** — clean and significant. **It was contaminated.**
Reading the top of the list caught it: *"Nick Chubb took over from Jerome Ford," "Alvin Kamara took
over from Jamaal Williams," "Josh Jacobs took over from Peyton Barber."* Those are **stars returning
from an early-season injury or suspension**, scored as takeovers because my "lead man" rule read
weeks 1–4, when the star was not playing.

**GUARD ADDED:** the replacement must have been a genuine backup in weeks 1–4 — on the field in at
least two of them, and under 60% of the lead man's early usage.

| | before the guard | **after** |
|---|---|---|
| RB, average share change | +9.8 pp, CI [+4.4, +15.4] | **+4.2 pp, CI [−1.5, +10.1]** |
| WR/TE | +1.6 pp, CI [−1.2, +4.4] | **−0.9 pp, CI [−3.1, +1.3]** |

**So the AVERAGE Wally Pipp effect is NOT established, and the +9.8 must not be quoted.** It failed
its own falsifier. `[TESTED, n=88]`

---

## 2. BUT THE CONDITIONAL EFFECT IS THE ONE HE ACTUALLY DESCRIBED, AND IT IS STRONG

His definition is not *"the backup gets more after."* It is **"a temporary replacement performed so
well that they took over."** Cut on that — RB only, n=40, median relief scoring 11.2 half-PPR ppg:

| the replacement, while filling in | n | share of the job after the starter returns, vs before |
|---|---|---|
| **scored above 11.2 ppg** | 20 | **+12.4 pp** CI [+4.2, +21.1] |
| scored below | 20 | **−4.1 pp** |
| **difference** | | **+16.6 pp, p=0.006** (permutation, 4,000 draws) |

**A back who produces in relief keeps a fifth of the job. A back who does not LOSES ground.**
`[TESTED, n=40]` **That is Wally Pipp exactly as he defined it, and it is the first time this
project has measured a mechanism he proposed and had it land above the falsifier on the first
honest cut.**

**And it is his §0.5(a3) frame again:** the signal is conditional, not standalone. The average is
null; the subgroup is +12.

---

## 3. FILLING IN HIS LIST — WHAT THE TRIGGER IS AND IS NOT

He wrote *"(please fill in here)."* Same 40 events, same outcome:

| candidate trigger | effect | p | verdict |
|---|---|---|---|
| **replacement produced in relief** | **+16.6 pp** | **0.006** | **THE trigger** |
| replacement is younger than the starter | +10.8 pp | 0.079 | his direction, **suggestive** |
| starter is 27 or older | +8.6 pp | 0.231 | his direction, underpowered |
| replacement on a rookie deal (≤3 yrs exp) | +2.1 pp | 0.734 | **null on its own** |
| replacement is 3+ years younger | −1.4 pp | 0.847 | **null** |
| **starter missed 3+ weeks** | **−10.6 pp** | 0.108 | **BACKWARDS — see below** |

**THE ROOKIE-CONTRACT ECONOMICS DO NOT SHOW UP.** Being cheap and young is not what moves the job;
**being good in the two weeks you get is.** Age is a weak echo of the same thing and does not
survive being sharpened to a 3-year gap. `[TESTED]` **His mechanism is right about the event and
wrong about the reason** — and the reason is the part that would have driven a draft rule.

**THE ONE I CAN ADD TO HIS LIST, AND IT INVERTS THE INTUITION: a SHORT absence is more dangerous to
the starter than a long one.** Missing 3+ weeks measures **−10.6 pp** against missing one or two.
Underpowered (p=0.108) and `[SUGGESTIVE]`, but the shape is legible: a long absence gets planned
around and the starter walks back into a defined role; **a one- or two-week cameo with a big number
is what actually flips a job.** Rhamondre Stevenson 25.4 ppg over one week in 2021; Rico Dowdle 31.4
over two in 2025; Kyle Monangai 21.3 over one in 2025.

---

## 4. IT DOES NOT WORK AT RECEIVER, AND THAT ANSWERS HIS QUESTION ABOUT HIS OWN LIST

Matt: *"at least some of the names i sent you fit that prototype. If not, then other signals likely
apply."*

**WR/TE: −0.9 pp, CI [−3.1, +1.3]. Only 10 of 48 replacements kept even 5 points of share.**
`[TESTED, n=48]` **The mechanism is measurably absent at receiver.**

**The reason is structural, not sample size: a backfield is ONE job and a receiver room is three to
five.** An absent WR1's targets scatter across the other three, each one's role is already defined,
and the incumbent walks back into his. There is nothing to seize.

So his list splits cleanly:

| his name | fits the measured prototype? |
|---|---|
| **Jonathon Brooks** (RB CAR, behind Hubbard, UNSETTLED) | **YES** — and Hubbard is himself in the takeover table, having taken the job off Miles Sanders in 2023 |
| **Jonah Coleman** (RB DEN, behind Dobbins) | **YES** — and Dobbins is the least available lead back we have measured (10 of 17, then 13 of 17) |
| **Blake Corum** (RB LAR, behind Kyren) | **YES** |
| Mike Washington Jr. (RB LV, behind Jeanty) | shape yes, **trigger unlikely** — Jeanty is a durable 22-year-old |
| Tyjae Spears (RB TEN, behind Pollard) | shape yes; already priced at ≈ −5 on his bench (doc 240) |
| **KC Concepcion · Quentin Johnston · Jordyn Tyson · Ladd McConkey** | **NO** — all receivers, and three of the four are already their team's depth-1. **Not a bad read on his part: the prototype simply does not exist at the position** |

**AND THIS CLOSES DOC 242's LOOP.** Tyson was never a Wally Pipp candidate. He is the *other* shape
— **a man who already holds a job the price does not believe in.** Two different gems, two different
finders, and the sheet has a flag for neither. `dart_shape` covers the first one badly (12 backup
RBs, doc 242) and the second one not at all.

---

## 5. THE TEN BIGGEST TAKEOVERS, 2021–2025 — the population, so it can be argued with

| year | who took the job | from | before → after | absence | ppg in relief |
|---|---|---|---|---|---|
| 2021 BAL | Devonta Freeman | Latavius Murray | 15.1% → 70.5% | 1 wk | 11.4 |
| 2024 NYG | **Tyrone Tracy Jr.** | Devin Singletary | 20.0% → 69.7% | 2 wk | 16.6 |
| 2024 LV | Alexander Mattison | Zamir White | 30.3% → 66.7% | 2 wk | 11.1 |
| 2025 CAR | **Rico Dowdle** | Chuba Hubbard | 30.1% → 63.3% | 2 wk | **31.4** |
| 2021 GB | AJ Dillon | Aaron Jones | 38.5% → 67.8% | 1 wk | 12.7 |
| 2023 CAR | **Chuba Hubbard** | Miles Sanders | 36.6% → 61.4% | 1 wk | 15.5 |
| 2022 TB | **Rachaad White** | Leonard Fournette | 30.8% → 55.6% | 1 wk | 15.4 |
| 2023 HOU | Devin Singletary | Dameon Pierce | 30.7% → 54.3% | 3 wk | 15.0 |
| 2025 CHI | **Kyle Monangai** | D'Andre Swift | 28.8% → 43.4% | 1 wk | 21.3 |
| 2023 SEA | Zach Charbonnet | Kenneth Walker III | 29.2% → 43.5% | 2 wk | 12.1 |

**Every one is a running back, and eight of the ten came off an absence of one or two weeks.**

---

## 6. WHAT THIS CHANGES

- **The gem lane's RB half is now measured end to end.** Doc 224 said claim the handcuff before the
  injury because he loses 5 of 6 contested claims. Doc 236 measured what the man scores while the
  starter is out. **This measures what he keeps afterwards, and it is conditional on him producing.**
- **The WR half of the gem lane needs a different instrument and this one is not it.** Do not build
  a receiver handcuff flag; the event does not exist.
- **`dart_shape` should be conditioned on the man ahead, not just on there being one.** The live
  version of the trigger is *the starter's fragility × the backup's ability to produce in two weeks*
  — which is doc 236's availability table times a per-game rate, both of which we already hold.

---

## 7. OPEN THREADS THIS ADDS

- **The two-shape gem finder.** Shape A (handcuff, RB only) is measured. Shape B (Tyson — holds a
  job the price does not believe) is stated in doc 243 §4 and **not yet run**.
- **Position styles.** Matt: *"there isn't one type of WR."* Nothing in this project distinguishes
  an X from a slot from a deep threat. nflverse carries `ngs_position` and air-yards, so it is
  buildable and has never been tried. **NOT YET RUN.**
- **Contract data** — still BLOCKED (doc 243 §4); and §3 above weakens the case for chasing it, since
  the rookie-deal term measured null on its own.
- Carried: the Aug-8 depth chart is a month stale; the back half of `draft_analysis.json` needs a
  real comparator; the register itself is unbuilt.
