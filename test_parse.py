from datetime import datetime
from zoneinfo import ZoneInfo
import sqlite3

conn=sqlite3.connect('feedback_streamlit.db')
cur=conn.cursor()
cur.execute('SELECT id, start_ts,end_ts FROM feedback_schedule ORDER BY id DESC LIMIT 1')
r=cur.fetchone()
print('row:', r)

import datetime as dt

s = dt.datetime.fromisoformat(r[1])
e = dt.datetime.fromisoformat(r[2])

tz = ZoneInfo('Asia/Kolkata')
if s.tzinfo is None:
    s = s.replace(tzinfo=tz)
else:
    s = s.astimezone(tz)
if e.tzinfo is None:
    e = e.replace(tzinfo=tz)
else:
    e = e.astimezone(tz)

now = datetime.now(ZoneInfo('Asia/Kolkata'))
print('start:', s.isoformat())
print('end  :', e.isoformat())
print('now  :', now.isoformat())
print('is open?', s <= now <= e)

conn.close()
