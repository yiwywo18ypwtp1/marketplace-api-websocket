from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas.user_schema import UserLogin, UserSignup
from app.utils.jwt import create_access_token
from app.utils.security import verify_pass


async def create_user(data: UserSignup, db: AsyncSession):
    result = await db.execute(
        select(User).where(User.email == data.email)
    )

    user_exists = result.scalar_one_or_none()
    
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    
    hashed = data.hashed_password()
    
    user = User(
        email=data.email,
        username=data.username,
        password=hashed,
        role=data.role,
    )
    db.add(user)

    await db.commit()
    await db.refresh(user)

    return user


async def login_user(data: UserLogin, db: AsyncSession):
    result = await db.execute(
        select(User).where(User.email == data.email)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_pass(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    token = create_access_token({
        "id": str(user.id),
        "email": str(user.email),
        "username": str(user.username),
    })

    return {"token": token, "user": user}