from fastapi import Depends, APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.users import User
from app.dependencies import get_db
from authlib.integrations.starlette_client import OAuth
from app.lib.constants import FRONTEND_URL
import os

router = APIRouter()

oauth = OAuth()

oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@router.get("/login")
async def login(request: Request, next: str = "/"):
    request.session["next_url"] = next
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/callback/google")
async def auth(request: Request, db: AsyncSession = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]

    statement = select(User).where(User.email == user_info["email"])
    result = await db.execute(statement=statement)
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            name=user_info.get("name"),
            email=user_info.get("email"),
            picture=user_info.get("picture"),
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    request.session["user"] = {
        "id": str(user.id),
        "name": user_info.get("name"),
        "email":user_info.get("email"),
        "picture":user_info.get("picture"),
    }

    next_path = request.session.pop("next_url", "/")
    redirect_url = f"{FRONTEND_URL}{next_path}"
    return RedirectResponse(url=redirect_url)


@router.get("/logout")
async def logout(request: Request, next: str = "/"):
    del request.session["user"]
    
    redirect_url = f"{FRONTEND_URL}{next}"
    return RedirectResponse(url=redirect_url)


@router.get("/me")
async def me(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401)
    return user