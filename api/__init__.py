from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter()


# DB session dependency is imported from database module


# POST /chats/ - Create a new chat
@router.post("/chats/", response_model=schemas.Chat)
def create_chat(chat_data: schemas.ChatCreate, db: Session = Depends(get_db)):
    # Validate title length
    title = chat_data.title.strip()
    if not title or len(title) > 200:
        raise HTTPException(status_code=400, detail="Title must be between 1 and 200 characters")
    
    chat = models.Chat(title=title)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


# POST /chats/{id}/messages/ - Send a message to a chat
@router.post("/chats/{chat_id}/messages/", response_model=schemas.Message)
def create_message(chat_id: int, message_data: schemas.MessageCreate, db: Session = Depends(get_db)):
    # Check if chat exists
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # Validate message text length
    text = message_data.text.strip()
    if not text or len(text) > 5000:
        raise HTTPException(status_code=400, detail="Text must be between 1 and 5000 characters")
    
    message = models.Message(chat_id=chat_id, text=text)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


# GET /chats/{id} - Get a chat and last N messages
@router.get("/chats/{chat_id}", response_model=schemas.ChatWithMessages)
def get_chat(chat_id: int, 
             limit: int = Query(default=20, ge=1, le=100), 
             db: Session = Depends(get_db)):
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # Get latest messages limited by the specified count
    messages = db.query(models.Message)\
                 .filter(models.Message.chat_id == chat_id)\
                 .order_by(models.Message.created_at.desc())\
                 .limit(limit)\
                 .all()
    
    # Reverse to get messages in ascending order (oldest first)
    chat.messages = messages[::-1]
    
    return chat


# DELETE /chats/{id} - Delete a chat and all its messages
@router.delete("/chats/{chat_id}")
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    db.delete(chat)  # Cascade deletion will handle messages
    db.commit()
    return {"status": "success"}