from sqlalchemy import (Column, Integer, ForeignKey, Text, DateTime)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)

    room_id = Column(Integer, ForeignKey("chat_rooms.id", ondelete="CASCADE"),nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    room = relationship("ChatRoom", back_populates="messages")
    sender = relationship("User", back_populates="sent_messages")