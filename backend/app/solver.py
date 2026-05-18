"""
Main Solver Logic
=================
Integrates all algorithms and handles the solving process
"""

import time
from typing import Dict, List, Any
from fastapi import HTTPException

from app.models.schemas import Inputs, SolverResponse, LandmarkResponse, TimePlanEntry
from ai_integration.core.data_loader import get_landmarks, get_hotels, get_time_matrix
from ai_integration.core.node_classes import Landmark, Hotel
from ai_integration.core.problems import TravelProblem_LocalSearch, TravelProblem_InformedSearch
from ai_integration.core.acs_environment import ACSEnvironment

from ai_integration.algorithms.greedy import greedy_search
from ai_integration.algorithms.simulated_annealing import Simulated_Annealing
from ai_integration.algorithms.genetic_algorithm import Genetic_Algorithm
from ai_integration.algorithms.hill_climbing import hill_climbing
from ai_integration.algorithms.acs import AntColonySystem
from ai_integration.algorithms.abc import ABC_Optimization
from ai_integration.algorithms.csp import TravelCSP


def calculate_unified_score(path: List[Landmark], time_matrix: Dict[str, Dict[str, float]]) -> float:
    """Calculate score: (7 * total_rating) - total_travel_time"""
    if not path:
        return 0.0
    
    total_rating = sum(node.interest_score for node in path if isinstance(node, Landmark))
    total_travel_time = 0.0
    
    for i in range(len(path) - 1):
        u_name = path[i].name
        v_name = path[i + 1].name
        total_travel_time += time_matrix.get(u_name, {}).get(v_name, 0.0)
    
    return (7.0 * total_rating) - total_travel_time


