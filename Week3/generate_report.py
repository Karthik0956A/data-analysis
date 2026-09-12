"""
Week 3 – Generate ML Model Plan Report (DOCX)
Run AFTER generate_diagrams.py and ml_pipeline.py
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

os.makedirs("report", exist_ok=True)

# ── Helpers ───────────────────────────────────────────────────────────────────

def set_heading(doc, text, level=1, color=(108, 99, 255)):
    h = doc.add_heading(text, level=level)
    run = h.runs[0] if h.runs else h.add_run(text)
    run.font.color.rgb = RGBColor(*color)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)
    return h

def add_para(doc, text, bold=False, size=11, color=None):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor(*color)
    p.paragraph_format.space_after = Pt(6)
    return p

def add_bullet(doc, text):
    p = doc.add_paragraph(text, style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    return p

def add_code(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = "Courier New"
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(86, 227, 159)
    p.paragraph_format.left_indent = Cm(1)
    p.paragraph_format.space_after = Pt(2)
    return p

def add_table(doc, headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    hdr = table.rows[0]
    for j, h in enumerate(headers):
        cell = hdr.cells[j]
        cell.text = h
        run = cell.paragraphs[0].runs[0]
        run.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:fill"), "FF8C42")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:val"), "clear")
        tcPr.append(shd)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for i, row in enumerate(rows):
        r = table.rows[i + 1]
        for j, val in enumerate(row):
            r.cells[j].text = val
    return table

def insert_image(doc, path, caption, width=5.5):
    if os.path.exists(path):
        doc.add_picture(path, width=Inches(width))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap = doc.add_paragraph(f"Figure: {caption}")
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.runs[0].italic = True
        cap.runs[0].font.size = Pt(9)
        cap.runs[0].font.color.rgb = RGBColor(120, 120, 120)
    else:
        doc.add_paragraph(f"[Image not found: {path}]")


# ── Build Document ────────────────────────────────────────────────────────────

def build_report():
    doc = Document()
    for section in doc.sections:
        section.top_margin    = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin   = Cm(2.5)
        section.right_margin  = Cm(2.5)

    title = doc.add_heading("Week 3 – ML Model Development & Evaluation Plan", 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.runs[0].font.color.rgb = RGBColor(255, 140, 66)

    sub = doc.add_paragraph("Customer Churn Prediction | Machine Learning Strategy")
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.runs[0].font.size = Pt(13)
    sub.runs[0].font.color.rgb = RGBColor(100, 100, 120)
    doc.add_page_break()

    # ── 1. Problem Definition ─────────────────────────────────────────────────
    set_heading(doc, "1. Problem Definition & ML Justification", level=1,
                color=(255, 140, 66))
    add_para(doc,
        "The business problem is binary classification: given a set of customer attributes "
        "and behavioural signals, predict whether a customer will churn within the next 30 days. "
        "This is formally defined as:")
    add_code(doc, "Input  : X = {demographic, contract, usage, support} features")
    add_code(doc, "Output : y ∈ {0: No Churn, 1: Churn}")
    add_code(doc, "Goal   : P(y=1 | X) → ranked risk score per customer")

    add_para(doc,
        "Machine learning is justified over rule-based systems because: (1) the relationship "
        "between 80+ features and churn is non-linear and highly interactive, (2) customer "
        "behaviour patterns shift over time requiring model updates, (3) ML provides "
        "probabilistic risk scores enabling ranked prioritisation.")

    # ── 2. Data Preprocessing ─────────────────────────────────────────────────
    set_heading(doc, "2. Data Preprocessing", level=1, color=(255, 140, 66))

    set_heading(doc, "2.1 Missing Value Handling", level=2, color=(67, 203, 255))
    add_code(doc, "from sklearn.impute import SimpleImputer, KNNImputer")
    add_code(doc, "# Numerical: median imputation")
    add_code(doc, "num_imputer = SimpleImputer(strategy='median')")
    add_code(doc, "# Categorical: mode imputation")
    add_code(doc, "cat_imputer = SimpleImputer(strategy='most_frequent')")

    set_heading(doc, "2.2 Encoding Categorical Variables", level=2, color=(67, 203, 255))
    enc_rows = [
        ["Nominal (≤5 categories)",  "One-Hot Encoding",    "Gender, InternetService",
         "OneHotEncoder(drop='first')"],
        ["Nominal (>5 categories)",  "Target Encoding",     "PaymentMethod, City",
         "category_encoders.TargetEncoder"],
        ["Ordinal",                  "Ordinal Encoding",    "Contract tier, Rating",
         "OrdinalEncoder(categories=[...])"],
        ["Binary",                   "Binary (0/1)",        "SeniorCitizen, PaperlessBilling",
         "Already binary in dataset"],
    ]
    add_table(doc, ["Variable Type", "Encoding Method", "Example Features", "Python API"],
              enc_rows)
    doc.add_paragraph()

    set_heading(doc, "2.3 Feature Scaling", level=2, color=(67, 203, 255))
    add_code(doc, "from sklearn.preprocessing import StandardScaler, RobustScaler")
    add_code(doc, "# StandardScaler: for Logistic Regression, Neural Nets")
    add_code(doc, "# RobustScaler: for data with outliers (uses IQR, not std)")
    add_para(doc, "Tree-based models (Random Forest, XGBoost, LightGBM) are invariant to "
             "scaling and do not require this step.")

    set_heading(doc, "2.4 Handling Class Imbalance", level=2, color=(67, 203, 255))
    add_para(doc, "The churn class comprises ~22% of records. Three strategies will be compared:")
    imb_rows = [
        ["SMOTE",              "Synthetic minority oversampling",
         "imbalanced-learn", "Training set only"],
        ["class_weight",       "Penalise majority class in loss function",
         "Built into sklearn", "All models"],
        ["Threshold Tuning",   "Adjust decision boundary post-training",
         "Youden's J statistic", "Evaluation phase"],
    ]
    add_table(doc, ["Strategy", "Mechanism", "Library", "Applied When"], imb_rows)
    doc.add_paragraph()

    set_heading(doc, "2.5 Feature Engineering", level=2, color=(67, 203, 255))
    features = [
        "tenure_bin: Bucket tenure into Early (0–12m), Mid (13–36m), Loyal (37m+)",
        "avg_monthly_spend_rank: Percentile rank of monthly charges within contract type",
        "support_intensity: support_calls / tenure (calls per month)",
        "contract_risk_score: Ordinal score (Month-to-month=2, One year=1, Two year=0)",
        "usage_per_dollar: data_usage_gb / monthly_charges",
    ]
    for f in features:
        add_bullet(doc, f)

    insert_image(doc, "diagrams/ml_workflow.png",
                 "End-to-End ML Pipeline for Customer Churn Prediction")
    doc.add_paragraph()

    # ── 3. Model Selection & Training ─────────────────────────────────────────
    set_heading(doc, "3. Model Selection & Training Strategy", level=1,
                color=(255, 140, 66))
    add_para(doc,
        "A progressive model selection strategy is adopted: start simple (Logistic Regression) "
        "as a baseline, add complexity (Random Forest), then deploy the most powerful "
        "model (LightGBM) if gains justify added complexity. This follows Occam's Razor — "
        "the simplest model that meets performance targets is preferred for interpretability.")

    model_rows = [
        ["Logistic Regression", "Baseline", "Fast, highly interpretable",
         "Assumes linearity; poor with interactions",
         "AUC-ROC ~0.79"],
        ["Decision Tree",       "Intermediate", "Interpretable; captures non-linearity",
         "Overfits without heavy pruning",
         "AUC-ROC ~0.74"],
        ["Random Forest",       "Strong Baseline", "Ensemble; handles missing values",
         "Less interpretable; slow for large data",
         "AUC-ROC ~0.87"],
        ["XGBoost",             "Primary Candidate", "State-of-the-art on tabular data",
         "Many hyperparameters; longer tuning",
         "AUC-ROC ~0.91"],
        ["LightGBM",            "Primary Candidate", "Faster than XGBoost; handles categoricals",
         "Can overfit small datasets",
         "AUC-ROC ~0.92"],
        ["Neural Network",      "Exploratory", "Captures complex patterns",
         "Requires more data; black-box",
         "AUC-ROC ~0.89"],
    ]
    add_table(doc,
              ["Model", "Role", "Strengths", "Weaknesses", "Expected AUC"],
              model_rows)
    doc.add_paragraph()

    insert_image(doc, "diagrams/model_comparison.png",
                 "Model Performance Comparison – AUC-ROC and F1-Score")
    doc.add_paragraph()

    set_heading(doc, "3.1 Hyperparameter Tuning Strategy", level=2, color=(67, 203, 255))
    add_para(doc,
        "Hyperparameter tuning uses Optuna (Bayesian Optimisation) with 100 trials, "
        "using 5-fold Stratified CV as the objective. Key hyperparameters for LightGBM:")
    tuning_rows = [
        ["num_leaves",        "31",       "50–500",   "Controls tree complexity"],
        ["learning_rate",     "0.05",     "0.01–0.3", "Step size per boosting round"],
        ["min_child_samples", "20",       "10–100",   "Minimum leaf samples (regularisation)"],
        ["subsample",         "0.8",      "0.5–1.0",  "Row subsampling fraction"],
        ["colsample_bytree",  "0.8",      "0.5–1.0",  "Feature subsampling fraction"],
        ["n_estimators",      "500",      "100–2000", "Number of boosting rounds"],
        ["reg_lambda",        "0.1",      "0.0–10.0", "L2 regularisation"],
    ]
    add_table(doc,
              ["Hyperparameter", "Default", "Search Range", "Effect"],
              tuning_rows)
    doc.add_paragraph()
    add_code(doc, "import optuna")
    add_code(doc, "def objective(trial):")
    add_code(doc, "    params = {")
    add_code(doc, "        'num_leaves': trial.suggest_int('num_leaves', 50, 500),")
    add_code(doc, "        'learning_rate': trial.suggest_float('lr', 0.01, 0.3, log=True),")
    add_code(doc, "    }")
    add_code(doc, "    return cross_val_score(lgbm_pipe, X_train, y_train, cv=cv, scoring='roc_auc').mean()")
    add_code(doc, "study = optuna.create_study(direction='maximize')")
    add_code(doc, "study.optimize(objective, n_trials=100)")

    # ── 4. Evaluation Metrics & Validation ────────────────────────────────────
    set_heading(doc, "4. Evaluation Metrics & Validation Strategy", level=1,
                color=(255, 140, 66))
    add_para(doc,
        "Given the class imbalance and the asymmetric cost of errors, we prioritise metrics "
        "that are robust to imbalance and align with business objectives.")

    metric_rows = [
        ["AUC-ROC",          "Primary",   "≥ 0.88",
         "Measures overall ranking ability; threshold-independent"],
        ["F1-Score (Churn)", "Primary",   "≥ 0.78",
         "Harmonic mean of precision & recall for minority class"],
        ["Recall (Churn)",   "Business",  "≥ 0.85",
         "Minimise missed churners (FN); each missed = lost revenue"],
        ["Precision (Churn)","Secondary", "≥ 0.72",
         "Control false positives; overly aggressive = wasted offers"],
        ["PR-AUC",           "Secondary", "≥ 0.75",
         "Better than AUC-ROC for highly imbalanced datasets"],
        ["Business Uplift",  "KPI",       "≥ 15% churn reduction",
         "Revenue recovered vs. cost of retention offers"],
    ]
    add_table(doc, ["Metric", "Priority", "Target", "Justification"], metric_rows)
    doc.add_paragraph()

    insert_image(doc, "diagrams/evaluation_metrics.png",
                 "Evaluation Metrics Visual – ROC Curves, Confusion Matrix, CV Folds")
    doc.add_paragraph()

    set_heading(doc, "4.1 Cross-Validation Strategy", level=2, color=(67, 203, 255))
    add_para(doc,
        "We use 5-Fold Stratified K-Fold Cross-Validation to ensure each fold maintains "
        "the original churn ratio (~22%). This prevents over-optimistic estimates from "
        "random splits with different class distributions.")
    add_code(doc, "from sklearn.model_selection import StratifiedKFold, cross_val_score")
    add_code(doc, "cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)")
    add_code(doc, "scores = cross_val_score(pipeline, X_train, y_train,")
    add_code(doc, "                         cv=cv, scoring='roc_auc', n_jobs=-1)")
    add_code(doc, "print(f'CV AUC: {scores.mean():.4f} ± {scores.std():.4f}')")

    insert_image(doc, "diagrams/ml_pipeline_results.png",
                 "Actual ML Pipeline Results on Synthetic Churn Dataset", width=6.0)
    doc.add_paragraph()

    # ── 5. Model Deployment (Optional) ────────────────────────────────────────
    set_heading(doc, "5. Model Deployment & Monitoring (Conceptual)", level=1,
                color=(255, 140, 66))
    set_heading(doc, "5.1 Deployment Architecture", level=2, color=(67, 203, 255))
    deploy = [
        "Model Artefact: Serialise best model using joblib; version with MLflow Model Registry.",
        "Batch Scoring: Monthly Airflow DAG → preprocessed features → LightGBM → predictions table.",
        "REST API: FastAPI endpoint for real-time single-customer scoring by CRM systems.",
        "Infrastructure: Docker container on AWS ECS; auto-scaling based on request volume.",
        "A/B Testing: Compare model-driven vs. rule-based retention strategies on 10% of customers.",
    ]
    for d in deploy:
        add_bullet(doc, d)

    set_heading(doc, "5.2 Model Monitoring", level=2, color=(67, 203, 255))
    monitor = [
        ("Data Drift",    "Monitor Population Stability Index (PSI) monthly; retrain if PSI > 0.2"),
        ("Model Drift",   "Track AUC-ROC on rolling 30-day labelled window; alert if drop > 0.03"),
        ("Feature Drift", "Monitor feature distribution shifts with KS test"),
        ("Business KPI",  "Track monthly churn rate vs. pre-model baseline"),
    ]
    for name, desc in monitor:
        add_para(doc, f"• {name}: {desc}")

    # ── 6. Conclusion ─────────────────────────────────────────────────────────
    set_heading(doc, "6. Conclusion", level=1, color=(255, 140, 66))
    add_para(doc,
        "This Week 3 document presents a rigorous, production-ready plan for developing and "
        "evaluating a machine learning model for customer churn prediction. The progressive "
        "modelling strategy — from interpretable baselines to powerful gradient boosting — "
        "ensures both technical performance (AUC-ROC ≥ 0.88) and business interpretability "
        "are achieved simultaneously. The comprehensive validation framework, including "
        "5-fold stratified cross-validation and business-aligned metrics, guarantees that "
        "the model performs robustly on unseen data. The deployment and monitoring plan "
        "ensures the system remains accurate and aligned with business objectives over time, "
        "making this a fully production-ready machine learning strategy.")

    out_path = "report/Week3_ML_Model_Plan.docx"
    doc.save(out_path)
    print(f"✓ Report saved → {out_path}")


if __name__ == "__main__":
    build_report()
