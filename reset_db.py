#!/usr/bin/env python
"""Complete database reset - drops all tables and recreates from schema."""

import os
import sys
from app import app, db, User, Faculty, Feedback

if __name__ == '__main__':
    with app.app_context():
        # Get database path
        db_path = 'feedback.db'
        
        print("Dropping all tables...")
        db.drop_all()
        print("✓ All tables dropped")
        
        print("Creating all tables...")
        db.create_all()
        print("✓ All tables created with new schema")
        
        # Add faculty members
        print("Adding faculty members...")
        faculty_list = [
            ('Dr. Rajesh Kumar', 'Computer Science'),
            ('Prof. Anita Singh', 'Mechanical Engineering'),
            ('Dr. Priya Patel', 'Electrical Engineering'),
            ('Prof. Suresh Verma', 'Civil Engineering'),
            ('Dr. Meera Sharma', 'Chemical Engineering'),
            ('Prof. Vikram Gupta', 'Electronics Engineering'),
        ]
        
        for name, dept in faculty_list:
            faculty = Faculty(name=name, department=dept)
            db.session.add(faculty)
        
        db.session.commit()
        print(f"✓ {len(faculty_list)} faculty members added")
        
        # Add admin user
        print("Adding admin user...")
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✓ Admin account created (username: admin, password: admin123)")
        
        # Add student user
        print("Adding student user...")
        student = User(username='student', role='student')
        student.set_password('student123')
        db.session.add(student)
        db.session.commit()
        print("✓ Student account created (username: student, password: student123)")
        
        print("\n✓✓✓ Database reset complete! ✓✓✓")
