from airflow import DAG
#from airflow.operators import PythonOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'truongcx',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 2),
    'email': ['*****@*****.**'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}
dag = DAG(
    'Weekday',
    default_args=default_args,
    schedule_interval="@once")

# used to fatorize the code and avoid repetition
tabDays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

# returns the week day (monday, tuesday, etc.)
# Indexing from 0: Monday to 6: Sunday
def get_weekday(ti):
    ti.xcom_push(key='day', value=datetime.now().weekday())
    print("-------CHECK WEEKDAY NOW--------")
    print(tabDays[datetime.now().weekday()])

# returns the name id of the task to launch (task_for_monday, task_for_tuesday, etc.)
def weekday_branch(ti):
    execution_date_weekday = ti.xcom_pull(task_ids='weekday', key='day')
    
    if execution_date_weekday in [0,1]:
        print (".....USER PROCESSING......")
        return 'up_task_for_' + tabDays[execution_date_weekday]
    else:
        # Create a DummyTask name from Monday to Saturday by adding the day of the week and the task name you want to run.
        print (".....TRANSACTION PROCESSING.....")
        return 'tp_task_for_' + tabDays[execution_date_weekday]
 
# PythonOperator will retrieve and store into "weekday" variable the week day
# Call get_weekday to store day of the week information in XCom.
get_weekday_operation = PythonOperator(
    task_id='weekday',
    python_callable=get_weekday,
    provide_context=True,
    dag=dag
)

# BranchPythonOperator will use "weekday" variable, and decide which task to launch next
fork = BranchPythonOperator(
    task_id='branching',
    python_callable=weekday_branch,
    provide_context=True,
    dag=dag)

#=============================================
# task get the week day
get_weekday_operation.set_downstream(fork)

# Connect DummyTask, a task that must be executed after branching.
# One dummy operator for each week day, all branched to the fork
for day in range(0, 6):
    if day in [0,1]:
        fork.set_downstream(DummyOperator(task_id='up_task_for_' + tabDays[day], dag=dag))
    else:
        fork.set_downstream(DummyOperator(task_id='tp_task_for_' + tabDays[day], dag=dag))

