from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.security import get_current_user
from core.ws_manager import manager
from models.user import User, UserRole
from models.requests import (
    BonafideRequest, TcRequest, IdCardRequest,
    LeaveRequest, BusPassRequest
)
from schemas.schemas import (
    BonafideCreate, BonafideOut,
    TcCreate, TcOut,
    IdCardCreate, IdCardOut,
    LeaveCreate, LeaveOut,
    BusPassCreate, BusPassOut,
)

router = APIRouter(prefix="/requests", tags=["Requests"])

# Mirrors state.js routing constants
TC_RECIPIENTS          = ["krishnasir@tkrcet.com", "accountant@tkrcet.com", "exambranch@tkrcet.com"]
ID_CARD_RECIPIENTS     = ["krishnasir@tkrcet.com", "accountant@tkrcet.com"]
LEAVE_RECIPIENTS       = ["krishnasir@tkrcet.com", "accountant@tkrcet.com"]
BONAFIDE_RECIPIENTS    = ["krishnasir@tkrcet.com", "accountant@tkrcet.com"]
BUS_PASS_RECIPIENTS    = ["accountant@tkrcet.com"]


def _require_student(me: User):
    if me.role != UserRole.student:
        raise HTTPException(status_code=403, detail="Students only")


def _require_teacher(me: User):
    if me.role != UserRole.teacher:
        raise HTTPException(status_code=403, detail="Teachers only")


# ── Bonafide ─────────────────────────────────────────────────────────────────
@router.post("/bonafide", response_model=BonafideOut, status_code=201)
async def submit_bonafide(
    data: BonafideCreate,
    db:   Session = Depends(get_db),
    me:   User    = Depends(get_current_user),
):
    _require_student(me)
    req = BonafideRequest(student_id=me.id, roll_number=me.identifier, **data.model_dump())
    db.add(req)
    db.commit()
    db.refresh(req)

    await manager.send_to_many(BONAFIDE_RECIPIENTS, {
        "event": "new_bonafide_request",
        "data": {"roll_number": me.identifier, "name": data.name, "purpose": data.purpose,
                 "id": req.id, "timestamp": int(req.created_at.timestamp() * 1000)}
    })
    return req


@router.get("/bonafide", response_model=List[BonafideOut])
def get_bonafide_requests(db: Session = Depends(get_db), me: User = Depends(get_current_user)):
    _require_teacher(me)
    if me.identifier not in BONAFIDE_RECIPIENTS:
        raise HTTPException(status_code=403, detail="Not authorized for bonafide requests")
    reqs = db.query(BonafideRequest).order_by(BonafideRequest.created_at.desc()).all()
    for r in reqs: r.is_read = True
    db.commit()
    return reqs


# ── TC ────────────────────────────────────────────────────────────────────────
@router.post("/tc", response_model=TcOut, status_code=201)
async def submit_tc(
    data: TcCreate,
    db:   Session = Depends(get_db),
    me:   User    = Depends(get_current_user),
):
    _require_student(me)
    req = TcRequest(student_id=me.id, roll_number=me.identifier, **data.model_dump())
    db.add(req)
    db.commit()
    db.refresh(req)

    await manager.send_to_many(TC_RECIPIENTS, {
        "event": "new_tc_request",
        "data": {"roll_number": me.identifier, "full_name": data.full_name, "course": data.course,
                 "id": req.id, "timestamp": int(req.created_at.timestamp() * 1000)}
    })
    return req


@router.get("/tc", response_model=List[TcOut])
def get_tc_requests(db: Session = Depends(get_db), me: User = Depends(get_current_user)):
    _require_teacher(me)
    if me.identifier not in TC_RECIPIENTS:
        raise HTTPException(status_code=403, detail="Not authorized for TC requests")
    reqs = db.query(TcRequest).order_by(TcRequest.created_at.desc()).all()
    for r in reqs: r.is_read = True
    db.commit()
    return reqs


# ── ID Card ───────────────────────────────────────────────────────────────────
@router.post("/id-card", response_model=IdCardOut, status_code=201)
async def submit_id_card(
    data: IdCardCreate,
    db:   Session = Depends(get_db),
    me:   User    = Depends(get_current_user),
):
    _require_student(me)
    req = IdCardRequest(student_id=me.id, roll_number=me.identifier, **data.model_dump())
    db.add(req)
    db.commit()
    db.refresh(req)

    await manager.send_to_many(ID_CARD_RECIPIENTS, {
        "event": "new_id_card_request",
        "data": {"roll_number": me.identifier, "reason": data.reason,
                 "id": req.id, "timestamp": int(req.created_at.timestamp() * 1000)}
    })
    return req


