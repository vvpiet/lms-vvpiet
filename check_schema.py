import sqlite3

conn = sqlite3.connect('feedback.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(feedback);")
cols = cursor.fetchall()

print("Columns in feedback table:")
for col in cols:
    print(f"  {col[1]} ({col[2]})")

conn.close()
