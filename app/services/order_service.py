from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Order, User, Product
from app.models.user import UserRole
from app.models.order import OrderStatus
from app.schemas.order_schema import OrderCreate


async def create(
    data: OrderCreate,
    db: AsyncSession,
    current_user: User
):
    if current_user.role != UserRole.buyer:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")
    
    result = await db.execute(
        select(Product).where(Product.id == data.product_id)
    )

    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found") 
    
    if product.stock < data.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough in stock")
    
    product.stock -= data.quantity

    order = Order(
        product_id=data.product_id,
        quantity=data.quantity,
        buyer_id=current_user.id,
        total_price=product.price * data.quantity,
    )

    db.add(order)

    await db.commit()
    await db.refresh(order)

    return order


async def cancel(
    order_id: int,
    db: AsyncSession,
    current_user: User
):
    order_result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = order_result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    product_result = await db.execute(
        select(Product).where(Product.id == order.product_id)
    )
    product = product_result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    if order.buyer_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")

    if order.status == OrderStatus.cancelled:
        raise HTTPException(status_code=400, detail="Order already cancelled")

    order.status = OrderStatus.cancelled
    product.stock += order.quantity

    await db.commit()
    await db.refresh(order)

    return order


async def get_seller_summary(
    seller_id: int,
    db: AsyncSession,
):
    result = await db.execute(
        select(
            func.count(Order.id),
            func.coalesce(func.sum(Order.total_price), 0)
        )
        .join(Product, Product.id == Order.product_id)
        .where(
            Product.seller_id == seller_id,
            Order.status == OrderStatus.active
        )
    )

    total_orders, total_revenue = result.one()

    return {
        "seller_id": seller_id,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
    }