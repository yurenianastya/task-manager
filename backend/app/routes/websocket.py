import asyncio

from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect, APIRouter

notifications: Dict[int, List[str]] = {}
active_connections: Dict[int, List[WebSocket]] = {}

ws_router = APIRouter()

async def notify_user(user_id: int, message: str):
    notifications.setdefault(user_id, []).append(message)
    conns = active_connections.get(user_id, []) + active_connections.get(0, [])
    disconnected = []
    for ws in conns:
        try:
            await ws.send_text(message)
        except Exception:
            disconnected.append(ws)
    for ws in disconnected:
        conns.remove(ws)

async def send_notification(msg: str, user_id: int):
    await notify_user(user_id, msg)

@ws_router.websocket("/ws/notifications")
async def global_websocket(websocket: WebSocket):
    await websocket.accept()
    active_connections.setdefault(0, []).append(websocket)
    try:
        while True:
            await asyncio.sleep(60)
    except WebSocketDisconnect:
        active_connections[0].remove(websocket)