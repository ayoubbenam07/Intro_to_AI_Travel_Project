"""
Pydantic Models for API
=======================
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import time # Assuming you use standard python time or sqlalchemy Time

class Inputs(BaseModel):
    """Request model for /api/solve endpoint"""
    Hotel_Name: str = Field(..., description="Name of the hotel")
    Travel_day: str = Field(..., description="Day of week (e.g., Monday)")
    Travel_Time: float = Field(..., description="Travel time in hours")
    type_filter: List[str] = Field(default_factory=list, description="Landmark types to filter")
    trip_start_time: float = Field(..., description="Start time as hour of day (e.g., 9)")
    algo_name: str = Field(..., description="Algorithm name (Greedy, SA, GA, ACS, ABC, HillClimbing, CSP)")


class LandmarkResponse(BaseModel):
    """Landmark object in response"""
    id: Optional[str] = None
    name: str
    lon: float
    lat: float
    type: str
    opening_hours: Dict[str, Any]
    visit_duration: int
    interest_score: float
    description: Optional[str] = None
    image_url: Optional[str] = None


from datetime import datetime


class TimePlanEntry(BaseModel):
    """Time plan entry for each landmark"""
    arriving_time: float
    visit_time: int


class SolverResponse(BaseModel):
    """Response model for /api/solve endpoint"""
    success: bool
    algorithm: str
    hotel: str
    travel_day: str
    path: List[LandmarkResponse]
    path_names: List[str]
    runtime_seconds: float
    evaluation_score: float
    time_plan: Dict[str, TimePlanEntry]
    metadata: Dict[str, Any]


class UserCreate(BaseModel):
    """Pydantic model for creating a user account"""
    email: str
    password: str


class UserLogin(BaseModel):
    """Pydantic model for logging in a user"""
    email: str
    password: str


class UserResponse(BaseModel):
    """Pydantic model for user detail response"""
    user_id: Any
    email: str
    full_name: Optional[str] = None
    budget_profile: Optional[str] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Pydantic model for auth tokens"""
    access_token: str
    token_type: str


class SavedItineraryResponse(BaseModel):
    """Pydantic model for a saved itinerary response"""
    itinerary_id: Any
    user_id: Any
    name: str
    itinerary_type: str
    algorithm: str
    evaluation_score: Optional[float] = None
    time_budget_hours: Optional[float] = None
    travel_day: Optional[str] = None
    start_time_hour: Optional[Any] = None
    is_saved: bool
    created_at: datetime
    num_types: Optional[int] = None

    class Config:
        from_attributes = True




class ItineraryPathItemResponse(BaseModel):
    """Represents a single landmark in the itinerary path"""
    landmark_id: str
    name: str
    landmark_type: str
    lat: float
    lon: float
    interest_score: Optional[float] = None
    visit_duration: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    
    # Specifics from the itinerary planning
    position: int
    arrival_time: Optional[time] = None
    departure_time: Optional[time] = None

    class Config:
        from_attributes = True