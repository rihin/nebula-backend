from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "CHANGE_ME_LATER"
ALGORITHM = "HS256"
EXPIRY_MINUTES = 60 * 24


def create_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=EXPIRY_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> str:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get("sub")
