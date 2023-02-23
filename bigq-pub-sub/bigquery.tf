resource "google_bigquery_dataset" "dataset" {
  dataset_id    = var.bigq_dataset_id
  friendly_name = var.bigq_name
  description   = var.bigq_desc
  location      = "US"

  delete_contents_on_destroy = true

  labels = local.bigq_labels
}

resource "google_bigquery_table" "dataset_table" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = var.bigq_table_id

  labels              = local.bigq_labels
  deletion_protection = false

  schema = <<EOF
    [
     {
      "name": "id",
      "type": "INTEGER",
      "mode": "NULLABLE"
     },
     {
      "name": "data",
      "type": "STRING",
      "mode": "NULLABLE" 
     },
     {
      "name": "status",
      "type": "STRING",
      "mode": "NULLABLE"
     }
    ]
    EOF
}
