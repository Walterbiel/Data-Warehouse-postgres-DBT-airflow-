from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='dbt_transform_pipeline',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /usr/app && dbt run'
    )
