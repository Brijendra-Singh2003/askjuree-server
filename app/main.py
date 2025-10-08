from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.routes.route import router
from app.lib.constants import FRONTEND_URL
import os

app = FastAPI()

AUTH_SECRET = os.getenv("AUTH_SECRET") or "your-secret-key"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ FRONTEND_URL],  # Allows all origins, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, adjust as needed
    allow_headers=["*"],  # Allows all headers, adjust as needed
)

app.add_middleware(
    SessionMiddleware,
    secret_key=AUTH_SECRET,
    same_site="none",
    https_only=True,
)

@app.get("/")
async def read_root():
    return {"message": "I'm Juree, you legal assistent!"}

app.include_router(router, prefix="/api")