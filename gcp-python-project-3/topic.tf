resource "google_pubsub_topic" "topic" {
  name    = "${var.env}-topic"
  project = var.projectId

  labels = {
    env = "dev"
  }
}

resource "google_pubsub_subscription" "sub" {
  name  = "${var.env}-sub"
  topic = google_pubsub_topic.topic.name

  labels = {
    env = "dev"
  }

  # 10 minutes
  message_retention_duration = "600s"
  retain_acked_messages      = true

  ack_deadline_seconds = 120

  expiration_policy {
    ttl = "300000.5s"
  }
  retry_policy {
    minimum_backoff = "10s"
  }

  enable_message_ordering = false
}
