gcloud auth login

curl -X DELETE \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application.json" https://us-central1-datalineage.googleapis.com/v1/projects/1089470781238/locations/us-central1/processes/2802cac6c0d4566958971e303371adae

curl -X POST \
'https://us-datalineage.googleapis.com/v1/projects/1089470781238/locations/us:searchLinks' \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
-d '{ "source": { "fully_qualified_name": "bigquery:cf-data-analytics.composer_destination.googl_bq_ingestion" } }'

gcloud storage ls --recursive gs://datastream-change-stream/example_persons/**.jsonl

gs://datastream-change-stream/example_persons/**.jsonl


gcloud dataproc clusters create cluster-f866 \
--region us-central1 \
--project cf-data-analytics \
--properties 'dataproc:dataproc.lineage.enabled=true' \
--image-version 2.0-debian10
