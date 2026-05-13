from sqlalchemy import (Column, Integer, String, Enum)
from sqlalchemy.orm import relationship
import enum

from app.db import Base


class UserRole(str, enum.Enum):
    buyer = "buyer"
    seller = "seller"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    products = relationship("Product", back_populates="seller", cascade="all, delete")
    orders = relationship("Order", back_populates="buyer", cascade="all, delete")
    sent_messages = relationship("Message", back_populates="sender", cascade="all, delete")