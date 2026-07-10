"""Module 02: orchestrates module 01's ingestion + module 03's warehouse load.

Copy or symlink this file into your Airflow dags/ folder (docker-compose.yml
in the repo root does this automatically via a volume mount).
"""
import sys
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator

# Make modules/01-ingestion and modules/03-warehouse importable.
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "modules" / "01-ingestion"))
sys.path.insert(0, str(REPO_ROOT / "modules" / "03-warehouse"))

from ingest import fetch_weather, write_landing_file  # noqa: E402
from load import load_landing_file_to_warehouse  # noqa: E402

default_args = {
    "owner": "course",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


def _ingest_weather(ds: str, **_context):
    payload = fetch_weather(ds)
    write_landing_file(ds, payload)


def _load_to_warehouse(ds: str, **_context):
    load_landing_file_to_warehouse(ds)


with DAG(
    dag_id="course_dag",
    default_args=default_args,
    description="Module 02: ingest weather data then load it into the warehouse",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["course", "module-02"],
) as dag:
    ingest_weather = PythonOperator(
        task_id="ingest_weather",
        python_callable=_ingest_weather,
    )

    load_to_warehouse = PythonOperator(
        task_id="load_to_warehouse",
        python_callable=_load_to_warehouse,
    )

    ingest_weather >> load_to_warehouse
