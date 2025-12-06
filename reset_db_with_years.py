#!/usr/bin/env python3
"""
Database reset script to update schema with year_level support.
This script will:
1. Drop existing tables
2. Recreate tables with new schema (includes year_level)
3. Seed faculty with year levels
4. Create demo users
"""

import sqlite3
import hashlib
import os

DB_PATH = "feedback_streamlit.db"

def hash_password(password):
    """Hash password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def main():
    # Backup existing database
    if os.path.exists(DB_PATH):
        backup_path = f"{DB_PATH}.backup"
        try:
            os.rename(DB_PATH, backup_path)
            print(f"✓ Existing database backed up to {backup_path}")
        except Exception as e:
            print(f"⚠ Could not backup database: {e}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Drop existing tables if they exist
        print("Dropping existing tables...")
        cursor.execute("DROP TABLE IF EXISTS attendance")
        cursor.execute("DROP TABLE IF EXISTS feedback")
        cursor.execute("DROP TABLE IF EXISTS faculty_subject")
        cursor.execute("DROP TABLE IF EXISTS subjects")
        cursor.execute("DROP TABLE IF EXISTS faculty")
        cursor.execute("DROP TABLE IF EXISTS users")
        print("✓ All tables dropped")
        
        # Create Users table
        print("Creating tables with new schema...")
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
        
        # Create Faculty table with year_level column
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS faculty (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                department TEXT,
                year_level TEXT DEFAULT 'FY'
            )
        ''')
        
        # Create Feedback table with year_level column
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
        
        # Create Subjects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                year_level TEXT NOT NULL
            )
        ''')
        
        # Create faculty_subject mapping table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS faculty_subject (
                faculty_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                PRIMARY KEY (faculty_id, subject_id),
                FOREIGN KEY(faculty_id) REFERENCES faculty(id),
                FOREIGN KEY(subject_id) REFERENCES subjects(id)
            )
        ''')
        
        # Create Attendance tracking table
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
        print("✓ All tables created with new schema")
        
        # Seed faculty with year levels
        print("Seeding faculty members...")
        faculty_list = [
            ('Dr. Rajesh Kumar', 'Computer Science', 'FY'),
            ('Prof. Anita Singh', 'Mechanical Engineering', 'SY'),
            ('Dr. Priya Patel', 'Electrical Engineering', 'TY'),
            ('Prof. Suresh Verma', 'Civil Engineering', 'Final Year'),
            ('Dr. Meera Sharma', 'Chemical Engineering', 'FY'),
            ('Prof. Vikram Gupta', 'Electronics Engineering', 'SY'),
            ('Dr. Rajesh Desai', 'Computer Science', 'TY'),
            ('Prof. Neha Verma', 'Mechanical Engineering', 'Final Year'),
        ]
        cursor.executemany(
            'INSERT INTO faculty (name, department, year_level) VALUES (?, ?, ?)',
            faculty_list
        )
        conn.commit()
        print(f"✓ {len(faculty_list)} faculty members added")
        
        # Seed Subjects
        print("Seeding subjects...")
        subjects = [
            ('Engineering Mathematics I', 'FY'),
            ('Basic Physics', 'FY'),
            ('Engineering Mechanics', 'FY'),
            ('Data Structures', 'SY'),
            ('Thermodynamics', 'SY'),
            ('Circuit Theory', 'SY'),
            ('Operating Systems', 'TY'),
            ('Fluid Mechanics', 'TY'),
            ('Power Electronics', 'TY'),
            ('Project Work', 'Final Year'),
            ('Advanced Topics in CS', 'Final Year')
        ]
        cursor.executemany('INSERT INTO subjects (name, year_level) VALUES (?, ?)', subjects)
        conn.commit()
        print(f"✓ {len(subjects)} subjects added")
        
        # Seed faculty_subject mappings
        print("Creating faculty-subject mappings...")
        mapping = [
            ('Dr. Rajesh Kumar', 'Engineering Mathematics I'),
            ('Dr. Rajesh Kumar', 'Data Structures'),
            ('Prof. Anita Singh', 'Thermodynamics'),
            ('Dr. Priya Patel', 'Circuit Theory'),
            ('Dr. Priya Patel', 'Power Electronics'),
            ('Prof. Suresh Verma', 'Fluid Mechanics'),
            ('Dr. Meera Sharma', 'Basic Physics'),
            ('Prof. Vikram Gupta', 'Circuit Theory'),
            ('Prof. Vikram Gupta', 'Power Electronics'),
            ('Prof. Suresh Verma', 'Project Work'),
            ('Prof. Anita Singh', 'Project Work'),
        ]
        for fname, subj in mapping:
            cursor.execute('SELECT id FROM faculty WHERE name = ?', (fname,))
            frow = cursor.fetchone()
            cursor.execute('SELECT id FROM subjects WHERE name = ?', (subj,))
            srow = cursor.fetchone()
            if frow and srow:
                try:
                    cursor.execute('INSERT INTO faculty_subject (faculty_id, subject_id) VALUES (?, ?)', (frow[0], srow[0]))
                except Exception:
                    pass
        conn.commit()
        print("✓ Faculty-subject mappings created")
        
        # Create demo users
        print("Creating demo users...")
        cursor.execute(
            'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
            ('admin', hash_password('admin123'), 'admin')
        )
        cursor.execute(
            'INSERT INTO users (username, password, role, faculty_id, name, branch) VALUES (?, ?, ?, ?, ?, ?)',
            ('rajesh_kumar', hash_password('faculty123'), 'faculty', 1, 'Dr. Rajesh Kumar', 'Computer Science')
        )
        cursor.execute(
            'INSERT INTO users (username, password, role, faculty_id, name, branch) VALUES (?, ?, ?, ?, ?, ?)',
            ('anita_singh', hash_password('faculty123'), 'faculty', 2, 'Prof. Anita Singh', 'Mechanical Engineering')
        )
        
        # Create demo students with branch and class
        demo_students = [
            ('student1', hash_password('student123'), 'student', None, 'Alice Johnson', 'Computer Science', 'FY'),
            ('student2', hash_password('student123'), 'student', None, 'Bob Smith', 'Computer Science', 'FY'),
            ('student3', hash_password('student123'), 'student', None, 'Carol White', 'Mechanical Engineering', 'SY'),
            ('student4', hash_password('student123'), 'student', None, 'David Lee', 'Electrical Engineering', 'TY'),
        ]
        for student in demo_students:
            cursor.execute(
                'INSERT INTO users (username, password, role, faculty_id, name, branch, class) VALUES (?, ?, ?, ?, ?, ?, ?)',
                student
            )
        
        conn.commit()
        print("✓ Admin account created (username: admin, password: admin123)")
        print("✓ Faculty accounts created:")
        print("  - rajesh_kumar (password: faculty123)")
        print("  - anita_singh (password: faculty123)")
        print(f"✓ {len(demo_students)} demo students created with branch and class info")
        
        print("\n" + "="*50)
        print("✓✓✓ Database reset complete! ✓✓✓")
        print("="*50)
        print("\nYear levels added to faculty:")
        print("- FY (First Year)")
        print("- SY (Second Year)")
        print("- TY (Third Year)")
        print("- Final Year")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
