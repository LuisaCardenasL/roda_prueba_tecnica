terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# Enable necessary APIs
resource "google_project_service" "run_api" {
  service = "run.googleapis.com"
}

resource "google_project_service" "artifactregistry_api" {
  service = "artifactregistry.googleapis.com"
}

# Create an Artifact Registry repository to store the Docker image
resource "google_artifact_registry_repository" "repo" {
  provider      = google
  location      = var.gcp_region
  repository_id = var.repo_name
  format        = "DOCKER"
  depends_on    = [google_project_service.artifactregistry_api]
}

# Deploy the Cloud Run service
resource "google_cloud_run_v2_service" "service" {
  provider   = google
  name       = var.service_name
  location   = var.gcp_region
  depends_on = [google_project_service.run_api]

  template {
    containers {
      image = "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.repo.repository_id}/${var.service_name}:latest"

      # IMPORTANT: These environment variables should be managed securely,
      # for example, using Google Secret Manager. They are hardcoded here
      # for simplicity, but this is not a recommended practice.
      env {
        name  = "PG_HOST"
        value = "your_database_host"
      }
      env {
        name  = "PG_PORT"
        value = "5432"
      }
      env {
        name  = "PG_DB"
        value = "roda"
      }
      env {
        name  = "PG_USER"
        value = "roda"
      }
      env {
        name  = "PG_PASSWORD"
        value = "roda"
      }
      env {
        name  = "PG_SSLMODE"
        value = "disable"
      }
    }
  }
}
