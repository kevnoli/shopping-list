from fastapi import APIRouter, Depends

from models import AccessToken, User, UserRead
from controllers.auth import token, register, refresh, get_user, signout

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=AccessToken)
async def login(access_token: AccessToken = Depends(token)):
    return access_token

@router.post("/signup", response_model=UserRead)
async def signup(user: UserRead = Depends(register)):
    return user

@router.post("/refresh", response_model=AccessToken)
async def refresh_token(access_token: AccessToken = Depends(refresh)):
    return access_token

@router.get("/me", response_model=UserRead)
async def get_current_user(user: User = Depends(get_user)):
    return user

@router.post("/logout")
async def logout(data = Depends(signout)):
    return None