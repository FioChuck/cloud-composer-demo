from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.contrib.operators.bigquery_to_gcs import BigQueryToCloudStorageOperator


args = {
    'owner': 'packt-developer',
}

query = f"""
CREATE OR REPLACE TABLE
  `cf-data-analytics.composer_destination.googl_summary` AS
SELECT
  symbol,
  MAX(trade_price) AS max_price,
  MIN(trade_price) AS min_price
FROM
  cf-data-analytics.composer_destination.googl_stock_data
GROUP BY
  symbol;
"""

with DAG(
    dag_id='googl_stock_data_etl',
    default_args=args,
    schedule_interval='*/10 * * * *',  # set schedule - at every tenth minute
    start_date=days_ago(1),
    is_paused_upon_creation=True

) as dag:

    gcs_parquet_ingestion = GoogleCloudStorageToBigQueryOperator(
        task_id="gcs_parquet_ingestion",
        bucket='cf-spark-external',
        source_format='parquet',
        source_objects=[
            'googl-market-data/*.parquet'],
        destination_project_dataset_table='composer_destination.googl_stock_data',
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

    aggregation_query = BigQueryInsertJobOperator(
        task_id="aggregation_query",
        configuration={
            "query": {
                "query": query,
                "useLegacySql": False
            }
        }
    )

# gs://cf-bq-external/atl_avg_temp.csv

    bq2gcp_override = BigQueryToCloudStorageOperator(
        task_id='bq2gcp_override',
        source_project_dataset_table='cf-data-analytics.weather_share.atlanta_weather',
        destination_cloud_storage_uris=[
            'gs://cf-bq-external/part-*.avro'
        ],
        export_format='AVRO',
        bigquery_conn_id='gcp_smoke',
    )

    bq2gcp_override >> gcs_parquet_ingestion >> aggregation_query

if __name__ == "__main__":
    dag.cli()
