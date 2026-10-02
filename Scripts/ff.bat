@echo off
REM ==========================================================================
REM  ff.bat -- what every scheduled task runs, and the ONE thing to double-click.
REM
REM  No day-of-week branching: branching is where a bug would live, and two
REM  ESPN calls cost nothing. Whichever shortcut you open, it is current.
REM  One exception (doc 439): ESPN's projection pull runs on the TUE task only, because
REM  each pull writes about 5.6 MB to the drive and ESPN re-projects once a week.
REM
REM      The weekly wire   -- who is available, the stash list, in-doubt, weeks ahead
REM      The week sheet    -- the bar grid and what every free body is worth (doc 273)
REM      Lineup check      -- anyone starting who is out, on bye or questionable
REM      Your to-do page   -- MY_TODO.html, your list plus every link and command (doc 342)
REM      The commands page -- COMMANDS.html, generated from that same list and from the batch
REM                           files themselves, so it cannot go stale the way the hand-written
REM                           one did (it sat eleven days describing draft night). Doc 353.
REM      The kit check     -- are the shipped files the ones they are supposed to be
REM      The page check    -- did any page ship a template, a dead link or a None
REM
REM  17 Sept: Matt asked for one batch file so he is not running the same commands in a row.
REM  THIS FILE ALREADY WAS THAT, so it was EXTENDED rather than duplicated -- a second NAME
REM  for one JOB is doc 146's after_pull.bat defect, and the directive names it as standing.
REM  The two new steps cannot break the two old ones: todo_page touches no network and no
REM  ESPN, and check_kit only reports.
REM
REM  Takes one optional label so the log says WHICH task fired:
REM      ff.bat TUE     ff.bat THU     ff.bat "SUN am"     ff.bat "SUN pm"
REM
REM  Neither script leaves a stale page looking current: if ESPN refuses, the
REM  page itself says so in red. An exit code is not a result.
REM
REM  Run it by hand any time:  "G:\My Drive\_Fantasy\2026\Scripts\ff.bat"
REM  Log of every run:         Scripts\ff_log.txt
REM ==========================================================================
setlocal
cd /d "%~dp0"
set LOG=%~dp0ff_log.txt
set SRC=%~dp0..\Source
set WHO=%~1
if "%WHO%"=="" set WHO=BY HAND
REM doc 380: the pages print WHICH run read ESPN (TUE, THU, SUNam, SUNpm, DAILY, BY HAND)
REM instead of "built by the scheduler", which they said even when you ran this by hand.
set FF_WHO=%WHO%

echo. >> "%LOG%"
echo ======== %WHO% ==== %DATE% %TIME% ============================ >> "%LOG%"

REM The sheet's timestamp BEFORE the run, so the open below can prove it actually changed.
set BEFORE=none
if exist "%SRC%\WEEK_SHEET.html" for %%F in ("%SRC%\WEEK_SHEET.html") do set BEFORE=%%~tF

