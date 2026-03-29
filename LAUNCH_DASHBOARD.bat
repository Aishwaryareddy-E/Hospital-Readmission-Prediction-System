@echo off
REM ============================================================
REM Launch Interactive Dashboard
REM ============================================================

color 0A
title Hospital Readmission Dashboard

cls
echo.
echo ============================================================
echo   HOSPITAL READMISSION PREDICTION - INTERACTIVE DASHBOARD
echo ============================================================
echo.
echo Starting Streamlit dashboard...
echo.
echo The dashboard will open in your default web browser.
echo.
echo Features:
echo ✓ Live data visualizations
echo ✓ ML model performance metrics
echo ✓ Real-time patient risk prediction
echo ✓ Interactive charts and insights
echo.
echo Press Ctrl+C in this window to stop the dashboard
echo.
echo ============================================================
echo.

cd /d "%~dp0"
streamlit run dashboard_app.py

pause
