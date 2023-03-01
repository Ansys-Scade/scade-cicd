@echo off

set SCADE_EXE=%SCADE_DIR%\SCADE\bin\scade.exe
set SCRIPT_PATH=%~dp0.
set WORKING_DIR=%cd%

:: check if there is an argument
if ["%~1"]==[""] goto usage
set PROJECT_NAME=%~1

:: get the SHA of the last commit on the target branch for the merge
:: this variable is not fulfill in the free GitLab
::for /f "usebackq delims=" %%i in (`git log -n 1 "--pretty=%%h" origin/%CI_MERGE_REQUEST_TARGET_BRANCH_NAME%`) do @set CI_MERGE_REQUEST_TARGET_BRANCH_SHA_new=%%i

:: create a tmp dir to download the target project
mkdir tmp

:: download and unzip the target project
@echo "Download project: https://niclineseg/api/v4/projects/%CI_PROJECT_ID%/repository/archive?sha=%CI_MERGE_REQUEST_DIFF_BASE_SHA%"
curl "https://niclineseg/api/v4/projects/%CI_PROJECT_ID%/repository/archive?sha=%CI_MERGE_REQUEST_DIFF_BASE_SHA%" -o tmp\target_project.gz

:: uncompress the downloaded file
tar -xf tmp\target_project.gz -C tmp

:: get the uncompressed folder name
for /f "delims=" %%i in ('dir /b /a:d tmp\%%CI_PROJECT_NAME%%-%%CI_MERGE_REQUEST_DIFF_BASE_SHA%%*') do @set PROJECT2=tmp\%%i\%PROJECT_NAME%

:: generate diff report between %PROJECT_NAME% and %PROJECT2%
@echo "Make a diff between %PROJECT_NAME% %PROJECT2%"
%SCRIPT_PATH%\ReportDiff.bat "%PROJECT_NAME%" "%PROJECT2%"

:: delete tmp folder
rmdir /s /q tmp

if %errorlevel% neq 0 exit /B 1

goto :eof

:usage
@echo Usage: %0 ^<SCADE project 1 name^> ^<SCADE project 2 name^>
exit /B 1
:filenotexist
@echo Error: file ^<%~s1^> does not exist
exit /B 1
