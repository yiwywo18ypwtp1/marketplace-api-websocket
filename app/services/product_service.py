from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product
from app.schemas.product_schema import ProductCreate
from app.models.user import User, UserRole

async def get_all(db: AsyncSession, max_price: float, min_price: float):
    query = select(Product)

    if min_price is not None:
        query = query.where(
            Product.price >= min_price
        )

    if max_price is not None: 
        query = query.where(
            Product.price <= max_price
        )

    result = await db.execute(query)

    products = result.scalars().all()

    return products


async def create(
    data: ProductCreate,
    db: AsyncSession,
    current_user: User
):
    if current_user.role != UserRole.seller:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")

    product = Product(
        title=data.title,
        description=data.description or "",
        price=data.price,
        stock=data.stock,
        seller_id=current_user.id,
    )
    db.add(product)

    await db.commit()
    await db.refresh(product)

    return product
