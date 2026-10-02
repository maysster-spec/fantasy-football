# 420 — "not priced" read as free, and the ladder took both defences

**24 Sept 2026.** Matt, on the page as shipped:

> *"The call makes no sense, i should drop both defenses and a kicker if i do that math? What is
> good about the Jet's d/st? **Who am i replacing my kicker with?** Those points don't realistically
> add up is what i'm saying. If i drop my kicker i'm not going to gain 1.8 points, lol."*

**Three separate defects, and he was right before two of them were even live.**

---

## 1. THE DROP TABLE LISTED HIS KICKER AND BOTH DEFENCES WITH NO PRICE

The table under THE CALL lists **every man he owns**, sorted by what dropping him costs. His two
defences and his only kicker sat at the bottom of it reading **`not priced`**.

A drop table in which three men have no price is a drop table that nominates those three.

**Why they had no price:** §4.8 and §4.9 keep K and D/ST off the wire on purpose, so the
replacement-aware cost had no free row to price against. An earlier session correctly rejected
`drop_costs()`'s raw answer — it said dropping the kicker costs 118.7, when the real answer is that
you add a kicker — and printed `not priced` instead. **Rejecting a wrong number is not the same as
supplying a right one**, and the blank read as free.

**The fix, and the D/ST half is measured.** §2 already carries it: under this league's bands a D/ST
week is 5.46 with sd 6.28, and **replacement, D/ST12's season average, is 5.99 a week** (n=2,576,
five seasons, doc 265). So a streamed defence at 6.0 is the replacement, and the table now prices
both of his against it:

| | pts/wk | costs to drop |
|---|---|---|
| Chiefs D/ST | 5.7 | **−0.3**, annotated *the replacement is better: this is an upgrade, not a cost* |
| Bengals D/ST | 6.1 | 0.8 |

**Both of his defences are at or below the level he can stream off the wire.** That is a real
finding the page had been hiding behind a blank.

**NO SUCH NUMBER EXISTS FOR KICKERS and one was not invented** (§0.2). That row now says what is
true: *"you must put another kicker in this slot the same week, and this page does not price
kickers."* Which is the direct answer to *"who am I replacing my kicker with?"* — nobody, on this
page, and the page now admits it instead of printing a blank that looks like zero.

## 2. THEN THE LADDER TOOK BOTH DEFENCES, EXACTLY AS HE PREDICTED

The moment D/ST had a price, both defences became cheap drops and **THE CALL offered both** — which
empties the D/ST starting slot. The second one does not cost 0.8. It costs the whole slot, because
there is no third defence behind it.

**Each drop is priced ONE AT A TIME against the full roster.** That is right for any single move and
wrong for a set of them, and nothing was checking the set. **§0.1(h) rule 4 has demanded "the
fifteen after the move" on every take since doc 378. It was a sentence in a reply and never a line
of code.** It is a line of code now:

```
_floor = {'QB': 1, 'RB': 2, 'WR': 2, 'TE': 1, 'D/ST': 1, 'K': 1}
```
plus RB+WR+TE keeping **6** bodies between them, not 5, because of the FLEX.

Verified on his own roster, after all three recommended moves:
`RB 5 · WR 4 · TE 1 · QB 1 · D/ST 1 · K 1` — **nothing short of a starter**, RB+WR+TE at 10.
The third drop moved off Bengals D/ST onto Devaughn Vele on its own.

## 3. A MAN WAS BEING REPLACED BY HIMSELF

The table printed **"Tre Tucker — replaced by Tre Tucker at 9.3"**. He is on `MY_ROSTER.csv` as owned
AND in `WIRE_20260923.csv` as free, because the two files are written at different moments and the
wire copy on disk can be a day old. He is the only such overlap today.

Dropping a man never makes him available to replace himself, **and a roster-mate is not a
replacement either** — he is already inside the lineup the cost is measured against, so using him
credits one body twice. The replacement lookup now excludes anyone on the roster, keyed on name AND
position (§3: never less). Vele's cost moved 2.9 → 3.5 and Tucker's 4.5 → 5.7 once the phantom
replacement was removed.

## 4. AND THE 03:30 LINE ASKED HIM TO BE AWAKE

> *"i don't get it, I'm not waking up at 3:30 am to check waivers."*

The line stated a fact about ESPN's clock in the shape of an instruction. Rewritten to say what to
DO, with the measured settlement times moved into the collapsed provenance box where provenance
belongs:

> **Your claims run Thursday, before dawn, while you are asleep.** Nothing here asks you to be up
> for it: place claims Wednesday night, and on Thursday whenever you wake, run `ff.bat` before you
> act on this page — it was built before the run, so the roster and the pool on it are last
> night's.

## OPEN

- **[OPEN] The kicker replacement level is NOT ESTABLISHED and it is measurable.** §2 carries this
  league's kicker scoring (PAT 1 · miss −1 · 0–39 = 3 · 40–49 = 4 · 50+ = 5) and five seasons of
  history exist, so K12's season average can be computed exactly as D/ST12's was in doc 265. Until
  it is, the kicker row stays honest rather than numbered. **NOT YET RUN.**
- **[OPEN]** `WIRE_*.csv` on disk can disagree with `MY_ROSTER.csv` about who is owned. Today it was
  one man and the guard above absorbs it, but the two files are written in the same run and should
  not be able to drift. **NOT YET RUN.**
