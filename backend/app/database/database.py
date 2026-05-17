"""
Database Configuration
======================
SQLAlchemy setup for Neon PostgreSQL
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Create engine
if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        poolclass=NullPool,
        echo=os.getenv("SQL_ECHO", "false").lower() == "true"
    )
else:
    # Fallback for development without Neon
    engine = create_engine("sqlite:///./travel_api.db")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency for FastAPI to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
