#!/usr/bin/env python3
import sqlite3

DB_PATH = "feedback_streamlit.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Test the get_test_attempts_for_test function (test_id = 3)
print("=== Testing get_test_attempts_for_test(test_id=3) ===")
cursor.execute('''SELECT ta.id, ta.test_id, ta.student_id, ta.answers, ta.score, ta.started_at, ta.submitted_at, u.username, u.name
                  FROM test_attempts ta
                  LEFT JOIN users u ON ta.student_id = u.id
                  WHERE ta.test_id = ?
                  ORDER BY ta.submitted_at DESC''', (3,))
rows = cursor.fetchall()
print(f"Found {len(rows)} rows for test_id=3:")
for row in rows:
    print(f"  {row}")

# Test the get_test_attempts_for_student function (student_id = 4)
print("\n=== Testing get_test_attempts_for_student(student_id=4) ===")
cursor.execute('SELECT id, test_id, score, started_at, submitted_at FROM test_attempts WHERE student_id = ? ORDER BY submitted_at DESC', (4,))
rows2 = cursor.fetchall()
print(f"Found {len(rows2)} rows for student_id=4:")
for row in rows2:
    print(f"  {row}")

conn.close()
