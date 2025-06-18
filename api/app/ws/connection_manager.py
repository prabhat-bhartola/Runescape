import json
from typing import Dict, List

from fastapi import WebSocket


class WSConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_json(self, data: List[Dict]):
        message = json.dumps(data)
        for connection in self.active_connections:
            await connection.send_text(message)


ws_conn_manager = WSConnectionManager()
