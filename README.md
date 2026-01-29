# Chat and Messages API

This is a FastAPI application that provides API endpoints for managing chats and messages. The application uses PostgreSQL as the database backend and SQLAlchemy as the ORM.

## Features

- Create new chats with titles
- Send messages to specific chats
- Retrieve chats along with their messages
- Delete chats (with all associated messages)
- Input validation for titles and messages
- Cascading deletion of messages when a chat is removed

## Requirements

- Docker
- Docker Compose

## Setup and Running

1. Clone this repository
2. Navigate to the project directory
3. Run the following command to start the application:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

## API Endpoints

- `POST /chats/` - Create a new chat
- `POST /chats/{id}/messages/` - Send a message to a chat
- `GET /chats/{id}` - Get a chat and its messages (with limit parameter)
- `DELETE /chats/{id}` - Delete a chat and all its messages

## Running Tests

To run the tests:

```bash
docker exec -it <container-name> pytest
```

Or locally after installing dependencies:

```bash
pip install -r requirements.txt
pytest tests/
```

## Technologies Used

- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker & Docker Compose
- Pydantic for request/response validation
- Pytest for testing