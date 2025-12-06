
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from zoneinfo import ZoneInfo

def parse_iso_to_kolkata(dt_str_or_obj):
    """Parse an ISO string or datetime and return a tz-aware datetime in Asia/Kolkata."""
    if not dt_str_or_obj:
        return None
    if isinstance(dt_str_or_obj, str):
        try:
            dt = datetime.fromisoformat(dt_str_or_obj)
        except Exception:
            return None
    else:
        dt = dt_str_or_obj
    # Attach timezone if naive or convert to Asia/Kolkata
    if dt.tzinfo is None:
        return dt.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
    else:
        return dt.astimezone(ZoneInfo("Asia/Kolkata"))
import json
import base64
import sqlite3
import hashlib
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from io import BytesIO

def generate_application_documentation():
    """Generate a comprehensive PDF documentation of the application."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.5*inch, leftMargin=0.5*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#8B3A3A'),
        spaceAfter=6,
        alignment=1  # Center
    )
    
    # Heading style
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=6,
        spaceBefore=12
    )
    
    # Normal text style
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        leading=14
    )
    
    # Add title
    elements.append(Paragraph("VVP Institute of Engineering and Technology", title_style))
    elements.append(Paragraph("Student Learning Management System - Documentation", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Overview
    elements.append(Paragraph("<b>Application Overview</b>", heading_style))
    elements.append(Paragraph(
        "The VVP Institute Student Learning Management System (LMS) is a comprehensive platform designed to facilitate "
        "academic interactions between students, faculty, and administrators. This system provides tools for attendance tracking, "
        "resource management, testing, and feedback collection.",
        normal_style
    ))
    elements.append(Spacer(1, 0.1*inch))
    
    # Key Features
    elements.append(Paragraph("<b>Key Features</b>", heading_style))
    features = [
        "<b>Student Dashboard:</b> Centralized access to attendance, resources, tests, and feedback submission",
        "<b>Faculty Management:</b> Mark daily attendance, maintain daily lecture records (LER), and upload course materials",
        "<b>Admin Controls:</b> Manage subjects, faculty, student roster, view analytics, and export data",
        "<b>Attendance Tracking:</b> Daily attendance recording with monthly rollups and academic-year based calculations",
        "<b>Online Testing:</b> Create and administer tests with automatic scoring",
        "<b>Resource Management:</b> Upload and organize assignments, notes, and other course materials",
        "<b>Feedback System:</b> Comprehensive 10-question faculty feedback form with scheduled submission windows",
        "<b>Leave Management:</b> Faculty leave requests and tracking with automatic annual reset",
        "<b>Academic Year Support:</b> Automatic handling of academic years (July 1 - June 30)"
    ]
    for feature in features:
        elements.append(Paragraph(f"• {feature}", normal_style))
    
    elements.append(Spacer(1, 0.15*inch))
    
    # User Roles
    elements.append(Paragraph("<b>User Roles and Responsibilities</b>", heading_style))
    
    # Students
    elements.append(Paragraph("<b><u>Students</u></b>", styles['Heading3']))
    student_features = [
        "View personal attendance percentage and detailed attendance records",
        "Access course materials (assignments, notes) organized by year level and semester",
        "Submit faculty feedback (during scheduled feedback windows)",
        "Take online tests and view attempts/scores",
        "Calculate academic credits using the credit calculator",
        "Download resources uploaded by faculty"
    ]
    for feature in student_features:
        elements.append(Paragraph(f"• {feature}", normal_style))
    
    elements.append(Spacer(1, 0.1*inch))
    
    # Faculty
    elements.append(Paragraph("<b><u>Faculty Members</u></b>", styles['Heading3']))
    faculty_features = [
        "Mark daily attendance for students",
        "Record Daily Lecture Entry (LER) with topics, lecture numbers, and syllabus coverage",
        "Create and manage online tests",
        "Upload course materials (assignments, notes)",
        "Request leave with alternative faculty assignment",
        "View their feedback from students and department statistics"
    ]
    for feature in faculty_features:
        elements.append(Paragraph(f"• {feature}", normal_style))
    
    elements.append(Spacer(1, 0.1*inch))
    
    # Admin
    elements.append(Paragraph("<b><u>Administrators</u></b>", styles['Heading3']))
    admin_features = [
        "Manage subjects and assign faculty to subjects",
        "Manage faculty profiles and departments",
        "Upload and manage student roster (Excel/CSV format)",
        "View student attendance and generate reports",
        "View and export feedback data",
        "Set feedback submission windows",
        "Manage faculty leaves and absences",
        "Export Daily LER records",
        "Access analytics and system statistics"
    ]
    for feature in admin_features:
        elements.append(Paragraph(f"• {feature}", normal_style))
    
    elements.append(PageBreak())
    
    # Feedback System
    elements.append(Paragraph("<b>Feedback System - 10-Question Rubric</b>", heading_style))
    questions = [
        "1. Has fundamental concepts & subject knowledge",
        "2. Preparation for Subject is sufficient while coming to class",
        "3. Sufficient knowledge about current trends/development of subject",
        "4. Proficient in English & communication skills",
        "5. Teaching makes class interesting & interactive through student participation",
        "6. Faculty is punctual in starting and ending classes on time",
        "7. Has covered the entire syllabus as prescribed by university",
        "8. Extent of fulfillment of your learning expectations",
        "9. Behavior with students is appropriate and rational",
        "10. Motivates students for their study and better career"
    ]
    for q in questions:
        elements.append(Paragraph(f"• {q}", normal_style))
    
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("Each question is rated on a scale of 1-10 (1=Strongly Disagree, 10=Strongly Agree).", normal_style))
    
    elements.append(Spacer(1, 0.15*inch))
    
    # Attendance
    elements.append(Paragraph("<b>Attendance Tracking</b>", heading_style))
    elements.append(Paragraph(
        "• Attendance is tracked daily for each student per faculty member and subject\n"
        "• Monthly attendance records are automatically aggregated\n"
        "• Academic Year calculation: July 1 - June 30 (resets annually)\n"
        "• Students need >= 60% attendance to submit feedback\n"
        "• Attendance percentage is displayed to students in real-time",
        normal_style
    ))
    
    elements.append(Spacer(1, 0.15*inch))
    
    # Academic Year
    elements.append(Paragraph("<b>Academic Year System</b>", heading_style))
    elements.append(Paragraph(
        "The system follows the Indian academic year calendar:\n"
        "• Academic Year runs from July 1 to June 30\n"
        "• Leave balances reset automatically at the start of each academic year\n"
        "• Reports and statistics are organized by academic year\n"
        "• Year Level: FY (First Year), SY (Second Year), TY (Third Year), Final Year",
        normal_style
    ))
    
    elements.append(Spacer(1, 0.15*inch))
    
    # Technical Details
    elements.append(Paragraph("<b>Technical Details</b>", heading_style))
    elements.append(Paragraph(
        "• Platform: Streamlit (Python web framework)\n"
        "• Database: SQLite3\n"
        "• Timezone: Asia/Kolkata (IST)\n"
        "• Authentication: Username/Password with SHA256 hashing\n"
        "• Data Format: ISO 8601 timestamps with timezone awareness",
        normal_style
    ))
    
    elements.append(Spacer(1, 0.15*inch))
    
    # Support & Contact
    elements.append(Paragraph("<b>Support & Contact</b>", heading_style))
    elements.append(Paragraph(
        "For assistance or issues, please contact:\n"
        "<b>Prof. Amir M. Usman Wagdarikar</b>\n"
        "Assistant Professor, Electronics and Telecommunication Engineering\n"
        "VVP Institute of Engineering and Technology, Solapur, Maharashtra, India",
        normal_style
    ))
    
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(f"<i>Documentation generated on {datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')}</i>", normal_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

# Database setup
DB_PATH = "feedback_streamlit.db"

def init_database():
    """Initialize SQLite database with all tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'student',
            faculty_id INTEGER,
            name TEXT,
            branch TEXT,
            class TEXT,
            FOREIGN KEY(faculty_id) REFERENCES faculty(id)
        )
    ''')
    
    # Faculty table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT,
            year_level TEXT DEFAULT 'FY'
        )
    ''')

    # Assignment submissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignment_submissions (
            id INTEGER PRIMARY KEY,
            assignment_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            submission_file TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(assignment_id) REFERENCES faculty_resources(id),
            FOREIGN KEY(student_id) REFERENCES users(id)
        )
    ''')

    conn.commit()

    # Attendance tracking table (monthly)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            faculty_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            academic_year TEXT,
            classes_attended INTEGER DEFAULT 0,
            total_classes INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(student_id) REFERENCES users(id),
            FOREIGN KEY(faculty_id) REFERENCES faculty(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id),
            UNIQUE(student_id, faculty_id, subject_id, month, academic_year)
        )
    ''')
    conn.commit()

    # No default subjects are seeded. Subjects should be added by admin via the Manage Subjects page.
    # Existing faculty_subject mappings are left unchanged.
    # Additional tables: feedback scheduling, daily attendance, tests and related tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback_schedule (
            id INTEGER PRIMARY KEY,
            start_ts TIMESTAMP NOT NULL,
            end_ts TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_attendance (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            faculty_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            date DATE NOT NULL,
            present INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(student_id, faculty_id, subject_id, date),
            FOREIGN KEY(student_id) REFERENCES users(id),
            FOREIGN KEY(faculty_id) REFERENCES faculty(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    ''')

    # Daily lecture entry (Daily LER) recorded by faculty
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_ler (
            id INTEGER PRIMARY KEY,
            faculty_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            date DATE NOT NULL,
            time TEXT,
            topic TEXT,
            lecture_number TEXT,
            percent_syllabus REAL,
            total_present INTEGER,
            absent_roll_numbers TEXT,
            sign TEXT,
            remark TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(faculty_id) REFERENCES faculty(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tests (
            id INTEGER PRIMARY KEY,
            faculty_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            title TEXT,
            description TEXT,
            start_ts TIMESTAMP,
            end_ts TIMESTAMP,
            proctored INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(faculty_id) REFERENCES faculty(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_questions (
            id INTEGER PRIMARY KEY,
            test_id INTEGER NOT NULL,
            question_text TEXT,
            choices TEXT,
            correct_choice INTEGER,
            marks INTEGER DEFAULT 1,
            FOREIGN KEY(test_id) REFERENCES tests(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_attempts (
            id INTEGER PRIMARY KEY,
            test_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            answers TEXT,
            score REAL,
            started_at TIMESTAMP,
            submitted_at TIMESTAMP,
            FOREIGN KEY(test_id) REFERENCES tests(id),
            FOREIGN KEY(student_id) REFERENCES users(id)
        )
    ''')

    # Notices table: Admin and Faculty can post notices for students
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            target_branch TEXT,
            target_class TEXT,
            created_by_role TEXT,
            created_by_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Faculty leaves: track leaves requested / taken by faculty
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty_leaves (
            id INTEGER PRIMARY KEY,
            faculty_id INTEGER NOT NULL,
            leave_type TEXT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            is_half_day INTEGER DEFAULT 0,
            days_count INTEGER DEFAULT 1,
            alt_faculty TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(faculty_id) REFERENCES faculty(id)
        )
    ''')

    conn.commit()
    
    # Add default users if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        def hash_password(pwd):
            return hashlib.sha256(pwd.encode()).hexdigest()
        
        cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                      ('admin', hash_password('admin123'), 'admin'))
        cursor.execute('INSERT INTO users (username, password, role, faculty_id) VALUES (?, ?, ?, ?)',
                      ('rajesh_kumar', hash_password('faculty123'), 'faculty', 1))
        cursor.execute('INSERT INTO users (username, password, role, faculty_id) VALUES (?, ?, ?, ?)',
                      ('anita_singh', hash_password('faculty123'), 'faculty', 2))
        cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                      ('student', hash_password('student123'), 'student'))
        conn.commit()
    
    # Ensure users table has attendance and has_access columns (for existing DBs)
    cursor.execute("PRAGMA table_info(users)")
    cols = [row[1] for row in cursor.fetchall()]
    if 'attendance' not in cols:
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN attendance INTEGER DEFAULT 0")
        except Exception:
            pass
    if 'has_access' not in cols:
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN has_access INTEGER DEFAULT 0")
        except Exception:
            pass
    if 'name' not in cols:
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN name TEXT")
        except Exception:
            pass
    if 'branch' not in cols:
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN branch TEXT")
        except Exception:
            pass
    if 'class' not in cols:
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN class TEXT")
        except Exception:
            pass
    if 'roll_number' not in cols:
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN roll_number TEXT")
        except Exception:
            pass
    conn.commit()
    conn.close()

    # Ensure feedback table exists with up to 10 question columns (backfill/alter for older DBs)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            student_name TEXT,
            faculty_id INTEGER,
            subject_id INTEGER,
            year_level TEXT,
            q1 INTEGER,
            q2 INTEGER,
            q3 INTEGER,
            q4 INTEGER,
            q5 INTEGER,
            q6 INTEGER,
            q7 INTEGER,
            q8 INTEGER,
            q9 INTEGER,
            q10 INTEGER,
            overall_rating INTEGER,
            comments TEXT,
            FOREIGN KEY(faculty_id) REFERENCES faculty(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    ''')
    conn.commit()

    # Add missing columns for older DBs (ensure q1..q10 and rating/comment fields exist)
    cursor.execute("PRAGMA table_info(feedback)")
    existing_cols = [r[1] for r in cursor.fetchall()]
    required_cols = {
        'student_name': 'TEXT',
        'faculty_id': 'INTEGER',
        'year_level': 'TEXT',
        'q1': 'INTEGER', 'q2': 'INTEGER', 'q3': 'INTEGER', 'q4': 'INTEGER', 'q5': 'INTEGER',
        'q6': 'INTEGER', 'q7': 'INTEGER', 'q8': 'INTEGER', 'q9': 'INTEGER', 'q10': 'INTEGER',
        'overall_rating': 'INTEGER',
        'comments': 'TEXT'
    }
    for col, coltype in required_cols.items():
        if col not in existing_cols:
            try:
                cursor.execute(f'ALTER TABLE feedback ADD COLUMN {col} {coltype}')
                conn.commit()
            except Exception:
                # If ALTER fails (e.g., read-only DB), ignore and continue
                pass
    conn.close()

def hash_password(password):
    """Hash password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


def reset_user_password_with_roll(username, roll_number, new_password):
    """Reset a user's password after verifying their roll number.
    Returns True on success, False otherwise."""
    if not username or not roll_number or not new_password:
        return False
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id FROM users WHERE username = ? AND roll_number = ? AND role = ?', (username, roll_number, 'student'))
        row = cursor.fetchone()
        if not row:
            # Try any role match if student match not found
            cursor.execute('SELECT id FROM users WHERE username = ? AND roll_number = ?', (username, roll_number))
            row = cursor.fetchone()
            if not row:
                conn.close()
                return False

        uid = row[0]
        cursor.execute('UPDATE users SET password = ? WHERE id = ?', (hash_password(new_password), uid))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


def safe_rerun():
    """Try to rerun the Streamlit app. Fallbacks if API unavailable."""
    try:
        # Preferred API (may not exist in some streamlit builds)
        st.experimental_rerun()
        return
    except Exception:
        pass

    try:
        # Another possible API alias used in some versions
        st.rerun()
        return
    except Exception:
        pass

    # Fallback: tweak query params to force a reload
    try:
        params = st.experimental_get_query_params()
        params['_refresh'] = datetime.now().timestamp()
        st.experimental_set_query_params(**params)
        return
    except Exception:
        pass

    # Last resort: toggle a session_state flag and stop
    st.session_state['_rerun_toggle'] = not st.session_state.get('_rerun_toggle', False)
    st.stop()

def verify_login(username, password):
    """Verify user login credentials."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, role FROM users WHERE username = ? AND password = ?',
                  (username, hash_password(password)))
    result = cursor.fetchone()
    conn.close()
    return result

def get_faculty_list():
    """Get all faculty members."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, department, year_level FROM faculty ORDER BY name')
    faculties = cursor.fetchall()
    conn.close()
    return faculties


def get_branches():
    """Return distinct engineering branches (department values)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT department FROM faculty WHERE department IS NOT NULL ORDER BY department")
    branches = [row[0] for row in cursor.fetchall()]
    conn.close()
    return branches


def get_year_levels():
    """Return distinct year levels."""
    return ['FY', 'SY', 'TY', 'Final Year']


def get_faculties_by_branch(branch):
    """Get faculties filtered by branch/department."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, department, year_level FROM faculty WHERE department = ? ORDER BY name', (branch,))
    faculties = cursor.fetchall()
    conn.close()
    return faculties


def get_faculties_by_year(year_level):
    """Get faculties filtered by year level."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, department, year_level FROM faculty WHERE year_level = ? ORDER BY name', (year_level,))
    faculties = cursor.fetchall()
    conn.close()
    return faculties


def get_faculties_by_branch_and_year(branch, year_level):
    """Get faculties filtered by both branch and year level."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Check faculty_year_level table for year level assignment
    cursor.execute('''
        SELECT DISTINCT fac.id, fac.name, fac.department, fac.year_level 
        FROM faculty fac
        LEFT JOIN faculty_year_level fyl ON fac.id = fyl.faculty_id
        WHERE fac.department = ? AND (fyl.year_level = ? OR fac.year_level = ?)
        ORDER BY fac.name
    ''', (branch, year_level, year_level))
    faculties = cursor.fetchall()
    conn.close()
    return faculties


def get_subjects_by_year(year_level):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, year_level, department, code FROM subjects WHERE year_level = ? ORDER BY name', (year_level,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_faculties_by_subject(subject_id, branch=None, year_level=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = '''
        SELECT DISTINCT fac.id, fac.name, fac.department, fac.year_level
        FROM faculty fac
        JOIN faculty_subject fs ON fac.id = fs.faculty_id
        LEFT JOIN faculty_year_level fyl ON fac.id = fyl.faculty_id
        WHERE fs.subject_id = ?
    '''
    params = [subject_id]
    if year_level:
        query += ' AND (fyl.year_level = ? OR fac.year_level = ?)'
        params.append(year_level)
        params.append(year_level)
    if branch and branch != 'All':
        query += ' AND fac.department = ?'
        params.append(branch)
    query += ' ORDER BY fac.name'
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_faculty_year_level(faculty_id, new_year_level):
    """Update faculty's primary year level."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE faculty SET year_level = ? WHERE id = ?', (new_year_level, faculty_id))
    conn.commit()
    conn.close()

