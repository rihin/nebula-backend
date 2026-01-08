import re
from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def validate_password(password: str) -> None:
    pattern = r"^[A-Z].*[!@#$%^&*(),.?\":{}|<>].*\d+$"

    if len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long"
        )

    if not re.match(pattern, password):
        raise HTTPException(
            status_code=400,
            detail=(
                "Password must start with a capital letter, "
                "contain a special character, "
                "and end with a number"
            )
        )

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)
