import sqlite3

conn = sqlite3.connect('feedback_streamlit.db')
cursor = conn.cursor()
cursor.execute("SELECT id, username, name, class FROM users WHERE role='student' LIMIT 10")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
