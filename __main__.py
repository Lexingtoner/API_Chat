from fastapi import FastAPI
from .api import router
from .database import engine, Base
import uvicorn
import os

# Create FastAPI app instance
app = FastAPI(
    title="Chat and Messages API",
    description="API for managing chats and messages",
    version="1.0.0",
)

# Create tables at startup if enabled via env var
@app.on_event("startup")
def on_startup():
    if os.getenv("AUTO_CREATE_TABLES", "false").lower() == "true":
        Base.metadata.create_all(bind=engine)

# Include API routes
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)