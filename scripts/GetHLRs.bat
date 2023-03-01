@echo off

set SCADE_EXE=%SCADE_DIR%\SCADE\bin\scade.exe
set PYTHON_EXE=%SCADE_DIR%\contrib\Python37\python.exe
set PYTHONPATH=%SCADE_DIR%\SCADE\bin;%SCADE_DIR%\SCADE\APIs\Python\Lib;%PYTHONPATH%
set SCRIPT_PATH=%~dp0.
set WORKING_DIR=%cd%

set LOGFILE=%~dpn0.log

:: check if there is an argument
if ["%~1"]==[""] goto usage
set PROJECT=%WORKING_DIR%\%~1

:: check if the project exists
if not exist "%PROJECT%" goto filenotexist


@echo get HLRs for %PROJECT%

FOR %%I in (%PROJECT%) do set HLR_LIST=%%~dpnI_hlrs.txt
"%PYTHON_EXE%" "%SCRIPT_PATH%\GetHLRs.py" -v "%PROJECT%" -o "%HLR_LIST%"

if %errorlevel% neq 0 exit /B 1

exit /B 0

:usage
@echo Usage: %0 ^<SCADE project^> ^<SCADE configuration^>
exit /B 1
:filenotexist
@echo Error: file ^<%PROJECT%^> does not exist
exit /B 1
