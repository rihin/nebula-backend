from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.auth.security import validate_password, hash_password, verify_password
from app.auth.jwt import create_token
from app.auth.schemas import RegisterRequest, LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(data: RegisterRequest):
    db: Session = SessionLocal()

    if db.query(User).filter(User.username == data.username).first():
        db.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    # 🔐 PASSWORD VALIDATION
    validate_password(data.password)

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

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    hashed_password: str = str(user.password_hash)

    if not verify_password(data.password, hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    username_str: str = str(user.username)
    token = create_token(username_str)

    return LoginResponse(
        token=token,
        username=username_str
    )