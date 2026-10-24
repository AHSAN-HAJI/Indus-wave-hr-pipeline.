from sqlalchemy import create_engine, text

DB_PATH = "sqlite:///indus_weave_hr.db"
engine = create_engine(DB_PATH)

def create_warehouse_schema():
    print("=== STAGE 4: BUILDING STAR SCHEMA ===")
    queries = [
        "CREATE TABLE IF NOT EXISTS dim_employee (emp_key INTEGER PRIMARY KEY AUTOINCREMENT, emp_id TEXT, first_name TEXT, last_name TEXT, department_id TEXT, plant_id TEXT, designation TEXT, is_current INTEGER);",
        "CREATE TABLE IF NOT EXISTS dim_department (department_id TEXT PRIMARY KEY, department_name TEXT, plant_id TEXT);",
        "CREATE TABLE IF NOT EXISTS fact_attendance_daily (fact_id INTEGER PRIMARY KEY AUTOINCREMENT, emp_id TEXT, work_date DATE, worked_hours REAL, late_minutes INTEGER, overtime_hours REAL, attendance_status TEXT);"
    ]
    with engine.connect() as conn:
        for q in queries:
            conn.execute(text(q))
        conn.commit()
    print("Star Schema created successfully.")

if __name__ == "__main__":
    create_warehouse_schema()
