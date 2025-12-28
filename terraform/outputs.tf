output "service_account_email" {
  value       = google_service_account.runtime.email
  description = "Deploy Cloud Run with this runtime identity."
}

output "secret_name" {
  value       = google_secret_manager_secret.api_key.secret_id
  description = "Use this in --set-secrets API_KEY=SECRET_NAME:latest"
}

output "api_key_value" {
  value       = random_password.api_key.result
  sensitive   = true
  description = "Use for testing X-API-KEY. (Workshop convenience)"
}
