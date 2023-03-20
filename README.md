# TL;DR

A simple Cloud Composer Airflow DAG _(Directed Acyclic Graph)_ that moves Parquet files from Google Cloud Storage into BigQuery. This repo can be used as a deployment template for Cloud Composer via GitHub actions. It also acts as a Dataplex Data Lineage demo.

# Overview

```mermaid
flowchart LR
A("Cloud Storage") -->|GoogleCloudStorageToBigQueryOperator| B("BigQuery") -->|BigQueryInsertJobOperator| C("BigQuery")
```

```shell
gcloud beta composer environments update etl-orchestration-pool \
    --location us-central1 \
    --enable-cloud-data-lineage-integration
```

## Deployment

```shell
gcloud composer environments storage dags import \
          --environment etl-orchestration-pool \
          --location us-central1 \
          --source gs://cf-cloud-composer-dags/dags/gcs-bq.py"
```
