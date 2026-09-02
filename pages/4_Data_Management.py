import streamlit as st
import pandas as pd

from utils.styling import inject_css, header, eligibility_badge
from utils.crud import create_application, read_applications, update_application, delete_application
from utils.config import EMI_SCENARIOS

st.set_page_config(page_title="Data Management | EMIPredict AI", page_icon="🗄️", layout="wide")
inject_css()
header("🗄️ Data Management", "Create, view, update, and delete loan application records — the administrative CRUD interface for the platform.")

tab_view, tab_create, tab_edit, tab_delete = st.tabs(["📋 View All", "➕ Create", "✏️ Update", "🗑️ Delete"])

# ---------------------------------------------------------------------------
# VIEW
# ---------------------------------------------------------------------------
with tab_view:
    df = read_applications()
    if df.empty:
        st.info("No records yet. Add one from the **Create** tab, or save predictions from the Prediction Engine page.")
    else:
        st.markdown(f'<div class="data-strip">📋 {len(df)} application(s) on record</div>', unsafe_allow_html=True)
        filter_col, _ = st.columns([1, 3])
        with filter_col:
            filter_elig = st.multiselect(
                "Filter by predicted eligibility",
                options=sorted(df["predicted_eligibility"].dropna().unique().tolist()),
            )
        display_df = df[df["predicted_eligibility"].isin(filter_elig)] if filter_elig else df
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        csv = display_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Export as CSV", csv, "emi_applications.csv", "text/csv")

# ---------------------------------------------------------------------------
# CREATE
# ---------------------------------------------------------------------------
with tab_create:
    st.markdown("Add a record directly (without running it through the prediction engine).")
    with st.form("create_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            applicant_name = st.text_input("Applicant name")
            age = st.number_input("Age", 18, 100, 35)
        with c2:
            gender = st.selectbox("Gender", ["Male", "Female"])
            monthly_salary = st.number_input("Monthly salary (₹)", min_value=0.0, value=50000.0, step=1000.0)
        with c3:
            employment_type = st.selectbox("Employment type", ["Private", "Government", "Self-employed"])
            credit_score = st.number_input("Credit score", 300, 850, 700)

        c1, c2, c3 = st.columns(3)
        with c1:
            emi_scenario = st.selectbox("EMI scenario", EMI_SCENARIOS)
        with c2:
            requested_amount = st.number_input("Requested amount (₹)", min_value=1000.0, value=100000.0, step=1000.0)
        with c3:
            requested_tenure = st.number_input("Requested tenure (months)", 1, 120, 24)

        predicted_eligibility = st.selectbox("Predicted eligibility (manual entry)", ["Eligible", "High_Risk", "Not_Eligible"])
        predicted_max_emi = st.number_input("Predicted max EMI (₹)", min_value=0.0, value=5000.0, step=100.0)
        notes = st.text_area("Notes")

        if st.form_submit_button("Create record", use_container_width=True):
            new_id = create_application({
                "applicant_name": applicant_name or "Unnamed", "age": age, "gender": gender,
                "monthly_salary": monthly_salary, "employment_type": employment_type,
                "emi_scenario": emi_scenario, "requested_amount": requested_amount,
                "requested_tenure": requested_tenure, "credit_score": credit_score,
                "predicted_eligibility": predicted_eligibility, "predicted_max_emi": predicted_max_emi,
                "notes": notes,
            })
            st.success(f"Created application #{new_id}.")

# ---------------------------------------------------------------------------
# UPDATE
# ---------------------------------------------------------------------------
with tab_edit:
    df = read_applications()
    if df.empty:
        st.info("No records to update yet.")
    else:
        record_id = st.selectbox("Select record ID to edit", df["id"].tolist())
        record = df[df["id"] == record_id].iloc[0]

        with st.form("update_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                applicant_name = st.text_input("Applicant name", value=record["applicant_name"])
                age = st.number_input("Age", 18, 100, int(record["age"]))
            with c2:
                monthly_salary = st.number_input("Monthly salary (₹)", min_value=0.0, value=float(record["monthly_salary"]))
                credit_score = st.number_input("Credit score", 300, 850, int(record["credit_score"]))
            with c3:
                predicted_eligibility = st.selectbox(
                    "Predicted eligibility", ["Eligible", "High_Risk", "Not_Eligible"],
                    index=["Eligible", "High_Risk", "Not_Eligible"].index(record["predicted_eligibility"])
                    if record["predicted_eligibility"] in ["Eligible", "High_Risk", "Not_Eligible"] else 0,
                )
                predicted_max_emi = st.number_input("Predicted max EMI (₹)", min_value=0.0, value=float(record["predicted_max_emi"]))
            notes = st.text_area("Notes", value=record["notes"] or "")

            if st.form_submit_button("Save changes", use_container_width=True):
                update_application(int(record_id), {
                    "applicant_name": applicant_name, "age": age, "monthly_salary": monthly_salary,
                    "credit_score": credit_score, "predicted_eligibility": predicted_eligibility,
                    "predicted_max_emi": predicted_max_emi, "notes": notes,
                })
                st.success(f"Updated application #{record_id}.")
                st.rerun()

# ---------------------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------------------
with tab_delete:
    df = read_applications()
    if df.empty:
        st.info("No records to delete.")
    else:
        record_id = st.selectbox("Select record ID to delete", df["id"].tolist(), key="delete_select")
        record = df[df["id"] == record_id].iloc[0]
        st.markdown(
            f"""
            <div class="delete-preview">
                <b>Applicant:</b> {record['applicant_name']} &nbsp;·&nbsp; <b>Eligibility:</b>
                {eligibility_badge(record['predicted_eligibility'])} &nbsp;·&nbsp; <b>Max EMI:</b> ₹{record['predicted_max_emi']:,.0f}
            </div>
            """,
            unsafe_allow_html=True,
        )
        confirm = st.checkbox(f"I confirm I want to permanently delete application #{record_id}.")
        if st.button("🗑️ Delete record", disabled=not confirm, use_container_width=True):
            delete_application(int(record_id))
            st.success(f"Deleted application #{record_id}.")
            st.rerun()
