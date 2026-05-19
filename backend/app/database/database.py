"""
Database Configuration
======================
SQLAlchemy setup for Neon PostgreSQL
"""

import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "")

SQLITE_URL = "sqlite:///./travel_api.db"

# Create engine
engine = None
if DATABASE_URL:
    try:
        engine = create_engine(
            DATABASE_URL,
            poolclass=NullPool,
            echo=os.getenv("SQL_ECHO", "false").lower() == "true"
        )
    except Exception as e:
        logger.warning(f"⚠️ Failed to create PostgreSQL engine: {e}. Falling back to SQLite.")
        engine = create_engine(SQLITE_URL)
else:
    engine = create_engine(SQLITE_URL)

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
    """Initialize database tables with automatic SQLite fallback on failure"""
    global engine, SessionLocal
    from sqlalchemy import text
    
    try:
        # Verify if existing tables match our ORM models (using user_id)
        with engine.connect() as conn:
            conn.execute(text("SELECT user_id FROM users LIMIT 1;"))
        logger.info("✅ Neon PostgreSQL database connection verified successfully!")
    except Exception as e:
        logger.warning(
            f"\n❌ DATABASE WARNING: Could not connect to Neon PostgreSQL!\n"
            f"⚠️  Error details: {e}\n"
            f"🔄 RESILIENT FALLBACK: Automatically switching to local SQLite Database (travel_api.db)...\n"
        )
        # Re-create engine with SQLite
        engine = create_engine(SQLITE_URL)
        # Re-bind sessionmaker
        SessionLocal.configure(bind=engine)
        # Re-create SQLite tables
        from app.database.models import Base
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Resilient Fallback database initialized successfully on SQLite (travel_api.db)!")
        
        # Automatically seed landmarks if empty
        db = SessionLocal()
        from app.database.models import Landmark
        try:
            if db.query(Landmark).count() == 0:
                logger.info("🌱 Seeding landmarks into SQLite database...")
                import csv
                import uuid
                csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'landmarks.csv')
                if os.path.exists(csv_path):
                    with open(csv_path, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            landmark = Landmark(
                                landmark_id=uuid.uuid4(),
                                name=row.get('Name', '').strip(),
                                landmark_type=row.get('Type', '').strip(),
                                interest_score=float(row.get('Rating')) if row.get('Rating') else None,
                                visit_duration=int(row.get('EstimatedTime (min)')) if row.get('EstimatedTime (min)') else None,
                                lat=float(row.get('Latitude')) if row.get('Latitude') else 0.0,
                                lon=float(row.get('Longitude')) if row.get('Longitude') else 0.0,
                                description=row.get('Description', ''),
                                image_url=row.get('Images', '')
                            )
                            db.add(landmark)
                    db.commit()
                    logger.info("✅ Successfully seeded landmarks into SQLite!")
                else:
                    logger.warning(f"⚠️ Could not find landmarks CSV at {csv_path} for seeding.")
        except Exception as seed_err:
            db.rollback()
            logger.warning(f"⚠️ Failed to seed landmarks: {seed_err}")
        finally:
            db.close()