def get_time_plan(path: List[Landmark], hotel: Hotel, time_matrix: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
    """Generate time plan showing arrival and visit times"""
    time_plan = {}
    total_elapsed_minutes = 0.0
    
    for i in range(len(path)):
        current = path[i]
        
        if i == 0:
            travel_time = time_matrix.get(hotel.name, {}).get(current.name, 0.0)
            time_plan[current.name] = {
                "arriving_time": round(travel_time, 1),
                "visit_time": current.visit_duration
            }
            total_elapsed_minutes += travel_time + current.visit_duration
        else:
            prev = path[i - 1]
            travel_time = time_matrix.get(prev.name, {}).get(current.name, 0.0)
            time_plan[current.name] = {
                "arriving_time": round(total_elapsed_minutes + travel_time, 1),
                "visit_time": current.visit_duration
            }
            total_elapsed_minutes += travel_time + current.visit_duration
    
    return time_plan


def _serialize_landmark(landmark: Landmark) -> Dict[str, Any]:
    """Convert Landmark to dict"""
    return {
        "id": str(landmark.id) if landmark.id else None,
        "name": landmark.name,
        "lon": landmark.lon,
        "lat": landmark.lat,
        "type": landmark.landmark_type,
        "opening_hours": landmark.opening_hours,
        "visit_duration": landmark.visit_duration,
        "interest_score": landmark.interest_score
    }


def _serialize_path(path: List[Landmark]) -> List[Dict[str, Any]]:
    """Convert path to dict list"""
    return [_serialize_landmark(node) for node in path if isinstance(node, Landmark)]


def solver(inputs: Inputs) -> Dict[str, Any]:
    """
    Main solver function
    """
    # Load data
    landmarks = get_landmarks()
    time_matrix = get_time_matrix()
    hotels = get_hotels()
    
    if not time_matrix:
        raise HTTPException(status_code=503, detail="Time matrix not loaded")
    
    # Validate inputs with robust accent and case-insensitive matching
    import unicodedata
    def clean(s: str) -> str:
        s = s.strip().lower()
        s = "".join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
        return s.replace("hotel", "").replace("hotel", "").replace("–", "-").replace("—", "-").replace(" ", "").replace("'", "").replace("\"", "")

    target_clean = clean(inputs.Hotel_Name)
    hotel = next((h for h in hotels if clean(h.name) == target_clean), None)
    if not hotel:
        # Fallback to substring match
        hotel = next((h for h in hotels if target_clean in clean(h.name) or clean(h.name) in target_clean), None)

    if not hotel:
        available = [h.name for h in hotels[:5]]
        raise HTTPException(
            status_code=404,
            detail=f"Hotel '{inputs.Hotel_Name}' not found. Available: {available}"
        )
    
    valid_days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    day_key = inputs.Travel_day.strip().lower()[:3]
    if day_key not in valid_days:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid Travel_day: '{inputs.Travel_day}'. Use one of: {valid_days}"
        )
    
    # Prepare travel information
    travel_information = {
        'hotel': hotel,
        'Travel_day': day_key,
        'Travel_Time': inputs.Travel_Time,
        'type_filter': inputs.type_filter,
        'trip_start_time': inputs.trip_start_time,
        'time_matrix': time_matrix
    }
    
    # Initialize problem instances
    problem_local = TravelProblem_LocalSearch(landmarks, travel_information)
    
    problem_informed = TravelProblem_InformedSearch(
        hotel=hotel,
        landmarks=landmarks,
        type_filter=inputs.type_filter,
        time_matrix=time_matrix,
        time_budget=int(inputs.Travel_Time * 60),
        starting_time=int(inputs.trip_start_time * 60),
        visiting_day=day_key,
    )
    
    env = ACSEnvironment(
        hotel=hotel,
        landmarks=landmarks,
        type_filter=inputs.type_filter,
        time_matrix=time_matrix,
        time_budget=inputs.Travel_Time,
        starting_time=inputs.trip_start_time,
        visiting_day=day_key,
    )
    
    # Run selected algorithm
    path = None
    runtime = 0.0
    
    if inputs.algo_name == 'Greedy':
        t0 = time.time()
        path = greedy_search(problem_informed)
        runtime = time.time() - t0
    
    elif inputs.algo_name == 'SA':
        sa = Simulated_Annealing(problem_local, initial_temp=50, cooling_rate=0.99, max_reheats=1)
        t0 = time.time()
        path = sa.run()
        runtime = time.time() - t0
    
    elif inputs.algo_name == 'GA':
        ga = Genetic_Algorithm(problem_local, population_size=100, generations=80, mutation_rate=0.10)
        t0 = time.time()
        path = ga.evolve(selection_method='tournament', crossover_method='order', mutation_method='scramble')
        runtime = time.time() - t0
    
    elif inputs.algo_name == 'ACS':
        acs = AntColonySystem(env, num_ants=50, generations=100, alpha=0.5, beta=3.0, rho=0.05)
        t0 = time.time()
        path = acs.solve()
        runtime = time.time() - t0
    
    elif inputs.algo_name == 'ABC':
        abc = ABC_Optimization(problem_local, colony_ratio=0.5, colony_size=60, limit=20, iterations=100, selection_method='rank')
        t0 = time.time()
        path = abc.solve()
        runtime = time.time() - t0
    
    elif inputs.algo_name == 'HillClimbing':
        hc = hill_climbing(problem_local, num_restarts=50, base_strategy='stochastic')
        t0 = time.time()
        path = hc.run()
        runtime = time.time() - t0
    
    elif inputs.algo_name == 'CSP':
        csp_obj = TravelCSP(problem_local, inference_method='fc', var_heuristic='mrv', val_heuristic='lcv', time_limit_s=30.0)
        t0 = time.time()
        path = csp_obj.solve()
        runtime = time.time() - t0
    
    elif inputs.algo_name == 'ACS_Hybrid':
        acs_h = AntColonySystem(env, num_ants=50, generations=100, alpha=0.5, beta=3.0, rho=0.3, hybrid_sa=True)
        t0 = time.time()
        path = acs_h.solve()
        runtime = time.time() - t0
    
    else:
        valid = ['Greedy', 'SA', 'GA', 'ACS', 'ABC', 'HillClimbing', 'CSP', 'ACS_Hybrid']
        raise HTTPException(status_code=400, detail=f"Invalid algorithm: '{inputs.algo_name}'. Choose from: {valid}")
    
    # Prepare response
    if not path:
        path = []
    
    evaluation = calculate_unified_score(path, time_matrix)
    time_plan = get_time_plan(path, hotel, time_matrix)
    
    return {
        "success": True,
        "algorithm": inputs.algo_name,
        "hotel": hotel.name,
        "travel_day": day_key,
        "path": _serialize_path(path),
        "path_names": [node.name for node in path if isinstance(node, Landmark)],
        "runtime_seconds": round(runtime, 3),
        "evaluation_score": round(evaluation, 2),
        "time_plan": time_plan,
        "metadata": {
            "total_landmarks_visited": len([n for n in path if isinstance(n, Landmark)]),
            "total_interest_score": calculate_unified_score(path , time_matrix),
            "time_budget_hours": inputs.Travel_Time,
            "start_time_hour": inputs.trip_start_time
        }
    }
