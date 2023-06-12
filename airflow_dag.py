from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import os

# Import the data stream function from your Python script
from crypto_data_stream import data_stream

# Define the DAG
dag = DAG(
    dag_id='crypto_data_stream',
    default_args={
        'owner': 'airflow',
        'retries': 10000,  # Set a high retry limit
        'retry_delay': timedelta(seconds=10),  # Set a short retry delay
    },
    start_date=datetime(2023, 4, 15),
    catchup=False,
    schedule_interval=timedelta(days=1),  # Set a long schedule interval to avoid starting multiple instances
)


# Define the PythonOperator task
data_stream_task = PythonOperator(
    task_id='data_stream',
    python_callable=data_stream,
    dag=dag,
)

# Set the task dependencies
data_stream_task