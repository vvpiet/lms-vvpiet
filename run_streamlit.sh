#!/usr/bin/env bash
# Run Streamlit safely on *nix systems
# Ensures the app has a .py extension before running
set -e

SCRIPT_PATH="$(pwd)/streamlit_app.py"
NOEXT_PATH="$(pwd)/streamlit_app"

if [ ! -f "$SCRIPT_PATH" ]; then
  if [ -f "$NOEXT_PATH" ]; then
    echo "Found 'streamlit_app' without extension — renaming to streamlit_app.py..."
    mv "$NOEXT_PATH" "$SCRIPT_PATH"
    echo "Renamed to streamlit_app.py"
  else
    echo "Cannot find streamlit_app.py — Please create it or use the correct filename."
    exit 1
  fi
fi

# Use venv python if available
if [ -f "venv/bin/python" ]; then
  PYTHON="venv/bin/python"
else
  PYTHON="python"
fi

echo "Running: $PYTHON -m streamlit run streamlit_app.py"
$PYTHON -m streamlit run streamlit_app.py
