from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse
import os

# Database URL - using environment variable or default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/chat_app")

# Parse the database URL to handle it properly
result = urlparse(DATABASE_URL)

# Create the engine with proper configuration for PostgreSQL
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=bool(os.getenv("DB_ECHO", False))  # Enable SQL logging if needed
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency for getting database session
    
    Yields:
        Session: A database session
    
    Ensures the session is closed after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()