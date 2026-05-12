"""
Greedy_test.py
=========================================================
Tests the Greedy Best-First Search algorithm across multiple:
  Different hotels       (All available)
  Different days         (mon-sun)
  Different time budgets (6h, 8h, 10h, 12h)
  Different start times  (8am, 9am, 10am)
"""

import sys, os, time, random
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import seaborn as sns

# ── project imports ──────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.data_loader import get_landmarks, get_hotels, get_time_matrix
from core.Problem_InformedSearch import TravelProblem_InformedSearch
from Algorithms.Greedy import greedy_search
from core.Node_Classes import Landmark

# ── data loading ─────────────────────────────────────────────────────────────
landmarks = get_landmarks()
hotels = get_hotels()
time_matrix = get_time_matrix()
# Create a landmarks dictionary for easier lookup by name
landmarks_dict = {lm.name: lm for lm in landmarks}
# ── parameters ───────────────────────────────────────────────────────────
Hotels_to_test = hotels[:min(5, len(hotels))]  # Test first 5 hotels
Days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
Time_budgets = [6.0, 8.0, 10.0, 12.0]  # hours
Start_times = [8, 9, 10]  # hours (24-hour format)

SEED = 42

# ── output directory ─────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Tests", "Greedy_test_results")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def calculate_path_metrics(path, landmarks_dict, time_matrix, problem_hotel):
    """
    Calculate metrics for a greedy path.
    Path is a list of states: (position_name, visited_set, current_time)
    
    Returns: (fitness, total_interest, total_time_hours, num_landmarks)
    """
    if not path or len(path) < 2:
        return 0, 0, 0, 0
    
    # Extract visited landmarks from the path's visited_set (the second element of the last state)
    final_state = path[-1]
    visited_names = final_state[1]  # frozenset of visited landmark names
    
    # Get the actual landmark objects
    visited_landmarks = []
    for name in visited_names:
        if name in landmarks_dict:
            visited_landmarks.append(landmarks_dict[name])
    
    if not visited_landmarks:
        return 0, 0, 0, 0
    
    total_interest = sum(lm.interest_score for lm in visited_landmarks)
    
    # Calculate total travel time between consecutive waypoints
    total_travel_time = 0
    for i in range(len(path) - 1):
        current_pos = path[i][0]  # position name from state tuple
        next_pos = path[i+1][0]
        
        if current_pos in time_matrix and next_pos in time_matrix[current_pos]:
            total_travel_time += time_matrix[current_pos][next_pos]
    
    total_time_hours = total_travel_time / 60.0  # convert minutes to hours
    num_landmarks = len(visited_landmarks)
    
    # Fitness: weighted combination of interest and efficiency
    fitness = (7 * total_interest) - total_travel_time if total_travel_time > 0 else total_interest * 7
    
    return fitness, total_interest, total_time_hours, num_landmarks

# ═════════════════════════════════════════════════════════════════════════════
# 1.  FULL COMPREHENSIVE TEST across all configurations
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PHASE 1 -- Full Comprehensive Test (Hotels × Days × Budgets × Times)")
print("=" * 70)

rows_full = []
total_configs = len(Hotels_to_test) * len(Days) * len(Time_budgets) * len(Start_times)
config_idx = 0

for hotel in Hotels_to_test:
    for day in Days:
        for budget in Time_budgets:
            for start_time in Start_times:
                config_idx += 1
                
                # Create problem instance
                problem = TravelProblem_InformedSearch(
                    hotel, landmarks, [], time_matrix,
                    time_budget=budget * 60,  # convert to minutes
                    starting_time=start_time * 60,  # convert to minutes
                    visiting_day=day
                )
                
                t0 = time.time()
                path = greedy_search(problem)
                elapsed = time.time() - t0
                
                if path:
                    fitness, interest, tot_time, n_lm = calculate_path_metrics(path, landmarks_dict, time_matrix, hotel)
                else:
                    fitness, interest, tot_time, n_lm = 0, 0, 0, 0
                
                rows_full.append({
                    'Hotel': hotel.name,
                    'Day': day,
                    'Budget_h': budget,
                    'StartTime': start_time,
                    'Fitness': round(fitness, 4),
                    'Interest': round(interest, 2),
                    'TravelTime_h': round(tot_time, 2),
                    'NumLandmarks': n_lm,
                    'Runtime_ms': round(elapsed * 1000, 2),
                })
                
                if config_idx % 10 == 0:
                    print(f"  [{config_idx:3d}/{total_configs}]  {hotel.name:20s} {day:3s} budget={budget:.0f}h start={start_time:2d}"
                          f"  ->  fit={fitness:7.2f} lm={n_lm:2d} ({elapsed*1000:.1f}ms)")

