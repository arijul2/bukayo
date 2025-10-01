# VPC Outputs
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

# Subnet Outputs
output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

# Security Group Outputs
output "eb_security_group_id" {
  description = "ID of the Elastic Beanstalk security group"
  value       = aws_security_group.eb.id
}

# Elastic Beanstalk Outputs
output "eb_application_name" {
  description = "Name of the Elastic Beanstalk application"
  value       = aws_elastic_beanstalk_application.main.name
}

output "eb_environment_name" {
  description = "Name of the Elastic Beanstalk environment"
  value       = aws_elastic_beanstalk_environment.main.name
}

output "eb_environment_id" {
  description = "ID of the Elastic Beanstalk environment"
  value       = aws_elastic_beanstalk_environment.main.id
}

output "eb_environment_url" {
  description = "URL of the Elastic Beanstalk environment"
  value       = aws_elastic_beanstalk_environment.main.endpoint_url
}

output "ssl_domain_url" {
  description = "HTTPS URL for the application"
  value       = "https://${var.record_name}.${var.domain_name}"
}

output "route53_nameservers" {
  description = "Route53 nameservers to configure in GoDaddy"
  value       = aws_route53_zone.hosted_zone.name_servers
}

# IAM Outputs
output "eb_service_role_arn" {
  description = "ARN of the Elastic Beanstalk service role"
  value       = aws_iam_role.eb_service_role.arn
}

output "eb_instance_profile_arn" {
  description = "ARN of the Elastic Beanstalk instance profile"
  value       = aws_iam_instance_profile.eb_instance_profile.arn
}

# Application URL (internal only)
output "application_url" {
  description = "Internal URL to access the application (from within VPC)"
  value       = "http://${aws_elastic_beanstalk_environment.main.endpoint_url}"
}

# Summary
output "deployment_summary" {
  description = "Summary of the deployment"
  value = {
    project_name        = var.project_name
    environment         = var.environment
    region              = var.aws_region
    vpc_id              = aws_vpc.main.id
    eb_environment_name = aws_elastic_beanstalk_environment.main.name
    application_url_http  = "http://${aws_elastic_beanstalk_environment.main.endpoint_url}"
    application_url_https = "https://${var.record_name}.${var.domain_name}"
    domain_name         = "${var.record_name}.${var.domain_name}"
    certificate_arn     = aws_acm_certificate_validation.this.certificate_arn
    note                = "HTTPS configured with SSL certificate"
  }
}
