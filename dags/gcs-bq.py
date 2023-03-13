from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator

args = {
    'owner': 'packt-developer',
}

with DAG(
    dag_id='hello_world_airflow',
    default_args=args,
    schedule_interval='*/5 * * * *',
    start_date=days_ago(1),
) as dag:

    print_hello = BashOperator(
        task_id='print_hello',
        bash_command='echo Hello',
    )

    print_world = BashOperator(
        task_id='print_world',
        bash_command='echo World',
    )

    print_world2 = BashOperator(
        task_id='print_world2',
        bash_command='echo World2',
    )

    gcs_to_bq_example = GoogleCloudStorageToBigQueryOperator(
        task_id="gcs_to_bq_example",
        bucket='cf-spark-jobs',
        source_format='parquet',
        source_objects=[
            'data/weather/*.parquet'],
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

    gcs_to_bq_example >> print_hello >> print_world >> print_world2

if __name__ == "__main__":
    dag.cli()