REM doc 439: the weekly fetches Matt was running by hand. build_form.py writes to a temp file
REM and swaps it in only after its checks pass, so a failed fetch leaves the last good file.
echo --- this season's usage: form and snaps --- >> "%LOG%"
py research\wk1\build_form.py >> "%LOG%" 2>&1
set RCF=%ERRORLEVEL%
if not "%RCF%"=="0" echo *** FORM FILE NOT REBUILT -- the sheet keeps the last good one; read the lines above >> "%LOG%"
py snaps_2026.py >> "%LOG%" 2>&1
set RCS=%ERRORLEVEL%
if not "%RCS%"=="0" echo *** SNAP FILE NOT REBUILT -- read the lines above >> "%LOG%"
REM doc 441: the daily depth chart and the practice report (nflverse, ESPN-sourced), written to Source\depth_daily.csv
REM and Source\practice_2026.csv through a temp file; a failed fetch keeps the last good file and says so.
py research\wk1\build_depth_daily.py >> "%LOG%" 2>&1
set RCD=%ERRORLEVEL%
if not "%RCD%"=="0" echo *** DEPTH CHART NOT REBUILT -- the seat lane keeps the last good file; read the lines above >> "%LOG%"
REM doc 442: the pregame lines (nflverse games.csv) into Source\lines_2026.csv, the D/ST and QB matchup axis;
REM and the seat lane's inherit_2026.csv rebuilt from today's depth chart. Each keeps its last good file on a failure.
py research\wk1\build_lines.py >> "%LOG%" 2>&1
set RCL=%ERRORLEVEL%
if not "%RCL%"=="0" echo *** LINES NOT REBUILT -- the wire falls back to last season's averages; read the lines above >> "%LOG%"
py research\build_inherit.py >> "%LOG%" 2>&1
set RCI=%ERRORLEVEL%
if not "%RCI%"=="0" echo *** INHERIT FILE NOT REBUILT -- the seat lane keeps the last good one; read the lines above >> "%LOG%"
set RCP=skipped
if /i "%WHO%"=="TUE" goto do_proj
REM doc 451 / 454: any run pulls when the newest projection file is more than half a day old (one pull a
REM day at most, on whichever run comes first); the Tuesday task always pulls. proj_due.py exits 0 when
REM the pull is due. After a pull it reports what ESPN moved and moves pulls older than the newest three
REM to _archive\projections (the draft-era pulls stay).
py proj_due.py >> "%LOG%" 2>&1
if not "%ERRORLEVEL%"=="0" goto after_proj
:do_proj
echo --- ESPN projections, the Tuesday task or a pull more than half a day old --- >> "%LOG%"
py Espn_pull_projections.py >> "%LOG%" 2>&1
set RCP=%ERRORLEVEL%
if not "%RCP%"=="0" echo *** PROJECTIONS NOT PULLED -- the sheet keeps the last pull; read the lines above >> "%LOG%"
if "%RCP%"=="0" py proj_due.py --report --prune >> "%LOG%" 2>&1
:after_proj
echo. >> "%LOG%"
echo --- lineup check --- >> "%LOG%"
py lineup.py --html >> "%LOG%" 2>&1
set RC1=%ERRORLEVEL%

echo. >> "%LOG%"
echo --- the injury feed --- >> "%LOG%"
REM doc 412: ESPN's PUBLIC injuries endpoint -> Source\news_2026.csv, which the week sheet
REM prints beside every man in the drop table. It runs BEFORE the wire, because the wire is what
REM builds the sheet. It REFUSES to write a partial league rather than leave a blank where a hurt
REM man should be, so a non-zero here means the sheet is showing older news.
py build_news.py >> "%LOG%" 2>&1
set RC0=%ERRORLEVEL%
if not "%RC0%"=="0" echo *** NEWS FEED DID NOT REFRESH -- the drop table is on older news >> "%LOG%"

echo. >> "%LOG%"
echo --- the wire --- >> "%LOG%"
py wire.py --html >> "%LOG%" 2>&1
set RC2=%ERRORLEVEL%

echo. >> "%LOG%"
echo --- your to-do page --- >> "%LOG%"
py todo_page.py >> "%LOG%" 2>&1
set RC3=%ERRORLEVEL%

echo. >> "%LOG%"
echo --- the open threads --- >> "%LOG%"
REM [doc 435] OPEN_THREADS.md had not been rebuilt since 20 Sept because nothing ran the
REM script. It reads every doc plus matt_todo.txt and claude_todo.txt, renders both lists at
REM the top, and skips its own previous output (it used to re-ingest it, 42 garbage rows).
py research\open_threads.py --quiet >> "%LOG%" 2>&1
set RC9=%ERRORLEVEL%
if not "%RC9%"=="0" echo *** OPEN_THREADS.md NOT REBUILT -- the thread list is stale >> "%LOG%"

