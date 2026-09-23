import os
import urllib.parse
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text

DB_USER = "root"
RAW_PASS = "@k$#@y@07"
DB_PASS = urllib.parse.quote_plus(RAW_PASS)
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "sbi_merger_analytics_db"

def get_engine(database=None):
    db_part = f"/{database}" if database else ""
    return create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}{db_part}")

def setup_and_clean_data():
    raw_file = "sbi_merger_raw_4000.csv"
    if not os.path.exists(raw_file):
        raise FileNotFoundError(f"{raw_file} not found in current directory.")
    
    print("Loading raw dataset...")
    df = pd.read_csv(raw_file)

    df["entity_name"] = df["entity_name"].str.strip()
    df["merger_cutoff_date"] = pd.to_datetime(df["merger_cutoff_date"], format="mixed").dt.strftime("%Y-%m-%d")

    pct_cols = ["gross_npa_pct", "net_npa_pct", "cost_to_income_pct", "roa_pct", "casa_ratio_pct", "car_crar_pct"]
    for col in pct_cols:
        df[col] = df[col].astype(str).str.replace("%", "").str.strip()
        df[col] = pd.to_numeric(df[col], errors="coerce")

    curr_cols = ["advances_inr_cr", "deposits_inr_cr"]
    for col in curr_cols:
        df[col] = df[col].astype(str).str.replace(",", "").str.strip()
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["cost_to_income_pct"] = df.groupby("entity_name")["cost_to_income_pct"].transform(lambda s: s.fillna(s.median()))
    df["net_npa_pct"] = df.groupby("entity_name")["net_npa_pct"].transform(lambda s: s.fillna(s.median()))

    clean_file = "sbi_merger_branch_cleaned_4000.csv"
    df.to_csv(clean_file, index=False)
    print(f"Exported cleaned data to '{clean_file}'.")

    print("Connecting to MySQL...")
    server_engine = get_engine()
    with server_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};"))
        conn.commit()

    db_engine = get_engine(DB_NAME)
    df.to_sql(name="sbi_branch_metrics", con=db_engine, if_exists="replace", index=False)
    print(f"Successfully loaded 4,000 rows into MySQL table: {DB_NAME}.sbi_branch_metrics")

def fetch_data(query: str) -> pd.DataFrame:
    engine = get_engine(DB_NAME)
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)

if __name__ == "__main__":
    setup_and_clean_data()
