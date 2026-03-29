@echo off
REM ============================================================
REM Quick Status Checker - What's Done, What's Pending
REM ============================================================

color 0B
title Project Setup Status Checker

cls
echo.
echo ============================================================
echo   HOSPITAL READMISSION PROJECT - SETUP STATUS
echo ============================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python is installed
    python --version
) else (
    echo [!!] Python NOT found - Install Python first!
)
echo.

echo Checking pip packages...
pip show pandas >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Required packages are installed
) else (
    echo [!!] Packages missing - Run: pip install -r requirements.txt
)
echo.

echo Checking project structure...
if exist "data" (
    echo [OK] data\ folder exists
) else (
    echo [!!] data\ folder missing
)

if exist "notebooks" (
    echo [OK] notebooks\ folder exists
) else (
    echo [!!] notebooks\ folder missing
)

if exist "api" (
    echo [OK] api\ folder exists
) else (
    echo [!!] api\ folder missing
)

if exist "models" (
    echo [OK] models\ folder exists
) else (
    echo [!!] models\ folder missing
)

if exist "plots" (
    echo [OK] plots\ folder exists
) else (
    echo [!!] plots\ folder missing
)

if exist "report" (
    echo [OK] report\ folder exists
) else (
    echo [!!] report\ folder missing
)
echo.

echo Checking dataset...
if exist "data\hospital_data.csv" (
    echo [OK] Dataset found!
    for %%A in ("data\hospital_data.csv") do echo      Size: %%~zA bytes
) else (
    echo [!!] Dataset NOT downloaded yet
    echo      Download from: https://www.kaggle.com/datasets/dubradave/hospital-readmissions
)
echo.

echo Checking MySQL connection...
python -c "import mysql.connector; mysql.connector.connect(host='localhost', user='root', password='YOUR_PASSWORD')" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] MySQL appears to be running
) else (
    echo [!!] MySQL not detected or password incorrect
    echo      1. Install MySQL from https://dev.mysql.com/downloads/mysql/
    echo      2. Update password in config files
)
echo.

echo Checking documentation files...
if exist "README.md" (
    echo [OK] README.md exists
) else (
    echo [!!] README.md missing
)

if exist "QUICKSTART.md" (
    echo [OK] QUICKSTART.md exists
) else (
    echo [!!] QUICKSTART.md missing
)

if exist "STEP_BY_STEP_EXECUTION.md" (
    echo [OK] STEP_BY_STEP_EXECUTION.md exists
) else (
    echo [!!] STEP_BY_STEP_EXECUTION.md missing
)
echo.

echo ============================================================
echo   SUMMARY
echo ============================================================
echo.
echo COMPLETED:
echo   [x] Python packages installed
echo.
echo PENDING (Do these NOW):
echo   [ ] MySQL installed and running
echo   [ ] Dataset downloaded from Kaggle
echo   [ ] Password updated in config files
echo   [ ] Data loaded into database
echo.
echo NEXT ACTION:
echo   1. Check if MySQL download completed
echo   2. Install MySQL (write down password!)
echo   3. Download dataset from Kaggle
echo   4. Come back when both are done
echo.
echo ============================================================
echo.
pause
