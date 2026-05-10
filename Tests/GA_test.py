"""
GA-test.py
=========================================================
Tests the GA across multiple:
  Generation counts        (50, 100, 200)
  Mutation rates            (0.05, 0.1, 0.2)
  Selection methods         (tournament, roulette, rank)
  Crossover methods         (one_point, two_point, pmx, order, cycle, edge_recombination)
  Mutation methods           (swap, inversion, scramble, insertion, deletion, displacement)
"""

import sys, os, random, time, itertools
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np

# ── project imports ──────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.data_loader import get_landmarks, get_hotels, get_time_matrix
from core.Problem_LocalSearch import TravelProblem_LocalSearch
from Algorithms.GA import Genetic_Algorithm

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
Generation_values   = [50, 75, 100, 125, 150, 175, 200]
Mutation_rates      = [0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.3]
Selection_methods   = ['tournament', 'roulette', 'rank']
Crossover_methods   = ['one_point', 'two_point', 'pmx', 'order', 'cycle', 'edge_recombination']
Mutation_methods    = ['insertion', 'swap', 'inversion', 'scramble', 'deletion', 'displacement']

POPULATION_SIZE     = 100
SEED                = 42

# ── output directory ─────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Tests", "GA_test_results")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ═════════════════════════════════════════════════════════════════════════════
# 1.  Full factorial test  (selection × crossover × mutation)
#     Using fixed generations=100, mutation_rate=0.1
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PHASE 1 -- Full Factorial: Selection x Crossover x Mutation")
print("         (generations=100, mutation_rate=0.1, pop=100)")
print("=" * 70)

rows_factorial = []
total_combos = len(Selection_methods) * len(Crossover_methods) * len(Mutation_methods)
combo_idx = 0

for sel in Selection_methods:
    for cx in Crossover_methods:
        for mut in Mutation_methods:
            combo_idx += 1
            random.seed(SEED)
            ga = Genetic_Algorithm(problem, population_size=POPULATION_SIZE,
                                   generations=100, mutation_rate=0.1)
            t0 = time.time()
            best = ga.evolve(
                selection_method=sel,
                crossover_method=cx,
                mutation_method=mut,
                tournament_size=5,
                neighborhood_selection='linear',
                elitism_rate=0.2,
            )
            elapsed = time.time() - t0
            fitness   = ga.calculate_fitness(best)
            interest = sum(lm.interest_score for lm in best)
            tot_time  = round(ga.calculate_total_time(best), 2)
            n_lm      = len(best)
            rows_factorial.append({
                'Selection': sel,
                'Crossover': cx,
                'Mutation':  mut,
                'Fitness':   round(fitness, 4),
                'Interest':    round(interest, 2),
                'TotalTime_h': tot_time,
                'NumLandmarks': n_lm,
                'Runtime_s':   round(elapsed, 2),
            })
            print(f"  [{combo_idx:3d}/{total_combos}]  {sel:11s} | {cx:22s} | {mut:14s}"
                  f"  ->  fit={fitness:7.2f} "
                  f"time={tot_time:5.2f}h  #lm={n_lm}  ({elapsed:.1f}s)")

df_factorial = pd.DataFrame(rows_factorial)
csv_path = os.path.join(OUTPUT_DIR, "factorial_results.csv")
df_factorial.to_csv(csv_path, index=False)
print(f"\n[OK] Factorial results saved -> {csv_path}")

# ═════════════════════════════════════════════════════════════════════════════
# 2.  Generation count sweep  (best combo from phase 1)
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PHASE 2 -- Generation Count Sweep")
print("=" * 70)

best_row = df_factorial.loc[df_factorial['Fitness'].idxmax()]
best_sel, best_cx, best_mut = best_row['Selection'], best_row['Crossover'], best_row['Mutation']
print(f"  Using best combo from Phase 1: {best_sel} / {best_cx} / {best_mut}")

rows_gen = []
for gen in Generation_values:
    random.seed(SEED)
    ga = Genetic_Algorithm(problem, population_size=POPULATION_SIZE,
                           generations=gen, mutation_rate=0.1)
    t0 = time.time()
    best = ga.evolve(
        selection_method=best_sel,
        crossover_method=best_cx,
        mutation_method=best_mut,
        tournament_size=5,
        neighborhood_selection='linear',
        elitism_rate=0.2,
    )
    elapsed = time.time() - t0
    fitness  = ga.calculate_fitness(best)
    interest = sum(lm.interest_score for lm in best)
    tot_time = round(ga.calculate_total_time(best), 2)
    n_lm     = len(best)
    rows_gen.append({
        'Generations': gen,
        'Fitness':     round(fitness, 4),
        'Interest':    round(interest, 2),
        'TotalTime_h': tot_time,
        'NumLandmarks': n_lm,
        'Runtime_s':   round(elapsed, 2),
    })
    print(f"  gen={gen:4d}  ->  fit={fitness:7.2f}"
          f"time={tot_time:5.2f}h  #lm={n_lm}  ({elapsed:.1f}s)")

