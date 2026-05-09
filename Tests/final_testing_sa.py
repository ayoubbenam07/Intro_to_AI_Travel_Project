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

from Algorithms.Simulated_Anealing import Simulated_Annealing
from core.Problem_LocalSearch import TravelProblem_LocalSearch
from core.Node_Classes import Landmark, Hotel

# ==========================================
# 1. SETUP AND CONFIGURATION
# ==========================================
RESULTS_DIR = os.path.join(project_root, "Tests", "final_testing", "SA")
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
        headers = reader.fieldnames
        print(f"Landmark Headers: {headers}")
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
        headers = reader.fieldnames
        print(f"Hotel Headers: {headers}")
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

print("Loading data (no pandas)...")
landmarks, hotels, time_matrix = load_data_no_pandas()
days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

# Fixed travel info for consistency across tests
travel_information = {
    "hotel": random.choice(hotels),
    "Travel_day": "sat", # Busy day to test opening hours
    "Travel_Time": 12,    # 12 hours budget
    "type_filter": None,
    "time_matrix": time_matrix,
    "trip_start_time": 8
}

print(f"Hotel: {travel_information['hotel'].name}")
print(f"Travel Day: {travel_information['Travel_day']}")
print(f"Time Budget: {travel_information['Travel_Time']} hours")

# ==========================================
# 2. ANALYSIS FUNCTIONS
# ==========================================
def plot_sa_results(results):
    print("Saving summary to CSV...")
    import csv
    summary_path = os.path.join(RESULTS_DIR, "sa_testing_summary.csv")
    with open(summary_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"Results saved to: {summary_path}")

# ==========================================
# 3. TEST RUNNER
# ==========================================
def run_comprehensive_tests():
    # Grid search parameters - reduced for quick testing/memory safety
    initial_temps = [100.0, 500.0]
    cooling_rates = [0.98, 0.995]
    min_temps = [0.01]
    runs_per_config = 3
    
    results = []
    configs = []
    for t in initial_temps:
        for cr in cooling_rates:
            for mt in min_temps:
                configs.append((t, cr, mt))
    
    total_runs = len(configs) * runs_per_config
    print(f"\nStarting {total_runs} test runs...", flush=True)
    
    start_total = time.time()
    
    for i, (temp, cr, mt) in enumerate(configs):
        for run_id in range(runs_per_config):
            problem = TravelProblem_LocalSearch(landmarks, travel_information)
            sa = Simulated_Annealing(problem, initial_temp=temp, cooling_rate=cr, min_temp=mt)
            
            start_time = time.time()
            best_state = sa.run()
            duration = time.time() - start_time
            
            score = sa.calculate_fitness(best_state)
            num_places = len(best_state)
            
            results.append({
                "Initial_Temp": temp,
                "Cooling_Rate": cr,
                "Min_Temp": mt,
                "Run_ID": run_id,
                "Score": score,
                "Time_Sec": duration,
                "Visited_Places": num_places
            })
            
        print(f"Completed config {i+1}/{len(configs)}: T={temp}, CR={cr}, MT={mt}", flush=True)

    # df = pd.DataFrame(results)
    # df.to_csv(os.path.join(RESULTS_DIR, "raw_testing_data.csv"), index=False)
    
    print(f"\nAll tests completed in {time.time() - start_total:.2f} seconds.")
    print("Saving analysis data...")
    plot_sa_results(results)
    print(f"Results saved to: {RESULTS_DIR}")

if __name__ == "__main__":
    run_comprehensive_tests()
