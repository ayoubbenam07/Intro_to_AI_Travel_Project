"""Fix: insert CSP dispatch into comparison loop."""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
NB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notebook.ipynb")
with open(NB,"r",encoding="utf-8") as f: nb=json.load(f)

csp_lines = [
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

for cell in nb["cells"]:
    joined = "".join(cell.get("source",[]))
    if "elif algo == 'HillClimbing':" in joined and "elif algo == 'CSP':" not in joined:
        new_src = []
        for i, line in enumerate(cell["source"]):
            new_src.append(line)
            # Insert CSP block right after the last HillClimbing line (before except)
            if "except Exception as e:" in line:
                # Insert CSP block BEFORE the except line
                new_src = new_src[:-1] + csp_lines + [line]
        cell["source"] = new_src
        cell["outputs"] = []
        print("[OK] Inserted CSP dispatch before 'except' block")
        break

with open(NB,"w",encoding="utf-8") as f: json.dump(nb, f, ensure_ascii=False, indent=1)
print("Done!")
