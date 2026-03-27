from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from jose import JWTError
from core.ws_manager import manager
from core.security import decode_token
from core.database import SessionLocal
from models.user import User

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    """
    Connect via:
        ws://localhost:8000/ws?token=<JWT>

    Events the SERVER pushes to the client:
        { "event": "new_message",           "data": { sender, message, timestamp, ... } }
        { "event": "new_bonafide_request",  "data": { roll_number, name, ... } }
        { "event": "new_tc_request",        "data": { roll_number, full_name, ... } }
        { "event": "new_id_card_request",   "data": { roll_number, reason, ... } }
        { "event": "new_leave_request",     "data": { roll_number, full_name, ... } }
        { "event": "new_bus_pass_request",  "data": { roll_number, name, ... } }
        { "event": "user_online",           "data": { identifier, online_users: [...] } }
        { "event": "user_offline",          "data": { identifier, online_users: [...] } }
        { "event": "typing",                "data": { from_user: "..." } }

    Events the CLIENT can send:
        { "event": "ping" }
        { "event": "typing", "to": "<identifier>" }
    """
    # Validate JWT before accepting
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        await websocket.close(code=4001)
        return

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            await websocket.close(code=4001)
            return
        identifier = user.identifier
    finally:
        db.close()

    await manager.connect(identifier, websocket)

    await manager.send_to(identifier, {
        "event": "connected",
        "data": {"identifier": identifier, "online_users": manager.online_users()}
    })

    await manager.send_to_many(
        [u for u in manager.online_users() if u != identifier],
        {"event": "user_online", "data": {"identifier": identifier, "online_users": manager.online_users()}}
    )

    try:
        while True:
            data = await websocket.receive_json()
            event = data.get("event")

            if event == "ping":
                await websocket.send_json({"event": "pong"})

            elif event == "typing":
                to = data.get("to")
                if to:
                    await manager.send_to(to, {
                        "event": "typing",
                        "data": {"from_user": identifier}
                    })

    except WebSocketDisconnect:
        manager.disconnect(identifier, websocket)
        await manager.send_to_many(
            manager.online_users(),
            {"event": "user_offline", "data": {"identifier": identifier, "online_users": manager.online_users()}}
        )
