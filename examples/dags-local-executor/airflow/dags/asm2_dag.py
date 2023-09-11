import os
import os.path
from os.path import exists

from google_drive_downloader import GoogleDriveDownloader as gddl

#datetime
from datetime import timedelta, datetime
from airflow.utils.dates import days_ago

# The DAG object
from airflow import DAG

# Operators
from airflow.operators.bash import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# Hook
from airflow.providers.mongo.hooks.mongo import MongoHook
from pymongo.mongo_client import MongoClient

from google_drive_downloader import GoogleDriveDownloader as gdd

# -------------------------------------
# DAGs
# -------------------------------------
# initializing the default arguments

default_args = {
        'owner': 'airflow',    
        'start_date': days_ago(1),
        #'start_date': datetime(2023, 9, 2),
        # 'end_date': datetime(),
        # 'depends_on_past': False,
        #'email': ['airflow@example.com'],
        #'email_on_failure': False,
        #'email_on_retry': False,
        # If a task fails, retry it once after waiting
        # at least 5 minutes
        #'retries': 1,
        'retry_delay': timedelta(minutes=5),
        
        }
# Instantiate a DAG object
my_dag = DAG('dep303_ams2_dag',
		default_args=default_args,
		description='Hello World DAG',
		#schedule_interval='0 0 * * *', 
        schedule_interval='@once',
		catchup=False,
        dagrun_timeout=timedelta(minutes=60),
		tags=['example, helloworld']
)

# -------------------------------------
# Python callable function
# -------------------------------------
# 

def check_all_files_exist():
    """
    Check if all files in a list exist and print the result.

    Args:
    file_paths (list): A list of file paths to check.

    Returns:
    bool: True if all files exist, False if at least one file does not exist.
    """

    # solution 1
    file_paths = ['/opt/airflow-data/input/Questions.csv', '/opt/airflow-data/input/Answers.csv']
    status = [exists(file) for file in file_paths]
    # check the status of all files
    # if any of the files doesn't exist, else will be called
    if(all(status)):
        print('All files are present.')
        return 'end'
    else:
        print('Any or all files do not exist.')
        return 'clear_file'

    # solution 2
    #file_paths = ['/opt/airflow-data/input/Questions.csv', '/opt/airflow-data/input/Answers.csv']
    #all_exist = all(os.path.isfile(file_path) for file_path in file_paths)
    #print ("------------all_exist----------")
    #print (all_exist)
    #if all_exist:
    #    print("All files exist.")
    #    return 'end'
    #else:
    #    print("Not all files exist.")
    #    return 'clear_file'
    
def download_file_from_google_drive(output_file_path,file_id_download):
    try:
        # Download the file from Google Drive
        #gdd.download_file_from_google_drive(file_id=file_id_download,
        #                            dest_path=output_file_path,
        #                            unzip=False)
        
        gddl.download_file_from_google_drive(file_id=file_id_download, dest_path=output_file_path, overwrite=True, unzip=True, showsize=False)

        print(f"Downloaded file from Google Drive to {output_file_path}")
    except Exception as e:
        print(f"Error downloading file from Google Drive: {str(e)}")
        

# -------------------------------------
# TASK
# -------------------------------------

# Creating start task
task_start = DummyOperator(task_id='start', dag=my_dag)

# Creating branching task
task_branching = BranchPythonOperator(
    task_id='branching',
    python_callable= check_all_files_exist,
	dag=my_dag
    )

# Creating branching task
task_clear_file = BashOperator(
    task_id='clear_file',
    bash_command='rm -f /opt/airflow-data/input/*',
    dag=my_dag,
)

# Creating download_question_file task
task_download_question_file = PythonOperator(
    task_id='download_question_file',
    python_callable=download_file_from_google_drive,
    op_args=['/opt/airflow-data/input/Questions.csv', '10KqCh7ZzGQ2Z69qSwXrMWNagnC54bFb2'], # 1-fgPn4tFcm8zqfSiCEFvI16ZWlujtmpd
    dag=my_dag,
)

