from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
)
from app.auth.jwt import create_token
from app.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    LoginResponse
)


import re
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_token

router = APIRouter(prefix="/auth", tags=["auth"])

PASSWORD_REGEX = re.compile(
    r"^[A-Z][A-Za-z0-9]*[@#$!][0-9]+$"
)

@router.post("/register")
def register(username: str, password: str):
    if not PASSWORD_REGEX.match(password):
        raise HTTPException(
            status_code=400,
            detail="Password must start with capital letter, include special character, and end with numbers (e.g. Asdfghjkl@11)"
        )

    db: Session = SessionLocal()

    if db.query(User).filter(User.username == username).first():
        db.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        username=username,
        password_hash=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return {"message": "User created"}


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.username == data.username).first()
    db.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    hashed_password: str = str(user.password_hash)

    if not verify_password(data.password, hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    username_str: str = str(user.username)
    token = create_token(username_str)

    return LoginResponse(token=token, username=username_str)