@router.get("/id-card", response_model=List[IdCardOut])
def get_id_card_requests(db: Session = Depends(get_db), me: User = Depends(get_current_user)):
    _require_teacher(me)
    if me.identifier not in ID_CARD_RECIPIENTS:
        raise HTTPException(status_code=403, detail="Not authorized for ID card requests")
    reqs = db.query(IdCardRequest).order_by(IdCardRequest.created_at.desc()).all()
    for r in reqs: r.is_read = True
    db.commit()
    return reqs


# ── Leave ─────────────────────────────────────────────────────────────────────
@router.post("/leave", response_model=LeaveOut, status_code=201)
async def submit_leave(
    data: LeaveCreate,
    db:   Session = Depends(get_db),
    me:   User    = Depends(get_current_user),
):
    _require_student(me)
    req = LeaveRequest(student_id=me.id, roll_number=me.identifier, **data.model_dump())
    db.add(req)
    db.commit()
    db.refresh(req)

    await manager.send_to_many(LEAVE_RECIPIENTS, {
        "event": "new_leave_request",
        "data": {"roll_number": me.identifier, "full_name": data.full_name,
                 "reason": data.reason, "start_date": data.start_date, "end_date": data.end_date,
                 "id": req.id, "timestamp": int(req.created_at.timestamp() * 1000)}
    })
    return req


@router.get("/leave", response_model=List[LeaveOut])
def get_leave_requests(db: Session = Depends(get_db), me: User = Depends(get_current_user)):
    _require_teacher(me)
    if me.identifier not in LEAVE_RECIPIENTS:
        raise HTTPException(status_code=403, detail="Not authorized for leave requests")
    reqs = db.query(LeaveRequest).order_by(LeaveRequest.created_at.desc()).all()
    for r in reqs: r.is_read = True
    db.commit()
    return reqs


# ── Bus Pass ──────────────────────────────────────────────────────────────────
@router.post("/bus-pass", response_model=BusPassOut, status_code=201)
async def submit_bus_pass(
    data: BusPassCreate,
    db:   Session = Depends(get_db),
    me:   User    = Depends(get_current_user),
):
    _require_student(me)
    req = BusPassRequest(student_id=me.id, roll_number=me.identifier, **data.model_dump())
    db.add(req)
    db.commit()
    db.refresh(req)

    await manager.send_to_many(BUS_PASS_RECIPIENTS, {
        "event": "new_bus_pass_request",
        "data": {"roll_number": me.identifier, "name": data.name, "class_info": data.class_info,
                 "id": req.id, "timestamp": int(req.created_at.timestamp() * 1000)}
    })
    return req


@router.get("/bus-pass", response_model=List[BusPassOut])
def get_bus_pass_requests(db: Session = Depends(get_db), me: User = Depends(get_current_user)):
    _require_teacher(me)
    if me.identifier not in BUS_PASS_RECIPIENTS:
        raise HTTPException(status_code=403, detail="Not authorized for bus pass requests")
    reqs = db.query(BusPassRequest).order_by(BusPassRequest.created_at.desc()).all()
    for r in reqs: r.is_read = True
    db.commit()
    return reqs


# ── Notification badge counts (for teacher dashboard) ────────────────────────
@router.get("/notification-counts")
def notification_counts(db: Session = Depends(get_db), me: User = Depends(get_current_user)):
    _require_teacher(me)
    counts = {}
    if me.identifier in BONAFIDE_RECIPIENTS:
        counts["bonafide"] = db.query(BonafideRequest).filter_by(is_read=False).count()
    if me.identifier in TC_RECIPIENTS:
        counts["tc"] = db.query(TcRequest).filter_by(is_read=False).count()
    if me.identifier in ID_CARD_RECIPIENTS:
        counts["id_card"] = db.query(IdCardRequest).filter_by(is_read=False).count()
    if me.identifier in LEAVE_RECIPIENTS:
        counts["leave"] = db.query(LeaveRequest).filter_by(is_read=False).count()
    if me.identifier in BUS_PASS_RECIPIENTS:
        counts["bus_pass"] = db.query(BusPassRequest).filter_by(is_read=False).count()
    return counts
