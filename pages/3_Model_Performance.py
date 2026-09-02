import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

from utils.styling import inject_css, header, kpi_card, pass_fail_badge
from utils.model_utils import artifacts_present, load_artifacts, engineer_features
from utils.config import (
    CLF_COMPARISON_CSV, REG_COMPARISON_CSV, RAW_DATASET_PATH,
    CLASSIFICATION_TARGET, REGRESSION_TARGET, ELIGIBILITY_COLORS,
    TARGET_CLASSIFICATION_ACCURACY, TARGET_REGRESSION_RMSE,
)

st.set_page_config(page_title="Model Performance | EMIPredict AI", page_icon="📈", layout="wide")
inject_css()
header("📈 Model Performance & MLflow Tracking", "Comparison across every trained model, champion selection, and experiment-tracking summary.")

if not artifacts_present() or not (os.path.exists(CLF_COMPARISON_CSV) and os.path.exists(REG_COMPARISON_CSV)):
    st.error(
        "Comparison CSVs / artifacts not found. Copy `classification_model_comparison.csv`, "
        "`regression_model_comparison.csv`, and the `.pkl` files from Kaggle's "
        "`/kaggle/working/artifacts/` into the local `artifacts/` folder."
    )
    st.stop()

clf_df = pd.read_csv(CLF_COMPARISON_CSV)
reg_df = pd.read_csv(REG_COMPARISON_CSV)
artifacts = load_artifacts()

best_clf = clf_df.sort_values("f1_score", ascending=False).iloc[0]
best_reg = reg_df.sort_values("rmse", ascending=True).iloc[0]

# ---------------------------------------------------------------------------
# Headline KPIs vs project-spec targets
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">Champion Models vs. Project Targets</div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Best Classifier", best_clf["model"], f"F1: {best_clf['f1_score']:.4f}")
with c2:
    acc_pass = best_clf["accuracy"] >= TARGET_CLASSIFICATION_ACCURACY
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-label">Accuracy</div>'
        f'<div class="kpi-value">{best_clf["accuracy"]*100:.2f}%</div>'
        f'<div class="kpi-sub">{pass_fail_badge(acc_pass, "PASS" if acc_pass else "FAIL")} target &gt;{TARGET_CLASSIFICATION_ACCURACY*100:.0f}%</div></div>',
        unsafe_allow_html=True,
    )
with c3:
    kpi_card("Best Regressor", best_reg["model"], f"R²: {best_reg['r2_score']:.4f}")
with c4:
    rmse_pass = best_reg["rmse"] <= TARGET_REGRESSION_RMSE
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-label">RMSE</div>'
        f'<div class="kpi-value">₹{best_reg["rmse"]:,.0f}</div>'
        f'<div class="kpi-sub">{pass_fail_badge(rmse_pass, "PASS" if rmse_pass else "FAIL")} target &lt;₹{TARGET_REGRESSION_RMSE:,.0f}</div></div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Classification model comparison
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">Classification Models — All Runs</div>', unsafe_allow_html=True)
c1, c2 = st.columns([1, 1])
with c1:
    st.dataframe(
        clf_df.sort_values("f1_score", ascending=False)
        .style.format({"accuracy": "{:.2%}", "precision": "{:.2%}", "recall": "{:.2%}",
                        "f1_score": "{:.2%}", "roc_auc": "{:.4f}"})
        .highlight_max(subset=["f1_score"], color="rgba(62,198,168,0.25)"),
        use_container_width=True, hide_index=True,
    )
with c2:
    metric_long = clf_df.melt(id_vars="model", value_vars=["accuracy", "precision", "recall", "f1_score"],
                               var_name="metric", value_name="value")
    fig = px.bar(metric_long, x="model", y="value", color="metric", barmode="group",
                 title="Classification Metrics by Model")
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Regression model comparison
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">Regression Models — All Runs</div>', unsafe_allow_html=True)
c1, c2 = st.columns([1, 1])
with c1:
    st.dataframe(
        reg_df.sort_values("rmse", ascending=True)
        .style.format({"rmse": "₹{:.2f}", "mae": "₹{:.2f}", "r2_score": "{:.4f}", "mape": "{:.2f}%"})
        .highlight_min(subset=["rmse"], color="rgba(62,198,168,0.25)"),
        use_container_width=True, hide_index=True,
    )
