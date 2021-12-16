resource "google_compute_network" "vpc" {
  name                    = "${var.env}-vpc"
  auto_create_subnetworks = "false"
  routing_mode            = "GLOBAL"
}

resource "google_compute_firewall" "allow-internal" {
  name    = "${var.env}-fw-allow-internal"
  network = google_compute_network.vpc.name
  allow {
    protocol = "icmp"
  }
  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }
  allow {
    protocol = "udp"
    ports    = ["0-65535"]
  }
  source_ranges = [
    var.uc1_public_subnet,
    var.uc1_private_subnet
  ]
}

resource "google_compute_firewall" "allow-http" {
  name    = "${var.env}-fw-allow-http"
  network = google_compute_network.vpc.name
  allow {
    protocol = "tcp"
    ports    = ["80"]
  }
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["http"]
}

resource "google_compute_firewall" "allow-bastion" {
  name    = "${var.env}-fw-allow-bastion"
  network = google_compute_network.vpc.name
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ssh"]
}
