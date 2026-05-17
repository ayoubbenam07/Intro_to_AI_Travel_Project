"""
FastAPI Routes
==============
"""

from fastapi import APIRouter, HTTPException
import traceback

from app.models.schemas import Inputs, SolverResponse
from app.solver import solver

router = APIRouter(prefix="/api", tags=["solver"])


@router.post("/solve", response_model=SolverResponse)
async def solve_travel(inputs: Inputs) -> SolverResponse:
    """
    Main endpoint for travel planning
    
    Accepts:
    - Hotel_Name: Name of the hotel
    - Travel_day: Day of week (mon, tue, wed, thu, fri, sat, sun)
    - Travel_Time: Travel time in hours
    - type_filter: List of landmark types to include
    - trip_start_time: Start time as hour of day (0-24)
    - algo_name: Algorithm to use
    
    Algorithms:
    - Greedy: Greedy Best-First Search
    - SA: Simulated Annealing
    - GA: Genetic Algorithm
    - ACS: Ant Colony System
    - ABC: Artificial Bee Colony
    - HillClimbing: Hill Climbing
    - CSP: Constraint Satisfaction Problem
    - ACS_Hybrid: ACS with Simulated Annealing
    """
    try:
        result = solver(inputs)
        return SolverResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": "1.0.0",
        "service": "Travel Itinerary Optimization API"
    }


@router.get("/algorithms")
async def get_algorithms():
    """Get list of available algorithms"""
    return {
        "algorithms": [
            {"name": "Greedy", "type": "Heuristic Search"},
            {"name": "SA", "type": "Metaheuristic"},
            {"name": "GA", "type": "Evolutionary"},
            {"name": "ACS", "type": "Swarm"},
            {"name": "ABC", "type": "Swarm"},
            {"name": "HillClimbing", "type": "Local Search"},
            {"name": "CSP", "type": "Constraint-based"},
            {"name": "ACS_Hybrid", "type": "Hybrid"}
        ]
    }
