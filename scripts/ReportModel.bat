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

@echo Report model for %PROJECT% using the configuration %CONF%
"%SCADE_EXE%" -report "%PROJECT%" -configuration "%CONF%" > "%LOGFILE%" 2>&1

:: display the command output
type "%LOGFILE%"

:: check for errors
type "%LOGFILE%" | find "report generated in:" > nul

if %errorlevel% neq 0 exit /B 1

goto :eof

:usage
@echo Usage: %0 ^<SCADE project^> ^<SCADE configuration^>
exit /B 1
:filenotexist
@echo Error: file ^<%~s1^> does not exist
exit /B 1