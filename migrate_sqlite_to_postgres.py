"""
migrate_sqlite_to_postgres.py

Usage:
  python migrate_sqlite_to_postgres.py --sqlite feedback_streamlit.db --pg "postgres://user:pass@host:5432/dbname" [--drop]

This script reads non-system tables from the SQLite database, creates equivalent tables in Postgres,
and copies rows. It attempts a conservative type mapping and is intended for a one-time migration.

Notes:
- Ensure `psycopg2-binary` is installed in the environment where you run this script.
- Backup your Postgres database before running with --drop.
"""
import argparse
import sqlite3
import os
import re
import sys
from urllib.parse import urlparse

try:
    import psycopg2
    from psycopg2 import sql
    from psycopg2.extras import execute_values
except Exception as e:
    print("Error: psycopg2 is required to run this migration. Install with: pip install psycopg2-binary")
    raise


def map_sqlite_type_to_postgres(sqlite_type):
    if not sqlite_type:
        return 'TEXT'
    t = sqlite_type.upper()
    if 'INT' in t:
        return 'INTEGER'
    if 'CHAR' in t or 'CLOB' in t or 'TEXT' in t:
        return 'TEXT'
    if 'BLOB' in t:
        return 'BYTEA'
    if 'REAL' in t or 'FLOA' in t or 'DOUB' in t:
        return 'REAL'
    return 'TEXT'


def get_sqlite_tables(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
    return [r[0] for r in cur.fetchall()]


def get_table_schema_sqlite(conn, table):
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info('{table}')")
    # columns: cid, name, type, notnull, dflt_value, pk
    cols = cur.fetchall()
    return cols


def create_table_postgres(pgconn, table, cols, drop_if_exists=False):
    cur = pgconn.cursor()
    if drop_if_exists:
        cur.execute(sql.SQL('DROP TABLE IF EXISTS {} CASCADE').format(sql.Identifier(table)))
    col_defs = []
    pk_cols = []
    for cid, name, ctype, notnull, dflt, pk in cols:
        pgtype = map_sqlite_type_to_postgres(ctype)
        # Basic default handling: avoid sqlite implicit defaults
        def_clause = ''
        if dflt is not None:
            # keep literal defaults as-is where possible
            def_clause = ' DEFAULT ' + dflt
        notnull_clause = ' NOT NULL' if notnull else ''
        col_defs.append(sql.SQL('{} {}{}{}').format(sql.Identifier(name), sql.SQL(pgtype), sql.SQL(def_clause), sql.SQL(notnull_clause)))
        if pk:
            pk_cols.append(name)
    if pk_cols:
        pk_sql = sql.SQL(', ').join([sql.Identifier(c) for c in pk_cols])
        create = sql.SQL('CREATE TABLE IF NOT EXISTS {} ({}, PRIMARY KEY({}))').format(sql.Identifier(table), sql.SQL(', ').join(col_defs), pk_sql)
    else:
        create = sql.SQL('CREATE TABLE IF NOT EXISTS {} ({})').format(sql.Identifier(table), sql.SQL(', ').join(col_defs))
    cur.execute(create)
    pgconn.commit()


def copy_table(conn_sqlite, pgconn, table):
    s_cur = conn_sqlite.cursor()
    s_cur.execute(f"SELECT * FROM {table}")
    rows = s_cur.fetchall()
    if not rows:
        print(f"Skipping table '{table}' (no rows)")
        return
    s_cur.execute(f"PRAGMA table_info('{table}')")
    cols_info = s_cur.fetchall()
    col_names = [c[1] for c in cols_info]
    placeholders = ','.join(['%s'] * len(col_names))
    insert_sql = sql.SQL('INSERT INTO {} ({}) VALUES %s').format(
        sql.Identifier(table),
        sql.SQL(',').join([sql.Identifier(c) for c in col_names])
    )
    pg_cur = pgconn.cursor()
    try:
        execute_values(pg_cur, insert_sql.as_string(pgconn), rows, template=None, page_size=100)
        pgconn.commit()
        print(f"Copied {len(rows)} rows into '{table}'")
    except Exception as e:
        pgconn.rollback()
        print(f"Error copying table '{table}': {e}")
        raise


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--sqlite', default='feedback_streamlit.db', help='Path to SQLite DB file')
    p.add_argument('--pg', default=os.environ.get('DATABASE_URL'), help='Postgres DATABASE_URL')
    p.add_argument('--drop', action='store_true', help='Drop tables in Postgres before creating (destructive)')
    p.add_argument('--tables', nargs='*', help='Optional list of tables to migrate (default: all)')
    args = p.parse_args()

    if not args.pg:
        print('Error: Postgres DATABASE_URL must be provided via --pg or the DATABASE_URL env var')
        sys.exit(2)

    if not os.path.exists(args.sqlite):
        print(f"Error: sqlite file not found: {args.sqlite}")
        sys.exit(2)

    print(f"Opening sqlite DB: {args.sqlite}")
    s_conn = sqlite3.connect(args.sqlite)
    try:
        tables = get_sqlite_tables(s_conn)
        if args.tables:
            tables = [t for t in tables if t in args.tables]
        if not tables:
            print('No tables found to migrate')
            return
        print('Tables to migrate:', ', '.join(tables))
        print('Connecting to Postgres...')
        pgconn = psycopg2.connect(args.pg)
        for t in tables:
            print('\n=== Table:', t)
            cols = get_table_schema_sqlite(s_conn, t)
            print(' - Columns:', ', '.join([c[1] for c in cols]))
            print(' - Creating table in Postgres (if not exists)')
            create_table_postgres(pgconn, t, cols, drop_if_exists=args.drop)
            print(' - Copying rows...')
            copy_table(s_conn, pgconn, t)
        # After copying all tables, ensure Postgres sequences (serial) are synced to the
        # maximum existing id values to avoid duplicate-key errors on future inserts.
        print('\nSyncing Postgres sequences...')
        pg_cur = pgconn.cursor()
        for t in tables:
            try:
                pg_cur.execute("SELECT pg_get_serial_sequence(%s, %s)", (t, 'id'))
                seq = pg_cur.fetchone()[0]
                if seq:
                    pg_cur.execute(f"SELECT setval('{seq}', COALESCE((SELECT MAX(id) FROM {t}), 1), true)")
                    print(f" - Synced sequence for table '{t}' -> {seq}")
                else:
                    # No serial sequence found for this table; skip
                    pass
            except Exception as e:
                print(f" - Could not sync sequence for table '{t}': {e}")
        pgconn.commit()
        print('\nMigration complete.')
    finally:
        s_conn.close()


if __name__ == '__main__':
    main()