df_full = pd.DataFrame(rows_full)
csv_path = os.path.join(OUTPUT_DIR, "full_test_results.csv")
df_full.to_csv(csv_path, index=False)
print(f"\n[OK] Full test results saved -> {csv_path}")

# ═════════════════════════════════════════════════════════════════════════════
# 2.  HOTEL COMPARISON
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PHASE 2 -- Hotel Comparison (fixed day=fri, budget=8h, time=9am)")
print("=" * 70)

rows_hotel = []
for hotel in Hotels_to_test:
    problem = TravelProblem_InformedSearch(
        hotel, landmarks, [], time_matrix,
        time_budget=8 * 60,
        starting_time=9 * 60,
        visiting_day='fri'
    )
    
    t0 = time.time()
    path = greedy_search(problem)
    elapsed = time.time() - t0
    
    if path:
        fitness, interest, tot_time, n_lm = calculate_path_metrics(path, landmarks_dict, time_matrix, hotel)
    else:
        fitness, interest, tot_time, n_lm = 0, 0, 0, 0
    
    rows_hotel.append({
        'Hotel': hotel.name,
        'Fitness': round(fitness, 4),
        'Interest': round(interest, 2),
        'TravelTime_h': round(tot_time, 2),
        'NumLandmarks': n_lm,
        'Runtime_ms': round(elapsed * 1000, 2),
    })
    print(f"  {hotel.name:20s}  ->  fit={fitness:7.2f} #lm={n_lm:2d} travel={tot_time:.1f}h ({elapsed*1000:.1f}ms)")

df_hotel = pd.DataFrame(rows_hotel)
csv_path = os.path.join(OUTPUT_DIR, "hotel_comparison.csv")
df_hotel.to_csv(csv_path, index=False)
print(f"  [OK] saved -> {csv_path}")

# ═════════════════════════════════════════════════════════════════════════════
# 3.  DAY-OF-WEEK COMPARISON
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PHASE 3 -- Day-of-Week Comparison (fixed hotel=first, budget=8h, time=9am)")
print("=" * 70)

rows_day = []
for day in Days:
    problem = TravelProblem_InformedSearch(
        Hotels_to_test[0], landmarks, [], time_matrix,
        time_budget=8 * 60,
        starting_time=9 * 60,
        visiting_day=day
    )
    
    t0 = time.time()
    path = greedy_search(problem)
    elapsed = time.time() - t0
    
    if path:
        fitness, interest, tot_time, n_lm = calculate_path_metrics(path, landmarks_dict, time_matrix, Hotels_to_test[0])
    else:
        fitness, interest, tot_time, n_lm = 0, 0, 0, 0
    
    rows_day.append({
        'Day': day,
        'Fitness': round(fitness, 4),
        'Interest': round(interest, 2),
        'TravelTime_h': round(tot_time, 2),
        'NumLandmarks': n_lm,
        'Runtime_ms': round(elapsed * 1000, 2),
    })
    print(f"  {day:3s}  ->  fit={fitness:7.2f} #lm={n_lm:2d} travel={tot_time:.1f}h ({elapsed*1000:.1f}ms)")

df_day = pd.DataFrame(rows_day)
csv_path = os.path.join(OUTPUT_DIR, "day_comparison.csv")
df_day.to_csv(csv_path, index=False)
print(f"  [OK] saved -> {csv_path}")

# ═════════════════════════════════════════════════════════════════════════════
# 4.  TIME BUDGET SWEEP
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PHASE 4 -- Time Budget Sweep (fixed hotel=first, day=fri, time=9am)")
print("=" * 70)

rows_budget = []
for budget in np.arange(4, 13, 0.5):
    problem = TravelProblem_InformedSearch(
        Hotels_to_test[0], landmarks, [], time_matrix,
        time_budget=budget * 60,
        starting_time=9 * 60,
        visiting_day='fri'
    )
    
    t0 = time.time()
    path = greedy_search(problem)
    elapsed = time.time() - t0
    
    if path:
        fitness, interest, tot_time, n_lm = calculate_path_metrics(path, landmarks_dict, time_matrix, Hotels_to_test[0])
    else:
        fitness, interest, tot_time, n_lm = 0, 0, 0, 0
    
    rows_budget.append({
        'Budget_h': round(budget, 1),
        'Fitness': round(fitness, 4),
        'Interest': round(interest, 2),
        'TravelTime_h': round(tot_time, 2),
        'NumLandmarks': n_lm,
        'Runtime_ms': round(elapsed * 1000, 2),
    })
    print(f"  budget={budget:.1f}h  ->  fit={fitness:7.2f} #lm={n_lm:2d} travel={tot_time:.1f}h ({elapsed*1000:.1f}ms)")

