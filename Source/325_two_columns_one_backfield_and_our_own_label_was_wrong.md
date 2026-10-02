# 325 — Two columns, one backfield, and our own label was wrong

*16 September 2026. Matt forwarded The Fantasy Footballers' Week 2 waiver piece, a day after Justin
Boone's. Both describe the same 49ers backfield, both in a way our data appeared to contradict, and
checking who was right found the error on our side.*

---

## 0. DO THIS

1. **Nothing in this column is claimable.** Every name in it that is not already on your sheet is
   **rostered in our league**: Coker, Allgeier, Marks, Mayer, Deebo. It reduces to Black, Vele,
   Douglas and Schultz, all of which were already in play.
2. **Schultz now has both shows and our own number.** Still first.
3. **A sentence on your week sheet was wrong and is fixed.** It said "He touched the ball N times";
   the number is **carries plus targets**. Re-run `py wire.py` and it reads correctly.
4. **Shough is your drop on two claims and both shows just called him a top add.** Our number says
   the spot is worth about 2.5 and he is a coin flip with Daniel Jones. Fine to drop him, but he
   will not clear.
5. **A number that must not be quoted: "touches" on any of our pages.** It is opportunities.

---

## 1. THE CLAIM I ALMOST CALLED WRONG

Fantasy Footballers: *"Kaelon Black... surprisingly logged 14 carries in the season opener —
out-touching Christian McCaffrey."* Boone, the day before: *"CMC poured in 88 scrimmage yards on
15 touches, Black wasn't far behind with 70 yards on 16 chances."*

Our own week-1 rows:

| | snaps | carries | targets | our `touches` column |
|---|---|---|---|---|
| Christian McCaffrey | 55% | 10 | **8** | **18** |
| Kaelon Black | 43% | **14** | 1 | 15 |

**Two independent shows say Black out-touched him; our column says McCaffrey led 18 to 15. I was
drafting a paragraph about two analysts making the same error.**

**They are not wrong. We are.** `build_form.py` line 156: `'touches': int(tg + ca)`. That is
**targets plus carries** — OPPORTUNITIES. True touches are carries plus RECEPTIONS, and McCaffrey
did not catch all eight. On the shows' definition Black very likely did out-touch him, exactly as
both said, **and our data cannot adjudicate it because we do not store receptions.**

**What survives every definition, and is the decision-relevant fact neither column states:**
**McCaffrey drew 8 targets and Black drew 1.** The carries are split; the passing down is not. In
half-PPR that is the difference between a flex and a handcuff, and it is why Black prices where he
does on our page.

---

## 2. THE DEFECT, AND WHAT IT DOES AND DOES NOT TOUCH

The week sheet has been printing, since doc 314 shipped:

> *"He touched the ball **N times** in his last game, and that is the number the rest of the league
> files on."*

**For a pass-catcher that number is always too high.** Jalen Coker's week 1 is 9 targets and 8
catches; the sheet would have said he touched the ball nine times. Michael Mayer, 7 targets and
fewer catches, same shape. It is only exact for a pure runner.

**DOC 314 IS UNAFFECTED, and this is the part worth being precise about.** The bands were FITTED on
this same column and are APPLIED to this same column, so under 5 / 5–9 / 10–14 / 15+ are opportunity
bands throughout and the measured relationship (r=+0.296, p=0.00005, n=403) stands exactly as
published. **The code comment was right all along** — it says "targets plus carries in his LAST
COMPLETED GAME." **Only the printed sentence was wrong**, and §0.1's scope rule is that a rendered
page carries the plain number and the plain words have to be true.

Fixed: **"He had N carries and targets in his last game."** `sheet_engine.py` 94,691 bytes,
re-pinned. Ledger row 61.

---

## 3. WHAT THE COLUMN OFFERS US: NOTHING NEW

**Free here:** Black (15.5% owned), Vele (13.1%), Douglas (15.6%), Washington (7.7%),
Schultz (19.6%).
**Rostered here, so not claimable whatever the show says:** **Jalen Coker** (their consensus number
one, 9 targets, 29.8 half-PPR), **Tyler Allgeier** (17 carries, ARI), **Woody Marks**,
**Michael Mayer**, **Deebo Samuel Sr.**

**And a dated-source conflict on their top name.** Boone's column, one day earlier, lists
**"Jalen Coker (ankle)"** under key injuries. The Footballers name him the consensus top claim and
do not mention it. `[SOURCED: Yahoo Fantasy Forecast, Boone, 15 Sep 2026 11:14 EDT; Fantasy
Footballers Week 2 waiver piece, undated in what was forwarded]` **Unactionable here because he is
rostered, but it is the B7 pattern: the later-read source was the one missing the injury.**

---

## 4. SHOUGH, BECAUSE HE IS YOUR DROP ON TWO CLAIMS

Both shows now name him a top quarterback target. Our side: week 1 was **4 rushes, 0.8 half-PPR**;
doc 259 puts **Daniel Jones at 21.87 a game against Shough's 21.92**, a gap of 0.05; doc 317's
ladder prices the drop at **2.5**.

**So dropping him is defensible and cheap. What is worth knowing is that he will not clear.** Two
shows naming a man is exactly the condition under which someone else files, and §4.32's term 5 cuts
the other way on a DROP: losing a claim usually costs a delay, but dropping a wanted man costs the
man. If there is any chance you want a second quarterback in three weeks, spend a different seat.

---

## 5. THE RULE, AND IT IS THE SECOND HALF OF DOC 324'S

Doc 324 said an outside column is a source and gets the same check as a hunch. **This is the
mirror: when a source disagrees with our own data twice, in the same direction, from two
independent authors, the next thing to check is our own column definition.** Two shows agreeing is
weak evidence about football and strong evidence about vocabulary.
