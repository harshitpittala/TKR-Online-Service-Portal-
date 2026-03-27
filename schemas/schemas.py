from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from models.user import UserRole


# ── Auth ─────────────────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    identifier: str   # roll number for student, email for teacher
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    identifier: str

class UserOut(BaseModel):
    id: int
    identifier: str
    role: UserRole
    display_name: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True


# ── Messages ─────────────────────────────────────────────────────────────────
class MessageCreate(BaseModel):
    recipient_identifier: str   # email or roll number of the other party
    content: str

class MessageOut(BaseModel):
    id: int
    sender_identifier: str
    receiver_identifier: str
    content: str
    is_read: bool
    created_at: datetime
    class Config:
        from_attributes = True


# ── Bonafide ─────────────────────────────────────────────────────────────────
class BonafideCreate(BaseModel):
    name: str
    fathers_name: str
    branch: str
    dob: str
    academic_year: str
    purpose: str
    date_of_issue: str

class BonafideOut(BaseModel):
    id: int
    roll_number: str
    name: str
    fathers_name: str
    branch: str
    dob: str
    academic_year: str
    purpose: str
    date_of_issue: str
    is_read: bool
    created_at: datetime
    class Config:
        from_attributes = True


# ── TC ────────────────────────────────────────────────────────────────────────
class TcCreate(BaseModel):
    full_name: str
    parent_name: str
    dob: str
    gender: str
    nationality: str
    course: str
    admission_year: str
    leaving_year: str
    class_year: str
    branch: str
    subjects: Optional[str] = None

class TcOut(BaseModel):
    id: int
    roll_number: str
    full_name: str
    parent_name: str
    dob: str
    gender: str
    nationality: str
    course: str
    admission_year: str
    leaving_year: str
    class_year: str
    branch: str
    subjects: Optional[str]
    is_read: bool
    created_at: datetime
    class Config:
        from_attributes = True


# ── ID Card ───────────────────────────────────────────────────────────────────
class IdCardCreate(BaseModel):
    reason: str

class IdCardOut(BaseModel):
    id: int
    roll_number: str
    reason: str
    is_read: bool
    created_at: datetime
    class Config:
        from_attributes = True


# ── Leave ─────────────────────────────────────────────────────────────────────
class LeaveCreate(BaseModel):
    full_name: str
    class_info: str
    reason: str
    start_date: str
    end_date: str
    total_days: int

class LeaveOut(BaseModel):
    id: int
    roll_number: str
    full_name: str
    class_info: str
    reason: str
    start_date: str
    end_date: str
    total_days: int
    is_read: bool
    created_at: datetime
    class Config:
        from_attributes = True


# ── Bus Pass ──────────────────────────────────────────────────────────────────
class BusPassCreate(BaseModel):
    name: str
    class_info: str

class BusPassOut(BaseModel):
    id: int
    roll_number: str
    name: str
    class_info: str
    is_read: bool
    created_at: datetime
    class Config:
        from_attributes = True
