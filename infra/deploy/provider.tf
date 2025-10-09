# Configure the AWS Provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1"
    }
  }
}

provider "aws" {
  region     = var.aws_region
                      # aws_access_key_id and aws_secret_access_key from terraform.tfvars

  default_tags {
    tags = var.common_tags
  }
}
