from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.auth.jwt import verify_token
from app.database import SessionLocal
from app.history.service import save_message, get_recent_messages
import asyncio

chat_router = APIRouter()

# room -> { username -> WebSocket }
rooms: dict[str, dict[str, WebSocket]] = {}

from fastapi import WebSocket, WebSocketDisconnect, Depends
from jose import jwt, JWTError
from app.auth.security import SECRET_KEY, ALGORITHM

async def get_user_from_ws(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        await websocket.close(code=1008)
        return None


async def heartbeat(ws: WebSocket):
    while True:
        await asyncio.sleep(25)
        await ws.send_text("__PING__")


def get_users(room: str):
    return list(rooms.get(room, {}).keys())


@chat_router.websocket("/ws/{room}")
async def chat(ws: WebSocket, room: str):
    token = ws.query_params.get("token")

    if not token:
        await ws.close(code=1008)
        return

    # 🔐 SAFE TOKEN VERIFICATION (CRITICAL FIX)
    try:
        username = verify_token(token, "access")
    except Exception:
        await ws.close(code=1008)
        return

    if not username:
        await ws.close(code=1008)
        return

    # Init room
    if room not in rooms:
        rooms[room] = {}

    await ws.accept()
    rooms[room][username] = ws

    # 🔥 SEND PRESENCE UPDATE (JOIN)
    users = get_users(room)
    for client in rooms[room].values():
        await client.send_text(f"__PRESENCE__:{','.join(users)}")

    # 📜 SEND MESSAGE HISTORY
    db = SessionLocal()
    history = get_recent_messages(db, room)
    for msg in history:
        await ws.send_text(f"[{room}] {msg.username}: {msg.content}")

    try:
        while True:
            message = await ws.receive_text()

            save_message(db, room, username, message)

            for client in rooms[room].values():
                await client.send_text(f"[{room}] {username}: {message}")

    except WebSocketDisconnect:
        # 🚪 REMOVE USER
        rooms[room].pop(username, None)

        # 🔥 PRESENCE UPDATE (LEAVE)
        users = get_users(room)
        for client in rooms.get(room, {}).values():
            await client.send_text(f"__PRESENCE__:{','.join(users)}")

        if not rooms.get(room):
            rooms.pop(room, None)

    finally:
        db.close()
