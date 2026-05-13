"""
Patch Section 6 visualization with comprehensive plots:
  - Line charts (score + runtime)
  - Grouped bar charts (score + runtime)
  - Heatmaps (score + runtime)
  - Radar chart
All for Main 3 separately, then All 6 together.
"""
import json, uuid, os

NB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notebook.ipynb")
uid = lambda: uuid.uuid4().hex[:8]
md  = lambda src: {"cell_type":"markdown","id":uid(),"metadata":{},"source":src}
code = lambda src: {"cell_type":"code","execution_count":None,"id":uid(),"metadata":{},"outputs":[],"source":src}

NEW_CELLS = [
    # ══════════════════════════════════════════════════════════════
    md([
        "## 6.2 - Visualization\n",
    ]),

    # ── Shared config ──
    code([
        "# ── Plot Configuration ──\n",
        "COLORS  = {'Greedy':'#2ecc71','SA':'#e74c3c','GA':'#3498db',\n",
        "           'ACS':'#9b59b6','ABC':'#f39c12','HillClimbing':'#1abc9c'}\n",
        "MARKERS = {'Greedy':'o','SA':'s','GA':'^','ACS':'D','ABC':'P','HillClimbing':'X'}\n",
        "MAIN_3  = ['Greedy','SA','GA']\n",
        "ALL_6   = ['Greedy','SA','GA','ACS','ABC','HillClimbing']\n",
    ]),

    # ══════════════════════════════════════════════════════════════
    # MAIN 3
    # ══════════════════════════════════════════════════════════════
    md([
        "### 6.2.1 — Main 3 Algorithms (Greedy, SA, GA)\n",
    ]),

    # ── Main3 Line: Score ──
    code([
        "# ── Main 3: Line Chart — Fitness vs Budget ──\n",
        "fig, axes = plt.subplots(len(START_TIMES), 1, figsize=(12, 5*len(START_TIMES)), sharex=True)\n",
        "if len(START_TIMES)==1: axes=[axes]\n",
        "for idx, st in enumerate(START_TIMES):\n",
        "    ax = axes[idx]\n",
        "    sub = df[df['start_time']==st]\n",
        "    for algo in MAIN_3:\n",
        "        adf = sub[sub['algorithm']==algo].sort_values('budget')\n",
        "        ax.plot(adf['budget'], adf['best_score'], color=COLORS[algo],\n",
        "                marker=MARKERS[algo], label=algo, linewidth=2.5, markersize=8)\n",
        "    ax.set_title(f'Start = {st}:00', fontsize=14, fontweight='bold')\n",
        "    ax.set_ylabel('Fitness Score', fontsize=12)\n",
        "    ax.grid(True, alpha=0.3); ax.legend(fontsize=11)\n",
        "axes[-1].set_xlabel('Budget (hours)', fontsize=12)\n",
        "fig.suptitle('Main 3 — Fitness vs Budget', fontsize=16, fontweight='bold')\n",
        "plt.tight_layout(rect=[0,0,1,0.96])\n",
        "fig.savefig(os.path.join(OUTPUT_DIR,'main3_line_score.png'), dpi=150, bbox_inches='tight')\n",
        "plt.show(); plt.close(fig)\n",
    ]),

    # ── Main3 Line: Runtime ──
    code([
        "# ── Main 3: Line Chart — Runtime vs Budget ──\n",
        "fig, axes = plt.subplots(len(START_TIMES), 1, figsize=(12, 5*len(START_TIMES)), sharex=True)\n",
        "if len(START_TIMES)==1: axes=[axes]\n",
        "for idx, st in enumerate(START_TIMES):\n",
        "    ax = axes[idx]\n",
        "    sub = df[df['start_time']==st]\n",
        "    for algo in MAIN_3:\n",
        "        adf = sub[sub['algorithm']==algo].sort_values('budget')\n",
        "        ax.plot(adf['budget'], adf['runtime_ms'], color=COLORS[algo],\n",
        "                marker=MARKERS[algo], label=algo, linewidth=2.5, markersize=8)\n",
        "    ax.set_title(f'Start = {st}:00', fontsize=14, fontweight='bold')\n",
        "    ax.set_ylabel('Runtime (ms)', fontsize=12)\n",
        "    ax.set_yscale('log')\n",
        "    ax.grid(True, alpha=0.3); ax.legend(fontsize=11)\n",
        "axes[-1].set_xlabel('Budget (hours)', fontsize=12)\n",
        "fig.suptitle('Main 3 — Runtime vs Budget', fontsize=16, fontweight='bold')\n",
        "plt.tight_layout(rect=[0,0,1,0.96])\n",
        "fig.savefig(os.path.join(OUTPUT_DIR,'main3_line_runtime.png'), dpi=150, bbox_inches='tight')\n",
        "plt.show(); plt.close(fig)\n",
    ]),

    # ── Main3 Grouped Bar: Score ──
    code([
        "# ── Main 3: Grouped Bar Chart — Fitness by Budget ──\n",
        "fig, axes = plt.subplots(len(START_TIMES), 1, figsize=(12, 5*len(START_TIMES)), sharex=True)\n",
        "if len(START_TIMES)==1: axes=[axes]\n",
        "bar_w = 0.25\n",
        "for idx, st in enumerate(START_TIMES):\n",
        "    ax = axes[idx]\n",
        "    sub = df[df['start_time']==st]\n",
        "    x = np.arange(len(BUDGETS))\n",
        "    for j, algo in enumerate(MAIN_3):\n",
        "        adf = sub[sub['algorithm']==algo].sort_values('budget')\n",
        "        offset = (j - len(MAIN_3)/2 + 0.5) * bar_w\n",
        "        ax.bar(x + offset, adf['best_score'].values, bar_w,\n",
        "               color=COLORS[algo], label=algo, edgecolor='white', linewidth=0.5)\n",
        "    ax.set_title(f'Start = {st}:00', fontsize=14, fontweight='bold')\n",
        "    ax.set_ylabel('Fitness Score', fontsize=12)\n",
        "    ax.set_xticks(x); ax.set_xticklabels([f'{b}h' for b in BUDGETS])\n",
        "    ax.grid(True, alpha=0.2, axis='y'); ax.legend(fontsize=11)\n",
        "axes[-1].set_xlabel('Budget', fontsize=12)\n",
        "fig.suptitle('Main 3 — Fitness Comparison (Bar)', fontsize=16, fontweight='bold')\n",
        "plt.tight_layout(rect=[0,0,1,0.96])\n",
        "fig.savefig(os.path.join(OUTPUT_DIR,'main3_bar_score.png'), dpi=150, bbox_inches='tight')\n",
        "plt.show(); plt.close(fig)\n",
    ]),

    # ── Main3 Grouped Bar: Runtime ──
    code([
        "# ── Main 3: Grouped Bar Chart — Runtime by Budget ──\n",
        "fig, axes = plt.subplots(len(START_TIMES), 1, figsize=(12, 5*len(START_TIMES)), sharex=True)\n",
        "if len(START_TIMES)==1: axes=[axes]\n",
        "bar_w = 0.25\n",
        "for idx, st in enumerate(START_TIMES):\n",
        "    ax = axes[idx]\n",
        "    sub = df[df['start_time']==st]\n",
        "    x = np.arange(len(BUDGETS))\n",
        "    for j, algo in enumerate(MAIN_3):\n",
        "        adf = sub[sub['algorithm']==algo].sort_values('budget')\n",
        "        offset = (j - len(MAIN_3)/2 + 0.5) * bar_w\n",
        "        ax.bar(x + offset, adf['runtime_ms'].values, bar_w,\n",
        "               color=COLORS[algo], label=algo, edgecolor='white', linewidth=0.5)\n",
        "    ax.set_title(f'Start = {st}:00', fontsize=14, fontweight='bold')\n",
        "    ax.set_ylabel('Runtime (ms)', fontsize=12)\n",
        "    ax.set_yscale('log')\n",
        "    ax.set_xticks(x); ax.set_xticklabels([f'{b}h' for b in BUDGETS])\n",
        "    ax.grid(True, alpha=0.2, axis='y'); ax.legend(fontsize=11)\n",
        "axes[-1].set_xlabel('Budget', fontsize=12)\n",
        "fig.suptitle('Main 3 — Runtime Comparison (Bar)', fontsize=16, fontweight='bold')\n",
        "plt.tight_layout(rect=[0,0,1,0.96])\n",
        "fig.savefig(os.path.join(OUTPUT_DIR,'main3_bar_runtime.png'), dpi=150, bbox_inches='tight')\n",
        "plt.show(); plt.close(fig)\n",
    ]),

    # ══════════════════════════════════════════════════════════════
    # ALL 6
    # ══════════════════════════════════════════════════════════════
    md([
        "### 6.2.2 — All 6 Algorithms\n",
    ]),

    # ── All6 Line: Score ──
    code([
        "# ── All 6: Line Chart — Fitness vs Budget ──\n",
        "fig, axes = plt.subplots(len(START_TIMES), 1, figsize=(12, 5*len(START_TIMES)), sharex=True)\n",
        "if len(START_TIMES)==1: axes=[axes]\n",
        "for idx, st in enumerate(START_TIMES):\n",
        "    ax = axes[idx]\n",
        "    sub = df[df['start_time']==st]\n",
        "    for algo in ALL_6:\n",
        "        adf = sub[sub['algorithm']==algo].sort_values('budget')\n",
        "        ax.plot(adf['budget'], adf['best_score'], color=COLORS[algo],\n",
        "                marker=MARKERS[algo], label=algo, linewidth=2.5, markersize=8)\n",
        "    ax.set_title(f'Start = {st}:00', fontsize=14, fontweight='bold')\n",
        "    ax.set_ylabel('Fitness Score', fontsize=12)\n",
        "    ax.grid(True, alpha=0.3); ax.legend(fontsize=10)\n",
        "axes[-1].set_xlabel('Budget (hours)', fontsize=12)\n",
        "fig.suptitle('All 6 — Fitness vs Budget', fontsize=16, fontweight='bold')\n",
        "plt.tight_layout(rect=[0,0,1,0.96])\n",
        "fig.savefig(os.path.join(OUTPUT_DIR,'all6_line_score.png'), dpi=150, bbox_inches='tight')\n",
        "plt.show(); plt.close(fig)\n",
    ]),

    # ── All6 Line: Runtime ──
    code([
        "# ── All 6: Line Chart — Runtime vs Budget ──\n",
        "fig, axes = plt.subplots(len(START_TIMES), 1, figsize=(12, 5*len(START_TIMES)), sharex=True)\n",
        "if len(START_TIMES)==1: axes=[axes]\n",
        "for idx, st in enumerate(START_TIMES):\n",
        "    ax = axes[idx]\n",
        "    sub = df[df['start_time']==st]\n",
        "    for algo in ALL_6:\n",
        "        adf = sub[sub['algorithm']==algo].sort_values('budget')\n",
        "        ax.plot(adf['budget'], adf['runtime_ms'], color=COLORS[algo],\n",
        "                marker=MARKERS[algo], label=algo, linewidth=2.5, markersize=8)\n",
        "    ax.set_title(f'Start = {st}:00', fontsize=14, fontweight='bold')\n",
        "    ax.set_ylabel('Runtime (ms)', fontsize=12)\n",
        "    ax.set_yscale('log')\n",
        "    ax.grid(True, alpha=0.3); ax.legend(fontsize=10)\n",
        "axes[-1].set_xlabel('Budget (hours)', fontsize=12)\n",
        "fig.suptitle('All 6 — Runtime vs Budget', fontsize=16, fontweight='bold')\n",
        "plt.tight_layout(rect=[0,0,1,0.96])\n",
        "fig.savefig(os.path.join(OUTPUT_DIR,'all6_line_runtime.png'), dpi=150, bbox_inches='tight')\n",
        "plt.show(); plt.close(fig)\n",
    ]),

    # ── All6 Grouped Bar: Score ──
    code([
        "# ── All 6: Grouped Bar Chart — Fitness by Budget ──\n",
        "fig, axes = plt.subplots(len(START_TIMES), 1, figsize=(14, 5*len(START_TIMES)), sharex=True)\n",
        "if len(START_TIMES)==1: axes=[axes]\n",
        "bar_w = 0.13\n",
        "for idx, st in enumerate(START_TIMES):\n",
        "    ax = axes[idx]\n",
        "    sub = df[df['start_time']==st]\n",
        "    x = np.arange(len(BUDGETS))\n",
        "    for j, algo in enumerate(ALL_6):\n",
        "        adf = sub[sub['algorithm']==algo].sort_values('budget')\n",
        "        offset = (j - len(ALL_6)/2 + 0.5) * bar_w\n",
        "        ax.bar(x + offset, adf['best_score'].values, bar_w,\n",
        "               color=COLORS[algo], label=algo, edgecolor='white', linewidth=0.5)\n",
        "    ax.set_title(f'Start = {st}:00', fontsize=14, fontweight='bold')\n",
        "    ax.set_ylabel('Fitness Score', fontsize=12)\n",
        "    ax.set_xticks(x); ax.set_xticklabels([f'{b}h' for b in BUDGETS])\n",
        "    ax.grid(True, alpha=0.2, axis='y'); ax.legend(fontsize=9, ncol=3)\n",
        "axes[-1].set_xlabel('Budget', fontsize=12)\n",
        "fig.suptitle('All 6 — Fitness Comparison (Bar)', fontsize=16, fontweight='bold')\n",
        "plt.tight_layout(rect=[0,0,1,0.96])\n",
        "fig.savefig(os.path.join(OUTPUT_DIR,'all6_bar_score.png'), dpi=150, bbox_inches='tight')\n",
        "plt.show(); plt.close(fig)\n",
    ]),

    # ── All6 Grouped Bar: Runtime ──
    code([
        "# ── All 6: Grouped Bar Chart — Runtime by Budget ──\n",
        "fig, axes = plt.subplots(len(START_TIMES), 1, figsize=(14, 5*len(START_TIMES)), sharex=True)\n",
        "if len(START_TIMES)==1: axes=[axes]\n",
        "bar_w = 0.13\n",
        "for idx, st in enumerate(START_TIMES):\n",
        "    ax = axes[idx]\n",
        "    sub = df[df['start_time']==st]\n",
        "    x = np.arange(len(BUDGETS))\n",
        "    for j, algo in enumerate(ALL_6):\n",
        "        adf = sub[sub['algorithm']==algo].sort_values('budget')\n",
        "        offset = (j - len(ALL_6)/2 + 0.5) * bar_w\n",
        "        ax.bar(x + offset, adf['runtime_ms'].values, bar_w,\n",
        "               color=COLORS[algo], label=algo, edgecolor='white', linewidth=0.5)\n",
        "    ax.set_title(f'Start = {st}:00', fontsize=14, fontweight='bold')\n",
        "    ax.set_ylabel('Runtime (ms)', fontsize=12)\n",
        "    ax.set_yscale('log')\n",
        "    ax.set_xticks(x); ax.set_xticklabels([f'{b}h' for b in BUDGETS])\n",
        "    ax.grid(True, alpha=0.2, axis='y'); ax.legend(fontsize=9, ncol=3)\n",
        "axes[-1].set_xlabel('Budget', fontsize=12)\n",
        "fig.suptitle('All 6 — Runtime Comparison (Bar)', fontsize=16, fontweight='bold')\n",
        "plt.tight_layout(rect=[0,0,1,0.96])\n",
        "fig.savefig(os.path.join(OUTPUT_DIR,'all6_bar_runtime.png'), dpi=150, bbox_inches='tight')\n",
        "plt.show(); plt.close(fig)\n",
    ]),

    # ── Heatmaps ──
    md(["### 6.2.3 — Heatmaps\n",
        "One heatmap per start_time showing algorithm × budget.\n"]),

    # ── Heatmap: Score ──
    code([
        "# ── Heatmap — Fitness (Algorithm × Budget, one per start_time) ──\n",
        "fig, axes = plt.subplots(len(START_TIMES), 1, figsize=(12, 4*len(START_TIMES)))\n",
        "if len(START_TIMES)==1: axes=[axes]\n",
        "for idx, st in enumerate(START_TIMES):\n",
        "    ax = axes[idx]\n",
        "    sub = df[df['start_time']==st]\n",
        "    pivot = sub.pivot_table(index='algorithm', columns='budget',\n",
        "                            values='best_score', aggfunc='first')\n",
        "    pivot = pivot.reindex(ALL_6)\n",
        "    im = ax.imshow(pivot.values, cmap='YlOrRd', aspect='auto')\n",
        "    ax.set_xticks(range(len(BUDGETS))); ax.set_xticklabels([f'{b}h' for b in BUDGETS])\n",
        "    ax.set_yticks(range(len(ALL_6))); ax.set_yticklabels(ALL_6)\n",
        "    ax.set_title(f'Fitness Heatmap — Start = {st}:00', fontsize=14, fontweight='bold')\n",
        "    # Annotate cells with values\n",
        "    for i in range(len(ALL_6)):\n",
        "        for j in range(len(BUDGETS)):\n",
        "            val = pivot.values[i, j]\n",
        "            if not np.isnan(val):\n",
        "                ax.text(j, i, f'{val:.0f}', ha='center', va='center',\n",
        "                        fontsize=9, fontweight='bold',\n",
        "                        color='white' if val > pivot.values.max()*0.6 else 'black')\n",
        "    plt.colorbar(im, ax=ax, shrink=0.8, label='Fitness')\n",
        "fig.suptitle('Fitness Heatmap — Algorithm × Budget', fontsize=16, fontweight='bold')\n",
        "plt.tight_layout(rect=[0,0,1,0.96])\n",
        "fig.savefig(os.path.join(OUTPUT_DIR,'heatmap_score.png'), dpi=150, bbox_inches='tight')\n",
        "plt.show(); plt.close(fig)\n",
    ]),

    # ── Heatmap: Runtime ──
    code([
        "# ── Heatmap — Runtime (Algorithm × Budget, one per start_time) ──\n",
        "fig, axes = plt.subplots(len(START_TIMES), 1, figsize=(12, 4*len(START_TIMES)))\n",
        "if len(START_TIMES)==1: axes=[axes]\n",
        "for idx, st in enumerate(START_TIMES):\n",
        "    ax = axes[idx]\n",
        "    sub = df[df['start_time']==st]\n",
        "    pivot = sub.pivot_table(index='algorithm', columns='budget',\n",
        "                            values='runtime_ms', aggfunc='first')\n",
        "    pivot = pivot.reindex(ALL_6)\n",
        "    # Log scale for heatmap — use log10 of runtime\n",
        "    log_vals = np.log10(pivot.values + 1)\n",
        "    im = ax.imshow(log_vals, cmap='YlGnBu', aspect='auto')\n",
        "    ax.set_xticks(range(len(BUDGETS))); ax.set_xticklabels([f'{b}h' for b in BUDGETS])\n",
        "    ax.set_yticks(range(len(ALL_6))); ax.set_yticklabels(ALL_6)\n",
        "    ax.set_title(f'Runtime Heatmap — Start = {st}:00', fontsize=14, fontweight='bold')\n",
        "    # Annotate cells with actual ms values\n",
        "    for i in range(len(ALL_6)):\n",
        "        for j in range(len(BUDGETS)):\n",
        "            val = pivot.values[i, j]\n",
        "            if not np.isnan(val):\n",
        "                if val >= 1000:\n",
        "                    txt = f'{val/1000:.1f}s'\n",
        "                else:\n",
        "                    txt = f'{val:.0f}ms'\n",
        "                ax.text(j, i, txt, ha='center', va='center',\n",
        "                        fontsize=8, fontweight='bold',\n",
        "                        color='white' if log_vals[i,j] > log_vals.max()*0.6 else 'black')\n",
        "    plt.colorbar(im, ax=ax, shrink=0.8, label='log₁₀(Runtime ms)')\n",
        "fig.suptitle('Runtime Heatmap — Algorithm × Budget', fontsize=16, fontweight='bold')\n",
        "plt.tight_layout(rect=[0,0,1,0.96])\n",
        "fig.savefig(os.path.join(OUTPUT_DIR,'heatmap_runtime.png'), dpi=150, bbox_inches='tight')\n",
        "plt.show(); plt.close(fig)\n",
    ]),

    # ── Radar ──
    md(["### 6.2.4 — Radar Chart\n"]),
    code([
        "# ── Radar Chart — Overall Multi-axis Comparison ──\n",
        "metrics = ['Avg Score', 'Speed', 'Feasibility', 'Coverage']\n",
        "agg = df.groupby('algorithm').agg(\n",
        "    avg_score=('best_score','mean'),\n",
        "    avg_runtime=('runtime_ms','mean'),\n",
        "    feasibility=('is_feasible','mean'),\n",
        "    avg_lm=('landmarks_visited','mean'),\n",
        ").reindex(ALL_6)\n",
        "\n",
        "agg['speed']    = 1.0 / (agg['avg_runtime'] + 1e-9)\n",
        "agg['coverage'] = agg['avg_lm'] / TOTAL_LANDMARKS\n",
        "\n",
        "radar_cols = ['avg_score','speed','feasibility','coverage']\n",
        "normed = agg[radar_cols].copy()\n",
        "for c in radar_cols:\n",
        "    mn, mx = normed[c].min(), normed[c].max()\n",
        "    normed[c] = (normed[c] - mn) / (mx - mn + 1e-9)\n",
        "\n",
        "angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()\n",
        "angles += angles[:1]\n",
        "\n",
        "fig, ax = plt.subplots(figsize=(9,9), subplot_kw=dict(polar=True))\n",
        "for algo in ALL_6:\n",
        "    vals = normed.loc[algo].tolist() + [normed.loc[algo].tolist()[0]]\n",
        "    ax.plot(angles, vals, color=COLORS[algo], linewidth=2.5, label=algo)\n",
        "    ax.fill(angles, vals, color=COLORS[algo], alpha=0.08)\n",
        "\n",
        "ax.set_thetagrids([a*180/np.pi for a in angles[:-1]], metrics, fontsize=13)\n",
        "ax.set_ylim(0, 1.05)\n",
        "ax.set_title('Algorithm Comparison — Radar', fontsize=16,\n",
        "             fontweight='bold', pad=25)\n",
        "ax.legend(loc='upper right', bbox_to_anchor=(1.35,1.1), fontsize=11)\n",
        "plt.tight_layout()\n",
        "fig.savefig(os.path.join(OUTPUT_DIR,'radar_chart.png'), dpi=150, bbox_inches='tight')\n",
        "plt.show(); plt.close(fig)\n",
    ]),

    # ── Summary table ──
    md(["### 6.2.5 — Summary Table\n"]),
    code([
        "# ── Summary Statistics ──\n",
        "summary = df.groupby('algorithm').agg(\n",
        "    avg_score=('best_score','mean'),\n",
        "    std_score=('best_score','std'),\n",
        "    avg_runtime_ms=('runtime_ms','mean'),\n",
        "    avg_landmarks=('landmarks_visited','mean'),\n",
        "    feasibility_pct=('is_feasible', lambda x: f\"{x.mean()*100:.1f}%\"),\n",
        ").reindex(ALL_6).round(2)\n",
        "\n",
        "print('=' * 80)\n",
        "print('ALGORITHM COMPARISON — SUMMARY')\n",
        "print('=' * 80)\n",
        "print(summary.to_string())\n",
        "print()\n",
        "print(f'Total runs: {len(df)}')\n",
        "print(f'Grid: {len(BUDGETS)} budgets × {len(START_TIMES)} start_times × {len(ALL_6)} algorithms')\n",
    ]),
]

# ── PATCH ──
with open(NB_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)
cells = nb["cells"]

viz_start = concl_start = None
for i, cell in enumerate(cells):
    src = "".join(cell.get("source", []))
    if "6.2" in src and "Visualization" in src and cell["cell_type"] == "markdown":
        viz_start = i
    if "6.3" in src and "Conclusions" in src and cell["cell_type"] == "markdown":
        concl_start = i

if viz_start is None:
    print("ERROR: Could not find 6.2 Visualization cell"); exit(1)
end = concl_start if concl_start else len(cells)

print(f"Replacing cells [{viz_start}..{end-1}] with {len(NEW_CELLS)} new cells")
nb["cells"] = cells[:viz_start] + NEW_CELLS + cells[end:]

with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("Done! Comprehensive visualization patched.")
