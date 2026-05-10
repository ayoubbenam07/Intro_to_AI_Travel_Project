import sys
import os
import random
import time
import csv
import json
from pathlib import Path

# Setup paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from core.Problem_AntColony import ACSEnvironment
from Algorithms.ACS import AntColonySystem
from core.Node_Classes import Landmark, Hotel

# ==========================================
# 1. SETUP AND CONFIGURATION
# ==========================================
RESULTS_DIR = os.path.join(project_root, "Tests", "final_testing", "ACS_Hybrid")
os.makedirs(RESULTS_DIR, exist_ok=True)

def load_data_no_pandas():
    base_dir = Path(project_root)
    landmarks_path = base_dir / "dataset" / "landmarks" / "Algiers_Landmarks.csv"
    hotels_path = base_dir / "dataset" / "hotels" / "Algiers_hotels.csv"
    time_matrix_path = base_dir / "utils" / "time_matrix.json"

    # Landmarks
    landmarks = []
    with open(landmarks_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            landmarks.append(Landmark(
                id=int(row['ID']),
                name=row['Name'],
                lon=float(row['Longitude']),
                lat=float(row['Latitude']),
                landmark_type=row['Type'],
                opening_hours=json.loads(row['Hours'].replace("'", '"')),
                visit_duration=float(row['EstimatedTime (min)']),
                interest_score=float(row['Rating'])
            ))
    
    # Hotels
    hotels = []
    with open(hotels_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            hotels.append(Hotel(
                name=row['name'],
                lon=float(row['longitude']),
                lat=float(row['latitude'])
            ))

    # Time Matrix
    with open(time_matrix_path, 'r', encoding='utf-8') as f:
        time_matrix = json.load(f)

    return landmarks, hotels, time_matrix

# Comparative score calculation (Same as in ACS_Test.py)
def evaluate_comparative_score(state, hotel, time_matrix):
    if not state: return 0.0
    total_rating = 0
    total_travel_time = 0 
    landmarks_only = [node for node in state if isinstance(node, Landmark)]
    if not landmarks_only: return 0.0
    
    for i, landmark in enumerate(landmarks_only):
        total_rating += landmark.interest_score
        if i == 0:
            total_travel_time += time_matrix[hotel.name][landmark.name]
        else:
            total_travel_time += time_matrix[landmarks_only[i-1].name][landmark.name]
    total_travel_time += time_matrix[landmarks_only[-1].name][hotel.name]
    return total_travel_time - (20 * total_rating)

print("Loading data...")
landmarks, hotels, time_matrix = load_data_no_pandas()

# Fixed travel info for consistency
travel_information = {
    "hotel": random.choice(hotels),
    "Travel_day": "sat",
    "Travel_Time": 12,
    "trip_start_time": 8
}

print(f"Testing ACS-Hybrid from Hotel: {travel_information['hotel'].name}")

# Parameters to sweep
num_ants_options = [10, 30]
generations_options = [50, 100]

results_file = os.path.join(RESULTS_DIR, "acs_hybrid_summary.csv")

with open(results_file, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Num_Ants", "Generations", "Run_ID", "Score", "Time_Sec", "Visited_Places"])

    for num_ants in num_ants_options:
        for gens in generations_options:
            for run_id in range(3):  # 3 runs each for stability
                print(f"Running: Ants={num_ants}, Gens={gens}, Run={run_id}")
                
                env = ACSEnvironment(
                    landmarks=landmarks,
                    hotel=travel_information['hotel'],
                    time_matrix=time_matrix,
                    visiting_day=travel_information['Travel_day'],
                    time_budget_hours=travel_information['Travel_Time'],
                    trip_start_time_hours=travel_information['trip_start_time']
                )
                
                start_time = time.time()
                acs = AntColonySystem(
                    environment=env,
                    num_ants=num_ants,
                    generations=gens,
                    hybrid_sa=True  # ENABLE HYBRID
                )
                
                best_path, _ = acs.solve()
                end_time = time.time()
                
                landmarks_visited = [node for node in best_path if isinstance(node, Landmark)]
                comp_score = evaluate_comparative_score(best_path, travel_information['hotel'], time_matrix)
                
                writer.writerow([num_ants, gens, run_id, comp_score, end_time - start_time, len(landmarks_visited)])
                f.flush()

print(f"Testing complete. Results saved to {results_file}")
