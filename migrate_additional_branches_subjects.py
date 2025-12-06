#!/usr/bin/env python3
"""
Migration script to add DBATU subjects for additional branches:
- Electronics and Telecommunication Engineering
- Mechanical Engineering
- Civil Engineering
- Artificial Intelligence & Data Science Engineering
"""
import sqlite3
DB_PATH = "feedback_streamlit.db"

BRANCH_SUBJECTS = [
    # Electronics and Telecommunication Engineering
    ('Electronics and Telecommunication Engineering', [
        ('Analog Electronics', 'SY'),
        ('Digital Signal Processing', 'TY'),
        ('Communication Systems', 'TY'),
        ('VLSI Design', 'TY'),
        ('Embedded Systems', 'TY'),
        ('Antenna and Wave Propagation', 'Final Year'),
        ('Wireless Communications', 'Final Year'),
    ]),
    # Mechanical Engineering
    ('Mechanical Engineering', [
        ('Thermodynamics', 'SY'),
        ('Fluid Mechanics', 'SY'),
        ('Kinematics of Machines', 'TY'),
        ('Heat Transfer', 'TY'),
        ('Design of Machine Elements', 'TY'),
        ('CAD/CAM', 'Final Year'),
        ('Dynamics of Machines', 'Final Year'),
    ]),
    # Civil Engineering
    ('Civil Engineering', [
        ('Surveying', 'SY'),
        ('Strength of Materials', 'SY'),
        ('Structural Analysis', 'TY'),
        ('Concrete Technology', 'TY'),
        ('Geotechnical Engineering', 'TY'),
        ('Transportation Engineering', 'Final Year'),
        ('Hydraulics and Water Resources', 'Final Year'),
    ]),
    # Artificial Intelligence & Data Science Engineering
    ('Artificial Intelligence & Data science engineering', [
        ('Introduction to AI', 'SY'),
        ('Probability and Statistics for AI', 'SY'),
        ('Machine Learning', 'TY'),
        ('Deep Learning', 'TY'),
        ('Natural Language Processing', 'TY'),
        ('Data Mining', 'Final Year'),
        ('Big Data Analytics', 'Final Year'),
    ])
]


def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("Starting additional subjects migration...")
    inserted = 0
    for branch, subjects in BRANCH_SUBJECTS:
        for name, year in subjects:
            # Insert if not exists
            cursor.execute('SELECT id FROM subjects WHERE name = ? AND year_level = ?', (name, year))
            if not cursor.fetchone():
                cursor.execute('INSERT INTO subjects (name, year_level) VALUES (?, ?)', (name, year))
                inserted += 1
    conn.commit()
    print(f"✓ Inserted {inserted} subjects for additional branches")
    cursor.execute('SELECT year_level, COUNT(*) FROM subjects GROUP BY year_level ORDER BY year_level')
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")
    conn.close()

if __name__ == '__main__':
    migrate()
