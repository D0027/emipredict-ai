"""
Central configuration for the EMIPredict AI Streamlit app.
Keep every path / constant here so pages never hardcode strings.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Artifacts exported from the Kaggle training notebook.
# Copy these 7 files from /kaggle/working/artifacts/ into ./artifacts/ locally.
PREPROCESSOR_PATH = os.path.join(ARTIFACTS_DIR, "preprocessor.pkl")
LABEL_ENCODER_PATH = os.path.join(ARTIFACTS_DIR, "target_label_encoder.pkl")
CLASSIFIER_PATH = os.path.join(ARTIFACTS_DIR, "best_classification_model.pkl")
REGRESSOR_PATH = os.path.join(ARTIFACTS_DIR, "best_regression_model.pkl")
FEATURE_CONFIG_PATH = os.path.join(ARTIFACTS_DIR, "feature_config.pkl")
CLF_COMPARISON_CSV = os.path.join(ARTIFACTS_DIR, "classification_model_comparison.csv")
REG_COMPARISON_CSV = os.path.join(ARTIFACTS_DIR, "regression_model_comparison.csv")

# Optional: the full 400K raw dataset, only needed for the EDA page and for
# recomputing test-set confusion matrix / actual-vs-predicted plots locally.
# Drop emi_prediction_dataset.csv here if you want those recomputed live.
RAW_DATASET_PATH = os.path.join(DATA_DIR, "emi_prediction_dataset.csv")

# Local CRUD store (SQLite) — created automatically on first run.
CRUD_DB_PATH = os.path.join(DATA_DIR, "emi_records.db")

CLASSIFICATION_TARGET = "emi_eligibility"
REGRESSION_TARGET = "max_monthly_emi"

EMI_SCENARIOS = [
    "E-commerce Shopping EMI",
    "Home Appliances EMI",
    "Vehicle EMI",
    "Personal Loan EMI",
    "Education EMI",
]

ELIGIBILITY_COLORS = {
    "Eligible": "#3EC6A8",
    "High_Risk": "#F6AE2D",
    "Not_Eligible": "#E63946",
}

# Project-spec targets (from Project_Title guidance doc) — used to render
# pass/fail badges on the Model Performance page.
TARGET_CLASSIFICATION_ACCURACY = 0.90
TARGET_REGRESSION_RMSE = 2000.0
