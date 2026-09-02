import streamlit as st
import pandas as pd

from utils.styling import inject_css, header, eligibility_badge
from utils.model_utils import artifacts_present, load_artifacts, predict_single
from utils.crud import create_application
from utils.config import EMI_SCENARIOS

st.set_page_config(page_title="Prediction Engine | EMIPredict AI", page_icon="🎯", layout="wide")
inject_css()
header("🎯 Real-Time Prediction Engine", "Enter an applicant's financial profile to get instant EMI eligibility and maximum safe EMI predictions.")

if not artifacts_present():
    st.error(
        "Model artifacts not found in `artifacts/`. Copy the 5 `.pkl` files from your Kaggle "
        "notebook's `/kaggle/working/artifacts/` output into the local `artifacts/` folder, then "
        "refresh this page."
    )
    st.stop()

artifacts = load_artifacts()

st.markdown('<div class="section-title">Applicant Profile</div>', unsafe_allow_html=True)

with st.form("prediction_form"):
    st.markdown("**Personal & Demographics**")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        applicant_name = st.text_input("Applicant name", value="")
        age = st.number_input("Age", min_value=18, max_value=100, value=35)
    with c2:
        gender = st.selectbox("Gender", ["Male", "Female"])
        marital_status = st.selectbox("Marital status", ["Single", "Married"])
    with c3:
        education = st.selectbox("Education", ["High School", "Graduate", "Post Graduate", "Professional"])
        employment_type = st.selectbox("Employment type", ["Private", "Government", "Self-employed"])
    with c4:
        years_of_employment = st.number_input("Years of employment", min_value=0.0, max_value=45.0, value=5.0, step=0.5)
        company_type = st.selectbox("Company type", ["Startup", "Mid-size", "Large Indian", "MNC", "Government"])

    st.markdown("**Housing & Family**")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        house_type = st.selectbox("House type", ["Rented", "Own", "Family"])
    with c2:
        monthly_rent = st.number_input("Monthly rent (₹)", min_value=0.0, value=10000.0, step=500.0)
    with c3:
        family_size = st.number_input("Family size", min_value=1, max_value=10, value=4)
    with c4:
        dependents = st.number_input("Dependents", min_value=0, max_value=10, value=2)

    st.markdown("**Monthly Financial Obligations (₹)**")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        school_fees = st.number_input("School fees", min_value=0.0, value=0.0, step=500.0)
    with c2:
        college_fees = st.number_input("College fees", min_value=0.0, value=0.0, step=500.0)
    with c3:
        travel_expenses = st.number_input("Travel expenses", min_value=0.0, value=4000.0, step=200.0)
    with c4:
        groceries_utilities = st.number_input("Groceries & utilities", min_value=0.0, value=10000.0, step=500.0)
    with c5:
        other_monthly_expenses = st.number_input("Other expenses", min_value=0.0, value=5000.0, step=500.0)

    st.markdown("**Financial Status & Credit History**")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        monthly_salary = st.number_input("Monthly salary (₹)", min_value=0.0, value=60000.0, step=1000.0)
    with c2:
        existing_loans = st.selectbox("Existing loans?", ["No", "Yes"])
    with c3:
        current_emi_amount = st.number_input("Current EMI amount (₹)", min_value=0.0, value=0.0, step=500.0)
    with c4:
        credit_score = st.number_input("Credit score", min_value=300, max_value=850, value=720)
    with c5:
        bank_balance = st.number_input("Bank balance (₹)", min_value=0.0, value=150000.0, step=1000.0)

    c1, c2 = st.columns(2)
    with c1:
        emergency_fund = st.number_input("Emergency fund (₹)", min_value=0.0, value=50000.0, step=1000.0)
    with c2:
        pass

    st.markdown("**Loan Application Details**")
    c1, c2, c3 = st.columns(3)
    with c1:
        emi_scenario = st.selectbox("EMI scenario", EMI_SCENARIOS)
    with c2:
        requested_amount = st.number_input("Requested amount (₹)", min_value=1000.0, value=200000.0, step=1000.0)
    with c3:
        requested_tenure = st.number_input("Requested tenure (months)", min_value=1, max_value=120, value=24)

    submitted = st.form_submit_button("🔮 Run Prediction", use_container_width=True)

