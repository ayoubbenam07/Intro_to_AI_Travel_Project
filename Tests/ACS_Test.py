"""

If you want to experiment with the algorithm's performance, here are the parameters 
you can change when initializing the `AntColonySystem` class.

--- 1. THE BIG 3 (These control the AI's "Intelligence" and pathfinding) ---
* alpha (float) : Trust in the Herd (Default: 1.0)
    - How much the ant follows the pheromones of past trips.
    - If too high (> 2.0), the ants all take the same path and get stuck in a local optimum.

* beta (float)  : Trust in Logic (Default: 2.5)
    - How much the ant cares about distance, ratings, and time limits.
    - Crucial for Time Windows: Beta MUST be higher than Alpha!
    - Try testing between 2.0 and 3.5.

* rho (float)   : Evaporation Rate (Default: 0.1)
    - How fast bad trips fade from memory (0.1 = 10% fade per generation).
    - If too low (0.01), bad paths linger forever. If too high (0.5), ants forget good trips.

--- 2. THE HARDWARE LIMITS (These control how long the code takes to run) ---
* num_ants (int)    : Number of tourists spawned per generation (Default: 30)
    - 30 to 50 is perfect for fast Python execution. 

* generations (int) : Number of iterations to run (Default: 100)
    - ACS usually finds the perfect route by generation 60-80. 100 guarantees convergence.

--- 3. THE MATH FIXERS (Hardcoded inside ACSEnvironment - Leave these alone!) ---
* Q (Scaling Factor = 0.05)   : Scales massive scores down to healthy pheromone drops.
* tau_min (Pheromone Floor)   : Never lets a path hit 0.0 to prevent math crashes.
* weight (Rank Decay = 0.8)   : Ensures the #1 ant drops more smell than the #5 ant.
======================================================================================
"""

import sys
import os
import random
import time
from typing import List

# Setup paths (Adjust this if your folder structure is slightly different)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Import the new ACS classes
from core.Problem_AntColony import ACSEnvironment
from Algorithms.ACS import AntColonySystem
from core.Node_Classes import Landmark, Hotel

# Import your data loader
from utils import data_loader


# ==========================================
# UNIVERSAL EVALUATOR (For Cross-Algorithm Comparison)
# ==========================================
def evaluate_comparative_score(state: List[Landmark], hotel: Hotel, time_matrix: dict) -> float:
    """ 
    The standard Fitness Function used across all algorithms (Local Search, SA, etc.).
    Minimizes distance while heavily maximizing the interest score.
    A lower (more negative) resulting float indicates a better itinerary.
    """ 
    if not state:
        return 0.0
        
    total_rating = 0
    total_travel_time = 0 

    for i, landmark in enumerate(state):
        total_rating += landmark.interest_score
        
        # Travel time from hotel to first landmark, or between landmarks
        if i == 0:
            total_travel_time += time_matrix[hotel.name][landmark.name]
        else:
            total_travel_time += time_matrix[state[i-1].name][landmark.name]

    # Travel time from final landmark back to the hotel
    total_travel_time += time_matrix[state[-1].name][hotel.name]

    # Let the rating act as the most important criteria 
    # The lower is better, it will be negative
    RATING_WEIGHT = 20
    score = total_travel_time - (RATING_WEIGHT * total_rating)
    
    return score


# ==========================================
# 1. LOAD DATA ONCE
# ==========================================
print("Loading data...")
landmarks = data_loader.get_landmarks()
hotels = data_loader.get_hotels()
time_matrix = data_loader.get_time_matrix()
days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

# Mock user request
travel_information = {
    "hotel": random.choice(hotels),
    "Travel_day": random.choice(days), 
    "Travel_Time": 10.0,            # 10 hours budget
    "type_filter": None,                    
    "time_matrix": time_matrix,
    "trip_start_time": 8.0          # Starts at 8:00 AM
}

print("="*50)
print(f"Start Hotel : {travel_information['hotel'].name}")
print(f"Travel Day  : {travel_information['Travel_day'].upper()}")
print(f"Time Budget : {travel_information['Travel_Time']} hours")
print("="*50)

# ==========================================
# 2. RUN A SINGLE TEST OF THE ALGORITHM
# ==========================================
def run_basic_acs_test():
    
    # 1. Initialize the Environment (The Map & Pheromone Memory)
    print("Initializing ACS Environment...")
    env = ACSEnvironment(
        hotel=travel_information["hotel"],
        landmarks=landmarks,
        time_matrix=travel_information["time_matrix"],
        time_budget_hours=travel_information["Travel_Time"],
        trip_start_time_hours=travel_information["trip_start_time"],
        visiting_day=travel_information["Travel_day"]
    )
    
    # 2. Initialize the Solver (The Ants)
    # Using the recommended defaults from the Cheat Sheet
    solver = AntColonySystem(
        environment=env,
        num_ants=30,
        generations=100,
        alpha=1.0,
        beta=1.0,
        rho=0.1
    )
    
    # 3. Track Time and Execute
    start_time = time.time()
    best_trip, internal_acs_score = solver.solve()
    exec_time = time.time() - start_time
    
    # 4. Extract landmarks purely for the Universal Evaluator
    # best_trip looks like: [Hotel, L1, L2, Hotel]
    # We slice [1:-1] to get just: [L1, L2]
    pure_landmarks = best_trip[1:-1]
    
    # Calculate the cross-algorithm comparative score
    comparative_score = evaluate_comparative_score(
        state=pure_landmarks, 
        hotel=travel_information["hotel"], 
        time_matrix=travel_information["time_matrix"]
    )


    total_minutes_spent = 0
    for i in range(len(best_trip) - 1):
        current_node = best_trip[i]
        next_node = best_trip[i+1]
        
        # Add travel time
        total_minutes_spent += travel_information["time_matrix"][current_node.name][next_node.name]
        
        # Add visit duration (Hotels don't have visit_duration, only Landmarks do)
        if hasattr(next_node, 'visit_duration'):
            total_minutes_spent += next_node.visit_duration
            
    total_hours_spent = total_minutes_spent / 60.0
    
    # 5. Print the Final Report
    print("\n" + "="*50)
    print("🏆 FINAL RESULTS 🏆")
    print("="*50)
    print(f"Total Execution Time  : {exec_time:.4f} seconds")
    print(f"ACS Internal Score    : {internal_acs_score:.2f} (Sum of ratings)")
    print(f"COMPARATIVE EVAL SCORE: {comparative_score:.2f} (Lower is better)")
    print(f"Total Time Spent      : {total_hours_spent:.2f} hours (Budget: {travel_information['Travel_Time']} hrs)")
    print(f"Total Places Visited  : {len(pure_landmarks)}")
    print("\nOptimal Route:")
    for i, place in enumerate(pure_landmarks):
        print(f" {i+1}. {place.name}")
    print("="*50)

if __name__ == "__main__":
    run_basic_acs_test()