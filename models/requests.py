from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class BonafideRequest(Base):
    __tablename__ = "bonafide_requests"

    id           = Column(Integer, primary_key=True, index=True)
    student_id   = Column(Integer, ForeignKey("users.id"), nullable=False)
    name         = Column(String, nullable=False)
    roll_number  = Column(String, nullable=False)
    fathers_name = Column(String, nullable=False)
    branch       = Column(String, nullable=False)
    dob          = Column(String, nullable=False)
    academic_year= Column(String, nullable=False)
    purpose      = Column(Text,   nullable=False)
    date_of_issue= Column(String, nullable=False)
    is_read      = Column(Boolean, default=False)
    created_at   = Column(DateTime, default=datetime.utcnow)

    student = relationship("User", foreign_keys=[student_id], back_populates="bonafide_requests")


class TcRequest(Base):
    __tablename__ = "tc_requests"

    id             = Column(Integer, primary_key=True, index=True)
    student_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name      = Column(String, nullable=False)
    parent_name    = Column(String, nullable=False)
    dob            = Column(String, nullable=False)
    gender         = Column(String, nullable=False)
    nationality    = Column(String, nullable=False)
    roll_number    = Column(String, nullable=False)
    course         = Column(String, nullable=False)
    admission_year = Column(String, nullable=False)
    leaving_year   = Column(String, nullable=False)
    class_year     = Column(String, nullable=False)
    branch         = Column(String, nullable=False)
    subjects       = Column(String, nullable=True)
    is_read        = Column(Boolean, default=False)
    created_at     = Column(DateTime, default=datetime.utcnow)

    student = relationship("User", foreign_keys=[student_id], back_populates="tc_requests")


class IdCardRequest(Base):
    __tablename__ = "id_card_requests"

    id          = Column(Integer, primary_key=True, index=True)
    student_id  = Column(Integer, ForeignKey("users.id"), nullable=False)
    roll_number = Column(String, nullable=False)
    reason      = Column(Text, nullable=False)
    is_read     = Column(Boolean, default=False)
    created_at  = Column(DateTime, default=datetime.utcnow)

    student = relationship("User", foreign_keys=[student_id], back_populates="id_card_requests")


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id          = Column(Integer, primary_key=True, index=True)
    student_id  = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name   = Column(String, nullable=False)
    roll_number = Column(String, nullable=False)
    class_info  = Column(String, nullable=False)
    reason      = Column(Text,   nullable=False)
    start_date  = Column(String, nullable=False)
    end_date    = Column(String, nullable=False)
    total_days  = Column(Integer, nullable=False)
    is_read     = Column(Boolean, default=False)
    created_at  = Column(DateTime, default=datetime.utcnow)

    student = relationship("User", foreign_keys=[student_id], back_populates="leave_requests")


class BusPassRequest(Base):
    __tablename__ = "bus_pass_requests"

    id          = Column(Integer, primary_key=True, index=True)
    student_id  = Column(Integer, ForeignKey("users.id"), nullable=False)
    name        = Column(String, nullable=False)
    roll_number = Column(String, nullable=False)
    class_info  = Column(String, nullable=False)
    is_read     = Column(Boolean, default=False)
    created_at  = Column(DateTime, default=datetime.utcnow)

    student = relationship("User", foreign_keys=[student_id], back_populates="bus_pass_requests")
