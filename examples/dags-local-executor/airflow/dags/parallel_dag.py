from airflow import DAG
from airflow.operators.bash import BashOperator
 
from datetime import datetime
 
with DAG('parallel_dag', start_date=datetime(2023, 9, 2), 
    schedule_interval='@daily', catchup=False) as dag:
 
    task_1 = BashOperator(
        task_id='task_1',
        bash_command='sleep 3'
    )
 
    task_2 = BashOperator(
        task_id='task_2',
        bash_command='sleep 3'
    )
 
    task_3 = BashOperator(
        task_id='task_3',
        bash_command='sleep 3'
    )
 
    task_4 = BashOperator(
        task_id='task_4',
        bash_command='sleep 3'
    )
 

task_1 >> [task_2, task_3] >> task_4