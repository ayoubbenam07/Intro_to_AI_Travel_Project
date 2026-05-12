"""
ABC_test.py
=========================================================
Tests the ABC (Artificial Bee Colony) across multiple:
  Colony sizes           (30, 40, 50, 60)
  Colony ratios          (0.3, 0.5, 0.7)
  Abandonment limits     (10, 20, 30)
  Selection methods      (roulette, tournament, rank)
  Number of iterations   (50, 100, 150)
"""

import sys, os, random, time, itertools
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import seaborn as sns

# ── project imports ──────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.data_loader import get_landmarks, get_hotels, get_time_matrix
from core.Problem_LocalSearch import TravelProblem_LocalSearch
from Algorithms.artificial_bee_colony import ABC_Optimization

# ── data loading ─────────────────────────────────────────────────────────────
landmarks = get_landmarks()
hotels     = get_hotels()
time_matrix = get_time_matrix()

# ── problem setup ─────────────────────────────────────────────────────────────
problem = TravelProblem_LocalSearch(
    landmarks,
    travel_information={
        'hotel': hotels[0],
        'time_matrix': time_matrix,
        'Travel_Time': 8,
        'Travel_day': 'fri',
        'type_filter': None,
        'trip_start_time': 9,
    },
)

# ── parameters ───────────────────────────────────────────────────────────
Colony_sizes     = [30, 40, 50, 60]
Colony_ratios    = [0.3, 0.5, 0.7]
Abandonment_limits = [10, 20, 30]
Selection_methods = ['roulette', 'tournament', 'rank']
Iterations_values = [50, 75, 100, 125, 150]

SEED = 42

# ── output directory ─────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Tests", "ABC_test_results")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ═════════════════════════════════════════════════════════════════════════════
# 1.  Full factorial test (colony_size × colony_ratio × limit × selection)
#     Using fixed iterations=100
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PHASE 1 -- Full Factorial: Colony Params x Selection Method")
print("         (iterations=100)")
print("=" * 70)

rows_factorial = []
total_combos = len(Colony_sizes) * len(Colony_ratios) * len(Abandonment_limits) * len(Selection_methods)
combo_idx = 0

for size, ratio, limit, sel in itertools.product(Colony_sizes, Colony_ratios, Abandonment_limits, Selection_methods):
    combo_idx += 1
    random.seed(SEED)
    abc = ABC_Optimization(
        problem,
        colony_size=size,
        colony_ratio=ratio,
        limit=limit,
        iterations=100,
        selection_method=sel,
    )
    t0 = time.time()
    best_state, fitness = abc.solve()
    elapsed = time.time() - t0
    interest = sum(lm.interest_score for lm in best_state)
    tot_time = round(abc.calculate_total_time(best_state), 2)
    n_lm = len(best_state)
    
    rows_factorial.append({
        'ColonySize': size,
        'ColonyRatio': ratio,
        'Limit': limit,
        'Selection': sel,
        'Fitness': round(fitness, 4),
        'Interest': round(interest, 2),
        'TotalTime_h': tot_time,
        'NumLandmarks': n_lm,
        'Runtime_s': round(elapsed, 2),
    })
    print(f"  [{combo_idx:3d}/{total_combos}]  size={size:2d} ratio={ratio:.1f} limit={limit:2d} sel={sel:11s}"
          f"  ->  fit={fitness:7.2f} time={tot_time:5.2f}h  #lm={n_lm}  ({elapsed:.1f}s)")

df_factorial = pd.DataFrame(rows_factorial)
csv_path = os.path.join(OUTPUT_DIR, "factorial_results.csv")
df_factorial.to_csv(csv_path, index=False)
print(f"\n[OK] Factorial results saved -> {csv_path}")

# ═════════════════════════════════════════════════════════════════════════════
# 2.  Colony size sweep (best combo from phase 1)
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PHASE 2 -- Colony Size Sweep")
print("=" * 70)

best_row = df_factorial.loc[df_factorial['Fitness'].idxmax()]
best_size, best_ratio, best_limit, best_sel = (
    best_row['ColonySize'], best_row['ColonyRatio'], best_row['Limit'], best_row['Selection']
)
print(f"  Using best combo: size={best_size} ratio={best_ratio} limit={best_limit} sel={best_sel}")

