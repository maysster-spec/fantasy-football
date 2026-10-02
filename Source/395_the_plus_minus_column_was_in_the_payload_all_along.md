# 395. The plus-minus column was in the payload all along, and the Thursday run is why it matters.

**23 Sept 2026. Matt, with a screenshot of ESPN's tight-end list, the `+/-` column circled:**
*"the plus/minus column is what i wanted you to note in terms of likeliness i'll get a waiver
pickup"*, then: *"is this something you can pull from ESPN. This is the benefit of having Thursday
waivers, we can see what other leagues are doing that have Tues night waivers."*

**Yes, and the second half is the better idea.**

---

## 1. THE FIELD EXISTS, AND WE HAVE BEEN THROWING IT AWAY EVERY RUN

`wire.py` read exactly one thing out of ESPN's `ownership` object, `percentOwned`, at two call
sites. **Confirmed live on ESPN's public endpoint at 07:19 ET, 23 Sept**, the object is:

```json
"ownership": { "activityLevel": null, "auctionValueAverage": 0.0,
  "auctionValueAverageChange": 0.0, "averageDraftPosition": 169.89,
  "averageDraftPositionPercentChange": -0.01, "date": 1790152222218,
  "leagueType": 0, "percentChange": -0.01,
  "percentOwned": 0.06, "percentStarted": 0.01 }
```

`percentChange` **is** the `+/-` column on his screen. `percentStarted` is a second signal we never
had: rostered and started are different questions. And `date` stamps when those two last refreshed.

**The pool ENTRY, not the player, carries one more:** `waiverProcessDate`. That is ESPN's own answer
to the clock §2 has been deriving as "placed plus two days". Read it, do not compute it.

*(The endpoint is blocked from the cloud container by egress policy; it was read through the browser
on Matt's machine. The sample came from `leaguedefaults/3`, so its `waiverProcessDate` of Fri 25
Sept 03:00 ET is the DEFAULT league's schedule, not his. Whether his league's payload carries his
own date is answered by the next `ff.bat` run, not by me.)*

---

## 2. WHY THE THURSDAY RUN TURNS THIS FROM A SIGNAL INTO AN EDGE, WHICH IS HIS POINT AND NOT MINE

I read the `+/-` as a demand signal, which it is. **Matt read it as a RESOLVED one, which is
sharper.** Most ESPN leagues clear waivers Tuesday night. His clears Thursday. So the number he sees
before committing is **the aggregate outcome of everyone else's waiver run**, not a forecast of it.

**And it is timestamped, which makes the window checkable rather than assumed.** The live
`ownership.date` read **Wed 23 Sept 04:30 ET**, so the figures roll over in the small hours. His
scheduler already runs `ff.bat` daily at 07:30, so **a Thursday 07:30 pull lands on figures
refreshed that morning**, after Tuesday-night and Wednesday processing everywhere else, and before
his own claims settle. Nothing new needs scheduling. The data just has to stop being discarded.

**On his screen this morning:** Schultz **43.6% rostered, +22.1**. Gadsden 7.5, +5.6. Waller 6.2,
+3.4. One of those is being taken across the format right now and two are not.

---

## 3. WHAT SHIPPED

`wire.py`: `own_chg`, `own_start`, `own_asof` and `clears` on both the priced WIRE rows and the
off-board `FREE_UNRANKED` rows. The WIRE writer takes its columns from the row keys so it picked
them up; **`FREE_UNRANKED` has an explicit `fieldnames` list, so a new key without a new column
would have been written nowhere and said nothing** (§3's silent-skip trap), and that list was
updated in the same edit.

**Never defaulted to 0.0.** A missing or unparseable field writes **blank**, because "ESPN says
0.0" and "ESPN did not say" are different answers, and `owned_pct` learned that the expensive way in
doc 292. **Ten negative controls run against the shipped helpers** (no `ownership` key, `ownership`
None, field absent, field None, field a string, `date` None, `date` nonsense, `date` out of range,
no `waiverProcessDate`, waiver date None): all ten blank, and a genuine 0.0 still prints as 0.0.
`check_kit.py` re-pinned, old pin shown failing first.

## 4. OPEN

- **[OPEN], one run away:** whether his league's payload carries HIS `waiverProcessDate`. If it
  does, §2's D+2 table stops being arithmetic and becomes a read.
- **[NOT YET RUN]:** whether `own_chg` predicts anything about whether HE lands a claim, against his
  own five seasons of waiver history. The screen is a demand signal; that it beats his waiver
  priority is a claim nobody has tested, and it should not be quoted as a rule until it is.
- **[OPEN]:** ESPN's claim-ordering mechanic, whether winning claim 1 drops his priority before
  claim 2 is processed. That decides how he ranks Schultz against the Bengals defence. I started
  reading ESPN's Waivers Overview and have not finished it.
