resource "google_pubsub_topic" "bigq_topic" {
  name = var.topic_name

  labels = local.bigq_labels
}

resource "google_pubsub_subscription" "sub" {
  name  = "bigq-sub-dev"
  topic = google_pubsub_topic.bigq_topic.name

  bigquery_config {
    table = "${google_bigquery_table.dataset_table.project}:${google_bigquery_table.dataset_table.dataset_id}.${google_bigquery_table.dataset_table.table_id}"
  }

  depends_on = [google_project_iam_member.bq_data_editor, google_project_iam_member.bq_jobs_role, google_project_iam_member.bq_pubsub_role]
}