echo. >> "%LOG%"
echo --- the copy for the web --- >> "%LOG%"
REM [doc 430] ff.bat CANNOT PUBLISH. Nothing on this PC can push to claude.ai, so the online
REM week sheet was six days stale while every local page was current. This step builds the
REM publish-ready file every run; the upload is the one manual half and Claude does it.
py make_online.py >> "%LOG%" 2>&1
set RC8=%ERRORLEVEL%
if not "%RC8%"=="0" echo *** ONLINE COPY NOT BUILT -- the published page cannot be refreshed >> "%LOG%"

echo. >> "%LOG%"
echo --- the commands page --- >> "%LOG%"
py make_commands.py >> "%LOG%" 2>&1
set RC5=%ERRORLEVEL%
if not "%RC5%"=="0" echo *** COMMANDS PAGE REFUSED TO BUILD -- it names a script that is not on disk >> "%LOG%"

echo. >> "%LOG%"
echo --- the kit check --- >> "%LOG%"
py check_kit.py >> "%LOG%" 2>&1
set RC4=%ERRORLEVEL%
if not "%RC4%"=="0" echo *** CHECK_KIT DISAGREES WITH THE TREE -- read the lines above >> "%LOG%"

REM [doc 448] A local read before it is assigned, found without running the function. The 29 Sept
REM 20:06 run died in wire.py main() that way (wire 1, no wire page, no week sheet) after a unit test
REM had passed on the function alone. Static, standard library, every shipped script.
echo. >> "%LOG%"
echo --- locals read before assignment --- >> "%LOG%"
py check_locals.py >> "%LOG%" 2>&1
set RCLC=%ERRORLEVEL%
if not "%RCLC%"=="0" echo *** A SCRIPT READS A LOCAL BEFORE IT IS ASSIGNED -- it will die at that line; read the lines above >> "%LOG%"

echo. >> "%LOG%"
echo --- what we believe about ESPN's data --- >> "%LOG%"
REM Docs 419/420/422: every error on 24 Sept passed every internal-consistency check,
REM because every file agreed. What none of them tested was whether an OUTSIDE field
REM means what this project assumes. This one does, and it fires on the real defects.
py check_sources.py >> "%LOG%" 2>&1
set RC5B=%ERRORLEVEL%
if not "%RC5B%"=="0" echo *** A BELIEF ABOUT ESPN'S DATA IS BROKEN -- read the lines above; a number computed from it is suspect >> "%LOG%"

echo. >> "%LOG%"
echo --- the vintage check --- >> "%LOG%"
py check_vintage.py >> "%LOG%" 2>&1
set RC6=%ERRORLEVEL%
if not "%RC6%"=="0" echo *** THE PAGE IS PRINTING A RATE THIS SEASON ALREADY REFUTES -- read the table above before trusting any pts/wk on the sheet >> "%LOG%"

echo. >> "%LOG%"
echo --- the page check --- >> "%LOG%"
REM Doc 369: eleven CSS rules shipped as literal braces and had NEVER applied, on any
REM build, until Matt looked at the page. This refuses a page carrying an unsubstituted
REM template, a local link with nothing behind it, or a cell that says None.
py check_pages.py >> "%LOG%" 2>&1
set RC7=%ERRORLEVEL%
if not "%RC7%"=="0" echo *** A PAGE IS SHOWING A TEMPLATE, A DEAD LINK OR A MISSING VALUE -- read the lines above; it is on the page and the reader can see it >> "%LOG%"
REM Doc 440 (doc 436 asked for it): the page LOGIC check. check_pages.py reads templates and links;
REM this one reads what the page SAYS against the roster it was built from, starting with the rule
REM that a man in the IR slot is never offered as a drop in THE CALL or named as the cheapest man.
py check_page_logic.py >> "%LOG%" 2>&1
set RC7B=%ERRORLEVEL%
if not "%RC7B%"=="0" echo *** THE PAGE CONTRADICTS THE ROSTER -- a parked man is offered as a drop; read the lines above >> "%LOG%"

