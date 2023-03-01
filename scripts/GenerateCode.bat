@echo off

set SCADE_EXE=%SCADE_DIR%\SCADE\bin\scade.exe
set SCRIPT_PATH=%~dp0.
set WORKING_DIR=%cd%

set LOGFILE=%~dpn0.log

:: check if there is an argument
if ["%~1"]==[""] goto usage
set PROJECT=%WORKING_DIR%\%~1
set PROJECT_PATH=%~dp1
set PROJECT_NAME=%~n1

:: check if the project exists
if not exist "%PROJECT%" goto filenotexist

:: check if there is an argument
if ["%~2"]==[""] goto usage
set CONF=%~2

:: check if KCG folder exists and delete it
if exist %PROJECT_PATH%KCG rmdir %PROJECT_PATH%KCG

@echo Generating code for %PROJECT% using the configuration %CONF%
"%SCADE_EXE%" -code "%PROJECT%" -conf "%CONF%" > "%LOGFILE%" 2>&1

:: display the command output
type "%LOGFILE%"

:: check for the correct completion of the command (no error code returned by SCADE)
type "%LOGFILE%" | find "Command completed" > nul

if %errorlevel% neq 0 exit /B 1

:: zip generated code for delivery
if exist %PROJECT_PATH%%PROJECT_NAME%_generated_code.zip del %PROJECT_PATH%%PROJECT_NAME%_generated_code.zip

powershell -NoProfile -NoLogo -Command "Compress-Archive -Path %PROJECT_PATH%KCG\*.* -DestinationPath %PROJECT_PATH%%PROJECT_NAME%_generated_code.zip"

goto :eof

:usage
@echo Usage: %0 ^<SCADE project^> ^<SCADE configuration^>
exit /B 1
:filenotexist
@echo Error: file ^<%~s1^> does not exist
exit /B 1