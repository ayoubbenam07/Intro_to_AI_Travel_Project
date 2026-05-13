import json
nb = json.load(open('notebook.ipynb', 'r', encoding='utf-8'))
for i, c in enumerate(nb['cells']):
    if 105 <= i <= 120:
        src = "".join(c["source"])[:80].replace("\n", " ")
        print(f"{i}: {c['cell_type']:8} | {src}")
