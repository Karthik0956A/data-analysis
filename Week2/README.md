# Week 2 – EDA & Visualization Framework Design

## Overview
This week designs a comprehensive Exploratory Data Analysis (EDA) and visualization framework for the Customer Churn Prediction project.

## Folder Structure
```
Week2/
├── generate_diagrams.py   → Generates EDA workflow, viz types, and data-types diagrams
├── eda_framework.py       → Demonstrates EDA code patterns on synthetic data
├── generate_report.py     → Builds the DOCX report with embedded diagrams
├── diagrams/              → Auto-generated PNG files
└── report/                → Output DOCX report
```

## How to Run
```bash
# From project root with venv activated:
cd Week2
python generate_diagrams.py
python eda_framework.py
python generate_report.py
```

## Deliverables
- `report/Week2_EDA_Framework.docx` — Full EDA framework document
- `diagrams/eda_workflow.png` — Step-by-step EDA workflow diagram
- `diagrams/visualization_types.png` — Visualization strategy matrix
- `diagrams/data_types_map.png` — Data types and analysis decision tree
- `diagrams/eda_sample_plots.png` — Sample EDA output plots
