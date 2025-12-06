#!/usr/bin/env powershell
<#
.SYNOPSIS
Quick-start script for testing the fixed test attempts feature
Run from D:\Feedback directory

.DESCRIPTION
This script:
1. Checks Python installation
2. Verifies database state
3. Starts Streamlit app with testing instructions
#>

$ErrorActionPreference = "Continue"

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Test Attempts Fix - Quick Start" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[CHECK] Python installation..." -ForegroundColor Yellow
py --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found. Make sure it's installed and in PATH." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ Python found" -ForegroundColor Green
Write-Host ""

# Check database
Write-Host "[1/3] Checking database state..." -ForegroundColor Yellow
Set-Location -Path 'D:\Feedback'
py verify_attempts.py
Write-Host ""

# Start Streamlit
Write-Host "[2/3] Starting Streamlit app on port 8502..." -ForegroundColor Yellow
Write-Host ""

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "TESTING INSTRUCTIONS:" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "OPTION 1: Fastest Test (Admin Seed)" -ForegroundColor Green
Write-Host "  1. Browser opens at: http://localhost:8502"
Write-Host "  2. Login: admin / admin123"
Write-Host "  3. Page: '🐛 Debug: Test Attempts' (click in sidebar)"
Write-Host "  4. Scroll down to '🔧 Admin: Seed Demo Attempt'"
Write-Host "  5. Select test 'test' and student 'student'"
Write-Host "  6. Click button - attempt should appear in table above"
Write-Host ""

Write-Host "OPTION 2: Student View Test" -ForegroundColor Green
Write-Host "  1. After seeding (or submit), logout in sidebar"
Write-Host "  2. Login: student / student123"
Write-Host "  3. Page: '🏠 Dashboard'"
Write-Host "  4. Scroll to '🧪 My Recent Test Attempts' section"
Write-Host "  5. Should see table with your attempt(s)"
Write-Host ""

Write-Host "OPTION 3: Faculty View Test" -ForegroundColor Green
Write-Host "  1. Logout"
Write-Host "  2. Login: snehal / faculty123 (created the tests)"
Write-Host "  3. Page: '🧪 Create Test'"
Write-Host "  4. Scroll to 'View Attempts for a Test' section"
Write-Host "  5. Select test 'test' from dropdown"
Write-Host "  6. Should see attempts in table + 'Download Attempts CSV' button"
Write-Host ""

Write-Host "OPTION 4: Full Student Submission Test" -ForegroundColor Green
Write-Host "  1. Login as student"
Write-Host "  2. Page: '🧪 Tests' → Click 'Start Test' on 'test'"
Write-Host "  3. Answer questions and click 'Submit Test'"
Write-Host "  4. Should see: Score, Saved record, Download button"
Write-Host "  5. Go to Dashboard → My Recent Test Attempts"
Write-Host "  6. New attempt should appear at top"
Write-Host ""

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Ready to test! Starting Streamlit..." -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# Start Streamlit
py -m streamlit run streamlit_app.py --server.port 8502
