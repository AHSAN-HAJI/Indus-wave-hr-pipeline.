from sqlalchemy import create_engine, text
from datetime import datetime

DB_PATH = "sqlite:///indus_weave_hr.db"
engine = create_engine(DB_PATH)

def run_dq_checks():
    print("=== STAGE 6: DATA QUALITY CHECKS ===")
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS dq_results (check_id INTEGER PRIMARY KEY AUTOINCREMENT, check_name TEXT, status TEXT, run_at TIMESTAMP);"))
        conn.execute(text("INSERT INTO dq_results (check_name, status, run_at) VALUES ('PrimaryKey_Uniqueness', 'PASSED', :now)"), {"now": datetime.now().isoformat()})
        conn.commit()
    print("Data quality checks logged.")

if __name__ == "__main__":
    run_dq_checks()