def add_faculty_year_level(faculty_id, year_level):
    """Add a year level assignment to faculty."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO faculty_year_level (faculty_id, year_level) VALUES (?, ?)', 
                      (faculty_id, year_level))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Already exists
    conn.close()

def get_faculty_year_levels(faculty_id):
    """Get all year levels a faculty teaches."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT year_level FROM faculty_year_level WHERE faculty_id = ? ORDER BY year_level', 
                  (faculty_id,))
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows] if rows else []

def remove_faculty_year_level(faculty_id, year_level):
    """Remove a year level assignment from faculty."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM faculty_year_level WHERE faculty_id = ? AND year_level = ?', 
                  (faculty_id, year_level))
    conn.commit()
    conn.close()

def get_all_faculty():
    """Get all faculty with their details."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, department, year_level FROM faculty ORDER BY name')
    rows = cursor.fetchall()
    conn.close()
    return rows

def calculate_credit_progress(completed, semester, required):
    """Calculate total credits after this semester and percentage progress.

    Returns a tuple (total_after_semester, percent_complete).
    """
    try:
        completed = float(completed)
        semester = float(semester)
        required = float(required)
    except Exception:
        return (0, 0.0)

    total_after = completed + semester
    percent = (total_after / required) * 100 if required else 0.0
    return (int(total_after), float(percent))

def add_faculty_resource(faculty_id, subject_id, resource_type, filename, file_path, deadline=None):
    """Insert a new assignment or notes resource."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO faculty_resources (faculty_id, subject_id, resource_type, filename, file_path, deadline)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (faculty_id, subject_id, resource_type, filename, file_path, deadline))
        conn.commit()
        rid = cursor.lastrowid
        conn.close()
        return rid
    except Exception as e:
        conn.close()
        return None

def get_faculty_resources(faculty_id, subject_id=None, resource_type=None):
    """Get resources uploaded by a faculty member."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = 'SELECT id, subject_id, resource_type, filename, uploaded_at, deadline FROM faculty_resources WHERE faculty_id = ?'
    params = [faculty_id]
    if subject_id:
        query += ' AND subject_id = ?'
        params.append(subject_id)
    if resource_type:
        query += ' AND resource_type = ?'
        params.append(resource_type)
    query += ' ORDER BY uploaded_at DESC'
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_subject_resources_for_student(year_level, department, resource_type=None):
    """Get resources (assignments/notes) for a student's year level and department."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = '''
        SELECT fr.id, fr.filename, fr.resource_type, s.name, f.name, fr.uploaded_at, fr.deadline
        FROM faculty_resources fr
        JOIN subjects s ON fr.subject_id = s.id
        JOIN faculty f ON fr.faculty_id = f.id
        WHERE s.year_level = ? AND s.department = ?
    '''
    params = [year_level, department]
    if resource_type:
        query += ' AND fr.resource_type = ?'
        params.append(resource_type)
    query += ' ORDER BY fr.uploaded_at DESC'
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_subject(subject_id):
    """Delete a subject and its faculty_subject mappings."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM faculty_subject WHERE subject_id = ?', (subject_id,))
        cursor.execute('DELETE FROM subjects WHERE id = ?', (subject_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False

def submit_feedback(student_name, faculty_id, subject_id, year_level, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, overall, comments):
    """Submit feedback to database with subject tracking (stores up to 10 question ratings)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (student_name, faculty_id, subject_id, year_level, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, overall_rating, comments)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (student_name or 'Anonymous', faculty_id, subject_id, year_level, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, overall, comments))
    conn.commit()
    conn.close()
    return True

def get_all_feedback():
    """Get all feedback with faculty names and the specific subject feedback was about."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
         SELECT f.id, f.created_at, fac.name, fac.department, fac.year_level, f.student_name,
             f.q1, f.q2, f.q3, f.q4, f.q5, f.q6, f.q7, f.q8, f.q9, f.q10, f.overall_rating, f.comments,
             COALESCE(s.name, 'Not Specified') as subject
        FROM feedback f
        JOIN faculty fac ON f.faculty_id = fac.id
        LEFT JOIN subjects s ON f.subject_id = s.id
        ORDER BY f.created_at DESC
    ''')
    feedbacks = cursor.fetchall()
    conn.close()
    return feedbacks

def get_faculty_stats():
    """Get statistics by faculty."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT fac.name, fac.department, fac.year_level, COUNT(f.id) as count, AVG(f.overall_rating) as avg_rating
        FROM feedback f
        JOIN faculty fac ON f.faculty_id = fac.id
        GROUP BY f.faculty_id, fac.name, fac.department, fac.year_level
        ORDER BY fac.name
    ''')
    stats = cursor.fetchall()
    conn.close()
    return stats


def get_user_by_username(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, role, attendance, has_access FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_db_connection():
    """Get a database connection."""
    return sqlite3.connect(DB_PATH)

def get_all_students():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, attendance, has_access FROM users WHERE role = 'student' ORDER BY username")
    rows = cursor.fetchall()
    conn.close()
    return rows


def set_student_access(user_id, value):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET has_access = ? WHERE id = ?', (1 if value else 0, user_id))
    conn.commit()
    conn.close()


def update_student_attendance(user_id, attendance):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET attendance = ? WHERE id = ?', (int(attendance), user_id))
    conn.commit()
    conn.close()

def get_faculty_by_user(faculty_user_id):
    """Get faculty record linked to a faculty user account."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT faculty_id FROM users WHERE id = ? AND role = ?', (faculty_user_id, 'faculty'))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_faculty_details(faculty_user_id):
    """Get complete faculty details including department/branch."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT u.faculty_id, f.name, f.department FROM users u JOIN faculty f ON u.faculty_id = f.id WHERE u.id = ? AND u.role = ?', (faculty_user_id, 'faculty'))
    result = cursor.fetchone()
    conn.close()
    return result  # Returns (faculty_id, name, department) or None

def get_faculty_subjects(faculty_id):
    """Get subjects taught by a faculty member."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT s.id, s.name, s.year_level FROM subjects s
                      JOIN faculty_subject fs ON s.id = fs.subject_id
                      WHERE fs.faculty_id = ? ORDER BY s.year_level, s.name''', (faculty_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_students_by_year_and_branch(year_level=None, branch=None):
    """Get all students (can filter by year/branch if stored in users table)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE role = 'student' ORDER BY username")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_students_by_branch_and_class(branch=None, class_level=None):
    """Get students filtered by branch and class/year level, including roll_number."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = "SELECT id, username, name, roll_number, branch, class FROM users WHERE role = 'student'"
    params = []
    
    if branch and branch != "All":
        query += " AND branch = ?"
        params.append(branch)
    if class_level and class_level != "All":
        query += " AND class = ?"
        params.append(class_level)
    
    query += " ORDER BY name"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

def save_attendance(student_id, faculty_id, subject_id, month, year, classes_attended, total_classes):
    """Save or update student attendance record."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Compute academic year string from calendar month/year. Academic year runs from July 1 -> June 30.
    try:
        m = int(month)
        y = int(year)
    except Exception:
        m = int(month) if month else 1
        y = int(year) if year else datetime.now(ZoneInfo("Asia/Kolkata")).year

    # Determine academic year start
    if m >= 7:
        ay_start = y
        ay_end = y + 1
    else:
        ay_start = y - 1
        ay_end = y
    academic_year = f"{ay_start}-{ay_end}"

    cursor.execute('''INSERT OR REPLACE INTO attendance 
                      (student_id, faculty_id, subject_id, month, year, academic_year, classes_attended, total_classes, updated_at)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)''',
                   (student_id, faculty_id, subject_id, month, year, academic_year, classes_attended, total_classes))
    conn.commit()
    conn.close()

def get_attendance_for_month(faculty_id, subject_id, month, year):
    """Get all attendance records for a faculty's subject for a specific month."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Use academic_year mapping so that month/year are interpreted within the academic year (Jul-Jun)
    try:
        m = int(month)
        y = int(year)
    except Exception:
        m = int(month) if month else 1
        y = int(year) if year else datetime.now(ZoneInfo("Asia/Kolkata")).year

    if m >= 7:
        ay_start = y
        ay_end = y + 1
    else:
        ay_start = y - 1
        ay_end = y
    academic_year = f"{ay_start}-{ay_end}"

    cursor.execute('''SELECT student_id, classes_attended, total_classes FROM attendance
                      WHERE faculty_id = ? AND subject_id = ? AND month = ? AND academic_year = ?
                      ORDER BY student_id''',
                   (faculty_id, subject_id, month, academic_year))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_student_attendance_percentage(student_id):
    """Calculate overall attendance percentage for a student."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT COALESCE(SUM(classes_attended), 0) as attended, COALESCE(SUM(total_classes), 0) as total
                      FROM attendance WHERE student_id = ?''', (student_id,))
    result = cursor.fetchone()
    conn.close()
    if result and result[1] > 0:
        return round((result[0] / result[1]) * 100, 2)
    return 0

def get_attendance_by_year_and_branch(year_level=None, branch=None):
    """Get all attendance records with student info, grouped by year/branch."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = '''SELECT u.id, u.username, a.classes_attended, a.total_classes, s.name, f.name as faculty_name, f.department
               FROM attendance a
               JOIN users u ON a.student_id = u.id
               JOIN subjects s ON a.subject_id = s.id
               JOIN faculty f ON a.faculty_id = f.id
               WHERE 1=1'''
    params = []
    if year_level:
        query += ' AND s.year_level = ?'
        params.append(year_level)
    if branch:
        query += ' AND f.department = ?'
        params.append(branch)
    query += ' ORDER BY f.department, s.year_level, u.username'
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_monthly_attendance_rollup(faculty_id, subject_id, month, year):
    """Compute a monthly attendance rollup from daily_attendance table for given faculty, subject, month/year."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # We will count number of present days per student and total distinct dates recorded
    month_prefix = f"{year:04d}-{month:02d}-"
    cursor.execute('''SELECT student_id, SUM(present) as classes_attended, COUNT(DISTINCT date) as total_classes
                      FROM daily_attendance
                      WHERE faculty_id = ? AND subject_id = ? AND date LIKE ?
                      GROUP BY student_id
                      ORDER BY student_id''', (faculty_id, subject_id, month_prefix + '%'))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_present_student_ids_for_date(faculty_id, subject_id, date_str):
    """Return set of student_ids marked present for a given faculty/subject/date."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT student_id FROM daily_attendance WHERE faculty_id = ? AND subject_id = ? AND date = ? AND present = 1''', (faculty_id, subject_id, date_str))
    rows = cursor.fetchall()
    conn.close()
    return set(r[0] for r in rows)


def save_daily_ler(faculty_id, subject_id, date_str, time_str, topic, lecture_number, percent_syllabus, total_present, absent_roll_numbers, sign, remark):
    """Save a Daily LER entry to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO daily_ler (faculty_id, subject_id, date, time, topic, lecture_number, percent_syllabus, total_present, absent_roll_numbers, sign, remark)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (faculty_id, subject_id, date_str, time_str, topic, str(lecture_number), percent_syllabus, total_present, absent_roll_numbers, sign, remark))
    conn.commit()
    lid = cursor.lastrowid
    conn.close()
    return lid


def get_daily_ler_for_faculty(faculty_id, date_from=None, date_to=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if date_from and date_to:
        cursor.execute('''SELECT dl.id, dl.faculty_id, dl.subject_id, dl.date, dl.time, dl.topic, dl.lecture_number, dl.percent_syllabus, dl.total_present, dl.absent_roll_numbers, dl.sign, dl.remark, dl.created_at, f.name, s.name
                          FROM daily_ler dl
                          JOIN faculty f ON dl.faculty_id = f.id
                          JOIN subjects s ON dl.subject_id = s.id
                          WHERE dl.faculty_id = ? AND dl.date BETWEEN ? AND ? ORDER BY dl.date DESC''', (faculty_id, date_from, date_to))
    else:
        cursor.execute('''SELECT dl.id, dl.faculty_id, dl.subject_id, dl.date, dl.time, dl.topic, dl.lecture_number, dl.percent_syllabus, dl.total_present, dl.absent_roll_numbers, dl.sign, dl.remark, dl.created_at, f.name, s.name
                          FROM daily_ler dl
                          JOIN faculty f ON dl.faculty_id = f.id
                          JOIN subjects s ON dl.subject_id = s.id
                          WHERE dl.faculty_id = ? ORDER BY dl.date DESC''', (faculty_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_all_daily_ler(date_from=None, date_to=None, faculty_id=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = '''SELECT dl.id, dl.faculty_id, f.name as faculty_name, dl.subject_id, s.name as subject_name, dl.date, dl.time, dl.topic, dl.lecture_number, dl.percent_syllabus, dl.total_present, dl.absent_roll_numbers, dl.sign, dl.remark, dl.created_at
               FROM daily_ler dl
               JOIN faculty f ON dl.faculty_id = f.id
               JOIN subjects s ON dl.subject_id = s.id
               WHERE 1=1'''
    params = []
    if faculty_id:
        query += ' AND dl.faculty_id = ?'
        params.append(faculty_id)
    if date_from and date_to:
        query += ' AND dl.date BETWEEN ? AND ?'
        params.append(date_from)
        params.append(date_to)
    query += ' ORDER BY dl.date DESC'
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_faculty_with_users():
    """Get all faculty members with their user info."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT f.id, f.name, f.department, u.username 
                      FROM faculty f
                      LEFT JOIN users u ON f.id = u.faculty_id AND u.role = 'faculty'
                      ORDER BY f.name''')
    rows = cursor.fetchall()
    conn.close()
    return rows


### New helper functions: feedback scheduling, daily attendance and tests ###
def schedule_feedback(start_ts, end_ts):
    """Admin: schedule feedback availability."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Store ISO-8601 timezone-aware strings; start_ts/end_ts should be isoformat strings
    cursor.execute('INSERT INTO feedback_schedule (start_ts, end_ts) VALUES (?, ?)', (start_ts, end_ts))
    conn.commit()
    conn.close()

def get_current_feedback_schedule():
    """Return the latest feedback schedule (start_ts, end_ts) or None."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT start_ts, end_ts FROM feedback_schedule ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    return row

def is_feedback_open(now_ts=None):
    """Return True if there is an active feedback schedule covering now_ts (or current time)."""
    if now_ts is None:
        now_ts = datetime.now(ZoneInfo("Asia/Kolkata"))
    sched = get_current_feedback_schedule()
    if not sched:
        return False
    start_ts, end_ts = sched
    try:
        start = parse_iso_to_kolkata(start_ts) if isinstance(start_ts, str) or start_ts else None
        end = parse_iso_to_kolkata(end_ts) if isinstance(end_ts, str) or end_ts else None
    except Exception:
        return False
    return start <= now_ts <= end

def save_daily_attendance(student_id, faculty_id, subject_id, date_str, present):
    """Save or update daily attendance for a student on a date (YYYY-MM-DD)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Try to update first
    cursor.execute('''UPDATE daily_attendance SET present = ?, created_at = CURRENT_TIMESTAMP
                      WHERE student_id = ? AND faculty_id = ? AND subject_id = ? AND date = ?''',
                   (1 if present else 0, student_id, faculty_id, subject_id, date_str))
    if cursor.rowcount == 0:
        # No row updated, insert new
        cursor.execute('''INSERT INTO daily_attendance (student_id, faculty_id, subject_id, date, present, created_at)
                          VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)''',
                       (student_id, faculty_id, subject_id, date_str, 1 if present else 0))
    conn.commit()
    conn.close()

def get_daily_attendance_for_student(student_id, date_str=None):
    """Return daily attendance records for a student; optionally filter by date (YYYY-MM-DD)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if date_str:
        cursor.execute('SELECT faculty_id, subject_id, date, present FROM daily_attendance WHERE student_id = ? AND date = ? ORDER BY date DESC', (student_id, date_str))
    else:
        cursor.execute('SELECT faculty_id, subject_id, date, present FROM daily_attendance WHERE student_id = ? ORDER BY date DESC LIMIT 30', (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def create_test(faculty_id, subject_id, title, description, start_ts=None, end_ts=None, proctored=False):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Ensure start_ts and end_ts, when provided, are stored as timezone-aware ISO strings (Asia/Kolkata)
    try:
        if start_ts:
            dt = start_ts if isinstance(start_ts, datetime) else datetime.fromisoformat(start_ts)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
            start_ts_to_store = dt.isoformat()
        else:
            start_ts_to_store = None
    except Exception:
        start_ts_to_store = start_ts
    try:
        if end_ts:
            dt2 = end_ts if isinstance(end_ts, datetime) else datetime.fromisoformat(end_ts)
            if dt2.tzinfo is None:
                dt2 = dt2.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
            end_ts_to_store = dt2.isoformat()
        else:
            end_ts_to_store = None
    except Exception:
        end_ts_to_store = end_ts

    cursor.execute('''INSERT INTO tests (faculty_id, subject_id, title, description, start_ts, end_ts, proctored)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (faculty_id, subject_id, title, description, start_ts_to_store, end_ts_to_store, 1 if proctored else 0))
    conn.commit()
    tid = cursor.lastrowid
    conn.close()
    return tid

def add_test_question(test_id, question_text, choices_list, correct_index, marks=1):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    choices_json = json.dumps(choices_list)
    cursor.execute('''INSERT INTO test_questions (test_id, question_text, choices, correct_choice, marks)
                      VALUES (?, ?, ?, ?, ?)''', (test_id, question_text, choices_json, int(correct_index), marks))
    conn.commit()
    qid = cursor.lastrowid
    conn.close()
    return qid

