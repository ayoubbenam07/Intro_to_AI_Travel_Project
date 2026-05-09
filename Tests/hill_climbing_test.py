"""
hill_climbing_test.py
=========================================================
Tests the Hill Climbing algorithm across multiple:
  Base strategies          (steepest, stochastic, first_choice)
  Number of restarts       (1, 10, 25, 50, 100)
"""

import sys, os, random, time
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np

# ── project imports ──────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.data_loader import get_landmarks, get_hotels, get_time_matrix
from core.Problem_LocalSearch import TravelProblem_LocalSearch
from Algorithms.hill_climbing import hill_climbing

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
        'Travel_Time': 12,
        'Travel_day': 'fri',
        'type_filter': None,
        'trip_start_time': 8,
    },
)

# ── parameters ───────────────────────────────────────────────────────────
Base_strategies    = ['steepest', 'stochastic', 'first_choice']
Num_restarts_values = [1, 25, 50, 100]

SEED = 42

# ── output directory ─────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Tests", "hill_climbing_test_results")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ═════════════════════════════════════════════════════════════════════════════
# 1.  Full test: strategies × restarts
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PHASE 1 -- Full Test: Strategies x Restarts")
print("=" * 70)

rows_full = []
total_combos = len(Base_strategies) * len(Num_restarts_values)
combo_idx = 0

for strategy in Base_strategies:
    for restarts in Num_restarts_values:
        combo_idx += 1
        random.seed(SEED)
        hc = hill_climbing(problem, num_restarts=restarts, base_strategy=strategy)
        t0 = time.time()
        best = hc.run()
        elapsed = time.time() - t0
        fitness   = hc.evaluate(best.state)
        interest = sum(lm.interest_score for lm in best.state)
        tot_time  = round(hc.calculate_total_time(best.state), 2)
        n_lm      = len(best.state)
        rows_full.append({
            'Strategy': strategy,
            'Restarts': restarts,
            'Fitness':   round(fitness, 4),
            'Interest':    round(interest, 2),
            'TotalTime_h': tot_time,
            'NumLandmarks': n_lm,
            'Runtime_s':   round(elapsed, 2),
        })
        print(f"  [{combo_idx:3d}/{total_combos}]  {strategy:12s} | restarts={restarts:3d}"
              f"  ->  Interest={interest:7.2f} "
              f"time={tot_time:5.2f}h  #lm={n_lm}  ({elapsed:.1f}s)")

df_full = pd.DataFrame(rows_full)
csv_path = os.path.join(OUTPUT_DIR, "full_results.csv")
df_full.to_csv(csv_path, index=False)
print(f"\n[OK] Full results saved -> {csv_path}")

# ═════════════════════════════════════════════════════════════════════════════
# 2.  Restarts sweep for each strategy
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PHASE 2 -- Restarts Sweep per Strategy")
print("=" * 70)

rows_restart = []
for strategy in Base_strategies:
    for restarts in Num_restarts_values:
        random.seed(SEED)
        hc = hill_climbing(problem, num_restarts=restarts, base_strategy=strategy)
        t0 = time.time()
        best = hc.run()
        elapsed = time.time() - t0
        fitness  = hc.evaluate(best.state)
        interest = sum(lm.interest_score for lm in best.state)
        tot_time = round(hc.calculate_total_time(best.state), 2)
        n_lm     = len(best.state)
        rows_restart.append({
            'Strategy': strategy,
            'Restarts': restarts,
            'Fitness':     round(fitness, 4),
            'Interest':    round(interest, 2),
            'TotalTime_h': tot_time,
            'NumLandmarks': n_lm,
            'Runtime_s':   round(elapsed, 2),
        })
    print(f"  [OK] {strategy} restarts sweep completed")

df_restart = pd.DataFrame(rows_restart)
csv_path = os.path.join(OUTPUT_DIR, "restarts_sweep.csv")
df_restart.to_csv(csv_path, index=False)
print(f"  [OK] saved -> {csv_path}")

# ═════════════════════════════════════════════════════════════════════════════
# 3.  PLOTS
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PHASE 3 -- Generating Plots")
print("=" * 70)

# ── colour palette ───────────────────────────────────────────────────────────
COLORS = ['#2ecc71', '#e74c3c', '#3498db', '#f39c12', '#9b59b6', '#1abc9c']

# ---------- Plot 1: Heatmap — fitness for each (Strategy × Restarts) ----------
fig, ax = plt.subplots(figsize=(12, 5))
pivot = df_full.pivot(index='Strategy', columns='Restarts', values='Fitness')
im = ax.imshow(pivot.values, cmap='YlGnBu', aspect='auto')
ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels(pivot.columns, rotation=40, ha='right', fontsize=9)
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(pivot.index, fontsize=10)
for i in range(len(pivot.index)):
    for j in range(len(pivot.columns)):
        val = pivot.values[i, j]
        ax.text(j, i, f'{val:.1f}', ha='center', va='center', fontsize=8,
                color='white' if val > pivot.values.mean() else 'black')
