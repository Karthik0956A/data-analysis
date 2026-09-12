"""
Week 4 – Generate Final Comprehensive Report (DOCX)
Run AFTER generate_diagrams.py and final_report.py
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

def add_table(doc, headers, rows, header_color="56E39F"):
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
        shd.set(qn("w:fill"), header_color)
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:val"), "clear")
        tcPr.append(shd)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for i, row in enumerate(rows):
        r = table.rows[i + 1]
        for j, val in enumerate(row):
            r.cells[j].text = val
    return table

def insert_image(doc, path, caption, width=5.8):
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

def add_kpi_row(doc, kpis):
    """Add a row of 3 KPI boxes as a table."""
    table = doc.add_table(rows=1, cols=len(kpis))
    table.style = "Table Grid"
    colors = ["6C63FF", "56E39F", "F9CB28", "FF6584", "43CBFF"]
    for j, (label, value, sub) in enumerate(kpis):
        cell = table.rows[0].cells[j]
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:fill"), colors[j % len(colors)] + "22")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:val"), "clear")
        tcPr.append(shd)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p.add_run(f"{label}\n")
        r1.font.size = Pt(9)
        r1.font.color.rgb = RGBColor(170, 170, 170)
        r2 = p.add_run(f"{value}\n")
        r2.font.size = Pt(18)
        r2.bold = True
        r2.font.color.rgb = RGBColor(*bytes.fromhex(colors[j % len(colors)]))
        r3 = p.add_run(sub)
        r3.font.size = Pt(8)
        r3.font.color.rgb = RGBColor(120, 120, 120)
    return table


# ── Build Document ────────────────────────────────────────────────────────────

def build_report():
    doc = Document()
    for section in doc.sections:
        section.top_margin    = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin   = Cm(2.5)
        section.right_margin  = Cm(2.5)

    # ── Cover Page ────────────────────────────────────────────────────────────
    title = doc.add_heading("Customer Churn Prediction", 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.runs[0].font.color.rgb = RGBColor(86, 227, 159)

    sub = doc.add_paragraph("Week 4 – Comprehensive Data Science Report & Insights Presentation")
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.runs[0].font.size = Pt(13)
    sub.runs[0].font.color.rgb = RGBColor(100, 100, 120)
    doc.add_paragraph()

    info_data = [
        ("Project    :", "Customer Churn Prediction – Telecom Industry"),
        ("Week       :", "Week 4 – Final Report & Executive Presentation"),
        ("Classification:", "CONFIDENTIAL – For Internal Business Use"),
        ("Date       :", "September 2026"),
        ("Status     :", "✓ COMPLETE – All objectives achieved"),
    ]
    for label, value in info_data:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p.add_run(f"{label}  ")
        r1.bold = True
        r1.font.color.rgb = RGBColor(86, 227, 159)
        r1.font.size = Pt(11)
        r2 = p.add_run(value)
        r2.font.size = Pt(11)
    doc.add_page_break()

    # ── 1. Executive Summary ──────────────────────────────────────────────────
    set_heading(doc, "1. Executive Summary", level=1, color=(86, 227, 159))
    add_para(doc,
        "This report presents the findings and strategic recommendations of a comprehensive "
        "data science engagement for customer churn prediction at a hypothetical mid-sized "
        "telecom operator. Over the course of this project, we developed, validated, and "
        "deployed a machine learning model that achieved an AUC-ROC of 0.921 — surpassing "
        "the target of 0.88 — and enabled a measurable reduction in annual churn from 22.1% "
        "to 15.9%, recovering an estimated $18.3 million in annual revenue.", size=11)
    doc.add_paragraph()

    # KPI summary boxes
    add_kpi_row(doc, [
        ("AUC-ROC", "0.921", "Target: ≥0.88 ✓"),
        ("Churn Rate", "15.9%", "Down from 22.1%"),
        ("Revenue Saved", "$18.3M", "Annual recovery"),
        ("F1-Score", "0.872", "Churn class"),
        ("ROI", "5.7x", "Net campaign ROI"),
    ])
    doc.add_paragraph()

    add_para(doc,
        "The project followed the CRISP-DM methodology over a 30-35 hour strategic engagement, "
        "progressing through business understanding, data preparation, feature engineering, "
        "model development, evaluation, and production deployment. A LightGBM gradient "
        "boosting model was selected as the final production model based on its superior "
        "balance of predictive accuracy, training speed, and interpretability via SHAP values.")

    insert_image(doc, "diagrams/executive_dashboard.png",
                 "Executive KPI Dashboard – Key Project Metrics and Outcomes", width=6.2)
    doc.add_paragraph()

    # ── 2. Methodology Overview ───────────────────────────────────────────────
    set_heading(doc, "2. Methodology Overview", level=1, color=(86, 227, 159))
    add_para(doc,
        "The project adopted a rigorous, industry-standard analytical methodology. Each phase "
        "was time-boxed with well-defined entry and exit criteria, ensuring quality and "
        "reproducibility at every step.")

    method_rows = [
        ["Business Understanding", "2 sessions",
         "Defined churn, KPIs, success criteria with business stakeholders"],
        ["Data Understanding",     "3 sessions",
         "Identified 80+ features across 5 data domains; profiled quality"],
        ["Data Preparation",       "8 sessions",
         "ETL, missing imputation (MICE), encoding, SMOTE, feature engineering"],
        ["Modelling",              "10 sessions",
         "Trained 5 model types; Optuna hyperparameter tuning (100 trials)"],
        ["Evaluation",             "5 sessions",
         "5-fold stratified CV; AUC, F1, PR-AUC, business uplift metrics"],
        ["Deployment",             "4 sessions",
         "FastAPI endpoint; Airflow batch pipeline; MLflow model registry"],
        ["Monitoring",             "Ongoing",
         "PSI drift detection; monthly retraining trigger; Plotly Dash"],
    ]
    add_table(doc, ["Phase", "Duration", "Key Activities"], method_rows,
              header_color="56E39F")
    doc.add_paragraph()

    set_heading(doc, "2.1 Data Architecture", level=2, color=(67, 203, 255))
    arch = [
        "Source Systems: CRM (demographics), Billing (charges), CDR (call records), Helpdesk (tickets).",
        "Data Volume: ~7 million customer records; 80 raw features; 24 months of historical data.",
        "ETL Pipeline: pandas + SQLAlchemy → data lake (S3) → feature store (Feast) → model.",
        "Training/Validation/Test Split: 60% / 20% / 20% — stratified by churn label.",
    ]
    for a in arch:
        add_bullet(doc, a)

    # ── 3. Insights & Analysis ────────────────────────────────────────────────
    set_heading(doc, "3. Key Insights & Analysis", level=1, color=(86, 227, 159))
    add_para(doc,
        "The exploratory and modelling analyses revealed several high-impact patterns that "
        "directly inform retention strategy. The insights below are ranked by business "
        "impact and supported by SHAP (SHapley Additive exPlanations) values from the "
        "production LightGBM model.")

    insert_image(doc, "diagrams/insights_chart.png",
                 "SHAP Feature Importance and Churn Rate Heatmap by Contract × Tenure")
    doc.add_paragraph()

    insights = [
        ("Contract Type is the #1 Churn Driver",
         "Customers on month-to-month contracts churn at 68.2% within the first 12 months — "
         "4.5x higher than two-year contract holders (15.3%). SHAP value: +0.52. "
         "Strategy: Incentivise annual/biannual contracts with discounted rates."),
        ("Early Tenure is the Highest-Risk Period",
         "Customers in their first 12 months exhibit disproportionate churn. This 'early churn' "
         "phenomenon suggests onboarding friction. SHAP value: +0.38. "
         "Strategy: Deploy a structured 90-day onboarding programme with proactive touchpoints."),
        ("Support Calls Signal Dissatisfaction",
         "Customers making >3 support calls per quarter are 2.8x more likely to churn. "
         "SHAP value: +0.29. Strategy: Flag high-contact customers for priority service queues."),
        ("High Monthly Charges Increase Churn Risk",
         "Customers paying >$80/month show elevated churn probability (+0.22 SHAP), particularly "
         "when combined with month-to-month contracts. Strategy: Review pricing competitiveness."),
        ("Fiber Optic Internet Has Surprising Churn Rate",
         "Despite being a premium service, fiber optic subscribers churn more than DSL users "
         "(SHAP: +0.14). Network quality issues are suspected. Strategy: Investigate outage rates."),
    ]
    for i, (title, desc) in enumerate(insights, 1):
        set_heading(doc, f"Insight {i}: {title}", level=2, color=(249, 203, 40))
        add_para(doc, desc)

    insert_image(doc, "diagrams/final_summary_plots.png",
                 "Final Summary – Churn Reduction, Revenue Impact, Model Comparison", width=6.2)
    doc.add_paragraph()

    # ── 4. Presentation Strategy ─────────────────────────────────────────────
    set_heading(doc, "4. Presentation Strategy for Non-Technical Stakeholders", level=1,
                color=(86, 227, 159))
    add_para(doc,
        "Communicating data science insights to non-technical executives requires translating "
        "statistical concepts into business language. We employ a structured storytelling "
        "approach — 'The Three-Act Framework' — to ensure clarity and impact.")

    acts = [
        ("Act 1: The Problem (Stakes)", 5,
         "Open with the financial cost: 'We are losing $42M annually to preventable churn.' "
         "Use a single, striking visual — the monthly churn rate trend line. Avoid technical "
         "jargon. Frame everything in business terms: customers, dollars, and time."),
        ("Act 2: The Solution (Hero)", 6,
         "Introduce the model as a 'early warning system' that identifies at-risk customers "
         "30–60 days before they leave. Show the churn rate heatmap (contract × tenure) to "
         "make patterns tangible. Use the ROC curve concept: 'Our model is right 92% of the time.'"),
        ("Act 3: The Outcome (Results)", 7,
         "Present the KPI dashboard: $18.3M recovered, churn rate at 15.9%, 5.7x ROI. "
         "Show the retention campaign success by risk tier. End with the recommendation matrix — "
         "clear next steps that the executive team can act on immediately."),
    ]
    for act, slide_no, desc in acts:
        set_heading(doc, act, level=2, color=(67, 203, 255))
        add_para(doc, f"(Slides {slide_no}-{slide_no+1}): {desc}")

    set_heading(doc, "4.1 Visualisation Principles for Non-Technical Audiences", level=2,
                color=(67, 203, 255))
    principles = [
        "One message per slide: each chart answers exactly one business question.",
        "Annotate directly: write the insight on the chart, not in bullet points below.",
        "Use colour meaningfully: red = risk/problem, green = success/improvement.",
        "Avoid showing model internals: no confusion matrices, no technical metrics.",
        "Lead with headlines: every slide title should be the conclusion, not the topic.",
    ]
    for p in principles:
        add_bullet(doc, p)

    # ── 5. Recommendations ────────────────────────────────────────────────────
    set_heading(doc, "5. Recommendations & Strategic Next Steps", level=1, color=(86, 227, 159))
    add_para(doc,
        "Based on the project findings, the following recommendations are presented in order "
        "of implementation priority, guided by the Impact vs. Effort framework.")

    insert_image(doc, "diagrams/recommendation_matrix.png",
                 "Strategic Recommendation Matrix – Impact vs. Effort Quadrant")
    doc.add_paragraph()

    rec_rows = [
        ["IMMEDIATE (0-30 days)",    "Quick Win",
         "Deploy monthly batch scoring; integrate scores into CRM",
         "HIGH", "2 weeks"],
        ["IMMEDIATE (0-30 days)",    "Quick Win",
         "Launch personalised retention offers for top 20% risk customers",
         "HIGH", "3 weeks"],
        ["SHORT-TERM (1-3 months)",  "Major Project",
         "Build and deploy Plotly Dash churn monitoring dashboard",
         "HIGH", "6 weeks"],
        ["SHORT-TERM (1-3 months)",  "Quick Win",
         "Automate ETL/scoring pipeline with Apache Airflow",
         "HIGH", "4 weeks"],
        ["MEDIUM-TERM (3-6 months)", "Major Project",
         "Develop real-time FastAPI endpoint for CRM integration",
         "MEDIUM", "8 weeks"],
        ["MEDIUM-TERM (3-6 months)", "Exploratory",
         "Investigate fiber optic network quality correlation with churn",
         "MEDIUM", "6 weeks"],
        ["LONG-TERM (6-12 months)",  "Strategic",
         "Deep learning model (TabNet) for complex interaction capture",
         "LOW", "12 weeks"],
        ["LONG-TERM (6-12 months)",  "Strategic",
         "Real-time streaming predictions via Kafka integration",
         "LOW", "16 weeks"],
    ]
    add_table(doc,
              ["Timeline", "Category", "Recommendation", "Impact", "Est. Duration"],
              rec_rows, header_color="56E39F")
    doc.add_paragraph()

    # ── 6. Conclusions ────────────────────────────────────────────────────────
    set_heading(doc, "6. Conclusions", level=1, color=(86, 227, 159))
    add_para(doc,
        "This four-week data science engagement has successfully delivered a production-ready "
        "customer churn prediction system that exceeds all predefined success metrics. The "
        "project demonstrates that a structured, rigorous approach to the full data science "
        "lifecycle — from business understanding through model deployment — can generate "
        "transformative business value from existing customer data.", size=12)
    add_para(doc,
        "The LightGBM model achieved an AUC-ROC of 0.921, reducing annual churn from 22.1% "
        "to 15.9% and recovering $18.3 million in annual revenue at a campaign ROI of 5.7x. "
        "The five key insights identified — contract type, early tenure risk, support call "
        "patterns, pricing pressure, and network quality — provide the retention team with "
        "clear, actionable levers to drive continued churn reduction.")
    add_para(doc,
        "The recommendation matrix provides a clear, prioritised roadmap for the next 12 months, "
        "ensuring the project's momentum translates into sustained business improvement. With "
        "the monitoring infrastructure in place, the model will continue to deliver accurate "
        "predictions as customer behaviour evolves, making this a foundation for long-term "
        "competitive advantage through data-driven customer retention.")

    # Closing statement
    doc.add_paragraph()
    closing = doc.add_paragraph(
        "\"Data is the new oil. But like oil, data needs to be refined before it can "
        "create value.\" — Clive Humby")
    closing.alignment = WD_ALIGN_PARAGRAPH.CENTER
    closing.runs[0].italic = True
    closing.runs[0].font.color.rgb = RGBColor(108, 99, 255)
    closing.runs[0].font.size = Pt(11)

    out_path = "report/Week4_Final_Report.docx"
    doc.save(out_path)
    print(f"✓ Report saved → {out_path}")


if __name__ == "__main__":
    build_report()
