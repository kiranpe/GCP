terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.65.0"
    }

    google-beta = {
      source  = "hashicorp/google-beta"
      version = "3.65.0"
    }

    local = {
      source  = "hashicorp/local"
      version = "2.3.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}
