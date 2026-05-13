import json, sys
sys.stdout.reconfigure(encoding='utf-8')
nb = json.load(open('notebook.ipynb','r',encoding='utf-8'))
for cell in nb['cells']:
    joined = "".join(cell.get("source",[]))
    if "elif algo == 'HillClimbing':" in joined:
        lines = cell["source"]
        for i, line in enumerate(lines):
            if "HillClimbing" in line or "CSP" in line or "except Exception" in line:
                print(f"L{i}: {line.rstrip()}")
        break
