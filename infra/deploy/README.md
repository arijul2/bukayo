# Bukayo Infrastructure Deployment

This Terraform module creates a simplified AWS Elastic Beanstalk environment for the Bukayo project.

## Architecture

The infrastructure includes:
- VPC with private subnets across 2 availability zones (no public subnets to avoid costs)
- Elastic Beanstalk environment with Classic Load Balancer in private subnets
- Security groups for Elastic Beanstalk
- IAM roles and policies for Elastic Beanstalk service and EC2 instances
- **Note**: This is an internal-only setup (no internet gateway) to minimize costs

## Prerequisites

1. **Terraform**: Install Terraform >= 1.0
2. **AWS CLI**: Install and configure AWS CLI (optional, but recommended)
3. **AWS Credentials**: You'll need AWS Access Key ID and Secret Access Key

## Quick Start

1. **Set up AWS credentials** (choose one method):

   **Method 1: Environment Variables**
   ```bash
   export AWS_ACCESS_KEY_ID="your-access-key-id"
   export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
   export AWS_DEFAULT_REGION="us-west-2"
   ```

   **Method 2: terraform.tfvars file**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your values
   ```

2. **Initialize Terraform**:
   ```bash
   terraform init
   ```

3. **Plan the deployment**:
   ```bash
   terraform plan
   ```

4. **Deploy the infrastructure**:
   ```bash
   terraform apply
   ```

5. **Get the application URL**:
   ```bash
   terraform output application_url
   ```

## Configuration

### Required Variables

- `aws_region`: AWS region for resources
- `aws_access_key_id`: AWS Access Key ID
- `aws_secret_access_key`: AWS Secret Access Key

### Optional Variables

- `project_name`: Name of the project (default: "bukayo")
- `environment`: Environment name (default: "dev")
- `vpc_cidr`: CIDR block for VPC (default: "10.0.0.0/16")
- `instance_type`: EC2 instance type (default: "t3.small")
- `min_size`: Minimum instances (default: "1")
- `max_size`: Maximum instances (default: "3")

## Outputs

After deployment, you'll get:
- `application_url`: Internal URL to access your application (from within VPC)
- `eb_environment_name`: Name of the Elastic Beanstalk environment
- `vpc_id`: ID of the VPC
- `eb_security_group_id`: Security group for the application
- And many more useful outputs

## Deployment Process

1. **VPC Setup**: Creates VPC with private subnets only
2. **Security Groups**: Configures EB security groups
3. **Load Balancer**: Sets up Classic Load Balancer (internal)
4. **IAM Roles**: Creates service roles for Elastic Beanstalk
5. **Elastic Beanstalk**: Deploys the EB application and environment

## Security

- Elastic Beanstalk instances are in private subnets only
- No internet gateway (internal-only access)
- Security groups restrict traffic to within VPC
- IAM roles follow least privilege principle

## Cost Optimization

- Uses t3.micro instances by default (free tier eligible)
- Auto Scaling Group with 1-3 instances
- Classic Load Balancer (lower cost than ALB)
- No Internet Gateway (saves ~$18/month)
- No NAT Gateway (saves ~$45/month)

## Cleanup

To destroy the infrastructure:
```bash
terraform destroy
```

## Troubleshooting

1. **Permission Issues**: Ensure your AWS credentials have sufficient permissions
2. **Region Issues**: Make sure the region supports all required services
3. **Resource Limits**: Check AWS service limits in your account

## Next Steps

After deployment:
1. Deploy your application to Elastic Beanstalk
2. Configure custom domain (optional)
3. Set up SSL/TLS certificates (optional)
4. Configure monitoring and logging


## Running Docker Containers in Dev

docker-compose -f docker-compose-dev.yml --env-file ./.env.dev up --build