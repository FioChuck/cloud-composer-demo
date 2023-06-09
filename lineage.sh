gcloud auth login

curl -X DELETE \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application.json" https://us-central1-datalineage.googleapis.com/v1/projects/1089470781238/locations/us-central1/processes/cc5f4a8459cae316f02eb343b60da1cb


curl -X POST \
'https://us-datalineage.googleapis.com/v1/projects/1089470781238/locations/us:searchLinks' \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
-d '{ "source": { "fully_qualified_name": "bigquery:cf-data-analytics.composer_destination.googl_bq_ingestion" } }'

gcloud storage ls --recursive gs://datastream-change-stream/example_persons/**.jsonl

gs://datastream-change-stream/example_persons/**.jsonl