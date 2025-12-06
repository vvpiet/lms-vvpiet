#!/usr/bin/env python3
import sqlite3
import json

DB_PATH = "feedback_streamlit.db"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Check test_attempts table schema
print("=== test_attempts table schema ===")
cur.execute("PRAGMA table_info(test_attempts)")
schema = cur.fetchall()
for col in schema:
    print(f"  {col[1]}: {col[2]}")

# Check current contents
print("\n=== All rows in test_attempts ===")
cur.execute("SELECT * FROM test_attempts")
attempts = cur.fetchall()
if attempts:
    print(f"Found {len(attempts)} rows:")
    for row in attempts:
        print(f"  {row}")
else:
    print("  (empty)")

# Check test_questions to ensure there are questions (needed for scoring)
print("\n=== Sample test_questions (first 5) ===")
cur.execute("SELECT id, test_id, question_text, correct_choice, marks FROM test_questions LIMIT 5")
questions = cur.fetchall()
if questions:
    for q in questions:
        print(f"  {q}")
else:
    print("  (empty)")

# Check tests
print("\n=== All tests ===")
cur.execute("SELECT id, title, faculty_id, start_ts, end_ts FROM tests")
tests = cur.fetchall()
if tests:
    for t in tests:
        print(f"  {t}")
else:
    print("  (empty)")

# Check students
print("\n=== All student users ===")
cur.execute("SELECT id, username, name FROM users WHERE role = 'student'")
students = cur.fetchall()
if students:
    for s in students:
        print(f"  {s}")
else:
    print("  (empty)")

conn.close()
