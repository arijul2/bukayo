# AWS Configuration
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-west-2"
}

variable "aws_access_key_id" {
  description = "AWS Access Key ID (optional if using environment variables)"
  type        = string
  sensitive   = true
  default     = null
}

variable "aws_secret_access_key" {
  description = "AWS Secret Access Key (optional if using environment variables)"
  type        = string
  sensitive   = true
  default     = null
}

# Project Configuration
variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "bukayo"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

# VPC Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.11.0/24", "10.0.12.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.20.0/24"]
}

# Elastic Beanstalk Configuration
variable "solution_stack_name" {
  description = "Elastic Beanstalk solution stack name"
  type        = string
  default     = "64bit Amazon Linux 2023 v4.7.2 running Python 3.11"
}

variable "instance_type" {
  description = "EC2 instance type for Elastic Beanstalk"
  type        = string
  default     = "t3.small"
}

variable "min_size" {
  description = "Minimum number of instances in Auto Scaling Group"
  type        = string
  default     = "1"
}

variable "max_size" {
  description = "Maximum number of instances in Auto Scaling Group"
  type        = string
  default     = "2"
}

# Application Configuration
variable "application_port" {
  description = "Port that the application listens on"
  type        = number
  default     = 8000
}

variable "health_check_path" {
  description = "Health check path for the application"
  type        = string
  default     = "/"
}

# Environment Variables
variable "openai_api_key" {
  description = "OpenAI API key for the application (set via TF_VAR_openai_api_key environment variable)"
  type        = string
  sensitive   = true
  default     = ""
}

variable "dockerhub_username" {
  description = "Docker Hub username for pulling images (set via TF_VAR_dockerhub_username environment variable)"
  type        = string
  default     = ""
}

variable "ssl_certificate_arn" {
  description = "ARN of the SSL certificate from ACM"
  type        = string
  default     = ""
}

# Tags
variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default = {
    Project     = "bukayo"
    Environment = "dev"
    ManagedBy   = "terraform"
  }
}

# Route53 variables for SSL
variable "domain_name" {
  description = "Domain name for SSL certificate"
  type        = string
}

variable "record_name" {
  description = "Subdomain name for SSL certificate"
  type        = string
}
