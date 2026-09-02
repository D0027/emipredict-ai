"""
Lightweight CRUD layer backed by SQLite for the 'Data Management' page.
Stores loan applications the user enters through the app (separate from the
400K training dataset), with the model's predictions attached to each row.
"""
import sqlite3
import pandas as pd
from datetime import datetime

from utils.config import CRUD_DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT,
    applicant_name TEXT,
    age INTEGER,
    gender TEXT,
    monthly_salary REAL,
    employment_type TEXT,
    emi_scenario TEXT,
    requested_amount REAL,
    requested_tenure INTEGER,
    credit_score REAL,
    predicted_eligibility TEXT,
    predicted_max_emi REAL,
    notes TEXT
);
"""


def get_conn():
    conn = sqlite3.connect(CRUD_DB_PATH, check_same_thread=False)
    conn.execute(SCHEMA)
    conn.commit()
    return conn


def create_application(record: dict) -> int:
    conn = get_conn()
    record = {**record, "created_at": datetime.utcnow().isoformat(timespec="seconds")}
    cols = ", ".join(record.keys())
    placeholders = ", ".join(["?"] * len(record))
    cur = conn.execute(
        f"INSERT INTO applications ({cols}) VALUES ({placeholders})",
        list(record.values()),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def read_applications() -> pd.DataFrame:
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM applications ORDER BY id DESC", conn)
    conn.close()
    return df


def update_application(record_id: int, updates: dict):
    conn = get_conn()
    set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
    conn.execute(
        f"UPDATE applications SET {set_clause} WHERE id = ?",
        list(updates.values()) + [record_id],
    )
    conn.commit()
    conn.close()


def delete_application(record_id: int):
    conn = get_conn()
    conn.execute("DELETE FROM applications WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
