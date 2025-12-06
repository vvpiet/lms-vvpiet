@echo off
REM Run Streamlit safely on Windows cmd
REM Ensures the app has a .py extension before running

if not exist streamlit_app.py (
  if exist streamlit_app (
    ren streamlit_app streamlit_app.py
  ) else (
    echo Cannot find streamlit_app.py or streamlit_app
    exit /b 1
  )
)

if exist venv\Scripts\python.exe (
  venv\Scripts\python.exe -m streamlit run streamlit_app.py
) else (
  python -m streamlit run streamlit_app.py
)
