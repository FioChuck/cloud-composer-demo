from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateBatchOperator, DataprocListBatchesOperator
import uuid


args = {
    'owner': 'packt-developer',
}


SPARK_JOB = {
    "reference": {"project_id": "cf-data-analytics"},
    "placement": {"cluster_name": "cluster-e5a6"},
    "spark_job": {
        "main_jar_file_uri": "gs://cf-spark-jobs/spark-stock-transformations/scala-2.12/spark-window-functions-assembly-3.0.jar",
        "jar_file_uris": ["gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.41.0.jar"]
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

    # name = str(uuid.uuid4())

    # list_batches = DataprocListBatchesOperator(
    #     task_id="list-all-batches",
    #     project_id="cf-data-analytics",
    #     region="us-central1"
    # )

    # create_batch = DataprocCreateBatchOperator(
    #     task_id="batch_create",
    #     project_id="cf-data-analytics",
    #     region="us-central1",
    #     batch={
    #         "spark_batch": {
    #             "main_jar_file_uri": "gs://cf-spark-jobs/spark-stock-transformations/scala-2.12/spark-window-functions-assembly-3.0.jar"
    #         },
    #         "runtime_config": {
    #             "version": "1.1",
    #             "properties": {"spark.dataproc.lineage.enabled": "true"}
    #         }
    #     },
    #     batch_id=name,
    # )

    #

    spark_task = DataprocSubmitJobOperator(
        task_id="spark_task", job=SPARK_JOB, region="us-central1", project_id="cf-data-analytics")

    spark_task

    # list_batches >> create_batch

if __name__ == "__main__":
    dag.cli()
    # dag.test()
