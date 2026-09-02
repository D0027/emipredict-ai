<div align="center">

# 💳 EMIPredict AI

### Intelligent Financial Risk Assessment Platform

*Dual ML pipeline for EMI eligibility classification & maximum safe EMI regression — tracked end-to-end with MLflow.*

[![Live App](https://img.shields.io/badge/🚀_Live_App-Streamlit-3EC6A8?style=for-the-badge)](https://emipredict-ai-027.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-006ACC?style=for-the-badge)](https://xgboost.ai/)
[![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)](https://mlflow.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](#)

**[🔗 Try the Live App →](https://emipredict-ai-027.streamlit.app/)**

</div>

---

## 📌 Overview

**EMIPredict AI** is a full-stack machine learning platform that assesses loan applicant risk in real time. It combines two ML models working together:

| Model | Task | Output |
|---|---|---|
| 🎯 **Classification** | Is the applicant eligible? | `Eligible` · `High_Risk` · `Not_Eligible` |
| 📈 **Regression** | What's the max safe EMI? | Predicted ₹ amount per month |

Trained on **400,000 records** across 5 EMI scenarios, with **33 engineered features**, and champion models selected via automated comparison — all tracked with **MLflow**.

---

## ✨ Key Results

<div align="center">

| Metric | Result | Target | Status |
|:---:|:---:|:---:|:---:|
| **Best Classifier** | XGBoost | — | — |
| **Accuracy** | 98.65% | > 90% | ✅ **PASS** |
| **Best Regressor** | XGBoost Regressor | — | — |
| **RMSE** | ₹581 | < ₹2,000 | ✅ **PASS** |

</div>

---

## 🖥️ App Pages

| Page | What it does |
|---|---|
| 🏠 **Home** | Platform overview, KPIs, and navigation |
| 📊 **Data Exploration** | Interactive EDA — distributions, correlations, demographic risk patterns |
| 🎯 **Prediction Engine** | Real-time eligibility + max EMI prediction from a live form |
| 📈 **Model Performance** | Full model comparison, feature importance, confusion matrix, MLflow experiment log |
| 🗄️ **Data Management** | CRUD interface for loan application records (SQLite-backed) |

---

## 🛠️ Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Scikit--learn](https://img.shields.io/badge/-Scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![XGBoost](https://img.shields.io/badge/-XGBoost-006ACC?style=flat-square)
![Pandas](https://img.shields.io/badge/-Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/-Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![MLflow](https://img.shields.io/badge/-MLflow-0194E2?style=flat-square&logo=mlflow&logoColor=white)
![SQLite](https://img.shields.io/badge/-SQLite-07405E?style=flat-square&logo=sqlite&logoColor=white)

</div>

**Models compared:** XGBoost, Random Forest, Decision Tree, Logistic Regression (classification) · XGBoost Regressor, Random Forest, Decision Tree, Linear Regression (regression)

---

## 📁 Project Structure
emipredict_app/
├── Home.py # Landing dashboard
├── pages/
│ ├── 1_Data_Exploration.py # Interactive EDA
│ ├── 2_Prediction_Engine.py # Real-time predictions
│ ├── 3_Model_Performance.py # Model comparison + MLflow log
│ └── 4_Data_Management.py # CRUD interface
├── utils/
│ ├── config.py # Paths & constants
│ ├── model_utils.py # Artifact loading + feature engineering
│ ├── crud.py # SQLite CRUD layer
│ └── styling.py # Custom CSS / UI components
├── artifacts/ # Trained model artifacts (.pkl, comparison CSVs)
├── data/ # Raw dataset (optional, for live EDA)
├── requirements.txt
└── .streamlit/config.toml # Theme config


---

## 🚀 Run Locally

```bash
git clone https://github.com/D0027/emipredict-ai.git
cd emipredict-ai

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
streamlit run Home.py
```

App opens at `http://localhost:8501`.

> ⚠️ **Note:** Model artifacts (`.pkl` files) are already included in `artifacts/`. If you retrain on your own data, keep the same filenames so the app picks them up automatically.

---

## 🧠 Model Training Pipeline

1. **Data Prep** — cleaning, missing-value handling, type coercion
2. **EDA** — eligibility distributions, correlation analysis, demographic risk patterns
3. **Feature Engineering** — 22 raw → 33 engineered features
4. **Model Training** — multiple classifiers & regressors compared head-to-head
5. **MLflow Tracking** — every run logged with hyperparameters, metrics, and artifacts
6. **Streamlit App** — this repository (real-time inference + dashboards)

All training was performed on Kaggle; this app loads the exported artifacts and serves predictions — **no retraining happens in the app itself**.

---

## 📄 License

This project is open-sourced under the MIT License.

---

<div align="center">

**Built with ❤️ using Python, Streamlit & Scikit-learn**

[🔗 Live App](https://emipredict-ai-027.streamlit.app/) · [🐛 Report an Issue](#)

</div>
