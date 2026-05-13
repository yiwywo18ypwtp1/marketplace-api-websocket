from sqlalchemy import Column, Integer, ForeignKey

from sqlalchemy.orm import relationship

from app.db import Base


class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    id = Column(Integer, primary_key=True)
    
    buyer_id = Column( Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    seller_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE") ,nullable=False)

    messages = relationship( "Message", back_populates="room", cascade="all, delete")