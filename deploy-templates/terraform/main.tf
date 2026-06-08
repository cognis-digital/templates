terraform {
  required_version = ">= 1.5"
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
}
provider "aws" { region = var.region }
variable "region" { default = "us-east-1" }
variable "app_name" { default = "cognis-app" }
# Example: containerized service on ECS Fargate (fill in cluster/task as needed).
output "next_steps" { value = "terraform init && terraform apply" }
