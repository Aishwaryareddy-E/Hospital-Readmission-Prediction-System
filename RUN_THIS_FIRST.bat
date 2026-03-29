@echo off
REM ============================================================
REM START HERE - Hospital Readmission Project
REM This is your first step to run the project
REM ============================================================

color 0A
title Hospital Readmission Project - Getting Started

cls
echo.
echo ============================================================
echo   HOSPITAL READMISSION PREVENTION SYSTEM
echo   Getting Started Wizard
echo ============================================================
echo.
echo Welcome! This will help you get started with the project.
echo.
pause

:MENU
cls
echo.
echo ============================================================
echo   MAIN MENU - Choose Your Current Status
echo ============================================================
echo.
echo Please select what applies to you:
echo.
echo [1] I'm completely new - Need to set up everything
echo [2] I have Python and MySQL installed - Just need to run project
echo [3] Everything is set up - Want to start analysis
echo [4] Want to deploy the API
echo [5] Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto SETUP_ALL
if "%choice%"=="2" goto RUN_PROJECT
if "%choice%"=="3" goto START_ANALYSIS
if "%choice%"=="4" goto DEPLOY_API
if "%choice%"=="5" goto END
goto MENU

:SETUP_ALL
cls
echo.
echo ============================================================
echo   COMPLETE SETUP GUIDE
echo ============================================================
echo.
echo STEP 1: Install Python
echo ----------------------------------------
echo 1. Go to: https://www.python.org/downloads/
echo 2. Download Python 3.8 or higher
echo 3. During installation, CHECK "Add Python to PATH"
echo 4. Complete installation
echo.
echo Press any key when done...
pause >nul

echo.
echo STEP 2: Install MySQL
echo ----------------------------------------
echo 1. Go to: https://dev.mysql.com/downloads/mysql/
echo 2. Download MySQL Community Server
echo 3. Install and REMEMBER your root password
echo 4. Also install MySQL Workbench
echo.
echo Press any key when done...
pause >nul

echo.
echo STEP 3: Installing Python Packages...
echo ----------------------------------------
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Installation failed!
    echo Try: python -m pip install --upgrade pip
    pause
    goto MENU
)
echo Installation successful!
echo.
echo Press any key to continue...
pause >nul

echo.
echo STEP 4: Download Dataset
echo ----------------------------------------
echo 1. Go to: https://www.kaggle.com/datasets/dubradave/hospital-readmissions
echo 2. Create free Kaggle account if needed
echo 3. Download the dataset
echo 4. Rename file to: hospital_data.csv
echo 5. Move it to: data\ folder
echo.
echo Press any key when done...
pause >nul

echo.
echo STEP 5: Set Up Database
echo ----------------------------------------
echo 1. Open MySQL Workbench
echo 2. Connect to localhost with your password
echo 3. Open: setup_database.sql
echo 4. Click lightning bolt to run
echo 5. Verify hospital_db is created
echo.
echo Press any key when done...
pause >nul

echo.
echo STEP 6: Configure Password
echo ----------------------------------------
echo IMPORTANT: You need to update your MySQL password in config files
echo.
echo Files to edit:
echo   1. config.py (line 13)
echo   2. load_data.py (line 27)
echo   3. notebooks\02_preprocessing.py (line 27)
echo.
echo Replace 'yourpassword' with YOUR actual MySQL password
echo.
echo Press any key when done...
pause >nul

echo.
echo STEP 7: Load Data
echo ----------------------------------------
python load_data.py
if %errorlevel% neq 0 (
    echo ERROR: Data loading failed!
    echo Check if MySQL is running and password is correct
    pause
    goto MENU
)
echo.
echo SUCCESS! Data loaded into database.
echo.
pause
goto START_ANALYSIS

:RUN_PROJECT
cls
echo.
echo ============================================================
echo   RUNNING THE PROJECT
echo ============================================================
echo.
echo First, let's verify your setup...
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python first.
    pause
    goto MENU
)
echo OK: Python found
echo.

echo Checking if packages are installed...
python -c "import pandas" 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Required packages missing!
    echo Run: pip install -r requirements.txt
    pause
    goto MENU
)
echo OK: Packages found
echo.

