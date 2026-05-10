import sys, os, time, random, itertools
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Add project root to path
_BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_BASE_DIR))

from Algorithms.ACS import AntColonySystem
from core.Problem_AntColony import ACSEnvironment
from core.Node_Classes import Landmark
from utils.data_loader import get_landmarks, get_hotels, get_time_matrix

ALGO_NAME = "Hybrid-ACS-SA"
RESULTS_DIR = _BASE_DIR / f"{ALGO_NAME}-results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Unified Score Function
def calculate_unified_score(path, time_matrix):
    if not path: return 0
    total_rating = sum(node.interest_score for node in path if isinstance(node, Landmark))
    total_travel_time = sum(time_matrix[path[i].name][path[i+1].name] for i in range(len(path) - 1))
    return (7 * total_rating) - total_travel_time

def run_hybrid_parameter_study():
    landmarks = get_landmarks()
    hotels = get_hotels()
    time_matrix = get_time_matrix()
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


    selected_hotel = random.choice(hotels)
    visiting_day = random.choice(days)

    print(f"--- Starting {ALGO_NAME} Parameter & Scaling Study ---")
    print(f"Environment Fixed to: Hotel {selected_hotel.name}, Day {visiting_day}")
    print("NOTE: Using best predefined Alpha(0.5), Beta(3.0), Rho(0.3). SA logic is embedded.")

    # Parameter Ranges: Focusing heavily on the scaling of Ants and Generations
    num_ants_list = [30, 40, 50]
    generations_list = [80, 100, 120]
    
    # We will lock the best standard ACS variables found previously
    best_alpha, best_beta, best_rho = 0.5, 3.0, 0.3
    
    param_results = []
    
    # Variables to track the absolute best path across ALL runs
    overall_best_score = -float('inf')
    overall_best_path_names = []
    
    print("\nExecuting Hybrid Scaling Grid Search (This will take some time)...")
    
    total_combinations = len(num_ants_list) * len(generations_list)
    current_iteration = 0

    for ants, gens in itertools.product(num_ants_list, generations_list):
        current_iteration += 1
        scores, times, visits = [], [], []
        
        # Run 3 times to smooth out the stochastic randomness of both algorithms
        for run_id in range(3):
            # Create a fresh environment
            env = ACSEnvironment(
                hotel=selected_hotel, 
                landmarks=landmarks, 
                time_matrix=time_matrix, 
                time_budget_hours=8.0, 
                trip_start_time_hours=9.0, 
                visiting_day=visiting_day
            )
            
            # Initialize with hybrid_sa=True
            acs_hybrid = AntColonySystem(
                env, 
                num_ants=ants, 
                generations=gens, 
                alpha=best_alpha, 
                beta=best_beta, 
                rho=best_rho, 
                hybrid_sa=True
            )
            
            start_t = time.time()
            best_path, _ = acs_hybrid.solve() 
            exec_time = time.time() - start_t
            
            # Calculate metrics
            score = calculate_unified_score(best_path, time_matrix)
            num_landmarks_visited = len([node for node in best_path if isinstance(node, Landmark)])
            
            scores.append(score)
            times.append(exec_time)
            visits.append(num_landmarks_visited)
            
            # Check if this is the best path seen overall
            if score > overall_best_score:
                overall_best_score = score
                overall_best_path_names = [node.name for node in best_path]
            
        avg_score = sum(scores) / 3
        avg_time = sum(times) / 3
        avg_visited = sum(visits) / 3
        
        param_results.append({
            "Ants": ants, 
            "Generations": gens,
            "Avg_Score": avg_score, 
            "Avg_Time_Sec": avg_time,
            "Avg_Visited": avg_visited
        })
        
        # Exact runtime and visited count logging dynamically printed
        print(f"[{current_iteration}/{total_combinations}] Ants={ants:<2} | Gens={gens:<3} --> Score: {avg_score:>6.2f} | Time: {avg_time:>6.2f}s | Visited: {avg_visited:>4.1f}")

    # Save CSV
    df_params = pd.DataFrame(param_results)
    df_params.to_csv(RESULTS_DIR / f"{ALGO_NAME}_Scaling_Study.csv", index=False)

    print("\nGenerating Plots...")

    # ---------------------------------------------------------
    # PLOT 1: Heatmap - Ants vs Generations (EVALUATION SCORE)
    # ---------------------------------------------------------
    pivot_score = df_params.pivot_table(index="Ants", columns="Generations", values="Avg_Score", aggfunc='mean')
    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot_score, annot=True, cmap="magma", fmt=".1f")
    plt.title(f"{ALGO_NAME}: Evaluation Score (Ants vs Generations)")
    plt.ylabel("Number of Ants")
    plt.xlabel("Number of Generations")
    plt.savefig(RESULTS_DIR / f"{ALGO_NAME}_Heatmap_Evaluation.png")
    plt.close()

    # ---------------------------------------------------------
    # PLOT 2: Heatmap - Ants vs Generations (TOTAL RUNTIME)
    # ---------------------------------------------------------
    pivot_time = df_params.pivot_table(index="Ants", columns="Generations", values="Avg_Time_Sec", aggfunc='mean')
    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot_time, annot=True, cmap="OrRd", fmt=".2f")
    plt.title(f"{ALGO_NAME}: Runtime in Seconds (Ants vs Generations)")
    plt.ylabel("Number of Ants")
    plt.xlabel("Number of Generations")
    plt.savefig(RESULTS_DIR / f"{ALGO_NAME}_Heatmap_Runtime.png")
    plt.close()

    # ---------------------------------------------------------
    # PLOT 3: Line Plot - Performance Scaling vs Runtime Penalty
    # ---------------------------------------------------------
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Configuration Setup (Ants x Gens)')
    ax1.set_ylabel('Evaluation Score', color=color)
    
    df_params['Config'] = df_params['Ants'].astype(str) + "x" + df_params['Generations'].astype(str)
    
    sns.lineplot(data=df_params, x='Config', y='Avg_Score', marker='D', color=color, ax=ax1, label='Score')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  
    color = 'tab:red'
    ax2.set_ylabel('Execution Time (sec)', color=color)  
    sns.lineplot(data=df_params, x='Config', y='Avg_Time_Sec', marker='o', color=color, ax=ax2, label='Time')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(f"{ALGO_NAME}: Evaluation Score vs Runtime Cost")
    fig.tight_layout()  
    plt.savefig(RESULTS_DIR / f"{ALGO_NAME}_DualAxis_Score_vs_Time.png")
    plt.close()

    # ---------------------------------------------------------
    # PLOT 4: Heatmap - Ants vs Generations (LANDMARKS VISITED)
    # ---------------------------------------------------------
    pivot_visited = df_params.pivot_table(index="Ants", columns="Generations", values="Avg_Visited", aggfunc='mean')
    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot_visited, annot=True, cmap="crest", fmt=".1f")  # Using a distinct green/blue color map
    plt.title(f"{ALGO_NAME}: Avg Landmarks Visited (Ants vs Generations)")
    plt.ylabel("Number of Ants")
    plt.xlabel("Number of Generations")
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
    run_hybrid_parameter_study()