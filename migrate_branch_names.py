#!/usr/bin/env python3
"""
Migration script to update branch names in the database.
Maps old branch names to new branch names.
"""

import sqlite3

DB_PATH = "feedback_streamlit.db"

# Mapping of old branch names to new branch names
BRANCH_MAPPING = {
    'Computer Science': 'Computer science & engineering',
    'Electrical Engineering': 'Electrical engineering',
    'Chemical Engineering': 'Basic sciences & Humanities',  # Maps chemical to basic sciences
    'Electronics Engineering': 'Electronics and Telecommunication Engineering',
}

def migrate_branch_names():
    """Update all references to old branch names with new branch names."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("Starting branch name migration...")
    
    # Update faculty table
    for old_name, new_name in BRANCH_MAPPING.items():
        cursor.execute('UPDATE faculty SET department = ? WHERE department = ?', (new_name, old_name))
        count = cursor.rowcount
        if count > 0:
            print(f"✓ Updated {count} faculty records: {old_name} → {new_name}")
    
    # Update users table
    for old_name, new_name in BRANCH_MAPPING.items():
        cursor.execute('UPDATE users SET branch = ? WHERE branch = ?', (new_name, old_name))
        count = cursor.rowcount
        if count > 0:
            print(f"✓ Updated {count} user records: {old_name} → {new_name}")
    
    conn.commit()
    
    # Show all current branches
    cursor.execute('SELECT DISTINCT department FROM faculty WHERE department IS NOT NULL ORDER BY department')
    branches = [row[0] for row in cursor.fetchall()]
    print("\n✓ Migration complete! Current branches in database:")
    for branch in branches:
        print(f"  - {branch}")
    
    conn.close()

if __name__ == "__main__":
    migrate_branch_names()
