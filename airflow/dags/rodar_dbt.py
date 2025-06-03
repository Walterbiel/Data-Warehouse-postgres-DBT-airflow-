# dags/dbt_every_10min.py
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

DEFAULT_ARGS = {
    "owner": "walter",
    "depends_on_past": False,
    "retries": 1,
}

DBT_PROJECT_DIR="/opt/airflow/dbt"
DBT_PROFILES_DIR="/opt/airflow/.dbt"

with DAG(
    dag_id="dbt_run_every_10min",
    description="Executa dbt run + test a cada 10 minutos",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2024, 1, 1),
    schedule_interval="*/10 * * * *",
    catchup=False,
    tags=["dbt"],
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"""
        cd {DBT_PROJECT_DIR} && \
        dbt run --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"""
        cd {DBT_PROJECT_DIR} && \
        dbt test --profiles-dir {DBT_PROFILES_DIR} --fail-fast
        """,
    )

    dbt_run >> dbt_test
