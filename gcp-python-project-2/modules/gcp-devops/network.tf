resource "google_compute_subnetwork" "public_subnet" {
  name          = "${var.vpc}-pub-net"
  ip_cidr_range = var.public_subnets[0]
  network       = google_compute_network.vpc.id
  region        = var.region
}
resource "google_compute_subnetwork" "private_subnet" {
  name          = "${var.vpc}-pri-net"
  ip_cidr_range = var.public_subnets[1]
  network       = google_compute_network.vpc.id
  region        = var.region
}
