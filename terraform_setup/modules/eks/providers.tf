#
# Provider Configuration

variable "aws-region" {}

provider "aws" {
  region = var.aws-region
  access_key = "my-access-key"
  secret_key = "my-secret-key"
}

provider "http" {}
