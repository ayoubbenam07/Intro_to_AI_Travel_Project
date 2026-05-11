from __future__ import annotations

import os
import sys
import time
import gc
import itertools
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

TESTS_DIR    = os.path.dirname(os.path.abspath(__file__))   
project_root = os.path.dirname(TESTS_DIR)                   
sys.path.append(project_root)

from Algorithms.CSP_Solver import TravelCSP
from core.Problem_LocalSearch import TravelProblem_LocalSearch
from utils import data_loader

OUT = os.path.join(TESTS_DIR, "CSP-test-results")
os.makedirs(OUT, exist_ok=True)

def savefig(name: str):
    path = os.path.join(OUT, name)
    plt.savefig(path, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"  ✓  {name}")

sns.set_theme(style="whitegrid", font_scale=1.05)
PALETTE = sns.color_palette("tab10")

print("Loading data …")
landmarks   = data_loader.get_landmarks()
hotels      = data_loader.get_hotels()
time_matrix = data_loader.get_time_matrix()

ALL_DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
for lm in landmarks:
    for day in ALL_DAYS:
        if day not in lm.opening_hours:
            lm.opening_hours[day] = [0] * 24
            
_sample_lm   = next(iter(landmarks))
DAYS         = sorted(_sample_lm.opening_hours.keys())
DAY_LABELS   = [d.capitalize() for d in DAYS]
BUDGET      = 8
DAY_FIXED   = "fri"

def make_problem(hotel, day, budget_h, type_filter=None):
    return TravelProblem_LocalSearch(landmarks, {
        "hotel"          : hotel,
        "Travel_day"     : day,
        "Travel_Time"    : budget_h,
        "type_filter"    : type_filter,
        "time_matrix"    : time_matrix,
        "trip_start_time": 8,
    })

def run_csp(problem, inference="fc", var_h="mrv", val_h="lcv",
            tl=30.0, quota=None):
    solver = TravelCSP(problem,
                       inference_method=inference,
                       var_heuristic=var_h,
                       val_heuristic=val_h,
                       time_limit_s=tl,
                       type_quota=quota or {})
    t0       = time.time()
    solution = solver.solve()
    elapsed  = time.time() - t0
    return {
        "solution" : solution,
        "score"    : sum(lm.interest_score for lm in solution),
        "visited"  : len(solution),
        "assigns"  : solver.nassigns,
        "time_sec" : round(elapsed, 4),
        "timed_out": solver._timed_out,
    }


print("\n── Test A: All hotels × all days ──")

n_h, n_d    = len(hotels), len(DAYS)
score_mx    = np.zeros((n_h, n_d))
runtime_mx  = np.zeros((n_h, n_d))
assign_mx   = np.zeros((n_h, n_d))

landmark_counter: Counter = Counter()
type_counter:     Counter = Counter()
visited_counts:   list    = []
hotel_solutions:  dict    = {h.name: set() for h in hotels}

hotel_names = [h.name for h in hotels]

for i, hotel in enumerate(hotels):
    for j, day in enumerate(DAYS):
        print(f"  {hotel.name[:20]:20s} / {day}", end=" … ", flush=True)
        try:
            r = run_csp(make_problem(hotel, day, BUDGET), tl=25.0)
            score_mx[i, j]   = r["score"]
            runtime_mx[i, j] = r["time_sec"]
            assign_mx[i, j]  = r["assigns"]
            visited_counts.append(r["visited"])
            for lm in r["solution"]:
                landmark_counter[lm.name] += 1
                type_counter[lm.landmark_type] += 1
                hotel_solutions[hotel.name].add(lm.name)
            print(f"score={r['score']:.1f}  n={r['visited']}  t={r['time_sec']}s")
        except Exception as e:
            print(f"ERROR: {e}")

    gc.collect()

print("\n  Computing averages across all hotels for each day...\n")

avg_scores = score_mx.mean(axis=0)  
std_scores = score_mx.std(axis=0)

fig, ax = plt.subplots(figsize=(10, 5))
x_pos = range(n_d)
bars = ax.bar(x_pos, avg_scores, yerr=std_scores, 
              color=PALETTE[:n_d], edgecolor="white", capsize=5)
