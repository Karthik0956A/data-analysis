"""
Week 1 – Generate Report
Builds Week1_Project_Plan.docx with all sections and embedded diagrams.
Run AFTER generate_diagrams.py.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

os.makedirs("report", exist_ok=True)

# ── Helper utilities ──────────────────────────────────────────────────────────

def set_heading(doc, text, level=1, color=(108, 99, 255)):
    h = doc.add_heading(text, level=level)
    run = h.runs[0] if h.runs else h.add_run(text)
    run.font.color.rgb = RGBColor(*color)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)
    return h

def add_para(doc, text, bold=False, italic=False, size=11, color=None):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor(*color)
    p.paragraph_format.space_after = Pt(6)
    return p

def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(text, style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    return p

def add_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    # Header row
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
        shd.set(qn("w:fill"), "6C63FF")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:val"), "clear")
        tcPr.append(shd)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    # Data rows
    for i, row in enumerate(rows):
        r = table.rows[i + 1]
        for j, val in enumerate(row):
            r.cells[j].text = val
            r.cells[j].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
    return table

def insert_image(doc, path, caption, width=5.5):
    if os.path.exists(path):
        doc.add_picture(path, width=Inches(width))
        last = doc.paragraphs[-1]
        last.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap = doc.add_paragraph(f"Figure: {caption}")
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.runs[0].italic = True
        cap.runs[0].font.size = Pt(9)
        cap.runs[0].font.color.rgb = RGBColor(120, 120, 120)
    else:
        doc.add_paragraph(f"[Diagram not found: {path}]")

# ── Build Document ────────────────────────────────────────────────────────────

def build_report():
    doc = Document()

    # Page margins
    for section in doc.sections:
        section.top_margin    = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin   = Cm(2.5)
        section.right_margin  = Cm(2.5)

    # ── Title Page ────────────────────────────────────────────────────────────
    title = doc.add_heading("Customer Churn Prediction", 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.runs[0].font.color.rgb = RGBColor(108, 99, 255)

    sub = doc.add_paragraph("Week 1 – Data Science Project Planning and Strategy Design")
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.runs[0].font.size = Pt(14)
    sub.runs[0].font.color.rgb = RGBColor(100, 100, 120)

    doc.add_paragraph()
    info_lines = [
        ("Project     :", "Customer Churn Prediction for Telecom Industry"),
        ("Week        :", "Week 1 – Planning & Strategy"),
        ("Prepared by :", "Data Science Intern"),
        ("Date        :", "September 2026"),
    ]
    for label, value in info_lines:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p.add_run(f"{label}  ")
        r1.bold = True
        r1.font.color.rgb = RGBColor(108, 99, 255)
        r1.font.size = Pt(11)
        r2 = p.add_run(value)
        r2.font.size = Pt(11)

    doc.add_page_break()

    # ── 1. Introduction & Project Background ─────────────────────────────────
    set_heading(doc, "1. Introduction & Project Background", level=1)
    add_para(doc,
        "Customer churn — the phenomenon where subscribers discontinue a service — is one of the "
        "most pressing business challenges faced by telecommunications companies worldwide. Industry "
        "research consistently shows that acquiring a new customer costs five to seven times more "
        "than retaining an existing one, and even a modest 5% reduction in churn can increase "
        "profitability by 25–95% (Reichheld, F., Harvard Business Review).")
    add_para(doc,
        "This project addresses churn prediction for a hypothetical mid-sized telecom operator "
        "serving approximately 7 million subscribers. The business is experiencing an annual churn "
        "rate of 22%, costing an estimated $42 million per year in lost revenue. Despite having "
        "rich customer data across CRM, billing, usage, and support channels, the company currently "
        "relies on reactive strategies — offering discounts only after a customer files a cancellation "
        "request. A predictive, data-driven approach would allow the business to intervene proactively.")

    set_heading(doc, "1.1 Problem Motivation", level=2, color=(255, 101, 132))
    add_para(doc,
        "The core motivation is to transition the telecom company from reactive churn management "
        "to proactive, AI-driven customer retention. By identifying at-risk customers 30–60 days "
        "before they churn, retention teams can deploy personalised offers, service improvements, "
        "or priority support — dramatically reducing the churn rate and protecting revenue.")

    set_heading(doc, "1.2 Why Python?", level=2, color=(255, 101, 132))
    bullets = [
        "Rich ecosystem: pandas, NumPy, scikit-learn, XGBoost, LightGBM, matplotlib, seaborn, plotly.",
        "Rapid prototyping and iteration through Jupyter Notebooks.",
        "Seamless integration with cloud services (AWS SageMaker, GCP Vertex AI, Azure ML).",
        "Strong community support and extensive open-source libraries for every stage of the pipeline.",
        "Production-readiness via Flask/FastAPI for model serving and MLflow for experiment tracking.",
    ]
    for b in bullets:
        add_bullet(doc, b)

    insert_image(doc, "diagrams/project_lifecycle.png",
                 "Data Science Project Lifecycle for Customer Churn Prediction")
    doc.add_paragraph()

    # ── 2. Project Objectives & Scope ────────────────────────────────────────
    set_heading(doc, "2. Project Objectives & Scope", level=1)
    set_heading(doc, "2.1 Primary Objectives", level=2, color=(255, 101, 132))
    objectives = [
        "Develop a binary classification model to predict customer churn with AUC-ROC ≥ 0.88.",
        "Identify the top 10 features driving churn behaviour.",
        "Reduce false-negative rate (missed churners) to below 15%.",
        "Deliver a scoring pipeline that can classify 1 million customers in under 10 minutes.",
        "Produce actionable, interpretable outputs for the marketing and retention teams.",
    ]
    for i, obj in enumerate(objectives, 1):
        add_bullet(doc, f"O{i}: {obj}")

    set_heading(doc, "2.2 Secondary Objectives", level=2, color=(255, 101, 132))
    sec_obj = [
        "Establish a reusable data pipeline for future churn cohorts.",
        "Create an interactive dashboard for ongoing churn monitoring.",
        "Document all steps to facilitate knowledge transfer.",
    ]
    for s in sec_obj:
        add_bullet(doc, s)

    set_heading(doc, "2.3 Scope", level=2, color=(255, 101, 132))
    add_para(doc, "IN-SCOPE:", bold=True)
    in_scope = [
        "Historical customer data (last 24 months): demographics, contract, billing, usage, support.",
        "Supervised ML classification (Logistic Regression, Random Forest, XGBoost, LightGBM).",
        "Batch prediction pipeline scored monthly.",
        "Explainability using SHAP values.",
        "Automated model retraining trigger on performance degradation.",
    ]
    for s in in_scope:
        add_bullet(doc, s)

    add_para(doc, "OUT-OF-SCOPE:", bold=True)
    out_scope = [
        "Real-time streaming prediction (future phase).",
        "Social media sentiment analysis.",
        "Customer lifetime value optimisation (separate project).",
        "Mobile application development.",
    ]
    for s in out_scope:
        add_bullet(doc, s)

    # ── 3. Methodology & Strategy ─────────────────────────────────────────────
    set_heading(doc, "3. Methodology & Strategy", level=1)
    add_para(doc,
        "The project follows the industry-standard CRISP-DM (Cross-Industry Standard Process for "
        "Data Mining) methodology, adapted with modern MLOps practices. Each phase is time-boxed "
        "and has well-defined entry and exit criteria.")

    phases = [
        ("Phase 1: Business Understanding",
         "Collaborate with business stakeholders to define churn precisely (e.g., no activity for "
         "60 days), agree on success KPIs, and document constraints such as data privacy regulations."),
        ("Phase 2: Data Understanding & Collection",
         "Identify data sources (CRM, billing system, call data records, helpdesk tickets), assess "
         "data quality, and create a data dictionary. Expected features: ~80 raw variables."),
        ("Phase 3: Data Preparation",
         "Execute ETL pipelines using pandas. Handle missing values via median/mode imputation and "
         "MICE for complex patterns. Encode categorical variables (one-hot, target encoding). "
         "Normalise numerical features using StandardScaler/RobustScaler. Address class imbalance "
         "using SMOTE or class_weight='balanced'."),
        ("Phase 4: Modelling",
         "Train baseline (Logistic Regression), intermediate (Random Forest), and advanced "
         "(XGBoost, LightGBM) models. Use Optuna for hyperparameter optimisation. Compare models "
         "on a stratified train/validation/test split (60/20/20)."),
        ("Phase 5: Evaluation",
         "Evaluate using AUC-ROC, F1-score, Precision-Recall curve, and business metrics (revenue "
         "at risk captured). Run 5-fold stratified cross-validation for robustness."),
        ("Phase 6: Deployment",
         "Package the best model as a REST API using FastAPI. Schedule monthly batch scoring via "
         "Apache Airflow. Store predictions in a data warehouse for the retention dashboard."),
    ]
    for title, desc in phases:
        set_heading(doc, title, level=2, color=(67, 203, 255))
        add_para(doc, desc)

    insert_image(doc, "diagrams/methodology_flowchart.png",
                 "Customer Churn Prediction – Methodology Flowchart (CRISP-DM adapted)")
    doc.add_paragraph()

    # ── 4. Timeline & Tools ───────────────────────────────────────────────────
    set_heading(doc, "4. Timeline & Resource Allocation", level=1)
    add_para(doc,
        "The project is planned over a 30–35 hour engagement for the planning and strategy phase. "
        "The Gantt chart below illustrates the allocation of effort across key activities.")

    insert_image(doc, "diagrams/timeline_gantt.png",
                 "Project Timeline – Gantt Chart (30–35 Hours Total)")
    doc.add_paragraph()

    add_para(doc, "Effort Summary Table:", bold=True)
    headers = ["Activity", "Hours", "Deliverable"]
    rows = [
        ["Problem Definition & Background Research", "3h", "Problem statement doc"],
        ["Project Objective & Scope Definition",     "2h", "Scope document"],
        ["Methodology & Strategy Design",            "4h", "Methodology plan"],
        ["Data Source Identification",               "3h", "Data dictionary draft"],
        ["Tool & Library Selection",                 "2h", "Tech stack decision"],
        ["Timeline & Resource Planning",             "2h", "Gantt chart"],
        ["Flowchart & Diagram Creation",             "3h", "3 PNG diagrams"],
        ["Risk & Challenge Analysis",                "2h", "Risk register"],
        ["Report Writing & Documentation",           "4h", "Week 1 DOCX"],
        ["Review & Finalization",                    "3h", "Reviewed final doc"],
        ["TOTAL",                                   "28h", "—"],
    ]
    add_table(doc, headers, rows)
    doc.add_paragraph()

    set_heading(doc, "4.1 Python Tools & Libraries", level=2, color=(255, 101, 132))
    headers2 = ["Category", "Libraries / Tools", "Purpose"]
    rows2 = [
        ["Data Manipulation",   "pandas, numpy",                      "Data loading, wrangling, aggregation"],
        ["Visualisation",       "matplotlib, seaborn, plotly",        "EDA plots, dashboards, interactive charts"],
        ["Machine Learning",    "scikit-learn, XGBoost, LightGBM",    "Model training and evaluation"],
        ["Explainability",      "SHAP, eli5",                         "Feature importance, LIME explanations"],
        ["Experiment Tracking", "MLflow",                             "Run tracking, model registry"],
        ["Pipeline Automation", "Apache Airflow",                     "Scheduled batch scoring pipelines"],
        ["Model Serving",       "FastAPI, uvicorn",                   "REST API for real-time predictions"],
        ["Imbalance Handling",  "imbalanced-learn (SMOTE)",           "Address class imbalance"],
        ["Hyperparameter Opt.", "Optuna",                             "Automated hyperparameter search"],
        ["Report Generation",   "python-docx, Jupyter",              "DOCX reports, notebook presentations"],
    ]
    add_table(doc, headers2, rows2)
    doc.add_paragraph()

    # ── 5. Expected Outcomes & Challenges ─────────────────────────────────────
    set_heading(doc, "5. Expected Outcomes", level=1)
    outcomes = [
        ("Predictive Model", "A production-ready churn prediction model with AUC-ROC ≥ 0.88, enabling "
         "the retention team to prioritise outreach to the top 20% highest-risk customers."),
        ("Business Impact", "Expected reduction of annual churn from 22% to 16–18%, translating to "
         "$15–20M in recovered annual revenue."),
        ("Customer Insights", "A ranked list of the 10 most predictive features driving churn, informing "
         "product and pricing strategy."),
        ("Reusable Pipeline", "A modular, fully documented ETL + ML pipeline reusable for future cohorts "
         "and other customer analytics projects."),
        ("Monitoring Dashboard", "A live Power BI / Plotly Dash dashboard tracking churn probability "
         "distributions, model drift, and retention campaign effectiveness."),
    ]
    for title, desc in outcomes:
        set_heading(doc, title, level=2, color=(86, 227, 159))
        add_para(doc, desc)

    set_heading(doc, "6. Anticipated Challenges & Mitigation Strategies", level=1)
    headers3 = ["Challenge", "Impact", "Mitigation Strategy"]
    rows3 = [
        ["Class imbalance (churn ~22%)", "High",
         "Use SMOTE oversampling + class_weight='balanced'; evaluate on F1 not accuracy"],
        ["Missing data in usage logs", "Medium",
         "MICE imputation for MAR; flag indicators for MNAR patterns"],
        ["Feature multicollinearity", "Medium",
         "VIF analysis; use tree-based models that handle correlation natively"],
        ["Concept drift post-deployment", "High",
         "Monitor PSI monthly; trigger retraining when PSI > 0.2"],
        ["Data privacy & GDPR compliance", "High",
         "Anonymise PII; use differential privacy where applicable"],
        ["Stakeholder alignment", "Medium",
         "Weekly status meetings; dashboard for non-technical stakeholders"],
        ["Computational resources", "Low",
         "Use cloud spot instances for training; cache preprocessed datasets"],
    ]
    add_table(doc, headers3, rows3)
    doc.add_paragraph()

    # ── 7. Conclusion ─────────────────────────────────────────────────────────
    set_heading(doc, "7. Conclusion", level=1)
    add_para(doc,
        "This Week 1 planning document establishes a solid strategic foundation for the Customer "
        "Churn Prediction project. By adopting the CRISP-DM methodology with modern MLOps practices, "
        "leveraging Python's powerful data science ecosystem, and maintaining rigorous documentation "
        "standards, the project is positioned to deliver measurable business value. The 30–35 hour "
        "planning investment ensures every subsequent phase — data collection, modelling, evaluation, "
        "and deployment — proceeds with clarity and purpose.")
    add_para(doc,
        "The comprehensive risk register and mitigation strategies ensure the team is prepared for "
        "common data science pitfalls. With executive buy-in secured through a clear ROI narrative "
        "and transparent success metrics, this project represents a benchmark for data-driven "
        "decision-making within the organisation.")

    # Save
    out_path = "report/Week1_Project_Plan.docx"
    doc.save(out_path)
    print(f"✓ Report saved → {out_path}")


if __name__ == "__main__":
    build_report()
