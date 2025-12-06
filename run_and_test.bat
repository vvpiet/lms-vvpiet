@echo off
REM Quick-start script for testing the fixed test attempts feature
REM Run this from D:\Feedback directory

title Faculty Feedback System - Test Attempts

echo.
echo ====================================================================
echo Test Attempts Fix - Quick Start
echo ====================================================================
echo.

REM Check Python
py --version
if errorlevel 1 (
    echo ERROR: Python not found. Make sure it's installed and in PATH.
    pause
    exit /b 1
)

echo.
echo [1/3] Checking database state...
py verify_attempts.py

echo.
echo [2/3] Starting Streamlit app on port 8502...
echo.
echo INSTRUCTIONS:
echo 1. Browser will open at: http://localhost:8502
echo 2. For fastest test, do this:
echo    - Login: admin / admin123
echo    - Page: Debug: Test Attempts
echo    - Action: Scroll to "Seed Demo Attempt"
echo    - Click "Seed demo attempt" button
echo    - You should see attempts appear in table above
echo.
echo 3. To see student view:
echo    - Logout
echo    - Login: student / student123
echo    - Page: Dashboard
echo    - Check "My Recent Test Attempts" section
echo.
echo 4. To see faculty view:
echo    - Logout
echo    - Login: snehal / faculty123
echo    - Page: Create Test
echo    - Check "View Attempts for a Test" section
echo.
echo Press any key to start Streamlit...
pause

py -m streamlit run streamlit_app.py --server.port 8502
