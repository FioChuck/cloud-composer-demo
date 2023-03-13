from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator

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
        destination_project_dataset_table='staging.test',
        schema_fields=[
            {
                "mode": "NULLABLE",
                "name": "id",
                "type": "INTEGER"
            },
            {
                "mode": "NULLABLE",
                "name": "lon",
                "type": "FLOAT"
            },
            {
                "mode": "NULLABLE",
                "name": "lat",
                "type": "FLOAT"
            },
            {
                "mode": "NULLABLE",
                "name": "desc_short",
                "type": "STRING"
            },
            {
                "mode": "NULLABLE",
                "name": "desc_long",
                "type": "STRING"
            },
            {
                "mode": "NULLABLE",
                "name": "temp",
                "type": "FLOAT"
            },
            {
                "mode": "NULLABLE",
                "name": "feels_like",
                "type": "FLOAT"
            },
            {
                "mode": "NULLABLE",
                "name": "temp_min",
                "type": "FLOAT"
            },
            {
                "mode": "NULLABLE",
                "name": "temp_max",
                "type": "FLOAT"
            },
            {
                "mode": "NULLABLE",
                "name": "pressure",
                "type": "FLOAT"
            },
            {
                "mode": "NULLABLE",
                "name": "humidity",
                "type": "FLOAT"
            },
            {
                "mode": "NULLABLE",
                "name": "visibility",
                "type": "FLOAT"
            },
            {
                "mode": "NULLABLE",
                "name": "wind_speed",
                "type": "FLOAT"
            },
            {
                "mode": "NULLABLE",
                "name": "wind_deg",
                "type": "FLOAT"
            },
            {
                "mode": "NULLABLE",
                "name": "clouds",
                "type": "FLOAT"
            },
            {
                "mode": "NULLABLE",
                "name": "dt",
                "type": "INTEGER"
            },
            {
                "mode": "NULLABLE",
                "name": "sunrise",
                "type": "INTEGER"
            },
            {
                "mode": "NULLABLE",
                "name": "sunset",
                "type": "INTEGER"
            },
            {
                "mode": "NULLABLE",
                "name": "timezone",
                "type": "INTEGER"
            },
            {
                "mode": "NULLABLE",
                "name": "city",
                "type": "STRING"
            },
            {
                "mode": "NULLABLE",
                "name": "processing_time",
                "type": "TIMESTAMP"
            },
            {
                "fields": [
                    {
                        "mode": "NULLABLE",
                        "name": "uuid",
                        "type": "STRING"
                    },
                    {
                        "mode": "NULLABLE",
                        "name": "source_timestamp",
                        "type": "INTEGER"
                    }
                ],
                "mode": "NULLABLE",
                "name": "datastream_metadata",
                "type": "RECORD"
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

    gcs_to_bq_example >> bq_to_bq

if __name__ == "__main__":
    dag.cli()
