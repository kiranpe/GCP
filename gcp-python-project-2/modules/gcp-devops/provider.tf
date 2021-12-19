terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">=3.5.0"
    }
    null = {
      source  = "hashicorp/null"
      version = ">=3.0.0"
    }
    local = {
      source  = "hashicorp/local"
      version = ">=2.0.0"
    }
  }
}

provider "google" {
  credentials = file("/home/kiran/devops/GCP/credentials.json")
  project     = var.projectId
  region      = var.region
}
