from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import User
from app.schemas.user_schema import LoginResponse, UserLogin, UserResponse, UserSignup
from app.services.user_service import create_user, login_user
from app.dependencies.auth import get_current_user


router = APIRouter()

@router.post("/signup", response_model=UserResponse)
async def signup(data: UserSignup, db: AsyncSession = Depends(get_db)):
    user = await create_user(data, db)

    return user


@router.post("/login", response_model=LoginResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await login_user(data, db)

    return result
    
    
@router.get("/me", response_model=UserResponse)
async def me (current_user: User = Depends(get_current_user)):
    return current_user