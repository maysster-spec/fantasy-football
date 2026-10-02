# 208 — Why the plain-English rule kept losing, and the guard that stops it

*2026-09-06. Matt: **"you know what I want right. somehow that refinement gets left out in the word
construction phase when you dump it off to the engine. I don't know what the issue is, but is it
persona based?... a repeated issue by my humble measure."***

---

## 0. THE ANSWER: NOT PERSONA. TWO RULES COLLIDE AND ONLY ONE HAS TEETH.

- **§0.2 and §3 REQUIRE provenance** on every number — baseline, population, sample size, a doc
  number, a `[TESTED]` tag. **Specific, mandatory, and enforced** by `audit_directive.py`.
- **§0.1 asks for plain English with no jargon.** **General, aspirational, enforced by nobody.**

**When both apply to one sentence, the specific mandatory rule wins. Every time.** That is the
whole mechanism, and it predicts exactly what he keeps finding:

> ⭐ *the only names §7 ranks at pick 32, in dollars over 100 board states (N=2,000): spread across
> all five is $2.7*

Every clause of that is required by §0.2 and §3. It is a **correct doc sentence printed on a sheet
he reads at 60 seconds a pick.** He is right that it repeats, and he is right that it is not a
one-off wording slip.

**It is also not persona.** The tell is that the same session that wrote that line also wrote the
plain version in chat without being asked twice. The register was available; the rule that would
have selected it had no force.

## 1. THE SCOPE RULE — now in §0.1 (v8.2)

**Provenance belongs in `Source\*.md`. A printed or rendered page carries the instruction and the
plain number, and nothing else.** Same fact, two registers, chosen by who is reading.

**Off the paper:** section numbers · doc numbers · p-values · sample sizes · rho and r · confidence
intervals · statistics vocabulary (bootstrap, quartile, regress) · internal column names
(`eff_pick`, `adp_pick`, `roll`) · and **VBD** — the paper says **VOR**.

**Lead with what to DO, then what it is.** The evidence is in the doc and he can ask for it.

## 2. AND IT IS A GUARD NOW — `py check_plain.py`

Step 12 of `sept5_after.bat`, `--warn` so a wording slip never halts a rebuild. Standard library
only. Strips `<style>`, `<script>` and comments first, so it reads only what a human can see.

**Its negative control is Matt's own quoted line** (`py check_plain.py --selftest`):

```
SELFTEST on the line Matt quoted:
   caught a directive section number   '&sect;7'
   caught a sample size                'N=2,000'
SELFTEST on its replacement: 0 hits
SELFTEST PASS
```

**And it caught a live one on its first run against the real pages:** `DRAFT_BOARD` still read
*"One list, 180 players, sorted by VBD"* where every other sheet says VOR. Fixed.

§0.2 asks that a guard be run against the specific historical defect that motivated it and shown to
fire. **This one was written from the defect and fires on it.**

## 3. WHAT WAS REWRITTEN

Both grids and the tier sheet. Examples:

| was | now |
|---|---|
| ⭐ *the only names §7 ranks at pick 32, in dollars over 100 board states (N=2,000)…* | **One of the five worth taking at pick 32.** Take whichever shows first — across a hundred simulated drafts all five came out within three dollars of each other. |
| *RB composite (doc 191: target share, 13+ games, NFL rounds 1–3 — +12.2 pts per signal, p=0.0008)* | **A back carrying all three signals that measure** — a real share of his team's targets, 13+ games last year, drafted in the NFL's first three rounds. Each one is worth about twelve points. |
| *bottom quartile (doc 197: +0.79 pts of beat per point of share, p<0.0001, survives the games control)* | **How much of his team's season he was actually on the field for.** Red means he was not out there — the strongest receiver warning we have. |
| *mean pairwise r 0.81 … −0.244, p=0.0009* | The six rankers mostly agree with each other, and the players they argue about have **finished worse**, not better. |
| *±(0.111 × 60 + 5.4) picks* | give or take twelve picks |

Both grid keys also restructured under three plain headings — **marks that come from a
measurement** · **marks that are somebody's opinion** · **two numbers that override what is beside
them** — so the reader can tell at a glance which kind of thing he is looking at.

## 4. THE HONEST LIMIT

**This guard checks vocabulary, not clarity.** A sentence can pass every pattern above and still be
a bad sentence. What it does is remove the *systematic* failure — the one that came from a rule
conflict rather than from carelessness — so what is left is ordinary editing, which he can catch
and I can fix. **It will not stop me writing a clumsy line. It will stop me writing a doc line on
his draft board.**

*Files: `check_plain.py` (new, pinned) · `sept5_after.bat` step 12 of 13 · `make_gridboard.py`,
`make_tiers.py`, `make_board.py` keys rewritten · `check_kit.py` re-pinned for all of them.*
