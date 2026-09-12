"""
Week 3 – ML Pipeline Skeleton
Demonstrates a full scikit-learn ML pipeline for Customer Churn Prediction.
Runs on synthetic data and produces pipeline_results.png in diagrams/.
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import (classification_report, roc_auc_score,
                              confusion_matrix, roc_curve, f1_score)
from sklearn.impute import SimpleImputer

np.random.seed(42)
os.makedirs("diagrams", exist_ok=True)


# ── Synthetic Dataset (same generator as Week 2) ──────────────────────────────
def make_synthetic_data(n=2000):
    tenure = np.random.randint(1, 72, n)
    monthly_charges = np.random.uniform(20, 120, n)
    num_support_calls = np.random.poisson(2, n)
    contract = np.random.choice(["Month-to-month", "One year", "Two year"], n,
                                p=[0.55, 0.25, 0.20])
    internet_service = np.random.choice(["DSL", "Fiber optic", "No"], n,
                                        p=[0.35, 0.45, 0.20])
    gender = np.random.choice(["Male", "Female"], n)
    senior_citizen = np.random.binomial(1, 0.16, n)

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
        "num_support_calls": num_support_calls,
        "contract": contract,
        "internet_service": internet_service,
        "gender": gender,
        "senior_citizen": senior_citizen,
        "churn": churn,
    })


# ── Define Feature Columns ────────────────────────────────────────────────────
NUM_FEATURES = ["tenure", "monthly_charges", "num_support_calls", "senior_citizen"]
CAT_FEATURES = ["contract", "internet_service", "gender"]
TARGET = "churn"


# ── Build Preprocessing + Model Pipelines ────────────────────────────────────
def build_pipeline(model):
    num_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler",  StandardScaler()),
    ])
    cat_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")),
    ])
    preprocessor = ColumnTransformer([
        ("num", num_transformer, NUM_FEATURES),
        ("cat", cat_transformer, CAT_FEATURES),
    ])
    return Pipeline([
        ("preprocessor", preprocessor),
        ("model",         model),
    ])


# ── Train, Evaluate, Compare Models ──────────────────────────────────────────
def train_and_evaluate(X_train, X_test, y_train, y_test):
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced",
                                                   random_state=42),
        "Random Forest":       RandomForestClassifier(n_estimators=200, class_weight="balanced",
                                                       random_state=42),
        "Gradient Boosting":   GradientBoostingClassifier(n_estimators=200, learning_rate=0.05,
                                                           max_depth=4, random_state=42),
    }

    results = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for name, model in models.items():
        pipe = build_pipeline(model)
        print(f"\n{'='*55}")
        print(f"  Model: {name}")
        print(f"{'='*55}")

        # Cross-validation AUC
        cv_scores = cross_val_score(pipe, X_train, y_train, cv=cv,
                                    scoring="roc_auc", n_jobs=-1)
        print(f"  CV AUC-ROC : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

        # Fit on full training set
        pipe.fit(X_train, y_train)

        # Test set evaluation
        y_pred  = pipe.predict(X_test)
        y_proba = pipe.predict_proba(X_test)[:, 1]
        auc     = roc_auc_score(y_test, y_proba)
        f1      = f1_score(y_test, y_pred)

        print(f"  Test AUC   : {auc:.4f}")
        print(f"  Test F1    : {f1:.4f}")
        print("\n  Classification Report:")
        print(classification_report(y_test, y_pred, target_names=["No Churn", "Churned"]))

        results[name] = {
            "pipeline":  pipe,
            "cv_mean":   cv_scores.mean(),
            "cv_std":    cv_scores.std(),
            "test_auc":  auc,
            "test_f1":   f1,
            "y_pred":    y_pred,
            "y_proba":   y_proba,
            "fpr":       roc_curve(y_test, y_proba)[0],
            "tpr":       roc_curve(y_test, y_proba)[1],
        }

    return results


# ── Visualise Results ─────────────────────────────────────────────────────────
def plot_results(results, y_test):
    DARK = "#0f1117"
    plt.rcParams.update({"figure.facecolor": DARK, "axes.facecolor": "#1a1a2e",
                         "text.color": "white", "axes.labelcolor": "white",
                         "xtick.color": "white", "ytick.color": "white"})

    fig, axes = plt.subplots(1, 3, figsize=(18, 6), facecolor=DARK)
    fig.suptitle("ML Pipeline Results – Customer Churn Prediction (Synthetic Data)",
                 fontsize=14, color="white", fontweight="bold", y=1.02)

    colors = ["#6C63FF", "#43CBFF", "#F9CB28"]
    model_names = list(results.keys())

    # 1. AUC comparison
    ax = axes[0]
    aucs = [results[m]["test_auc"] for m in model_names]
    bars = ax.bar(model_names, aucs, color=colors, edgecolor="white", lw=0.8, width=0.5)
    for bar, v in zip(bars, aucs):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.004,
                f"{v:.3f}", ha="center", color="white", fontsize=9.5, fontweight="bold")
    ax.set_ylim(0.6, 1.0)
    ax.set_title("Test AUC-ROC Comparison", color="white", fontweight="bold")
    ax.set_ylabel("AUC-ROC")
    ax.tick_params(axis="x", labelsize=8)
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    for sp in ["left", "bottom"]:
        ax.spines[sp].set_color("#333355")
    ax.grid(axis="y", color="#ffffff10")

    # 2. ROC Curves
    ax = axes[1]
    for (name, res), color in zip(results.items(), colors):
        ax.plot(res["fpr"], res["tpr"], color=color, lw=2,
                label=f"{name.split()[0]} (AUC={res['test_auc']:.3f})")
    ax.plot([0, 1], [0, 1], "w--", alpha=0.4, lw=1)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curves", color="white", fontweight="bold")
    ax.legend(facecolor="#1a1a2e", labelcolor="white", fontsize=8)
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    for sp in ["left", "bottom"]:
        ax.spines[sp].set_color("#333355")

    # 3. F1 Scores
    ax = axes[2]
    f1s = [results[m]["test_f1"] for m in model_names]
    bars = ax.barh(model_names, f1s, color=colors, edgecolor="white", lw=0.8, height=0.45)
    for bar, v in zip(bars, f1s):
        ax.text(v + 0.005, bar.get_y() + bar.get_height() / 2,
                f"{v:.3f}", va="center", color="white", fontsize=9.5, fontweight="bold")
    ax.set_xlim(0, 1.0)
    ax.set_title("Test F1-Score (Churn Class)", color="white", fontweight="bold")
    ax.set_xlabel("F1-Score")
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    for sp in ["left", "bottom"]:
        ax.spines[sp].set_color("#333355")
    ax.grid(axis="x", color="#ffffff10")

    fig.tight_layout()
    fig.savefig("diagrams/ml_pipeline_results.png", dpi=150, bbox_inches="tight",
                facecolor=DARK)
    plt.close(fig)
    print("\n✓ ml_pipeline_results.png saved")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating synthetic dataset (2000 rows)...")
    df = make_synthetic_data(2000)
    print(f"  Churn rate: {df['churn'].mean() * 100:.1f}%")

    X = df[NUM_FEATURES + CAT_FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=42
    )
    print(f"  Train size: {X_train.shape[0]}  |  Test size: {X_test.shape[0]}")

    results = train_and_evaluate(X_train, X_test, y_train, y_test)
    plot_results(results, y_test)

    best_model = max(results, key=lambda m: results[m]["test_auc"])
    print(f"\n🏆 Best Model: {best_model}")
    print(f"   Test AUC: {results[best_model]['test_auc']:.4f}")
    print(f"   Test F1 : {results[best_model]['test_f1']:.4f}")
    print("\nML pipeline complete.")
