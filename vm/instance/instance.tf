resource "google_service_account" "vm_sa" {
  account_id   = var.sa_name
  display_name = var.sa_display_name
}

resource "google_compute_instance" "vm" {
  name         = var.vm_name
  machine_type = var.machine_type
  zone         = var.zone

  tags   = local.vm_tags
  labels = local.vm_labels

  boot_disk {
    initialize_params {
      image = var.boot_image
      labels = {
        app = "nginx"
      }
    }
  }

  network_interface {
    network = var.vpc_network

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
