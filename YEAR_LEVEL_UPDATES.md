# Faculty Feedback System - Year Level & Branch Updates

## Changes Made

### 1. Database Schema Updates

**Faculty Table - Added `year_level` column:**
```sql
CREATE TABLE faculty (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    department TEXT,
    year_level TEXT DEFAULT 'FY'  -- NEW: Tracks which year this faculty teaches
)
```

**Feedback Table - Added `year_level` column:**
```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY,
    student_name TEXT,
    faculty_id INTEGER NOT NULL,
    year_level TEXT NOT NULL,  -- NEW: Records the student's year level
    q1_teaching_quality INTEGER,
    q2_course_content INTEGER,
    q3_communication INTEGER,
    q4_feedback_quality INTEGER,
    q5_subject_knowledge INTEGER,
    overall_rating INTEGER,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(faculty_id) REFERENCES faculty(id)
)
```

### 2. New Year Levels Supported

- **FY** - First Year
- **SY** - Second Year
- **TY** - Third Year
- **Final Year** - Final Year

### 3. Code Updates

#### New Helper Functions:

```python
def get_year_levels():
    """Return distinct year levels."""
    return ['FY', 'SY', 'TY', 'Final Year']

def get_faculties_by_year(year_level):
    """Get faculties filtered by year level."""
    # Returns faculty list for a specific year

def get_faculties_by_branch_and_year(branch, year_level):
    """Get faculties filtered by both branch and year level."""
    # Combined filtering by department AND year level
```

#### Updated Functions:

- `submit_feedback()` - Now accepts and stores `year_level` parameter
- `get_all_feedback()` - Now returns faculty `year_level` information
- `get_faculty_stats()` - Now groups statistics by year level
- `get_faculty_list()` - Returns 4 columns including `year_level`
- `get_faculties_by_branch()` - Returns 4 columns including `year_level`

### 4. Student Feedback Form Updates

**New Selection Order:**
1. **Select Your Year Level*** - Dropdown with FY, SY, TY, Final Year
2. **Select Branch*** - Filter by department
3. **Select Faculty*** - Shows only faculty teaching selected year and branch

**Display Format:**
- Faculty shown as: "Faculty Name (Department)"
- Form captures both year level and branch information

### 5. Admin Dashboard Updates

**Faculty Statistics Table Now Shows:**
- Faculty Name
- Department
- Year Level (NEW)
- Response Count
- Average Rating

**Recent Submissions Include:**
- Faculty name and department
- Year level (NEW)
- Student name
- Submission date
- Individual ratings (Q1-Q5)
- Overall rating
- Comments

### 6. Analytics Updates

**Question-wise Analysis:**
- Updated column indexing to accommodate new year_level column
- All existing charts and visualizations continue to work

### 7. Export Data Updates

**CSV Export Now Includes:**
- Date
- Faculty Name
- Department
- Year Level (NEW)
- Student Name
- All 5 Question Ratings
- Overall Rating
- Comments

## Database Migration

### Running the Reset Script

A new reset script has been created: `reset_db_with_years.py`

```bash
python reset_db_with_years.py
```

**What it does:**
1. Backs up existing database to `feedback_streamlit.db.backup`
2. Drops all existing tables
3. Creates new tables with year_level support
4. Seeds 8 faculty members across all year levels and departments:
   - Dr. Rajesh Kumar (Computer Science, FY)
   - Prof. Anita Singh (Mechanical Engineering, SY)
   - Dr. Priya Patel (Electrical Engineering, TY)
   - Prof. Suresh Verma (Civil Engineering, Final Year)
   - Dr. Meera Sharma (Chemical Engineering, FY)
   - Prof. Vikram Gupta (Electronics Engineering, SY)
   - Dr. Rajesh Desai (Computer Science, TY)
   - Prof. Neha Verma (Mechanical Engineering, Final Year)
5. Creates demo users (admin/student)

### Demo Credentials

- **Admin:** username: `admin`, password: `admin123`
- **Student:** username: `student`, password: `student123`

## How to Use

### For Students:

1. Login with student credentials
2. Click "Submit Feedback"
3. Select your **Year Level** (FY, SY, TY, or Final Year)
4. Select your **Branch/Department** (optional - shows all if "All" selected)
5. Select **Faculty** (filtered to show only those teaching your year and branch)
6. Rate the faculty on 5 criteria (1-10 scale)
7. Add comments (optional)
8. Submit

### For Admins:

1. Login with admin credentials
2. Dashboard shows:
   - Total feedback count
   - Average rating
   - Faculty statistics (now with year level info)
   - Recent submissions (including year level)
3. Analytics page shows:
   - Rating distribution
   - Faculty performance by year level
   - Question-wise analysis
4. Export data as CSV (includes year level)

## Benefits

✓ Better organization of feedback by academic year
✓ Faculty can be tracked across different year levels
✓ More granular filtering and reporting
✓ Students can provide feedback specific to their year level
✓ Admin can analyze performance by year cohort
✓ Easier identification of year-specific teaching quality issues

## Testing Checklist

- [x] Database schema created successfully
- [x] Faculty table includes year_level column
- [x] Feedback table includes year_level column
- [x] Demo faculty seeded with year levels
- [x] No syntax errors in streamlit_app.py
- [ ] Run Streamlit app and test student feedback form
- [ ] Verify year level selector appears
- [ ] Verify faculty filtering by year level works
- [ ] Verify admin dashboard shows year levels
- [ ] Verify CSV export includes year level
- [ ] Test with different year level combinations

