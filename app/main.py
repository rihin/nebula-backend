from fastapi import FastAPI
from app.auth.routes import router as auth_router

app = FastAPI(title="Nebula API 🚀")

app.include_router(auth_router, prefix="/auth")

@app.get("/")
async def root():
    return {"status": "API is live 🚀"}
