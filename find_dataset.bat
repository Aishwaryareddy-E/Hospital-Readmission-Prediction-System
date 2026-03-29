@echo off
REM ============================================================
REM Find and Move Dataset Helper Script
REM This will help you locate the downloaded Kaggle dataset
REM ============================================================

color 0A
title Dataset Locator

cls
echo.
echo ============================================================
echo   FINDING YOUR KAGGLE DATASET
echo ============================================================
echo.

echo Searching for CSV files in Downloads folder...
echo.

REM Check common download locations
set "downloads=%USERPROFILE%\Downloads"
set "desktop=%USERPROFILE%\Desktop"
set "documents=%USERPROFILE%\Documents"

echo Checking: %downloads%
dir /s /b "%downloads%\*.csv" 2>nul | findstr /i "hospital diabetic" > "%temp%\found_csv.txt"
if exist "%temp%\found_csv.txt" (
    echo [FOUND] CSV files found:
    type "%temp%\found_csv.txt"
) else (
    echo [NOT FOUND] No hospital/diabetic CSV in Downloads
)
echo.

echo Checking: %desktop%
dir /s /b "%desktop%\*.csv" 2>nul | findstr /i "hospital diabetic" >> "%temp%\found_csv.txt"
if exist "%temp%\found_csv.txt" (
    type "%temp%\found_csv.txt"
)
echo.

echo ============================================================
echo   WHAT TO DO NOW
echo ============================================================
echo.
echo If you found your CSV file above:
echo.
echo 1. Note the file path
echo 2. Copy the file to:
echo    c:\data science project\hospital-readmission-project\data\
echo 3. Rename it to: hospital_data.csv
echo.
echo Example commands:
echo   copy "PATH_TO_YOUR_FILE\diabetic_data.csv" "c:\data science project\hospital-readmission-project\data\hospital_data.csv"
echo.
echo OR
echo.
echo Just manually move the file using File Explorer:
echo   1. Open Downloads folder
echo   2. Find the CSV file (probably diabetic_data.csv or similar)
echo   3. Copy it
echo   4. Navigate to: c:\data science project\hospital-readmission-project\data\
echo   5. Paste it there
echo   6. Rename to: hospital_data.csv
echo.
echo ============================================================
echo.
pause
