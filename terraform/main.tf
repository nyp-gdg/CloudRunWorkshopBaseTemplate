provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  # Keep names short + safe for service account constraints (<=30 chars, lowercase).
  short_suffix = substr(lower(var.name_suffix), 0, 16)

  # Service account id must start with a letter and be 6-30 chars.
  sa_account_id = substr("cr-cpn-${local.short_suffix}", 0, 30)

  # Secret id can be longer, but we keep it tidy.
  secret_id = substr("coupon-api-key-${local.short_suffix}", 0, 64)
}

resource "google_service_account" "runtime" {
  account_id   = local.sa_account_id
  display_name = "Cloud Run Coupon SA (${local.short_suffix})"
}

resource "random_password" "api_key" {
  length  = 32
  special = false
}

resource "google_secret_manager_secret" "api_key" {
  secret_id = local.secret_id

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "api_key_ver" {
  secret      = google_secret_manager_secret.api_key.id
  secret_data = random_password.api_key.result
}

resource "google_secret_manager_secret_iam_member" "allow_runtime" {
  secret_id = google_secret_manager_secret.api_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.runtime.email}"
}
