variable "project_id" {
  default = "k8s-devops-377116"
}

variable "region" {
  default = "us-central1"
}

variable "zone" {
  default = "us-central1-a"
}

variable "sa_id" {
  default = "nginx-vm-sa"
}

variable "sa_display_name" {
  default = "Nginx VM Service Account"
}

variable "image_version" { default = "debian-10" }
variable "image_project" { default = "debian-cloud" }
variable "disk_name" { default = "nginx-app-disk" }
variable "disk_size" { default = "15" }
variable "disk_type" { default = "pd-ssd" }
variable "vm_tpl_name" { default = "nginx-app-tpl" }
variable "vm_name" { default = "nginx-app" }
variable "vm_desc" { default = "This template is used to create nginx app instances." }
variable "vm_machine" { default = "e2-medium" }
variable "vpc_name" { default = "default" }
