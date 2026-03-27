from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
import enum


class UserRole(str, enum.Enum):
    student = "student"
    teacher = "teacher"


class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, index=True)
    # For students: their roll number (e.g. 24K91A67F3)
    # For teachers: their email (e.g. krishnasir@tkrcet.com)
    identifier      = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role            = Column(Enum(UserRole), nullable=False)
    # Teacher-only display name (optional)
    display_name    = Column(String, nullable=True)
    created_at      = Column(DateTime, default=datetime.utcnow)

    # Relationships
    sent_messages       = relationship("Message",          foreign_keys="Message.sender_id",   back_populates="sender")
    received_messages   = relationship("Message",          foreign_keys="Message.receiver_id", back_populates="receiver")
    bonafide_requests   = relationship("BonafideRequest",  foreign_keys="BonafideRequest.student_id", back_populates="student")
    tc_requests         = relationship("TcRequest",        foreign_keys="TcRequest.student_id",        back_populates="student")
    id_card_requests    = relationship("IdCardRequest",    foreign_keys="IdCardRequest.student_id",    back_populates="student")
    leave_requests      = relationship("LeaveRequest",     foreign_keys="LeaveRequest.student_id",     back_populates="student")
    bus_pass_requests   = relationship("BusPassRequest",   foreign_keys="BusPassRequest.student_id",   back_populates="student")
