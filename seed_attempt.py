import sqlite3, json
conn = sqlite3.connect('feedback_streamlit.db')
cur = conn.cursor()
answers = {"1": 0, "2": 1}
cur.execute('INSERT INTO test_attempts (test_id, student_id, answers, score, started_at, submitted_at) VALUES (?, ?, ?, ?, ?, ?)', (3, 4, json.dumps(answers), 2.0, '2025-12-02T11:20:00+05:30', '2025-12-02T11:25:00+05:30'))
conn.commit()
print('Inserted attempt id', cur.lastrowid)
conn.close()
