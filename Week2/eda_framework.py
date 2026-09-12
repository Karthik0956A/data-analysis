"""
Week 2 – EDA Framework
Demonstrates EDA code patterns on synthetic churn data and produces
sample visualisation plots saved to diagrams/eda_sample_plots.png
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

np.random.seed(42)
os.makedirs("diagrams", exist_ok=True)

# ── Generate synthetic churn dataset ─────────────────────────────────────────
def make_synthetic_data(n=1000):
    tenure = np.random.randint(1, 72, n)
    monthly_charges = np.random.uniform(20, 120, n)
    total_charges = tenure * monthly_charges + np.random.normal(0, 50, n)
    num_support_calls = np.random.poisson(2, n)
    contract = np.random.choice(["Month-to-month", "One year", "Two year"], n,
                                p=[0.55, 0.25, 0.20])
    internet_service = np.random.choice(["DSL", "Fiber optic", "No"], n,
                                        p=[0.35, 0.45, 0.20])
    gender = np.random.choice(["Male", "Female"], n)
    senior_citizen = np.random.binomial(1, 0.16, n)

    # Churn probability based on features
    churn_prob = (
        0.35 * (contract == "Month-to-month").astype(float)
        + 0.15 * (num_support_calls > 3).astype(float)
        + 0.10 * (tenure < 12).astype(float)
        + 0.08 * (monthly_charges > 80).astype(float)
        - 0.05 * senior_citizen
        + np.random.uniform(0, 0.15, n)
    )
    churn = (churn_prob > 0.35).astype(int)

    return pd.DataFrame({
        "tenure": tenure,
        "monthly_charges": monthly_charges.round(2),
        "total_charges": total_charges.round(2),
        "num_support_calls": num_support_calls,
        "contract": contract,
        "internet_service": internet_service,
        "gender": gender,
        "senior_citizen": senior_citizen,
        "churn": churn,
    })


# ── EDA Techniques ────────────────────────────────────────────────────────────
def run_eda(df):
    print("=" * 60)
    print("STEP 1: DATA INGESTION & BASIC INSPECTION")
    print("=" * 60)
    print(f"  Shape         : {df.shape}")
    print(f"  Columns       : {list(df.columns)}")
    print(f"  Memory usage  : {df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    print("\n  Data types:\n", df.dtypes)

    print("\n" + "=" * 60)
    print("STEP 2: MISSING VALUE ANALYSIS")
    print("=" * 60)
    missing = df.isnull().sum()
    pct = (missing / len(df) * 100).round(2)
    mv = pd.DataFrame({"Missing": missing, "Pct%": pct})
    print(mv[mv["Missing"] > 0] if mv["Missing"].sum() > 0 else "  No missing values found.")

    print("\n" + "=" * 60)
    print("STEP 3: DESCRIPTIVE STATISTICS")
    print("=" * 60)
    print(df.describe().round(2))

    print("\n" + "=" * 60)
    print("STEP 4: UNIVARIATE ANALYSIS – Churn Distribution")
    print("=" * 60)
    vc = df["churn"].value_counts()
    print(f"  Churned     : {vc[1]} ({vc[1]/len(df)*100:.1f}%)")
    print(f"  Not Churned : {vc[0]} ({vc[0]/len(df)*100:.1f}%)")

    print("\n" + "=" * 60)
    print("STEP 5: BIVARIATE ANALYSIS – Churn by Contract Type")
    print("=" * 60)
    ct = df.groupby("contract")["churn"].mean().round(3) * 100
    for k, v in ct.items():
        print(f"  {k:<20}: {v:.1f}% churn rate")

    print("\n" + "=" * 60)
    print("STEP 6: MULTIVARIATE – Correlation Matrix (numerical)")
    print("=" * 60)
    num_cols = ["tenure", "monthly_charges", "total_charges",
                "num_support_calls", "churn"]
    corr = df[num_cols].corr().round(3)
    print(corr)

    print("\n" + "=" * 60)
    print("STEP 7: OUTLIER DETECTION – IQR Method")
    print("=" * 60)
    for col in ["monthly_charges", "total_charges", "num_support_calls"]:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
        print(f"  {col:<25}: {len(outliers)} outliers ({len(outliers)/len(df)*100:.1f}%)")

    return df


# ── Sample Visualisation Plots ────────────────────────────────────────────────
def generate_sample_plots(df):
    sns.set_theme(style="darkgrid", palette="muted")
    plt.rcParams.update({"figure.facecolor": "#0f1117", "axes.facecolor": "#1a1a2e",
                         "text.color": "white", "axes.labelcolor": "white",
                         "xtick.color": "white", "ytick.color": "white",
                         "axes.edgecolor": "#333355"})

    fig, axes = plt.subplots(2, 3, figsize=(16, 10), facecolor="#0f1117")
    fig.suptitle("EDA Sample Plots – Customer Churn Dataset",
                 fontsize=16, color="white", fontweight="bold", y=0.98)

    palette = {0: "#56E39F", 1: "#FF6584"}

    # Plot 1: Churn distribution
    ax = axes[0, 0]
    vals = df["churn"].value_counts()
    bars = ax.bar(["Not Churned\n(0)", "Churned\n(1)"], vals.values,
                  color=["#56E39F", "#FF6584"], edgecolor="white", linewidth=0.8)
    for bar, v in zip(bars, vals.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                f"{v}\n({v/len(df)*100:.0f}%)", ha="center", color="white", fontsize=9)
    ax.set_title("Churn Distribution", color="white", fontweight="bold")
    ax.set_ylabel("Count", color="white")

    # Plot 2: Tenure histogram by churn
    ax = axes[0, 1]
    for churn_val, color, label in [(0, "#56E39F", "Not Churned"), (1, "#FF6584", "Churned")]:
        subset = df[df["churn"] == churn_val]["tenure"]
        ax.hist(subset, bins=20, alpha=0.7, color=color, label=label, edgecolor="black", lw=0.5)
    ax.set_title("Tenure Distribution by Churn", color="white", fontweight="bold")
    ax.set_xlabel("Tenure (months)", color="white")
    ax.legend(facecolor="#1a1a2e", labelcolor="white")

    # Plot 3: Monthly charges boxplot
    ax = axes[0, 2]
    data_by_churn = [df[df["churn"] == 0]["monthly_charges"],
                     df[df["churn"] == 1]["monthly_charges"]]
    bp = ax.boxplot(data_by_churn, patch_artist=True, notch=True,
                    labels=["Not Churned", "Churned"])
    bp["boxes"][0].set_facecolor("#56E39F44")
    bp["boxes"][1].set_facecolor("#FF658444")
    for element in ["whiskers", "caps", "medians", "fliers"]:
        for item in bp[element]:
            item.set_color("white")
    ax.set_title("Monthly Charges by Churn", color="white", fontweight="bold")
    ax.set_ylabel("Monthly Charges ($)", color="white")

    # Plot 4: Churn rate by contract type
    ax = axes[1, 0]
    ct = df.groupby("contract")["churn"].mean() * 100
    bars = ax.bar(ct.index, ct.values,
                  color=["#6C63FF", "#43CBFF", "#F9CB28"], edgecolor="white", lw=0.8)
    for bar, v in zip(bars, ct.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{v:.1f}%", ha="center", color="white", fontsize=9, fontweight="bold")
    ax.set_title("Churn Rate by Contract Type", color="white", fontweight="bold")
    ax.set_ylabel("Churn Rate (%)", color="white")
    ax.tick_params(axis="x", labelsize=8)

    # Plot 5: Correlation heatmap
    ax = axes[1, 1]
    num_cols = ["tenure", "monthly_charges", "total_charges",
                "num_support_calls", "churn"]
    corr = df[num_cols].corr()
    im = ax.imshow(corr.values, cmap="RdYlGn", aspect="auto", vmin=-1, vmax=1)
    ax.set_xticks(range(len(num_cols)))
    ax.set_yticks(range(len(num_cols)))
    ax.set_xticklabels([c.replace("_", "\n") for c in num_cols], fontsize=7, color="white")
    ax.set_yticklabels([c.replace("_", " ") for c in num_cols], fontsize=7, color="white")
    for i in range(len(num_cols)):
        for j in range(len(num_cols)):
            ax.text(j, i, f"{corr.values[i, j]:.2f}", ha="center", va="center",
                    fontsize=7, color="black" if abs(corr.values[i, j]) > 0.3 else "white")
    ax.set_title("Correlation Heatmap", color="white", fontweight="bold")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    # Plot 6: Support calls violin
    ax = axes[1, 2]
    data_0 = df[df["churn"] == 0]["num_support_calls"]
    data_1 = df[df["churn"] == 1]["num_support_calls"]
    parts = ax.violinplot([data_0, data_1], showmeans=True, showmedians=True)
    for i, (pc, color) in enumerate(zip(parts["bodies"], ["#56E39F", "#FF6584"])):
        pc.set_facecolor(color)
        pc.set_alpha(0.7)
    ax.set_xticks([1, 2])
    ax.set_xticklabels(["Not Churned", "Churned"], color="white")
    ax.set_title("Support Calls Distribution by Churn", color="white", fontweight="bold")
    ax.set_ylabel("Number of Support Calls", color="white")

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig("diagrams/eda_sample_plots.png", dpi=150, bbox_inches="tight",
                facecolor="#0f1117")
    plt.close(fig)
    print("✓ eda_sample_plots.png saved")


if __name__ == "__main__":
    print("Generating synthetic churn dataset...")
    df = make_synthetic_data(1000)
    print(f"  Dataset created: {df.shape[0]} rows × {df.shape[1]} columns\n")
    df = run_eda(df)
    print("\nGenerating sample EDA visualisations...")
    generate_sample_plots(df)
    print("\nEDA framework demo complete.")
