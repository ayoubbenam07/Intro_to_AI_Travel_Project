import sys
import os
import random
import time
import tracemalloc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import concurrent.futures

# Setup paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from Algorithms.Simulated_Anealing import Simulated_Annealing
from core.Problem_LocalSearch import TravelProblem_LocalSearch
from utils import data_loader

# ==========================================
# 1. LOAD DATA ONCE (Shared Memory)
# ==========================================
print("Loading data into shared memory...")
landmarks = data_loader.get_landmarks()
hotels = data_loader.get_hotels()
time_matrix = data_loader.get_time_matrix()
days = ["mon","tue", "wed" ,"thu","fri","sat","sun"]

travel_information = {
    "hotel": random.choice(hotels),
    "Travel_day": random.choice(days), 
    "Travel_Time": 10,
    "type_filter": None,                    
    "time_matrix": time_matrix,
    "trip_start_time": 8
}

# ==========================================
# 2. THE WORKER FUNCTION (Runs on 1 Core)
# ==========================================
def run_single_config(config):
    """
    Tests one specific combination of parameters.
    """
    temp, cr, min_t, runs_per_config = config
    scores, times, memories = [], [], []
    
    for _ in range(runs_per_config):
        problem = TravelProblem_LocalSearch(landmarks, travel_information)
        sa = Simulated_Annealing(problem, initial_temp=temp, cooling_rate=cr, min_temp=min_t)
        
        tracemalloc.start()
        start_time = time.time()
        
        best_state = sa.run()
        score = sa.calculate_fitness(best_state)
        
        exec_time = time.time() - start_time
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        scores.append(score)
        times.append(exec_time)
        memories.append(peak_mem / 1024) # KB

    return {
        "Initial_Temp": temp,
        "Cooling_Rate": cr,
        "Min_Temp": min_t,
        "Avg_Score": sum(scores) / len(scores),
        "Avg_Time_Sec": sum(times) / len(times),
        "Avg_Memory_KB": sum(memories) / len(memories)
    }

# ==========================================
# 3. THE PLOTTING FUNCTION
# ==========================================
def plot_comprehensive_results(df):
    """Generates and saves multiple analytical plots."""
    sns.set_theme(style="whitegrid")
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_folder = os.path.join(script_dir, "SA-test-results")
    
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    # PLOT 1: Fitness Score Matrix
    plt.figure(figsize=(10, 8))
    score_pivot = df.groupby(["Initial_Temp", "Cooling_Rate"])["Avg_Score"].mean().unstack()
    sns.heatmap(score_pivot, annot=True, fmt=".1f", cmap="YlGnBu_r")
    plt.title("Average Final Score (Lower is Better)")
    plt.savefig(os.path.join(results_folder, "1_Fitness_Score_Heatmap.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # PLOT 2: Time Complexity
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="Cooling_Rate", y="Avg_Time_Sec", hue="Min_Temp", marker="o", palette="viridis")
    plt.title("Execution Time Impact: Cooling Rate vs Min Temp")
    plt.ylabel("Execution Time (Seconds)")
    plt.yscale("log") # Log scale for exponential growth
    plt.savefig(os.path.join(results_folder, "2_Time_Complexity.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # PLOT 3: Space Complexity
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="Cooling_Rate", y="Avg_Memory_KB", hue="Initial_Temp", palette="Set2")
    plt.title("Peak Memory Usage (Space Complexity)")
    plt.ylabel("Memory (KB)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title="Initial Temp")
    plt.savefig(os.path.join(results_folder, "3_Space_Complexity.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # PLOT 4: Min Temp Impact
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="Min_Temp", y="Avg_Score", palette="mako")
    plt.title("How Minimum Temperature Bounds Impact Final Score")
    plt.xlabel("Minimum Temperature (Stopping Criteria)")
    plt.ylabel("Distribution of Scores (Lower is Better)")
    plt.savefig(os.path.join(results_folder, "4_Min_Temp_Impact.png"), dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\nSUCCESS! 4 Comprehensive Plots have been saved to the '{results_folder}' folder.")

# ==========================================
# 4. THE MAIN CONTROLLER
# ==========================================
def run_multiprocess_tests():
    

    initial_temps = [100.0, 500.0, 1000.0, 5000.0]
    cooling_rates = [ 0.95, 0.98, 0.99]
    min_temps = [1.0, 0.1,  0.001]
    runs_per_config = 3
   

    tasks = []
    for temp in initial_temps:
        for cr in cooling_rates:
            for min_t in min_temps:
                tasks.append((temp, cr, min_t, runs_per_config))

    print(f"Starting parallel processing for {len(tasks)} configurations...")
    start_total_time = time.time()
    
    results = []
    
    # ProcessPoolExecutor splits the tasks across your CPU cores
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for result in executor.map(run_single_config, tasks):
            results.append(result)
            if len(results) % 2 == 0: 
                print(f"Progress: {len(results)}/{len(tasks)} completed...")

    print(f"All tests finished in {time.time() - start_total_time:.2f} seconds!")

    df = pd.DataFrame(results)
    plot_comprehensive_results(df)

if __name__ == "__main__":
    run_multiprocess_tests()