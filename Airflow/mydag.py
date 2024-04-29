from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'Daniel',
    'start_date': datetime.today,
    'email': 'Daniel@gmail.com',
    'email_on_failure': True,
    'eamil_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id='ETL_toll_data',
    schedule_interval='@daily',
    default_args=default_args,
    description='Apache Airflow Final Assignment'
)


task1 = BashOperator(
    task_id='unzip_data',
    bash_command="sudo wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/tolldata.tgz \
        -o /home/project/airflow/dags/finalassignment/tolldata.tgz; \
        tar -xvzf /home/project/airflow/dags/finalassignment/tolldata.tgz",
    dag=dag,
)

task2 = BashOperator(
    task_id='extract_data_from_csv',
    bash_command="touch csv_data.csv; \
        echo \'Rowid,Timestamp,AnonymizedVehicleNumber,VehicleType\' > csv_data.csv \
            && cut -d',' -f1-4 vehicle-data.csv | head -n3 >> csv_data.csv",
    dag=dag
)