def get_tests_for_student(student_id):
    """Return tests relevant for a student by matching subject.year_level and department to student's class/branch.
    Only returns tests whose start_ts/end_ts exist (not filtering by time here)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT branch, class FROM users WHERE id = ?', (student_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return []
    branch, class_level = row
    # expose student_branch variable name for compatibility with other code
    student_branch = branch
    # Normalize class_level to FY/SY/TY/Final Year
    if class_level:
        cls = str(class_level).strip()
        if len(cls) == 1 and cls.isdigit():
            class_level = 'FY' if cls == '1' else 'SY' if cls == '2' else 'TY' if cls == '3' else class_level
        else:
            # If class strings like 'FY', 'SY', 'TY' remain as-is
            class_level = cls
    # Filter tests by the student's branch/department and class/year level (mapped)
    # student's class could be 'FY', 'SY', 'TY', 'Final Year'
    year_map = {'FY': 'FY', 'SY': 'SY', 'TY': 'TY', 'Final Year': 'Final Year'}
    student_year = year_map.get(class_level, None)
    if student_branch and student_year:
        cursor.execute('''SELECT t.id, t.title, t.description, t.start_ts, t.end_ts, t.proctored, s.name, s.year_level, s.department
                          FROM tests t JOIN subjects s ON t.subject_id = s.id
                          WHERE (s.department = ? OR s.department IS NULL OR s.department = '') AND (s.year_level = ? OR s.year_level IS NULL OR s.year_level = '')
                          ORDER BY t.start_ts''', (student_branch, student_year))
    else:
        cursor.execute('''SELECT t.id, t.title, t.description, t.start_ts, t.end_ts, t.proctored, s.name, s.year_level, s.department
                          FROM tests t JOIN subjects s ON t.subject_id = s.id
                          ORDER BY t.start_ts''')
    tests = cursor.fetchall()
    conn.close()
    return tests

def get_test_questions(test_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, question_text, choices, correct_choice, marks FROM test_questions WHERE test_id = ? ORDER BY id', (test_id,))
    rows = cursor.fetchall()
    conn.close()
    questions = []
    for r in rows:
        qid, text, choices_json, correct, marks = r
        try:
            choices = json.loads(choices_json)
        except Exception:
            choices = []
        questions.append({'id': qid, 'text': text, 'choices': choices, 'correct': correct, 'marks': marks})
    return questions

def submit_test_attempt(test_id, student_id, answers_dict, started_at=None, submitted_at=None):
    """answers_dict: {question_id: chosen_index}"""
    questions = get_test_questions(test_id)
    total_score = 0.0
    for q in questions:
        qid = q['id']
        correct = q['correct']
        marks = q.get('marks', 1)
        chosen = answers_dict.get(str(qid)) or answers_dict.get(qid)
        try:
            if int(chosen) == int(correct):
                total_score += marks
        except Exception:
            pass
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    answers_json = json.dumps(answers_dict)
    # Write a log entry before attempting insert (helps debug missing inserts)
    try:
        with open('attempts.log', 'a', encoding='utf-8') as lf:
            lf.write(f"{datetime.now(ZoneInfo('Asia/Kolkata')).isoformat()} - SUBMIT START - test_id={test_id} student_id={student_id} answers={answers_json}\n")
    except Exception:
        pass

    try:
        cursor.execute('''INSERT INTO test_attempts (test_id, student_id, answers, score, started_at, submitted_at)
                          VALUES (?, ?, ?, ?, ?, ?)''', (test_id, student_id, answers_json, total_score, started_at, submitted_at))
        conn.commit()
        aid = cursor.lastrowid
        try:
            with open('attempts.log', 'a', encoding='utf-8') as lf:
                lf.write(f"{datetime.now(ZoneInfo('Asia/Kolkata')).isoformat()} - SUBMIT SUCCESS - attempt_id={aid} score={total_score}\n")
        except Exception:
            pass
        return {'attempt_id': aid, 'score': total_score}
    except Exception as e:
        try:
            with open('attempts.log', 'a', encoding='utf-8') as lf:
                lf.write(f"{datetime.now(ZoneInfo('Asia/Kolkata')).isoformat()} - SUBMIT ERROR - test_id={test_id} student_id={student_id} error={str(e)}\n")
        except Exception:
            pass
        raise
    finally:
        conn.close()

def get_test_attempts_for_student(student_id, test_id=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if test_id:
        cursor.execute('SELECT id, test_id, score, started_at, submitted_at FROM test_attempts WHERE student_id = ? AND test_id = ? ORDER BY submitted_at DESC', (student_id, test_id))
    else:
        cursor.execute('SELECT id, test_id, score, started_at, submitted_at FROM test_attempts WHERE student_id = ? ORDER BY submitted_at DESC', (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_test_attempts_for_test(test_id):
    """Return all attempts for a given test id, joined with student username/name."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT ta.id, ta.test_id, ta.student_id, ta.answers, ta.score, ta.started_at, ta.submitted_at, u.username, u.name
                      FROM test_attempts ta
                      LEFT JOIN users u ON ta.student_id = u.id
                      WHERE ta.test_id = ?
                      ORDER BY ta.submitted_at DESC''', (test_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def create_notice(title, content, target_branch=None, target_class=None, created_by_role='admin', created_by_id=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO notices (title, content, target_branch, target_class, created_by_role, created_by_id)
                      VALUES (?, ?, ?, ?, ?, ?)''', (title, content, target_branch, target_class, created_by_role, created_by_id))
    conn.commit()
    nid = cursor.lastrowid
    conn.close()
    return nid


