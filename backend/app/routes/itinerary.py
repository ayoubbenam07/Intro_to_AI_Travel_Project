"""
Itinerary Routes
================
Endpoints to manage saved itineraries for authenticated users
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db
from app.database.models import Itinerary, User
from app.models.schemas import SavedItineraryResponse
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api", tags=["itineraries"])


class ItineraryCreate(BaseModel):
    """Payload to save an itinerary"""
    algorithm: str
    hotel: str
    travel_day: str
    evaluation_score: float
    runtime_seconds: float
    path: List[Dict[str, Any]]
    time_plan: Dict[str, Any]
    metadata_info: Dict[str, Any]


@router.post("/itineraries", response_model=SavedItineraryResponse, status_code=status.HTTP_201_CREATED)
async def save_itinerary(
    payload: ItineraryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save an itinerary for the currently logged-in user"""
    itinerary = Itinerary(
        user_id=current_user.user_id,
        algorithm=payload.algorithm,
        hotel=payload.hotel,
        travel_day=payload.travel_day,
        evaluation_score=payload.evaluation_score,
        runtime_seconds=payload.runtime_seconds,
        path=payload.path,
        time_plan=payload.time_plan,
        metadata_info=payload.metadata_info
    )
    db.add(itinerary)
    db.commit()
    db.refresh(itinerary)
    return itinerary


@router.get("/itineraries", response_model=List[SavedItineraryResponse])
async def list_itineraries(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all saved itineraries for the logged-in user"""
    itineraries = db.query(Itinerary).filter(Itinerary.user_id == current_user.user_id).order_by(Itinerary.created_at.desc()).all()
    return itineraries


@router.delete("/itineraries/{itinerary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_itinerary(
    itinerary_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a specific saved itinerary"""
    itinerary = db.query(Itinerary).filter(
        Itinerary.itinerary_id == itinerary_id,
        Itinerary.user_id == current_user.user_id
    ).first()
    
    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Itinerary not found or unauthorized to delete"
        )
        
    db.delete(itinerary)
    db.commit()
    return None
