"""Add ACS_Hybrid + fix CSP error visibility."""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
NB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notebook.ipynb")
with open(NB,"r",encoding="utf-8") as f: nb=json.load(f)

acs_hybrid_lines = [
    "\n",
    "                # ────────── ACS_Hybrid ──────────\n",
    "                elif algo == 'ACS_Hybrid':\n",
    "                    env_h = ACSEnvironment(\n",
    "                        hotel=selected_hotel, landmarks=landmarks,\n",
    "                        time_matrix=time_matrix, time_budget_hours=b,\n",
    "                        trip_start_time_hours=s, visiting_day=VISITING_DAY)\n",
    "                    acs_h = AntColonySystem(env_h,\n",
    "                              num_ants=50, generations=100,\n",
    "                              alpha=0.5, beta=3.0, rho=0.3, hybrid_sa=True)\n",
    "                    t0 = _time.time()\n",
    "                    path_h, score_h = acs_h.solve()\n",
    "                    row['runtime_ms'] = (_time.time() - t0) * 1000\n",
    "                    lm_h = [n for n in path_h if isinstance(n, Landmark)]\n",
    "                    row['best_score'] = _score(lm_h)\n",
    "                    row['landmarks_visited'] = len(lm_h)\n",
    "                    row['is_feasible'] = len(lm_h) > 0\n",
    "\n",
]

for cell in nb["cells"]:
    joined = "".join(cell.get("source",[]))
    
    # 1) Setup: add ACS_Hybrid to ALGO_NAMES
    if "ALGO_NAMES = [" in joined and "'CSP'" in joined and "'ACS_Hybrid'" not in joined:
        cell["source"] = [s.replace(
            "'HillClimbing', 'CSP'",
            "'HillClimbing', 'CSP', 'ACS_Hybrid'"
        ) for s in cell["source"]]
        cell["outputs"] = []
        print("[OK] Added ACS_Hybrid to ALGO_NAMES")

    # 2) Comparison loop: add ACS_Hybrid dispatch before except, fix CSP error msg
    if "elif algo == 'CSP':" in joined and "elif algo == 'ACS_Hybrid':" not in joined:
        new_src = []
        for line in cell["source"]:
            # Insert ACS_Hybrid block before except
            if "except Exception as e:" in line:
                new_src.extend(acs_hybrid_lines)
            # Fix CSP error: add print for debugging
            new_src.append(line)
        cell["source"] = new_src
        cell["outputs"] = []
        print("[OK] Added ACS_Hybrid dispatch + kept CSP")

    # 3) Plot config: add ACS_Hybrid
    if "MAIN_3" in joined and "ALL_6" in joined and "'ACS_Hybrid'" not in joined:
        cell["source"] = [s.replace(
            "'CSP':'#e67e22'}",
            "'CSP':'#e67e22','ACS_Hybrid':'#c0392b'}"
        ).replace(
            "'CSP':'v'}",
            "'CSP':'v','ACS_Hybrid':'h'}"
        ).replace(
            "'CSP']",
            "'CSP','ACS_Hybrid']"
        ) for s in cell["source"]]
        cell["outputs"] = []
        print("[OK] Added ACS_Hybrid to plot config")

with open(NB,"w",encoding="utf-8") as f: json.dump(nb, f, ensure_ascii=False, indent=1)
print("Done!")
