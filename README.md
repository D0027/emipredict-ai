# EMIPredict AI — Local Streamlit App

Implements **Step 6 (Streamlit application)** of the EMIPredict AI project guidance, built on
top of the models trained in `emipredict-ai-notebook.ipynb` on Kaggle (Steps 1–5).

This app does **not** retrain anything. It loads the artifacts your Kaggle notebook already
exported and serves them for real-time prediction, EDA, model comparison, and CRUD data
management.

## 1. Project structure

```
emipredict_app/
├── Home.py                          # Landing dashboard
├── pages/
│   ├── 1_📊_Data_Exploration.py     # Step 2 EDA, reproduced interactively
│   ├── 2_🎯_Prediction_Engine.py    # Real-time classification + regression predictions
│   ├── 3_📈_Model_Performance.py    # Model comparison, feature importance, MLflow summary
│   └── 4_🗄️_Data_Management.py     # CRUD for loan application records
├── utils/
│   ├── config.py                    # All paths/constants
│   ├── model_utils.py               # Artifact loading + exact feature-engineering logic
│   ├── crud.py                      # SQLite CRUD layer
│   └── styling.py                   # Custom CSS / UI components
├── artifacts/                       # <-- put your Kaggle artifacts here (see step 3 below)
├── data/                            # <-- optionally put the raw CSV here (see step 3 below)
├── requirements.txt
└── .streamlit/config.toml           # Dark fintech theme
```

## 2. Install locally

```bash
cd emipredict_app
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Important:** the scikit-learn / xgboost versions installed locally should match (or be
compatible with) the versions Kaggle used when the `.pkl` files were pickled. If you hit an
`unpickling` error, check the versions Kaggle installed (`!pip show scikit-learn xgboost` in a
Kaggle cell) and match them in `requirements.txt`.

## 3. Copy your trained artifacts from Kaggle (required)

You do **not** need to retrain. From your Kaggle notebook's Output panel
(`/kaggle/working/artifacts/`), download these 7 files and place them in the local
`artifacts/` folder, keeping the exact filenames:

- `preprocessor.pkl`
- `target_label_encoder.pkl`
- `best_classification_model.pkl`
- `best_regression_model.pkl`
- `feature_config.pkl`
- `classification_model_comparison.csv`
- `regression_model_comparison.csv`

**Optional but recommended** — for the full EDA page and for the app to recompute the
confusion matrix / actual-vs-predicted plot live: also copy the raw
`emi_prediction_dataset.csv` into the local `data/` folder.

**Optional** — for the local MLflow UI: copy `mlflow.db` (and the `mlruns/` folder, if you
used the filesystem store) into the project root, then run:
```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

## 4. Run the app

```bash
streamlit run Home.py
```

Opens at `http://localhost:8501`. The sidebar lets you navigate between pages.

## 5. What each page covers vs. the guidance doc

| Guidance requirement | Where it's implemented |
|---|---|
| Multi-page app, intuitive UI | `Home.py` + 4 pages, custom dark theme, KPI cards |
| Real-time classification + regression prediction | `2_🎯_Prediction_Engine.py` |
| Interactive data exploration/visualization | `1_📊_Data_Exploration.py` (every chart from Step 2 of the notebook) |
| Model performance / MLflow dashboard | `3_📈_Model_Performance.py` |
| CRUD for financial data management | `4_🗄️_Data_Management.py` (SQLite-backed) |

## 6. Deploying to Streamlit Cloud (Step 7)

1. Push this whole folder (including populated `artifacts/`, excluding the large raw CSV if
   it's too big for GitHub — the app works without it, just without live EDA/recompute) to a
   GitHub repo.
2. If the raw CSV is large, either use Git LFS, host it externally and adjust
   `RAW_DATASET_PATH`, or skip it — the Prediction Engine and Model Performance pages (minus
   the live confusion-matrix recompute) work from the `.pkl`/CSV artifacts alone.
3. Go to [share.streamlit.io](https://share.streamlit.io), connect your GitHub repo, set the
   main file to `Home.py`, and deploy.
4. Streamlit Cloud installs from `requirements.txt` automatically.
