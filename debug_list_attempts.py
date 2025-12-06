import sqlite3, json, pprint
conn = sqlite3.connect('feedback_streamlit.db')
cur = conn.cursor()
cur.execute('SELECT id,test_id,student_id,score,submitted_at,answers FROM test_attempts')
rows = cur.fetchall()
print(f"Found {len(rows)} rows in test_attempts:")
pprint.pprint(rows)
print('\nUsers in DB:')
cur.execute("SELECT id, username, role, name, roll_number FROM users")
users = cur.fetchall()
pprint.pprint(users)

print('\nTests in DB:')
cur.execute('SELECT id, title, faculty_id, start_ts, end_ts FROM tests')
tests = cur.fetchall()
pprint.pprint(tests)

conn.close()
