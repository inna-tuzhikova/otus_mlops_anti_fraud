import json

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
import requests


args = {
    "owner": "ubuntu",
}

dag = DAG(
    dag_id="iss_to_hdfs",
    default_args=args,
    schedule_interval="*/1 * * * *",
    start_date=days_ago(1),
    catchup=False,
    tags=["API"],
)


def iss_to_json():
    """Returns mks geoposition from open-notify API"""

    url_response = requests.get("http://api.open-notify.org/iss-now.json")
    dict_of_values = json.loads(url_response.text)

    longitude = dict_of_values["iss_position"]["longitude"]
    latitude = dict_of_values["iss_position"]["latitude"]
    timestamp = dict_of_values["timestamp"]
    output_path = f"/home/ubuntu/iss/{timestamp}.json"
    data = dict(longitude=longitude, latitude=latitude)
    with open(output_path, "w") as f:
        json.dump(data, f)
    return output_path


prepare_iss_json = PythonOperator(
    task_id="iss_to_json",
    python_callable=iss_to_json,
    dag=dag
)

json_to_hdfs = BashOperator(
    task_id="json_to_hdfs",
    bash_command="hdfs dfs -copyFromLocal "
                 "{{ ti.xcom_pull(task_ids='iss_to_json') }} "
                 "/user/root/iss",
    dag=dag,
    run_as_user="ubuntu"
)

rm_json = BashOperator(
    task_id="rm_json",
    bash_command="rm {{ ti.xcom_pull(task_ids='iss_to_json') }} ",
    dag=dag,
    run_as_user="ubuntu"
)

prepare_iss_json >> json_to_hdfs >> rm_json
