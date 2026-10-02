@echo off
REM ==========================================================================
REM  setup_tasks.bat -- THE ONE FILE THAT REGISTERS THE SCHEDULE.
REM
REM  FIVE separately-named tasks, all running the same ff.bat:
REM      FF2026 - 1 Tue wire      Tuesday  06:00
REM      FF2026 - 2 Thu lineup    Thursday 17:30
REM      FF2026 - 3 Sun early     Sunday   11:45
REM      FF2026 - 4 Sun late      Sunday   15:30
REM      FF2026 - 5 daily post-waiver   every day 07:30   (added 19 Sept, doc 374)
REM
REM  WHY FOUR AND NOT ONE WITH FOUR TRIGGERS:
REM    Task Scheduler shows "Last Run Time" and "Last Run Result" PER TASK, not
REM    per trigger. With one task you cannot tell from the list whether Sunday
REM    ever fired -- you only ever see the most recent run of the four. Four
REM    rows means one glance tells you which occasion worked and which did not.
REM    That is exactly the question we could not answer for two days.
REM    They all call the same batch file, so the BEHAVIOUR is identical; only
REM    the reporting is split. The number prefix keeps them in order in the list.
REM
REM  HOW TO RUN (once):
REM    Start -> type  cmd  -> right-click Command Prompt -> Run as administrator
REM    Paste:   "G:\My Drive\_Fantasy\2026\Scripts\setup_tasks.bat"
REM
REM  Safe to run twice. It removes every older FF2026 name first.
REM ==========================================================================
setlocal
set S=%~dp0
if not exist "%S%ff.bat" (echo MISSING: %S%ff.bat & goto :end)

echo.
echo Removing every older FF2026 task so the list is clean ...
REM  doc 261: two of these SURVIVED a clean run on 2026-09-09 -- "FF2026 - Tuesday wire"
REM  and "FF2026 - Lineup check" were both still in the list afterwards, each firing at
REM  the same minute as its replacement. The delete was piped to nul, so whatever
REM  schtasks said about them was thrown away. It is not silenced any more.
for %%T in (
  "FF2026"
  "FF2026 - Tuesday wire" "FF2026 - Lineup check"
  "FF2026 - Lineup THU" "FF2026 - Lineup SUN am" "FF2026 - Lineup SUN pm"
  "FF2026 - Sept 5 projection pull" "FF2026 - DRAFT NIGHT"
) do call :killtask %%T

echo.
echo Creating the five tasks ...
echo.
schtasks /create /f /tn "FF2026 - 1 Tue wire"   /tr "cmd /c \"%S%ff.bat\" TUE"      /sc WEEKLY /d TUE /st 06:00
schtasks /create /f /tn "FF2026 - 2 Thu lineup" /tr "cmd /c \"%S%ff.bat\" THU"      /sc WEEKLY /d THU /st 17:30
schtasks /create /f /tn "FF2026 - 3 Sun early"  /tr "cmd /c \"%S%ff.bat\" SUNam"    /sc WEEKLY /d SUN /st 11:45
schtasks /create /f /tn "FF2026 - 4 Sun late"   /tr "cmd /c \"%S%ff.bat\" SUNpm"    /sc WEEKLY /d SUN /st 15:30

REM 5. THE ONE THAT WAS MISSING, AND MATT FOUND IT ON 19 SEPT: "What about the Saturday claims
REM    that went through early this AM." Waiver claims settle on ESPN's own clock, which is not
REM    any of the four days above, so a claim could process and every file on this drive would
REM    still describe the roster he had BEFORE it. No page was wrong; they were all answering a
REM    question about yesterday. A daily morning pull is the only thing that closes that, and it
REM    costs about a minute of his machine.
schtasks /create /f /tn "FF2026 - 5 daily post-waiver" /tr "cmd /c \"%S%ff.bat\" DAILY" /sc DAILY /st 07:30

echo.
echo ================ WHAT EXISTS NOW ================
echo.
REM An exit code is not a result -- read the four blocks below, not the SUCCESS lines.
for %%T in (
  "FF2026 - 1 Tue wire" "FF2026 - 2 Thu lineup" "FF2026 - 3 Sun early" "FF2026 - 4 Sun late"
  "FF2026 - 5 daily post-waiver"
) do (
  schtasks /query /tn %%T /fo LIST | findstr /i "TaskName Next Status"
  echo.
)

echo ============ EVERY FF2026 TASK ON THIS MACHINE ============
REM  doc 261 / SECTION 0.5(c)5. The block above proves the five we WANT exist. It says
REM  nothing about a leftover that also exists -- and a leftover is not cosmetic: two
REM  tasks firing the same minute run ff.bat twice at once, and both runs write the same
REM  two HTML pages and the same log. Anything listed here that is not one of the five
REM  numbered names must be deleted.
REM  19 Sept, doc 379: this block still said FOUR after the fifth task was added above, so
REM  the script told Matt the task it had just created was a duplicate to delete.
schtasks /query /fo LIST | findstr /i "FF2026"
echo.
echo EXPECTED: EXACTLY five TaskName lines above -- 1 Tue wire, 2 Thu lineup,
echo           3 Sun early, 4 Sun late, 5 daily post-waiver.  Any sixth name is a
echo           duplicate: delete it with   schtasks /delete /tn "THE NAME" /f
echo.
echo EXPECTED: five tasks, each with its own Next Run Time.
echo If any is missing, copy this whole window and send it to me.
echo.
echo TEST ONE NOW:   schtasks /run /tn "FF2026 - 2 Thu lineup"
echo Then read Scripts\ff_log.txt -- the first line of the run says THU.
echo.
:end
pause
endlocal
goto :eof

REM ==========================================================================
REM  killtask -- delete one task and SAY WHAT HAPPENED. The old loop sent both
REM  streams to nul, which is SECTION 0.2's "an exit code is not a result" in its
REM  cheapest form: a delete that silently refused looked exactly like a delete
REM  that worked, and two tasks lived through it.
REM ==========================================================================
:killtask
schtasks /query /tn %1 >nul 2>&1
if errorlevel 1 (
  echo   not there    %~1
  goto :eof
)
schtasks /delete /tn %1 /f >nul 2>&1
if errorlevel 1 (
  echo   *** REFUSED  %~1   -- running the delete again without /nul to show why:
  schtasks /delete /tn %1 /f
) else (
  echo   deleted      %~1
)
goto :eof
