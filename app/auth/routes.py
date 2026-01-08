from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import re

from app.database import get_db
from app.models import User
from app.auth.security import hash_password, verify_password, create_access_token
from app.auth.schemas import RegisterRequest, LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])

PASSWORD_REGEX = re.compile(
    r"^[A-Z][A-Za-z0-9]*[@#$!][0-9]+$"
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    if not PASSWORD_REGEX.fullmatch(data.password):
        raise HTTPException(
            status_code=400,
            detail=(
                "Password must start with a capital letter, "
                "contain one special character (@#$!), "
                "and end with numbers. Example: Zxcvbnm@11"
            ),
        )

    result = await db.execute(
        select(User).where(User.username == data.username)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    user = User(
        username=data.username,
        hashed_password=hash_password(data.password),
    )

    db.add(user)
    await db.commit()

    return {"message": "User created successfully"}


@router.post("/login", response_model=LoginResponse)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.username == data.username)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(
        data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    access_token = create_access_token(
        {"sub": user.username}
    )

    return LoginResponse(
        access_token=access_token,
        username=user.username,
    )
