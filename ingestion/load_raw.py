import os, glob, hashlib, json
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

DB_PATH = "sqlite:///indus_weave_hr.db"
engine = create_engine(DB_PATH)
DATA_DIR = "data"

def compute_row_hash(val_str):
    return hashlib.md5(str(val_str).encode('utf-8')).hexdigest()

def ingest_all():
    print("=== STAGE 1: INGESTING RAW DATA ===")
    if not os.path.exists(DATA_DIR):
        print(f"Error: '{DATA_DIR}' folder not found.")
        return

    for file_path in glob.glob(os.path.join(DATA_DIR, "*.csv")):
        filename = os.path.basename(file_path)
        table_name = f"raw_{filename.replace('.csv', '')}"
        df = pd.read_csv(file_path, dtype=str)
        df["_source_file"] = filename
        df["_loaded_at"] = datetime.now().isoformat()
        df["_row_hash"] = df.apply(lambda r: compute_row_hash("".join(r.dropna().values)), axis=1)
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
        print(f"Loaded {len(df)} rows into '{table_name}'")

if __name__ == "__main__":
    ingest_all()
