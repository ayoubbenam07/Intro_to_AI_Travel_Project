"""
FastAPI Routes
==============
"""

from fastapi import APIRouter, HTTPException, Header, Depends
from sqlalchemy.orm import Session
import traceback

from app.models.schemas import Inputs, SolverResponse
from app.solver import solver
from app.database.database import get_db
from app.database.models import Itinerary, ItineraryLandmark, Landmark
from app.utils.auth import decode_access_token

router = APIRouter(prefix="/api", tags=["solver"])


@router.get("/hotels")
async def get_hotels_endpoint():
    """Get list of hotels directly from backend/data/hotels.csv"""
    try:
        from ai_integration.core.data_loader import get_hotels
        hotels = get_hotels()
        return [
            {
                "id": f"hotel-{h.name}",
                "name": h.name,
                "latitude": h.lat,
                "longitude": h.lon,
                "type": "Hotel",
                "icon": "🏨",
                "color": "#f39c12"
            }
            for h in hotels
        ]
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to load hotels: {str(e)}")



@router.post("/solve", response_model=SolverResponse)
async def solve_travel(
    inputs: Inputs,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> SolverResponse:
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
    print(f"🔑 [Solve Request] Received Authorization Header: {authorization}")
    try:
        result = solver(inputs)
        
        # If user is logged in (has valid authorization token), save automatically
        if authorization:
            try:
                parts = authorization.split(" ")
                if len(parts) == 2 and parts[0].lower() == "bearer":
                    token = parts[1]
                    payload = decode_access_token(token)
                    if payload and "id" in payload:
                        import uuid
                        import datetime
                        
                        # 1. Fetch pre-loaded landmarks from DB to map names to UUIDs
                        db_landmarks = db.query(Landmark).all()
                        landmark_uuid_map = {l.name.strip().lower(): l.landmark_id for l in db_landmarks}
                        
                        # 2. Translate algorithm name to custom DB enum format
                        ALGO_ENUM_MAP = {
                            "Greedy": "greedy",
                            "SA": "SA",
                            "GA": "GA",
                            "CSP": "CSP",
                            "ACS": "ACS",
                            "ABC": "ABC",
                            "HillClimbing": "hill_climbing",
                            "ACS_Hybrid": "ACS-SA"
                        }
                        algo_enum = ALGO_ENUM_MAP.get(inputs.algo_name, "greedy")
                        
                        # 3. Create start time object
                        start_hour = int(inputs.trip_start_time)
                        start_minute = int((inputs.trip_start_time - start_hour) * 60)
                        start_time_obj = datetime.time(hour=start_hour, minute=start_minute)
                        
                        # 4. Generate a UUID for the itinerary
                        itinerary_uuid = uuid.uuid4()
                        
                        # Resolve user UUID safely with email fallback if token is old/cached
                        user_uuid = None
                        try:
                            user_uuid = uuid.UUID(str(payload.get("id")))
                        except Exception:
                            user_email = payload.get("email")
                            if user_email:
                                db_user = db.query(User).filter(User.email == user_email).first()
                                if db_user:
                                    user_uuid = db_user.user_id
                                    
                        if not user_uuid:
                            raise ValueError(f"Could not resolve UUID for user {payload.get('email')}")
                            
                        travel_day_val = inputs.Travel_day.strip().lower()
                        
                        itinerary = Itinerary(
                            itinerary_id=itinerary_uuid,
                            user_id=user_uuid,
                            name=f"Trip from {inputs.Hotel_Name}",
                            itinerary_type="day_trip",
                            algorithm_used=algo_enum,
                            fitness_score=result.get("evaluation_score", 0.0),
                            time_budget_h=inputs.Travel_Time,
                            travel_day=travel_day_val,
                            start_time=start_time_obj,
                            is_saved=True,
                            created_at=datetime.datetime.utcnow()
                        )
                        db.add(itinerary)
                        db.flush()  # Allocate session resources before child relations
                        
                        # 6. Save order, arrival and departure details in itinerary_landmarks join table
                        path_data = result.get("path", [])
                        time_plan_data = result.get("time_plan", {})
                        
                        start_minutes = inputs.trip_start_time * 60.0
                        
                        for idx, lm in enumerate(path_data):
                            lm_name = ""
                            if isinstance(lm, dict):
                                lm_name = lm.get("name", "")
                            else:
                                lm_name = getattr(lm, "name", "")
                                
                            lm_name_clean = lm_name.strip().lower()
                            landmark_id = landmark_uuid_map.get(lm_name_clean)
                            
                            # If not pre-loaded, lookup by close substring match
                            if not landmark_id:
                                for name, u_id in landmark_uuid_map.items():
                                    if lm_name_clean in name or name in lm_name_clean:
                                        landmark_id = u_id
                                        break
                                        
                            if landmark_id:
                                # Retrieve arrival and departure details from time_plan
                                plan_entry = time_plan_data.get(lm_name, {})
                                arriving_time_min = 0.0
                                visit_duration_min = 0.0
                                
                                if plan_entry:
                                    if isinstance(plan_entry, dict):
                                        arriving_time_min = float(plan_entry.get("arriving_time", 0.0))
                                        visit_duration_min = float(plan_entry.get("visit_time", 0.0))
                                    else:
                                        arriving_time_min = float(getattr(plan_entry, "arriving_time", 0.0))
                                        visit_duration_min = float(getattr(plan_entry, "visit_time", 0.0))
                                
                                # Convert minutes relative to trip start time into absolute clock times
                                arr_minutes_abs = start_minutes + arriving_time_min
                                arr_hour = int((arr_minutes_abs / 60.0) % 24)
                                arr_min = int(arr_minutes_abs % 60)
                                arr_time_obj = datetime.time(hour=arr_hour, minute=arr_min)
                                
                                dep_minutes_abs = arr_minutes_abs + visit_duration_min
                                dep_hour = int((dep_minutes_abs / 60.0) % 24)
                                dep_min = int(dep_minutes_abs % 60)
                                dep_time_obj = datetime.time(hour=dep_hour, minute=dep_min)
                                
                                itinerary_landmark = ItineraryLandmark(
                                    itinerary_id=itinerary_uuid,
                                    landmark_id=landmark_id,
                                    position=idx + 1,  # 1-based index for order
                                    arrival_time=arr_time_obj,
                                    departure_time=dep_time_obj
                                )
                                db.add(itinerary_landmark)
                                
                        db.commit()
                        print(f"🎉 Successfully saved itinerary {itinerary_uuid} and its landmarks into itinerary_landmarks for user {payload['email']}")
            except Exception as auth_err:
                print(f"Skipping auto-save: {auth_err}")
                traceback.print_exc()

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
