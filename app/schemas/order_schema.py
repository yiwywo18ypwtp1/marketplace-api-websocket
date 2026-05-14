from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.order import OrderStatus


class Order(BaseModel):
    product_id: int
    quantity: int
    buyer_id: int
    total_price: float


class OrderCreate(BaseModel):
    product_id: int
    quantity: int


class OrderResponse(BaseModel):
    id: int
    quantity: int
    status: OrderStatus
    total_price: float
    created_at: datetime
    buyer_id: int
    product_id: int

    model_config = ConfigDict(from_attributes=True)


class SellerSummaryResponse(BaseModel):
    seller_id: int
    total_orders: int
    total_revenue: float