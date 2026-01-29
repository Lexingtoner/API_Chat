from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import re

Base = declarative_base()


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)  # Limit title length
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Relationship with messages
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan", lazy="select")

    def __repr__(self):
        return f"<Chat(id={self.id}, title='{self.title}', created_at={self.created_at})>"


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True)  # Add index and cascade delete
    text = Column(String(5000), nullable=False)  # Limit text length
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Relationship with chat
    chat = relationship("Chat", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, chat_id={self.chat_id}, created_at={self.created_at})>"