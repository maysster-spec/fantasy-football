# 408 — A snap share is not a cause, and there was no injury feed at all

*24 Sept 2026. Matt: "Dowdle, 26%, yes, he got injured week 2, lol. Somehow you still only see a
very narrow picture of what i see."*

## WHAT I GOT WRONG
Rico Dowdle went 58% of snaps in week 1 to 26% in week 2 while Jaylen Warren went 37% to 71%. I
read a handover, named Warren as the man who took the job, and recommended dropping Dowdle over
Xavier Worthy. **He was hurt.** The snap share is an injury, not a demotion.

## WHY IT IS A METHOD FAILURE AND NOT BAD LUCK
**The answer was in a file I had already printed.** `MY_ROSTER.csv` carries a `status` column. It
read `QUESTIONABLE` on Dowdle's own row, in a table I rendered two tool calls earlier. I checked
the INCUMBENT's status (Warren) and never the CANDIDATE's. That is the take contract's line 3
obeyed against the wrong object, which is §0.5(a2) inside a filter.

## THE REAL GAP UNDERNEATH
What this project could see about a roster: a preseason projection, two weeks of snap and target
counts, and a one-word ESPN status. **No injury events. No news.** `cards_2026.csv`, the only news
file, was built 11 Sept and contains no row for anybody on his roster. With that input set,
"Warren took the job" was never a finding. It was a guess with a number beside it.

## THE RULES (now in `METHOD_TRAPS.md`)
- Never explain a usage change without first quoting the player's OWN status.
- A status other than ACTIVE on the candidate is a STOP, not a footnote.
- When the inputs cannot separate injury from demotion, say BLOCKED and name the missing input.
- Matt sees the games; this project sees a CSV. When his account contradicts the table, the table
  is wrong about WHY even when it is right about WHAT (§0.6 rule 4).

**The missing input is built: doc 412.**
