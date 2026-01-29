import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..__main__ import app
from ..database import Base
from ..api import get_db

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the dependency to use test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def setup_module():
    """Setup function that runs once before module"""
    Base.metadata.create_all(bind=engine)


def teardown_module():
    """Teardown function that runs once after module"""
    Base.metadata.drop_all(bind=engine)


def test_create_chat():
    # Test creating a chat
    response = client.post("/chats/", json={"title": "Test Chat"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Chat"
    chat_id = data["id"]
    
    # Test getting the chat
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == chat_id
    assert data["title"] == "Test Chat"
    assert data["messages"] == []


def test_send_message_to_nonexistent_chat():
    # Try sending a message to a non-existent chat
    response = client.post("/chats/99999/messages/", json={"text": "Hello"})
    assert response.status_code == 404


def test_send_and_get_message():
    # Create a chat first
    response = client.post("/chats/", json={"title": "Another Test Chat"})
    assert response.status_code == 200
    chat_data = response.json()
    chat_id = chat_data["id"]
    assert "id" in chat_data
    
    # Send a message to the chat
    response = client.post(f"/chats/{chat_id}/messages/", json={"text": "Hello World!"})
    assert response.status_code == 200
    msg_data = response.json()
    assert "id" in msg_data
    assert msg_data["chat_id"] == chat_id
    assert msg_data["text"] == "Hello World!"
    message_id = msg_data["id"]
    
    # Get the chat and verify the message is there
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 200
    chat_data = response.json()
    assert len(chat_data["messages"]) == 1
    assert chat_data["messages"][0]["id"] == message_id
    assert chat_data["messages"][0]["text"] == "Hello World!"


def test_delete_chat():
    # Create a chat
    response = client.post("/chats/", json={"title": "To Delete"})
    assert response.status_code == 200
    chat_data = response.json()
    chat_id = chat_data["id"]
    assert "id" in chat_data
    
    # Send a message to the chat
    response = client.post(f"/chats/{chat_id}/messages/", json={"text": "Message to delete"})
    assert response.status_code == 200
    msg_data = response.json()
    assert "id" in msg_data
    
    # Get the chat to confirm it exists
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 200
    
    # Delete the chat
    response = client.delete(f"/chats/{chat_id}")
    assert response.status_code == 200
    
    # Verify the chat doesn't exist anymore
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 404