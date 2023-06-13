from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from crypto_data_stream import data_stream

start_date = datetime(2023, 1, 1, 12, 10)

default_args = {
    'owner': 'airflow',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

with DAG('crypto_data_stream', default_args=default_args, schedule_interval='*/5 * * * *', catchup=False) as dag:


    data_stream_task = PythonOperator(
    task_id='data_stream',
    python_callable=data_stream,
    dag=dag,
    )

    data_stream_task