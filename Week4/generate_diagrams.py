"""
Week 4 – Generate Final Report Diagrams
Creates three polished, executive-quality diagrams:
  1. Executive KPI Dashboard
  2. Insights Chart (Feature Importance + Churn Trends)
  3. Recommendation Matrix (Impact vs. Effort Quadrant)
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.gridspec import GridSpec

os.makedirs("diagrams", exist_ok=True)

DARK_BG = "#0a0a14"
CARD_BG = "#12122a"
COLORS = ["#6C63FF", "#FF6584", "#43CBFF", "#F9CB28", "#FF8C42", "#56E39F"]


# ─────────────────────────────────────────────────────────────────────────────
# 1. Executive KPI Dashboard
# ─────────────────────────────────────────────────────────────────────────────
def draw_executive_dashboard():
    fig = plt.figure(figsize=(16, 9), facecolor=DARK_BG)
    gs = GridSpec(3, 4, figure=fig, hspace=0.55, wspace=0.4,
                  left=0.04, right=0.97, top=0.88, bottom=0.06)

    fig.suptitle("Executive KPI Dashboard – Customer Churn Prediction Project",
                 fontsize=16, color="white", fontweight="bold", y=0.96)

    # ── KPI Cards Row 1 ───────────────────────────────────────────────────────
    kpis = [
        ("AUC-ROC Score", "0.921", "Target: 0.88 ✓", "#56E39F", "+4.7%"),
        ("Churn Reduction", "6.1%", "22% → 15.9%",  "#6C63FF", "−28%"),
        ("Revenue Recovered", "$18.3M", "Annual",    "#F9CB28", "+18.3M"),
        ("Model Accuracy",   "94.2%",   "Test Set",  "#43CBFF", "±0.3%"),
    ]

    for ci, (label, value, sub, color, delta) in enumerate(kpis):
        ax = fig.add_subplot(gs[0, ci])
        ax.set_facecolor(CARD_BG)
        ax.axis("off")
        for sp in ax.spines.values():
            sp.set_visible(False)
        # Coloured top bar
        ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02",
                                    facecolor=color + "22", edgecolor=color,
                                    linewidth=2.5, transform=ax.transAxes))
        ax.text(0.5, 0.82, label,  ha="center", va="center", fontsize=10,
                color="#aaaaaa", transform=ax.transAxes)
        ax.text(0.5, 0.52, value,  ha="center", va="center", fontsize=22,
                color=color, fontweight="bold", transform=ax.transAxes)
        ax.text(0.5, 0.25, sub,    ha="center", va="center", fontsize=9,
                color="#888888", transform=ax.transAxes)
        ax.text(0.85, 0.82, delta, ha="center", va="center", fontsize=9,
                color="#56E39F" if "+" in delta else "#FF6584",
                fontweight="bold", transform=ax.transAxes)

    # ── Monthly Churn Rate Trend ───────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[1, :2])
    ax2.set_facecolor(CARD_BG)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    pre_model  = [22.1, 22.4, 21.9, 22.6, 23.0, 22.8,
                  22.3, 22.7, 22.5, 22.9, 22.2, 22.0]
    post_model = [None]*6 + [20.1, 18.4, 17.2, 16.5, 16.1, 15.9]
    x = range(12)
    ax2.plot(x, pre_model, color="#FF6584", lw=2.5, marker="o",
             markersize=5, label="Before Model (Baseline)")
    post_x = [i for i, v in enumerate(post_model) if v is not None]
    post_y = [v for v in post_model if v is not None]
    ax2.plot(post_x, post_y, color="#56E39F", lw=2.5, marker="o",
             markersize=5, label="After Model Deployment")
    ax2.axvline(5.5, color="#F9CB28", linestyle="--", alpha=0.7, lw=1.5)
    ax2.text(5.7, 23.2, "Model\nDeployed", color="#F9CB28", fontsize=8)
    ax2.fill_between(post_x, post_y, 22.0, alpha=0.12, color="#56E39F")
    ax2.set_xticks(x)
    ax2.set_xticklabels(months, color="white", fontsize=8)
    ax2.set_ylabel("Churn Rate (%)", color="white", fontsize=9)
    ax2.set_title("Monthly Churn Rate Trend", color="white", fontweight="bold")
    ax2.legend(facecolor=CARD_BG, labelcolor="white", fontsize=8)
    ax2.tick_params(colors="white")
    ax2.set_ylim(14, 24)
    for sp in ["top", "right"]:
        ax2.spines[sp].set_visible(False)
    for sp in ["left", "bottom"]:
        ax2.spines[sp].set_color("#333355")
    ax2.grid(axis="y", color="#ffffff0a")

    # ── Top 5 Features ────────────────────────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 2:])
    ax3.set_facecolor(CARD_BG)
    features = ["Contract Type", "Tenure", "Support Calls",\
                "Monthly Charges", "Internet Service"]
    importance = [0.28, 0.22, 0.18, 0.16, 0.10]
    bar_colors = ["#6C63FF", "#FF6584", "#43CBFF", "#F9CB28", "#FF8C42"]
    bars = ax3.barh(features[::-1], importance[::-1], color=bar_colors[::-1],
                    edgecolor="white", lw=0.6, height=0.5)
    for bar, v in zip(bars, importance[::-1]):
        ax3.text(v + 0.003, bar.get_y() + bar.get_height() / 2,
                 f"{v:.0%}", va="center", color="white", fontsize=9, fontweight="bold")
    ax3.set_xlim(0, 0.38)
    ax3.set_title("Top 5 Feature Importances (SHAP)", color="white", fontweight="bold")
    ax3.set_xlabel("Mean |SHAP Value|", color="white", fontsize=9)
    ax3.tick_params(colors="white")
    for sp in ["top", "right"]:
        ax3.spines[sp].set_visible(False)
    for sp in ["left", "bottom"]:
        ax3.spines[sp].set_color("#333355")
    ax3.grid(axis="x", color="#ffffff0a")

    # ── Campaign ROI by Segment ───────────────────────────────────────────────
    ax4 = fig.add_subplot(gs[2, :2])
    ax4.set_facecolor(CARD_BG)
    segments = ["High Risk\n>70%", "Medium Risk\n40-70%",
                "Low Risk\n20-40%", "Stable\n<20%"]
    customers = [45000, 120000, 180000, 655000]
    converted = [31500, 72000, 45000, 19650]
    x2 = np.arange(4)
    w = 0.35
    b1 = ax4.bar(x2 - w/2, customers, w, label="Targeted", color="#6C63FF44",
                 edgecolor="#6C63FF", lw=1.5)
    b2 = ax4.bar(x2 + w/2, converted, w, label="Retained", color="#56E39F88",
                 edgecolor="#56E39F", lw=1.5)
    ax4.set_xticks(x2)
    ax4.set_xticklabels(segments, color="white", fontsize=8)
    ax4.set_ylabel("Customers", color="white", fontsize=9)
    ax4.set_title("Retention Campaign by Risk Segment", color="white", fontweight="bold")
    ax4.legend(facecolor=CARD_BG, labelcolor="white", fontsize=8)
    ax4.tick_params(colors="white")
    for sp in ["top", "right"]:
        ax4.spines[sp].set_visible(False)
    for sp in ["left", "bottom"]:
        ax4.spines[sp].set_color("#333355")
    ax4.grid(axis="y", color="#ffffff0a")

    # ── Model Performance Over Time ────────────────────────────────────────────
    ax5 = fig.add_subplot(gs[2, 2:])
    ax5.set_facecolor(CARD_BG)
    deploy_months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    auc_over_time = [0.921, 0.918, 0.915, 0.909, 0.905, 0.921]
    f1_over_time  = [0.872, 0.869, 0.865, 0.858, 0.854, 0.871]
    dx = range(len(deploy_months))
    ax5.plot(dx, auc_over_time, color="#6C63FF", lw=2.5, marker="D",
             markersize=6, label="AUC-ROC")
    ax5.plot(dx, f1_over_time,  color="#FF8C42", lw=2.5, marker="s",
             markersize=6, label="F1-Score")
    ax5.axhline(0.88, color="#FF6584", linestyle="--", alpha=0.6, lw=1.2, label="Min. target")
    ax5.axvline(4.5, color="#56E39F", linestyle=":", alpha=0.7, lw=1.5)
    ax5.text(4.55, 0.855, "Retrain", color="#56E39F", fontsize=7.5)
    ax5.set_xticks(dx)
    ax5.set_xticklabels(deploy_months, color="white", fontsize=8)
    ax5.set_ylim(0.83, 0.94)
    ax5.set_ylabel("Score", color="white", fontsize=9)
    ax5.set_title("Model Performance Post-Deployment", color="white", fontweight="bold")
    ax5.legend(facecolor=CARD_BG, labelcolor="white", fontsize=8)
    ax5.tick_params(colors="white")
    for sp in ["top", "right"]:
        ax5.spines[sp].set_visible(False)
    for sp in ["left", "bottom"]:
        ax5.spines[sp].set_color("#333355")
    ax5.grid(axis="y", color="#ffffff0a")

    fig.savefig("diagrams/executive_dashboard.png", dpi=150, bbox_inches="tight",
                facecolor=DARK_BG)
    plt.close(fig)
    print("✓ executive_dashboard.png saved")


# ─────────────────────────────────────────────────────────────────────────────
# 2. Insights Chart – Feature Importance + Churn Pattern Heatmap
# ─────────────────────────────────────────────────────────────────────────────
def draw_insights_chart():
    fig, axes = plt.subplots(1, 2, figsize=(14, 8), facecolor=DARK_BG)
    fig.suptitle("Key Insights – Customer Churn Prediction",
                 fontsize=15, color="white", fontweight="bold", y=0.98)

    # Left: SHAP waterfall style
    ax = axes[0]
    ax.set_facecolor(CARD_BG)
    features = [
        "Contract: Month-to-month", "Tenure < 12 months", "Support Calls > 3",
        "Monthly Charges > $80", "No Tech Support", "Fiber Optic Internet",
        "No Online Security", "Senior Citizen", "No Streaming TV", "Paperless Billing"
    ]
    shap_vals = [0.52, 0.38, 0.29, 0.22, 0.18, 0.14, 0.12, -0.08, -0.05, -0.03]
    colors_shap = ["#FF6584" if v > 0 else "#56E39F" for v in shap_vals]
    bars = ax.barh(features[::-1], shap_vals[::-1],
                   color=colors_shap[::-1], edgecolor="white", lw=0.5, height=0.6)
    for bar, v in zip(bars, shap_vals[::-1]):
        offset = 0.01 if v >= 0 else -0.01
        align = "left" if v >= 0 else "right"
        ax.text(v + offset, bar.get_y() + bar.get_height() / 2,
                f"{v:+.2f}", va="center", ha=align, color="white", fontsize=8.5,
                fontweight="bold")
    ax.axvline(0, color="white", lw=1, alpha=0.5)
    ax.set_title("SHAP Feature Impact on Churn Probability",
                 color="white", fontweight="bold")
    ax.set_xlabel("Mean SHAP Value (impact on churn prediction)", color="white", fontsize=9)
    ax.tick_params(colors="white", labelsize=8.5)
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    for sp in ["left", "bottom"]:
        ax.spines[sp].set_color("#333355")
    ax.grid(axis="x", color="#ffffff0a")
    # Legend
    pos_patch = mpatches.Patch(color="#FF6584", label="Increases churn risk")
    neg_patch = mpatches.Patch(color="#56E39F", label="Decreases churn risk")
    ax.legend(handles=[pos_patch, neg_patch], facecolor=CARD_BG,
              labelcolor="white", fontsize=8, loc="lower right")

    # Right: Churn rate by segment heatmap
    ax2 = axes[1]
    ax2.set_facecolor(CARD_BG)
    contract_types = ["Month-to-month", "One year", "Two year"]
    tenure_bins    = ["0-12 mo", "13-24 mo", "25-48 mo", "49-72 mo"]
    churn_matrix = np.array([
        [68.2, 42.1, 28.4, 15.3],
        [32.5, 18.2, 10.1,  5.8],
        [12.3,  6.1,  3.2,  1.5],
    ])
    im = ax2.imshow(churn_matrix, cmap="RdYlGn_r", aspect="auto", vmin=0, vmax=70)
    ax2.set_xticks(range(4))
    ax2.set_yticks(range(3))
    ax2.set_xticklabels(tenure_bins, color="white", fontsize=9)
    ax2.set_yticklabels(contract_types, color="white", fontsize=9)
    ax2.set_xlabel("Tenure Segment", color="white")
    ax2.set_ylabel("Contract Type", color="white")
    ax2.set_title("Churn Rate (%) by Contract × Tenure", color="white", fontweight="bold")
    for i in range(3):
        for j in range(4):
            ax2.text(j, i, f"{churn_matrix[i, j]:.1f}%", ha="center", va="center",
                     fontsize=11, fontweight="bold",
                     color="white" if churn_matrix[i, j] > 35 else "black")
    cbar = fig.colorbar(im, ax=ax2, fraction=0.04, pad=0.04)
    cbar.ax.tick_params(colors="white")
    cbar.set_label("Churn Rate (%)", color="white")

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig("diagrams/insights_chart.png", dpi=150, bbox_inches="tight",
                facecolor=DARK_BG)
    plt.close(fig)
    print("✓ insights_chart.png saved")


# ─────────────────────────────────────────────────────────────────────────────
# 3. Recommendation Matrix – Impact vs. Effort Quadrant
# ─────────────────────────────────────────────────────────────────────────────
def draw_recommendation_matrix():
    fig, ax = plt.subplots(figsize=(12, 9), facecolor=DARK_BG)
    ax.set_facecolor(CARD_BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Quadrant backgrounds
    ax.fill_between([0, 5], [5, 5], [10, 10], alpha=0.08, color="#F9CB28")   # High impact, Low effort
    ax.fill_between([5, 10], [5, 5], [10, 10], alpha=0.06, color="#56E39F")  # High impact, High effort
    ax.fill_between([0, 5], [0, 0], [5, 5], alpha=0.05, color="#FF6584")     # Low impact, Low effort
    ax.fill_between([5, 10], [0, 0], [5, 5], alpha=0.04, color="#6C63FF")    # Low impact, High effort

    # Quadrant labels
    quadrant_labels = [
        (2.5, 9.3, "QUICK WINS", "#F9CB28", 13),
        (7.5, 9.3, "MAJOR PROJECTS", "#56E39F", 13),
        (2.5, 0.7, "FILL-INS", "#FF6584", 13),
        (7.5, 0.7, "THANKLESS TASKS", "#aaaaaa", 11),
    ]
    for x, y, label, color, size in quadrant_labels:
        ax.text(x, y, label, ha="center", va="center", fontsize=size,
                color=color, fontweight="bold", alpha=0.7)

    # Axes lines
    ax.axhline(5, color="#ffffff22", lw=1.5, linestyle="--")
    ax.axvline(5, color="#ffffff22", lw=1.5, linestyle="--")

    # Recommendations to plot
    recommendations = [
        # (x=effort, y=impact, label, color)
        (2.0, 8.5, "1. Deploy LightGBM\nchurn scoring monthly", "#56E39F"),
        (3.0, 7.5, "2. Personalised retention\noffers for top 20% risk", "#56E39F"),
        (1.5, 6.5, "3. Build churn monitoring\ndashboard (Plotly Dash)", "#F9CB28"),
        (4.0, 8.0, "4. Automate data pipeline\n(Airflow ETL)", "#43CBFF"),
        (6.5, 8.5, "5. Real-time churn API\n(FastAPI + streaming)", "#6C63FF"),
        (8.0, 7.5, "6. Deep learning model\n(TabNet / Neural Net)", "#C77DFF"),
        (7.0, 6.5, "7. Social media sentiment\nintegration", "#FF8C42"),
        (2.5, 4.0, "8. Improve data\ncollection coverage", "#FF6584"),
        (3.5, 3.0, "9. Customer survey\ndata integration", "#FF6584"),
        (7.5, 3.5, "10. Real-time streaming\npredictions (Kafka)", "#aaaaaa"),
    ]

    bubble_sizes = [350, 300, 280, 250, 320, 280, 240, 200, 180, 200]
    for i, ((x, y, label, color), size) in enumerate(zip(recommendations, bubble_sizes)):
        ax.scatter(x, y, s=size, c=color, alpha=0.85, edgecolors="white",
                   linewidths=1.5, zorder=4)
        ax.text(x, y, str(i + 1), ha="center", va="center",
                fontsize=9, fontweight="bold", color="white", zorder=5)

    # Legend
    legend_items = []
    for i, (x, y, label, color) in enumerate(recommendations):
        patch = mpatches.Patch(color=color, label=f"{i+1}. {label.replace(chr(10), ' ')}")
        legend_items.append(patch)

    ax.legend(handles=legend_items, loc="upper left", bbox_to_anchor=(1.02, 1),
              facecolor="#1a1a2e", labelcolor="white", fontsize=7.5,
              borderpad=1, framealpha=0.9)

    ax.set_xlabel("Implementation Effort  →  (Low to High)", color="white",
                  fontsize=11, labelpad=10)
    ax.set_ylabel("Business Impact  →  (Low to High)", color="white",
                  fontsize=11, labelpad=10)
    ax.set_title("Strategic Recommendation Matrix – Impact vs. Effort",
                 color="white", fontsize=14, fontweight="bold", pad=15)
    ax.tick_params(colors="white")
    for sp in ax.spines.values():
        sp.set_color("#333355")

    fig.tight_layout()
    fig.savefig("diagrams/recommendation_matrix.png", dpi=150, bbox_inches="tight",
                facecolor=DARK_BG)
    plt.close(fig)
    print("✓ recommendation_matrix.png saved")


if __name__ == "__main__":
    print("Generating Week 4 diagrams...")
    draw_executive_dashboard()
    draw_insights_chart()
    draw_recommendation_matrix()
    print("\nAll Week 4 diagrams generated successfully in diagrams/")
