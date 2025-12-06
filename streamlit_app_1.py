import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sqlite3
import hashlib
import os

# Page config
st.set_page_config(page_title="VVPIET Student LMS", layout="wide", initial_sidebar_state="expanded")

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

    # Faculty-Year Level mapping (allows faculty to teach at multiple year levels)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty_year_level (
            faculty_id INTEGER NOT NULL,
            year_level TEXT NOT NULL,
            PRIMARY KEY (faculty_id, year_level),
            FOREIGN KEY(faculty_id) REFERENCES faculty(id)
        )
    ''')

    # Feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY,
            student_name TEXT,
            faculty_id INTEGER NOT NULL,
            year_level TEXT NOT NULL,
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
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY DEFAULT 1,
        feedback_enabled INTEGER DEFAULT 0,
        feedback_date DATE,
        feedback_time TIME
        )
    ''')
# Insert a default settings record if it doesn't exist
    cursor.execute("INSERT OR IGNORE INTO settings (id) VALUES (1)")
   
    conn.commit()
    
    # Add default faculty if empty
    cursor.execute("SELECT COUNT(*) FROM faculty")
    if cursor.fetchone()[0] == 0:
        faculty_list = [
            ('Dr. Rajesh Kumar', 'Computer science & engineering', 'FY'),
            ('Prof. Anita Singh', 'Mechanical Engineering', 'SY'),
            ('Dr. Priya Patel', 'Electrical engineering', 'TY'),
            ('Prof. Suresh Verma', 'Civil Engineering', 'Final Year'),
            ('Dr. Meera Sharma', 'Basic sciences & Humanities', 'FY'),
            ('Prof. Vikram Gupta', 'Electronics and Telecommunication Engineering', 'SY'),
            ('Dr. Neha Verma', 'Artificial Intelligence & Data science engineering', 'TY'),
        ]
        cursor.executemany('INSERT INTO faculty (name, department, year_level) VALUES (?, ?, ?)', faculty_list)
        conn.commit()

    # Subjects table and faculty-subject mapping
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            year_level TEXT NOT NULL,
            department TEXT,
            code TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty_subject (
            faculty_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            PRIMARY KEY (faculty_id, subject_id),
            FOREIGN KEY(faculty_id) REFERENCES faculty(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    ''')

    # Ensure subjects table has 'department' and 'code' columns for existing DBs
    cursor.execute("PRAGMA table_info(subjects)")
    subj_cols = [row[1] for row in cursor.fetchall()]
    if 'department' not in subj_cols:
        try:
            cursor.execute("ALTER TABLE subjects ADD COLUMN department TEXT")
        except Exception:
            pass
    if 'code' not in subj_cols:
        try:
            cursor.execute("ALTER TABLE subjects ADD COLUMN code TEXT")
        except Exception:
            pass

    # Faculty resources table (assignments and notes)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty_resources (
            id INTEGER PRIMARY KEY,
            faculty_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            resource_type TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            deadline TIMESTAMP,
            FOREIGN KEY(faculty_id) REFERENCES faculty(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
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
            classes_attended INTEGER DEFAULT 0,
            total_classes INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(student_id) REFERENCES users(id),
            FOREIGN KEY(faculty_id) REFERENCES faculty(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id),
            UNIQUE(student_id, faculty_id, subject_id, month, year)
        )
    ''')
    conn.commit()

    # No default subjects are seeded. Subjects should be added by admin via the Manage Subjects page.
    # Existing faculty_subject mappings are left unchanged.
    pass
    
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
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


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

def submit_feedback(student_name, faculty_id, year_level, q1, q2, q3, q4, q5, overall, comments):
    """Submit feedback to database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (student_name, faculty_id, year_level, q1_teaching_quality, q2_course_content,
                            q3_communication, q4_feedback_quality, q5_subject_knowledge, 
                            overall_rating, comments)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (student_name or 'Anonymous', faculty_id, year_level, q1, q2, q3, q4, q5, overall, comments))
    conn.commit()
    conn.close()
    return True

def get_all_feedback():
    """Get all feedback with faculty names."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT f.id, f.created_at, fac.name, fac.department, fac.year_level, f.student_name,
               f.q1_teaching_quality, f.q2_course_content, f.q3_communication,
               f.q4_feedback_quality, f.q5_subject_knowledge, f.overall_rating, f.comments
        FROM feedback f
        JOIN faculty fac ON f.faculty_id = fac.id
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
    """Get students filtered by branch and class/year level."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = "SELECT id, username, name, branch, class FROM users WHERE role = 'student'"
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
    cursor.execute('''INSERT OR REPLACE INTO attendance 
                      (student_id, faculty_id, subject_id, month, year, classes_attended, total_classes, updated_at)
                      VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)''',
                   (student_id, faculty_id, subject_id, month, year, classes_attended, total_classes))
    conn.commit()
    conn.close()

def get_attendance_for_month(faculty_id, subject_id, month, year):
    """Get all attendance records for a faculty's subject for a specific month."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT student_id, classes_attended, total_classes FROM attendance
                      WHERE faculty_id = ? AND subject_id = ? AND month = ? AND year = ?
                      ORDER BY student_id''',
                   (faculty_id, subject_id, month, year))
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

def get_all_subjects():
    """Get all available subjects."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, year_level, department, code FROM subjects ORDER BY year_level, name')
    rows = cursor.fetchall()
    conn.close()
    return rows

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
def get_feedback_settings():
    """Fetches the feedback settings from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT feedback_enabled, feedback_date, feedback_time FROM settings WHERE id = 1")
    settings = cursor.fetchone()
    conn.close()
    return settings

def update_feedback_settings(enabled, date, time):
    """Updates the feedback settings in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE settings SET feedback_enabled = ?, feedback_date = ?, feedback_time = ? WHERE id = 1",
        (enabled, date, time)
    )
    conn.commit()
    conn.close()
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
            page = st.radio("Navigation", ["📝 Submit Feedback", "💰 Credit Calculator", "ℹ️ About"])
        elif st.session_state.role == 'faculty':
            page = st.radio("Navigation", ["📅 Mark Attendance", "📚 Upload Resources", "ℹ️ About"])
        else:  # admin
            page = st.radio("Navigation", ["📊 Dashboard", "👥 Student Attendance", "📚 Manage Subjects", "👨‍🏫 Manage Faculty", "📈 Analytics", "📋 Export Data", "ℹ️ About"])
    else:
        page = st.radio("Navigation", ["🔐 Login", "📝 Register"])

# Main content area
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
        
        st.info("Demo Credentials:\n\n**Student:** username: student | password: student123\n\n**Admin:** username: admin | password: admin123\n\n**Faculty:** username: rajesh_kumar or anita_singh | password: faculty123")
    
    elif page == "📝 Register":
        st.title("📝 Register")
        
        reg_type = st.radio("Select Registration Type:", ["Student", "Faculty"], horizontal=True)
        
        if reg_type == "Student":
            st.subheader("Student Registration")
            with st.form("student_register_form"):
                name = st.text_input("Full Name *")
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
                if not name or not new_username or not new_password:
                    st.error("Please fill all required fields")
                elif new_password != confirm_password:
                    st.error("Passwords don't match!")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    try:
                        cursor.execute('INSERT INTO users (username, password, role, name, branch, class) VALUES (?, ?, ?, ?, ?, ?)',
                                      (new_username, hash_password(new_password), 'student', name, selected_branch, selected_class))
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
        if page == "📝 Submit Feedback":
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
                
                # Create tabs for different sections
                tab1, tab2, tab3 = st.tabs(["📝 Submit Feedback", "📥 Download Resources", "📊 My Attendance"])
                
                # TAB 1: Submit Feedback
                with tab1:
                    st.subheader("Submit Faculty Feedback")

                    # Get year level from student's class (FY, SY, TY, Final Year mapping)
                    year_level_map = {'FY': 'FY', 'SY': 'SY', 'TY': 'TY', 'Final Year': 'Final Year'}
                    # If class has numbers like "2A" or "2B", map to SY
                    student_year_level = 'SY' if student_class and student_class[0] == '2' else 'FY' if student_class and student_class[0] == '1' else 'TY' if student_class and student_class[0] == '3' else 'Final Year'
                    
                    st.info(f"Showing subjects and faculty for: **{student_year_level}**")
                    
                    # Get student's attendance percentage
                    user_attendance_pct = get_student_attendance_percentage(user_id) if user_id else 0
                    user_has_access = user_attendance_pct >= 60 if user_id else False

                    # Determine faculties to show - ONLY from student's branch and year level
                    subjects = get_subjects_by_year(student_year_level)
                    subject_options = [s[1] for s in subjects if s[3] == student_branch] if subjects else []
                    subject_options = ["All"] + subject_options
                    selected_subject = st.selectbox("Select Subject (optional)", options=subject_options, key="fb_subject")

                    if selected_subject and selected_subject != "All":
                        subj = next((s for s in subjects if s[1] == selected_subject and s[3] == student_branch), None)
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
                                selected_faculty = st.selectbox(
                                    "Select Faculty *",
                                    options=faculty_dict.keys()
                                )

                                st.markdown("### Rate the following aspects (1-10)")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    q1 = st.number_input("Teaching Quality", min_value=1, max_value=10, value=5, step=1)
                                    q3 = st.number_input("Communication Skills", min_value=1, max_value=10, value=5, step=1)
                                    q5 = st.number_input("Subject Knowledge", min_value=1, max_value=10, value=5, step=1)

                                with col2:
                                    q2 = st.number_input("Course Content Clarity", min_value=1, max_value=10, value=5, step=1)
                                    q4 = st.number_input("Feedback Quality", min_value=1, max_value=10, value=5, step=1)

                                with col3:
                                    overall = st.number_input("Overall Rating", min_value=1, max_value=10, value=5, step=1)

                                comments = st.text_area("Additional Comments (optional)", height=100)
                                submitted = st.form_submit_button("Submit Feedback", use_container_width=True)

                            if submitted:
                                faculty_id = faculty_dict[selected_faculty]
                                if submit_feedback(feedback_student_name, faculty_id, student_year_level, int(q1), int(q2), int(q3), int(q4), int(q5), int(overall), comments):
                                    st.success("✓ Feedback submitted successfully!")
                                    st.balloons()
                                else:
                                    st.error("Error submitting feedback")
                
                # TAB 2: Download Resources
                with tab2:
                    st.subheader("Download Assignments & Notes")
                    
                    # Get student's year level (map from class)
                    student_year_level = 'SY' if student_class and student_class[0] == '2' else 'FY' if student_class and student_class[0] == '1' else 'TY' if student_class and student_class[0] == '3' else 'Final Year'
                    
                    # Get resources for student's year level and branch
                    resources = get_subject_resources_for_student(student_year_level, student_branch)
                    
                    if resources:
                        st.info(f"Resources available for {student_year_level} — {student_branch}")
                        
                        # Group by subject
                        by_subject = {}
                        for res in resources:
                            res_id, filename, res_type, subject_name, faculty_name, uploaded_at, deadline = res
                            if subject_name not in by_subject:
                                by_subject[subject_name] = []
                            by_subject[subject_name].append((filename, res_type, faculty_name, uploaded_at, deadline))
                        
                        for subject, items in by_subject.items():
                            with st.expander(f"📚 {subject}"):
                                for filename, res_type, faculty_name, uploaded_at, deadline in items:
                                    col1, col2 = st.columns([4, 1])
                                    col1.write(f"📄 {filename} ({res_type.capitalize()})")
                                    col1.caption(f"By: {faculty_name} | Uploaded: {uploaded_at}")
                                    if deadline and res_type == "assignment":
                                        col1.caption(f"⏰ Deadline: {deadline}")
                                    col2.download_button(
                                        label="⬇️",
                                        data=open(f"faculty_resources/{filename}", "rb").read() if os.path.exists(f"faculty_resources/{filename}") else b"",
                                        file_name=filename,
                                        key=f"download_{res_id}_{filename}"
                                    )
                    else:
                        st.info(f"No resources available yet for {student_year_level} in {student_branch}")
                
                # TAB 3: My Attendance
                with tab3:
                    st.subheader("Your Attendance Record")
                    
                    user_attendance_pct = get_student_attendance_percentage(user_id) if user_id else 0
                    
                    # Show attendance as metric
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
                    ''', (student_id,))
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
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    c_completed = st.number_input("Credits Already Completed", min_value=0, value=0, step=1)
                with col2:
                    c_semester = st.number_input("Credits This Semester", min_value=0, value=0, step=1)
                with col3:
                    c_required = st.number_input("Total Credits Required", min_value=1, value=160, step=1)
                
                if st.button("Calculate Progress", use_container_width=True, type="primary"):
                    total_after, pct = calculate_credit_progress(c_completed, c_semester, c_required)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Credits After Semester", f"{total_after}")
                    with col2:
                        st.metric("Degree Progress", f"{pct:.1f}%")
                    
                     # Show progress bar
                    st.progress(min(pct / 100, 1.0))
                    st.caption(f"Credits completed: {total_after} / {c_required}")
                    
                    if total_after >= c_required:
                        st.success("🎉 Congratulations! You've completed all required credits!")
                    else:
                        remaining = c_required - total_after
                        st.info(f"📚 You need {remaining} more credits to complete your degree.")
        
        elif page == "ℹ️ About":
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
    
    # Faculty pages
    elif st.session_state.role == 'faculty':
        if page == "📅 Mark Attendance":
            st.title("📅 Mark Student Attendance")
            st.markdown("Record your students' attendance for the current month")
            
            # Get complete faculty details (id, name, department)
            faculty_info = get_faculty_details(st.session_state.user_id)
            if not faculty_info:
                st.error("Faculty record not found for your account")
            else:
                faculty_id, faculty_name, faculty_branch = faculty_info
                st.info(f"**You are:** {faculty_name} ({faculty_branch})")
                
                # Get faculty's subjects
                subjects = get_faculty_subjects(faculty_id)
                if not subjects:
                    st.warning("No subjects assigned to you yet")
                else:
                    # Top row: Class and Subject (Branch is fixed to faculty's branch)
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        class_options = ["All", "FY", "SY", "TY", "Final Year"]
                        selected_class = st.selectbox("Select Class/Year", options=class_options)
                    
                    with col2:
                        subject_options = {f"{s[1]} ({s[2]})": s[0] for s in subjects}
                        selected_subject_display = st.selectbox("Select Subject", options=list(subject_options.keys()))
                        selected_subject_id = subject_options[selected_subject_display]
                    
                    # Get current month and year
                    from datetime import datetime
                    now = datetime.now()
                    col1, col2 = st.columns(2)
                    with col1:
                        month = st.number_input("Month", min_value=1, max_value=12, value=now.month)
                    with col2:
                        year = st.number_input("Year", min_value=2020, max_value=2030, value=now.year)
                    
                    st.subheader(f"Mark Attendance: {selected_subject_display}")
                    st.caption(f"Branch: {faculty_branch} | Class: {selected_class} | {month}/{year}")
                    
                    # Get filtered students - ONLY from faculty's branch
                    class_param = selected_class if selected_class != "All" else None
                    students = get_students_by_branch_and_class(branch=faculty_branch, class_level=class_param)
                    
                    if students:
                        st.markdown("**Enter attendance for each student:**")
                        
                        # Create form for bulk entry
                        attendance_data = {}
                        cols = st.columns([2, 2, 2, 2])
                        cols[0].write("**Student Name**")
                        cols[1].write("**Class**")
                        cols[2].write("**Classes Attended**")
                        cols[3].write("**Total Classes**")
                        
                        for student in students:
                            student_id, student_username, student_name, student_branch, student_class = student
                            cols = st.columns([2, 2, 2, 2])
                            cols[0].write(student_name or student_username)
                            cols[1].write(f"{student_class}")
                            attended = cols[2].number_input("Attended", min_value=0, value=0, key=f"att_{student_id}_{month}_{year}")
                            total = cols[3].number_input("Total", min_value=0, value=1, key=f"total_{student_id}_{month}_{year}")
                            if attended > 0 or total > 0:
                                attendance_data[student_id] = (attended, total)
                        
                        if st.button("Save Attendance", use_container_width=True):
                            if attendance_data:
                                for student_id, (attended, total) in attendance_data.items():
                                    save_attendance(student_id, faculty_id, selected_subject_id, month, year, attended, total)
                                st.success(f"✓ Attendance saved for {len(attendance_data)} students")
                                safe_rerun()
                            else:
                                st.warning("Please enter attendance for at least one student")
                    else:
                        st.info(f"No students found in {faculty_branch} for {selected_class}")
        
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
        
        elif page == "ℹ️ About":
            st.title("About This System - Faculty View")
            
            # Display faculty info
            faculty_info = get_faculty_details(st.session_state.user_id)
            if faculty_info:
                faculty_id, faculty_name, faculty_branch = faculty_info
                st.info(f"**Faculty Name:** {faculty_name}\n**Branch:** {faculty_branch}")
                
                # Show assigned subjects
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
                    # 6:q1,7:q2,8:q3,9:q4,10:q5,11:overall,12:comments
                    with st.expander(f"{fb[2]} ({fb[4]}) - {fb[1][:10]} (Avg: {fb[11]}/10)"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Faculty:** {fb[2]}")
                            st.write(f"**Department:** {fb[3]}")
                            st.write(f"**Year Level:** {fb[4]}")
                            st.write(f"**Student:** {fb[5]}")
                            st.write(f"**Date:** {fb[1]}")
                        with col2:
                            st.write(f"**Ratings:**")
                            st.write(f"- Teaching Quality: {fb[6]}/10")
                            st.write(f"- Course Content: {fb[7]}/10")
                            st.write(f"- Communication: {fb[8]}/10")
                            st.write(f"- Feedback Quality: {fb[9]}/10")
                            st.write(f"- Subject Knowledge: {fb[10]}/10")
                        st.write(f"**Overall Rating:** {fb[11]}/10")
                        st.write(f"**Comments:** {fb[12] or 'None'}")
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
                df = pd.DataFrame(feedbacks, columns=[
                    'ID', 'Date', 'Faculty', 'Department', 'Year Level', 'Student',
                    'Teaching Quality', 'Course Content', 'Communication',
                    'Feedback Quality', 'Subject Knowledge', 'Overall Rating', 'Comments'
                ])
                
                # Remove ID column for export
                df_export = df[['Date', 'Faculty', 'Department', 'Year Level', 'Student', 'Teaching Quality', 
                               'Course Content', 'Communication', 'Feedback Quality', 
                               'Subject Knowledge', 'Overall Rating', 'Comments']]
                
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
def admin_dashboard(user_id):
    # ... existing admin code
            st.sidebar.title("Admin Portal")
            menu = st.sidebar.selectbox("Menu", ["Dashboard", "Manage Faculty", "Manage Subjects", "Set Feedback Schedule", "View Feedback"])

            if menu == "Set Feedback Schedule":
                st.subheader("Set Feedback Availability")
                enabled, date_str, time_str = get_feedback_settings()
            
                current_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else datetime.date.today()
                current_time = datetime.strptime(time_str, "%H:%M:%S").time() if time_str else datetime.time(8, 0)
            
            with st.form("feedback_schedule_form"):
                enable_feedback = st.checkbox("Enable Feedback for Students", value=enabled)
                feedback_date = st.date_input("Feedback Date", current_date)
                feedback_time = st.time_input("Feedback Time", current_time)
            
            if st.form_submit_button("Save Settings"):
                update_feedback_settings(enable_feedback, feedback_date.isoformat(), feedback_time.isoformat())
                st.success("Feedback settings updated successfully!")