REM [doc 450] The standing rules a page states, read against the directive: a retracted phrase or number on any
REM page fails, and the wire page must carry the live claim day, the run, a drop on every claim, Add before Claim.
REM The wire page said "Tuesday night: put in claims" for a week after v9.26; nothing read it.
echo. >> "%LOG%"
echo --- the rules the pages state --- >> "%LOG%"
py check_page_rules.py >> "%LOG%" 2>&1
set RCR=%ERRORLEVEL%
if not "%RCR%"=="0" echo *** A PAGE STATES A RETRACTED RULE OR OMITS A LIVE ONE -- read the lines above >> "%LOG%"

REM How old is the usage file every workload number on the sheet is read from? Since doc 439
REM it is rebuilt at the top of every run; this line says whether that took.
if exist "%SRC%\form_2026.csv" (for %%F in ("%SRC%\form_2026.csv") do echo FORM FILE  %%~tF   ^(rebuilt at the top of every run^) >> "%LOG%") else (echo *** NO form_2026.csv -- run py research\wk1\build_form.py >> "%LOG%")

echo. >> "%LOG%"
REM Check the ARTIFACTS, not the exit codes.
if exist "%SRC%\LINEUP_CHECK.html"    (echo PAGE OK   LINEUP_CHECK.html      >> "%LOG%") else (echo *** NO LINEUP_CHECK.html ON DISK    >> "%LOG%")
if exist "%SRC%\THE_WEEKLY_WIRE.html" (echo PAGE OK   THE_WEEKLY_WIRE.html   >> "%LOG%") else (echo *** NO THE_WEEKLY_WIRE.html ON DISK >> "%LOG%")
if exist "%SRC%\WEEK_SHEET.html"      (echo PAGE OK   WEEK_SHEET.html         >> "%LOG%") else (echo *** NO WEEK_SHEET.html ON DISK      >> "%LOG%")
if exist "%SRC%\MY_TODO.html"         (echo PAGE OK   MY_TODO.html            >> "%LOG%") else (echo *** NO MY_TODO.html ON DISK         >> "%LOG%")
if exist "%~dp0..\COMMANDS.html"      (echo PAGE OK   COMMANDS.html           >> "%LOG%") else (echo *** NO COMMANDS.html ON DISK        >> "%LOG%")
REM ---- OPEN THE SHEET, because a page you have to go and find is a page you read late.
REM Matt, 2026-09-11: "I'd love it if a new page popped up on this machine when it was
REM refreshed so i'd see the instant i sat down here." It opens ONLY when the file's own
REM timestamp moved in this run -- opening a stale page on a schedule is the exit-code
REM defect wearing a different hat. Set FF_NO_OPEN=1 to suppress it.
set AFTER=none
if exist "%SRC%\WEEK_SHEET.html" for %%F in ("%SRC%\WEEK_SHEET.html") do set AFTER=%%~tF
if defined FF_NO_OPEN (
  echo SHEET NOT OPENED -- FF_NO_OPEN is set >> "%LOG%"
) else if "%AFTER%"=="none" (
  echo SHEET NOT OPENED -- there is no WEEK_SHEET.html to open >> "%LOG%"
) else if "%AFTER%"=="%BEFORE%" (
  echo SHEET NOT OPENED -- the page did not change in this run >> "%LOG%"
) else (
  echo SHEET OPENED -- %SRC%\WEEK_SHEET.html >> "%LOG%"
  start "" "%SRC%\WEEK_SHEET.html"
)
echo RESULT: %WHO% -- form %RCF%, snaps %RCS%, depth %RCD%, lines %RCL%, inherit %RCI%, projections %RCP%, news %RC0%, lineup %RC1%, wire %RC2%, to-do %RC3%, threads %RC9%, online %RC8%, commands %RC5%, kit %RC4%, locals %RCLC%, sources %RC5B%, vintage %RC6%, pages %RC7%, logic %RC7B%, rules %RCR% >> "%LOG%"
endlocal
