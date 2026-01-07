from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.auth.jwt import create_token

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    username: str

@router.post("/login")
def login(data: LoginRequest):
    if not data.username.strip():
        raise HTTPException(status_code=400, detail="Username required")

    token = create_token(data.username)
    return {"token": token}
