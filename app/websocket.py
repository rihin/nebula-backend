from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.auth.jwt import verify_token
from app.database import SessionLocal
from app.history.service import save_message, get_recent_messages

def get_users(room: str):
    return list(rooms.get(room, {}).keys())

chat_router = APIRouter()
rooms: dict[str, dict[str, WebSocket]] = {}

@chat_router.websocket("/ws/{room}")
async def chat(ws: WebSocket, room: str):
    token = ws.query_params.get("token")
    username = verify_token(token) if token else None

    if not username:
        await ws.close(code=1008)
        return

    if room not in rooms:
        rooms[room] = {}

    await ws.accept()
    rooms[room][username] = ws

    # 🔥 SEND UPDATED USER LIST
    users = get_users(room)
    for client in rooms[room].values():
        await client.send_text(
            f"__PRESENCE__:{','.join(users)}"
        )

    # 📜 send history (already present)
    db = SessionLocal()
    history = get_recent_messages(db, room)
    for msg in history:
        await ws.send_text(
            f"[{room}] {msg.username}: {msg.content}"
        )

    try:
        while True:
            message = await ws.receive_text()

            save_message(db, room, username, message)

            for client in rooms[room].values():
                if client != ws:
                    await client.send_text(
                        f"[{room}] {username}: {message}"
                    )

    except WebSocketDisconnect:
        rooms[room].pop(username, None)

        # 🔥 UPDATE PRESENCE ON LEAVE
        users = get_users(room)
        for client in rooms[room].values():
            await client.send_text(
                f"__PRESENCE__:{','.join(users)}"
            )

        if not rooms[room]:
            rooms.pop(room)

    finally:
        db.close()
