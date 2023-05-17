from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateBatchOperator, DataprocGetBatchOperator, DataprocSubmitJobOperator)
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.composer.data_lineage.entities import BigQueryTable


args = {
    'owner': 'packt-developer',
}

SPARK_JOB = {
    "reference": {"project_id": "cf-data-analytics"},
    "placement": {"cluster_name": "cluster-a7bd"},
    "spark_job": {
        "jar_file_uris": ["gs://cf-spark-jobs/template/scala-2.12/file-creator-assembly-1.0.jar"],
        "main_class": "BqDemo",
    },
}

with DAG(
    dag_id='spark-bq',
    default_args=args,
    schedule_interval='@once',  # set schedule - at every tenth minute
    start_date=days_ago(1),
    max_active_runs=1,
    is_paused_upon_creation=False
) as dag:

    spark_task = DataprocSubmitJobOperator(
        task_id="spark_task", job=SPARK_JOB, region="us-central1", project_id="cf-data-analytics",
        inlets=[BigQueryTable(
            project_id="cf-data-analytics",
            dataset_id='raw_zone',
            table_id='googl_data',
        )],
        outlets=[BigQueryTable(
            project_id="cf-data-analytics",
            dataset_id='composer_destination',
            table_id='googl_dataproc_summarized',
        )]
    )

    spark_task

if __name__ == "__main__":
    dag.cli()
