import streamlit as st
import pandas as pd
import os

from utils.styling import inject_css, header, kpi_card
from utils.model_utils import artifacts_present, load_artifacts
from utils.config import (
    RAW_DATASET_PATH, CLF_COMPARISON_CSV, REG_COMPARISON_CSV,
    TARGET_CLASSIFICATION_ACCURACY, TARGET_REGRESSION_RMSE,
)

st.set_page_config(
    page_title="EMIPredict AI | Financial Risk Platform",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

header(
    "💳 EMIPredict AI",
    "Intelligent Financial Risk Assessment Platform — dual ML pipeline for EMI eligibility "
    "(classification) and maximum safe EMI amount (regression), tracked end-to-end with MLflow."
)

# ---------------------------------------------------------------------------
# Setup status
# ---------------------------------------------------------------------------
ready = artifacts_present()

if not ready:
    st.warning(
        "**Setup required.** This app expects the trained model artifacts exported from your "
        "Kaggle notebook. Copy the following files from `/kaggle/working/artifacts/` into the "
        "local `artifacts/` folder next to this app, then refresh:\n\n"
        "- `preprocessor.pkl`\n- `target_label_encoder.pkl`\n- `best_classification_model.pkl`\n"
        "- `best_regression_model.pkl`\n- `feature_config.pkl`\n"
        "- `classification_model_comparison.csv`\n- `regression_model_comparison.csv`"
    )
else:
    st.success("Model artifacts loaded. Prediction Engine and Model Performance pages are ready.")

st.markdown('<div class="section-title">Platform Overview</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Total Records Trained On", "400,000", "5 EMI scenarios")
with c2:
    kpi_card("Input Features", "22 raw → 33 engineered", "after feature engineering")
with c3:
    if ready and os.path.exists(CLF_COMPARISON_CSV):
        clf_df = pd.read_csv(CLF_COMPARISON_CSV)
        best_acc = clf_df["accuracy"].max()
        kpi_card("Best Classification Accuracy", f"{best_acc*100:.2f}%",
                  f"Target: >{TARGET_CLASSIFICATION_ACCURACY*100:.0f}%")
    else:
        kpi_card("Best Classification Accuracy", "—", "load artifacts to compute")
with c4:
    if ready and os.path.exists(REG_COMPARISON_CSV):
        reg_df = pd.read_csv(REG_COMPARISON_CSV)
        best_rmse = reg_df["rmse"].min()
        kpi_card("Best Regression RMSE", f"₹{best_rmse:,.0f}",
                  f"Target: <₹{TARGET_REGRESSION_RMSE:,.0f}")
    else:
        kpi_card("Best Regression RMSE", "—", "load artifacts to compute")

st.markdown('<div class="section-title">What this platform solves</div>', unsafe_allow_html=True)
left, right = st.columns(2)
with left:
    st.markdown(
        """
        <div class="info-panel">
            <h4>The Problem</h4>
            <p>People struggle to repay EMIs due to poor financial planning and inadequate risk
            assessment at the point of loan approval — costing lenders time and exposing
            borrowers to over-leveraged debt.</p>
            <h4>The Solution</h4>
            <ul>
                <li><b>Classification</b> → is this applicant <code>Eligible</code>, <code>High_Risk</code>, or <code>Not_Eligible</code>?</li>
                <li><b>Regression</b> → if eligible, what's the maximum monthly EMI they can safely afford?</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    st.markdown(
        """
        <div class="info-panel">
            <h4>Who Uses This</h4>
            <ul>
                <li>🏦 <b>Banks & credit agencies</b> — data-driven loan amount recommendations</li>
                <li>💻 <b>FinTech lenders</b> — instant pre-qualification for digital lending</li>
                <li>🧑‍💼 <b>Loan officers</b> — AI-assisted underwriting in seconds instead of manual review</li>
                <li>📊 <b>Risk teams</b> — portfolio-level default risk monitoring</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="section-title">Navigate the app</div>', unsafe_allow_html=True)
nav1, nav2, nav3, nav4 = st.columns(4)
nav_items = [
    ("📊", "Data Exploration", "EDA charts: eligibility distribution, correlations, demographic risk patterns."),
    ("🎯", "Prediction Engine", "Enter an applicant's profile and get real-time eligibility + max EMI predictions."),
    ("📈", "Model Performance", "Compare all trained models, MLflow metrics, confusion matrix, feature importance."),
    ("🗄️", "Data Management", "Create, view, update, and delete loan application records (CRUD)."),
]
for col, (icon, title, desc) in zip([nav1, nav2, nav3, nav4], nav_items):
    with col:
        st.markdown(
            f"""
            <div class="nav-card">
                <span class="nav-icon">{icon}</span>
                <div class="nav-title">{title}</div>
                <div class="nav-desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")
st.caption(
    "Built on Steps 1–5 of the EMIPredict AI project guidance (data prep, EDA, feature "
    "engineering, model training, MLflow tracking) run on Kaggle. This app implements Step 6 "
    "(Streamlit application) — ready for Step 7 (Streamlit Cloud deployment)."
)