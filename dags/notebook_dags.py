import os
import glob
import json
import logging
import papermill as pm
from datetime import datetime, timedelta

import airflow
from airflow import DAG
from airflow.configuration import conf
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import Variable

DAGS_DIR = conf.get('core', 'dags_folder')
NOTEBOOKS_DIR = os.path.abspath(conf.get('core', 'dags_folder') + "/../notebooks") + "/"
OUTPUT_DIR = os.path.abspath(conf.get('core', 'dags_folder') + "/../output") + "/"
CONFIG_DIR = os.path.abspath(conf.get('core', 'dags_folder') + "/../config") + "/"

with open( CONFIG_DIR + "/notebooks.json", 'r') as f:
    notebooks = json.load(f)

def create_dag(dag_id, args):

    # notebook name without extension
    basename = args.get('basename')

    # notebook file, this will be executed
    notebook_file = NOTEBOOKS_DIR + basename + ".ipynb"

    # directory to look for output files
    output_root = OUTPUT_DIR

    # the csv file location which wil be generated by the notebook, for example: /home/ec2-user/output/dromic-covid19-sitreps_2020-04-04.csv
    output_file_glob = OUTPUT_DIR + basename + '*'

    dag = DAG(
        dag_id=dag_id,
        default_args=args,
        max_active_runs=1,
        schedule_interval=notebooks[basename]['interval'],
        dagrun_timeout=timedelta(minutes=60)
    )

    with dag:
        start = DummyOperator(task_id='start')
        stop = DummyOperator(task_id='stop')

        def clean_generated_files():
            for output_file in glob.glob(output_file_glob):
                if os.path.exists(output_file):
                    os.remove(output_file)

        def execute_notebook(**kwargs):
            name = kwargs.get('name')
            keyword = kwargs.get('keyword')
            mime_type = kwargs.get('mime_type')
            execution_time_str = kwargs.get('ts')
            execution_time = datetime.strptime(execution_time_str, '%Y-%m-%dT%H:%M:%S%z')
            execution_date_str = execution_time.strftime('%Y-%m-%d')
            
            pm.execute_notebook(
                input_path=notebook_file,
                output_path='/dev/null',
                parameters=dict({
                    'output_dir': OUTPUT_DIR,
                    'execution_date': execution_date_str,
                    'execution_time': execution_time_str,
                }),
                log_output=True,
                report_mode=True
            )

        def create_dynamic_task(task_id, callable_function):
            task = PythonOperator(
                task_id=task_id,
                python_callable=callable_function,
                provide_context=True
            )
            return task

        cleanup = create_dynamic_task('cleanup', clean_generated_files)

        execute = create_dynamic_task('execute', execute_notebook)

        start >> cleanup >> execute >> stop

    return dag

#  Look for python notebooks to execute
for file in os.listdir(NOTEBOOKS_DIR):
    if file.startswith("."):
        continue
    filename_without_extension = os.path.splitext(file)[0]
    dag_id = filename_without_extension

    default_args = {'owner': 'altcoder',
                    'start_date': days_ago(2),
                    'basename': filename_without_extension
                    }
    globals()[dag_id] = create_dag(dag_id, default_args)
