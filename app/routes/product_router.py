from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import User
from app.schemas.product_schema import ProductResponse, ProductCreate
from app.services import product_service
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=list[ProductResponse])
async def get_all_products(
    db: AsyncSession = Depends(get_db),
    min_price: int | None = None,
    max_price: int | None = None,
):
    products = await product_service.get_all(db, max_price, min_price)

    return products


@router.post("/", response_model=ProductResponse)
async def add_new_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await product_service.create(data, db, current_user)

    return result