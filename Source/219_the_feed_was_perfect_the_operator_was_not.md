# 219 — The feed was perfect, the board stopped, and the roster broke the doctrine twice

**2026-09-07, 17:45 ET. Keeper lock T−75m.** Matt: *"check the logs please. I just ran a mock but
the draft board never completed, even after refresh"* and *"there could be other data anomalies.
I'm not sure it got to D/ST."*

---

## 0. ACTIONABLE

1. **It DID get to D/ST and K.** Matt took **Steelers D/ST at 152** and **Harrison Butker at 161**.
   Both are in the captured feed. That worry is closed.
2. **The feed is perfect: 179 picks, overall 1 → 179, ZERO gaps.** The bridge is not the problem.
3. **The board's last page was pick 159, written 186 ms after the feed's last pick landed. No error
   was logged.** Cause NOT proven — see §2. It does not reproduce.
4. **THE REAL FINDING IS THE ROSTER: three QBs and three TEs.** Both were picks the board could not
   have offered. §6's doctrine was overridden twice, live, in rehearsal.
5. **Nothing to change before 8:00.** Every fix here is a reading, not a file.

---

## 1. THE FEED — CLEAN, AND THIS IS THE PART THAT MATTERS TONIGHT

```
session_started 17:14:14   updated 17:21:17   picks 179
overall range 1..179   unique 179   MISSING: none
```
**179 of 179, no duplicates, no holes.** Twelve teams at 15 picks each (one short — Matt's 15th
never came). **The bridge captured a complete draft.** Whatever stopped the page did not lose data.

**One thing that LOOKS like an anomaly and is not:** every pick carries a `round` field that is
wrong — pick 1 says "round 2", pick 179 says "round 9". **That is doc 210's known misnomer: token 4
of `SELECTED <team> <pid> <n>` is the ROSTER SLOT, not the round.** Nothing reads it. Do not chase
it. *(Renaming it is on the post-draft list and has been since doc 210.)*

## 2. WHY THE PAGE STOPPED — WHAT I CAN PROVE, AND WHAT I CANNOT

**Proven:**
- Last page written: `<title>JUG board - pick 159</title>`, `updated 17:21:18`, 43,944 bytes — a
  complete, healthy board, not a half-write.
- The feed's final write was **17:21:17.958**. The page landed **186 ms later**.
- **`feed_evidence\` holds NO `pollfail` from this session.** The poll loop writes one on any
  exception. It never threw.
- **It does not reproduce.** I replayed the captured feed through the production `render()` and
  `render_streamer()` for **all 180 states, including 152 and 161: zero failures.**

**Not proven — and I am not going to dress a guess as a diagnosis (§0.2).** The consistent story is
that the mock auto-completed its final rounds in a burst — picks 170–179 are all K and D/ST, taken
by teams in scrambled order, which is the signature of clocks expiring — and the board wrote the
state it had read and then stopped polling. Whether the process was closed, or the window went away
with the mock, I cannot tell from the artifacts. **The console output is the one log that would have
answered it and it is gone with the window.**

**Why a refresh could not help:** refreshing re-reads the file the board writes. If the board is not
writing, every refresh shows the same page. **A stale page is not a stuck browser.**

**What this means for tonight, and it is the honest bound:** this happened in a burst of ~20 picks
in seconds. **A live 12-human draft at 60 seconds a pick cannot produce that**, and the board renders
in 0.4 s while waiting. If the room ever does blitz — several autodrafts in a row — expect the board
to lag and then catch up; that is not a fault. **If the header ever stops advancing while ESPN moves
on, the answer is to restart `py live_draft.py --bridge`. It re-reads every pick and remembers
nothing, so restarting is always safe.**

## 3. THE THING THAT ACTUALLY WENT WRONG, AND IT IS NOT THE SOFTWARE

Final roster: **JSN · Walker · Kyren · Lamar · Jadarian Price · LaPorta · Dowdle · Stafford · Bo Nix
· Andrews · Kincaid · Deebo · Steelers · Butker.**

**Three quarterbacks and three tight ends.** §6, in Matt's own doctrine: *"Never three QBs. Never
three TEs."* The engine encodes it — `CAPS = {'QB':2, 'RB':6, 'WR':6, 'TE':2}`, tighter than the
league's own QB3/TE3 limit, on purpose.

**Neither pick was on the board when he made it. I re-ran both turns:**

| turn | what the board offered (top rows) | what he took |
|---|---|---|
| **104** | Goedert TE *(free)* · Matthew Golden WR *(free)* · Andrews · Ferguson · Kincaid · Likely | **Bo Nix — QB3** |
| **128** | Xavier Worthy WR *(free)* · Jordan Mason RB · Deebo · Spears · Concepcion · Tank Dell | **Dalton Kincaid — TE3** |

**The cap means a third QB and a third TE cannot appear as rows at all** — so these were not close
calls the engine lost, they were selections made past the list. At 104 the doctrine and §4.18's
draft-night rule agree with each other for once: he already had two quarterbacks, so QB2 was
answered, and the row marked `free` was a tight end.

**This is not a criticism of a mock, which is for exactly this.** It is the one lesson worth
carrying into a room with money in it: **the board cannot stop him, it can only be right.** Both
overrides cost real starters — Matthew Golden and Xavier Worthy were the `free` rows.

**And per §0.5(b), the counter-case stated once:** a mock is where you test things, and if he was
deliberately probing what happens when he ignores the tool, that is a legitimate use of a rehearsal
and there is nothing to fix. **He is the one who knows which it was.**

## 4. TWO SMALLER READS

- **The mock was 15 rounds (180 picks); his league is 14 selections** with the keeper charged to
  round 15 (§2.1b). So the tool's 14-round configuration was RIGHT for tonight and wrong for that
  mock — the region past pick 168 that the mock reached is not a state tonight produces the same
  way, because tonight ESPN puts the twelve keepers at 169–180 and the tool filters them.
- **Steelers at 152 is a defensible pick and doc 212 predicted its window.** Pittsburgh is opening
  rank **3**; doc 212 expected them gone around pick 110 and they lasted. The Jaguars (rank 2) were
  the fallback for exactly the case where Pittsburgh does not last. **The amber ranking did its
  job.**

## 5. OPEN

- **Why the loop stopped is UNRESOLVED and stays on the list.** The fix that would answer it is a
  one-line heartbeat to a log file so the next occurrence has an artifact instead of a memory.
  Post-draft, not tonight.
- `bridge_server.py`'s `round` field should be renamed `slot` (doc 210, still open).
- Everything on docs 216 §4, 217 §4 and 218 §5 still stands.
