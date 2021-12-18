resource "google_compute_instance" "vms" {
  count        = length(var.env)
  name         = "${var.vm[count.index]}-${var.env[count.index]}-${var.client[count.index]}"
  machine_type = "n1-standard-1"
  zone         = var.zone
  tags         = ["ssh", "http"]
  boot_disk {
    initialize_params {
      image = "ubuntu-2004-focal-v20211212"
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

  metadata_startup_script = file("${path.module}/startup.sh")
}

output "external_ips" {
  value = google_compute_instance.vms[*].network_interface.0.access_config.0.nat_ip
}

resource "null_resource" "check_status" {
  provisioner "local-exec" {
    command = "sleep 120 && ./gcp_services_status.py ${google_storage_bucket.my_bucket.name} ${google_compute_instance.vms[0].name} ${google_compute_instance.vms[1].name} ${google_compute_instance.vms[0].network_interface.0.access_config.0.nat_ip} ${google_compute_instance.vms[1].network_interface.0.access_config.0.nat_ip}"
  }

  depends_on = [google_compute_instance.vms]
}
