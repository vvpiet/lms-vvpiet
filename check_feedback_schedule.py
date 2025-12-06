import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

DB_PATH = "feedback_streamlit.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=== Feedback Schedule in Database ===")
cursor.execute("SELECT id, start_ts, end_ts FROM feedback_schedule ORDER BY id DESC")
schedules = cursor.fetchall()

if schedules:
    for id, start, end in schedules:
        print(f"\nID: {id}")
        print(f"  Start: {start}")
        print(f"  End:   {end}")
else:
    print("  (No schedules found)")

print(f"\nCurrent Time (Asia/Kolkata): {datetime.now(ZoneInfo('Asia/Kolkata')).isoformat()}")

conn.close()
