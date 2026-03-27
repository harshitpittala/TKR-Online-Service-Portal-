from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.security import get_current_user
from core.ws_manager import manager
from models.user import User
from models.message import Message
from schemas.schemas import MessageCreate, MessageOut

router = APIRouter(prefix="/messages", tags=["Messenger"])


def _out(msg: Message, db: Session) -> dict:
    sender   = db.query(User).filter(User.id == msg.sender_id).first()
    receiver = db.query(User).filter(User.id == msg.receiver_id).first()
    return {
        "id": msg.id,
        "sender_identifier":   sender.identifier   if sender   else "",
        "receiver_identifier": receiver.identifier if receiver else "",
        "content":   msg.content,
        "is_read":   msg.is_read,
        "created_at": msg.created_at,
    }


@router.post("/", status_code=201)
async def send_message(
    data: MessageCreate,
    db:   Session = Depends(get_db),
    me:   User    = Depends(get_current_user),
):
    recipient = db.query(User).filter(User.identifier == data.recipient_identifier).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    if recipient.id == me.id:
        raise HTTPException(status_code=400, detail="Cannot message yourself")

    msg = Message(sender_id=me.id, receiver_id=recipient.id, content=data.content)
    db.add(msg)
    db.commit()
    db.refresh(msg)

    # Real-time push to recipient if online
    await manager.send_to(recipient.identifier, {
        "event": "new_message",
        "data": {
            "id":               msg.id,
            "sender_identifier": me.identifier,
            "content":          msg.content,
            "timestamp":        int(msg.created_at.timestamp() * 1000),
            "is_read":          False,
        }
    })

    return _out(msg, db)


@router.get("/conversation/{other_identifier}")
def get_conversation(
    other_identifier: str,
    db: Session = Depends(get_db),
    me: User    = Depends(get_current_user),
):
    other = db.query(User).filter(User.identifier == other_identifier).first()
    if not other:
        raise HTTPException(status_code=404, detail="User not found")

    msgs = (
        db.query(Message)
        .filter(
            ((Message.sender_id == me.id) & (Message.receiver_id == other.id)) |
            ((Message.sender_id == other.id) & (Message.receiver_id == me.id))
        )
        .order_by(Message.created_at.asc())
        .all()
    )

    # Mark received messages as read
    for m in msgs:
        if m.receiver_id == me.id and not m.is_read:
            m.is_read = True
    db.commit()

    return [_out(m, db) for m in msgs]


@router.get("/contacts")
def get_contacts(
    db: Session = Depends(get_db),
    me: User    = Depends(get_current_user),
):
    """Return all users the current user can message (mirrors frontend contact logic)."""
    from models.user import UserRole
    if me.role == UserRole.student:
        # Students can only message teachers
        contacts = db.query(User).filter(User.role == UserRole.teacher).all()
    else:
        # Teachers can message everyone except themselves
        contacts = db.query(User).filter(User.id != me.id).all()

    return [{"identifier": u.identifier, "role": u.role, "display_name": u.display_name} for u in contacts]


@router.get("/unread-count")
def unread_count(db: Session = Depends(get_db), me: User = Depends(get_current_user)):
    count = db.query(Message).filter(Message.receiver_id == me.id, Message.is_read == False).count()
    return {"unread": count}
