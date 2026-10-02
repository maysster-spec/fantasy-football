# 152 — Homer bias beyond Buffalo. One result survives, and it is not one of the three he named.

**2026-09-03.** Matt: *"Beyond the Buffalo Bills homers we already discussed, what about the other
known teams in my league? Herman Allen for one is a Washington Commanders fan. Others like myself
are Carolina Panthers homies."*

`[TESTED, n=680 true selections 2021–2025, 27 testable manager–team pairs]`

**BASELINE — state it every time: `reach = preseason ADP − actual pick`. POSITIVE = took him
EARLIER than the market.** Preseason ADP only, from the sanctioned registry (§1.1); keepers
excluded (§4.7). **A manager is compared against his own other picks**, because a manager who
reaches on everybody is not a homer, he is just aggressive. Method is `buf_bias.py`'s, generalised
from one team to all of them, so the Bills number reproduces as a control.

## THE CORRECTION THAT DECIDES THIS, STATED BEFORE THE NUMBERS

27 pairs cleared the n≥4 bar. **At p<0.05 you expect one by chance.** Everything below carries a
Benjamini-Hochberg false-discovery value; a raw p under 0.05 that does not survive it is noise
wearing a number. This is §4.21/§4.24's clustering lesson in its multiple-comparisons form, and it
is the fourth time this project has had to apply it.

| manager | tm | n | his reach on them | his own other picks | diff | p | BH |
|---|---|---|---|---|---|---|---|
| Lobsinger | MIA | 5 | +41.7 | +1.5 | **+40.2** | 0.211 | 0.475 |
| **Rychlicki** | BUF | 5 | +19.9 | −2.9 | **+22.8** | 0.021 | 0.139 |
| **herman allen** | **WAS** | 6 | +26.8 | +6.0 | **+20.8** | 0.149 | 0.404 |
| **Rychlicki** | **CHI** | 5 | +14.4 | −2.3 | **+16.7** | **0.003** | **0.040 — SURVIVES** |
| David Snyder | BUF | 6 | +20.1 | +6.8 | +13.3 | 0.244 | 0.508 |
| Brown/Collins | MIA | 4 | +17.5 | +7.3 | +10.2 | 0.395 | 0.666 |
| R Taylor | KC | 5 | +6.4 | −0.8 | +7.2 | 0.336 | 0.648 |
| Matt Mays | CHI | 4 | +1.7 | +0.0 | +1.7 | 0.868 | 0.938 |

## THE THREE ANSWERS

**1. Rychlicki (POT, slot 10) reaches on Chicago by 16.7 picks and it is the only result that
survives correction.** He does not reach in general — his other picks run −2.3. Nobody suggested
him and no story predicted it, which is the good kind of finding and also the kind most likely to
be a fluke; it is one result out of 27 and it is n=5.

**2. herman allen and Washington is the right shape and is NOT resolved.** +20.8 picks early on
six players, third-largest effect in the table, raw p=0.149. Matt's read of his own league is
directionally supported and statistically unproven. **Do not treat it as a fact at the draft.**

**3. Carolina cannot be tested at all, and that is itself the answer.** Twelve Panthers were
drafted league-wide in five seasons and no manager took four. **Matt's own team is too unpopular
to measure a bias against.** Nothing to correct for at picks 8–137.

## WHAT THIS DOES *NOT* SAY ABOUT §5

**Rychlicki out-reaches Snyder on Bills (+22.8 vs +13.3), and that does not touch §5.** §5's
Snyder finding is about ONE PLAYER — Josh Allen, 4-for-4 at his turn when available, fitted at
q ≈ 0.90 — which is a far sharper claim than team-wide average reach, measured on a different
quantity. Both can be true. What this adds is that **a second manager in the room also pays up
for Bills**, which if anything makes Allen's survival to 17 *shorter*, not longer, and §4.2
already puts it at ≈0.03.

## SHIPPED: NOTHING

**Surfaced, not scored** — the same call as §4.22's badge and for the same reason. §4.12's noise
model is fitted league-wide on n=680; one BH-surviving pair on n=5 does not become a coefficient
four days before a draft. The usable form is a sentence, not a number:

> **If a Bears or a Bills player is one you want and Rychlicki picks before your next turn,
> expect him gone earlier than his ADP says.** Herman allen and Commanders, same direction,
> weaker evidence. Panthers, nothing — nobody else wants them.

Reproduce with `Scripts\homer_bias.py`. Full table in `Source\homer_bias.csv`.
