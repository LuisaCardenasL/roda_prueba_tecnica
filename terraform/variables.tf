variable "gcp_project_id" {
  description = "The GCP project ID to deploy the resources to."
  type        = string
}

variable "gcp_region" {
  description = "The GCP region to deploy the resources to."
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "The name of the Cloud Run service."
  type        = string
  default     = "roda-microservice"
}

variable "repo_name" {
  description = "The name of the Artifact Registry repository."
  type        = string
  default     = "roda-repo"
}
