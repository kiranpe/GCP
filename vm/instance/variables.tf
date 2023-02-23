variable "project_id" {
  default = "k8s-devops-377116"
}

variable "region" {
  default = "us-central1"
}

variable "zone" {
  default = "us-central1-a"
}

variable "sa_name" {
  default = "nginx-vm-sa"
}

variable "sa_display_name" {
  default = "Nginx VM ServiceAccount"
}

variable "vm_name" {
  default = "nginx-web-app"
}

variable "machine_type" {
  default = "e2-medium"
}

variable "boot_image" {
  default = "debian-cloud/debian-11"
}

variable "vpc_network" {
  default = "default"
}
