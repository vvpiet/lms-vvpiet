#!/usr/bin/env python
"""Migrate database schema by adding missing faculty_id column."""

from app import app, db, Feedback, Faculty
import sqlalchemy as sa

if __name__ == '__main__':
    with app.app_context():
        # Check if faculty_id column exists
        inspector = sa.inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('feedback')]
        
        if 'faculty_id' not in columns:
            print("Adding faculty_id column to feedback table...")
            
            with db.engine.connect() as conn:
                # SQLite doesn't support ALTER TABLE ADD COLUMN NOT NULL without default
                # So we add it as nullable first
                conn.execute(sa.text('ALTER TABLE feedback ADD COLUMN faculty_id INTEGER'))
                conn.commit()
            
            print("✓ faculty_id column added")
        else:
            print("✓ faculty_id column already exists")
        
        # Ensure users and faculty tables exist
        db.create_all()
        print("✓ Database schema synchronized")
