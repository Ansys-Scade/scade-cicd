@echo off

set SCADE_EXE=%SCADE_DIR%\SCADE\bin\scade.exe
set SCRIPT_PATH=%~dp0.
set WORKING_DIR=%cd%

set LOGFILE=%~dpn0.log

:: check if there is an argument
if ["%~1"]==[""] goto usage
set PROJECT=%WORKING_DIR%\%~1

:: check if the project exists
if not exist "%PROJECT%" goto filenotexist

:: check if there is an argument
if ["%~2"]==[""] goto usage
set CONF=%~2

@echo Check model for %PROJECT% using the configuration %CONF%
"%SCADE_EXE%" -check "%PROJECT%" -conf "%CONF%" > "%LOGFILE%" 2>&1

:: display the command output
type "%LOGFILE%"

:: check for errors
for /F "tokens=4,5" %%I in (%LOGFILE%) do (
    if "%%J" == "error(s)" (
        if %%I NEQ 0 exit /B 1
    )
)

@echo Check rules for %PROJECT% using the configuration %CONF%
"%SCADE_EXE%" -rules_checker "%PROJECT%" -conf "%CONF%"

@echo Check metrics for %PROJECT% using the configuration %CONF%
"%SCADE_EXE%" -metrics "%PROJECT%" -conf "%CONF%"

exit /B 0

:usage
@echo Usage: %0 ^<SCADE project^> ^<SCADE configuration^>
exit /B 1
:filenotexist
@echo Error: file ^<%PROJECT%^> does not exist
exit /B 1
