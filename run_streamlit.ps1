# Run Streamlit safely from PowerShell
# This script ensures the app filename ends with .py and then runs streamlit
# Usage: .\run_streamlit.ps1

Set-StrictMode -Version Latest

$scriptPath = Join-Path $PSScriptRoot 'streamlit_app.py'
$noExtPath = Join-Path $PSScriptRoot 'streamlit_app'

if (-not (Test-Path $scriptPath)) {
    if (Test-Path $noExtPath) {
        Write-Host "Found 'streamlit_app' without extension — renaming to streamlit_app.py..."
        try {
            Rename-Item -Path $noExtPath -NewName 'streamlit_app.py' -Force -ErrorAction Stop
            Write-Host "Renamed to streamlit_app.py"
        }
        catch {
            Write-Host "Failed to rename the file: $_"
            exit 1
        }
    }
    else {
        Write-Host "Cannot find streamlit_app.py — please create it or use the correct filename." -ForegroundColor Red
        exit 1
    }
}

# Use venv's python if available, else fallback to system python
$venvPython = Join-Path $PSScriptRoot 'venv\Scripts\python.exe'
if (Test-Path $venvPython) { $python = $venvPython } else { $python = 'python' }

Write-Host "Running: $python -m streamlit run streamlit_app.py"
& $python -m streamlit run "streamlit_app.py" 
