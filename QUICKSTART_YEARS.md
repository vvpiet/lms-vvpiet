# Quick Start Guide - Year Level & Branch Features

## Setup

1. **Reset Database with Year Level Support**
   ```powershell
   cd C:\Users\ho\Desktop\Feedback
   C:/Users/ho/Desktop/Feedback/venv/Scripts/python.exe reset_db_with_years.py
   ```

2. **Start the Application**
    - Using PowerShell (recommended):
       ```powershell
       cd C:\Users\ho\Desktop\Feedback
       .\run_streamlit.ps1
       ```
    - Or run with the virtual environment's Python:
       ```powershell
       C:/Users/ho/Desktop/Feedback/venv/Scripts/python.exe -m streamlit run streamlit_app.py
       ```

3. **Access the App**
   - Open your browser to `http://localhost:8501`

## Demo Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Student | student | student123 |

## Faculty Assignments by Year & Department

### First Year (FY)
- Dr. Rajesh Kumar (Computer Science)
- Dr. Meera Sharma (Chemical Engineering)

### Second Year (SY)
- Prof. Anita Singh (Mechanical Engineering)
- Prof. Vikram Gupta (Electronics Engineering)

### Third Year (TY)
- Dr. Priya Patel (Electrical Engineering)
- Dr. Rajesh Desai (Computer Science)

### Final Year
- Prof. Suresh Verma (Civil Engineering)
- Prof. Neha Verma (Mechanical Engineering)

## Student Feedback Workflow

```
1. Login as Student
   ↓
2. Click "Submit Feedback"
   ↓
3. Select Year Level (FY/SY/TY/Final Year) *
   ↓
4. Select Branch (Computer Science, etc.) *
   ↓
5. Select Faculty * (filtered by year and branch)
   ↓
6. Rate on 5 dimensions (1-10 scale):
   - Teaching Quality
   - Course Content Clarity
   - Communication Skills
   - Feedback Quality
   - Subject Knowledge
   ↓
7. Overall Rating (1-10)
   ↓
8. Add Comments (optional)
   ↓
9. Submit
```

## Admin Dashboard Features

### Dashboard Tab
- **Metrics**: Total feedbacks, average rating, faculty count
- **Faculty Statistics**: Name, Department, Year Level, Response Count, Avg Rating
- **Recent Submissions**: Last 10 feedbacks with full details including year level

### Analytics Tab
- **Rating Distribution**: Histogram of all ratings
- **Faculty Performance**: Average rating by faculty
- **Question-wise Analysis**: Average rating for each of the 5 questions

### Export Data Tab
- **CSV Download**: Export all feedback data with year level information
- **Data Preview**: View the data before downloading

## Database Schema

### Faculty Table
```
id (INTEGER, PRIMARY KEY)
name (TEXT, UNIQUE)
department (TEXT)
year_level (TEXT)  -- FY, SY, TY, Final Year
```

### Feedback Table
```
id (INTEGER, PRIMARY KEY)
student_name (TEXT)
faculty_id (INTEGER, FOREIGN KEY)
year_level (TEXT)  -- Student's year level
q1_teaching_quality (INTEGER, 1-10)
q2_course_content (INTEGER, 1-10)
q3_communication (INTEGER, 1-10)
q4_feedback_quality (INTEGER, 1-10)
q5_subject_knowledge (INTEGER, 1-10)
overall_rating (INTEGER, 1-10)
comments (TEXT)
created_at (TIMESTAMP)
```

## Key Features

✓ **Multi-dimensional Feedback**: 5 specific criteria + overall rating
✓ **Year-based Filtering**: Separate feedback collection by academic year
✓ **Department Filtering**: Filter by engineering branch/department
✓ **Real-time Analytics**: Charts and statistics for admin
✓ **Data Export**: CSV format for further analysis
✓ **User Authentication**: Student and Admin roles
✓ **Anonymous Feedback**: Students can submit anonymously

## Troubleshooting

### Issue: "No module named streamlit"
**Solution:**
```bash
C:/Users/ho/Desktop/Feedback/venv/Scripts/python.exe -m pip install streamlit pandas numpy matplotlib openpyxl
```

### Issue: "table feedback has no column named year_level"
**Solution:**
```bash
C:/Users/ho/Desktop/Feedback/venv/Scripts/python.exe reset_db_with_years.py
```

### Issue: Faculty not showing up in dropdown
**Check:**
1. Verify year level is selected
2. Try selecting "All" for branch
3. Check database was reset properly
4. Faculty must have a matching year_level in database

## File Changes Summary

| File | Changes |
|------|---------|
| `streamlit_app.py` | Added year level support, updated functions, modified UI forms |
| `reset_db_with_years.py` | New script to initialize DB with year level schema |
| `YEAR_LEVEL_UPDATES.md` | Detailed changelog |
| `feedback_streamlit.db` | Database file (auto-created on first run) |

## Support

For detailed information, see:
- `YEAR_LEVEL_UPDATES.md` - Complete changelog and technical details
- `README.md` - Original project documentation

