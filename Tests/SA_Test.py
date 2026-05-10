import sys
import os
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setup paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from Algorithms.Simulated_Anealing import Simulated_Annealing
from core.Problem_LocalSearch import TravelProblem_LocalSearch
from utils import data_loader

# ==========================================
# 1. LOAD DATA ONCE
# ==========================================
print("Loading data...")
landmarks = data_loader.get_landmarks()
hotels = data_loader.get_hotels()
time_matrix = data_loader.get_time_matrix()
days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

travel_information = {
    "hotel": random.choice(hotels),
    "Travel_day": random.choice(days), 
    "Travel_Time": 10,
    "type_filter": None,                    
    "time_matrix": time_matrix,
    "trip_start_time": 8
}

print(f"hotel : {travel_information['hotel'].name}")
print(f"travel day : {travel_information['Travel_day']}")
# ==========================================
# 2. THE PLOTTING FUNCTION (Upgraded with Extra Heatmaps & Polygons)
# ==========================================
def plot_comprehensive_results(df):
    """Generates and saves analytical plots covering all parameter relationships."""
    sns.set_theme(style="whitegrid")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_folder = os.path.join(script_dir, "SA-test-results")
    
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    # PLOT 1: Score Heatmap (Initial Temp vs Cooling Rate)
    plt.figure(figsize=(10, 8))
    score_pivot = df.groupby(["Initial_Temp", "Cooling_Rate"])["Score"].mean().unstack()
    sns.heatmap(score_pivot, annot=True, fmt=".1f", cmap="YlGnBu_r")
    plt.title("Parameter Relation: Impact on FINAL SCORE (Lower = Better)")
    plt.savefig(os.path.join(results_folder, "1_Score_Heatmap.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # PLOT 2: Time Heatmap (Initial Temp vs Cooling Rate)
    plt.figure(figsize=(10, 8))
    time_pivot = df.groupby(["Initial_Temp", "Cooling_Rate"])["Time_Sec"].mean().unstack()
    sns.heatmap(time_pivot, annot=True, fmt=".3f", cmap="Reds")
    plt.title("Parameter Relation: Impact on EXECUTION TIME (Seconds)")
    plt.savefig(os.path.join(results_folder, "2_Time_Heatmap.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # PLOT 3: Visited Places Heatmap (Initial Temp vs Cooling Rate) -- NEW
    plt.figure(figsize=(10, 8))
    places_pivot = df.groupby(["Initial_Temp", "Cooling_Rate"])["Visited_Places"].mean().unstack()
    sns.heatmap(places_pivot, annot=True, fmt=".0f", cmap="Greens")
    plt.title("Parameter Relation: Average VISITED PLACES")
    plt.savefig(os.path.join(results_folder, "3_Visited_Places_Heatmap.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # PLOT 4: The Spread of Scores by Cooling Rate
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="Cooling_Rate", y="Score", hue="Initial_Temp", palette="Set2")
    plt.title("Score Consistency based on Cooling Rate & Initial Temp")
    plt.ylabel("Score (Lower is Better)")
    plt.legend(title="Initial Temp", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig(os.path.join(results_folder, "4_Cooling_Rate_Spread.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # PLOT 5: Number of Visited Places vs Score
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="Visited_Places", y="Score", hue="Cooling_Rate", size="Initial_Temp", sizes=(50, 200), palette="deep", alpha=0.7)
    plt.title("How Number of Places Relates to Score & Parameters")
    plt.savefig(os.path.join(results_folder, "5_Places_vs_Score.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # PLOT 6: Execution Time vs Number of Visited Places
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="Visited_Places", y="Time_Sec", hue="Min_Temp", size="Cooling_Rate", sizes=(50, 200), palette="Set1", alpha=0.8)
    plt.title("How Number of Places Relates to Execution Time")
    plt.savefig(os.path.join(results_folder, "6_Places_vs_Time.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # PLOT 7: Polygon Hexbin Density (Time vs Score) -- NEW
    hexplot = sns.jointplot(data=df, x="Time_Sec", y="Score", kind="hex", color="#4CB391", gridsize=15, cmap="viridis")
    hexplot.fig.suptitle("Polygon Density: Execution Time vs Final Score", y=1.02)
    plt.savefig(os.path.join(results_folder, "7_Polygon_Hexbin_Time_vs_Score.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # PLOT 8: Polygon Topography Contour (Visited Places vs Score) -- NEW
    plt.figure(figsize=(10, 8))
    sns.kdeplot(data=df, x="Visited_Places", y="Score", fill=True, cmap="mako", thresh=0, levels=10, alpha=0.8)
    sns.scatterplot(data=df, x="Visited_Places", y="Score", color="black", alpha=0.5, s=20) # Add the actual dots over the polygons
    plt.title("Polygon Topography: Where do the best scores land based on Visited Places?")
    plt.savefig(os.path.join(results_folder, "8_Polygon_Topography_Places_vs_Score.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # PLOT 9: THE ULTIMATE PAIRPLOT
    pair_plot = sns.pairplot(df, vars=['Initial_Temp', 'Cooling_Rate', 'Min_Temp', 'Score', 'Time_Sec', 'Visited_Places'], 
                             diag_kind='kde', plot_kws={'alpha': 0.6})
    pair_plot.fig.suptitle("Full Relational Matrix of All SA Variables", y=1.02)
    plt.savefig(os.path.join(results_folder, "9_Full_Relational_Pairplot.png"), dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\nSUCCESS! 9 Comprehensive Analytical Plots (including Heatmaps & Polygons) have been saved to '{results_folder}'.")

# ==========================================
# 3. THE MAIN CONTROLLER (Single Core)
# ==========================================
def run_single_core_tests():
    
    # Keeping your updated parameters
    initial_temps = [100.0, 250.0, 500.0]
    cooling_rates = [ 0.97, 0.98 , 0.99]
    min_temps = [ 0.05, 0.1]
    runs_per_config = 3  
                            
    results = []
    
    total_runs = len(initial_temps) * len(cooling_rates) * len(min_temps) * runs_per_config
    current_run = 0

    print(f"\nStarting Single-Core Tests: {total_runs} total runs planned...\n" + "="*50)
    start_total_time = time.time()
    
    for temp in initial_temps:
        for cr in cooling_rates:
            for min_t in min_temps:
                for run_id in range(runs_per_config):
                    current_run += 1
                    
                    # 1. Initialize Problem and Algorithm
                    problem = TravelProblem_LocalSearch(landmarks, travel_information)
                    sa = Simulated_Annealing(problem, initial_temp=temp, cooling_rate=cr, min_temp=min_t)
                    
                    # 2. Track Time and Run
                    start_time = time.time()
                    best_state = sa.run()
                    exec_time = time.time() - start_time
                    
                    # 3. Extract Data
                    score = sa.calculate_fitness(best_state)
                    path_names = [landmark.name for landmark in best_state]
                    num_places = len(best_state)
                    
                    # 4. Save to Results
                    results.append({
                        "Initial_Temp": temp,
                        "Cooling_Rate": cr,
                        "Min_Temp": min_t,
                        "Score": score,
                        "Time_Sec": exec_time,
                        "Visited_Places": num_places
                    })
                    
                    # 5. Print Output for Every Run
                    print(f"Run [{current_run}/{total_runs}] | Params: Temp={temp}, Cool={cr}, MinT={min_t}")
                    print(f"--> Score: {score:.2f}")
                    print(f"--> Time:  {exec_time:.4f} seconds")
                    print(f"--> Places Visited: {num_places}")
                    print(f"--> Path:  {path_names}")
                    print("-" * 50)

    print(f"\nAll tests finished in {time.time() - start_total_time:.2f} seconds!")

    # Generate plots
    df = pd.DataFrame(results)
    plot_comprehensive_results(df)

if __name__ == "__main__":
    run_single_core_tests()