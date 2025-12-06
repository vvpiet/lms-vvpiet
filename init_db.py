#!/usr/bin/env python
"""Initialize the database with faculty list and demo accounts."""

from app import app, db, User, Faculty

if __name__ == '__main__':
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Add faculty members if they don't exist
        faculty_list = [
            ('Dr. Rajesh Kumar', 'Computer Science'),
            ('Prof. Anita Singh', 'Mechanical Engineering'),
            ('Dr. Priya Patel', 'Electrical Engineering'),
            ('Prof. Suresh Verma', 'Civil Engineering'),
            ('Dr. Meera Sharma', 'Chemical Engineering'),
            ('Prof. Vikram Gupta', 'Electronics Engineering'),
        ]
        
        for name, dept in faculty_list:
            if not Faculty.query.filter_by(name=name).first():
                faculty = Faculty(name=name, department=dept)
                db.session.add(faculty)
        
        db.session.commit()
        print("✓ Faculty members added")
        
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin account created (username: admin, password: admin123)")
        else:
            print("✓ Admin account already exists")
        
        # Create a demo student account
        student = User.query.filter_by(username='student').first()
        if not student:
            student = User(username='student', role='student')
            student.set_password('student123')
            db.session.add(student)
            db.session.commit()
            print("✓ Student account created (username: student, password: student123)")
        else:
            print("✓ Student account already exists")
        
        print("\nDatabase initialized successfully!")
