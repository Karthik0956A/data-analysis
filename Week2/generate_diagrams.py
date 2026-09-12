"""
Week 2 – Generate EDA Diagrams
Creates three strategic diagrams for the EDA & Visualization framework:
  1. EDA Workflow (step-by-step flowchart)
  2. Visualization Types Matrix
  3. Data Types Decision Map
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

os.makedirs("diagrams", exist_ok=True)

DARK_BG = "#0f1117"
COLORS = ["#6C63FF", "#FF6584", "#43CBFF", "#F9CB28", "#FF8C42", "#56E39F",
          "#C77DFF", "#4CC9F0"]


# ─────────────────────────────────────────────────────────────────────────────
# 1. EDA Workflow – Step-by-step flowchart
# ─────────────────────────────────────────────────────────────────────────────
def draw_eda_workflow():
    fig, ax = plt.subplots(figsize=(12, 15), facecolor=DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 15)
    ax.axis("off")

    steps = [
        (6, 14.2, "STEP 1: DATA INGESTION",
         "Load CSV/Excel/DB → pd.read_csv() / SQLAlchemy", "#6C63FF"),
        (6, 12.4, "STEP 2: INITIAL INSPECTION",
         "df.shape, df.dtypes, df.head(), df.describe()", "#FF6584"),
        (6, 10.6, "STEP 3: MISSING VALUE ANALYSIS",
         "df.isnull().sum() → heatmap → imputation strategy", "#43CBFF"),
        (6, 8.8,  "STEP 4: UNIVARIATE ANALYSIS",
         "Histograms, boxplots, KDE plots per feature", "#F9CB28"),
        (6, 7.0,  "STEP 5: BIVARIATE ANALYSIS",
         "Scatter plots, violin plots, feature vs. churn label", "#FF8C42"),
        (6, 5.2,  "STEP 6: MULTIVARIATE ANALYSIS",
         "Correlation heatmap, pair plots, PCA projections", "#56E39F"),
        (6, 3.4,  "STEP 7: OUTLIER DETECTION",
         "IQR method, Z-score, Isolation Forest", "#C77DFF"),
        (6, 1.6,  "STEP 8: INSIGHTS DOCUMENTATION",
         "Summarise findings → hypothesis list → next steps", "#4CC9F0"),
    ]

    bw, bh = 9.5, 1.1
    for i, (x, y, title, desc, color) in enumerate(steps):
        rect = FancyBboxPatch((x - bw / 2, y - bh / 2), bw, bh,
                              boxstyle="round,pad=0.1", facecolor=color + "25",
                              edgecolor=color, linewidth=2.5, zorder=3)
        ax.add_patch(rect)
        # Step number badge
        badge = plt.Circle((x - bw / 2 + 0.45, y), 0.32, color=color, zorder=4)
        ax.add_patch(badge)
        ax.text(x - bw / 2 + 0.45, y, str(i + 1), ha="center", va="center",
                fontsize=9, fontweight="bold", color="white", zorder=5)

        ax.text(x + 0.1, y + 0.22, title, ha="center", va="center",
                fontsize=10.5, fontweight="bold", color=color, zorder=4)
        ax.text(x + 0.1, y - 0.22, desc, ha="center", va="center",
                fontsize=8.5, color="#cccccc", zorder=4)

        if i < len(steps) - 1:
            ax.annotate("", xy=(x, steps[i + 1][1] + bh / 2),
                        xytext=(x, y - bh / 2),
                        arrowprops=dict(arrowstyle="->", color="#ffffff55", lw=2))

    ax.set_title("EDA Workflow – Customer Churn Prediction",
                 fontsize=15, color="white", fontweight="bold", pad=10, y=0.99)
    fig.tight_layout()
    fig.savefig("diagrams/eda_workflow.png", dpi=150, bbox_inches="tight",
                facecolor=DARK_BG)
    plt.close(fig)
    print("✓ eda_workflow.png saved")


# ─────────────────────────────────────────────────────────────────────────────
# 2. Visualization Types Matrix
# ─────────────────────────────────────────────────────────────────────────────
def draw_visualization_matrix():
    fig, ax = plt.subplots(figsize=(14, 9), facecolor=DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.axis("off")

    categories = {
        "Univariate\n(Single Variable)": [
            ("Histogram", "Distribution shape", "#6C63FF"),
            ("KDE Plot", "Smooth density estimate", "#6C63FF"),
            ("Box Plot", "Quartiles & outliers", "#6C63FF"),
            ("Bar Chart", "Category frequencies", "#6C63FF"),
        ],
        "Bivariate\n(Two Variables)": [
            ("Scatter Plot", "Correlation pattern", "#FF6584"),
            ("Violin Plot", "Distribution by class", "#FF6584"),
            ("Heatmap", "Correlation matrix", "#FF6584"),
            ("Grouped Bar", "Category comparisons", "#FF6584"),
        ],
        "Multivariate\n(Many Variables)": [
            ("Pair Plot", "All-vs-all scatter", "#43CBFF"),
            ("3D Scatter", "Three-feature view", "#43CBFF"),
            ("Parallel Coord", "Multi-dim patterns", "#43CBFF"),
            ("PCA Biplot", "Reduced dimensions", "#43CBFF"),
        ],
        "Time-Series &\nSpecialised": [
            ("Line Chart", "Trends over time", "#F9CB28"),
            ("Churn Funnel", "Dropout stages", "#F9CB28"),
            ("Sankey Diagram", "Flow analysis", "#F9CB28"),
            ("SHAP Beeswarm", "Feature impact", "#F9CB28"),
        ],
    }

    n_cols = len(categories)
    col_w = 1.0 / n_cols
    colors_main = ["#6C63FF", "#FF6584", "#43CBFF", "#F9CB28"]

    for ci, (cat, plots) in enumerate(categories.items()):
        cx = (ci + 0.5) * col_w
        # Category header
        ax.text(cx, 0.96, cat, ha="center", va="top",
                fontsize=11, fontweight="bold", color=colors_main[ci],
                transform=ax.transAxes, multialignment="center")
        for ri, (pname, pdesc, color) in enumerate(plots):
            y_pos = 0.78 - ri * 0.19
            rect = FancyBboxPatch((cx - 0.11, y_pos - 0.07), 0.22, 0.13,
                                  boxstyle="round,pad=0.01",
                                  facecolor=color + "30", edgecolor=color,
                                  linewidth=1.8, transform=ax.transAxes, zorder=3)
            ax.add_patch(rect)
            ax.text(cx, y_pos + 0.015, pname, ha="center", va="center",
                    fontsize=9.5, fontweight="bold", color=color,
                    transform=ax.transAxes)
            ax.text(cx, y_pos - 0.028, pdesc, ha="center", va="center",
                    fontsize=7.5, color="#aaaaaa", transform=ax.transAxes)

    ax.set_title("Visualization Strategy Matrix – EDA Framework",
                 fontsize=15, color="white", fontweight="bold")
    fig.savefig("diagrams/visualization_types.png", dpi=150, bbox_inches="tight",
                facecolor=DARK_BG)
    plt.close(fig)
    print("✓ visualization_types.png saved")


# ─────────────────────────────────────────────────────────────────────────────
# 3. Data Types Decision Map
# ─────────────────────────────────────────────────────────────────────────────
def draw_data_types_map():
    fig, ax = plt.subplots(figsize=(13, 9), facecolor=DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9)
    ax.axis("off")

    def box(x, y, text, color, w=2.5, h=0.7):
        rect = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                              boxstyle="round,pad=0.08",
                              facecolor=color + "33", edgecolor=color,
                              linewidth=2, zorder=3)
        ax.add_patch(rect)
        for j, line in enumerate(text.split("\n")):
            offset = 0.15 if len(text.split("\n")) > 1 else 0
            ax.text(x, y + offset - j * 0.28, line, ha="center", va="center",
                    fontsize=8.5 if j > 0 else 9, color=color if j == 0 else "#cccccc",
                    fontweight="bold" if j == 0 else "normal", zorder=4)

    def arrow(x1, y1, x2, y2, label=""):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#ffffff55", lw=1.5))
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx + 0.15, my, label, fontsize=7.5, color="#888888")

    # Root
    box(6.5, 8.2, "RAW FEATURE", "#6C63FF", w=3)

    # Level 1 split
    box(2.5, 6.5, "NUMERICAL\n(int, float)", "#43CBFF")
    box(10.5, 6.5, "CATEGORICAL\n(object, bool)", "#FF6584")
    arrow(6.5, 7.85, 2.5, 6.85, "numeric")
    arrow(6.5, 7.85, 10.5, 6.85, "string/bool")

    # Numerical children
    box(1.2, 4.8, "CONTINUOUS\nAge, Income", "#43CBFF", w=2.2)
    box(3.8, 4.8, "DISCRETE\nCall Count", "#43CBFF", w=2.2)
    arrow(2.5, 6.15, 1.2, 5.15, "float")
    arrow(2.5, 6.15, 3.8, 5.15, "int")

    # Numerical → plots
    box(1.2, 3.2, "Histogram\nKDE, Box", "#56E39F", w=2.2)
    box(3.8, 3.2, "Bar Chart\nBox Plot", "#56E39F", w=2.2)
    arrow(1.2, 4.45, 1.2, 3.55)
    arrow(3.8, 4.45, 3.8, 3.55)

    # Categorical children
    box(9.0, 4.8, "NOMINAL\nGender, Region", "#FF6584", w=2.4)
    box(12.0, 4.8, "ORDINAL\nRating, Plan Tier", "#FF6584", w=2.4)
    arrow(10.5, 6.15, 9.0, 5.15, "no order")
    arrow(10.5, 6.15, 12.0, 5.15, "ordered")

    box(9.0, 3.2, "One-Hot\nEncoding", "#F9CB28", w=2.4)
    box(12.0, 3.2, "Label/Ordinal\nEncoding", "#F9CB28", w=2.4)
    arrow(9.0, 4.45, 9.0, 3.55)
    arrow(12.0, 4.45, 12.0, 3.55)

    # Bottom row – Analysis methods
    ax.text(6.5, 2.2, "▼  Analysis & Visualisation Techniques  ▼",
            ha="center", color="#888888", fontsize=9)
    methods = [
        (1.5, 1.3, "Univariate\nHistogram, KDE", "#6C63FF"),
        (4.5, 1.3, "Bivariate\nScatter, Violin", "#FF6584"),
        (7.5, 1.3, "Correlation\nHeatmap, PCA", "#43CBFF"),
        (10.5, 1.3, "Target Analysis\nChurn by Feature", "#F9CB28"),
    ]
    for mx, my, text, col in methods:
        box(mx, my, text, col, w=2.6)

    ax.set_title("Data Types Map & Analysis Decision Framework",
                 fontsize=14, color="white", fontweight="bold", y=0.99)
    fig.tight_layout()
    fig.savefig("diagrams/data_types_map.png", dpi=150, bbox_inches="tight",
                facecolor=DARK_BG)
    plt.close(fig)
    print("✓ data_types_map.png saved")


if __name__ == "__main__":
    print("Generating Week 2 diagrams...")
    draw_eda_workflow()
    draw_visualization_matrix()
    draw_data_types_map()
    print("\nAll Week 2 diagrams generated successfully in diagrams/")
