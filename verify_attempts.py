#!/usr/bin/env python3
"""
Test script to verify that attempts are being recorded and retrieved correctly
Run this after a student submits a test through the Streamlit app
"""
import sqlite3
import json
from datetime import datetime
from zoneinfo import ZoneInfo

DB_PATH = "feedback_streamlit.db"

def check_attempts():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("=" * 80)
    print("TEST ATTEMPTS VERIFICATION SCRIPT")
    print("=" * 80)
    
    # Check if any attempts exist at all
    cur.execute("SELECT COUNT(*) FROM test_attempts")
    total_count = cur.fetchone()[0]
    print(f"\n✓ Total attempts in DB: {total_count}")
    
    if total_count == 0:
        print("\n⚠️  No attempts found. Here's what to check:")
        print("  1. Did the student actually submit the test form?")
        print("  2. Check the 'attempts.log' file for submission logs:")
        print("     - If it has 'SUBMIT SUCCESS' entries, the insert worked")
        print("     - If it has 'SUBMIT ERROR' entries, the insert failed")
        print("  3. Try the admin seed button: Debug page → Seed Demo Attempt")
        conn.close()
        return False
    
    # List all attempts
    print("\n" + "=" * 80)
    print("ALL ATTEMPTS IN DATABASE:")
    print("=" * 80)
    cur.execute('''
        SELECT ta.id, ta.test_id, ta.student_id, ta.score, ta.submitted_at,
               t.title, u.username
        FROM test_attempts ta
        LEFT JOIN tests t ON ta.test_id = t.id
        LEFT JOIN users u ON ta.student_id = u.id
        ORDER BY ta.submitted_at DESC
    ''')
    attempts = cur.fetchall()
    for att in attempts:
        att_id, test_id, student_id, score, submitted_at, test_title, username = att
        print(f"\n  Attempt {att_id}:")
        print(f"    Test: {test_title} (ID: {test_id})")
        print(f"    Student: {username} (ID: {student_id})")
        print(f"    Score: {score}")
        print(f"    Submitted: {submitted_at}")
    
    # Test the query functions
    print("\n" + "=" * 80)
    print("TESTING QUERY FUNCTIONS:")
    print("=" * 80)
    
    # Test for each student
    cur.execute("SELECT DISTINCT student_id FROM test_attempts")
    student_ids = [row[0] for row in cur.fetchall()]
    
    for sid in student_ids:
        print(f"\n✓ Student ID {sid}:")
        cur.execute('SELECT id, test_id, score FROM test_attempts WHERE student_id = ? ORDER BY id', (sid,))
        student_attempts = cur.fetchall()
        print(f"  Found {len(student_attempts)} attempt(s)")
        for att in student_attempts:
            print(f"    - Attempt {att[0]}: Test {att[1]}, Score {att[2]}")
    
    # Test for each test
    cur.execute("SELECT DISTINCT test_id FROM test_attempts")
    test_ids = [row[0] for row in cur.fetchall()]
    
    for tid in test_ids:
        print(f"\n✓ Test ID {tid}:")
        cur.execute('''
            SELECT ta.id, u.username, ta.score
            FROM test_attempts ta
            LEFT JOIN users u ON ta.student_id = u.id
            WHERE ta.test_id = ?
        ''', (tid,))
        test_attempts = cur.fetchall()
        print(f"  Found {len(test_attempts)} attempt(s)")
        for att in test_attempts:
            print(f"    - Attempt {att[0]}: {att[1]}, Score {att[2]}")
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ VERIFICATION COMPLETE")
    print("=" * 80)
    print("\nNext steps:")
    print("  1. Login to the Streamlit app as:")
    print(f"     - Student user to see attempts on Dashboard")
    print(f"     - Faculty user to see attempts on 'Create Test' page")
    print(f"     - Admin to see attempts on 'Debug: Test Attempts' page")
    print("  2. If attempts still don't show, check the browser console for JS errors")
    print("  3. Force browser refresh (Ctrl+F5) to clear cache")
    print()

if __name__ == "__main__":
    check_attempts()
