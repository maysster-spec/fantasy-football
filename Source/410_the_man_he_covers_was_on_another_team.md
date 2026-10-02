# 410 — "The man he covers" was on another team

*24 Sept 2026. Matt quoted the page back: "Every pickup below costs a drop. The cheapest man you
own is Jonah Coleman, at 0.0. And it holds only while Ashton Jeanty stays healthy, because that is
the man he covers." — "this was supposed to be fixed already".*

## DEFECT 1 — NO TEAM CHECK, AT ALL
`sheet_engine.py` line 1814 selected every rostered player at the same POSITION with a higher rate
and took the top one:

    ahead_of_fp = sorted((pl for pl in roster if pl.get('pos') == fp.get('pos')
                          and pl.get('wk', 0) > fp.get('wk', 0)), ...)

**Coleman is Denver. Jeanty is Las Vegas.** He covers nothing of Jeanty's. The man actually ahead
of him is J.K. Dobbins, also Denver, who is QUESTIONABLE — which makes that seat worth MORE, the
opposite of what the page said. This is §8.6 in code: a bench back earns his spot by the job he
would INHERIT, and you cannot inherit a job on another team. **Fixed: same `tm` now required.**

## DEFECT 2 — THE PAGE CONTRADICTED ITSELF ON ONE SCREEN
Doc 407 added a block showing Coleman at 6.7 a game this season. The drop-cost line two screens
down still said 0.0. **Same page, same man, two numbers.** §3 says when a finding invalidates a
metric you enumerate every downstream use; I fixed the display in one place and stopped. The cost
line now carries the season inline where the decision is made:

> The cheapest man you own is Jonah Coleman, at 0.0, **but that is a preseason number and this
> season disagrees.** He has averaged **6.7** over 2 games. Price the drop off that, not off the 0.0.

## A TRAP WORTH RECORDING
The first attempt passed the season data into `render()` as a kwarg named `season`, which shadowed
the module's own `season()` function and killed the page at `base = season(roster)`. Caught because
the whole page is rendered before every commit, not just the changed block. **Grep before naming a
parameter in that function.** It happened again the same day with `news` (doc 412).