echo Checking database setup...
echo Open MySQL Workbench and verify:
echo   1. hospital_db database exists
echo   2. patients table exists
echo   3. Data is loaded (101,766 rows)
echo.
echo Have you done this? (Y/N)
set /p done=""
if /i "%done%"=="N" (
    echo.
    echo Please complete these steps first:
    echo   1. Run setup_database.sql in MySQL Workbench
    echo   2. Edit load_data.py with your password
    echo   3. Run: python load_data.py
    echo.
    pause
    goto MENU
)

goto START_ANALYSIS

:START_ANALYSIS
cls
echo.
echo ============================================================
echo   STARTING DATA ANALYSIS
echo ============================================================
echo.
echo What would you like to do?
echo.
echo [1] Run Exploratory Data Analysis (Recommended first)
echo [2] Train Machine Learning Models
echo [3] Run SHAP Analysis (Model Explainability)
echo [4] Back to Menu
echo.
set /p analysis_choice="Enter choice (1-4): "

if "%analysis_choice%"=="1" goto RUN_EDA
if "%analysis_choice%"=="2" goto TRAIN_MODELS
if "%analysis_choice%"=="3" goto RUN_SHAP
if "%analysis_choice%"=="4" goto MENU
goto START_ANALYSIS

:RUN_EDA
cls
echo.
echo ============================================================
echo   EXPLORATORY DATA ANALYSIS
echo ============================================================
echo.
echo Opening Jupyter Notebook for EDA...
echo.
echo INSTRUCTIONS:
echo - Run each cell one by one (Shift+Enter)
echo - Don't skip cells - they build on each other
echo - Plots will be saved to plots\ folder automatically
echo.
echo Starting notebook...
echo.
jupyter notebook notebooks/01_eda.ipynb
echo.
echo When you're done with EDA, come back and train models!
pause
goto START_ANALYSIS

:TRAIN_MODELS
cls
echo.
echo ============================================================
echo   MACHINE LEARNING MODEL TRAINING
echo ============================================================
echo.
echo This will:
echo   1. Preprocess the data
echo   2. Train 4 different ML models
echo   3. Compare their performance
echo   4. Save the best model
echo.
echo Expected time: 3-5 minutes
echo.
set /p confirm="Ready to start? (Y/N): "
if /i not "%confirm%"=="Y" goto START_ANALYSIS

echo.
echo Starting model training...
echo.
python notebooks/03_model_training.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR during training!
    echo Make sure you've run EDA and data is preprocessed.
    pause
    goto START_ANALYSIS
)
echo.
echo Training complete! Check models\ folder for saved models.
echo.
pause
goto START_ANALYSIS

:RUN_SHAP
cls
echo.
echo ============================================================
echo   SHAP ANALYSIS - MODEL EXPLAINABILITY
echo ============================================================
echo.
echo This will show you WHY your model makes predictions
echo.
echo Expected time: 2-3 minutes
echo.
set /p confirm="Ready to start? (Y/N): "
if /i not "%confirm%"=="Y" goto START_ANALYSIS

echo.
python notebooks/04_shap_analysis.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR during SHAP analysis!
    echo Make sure you've trained models first.
    pause
    goto START_ANALYSIS
)
echo.
echo SHAP analysis complete! Check plots\ and report\ folders.
echo.
pause
goto START_ANALYSIS

:DEPLOY_API
cls
echo.
echo ============================================================
echo   DEPLOYING THE API
echo ============================================================
echo.
echo This will start the FastAPI server
echo.
echo The API will be available at: http://localhost:8000
echo Interactive docs at: http://localhost:8000/docs
echo.
echo IMPORTANT: Keep this window open while testing the API
echo.
set /p confirm="Start API server? (Y/N): "
if /i not "%confirm%"=="Y" goto MENU

echo.
echo Starting FastAPI server...
echo.
start cmd /k "cd /d %~dp0 && python api/app.py"
echo.
echo API server starting in new window...
echo.
timeout /t 3 /nobreak >nul
echo.
echo Now testing the API...
python api/test_api.py
echo.
pause
goto MENU

:END
cls
echo.
echo ============================================================
echo   Good luck with your project!
echo ============================================================
echo.
echo Remember:
echo   - Read the documentation in README.md
echo   - Check QUICKSTART.md for detailed steps
echo   - Use CHECKLIST.md to track progress
echo.
echo Happy coding!
echo.
timeout /t 3 /nobreak >nul
exit

:MENU