rows_size = []
for size in [20, 30, 40, 50, 60, 70, 80]:
    random.seed(SEED)
    abc = ABC_Optimization(
        problem,
        colony_size=size,
        colony_ratio=best_ratio,
        limit=best_limit,
        iterations=100,
        selection_method=best_sel,
    )
    t0 = time.time()
    best_state, fitness = abc.solve()
    elapsed = time.time() - t0
    interest = sum(lm.interest_score for lm in best_state)
    tot_time = round(abc.calculate_total_time(best_state), 2)
    n_lm = len(best_state)
    
    rows_size.append({
        'ColonySize': size,
        'Fitness': round(fitness, 4),
        'Interest': round(interest, 2),
        'TotalTime_h': tot_time,
        'NumLandmarks': n_lm,
        'Runtime_s': round(elapsed, 2),
    })
    print(f"  size={size:2d}  ->  fit={fitness:7.2f} time={tot_time:5.2f}h  #lm={n_lm}  ({elapsed:.1f}s)")

df_size = pd.DataFrame(rows_size)
csv_path = os.path.join(OUTPUT_DIR, "colony_size_sweep.csv")
df_size.to_csv(csv_path, index=False)
print(f"  [OK] saved -> {csv_path}")

# ═════════════════════════════════════════════════════════════════════════════
# 3.  Abandonment limit sweep
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PHASE 3 -- Abandonment Limit Sweep")
print("=" * 70)

rows_limit = []
for limit in [5, 10, 15, 20, 25, 30, 35, 40]:
    random.seed(SEED)
    abc = ABC_Optimization(
        problem,
        colony_size=best_size,
        colony_ratio=best_ratio,
        limit=limit,
        iterations=100,
        selection_method=best_sel,
    )
    t0 = time.time()
    best_state, fitness = abc.solve()
    elapsed = time.time() - t0
    interest = sum(lm.interest_score for lm in best_state)
    tot_time = round(abc.calculate_total_time(best_state), 2)
    n_lm = len(best_state)
    
    rows_limit.append({
        'Limit': limit,
        'Fitness': round(fitness, 4),
        'Interest': round(interest, 2),
        'TotalTime_h': tot_time,
        'NumLandmarks': n_lm,
        'Runtime_s': round(elapsed, 2),
    })
    print(f"  limit={limit:2d}  ->  fit={fitness:7.2f} time={tot_time:5.2f}h  #lm={n_lm}  ({elapsed:.1f}s)")

df_limit = pd.DataFrame(rows_limit)
csv_path = os.path.join(OUTPUT_DIR, "limit_sweep.csv")
df_limit.to_csv(csv_path, index=False)
print(f"  [OK] saved -> {csv_path}")

# ═════════════════════════════════════════════════════════════════════════════
# 4.  Iterations sweep
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PHASE 4 -- Iterations Sweep")
print("=" * 70)

rows_iter = []
for iters in Iterations_values:
    random.seed(SEED)
    abc = ABC_Optimization(
        problem,
        colony_size=best_size,
        colony_ratio=best_ratio,
        limit=best_limit,
        iterations=iters,
        selection_method=best_sel,
    )
    t0 = time.time()
    best_state, fitness = abc.solve()
    elapsed = time.time() - t0
    interest = sum(lm.interest_score for lm in best_state)
    tot_time = round(abc.calculate_total_time(best_state), 2)
    n_lm = len(best_state)
    
    rows_iter.append({
        'Iterations': iters,
        'Fitness': round(fitness, 4),
        'Interest': round(interest, 2),
        'TotalTime_h': tot_time,
        'NumLandmarks': n_lm,
        'Runtime_s': round(elapsed, 2),
    })
    print(f"  iter={iters:3d}  ->  fit={fitness:7.2f} time={tot_time:5.2f}h  #lm={n_lm}  ({elapsed:.1f}s)")

df_iter = pd.DataFrame(rows_iter)
csv_path = os.path.join(OUTPUT_DIR, "iterations_sweep.csv")
df_iter.to_csv(csv_path, index=False)
print(f"  [OK] saved -> {csv_path}")

# ═════════════════════════════════════════════════════════════════════════════
# 5.  PLOTS
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PHASE 5 -- Generating Plots")
print("=" * 70)

COLORS = ['#2ecc71', '#e74c3c', '#3498db', '#f39c12', '#9b59b6', '#1abc9c']

# ---------- Plot 1: Heatmap - Colony Size vs Ratio (Fitness) ----------
fig, ax = plt.subplots(figsize=(10, 6))
pivot = df_factorial.groupby(['ColonySize', 'ColonyRatio'])['Fitness'].max().unstack()
im = ax.imshow(pivot.values, cmap='YlGnBu', aspect='auto')
ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels([f'{x:.1f}' for x in pivot.columns], fontsize=9)
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(pivot.index, fontsize=9)
for i in range(len(pivot.index)):
    for j in range(len(pivot.columns)):
        val = pivot.values[i, j]
        ax.text(j, i, f'{val:.1f}', ha='center', va='center', fontsize=8,
                color='white' if val > pivot.values.mean() else 'black')
