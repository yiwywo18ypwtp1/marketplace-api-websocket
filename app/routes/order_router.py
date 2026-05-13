from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import User
from app.dependencies.auth import get_current_user
from app.services import order_service
from app.schemas.order_schema import OrderCreate, OrderResponse, SellerSummaryResponse

router = APIRouter()

@router.post("/", response_model=OrderResponse)
async def place_order(
    data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await order_service.create(data, db, current_user)

    return result


@router.patch("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await order_service.cancel(order_id, db, current_user)

    return result


@router.get("/sellers/{seller_id}/summary", response_model=SellerSummaryResponse)
async def seller_summary(
    seller_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await order_service.get_seller_summary(seller_id, db)

    return result