# Creating download_answer_file task
task_download_answer_file = PythonOperator(
    task_id='download_answer_file',
    python_callable=download_file_from_google_drive,
    op_args=['/opt/airflow-data/input/Answers.csv', '10KqCh7ZzGQ2Z69qSwXrMWNagnC54bFb2'], #
    dag=my_dag,
)

# Creating import_questions_mongo task
task_import_questions_mongo = BashOperator(
    task_id='import_questions_mongo',
    #bash_command='mongoimport --type csv -d <database> -c <collection> --headerline --drop <file>', 
	#bash_command='mongoimport --host mongodb://localhost:27011 --db DEP303_ASM2 --collection Questions --type csv --file /opt/airflow-data/inputQuestions.csv --headerline',
    bash_command='mongoimport --host mongodb --db DEP303_ASM2 --collection Questions --type csv --file /opt/airflow-data/input/Questions.csv --headerline',  
    trigger_rule='all_success',
    dag=my_dag,
)

# Creating import_answers_mongo task
task_import_answers_mongo = BashOperator(
    task_id='import_answers_mongo',
    #bash_command='mongoimport --type csv -d <database> -c <collection> --headerline --drop <file>',
	#bash_command='mongoimport --host mongodb://mongodb-container:27011 --db DEP303_ASM2 --collection Questions --type csv --file /opt/airflow-data/inputQuestions.csv --headerline',
    bash_command='mongoimport --host mongodb --db DEP303_ASM2 --collection Answers --type csv --file /opt/airflow-data/input/Answers.csv --headerline',
    trigger_rule='all_success',
    dag=my_dag,
)

# Creating spark_process task using SparkSubmitOperator
""" task_spark_process = SparkSubmitOperator(
	task_id='spark_process',
    conn_id="spark_conn",
    application="/opt/airflow/app/mongodb_to_csv.py",  
    verbose=1,
    conf={"spark.jars.packages":'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1'},
    trigger_rule='all_success',
    dag=my_dag,
) """

# Creating spark_process task using BashOperator
task_spark_process = BashOperator(
    task_id='spark_process',
    bash_command='spark-submit --master spark://spark-master:7077 \
                    --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
                    --driver-memory 1G \
                    --executor-memory 1G \
                    /opt/airflow/app/mongodb_to_csv.py', 
    trigger_rule='all_success',
    dag=my_dag,
)

# Creating import_output_mongo task
task_import_output_mongo = BashOperator(
    task_id='import_output_mongo',
    #bash_command='mongoimport --type csv -d <database> -c <collection> --headerline --drop <file>',
	#bash_command='mongoimport --host mongodb-container:27017 --db DEP303_ASM2 --collection Questions --type csv --file /opt/airflow-data/inputAnswers.csv --headerline',
    bash_command=""" echo "get file csv name"
                    file_name=$(ls /opt/airflow-data/output/ | grep .csv)
                    echo "import data from csv file to mongodb"
                    mongoimport --host mongodb --db DEP303_ASM2 --collection Results --type csv --file "/opt/airflow-data/output/${file_name}" --headerline """,
    trigger_rule='all_success',
    dag=my_dag,
)

# Creating end task
task_end = DummyOperator(task_id='end', trigger_rule='none_failed', dag=my_dag)

# Set the order of execution of tasks. 
task_start >> task_branching >> [task_clear_file, task_end]
task_clear_file >> [task_download_answer_file,task_download_question_file ]
task_download_answer_file >> task_import_answers_mongo
task_download_question_file >> task_import_questions_mongo
[task_import_questions_mongo, task_import_answers_mongo] >> task_spark_process >> task_import_output_mongo >> task_end

#[task_import_questions_mongo, task_import_answers_mongo] >> task_spark_process  >> task_end
#[task_import_questions_mongo, task_import_answers_mongo]  >> task_end