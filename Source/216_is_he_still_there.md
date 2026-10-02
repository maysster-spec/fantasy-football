# 216 — "Is he still there?" — the strip the board was missing, and three darts priced

**2026-09-07, 17:10 ET. Draft T−2h50m.** Matt, after the practice draft: *"i couldn't tell in
either the espn window or in the live draft board if he was available or taken. If available he was
too far down the page."*

---

## 0. ACTIONABLE

1. **`live_draft.py` is 134,716 bytes / `f711550878c6c5f0`.** `check_kit.py` re-pinned. Both
   committed. **`draft_night.bat` runs `check_kit` as its step 1 and gates on it** — so this is
   covered automatically at 7:00.
2. **New on the live board: a "Still on the board?" panel** — 30 names grouped by turn, green if
   available, struck through if gone. It answers one question and no others.
3. **Jayden Daniels played 7 games in 2025.** Matt's injury read is right and it is already the
   board's strongest warning: the 7–9 game band averages **−27 points against price**.
4. **Jordan Mason and Croskey-Merritt are the SAME bet**, not two different ones — both UNSETTLED,
   job worth 154 and 151. **Mike Washington is a different bet: a 247-point job he probably
   doesn't get.**

---

## 1. THE STRIP

The board renders twelve rows ordered by `cost vs #1`. A player Matt is holding for a **later** turn
is invisible until he climbs into those twelve — and by then the question has answered itself.
Nothing on the page, and nothing in ESPN's room at a glance, said whether Luther Burden was gone.

**`render_watch()` shows thirty names in six groups labelled by turn** (17 · 32-41 · 56-65 · 80-89 ·
104-113 · 128-137). Green = still there. Struck through = taken. Groups for turns already past go
dim. **No value, no ordering, no advice** — those belong to the board, and duplicating them here
would invite reading the strip instead of it.

**Design constraints honoured:**
- **Fixed content, fixed height (§7).** The same thirty names every refresh; the page never changes
  shape underneath him. Verified: 6 rows at every pick from 1 to 169.
- **It cannot take the board down.** Every path sits inside one `try`; the failure return is `''`.
  **Negative control run:** an engine object that raises on attribute access returns an empty
  string and no traceback.
- **A missing name is VISIBLE, not silent.** An unmatched name renders a grey `?` — the §0.5(c)5
  defect this same session found on the D/ST page. All thirty were verified against
  `board_v8_fixed.csv` before shipping: **30/30 exact matches, zero `?`**.

**Tested through the production `render()`**, not an equivalent (§0.2 / doc 80): four pick states,
on-clock and waiting. Render cost unchanged — **3.3s on the clock at pick 17, 0.4s waiting** — and
the strip flips correctly when players are taken (Burden, Godwin and Bowers marked gone; Odunze
still green).

## 2. THE THREE LATE DARTS, PRICED — Matt asked, and the flag separates them

From `depth_map.py`, computed on the SOURCE pull (§4.20). `job worth` is ESPN's projection for the
man currently holding the job — the closest thing this project has to a ceiling number.

| dart | ADP | VOR | job flag | gap | **job worth** | 2025 games |
|---|---|---|---|---|---|---|
| Jacory Croskey-Merritt (WAS) | 137.1 | −17.2 | **UNSETTLED** | 7 | **151** | 17 |
| Jordan Mason (MIN) | 140.3 | −24.8 | **UNSETTLED** | 9 | **154** | 16 |
| Mike Washington Jr. (LV) | 162.8 | −107.6 | **LEAD BACK** | 184 | **247** | rookie |

**THE ANSWER IS THE LAST TWO COLUMNS.** Mason and Croskey-Merritt are **the same bet wearing
different jerseys**: an unresolved job worth about 150 points, gap of 7 against 9. Matt's instinct
that Washington's offense might crater does not separate them — **`job worth` already prices the
offense**, and Minnesota's is 154 against Washington's 151. Three points apart.

**Mike Washington is the different one, and not in the direction the 4.33 forty suggests.** His job
is worth **247** — far the best of the three — but it is flagged **LEAD BACK**, which means it
belongs to Ashton Jeanty. He is chasing a much bigger prize with a much smaller chance.

**And §4.20's own test says the flag does not pick the winner** — doc 141, incumbent minus
challenger **+8.2, p=0.604**, point estimate leaning the *opposite* way to intuition. Washington's
depth chart is Croskey-Merritt, Rachaad White and Kaytron Allen at gap 7. **We have no opinion on
who wins it, and neither does anyone else.** Buy the job, never the name.

**`[SOURCED]` with dates:** Croskey-Merritt is Washington's projected lead back, was RB10 in points
per game during the 2025 playoff weeks with two 95-yard games and four touchdowns in the final
month, must improve as a receiver to hold the role, and Washington has the sixth-easiest RB schedule
(Yahoo, **Aug 18 2026**). Mason is positioned ahead of Aaron Jones for roughly 200 carries, is over
**5.0 yards per carry on ~400 career attempts**, went 4.8 with 6 touchdowns last season, and ranked
**10th of 49** qualified backs in production against expectation (Yahoo, **Sep 5 2026**).

**Neither number is a forecast. Both are somebody's case, and §4.13d applies: an analyst call on a
near-tie is a human judgement with no metric behind it.**

## 3. JAYDEN DANIELS — his read is right, and it is already printed

Matt: *"Jayden Daniels is great, but he is thin and puts himself at risk for injury the way he
plays."*

**`games_2025.csv` says Daniels played 7 games.** §4.22(e)'s dose-dependent bands put a 7–9 game
season at a mean of **−27.1 points against price (n=30)**, against −12.6 for a 13+ game season. The
board already draws his `12g` badge in the middle shade.

**And §4.25b says the badge is a real warning on him specifically** — doc 204 stood the signal down
for *established veterans* with three prior seasons on file. Daniels is not one. **The mechanism
Matt names is exactly what availability measures, and it is the strongest downside signal in the
project at −19 points overall.**

He is Boone's 68th and our board's 39th. **The board already fades him for the reason Matt gives.**

## 4. OPEN

- The watch list is hard-coded. If a name on it is no longer relevant post-draft it is dead weight;
  a `--watch` flag is the post-draft version.
- Everything on doc 215 §5 still stands: the `n=6` audit elsewhere, pick 56's single-state margin,
  the pick-8 margin disagreement, the missing `Yahoo_Top_300_as_of_817.csv`, the doc-number
  collisions, age × situation change.
- **New:** a post-draft grade — roster strengths, weaknesses, and where the board was overruled.
  Matt asked for it; it is a post-draft build.

*Sources: [Yahoo, Aug 18 2026](https://sports.yahoo.com/fantasy/article/2026-fantasy-football-jacory-croskey-merritt-among-justin-boones-top-sleeper-picks-at-rb-145609904.html) · [Yahoo, Sep 5 2026](https://sports.yahoo.com/articles/jordan-mason-fantasy-prediction-2026-153000650.html)*
