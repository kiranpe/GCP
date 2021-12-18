resource "google_compute_network" "vpc" {
  name                    = "${var.vpc}-vpc"
  auto_create_subnetworks = "false"
  routing_mode            = "GLOBAL"
}

resource "google_compute_firewall" "allow-internal" {
  name    = "${var.vpc}-fw-allow-internal"
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
    var.public_subnets[0]
  ]
}

resource "google_compute_firewall" "allow-http" {
  name    = "${var.vpc}-fw-allow-http"
  network = google_compute_network.vpc.name
  allow {
    protocol = "tcp"
    ports    = ["80", "10800", "10801"]
  }
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["http"]
}

resource "google_compute_firewall" "allow-bastion" {
  name    = "${var.vpc}-fw-allow-bastion"
  network = google_compute_network.vpc.name
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ssh"]
}