df_gen = pd.DataFrame(rows_gen)
csv_path = os.path.join(OUTPUT_DIR, "generation_sweep.csv")
df_gen.to_csv(csv_path, index=False)
print(f"  [OK] saved -> {csv_path}")

# ═════════════════════════════════════════════════════════════════════════════
# 3.  Mutation rate sweep
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PHASE 3 -- Mutation Rate Sweep")
print("=" * 70)

rows_mr = []
for mr in Mutation_rates:
    random.seed(SEED)
    ga = Genetic_Algorithm(problem, population_size=POPULATION_SIZE,
                           generations=100, mutation_rate=mr)
    t0 = time.time()
    best = ga.evolve(
        selection_method=best_sel,
        crossover_method=best_cx,
        mutation_method=best_mut,
        tournament_size=5,
        neighborhood_selection='linear',
        elitism_rate=0.2,
    )
    elapsed = time.time() - t0
    fitness  = ga.calculate_fitness(best)
    interest = sum(lm.interest_score for lm in best)
    tot_time = round(ga.calculate_total_time(best), 2)
    n_lm     = len(best)
    rows_mr.append({
        'MutationRate': mr,
        'Fitness':      round(fitness, 4),
        'Interest':     round(interest, 2),
        'TotalTime_h':  tot_time,
        'NumLandmarks': n_lm,
        'Runtime_s':    round(elapsed, 2),
    })
    print(f"  mr={mr:.2f}  ->  fit={fitness:7.2f}"
          f"time={tot_time:5.2f}h  #lm={n_lm}  ({elapsed:.1f}s)")

df_mr = pd.DataFrame(rows_mr)
csv_path = os.path.join(OUTPUT_DIR, "mutation_rate_sweep.csv")
df_mr.to_csv(csv_path, index=False)
print(f"  [OK] saved -> {csv_path}")


# ═════════════════════════════════════════════════════════════════════════════
# 4.  PLOTS
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PHASE 4 -- Generating Plots")
print("=" * 70)

# ── colour palette ───────────────────────────────────────────────────────────
COLORS = ['#2ecc71', '#e74c3c', '#3498db', '#f39c12', '#9b59b6', '#1abc9c']

# ---------- Plot 1: Heatmap  — best fitness for each (Selection × Crossover) ----------
fig, ax = plt.subplots(figsize=(12, 5))
pivot = df_factorial.groupby(['Selection', 'Crossover'])['Fitness'].max().unstack()
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
fig.colorbar(im, ax=ax, label='Best Fitness')
ax.set_title('Best Fitness -- Selection x Crossover  (best over all mutations)', fontsize=13, pad=12)
ax.set_xlabel('Crossover Method')
ax.set_ylabel('Selection Method')
plt.tight_layout()
path1 = os.path.join(OUTPUT_DIR, "heatmap_sel_cx.png")
fig.savefig(path1, dpi=150)
plt.close(fig)
print(f"  [OK] {path1}")

# ---------- Plot 2: Grouped bar — mean fitness by mutation method per selection ----------
fig, ax = plt.subplots(figsize=(12, 6))
grouped = df_factorial.groupby(['Selection', 'Mutation'])['Fitness'].mean().unstack()
x = np.arange(len(grouped.index))
width = 0.12
for i, mut in enumerate(grouped.columns):
    ax.bar(x + i * width, grouped[mut], width, label=mut, color=COLORS[i % len(COLORS)])
ax.set_xticks(x + width * (len(grouped.columns) - 1) / 2)
ax.set_xticklabels(grouped.index, fontsize=11)
ax.set_ylabel('Mean Fitness', fontsize=11)
ax.set_title('Mean Fitness by Mutation Method per Selection Strategy', fontsize=13, pad=12)
ax.legend(title='Mutation', fontsize=8, title_fontsize=9, ncol=3, loc='lower right')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
path2 = os.path.join(OUTPUT_DIR, "bar_mutation_by_selection.png")
fig.savefig(path2, dpi=150)
plt.close(fig)
print(f"  [OK] {path2}")

# ---------- Plot 3: Grouped bar — mean fitness by crossover method per selection ----------
fig, ax = plt.subplots(figsize=(14, 6))
grouped_cx = df_factorial.groupby(['Selection', 'Crossover'])['Fitness'].mean().unstack()
x = np.arange(len(grouped_cx.index))
width = 0.12
for i, cx in enumerate(grouped_cx.columns):
    ax.bar(x + i * width, grouped_cx[cx], width, label=cx, color=COLORS[i % len(COLORS)])
ax.set_xticks(x + width * (len(grouped_cx.columns) - 1) / 2)
ax.set_xticklabels(grouped_cx.index, fontsize=11)
ax.set_ylabel('Mean Fitness', fontsize=11)
ax.set_title('Mean Fitness by Crossover Method per Selection Strategy', fontsize=13, pad=12)
ax.legend(title='Crossover', fontsize=8, title_fontsize=9, ncol=3, loc='lower right')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
path3 = os.path.join(OUTPUT_DIR, "bar_crossover_by_selection.png")
fig.savefig(path3, dpi=150)
plt.close(fig)
print(f"  [OK] {path3}")