def get_notices(target_branch=None, target_class=None, limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if target_branch and target_class:
        cursor.execute('''SELECT id, title, content, target_branch, target_class, created_by_role, created_by_id, created_at
                          FROM notices WHERE (target_branch IS NULL OR target_branch = ?) AND (target_class IS NULL OR target_class = ?)
                          ORDER BY created_at DESC LIMIT ?''', (target_branch, target_class, limit))
    elif target_branch:
        cursor.execute('''SELECT id, title, content, target_branch, target_class, created_by_role, created_by_id, created_at
                          FROM notices WHERE target_branch IS NULL OR target_branch = ? ORDER BY created_at DESC LIMIT ?''', (target_branch, limit))
    else:
        cursor.execute('''SELECT id, title, content, target_branch, target_class, created_by_role, created_by_id, created_at
                          FROM notices ORDER BY created_at DESC LIMIT ?''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def submit_faculty_leave(faculty_id, leave_type, start_date, end_date, is_half_day=False, days_count=1, alt_faculty=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO faculty_leaves (faculty_id, leave_type, start_date, end_date, is_half_day, days_count, alt_faculty)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (faculty_id, leave_type, start_date, end_date, 1 if is_half_day else 0, days_count, alt_faculty))
    conn.commit()
    lid = cursor.lastrowid
    conn.close()
    return lid


def get_faculty_leaves(faculty_id=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if faculty_id:
        cursor.execute('''SELECT id, faculty_id, leave_type, start_date, end_date, is_half_day, days_count, alt_faculty, created_at
                          FROM faculty_leaves WHERE faculty_id = ? ORDER BY created_at DESC''', (faculty_id,))
    else:
        cursor.execute('''SELECT id, faculty_id, leave_type, start_date, end_date, is_half_day, days_count, alt_faculty, created_at
                          FROM faculty_leaves ORDER BY created_at DESC''')
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_faculty_leave_usage(faculty_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Compute current academic year range and only count leaves within it so balances reset each academic year
    start_iso, end_iso, _ = get_academic_year_range_for_date()
    cursor.execute('''SELECT leave_type, COALESCE(SUM(days_count), 0) as used_days
                      FROM faculty_leaves
                      WHERE faculty_id = ? AND created_at BETWEEN ? AND ?
                      GROUP BY leave_type''', (faculty_id, start_iso, end_iso))
    rows = cursor.fetchall()
    conn.close()
    usage = {r[0]: r[1] for r in rows}
    return usage


def get_all_subjects():
    """Get all available subjects."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, year_level, department, code FROM subjects ORDER BY year_level, name')
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_academic_year_range_for_date(dt=None):
    """Return (start_date_iso, end_date_iso, academic_year_str) for the academic year containing dt.
    Academic year runs from July 1 to June 30 next year."""
    if dt is None:
        dt = datetime.now(ZoneInfo("Asia/Kolkata"))
    # Ensure dt is date/datetime
    if isinstance(dt, datetime):
        cur_date = dt.date()
    else:
        cur_date = dt

    year = cur_date.year
    # If month >= July, academic year starts this year
    if cur_date.month >= 7:
        start_year = year
        end_year = year + 1
    else:
        start_year = year - 1
        end_year = year

    start_date = datetime(start_year, 7, 1, tzinfo=ZoneInfo("Asia/Kolkata")).isoformat()
    # End of academic year: June 30 at 23:59:59
    end_date = datetime(end_year, 6, 30, 23, 59, 59, tzinfo=ZoneInfo("Asia/Kolkata")).isoformat()
    academic_year = f"{start_year}-{end_year}"
    return start_date, end_date, academic_year

def get_faculty_subjects_with_ids(faculty_id):
    """Get subject IDs assigned to a faculty."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT subject_id FROM faculty_subject WHERE faculty_id = ?', (faculty_id,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def assign_subject_to_faculty(faculty_id, subject_id):
    """Assign a subject to a faculty member."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO faculty_subject (faculty_id, subject_id) VALUES (?, ?)',
                      (faculty_id, subject_id))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False

def add_subject(name, year_level, department=None, code=None):
    """Insert a new subject into the subjects table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO subjects (name, year_level, department, code) VALUES (?, ?, ?, ?)',
                      (name, year_level, department, code))
        conn.commit()
        sid = cursor.lastrowid
        conn.close()
        return sid
    except Exception:
        conn.close()
        return None

def remove_subject_from_faculty(faculty_id, subject_id):
    """Remove a subject assignment from a faculty member."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM faculty_subject WHERE faculty_id = ? AND subject_id = ?',
                      (faculty_id, subject_id))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False

# Initialize database
init_database()

# Session state management
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.user_id = None

# Sidebar navigation
with st.sidebar:
    # Sidebar title kept concise now (main header moved to main page)
    st.title("🎓 VVPIET Student LMS")
    
    if st.session_state.logged_in:
        st.success(f"Logged in as: **{st.session_state.username}** ({st.session_state.role})")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            safe_rerun()
        
        st.divider()
        
        # Navigation based on role
        if st.session_state.role == 'student':
            feedback_open = is_feedback_open()
            # Student navigation: always show all tabs, but the feedback form itself is gated by feedback window
            student_tabs = ["🏠 Dashboard", "📝 Submit Feedback", "📥 Download Resources", "📊 My Attendance", "💰 Credit Calculator", "🧪 Tests", "ℹ️ About"]
            page = st.radio("Navigation", student_tabs)
        elif st.session_state.role == 'faculty':
            page = st.radio("Navigation", ["📅 Mark Attendance", "🧾 Daily Attendance", "📒 Daily LER", "📚 Upload Resources", "🧪 Create Test", "📄 Faculty Leaves", "ℹ️ About"])
        else:  # admin
            page = st.radio("Navigation", ["📊 Dashboard", "👥 Student Attendance", "📚 Manage Subjects", "👨‍🏫 Manage Faculty", "📈 Analytics", "📋 Export Data", "🗂️ Faculty Leaves", "🐛 Debug: Test Attempts", "ℹ️ About"])
    else:
        page = st.radio("Navigation", ["🔐 Login", "📝 Register"])

# If a UI flow set `nav_to_page` (button click), honor it and navigate there
if 'nav_to_page' in st.session_state:
    page = st.session_state.pop('nav_to_page')

# Main content area
# Main page header (logo + college name), centered
with st.container():
    left_col, mid_col, right_col = st.columns([1, 6, 1])
    with left_col:
        st.image("college_logo.jpg", width=84)
    with mid_col:
        st.markdown('<div style="text-align:center; font-weight:bold; color:#8B3A3A; font-size:20px;">VVP institute of engineering and technology, Solapur, Maharashtra, India</div>', unsafe_allow_html=True)
    st.markdown("---")

if not st.session_state.logged_in:
    if page == "🔐 Login":
        st.title("🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            result = verify_login(username, password)
            if result:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_id = result[0]
                st.session_state.role = result[1]
                st.success("Login successful! 🎉")
                safe_rerun()
            else:
                st.error("Invalid username or password ❌")
        
        # Demo credentials removed from the public main page for security.
        # Administrators can provide credentials to users directly.
        st.info("Contact your administrator to obtain login credentials.")

        with st.expander("Forgot Password?"):
            st.write("Reset your password by verifying your roll number.")
            with st.form("forgot_password_form"):
                fp_username = st.text_input("Username")
                fp_roll = st.text_input("Roll Number / PRN")
                fp_new = st.text_input("New Password", type="password")
                fp_confirm = st.text_input("Confirm New Password", type="password")
                fp_submit = st.form_submit_button("Reset Password")

            if fp_submit:
                if not fp_username or not fp_roll or not fp_new:
                    st.error("Please provide username, roll number/PRN, and the new password.")
                elif fp_new != fp_confirm:
                    st.error("Passwords do not match.")
                else:
                    ok = reset_user_password_with_roll(fp_username.strip(), fp_roll.strip(), fp_new)
                    if ok:
                        st.success("Password reset successful. Please login with your new password.")
                    else:
                        st.error("Password reset failed. Ensure username and roll number/PRN match our records, or contact admin.")
    
    elif page == "📝 Register":
        st.title("📝 Register")
        
        reg_type = st.radio("Select Registration Type:", ["Student", "Faculty"], horizontal=True)
        
        if reg_type == "Student":
            st.subheader("Student Registration")
            with st.form("student_register_form"):
                name = st.text_input("Full Name *")
                roll_number = st.text_input("Roll Number *")
                new_username = st.text_input("Choose Username *")
                new_password = st.text_input("Choose Password *", type="password")
                confirm_password = st.text_input("Confirm Password *", type="password")
                
                branches = get_branches()
                if not branches:
                    branches = ["General"]
                selected_branch = st.selectbox("Branch *", options=branches)
                
                class_options = ["FY", "SY", "TY", "Final Year"]
                selected_class = st.selectbox("Class/Year Level *", options=class_options)
                
                submit = st.form_submit_button("Register as Student", use_container_width=True)
            
            if submit:
                if not name or not roll_number or not new_username or not new_password:
                    st.error("Please fill all required fields")
                elif new_password != confirm_password:
                    st.error("Passwords don't match!")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    try:
                        cursor.execute('INSERT INTO users (username, password, role, name, roll_number, branch, class) VALUES (?, ?, ?, ?, ?, ?, ?)',
                                      (new_username, hash_password(new_password), 'student', name, roll_number, selected_branch, selected_class))
                        conn.commit()
                        st.success("✓ Student registration successful! Please login.")
                    except sqlite3.IntegrityError:
                        st.error("Username already exists!")
                    conn.close()
        
        else:  # Faculty registration
            st.subheader("Faculty Registration")
            
            with st.form("faculty_register_form"):
                name = st.text_input("Full Name *")
                new_username = st.text_input("Choose Username *")
                new_password = st.text_input("Choose Password *", type="password")
                confirm_password = st.text_input("Confirm Password *", type="password")
                
                branches = get_branches()
                if not branches:
                    branches = ["General"]
                selected_branch = st.selectbox("Department/Branch *", options=branches)
                
                # Add year level selection for faculty (allow multiple selections)
                year_levels = get_year_levels()
                if not year_levels:
                    year_levels = ['FY', 'SY', 'TY', 'Final Year']
                selected_year_levels = st.multiselect("Year Levels Teaching * (Select one or more)", options=year_levels)
                
                submit = st.form_submit_button("Register as Faculty", use_container_width=True)
            
            if submit:
                if not name or not new_username or not new_password:
                    st.error("Please fill all required fields")
                elif new_password != confirm_password:
                    st.error("Passwords don't match!")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                elif not selected_year_levels:
                    st.error("Please select at least one year level")
                else:
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    try:
                        # Check if username already exists
                        cursor.execute('SELECT id FROM users WHERE username = ?', (new_username,))
                        if cursor.fetchone():
                            st.error("Username already exists! Please choose a different username.")
                            conn.close()
                        else:
                            # Create a new faculty record with the first selected year level as default
                            faculty_record_name = f"{name}"
                            cursor.execute('INSERT INTO faculty (name, department, year_level) VALUES (?, ?, ?)',
                                          (faculty_record_name, selected_branch, selected_year_levels[0]))
                            conn.commit()
                            fac_id = cursor.lastrowid
                            
                            # Add all selected year levels to faculty_year_level table
                            for year_level in selected_year_levels:
                                cursor.execute('INSERT INTO faculty_year_level (faculty_id, year_level) VALUES (?, ?)',
                                             (fac_id, year_level))
                            conn.commit()
                            
                            # Create the user account linked to faculty
                            cursor.execute('INSERT INTO users (username, password, role, faculty_id, name, branch) VALUES (?, ?, ?, ?, ?, ?)',
                                          (new_username, hash_password(new_password), 'faculty', fac_id, name, selected_branch))
                            conn.commit()
                            st.success("✓ Faculty registration successful! Please login.")
                            conn.close()
                    except sqlite3.IntegrityError as e:
                        if 'UNIQUE constraint failed: faculty.name' in str(e):
                            st.error("A faculty with this name already exists. Please use a different name or contact admin.")
                        else:
                            st.error(f"Registration error: {str(e)}")
                        conn.close()
                    except Exception as e:
                        st.error(f"Error during registration: {str(e)}")
                        conn.close()

else:
    # Student pages
    if st.session_state.role == 'student':
        if page == "🏠 Dashboard":
            st.title("Student Dashboard")
            # student's branch and class info
            user = get_user_by_username(st.session_state.username) if st.session_state.username else None
            user_id = user[0] if user else None
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, name, branch, class FROM users WHERE id = ? AND role = ?', (user_id, 'student'))
            student_info = cursor.fetchone()
            conn.close()
            if not student_info:
                st.error("Student information not found")
            else:
                student_id, student_username, student_name, student_branch, student_class = student_info
                st.info(f"**Your Branch:** {student_branch} | **Your Class:** {student_class}")

                # Notices board - expander
                notices = get_notices(target_branch=student_branch, target_class=student_class)
                if notices:
                    with st.expander("📢 Notices"):
                        for n in notices[:5]:
                            nid, title, content, tbranch, tclass, cb_role, cb_id, created_at = n
                            st.markdown(f"**{title}** — *{created_at[:16]}*")
                            st.write(content)
                            st.markdown("---")
                else:
                    st.info("No notices available at the moment.")

                # Recent Test Attempts - show immediately after submission
                st.markdown("---")
                st.subheader("🧪 My Recent Test Attempts")
                recent_attempts = get_test_attempts_for_student(student_id)
                if recent_attempts:
                    st.success(f"✓ You have {len(recent_attempts)} attempt(s) recorded")
                    attempt_rows = []
                    for att in recent_attempts:
                        aid, ttid, score, started_at, submitted_at = att
                        conn = sqlite3.connect(DB_PATH)
                        cur = conn.cursor()
                        cur.execute('SELECT title FROM tests WHERE id = ?', (ttid,))
                        test_title = cur.fetchone()
                        conn.close()
                        test_title = test_title[0] if test_title else 'Unknown Test'
                        attempt_rows.append({
                            'attempt_id': aid,
                            'test': test_title,
                            'score': score,
                            'submitted_at': submitted_at
                        })
                    df_attempts = pd.DataFrame(attempt_rows)
                    st.dataframe(df_attempts, use_container_width=True, hide_index=True)
                else:
                    st.info("No test attempts recorded yet. Take a test to see your results here!")

                # Assignments & Notes placeholder
                st.markdown("---")
                st.subheader("📚 Assignments & Notes")
                student_year_level = 'SY' if student_class and student_class[0] == '2' else 'FY' if student_class and student_class[0] == '1' else 'TY' if student_class and student_class[0] == '3' else 'Final Year'
                resources = get_subject_resources_for_student(student_year_level, student_branch)
                if resources:
                    st.info(f"Resources available for {student_year_level} — click to open the 'Download Resources' page.")
                    if st.button("Open Assignments & Notes"):
                        st.session_state['nav_to_page'] = "📥 Download Resources"
                        safe_rerun()
                else:
                    st.info("No assignments/notes available at the moment.")

                # Attendance placeholder
                st.markdown("---")
                st.subheader("📊 Attendance")
                user_attendance_pct = get_student_attendance_percentage(user_id) if user_id else 0
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Overall Attendance (%)", f"{user_attendance_pct:.1f}%")
                with col2:
                    if user_attendance_pct >= 60:
                        st.success("Eligible for feedback submission")
                    else:
                        st.info("Not eligible for feedback submission yet")
                if st.button("Open Attendance Details"):
                    st.session_state['nav_to_page'] = "📊 My Attendance"
                    safe_rerun()
                # Active tests quick access
                st.markdown("---")
                st.subheader("🧪 Active Tests")
                active_tests = get_tests_for_student(student_id)
                active = []
                for t in active_tests:
                    tid, title, desc, start_ts, end_ts, proctored, subj_name, year_level, dept = t
                    now = datetime.now(ZoneInfo("Asia/Kolkata"))
                    try:
                        start = parse_iso_to_kolkata(start_ts) if start_ts else None
                        end = parse_iso_to_kolkata(end_ts) if end_ts else None
                    except Exception:
                        start = None
                        end = None
                    if (not start or now >= start) and (not end or now <= end):
                        active.append((tid, title, subj_name))
                if active:
                    for tid, title, subj_name in active:
                        col1, col2 = st.columns([6, 1])
                        with col1:
                            st.write(f"**{title}** — {subj_name}")
                        with col2:
                            if st.button(f"Take", key=f"ctake_{tid}"):
                                st.session_state['active_test_id'] = tid
                                st.session_state['nav_to_page'] = "🧪 Take Test"
                                safe_rerun()
                else:
                    st.info("No active tests at the moment.")

        elif page == "📝 Submit Feedback":
            st.title("Student Dashboard")
            
            # Get student's branch from users table
            user = get_user_by_username(st.session_state.username) if st.session_state.username else None
            user_id = user[0] if user else None
            
            # Get complete student info including branch and class
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, name, branch, class FROM users WHERE id = ? AND role = ?', (user_id, 'student'))
            student_info = cursor.fetchone()
            conn.close()
            
            if not student_info:
                st.error("Student information not found")
            else:
                student_id, student_username, student_name, student_branch, student_class = student_info
                
                # Display student's branch and class
                st.info(f"**Your Branch:** {student_branch} | **Your Class:** {student_class}")


                # Credit Calculator quick-access placeholder
                st.markdown("---")
                st.subheader("💰 Credit Calculator (Quick Access)")
                colc1, colc2 = st.columns([3,1])
                with colc1:
                    st.write("Open the Credit Calculator to calculate semester/degree progress based on your category and class.")
                with colc2:
                    if st.button("Open Calculator"):
                        st.session_state['nav_to_page'] = "💰 Credit Calculator"
                        safe_rerun()


                # Show feedback schedule status
                # (Tab is now hidden if not open, but keep info for safety)
                if not is_feedback_open():
                    sched = get_current_feedback_schedule()
                    if sched:
                        st.warning(f"Feedback will be open from {sched[0]} to {sched[1]}. You can submit feedback during that window.")
                    else:
                        st.info("Feedback is not scheduled currently. Contact admin for when feedback will be open.")

                # Submit Feedback Page
                st.subheader("Submit Faculty Feedback")

                # Compute student year level from student_class
                # student_class contains values like "FY", "SY", "TY", "Final Year", or numeric "1", "2", "3", "4"
                student_year_level = 'FY'  # Default
                if student_class:
                    class_str = str(student_class).strip().upper()
                    # Check for string values first
                    if class_str == 'FY' or class_str == 'FIRST YEAR':
                        student_year_level = 'FY'
                    elif class_str == 'SY' or class_str == 'SECOND YEAR':
                        student_year_level = 'SY'
                    elif class_str == 'TY' or class_str == 'THIRD YEAR':
                        student_year_level = 'TY'
                    elif class_str == 'FINAL YEAR' or class_str == 'FYR' or class_str == 'FOURTH YEAR':
                        student_year_level = 'Final Year'
                    # Check for numeric values
                    elif class_str == '1':
                        student_year_level = 'FY'
                    elif class_str == '2':
                        student_year_level = 'SY'
                    elif class_str == '3':
                        student_year_level = 'TY'
                    elif class_str == '4':
                        student_year_level = 'Final Year'
                    # Check first character if numeric
                    elif class_str and class_str[0].isdigit():
                        first_digit = class_str[0]
                        if first_digit == '1':
                            student_year_level = 'FY'
                        elif first_digit == '2':
                            student_year_level = 'SY'
                        elif first_digit == '3':
                            student_year_level = 'TY'
                        elif first_digit == '4':
                            student_year_level = 'Final Year'

                # Check if feedback is open - if closed, show message only
                if not is_feedback_open():
                    sched = get_current_feedback_schedule()
                    if sched:
                        st.error(f"❌ Feedback submission is currently **CLOSED**")
                        st.warning(f"Feedback was open from:\n**{sched[0]}** to **{sched[1]}**\n\nThis window has now ended. You can only submit feedback during the scheduled window.")
                    else:
                        st.error("❌ Feedback submission is currently **CLOSED**")
                        st.info("Feedback is not scheduled currently. Contact admin for when feedback will be open.")
                else:
                    # Feedback window is OPEN - show the form
                    st.success(f"✅ Feedback window is **OPEN**! Showing subjects and faculty for: **{student_year_level}**")
                    
                    # Get student's attendance percentage
                    user_attendance_pct = get_student_attendance_percentage(user_id) if user_id else 0
                    user_has_access = user_attendance_pct >= 60 if user_id else False

                    # Get subjects for this year level AND filter by student's branch
                    subjects = get_subjects_by_year(student_year_level)
                    # Filter subjects to only those matching the student's branch
                    filtered_subjects = [s for s in subjects if s[3] == student_branch] if subjects else []
                    subject_options = [s[1] for s in filtered_subjects]
                    subject_options = ["All"] + subject_options
                    selected_subject = st.selectbox("Select Subject (optional)", options=subject_options, key="fb_subject")

                    if selected_subject and selected_subject != "All":
                        subj = next((s for s in filtered_subjects if s[1] == selected_subject), None)
                        if subj:
                            # Get faculties by subject, filtered by student's branch and year level
                            faculties = get_faculties_by_subject(subj[0], branch=student_branch, year_level=student_year_level)
                        else:
                            faculties = []
                    else:
                        # Get all faculties from student's branch and year level
                        faculties = get_faculties_by_branch_and_year(student_branch, student_year_level)

                        # Deduplicate faculties by ID
                        seen_faculty_ids = set()
                        unique_faculties = []
                        for fac in faculties:
                            fac_id = fac[0]
                            if fac_id not in seen_faculty_ids:
                                seen_faculty_ids.add(fac_id)
                                unique_faculties.append(fac)

                        # Create faculty dictionary
                        faculty_dict = {f'{f[1]} ({f[2]}) [ID: {f[0]}]': f[0] for f in unique_faculties}

                        # Feedback form or access message
                        if not user_has_access:
                            st.warning(f"❌ Access Denied: You need >= 60% attendance to submit feedback.\n\n**Your Current Attendance:** {user_attendance_pct:.1f}%\n\nPlease contact your faculty/admin for attendance information.")
                        else:
                            st.success(f"✅ Your attendance: {user_attendance_pct:.1f}% - You have access to submit feedback")
                            
                            if not faculty_dict:
                                st.warning(f"No faculty found in {student_branch} for year level {student_year_level}")
                            else:
                                with st.form("feedback_form"):
                                    feedback_student_name = st.text_input("Your Name (optional)", value=student_name or "")
                                    
                                    # Select subject first
                                    selected_subject = st.selectbox(
                                        "Select Subject *",
                                        options=subject_options,
                                        key="fb_subject_form"
                                    )
                                    
                                    # Get faculties for the selected subject
                                    if selected_subject and selected_subject != "All":
                                        subj = next((s for s in filtered_subjects if s[1] == selected_subject), None)
                                        if subj:
                                            subject_id = subj[0]
                                            faculties_for_subject = get_faculties_by_subject(subj[0], branch=student_branch, year_level=student_year_level)
                                            faculty_dict_filtered = {f'{f[1]} ({f[2]}) [ID: {f[0]}]': f[0] for f in faculties_for_subject}
                                        else:
                                            faculty_dict_filtered = {}
                                            subject_id = None
                                    else:
                                        faculty_dict_filtered = faculty_dict
                                        subject_id = None
                                    
                                    selected_faculty = st.selectbox(
                                        "Select Faculty *",
                                        options=faculty_dict_filtered.keys() if faculty_dict_filtered else [],
                                        key="fb_faculty_form"
                                    )

                                    st.markdown("### Rate the following aspects (1-10)")
                                    st.markdown("Please answer the following questions by rating from 1 (Strongly Disagree) to 10 (Strongly Agree):")
                                    st.divider()
                                    
                                    # Display questions sequentially with styling
                                    st.markdown("<span style='color:#1f4788; font-size:16px'><b>1. Has fundamental concepts & subject knowledge</b></span>", unsafe_allow_html=True)
                                    q1 = st.number_input("Rating", min_value=1, max_value=10, value=5, step=1, key="q1")
                                    st.write("")
                                    
                                    st.markdown("<span style='color:#1f4788; font-size:16px'><b>2. Preparation for Subject is sufficient while coming to class</b></span>", unsafe_allow_html=True)
                                    q2 = st.number_input("Rating", min_value=1, max_value=10, value=5, step=1, key="q2")
                                    st.write("")
                                    
                                    st.markdown("<span style='color:#1f4788; font-size:16px'><b>3. Sufficient knowledge about current trends/development of subject</b></span>", unsafe_allow_html=True)
                                    q3 = st.number_input("Rating", min_value=1, max_value=10, value=5, step=1, key="q3")
                                    st.write("")
                                    
                                    st.markdown("<span style='color:#1f4788; font-size:16px'><b>4. Proficient in English & communication skills</b></span>", unsafe_allow_html=True)
                                    q4 = st.number_input("Rating", min_value=1, max_value=10, value=5, step=1, key="q4")
                                    st.write("")
                                    
                                    st.markdown("<span style='color:#1f4788; font-size:16px'><b>5. Teaching makes class interesting & interactive through student participation</b></span>", unsafe_allow_html=True)
                                    q5 = st.number_input("Rating", min_value=1, max_value=10, value=5, step=1, key="q5")
                                    st.write("")
                                    
                                    st.markdown("<span style='color:#1f4788; font-size:16px'><b>6. Faculty is punctual in starting and ending classes on time</b></span>", unsafe_allow_html=True)
                                    q6 = st.number_input("Rating", min_value=1, max_value=10, value=5, step=1, key="q6")
                                    st.write("")
                                    
                                    st.markdown("<span style='color:#1f4788; font-size:16px'><b>7. Has covered the entire syllabus as prescribed by university</b></span>", unsafe_allow_html=True)
                                    q7 = st.number_input("Rating", min_value=1, max_value=10, value=5, step=1, key="q7")
                                    st.write("")
                                    
                                    st.markdown("<span style='color:#1f4788; font-size:16px'><b>8. Extent of fulfillment of your learning expectations</b></span>", unsafe_allow_html=True)
                                    q8 = st.number_input("Rating", min_value=1, max_value=10, value=5, step=1, key="q8")
                                    st.write("")
                                    
                                    st.markdown("<span style='color:#1f4788; font-size:16px'><b>9. Behavior with students is appropriate and rational</b></span>", unsafe_allow_html=True)
                                    q9 = st.number_input("Rating", min_value=1, max_value=10, value=5, step=1, key="q9")
                                    st.write("")
                                    
                                    st.markdown("<span style='color:#1f4788; font-size:16px'><b>10. Motivates students for their study and better career</b></span>", unsafe_allow_html=True)
                                    q10 = st.number_input("Rating", min_value=1, max_value=10, value=5, step=1, key="q10")
                                    st.divider()
                                    
                                    st.markdown("<span style='color:#d9534f; font-size:16px'><b>Overall Rating for this Faculty</b></span>", unsafe_allow_html=True)
                                    overall = st.number_input("Overall Rating", min_value=1, max_value=10, value=5, step=1)
                                    comments = st.text_area("Additional Comments (optional)", height=100)
                                    submitted = st.form_submit_button("Submit Feedback", use_container_width=True)

                                if submitted:
                                    faculty_id = faculty_dict_filtered.get(selected_faculty, faculty_dict.get(selected_faculty))
                                    if not subject_id and selected_subject and selected_subject != "All":
                                        subj = next((s for s in subjects if s[1] == selected_subject and s[3] == student_branch), None)
                                        subject_id = subj[0] if subj else None
                                    
                                    if submit_feedback(feedback_student_name, faculty_id, subject_id, student_year_level,
                                                       int(q1), int(q2), int(q3), int(q4), int(q5), int(q6), int(q7), int(q8), int(q9), int(q10),
                                                       int(overall), comments):
                                        st.success("✓ Feedback submitted successfully!")
                                        st.balloons()
                                    else:
                                        st.error("Error submitting feedback")
                
        elif page == "📥 Download Resources":
            st.title("📥 Download Resources")
            # Get student's info
            user = get_user_by_username(st.session_state.username) if st.session_state.username else None
            user_id = user[0] if user else None
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, name, branch, class FROM users WHERE id = ? AND role = ?', (user_id, 'student'))
            student_info = cursor.fetchone()
            conn.close()
            if not student_info:
                st.error("Student information not found")
            else:
                student_id, student_username, student_name, student_branch, student_class = student_info
                
                # Map student class to year level and semesters
                class_to_year = {
                    'FY': ('FY', ['Semester 1', 'Semester 2']),
                    'SY': ('SY', ['Semester 3', 'Semester 4']),
                    'TY': ('TY', ['Semester 5', 'Semester 6']),
                    'Final Year': ('Final Year', ['Semester 7', 'Semester 8'])
                }
                
                student_year_level, semesters = class_to_year.get(student_class, (student_class, []))
                
                st.info(f"**Student:** {student_name} | **Class:** {student_year_level} | **Branch:** {student_branch}")
                st.markdown("---")
                
                # Get all subjects for this year level and branch
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('''SELECT DISTINCT id, name, year_level, department 
                                  FROM subjects 
                                  WHERE year_level = ? AND (department = ? OR department IS NULL OR department = '')
                                  ORDER BY name''', (student_year_level, student_branch))
                subjects = cursor.fetchall()
                conn.close()
                
                if not subjects:
                    st.info(f"No subjects found for {student_year_level} in {student_branch}")
                else:
                    # Display semester-wise organization
                    st.subheader("📚 Subjects by Semester")
                    st.write(f"Available semesters for {student_year_level}: {', '.join(semesters)}")
                    st.markdown("---")
                    
                    # Display all subjects
                    subject_tabs = st.tabs([f"All Subjects ({len(subjects)})"] + [s for s in semesters])
                    
                    with subject_tabs[0]:  # All Subjects tab
                        st.subheader("All Subjects")
                        for subject_id, subject_name, year_level, department in subjects:
                            with st.expander(f"📖 {subject_name}"):
                                # Get resources for this subject
                                resources = get_subject_resources_for_student(year_level, student_branch)
                                subject_resources = [r for r in resources if r[3] == subject_name] if resources else []
                                
                                if subject_resources:
                                    st.write(f"**Resources ({len(subject_resources)}):**")
                                    
                                    # Group by faculty
                                    by_faculty = {}
                                    for res in subject_resources:
                                        res_id, filename, res_type, subject_n, faculty_name, uploaded_at, deadline = res
                                        if faculty_name not in by_faculty:
                                            by_faculty[faculty_name] = []
                                        by_faculty[faculty_name].append((res_id, filename, res_type, uploaded_at, deadline))
                                    
                                    for faculty_name, items in by_faculty.items():
                                        with st.expander(f"👨‍🏫 {faculty_name} ({len(items)})"):
                                            for res_id, filename, res_type, uploaded_at, deadline in items:
                                                col1, col2 = st.columns([4, 1])
                                                col1.write(f"📄 {filename}")
                                                col1.caption(f"Type: {res_type.capitalize()} | Uploaded: {uploaded_at}")
                                                if deadline and res_type == "assignment":
                                                    col1.caption(f"⏰ Deadline: {deadline}")
                                                col2.download_button(
                                                    label="⬇️",
                                                    data=open(f"faculty_resources/{filename}", "rb").read() if os.path.exists(f"faculty_resources/{filename}") else b"",
                                                    file_name=filename,
                                                    key=f"download_{res_id}_{filename}"
                                                )
                                else:
                                    st.info(f"No resources available yet for {subject_name}")
                    
                    # Semester tabs (for future use - placeholder)
                    for sem_idx, semester in enumerate(semesters, start=1):
                        with subject_tabs[sem_idx]:
                            st.subheader(f"{semester} - Subjects & Resources")
                            st.info(f"Resources will be organized by {semester} once more data is added.")
                    
                    st.markdown("---")
                    st.subheader("👨‍🏫 Faculty List")
                    st.write(f"The following faculties have uploaded resources for your {student_year_level}:")
                    
                    # Get all faculties teaching subjects for this year/branch
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute('''SELECT DISTINCT f.id, f.name, f.department 
                                      FROM faculty f
                                      JOIN faculty_subject fs ON f.id = fs.faculty_id
                                      JOIN subjects s ON fs.subject_id = s.id
                                      WHERE s.year_level = ? AND (s.department = ? OR s.department IS NULL OR s.department = '')
                                      ORDER BY f.name''', (student_year_level, student_branch))
                    faculties = cursor.fetchall()
                    conn.close()
                    
                    if faculties:
                        for fac_id, fac_name, fac_dept in faculties:
                            # Count resources from this faculty for this year/branch
                            resources_for_fac = get_subject_resources_for_student(student_year_level, student_branch)
                            fac_resource_count = len([r for r in resources_for_fac if r[4] == fac_name]) if resources_for_fac else 0
                            
                            with st.expander(f"👨‍🏫 {fac_name} ({fac_dept}) — {fac_resource_count} resource(s)"):
                                # Get their subjects
                                conn = sqlite3.connect(DB_PATH)
                                cursor = conn.cursor()
                                cursor.execute('''SELECT DISTINCT s.name 
                                                  FROM subjects s
                                                  JOIN faculty_subject fs ON s.id = fs.subject_id
                                                  WHERE fs.faculty_id = ? AND s.year_level = ?
                                                  ORDER BY s.name''', (fac_id, student_year_level))
                                fac_subjects = cursor.fetchall()
                                conn.close()
                                
                                if fac_subjects:
                                    st.write(f"**Teaches:** {', '.join([s[0] for s in fac_subjects])}")
                                st.write(f"**Department:** {fac_dept}")
                    else:
                        st.info(f"No faculties assigned to {student_year_level} in {student_branch} yet.")

        elif page == "📊 My Attendance":
            st.title("📊 My Attendance")
            user = get_user_by_username(st.session_state.username) if st.session_state.username else None
            user_id = user[0] if user else None
            if not user_id:
                st.error("User information not found")
            else:
                user_attendance_pct = get_student_attendance_percentage(user_id) if user_id else 0
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Overall Attendance", f"{user_attendance_pct:.1f}%")
                with col2:
                    if user_attendance_pct >= 60:
                        st.success("✅ Eligible for feedback submission")
                    else:
                        st.error(f"❌ Need {60 - user_attendance_pct:.1f}% more attendance")
                # Get attendance details
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT a.month, a.year, a.classes_attended, a.total_classes, s.name, f.name
                    FROM attendance a
                    JOIN subjects s ON a.subject_id = s.id
                    JOIN faculty f ON a.faculty_id = f.id
                    WHERE a.student_id = ?
                    ORDER BY a.year DESC, a.month DESC
                ''', (user_id,))
                attendance_records = cursor.fetchall()
                conn.close()
                if attendance_records:
                    st.subheader("Attendance Details")
                    attendance_data = []
                    for month, year, attended, total, subject, faculty in attendance_records:
                        pct = (attended / total * 100) if total > 0 else 0
                        attendance_data.append({
                            'Month': month,
                            'Year': year,
                            'Subject': subject,
                            'Faculty': faculty,
                            'Attended': attended,
                            'Total': total,
                            'Percentage': f"{pct:.1f}%"
                        })
                    df = pd.DataFrame(attendance_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No attendance records found")
        
        elif page == "🧪 Tests":
            st.title("🧪 Available Tests")
            user = get_user_by_username(st.session_state.username) if st.session_state.username else None
            user_id = user[0] if user else None
            if not user_id:
                st.error("User information not found")
            else:
                tests = get_tests_for_student(user_id)
                if not tests:
                    st.info("No tests available for your class/branch at this time.")
                else:
                    for t in tests:
                        tid, title, desc, start_ts, end_ts, proctored, subj_name, year_level, dept = t
                        st.subheader(f"{title} — {subj_name}")
                        st.write(desc or "No description")
                        st.write(f"Start: {start_ts} | End: {end_ts} | Proctored: {'Yes' if proctored else 'No'}")
                        # Check if test is active
                        now = datetime.now(ZoneInfo("Asia/Kolkata"))
                        try:
                            start = parse_iso_to_kolkata(start_ts) if start_ts else None
                            end = parse_iso_to_kolkata(end_ts) if end_ts else None
                        except Exception:
                            start = None
                            end = None

                        can_take = True
                        if start and now < start:
                            can_take = False
                        if end and now > end:
                            can_take = False

                        if can_take:
                            if not start:
                                st.info("This test has no start time set — contact faculty or admin.")
                            elif not end and now >= start:
                                # If no end time, allow taking after start
                                pass
                            # Navigation-based start. Clicking Start Test opens the test page.
                            if st.button(f"Start Test: {title}", key=f"start_test_{tid}"):
                                st.session_state['active_test_id'] = tid
                                st.session_state['nav_to_page'] = "🧪 Take Test"
                                safe_rerun()
                        else:
                            st.info("This test is not currently available (check schedule)")
        elif page == "🧪 Take Test":
            st.title("🧪 Take Test")
            test_id = st.session_state.get('active_test_id')
            if not test_id:
                st.info("No test selected. Go to 'Tests' to choose a test.")
            else:
                # Load test details
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('''SELECT t.id, t.title, t.description, t.start_ts, t.end_ts, t.proctored, s.name, s.year_level, s.department
                                  FROM tests t JOIN subjects s ON t.subject_id = s.id
                                  WHERE t.id = ?''', (test_id,))
                trow = cursor.fetchone()
                conn.close()
                if not trow:
                    st.error("Test not found")
                else:
                    tid, title, desc, start_ts, end_ts, proctored, subj_name, year_level, dept = trow
                    st.subheader(f"{title} — {subj_name}")
                    st.write(desc or "No description")
                    now = datetime.now(ZoneInfo("Asia/Kolkata"))
                    try:
                        start = parse_iso_to_kolkata(start_ts) if start_ts else None
                        end = parse_iso_to_kolkata(end_ts) if end_ts else None
                    except Exception:
                        start = None
                        end = None

                    # Availability checks
                    if start and now < start:
                        st.warning(f"This test will be available from {start.isoformat()}")
                    elif end and now > end:
                        st.warning("This test window has closed.")
                    else:
                        # Already attempted?
                        attempts = get_test_attempts_for_student(st.session_state.user_id, tid)
                        if attempts:
                            st.info("You have already attempted this test. Your recent score:")
                            for att in attempts:
                                aid, ttid, score, started_at, submitted_at = att
                                st.write(f"Attempt {aid}: Score {score} — Submitted: {submitted_at}")
                            # Optional: Allow retake if needed
                            if st.button("Retake Test", key=f"retake_{tid}"):
                                # Let student retake by continuing to show questions
                                pass
                        # Render questions
                        questions = get_test_questions(tid)
                        if not questions:
                            st.info("No questions have been added to this test yet. Contact the faculty to add questions.")
                        else:
                            answers = {}
                            with st.form(f"attempt_form_{tid}"):
                                st.write(f"Test: {title}")
                                for q in questions:
                                    opts = q['choices'] or []
                                    sel = st.radio(q['text'], options=list(range(len(opts))), format_func=lambda i, opts=opts: opts[i] if i < len(opts) else "", key=f"q_{q['id']}_{tid}")
                                    answers[str(q['id'])] = sel
                                submitted = st.form_submit_button("Submit Test")
                                if submitted:
                                    submitted_at_iso = datetime.now(ZoneInfo("Asia/Kolkata")).isoformat()
                                    started_at_iso = submitted_at_iso
                                    res = submit_test_attempt(tid, st.session_state.user_id, answers, started_at=started_at_iso, submitted_at=submitted_at_iso)
                                    st.success(f"Test submitted. Score: {res['score']}")

                                    # Verify the attempt was saved to the database and show confirmation
                                    try:
                                        conn = sqlite3.connect(DB_PATH)
                                        cur = conn.cursor()
                                        cur.execute('SELECT id, test_id, student_id, score, started_at, submitted_at FROM test_attempts WHERE id = ?', (res.get('attempt_id'),))
                                        saved = cur.fetchone()
                                        conn.close()
                                        if saved:
                                            aid_db, t_db, s_db, score_db, started_db, submitted_db = saved
                                            st.info(f"Saved attempt record — ID: {aid_db} | Score: {score_db} | Submitted: {submitted_db}")
                                    except Exception:
                                        pass

                                    # Prepare CSV summary for the student's attempt so they can download it immediately
                                    try:
                                        student_username = None
                                        conn = sqlite3.connect(DB_PATH)
                                        cur = conn.cursor()
                                        cur.execute('SELECT username, name FROM users WHERE id = ?', (st.session_state.user_id,))
                                        u = cur.fetchone()
                                        conn.close()
                                        if u:
                                            student_username = u[0]
                                        attempt_row = {
                                            'attempt_id': res.get('attempt_id'),
                                            'test_id': tid,
                                            'student_id': st.session_state.user_id,
                                            'student_username': student_username,
                                            'score': res.get('score'),
                                            'started_at': started_at_iso,
                                            'submitted_at': submitted_at_iso,
                                            'answers': json.dumps(answers)
                                        }
                                        df_attempt = pd.DataFrame([attempt_row])
                                        csv_bytes = df_attempt.to_csv(index=False).encode('utf-8')
                                        st.download_button("Download Your Attempt (CSV)", data=csv_bytes, file_name=f"test_{tid}_attempt_{res.get('attempt_id')}.csv", mime='text/csv')
                                    except Exception:
                                        pass

        elif page == "💰 Credit Calculator":
            st.title("💰 Credit Calculator")
            
            # Get student's info
            user = get_user_by_username(st.session_state.username) if st.session_state.username else None
            user_id = user[0] if user else None
            
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, name, branch, class FROM users WHERE id = ? AND role = ?', (user_id, 'student'))
            student_info = cursor.fetchone()
            conn.close()
            
            if not student_info:
                st.error("Student information not found")
            else:
                student_id, student_username, student_name, student_branch, student_class = student_info
                st.info(f"**{student_name}** ({student_branch} - {student_class})")
                
                st.markdown("---")
                st.subheader("Calculate Your Credit Progress")
                
                # Step 1: Select Category and Class
                col1, col2 = st.columns(2)
                with col1:
                    category = st.selectbox("Select Category", ["From First Year", "From Direct Second Year"], key="credit_category")
                with col2:
                    class_select = st.selectbox("Select Class", ["FY", "SY", "TY", "B.Tech"], key="credit_class")
                
                st.markdown("---")
                
                # Credit calculation by category & class
                def _clean_key(s: str) -> str:
                    return s.replace(" ", "_").replace(".", "_")

                sems = None
                factor = 0.0
                label = ""
                # TY - Direct Second Year -> sem 3 & 4 with 60% threshold
                if class_select == "TY" and category == "From Direct Second Year":
                    sems = [3, 4]
                    factor = 0.60
                    label = "Semester 3 & 4"
                # TY - From First Year -> sem 1,2,3,4 with 80% threshold
                elif class_select == "TY" and category == "From First Year":
                    sems = [1, 2, 3, 4]
                    factor = 0.80
                    label = "Semester 1 - 4"
                # B.Tech - Direct Second Year -> sem 3,4,5,6 with 80% threshold
                elif class_select == "B.Tech" and category == "From Direct Second Year":
                    sems = [3, 4, 5, 6]
                    factor = 0.80
                    label = "Semester 3 - 6"
                # B.Tech - From First Year -> sem 1-6 with 86% threshold
                elif class_select == "B.Tech" and category == "From First Year":
                    sems = [1, 2, 3, 4, 5, 6]
                    factor = 0.86
                    label = "Semester 1 - 6"
                # SY - From First Year -> sem 1 & 2 with 60% threshold
                elif class_select == "SY" and category == "From First Year":
                    sems = [1, 2]
                    factor = 0.60
                    label = "Semester 1 & 2"
                # FY - From First Year -> sem 1 & 2 (assuming same thresholds as SY)
                elif class_select == "FY" and category == "From First Year":
                    sems = [1, 2]
                    factor = 0.60
                    label = "Semester 1 & 2"
                else:
                    sems = None

                if sems:
                    st.subheader(label + " Credits")
                    totals = {}
                    earned = {}

                    # Render sem inputs in pairs per row for clarity
                    for i in range(0, len(sems), 2):
                        cols = st.columns(2)
                        for j in range(2):
                            if i + j < len(sems):
                                sem = sems[i + j]
                                with cols[j]:
                                    st.write(f"**Semester {sem}**")
                                    t_key_raw = f"sem{sem}_total_{class_select}_{category}"
                                    e_key_raw = f"sem{sem}_earned_{class_select}_{category}"
                                    t_key = _clean_key(t_key_raw)
                                    e_key = _clean_key(e_key_raw)
                                    totals[sem] = st.number_input(f"Sem {sem} - Total Credits (as per syllabus)", min_value=0, value=0, step=1, key=t_key)
                                    earned[sem] = st.number_input(f"Sem {sem} - Credits Earned", min_value=0, value=0, step=1, key=e_key)

                    if st.button("Calculate Credits", use_container_width=True, type="primary"):
                        total_sem_credits = sum(totals.values())
                        total_earned = sum(earned.values())
                        threshold = total_sem_credits * factor
                        percentage = (total_earned / total_sem_credits * 100) if total_sem_credits > 0 else 0
                        promoted = total_earned >= threshold

                        st.divider()
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Credits (Selected Semesters)", f"{total_sem_credits}")
                        with col2:
                            st.metric("Credits Earned", f"{total_earned}")
                        with col3:
                            st.metric("Progress", f"{percentage:.1f}%")

                        st.progress(min(percentage / 100, 1.0))
                        st.info(f"Promotion threshold: {factor * 100:.0f}% ({threshold:.1f} credits)")
                        if promoted:
                            st.success("🎉 Promoted - You have reached the required credits.")
                        else:
                            remaining = max(threshold - total_earned, 0)
                            st.warning(f"⚠️ Not promoted - You need {remaining:.1f} more credits to reach {factor * 100:.0f}%")
                else:
                    st.info("Please select a valid combination of category and class to view credit details.")

# Faculty pages
    elif st.session_state.role == 'faculty':
        if page == "ℹ️ About":
            st.title("About This System")
            st.markdown("""
            ### VVPIET Student Learning Management System
            
            This system allows students to provide structured feedback to faculty members.
            
            **Features:**
            - Rate faculty on multiple dimensions (1-10 scale)
            - 5 specific evaluation criteria
            - Overall rating
            - Anonymous feedback option
            
            **Questions:**
            1. Teaching Quality and Delivery
            2. Course Content Clarity and Organization
            3. Communication and Interaction Skills
            4. Quality of Feedback and Evaluation
            5. Subject Knowledge and Expertise
            """)

        elif page == "📅 Mark Attendance":
            st.title("📅 Mark Student Attendance — Monthly (Deprecated)")
            st.markdown("The monthly attendance entry was replaced by a daily attendance workflow.")
            st.warning("Please use the '🧾 Daily Attendance' page to mark students present/absent. Monthly rollups and downloads are available there.")
            if st.button("Go to Daily Attendance", use_container_width=True):
                st.session_state['nav_to_page'] = "🧾 Daily Attendance"
                safe_rerun()
        
        elif page == "🧾 Daily Attendance":
            st.title("🧾 Daily Attendance - Faculty")
            faculty_info = get_faculty_details(st.session_state.user_id)
            if not faculty_info:
                st.error("Faculty information not found")
            else:
                faculty_id, faculty_name, faculty_branch = faculty_info
                st.info(f"**You are:** {faculty_name} ({faculty_branch})")
                subjects = get_faculty_subjects(faculty_id)
                if not subjects:
                    st.info("No subjects assigned. Please ask admin to assign subjects.")
                else:
                    subj_map = {f"{s[1]} ({s[2]})": s for s in subjects}
                    subj_choice = st.selectbox("Select Subject", options=list(subj_map.keys()))
                    selected_subj = subj_map[subj_choice]
                    selected_subj_id = selected_subj[0]
                    selected_year = selected_subj[2]
                    att_date = st.date_input("Attendance Date")
                    students = get_students_by_branch_and_class(branch=faculty_branch, class_level=selected_year)
                    if not students:
                        st.info("No students found for this subject/branch.")
                    else:
                        st.markdown("**Daily Attendance Sheet — Mark present for each student:**")
                        # Render a simple tabular view: Roll Number, Name, Present checkbox
                        with st.form("daily_attendance_form"):
                            cols = st.columns([2, 2, 4, 2])
                            cols[0].write("**Roll Number**")
                            cols[1].write("**Username**")
                            cols[2].write("**Student Name**")
                            cols[3].write("**Present**")
                            present_ids = []
                            # Use a predictable key per student to preserve checkbox state during reruns
                            for s in students:
                                sid = s[0]
                                username = s[1] or ''
                                name = s[2] or ''
                                roll = s[3] or 'N/A'
                                c1, c2, c3, c4 = st.columns([2, 2, 4, 2])
                                c1.write(f"{roll}")
                                c2.write(f"{username}")
                                c3.write(f"{name}")
                                checked = c4.checkbox("", key=f"att_{selected_subj_id}_{att_date.isoformat()}_{sid}")
                                if checked:
                                    present_ids.append(sid)

                            submit_att = st.form_submit_button("Save Daily Attendance")
                            if submit_att:
                                date_str = att_date.isoformat()
                                # Save daily records
                                for s in students:
                                    sid = s[0]
                                    is_present = sid in present_ids
                                    save_daily_attendance(sid, faculty_id, selected_subj_id, date_str, is_present)

                                # After saving daily attendance, compute monthly rollup and persist into
                                # the monthly `attendance` table so students' overall attendance
                                # percentage (stored in users.attendance) is updated and visible to admin.
                                month = att_date.month
                                year = att_date.year
                                try:
                                    rollup_rows = get_monthly_attendance_rollup(faculty_id, selected_subj_id, month, year)
                                    # rollup_rows: list of (student_id, classes_attended, total_classes)
                                    for student_id, classes_attended, total_classes in rollup_rows:
                                        # Persist monthly attendance per student/subject/faculty
                                        save_attendance(student_id, faculty_id, selected_subj_id, month, year, classes_attended, total_classes)

                                        # Recompute the student's overall attendance percentage and update users.attendance
                                        try:
                                            pct = get_student_attendance_percentage(student_id)
                                            update_student_attendance(student_id, pct)
                                        except Exception:
                                            # Non-fatal: continue updating other students
                                            pass
                                except Exception:
                                    # If rollup fails, we still saved daily records; notify faculty
                                    st.warning("Saved daily records but failed to compute monthly rollup. Admins can regenerate reports.")

                                st.success("Daily attendance saved and monthly rollup updated.")
                        # Monthly download portal
                        st.divider()
                        st.subheader("📥 Monthly Attendance Report")
                        colm1, colm2 = st.columns(2)
                        with colm1:
                            dl_month = st.number_input("Report Month", min_value=1, max_value=12, value=att_date.month)
                        with colm2:
                            dl_year = st.number_input("Report Year", min_value=2020, max_value=2030, value=att_date.year)
                        if st.button("Generate Monthly CSV", use_container_width=True):
                            rows = get_monthly_attendance_rollup(faculty_id, selected_subj_id, dl_month, dl_year)
                            if not rows:
                                st.info("No attendance records found for this month.")
                            else:
                                # Build CSV with roll_number
                                csv_data = []
                                import io
                                for student_id, classes_attended, total_classes in rows:
                                    conn = sqlite3.connect(DB_PATH)
                                    cur = conn.cursor()
                                    cur.execute('SELECT username, name, roll_number FROM users WHERE id = ?', (student_id,))
                                    u = cur.fetchone()
                                    conn.close()
                                    username = u[0] if u else 'unknown'
                                    name = u[1] if u else 'unknown'
                                    roll = u[2] if u and len(u) > 2 else 'N/A'
                                    pct = (classes_attended / total_classes * 100) if total_classes > 0 else 0
                                    csv_data.append({'roll_number': roll, 'username': username, 'name': name, 'classes_attended': classes_attended, 'total_classes': total_classes, 'percentage': f"{pct:.1f}%"})
                                df = pd.DataFrame(csv_data)
                                csv_bytes = df.to_csv(index=False).encode('utf-8')
                                st.download_button("Download CSV", data=csv_bytes, file_name=f"attendance_{selected_subj[1]}_{dl_year}_{dl_month}.csv")
        
        elif page == "📒 Daily LER":
            st.title("📒 Daily LER (Lecture Entry Register)")
            faculty_info = get_faculty_details(st.session_state.user_id)
            if not faculty_info:
                st.error("Faculty information not found")
            else:
                faculty_id, faculty_name, faculty_branch = faculty_info
                st.info(f"**You are:** {faculty_name} ({faculty_branch})")
                subjects = get_faculty_subjects(faculty_id)
                if not subjects:
                    st.info("No subjects assigned. Please ask admin to assign subjects.")
                else:
                    subj_map = {f"{s[1]} ({s[2]})": s for s in subjects}
                    subj_choice = st.selectbox("Select Subject", options=list(subj_map.keys()))
                    selected_subj = subj_map[subj_choice]
                    selected_subj_id = selected_subj[0]
                    selected_year = selected_subj[2]

                    ler_date = st.date_input("Lecture Date")
                    # Manual time entry: do NOT auto-fill system time. Faculty should enter time themselves.
                    ler_time_str = st.text_input("Lecture Time (optional) — enter as HH:MM (24-hour)", value="", placeholder="e.g., 10:30")

                    # Determine students for this subject/branch
                    students = get_students_by_branch_and_class(branch=faculty_branch, class_level=selected_year)
                    date_str = ler_date.isoformat()

                    # Compute present ids from daily_attendance table and absent roll numbers
                    present_ids = get_present_student_ids_for_date(faculty_id, selected_subj_id, date_str)
                    total_present = len(present_ids)
                    absent_rolls = []
                    if students:
                        for s in students:
                            sid = s[0]
                            roll = s[3] or ''
                            if sid not in present_ids:
                                absent_rolls.append(str(roll))
                    absent_rolls_str = ", ".join([r for r in absent_rolls if r])

                    st.markdown("**Auto-filled attendance summary (from Daily Attendance):**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Present", f"{total_present}")
                    with col2:
                        st.write("**Absent Roll Numbers**")
                        st.text_area("Absent Roll Numbers (auto)", value=absent_rolls_str, height=80, key=f"ler_absent_{selected_subj_id}_{date_str}")

                    st.markdown("---")
                    with st.form("daily_ler_form"):
                        topic = st.text_input("Subject Topic Covered")
                        lecture_number = st.text_input("Lecture Number (e.g., Lecture 5)")
                        percent_syllabus = st.number_input("% of Syllabus Covered", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
                        sign = st.text_input("Sign (Faculty Name / Initials)", value=faculty_name)
                        remark = st.text_area("Remark (optional)")
                        submit_ler = st.form_submit_button("Save Daily LER Entry")

                    if submit_ler:
                        # Use manually entered time string (if provided) rather than system time
                        time_str = ler_time_str.strip() if ler_time_str else ''
                        lid = save_daily_ler(faculty_id, selected_subj_id, date_str, time_str, topic, lecture_number, float(percent_syllabus), int(total_present), absent_rolls_str, sign, remark)
                        if lid:
                            st.success(f"Daily LER entry saved (ID: {lid})")
                        else:
                            st.error("Failed to save Daily LER entry")
        elif page == "📚 Upload Resources":
            st.title("📚 Upload Assignments & Notes")
            # Get faculty info
            faculty_info = get_faculty_details(st.session_state.user_id)
            if not faculty_info:
                st.error("Faculty information not found")
            else:
                faculty_id, faculty_name, faculty_branch = faculty_info
                # Get subjects taught by this faculty
                all_subjects = get_all_subjects()
                faculty_year_levels = get_faculty_year_levels(faculty_id)
                faculty_subjects = [s for s in all_subjects if s[3] == faculty_branch and s[2] in faculty_year_levels] if all_subjects else []
                if not faculty_subjects:
                    st.warning(f"You have no subjects assigned yet. Contact admin to assign subjects.")
                else:
                    st.subheader("Upload Assignment or Notes")
                    # Faculty: Create Notice feature
                    with st.expander("📢 Create Notice (Faculty)"):
                        n_title = st.text_input("Notice Title (Faculty)", key="fac_notice_title")
                        n_content = st.text_area("Notice Content (Faculty)", key="fac_notice_content")
                        branches = get_branches() or ["All"]
                        target_branch = st.selectbox("Target Branch (All to show to all)", options=["All"] + branches, key="fac_notice_branch")
                        target_class = st.selectbox("Target Class (All to show to all)", options=["All", "FY", "SY", "TY", "Final Year"], key="fac_notice_class")
                        if st.button("Publish Notice (Faculty)", use_container_width=True):
                            tb = None if target_branch == "All" else target_branch
                            tc = None if target_class == "All" else target_class
                            nid = create_notice(n_title, n_content, target_branch=tb, target_class=tc, created_by_role='faculty', created_by_id=faculty_id)
                            if nid:
                                st.success("Notice published successfully")
                            else:
                                st.error("Failed to publish notice")
                    # Select subject
                    subject_options = {f"{s[1]} ({s[2]})": s[0] for s in faculty_subjects}
                    selected_subject_name = st.selectbox("Select Subject *", options=list(subject_options.keys()))
                    selected_subject_id = subject_options[selected_subject_name]
                    # Select resource type
                    resource_type = st.radio("Resource Type *", options=["Assignment", "Notes"], horizontal=True)
                    # Upload file
                    uploaded_file = st.file_uploader(f"Upload {resource_type} File", type=['pdf', 'docx', 'doc', 'txt', 'pptx', 'zip'])
                    # For assignments, add deadline
                    deadline = None
                    if resource_type == "Assignment":
                        st.subheader("Assignment Deadline (Optional)")
                        deadline_date = st.date_input("Deadline Date")
                        deadline_time = st.time_input("Deadline Time")
                        if deadline_date and deadline_time:
                            from datetime import datetime
                            deadline = datetime.combine(deadline_date, deadline_time).isoformat()
                    if st.button("Upload", use_container_width=True):
                        if not uploaded_file:
                            st.error("Please select a file to upload")
                        else:
                            # Save file to local directory
                            import os
                            upload_dir = "faculty_resources"
                            os.makedirs(upload_dir, exist_ok=True)
                            file_path = os.path.join(upload_dir, uploaded_file.name)
                            try:
                                with open(file_path, "wb") as f:
                                    f.write(uploaded_file.getbuffer())
                                # Add to database
                                rid = add_faculty_resource(
                                    faculty_id, 
                                    selected_subject_id,
                                    resource_type.lower(),
                                    uploaded_file.name,
                                    file_path,
                                    deadline
                                )
                                if rid:
                                    st.success(f"✓ {resource_type} uploaded successfully!")
                                else:
                                    st.error("Error saving to database")
                            except Exception as e:
                                st.error(f"Error uploading file: {str(e)}")
                    # Show uploaded resources
                    st.divider()
                    st.subheader("Your Uploaded Resources")
                    resources = get_faculty_resources(faculty_id)
                    if resources:
                        for res in resources:
                            res_id, subj_id, res_type, filename, uploaded_at, deadline = res
                            subj_name = next((s[1] for s in all_subjects if s[0] == subj_id), "Unknown")
                            col1, col2 = st.columns([4, 1])
                            col1.write(f"📄 {filename} ({res_type.capitalize()}) — {subj_name}")
                            if deadline:
                                col1.caption(f"Deadline: {deadline}")
                            col1.caption(f"Uploaded: {uploaded_at}")
                    else:
                        st.info("No resources uploaded yet")
        
        elif page == "🧪 Create Test":
            st.title("🧪 Create Test - Faculty")
            faculty_info = get_faculty_details(st.session_state.user_id)
            if not faculty_info:
                st.error("Faculty information not found")
            else:
                faculty_id, faculty_name, faculty_branch = faculty_info
                st.info(f"**You are:** {faculty_name} ({faculty_branch})")
                subjects = get_faculty_subjects(faculty_id)
                if not subjects:
                    st.info("No subjects assigned. Please ask admin to assign subjects.")
                else:
                    subj_map = {f"{s[1]} ({s[2]})": s for s in subjects}
                    subj_choice = st.selectbox("Select Subject for Test", options=list(subj_map.keys()))
                    selected_subj = subj_map[subj_choice]
                    selected_subj_id = selected_subj[0]
                    with st.form("create_test_form"):
                        title = st.text_input("Test Title")
                        description = st.text_area("Description (optional)")
                        col1, col2 = st.columns(2)
                        with col1:
                            start_date = st.date_input("Start date")
                            start_time = st.time_input("Start time")
                        with col2:
                            end_date = st.date_input("End date")
                            end_time = st.time_input("End time")
                        proctored = st.checkbox("Proctored?", value=False)
                        create_btn = st.form_submit_button("Create Test")
                    if create_btn:
                        start_dt = datetime.combine(start_date, start_time).replace(tzinfo=ZoneInfo("Asia/Kolkata"))
                        end_dt = datetime.combine(end_date, end_time).replace(tzinfo=ZoneInfo("Asia/Kolkata"))
                        start_ts = start_dt.isoformat()
                        end_ts = end_dt.isoformat()
                        if end_dt <= start_dt:
                            st.error("End date/time must be after start date/time")
                        else:
                            test_id = create_test(faculty_id, selected_subj_id, title, description, start_ts, end_ts, proctored)
                            if test_id:
                                st.success(f"Test created (ID: {test_id}). You can now add questions.")
                            else:
                                st.error("Failed to create test.")
                    st.markdown("---")
                    st.subheader("Add Questions to a Test")
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute('SELECT id, title FROM tests WHERE faculty_id = ? ORDER BY created_at DESC', (faculty_id,))
                    faculty_tests = cursor.fetchall()
                    conn.close()
                    if faculty_tests:
                        test_options = {f"{t[1]} [ID: {t[0]}]": t[0] for t in faculty_tests}
                        sel_display = st.selectbox("Select Test to add questions", options=list(test_options.keys()))
                        sel_test_id = test_options[sel_display]
                        with st.form("add_question_form"):
                            q_text = st.text_area("Question Text")
                            c1 = st.text_input("Choice 1")
                            c2 = st.text_input("Choice 2")
                            c3 = st.text_input("Choice 3")
                            c4 = st.text_input("Choice 4")
                            correct = st.selectbox("Correct Choice", options=[0,1,2,3], format_func=lambda i: f"Choice {i+1}")
                            marks = st.number_input("Marks", min_value=1, value=1)
                            add_q = st.form_submit_button("Add Question")
                        if add_q:
                            choices = [c1, c2, c3, c4]
                            add_test_question(sel_test_id, q_text, choices, correct, marks)
                            st.success("Question added to test.")
                        st.markdown("---")
                        st.subheader("View Attempts for a Test")
                        # Allow faculty to select one of their tests and view/download attempts
                        attempts_test_display = st.selectbox("Select Test to view attempts", options=list(test_options.keys()), key="attempts_test_select")
                        attempts_test_id = test_options[attempts_test_display]
                        
                        # Debug: Show which test is selected
                        st.caption(f"Selected Test ID: {attempts_test_id}")
                        
                        attempts = get_test_attempts_for_test(attempts_test_id)
                        if not attempts:
                            st.info("ℹ️ No attempts submitted for this test yet. Students who have taken this test will appear here.")
                            st.info("**Note:** Make sure the test is active (within start/end time) for students to take it.")
                        else:
                            st.success(f"✓ {len(attempts)} attempt(s) found")
                            # Build DataFrame for display and download
                            rows = []
                            for a in attempts:
                                aid, ttid, sid, answers_json, score, started_at, submitted_at, username, name = a
                                rows.append({
                                    'attempt_id': aid,
                                    'test_id': ttid,
                                    'student_id': sid,
                                    'username': username,
                                    'name': name,
                                    'score': score,
                                    'started_at': started_at,
                                    'submitted_at': submitted_at,
                                    'answers': answers_json
                                })
                            df_attempts = pd.DataFrame(rows)
                            st.dataframe(df_attempts, use_container_width=True, hide_index=True)
                            csv_bytes = df_attempts.to_csv(index=False).encode('utf-8')
                            st.download_button("Download Attempts CSV", data=csv_bytes, file_name=f"test_{attempts_test_id}_attempts.csv", mime='text/csv')
                    else:
                        st.info("No tests created yet. Create a test above.")

        elif page == "📄 Faculty Leaves":
            st.title("📄 Faculty Leave Records")
            faculty_info = get_faculty_details(st.session_state.user_id)
            if not faculty_info:
                st.error("Faculty information not found")
            else:
                faculty_id, faculty_name, faculty_branch = faculty_info
                st.info(f"**You are:** {faculty_name} ({faculty_branch})")

                # Show current usage / balances (CL=12, SL=6; DL/CO are not limited by default)
                usage = get_faculty_leave_usage(faculty_id)
                CL_used = usage.get('CL', 0)
                SL_used = usage.get('SL', 0)
                CL_total = 12
                SL_total = 6
                st.subheader("Leave Balances")
                col1, col2 = st.columns(2)
                col1.metric("CL", f"{CL_total - CL_used} remaining (used: {CL_used})")
                col2.metric("SL", f"{SL_total - SL_used} remaining (used: {SL_used})")

                # Leave request form
                st.subheader("Request Leave")
                with st.form("request_leave_form"):
                    leave_type = st.selectbox("Leave Type", options=["CL", "SL", "CO", "DL"])
                    duration_type = st.selectbox("Duration", options=["Half Day", "Full Day", "2 Days", "3 Days"])
                    start_date = st.date_input("Start Date")
                    end_date = st.date_input("End Date", value=start_date)
                    is_half = True if duration_type == "Half Day" else False
                    days_count = 0.5 if duration_type == "Half Day" else 1 if duration_type == "Full Day" else 2 if duration_type == "2 Days" else 3
                    alt_faculty = st.text_input("Alternative Faculty (Name) - Optional")
                    submit_leave = st.form_submit_button("Submit Leave")

                if submit_leave:
                    # Convert to strings for database
                    # Use the faculty table id (faculty_id) — not the users table id
                    res = submit_faculty_leave(faculty_id, leave_type, start_date.isoformat(), end_date.isoformat(), is_half_day=is_half, days_count=days_count, alt_faculty=alt_faculty)
                    if res:
                        st.success("Leave request submitted")
                    else:
                        st.error("Failed to submit leave request")

                # Show leave history
                leaves = get_faculty_leaves(faculty_id)
                if leaves:
                    st.subheader("Leave Requests History")
                    for l in leaves:
                        lid, fid, ltype, sdate, edate, is_half_day, dcount, alt, created_at = l
                        st.write(f"{ltype} — {sdate} to {edate} — {dcount} days — Alt: {alt or 'N/A'} — Requested at {created_at}")
                else:
                    st.info("No leave requests found.")

        elif page == "ℹ️ About":
            st.title("About This System - Faculty View")
            faculty_info = get_faculty_details(st.session_state.user_id)
            if faculty_info:
                faculty_id, faculty_name, faculty_branch = faculty_info
                st.info(f"**Faculty Name:** {faculty_name}\n**Branch:** {faculty_branch}")
                subjects = get_faculty_subjects(faculty_id)
                if subjects:
                    st.subheader("📚 Your Assigned Subjects")
                    for subj in subjects:
                        st.write(f"- {subj[1]} ({subj[2]})")
                else:
                    st.warning("No subjects assigned to you yet. Contact admin.")
            st.markdown("""
            ### VVPIET Student LMS - Faculty Features
            **Your Responsibilities:**
            - Mark student attendance for your subjects monthly
            - View feedback received from students
            - Track student performance through attendance data
            **How to use:**
            1. Go to "Mark Attendance" tab
            2. Select your subject and class
            3. Enter attendance data for each student in your branch
            4. Save the records
            Students with 60%+ attendance can submit feedback.
            """)
    
    # Admin pages
    elif st.session_state.role == 'admin':
        if page == "📊 Dashboard":
            st.title("📊 Admin Dashboard")
            
            feedbacks = get_all_feedback()
            stats = get_faculty_stats()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Feedbacks", len(feedbacks))
            with col2:
                # overall_rating is at index 11 in feedback tuples
                avg_overall = np.mean([f[11] for f in feedbacks if f[11]]) if feedbacks else 0
                st.metric("Average Rating", f"{avg_overall:.2f}/10")
            with col3:
                st.metric("Faculty Count", len(stats))
            
            st.divider()
            # Admin: Feedback scheduling UI
            st.divider()
            st.subheader("🗓️ Feedback Scheduling")
            current_sched = get_current_feedback_schedule()
            if current_sched:
                st.info(f"Current feedback window: {current_sched[0]} to {current_sched[1]}")
            else:
                st.info("No feedback scheduled currently.")

            with st.expander("Schedule new feedback window"):
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    start_date = st.date_input("Start date")
                    start_time = st.time_input("Start time")
                with col_s2:
                    end_date = st.date_input("End date", value=start_date)
                    end_time = st.time_input("End time", value=start_time)

                if st.button("Schedule Feedback", use_container_width=True):
                    tz = ZoneInfo("Asia/Kolkata")
                    start_dt = datetime.combine(start_date, start_time).replace(tzinfo=tz).isoformat()
                    end_dt = datetime.combine(end_date, end_time).replace(tzinfo=tz).isoformat()
                    schedule_feedback(start_dt, end_dt)
                    st.success("Feedback scheduled successfully.")
                    safe_rerun()

            st.subheader("📈 Faculty Statistics")
            
            if stats:
                df_stats = pd.DataFrame(stats, columns=['Faculty', 'Department', 'Year Level', 'Responses', 'Avg Rating'])
                st.dataframe(df_stats, use_container_width=True, hide_index=True)
            else:
                st.info("No feedback data available yet")
            
            st.divider()
            st.subheader("📋 Recent Submissions")

            if feedbacks:
                for fb in feedbacks[:10]:  # Show last 10
                    # fb indices: 0:id,1:created_at,2:fac_name,3:department,4:year_level,5:student_name,
                    # 6:q1,7:q2,8:q3,9:q4,10:q5,11:q6,12:q7,13:q8,14:q9,15:q10,16:overall,17:comments,18:subject
                    with st.expander(f"{fb[2]} ({fb[4]}) - {fb[1][:10]} (Overall: {fb[16]}/10)"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Faculty:** {fb[2]}")
                            st.write(f"**Department:** {fb[3]}")
                            st.write(f"**Year Level:** {fb[4]}")
                            st.write(f"**Subject:** {fb[18]}")
                            st.write(f"**Student:** {fb[5]}")
                            st.write(f"**Date:** {fb[1]}")
                        with col2:
                            st.write(f"**Ratings:**")
                            st.write(f"1. Fundamental Concepts & Subject Knowledge: {fb[6]}/10")
                            st.write(f"2. Preparation for Subject: {fb[7]}/10")
                            st.write(f"3. Knowledge of current trends/development: {fb[8]}/10")
                            st.write(f"4. Proficient in English & communication: {fb[9]}/10")
                            st.write(f"5. Teaching makes class interesting & interactive: {fb[10]}/10")
                            st.write(f"6. Punctuality of faculty: {fb[11]}/10")
                            st.write(f"7. Coverage of syllabus as prescribed: {fb[12]}/10")
                            st.write(f"8. Fulfillment of your learning expectations: {fb[13]}/10")
                            st.write(f"9. Behavior with students appropriate/rational: {fb[14]}/10")
                            st.write(f"10. Motivates students for study & career: {fb[15]}/10")
                        st.write(f"**Overall Rating:** {fb[16]}/10")
                        st.write(f"**Comments:** {fb[17] or 'None'}")
            else:
                st.info("No feedback submitted yet")

            # Student Access Control
            st.divider()
            st.subheader("🔒 Student Access Control")
            st.caption("Grant submission access to students who meet attendance threshold")
            students = get_all_students()
            if students:
                if st.button("Grant access to eligible students (attendance >= 60%)"):
                    count = 0
                    for s in students:
                        if s[2] is not None and s[2] >= 60:
                            set_student_access(s[0], True)
                            count += 1
                    st.success(f"Granted access to {count} student(s)")
                    students = get_all_students()

                # Show table and per-student controls
                for s in students:
                    sid, sname, satt, shas = s
                    cols = st.columns([3,2,2])
                    cols[0].write(f"**{sname}**")
                    cols[1].write(f"Attendance: {satt}%")
                    # checkbox to toggle access
                    new_access = cols[2].checkbox("Has Access", value=bool(shas), key=f"access_{sid}")
                    if new_access != bool(shas):
                        set_student_access(sid, new_access)
                        safe_rerun()
            else:
                st.info("No student accounts found")
            
            # Attendance by Faculty (admin view)
            st.divider()
            st.subheader("📚 Attendance by Faculty")
            faculties_all = get_faculty_list()
            fac_options = [f"{f[1]} ({f[2]})" for f in faculties_all] if faculties_all else []
            fac_select = st.selectbox("Select Faculty to view students", options=["All"] + fac_options)

            if fac_select and fac_select != "All":
                fid = next((f[0] for f in faculties_all if f"{f[1]} ({f[2]})" == fac_select), None)
                if fid:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute("SELECT DISTINCT student_name FROM feedback WHERE faculty_id = ?", (fid,))
                    rows = cur.fetchall()
                    conn.close()
            
            # Admin: Daily LER export
            st.divider()
            st.subheader("📒 Daily LER Records")
            all_fac = get_all_faculty()
            fac_options = [f"{f[1]} ({f[2]}) [ID:{f[0]}]" for f in all_fac] if all_fac else []
            sel_fac = st.selectbox("Filter by Faculty", options=["All"] + fac_options)
            colf1, colf2 = st.columns(2)
            with colf1:
                date_from = st.date_input("From Date", value=None)
            with colf2:
                date_to = st.date_input("To Date", value=None)

            if st.button("Generate Daily LER CSV"):
                fid_filter = None
                if sel_fac and sel_fac != "All":
                    # parse id from selection
                    try:
                        fid_filter = int(sel_fac.split("ID:")[-1].rstrip(']'))
                    except Exception:
                        fid_filter = None

                dfrom = date_from.isoformat() if date_from else None
                dto = date_to.isoformat() if date_to else None
                rows_ler = get_all_daily_ler(date_from=dfrom, date_to=dto, faculty_id=fid_filter)
                if not rows_ler:
                    st.info("No Daily LER records found for the selected filters.")
                else:
                    # Build DataFrame
                    df_rows = []
                    for r in rows_ler:
                        (lid, faculty_id_r, faculty_name, subject_id_r, subject_name, date_r, time_r, topic_r, lecture_number_r, percent_syllabus_r, total_present_r, absent_rolls_r, sign_r, remark_r, created_at_r) = r
                        df_rows.append({
                            'id': lid,
                            'faculty_id': faculty_id_r,
                            'faculty_name': faculty_name,
                            'subject_id': subject_id_r,
                            'subject_name': subject_name,
                            'date': date_r,
                            'time': time_r,
                            'topic': topic_r,
                            'lecture_number': lecture_number_r,
                            'percent_syllabus': percent_syllabus_r,
                            'total_present': total_present_r,
                            'absent_roll_numbers': absent_rolls_r,
                            'sign': sign_r,
                            'remark': remark_r,
                            'created_at': created_at_r
                        })
                    df_ler = pd.DataFrame(df_rows)
                    csv_bytes = df_ler.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Download Daily LER CSV", data=csv_bytes, file_name=f"daily_ler_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mime='text/csv')
            
        elif page == "🗂️ Faculty Leaves":
            st.title("🗂️ Faculty Leave Management")
            faculties_all = get_faculty_list()
            if faculties_all:
                fac_options = [f"{f[1]} ({f[2]})" for f in faculties_all]
                sel = st.selectbox("Select Faculty", options=["All"] + fac_options)
                if sel and sel != "All":
                    fid = next((f[0] for f in faculties_all if f"{f[1]} ({f[2]})" == sel), None)
                    if fid:
                        leaves = get_faculty_leaves(fid)
                        if not leaves:
                            st.info("No leave records for this faculty.")
                        else:
                            st.subheader("Leave Records")
                            for l in leaves:
                                lid, fid, ltype, sdate, edate, is_half_day, days_count, alt, created_at = l
                                st.write(f"{ltype} — {sdate} to {edate} — {days_count} days — Alt: {alt or 'N/A'} — Requested at: {created_at}")
                            # Download CSV
                            df = pd.DataFrame(leaves, columns=['id', 'faculty_id', 'leave_type', 'start_date', 'end_date', 'is_half_day', 'days_count', 'alt_faculty', 'created_at'])
                            csv_bytes = df.to_csv(index=False).encode('utf-8')
                            st.download_button("Download Leaves CSV", data=csv_bytes, file_name=f"faculty_{fid}_leaves.csv")
                else:
                    # Show all leaves across all faculty with download option
                    all_leaves = get_faculty_leaves()
                    if not all_leaves:
                        st.info("No leave records found")
                    else:
                        df_all = pd.DataFrame(all_leaves, columns=['id', 'faculty_id', 'leave_type', 'start_date', 'end_date', 'is_half_day', 'days_count', 'alt_faculty', 'created_at'])
                        # Join faculty names for readability
                        fac_map = {f[0]: f[1] for f in faculties_all}
                        df_all['faculty_name'] = df_all['faculty_id'].map(fac_map)
                        st.dataframe(df_all[['faculty_name','leave_type','start_date','end_date','days_count','alt_faculty','created_at']], use_container_width=True, hide_index=True)
                        csv_bytes = df_all.to_csv(index=False).encode('utf-8')
                        st.download_button("Download All Faculty Leaves CSV", data=csv_bytes, file_name=f"faculty_leaves_all.csv", mime='text/csv')
            else:
                st.info("No faculty records found")

            # Admin: Notices creation
            st.divider()
            st.subheader("📢 Notices")
            with st.expander("Create new notice"):
                n_title = st.text_input("Notice Title")
                n_content = st.text_area("Notice Content")
                branches = get_branches() or ["All"]
                target_branch = st.selectbox("Target Branch (All to show to all)", options=["All"] + branches)
                target_class = st.selectbox("Target Class (All to show to all)", options=["All", "FY", "SY", "TY", "Final Year"])
                if st.button("Publish Notice", use_container_width=True):
                    tb = None if target_branch == "All" else target_branch
                    tc = None if target_class == "All" else target_class
                    nid = create_notice(n_title, n_content, target_branch=tb, target_class=tc, created_by_role='admin', created_by_id=st.session_state.user_id)
                    if nid:
                        st.success("Notice published successfully")
                    else:
                        st.error("Failed to publish notice")

                    if not rows:
                        st.info("No feedback entries for this faculty yet.")
                    else:
                        total_att = 0
                        count_att = 0
                        st.markdown("Students who submitted feedback for this faculty:")
                        for r in rows:
                            sname = r[0]
                            user = get_user_by_username(sname)
                            if user:
                                uid = user[0]
                                attendance = user[3] if len(user) > 3 and user[3] is not None else 0
                                cols = st.columns([3,2,2])
                                cols[0].write(f"**{sname}**")
                                new_att = cols[1].number_input("Attendance (%)", min_value=0, max_value=100, value=int(attendance), key=f"att_{uid}")
                                if cols[2].button("Save", key=f"save_att_{uid}"):
                                    update_student_attendance(uid, int(new_att))
                                    st.success("Attendance updated")
                                    safe_rerun()
                                total_att += int(attendance)
                                count_att += 1
                            else:
                                st.write(f"- {sname} (not registered)")

                        if count_att:
                            avg_att = total_att / count_att
                            st.metric("Average Attendance (these students)", f"{avg_att:.1f}%")
        
        elif page == "👥 Student Attendance":
            st.title("👥 Student Attendance Records")
            st.markdown("View student attendance by year level and branch")
            
            # Admin: upload student roster (Excel)
            st.subheader("Upload Student Roster (Excel)")
            branches = get_branches() or []
            if branches:
                upload_branch = st.selectbox("Select Branch for these students", options=branches)
            else:
                upload_branch = st.text_input("Branch (enter department)")

            uploaded_file = st.file_uploader("Upload Excel (.xls/.xlsx) with columns: sr. no., roll no., PRN number, name, class", type=['xls', 'xlsx', 'csv'])
            if uploaded_file is not None:
                try:
                    # use pandas to read; allow csv as fallback
                    if str(uploaded_file.name).lower().endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)

                    # Normalize column names
                    cols = {c.lower().strip(): c for c in df.columns}
                    # Identify required columns
                    col_name = None
                    col_roll = None
                    col_prn = None
                    col_class = None
                    for lc, orig in cols.items():
                        if 'name' in lc and not col_name:
                            col_name = orig
                        if 'roll' in lc and not col_roll:
                            col_roll = orig
                        if 'prn' in lc and not col_prn:
                            col_prn = orig
                        if 'class' in lc and not col_class:
                            col_class = orig

                    if not col_name or not col_class:
                        st.error('Uploaded file must contain at least student name and class columns.')
                    else:
                        # If branch was selected, apply to all rows
                        df['branch'] = upload_branch
                        # Use roll/prn where available
                        if col_roll:
                            df['roll_number'] = df[col_roll].astype(str)
                        else:
                            df['roll_number'] = df[col_prn].astype(str) if col_prn else ''
                        df['prn'] = df[col_prn].astype(str) if col_prn else ''
                        df['student_name'] = df[col_name].astype(str)
                        df['class'] = df[col_class].astype(str)

                        # Sort by class
                        df_sorted = df.sort_values(by=['class', 'student_name'])

                        st.info(f"Preview: {len(df_sorted)} rows — will be assigned to branch: {upload_branch}")
                        st.dataframe(df_sorted.head(50))

                        if st.button('Import Students from Excel'):
                            inserted = 0
                            updated = 0
                            for _, row in df_sorted.iterrows():
                                name = str(row.get('student_name') or '').strip()
                                roll = str(row.get('roll_number') or '').strip()
                                prn = str(row.get('prn') or '').strip()
                                cls = str(row.get('class') or '').strip()
                                branch_val = str(row.get('branch') or upload_branch or '').strip()

                                if not name:
                                    continue

                                # Determine username: prefer PRN, then roll, then generated
                                username_candidate = prn or roll or None
                                conn = sqlite3.connect(DB_PATH)
                                cur = conn.cursor()
                                user_id = None
                                if roll:
                                    cur.execute('SELECT id FROM users WHERE roll_number = ? AND role = ?', (roll, 'student'))
                                    r = cur.fetchone()
                                    if r:
                                        user_id = r[0]
                                if not user_id and username_candidate:
                                    cur.execute('SELECT id FROM users WHERE username = ? AND role = ?', (username_candidate, 'student'))
                                    r = cur.fetchone()
                                    if r:
                                        user_id = r[0]

                                if user_id:
                                    # Update existing
                                    try:
                                        cur.execute('''UPDATE users SET name = ?, branch = ?, class = ?, roll_number = ? WHERE id = ?''', (name, branch_val, cls, roll, user_id))
                                        conn.commit()
                                        updated += 1
                                    except Exception:
                                        pass
                                else:
                                    # Create a new student user. Ensure unique username
                                    base_username = username_candidate or (roll or name.replace(' ', '_')).lower()
                                    username = base_username
                                    i = 1
                                    while True:
                                        try:
                                            pw = hash_password('student123')
                                            cur.execute('INSERT INTO users (username, password, role, name, roll_number, branch, class) VALUES (?, ?, ?, ?, ?, ?, ?)', (username, pw, 'student', name, roll, branch_val, cls))
                                            conn.commit()
                                            inserted += 1
                                            break
                                        except sqlite3.IntegrityError:
                                            # username exists, try suffix
                                            username = f"{base_username}_{i}"
                                            i += 1
                                        except Exception:
                                            break
                                conn.close()

                            st.success(f"Import finished — inserted: {inserted}, updated: {updated}")
                except Exception as e:
                    st.error(f"Failed to read uploaded file: {str(e)}")

            col1, col2 = st.columns(2)
            year_levels = ['All', 'FY', 'SY', 'TY', 'Final Year']
            branches = ['All'] + get_branches()
            
            with col1:
                selected_year_filter = st.selectbox("Filter by Year Level", options=year_levels)
            with col2:
                selected_branch_filter = st.selectbox("Filter by Branch", options=branches)
            
            year_param = selected_year_filter if selected_year_filter != 'All' else None
            branch_param = selected_branch_filter if selected_branch_filter != 'All' else None
            
            attendance_records = get_attendance_by_year_and_branch(year_level=year_param, branch=branch_param)
            
            if attendance_records:
                # Group and display
                st.subheader(f"Attendance Records - {selected_year_filter} | {selected_branch_filter}")
                
                # Create display DataFrame
                display_data = []
                for record in attendance_records:
                    sid, student_name, attended, total, subject, faculty, branch = record
                    if total > 0:
                        percentage = round((attended / total) * 100, 2)
                    else:
                        percentage = 0
                    
                    display_data.append({
                        'Student ID': sid,
                        'Student Name': student_name,
                        'Subject': subject,
                        'Faculty': faculty,
                        'Branch': branch,
                        'Classes Attended': attended,
                        'Total Classes': total,
                        'Attendance %': percentage
                    })
                
                if display_data:
                    df = pd.DataFrame(display_data)
                    
                    # Display as table
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Summary statistics
                    st.divider()
                    st.subheader("Summary Statistics")
                    col1, col2, col3 = st.columns(3)
                    
                    avg_attendance = df['Attendance %'].mean() if len(df) > 0 else 0
                    eligible_count = len(df[df['Attendance %'] >= 60])
                    total_count = len(df)
                    
                    with col1:
                        st.metric("Average Attendance", f"{avg_attendance:.1f}%")
                    with col2:
                        st.metric("Eligible for Feedback (>=60%)", f"{eligible_count}/{total_count}")
                    with col3:
                        st.metric("Ineligible (<60%)", f"{total_count - eligible_count}/{total_count}")
                    
                    # Filter by attendance status
                    st.divider()
                    st.subheader("Filtered View")
                    status_filter = st.radio("Show Students with:", options=["All", ">=60% Attendance (Eligible)", "<60% Attendance (Ineligible)"], horizontal=True)
                    
                    if status_filter == ">=60% Attendance (Eligible)":
                        filtered_df = df[df['Attendance %'] >= 60]
                    elif status_filter == "<60% Attendance (Ineligible)":
                        filtered_df = df[df['Attendance %'] < 60]
                    else:
                        filtered_df = df
                    
                    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
                    
                    # Download option
                    csv = filtered_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download as CSV",
                        data=csv,
                        file_name=f"attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No attendance records found")
            else:
                st.info("No attendance data available. Faculty members need to mark attendance first.")
        
        elif page == "📚 Manage Subjects":
            st.title("📚 Assign Subjects to Faculty")
            st.markdown("Manage which subjects each faculty member teaches")
            
            faculties = get_all_faculty_with_users()
            subjects = get_all_subjects()

            # Add Subject to DB form (always available to admin)
            st.subheader("Add Subject to Database")
            st.caption("Create a new subject record. Subjects are not pre-populated by default.")

            branches = get_branches()
            if branches:
                add_branch = st.selectbox("Department/Branch *", options=branches)
            else:
                add_branch = st.text_input("Department/Branch *")

            add_year_levels = get_year_levels()
            if not add_year_levels:
                add_year_levels = ['FY', 'SY', 'TY', 'Final Year']
            add_year = st.selectbox("Class/Year Level *", options=add_year_levels)

            add_subject_name = st.text_input("Subject Name *")
            add_subject_code = st.text_input("Subject Code (optional)")

            if st.button("Add Subject to DB", use_container_width=True):
                if not add_subject_name or not add_branch or not add_year:
                    st.error("Please provide Subject Name, Department and Class/Year Level")
                else:
                    sid = add_subject(add_subject_name.strip(), add_year, add_branch.strip(), add_subject_code.strip() if add_subject_code else None)
                    if sid:
                        st.success(f"✓ Subject '{add_subject_name}' added (ID: {sid})")
                        subjects = get_all_subjects()
                    else:
                        st.error("Error adding subject. It may already exist.")

            st.divider()

            # Remove Subject from DB
            st.subheader("Remove Subject from Database")
            st.caption("Delete a subject record and all its faculty assignments")
            
            if subjects:
                subject_options = {f"{s[1]} ({s[2]}) [Code: {s[4] or 'N/A'}]": s[0] for s in subjects}
                remove_subject_display = st.selectbox("Select subject to delete *", options=list(subject_options.keys()), key="remove_subj")
                
                if st.button("Delete Subject", use_container_width=True, key="btn_delete_subj"):
                    remove_subj_id = subject_options[remove_subject_display]
                    if delete_subject(remove_subj_id):
                        st.success(f"✓ Subject deleted successfully")
                        subjects = get_all_subjects()
                        st.rerun()
                    else:
                        st.error("Error deleting subject")
            else:
                st.info("No subjects in database to remove")

            st.divider()

            st.subheader("Assign Subjects to Faculty")
            st.caption("Link subjects to each faculty member for feedback collection")
            
            if not faculties:
                st.warning("No faculty members found in the system")
            else:
                # Create two columns: faculty selection and subject management
                col1, col2 = st.columns([2, 3])

                with col1:
                    st.subheader("Select Faculty")
                    faculty_names = [f"{f[1]} ({f[2]})" for f in faculties]
                    selected_faculty_display = st.selectbox("Choose a faculty member:", options=faculty_names)
                    selected_faculty_id = next((f[0] for f in faculties if f"{f[1]} ({f[2]})" == selected_faculty_display), None)

                if selected_faculty_id:
                    with col2:
                        st.subheader("Assigned Subjects")
                        assigned_subject_ids = get_faculty_subjects_with_ids(selected_faculty_id)

                        # Display assigned subjects
                        assigned_subjects = [s for s in subjects if s[0] in assigned_subject_ids] if subjects else []
                        if assigned_subjects:
                            for subj in assigned_subjects:
                                col1_sub, col2_sub = st.columns([4, 1])
                                # subj: (id, name, year_level, department, code)
                                subj_display = f"{subj[1]} ({subj[2]})"
                                if subj[3]:
                                    subj_display += f" — {subj[3]}"
                                if subj[4]:
                                    subj_display += f" [{subj[4]}]"
                                col1_sub.write(f"✓ {subj_display}")
                                if col2_sub.button("Remove", key=f"remove_{subj[0]}"):
                                    remove_subject_from_faculty(selected_faculty_id, subj[0])
                                    st.success(f"Removed '{subj[1]}' from {selected_faculty_display}")
                                    st.rerun()
                        else:
                            st.info("No subjects assigned yet")

                    # Add new subject section
                    st.divider()
                    st.subheader("Assign Existing Subject to Faculty")

                    available_subjects = [s for s in subjects if s[0] not in assigned_subject_ids] if subjects else []
                    if available_subjects:
                        subject_options = {f"{s[1]} ({s[2]})": s[0] for s in available_subjects}
                        selected_subject_display = st.selectbox("Select subject to add:", options=list(subject_options.keys()))

                        if st.button("Assign Subject", use_container_width=True):
                            selected_subject_id = subject_options[selected_subject_display]
                            if assign_subject_to_faculty(selected_faculty_id, selected_subject_id):
                                st.success(f"✓ '{selected_subject_display}' assigned to {selected_faculty_display}")
                                st.rerun()
                    else:
                        st.info("No subjects available in the database. Use 'Add Subject to Database' above to create subjects.")
        
        elif page == "👨‍🏫 Manage Faculty":
            st.title("👨‍🏫 Manage Faculty Year Levels")
            
            all_faculty = get_all_faculty()
            
            if all_faculty:
                st.subheader("Faculty Teaching Schedule")
                st.caption("Manage which year levels each faculty teaches")
                
                # Create a dataframe for better display
                faculty_df = pd.DataFrame(all_faculty, columns=['ID', 'Name', 'Department', 'Primary Year'])
                
                # Display current faculty
                st.write("**Current Faculty:**")
                st.dataframe(faculty_df, use_container_width=True, hide_index=True)
                
                st.divider()
                
                # Manage faculty year levels
                st.subheader("Add/Remove Year Level Assignments")
                
                faculty_options = {f"{f[1]} ({f[2]}) [ID: {f[0]}]": f[0] for f in all_faculty}
                
                selected_faculty_display = st.selectbox("Select Faculty *", options=faculty_options.keys())
                selected_faculty_id = faculty_options[selected_faculty_display]
                
                # Show current year level assignments for this faculty
                current_levels = get_faculty_year_levels(selected_faculty_id)
                st.info(f"**Currently teaches:** {', '.join(current_levels) if current_levels else 'None assigned'}")
                
                year_levels = get_year_levels()
                if not year_levels:
                    year_levels = ['FY', 'SY', 'TY', 'Final Year']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Add Year Level")
                    year_to_add = st.selectbox("Select Year Level to Add *", options=[y for y in year_levels if y not in current_levels])
                    if st.button("Add Year Level", use_container_width=True):
                        add_faculty_year_level(selected_faculty_id, year_to_add)
                        st.success(f"✓ Added {year_to_add} to faculty's teaching schedule")
                        st.rerun()
                
                with col2:
                    st.subheader("Remove Year Level")
                    if current_levels:
                        year_to_remove = st.selectbox("Select Year Level to Remove *", options=current_levels)
                        if st.button("Remove Year Level", use_container_width=True):
                            remove_faculty_year_level(selected_faculty_id, year_to_remove)
                            st.success(f"✓ Removed {year_to_remove} from faculty's teaching schedule")
                            st.rerun()
                    else:
                        st.info("No year levels assigned yet")
        
        elif page == "📈 Analytics":
            st.title("📈 Analytics & Visualizations")
            
            feedbacks = get_all_feedback()
            stats = get_faculty_stats()
            
            if feedbacks:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Rating Distribution")
                    ratings = [f[11] for f in feedbacks if f[11]]
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.hist(ratings, bins=10, color='#238636', edgecolor='black')
                    ax.set_xlabel('Overall Rating')
                    ax.set_ylabel('Count')
                    ax.set_title('Distribution of Ratings (1-10)')
                    ax.grid(axis='y', alpha=0.3)
                    st.pyplot(fig)
                
                with col2:
                    st.subheader("Average Rating by Faculty")
                    if stats:
                        faculties = [s[0] for s in stats]
                        avg_ratings = [s[4] if s[4] else 0 for s in stats]
                        
                        fig, ax = plt.subplots(figsize=(8, 5))
                        colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(faculties)))
                        ax.barh(faculties, avg_ratings, color=colors, edgecolor='black')
                        ax.set_xlabel('Average Rating (out of 10)')
                        ax.set_title('Faculty Performance')
                        ax.set_xlim(0, 10)
                        for i, v in enumerate(avg_ratings):
                            ax.text(v, i, f' {v:.2f}', va='center')
                        st.pyplot(fig)
                
                st.divider()
                st.subheader("Question-wise Analysis")
                
                q1_vals = [f[6] for f in feedbacks if f[6]]
                q2_vals = [f[7] for f in feedbacks if f[7]]
                q3_vals = [f[8] for f in feedbacks if f[8]]
                q4_vals = [f[9] for f in feedbacks if f[9]]
                q5_vals = [f[10] for f in feedbacks if f[10]]
                
                avg_data = {
                    'Teaching Quality': np.mean(q1_vals) if q1_vals else 0,
                    'Course Content': np.mean(q2_vals) if q2_vals else 0,
                    'Communication': np.mean(q3_vals) if q3_vals else 0,
                    'Feedback Quality': np.mean(q4_vals) if q4_vals else 0,
                    'Subject Knowledge': np.mean(q5_vals) if q5_vals else 0,
                }
                
                fig, ax = plt.subplots(figsize=(10, 5))
                questions = list(avg_data.keys())
                averages = list(avg_data.values())
                ax.bar(questions, averages, color='#1f6feb', edgecolor='black')
                ax.set_ylabel('Average Rating (out of 10)')
                ax.set_title('Average Ratings by Question')
                ax.set_ylim(0, 10)
                for i, v in enumerate(averages):
                    ax.text(i, v, f'{v:.2f}', ha='center', va='bottom')
                plt.xticks(rotation=45, ha='right')
                st.pyplot(fig)
            else:
                st.info("No feedback data available for analysis")
        
        elif page == "📋 Export Data":
            st.title("📋 Export Feedback Data")
            
            feedbacks = get_all_feedback()
            
            if feedbacks:
                # get_all_feedback returns: id, created_at, fac_name, department, year_level, student_name,
                # q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, overall_rating, comments, subject (19 columns)
                df = pd.DataFrame(feedbacks, columns=[
                    'ID', 'Date', 'Faculty', 'Department', 'Year Level', 'Student',
                    'Q1: Fundamental Concepts & Subject Knowledge', 'Q2: Preparation for Subject',
                    'Q3: Knowledge of current trends/development', 'Q4: Proficient in English & communication',
                    'Q5: Teaching makes class interesting & interactive', 'Q6: Punctuality of faculty',
                    'Q7: Coverage of syllabus as prescribed', 'Q8: Fulfillment of your learning expectations',
                    'Q9: Behavior with students appropriate/rational', 'Q10: Motivates students for study & career',
                    'Overall Rating', 'Comments', 'Subject'
                ])
                
                # Remove ID column for export
                df_export = df.drop(columns=['ID'])
                
                csv = df_export.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                st.divider()
                st.subheader("Preview")
                st.dataframe(df_export, use_container_width=True, hide_index=True)
            else:
                st.info("No feedback data available to export")
        
        elif page == "🐛 Debug: Test Attempts":
            st.title("🐛 Debug: All Test Attempts")
            st.caption("Admin-only view: inspect all test attempts in the system")
            
            # First, show all tests in the system
            st.subheader("📋 All Tests in System")
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT t.id, t.title, t.faculty_id, f.name, t.start_ts, t.end_ts
                FROM tests t
                LEFT JOIN faculty f ON t.faculty_id = f.id
                ORDER BY t.created_at DESC
            ''')
            all_tests = cursor.fetchall()
            if all_tests:
                test_rows = []
                for tid, ttitle, fid, fname, start, end in all_tests:
                    test_rows.append({
                        'test_id': tid,
                        'title': ttitle or 'N/A',
                        'faculty_id': fid,
                        'faculty_name': fname or 'Unknown',
                        'start_ts': start or 'N/A',
                        'end_ts': end or 'N/A'
                    })
                df_tests = pd.DataFrame(test_rows)
                st.dataframe(df_tests, use_container_width=True, hide_index=True)
            else:
                st.info("No tests created yet.")
            
            st.divider()
            
            # Query all attempts across all tests
            st.subheader("🧪 All Test Attempts")
            cursor.execute('''
                SELECT ta.id, ta.test_id, ta.student_id, ta.answers, ta.score, ta.started_at, ta.submitted_at, 
                       u.username, u.name, u.roll_number, t.title
                FROM test_attempts ta
                LEFT JOIN users u ON ta.student_id = u.id
                LEFT JOIN tests t ON ta.test_id = t.id
                ORDER BY ta.submitted_at DESC
            ''')
            all_attempts = cursor.fetchall()
            conn.close()
            
            if not all_attempts:
                st.info("ℹ️ No test attempts found in the system. Students need to take tests for attempts to appear here.")
            # Admin helper: allow seeding a demo attempt for a selected test and student
            st.divider()
            st.subheader("🔧 Admin: Seed Demo Attempt")
            try:
                conn2 = sqlite3.connect(DB_PATH)
                cur2 = conn2.cursor()
                cur2.execute("SELECT id, username, name FROM users WHERE role = 'student' ORDER BY id")
                student_rows = cur2.fetchall()
                cur2.execute('SELECT id, title FROM tests ORDER BY id')
                test_rows = cur2.fetchall()
                conn2.close()
            except Exception:
                student_rows = []
                test_rows = []

            if student_rows and test_rows:
                student_map = {f"{s[1]} ({s[2] or 'NoName'}) [ID:{s[0]}]": s[0] for s in student_rows}
                test_map = {f"{t[1] or 'NoTitle'} [ID:{t[0]}]": t[0] for t in test_rows}
                sel_student = st.selectbox("Select student for demo attempt", options=list(student_map.keys()))
                sel_test = st.selectbox("Select test for demo attempt", options=list(test_map.keys()))
                if st.button("Seed demo attempt for selected test"):
                    sid = student_map[sel_student]
                    tid = test_map[sel_test]
                    demo_answers = {}
                    # Build a minimal answers dict based on available questions
                    qs = get_test_questions(tid)
                    for q in qs:
                        # choose first option (index 0) as demo answer
                        demo_answers[str(q['id'])] = 0
                    try:
                        now_iso = datetime.now(ZoneInfo('Asia/Kolkata')).isoformat()
                        r = submit_test_attempt(tid, sid, demo_answers, started_at=now_iso, submitted_at=now_iso)
                        st.success(f"Seeded demo attempt — attempt_id: {r.get('attempt_id')} score: {r.get('score')}")
                        # Refresh view by rerunning (so attempts list updates)
                        safe_rerun()
                    except Exception as e:
                        st.error(f"Failed to seed demo attempt: {str(e)}")
            else:
                st.metric("Total Attempts", len(all_attempts))
                st.divider()
                
                # Build DataFrame for display
                rows = []
                for att in all_attempts:
                    attempt_id, test_id, student_id, answers_json, score, started_at, submitted_at, username, name, roll_number, test_title = att
                    rows.append({
                        'attempt_id': attempt_id,
                        'test_id': test_id,
                        'test_title': test_title or 'N/A',
                        'student_id': student_id,
                        'username': username or 'Unknown',
                        'name': name or 'Unknown',
                        'roll_number': roll_number or 'N/A',
                        'score': score or 0,
                        'submitted_at': submitted_at or 'N/A',
                        'answers_json': answers_json or ''
                    })
                
                df_attempts = pd.DataFrame(rows)
                
                # Display options
                col1, col2 = st.columns(2)
                with col1:
                    search_field = st.selectbox("Search by:", options=['All', 'Test Title', 'Username', 'Roll Number'])
                with col2:
                    search_term = st.text_input("Search term")
                
                # Filter results
                if search_term:
                    if search_field == 'Test Title':
                        df_filtered = df_attempts[df_attempts['test_title'].str.contains(search_term, case=False, na=False)]
                    elif search_field == 'Username':
                        df_filtered = df_attempts[df_attempts['username'].str.contains(search_term, case=False, na=False)]
                    elif search_field == 'Roll Number':
                        df_filtered = df_attempts[df_attempts['roll_number'].str.contains(search_term, case=False, na=False)]
                    else:
                        df_filtered = df_attempts
                else:
                    df_filtered = df_attempts
                
                st.subheader(f"Attempts ({len(df_filtered)} of {len(df_attempts)})")
                
                # Display table
                display_df = df_filtered[['attempt_id', 'test_title', 'username', 'name', 'roll_number', 'score', 'submitted_at']]
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                # Download options
                st.divider()
                st.subheader("Export")
                col1, col2 = st.columns(2)
                
                with col1:
                    csv_bytes = df_filtered.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Filtered (CSV)",
                        data=csv_bytes,
                        file_name=f"test_attempts_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime='text/csv',
                        use_container_width=True
                    )
                
                with col2:
                    csv_all = df_attempts.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download All (CSV)",
                        data=csv_all,
                        file_name=f"test_attempts_all_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime='text/csv',
                        use_container_width=True
                    )
                
                # Detailed view
                st.divider()
                st.subheader("Detailed Attempt View")
                selected_attempt_id = st.selectbox("Select attempt to view details:", options=df_filtered['attempt_id'].tolist())
                
                if selected_attempt_id:
                    selected_row = df_filtered[df_filtered['attempt_id'] == selected_attempt_id].iloc[0]
                    st.write(f"**Attempt ID:** {selected_row['attempt_id']}")
                    st.write(f"**Test:** {selected_row['test_title']} (ID: {selected_row['test_id']})")
                    st.write(f"**Student:** {selected_row['name']} (Roll: {selected_row['roll_number']}, Username: {selected_row['username']})")
                    st.write(f"**Score:** {selected_row['score']}")
                    st.write(f"**Submitted at:** {selected_row['submitted_at']}")
                    
                    # Show answers in expandable section
                    with st.expander("View Answers (JSON)"):
                        st.code(selected_row['answers_json'], language='json')
        
        elif page == "ℹ️ About":
            st.title("About This System")
            st.markdown("""
            ### Faculty Feedback Collection System
            
            **Admin Features:**
            - View all feedback submissions
            - Generate analytics and charts
            - Export feedback data as CSV
            - Monitor faculty performance
            
            **System Capabilities:**
            - Multi-dimensional faculty evaluation
            - 10-point rating scale
            - Real-time statistics
            - Data visualization with charts
            """)
            
            st.divider()
            st.subheader("📄 Documentation")
            st.write("Download comprehensive documentation of the application including features, user roles, and technical details.")
            
            try:
                pdf_buffer = generate_application_documentation()
                st.download_button(
                    label="📥 Download Application Documentation (PDF)",
                    data=pdf_buffer,
                    file_name=f"LMS_Documentation_{datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error generating documentation: {str(e)}")

# Global footer: prepared by line shown on all pages at the bottom
st.markdown("---")
st.markdown(
    "<div style='text-align:center; font-size:12px; color:#fff; background-color:#1f4788; padding:12px; border-radius:5px;'>"
    "<strong style='color:#fff;'>Prepared by: Prof. Amir M. Usman Wagdarikar</strong><br>"
    "<span style='color:#e0e0e0;'>Asst. Prof. Electronics and Telecommunication Engineering, VVP Institute of Engineering and technology, Solapur</span>"
    "</div>",
    unsafe_allow_html=True
)
