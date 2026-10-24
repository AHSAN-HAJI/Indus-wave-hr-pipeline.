import sys, os, subprocess

def run_stage(script_path, stage_name):
    print(f"\n--- {stage_name} ---")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"[ERROR] {result.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    print("Starting HR Pipeline...")
    run_stage(os.path.join("ingestion", "load_raw.py"), "Stage 1: Raw Ingestion")
    run_stage(os.path.join("transform", "clean_transform.py"), "Stage 2 & 3: Clean & Business Logic")
    run_stage(os.path.join("warehouse", "ddl", "create_warehouse.py"), "Stage 4: Star Schema")
    run_stage(os.path.join("analytics", "run_queries.py"), "Stage 5: Analytics Queries")
    run_stage(os.path.join("quality", "dq_checks.py"), "Stage 6: DQ Checks")
    print("\nPipeline execution complete!")
