import sys, os, time, random, itertools
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Add project root to path
_BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_BASE_DIR))

from Algorithms.Simulated_Anealing import Simulated_Annealing
from core.Problem_LocalSearch import TravelProblem_LocalSearch
from core.Node_Classes import Landmark
from utils.data_loader import get_landmarks, get_hotels, get_time_matrix

ALGO_NAME = "SA"
RESULTS_DIR = _BASE_DIR / f"{ALGO_NAME}-results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Unified Score Function
def calculate_unified_score(path, time_matrix):
    if not path: return 0
    total_rating = sum(node.interest_score for node in path if isinstance(node, Landmark))
    total_travel_time = sum(time_matrix[path[i].name][path[i+1].name] for i in range(len(path) - 1))
    return (7 * total_rating) - total_travel_time

def run_sa_parameter_study():
    landmarks = get_landmarks()
    hotels = get_hotels()
    time_matrix = get_time_matrix()
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    
    # Force identical environment for fair comparison
    random.seed(42)
    selected_hotel = random.choice(hotels)
    visiting_day = random.choice(days)  
    
    print(f"--- Starting {ALGO_NAME} Parameter Study ---")
    print(f"Environment Fixed to: Hotel {selected_hotel.name}, Day {visiting_day}")

    # Adjusted parameters to prevent infinite loops / hours of execution
    initial_temps = [50, 100, 300]
    cooling_rates = [0.95, 0.97, 0.99]
    max_reheats = [1, 2]
    
    param_results = []
    
    # Variables to track the absolute best path across ALL runs
    overall_best_score = -float('inf')
    overall_best_path_names = []
    
    travel_info = {
        'hotel': selected_hotel, 'Travel_day': visiting_day, 'Travel_Time': 8.0, 
        'type_filter': [], 'time_matrix': time_matrix, 'trip_start_time': 9
    }
    problem = TravelProblem_LocalSearch(landmarks, travel_info)

    print("\nExecuting Parameter Grid Search (This will take some time)...")
    
    total_combinations = len(initial_temps) * len(cooling_rates) * len(max_reheats)
    current_iteration = 0

    for temp, cool, reheat in itertools.product(initial_temps, cooling_rates, max_reheats):
        current_iteration += 1
        scores, times, visits = [], [], []
        
        # Run each configuration 3 times for stability
        for run_id in range(3):
            sa = Simulated_Annealing(problem, initial_temp=temp, cooling_rate=cool, max_reheats=reheat)
            
            start_time = time.time()
            best_state = sa.run()
            exec_time = time.time() - start_time
            
            # Format path and calculate score
            full_path = [selected_hotel] + best_state + [selected_hotel]
            score = calculate_unified_score(full_path, time_matrix)
            num_landmarks_visited = len(best_state)  # best_state only contains landmarks
            
            scores.append(score)
            times.append(exec_time)
            visits.append(num_landmarks_visited)
            
            # Check if this is the best path seen overall
            if score > overall_best_score:
                overall_best_score = score
                overall_best_path_names = [node.name for node in full_path]
            
        avg_score = sum(scores) / 3
        avg_time = sum(times) / 3
        avg_visited = sum(visits) / 3
        
        # Save to list
        param_results.append({
            "Init_Temp": temp, 
            "Cooling_Rate": cool, 
            "Max_Reheats": reheat,
            "Avg_Score": avg_score, 
            "Avg_Time_Sec": avg_time,
            "Avg_Visited": avg_visited
        })
        
        # Print runtime exactly as requested
        print(f"[{current_iteration}/{total_combinations}] Temp: {temp:<4} | Cool: {cool:<4} | Reheats: {reheat} --> Score: {avg_score:>6.2f} | Time: {avg_time:>6.2f}s | Visited: {avg_visited:>4.1f}")

    # Convert to DataFrame and Save CSV
    df_params = pd.DataFrame(param_results)
    df_params.to_csv(RESULTS_DIR / f"{ALGO_NAME}_Parameter_Study.csv", index=False)

    print("\nGenerating Plots...")

    # ---------------------------------------------------------
    # PLOT 1: Heatmap - Temp vs Cooling Rate (EVALUATION SCORE)
    # ---------------------------------------------------------
    # Averages out the "Reheats" so we strictly see Temp vs Cool
    pivot_score = df_params.pivot_table(index="Init_Temp", columns="Cooling_Rate", values="Avg_Score", aggfunc='mean')
    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot_score, annot=True, cmap="YlGnBu", fmt=".1f")
    plt.title(f"{ALGO_NAME}: Evaluation Score (Temp vs Cooling Rate)")
    plt.ylabel("Initial Temperature")
    plt.xlabel("Cooling Rate")
    plt.savefig(RESULTS_DIR / f"{ALGO_NAME}_Heatmap_Evaluation.png")
    plt.close()

    # ---------------------------------------------------------
    # PLOT 2: Heatmap - Temp vs Cooling Rate (TOTAL RUNTIME)
    # ---------------------------------------------------------
    pivot_time = df_params.pivot_table(index="Init_Temp", columns="Cooling_Rate", values="Avg_Time_Sec", aggfunc='mean')
    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot_time, annot=True, cmap="OrRd", fmt=".2f")
    plt.title(f"{ALGO_NAME}: Runtime in Seconds (Temp vs Cooling Rate)")
    plt.ylabel("Initial Temperature")
    plt.xlabel("Cooling Rate")
    plt.savefig(RESULTS_DIR / f"{ALGO_NAME}_Heatmap_Runtime.png")
    plt.close()

    # ---------------------------------------------------------
    # PLOT 3: Line Plot - Max Reheats vs Evaluation Score
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_params, x="Max_Reheats", y="Avg_Score", hue="Cooling_Rate", marker="o", palette="Set2")
    plt.title(f"{ALGO_NAME}: Impact of Reheats on Evaluation Score")
    plt.ylabel("Evaluation Score")
    plt.xlabel("Number of Reheats")
    plt.xticks(max_reheats) # Dynamically adapts to [1, 2]
    plt.savefig(RESULTS_DIR / f"{ALGO_NAME}_Line_Reheats_vs_Score.png")
    plt.close()

    # ---------------------------------------------------------
    # PLOT 4: Heatmap - Temp vs Cooling Rate (LANDMARKS VISITED)
    # ---------------------------------------------------------
    pivot_visited = df_params.pivot_table(index="Init_Temp", columns="Cooling_Rate", values="Avg_Visited", aggfunc='mean')
    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot_visited, annot=True, cmap="crest", fmt=".1f")
    plt.title(f"{ALGO_NAME}: Avg Landmarks Visited (Temp vs Cooling Rate)")
    plt.ylabel("Initial Temperature")
    plt.xlabel("Cooling Rate")
    plt.savefig(RESULTS_DIR / f"{ALGO_NAME}_Heatmap_Visited.png")
    plt.close()

    # Print the overall best path summary
    print("\n" + "="*60)
    print("🏆 OVERALL BEST ROUTE FOUND 🏆")
    print("="*60)
    print(f"Best Unified Score: {overall_best_score:.2f}")
    print(f"Total Places Visited: {len(overall_best_path_names) - 2} (excluding start/end hotel)")
    print("-" * 60)
    
    # Format the path nicely
    formatted_path = "\n  -> ".join(overall_best_path_names)
    print(f"Full Path:\n  {formatted_path}")
    print("="*60)

    print(f"\nDone! Check the '{ALGO_NAME}-results' folder for the CSV and charts.")

if __name__ == "__main__":
    run_sa_parameter_study()