# ---------- Plot 4: Generation sweep — line chart ----------
fig, ax1 = plt.subplots(figsize=(8, 5))
ax1.plot(df_gen['Generations'], df_gen['Fitness'], 'o-', color='#2ecc71', linewidth=2, markersize=8, label='Fitness')
ax1.set_xlabel('Generations', fontsize=11)
ax1.set_ylabel('Fitness', color='#2ecc71', fontsize=11)
ax1.tick_params(axis='y', labelcolor='#2ecc71')

ax2 = ax1.twinx()
ax2.plot(df_gen['Generations'], df_gen['Runtime_s'], 's--', color='#e74c3c', linewidth=2, markersize=8, label='Runtime (s)')
ax2.set_ylabel('Runtime (s)', color='#e74c3c', fontsize=11)
ax2.tick_params(axis='y', labelcolor='#e74c3c')

ax1.set_title('Generation Count vs Fitness & Runtime', fontsize=13, pad=12)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='center right')
ax1.grid(alpha=0.3)
plt.tight_layout()
path4 = os.path.join(OUTPUT_DIR, "generation_sweep.png")
fig.savefig(path4, dpi=150)
plt.close(fig)
print(f"  [OK] {path4}")

# ---------- Plot 5: Mutation rate sweep — line chart ----------
fig, ax1 = plt.subplots(figsize=(8, 5))
ax1.plot(df_mr['MutationRate'], df_mr['Fitness'], 'o-', color='#3498db', linewidth=2, markersize=8, label='Fitness')
ax1.set_xlabel('Mutation Rate', fontsize=11)
ax1.set_ylabel('Fitness', color='#3498db', fontsize=11)
ax1.tick_params(axis='y', labelcolor='#3498db')

ax2 = ax1.twinx()
ax2.plot(df_mr['MutationRate'], df_mr['Runtime_s'], 's--', color='#f39c12', linewidth=2, markersize=8, label='Runtime (s)')
ax2.set_ylabel('Runtime (s)', color='#f39c12', fontsize=11)
ax2.tick_params(axis='y', labelcolor='#f39c12')

ax1.set_title('Mutation Rate vs Fitness & Runtime', fontsize=13, pad=12)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='center right')
ax1.grid(alpha=0.3)
plt.tight_layout()
path5 = os.path.join(OUTPUT_DIR, "mutation_rate_sweep.png")
fig.savefig(path5, dpi=150)
plt.close(fig)
print(f"  [OK] {path5}")

# ---------- Plot 6: Top 10 best configurations ----------
top10 = df_factorial.nlargest(10, 'Fitness')
fig, ax = plt.subplots(figsize=(14, 6))
labels_top = [f"{r['Selection']}\n{r['Crossover']}\n{r['Mutation']}" for _, r in top10.iterrows()]
bars = ax.barh(range(len(top10)), top10['Fitness'], color=COLORS * 2)
ax.set_yticks(range(len(top10)))
ax.set_yticklabels(labels_top, fontsize=8)
ax.set_xlabel('Fitness', fontsize=11)
ax.set_title('Top 10 GA Configurations by Fitness', fontsize=13, pad=12)
for i, (val, interest) in enumerate(zip(top10['Fitness'], top10['Interest'])):
    ax.text(val + 0.1, i, f'  fit={val:.1f}, int={interest:.1f}', va='center', fontsize=8)
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()
plt.tight_layout()
path6 = os.path.join(OUTPUT_DIR, "top10_configs.png")
fig.savefig(path6, dpi=150)
plt.close(fig)
print(f"  [OK] {path6}")

# ---------- Plot 7: Runtime heatmap  — Selection × Crossover ----------
fig, ax = plt.subplots(figsize=(12, 5))
pivot_rt = df_factorial.groupby(['Selection', 'Crossover'])['Runtime_s'].mean().unstack()
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
fig.colorbar(im, ax=ax, label='Mean Runtime (s)')
ax.set_title('Mean Runtime (s) -- Selection x Crossover', fontsize=13, pad=12)
ax.set_xlabel('Crossover Method')
ax.set_ylabel('Selection Method')
plt.tight_layout()
path7 = os.path.join(OUTPUT_DIR, "heatmap_runtime.png")
fig.savefig(path7, dpi=150)
plt.close(fig)
print(f"  [OK] {path7}")


# ═════════════════════════════════════════════════════════════════════════════
# 5.  SUMMARY TABLE  (printed to console)
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SUMMARY -- Top 15 Configurations (by Fitness)")
print("=" * 70)
top15 = df_factorial.nlargest(15, 'Fitness')
print(top15.to_string(index=False))

print("\n" + "=" * 70)
print("Generation Sweep Results")
print("=" * 70)
print(df_gen.to_string(index=False))

print("\n" + "=" * 70)
print("Mutation Rate Sweep Results")
print("=" * 70)
print(df_mr.to_string(index=False))

print("\n[DONE] All done! Results & plots saved in:", OUTPUT_DIR)
