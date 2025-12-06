#!/usr/bin/env python3
import sqlite3

DB_PATH = "feedback_streamlit.db"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print("=== Faculty users ===")
cur.execute("SELECT u.id, u.username, u.faculty_id, f.id, f.name FROM users u LEFT JOIN faculty f ON u.faculty_id = f.id WHERE u.role='faculty'")
for row in cur.fetchall():
    print(row)

print("\n=== Tests and their creators ===")
cur.execute("SELECT t.id, t.title, t.faculty_id, f.name FROM tests t LEFT JOIN faculty f ON t.faculty_id = f.id")
for row in cur.fetchall():
    print(row)

conn.close()
