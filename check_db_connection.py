"""
check_db_connection.py

Quick helper to verify which DB the app will use and to print counts for key tables.
Usage:
  # If you have DATABASE_URL in env (PowerShell):
  $env:DATABASE_URL = "postgres://user:pass@host:5432/dbname"
  python check_db_connection.py

  # Or provide sqlite path explicitly:
  python check_db_connection.py --sqlite feedback_streamlit.db

This script will NOT modify data; it only reads simple counts.
"""
import argparse
import os
import sqlite3

try:
    from urllib.parse import urlparse
except Exception:
    from urlparse import urlparse


def check_sqlite(path):
    if not os.path.exists(path):
        print(f"SQLite DB not found: {path}")
        return
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    print(f"Using SQLite file: {path}")
    for t in ['users','feedback','tests','test_attempts','subjects','faculty']:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {t}")
            c = cur.fetchone()[0]
        except Exception:
            c = 'n/a'
        print(f"  {t}: {c}")
    conn.close()


def check_postgres(dsn):
    try:
        import psycopg2
    except Exception:
        print('psycopg2 not installed in this environment. pip install psycopg2-binary')
        return
    try:
        conn = psycopg2.connect(dsn)
        cur = conn.cursor()
        print(f"Connected to Postgres: {dsn.split('@')[-1]}")
        for t in ['users','feedback','tests','test_attempts','subjects','faculty']:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {t}")
                c = cur.fetchone()[0]
            except Exception:
                c = 'n/a'
            print(f"  {t}: {c}")
        conn.close()
        if args.inspect_sequences:
            try:
                import psycopg2
                conn = psycopg2.connect(args.pg)
                cur = conn.cursor()
                print('\nInspect sequences for tables (pg_get_serial_sequence, seq last_value, max(id)):')
                for t in ['users','faculty','faculty_year_level','faculty_resources','daily_ler','tests','test_questions','test_attempts','notices','faculty_leaves','subjects','feedback_schedule']:
                    try:
                        cur.execute("SELECT pg_get_serial_sequence(%s, %s)", (t, 'id'))
                        seq = cur.fetchone()[0]
                        if seq:
                            try:
                                cur.execute(f"SELECT last_value, is_called FROM {seq}")
                                lv = cur.fetchone()
                            except Exception:
                                lv = None
                            try:
                                cur.execute(f"SELECT COALESCE(MAX(id), 0) FROM {t}")
                                mx = cur.fetchone()[0]
                            except Exception:
                                mx = 'n/a'
                            print(f" - {t}: seq={seq}, seq_last={lv}, max_id={mx}")
                        else:
                            # no sequence associated (maybe table created manually)
                            try:
                                cur.execute(f"SELECT COALESCE(MAX(id), 0) FROM {t}")
                                mx = cur.fetchone()[0]
                            except Exception:
                                mx = 'n/a'
                            print(f" - {t}: NO seq associated, max_id={mx}")
                    except Exception as ex:
                        print(f" - {t}: inspect error: {ex}")
                conn.close()
            except Exception as e:
                print('Failed to inspect sequences:', e)
    except Exception as e:
        print('Failed to connect to Postgres:', e)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--sqlite', default=os.environ.get('SQLITE_PATH','feedback_streamlit.db'))
    p.add_argument('--pg', default=os.environ.get('DATABASE_URL'))
    p.add_argument('--sync-sequences', action='store_true', help='If set and using Postgres, sync serial sequences to max(id) for common tables')
    p.add_argument('--inspect-sequences', action='store_true', help='Inspect whether tables have serial sequences and show their last_value and max(id)')
    args = p.parse_args()

    if args.pg:
        print('DATABASE_URL is set — checking Postgres...')
        check_postgres(args.pg)
        if args.sync_sequences:
            try:
                import psycopg2
                conn = psycopg2.connect(args.pg)
                cur = conn.cursor()
                print('\nSyncing sequences:')
                for t in ['users','feedback','tests','test_attempts','subjects','faculty','feedback_schedule']:
                    try:
                        cur.execute("SELECT pg_get_serial_sequence(%s, %s)", (t, 'id'))
                        seq = cur.fetchone()[0]
                        if seq:
                            cur.execute(f"SELECT setval('{seq}', COALESCE((SELECT MAX(id) FROM {t}), 1), true)")
                            print(f" - Synced sequence for {t}")
                    except Exception as e:
                        print(f" - Could not sync {t}: {e}")
                conn.commit()
                conn.close()
            except Exception as e:
                print('Failed to sync sequences:', e)
    else:
        print('DATABASE_URL not set — falling back to SQLite')
        check_sqlite(args.sqlite)

if __name__ == '__main__':
    main()
