@echo off

set SCADE_EXE=%SCADE_DIR%\SCADE\bin\scade.exe
set SCRIPT_PATH=%~dp0.
set WORKING_DIR=%cd%

:: check if there is an argument
if ["%~1"]==[""] goto usage
set PROJECT1=%WORKING_DIR%\%~1

:: check if the project exists
if not exist "%PROJECT1%" goto file1notexist

:: check if there is an argument
if ["%~2"]==[""] goto usage
set PROJECT2=%WORKING_DIR%\%~2

:: check if the project exists
if not exist "%PROJECT2%" goto file2notexist

@echo Generate diff report between %PROJECT1% and %PROJECT2%
"%SCADE_EXE%" -diff "%PROJECT2%" "%PROJECT1%" -report diff_report.html

if %errorlevel% neq 0 exit /B 1

goto :eof

:usage
@echo Usage: %0 ^<SCADE project 1^> ^<SCADE project 2^>
exit /B 1
:file1notexist
@echo Error: file ^<%~s1^> does not exist
exit /B 1
:file2notexist
@echo Error: file ^<%~s2^> does not exist
exit /B 1