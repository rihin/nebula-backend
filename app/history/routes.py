from fastapi import APIRouter
from app.database import SessionLocal
from app.history.service import get_recent_messages

router = APIRouter(prefix="/history", tags=["history"])

@router.get("/{room}")
def history(room: str, limit: int = 20):
    db = SessionLocal()
    msgs = get_recent_messages(db, room, limit)
    db.close()

    return [
        {
            "room": m.room,
            "user": m.username,
            "content": m.content,
            "time": m.timestamp
        }
        for m in msgs
    ]
