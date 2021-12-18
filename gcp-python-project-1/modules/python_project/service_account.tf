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

resource "local_file" "sa_file" {
  depends_on      = [google_service_account.sa]
  filename        = "credentials.json"
  file_permission = "0600"
  content         = base64decode(google_service_account_key.mykey.private_key)
}

resource "google_storage_bucket" "my_bucket" {
  name     = var.bucket_name
  location = var.region
}

resource "null_resource" "attach_sa" {
  provisioner "local-exec" {
    command = "gsutil acl ch -u pythonlogin@pythonproject-335216.iam.gserviceaccount.com:R gs://kiran-python-project-1"
  }

  depends_on = [google_service_account.sa, google_storage_bucket.my_bucket]
}