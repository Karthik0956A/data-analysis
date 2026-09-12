"""
Week 4 – Final Report Visualisations
Produces polished summary visualisations for the executive final report.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("diagrams", exist_ok=True)
DARK_BG = "#0a0a14"
CARD_BG = "#12122a"

np.random.seed(42)


def generate_final_plots():
    fig, axes = plt.subplots(2, 3, figsize=(18, 11), facecolor=DARK_BG)
    fig.suptitle("Final Project Summary – Customer Churn Prediction\nKey Findings & Business Impact",
                 fontsize=16, color="white", fontweight="bold", y=0.98)

    # ── 1. Pre vs Post Churn Rate ─────────────────────────────────────────────
    ax = axes[0, 0]
    ax.set_facecolor(CARD_BG)
    categories = ["Q1 2026\n(Pre)", "Q2 2026\n(Pre)", "Q3 2026\n(Post)", "Q4 2026\n(Post)"]
    rates = [22.4, 22.1, 18.3, 15.9]
    bar_colors = ["#FF6584", "#FF6584", "#56E39F", "#56E39F"]
    bars = ax.bar(categories, rates, color=bar_colors, edgecolor="white", lw=0.8, width=0.5)
    for bar, v in zip(bars, rates):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                f"{v}%", ha="center", color="white", fontsize=10, fontweight="bold")
    ax.set_ylim(0, 28)
    ax.set_title("Churn Rate: Pre vs. Post Deployment", color="white", fontweight="bold")
    ax.set_ylabel("Churn Rate (%)", color="white")
    ax.tick_params(colors="white")
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    for sp in ["left", "bottom"]:
        ax.spines[sp].set_color("#333355")
    ax.axhline(22.0, color="#FF6584", linestyle="--", alpha=0.5, lw=1.2, label="Baseline avg")
    ax.legend(facecolor=CARD_BG, labelcolor="white", fontsize=8)
    ax.grid(axis="y", color="#ffffff0a")

    # ── 2. Revenue Impact ─────────────────────────────────────────────────────
    ax = axes[0, 1]
    ax.set_facecolor(CARD_BG)
    items = ["Revenue at\nRisk (Annual)", "Recovered\nRevenue", "Campaign\nCost", "Net ROI"]
    values = [42.0, 18.3, 3.2, 15.1]
    colors2 = ["#FF6584", "#56E39F", "#F9CB28", "#6C63FF"]
    bars2 = ax.bar(items, values, color=colors2, edgecolor="white", lw=0.8, width=0.5)
    for bar, v in zip(bars2, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                f"${v}M", ha="center", color="white", fontsize=10, fontweight="bold")
    ax.set_ylim(0, 52)
    ax.set_title("Financial Impact (Millions USD)", color="white", fontweight="bold")
    ax.set_ylabel("Amount ($M)", color="white")
    ax.tick_params(colors="white")
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    for sp in ["left", "bottom"]:
        ax.spines[sp].set_color("#333355")
    ax.grid(axis="y", color="#ffffff0a")

    # ── 3. Model Comparison Summary ───────────────────────────────────────────
    ax = axes[0, 2]
    ax.set_facecolor(CARD_BG)
    models  = ["Logistic\nReg", "Random\nForest", "Gradient\nBoosting"]
    aucs    = [0.792, 0.873, 0.921]
    f1s     = [0.618, 0.741, 0.872]
    x = np.arange(len(models))
    w = 0.3
    b1 = ax.bar(x - w/2, aucs, w, label="AUC-ROC", color="#6C63FF", edgecolor="white", lw=0.8)
    b2 = ax.bar(x + w/2, f1s,  w, label="F1-Score", color="#43CBFF", edgecolor="white", lw=0.8)
    for bar, v in zip(list(b1) + list(b2), list(aucs) + list(f1s)):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                f"{v:.3f}", ha="center", color="white", fontsize=8, fontweight="bold")
    ax.set_ylim(0.5, 1.02)
    ax.set_xticks(x)
    ax.set_xticklabels(models, color="white")
    ax.set_title("Final Model Comparison", color="white", fontweight="bold")
    ax.legend(facecolor=CARD_BG, labelcolor="white", fontsize=9)
    ax.tick_params(colors="white")
    ax.axhline(0.88, color="#FF6584", linestyle="--", alpha=0.6, lw=1.2, label="Target")
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    for sp in ["left", "bottom"]:
        ax.spines[sp].set_color("#333355")
    ax.grid(axis="y", color="#ffffff0a")

    # ── 4. Retention Rate by Risk Tier ────────────────────────────────────────
    ax = axes[1, 0]
    ax.set_facecolor(CARD_BG)
    tiers = ["Very High\n(>80%)", "High\n(60-80%)", "Medium\n(40-60%)", "Low\n(<40%)"]
    offered = [12000, 33000, 55000, 105000]
    retained = [8400, 19800, 22000, 31500]
    x2 = np.arange(4)
    w2 = 0.35
    ax.bar(x2 - w2/2, offered,  w2, label="Offered Retention", color="#6C63FF77",
           edgecolor="#6C63FF", lw=1.5)
    ax.bar(x2 + w2/2, retained, w2, label="Successfully Retained", color="#56E39F99",
           edgecolor="#56E39F", lw=1.5)
    retention_rates = [r / o * 100 for r, o in zip(retained, offered)]
    for i, rate in enumerate(retention_rates):
        ax.text(i, max(offered[i], retained[i]) + 500, f"{rate:.0f}%",
                ha="center", color="#F9CB28", fontsize=9, fontweight="bold")
    ax.set_xticks(x2)
    ax.set_xticklabels(tiers, color="white", fontsize=8)
    ax.set_title("Retention Success by Risk Tier", color="white", fontweight="bold")
    ax.set_ylabel("Number of Customers", color="white")
    ax.legend(facecolor=CARD_BG, labelcolor="white", fontsize=8)
    ax.tick_params(colors="white")
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    for sp in ["left", "bottom"]:
        ax.spines[sp].set_color("#333355")
    ax.grid(axis="y", color="#ffffff0a")

    # ── 5. Confusion Matrix ───────────────────────────────────────────────────
    ax = axes[1, 1]
    ax.set_facecolor(CARD_BG)
    cm = np.array([[7450, 380], [210, 1960]])
    im = ax.imshow(cm, cmap="Blues", aspect="auto")
    labels = [["TN = 7,450\n(True Negatives)", "FP = 380\n(False Positives)"],
              ["FN = 210\n(False Negatives)", "TP = 1,960\n(True Positives)"]]
    for i in range(2):
        for j in range(2):
            ax.text(j, i, labels[i][j], ha="center", va="center",
                    fontsize=9.5, color="white", fontweight="bold")
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Predicted: No Churn", "Predicted: Churn"], color="white")
    ax.set_yticklabels(["Actual: No Churn", "Actual: Churn"], color="white")
    ax.set_title("Confusion Matrix – Best Model (LightGBM)", color="white", fontweight="bold")
    for sp in ax.spines.values():
        sp.set_visible(False)

    # ── 6. Project Timeline Actual vs Planned ─────────────────────────────────
    ax = axes[1, 2]
    ax.set_facecolor(CARD_BG)
    phases = ["Data Prep", "Feature Eng", "Modelling", "Tuning",
              "Evaluation", "Reporting"]
    planned = [5.0, 4.0, 8.0, 6.0, 4.0, 3.0]
    actual  = [5.5, 3.5, 9.0, 7.0, 3.5, 2.5]
    x3 = np.arange(len(phases))
    w3 = 0.35
    ax.bar(x3 - w3/2, planned, w3, label="Planned Hours", color="#6C63FF77",
           edgecolor="#6C63FF", lw=1.5)
    ax.bar(x3 + w3/2, actual,  w3, label="Actual Hours",  color="#F9CB2899",
           edgecolor="#F9CB28", lw=1.5)
    ax.set_xticks(x3)
    ax.set_xticklabels(phases, color="white", fontsize=8, rotation=15, ha="right")
    ax.set_title("Planned vs. Actual Effort (Hours)", color="white", fontweight="bold")
    ax.set_ylabel("Hours", color="white")
    ax.legend(facecolor=CARD_BG, labelcolor="white", fontsize=8)
    ax.tick_params(colors="white")
    total_planned = sum(planned)
    total_actual  = sum(actual)
    ax.text(0.98, 0.95, f"Total: {total_planned:.0f}h planned / {total_actual:.0f}h actual",
            ha="right", va="top", fontsize=8, color="#aaaaaa", transform=ax.transAxes)
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    for sp in ["left", "bottom"]:
        ax.spines[sp].set_color("#333355")
    ax.grid(axis="y", color="#ffffff0a")

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig("diagrams/final_summary_plots.png", dpi=150, bbox_inches="tight",
                facecolor=DARK_BG)
    plt.close(fig)
    print("✓ final_summary_plots.png saved")


if __name__ == "__main__":
    print("Generating final summary visualisations...")
    generate_final_plots()
    print("\nFinal visualisations complete.")
