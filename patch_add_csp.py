"""Add CSP to Section 6 comparison loop + plots."""
import json, os
NB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notebook.ipynb")
with open(NB,"r",encoding="utf-8") as f: nb=json.load(f)

for cell in nb["cells"]:
    src = cell.get("source",[])
    joined = "".join(src)

    # 1) Setup cell: add CSP to ALGO_NAMES
    if "ALGO_NAMES = [" in joined and "'HillClimbing'" in joined:
        cell["source"] = [s.replace(
            "ALGO_NAMES = ['Greedy', 'SA', 'GA', 'ACS', 'ABC', 'HillClimbing']",
            "ALGO_NAMES = ['Greedy', 'SA', 'GA', 'ACS', 'ABC', 'HillClimbing', 'CSP']"
        ) for s in src]
        cell["outputs"] = []
        print("  [OK] Patched ALGO_NAMES in setup cell")

    # 2) Comparison loop: add CSP dispatch before the except
    if "elif algo == 'HillClimbing':" in joined and "elif algo == 'CSP':" not in joined:
        csp_block = [
            "\n",
            "                # ────────── CSP ──────────\n",
            "                elif algo == 'CSP':\n",
            "                    csp_obj = TravelCSP(problem_local,\n",
            "                                 inference_method='mac',\n",
            "                                 var_heuristic='mrv',\n",
            "                                 val_heuristic='lcv',\n",
            "                                 time_limit_s=30.0)\n",
            "                    t0 = _time.time()\n",
            "                    res = csp_obj.solve()\n",
            "                    row['runtime_ms'] = (_time.time() - t0) * 1000\n",
            "                    if res:\n",
            "                        row['best_score'] = _score(res)\n",
            "                        row['landmarks_visited'] = len(res)\n",
            "                        row['is_feasible'] = problem_local.valid_state(res)\n",
            "\n",
        ]
        new_src = []
        for line in src:
            new_src.append(line)
            if "row['is_feasible'] = problem_local.valid_state(cand.state)\\n" in line:
                new_src.extend(csp_block)
        cell["source"] = new_src
        cell["outputs"] = []
        print("  [OK] Added CSP dispatch to comparison loop")

    # 3) Plot config: add CSP color/marker, rename ALL_6->ALL_7
    if "MAIN_3" in joined and "ALL_6" in joined and "COLORS" in joined:
        cell["source"] = [s.replace(
            "           'ACS':'#9b59b6','ABC':'#f39c12','HillClimbing':'#1abc9c'}",
            "           'ACS':'#9b59b6','ABC':'#f39c12','HillClimbing':'#1abc9c','CSP':'#e67e22'}"
        ).replace(
            "MARKERS = {'Greedy':'o','SA':'s','GA':'^','ACS':'D','ABC':'P','HillClimbing':'X'}",
            "MARKERS = {'Greedy':'o','SA':'s','GA':'^','ACS':'D','ABC':'P','HillClimbing':'X','CSP':'v'}"
        ).replace(
            "ALL_6   = ['Greedy','SA','GA','ACS','ABC','HillClimbing']",
            "ALL_6   = ['Greedy','SA','GA','ACS','ABC','HillClimbing','CSP']"
        ) for s in src]
        cell["outputs"] = []
        print("  [OK] Added CSP to plot config")

with open(NB,"w",encoding="utf-8") as f: json.dump(nb, f, ensure_ascii=False, indent=1)
print("Done! CSP added to comparison + plots.")
