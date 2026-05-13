from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    title: str
    description: str | None
    price: float
    stock: int


class ProductResponse(BaseModel):
    id: int
    title: str
    description: str | None
    price: float
    stock: int
    seller_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)