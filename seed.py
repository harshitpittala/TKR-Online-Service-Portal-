"""
Seed script — run once to populate the database with the same
students and teachers that are hard-coded in the frontend's state.js.

Usage:
    python seed.py
"""
from core.database import engine, SessionLocal, Base
from core.security import hash_password
from models.user import User, UserRole

# Import all models so SQLAlchemy creates their tables
import models.user       # noqa
import models.message    # noqa
import models.requests   # noqa

Base.metadata.create_all(bind=engine)

STUDENTS = [
    "24K91A67F3", "24K91A67D8", "24K91A67B8", "24K91A67E7",
    "24K91A67C3", "24K91A67C5", "24K91A67B3", "24K91A67B4",
    "24K91A67B5", "24K91A67F2",
]

# Original password is the same as the identifier for students (per state.js logic)
TEACHERS = {
    "krishnasir@tkrcet.com":    ("hodtkrcet",           "HOD / Principal"),
    "accountant@tkrcet.com":    ("accountanttkrcet",     "Accountant"),
    "exambranch@tkrcet.com":    ("exambranchtkrcet",     "Exam Branch"),
    "placementcell@tkrcet.com": ("placementcelltkrcet",  "Placement Cell"),
    "library@tkrcet.com":       ("librarytkrcet",        "Library"),
    "bus@tkrcet.com":           ("bustkrcet",            "Bus Coordinator"),
    "shakeel@tkrcet.com":       ("shakeeltkrcet",        "Shakeel"),
}


def seed():
    db = SessionLocal()
    try:
        created = 0

        for roll in STUDENTS:
            if not db.query(User).filter_by(identifier=roll).first():
                db.add(User(
                    identifier=roll,
                    hashed_password=hash_password(roll),  # password == roll number
                    role=UserRole.student,
                ))
                created += 1

        for email, (password, display_name) in TEACHERS.items():
            if not db.query(User).filter_by(identifier=email).first():
                db.add(User(
                    identifier=email,
                    hashed_password=hash_password(password),
                    role=UserRole.teacher,
                    display_name=display_name,
                ))
                created += 1

        db.commit()
        print(f"[OK] Seeded {created} users (skipped existing).")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
