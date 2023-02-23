resource "google_service_account" "vm_sa" {
  account_id   = var.sa_id
  display_name = var.sa_display_name
}

data "google_compute_image" "vm_image" {
  family  = var.image_version
  project = var.image_project
}

resource "google_compute_disk" "vm_disk" {
  name  = var.disk_name
  image = data.google_compute_image.vm_image.self_link
  size  = var.disk_size
  type  = var.disk_type
  zone  = var.zone
}

resource "google_compute_instance_template" "vm_tpl" {
  name        = var.vm_name
  description = var.vm_desc

  tags   = local.tags
  labels = local.vm_labels

  machine_type = var.vm_machine

  disk {
    source      = google_compute_disk.vm_disk.name
    auto_delete = false
    boot        = true
  }

  network_interface {
    network = var.vpc_name
    access_config {
      // Ephemeral public IP
    }
  }

  metadata_startup_script = file("./startup/script.sh")

  service_account {
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    email  = google_service_account.vm_sa.email
    scopes = ["cloud-platform"]
  }
}
