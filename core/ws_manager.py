from fastapi import WebSocket
from typing import Dict
import json


class ConnectionManager:
    """
    Maps identifier (email or roll number) → WebSocket.
    Used to push real-time events to specific users.
    """
    def __init__(self):
        # Allow multiple concurrent sessions per identifier (e.g., phone + laptop).
        self.active: Dict[str, list[WebSocket]] = {}

    async def connect(self, identifier: str, ws: WebSocket):
        await ws.accept()
        self.active.setdefault(identifier, []).append(ws)

    def disconnect(self, identifier: str, ws: WebSocket | None = None):
        if identifier not in self.active:
            return

        if ws is None:
            self.active.pop(identifier, None)
            return

        sockets = self.active.get(identifier, [])
        self.active[identifier] = [sock for sock in sockets if sock is not ws]
        if not self.active[identifier]:
            self.active.pop(identifier, None)

    async def send_to(self, identifier: str, event: dict):
        sockets = list(self.active.get(identifier, []))
        for ws in sockets:
            try:
                await ws.send_text(json.dumps(event))
            except Exception:
                self.disconnect(identifier, ws)

    async def send_to_many(self, identifiers: list, event: dict):
        for ident in identifiers:
            await self.send_to(ident, event)

    def online_users(self) -> list:
        return list(self.active.keys())


manager = ConnectionManager()
