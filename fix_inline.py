"""Fix matplotlib inline for Jupyter."""
import json, os
NB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notebook.ipynb")
with open(NB,"r",encoding="utf-8") as f: nb=json.load(f)

for cell in nb["cells"]:
    joined = "".join(cell.get("source",[]))
    if "MAIN_3" in joined and "ALL_6" in joined and "COLORS" in joined:
        cell["source"].insert(0, "%matplotlib inline\n")
        cell["outputs"] = []
        print("[OK] Added %matplotlib inline to plot config cell")
        break

with open(NB,"w",encoding="utf-8") as f: json.dump(nb, f, ensure_ascii=False, indent=1)
print("Done!")
