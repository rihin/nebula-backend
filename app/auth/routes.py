from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_token
from app.auth.schemas import RegisterRequest, LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(data: RegisterRequest):
    db: Session = SessionLocal()

    if db.query(User).filter(User.username == data.username).first():
        db.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        username=data.username,
        password_hash=hash_password(data.password)
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

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": user.username})

    return LoginResponse(
        token=token,
        username=user.username
    )
