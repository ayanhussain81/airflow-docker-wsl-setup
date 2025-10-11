from airflow import DAG
#from airflow.operators.python import PythonOperator
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta


def extract():
    print("Extracting data...")
    return "raw_data"


def transform(ti):
    raw_data = ti.xcom_pull(task_ids='extract_task')
    transformed_data = raw_data.upper()
    print(f"Transforming data: {transformed_data}")
    return transformed_data


def load(ti):
    transformed_data = ti.xcom_pull(task_ids='transform_task')
    print(f"Loading data: {transformed_data}")


# Define the DAG for Airflow
with DAG(
    dag_id='simple_etl_dag',
    description='A simple ETL DAG',
    start_date=datetime(2025, 1, 1),
    schedule='@daily',              
    catchup=False,                 
    default_args={
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    tags=['example', 'etl'],
) as dag:

    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract
    )

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform
    )

    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load
    )

    extract_task >> transform_task >> load_task