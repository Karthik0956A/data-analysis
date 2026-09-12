"""
Week 1 – Generate Diagrams
Generates three strategic diagrams for the Customer Churn Prediction project plan:
  1. Data Science Project Lifecycle (circular flow)
  2. Project Timeline Gantt Chart (30-35 hours)
  3. Methodology Flowchart
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import matplotlib.patheffects as pe

# ── Output directory ──────────────────────────────────────────────────────────
os.makedirs("diagrams", exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# 1. Data Science Project Lifecycle – Circular Flow Diagram
# ─────────────────────────────────────────────────────────────────────────────
def draw_lifecycle():
    fig, ax = plt.subplots(figsize=(10, 10), facecolor="#0f1117")
    ax.set_facecolor("#0f1117")
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.axis("off")

    steps = [
        ("Problem\nDefinition", "#6C63FF"),
        ("Data\nCollection", "#FF6584"),
        ("Data\nCleaning", "#43CBFF"),
        ("EDA", "#F9CB28"),
        ("Feature\nEngineering", "#FF8C42"),
        ("Modeling", "#56E39F"),
        ("Evaluation", "#FF6584"),
        ("Deployment", "#6C63FF"),
    ]
    n = len(steps)
    angles = [2 * np.pi * i / n - np.pi / 2 for i in range(n)]
    r = 1.1

    # Draw connecting circle
    theta = np.linspace(0, 2 * np.pi, 300)
    ax.plot(r * np.cos(theta), r * np.sin(theta), color="#ffffff22", lw=1.5, linestyle="--")

    # Draw arrows between nodes
    for i in range(n):
        a1, a2 = angles[i], angles[(i + 1) % n]
        mid_a = (a1 + a2) / 2
        ax.annotate(
            "",
            xy=(r * np.cos(a2), r * np.sin(a2)),
            xytext=(r * np.cos(a1), r * np.sin(a1)),
            arrowprops=dict(arrowstyle="->", color="#ffffff55", lw=1.5,
                            connectionstyle=f"arc3,rad=0.2"),
        )

    # Draw nodes
    for i, (label, color) in enumerate(steps):
        x, y = r * np.cos(angles[i]), r * np.sin(angles[i])
        circle = plt.Circle((x, y), 0.22, color=color, zorder=5)
        ax.add_patch(circle)
        ax.text(x, y, label, ha="center", va="center", fontsize=9,
                fontweight="bold", color="white", zorder=6,
                multialignment="center")

    # Center text
    ax.text(0, 0.08, "Customer", ha="center", va="center", fontsize=14,
            fontweight="bold", color="white")
    ax.text(0, -0.08, "Churn Prediction", ha="center", va="center", fontsize=11,
            color="#aaaaaa")
    ax.text(0, -0.28, "Project Lifecycle", ha="center", va="center", fontsize=9,
            color="#666666")

    ax.set_title("Data Science Project Lifecycle", fontsize=16, color="white",
                 fontweight="bold", pad=20)
    fig.tight_layout()
    fig.savefig("diagrams/project_lifecycle.png", dpi=150, bbox_inches="tight",
                facecolor="#0f1117")
    plt.close(fig)
    print("✓ project_lifecycle.png saved")


# ─────────────────────────────────────────────────────────────────────────────
# 2. Project Timeline – Gantt Chart (30-35 hours)
# ─────────────────────────────────────────────────────────────────────────────
def draw_gantt():
    fig, ax = plt.subplots(figsize=(14, 8), facecolor="#0f1117")
    ax.set_facecolor("#0f1117")

    tasks = [
        ("Problem Definition & Background Research", 0, 3, "#6C63FF"),
        ("Project Objective & Scope Definition",     3, 2, "#FF6584"),
        ("Methodology & Strategy Design",            5, 4, "#43CBFF"),
        ("Data Source Identification",               5, 3, "#F9CB28"),
        ("Tool & Library Selection",                 8, 2, "#FF8C42"),
        ("Timeline & Resource Planning",             9, 2, "#56E39F"),
        ("Flowchart & Diagram Creation",            10, 3, "#FF6584"),
        ("Risk & Challenge Analysis",               11, 2, "#6C63FF"),
        ("Report Writing & Documentation",          13, 4, "#43CBFF"),
        ("Review & Finalization",                   17, 3, "#F9CB28"),
    ]

    yticks, ylabels = [], []
    bar_height = 0.55

    for i, (name, start, duration, color) in enumerate(tasks):
        y = len(tasks) - i - 1
        ax.barh(y, duration, left=start, height=bar_height,
                color=color, alpha=0.85, edgecolor="white", linewidth=0.5)
        ax.text(start + duration / 2, y, f"{duration}h",
                ha="center", va="center", color="white", fontsize=8.5,
                fontweight="bold")
        yticks.append(y)
        ylabels.append(name)

    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels, color="white", fontsize=9)
    ax.set_xlabel("Hours", color="white", fontsize=11)
    ax.set_xlim(0, 21)
    ax.set_xticks(range(0, 22, 2))
    ax.tick_params(colors="white")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#333333")
    ax.spines["bottom"].set_color("#333333")
    ax.set_title("Week 1 Project Timeline  (Total: ~30–35 Hours)", fontsize=15,
                 color="white", fontweight="bold", pad=15)
    ax.axvline(20, color="#FF6584", linestyle="--", alpha=0.6, label="35h mark")
    ax.legend(facecolor="#1a1a2e", labelcolor="white", fontsize=9)
    ax.grid(axis="x", color="#ffffff15", linestyle="--")

    fig.tight_layout()
    fig.savefig("diagrams/timeline_gantt.png", dpi=150, bbox_inches="tight",
                facecolor="#0f1117")
    plt.close(fig)
    print("✓ timeline_gantt.png saved")


# ─────────────────────────────────────────────────────────────────────────────
# 3. Methodology Flowchart
# ─────────────────────────────────────────────────────────────────────────────
def draw_methodology():
    fig, ax = plt.subplots(figsize=(10, 14), facecolor="#0f1117")
    ax.set_facecolor("#0f1117")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis("off")

    boxes = [
        (5, 13.0, "BUSINESS UNDERSTANDING\nDefine churn, KPIs, success criteria", "#6C63FF"),
        (5, 11.2, "DATA COLLECTION\nCRM records, billing, usage logs, support tickets", "#FF6584"),
        (5,  9.4, "DATA CLEANING\nHandle nulls, duplicates, type casting, encoding", "#43CBFF"),
        (5,  7.6, "EXPLORATORY DATA ANALYSIS\nDistributions, correlations, churn rate analysis", "#F9CB28"),
        (5,  5.8, "FEATURE ENGINEERING\nRFM metrics, tenure bins, usage ratios", "#FF8C42"),
        (5,  4.0, "MODEL DEVELOPMENT\nLogistic Reg → Random Forest → XGBoost", "#56E39F"),
        (5,  2.2, "EVALUATION & VALIDATION\nAUC-ROC, F1, Cross-validation, Confusion Matrix", "#FF6584"),
        (5,  0.4, "DEPLOYMENT & MONITORING\nFlask API, Drift detection, Retraining triggers", "#6C63FF"),
    ]

    box_w, box_h = 7.5, 0.95

    for i, (x, y, label, color) in enumerate(boxes):
        rect = FancyBboxPatch((x - box_w / 2, y - box_h / 2), box_w, box_h,
                              boxstyle="round,pad=0.08", facecolor=color + "33",
                              edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        lines = label.split("\n")
        ax.text(x, y + 0.18, lines[0], ha="center", va="center",
                fontsize=10, fontweight="bold", color=color)
        if len(lines) > 1:
            ax.text(x, y - 0.18, lines[1], ha="center", va="center",
                    fontsize=8, color="#cccccc")

        if i < len(boxes) - 1:
            ax.annotate("", xy=(x, boxes[i + 1][1] + box_h / 2),
                        xytext=(x, y - box_h / 2),
                        arrowprops=dict(arrowstyle="->", color="#ffffff66", lw=1.8))

    ax.set_title("Customer Churn Prediction – Methodology Flowchart",
                 fontsize=14, color="white", fontweight="bold", pad=10,
                 y=0.99)
    fig.tight_layout()
    fig.savefig("diagrams/methodology_flowchart.png", dpi=150,
                bbox_inches="tight", facecolor="#0f1117")
    plt.close(fig)
    print("✓ methodology_flowchart.png saved")


if __name__ == "__main__":
    print("Generating Week 1 diagrams...")
    draw_lifecycle()
    draw_gantt()
    draw_methodology()
    print("\nAll Week 1 diagrams generated successfully in diagrams/")
