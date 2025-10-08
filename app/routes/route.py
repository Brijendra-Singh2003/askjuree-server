from fastapi import APIRouter
from app.api.chat import router as chat_api_router 
from app.routes import review_offer_letter, user

router = APIRouter()

router.include_router(chat_api_router, tags=["Chat"])
router.include_router(user.router, tags=["User"])
router.include_router(review_offer_letter.router, tags=["Review offer letter"])
