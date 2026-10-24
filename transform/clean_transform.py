import pandas as pd
from sqlalchemy import create_engine

DB_PATH = "sqlite:///indus_weave_hr.db"
engine = create_engine(DB_PATH)

def clean_and_transform():
    print("=== STAGE 2 & 3: CLEANING & BUSINESS RULES ===")
    try:
        emp_df = pd.read_sql("SELECT * FROM raw_employees", con=engine)
        emp_df["updated_at_dt"] = pd.to_datetime(emp_df.get("updated_at", pd.Series()), errors="coerce")
        emp_df = emp_df.sort_values("updated_at_dt").groupby("emp_id").last().reset_index()
        emp_df.to_sql("staging_employees", con=engine, if_exists="replace", index=False)
        print(f"Staged {len(emp_df)} unique employees.")
    except Exception as e:
        print("Transform note:", e)

if __name__ == "__main__":
    clean_and_transform()
