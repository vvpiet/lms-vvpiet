#!/usr/bin/env python3
"""
Migration script to update subjects to DBATU University subjects.
"""

import sqlite3

DB_PATH = "feedback_streamlit.db"

def migrate_subjects():
    """Replace all subjects with DBATU University subjects."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("Starting DBATU subjects migration...")
    
    # Clear existing subjects and faculty_subject mappings
    cursor.execute('DELETE FROM faculty_subject')
    cursor.execute('DELETE FROM subjects')
    conn.commit()
    print("✓ Cleared old subjects and faculty mappings")
    
    # Insert new DBATU subjects
    subjects = [
        # FY subjects - DBATU University
        ('Engineering Mathematics I', 'FY'),
        ('Engineering Physics', 'FY'),
        ('Engineering Chemistry', 'FY'),
        ('Computer Fundamentals', 'FY'),
        ('Basic Civil Engineering', 'FY'),
        ('Engineering Drawing', 'FY'),
        ('Workshop Practice', 'FY'),
        
        # SY subjects - DBATU University
        ('Discrete Mathematics', 'SY'),
        ('Digital Electronics', 'SY'),
        ('Data Structures & Algorithms', 'SY'),
        ('Object Oriented Programming', 'SY'),
        ('Database Management Systems', 'SY'),
        ('Web Technologies', 'SY'),
        ('Microprocessors and Microcontrollers', 'SY'),
        
        # TY subjects - DBATU University
        ('Software Engineering', 'TY'),
        ('Operating Systems', 'TY'),
        ('Computer Networks', 'TY'),
        ('Artificial Intelligence', 'TY'),
        ('Machine Learning', 'TY'),
        ('Cloud Computing', 'TY'),
        ('Cryptography and Network Security', 'TY'),
        
        # Final Year subjects - DBATU University
        ('Project Work', 'Final Year'),
        ('Internship', 'Final Year'),
        ('Advanced Web Development', 'Final Year'),
        ('Data Science and Analytics', 'Final Year'),
        ('IoT and Embedded Systems', 'Final Year'),
        ('Advanced Database Management', 'Final Year')
    ]
    
    cursor.executemany('INSERT INTO subjects (name, year_level) VALUES (?, ?)', subjects)
    conn.commit()
    print(f"✓ Inserted {len(subjects)} DBATU University subjects")
    
    # Show all current subjects
    cursor.execute('SELECT year_level, COUNT(*) FROM subjects GROUP BY year_level ORDER BY year_level')
    for year_level, count in cursor.fetchall():
        print(f"  {year_level}: {count} subjects")
    
    print("\n✓ DBATU subjects migration complete!")
    conn.close()

if __name__ == "__main__":
    migrate_subjects()
