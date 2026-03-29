@echo off
REM ============================================================
REM Windows Installation Script for Hospital Readmission Project
REM ============================================================
REM This script automates the initial setup process
REM Run this from the project root directory
REM ============================================================

echo.
echo ============================================================
echo HOSPITAL READMISSION PROJECT - WINDOWS INSTALLER
echo ============================================================
echo.

REM Step 1: Check if Python is installed
echo [Step 1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
echo SUCCESS: Python found
python --version
echo.

REM Step 2: Check if pip is available
echo [Step 2/5] Checking pip installation...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip is not available
    echo Please reinstall Python with pip support
    pause
    exit /b 1
)
echo SUCCESS: pip found
echo.

REM Step 3: Install dependencies
echo [Step 3/5] Installing Python packages...
echo This may take 5-10 minutes depending on your internet speed
echo.
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    echo Try running: python -m pip install --upgrade pip
    echo Then run this script again
    pause
    exit /b 1
)
echo SUCCESS: All packages installed
echo.

REM Step 4: Create necessary directories
echo [Step 4/5] Creating project directories...
if not exist "data" mkdir data
if not exist "models" mkdir models
if not exist "plots" mkdir plots
if not exist "report" mkdir report
if not exist "dashboard" mkdir dashboard
echo SUCCESS: Directories created
echo.

REM Step 5: Verify installation
echo [Step 5/5] Verifying installation...
python -c "import pandas; import numpy; import sklearn; import xgboost; import shap; import fastapi" 2>nul
if %errorlevel% neq 0 (
    echo WARNING: Some packages may not be installed correctly
    echo Try importing them manually in Python to see the error
    echo You can still proceed, but may encounter issues
) else (
    echo SUCCESS: All core packages imported successfully
)
echo.

REM Summary
echo ============================================================
echo INSTALLATION COMPLETE!
echo ============================================================
echo.
echo Next steps:
echo 1. Install MySQL from https://dev.mysql.com/downloads/mysql/
echo 2. Open MySQL Workbench and run setup_database.sql
echo 3. Edit load_data.py and replace 'yourpassword' with your MySQL password
echo 4. Run: python load_data.py
echo 5. Open QUICKSTART.md for detailed instructions
echo.
echo IMPORTANT: Remember to set your MySQL password in:
echo   - load_data.py
echo   - config.py
echo   - notebooks/02_preprocessing.py
echo.
echo For help, open README.md or QUICKSTART.md
echo.
echo Press any key to continue...
pause >nul
