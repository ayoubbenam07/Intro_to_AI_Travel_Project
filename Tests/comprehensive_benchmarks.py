import sys
import os
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Setup paths
_BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE_DIR))

from Algorithms.Simulated_Anealing import Simulated_Annealing
from Algorithms.ACS import AntColonySystem
from core.Problem_LocalSearch import TravelProblem_LocalSearch
from core.Problem_AntColony import ACSEnvironment
from core.Node_Classes import Landmark
from utils import data_loader

def setup_results_folder(algo_name):
    # Updated to use "final testing" subfolder as requested
    folder = _BASE_DIR / "Tests" / f"{algo_name}-test-results" / "final testing"
    folder.mkdir(parents=True, exist_ok=True)
    return folder

def plot_analytical_results(df, results_folder, title_suffix):
    sns.set_theme(style="whitegrid")
    
    # Identify categorical/numeric params for pivoting
    cols = df.columns
    pivot_cols = [c for c in cols if c not in ["Score", "Time_Sec", "Visited_Places", "Run_ID"]]
    
    if len(pivot_cols) >= 2:
        # PLOT 1: Score vs Params (Heatmap)
        plt.figure(figsize=(10, 8))
        score_pivot = df.groupby([pivot_cols[0], pivot_cols[1]])["Score"].mean().unstack()
        sns.heatmap(score_pivot, annot=True, fmt=".1f", cmap="YlGnBu")
        plt.title(f"Score Distribution: {title_suffix}")
        plt.savefig(results_folder / "1_Score_Heatmap.png", dpi=100) # Lower DPI to save memory
        plt.close('all')

        # PLOT 2: Time vs Params
        plt.figure(figsize=(10, 8))
        time_pivot = df.groupby([pivot_cols[0], pivot_cols[1]])["Time_Sec"].mean().unstack()
        sns.heatmap(time_pivot, annot=True, fmt=".3f", cmap="Reds")
        plt.title(f"Execution Time: {title_suffix}")
        plt.savefig(results_folder / "2_Time_Heatmap.png", dpi=100)
        plt.close('all')

    # Minimal logic for other plots to avoid memory spikes
    plt.close('all')

def run_sa_tests(landmarks, travel_info):
    print("\n[SA] Running parameter sweep (Final Testing)...")
    folder = setup_results_folder("SA")
    results = []
    
    # 4x4 Grid for stability
    temps = [50.0, 100.0, 500.0, 1000.0]
    rates = [0.9, 0.95, 0.98, 0.99]
    
    for t in temps:
        for r in rates:
            prob = TravelProblem_LocalSearch(landmarks, travel_info)
            sa = Simulated_Annealing(prob, initial_temp=t, cooling_rate=r, max_reheats=1)
            start = time.time()
            path = sa.run()
            dur = time.time() - start
            score = sum(lm.interest_score for lm in path)
            results.append({
                "Temp": t,
                "CoolRate": r,
                "Score": score,
                "Time_Sec": dur,
                "Visited_Places": len(path),
                "Run_ID": 0
            })
    df = pd.DataFrame(results)
    plot_analytical_results(df, folder, "Simulated Annealing")
    print(f"SA Results saved to {folder}")

def run_acs_tests(landmarks, hotel, time_matrix, hybrid=False):
    algo_name = "ACS-Hybrid" if hybrid else "ACS-Pure"
    print(f"\n[{algo_name}] Running parameter sweep (Final Testing)...")
    folder = setup_results_folder(algo_name)
    results = []
    
    # 3x3 Grid for ACS instability/memory management
    ants = [5, 10, 20]
    gens = [5, 10, 20]
    
    travel_info = {
        'hotel': hotel,
        'Travel_day': 'mon',
        'Travel_Time': 8.0,
        'Landmarks_number': 5,
        'type_filter': [],
        'time_matrix': time_matrix,
        'trip_start_time': 9
    }

    for a in ants:
        for g in gens:
            env = ACSEnvironment(hotel, landmarks, time_matrix, 8.0, 9.0, 'mon')
            env.travel_info = travel_info
            env.all_landmarks = landmarks
            
            acs = AntColonySystem(env, num_ants=a, generations=g, hybrid_sa=hybrid)
            start = time.time()
            path, score = acs.solve()
            dur = time.time() - start
            results.append({
                "Ants": a,
                "Gens": g,
                "Score": score,
                "Time_Sec": dur,
                "Visited_Places": len([n for n in path if isinstance(n, Landmark)]),
                "Run_ID": 0
            })
            # Explicit clear between runs
            del acs
            del env
    df = pd.DataFrame(results)
    plot_analytical_results(df, folder, algo_name)
    print(f"{algo_name} Results saved to {folder}")

if __name__ == "__main__":
    landmarks = data_loader.get_landmarks()
    hotels = data_loader.get_hotels()
    time_matrix = data_loader.get_time_matrix()
    selected_hotel = hotels[0]
    
    travel_info = {
        'hotel': selected_hotel,
        'Travel_day': 'mon',
        'Travel_Time': 8.0,
        'Landmarks_number': 5,
        'type_filter': [],
        'time_matrix': time_matrix,
        'trip_start_time': 9
    }

    # Focus ONLY on SA first to ensure memory stability and multi-square output
    run_sa_tests(landmarks, travel_info)
    
    # run_acs_tests(landmarks, selected_hotel, time_matrix, hybrid=False)
    # run_acs_tests(landmarks, selected_hotel, time_matrix, hybrid=True)
