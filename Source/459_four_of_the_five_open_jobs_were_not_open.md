# 459. FOUR OF THE FIVE OPEN JOBS WERE NOT OPEN

*1 Oct 2026, 02:50 ET. Claude (Cowork). Matt, 1 Oct 02:30: "Tyler Badie? What is the upside, and what is the weekly value?
... a 4th string running back in a RB by committee backfield. This must be some kinda error. Also, as i suspect, high end
backups are undervalued by the model ... wish those somehow could be measured against other priority pickups." 459
reserved by listing `Source\` (458 is the defense doc). No em dashes.*

---

## 0. WHAT TO DO

1. **Badie was an error, and you found the class, not the instance: of the five "open jobs" the sheet priced on 30 Sept,
   one was open.** The wire's doubt lane pairs any ROSTERED back who carries a status with the first FREE back on his team,
   and doc 451's open-job block priced every such pair at the lead-back relief rate (12.1 a game). Coleman never held
   Denver's job (6.5 touches a game to Dobbins' 12.3); Mason never held Minnesota's (Jones 19.7); Etienne holds New
   Orleans' but Kamara inherits it (10 touches to Miller's 7 last game) and Kamara is rostered; Brooks never held
   Carolina's. Achane did hold Miami's (15.3 a game) and Gordon did inherit it (20 touches). The block now asks both
   questions off the form file before pricing, and names the man and the numbers when it says no. Badie, Dallas and
   Miller are off the picks; Gordon is unchanged.
2. **Seats are already measured against the other pickups, in the same list, in the same unit.** A seat enters the picks
   at odds times relief (Keaton Mitchell, row 6 tonight: the job opens about 47% of the time, 8.4 if it does, 4.0 expected),
   next to a screened receiver at odds times hit and an open job at relief times weeks. The ten-row seat table below is
   the full menu; only a seat whose expected clears zero is promoted. What you are seeing as "undervalued" is the flat
   relief rate, and that is measured twice: nothing about the backup predicts his relief scoring (doc 411, 62 absences,
   his best two weeks against relief points rho +0.006) and nothing about the job's size does either (doc 456, 30
   absences, slope minus 0.08 a point). A high-end backup is worth more only through the odds (the starter's fragility,
   which prior-season availability does predict, 4.22) and the weeks, and both are in his price.
3. **The honest remainder: the "high-end backup" you mean may be a different object from what was measured.** Doc 411
   measured the backup's own prior scoring; it did not measure draft capital, nor the two-back committee where the
   backup already has 8 to 10 touches a week (Kamara, Harvey). A man like that is not a seat; he is a part-time starter,
   and the page prices him on his own rate like anyone else. If you have a specific name in mind, give it to me and I
   will say which object he is and what the page does with him.
4. **Nothing to run.** Tomorrow's 07:30 run carries the fix; the week-5 claim for the tight end and the Nacua move stand.

---

## 1. THE FIVE, OFF THE FORM FILE (carries plus targets, 2026 through week 3)

| team | absent man, touches a game | holds the job | inherits it (last game) | the free man | verdict |
|---|---|---|---|---|---|
| MIA | Achane 15.3 (3 g) | Achane | Gordon, 20 | Gordon | open job, priced |
| NO | Etienne 14.3 (3 g, played week 3) | Etienne | Kamara, 10 (rostered) | Miller, 7 | behind Kamara, not priced |
| DEN | Coleman 6.5 (2 g) | Dobbins, 12.3 | | Badie, 3.0 a game | never held it, not priced |
| MIN | Mason 15.0 (1 g) | Jones, 19.7 | | Dallas, 1.7 a game | never held it, not priced |
| CAR | Brooks 6.0 (2 g) | Hubbard, 16.7 | | Trevor Etienne | never held it (and unprojected) |

`sheet_engine.rb_usage()` reads the week-0 aggregate and each back's last game; the open-job block cuts a row when
another back on the team out-touches the absent man over the season, or when the back with the most touches in the last
game is not the free man, and prints the names and the numbers under the picks. `check_page_logic` P3 still requires every
marked man to be named, which these are.

## 2. OPEN, BY NAME

- **Matt's:** a name, if you have one, for the high-end backup the page undervalues; otherwise unchanged from doc 457.
- **Mine, tomorrow:** v9.38 (4.44 to 4.47, and this as an amendment to the open-job rule of doc 451); the rest as doc 457.
