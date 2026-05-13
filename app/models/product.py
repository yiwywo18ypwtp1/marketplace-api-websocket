from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    seller = relationship("User", back_populates="products")
    orders = relationship("Order", back_populates="product", cascade="all, delete")