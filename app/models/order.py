from sqlalchemy import Column, Float,Integer,ForeignKey,DateTime,Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base
import enum


class OrderStatus(str, enum.Enum):
    active = "active"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    quantity = Column(Integer, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.active, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    buyer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    total_price = Column(Float, nullable=False)

    buyer = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")
