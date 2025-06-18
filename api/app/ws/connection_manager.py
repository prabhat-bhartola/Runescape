import json
from typing import Dict, List
from uuid import UUID

from fastapi import WebSocket


class WSConnectionManager:
    def __init__(self):
        self.active_connections: Dict[UUID, WebSocket] = {}

    async def connect(self, user_id: UUID, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def send_personal_message(self, user_id: UUID, message: str):
        await self.active_connections[user_id].send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

    async def broadcast_json(self, data: List[Dict]):
        message = json.dumps(data)
        for connection in self.active_connections.values():
            await connection.send_text(message)

    def disconnect(self, user_id: UUID):
        del self.active_connections[user_id]


ws_conn_manager = WSConnectionManager()