with c2:
    fig = px.bar(reg_df.sort_values("rmse"), x="model", y="rmse", color="model",
                 title="RMSE by Model (lower is better)", color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Feature importance for champion models
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">Feature Importance — Champion Models</div>', unsafe_allow_html=True)
feature_config = artifacts["feature_config"]
preprocessor = artifacts["preprocessor"]
cat_features = feature_config["categorical"]
num_features = feature_config["numeric"]

tabs = st.tabs(["Classification", "Regression"])
for tab, model, label in zip(tabs, [artifacts["classifier"], artifacts["regressor"]], ["Classification", "Regression"]):
    with tab:
        if hasattr(model, "feature_importances_"):
            try:
                cat_names = list(preprocessor.named_transformers_["cat"].get_feature_names_out(cat_features)) if cat_features else []
            except Exception:
                cat_names = []
            feature_names = num_features + cat_names
            importances = pd.Series(model.feature_importances_[:len(feature_names)], index=feature_names)
            importances = importances.sort_values(ascending=False).head(15)
            fig = px.bar(
                x=importances.values[::-1], y=importances.index[::-1], orientation="h",
                labels={"x": "Importance", "y": ""}, title=f"Top 15 Feature Importances — {label}",
                color_discrete_sequence=["#3EC6A8"],
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"{type(model).__name__} has no native feature_importances_.")

# ---------------------------------------------------------------------------
# Optional: recompute confusion matrix / actual-vs-predicted if raw data present
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">Held-out Test Set Diagnostics</div>', unsafe_allow_html=True)
if os.path.exists(RAW_DATASET_PATH):
    with st.spinner("Recomputing test-set diagnostics from local dataset..."):
        df = pd.read_csv(RAW_DATASET_PATH, low_memory=False)
        for col in ["age", "monthly_salary", "bank_balance"]:
            if col in df.columns and df[col].dtype == object:
                df[col] = pd.to_numeric(df[col].astype(str).str.extract(r"^(-?\d+\.?\d*)")[0], errors="coerce")
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        for col in num_cols:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].median())
        cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
        for col in cat_cols:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].mode()[0])

        from sklearn.model_selection import train_test_split
        _, test_df = train_test_split(df, test_size=0.15, random_state=42, stratify=df[CLASSIFICATION_TARGET])
        test_fe = engineer_features(test_df)
        all_cols = feature_config["all"]
        for col in all_cols:
            if col not in test_fe.columns:
                test_fe[col] = 0
        X_test = preprocessor.transform(test_fe[all_cols])

        label_encoder = artifacts["label_encoder"]
        y_test_clf = label_encoder.transform(test_fe[CLASSIFICATION_TARGET])
        y_test_reg = test_fe[REGRESSION_TARGET].values

        from sklearn.metrics import confusion_matrix, mean_squared_error, r2_score
        clf_preds = artifacts["classifier"].predict(X_test)
        cm = confusion_matrix(y_test_clf, clf_preds)

        c1, c2 = st.columns(2)
        with c1:
            fig = px.imshow(
                cm, text_auto=True, color_continuous_scale="Teal",
                x=list(label_encoder.classes_), y=list(label_encoder.classes_),
                labels={"x": "Predicted", "y": "Actual"},
                title=f"Confusion Matrix — {best_clf['model']} (Test Set)",
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            reg_preds = artifacts["regressor"].predict(X_test)
            plot_df = pd.DataFrame({"actual": y_test_reg, "predicted": reg_preds}).sample(
                min(5000, len(y_test_reg)), random_state=42
            )
            fig = px.scatter(
                plot_df, x="actual", y="predicted", opacity=0.3,
                title=f"Actual vs Predicted — {best_reg['model']} (Test Set)",
                color_discrete_sequence=["#3EC6A8"],
            )
            fig.add_shape(type="line", x0=plot_df["actual"].min(), y0=plot_df["actual"].min(),
                          x1=plot_df["actual"].max(), y1=plot_df["actual"].max(),
                          line=dict(color="#E63946", dash="dash"))
            st.plotly_chart(fig, use_container_width=True)

        test_rmse = np.sqrt(mean_squared_error(y_test_reg, reg_preds))
        test_r2 = r2_score(y_test_reg, reg_preds)
        st.caption(f"Recomputed on held-out test split: RMSE = ₹{test_rmse:,.2f} | R² = {test_r2:.4f}")
else:
    st.info(
        "Drop `emi_prediction_dataset.csv` into the local `data/` folder to recompute the "
        "confusion matrix and actual-vs-predicted plot live on your held-out test split. "
        "The model comparison tables and feature importance above work without it."
    )


# ---------------------------------------------------------------------------
# Experiment Log — public-safe summary of all MLflow runs
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">Experiment Log</div>', unsafe_allow_html=True)
st.caption("Every model run tracked in MLflow, identified by its unique run ID.")

log_tab1, log_tab2 = st.tabs(["Classification Runs", "Regression Runs"])
with log_tab1:
    clf_log = clf_df[["model", "accuracy", "f1_score", "roc_auc", "run_id"]].sort_values("f1_score", ascending=False)
    st.dataframe(
        clf_log.style.format({"accuracy": "{:.2%}", "f1_score": "{:.2%}", "roc_auc": "{:.4f}"}),
        use_container_width=True, hide_index=True,
    )
with log_tab2:
    reg_log = reg_df[["model", "rmse", "r2_score", "mape", "run_id"]].sort_values("rmse", ascending=True)
    st.dataframe(
        reg_log.style.format({"rmse": "₹{:.2f}", "r2_score": "{:.4f}", "mape": "{:.2f}%"}),
        use_container_width=True, hide_index=True,
    )


# ---------------------------------------------------------------------------
# MLflow experiment tracking summary
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">MLflow Experiment Tracking</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="info-panel">
    <p>Training runs were tracked with MLflow using a SQLite-backed store
    (<code>sqlite:///mlflow.db</code>), with two experiments: <b>EMIPredict_Classification</b> and
    <b>EMIPredict_Regression</b>. Every model run logged its full hyperparameter set, evaluation
    metrics, and a serialized model artifact. The two champion models above were promoted to
    the <b>Production</b> stage in the MLflow Model Registry
    (<code>models:/EMIPredict_Classifier/Production</code>, <code>models:/EMIPredict_Regressor/Production</code>).</p>
    <p>To browse the full MLflow UI locally: copy <code>mlflow.db</code> from Kaggle's output into this
    project folder and run:</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.code("mlflow ui --backend-store-uri sqlite:///mlflow.db", language="bash")
st.caption("Then open http://localhost:5000 in your browser to explore every run, compare parameters, and inspect logged artifacts.")
