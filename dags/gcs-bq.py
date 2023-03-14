from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
args = {
    'owner': 'packt-developer',
}

with DAG(
    dag_id='hello_world_airflow',
    default_args=args,
    schedule_interval='*/10 * * * *',
    start_date=days_ago(1),
) as dag:

    gcs_to_bq_example = GoogleCloudStorageToBigQueryOperator(
        task_id="gcs_to_bq_example",
        bucket='cf-spark-external',
        source_format='parquet',
        source_objects=[
            'googl-market-data/*.parquet'],
        destination_project_dataset_table='composer_destination.market_data2',
        schema_fields=[
            {
                "mode": "NULLABLE",
                "name": "symbol",
                "type": "STRING"
            },
            {
                "mode": "NULLABLE",
                "name": "datetime",
                "type": "STRING"
            },
            {
                "mode": "NULLABLE",
                "name": "tm",
                "type": "INTEGER"
            },
            {
                "mode": "NULLABLE",
                "name": "dt",
                "type": "DATE"
            },
            {
                "mode": "NULLABLE",
                "name": "exchange_code",
                "type": "STRING"
            },
            {
                "mode": "NULLABLE",
                "name": "trade_price",
                "type": "FLOAT"
            },
            {
                "mode": "NULLABLE",
                "name": "trade_size",
                "type": "INTEGER"
            },
            {
                "fields": [
                    {
                        "fields": [
                            {
                                "mode": "NULLABLE",
                                "name": "element",
                                "type": "STRING"
                            }
                        ],
                        "mode": "REPEATED",
                        "name": "list",
                        "type": "RECORD"
                    }
                ],
                "mode": "NULLABLE",
                "name": "trade_condition",
                "type": "RECORD"
            },
            {
                "mode": "NULLABLE",
                "name": "trade_id",
                "type": "INTEGER"
            },
            {
                "mode": "NULLABLE",
                "name": "tape",
                "type": "STRING"
            }
        ],
        write_disposition='WRITE_TRUNCATE'
    )

    bq_to_bq = BigQueryOperator(
        task_id="bq_to_bq",
        sql="SELECT count(*) as count FROM `cf-data-analytics.staging.test`",
        destination_dataset_table='cf-data-analytics.staging.test2',
        write_disposition='WRITE_TRUNCATE',
        create_disposition='CREATE_IF_NEEDED',
        use_legacy_sql=False,
        priority='BATCH'
    )

    task3 = BigQueryInsertJobOperator(
        task_id='snapshot_task',
        dag=dag,
        location='US',
        write_disposition='WRITE_TRUNCATE',
        configuration={
            'query': {
                'query': 'SELECT * FROM cf-data-analytics.staging.test2',
                'useLegacySql': False,
                'destinationTable': {
                    'project_id': 'cf-data-analytics',
                    'dataset_id': 'test',
                    'table_id': 'test',
                },
            }
        },
    )

    gcs_to_bq_example >> bq_to_bq >> task3

if __name__ == "__main__":
    dag.cli()
