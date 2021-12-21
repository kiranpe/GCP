resource "google_service_account" "sa" {
  account_id   = "pythonlogin"
  display_name = "readaccess"
}

resource "google_service_account_iam_member" "admin-account-iam" {
  service_account_id = google_service_account.sa.name
  role               = "roles/iam.serviceAccountUser"
  member             = "user:kiranpeddineni@gmail.com"
}

resource "google_service_account_key" "mykey" {
  service_account_id = google_service_account.sa.name
}

resource "google_storage_bucket" "my_bucket" {
  name     = var.bucket_name
  location = var.region
}

resource "google_storage_bucket_acl" "read-acl" {
  bucket = google_storage_bucket.my_bucket.name

  role_entity = [
    "READER:user-${google_service_account.sa.account_id}@${var.projectId}.iam.gserviceaccount.com",
  ]
}

resource "local_file" "sa_file" {
  depends_on      = [google_service_account.sa]
  filename        = "credentials.json"
  file_permission = "0600"
  content         = base64decode(google_service_account_key.mykey.private_key)
}
