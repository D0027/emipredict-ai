import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

from utils.styling import inject_css, header
from utils.config import RAW_DATASET_PATH, CLASSIFICATION_TARGET, REGRESSION_TARGET, ELIGIBILITY_COLORS

st.set_page_config(page_title="Data Exploration | EMIPredict AI", page_icon="📊", layout="wide")
inject_css()
header("📊 Exploratory Data Analysis", "Eligibility distribution, correlations, and demographic risk patterns across 400K applicant records.")


@st.cache_data(show_spinner="Loading dataset...")
def load_data(path):
    return pd.read_csv(path, low_memory=False)


if not os.path.exists(RAW_DATASET_PATH):
    st.warning(
        f"Raw dataset not found at `data/emi_prediction_dataset.csv`. Copy the CSV you used on "
        f"Kaggle into the local `data/` folder to enable this page. All charts below mirror "
        f"Step 2 of the training notebook exactly, so once the file is in place everything "
        f"renders automatically — no code changes needed."
    )
    st.stop()

df = load_data(RAW_DATASET_PATH)

# Light-touch cleaning purely for display purposes (mirrors notebook's cleaning cell)
for col in ["age", "monthly_salary", "bank_balance"]:
    if col in df.columns and df[col].dtype == object:
        df[col] = pd.to_numeric(df[col].astype(str).str.extract(r"^(-?\d+\.?\d*)")[0], errors="coerce")
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
for col in numeric_cols:
    if df[col].isnull().any():
        df[col] = df[col].fillna(df[col].median())
categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
for col in categorical_cols:
    if df[col].isnull().any():
        df[col] = df[col].fillna(df[col].mode()[0])

st.markdown(f'<div class="data-strip">📁 Loaded {len(df):,} records · {df.shape[1]} columns</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 1. Eligibility distribution + target distribution
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">EMI Eligibility & Target Distribution</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    counts = df[CLASSIFICATION_TARGET].value_counts()
    fig = px.bar(
        x=counts.index, y=counts.values,
        color=counts.index, color_discrete_map=ELIGIBILITY_COLORS,
        labels={"x": "Eligibility Class", "y": "Count"},
        title="EMI Eligibility Distribution",
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
with c2:
    fig = px.histogram(
        df, x=REGRESSION_TARGET, nbins=60, title="Max Monthly EMI Distribution",
        color_discrete_sequence=["#3EC6A8"],
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# 2. Eligibility by EMI scenario
# ---------------------------------------------------------------------------
if "emi_scenario" in df.columns:
    st.markdown('<div class="section-title">Eligibility by Lending Scenario</div>', unsafe_allow_html=True)
    scenario_counts = df.groupby(["emi_scenario", CLASSIFICATION_TARGET]).size().reset_index(name="count")
    fig = px.bar(
        scenario_counts, x="emi_scenario", y="count", color=CLASSIFICATION_TARGET,
        barmode="group", color_discrete_map=ELIGIBILITY_COLORS,
        title="EMI Eligibility by Scenario",
    )
    fig.update_layout(xaxis_tickangle=-15)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# 3. Correlation heatmap + top correlations
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">Correlation Analysis</div>', unsafe_allow_html=True)
numeric_df = df.select_dtypes(include=[np.number])
corr = numeric_df.corr()

c1, c2 = st.columns([2, 1])
with c1:
    fig = px.imshow(
        corr, color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
        title="Correlation Heatmap — Numeric Financial Variables",
        aspect="auto",
    )
    st.plotly_chart(fig, use_container_width=True)
with c2:
    st.markdown("**Top correlations with `max_monthly_emi`**")
    top_corr = corr[REGRESSION_TARGET].sort_values(ascending=False).drop(REGRESSION_TARGET).head(10)
    st.dataframe(top_corr.rename("correlation").to_frame(), use_container_width=True)

# ---------------------------------------------------------------------------
# 4. Demographic patterns
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">Demographic Risk Patterns</div>', unsafe_allow_html=True)
demo_cols = [c for c in ["gender", "marital_status", "education", "employment_type"] if c in df.columns]
tabs = st.tabs(demo_cols)
for tab, col in zip(tabs, demo_cols):
    with tab:
        grp = df.groupby([col, CLASSIFICATION_TARGET]).size().reset_index(name="count")
        fig = px.bar(
            grp, x=col, y="count", color=CLASSIFICATION_TARGET,
            barmode="group", color_discrete_map=ELIGIBILITY_COLORS,
            title=f"Eligibility by {col}",
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# 5. Credit score by eligibility
# ---------------------------------------------------------------------------
if "credit_score" in df.columns:
    st.markdown('<div class="section-title">Credit Score by Eligibility Class</div>', unsafe_allow_html=True)
    fig = px.box(
        df, x=CLASSIFICATION_TARGET, y="credit_score", color=CLASSIFICATION_TARGET,
        color_discrete_map=ELIGIBILITY_COLORS, title="Credit Score by Eligibility Class",
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# 6. Business insight summary
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">Business Insight Summary</div>', unsafe_allow_html=True)
summary_cols = [c for c in ["monthly_salary", "credit_score", "bank_balance"] if c in df.columns]
summary = df.groupby(CLASSIFICATION_TARGET)[summary_cols].mean().round(1)
st.dataframe(summary, use_container_width=True)
st.caption(
    "Eligible applicants show consistently higher average salary, credit score, and bank "
    "balance than High_Risk or Not_Eligible applicants — validating that the engineered "
    "financial-ratio features carry real signal for both target variables."
)
