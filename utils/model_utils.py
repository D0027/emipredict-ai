"""
Loads the artifacts exported by the Kaggle training notebook and reproduces
the exact same feature-engineering function used during training, so that
predictions made here match what the notebook evaluated.
"""
import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st

from utils.config import (
    PREPROCESSOR_PATH, LABEL_ENCODER_PATH, CLASSIFIER_PATH,
    REGRESSOR_PATH, FEATURE_CONFIG_PATH,
)


def artifacts_present() -> bool:
    return all(
        os.path.exists(p)
        for p in [PREPROCESSOR_PATH, LABEL_ENCODER_PATH, CLASSIFIER_PATH,
                  REGRESSOR_PATH, FEATURE_CONFIG_PATH]
    )


@st.cache_resource(show_spinner=False)
def load_artifacts():
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    label_encoder = joblib.load(LABEL_ENCODER_PATH)
    classifier = joblib.load(CLASSIFIER_PATH)
    regressor = joblib.load(REGRESSOR_PATH)
    feature_config = joblib.load(FEATURE_CONFIG_PATH)
    return {
        "preprocessor": preprocessor,
        "label_encoder": label_encoder,
        "classifier": classifier,
        "regressor": regressor,
        "feature_config": feature_config,
    }


def engineer_features(data: pd.DataFrame) -> pd.DataFrame:
    """Identical logic to the Kaggle notebook's engineer_features() —
    do not change this without retraining, or predictions will drift
    from the trained pipeline."""
    d = data.copy()

    expense_cols = [c for c in ["school_fees", "college_fees", "travel_expenses",
                                 "groceries_utilities", "other_monthly_expenses"] if c in d.columns]
    if expense_cols:
        d["total_monthly_expenses"] = d[expense_cols].sum(axis=1)

    if {"current_emi_amount", "monthly_salary"}.issubset(d.columns):
        d["debt_to_income_ratio"] = d["current_emi_amount"] / d["monthly_salary"].replace(0, np.nan)

    if "total_monthly_expenses" in d.columns and "monthly_salary" in d.columns:
        d["expense_to_income_ratio"] = d["total_monthly_expenses"] / d["monthly_salary"].replace(0, np.nan)

    if {"monthly_rent", "monthly_salary"}.issubset(d.columns):
        d["rent_to_income_ratio"] = d["monthly_rent"] / d["monthly_salary"].replace(0, np.nan)

    obligation_cols = [c for c in ["total_monthly_expenses", "current_emi_amount", "monthly_rent"] if c in d.columns]
    if obligation_cols and "monthly_salary" in d.columns:
        d["disposable_income"] = d["monthly_salary"] - d[obligation_cols].sum(axis=1)

    if {"requested_amount", "requested_tenure", "disposable_income"}.issubset(d.columns):
        d["affordability_ratio"] = d["requested_amount"] / (
            (d["disposable_income"].clip(lower=1)) * d["requested_tenure"].replace(0, np.nan)
        )

    if {"bank_balance", "monthly_salary"}.issubset(d.columns):
        d["savings_to_income_ratio"] = d["bank_balance"] / d["monthly_salary"].replace(0, np.nan)

    if {"emergency_fund", "monthly_salary"}.issubset(d.columns):
        d["emergency_fund_months"] = d["emergency_fund"] / d["monthly_salary"].replace(0, np.nan)

    if "years_of_employment" in d.columns:
        d["employment_stability_score"] = np.clip(d["years_of_employment"] / 10.0, 0, 1)

    if {"dependents", "family_size"}.issubset(d.columns):
        d["dependent_ratio"] = d["dependents"] / d["family_size"].replace(0, np.nan)

    if {"credit_score", "debt_to_income_ratio", "employment_stability_score"}.issubset(d.columns):
        norm_credit = (d["credit_score"] - 300) / (850 - 300)
        d["composite_risk_score"] = (
            0.5 * norm_credit
            + 0.3 * (1 - d["debt_to_income_ratio"].clip(0, 1))
            + 0.2 * d["employment_stability_score"]
        )

    if {"requested_amount", "requested_tenure"}.issubset(d.columns):
        d["implied_new_emi"] = d["requested_amount"] / d["requested_tenure"].replace(0, np.nan)

    d = d.replace([np.inf, -np.inf], np.nan)
    ratio_like_cols = [c for c in d.columns if "ratio" in c or "score" in c or c in
                        ["disposable_income", "implied_new_emi", "emergency_fund_months"]]
    for col in ratio_like_cols:
        if col in d.columns and d[col].isnull().any():
            d[col] = d[col].fillna(d[col].median())

    return d


def predict_single(raw_record: dict, artifacts: dict):
    """raw_record: dict of the 25 raw input fields (same names as training data).
    Returns (eligibility_label, eligibility_probabilities, predicted_max_emi)."""
    df = pd.DataFrame([raw_record])
    df_fe = engineer_features(df)

    feature_config = artifacts["feature_config"]
    all_cols = feature_config["all"]

    # Ensure every expected column exists (fill anything missing with 0/most common)
    for col in all_cols:
        if col not in df_fe.columns:
            df_fe[col] = 0

    X = df_fe[all_cols]
    X_processed = artifacts["preprocessor"].transform(X)

    clf = artifacts["classifier"]
    reg = artifacts["regressor"]
    label_encoder = artifacts["label_encoder"]

    pred_class_idx = clf.predict(X_processed)[0]
    pred_label = label_encoder.inverse_transform([pred_class_idx])[0]

    proba = None
    if hasattr(clf, "predict_proba"):
        proba_arr = clf.predict_proba(X_processed)[0]
        proba = dict(zip(label_encoder.classes_, proba_arr))

    pred_emi = float(reg.predict(X_processed)[0])

    return pred_label, proba, pred_emi
