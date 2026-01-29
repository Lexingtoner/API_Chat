from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime


# Chat Schemas
class ChatBase(BaseModel):
    title: str


class ChatCreate(ChatBase):
    pass


class Chat(ChatBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Message Schemas
class MessageBase(BaseModel):
    text: str


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    chat_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Chat with Messages Schema
class ChatWithMessages(Chat):
    messages: List[Message] = Field(default_factory=list)