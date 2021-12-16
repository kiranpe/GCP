resource "google_compute_instance" "vms" {
  count        = 2
  name         = "vm-${count.index}"
  machine_type = "n1-standard-1"
  zone         = "us-west4-b"
  tags         = ["ssh", "http"]
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }
  labels = {
    webserver = "true"
  }
  network_interface {
    subnetwork = google_compute_subnetwork.public_subnet.name
    access_config {
      // Ephemeral IP
    }
  }
}

resource "null_resource" "check_status" {
  provisioner "local-exec" {
    command = "sleep 60 && ./gcp_services_status.py"
  }

  depends_on = [google_compute_instance.vms]
}