fig.colorbar(im, ax=ax, label='Best Fitness')
ax.set_title('Best Fitness -- Colony Size x Colony Ratio', fontsize=13, pad=12)
ax.set_xlabel('Colony Ratio')
ax.set_ylabel('Colony Size')
plt.tight_layout()
path1 = os.path.join(OUTPUT_DIR, "heatmap_size_ratio.png")
fig.savefig(path1, dpi=150)
plt.close(fig)
print(f"  [OK] {path1}")

# ---------- Plot 2: Heatmap - Limit vs Selection (Fitness) ----------
fig, ax = plt.subplots(figsize=(10, 6))
pivot_limit = df_factorial.groupby(['Limit', 'Selection'])['Fitness'].max().unstack()
im = ax.imshow(pivot_limit.values, cmap='YlGnBu', aspect='auto')
ax.set_xticks(range(len(pivot_limit.columns)))
ax.set_xticklabels(pivot_limit.columns, fontsize=9)
ax.set_yticks(range(len(pivot_limit.index)))
ax.set_yticklabels(pivot_limit.index, fontsize=9)
for i in range(len(pivot_limit.index)):
    for j in range(len(pivot_limit.columns)):
        val = pivot_limit.values[i, j]
        ax.text(j, i, f'{val:.1f}', ha='center', va='center', fontsize=8,
                color='white' if val > pivot_limit.values.mean() else 'black')
fig.colorbar(im, ax=ax, label='Best Fitness')
ax.set_title('Best Fitness -- Abandonment Limit x Selection Method', fontsize=13, pad=12)
ax.set_xlabel('Selection Method')
ax.set_ylabel('Abandonment Limit')
plt.tight_layout()
path2 = os.path.join(OUTPUT_DIR, "heatmap_limit_selection.png")
fig.savefig(path2, dpi=150)
plt.close(fig)
print(f"  [OK] {path2}")

# ---------- Plot 3: Mean Fitness by Selection Method ----------
fig, ax = plt.subplots(figsize=(10, 6))
sel_mean = df_factorial.groupby('Selection')['Fitness'].mean().sort_values(ascending=False)
bars = ax.bar(sel_mean.index, sel_mean.values, color=COLORS[:len(sel_mean)])
ax.set_ylabel('Mean Fitness', fontsize=11)
ax.set_title('Mean Fitness by Selection Method', fontsize=13, pad=12)
ax.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, sel_mean.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f'{val:.2f}', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
path3 = os.path.join(OUTPUT_DIR, "bar_selection_mean.png")
fig.savefig(path3, dpi=150)
plt.close(fig)
print(f"  [OK] {path3}")

# ---------- Plot 4: Colony Size Sweep - Line Chart ----------
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(df_size['ColonySize'], df_size['Fitness'], 'o-', color='#2ecc71', linewidth=2.5, markersize=8, label='Fitness')
ax1.set_xlabel('Colony Size', fontsize=11)
ax1.set_ylabel('Fitness', color='#2ecc71', fontsize=11)
ax1.tick_params(axis='y', labelcolor='#2ecc71')

ax2 = ax1.twinx()
ax2.plot(df_size['ColonySize'], df_size['Runtime_s'], 's--', color='#e74c3c', linewidth=2.5, markersize=8, label='Runtime (s)')
ax2.set_ylabel('Runtime (s)', color='#e74c3c', fontsize=11)
ax2.tick_params(axis='y', labelcolor='#e74c3c')

ax1.set_title('Colony Size vs Fitness & Runtime', fontsize=13, pad=12)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='center right')
ax1.grid(alpha=0.3)
plt.tight_layout()
path4 = os.path.join(OUTPUT_DIR, "colony_size_sweep.png")
fig.savefig(path4, dpi=150)
plt.close(fig)
print(f"  [OK] {path4}")

# ---------- Plot 5: Abandonment Limit Sweep - Line Chart ----------
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(df_limit['Limit'], df_limit['Fitness'], 'o-', color='#3498db', linewidth=2.5, markersize=8, label='Fitness')
ax1.set_xlabel('Abandonment Limit', fontsize=11)
ax1.set_ylabel('Fitness', color='#3498db', fontsize=11)
ax1.tick_params(axis='y', labelcolor='#3498db')

ax2 = ax1.twinx()
ax2.plot(df_limit['Limit'], df_limit['Runtime_s'], 's--', color='#f39c12', linewidth=2.5, markersize=8, label='Runtime (s)')
ax2.set_ylabel('Runtime (s)', color='#f39c12', fontsize=11)
ax2.tick_params(axis='y', labelcolor='#f39c12')

ax1.set_title('Abandonment Limit vs Fitness & Runtime', fontsize=13, pad=12)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='center right')
ax1.grid(alpha=0.3)
plt.tight_layout()
path5 = os.path.join(OUTPUT_DIR, "limit_sweep.png")
fig.savefig(path5, dpi=150)
plt.close(fig)
print(f"  [OK] {path5}")

