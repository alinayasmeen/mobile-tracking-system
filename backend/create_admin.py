#!/usr/bin/env python3
"""
Script to create an admin user for the Mobile Tracking System.
Run this script after setting up the database.
"""

from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, UserRole
from auth import get_password_hash

def create_admin():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        admin = db.query(User).filter(User.email == "admin@system.com").first()
        
        if admin:
            print("❌ Admin user already exists!")
            print(f"Email: admin@system.com")
            return
        
        # Create admin user
        admin = User(
            email="admin@system.com",
            password_hash=get_password_hash("Admin@123456"),
            role=UserRole.ADMIN,
            cnic="1234567890123",  # Dummy CNIC for admin
            ntn=None,
            shop_address=None
        )
        
        db.add(admin)
        db.commit()
        
        print("✅ Admin user created successfully!")
        print("\n" + "="*50)
        print("Admin Credentials:")
        print("="*50)
        print("Email: admin@system.com")
        print("Password: Admin@123456")
        print("="*50)
        print("\n⚠️  IMPORTANT: Change these credentials in production!")
        
    except Exception as e:
        print(f"❌ Error creating admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
