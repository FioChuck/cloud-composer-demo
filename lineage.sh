gcloud auth login

curl -X DELETE \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application.json" https://us-datalineage.googleapis.com/v1/projects/1089470781238/locations/us/processes/b14ee5e8185e5a7c03970129cb96f25a/runs/cc345a25e1f219f3fe3403abdf7244a2


curl -X POST \
'https://us-datalineage.googleapis.com/v1/projects/1089470781238/locations/us:searchLinks' \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
-d '{ "source": { "fully_qualified_name": "bigquery:cf-data-analytics.composer_destination.googl_bq_ingestion" } }'