from fastapi import FastAPI  # type: ignore[import-not-found]
from app.api.audit import router

app = FastAPI(title="Page Pulse API", version="1.0.0")
app.include_router(router)

@app.get("/")
def home():
    return {
        "message": "Page Pulse API Running 🚀"
    }