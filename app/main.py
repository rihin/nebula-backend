from fastapi import FastAPI
from app.websocket import chat_router
from app.auth.routes import router as auth_router
from app.database import engine
from app.models import Base
from app.history.routes import router as history_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🧱 Create tables on startup
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(history_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)