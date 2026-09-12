"""
Week 3 – Generate ML Diagrams
Creates three strategic diagrams for the ML Model Development plan:
  1. Full ML Workflow (end-to-end flowchart)
  2. Model Comparison Chart (theoretical performance bar chart)
  3. Evaluation Metrics Visual (ROC curve concept + confusion matrix layout)
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from matplotlib.gridspec import GridSpec

os.makedirs("diagrams", exist_ok=True)

DARK_BG = "#0f1117"
COLORS = ["#6C63FF", "#FF6584", "#43CBFF", "#F9CB28", "#FF8C42", "#56E39F",
          "#C77DFF", "#4CC9F0"]


# ─────────────────────────────────────────────────────────────────────────────
# 1. ML Workflow – End-to-End Flowchart
# ─────────────────────────────────────────────────────────────────────────────
def draw_ml_workflow():
    fig, ax = plt.subplots(figsize=(11, 16), facecolor=DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 16)
    ax.axis("off")

    main_steps = [
        (5.5, 15.2, "DATA PREPROCESSING",
         "Missing imputation • Encoding • Scaling • SMOTE", "#6C63FF"),
        (5.5, 13.0, "FEATURE ENGINEERING",
         "RFM scores • Tenure bins • Usage ratios • Interaction terms", "#FF6584"),
        (5.5, 10.8, "FEATURE SELECTION",
         "VIF analysis • RFE • Mutual Information • Correlation filter", "#43CBFF"),
        (5.5,  8.6, "MODEL TRAINING",
         "Logistic Regression  →  Random Forest  →  XGBoost  →  LightGBM", "#F9CB28"),
        (5.5,  6.4, "HYPERPARAMETER TUNING",
         "Optuna (Bayesian Optimization) • 100 trials • Stratified CV", "#FF8C42"),
        (5.5,  4.2, "MODEL EVALUATION",
         "AUC-ROC • F1 • Precision-Recall • Business metrics", "#56E39F"),
        (5.5,  2.0, "DEPLOYMENT & MONITORING",
         "FastAPI endpoint • Airflow scheduling • MLflow tracking", "#C77DFF"),
    ]

    bw, bh = 9.0, 1.3

    for i, (x, y, title, desc, color) in enumerate(main_steps):
        # Outer border glow
        glow = FancyBboxPatch((x - bw / 2 - 0.05, y - bh / 2 - 0.05),
                              bw + 0.1, bh + 0.1,
                              boxstyle="round,pad=0.1", facecolor=color + "15",
                              edgecolor=color + "55", linewidth=3)
        ax.add_patch(glow)
        # Main box
        rect = FancyBboxPatch((x - bw / 2, y - bh / 2), bw, bh,
                              boxstyle="round,pad=0.08", facecolor=color + "22",
                              edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        # Step badge
        badge = plt.Circle((x - bw / 2 + 0.5, y), 0.38, color=color, zorder=4)
        ax.add_patch(badge)
        ax.text(x - bw / 2 + 0.5, y, str(i + 1), ha="center", va="center",
                fontsize=10, fontweight="bold", color="white", zorder=5)

        ax.text(x + 0.15, y + 0.25, title, ha="center", va="center",
                fontsize=11, fontweight="bold", color=color, zorder=4)
        ax.text(x + 0.15, y - 0.25, desc, ha="center", va="center",
                fontsize=8.5, color="#cccccc", zorder=4)

        if i < len(main_steps) - 1:
            ax.annotate("", xy=(x, main_steps[i + 1][1] + bh / 2 + 0.05),
                        xytext=(x, y - bh / 2 - 0.05),
                        arrowprops=dict(arrowstyle="->", color="#ffffff66", lw=2))

    # Feedback loop arrow
    ax.annotate("", xy=(10.3, main_steps[3][1]),
                xytext=(10.3, main_steps[5][1]),
                arrowprops=dict(arrowstyle="<-", color="#FF8C4288", lw=2,
                                connectionstyle="arc3,rad=0"))
    ax.text(10.55, (main_steps[3][1] + main_steps[5][1]) / 2,
            "Retrain\nloop", ha="center", va="center", fontsize=7.5,
            color="#FF8C42", rotation=90)

    ax.set_title("End-to-End ML Pipeline – Customer Churn Prediction",
                 fontsize=14, color="white", fontweight="bold", y=0.99)
    fig.tight_layout()
    fig.savefig("diagrams/ml_workflow.png", dpi=150, bbox_inches="tight",
                facecolor=DARK_BG)
    plt.close(fig)
    print("✓ ml_workflow.png saved")


# ─────────────────────────────────────────────────────────────────────────────
# 2. Model Comparison Chart
# ─────────────────────────────────────────────────────────────────────────────
def draw_model_comparison():
    fig, axes = plt.subplots(1, 2, figsize=(14, 7), facecolor=DARK_BG)
    fig.suptitle("Model Comparison – Theoretical Performance Expectations",
                 fontsize=14, color="white", fontweight="bold", y=0.98)

    models = ["Logistic\nRegression", "Decision\nTree", "Random\nForest",
              "XGBoost", "LightGBM", "Neural\nNet"]
    colors = ["#6C63FF", "#FF6584", "#43CBFF", "#F9CB28", "#56E39F", "#C77DFF"]

    # AUC-ROC
    auc_scores = [0.79, 0.74, 0.87, 0.91, 0.92, 0.89]
    ax1 = axes[0]
    ax1.set_facecolor("#1a1a2e")
    bars = ax1.bar(models, auc_scores, color=colors, edgecolor="white",
                   linewidth=0.8, width=0.6)
    for bar, score in zip(bars, auc_scores):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.003,
                 f"{score:.2f}", ha="center", color="white", fontsize=9, fontweight="bold")
    ax1.set_ylim(0.6, 1.0)
    ax1.set_title("AUC-ROC Score (Higher = Better)", color="white", fontweight="bold")
    ax1.set_ylabel("AUC-ROC", color="white")
    ax1.tick_params(colors="white", axis="both")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_color("#333355")
    ax1.spines["bottom"].set_color("#333355")
    ax1.axhline(0.88, color="#FF6584", linestyle="--", alpha=0.7, label="Target: 0.88")
    ax1.legend(facecolor="#1a1a2e", labelcolor="white")
    ax1.grid(axis="y", color="#ffffff10")

    # F1 Scores
    f1_scores = [0.62, 0.58, 0.74, 0.80, 0.81, 0.77]
    ax2 = axes[1]
    ax2.set_facecolor("#1a1a2e")
    bars2 = ax2.bar(models, f1_scores, color=colors, edgecolor="white",
                    linewidth=0.8, width=0.6)
    for bar, score in zip(bars2, f1_scores):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.003,
                 f"{score:.2f}", ha="center", color="white", fontsize=9, fontweight="bold")
    ax2.set_ylim(0.4, 0.95)
    ax2.set_title("F1-Score (Churn Class)", color="white", fontweight="bold")
    ax2.set_ylabel("F1-Score", color="white")
    ax2.tick_params(colors="white", axis="both")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("#333355")
    ax2.spines["bottom"].set_color("#333355")
    ax2.grid(axis="y", color="#ffffff10")

    # Annotation for best model
    ax1.annotate("★ Best Choice", xy=(3, 0.91), xytext=(2, 0.95),
                 arrowprops=dict(arrowstyle="->", color="#F9CB28"), color="#F9CB28",
                 fontsize=9, fontweight="bold")
    ax2.annotate("★ Best Choice", xy=(4, 0.81), xytext=(2.5, 0.88),
                 arrowprops=dict(arrowstyle="->", color="#56E39F"), color="#56E39F",
                 fontsize=9, fontweight="bold")

    fig.tight_layout()
    fig.savefig("diagrams/model_comparison.png", dpi=150, bbox_inches="tight",
                facecolor=DARK_BG)
    plt.close(fig)
    print("✓ model_comparison.png saved")


# ─────────────────────────────────────────────────────────────────────────────
# 3. Evaluation Metrics Visual
# ─────────────────────────────────────────────────────────────────────────────
def draw_evaluation_metrics():
    fig = plt.figure(figsize=(14, 9), facecolor=DARK_BG)
    gs = GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.35)

    # 3a. ROC Curve (conceptual)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor("#1a1a2e")
    fpr = np.linspace(0, 1, 100)
    # Simulate multiple ROC curves
    model_rocs = [
        ("Logistic Reg (AUC=0.79)", 0.79, "#6C63FF"),
        ("Random Forest (AUC=0.87)", 0.87, "#43CBFF"),
        ("XGBoost (AUC=0.91)", 0.91, "#F9CB28"),
        ("LightGBM (AUC=0.92)", 0.92, "#56E39F"),
    ]
    for name, auc, color in model_rocs:
        tpr = fpr ** ((1 - auc) / auc)
        ax1.plot(fpr, tpr, color=color, lw=1.8, label=f"{name}")
    ax1.plot([0, 1], [0, 1], "w--", alpha=0.4, lw=1, label="Random (AUC=0.5)")
    ax1.set_xlabel("False Positive Rate", color="white", fontsize=9)
    ax1.set_ylabel("True Positive Rate", color="white", fontsize=9)
    ax1.set_title("ROC Curves", color="white", fontweight="bold")
    ax1.legend(fontsize=7, facecolor="#1a1a2e", labelcolor="white")
    ax1.tick_params(colors="white")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    for spine in ["left", "bottom"]:
        ax1.spines[spine].set_color("#333355")
    ax1.fill_between(fpr, fpr ** ((1 - 0.92) / 0.92), fpr, alpha=0.07, color="#56E39F")

    # 3b. Confusion Matrix Layout
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor("#1a1a2e")
    # Conceptual confusion matrix values
    cm = np.array([[7450, 380], [210, 1960]])
    im = ax2.imshow(cm, cmap="Blues", aspect="auto")
    labels = [["TN\n(True Negative)\n7,450", "FP\n(False Positive)\n380"],
              ["FN\n(False Negative)\n210", "TP\n(True Positive)\n1,960"]]
    colors_cm = [["#56E39F", "#FF6584"], ["#FF8C42", "#6C63FF"]]
    for i in range(2):
        for j in range(2):
            ax2.text(j, i, labels[i][j], ha="center", va="center",
                     fontsize=9.5, color="white", fontweight="bold")
    ax2.set_xticks([0, 1])
    ax2.set_yticks([0, 1])
    ax2.set_xticklabels(["Predicted: No Churn", "Predicted: Churn"],
                        color="white", fontsize=8)
    ax2.set_yticklabels(["Actual: No Churn", "Actual: Churn"],
                        color="white", fontsize=8)
    ax2.set_title("Confusion Matrix (Conceptual)", color="white", fontweight="bold")
    for spine_name in ax2.spines:
        ax2.spines[spine_name].set_visible(False)

    # 3c. Metrics Bar Chart
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor("#1a1a2e")
    metric_names = ["Accuracy", "Precision\n(Churn)", "Recall\n(Churn)", "F1-Score\n(Churn)",
                    "AUC-ROC", "AP Score"]
    metric_values = [0.94, 0.84, 0.90, 0.87, 0.92, 0.88]
    bar_colors = ["#6C63FF", "#FF6584", "#43CBFF", "#F9CB28", "#56E39F", "#C77DFF"]
    bars = ax3.barh(metric_names, metric_values, color=bar_colors,
                    edgecolor="white", linewidth=0.6, height=0.5)
    for bar, v in zip(bars, metric_values):
        ax3.text(v + 0.005, bar.get_y() + bar.get_height() / 2,
                 f"{v:.2f}", va="center", color="white", fontsize=9)
    ax3.set_xlim(0, 1.05)
    ax3.set_title("Evaluation Metrics – LightGBM (Best Model)", color="white", fontweight="bold")
    ax3.axvline(0.88, color="#FF6584", linestyle="--", alpha=0.6, label="Target")
    ax3.tick_params(colors="white")
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    for sp in ["left", "bottom"]:
        ax3.spines[sp].set_color("#333355")
    ax3.legend(facecolor="#1a1a2e", labelcolor="white", fontsize=8)

    # 3d. Cross-Validation Diagram
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor("#1a1a2e")
    ax4.set_xlim(0, 10)
    ax4.set_ylim(0, 6)
    ax4.axis("off")
    ax4.set_title("5-Fold Stratified Cross-Validation", color="white", fontweight="bold")

    fold_colors = ["#6C63FF44", "#FF658444", "#43CBFF44", "#F9CB2844", "#56E39F44"]
    val_colors  = ["#6C63FF",  "#FF6584",  "#43CBFF",  "#F9CB28",  "#56E39F"]
    folds = [
        ([0, 1, 2, 3], [4]),
        ([0, 1, 2, 4], [3]),
        ([0, 1, 3, 4], [2]),
        ([0, 2, 3, 4], [1]),
        ([1, 2, 3, 4], [0]),
    ]
    fold_scores = [0.906, 0.912, 0.898, 0.921, 0.909]
    block_w = 1.8
    block_h = 0.55
    for fi, (train_folds, val_fold) in enumerate(folds):
        y = 5.0 - fi * 0.95
        for ti in train_folds:
            rect = FancyBboxPatch((ti * block_w + 0.1, y - block_h / 2),
                                  block_w - 0.15, block_h,
                                  boxstyle="round,pad=0.02",
                                  facecolor="#33336655", edgecolor="#6666aa",
                                  linewidth=1, transform=ax4.transData)
            ax4.add_patch(rect)
            ax4.text(ti * block_w + block_w / 2 + 0.1, y,
                     f"Fold {ti + 1}", ha="center", va="center",
                     fontsize=7, color="#aaaaaa")
        vf = val_fold[0]
        vrect = FancyBboxPatch((vf * block_w + 0.1, y - block_h / 2),
                               block_w - 0.15, block_h,
                               boxstyle="round,pad=0.02",
                               facecolor=val_colors[fi] + "44",
                               edgecolor=val_colors[fi], linewidth=2,
                               transform=ax4.transData)
        ax4.add_patch(vrect)
        ax4.text(vf * block_w + block_w / 2 + 0.1, y,
                 "VAL", ha="center", va="center",
                 fontsize=7.5, color=val_colors[fi], fontweight="bold")
        ax4.text(9.5, y, f"AUC={fold_scores[fi]:.3f}", ha="right", va="center",
                 fontsize=8, color=val_colors[fi], fontweight="bold")

    ax4.text(5, 0.4, f"Mean AUC = {np.mean(fold_scores):.3f}  ±  {np.std(fold_scores):.3f}",
             ha="center", va="center", fontsize=10, color="white",
             fontweight="bold")

    fig.savefig("diagrams/evaluation_metrics.png", dpi=150, bbox_inches="tight",
                facecolor=DARK_BG)
    plt.close(fig)
    print("✓ evaluation_metrics.png saved")


if __name__ == "__main__":
    print("Generating Week 3 diagrams...")
    draw_ml_workflow()
    draw_model_comparison()
    draw_evaluation_metrics()
    print("\nAll Week 3 diagrams generated successfully in diagrams/")
