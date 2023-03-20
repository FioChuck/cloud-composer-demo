# cloud-composer-demo

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
