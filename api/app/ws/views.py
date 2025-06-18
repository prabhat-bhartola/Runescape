from fastapi import APIRouter
from fastapi.websockets import WebSocket

from .connection_manager import ws_conn_manager

router = APIRouter()


@router.websocket("")
async def websocket_endpoint(
    websocket: WebSocket,
):
    await ws_conn_manager.connect(websocket)

    async for data in websocket.iter_text():
        ...