fig.colorbar(im, ax=ax, label='Fitness')
ax.set_title('Fitness -- Strategy x Restarts', fontsize=13, pad=12)
ax.set_xlabel('Number of Restarts')
ax.set_ylabel('Strategy')
plt.tight_layout()
path1 = os.path.join(OUTPUT_DIR, "heatmap_strategy_restarts.png")
fig.savefig(path1, dpi=150)
plt.close(fig)
print(f"  [OK] {path1}")

# ---------- Plot 2: Line chart — fitness vs restarts per strategy ----------
fig, ax = plt.subplots(figsize=(10, 6))
for i, strategy in enumerate(Base_strategies):
    subset = df_restart[df_restart['Strategy'] == strategy]
    ax.plot(subset['Restarts'], subset['Fitness'], 'o-', color=COLORS[i % len(COLORS)], linewidth=2, markersize=6, label=strategy)
ax.set_xlabel('Number of Restarts', fontsize=11)
ax.set_ylabel('Fitness', fontsize=11)
ax.set_title('Fitness vs Restarts per Strategy', fontsize=13, pad=12)
ax.legend(title='Strategy', fontsize=10, title_fontsize=11)
ax.grid(alpha=0.3)
plt.tight_layout()
path2 = os.path.join(OUTPUT_DIR, "line_fitness_restarts.png")
fig.savefig(path2, dpi=150)
plt.close(fig)
print(f"  [OK] {path2}")

# ---------- Plot 3: Bar chart — best fitness per strategy ----------
best_per_strategy = df_full.groupby('Strategy')['Fitness'].max()
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(best_per_strategy.index, best_per_strategy.values, color=COLORS[:len(Base_strategies)])
ax.set_ylabel('Best Fitness', fontsize=11)
ax.set_title('Best Fitness per Strategy', fontsize=13, pad=12)
ax.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, best_per_strategy.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f'{val:.2f}', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
path3 = os.path.join(OUTPUT_DIR, "bar_best_fitness_strategy.png")
fig.savefig(path3, dpi=150)
plt.close(fig)
print(f"  [OK] {path3}")

# ---------- Plot 4: Runtime heatmap — Strategy × Restarts ----------
fig, ax = plt.subplots(figsize=(12, 5))
pivot_rt = df_full.pivot(index='Strategy', columns='Restarts', values='Runtime_s')
im = ax.imshow(pivot_rt.values, cmap='OrRd', aspect='auto')
ax.set_xticks(range(len(pivot_rt.columns)))
ax.set_xticklabels(pivot_rt.columns, rotation=40, ha='right', fontsize=9)
ax.set_yticks(range(len(pivot_rt.index)))
ax.set_yticklabels(pivot_rt.index, fontsize=10)
for i in range(len(pivot_rt.index)):
    for j in range(len(pivot_rt.columns)):
        val = pivot_rt.values[i, j]
        ax.text(j, i, f'{val:.1f}s', ha='center', va='center', fontsize=8,
                color='white' if val > pivot_rt.values.mean() else 'black')
fig.colorbar(im, ax=ax, label='Runtime (s)')
ax.set_title('Runtime (s) -- Strategy x Restarts', fontsize=13, pad=12)
ax.set_xlabel('Number of Restarts')
ax.set_ylabel('Strategy')
plt.tight_layout()
path4 = os.path.join(OUTPUT_DIR, "heatmap_runtime.png")
fig.savefig(path4, dpi=150)
plt.close(fig)
print(f"  [OK] {path4}")

# ---------- Plot 5: Top 10 configurations ----------
top10 = df_full.nlargest(10, 'Fitness')
fig, ax = plt.subplots(figsize=(14, 6))
labels_top = [f"{r['Strategy']}\nRestarts: {r['Restarts']}" for _, r in top10.iterrows()]
bars = ax.barh(range(len(top10)), top10['Fitness'], color=COLORS * 2)
ax.set_yticks(range(len(top10)))
ax.set_yticklabels(labels_top, fontsize=8)
ax.set_xlabel('Fitness', fontsize=11)
ax.set_title('Top 10 Hill Climbing Configurations by Fitness', fontsize=13, pad=12)
for i, (val, interest) in enumerate(zip(top10['Fitness'], top10['Interest'])):
    ax.text(val + 0.1, i, f'  fit={val:.1f}, int={interest:.1f}', va='center', fontsize=8)
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()
plt.tight_layout()
path5 = os.path.join(OUTPUT_DIR, "top10_configs.png")
fig.savefig(path5, dpi=150)
plt.close(fig)
print(f"  [OK] {path5}")

# ═════════════════════════════════════════════════════════════════════════════
# 4.  SUMMARY TABLE  (printed to console)
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SUMMARY -- Top 15 Configurations (by Fitness)")
print("=" * 70)
top15 = df_full.nlargest(15, 'Fitness')
print(top15.to_string(index=False))

print("\n" + "=" * 70)
print("Restarts Sweep Results")
print("=" * 70)
print(df_restart.to_string(index=False))

print("\n[DONE] All done! Results & plots saved in:", OUTPUT_DIR)