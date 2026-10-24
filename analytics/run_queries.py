import os, pandas as pd
from sqlalchemy import create_engine

DB_PATH = "sqlite:///indus_weave_hr.db"
engine = create_engine(DB_PATH)
RESULTS_DIR = os.path.join("analytics", "results")

def run_all_queries():
    print("=== STAGE 5: RUNNING ANALYTICS QUERIES ===")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    queries = {
        "q01_headcount": "SELECT department_id, COUNT(DISTINCT emp_id) as headcount FROM dim_employee GROUP BY department_id;",
        "q04_top_late_arrivals": "SELECT emp_id, COUNT(*) as late_count FROM fact_attendance_daily WHERE late_minutes > 10 GROUP BY emp_id ORDER BY late_count DESC LIMIT 10;"
    }
    with engine.connect() as conn:
        for name, q in queries.items():
            path = os.path.join(RESULTS_DIR, f"{name}.csv")
            try:
                df = pd.read_sql(q, conn)
            except Exception:
                df = pd.DataFrame()
            df.to_csv(path, index=False)
            print(f"Saved {name}.csv")

if __name__ == "__main__":
    run_all_queries()