if submitted:
    raw_record = {
        "age": age, "gender": gender, "marital_status": marital_status, "education": education,
        "monthly_salary": monthly_salary, "employment_type": employment_type,
        "years_of_employment": years_of_employment, "company_type": company_type,
        "house_type": house_type, "monthly_rent": monthly_rent, "family_size": family_size,
        "dependents": dependents, "school_fees": school_fees, "college_fees": college_fees,
        "travel_expenses": travel_expenses, "groceries_utilities": groceries_utilities,
        "other_monthly_expenses": other_monthly_expenses, "existing_loans": existing_loans,
        "current_emi_amount": current_emi_amount, "credit_score": credit_score,
        "bank_balance": bank_balance, "emergency_fund": emergency_fund,
        "emi_scenario": emi_scenario, "requested_amount": requested_amount,
        "requested_tenure": requested_tenure,
    }

    label, proba, pred_emi = predict_single(raw_record, artifacts)

    # Persist in session_state so the result + checkbox survive reruns
    # (clicking the checkbox itself triggers a rerun, which would otherwise
    # wipe out `submitted` and lose the result).
    st.session_state["last_prediction"] = {
        "raw_record": raw_record,
        "applicant_name": applicant_name,
        "label": label,
        "proba": proba,
        "pred_emi": pred_emi,
    }

if "last_prediction" in st.session_state:
    p = st.session_state["last_prediction"]
    raw_record = p["raw_record"]

    st.markdown('<div class="section-title">Prediction Result</div>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1:
        st.markdown(
            f"""
            <div class="predict-result-card">
                <div class="result-label">EMI Eligibility</div>
                {eligibility_badge(p['label'])}
            </div>
            """,
            unsafe_allow_html=True,
        )
        if p["proba"]:
            proba_df = pd.DataFrame({"class": list(p["proba"].keys()), "probability": list(p["proba"].values())})
            proba_df = proba_df.sort_values("probability", ascending=False)
            st.dataframe(
                proba_df.style.format({"probability": "{:.1%}"}),
                use_container_width=True, hide_index=True,
            )
    with r2:
        st.metric("Predicted Maximum Safe Monthly EMI", f"₹{p['pred_emi']:,.0f}")
        implied_emi = raw_record["requested_amount"] / max(raw_record["requested_tenure"], 1)
        if p["pred_emi"] < implied_emi:
            st.caption("⚠️ Requested EMI implied by amount/tenure exceeds the model's recommended safe maximum.")
        else:
            st.caption("✅ Implied EMI from the request is within the model's recommended safe maximum.")

    save = st.checkbox("Save this application to Data Management records", key="save_checkbox")
    if save and not st.session_state.get("last_saved_id"):
        record_id = create_application({
            "applicant_name": p["applicant_name"] or "Unnamed",
            "age": raw_record["age"], "gender": raw_record["gender"],
            "monthly_salary": raw_record["monthly_salary"],
            "employment_type": raw_record["employment_type"],
            "emi_scenario": raw_record["emi_scenario"],
            "requested_amount": raw_record["requested_amount"],
            "requested_tenure": raw_record["requested_tenure"],
            "credit_score": raw_record["credit_score"],
            "predicted_eligibility": p["label"], "predicted_max_emi": p["pred_emi"], "notes": "",
        })
        st.session_state["last_saved_id"] = record_id
        st.success(f"Saved as application #{record_id}. View it on the Data Management page.")
    elif save and st.session_state.get("last_saved_id"):
        st.success(f"Already saved as application #{st.session_state['last_saved_id']}.")
    elif not save:
        st.session_state["last_saved_id"] = None