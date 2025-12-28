
variable "project_id" {
  type        = string
  description = "GCP Project ID"
}

variable "region" {
  type        = string
  description = "GCP region (e.g. asia-southeast1)"
}

variable "name_suffix" {
  type        = string
  description = "Unique suffix for per-participant resources"
}
