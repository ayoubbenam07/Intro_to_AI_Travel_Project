"""
Pydantic Models for API
=======================
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


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
