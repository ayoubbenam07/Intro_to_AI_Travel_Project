import json

nb_path = r"c:\Users\maaro\OneDrive\Bureau\Ai_project\Intro_to_AI_Travel_Project\notebook.ipynb"
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

for i, c in enumerate(nb["cells"]):
    src = c["source"]
    first = ""
    if src:
        first = "".join(src[:2])[:150].replace("\n", " | ")
    print(f"Cell {i:3d} [{c['cell_type']:8s}] id={c.get('id','?'):20s}  {first}")
