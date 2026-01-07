from sqlalchemy.orm import Session
from app.models import Message

def save_message(
    db: Session,
    room: str,
    username: str,
    content: str
):
    msg = Message(
        room=room,
        username=username,
        content=content
    )
    db.add(msg)
    db.commit()

def get_recent_messages(
    db: Session,
    room: str,
    limit: int = 20
):
    return (
        db.query(Message)
        .filter(Message.room == room)
        .order_by(Message.timestamp.asc())
        .limit(limit)
        .all()
    )
