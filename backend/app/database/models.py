"""
Database Models
===============
SQLAlchemy models matching the pre-existing Neon PostgreSQL schema
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database.database import Base


class User(Base):
    """User accounts model matching Neon schema"""
    __tablename__ = "users"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    budget_profile = Column(String, nullable=False)  # 'low', 'medium', 'high' enums
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    itineraries = relationship("Itinerary", back_populates="user", cascade="all, delete-orphan")


class Landmark(Base):
    """Landmarks pre-loaded in database"""
    __tablename__ = "landmarks"
    
    landmark_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    landmark_type = Column(String, nullable=False)
    interest_score = Column(Float, nullable=True)
    visit_duration = Column(Integer, nullable=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)


class Itinerary(Base):
    """Itineraries master table matching Neon schema"""
    __tablename__ = "itineraries"
    
    itinerary_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    itinerary_type = Column(String, nullable=False)  # 'day_trip', 'weekend', 'week', 'custom'
    algorithm_used = Column(String, nullable=False)  # enums: 'greedy', 'SA', 'GA', etc.
    fitness_score = Column(Float, nullable=True)
    time_budget_h = Column(Float, nullable=True)
    travel_day = Column(String, nullable=True)
    start_time = Column(Time, nullable=True)
    is_saved = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    user = relationship("User", back_populates="itineraries")
    landmarks = relationship("ItineraryLandmark", back_populates="itinerary", cascade="all, delete-orphan")


class ItineraryLandmark(Base):
    """Relation table joining itineraries and landmarks in order"""
    __tablename__ = "itinerary_landmarks"
    
    itinerary_id = Column(UUID(as_uuid=True), ForeignKey("itineraries.itinerary_id", ondelete="CASCADE"), primary_key=True)
    landmark_id = Column(UUID(as_uuid=True), ForeignKey("landmarks.landmark_id", ondelete="CASCADE"), primary_key=True)
    position = Column(Integer, nullable=False)  # Order of visit
    arrival_time = Column(Time, nullable=True)
    departure_time = Column(Time, nullable=True)
    
    itinerary = relationship("Itinerary", back_populates="landmarks")
    landmark = relationship("Landmark")
