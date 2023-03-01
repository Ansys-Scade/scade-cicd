@echo off

set SCADE_EXE="%SCADE_DIR%\SCADE\bin\scade.exe"
set SCRIPT_PATH=%~dp0.
set WORKING_DIR=%cd%

set LOGFILE=%~dpn0.log

:: check if there is an argument
if ["%~1"]==[""] goto usage
set PROJECT=%WORKING_DIR%\%~1
set PROJECT_PATH=%~dp1
set PROJECT_NAME=%~n1
set PROJECT_PATH_NAME=%~dpn1

:: check if the project exists
if not exist "%PROJECT%" goto file1notexist

:: check if there is an argument
if ["%~2"]==[""] goto usage
set PROJECT_TEST=%WORKING_DIR%\%~2
set PROJECT_TEST_PATH=%~dp2
set PROJECT_TEST_NAME=%~n2
set PROJECT_TEST_PATH_NAME=%~dpn2

:: check if the project exists
if not exist "%PROJECT_TEST%" goto file2notexist

:: copy all artifacts in a zip
if exist delivery rd /S /Q delivery
md delivery

powershell -NoProfile -NoLogo -Command "Compress-Archive -LiteralPath %PROJECT_PATH_NAME%.htm, %PROJECT_PATH_NAME%_rules.htm, %PROJECT_PATH_NAME%.rtf, %PROJECT_PATH%KCG_Generated_Code.zip, %PROJECT_TEST_PATH%Test_TEE\%PROJECT_NAME%_Tests.txt, %PROJECT_TEST_PATH_NAME%_mcsummary.html -DestinationPath delivery\%PROJECT_NAME%.zip"
if %errorlevel% neq 0 echo "Error packaging project" & exit /B 1

goto :eof

:usage
@echo Usage: %0 ^<SCADE project^> ^<SCADE Test project^>
exit /B 1
:file1notexist
@echo Error: file ^<%~s1^> does not exist
exit /B 1
:file2notexist
@echo Error: file ^<%~s2^> does not exist
exit /B 1