from fastapi import APIRouter
from app.api.chat import router as chat_api_router 

router = APIRouter()

router.include_router(chat_api_router, tags=["Chat"])
