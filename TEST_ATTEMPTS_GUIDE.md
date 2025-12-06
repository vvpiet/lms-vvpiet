# Test Attempts Troubleshooting Guide

## ✅ What's Fixed
- Database schema: `test_attempts` table is properly created with correct columns
- DB queries: `get_test_attempts_for_student()` and `get_test_attempts_for_test()` return correct data
- Attempt inserts: `submit_test_attempt()` function logs to `attempts.log` and inserts records
- Student UI: Dashboard now shows "My Recent Test Attempts" section with all recorded attempts
- Faculty UI: "Create Test" → "View Attempts for a Test" page displays attempts and allows CSV download
- Admin UI: "Debug: Test Attempts" page shows all attempts system-wide + seed button

## 🔍 Current DB State
- **3 attempts recorded** for test_id=3, student_id=4, score=2.0 each
- **Queries verified working**: Both student and test queries return correct rows
- **Data is persistently stored** in `feedback_streamlit.db`

## 🐛 If You Still Don't See Attempts in the App

### Step 1: Verify DB State
```powershell
# Check if attempts exist in DB
py verify_attempts.py

# Or manually query
py -c "import sqlite3; c=sqlite3.connect('feedback_streamlit.db'); cur=c.cursor(); cur.execute('SELECT COUNT(*) FROM test_attempts'); print(f'Attempts: {cur.fetchone()[0]}'); c.close()"
```

### Step 2: Check App Session
**Attempts may not display if:**
1. **User not logged in**: Student login is required. Session expires on page refresh.
2. **Wrong user role**: 
   - Student sees attempts on "🏠 Dashboard" (new "My Recent Test Attempts" section)
   - Faculty sees attempts on "🧪 Create Test" (must be faculty who CREATED the test)
   - Admin sees attempts on "🐛 Debug: Test Attempts" (all tests/all students)

### Step 3: Browser Cache
- **Force refresh**: Press `Ctrl+F5` (or `Cmd+Shift+R` on Mac)
- **Clear Streamlit cache**: Delete `.streamlit/` folder if it exists

### Step 4: Check App Logs
Streamlit shows real-time output in the terminal. Look for:
- `Please replace st.experimental_rerun` warnings (safe to ignore)
- Python errors (red text) = something crashed
- Test if submission worked: check `attempts.log`

```powershell
# View recent log entries
Set-Location 'D:\Feedback'
if (Test-Path attempts.log) { Get-Content attempts.log -Tail 20 }
```

### Step 5: Seed a Demo Attempt (Easiest Test)
1. Start the app: `py -m streamlit run streamlit_app.py --server.port 8502`
2. Login as **admin** (user: admin, password: admin123)
3. Go to "🐛 Debug: Test Attempts" section
4. Scroll to "🔧 Admin: Seed Demo Attempt"
5. Select a test and student, click "Seed demo attempt for selected test"
6. **Now that a fresh attempt is created**, login as the student/faculty and check if it displays

### Step 6: Full Submission Test (More Realistic)
1. Start the app
2. Login as **student** (user: student, password: student123)
3. Go to "🧪 Tests"
4. Click "Start Test" on an active test (must be within start/end time)
5. Submit the test
6. **You should immediately see**:
   - "Test submitted. Score: X"
   - "Saved attempt record — ID: ... | Score: ... | Submitted: ..."
   - A "Download Your Attempt (CSV)" button
7. Go to "🏠 Dashboard" → "My Recent Test Attempts" section
   - You should see your new attempt listed
8. Logout and login as **faculty** who created that test
9. Go to "🧪 Create Test" → "View Attempts for a Test"
   - Select the test you just submitted
   - You should see your attempt in the table
   - Click "Download Attempts CSV" to get a CSV file

## 📋 What Each Page Shows

| Role | Page | What It Shows |
|------|------|--------------|
| **Student** | Dashboard → My Recent Test Attempts | All their attempts across all tests |
| **Faculty** | Create Test → View Attempts | Attempts for their OWN tests only |
| **Admin** | Debug: Test Attempts | ALL attempts in the system + seed button |

## 🔧 Debugging Commands

```powershell
# Show all attempts in DB
py -c "import sqlite3; c=sqlite3.connect('feedback_streamlit.db'); cur=c.cursor(); cur.execute('SELECT id, test_id, student_id, score, submitted_at FROM test_attempts'); [print(r) for r in cur.fetchall()]; c.close()"

# Show all tests
py -c "import sqlite3; c=sqlite3.connect('feedback_streamlit.db'); cur=c.cursor(); cur.execute('SELECT id, title, faculty_id FROM tests'); [print(r) for r in cur.fetchall()]; c.close()"

# Show all students
py -c "import sqlite3; c=sqlite3.connect('feedback_streamlit.db'); cur=c.cursor(); cur.execute('SELECT id, username, name FROM users WHERE role=\"student\"'); [print(r) for r in cur.fetchall()]; c.close()"

# Show submission log (if exists)
Get-Content D:\Feedback\attempts.log -Tail 50
```

## ✨ New Features Added
1. **Student Dashboard**: "My Recent Test Attempts" section shows all attempts with test names and scores
2. **Logging**: `submit_test_attempt()` now writes to `attempts.log` for debugging
3. **Admin Seed Button**: "Debug: Test Attempts" page has a UI button to seed demo attempts
4. **Attempt Verification**: After student submits, app shows "Saved attempt record" confirmation
5. **Verification Script**: `verify_attempts.py` shows DB state and tests all query functions

## 🚀 If Everything Works
Once you see attempts displaying correctly:
1. You can create tests in "🧪 Create Test"
2. Students can take and submit tests in "🧪 Tests" / "🧪 Take Test"
3. Faculty can view and download attempts in "🧪 Create Test"
4. Admin can see all attempts and export in "🐛 Debug: Test Attempts"

---
**Next Step**: Start the app and follow "Step 5: Seed a Demo Attempt" to verify the UI displays correctly.
