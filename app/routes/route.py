from fastapi import APIRouter
from app.api.chat import router as chat_api_router 
from app.routes import user

router = APIRouter()

router.include_router(chat_api_router, tags=["Chat"])
router.include_router(user.router, prefix="/users", tags=["User"])
