terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">=3.5.0"
    }
  }
}

provider "google" {
  credentials = file("/home/kiran/devops/GCP/credentials.json")
  project     = var.projectId
  region      = var.region
}
