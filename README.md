# Engineering Faculty Feedback (Student-facing)

Simple Flask app to collect student feedback for engineering faculty with SQLite database.

Quick start (Windows PowerShell):

```powershell
cd "C:\Users\ho\Desktop\Feedback"
python -m venv venv; .\venv\Scripts\Activate
pip install -r requirements.txt
# (optional) set a custom DB: $env:DATABASE_URL = 'sqlite:///C:/path/to/feedback.db'
python app.py
```

Open http://127.0.0.1:5000/ in your browser to submit feedback. Admin view at `/admin`.

If you're using the Streamlit app (`streamlit_app.py`), use the provided run script to ensure the filename includes the `.py` extension and to avoid errors:

PowerShell (recommended):
```powershell
cd "C:\Users\ho\Desktop\Feedback"
.\run_streamlit.ps1
```

Alternative using your venv Python:
```powershell
C:/Users/ho/Desktop/Feedback/venv/Scripts/python.exe -m streamlit run streamlit_app.py
```
Alternative using your venv Python (PowerShell) or Shell (macOS / Linux):
```powershell
C:/Users/ho/Desktop/Feedback/venv/Scripts/python.exe -m streamlit run streamlit_app.py
```

macOS / Linux:
```bash
./run_streamlit.sh
```

Note for PowerShell users: if you haven't enabled script execution on your machine, run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

Notes:
- Uses SQLite by default and creates `feedback.db` in the project folder.
- This is a minimal example intended for demonstration and local use.