ax.bar_label(bars, fmt='%.1f', padding=3, fontsize=10)
ax.set_xticks(x_pos)
ax.set_xticklabels(DAY_LABELS)
ax.set_ylabel("Average Interest Score (across all hotels)")
ax.set_title("CSP — Average Score by Day  |  ±1 std dev across hotels  (8 h, FC+MRV+LCV)",
             fontweight="bold", pad=12)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout(); savefig("1_avg_score_by_day.png")


print("\n  Average Interest Score by Day:")
for day, avg, std in zip(DAY_LABELS, avg_scores, std_scores):
    print(f"    {day:5s} : {avg:.1f} ± {std:.1f}")


avg_runtimes = runtime_mx.mean(axis=0)  
std_runtimes = runtime_mx.std(axis=0)

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(x_pos, avg_runtimes, yerr=std_runtimes,
              color=sns.color_palette("Reds", n_d), edgecolor="white", capsize=5)
ax.bar_label(bars, fmt='%.2f', padding=3, fontsize=10)
ax.set_xticks(x_pos)
ax.set_xticklabels(DAY_LABELS)
ax.set_ylabel("Average Runtime (seconds, across all hotels)")
ax.set_title("CSP — Average Runtime by Day  |  ±1 std dev across hotels\n"
             "CON: runtime varies significantly with opening-hour patterns",
             fontweight="bold", pad=12)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout(); savefig("2_avg_runtime_by_day.png")

print("\n  Average Runtime by Day:")
for day, avg, std in zip(DAY_LABELS, avg_runtimes, std_runtimes):
    print(f"    {day:5s} : {avg:.3f}s ± {std:.3f}s")


top_n  = min(20, len(landmark_counter))
top_lm = landmark_counter.most_common(top_n)
names, counts = zip(*top_lm)

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(list(reversed(names)), list(reversed(counts)),
               color=PALETTE[:top_n], edgecolor="white")
ax.bar_label(bars, padding=3, fontsize=9)
ax.set_xlabel("Times recommended  (across all hotels × all days)")
ax.set_title(f"CSP — Top {top_n} Most Recommended Landmarks  (all hotels × all days)\n"
             "PRO: consistently surfaces the same high-value landmarks",
             fontweight="bold")
ax.set_xlim(0, max(counts) * 1.15)
plt.tight_layout(); savefig("4_landmark_frequency.png")

print("\n── Test C: Heuristic comparison ──")

combos = list(itertools.product(["fc", "mac"], ["mrv", "none"], ["lcv", "none"]))
heuristic_rows = []
for inf, var, val in combos:
    label = f"{inf.upper()}|{var.upper()}|{val.upper()}"
    print(f"  {label:18s}", end=" … ", flush=True)
    try:
        r = run_csp(make_problem(hotels[0], DAY_FIXED, BUDGET),
                    inference=inf, var_h=var, val_h=val, tl=30.0)
        heuristic_rows.append({
            "label"   : label,
            "score"   : r["score"],
            "assigns" : r["assigns"],
            "time_sec": r["time_sec"],
            "visited" : r["visited"],
        })
        print(f"score={r['score']:.1f}  assigns={r['assigns']}  t={r['time_sec']}s")
    except Exception as e:
        print(f"ERROR: {e}")

df_h = pd.DataFrame(heuristic_rows)

if not df_h.empty:
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for ax, (col, ylabel, cmap, fmt) in zip(axes, [
        ("score",    "Total Score",           "YlGnBu",  ".1f"),
        ("assigns",  "Assignments Made",      "Oranges", ".0f"),
        ("time_sec", "Runtime (s)",           "Reds",    ".3f"),
    ]):
        colors = sns.color_palette(cmap, len(df_h))
        bars   = ax.bar(df_h["label"], df_h[col], color=colors, edgecolor="white")
        ax.bar_label(bars,
                     labels=[f"{v:{fmt}}" for v in df_h[col]],
                     padding=3, fontsize=8)
        ax.set_title(ylabel, fontweight="bold")
        ax.set_xlabel("Inference | Var | Val heuristic")
        ax.set_ylabel(ylabel)
        ax.tick_params(axis="x", rotation=40)

    plt.suptitle(
        f"CSP — Heuristic Comparison  ({hotels[0].name}, {DAY_FIXED}, {BUDGET}h)\n"
        "PRO: MRV+LCV minimise assignments  "
        "CON: MAC overhead not always worth it",
        fontweight="bold", y=1.03)
    plt.tight_layout(); savefig("3_heuristic_comparison.png")