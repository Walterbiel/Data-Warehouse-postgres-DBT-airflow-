from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(seconds=15),
}

with DAG(
    dag_id='chamar_api_vendas',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval='* * * * *',  # Executa a cada minuto
    catchup=False,
    tags=['fastapi', 'vendas'],
) as dag:

    chamar_api = BashOperator(
        task_id='chamar_api',
        bash_command="curl -X POST 'http://127.0.0.1:8002/gerar-vendas' -H 'accept: application/json'"
    )

    chamar_api