# ---------- Plot 6: Iterations Sweep - Line Chart ----------
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(df_iter['Iterations'], df_iter['Fitness'], 'o-', color='#9b59b6', linewidth=2.5, markersize=8, label='Fitness')
ax1.set_xlabel('Number of Iterations', fontsize=11)
ax1.set_ylabel('Fitness', color='#9b59b6', fontsize=11)
ax1.tick_params(axis='y', labelcolor='#9b59b6')

ax2 = ax1.twinx()
ax2.plot(df_iter['Iterations'], df_iter['Runtime_s'], 's--', color='#1abc9c', linewidth=2.5, markersize=8, label='Runtime (s)')
ax2.set_ylabel('Runtime (s)', color='#1abc9c', fontsize=11)
ax2.tick_params(axis='y', labelcolor='#1abc9c')

ax1.set_title('Iterations vs Fitness & Runtime', fontsize=13, pad=12)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='center right')
ax1.grid(alpha=0.3)
plt.tight_layout()
path6 = os.path.join(OUTPUT_DIR, "iterations_sweep.png")
fig.savefig(path6, dpi=150)
plt.close(fig)
print(f"  [OK] {path6}")

# ---------- Plot 7: Top 10 best configurations ----------
top10 = df_factorial.nlargest(10, 'Fitness')
fig, ax = plt.subplots(figsize=(14, 7))
labels_top = [f"Size={int(r['ColonySize'])}\nRatio={r['ColonyRatio']:.1f}\nLimit={int(r['Limit'])}\n{r['Selection']}" 
              for _, r in top10.iterrows()]
bars = ax.barh(range(len(top10)), top10['Fitness'], color=COLORS * 2)
ax.set_yticks(range(len(top10)))
ax.set_yticklabels(labels_top, fontsize=7)
ax.set_xlabel('Fitness', fontsize=11)
ax.set_title('Top 10 ABC Configurations by Fitness', fontsize=13, pad=12)
for i, (val, interest) in enumerate(zip(top10['Fitness'], top10['Interest'])):
    ax.text(val + 0.1, i, f'  fit={val:.1f}', va='center', fontsize=8)
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()
plt.tight_layout()
path7 = os.path.join(OUTPUT_DIR, "top10_configs.png")
fig.savefig(path7, dpi=150)
plt.close(fig)
print(f"  [OK] {path7}")

# ---------- Plot 8: Runtime Heatmap - Colony Size vs Ratio ----------
fig, ax = plt.subplots(figsize=(10, 6))
pivot_rt = df_factorial.groupby(['ColonySize', 'ColonyRatio'])['Runtime_s'].mean().unstack()
im = ax.imshow(pivot_rt.values, cmap='OrRd', aspect='auto')
ax.set_xticks(range(len(pivot_rt.columns)))
ax.set_xticklabels([f'{x:.1f}' for x in pivot_rt.columns], fontsize=9)
ax.set_yticks(range(len(pivot_rt.index)))
ax.set_yticklabels(pivot_rt.index, fontsize=9)
for i in range(len(pivot_rt.index)):
    for j in range(len(pivot_rt.columns)):
        val = pivot_rt.values[i, j]
        ax.text(j, i, f'{val:.1f}s', ha='center', va='center', fontsize=8,
                color='white' if val > pivot_rt.values.mean() else 'black')
fig.colorbar(im, ax=ax, label='Mean Runtime (s)')
ax.set_title('Mean Runtime (s) -- Colony Size x Colony Ratio', fontsize=13, pad=12)
ax.set_xlabel('Colony Ratio')
ax.set_ylabel('Colony Size')
plt.tight_layout()
path8 = os.path.join(OUTPUT_DIR, "heatmap_runtime.png")
fig.savefig(path8, dpi=150)
plt.close(fig)
print(f"  [OK] {path8}")

# ═════════════════════════════════════════════════════════════════════════════
# 6.  SUMMARY TABLE (printed to console)
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SUMMARY -- Top 15 Configurations (by Fitness)")
print("=" * 70)
top15 = df_factorial.nlargest(15, 'Fitness')
print(top15.to_string(index=False))

print("\n" + "=" * 70)
print("Colony Size Sweep Results")
print("=" * 70)
print(df_size.to_string(index=False))

print("\n" + "=" * 70)
print("Abandonment Limit Sweep Results")
print("=" * 70)
print(df_limit.to_string(index=False))

print("\n" + "=" * 70)
print("Iterations Sweep Results")
print("=" * 70)
print(df_iter.to_string(index=False))

print("\n[DONE] All done! Results & plots saved in:", OUTPUT_DIR)