df_budget = pd.DataFrame(rows_budget)
csv_path = os.path.join(OUTPUT_DIR, "budget_sweep.csv")
df_budget.to_csv(csv_path, index=False)
print(f"  [OK] saved -> {csv_path}")

# ═════════════════════════════════════════════════════════════════════════════
# 5.  PLOTS
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PHASE 5 -- Generating Plots")
print("=" * 70)

COLORS = ['#2ecc71', '#e74c3c', '#3498db', '#f39c12', '#9b59b6', '#1abc9c']

# ---------- Plot 1: Hotel Comparison - Bar Chart ----------
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(df_hotel['Hotel'], df_hotel['Fitness'], color=COLORS[:len(df_hotel)])
ax.set_ylabel('Fitness', fontsize=11)
ax.set_title('Greedy Performance by Hotel (day=fri, budget=8h, time=9am)', fontsize=13, pad=12)
ax.tick_params(axis='x', rotation=45)
ax.grid(axis='y', alpha=0.3)
for bar, val, lm in zip(bars, df_hotel['Fitness'], df_hotel['NumLandmarks']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, 
            f'{val:.1f}\n({int(lm)} lm)', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
path1 = os.path.join(OUTPUT_DIR, "hotel_comparison.png")
fig.savefig(path1, dpi=150)
plt.close(fig)
print(f"  [OK] {path1}")

# ---------- Plot 2: Day-of-Week Comparison - Line Chart ----------
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_day['Day'], df_day['Fitness'], 'o-', color='#2ecc71', linewidth=2.5, markersize=8, label='Fitness')
ax.set_xlabel('Day of Week', fontsize=11)
ax.set_ylabel('Fitness', fontsize=11)
ax.set_title('Greedy Performance by Day (hotel=first, budget=8h, time=9am)', fontsize=13, pad=12)
ax.grid(alpha=0.3)
for x, y, n_lm in zip(range(len(df_day)), df_day['Fitness'], df_day['NumLandmarks']):
    ax.text(x, y + 0.2, f'{int(n_lm)}', ha='center', va='bottom', fontsize=8)
plt.tight_layout()
path2 = os.path.join(OUTPUT_DIR, "day_comparison.png")
fig.savefig(path2, dpi=150)
plt.close(fig)
print(f"  [OK] {path2}")

# ---------- Plot 3: Time Budget Sweep - Line Chart ----------
fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(df_budget['Budget_h'], df_budget['Fitness'], 'o-', color='#3498db', linewidth=2.5, markersize=8, label='Fitness')
ax1.set_xlabel('Time Budget (hours)', fontsize=11)
ax1.set_ylabel('Fitness', color='#3498db', fontsize=11)
ax1.tick_params(axis='y', labelcolor='#3498db')

ax2 = ax1.twinx()
ax2.plot(df_budget['Budget_h'], df_budget['NumLandmarks'], 's--', color='#e74c3c', linewidth=2.5, markersize=8, label='# Landmarks')
ax2.set_ylabel('Number of Landmarks', color='#e74c3c', fontsize=11)
ax2.tick_params(axis='y', labelcolor='#e74c3c')

ax1.set_title('Greedy Performance vs Time Budget', fontsize=13, pad=12)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='center left')
ax1.grid(alpha=0.3)
plt.tight_layout()
path3 = os.path.join(OUTPUT_DIR, "budget_sweep.png")
fig.savefig(path3, dpi=150)
plt.close(fig)
print(f"  [OK] {path3}")

# ---------- Plot 4: Heatmap - Hotel vs Budget (Fitness) ----------
fig, ax = plt.subplots(figsize=(10, 6))
# Create a subset for hotel vs budget
heatmap_data = df_full[df_full['Day'] == 'fri'].copy()
heatmap_data = heatmap_data[heatmap_data['StartTime'] == 9]
pivot_hb = heatmap_data.pivot_table(index='Hotel', columns='Budget_h', values='Fitness', aggfunc='mean')
im = ax.imshow(pivot_hb.values, cmap='YlGnBu', aspect='auto')
ax.set_xticks(range(len(pivot_hb.columns)))
ax.set_xticklabels([f'{x:.0f}h' for x in pivot_hb.columns], fontsize=9)
ax.set_yticks(range(len(pivot_hb.index)))
ax.set_yticklabels(pivot_hb.index, fontsize=9)
for i in range(len(pivot_hb.index)):
    for j in range(len(pivot_hb.columns)):
        val = pivot_hb.values[i, j]
        if not np.isnan(val):
            ax.text(j, i, f'{val:.1f}', ha='center', va='center', fontsize=8,
                    color='white' if val > np.nanmean(pivot_hb.values) else 'black')
