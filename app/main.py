from fastapi import FastAPI

app = FastAPI(
    title="Nebula Backend",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"status": "API is live 🚀"}

@app.get("/ping")
def ping():
    return {"ping": "pong"}
