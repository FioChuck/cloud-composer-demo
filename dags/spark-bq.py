from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator


args = {
    'owner': 'packt-developer',
}

SPARK_JOB = {
    "reference": {"project_id": "cf-data-analytics"},
    "placement": {"cluster_name": "cluster-f866"},
    "spark_job": {
        "jar_file_uris": ["gs://cf-spark-jobs/spark-stock-transformations/scala-2.13/spark-window-functions-assembly-3.0.jar"],
        "main_class": "Main",
    },
}

with DAG(
    dag_id='spark-bq',
    default_args=args,
    schedule_interval=None,
    start_date=days_ago(1),
    max_active_runs=1,
    is_paused_upon_creation=False
) as dag:

    spark_task = DataprocSubmitJobOperator(
        task_id="spark_task", job=SPARK_JOB, region="us-central1", project_id="cf-data-analytics")

    spark_task

if __name__ == "__main__":
    dag.cli()
    # dag.test()
