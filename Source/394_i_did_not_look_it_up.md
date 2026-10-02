# 394. He gave me an example and asked me to look up the rules. I never looked them up.

**22 Sept 2026. Matt:** *"I don't honestly know the exact rules and I don't pretend to know all the
details. I'm just going off what I've seen previously. I don't know all the conditions. Instead I
thought I could give you an example and from there you could simply look up details from the
documentation on ESPN and league settings I've provided. Is that not the case? Did you corroborate
everything? I don't want to hear we got it confused again and then I'm updating project directive
v100.18."*

**The answer was no, and the churn he is complaining about is entirely mine.** Across v9.14 to v9.18
I treated his example as a claim to install, then as a claim to overturn, then as a claim to
reinstate, and shipped a version each time. **He was never asserting the rule. He was handing me a
pointer to the documentation.**

---

## 1. THREE METHOD FAILURES, NAMED, BECAUSE EACH ONE PUT SOMETHING WRONG IN A FILE

**(a) I compared a football page to a WOMEN'S BASKETBALL page and published "the vendor contradicts
itself" twice.** The page I cited as the contradiction, *How does the Injured Reserve / Injury List
impact Waivers?*, carries the breadcrumb **ESPN Fan Support > Fantasy Women's Basketball > Managing
Your Team**. Different sport, different rules: it says only an **IR/IL tag** qualifies, where
football also accepts **Out**. There is no contradiction. **Check the breadcrumb for the sport before
quoting any support page.**

**(b) I put quotation marks around a summariser's output.** `WebFetch` runs a small model over a page
and returns its rendering, not the page. I wrote those renderings into the directive as verbatim ESPN
quotes. Read back with the browser, the football quote happened to be accurate, **which was luck, not
method** (§3: never state something not present in a source). **Read support pages with the browser
and use the page text.**

**(c) I grepped the settings file instead of reading it.** `2026_League_Settings.txt` is 5,756 bytes.
I searched it for *waiver*, *injured*, *reserve* and *IR*, which misses **`Auto Reactivate: No`** and
**`Lineup Protection: Off`**, both of which look IR-relevant, and misses `Votes Required to Veto
Trade: 4`. **A file this small gets read, not searched.** This is §0.5(c)5's missing-row check in a
new place: the check looks for rows that should be on a page, and nothing looked for lines that
should have been read.

---

## 2. THE RULES, VERBATIM, FROM ESPN'S FOOTBALL PAGES

**ESPN Fan Support > Fantasy Football > Managing Your Team, *Players on Injured Reserve (IR)*:**

> *"In ESPN Fantasy Football, players with either the Out (O) or Injured/Reserve (IR) status may be
> placed into the IR slot"*
> *"Suspended players (SSPD) are NOT eligible for IR on FFL."*
> *"If a player in the IR slot has their status updated from OUT or IR to QUESTIONABLE or DOUBTFUL,
> the user's roster is NOT invalid. Those players can remain in that IR slot, and the user can make
> claims/add players, adjust their lineups as they wish."*
> *"If a player goes from OUT to no longer having an injury designation, the user's roster becomes
> INVALID, and they must update it accordingly."*

**ESPN Fan Support > Fantasy Football > Trades and Waivers, *Reasons Why a Waiver Pickup May Not
Process*:**

> *"Teams are not allowed to make claims if they have an ineligible player in the IR slot. If you
> have a healthy player in IR, the claim will not process."*

---

## 3. WHAT THAT OVERTURNS, AND ALL FOUR WERE LIVE RULES

| what the files said | what ESPN says |
|---|---|
| *"ruled Out then upgraded in-week flips any day and nothing on a schedule protects you"* | **an upgrade to Questionable or Doubtful breaks nothing.** He keeps the seat, keeps claiming, keeps setting lineups |
| *"the 19.5% downgraded-to-Questionable cell is the quiet failure, seat gone and nothing gained"* | **not a failure at all.** It is the safe case, and it is the most common one |
| §6, live since v5.5: *"PUP/NFI/suspension stashes cost nothing"* | **SSPD is never IR-eligible in football.** PUP and NFI are unaddressed, so NOT ESTABLISHED |
| *"the two ESPN pages contradict each other"* | **they do not.** See §1(a) |

**And it answers the *"which designations does this league's slot accept"* item that had sat
UNVERIFIED since doc 390: Out (O) and IR, and nothing else.**

**THE MECHANIC, FINALLY.** Park an Out or IR man. Keep the free seat. Ride any downgrade to
Questionable or Doubtful at no cost. **The only event that costs anything is the designation
disappearing entirely**, which invalidates the roster and freezes lineup moves until someone is cut.
That is Matt's *"my players are locked... not until I drop someone to fit the limit"*, and it is far
narrower than anything in v9.15 to v9.18. **Clear the slot before entering claims**, because a
healthy man sitting in it blocks them outright.

---

## 4. STILL NOT ESTABLISHED, AND I LOOKED

- **`Auto Reactivate: No`** in his settings. No ESPN Fantasy Football help page documents it; a web
  search returned nothing on point. **Not guessed.** It plausibly governs whether a healthy man is
  pulled out of the slot automatically, which would matter, so it is worth one look at the league
  settings screen.
- **Whether an IR man counts against a position cap.** Unaddressed by every page found.
- **Whether time on IR breaks *"rostered all season"*** for keeper eligibility (§2.1(a)). Unaddressed.

## 5. WHAT STANDS UNTOUCHED

The waiver-history measurement (doc 393 §4): **a claim naming a drop, 884 executed and 0 roster-limit
failures; naming none, 371 and 24.** His own league, five seasons, nothing to do with ESPN's docs.
And `STATUS_LOG.csv` still earns its place, for a narrower reason: **the event to watch is the
designation vanishing, not a downgrade.**

**Sources, read with the browser as page text:**
[Players on Injured Reserve (IR)](https://support.espn.com/hc/en-us/articles/115003849911-Players-on-Injured-Reserve-IR) ·
[Reasons Why a Waiver Pickup May Not Process](https://support.espn.com/hc/en-us/articles/360029528571-Reasons-Why-a-Waiver-Pickup-May-Not-Process) ·
[the Women's Basketball page that is NOT football](https://support.espn.com/hc/en-us/articles/4669672308116-How-does-the-Injured-Reserve-IR-slot-impact-Waiver-Claims-and-Free-Agents)
