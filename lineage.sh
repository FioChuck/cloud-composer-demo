gcloud auth login

curl -X DELETE \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application.json" https://us-datalineage.googleapis.com/v1/projects/1089470781238/locations/us/processes/ecdd3ea103f9d3ce56e193a0784c2e82


curl -X POST \
'https://us-datalineage.googleapis.com/v1/projects/1089470781238/locations/us:searchLinks' \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
-d '{ "source": { "fully_qualified_name": "bigquery:cf-data-analytics.composer_destination.googl_bq_ingestion" } }'

gcloud storage ls --recursive gs://datastream-change-stream/example_persons/**.jsonl

gs://datastream-change-stream/example_persons/**.jsonl


gcloud dataproc clusters create cluster-f866 \
--region us-central1 \
--zone us-central1-a \
--image-version 2.1-debian11 \
--project cf-data-analytics \
--properties 'dataproc:dataproc.lineage.enabled=true' \
--scopes https://www.googleapis.com/auth/cloud-platform