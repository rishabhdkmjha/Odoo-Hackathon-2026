"""
One-time bootstrap script to create the FIRST Admin account.
Since signup always creates a plain Employee (by design - no self-elevation),
someone has to exist to promote others via PUT /employees/{id}. Run this once
after the database is created.

Usage:
    python seed_admin.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.database import Base, engine, SessionLocal
from app import models  # noqa: F401
from app.models.user import User
from app.models.enums import RoleEnum, UserStatusEnum
from app.auth.security import hash_password

ADMIN_NAME = "System Admin"
ADMIN_EMAIL = "admin@assetflow.com"
ADMIN_PASSWORD = "Admin@123"  # change immediately after first login


def seed_admin():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == ADMIN_EMAIL).first()
        if existing:
            print(f"Admin already exists: {ADMIN_EMAIL}")
            return

        admin = User(
            name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            hashed_password=hash_password(ADMIN_PASSWORD),
            role=RoleEnum.ADMIN,
            status=UserStatusEnum.ACTIVE,
        )
        db.add(admin)
        db.commit()
        print(f"Admin created -> email: {ADMIN_EMAIL}  password: {ADMIN_PASSWORD}")
        print("Log in via POST /auth/login, then change this password ASAP.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()
