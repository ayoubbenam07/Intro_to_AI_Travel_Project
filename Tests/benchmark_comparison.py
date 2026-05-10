import sys
import os
from pathlib import Path

# Add project root to sys.path
_BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE_DIR))

import time
import matplotlib.pyplot as plt
from core.Node_Classes import Landmark, Hotel
from core.Problem_LocalSearch import TravelProblem_LocalSearch
from core.Problem_AntColony import ACSEnvironment
from Algorithms.Simulated_Anealing import Simulated_Annealing
from Algorithms.ACS import AntColonySystem
from utils.data_loader import get_landmarks, get_hotels, get_time_matrix

def run_benchmarks():
    # 1. Setup Data
    landmarks = get_landmarks()
    hotels = get_hotels()
    time_matrix = get_time_matrix()
    
    # Select a hotel and setup problem parameters
    selected_hotel = hotels[0]
    travel_info = {
        'hotel': selected_hotel,
        'Travel_day': 'mon',
        'Travel_Time': 8.0, # 8 hours
        'Landmarks_number': 5,
        'type_filter': [],
        'time_matrix': time_matrix,
        'trip_start_time': 9 # 9 AM
    }
    
    # Problem for SA
    problem_sa = TravelProblem_LocalSearch(landmarks, travel_info)
    
    # Environment for ACS
    env = ACSEnvironment(
        hotel=selected_hotel,
        landmarks=landmarks,
        time_matrix=time_matrix,
        time_budget_hours=8.0,
        trip_start_time_hours=9.0,
        visiting_day='mon'
    )
    # Add travel_info and all_landmarks to env for Hybrid support
    env.travel_info = travel_info
    env.all_landmarks = landmarks

    results = []

    # 2. Test Simulated Annealing
    print("Running Simulated Annealing...")
    start_time = time.time()
    # Fast SA configuration
    sa = Simulated_Annealing(problem_sa, initial_temp=50.0, cooling_rate=0.9, max_reheats=0)
    best_sa_path = sa.run()
    sa_time = time.time() - start_time
    sa_score = sum(lm.interest_score for lm in best_sa_path)
    results.append(('SA (Fast)', sa_score, sa_time))

    # 3. Test Pure ACS
    print("Running Pure ACS...")
    start_time = time.time()
    # Reduced population and generations for speed
    acs_pure = AntColonySystem(env, num_ants=5, generations=5, hybrid_sa=False)
    best_acs_path, acs_score = acs_pure.solve()
    acs_time = time.time() - start_time
    results.append(('Pure ACS', acs_score, acs_time))

    # 4. Test Hybrid ACS-SA
    print("Running Hybrid ACS-SA...")
    start_time = time.time()
    # Reduced population and generations for speed
    acs_hybrid = AntColonySystem(env, num_ants=5, generations=5, hybrid_sa=True)
    best_hybrid_path, hybrid_score = acs_hybrid.solve()
    hybrid_time = time.time() - start_time
    results.append(('Hybrid ACS-SA', hybrid_score, hybrid_time))

    # 5. Plotting and Saving Results
    names = [r[0] for r in results]
    scores = [r[1] for r in results]
    times = [r[2] for r in results]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Algorithm')
    ax1.set_ylabel('Total Interest Score', color=color)
    bars = ax1.bar(names, scores, color=color, alpha=0.6, label='Score')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Execution Time (s)', color=color)
    ax2.plot(names, times, color=color, marker='o', linewidth=2, label='Time')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Comparison of AI Algorithms for Algiers Travel Guide')
    fig.tight_layout()
    
    save_path = _BASE_DIR / "Tests" / "Comparison_Results.png"
    plt.savefig(save_path)
    print(f"Plot saved to {save_path}")

    # Save summary text
    with open(_BASE_DIR / "Tests" / "benchmark_summary.txt", "w") as f:
        f.write("Algorithm Comparison Summary\n")
        f.write("============================\n")
        for name, score, t in results:
            f.write(f"{name}: Score = {score:.2f}, Time = {t:.4f}s\n")

if __name__ == "__main__":
    run_benchmarks()
