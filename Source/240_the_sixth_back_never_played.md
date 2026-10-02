# 240 — The sixth running back never played, and the spot he held cost about five points

**2026-09-09.** Matt: *"holding Spears on my bench was of negative value. the only time I would need
him is if I was hungry and desperate on a bye week and needed a fill in."*

**Both halves are right, and the second half is stronger than he put it: there was no bye week where
he would have needed him.** My own number — dropping Spears measures **+0.00** (doc 234 §2) — was
true and understated the case, because it priced the man and never priced the spot.

---

## 0. ACTIONABLE

1. **HE NEVER STARTS. Not one of the fourteen weeks — week 11 included, with three starters off.**
2. **A NUMBER THAT REPLACES MY OWN: holding him was about −5, not 0.00.** The option on Pollard is
   worth roughly **+2**; the same spot on the week-6 tight end measured **+7.1**.
3. **NEW RULE, now in §6 at v8.6: a bench running back earns his spot by the JOB he would inherit
   and the fragility of the man ahead — never by his own projection.**
4. **SAME ROSTER, SAME ROUNDS, OPPOSITE VERDICTS:** Washington sits behind a **247** job whose
   holder is flagged today; Spears sat behind a **171** job whose holder had missed **one game in
   two years**.
5. **§4.17b's "the sixth body plays only when three are out at once" IS TOO GENEROUS** — three were
   out in week 11 and he still did not play.
6. **THE DOCTRINE IS NOT OVERRIDDEN.** "Bench RB to the cap" rests on §4.19 and is untouched. What
   changes is WHICH backs fill the cap, not how many.
7. **Directive at v8.6 — this supersedes v8.5, paste this one.** v8.5 archived as
   `00_PROJECT_DIRECTIVE_20260909b.md`; it lived one hour and was never pasted.
8. **Nothing to run.**

---

## 1. THE TEST

**POPULATION: his 15-man roster as drafted. BASELINE: best legal nine (1 QB, 2 RB, 2 WR, 1 TE,
1 FLEX, 1 D/ST, 1 K), recomputed for each of weeks 1–14 with that week's bye men removed, on ESPN's
projections divided by 16.** The question is not what Spears is worth — it is whether the lineup
ever reaches him.

| week | who is off | the nine that start |
|---|---|---|
| 9 | **Dowdle, Spears** | Hurts · Jeanty · Judkins · Nacua · Pickens · LaPorta · Adams · Browns · Pineiro |
| **11** | **Nacua, Judkins, Adams, Browns** | Hurts · Jeanty · **Dowdle** · Pickens · **Worthy** · LaPorta · **Dobbins** · Pineiro |
| 13 | Jeanty, M. Washington | Hurts · Judkins · Dowdle · Nacua · Pickens · LaPorta · Adams · Browns · Pineiro |

**Weeks Spears would have started: NONE.** He is 8.09 a game against Dowdle 10.85, Dobbins 10.26 and
whoever takes FLEX. **Week 11 is the case that settles it** — the worst week of the season, three
starters and the defence gone, and the lineup still reaches only as far as Dobbins. **The three men
off were WR/WR/RB, so the FLEX absorbed the running back and the hole opened at receiver, where
Worthy filled it.** `[TESTED — arithmetic on the shipped projections, all 14 weeks]`

## 2. WHAT THE SPOT WAS WORTH, WHICH I HAD NEVER PRICED

**+0.00 was a measure of the MAN. Matt is talking about the SPOT, and he is right that the project
has only ever priced one of those.**

- **What Spears was:** an option on Tony Pollard. **Pollard played 33 of 34 games in 2024–25.**
  Tennessee's `job_ceil` is **171 — the smallest backfield job in anything we have looked at**, on
  the league's **30th-ranked scoring offence** (doc 221, and Matt called that one himself). Even
  granting the full inheritance at the job's own rate (~10.1 a game) against a wire back at 5.43
  (doc 12), and Pollard's own missed-game rate over fourteen weeks, **the option is about +2 points,
  with a low-probability tail if the UNSETTLED flag resolves his way rather than by injury.**
- **What the spot could have been:** the tight end that closes the week-6 hole measured **+7.1**
  (doc 234 §3). **Net: roughly −5.**
- **`[ARITHMETIC, not a simulation — and the +2 rests on one man's two-season durability, which is
  a thin base. Treat the sign as solid and the size as loose.]`**

**And his "hungry and desperate on a bye week" is the honest test of the whole idea — it is exactly
the scenario the +0.00 was supposed to cover, and §1 shows the scenario never arrives.**

## 3. THE RULE

**A BENCH RUNNING BACK EARNS HIS SPOT BY THE JOB HE WOULD INHERIT AND THE FRAGILITY OF THE MAN
AHEAD OF HIM — NEVER BY HIS OWN PROJECTION.**

This is not new evidence. It is **§4.20's "buy the job, never the name" applied to the bench**, and
it is what doc 236's handcuff measurement was already saying: when a lead back sits, the next man
scores **13.62 a game and is startable 62% of the time** — a number that belongs to the JOB, not to
the backup's preseason line.

| | job ceiling | the man ahead | his 2024/25 games | verdict |
|---|---|---|---|---|
| **Mike Washington Jr.** | **247** | Ashton Jeanty | 17, **flagged today** | keep |
| **Tyjae Spears** | **171** | Tony Pollard | **33 of 34** | drop — and he did |

**Two backs, same roster, adjacent rounds, and the projections barely separate them (8.09 against
3.91 — the WRONG way). The jobs separate them completely.**

## 4. OPEN

- Everything carried from docs 236–239: the tight-end decision, LaPorta's week-1 designation, the
  waiver-window field, the bye-table divisor, the denial term, Hampton's and Skattebo's game counts,
  `manager_identity_map.csv`, the bet metric in doc 239 §0, and **pasting v8.6**.