fig.colorbar(im, ax=ax, label='Fitness')
ax.set_title('Fitness Heatmap -- Hotel vs Time Budget (day=fri, time=9am)', fontsize=13, pad=12)
ax.set_xlabel('Time Budget')
ax.set_ylabel('Hotel')
plt.tight_layout()
path4 = os.path.join(OUTPUT_DIR, "heatmap_hotel_budget.png")
fig.savefig(path4, dpi=150)
plt.close(fig)
print(f"  [OK] {path4}")

# ---------- Plot 5: Heatmap - Day vs Budget (Fitness) ----------
fig, ax = plt.subplots(figsize=(10, 7))
heatmap_data2 = df_full[df_full['Hotel'] == Hotels_to_test[0].name].copy()
heatmap_data2 = heatmap_data2[heatmap_data2['StartTime'] == 9]
pivot_db = heatmap_data2.pivot_table(index='Day', columns='Budget_h', values='Fitness', aggfunc='mean')
im = ax.imshow(pivot_db.values, cmap='YlGnBu', aspect='auto')
ax.set_xticks(range(len(pivot_db.columns)))
ax.set_xticklabels([f'{x:.0f}h' for x in pivot_db.columns], fontsize=9)
ax.set_yticks(range(len(pivot_db.index)))
ax.set_yticklabels(pivot_db.index, fontsize=9)
for i in range(len(pivot_db.index)):
    for j in range(len(pivot_db.columns)):
        val = pivot_db.values[i, j]
        if not np.isnan(val):
            ax.text(j, i, f'{val:.1f}', ha='center', va='center', fontsize=8,
                    color='white' if val > np.nanmean(pivot_db.values) else 'black')
fig.colorbar(im, ax=ax, label='Fitness')
ax.set_title(f'Fitness Heatmap -- Day vs Time Budget (hotel={Hotels_to_test[0].name}, time=9am)', fontsize=13, pad=12)
ax.set_xlabel('Time Budget')
ax.set_ylabel('Day of Week')
plt.tight_layout()
path5 = os.path.join(OUTPUT_DIR, "heatmap_day_budget.png")
fig.savefig(path5, dpi=150)
plt.close(fig)
print(f"  [OK] {path5}")

# ---------- Plot 6: Landmarks Visited by Budget ----------
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(df_budget['Budget_h'], df_budget['NumLandmarks'], color=COLORS[0], alpha=0.7, width=0.3)
ax.set_xlabel('Time Budget (hours)', fontsize=11)
ax.set_ylabel('Number of Landmarks Visited', fontsize=11)
ax.set_title('Landmarks Visited vs Time Budget (Greedy Algorithm)', fontsize=13, pad=12)
ax.grid(axis='y', alpha=0.3)
for x, y in zip(df_budget['Budget_h'], df_budget['NumLandmarks']):
    ax.text(x, y + 0.1, str(int(y)), ha='center', va='bottom', fontsize=9)
plt.tight_layout()
path6 = os.path.join(OUTPUT_DIR, "landmarks_by_budget.png")
fig.savefig(path6, dpi=150)
plt.close(fig)
print(f"  [OK] {path6}")

# ---------- Plot 7: Runtime Comparison ----------
fig, ax = plt.subplots(figsize=(10, 6))
avg_runtime = df_full.groupby('Day')['Runtime_ms'].mean()
bars = ax.bar(avg_runtime.index, avg_runtime.values, color=COLORS[1], alpha=0.7)
ax.set_xlabel('Day of Week', fontsize=11)
ax.set_ylabel('Avg Runtime (milliseconds)', fontsize=11)
ax.set_title('Greedy Algorithm Runtime by Day', fontsize=13, pad=12)
ax.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, avg_runtime.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
            f'{val:.2f}ms', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
path7 = os.path.join(OUTPUT_DIR, "runtime_by_day.png")
fig.savefig(path7, dpi=150)
plt.close(fig)
print(f"  [OK] {path7}")

# ═════════════════════════════════════════════════════════════════════════════
# 6.  SUMMARY TABLE (printed to console)
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SUMMARY -- Hotel Comparison Results")
print("=" * 70)
print(df_hotel.to_string(index=False))

print("\n" + "=" * 70)
print("Day-of-Week Comparison Results")
print("=" * 70)
print(df_day.to_string(index=False))

print("\n" + "=" * 70)
print("Time Budget Sweep Results")
print("=" * 70)
print(df_budget.to_string(index=False))

print("\n[DONE] All done! Results & plots saved in:", OUTPUT_DIR)
