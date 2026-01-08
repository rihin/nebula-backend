from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "CHANGE_ME"
ALGORITHM = "HS256"

def create_access_token(username: str) -> str:
    payload = {
        "sub": username,
        "type": "access",
        "exp": datetime.utcnow() + timedelta(minutes=15),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(username: str) -> str:
    payload = {
        "sub": username,
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=7),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str, expected_type: str = "access") -> str:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    if payload.get("type") != expected_type:
        raise JWTError("Invalid token type")

    return payload["sub"]
